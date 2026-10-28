#!/usr/bin/env python3
"""Convert a campaign's raw NotebookLM briefing into a 2-page brand PDF.

Pipeline
--------
raw-briefing.md  ->  markdown parse  ->  template slots  ->  Jinja2 merge into
static/brand/templates/executive-briefing-template.html  ->  Chromium print to
PDF (A4, 2 pages)  ->  palette + layout QA  ->  brand-qa.json

Layout contract (fixed, two pages):
    page 1  Executive Summary + 4 Pillars
    page 2  Field Evidence + Governance + Action Steps + decision gate

Content is *selected from the source*, never invented: every string in the PDF
is a substring of (or derived from) the source sentences, except brand chrome
(labels, kickers, footer, eyebrow date). When a slot has no matching source
section it is omitted rather than filled.

Usage
-----
    uv run python scripts/brand_briefing.py
    uv run python scripts/brand_briefing.py --campaign artifacts/campaigns/<slug>
    uv run python scripts/brand_briefing.py --campaign <slug>/notebooklm/raw-briefing.md

Exit codes: 0 = PDF built and all QA gates passed, 1 = QA failed, 2 = setup error.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import html as html_lib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import jinja2
import numpy as np
import pymupdf
from PIL import Image

REPO = Path(__file__).resolve().parents[1]
TEMPLATE = REPO / "static" / "brand" / "templates" / "executive-briefing-template.html"
LOGO = REPO / "brand" / "logo" / "logo-full.png"
TOKENS = REPO / "brand" / "tokens" / "brand-tokens.json"
PALETTE_GATE = (
    REPO / ".agents" / "skills" / "ls-visual-storytelling" / "scripts" / "check_brand_palette.py"
)
CAMPAIGNS = REPO / "artifacts" / "campaigns"

SOURCE_REL = Path("notebooklm") / "raw-briefing.md"
PDF_REL = Path("open-design") / "executive-briefing-branded.pdf"
HTML_REL = Path("open-design") / "executive-briefing.html"
QA_REL = Path("qa") / "brand-briefing"

TOLERANCE = 3.0
DPI = 300
MIN_FIT = 0.70
FIT_STEP = 0.02

# Artwork lockup: 44mm displayed artwork width (brand minimum is 30mm),
# 1x 'L' clear space. The 'L' cap height is 0.1887 x artwork width in
# logo-full.png, i.e. 8.3mm at 44mm, so 9mm satisfies the clear-space rule.
LOGO_ART_WIDTH_MM = 44.0
LOGO_CAP_RATIO = 0.1887

# Per-slot text budgets (characters, cut on sentence boundaries). Sized so a
# typical NotebookLM briefing holds the 2-page grid at the full brand type scale.
BUDGET = {
    "summary": 400,
    "pillar": 125,
    "evidence_intro": 165,
    "evidence_item": 112,
    "callout": 175,
    "mandate_intro": 190,
    "mandate": 110,
    "step": 155,
    "gate": 200,
}

EVIDENCE_RE = re.compile(r"evidenc|validat|field|cases? stud|proof|deploy", re.I)
GOVERNANCE_RE = re.compile(r"governance|compliance|regulat|policy|quality|assurance", re.I)
ACTION_RE = re.compile(r"action|next step|recommend|decision|implication", re.I)
TAKEAWAY_RE = re.compile(r"summary|takeaway|key point|conclusion", re.I)
GAP_RE = re.compile(r"\bgap|unverified|missing|risk|limitation|caveat|uncertain|unknown", re.I)
CALLOUT_RE = re.compile(r"so what|matters|implication|\bmeans\b|significan", re.I)

# Canonical LightSpeed scale facts. Labels are the company's own vocabulary
# (company-registry.yaml); values are read from the source text, never assumed.
METRIC_FACTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(\d{1,3})\s+(?:AI\s+)?[Aa]gents\b"), "AI agents in operation"),
    (
        re.compile(r"(\d{1,3})\s+(?:distinct\s+|operational\s+)*departments\b", re.I),
        "Operating departments",
    ),
    (re.compile(r"(\d{1,3})[-\s]tier\s+(?:HITL|Human)", re.I), "HITL approval tiers"),
    (re.compile(r"(\d{1,3})[-\s]gate\s+(?:CI|Continuous)", re.I), "CI quality gates"),
]
GENERIC_METRIC_RE = re.compile(
    r"(?<![\d.])(\d{1,3})\s+((?:[A-Za-z][A-Za-z-]{2,}\s+){0,2}[A-Za-z][A-Za-z-]{2,})"
)


# ── markdown parsing ──────────────────────────────────────────────────────────


@dataclass
class Block:
    kind: str  # "para" | "bullets" | "table"
    text: str = ""
    items: list[str] = field(default_factory=list)
    rows: list[list[str]] = field(default_factory=list)


@dataclass
class Section:
    level: int
    heading: str
    blocks: list[Block] = field(default_factory=list)
    raw: list[str] = field(default_factory=list)  # source lines, for chip extraction


@dataclass
class Parsed:
    title: str
    sections: list[Section]

    def text(self) -> str:
        parts = [self.title]
        for section in self.sections:
            parts.append(section.heading)
            for block in section.blocks:
                parts.append(block.text)
                parts.extend(block.items)
                for row in block.rows:
                    parts.extend(row)
        return " ".join(p for p in parts if p)


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
BULLET_RE = re.compile(r"^\s*(?:[*\-+]|\d+[.)])\s+(.*)$")
RULE_RE = re.compile(r"^\|?[\s:|-]{3,}$")


def clean(text: str) -> str:
    """Strip markdown syntax and normalise whitespace; keeps the words intact."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links -> label
    text = re.sub(r"\\(.)", r"\1", text)  # markdown escapes
    text = re.sub(r"\*\*|__|~~|`", "", text)  # emphasis / code marks
    text = re.sub(r"(?<!\w)[*_]|[*_](?!\w)", "", text)  # stray * / _ emphasis
    text = html_lib.unescape(text)
    text = text.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    """Split prose on sentence terminators that are followed by a new sentence."""
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(\u2014])", text.strip())
    return [p.strip() for p in parts if p.strip()]


def take(text: str, limit: int) -> str:
    """Whole sentences up to `limit` characters. Never truncates mid-sentence."""
    sentences = split_sentences(text)
    if not sentences:
        return ""
    out: list[str] = []
    for sentence in sentences:
        candidate = " ".join([*out, sentence])
        if out and len(candidate) > limit:
            break
        out.append(sentence)
        if len(" ".join(out)) >= limit:
            break
    chosen = " ".join(out)
    if len(chosen) > limit and len(sentences) == 1:
        # A single sentence that only just overruns reads better whole than
        # ellipsised; beyond that, cut on a clause boundary, then on a word.
        if len(chosen) <= limit * 1.25:
            return chosen
        window = chosen[:limit]
        for separator in ("; ", ", ", " - ", " "):
            if separator not in window:
                continue
            cut = window.rsplit(separator, 1)[0].rstrip(" ,;:")
            if len(cut) > limit * 0.55:
                # Never leave an unclosed parenthetical hanging.
                if cut.count("(") > cut.count(")"):
                    cut = cut[: cut.rfind("(")].rstrip(" ,;:")
                return cut + "\u2026"
        return window.rstrip() + "\u2026"
    return chosen


def make_block(lines: list[str]) -> Block | None:
    if all(line.strip().startswith("|") for line in lines):
        rows = []
        for line in lines:
            if RULE_RE.match(line.strip()):
                continue
            cells = [clean(c) for c in line.strip().strip("|").split("|")]
            if any(cells):
                rows.append(cells)
        return Block("table", rows=rows) if rows else None
    if all(BULLET_RE.match(line) for line in lines):
        items = [clean(BULLET_RE.match(line).group(1)) for line in lines]  # type: ignore[union-attr]
        items = [i for i in items if i]
        return Block("bullets", items=items) if items else None
    text = clean(" ".join(lines))
    return Block("para", text=text) if text else None


def parse_markdown(raw: str) -> Parsed:
    title = ""
    sections: list[Section] = []
    current: Section | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer
        if buffer and current is not None:
            block = make_block(buffer)
            if block is not None:
                current.blocks.append(block)
        buffer = []

    for line in raw.splitlines():
        heading = HEADING_RE.match(line)
        if heading:
            flush()
            level = len(heading.group(1))
            text = clean(heading.group(2))
            if level == 1 and not title and not sections:
                title = text
                current = None
                continue
            current = Section(level, text)
            sections.append(current)
            continue
        if not line.strip():
            flush()
            continue
        buffer.append(line)
        if current is not None:
            current.raw.append(line)
    flush()
    return Parsed(title, sections)


def paragraphs(section: Section) -> list[str]:
    return [b.text for b in section.blocks if b.kind == "para" and b.text]


def lead_in(section: Section) -> str:
    """The paragraph that introduces this section's bullet list.

    For a bullet-heavy briefing the sentence immediately above the list is the
    one that frames it, so it makes the better column intro than the opening
    paragraph (which usually restates the section heading).
    """
    index = next((i for i, b in enumerate(section.blocks) if b.kind == "bullets"), None)
    if index is None:
        paras = paragraphs(section)
        return paras[0] if paras else ""
    above = [b.text for b in section.blocks[:index] if b.kind == "para" and b.text]
    if above:
        return above[-1]
    paras = paragraphs(section)
    return paras[0] if paras else ""


def bullets(section: Section) -> list[str]:
    out: list[str] = []
    for block in section.blocks:
        if block.kind == "bullets":
            out.extend(block.items)
    return out


def split_label(text: str) -> tuple[str, str]:
    """`Inventory Control: real-time tracking` -> ('Inventory Control', 'real-time ...')."""
    match = re.match(r"^([^:.]{3,60}):\s*(.+)$", text)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    if len(text) <= 70:
        return text, ""
    sentence = split_sentences(text)
    if len(sentence) > 1:
        return sentence[0].rstrip("."), " ".join(sentence[1:])
    return text[:68].rstrip() + "\u2026", text


# ── slot building ─────────────────────────────────────────────────────────────


def strip_numbering(heading: str) -> str:
    return re.sub(r"^\d+\s*[.)]\s*", "", heading).strip()


def pick_section(sections: list[Section], pattern: re.Pattern[str]) -> Section | None:
    for section in sections:
        if pattern.search(section.heading):
            return section
    return None


def build_metrics(full_text: str) -> list[dict[str, str]]:
    metrics: list[dict[str, str]] = []
    seen_values: set[str] = set()
    for pattern, label in METRIC_FACTS:
        match = pattern.search(full_text)
        if not match:
            continue
        value = match.group(1)
        if value in seen_values:
            continue
        seen_values.add(value)
        metrics.append({"value": value, "label": label, "source": match.group(0)})
    if len(metrics) < 4:
        for match in GENERIC_METRIC_RE.finditer(full_text):
            value, phrase = match.group(1), match.group(2).strip()
            if len(metrics) >= 4:
                break
            if value in seen_values or phrase.lower().startswith(("the ", "and ", "of ")):
                continue
            if re.fullmatch(r"(19|20)\d{2}", value):  # a year, not a metric
                continue
            seen_values.add(value)
            metrics.append({"value": value, "label": phrase.capitalize(), "source": match.group(0)})
    return metrics[:4]


def build_pillars(sections: list[Section], skip: set[str]) -> list[dict[str, Any]]:
    """The four headline themes: the shallowest sections, takeaway sections last."""
    if not sections:
        return []
    level = min(s.level for s in sections)
    pool = [s for s in sections if s.level == level]
    # Prefer substantive sections, but backfill with takeaway sections so the
    # page still carries four pillars.
    pool = [s for s in pool if not TAKEAWAY_RE.search(s.heading)] + [
        s for s in pool if TAKEAWAY_RE.search(s.heading)
    ]

    pillars = []
    for section in pool[:4]:
        bodies = [p for p in paragraphs(section) if p not in skip] or paragraphs(section)
        body_source = bodies[0] if bodies else ""
        body = take(body_source, BUDGET["pillar"]) if body_source else ""
        if not body:
            body = take(" ".join(bullets(section)[:1]), BUDGET["pillar"])
        if not body:
            continue
        chips: list[str] = []
        prose = "\n".join(line for line in section.raw if not line.lstrip().startswith("|"))
        for token in re.findall(r"\*\*(.+?)\*\*|`([^`]+)`", prose):
            chip = clean(token[0] or token[1]).rstrip(":;,")
            if 2 < len(chip) <= 26 and "|" not in chip and chip not in chips:
                chips.append(chip)
        pillars.append(
            {"heading": strip_numbering(section.heading), "body": body, "chips": chips[:3]}
        )
    return pillars


def build_evidence(sections: list[Section]) -> dict[str, Any] | None:
    section = pick_section(sections, EVIDENCE_RE)
    if section is None:
        return None
    items = []
    for bullet in bullets(section):
        heading, body = split_label(bullet)
        items.append({"heading": heading, "body": take(body or heading, BUDGET["evidence_item"])})
    if not items:
        for sentence in split_sentences(" ".join(paragraphs(section)))[1:4]:
            items.append({"heading": "Evidence", "body": take(sentence, BUDGET["evidence_item"])})
    if not items:
        return None

    intro = take(lead_in(section), BUDGET["evidence_intro"])
    callout = None
    for paragraph in paragraphs(section):
        if CALLOUT_RE.search(paragraph) and paragraph != lead_in(section):
            callout = {"label": "Why it matters", "body": take(paragraph, BUDGET["callout"])}
            break
    return {
        "heading": strip_numbering(section.heading),
        "kicker": "Field proof",
        "intro": intro,
        "cards": items[:3],
        "columns": min(len(items), 3) or 1,
        "callout": callout,
    }


def build_mandates(sections: list[Section]) -> dict[str, Any] | None:
    section = pick_section(sections, GOVERNANCE_RE)
    if section is None:
        return None
    mandates = []
    for bullet in bullets(section):
        label, body = split_label(bullet)
        mandates.append(
            {"label": label.upper()[:34], "body": take(body or label, BUDGET["mandate"])}
        )
    if not mandates:
        return None
    return {
        "heading": strip_numbering(section.heading),
        "kicker": "Governance",
        "intro": take(lead_in(section), BUDGET["mandate_intro"]),
        "items": mandates[:3],
    }


def build_steps(
    sections: list[Section], used: set[int]
) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    """Action steps: an explicit action section first, else the closing takeaways."""
    section = pick_section(sections, ACTION_RE)
    if section is None or id(section) in used:
        section = None
        for candidate in reversed(sections):
            if id(candidate) not in used and TAKEAWAY_RE.search(candidate.heading):
                section = candidate
                break
    if section is None:
        return None, []
    steps = []
    for bullet in bullets(section):
        heading, body = split_label(bullet)
        steps.append({"heading": heading, "body": take(body or heading, BUDGET["step"])})
    if not steps:
        return None, []
    return {"heading": strip_numbering(section.heading), "kicker": "Decision required"}, steps[:3]


def build_gate(sections: list[Section], used: set[int]) -> dict[str, str] | None:
    """Red callout: the source's own unverified/open items, never invented."""
    for section in sections:
        if id(section) in used or not GAP_RE.search(section.heading):
            continue
        candidates = bullets(section) or paragraphs(section)
        picked = []
        for candidate in candidates[:2]:
            label, body = split_label(candidate)
            text = (
                f"{label}: {take(body, BUDGET['gate'] // 2)}"
                if body
                else take(candidate, BUDGET["gate"] // 2)
            )
            picked.append(text)
        if picked:
            return {"label": "Decision gate", "body": " ".join(picked)}
    return None


def build_slots(parsed: Parsed, when: datetime) -> dict[str, Any]:
    sections = parsed.sections
    full_text = parsed.text()

    title = (
        re.sub(r"^(executive\s+briefing|briefing)\s*[:\u2014-]\s*", "", parsed.title, flags=re.I)
        .strip()
        .rstrip(":")
    )

    first = sections[0] if sections else None
    first_paragraphs = paragraphs(first) if first else []
    subtitle = ""
    summary_paragraphs: list[str] = []
    if first_paragraphs:
        sentences = split_sentences(first_paragraphs[0])
        subtitle = sentences[0] if sentences else ""
        remainder = " ".join(sentences[1:])
        rest = " ".join(first_paragraphs[1:])
        # The dek sentence is spent on the masthead; the lede continues from it.
        body = " ".join(p for p in (remainder, rest) if p)
        summary_paragraphs = [take(body, BUDGET["summary"])] if body else []

    # Paragraphs already spent on the masthead / summary must not reappear as a
    # pillar body.
    consumed: set[str] = set()
    if first_paragraphs:
        consumed.add(first_paragraphs[0])
        summary_text = " ".join(summary_paragraphs)
        consumed |= {p for p in first_paragraphs if p and p in summary_text}
    pillars = build_pillars(sections, consumed)

    evidence = build_evidence(sections)
    mandates = build_mandates(sections)

    used: set[int] = set()
    for section in sections:
        if (
            evidence
            and section.heading == evidence["heading"]
            and EVIDENCE_RE.search(section.heading)
        ):
            used.add(id(section))
        if mandates and section.heading == mandates["heading"]:
            used.add(id(section))
    steps_meta, steps = build_steps(sections, used)
    gate = build_gate(sections, used)

    return {
        "title": title or "Executive Briefing",
        "eyebrow": f"Executive Briefing \u2014 {when.strftime('%B %Y')}",
        "subtitle": subtitle,
        "meta_description": f"{title} \u2014 LightSpeed Holdings Limited executive briefing.",
        "metrics": build_metrics(full_text),
        "summary": {
            "heading": "Executive Summary",
            "kicker": "The position",
            "paragraphs": summary_paragraphs,
        },
        "pillars": pillars,
        "pillars_heading": "Four Core Pillars" if len(pillars) == 4 else "Core Pillars",
        "pillars_kicker": "How it holds up",
        "evidence": evidence,
        "mandates": mandates["items"] if mandates else [],
        "mandates_heading": mandates["heading"] if mandates else "",
        "mandates_kicker": mandates["kicker"] if mandates else "",
        "mandates_intro": mandates["intro"] if mandates else "",
        "steps": steps,
        "steps_heading": steps_meta["heading"] if steps_meta else "",
        "steps_kicker": steps_meta["kicker"] if steps_meta else "",
        "gate": gate,
        "rail_right": "Evidence \u00b7 Governance \u00b7 Action",
    }


# ── logo geometry ─────────────────────────────────────────────────────────────


def artwork_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    """Bounding box of the artwork, measured against the plate colour at (0, 0)."""
    rgb = np.asarray(image.convert("RGBA"))[:, :, :3].astype(np.int16)
    plate = rgb[0, 0]
    delta = np.abs(rgb - plate).sum(axis=2)
    rows = np.where(delta.max(axis=1) > 18)[0]
    cols = np.where(delta.max(axis=0) > 18)[0]
    if rows.size == 0 or cols.size == 0:
        return 0, 0, image.width, image.height
    return int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1


def logo_geometry(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise SystemExit(f"ERROR: logo not found: {path}")
    with Image.open(path) as image:
        image = image.convert("RGBA")
        width, height = image.size
        x0, y0, x1, y1 = artwork_bbox(image)
    art_w, art_h = x1 - x0, y1 - y0
    scale = LOGO_ART_WIDTH_MM / art_w
    clear = max(9.0, round(LOGO_ART_WIDTH_MM * LOGO_CAP_RATIO * 1.05, 1))
    return {
        "src": "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii"),
        "box_w": f"{LOGO_ART_WIDTH_MM:.2f}mm",
        "box_h": f"{art_h * scale:.2f}mm",
        "img_w": f"{width * scale:.2f}mm",
        "img_h": f"{height * scale:.2f}mm",
        "off_x": f"{-x0 * scale:.2f}mm",
        "off_y": f"{-y0 * scale:.2f}mm",
        "clear_space": f"{clear:.1f}mm",
    }


# ── rendering ─────────────────────────────────────────────────────────────────


def render_html(slots: dict[str, Any], logo: dict[str, str], *, fit: float, measure: bool) -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    env = jinja2.Environment(autoescape=jinja2.select_autoescape(["html"]), trim_blocks=True)
    return env.from_string(template).render(fit=f"{fit:.2f}", measure=measure, logo=logo, **slots)


def find_browser() -> str:
    candidates = [os.environ.get("BROWSER_BIN", "")]
    candidates += [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    for name in ("chrome", "google-chrome", "chromium", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    raise SystemExit("ERROR: no Chromium-based browser found; set BROWSER_BIN to enable PDF print.")


def print_pdf(browser: str, html_path: Path, pdf_path: Path) -> None:
    pdf_path.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(prefix="ls-briefing-") as profile:
        command = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-extensions",
            "--disable-sync",
            "--disable-background-networking",
            "--disable-lcd-text",
            "--font-render-hinting=none",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=5000",
            "--no-pdf-header-footer",
            f"--user-data-dir={profile}",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ]
        proc = subprocess.run(command, capture_output=True, text=True, timeout=180, check=False)
    if not pdf_path.is_file() or pdf_path.stat().st_size == 0:
        detail = (proc.stderr or proc.stdout or "").strip()[:600]
        raise SystemExit(f"ERROR: PDF print failed ({pdf_path}).\n{detail}")


def page_count(pdf_path: Path) -> int:
    with pymupdf.open(pdf_path) as doc:
        return doc.page_count


def build_pdf(slots: dict[str, Any], logo: dict[str, str], out_html: Path, out_pdf: Path) -> float:
    """Render, shrinking the type scale only when content would spill to page 3."""
    browser = find_browser()
    fit = 1.0
    chosen: float | None = None
    while fit >= MIN_FIT - 1e-9:
        out_html.write_text(render_html(slots, logo, fit=fit, measure=True), encoding="utf-8")
        print_pdf(browser, out_html, out_pdf)
        sheets = page_count(out_pdf)
        print(f"  fit {fit:.2f}: {sheets} sheet(s)")
        if sheets <= 2:
            chosen = fit
            break
        fit = round(fit - FIT_STEP, 2)
    if chosen is None:
        chosen = MIN_FIT
        print(
            f"  WARNING: content still overflowed at fit {MIN_FIT:.2f}; "
            "page 2 will clip. Trim the source briefing."
        )

    out_html.write_text(render_html(slots, logo, fit=chosen, measure=False), encoding="utf-8")
    print_pdf(browser, out_html, out_pdf)
    if page_count(out_pdf) != 2:
        raise SystemExit("ERROR: final render is not 2 pages.")
    return chosen


# ── QA ────────────────────────────────────────────────────────────────────────


def brand_hexes() -> set[str]:
    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    return {
        spec["value"].upper()
        for spec in data["color"].values()
        if str(spec.get("value", "")).startswith("#")
    }


def rasterise(pdf_path: Path, qa_dir: Path, dpi: int) -> tuple[list[Path], str]:
    """Rasterise with anti-aliasing off so glyph edges stay exact token colours.

    With AA on, every anti-aliased glyph edge is an off-palette blend and the
    palette gate fails for a reason unrelated to the artifact's colours.
    """
    for old in qa_dir.glob("page-*.png"):
        old.unlink()
    prefix = qa_dir / "page"
    poppler = shutil.which("pdftoppm")
    if poppler:
        subprocess.run(
            [
                poppler,
                "-r",
                str(dpi),
                "-png",
                "-aa",
                "no",
                "-aaVector",
                "no",
                str(pdf_path),
                str(prefix),
            ],
            capture_output=True,
            check=True,
        )
        return sorted(qa_dir.glob("page-*.png")), "pdftoppm (anti-aliasing off)"
    with pymupdf.open(pdf_path) as doc:
        pages = []
        for index, page in enumerate(doc, start=1):
            path = qa_dir / f"page-{index}.png"
            page.get_pixmap(dpi=dpi).save(path)
            pages.append(path)
    return pages, "PyMuPDF (anti-aliasing on; palette % may read high)"


def run_qa(
    pdf_path: Path, html_path: Path, qa_dir: Path, title: str, tolerance: float, dpi: int
) -> dict[str, Any]:
    checks: dict[str, Any] = {}

    with pymupdf.open(pdf_path) as doc:
        checks["page_count"] = {"value": doc.page_count, "pass": doc.page_count == 2}
        sizes = [(round(p.rect.width, 1), round(p.rect.height, 1)) for p in doc]
        checks["a4"] = {
            "value": sizes,
            "pass": all(abs(w - 595.3) < 1.6 and abs(h - 841.9) < 1.6 for w, h in sizes),
        }
        text = "\n".join(p.get_text() for p in doc)
    probe = " ".join(title.split()[:4])
    checks["title_in_pdf"] = {
        "value": probe,
        "pass": probe.lower() in " ".join(text.split()).lower(),
    }
    checks["text_extracted"] = {"value": len(text), "pass": len(text) > 1200}

    gate_script = PALETTE_GATE
    if not gate_script.is_file():
        raise SystemExit(f"ERROR: palette gate not found: {gate_script}")
    pages = []
    palette_results = []
    pages, rasteriser = rasterise(pdf_path, qa_dir, dpi)
    checks["rasteriser"] = {"value": rasteriser, "pass": True}
    for page in pages:
        proc = subprocess.run(
            [
                sys.executable,
                str(gate_script),
                str(page),
                "--tolerance",
                str(tolerance),
                "--verbose",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        output = (proc.stdout + proc.stderr).strip().splitlines()
        palette_results.append(
            {
                "page": page.name,
                "rc": proc.returncode,
                "output": output[-1] if output else "",
                "detail": output[0] if len(output) > 1 else "",
            }
        )
    checks["palette"] = {
        "value": palette_results,
        "tolerance_pct": tolerance,
        "pass": bool(palette_results) and all(r["rc"] == 0 for r in palette_results),
    }

    tokens = brand_hexes()
    markup = html_path.read_text(encoding="utf-8")
    # Comments describe colours ("plate is opaque #02062F"); they do not declare
    # them, so only real declarations are gated.
    markup = re.sub(r"/\*.*?\*/", "", markup, flags=re.S)
    declared = {("#" + m).upper() for m in re.findall(r"#([0-9A-Fa-f]{6})\b", markup)}
    off = sorted(declared - tokens)
    checks["css_colours"] = {"value": off, "pass": not off}

    return {"checks": checks, "pass": all(c["pass"] for c in checks.values())}


# ── CLI ───────────────────────────────────────────────────────────────────────


def resolve_campaign(raw: str | None) -> Path:
    if raw:
        path = Path(raw).expanduser()
        if not path.is_absolute():
            path = (REPO / path).resolve()
        if path.is_file():
            path = path.parent.parent
        if not (path / SOURCE_REL).is_file():
            raise SystemExit(f"ERROR: no {SOURCE_REL.as_posix()} under {path}")
        return path
    if not CAMPAIGNS.is_dir():
        raise SystemExit(f"ERROR: campaign root not found: {CAMPAIGNS}")
    candidates = [p for p in CAMPAIGNS.iterdir() if p.is_dir() and (p / SOURCE_REL).is_file()]
    if not candidates:
        raise SystemExit(f"ERROR: no campaign under {CAMPAIGNS} has {SOURCE_REL.as_posix()}")
    return max(candidates, key=lambda p: (p.name, p.stat().st_mtime))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert a campaign's raw NotebookLM briefing into a branded 2-page PDF."
    )
    parser.add_argument("--campaign", help="campaign directory (or its raw-briefing.md path)")
    parser.add_argument(
        "campaign_path",
        nargs="?",
        help="campaign directory, as a positional shorthand for --campaign",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=TOLERANCE,
        help=f"palette off-palette tolerance in percent (default {TOLERANCE:g})",
    )
    parser.add_argument("--dpi", type=int, default=DPI, help=f"QA raster DPI (default {DPI})")
    args = parser.parse_args(argv)

    campaign = resolve_campaign(args.campaign or args.campaign_path)
    source = campaign / SOURCE_REL
    out_pdf = campaign / PDF_REL
    out_html = campaign / HTML_REL
    qa_dir = campaign / QA_REL
    qa_dir.mkdir(parents=True, exist_ok=True)
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    raw = source.read_text(encoding="utf-8")
    when = datetime.now()
    print(f"campaign : {campaign}")
    print(f"source   : {source} ({len(raw):,} chars)")

    parsed = parse_markdown(raw)
    slots = build_slots(parsed, when)
    print(f"title    : {slots['title']}")
    print(
        f"slots    : {len(slots['metrics'])} metrics, {len(slots['pillars'])} pillars, "
        f"{len(slots['steps'])} steps, gate={'yes' if slots['gate'] else 'no'}"
    )

    logo = logo_geometry(LOGO)
    fit = build_pdf(slots, logo, out_html, out_pdf)
    if fit < 1.0:
        print(f"  NOTE: type scale reduced to {fit:.2f} to hold the 2-page grid.")

    report = run_qa(out_pdf, out_html, qa_dir, slots["title"], args.tolerance, args.dpi)
    report.update(
        {
            "campaign": campaign.name,
            "source": str(source.relative_to(REPO)),
            "source_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            "generated": when.isoformat(timespec="seconds"),
            "pdf": str(out_pdf.relative_to(REPO)),
            "html": str(out_html.relative_to(REPO)),
            "fit": fit,
            "metrics": [{k: v for k, v in m.items()} for m in slots["metrics"]],
        }
    )
    report_path = qa_dir / "brand-qa.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\nQA gates")
    for name, check in report["checks"].items():
        status = "PASS" if check["pass"] else "FAIL"
        if name == "palette":
            print(f"  {name:<14} {status}")
            for row in check["value"]:
                print(f"                 {row['page']}: {row['output']}")
        elif name == "css_colours":
            print(f"  {name:<14} {status} (off-palette: {check['value'] or 'none'})")
        else:
            print(f"  {name:<14} {status} ({check['value']})")

    size_kb = out_pdf.stat().st_size / 1024
    verdict = "PASS" if report["pass"] else "FAIL"
    print("\n" + "=" * 62)
    print("  BRAND BRIEFING READY" if report["pass"] else "  BRAND BRIEFING FAILED")
    print("=" * 62)
    print(f"  PDF      : {out_pdf}")
    print(f"  Pages    : {page_count(out_pdf)} (A4)  {size_kb:,.0f} KB")
    print("  Layout   : page 1 summary + pillars, page 2 evidence + action")
    print(f"  Palette  : {verdict} (tolerance {args.tolerance:g}%)")
    print(f"  QA report: {report_path}")
    print(f"STATUS: {'OK' if report['pass'] else 'FAILED'}")
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
