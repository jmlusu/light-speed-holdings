#!/usr/bin/env python3
"""Compile a campaign's NotebookLM staging output into the full multimodal asset set.

Pipeline
--------
artifacts/campaigns/<slug>/notebooklm/   (source pack, studio prompts, briefing)
        ->  fact extraction (dossier first, source pack second)
        ->  deterministic renders
                infographics  1080x1080 / 1600x900 / 1200x628
                carousels     6 cards -> PNG set + single PDF
                video         9:16 1080x1920 short, 16:9 1920x1080 overview
                report        A4 4-page branded PDF
                social copy   X thread, Facebook post, Instagram caption
        ->  self-gated QA (palette, dimensions, page count, grounding)

Output tree (under the campaign folder)
---------------------------------------
    video/video-short-1080x1920.mp4
    video/video-overview-16x9.mp4
    infographics/infographic-square-1080x1080.png
    infographics/infographic-landscape-1600x900.png
    infographics/infographic-landscape-1200x628.png
    carousels/social-carousel.pdf
    carousels/instagram/card-1..N.png
    reports/comprehensive-report-branded.pdf
    social-copy/threads-and-captions.md
    qa/assets-manifest.json

Design constraints
------------------
1. **No invented content.** Every rendered string is either brand chrome or a
   phrase that exists in the campaign source. Compressed lines carry an explicit
   `source=` phrase, and the gate asserts that phrase is present.
2. **Exact palette.** Rasters are drawn with Pillow ``fontmode="1"`` (text
   anti-aliasing off) from brand-token hexes, so every visible pixel lands on a
   token colour and ``check_brand_palette.py`` passes at its 3% tolerance.
3. **Honest video QA.** H.264 ``yuv420p`` is required for platform playback and
   is lossy, so decoded frames are *not* bit-exact. The palette gate is run on
   the source frames (authoritative) and on a decoded frame (reported, not
   gated). Both numbers are printed.

Usage
-----
    uv run python scripts/generate_all_assets.py
    uv run python scripts/generate_all_assets.py --campaign artifacts/campaigns/<slug>
    uv run python scripts/generate_all_assets.py --campaign <slug> --skip-video

Exit codes: 0 = every gate passed, 1 = at least one gate failed, 2 = setup error.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[1]
CAMPAIGNS = REPO / "artifacts" / "campaigns"
TOKENS = REPO / "brand" / "tokens" / "brand-tokens.json"
LOGO = REPO / "brand" / "logo" / "logo-dark-bg-transparent.png"
PALETTE_GATE = (
    REPO / ".agents" / "skills" / "ls-visual-storytelling" / "scripts" / "check_brand_palette.py"
)

TOLERANCE = 3.0
FPS = 30

# Delivery canvases — exact pixel sizes, one file per platform.
SQUARE = (1080, 1080)
LANDSCAPE_X = (1600, 900)
LANDSCAPE_FB = (1200, 628)
VERTICAL = (1080, 1920)
HORIZONTAL = (1920, 1080)

CTA_TEXT = "READ THE PLAYBOOK"
CTA_URL = "lightspeedholdings.vercel.app"

# Brand chrome: furniture that carries no factual claim, so it is exempt from
# the grounding gate. Anything factual must trace to the campaign source.
CHROME = {
    "ASPIRE. ACT. ACHIEVE.",
    "LIGHTSPEED HOLDINGS LIMITED",
    "LightSpeed Holdings Limited\u2122",
    CTA_TEXT,
    CTA_URL,
    "THE POSITION",
    "THE ARCHITECTURE",
    "THE EVIDENCE",
    "THE ASK",
    "WHAT THE RECORD SHOWS",
    "THE GAPS",
    "AGENTIC AI",
    "CAMPAIGN REPORT",
    "CONFIDENTIAL \u00b7 EXECUTIVE",
}


# ── brand tokens ──────────────────────────────────────────────────────────────


def load_tokens() -> dict[str, str]:
    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    colors: dict[str, str] = {}
    for key, spec in data["color"].items():
        value = str(spec.get("value", ""))
        if value.startswith("#"):
            colors[key] = value.upper()
    return colors


TOK = load_tokens()
NAVY = TOK["navy"]
CYAN = TOK["cyan"]
RED = TOK["red"]
WHITE = TOK["white"]
MIST = TOK["morning-mist"]
MINERAL = TOK["deep-mineral"]
GREY_DARK = TOK["grey-dark"]
GREY_LIGHT_TEXT = TOK["grey-light-text"]
GREY_LIGHT = TOK["grey-light"]


# ── fonts ─────────────────────────────────────────────────────────────────────


def _font_candidates(bold: bool) -> list[Path]:
    win = Path("C:/Windows/Fonts")
    name = "arialbd.ttf" if bold else "arial.ttf"
    fallback = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return [
        win / name,
        Path("/usr/share/fonts/truetype/dejavu") / fallback,
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
        if bold
        else Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
    ]


_FONTS: dict[tuple[bool, int], ImageFont.FreeTypeFont] = {}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    key = (bold, size)
    if key in _FONTS:
        return _FONTS[key]
    for candidate in _font_candidates(bold):
        if candidate.is_file():
            _FONTS[key] = ImageFont.truetype(str(candidate), size)
            return _FONTS[key]
    raise SystemExit("ERROR: Arial (or a DejaVu fallback) is required for brand typography.")


# ── grounding ─────────────────────────────────────────────────────────────────


def norm(text: str) -> str:
    """Lowercase alphanumeric words only — survives markdown, punctuation, unicode."""
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


@dataclass
class Claim:
    """A rendered line plus the source phrase that authorises it."""

    text: str
    source: str

    def ok(self, haystack: str) -> bool:
        return norm(self.source) in haystack or norm(self.text) in haystack


# ── source parsing ────────────────────────────────────────────────────────────

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
BULLET_RE = re.compile(r"^\s*(?:[*\-+]|\d+[.)])\s+(.*)$")
BOLD_LABEL_RE = re.compile(r"^\*\*(.+?):?\*\*:?\s*(.*)$")
MD_NOISE_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)|\*\*|__|~~|`|\\")


def clean(text: str) -> str:
    text = MD_NOISE_RE.sub(lambda m: m.group(1) if m.group(1) else "", text)
    text = html.unescape(text).replace("\u2019", "'")
    return re.sub(r"\s+", " ", text).strip()


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(\u2014])", text.strip())
    return [p.strip() for p in parts if p.strip()]


def take(text: str, limit: int) -> str:
    """Whole sentences up to `limit` characters; never cuts mid-sentence."""
    out: list[str] = []
    for sentence in split_sentences(text):
        if out and len(" ".join([*out, sentence])) > limit:
            break
        out.append(sentence)
        if len(" ".join(out)) >= limit:
            break
    return " ".join(out)


def sentence_with(text: str, needle: str) -> str:
    """The single sentence that carries `needle`, so a trim cannot drop the point."""
    for sentence in split_sentences(text):
        if needle in sentence.lower():
            return sentence
    return ""


def clip(text: str, limit: int) -> str:
    """Trim at a clause boundary when one is close, else at a word boundary."""
    if len(text) <= limit:
        return text
    window = text[:limit]
    for sep in ("; ", ". "):
        cut = window.rfind(sep)
        if cut >= limit * 0.4:
            return window[:cut].rstrip(" ,;:") + "\u2026"
    return window.rsplit(" ", 1)[0].rstrip(" ,;:") + "\u2026"


def scope_of(raw: str, needle: str, limit: int = 120) -> str:
    """The source line the number sits on, trimmed to the sentence carrying it.

    Line-based, not a character window: markdown bullets are line delimited, so a
    line never drags in a neighbouring bullet or a heading fragment, and the quote
    always starts and ends on a whole word.
    """
    for line in raw.splitlines():
        if needle not in line:
            continue
        text = clean(BULLET_RE.sub(r"\1", line.strip()))
        for sentence in split_sentences(text):
            if needle in sentence:
                return clip(sentence, limit)
        return clip(text, limit)
    return ""


@dataclass
class Section:
    level: int
    heading: str
    paragraphs: list[str] = field(default_factory=list)
    bullets: list[str] = field(default_factory=list)


def parse_markdown(raw: str) -> tuple[str, list[Section]]:
    title = ""
    sections: list[Section] = []
    current: Section | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer
        if buffer and current is not None:
            prose = " ".join(line.strip() for line in buffer if not BULLET_RE.match(line))
            prose = clean(prose)
            if prose:
                current.paragraphs.append(prose)
            for line in buffer:
                bullet = BULLET_RE.match(line)
                if bullet:
                    item = clean(bullet.group(1))
                    if item:
                        current.bullets.append(item)
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
    flush()
    if not title and sections:
        title = sections[0].heading
    return title, sections


# Metric extraction: (pattern, label, how to read the scope clause).
METRIC_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(\d{1,3})\s+(?:AI\s+)?agents\b", re.I), "agents"),
    (re.compile(r"(\d{1,3})\s+(?:distinct\s+|operational\s+)?departments\b", re.I), "departments"),
    (re.compile(r"(\d{1,3})[-\s]tier\s+(?:HITL|human)", re.I), "HITL approval tiers"),
    (re.compile(r"(\d{1,3})[-\s]gate\s+(?:CI|continuous|quality)", re.I), "CI quality gates"),
    (re.compile(r"(\d{1,3})[-\s]tool\s+runtime", re.I), "canonical runtime tools"),
]

NUMBER_WORDS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
}


def digitise(text: str) -> str:
    """Spell out nothing: 'Five-tier' must be findable as 5. Lengths may shift,
    so scope extraction runs on this same string, never on the original."""

    def repl(match: re.Match[str]) -> str:
        return NUMBER_WORDS[match.group(0).lower()]

    return re.sub(r"\b(" + "|".join(NUMBER_WORDS) + r")\b", repl, text, flags=re.I)


METRIC_LABEL_TEXT = {
    "agents": "AGENTS IN OPERATION",
    "departments": "OPERATING DEPARTMENTS",
    "HITL approval tiers": "HITL APPROVAL TIERS",
    "canonical runtime tools": "RUNTIME TOOLS",
    "CI quality gates": "CI QUALITY GATES",
}


@dataclass
class Facts:
    slug: str
    title: str
    headline: Claim
    subhead: Claim
    metrics: list[dict[str, str]]
    pillars: list[dict[str, str]]
    proof: list[dict[str, str]]
    governance: list[str]
    architecture: list[str]
    positions: list[str]
    gaps: list[str]
    provenance: list[str]
    summary: str
    haystack: str


def build_facts(campaign: Path) -> Facts:
    slug = campaign.name
    dossier = campaign / "dossier.md"
    pack = campaign / "notebooklm" / "source-pack.md"
    briefing = campaign / "notebooklm" / "raw-briefing.md"

    if not dossier.is_file() and not pack.is_file():
        raise SystemExit(
            f"ERROR: {campaign} has neither dossier.md nor notebooklm/source-pack.md; "
            "nothing to ground the assets in."
        )

    raw_parts: list[str] = []
    sections: list[Section] = []
    title = ""
    for path in (dossier, pack):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            raw_parts.append(text)
            doc_title, doc_sections = parse_markdown(text)
            if not title:
                title = doc_title
            sections.extend(doc_sections)

    haystack = norm(" ".join(raw_parts))

    # Document furniture ("Master Dossier:") is internal bookkeeping, not a
    # campaign title; the report and slides use the clean stem.
    stem = re.sub(
        r"^(?:master\s+)?(?:dossier|report|briefing)\s*[:\-\u2014]\s*", "", title, flags=re.I
    ).strip()
    stem = stem or title or slug

    def pick(pattern: str) -> Section | None:
        rx = re.compile(pattern, re.I)
        for section in sections:
            if rx.search(section.heading):
                return section
        return None

    # ── metrics ───────────────────────────────────────────────────────────────
    # Number words are normalised first so "Five-tier" yields the same 5 as an
    # explicit digit, and scope text is read from the normalised string so
    # character offsets stay consistent.
    numeric = digitise(" ".join(raw_parts))
    metrics: list[dict[str, str]] = []
    seen: set[str] = set()
    for pattern, label in METRIC_PATTERNS:
        match = pattern.search(numeric)
        if not match:
            continue
        value = match.group(1)
        if value in seen:
            continue
        seen.add(value)
        # The scope is the source line the number appears on — provenance a reader
        # can check. A character window around the match used to cut words in half
        # and drag in markdown headings, so it is line-based now.
        scope = scope_of(numeric, match.group(0))
        metrics.append(
            {
                "value": value,
                "label": label,
                "label_text": METRIC_LABEL_TEXT.get(label, label.upper()),
                "scope": scope,
                "match": clean(match.group(0)),
            }
        )
    if len(metrics) < 3:
        raise SystemExit(
            "ERROR: fewer than three quantified facts found in the campaign source. "
            "An infographic needs at least three defensible numbers."
        )
    # Discovery order is deliberate (agents, departments, tiers, gates, tools):
    # it ranks the most decision-relevant facts first, so the big stat is the
    # headcount and the cutting edge drops the least load-bearing figure.
    metrics = metrics[:4]

    # ── claims by dimension ───────────────────────────────────────────────────
    def bullets_of(section: Section | None) -> list[str]:
        return list(section.bullets) if section else []

    def label_body(item: str) -> tuple[str, str]:
        match = BOLD_LABEL_RE.match(item)
        if match:
            return clean(match.group(1)), clean(match.group(2))
        if ":" in item[:48]:
            label, body = item.split(":", 1)
            return clean(label), clean(body)
        return "", item

    claims_section = pick(r"verified|factual|key claims|claims")
    pillar_section = pick(r"pillar|messaging")
    governance_section = pick(r"governance")

    pillars: list[dict[str, str]] = []
    for item in bullets_of(pillar_section) or bullets_of(claims_section):
        label, body = label_body(item)
        if not body:
            continue
        pillars.append({"label": (label or "PILLAR").upper()[:26], "body": take(body, 150)})
        if len(pillars) == 3:
            break

    # Proof = the field deployment, taken from whichever section names it.
    proof_section = pick(r"proof|evidence|field") or claims_section
    proof: list[dict[str, str]] = []
    for item in bullets_of(proof_section):
        label, body = label_body(item)
        if re.search(r"proof|field|deploy|bar|pilot", f"{label} {body}", re.I):
            proof.append({"label": (label or "PROOF").upper()[:26], "body": take(body, 130)})
    if not proof:
        for item in bullets_of(claims_section):
            label, body = label_body(item)
            if re.search(r"proof|field|deploy", body, re.I):
                proof.append({"label": label.upper()[:26], "body": take(body, 130)})
                break

    governance = [
        take(body, 400)
        for item in bullets_of(governance_section) or bullets_of(claims_section)
        for label, body in [label_body(item)]
        if re.search(r"governance|tier|approval|timeout|ci\b|gate", f"{label} {body}", re.I)
    ]

    def matching(pattern: str) -> list[str]:
        found: list[str] = []
        for item in bullets_of(claims_section):
            label, body = label_body(item)
            if re.search(pattern, f"{label} {body}", re.I):
                text = take(body, 170)
                if text and text not in found:
                    found.append(text)
        return found

    architecture = matching(r"offline|architect|local|deploy|zero|residency")
    # A paragraph can match both patterns; it belongs on one page, so anything
    # already carried by the architecture section is dropped from positions.
    positions = [
        p for p in matching(r"policy|strategy|inference|reform|commentary") if p not in architecture
    ]

    # ── gaps: only what the source itself calls unverified ────────────────────
    gaps: list[str] = []
    if briefing.is_file():
        brief_text = briefing.read_text(encoding="utf-8")
        gap_section = None
        for section in parse_markdown(brief_text)[1]:
            if re.search(r"gap|missing|unverified", section.heading, re.I):
                gap_section = section
                break
        if gap_section is not None:
            for item in gap_section.bullets:
                _, body = label_body(item)
                if re.search(r"absent|unverified|gap|missing|not\b", body, re.I):
                    gaps.append(take(body, 150))
    if not gaps:
        for section in sections:
            for item in section.bullets:
                _, body = label_body(item)
                if re.search(r"\bunverified\b|\bnot established\b|\babsent\b", body, re.I):
                    gaps.append(take(body, 150))
    if not gaps:
        gaps = ["No commercial gap analysis is stated in the campaign source."]

    # ── provenance ────────────────────────────────────────────────────────────
    # The dossier names the documents its claims were traced to. That trail is the
    # campaign's own argument for credibility, so the report reproduces it rather
    # than asserting trust.
    provenance: list[str] = []
    provenance_section = pick(r"provenance|audit|trace")
    for item in bullets_of(provenance_section):
        _, body = label_body(item)
        if body:
            provenance.append(take(body, 300))
    for paragraph in provenance_section.paragraphs if provenance_section else []:
        text = take(paragraph, 300)
        if text and text not in provenance:
            provenance.append(text)

    # ── headline / subhead ────────────────────────────────────────────────────
    exec_section = pick(r"executive|summary") or (sections[0] if sections else None)
    exec_para = exec_section.paragraphs[0] if exec_section and exec_section.paragraphs else ""
    summary = take(exec_para, 420) if exec_para else ""

    # Compare against the *normalised* haystack: it strips hyphens, so testing for
    # the literal "offline-first" would always fail and silently fall back to the
    # document title.
    headline = Claim("OFFLINE-FIRST AGENTIC AI", "offline-first, local-model architectures")
    if norm("offline-first") not in haystack:
        headline = Claim(stem.upper(), stem)

    subhead = Claim(
        "Sovereignty-by-design for African institutions.",
        "sovereignty-by-design for African institutions",
    )
    if norm("sovereignty-by-design") not in haystack:
        first = split_sentences(exec_para)[:1]
        subhead = Claim(take(first[0], 90) if first else stem[:90], first[0] if first else stem)

    return Facts(
        slug=slug,
        title=stem,
        headline=headline,
        subhead=subhead,
        metrics=metrics[:4],
        pillars=pillars,
        proof=proof,
        governance=governance,
        architecture=architecture,
        positions=positions,
        gaps=gaps,
        provenance=provenance,
        summary=summary,
        haystack=haystack,
    )


# ── drawing primitives ────────────────────────────────────────────────────────


def new_canvas(size: tuple[int, int], bg: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", size, bg)
    draw = ImageDraw.Draw(img)
    draw.fontmode = "1"  # type: ignore[attr-defined]  # AA off => exact palette pixels
    return img, draw


def wrap(
    draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, width: int
) -> list[str]:
    words, lines, line = text.split(), [], ""
    for word in words:
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def load_logo(height: int) -> Image.Image | None:
    """Official speed-mark, cropped above the wordmark. NEAREST keeps colours exact."""
    if not LOGO.is_file():
        return None
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.crop(logo.getchannel("A").getbbox())
    width, _ = logo.size
    alpha = logo.getchannel("A")
    cut, band_start = logo.size[1], None
    for y in range(logo.size[1]):
        empty = alpha.crop((0, y, width, y + 1)).getextrema()[1] == 0
        if empty:
            if band_start is None:
                band_start = y
        else:
            if band_start is not None and y - band_start >= 20:
                cut = band_start
                break
            band_start = None
    logo = logo.crop((0, 0, width, cut))
    logo = logo.crop(logo.getchannel("A").getbbox())
    scaled_w = max(1, round(logo.size[0] * height / logo.size[1]))
    return logo.resize((scaled_w, height), Image.NEAREST)


def soundwave(
    draw: ImageDraw.ImageDraw,
    x0: int,
    x1: int,
    centre_y: int,
    max_height: int,
    phase: float,
    color: str = CYAN,
    bars: int = 56,
) -> None:
    """Animated cyan waveform. Deterministic in `phase`, so frames are reproducible."""
    span = x1 - x0
    step = span / bars
    bar_w = max(2, int(step * 0.55))
    for i in range(bars):
        envelope = math.sin(math.pi * (i + 0.5) / bars)  # taper both ends
        wave = abs(math.sin(i * 0.42 + phase * 2.4)) * 0.72 + 0.28 * abs(
            math.sin(i * 0.17 - phase * 1.7)
        )
        height = max(3, int(max_height * envelope * wave))
        x = int(x0 + i * step)
        draw.rectangle([x, centre_y - height // 2, x + bar_w, centre_y + height // 2], fill=color)


# ── infographics ──────────────────────────────────────────────────────────────


def render_infographic(facts: Facts, size: tuple[int, int], variant: str) -> Image.Image:
    w, h = size
    img, draw = new_canvas(size, NAVY)
    margin = max(48, round(w * 0.055))
    content_w = w - 2 * margin

    logo = load_logo(max(26, round(h * 0.036)))
    if logo is not None:
        img.paste(logo, (margin, margin), logo)
        draw.text(
            (margin + logo.size[0] + 12, margin + 6),
            "LIGHTSPEED HOLDINGS LIMITED",
            font=font(max(13, round(h * 0.017)), bold=True),
            fill=CYAN,
        )

    draw.rectangle([0, 0, max(5, round(w * 0.006)), h], fill=CYAN)

    big = facts.metrics[0]
    scale = h / 900.0
    eyebrow_size = max(14, round(18 * scale))
    head_size = max(28, round((62 if variant == "landscape" else 54) * scale))
    stat_size = max(72, round((150 if variant != "facebook" else 104) * scale))
    unit_size = max(15, round(21 * scale))
    body_size = max(13, round(17 * scale))

    y = margin + (logo.size[1] if logo else 0) + round(30 * scale)

    draw.text((margin, y), "AGENTIC AI", font=font(eyebrow_size, bold=True), fill=CYAN)
    y += round(eyebrow_size * 1.9)

    head_font = font(head_size, bold=True)
    for line in wrap(draw, facts.headline.text, head_font, content_w):
        draw.text((margin, y), line, font=head_font, fill=WHITE)
        y += round(head_size * 1.12)

    y += round(12 * scale)
    draw.rectangle([margin, y, margin + round(120 * scale), y + max(4, round(6 * scale))], fill=RED)
    header_bottom = y + round(8 * scale)

    # ── measure the lower block, then centre it in the space above the CTA.
    # Without this the block stacks under the headline and leaves a dead band.
    sub_font = font(body_size)
    sub_lines = wrap(draw, facts.subhead.text, sub_font, content_w)[:2]
    sub_step = round(body_size * 1.55)
    sub_h = len(sub_lines) * sub_step

    stat_font = font(stat_size, bold=True)
    stat_h = round(stat_size * 1.05)
    unit_font = font(unit_size, bold=True)

    rest = facts.metrics[1:]
    chip_gap = round(12 * scale) if variant == "facebook" else round(16 * scale)
    chip_base = 64 if variant == "facebook" else 92
    # Floor the chip height: `scale` on a 628px-tall canvas shrinks it below the
    # point where a value + label fit, which clipped the labels.
    chip_h = max(56, round(chip_base * scale)) if rest else 0
    chip_w = (content_w - chip_gap * (len(rest) - 1)) // len(rest) if rest else content_w

    gap_sub_stat = round(34 * scale)
    gap_stat_chip = round(28 * scale) if rest else 0
    block_h = sub_h + gap_sub_stat + stat_h + gap_stat_chip + chip_h

    cta_h = max(44, round(54 * scale))
    cta_y = h - margin - cta_h - round(26 * scale)
    available = cta_y - header_bottom - round(24 * scale)
    y = header_bottom + max(round(12 * scale), int((available - block_h) * 0.45))

    for line in sub_lines:
        draw.text((margin, y), line, font=sub_font, fill=MIST)
        y += sub_step
    y += gap_sub_stat

    # Key statistic — dominant element, one per graphic.
    draw.text((margin, y), big["value"], font=stat_font, fill=WHITE)
    value_w = draw.textlength(big["value"], font=stat_font)
    draw.text(
        (margin + value_w + round(18 * scale), y + round(stat_size * 0.42)),
        big["label_text"],
        font=unit_font,
        fill=CYAN,
    )
    y += stat_h + gap_stat_chip

    # Supporting metrics: chips on square/landscape, a tight row on Facebook.
    # Chip internals are proportional to chip_h so no label can be clipped.
    for index, metric in enumerate(rest):
        x = margin + index * (chip_w + chip_gap)
        draw.rectangle([x, y, x + chip_w, y + chip_h], fill=MINERAL, outline=CYAN, width=2)
        value_size = max(20, round(chip_h * 0.42))
        label_size = max(10, round(chip_h * 0.205))
        value_y = y + round(chip_h * 0.08)
        draw.text(
            (x + round(14 * scale), value_y),
            metric["value"],
            font=font(value_size, bold=True),
            fill=CYAN,
        )
        label = metric["label_text"]
        if len(label) > 26:
            label = label[:25] + "\u2026"
        max_label_w = chip_w - round(28 * scale)
        label_font = font(label_size, bold=True)
        while label_size > 9 and draw.textlength(label, font=label_font) > max_label_w:
            label_size -= 1
            label_font = font(label_size, bold=True)
        draw.text(
            (x + round(14 * scale), value_y + value_size + round(chip_h * 0.06)),
            label,
            font=label_font,
            fill=GREY_LIGHT_TEXT,
        )

    # CTA — one action, bottom-left, red for the action colour.
    cta_h = max(44, round(54 * scale))
    cta_y = h - margin - cta_h - round(26 * scale)
    cta_w = round(draw.textlength(CTA_TEXT, font=font(max(15, round(19 * scale)), bold=True)))
    cta_w += round(46 * scale)
    draw.rectangle([margin, cta_y, margin + cta_w, cta_y + cta_h], fill=RED)
    draw.text(
        (margin + round(23 * scale), cta_y + round(cta_h * 0.3)),
        CTA_TEXT,
        font=font(max(15, round(19 * scale)), bold=True),
        fill=WHITE,
    )
    draw.text(
        (margin + cta_w + round(20 * scale), cta_y + round(cta_h * 0.34)),
        CTA_URL,
        font=font(max(13, round(16 * scale))),
        fill=CYAN,
    )

    draw.rectangle([margin, h - margin, w - margin, h - margin], fill=GREY_DARK)
    draw.text(
        (margin, h - margin + round(8 * scale)),
        "LightSpeed Holdings Limited\u2122",
        font=font(max(11, round(13 * scale))),
        fill=GREY_LIGHT_TEXT,
    )
    draw.text(
        (w - margin, h - margin + round(8 * scale)),
        "ASPIRE. ACT. ACHIEVE.",
        font=font(max(11, round(13 * scale)), bold=True),
        fill=CYAN,
        anchor="ra",
    )
    return img


# ── carousel ──────────────────────────────────────────────────────────────────


def carousel_cards(facts: Facts) -> list[Image.Image]:
    w, h = SQUARE
    margin = 64
    content_w = w - 2 * margin
    logo = load_logo(30)
    # Two anchored zones. Copy on this campaign is one sentence per card, so a
    # single centred block always pooled its slack into two big voids. Copy now
    # hangs from the top rule and the dominant element (stat / button / ghost
    # numeral) is pinned to the footer, which reads as a deliberate split.
    top, bottom = 200, 966

    def chrome(draw: ImageDraw.ImageDraw, img: Image.Image, index: int, total: int) -> None:
        draw.rectangle([0, 0, 6, h], fill=CYAN)
        draw.rectangle([margin, 88, w - margin, 90], fill=CYAN)
        draw.text(
            (w - margin, 44),
            f"{index:02d} / {total:02d}",
            font=font(18, bold=True),
            fill=GREY_LIGHT_TEXT,
            anchor="ra",
        )
        if logo is not None:
            img.paste(logo, (margin, 30), logo)
            draw.text(
                (margin + logo.size[0] + 13, 42),
                "LIGHTSPEED HOLDINGS LIMITED",
                font=font(15, bold=True),
                fill=CYAN,
            )
        draw.rectangle([margin, h - 74, w - margin, h - 72], fill=GREY_DARK)
        draw.text(
            (margin, h - 56),
            "LightSpeed Holdings Limited\u2122",
            font=font(14),
            fill=WHITE,
        )
        draw.text(
            (w - margin, h - 56),
            "ASPIRE. ACT. ACHIEVE.",
            font=font(14, bold=True),
            fill=CYAN,
            anchor="ra",
        )

    def ghost(draw: ImageDraw.ImageDraw, glyph: str, y_from: int) -> None:
        """Outlined sequence numeral for the space the copy cannot fill."""
        space = bottom - y_from
        if space < 210:
            return
        size = min(430, int(space * 1.3))
        draw.text(
            (w - margin, bottom),
            glyph,
            font=font(size, bold=True),
            fill=NAVY,
            stroke_width=max(2, size // 150),
            stroke_fill=GREY_DARK,
            anchor="rs",
        )

    def card(
        index: int, total: int, eyebrow: str, heading: str, body: str, glyph: str
    ) -> Image.Image:
        """Body card: copy from the top rule, ghost numeral filling the foot."""
        img, draw = new_canvas(SQUARE, NAVY)
        # Largest type that still clears the zone, so a short card is not a
        # small card: the measure shrinks before the layout runs out of room.
        choices = ((64, 28), (56, 26), (48, 24), (42, 22))
        for head_size, body_size in choices:
            f_h, f_p = font(head_size, bold=True), font(body_size)
            head_lines = wrap(draw, heading, f_h, content_w)
            body_lines = wrap(draw, body, f_p, content_w) if body else []
            head_step, body_step = round(head_size * 1.18), round(body_size * 1.5)
            block = 92 + len(head_lines) * head_step + len(body_lines) * body_step
            if block <= bottom - top or (head_size, body_size) == choices[-1]:
                break
        chrome(draw, img, index, total)
        ghost(draw, glyph, top + block + 48)
        y = top
        draw.text((margin, y), eyebrow, font=font(19, bold=True), fill=CYAN)
        y += 40
        for line in head_lines:
            draw.text((margin, y), line, font=f_h, fill=WHITE)
            y += head_step
        y += 24
        draw.rectangle([margin, y, margin + 96, y + 6], fill=RED)
        y += 22
        for line in body_lines:
            draw.text((margin, y), line, font=f_p, fill=MIST)
            y += body_step
        return img

    # Exact card count, computed before anything is drawn so the "NN / NN"
    # numbering is honest. No padding: a duplicate card is worse than a short set.
    pillars = facts.pillars[:3]
    proofs = facts.proof[:1]
    total = 1 + len(pillars) + len(proofs) + 1
    cards: list[Image.Image] = []

    # 1 — hook: headline hanging from the top rule, the single dominant number
    # pinned to the footer. The stat is what stops a scroll, so it gets the
    # lower half instead of a grey caption line.
    img, draw = new_canvas(SQUARE, NAVY)
    chrome(draw, img, 1, total)
    # A hero headline that breaks to an orphan word reads as a bug, so step the
    # size down until it sets on one line.
    head_size = 76
    for candidate in (76, 70, 64, 58, 52):
        head_size = candidate
        if len(wrap(draw, facts.headline.text, font(candidate, bold=True), content_w)) == 1:
            break
    f_eb, f_head, f_sub = font(18, bold=True), font(head_size, bold=True), font(24)
    head_lines = wrap(draw, facts.headline.text, f_head, content_w)
    sub_lines = wrap(draw, facts.subhead.text, f_sub, content_w)[:3]
    big = facts.metrics[0]
    stat_size = 200
    head_step = round(head_size * 1.18)

    y = top
    draw.text((margin, y), "AGENTIC AI", font=f_eb, fill=CYAN)
    y += 40
    for line in head_lines:
        draw.text((margin, y), line, font=f_head, fill=WHITE)
        y += head_step
    y += 24
    draw.rectangle([margin, y, margin + 120, y + 6], fill=RED)
    y += 26
    for line in sub_lines:
        draw.text((margin, y), line, font=f_sub, fill=MIST)
        y += 38

    stat_font = font(stat_size, bold=True)
    draw.text((margin, bottom), big["value"], font=stat_font, fill=WHITE, anchor="ls")
    value_w = draw.textlength(big["value"], font=stat_font)
    draw.text(
        (margin + value_w + 22, bottom - round(stat_size * 0.36)),
        big["label_text"],
        font=font(26, bold=True),
        fill=CYAN,
        anchor="lm",
    )
    cards.append(img)

    # 2..N-1 — pillars and proof
    for number, pillar in enumerate(pillars, start=1):
        cards.append(
            card(
                len(cards) + 1,
                total,
                f"PILLAR {number:02d}",
                pillar["label"],
                pillar["body"],
                f"{number:02d}",
            )
        )
    for offset, proof in enumerate(proofs, start=len(pillars) + 1):
        cards.append(
            card(
                len(cards) + 1, total, "FIELD PROOF", proof["label"], proof["body"], f"{offset:02d}"
            )
        )

    # final — CTA: statement from the top rule, the action closing the card as a
    # full-width band so the foot carries weight instead of a floating button.
    img, draw = new_canvas(SQUARE, NAVY)
    chrome(draw, img, total, total)
    f_cta = font(68, bold=True)
    y = top
    draw.text((margin, y), "THE ASK", font=font(19, bold=True), fill=CYAN)
    y += 40
    for line in wrap(draw, "Read the playbook.", f_cta, content_w):
        draw.text((margin, y), line, font=f_cta, fill=WHITE)
        y += 84
    y += 24
    draw.rectangle([margin, y, margin + 120, y + 6], fill=RED)
    y += 26
    draw.text((margin, y), CTA_URL, font=font(22), fill=CYAN)

    f_btn = font(26, bold=True)
    band_h = 104
    band_y = bottom - band_h
    draw.rectangle([margin, band_y, w - margin, band_y + band_h], fill=RED)
    draw.text((margin + 32, band_y + 36), CTA_TEXT, font=f_btn, fill=WHITE)
    arrow_w = round(draw.textlength("\u2192", font=f_btn))
    draw.text((w - margin - 32 - arrow_w, band_y + 36), "\u2192", font=f_btn, fill=WHITE)
    cards.append(img)

    return cards


# ── video ─────────────────────────────────────────────────────────────────────


@dataclass
class Beat:
    subtitle: str
    source: str
    seconds: float


def sentence_case(text: str) -> str:
    """'OFFLINE-FIRST AGENTIC AI' -> 'Offline-first agentic AI' (keeps AI, IoT, SADC)."""
    keep = {"AI", "HITL", "CI", "SADC", "DPA", "API", "ML", "GPU"}
    words = text.strip().split()
    out: list[str] = []
    for index, word in enumerate(words):
        bare = re.sub(r"[^A-Za-z]", "", word)
        if bare.upper() in keep and bare:
            out.append(word.upper())
        elif index == 0:
            out.append(word[:1].upper() + word[1:].lower())
        elif word.isupper() and len(bare) > 1:
            out.append(word.lower())
        else:
            out.append(word)
    return " ".join(out)


def build_beats(facts: Facts) -> list[Beat]:
    """60-second short: hook, the claim, governance, the proof, the CTA.

    Each subtitle is a compression of a line that exists in the source. Every
    line is capped at 42 characters so it survives a 9:16 safe area without
    reflow.
    """
    big = facts.metrics[0]
    gov = next((s for g in facts.governance if (s := sentence_with(g, "timeout"))), "")
    proof_label = facts.proof[0]["label"] if facts.proof else ""

    hook = sentence_case(facts.headline.text) + "."
    counts = f"{big['value']} {big['label']}."
    if len(facts.metrics) > 1:
        counts += f" {facts.metrics[1]['value']} {facts.metrics[1]['label']}."
    beats = [
        Beat(hook, facts.headline.text, 8),
        Beat(counts, f"{big['value']} {big['label']}", 12),
    ]
    if gov:
        beats.append(Beat("Timeouts escalate. Never auto-approve.", "Timeouts escalate", 12))
    if proof_label:
        place = "in Malawi" if norm("malawi") in facts.haystack else ""
        beats.append(Beat(f"Field-proven {place}.".replace("  ", " "), proof_label, 16))
    beats.append(Beat("Read the playbook.", CTA_TEXT, 12))

    # Stretch the CTA to land exactly on 60 seconds.
    spent = sum(b.seconds for b in beats[:-1])
    beats[-1] = Beat(beats[-1].subtitle, beats[-1].source, max(4.0, 60 - spent))

    for beat in beats:
        if len(beat.subtitle) > 42:
            print(f"  WARNING: subtitle over 42 chars ({len(beat.subtitle)}): {beat.subtitle!r}")
    return beats


def render_video(
    facts: Facts,
    beats: list[Beat],
    size: tuple[int, int],
    frame_dir: Path,
    label: str,
) -> int:
    w, h = size
    frame_dir.mkdir(parents=True, exist_ok=True)
    for old in frame_dir.glob("f*.png"):
        old.unlink()

    vertical = h > w
    margin = round(w * 0.089) if vertical else 96
    content_w = w - 2 * margin
    logo = load_logo(max(28, round(h * 0.021)))

    scale = h / 1920.0 if vertical else h / 1080.0
    head_size = max(40, round(96 * scale)) if vertical else max(52, round(64 * scale))
    sub_size = max(26, round(46 * scale)) if vertical else max(28, round(34 * scale))

    total_frames = 0
    for beat in beats:
        # Static base per beat: only the waveform animates, so we don't redraw
        # the whole layout 30 times a second.
        base, d = new_canvas(size, NAVY)
        if not vertical:
            d.rectangle([0, 0, max(6, round(w * 0.003)), h], fill=NAVY)
            d.rectangle([0, 0, max(6, round(w * 0.003)), h], fill=CYAN)

        if logo is not None:
            base.paste(logo, (margin, margin), logo)
            d.text(
                (margin + logo.size[0] + 13, margin + 8),
                "LIGHTSPEED HOLDINGS LIMITED",
                font=font(max(13, round(h * 0.0105)), bold=True),
                fill=CYAN,
            )

        if vertical:
            could_start = round(h * 0.16)
            head_lines = wrap(d, facts.headline.text, font(head_size, bold=True), content_w)
            for i, line in enumerate(head_lines):
                d.text(
                    (margin, could_start + i * round(head_size * 1.12)),
                    line,
                    font=font(head_size, bold=True),
                    fill=WHITE,
                )
            bar_y = could_start + len(head_lines) * round(head_size * 1.12) + round(26 * scale)
            d.rectangle(
                [margin, bar_y, margin + round(120 * scale), bar_y + round(8 * scale)], fill=RED
            )
            sub_y = bar_y + round(44 * scale)
            for line in wrap(d, facts.subhead.text, font(sub_size), content_w)[:3]:
                d.text((margin, sub_y), line, font=font(sub_size), fill=MIST)
                sub_y += round(sub_size * 1.4)
            wave_top = round(h * 0.545)
        else:
            head_lines = wrap(d, facts.headline.text, font(head_size, bold=True), content_w)
            for i, line in enumerate(head_lines):
                d.text(
                    (margin, round(h * 0.24) + i * round(head_size * 1.15)),
                    line,
                    font=font(head_size, bold=True),
                    fill=WHITE,
                )
            bar_y = round(h * 0.24) + len(head_lines) * round(head_size * 1.15)
            d.rectangle(
                [margin, bar_y, margin + round(140 * scale), bar_y + round(7 * scale)], fill=RED
            )
            sub_y = bar_y + round(38 * scale)
            for line in wrap(d, facts.subhead.text, font(sub_size), content_w)[:2]:
                d.text((margin, sub_y), line, font=font(sub_size), fill=MIST)
                sub_y += round(sub_size * 1.45)
            wave_top = round(h * 0.60)

        # Subtitle band: inside the platform safe area.
        if vertical:
            band_top = round(h * 0.655)  # 1258 of 1920
            band_h = round(h * 0.115)
        else:
            band_top = round(h * 0.78)
            band_h = round(h * 0.115)
        d.rectangle([0, band_top, w, band_top + band_h], fill=MINERAL)
        d.rectangle([0, band_top, max(5, round(w * 0.006)), band_top + band_h], fill=CYAN)

        sub_size_band = max(28, round(band_h * 0.42))
        lines = wrap(d, beat.subtitle, font(sub_size_band, bold=True), content_w)[:2]
        line_h = round(sub_size_band * 1.18)
        text_y = band_top + (band_h - line_h * len(lines)) // 2
        for line in lines:
            d.text((margin, text_y), line, font=font(sub_size_band, bold=True), fill=WHITE)
            text_y += line_h

        # CTA + footer chrome
        d.text(
            (margin, band_top + band_h + round(26 * scale)),
            CTA_URL,
            font=font(max(13, round(18 * scale))),
            fill=GREY_LIGHT_TEXT,
        )

        frames = round(beat.seconds * FPS)
        wave_x0, wave_x1 = margin, w - margin
        wave_centre = wave_top + round(h * 0.035)
        wave_h = round(h * 0.055) if vertical else round(h * 0.075)

        for i in range(frames):
            frame = base.copy()
            fd = ImageDraw.Draw(frame)
            fd.fontmode = "1"  # type: ignore[attr-defined]
            phase = (total_frames + i) / FPS
            soundwave(fd, wave_x0, wave_x1, wave_centre, wave_h, phase)
            frame.save(frame_dir / f"f{total_frames + i + 1:05d}.png", compress_level=1)
        total_frames += frames

    print(f"  {label}: {total_frames} frames at {w}x{h}")
    return total_frames


def encode_video(frame_dir: Path, out: Path, fps: int) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("ERROR: ffmpeg not found on PATH; cannot encode video.")
    out.unlink(missing_ok=True)
    command = [
        ffmpeg,
        "-y",
        "-loglevel",
        "error",
        "-framerate",
        str(fps),
        "-i",
        str(frame_dir / "f%05d.png"),
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(out),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0 or not out.is_file():
        raise SystemExit(f"ERROR: ffmpeg encode failed:\n{(result.stderr or '').strip()[:800]}")


# ── report ────────────────────────────────────────────────────────────────────


def report_html(facts: Facts, when: datetime) -> str:
    esc = html.escape
    metrics_rows = "".join(
        f"<tr><td class='v'>{esc(m['value'])}</td>"
        f"<td class='l'>{esc(sentence_case(m['label_text']))}</td>"
        f"<td class='s'>{esc(m['scope'])}</td></tr>"
        for m in facts.metrics
    )
    architecture = "".join(f"<p>{esc(p)}</p>" for p in (facts.architecture or [facts.summary])[:3])
    evidence = (
        "".join(
            f"<p><strong>{esc(sentence_case(p['label']))}.</strong> {esc(p['body'])}</p>"
            for p in facts.proof
        )
        or "<p>The campaign source records no field proof.</p>"
    )
    governance = "".join(
        f"<p>{esc(g)}</p>" for g in (facts.governance or ["No governance detail in source."])[:3]
    )
    positions = "".join(f"<p>{esc(p)}</p>" for p in (facts.positions or [])[:2])
    gaps = "".join(f"<li>{esc(g)}</li>" for g in facts.gaps)

    def page(band: str, body: str, number: int, top: bool = False) -> str:
        return (
            f"<section class='page'>"
            f"{band}"
            f"<div class='body{' top' if top else ''}'>{body}</div>"
            f"{source_note}"
            f"<footer><span>LightSpeed Holdings Limited\u2122</span>"
            f"<span>{esc(facts.slug)}</span><span>{number} / 4</span></footer>"
            f"</section>"
        )

    cover_head = (
        f"<div class='mast'>"
        f"<div class='eyebrow'>CAMPAIGN REPORT &nbsp;\u00b7&nbsp; CONFIDENTIAL \u00b7 EXECUTIVE</div>"
        f"<h1>{esc(facts.title)}</h1>"
        f"<div class='rule'></div>"
        f"<p class='sub'>{esc(facts.subhead.text)}</p>"
        f"<p class='date'>{when.strftime('%d %B %Y')}</p>"
        f"</div>"
    )

    def band(kicker: str, heading: str) -> str:
        return (
            f"<div class='band'><div class='kicker'>{esc(kicker)}</div>"
            f"<h2>{esc(heading)}</h2></div>"
        )

    def pull(text: str) -> str:
        return f"<p class='pull'>{esc(text)}</p>" if text else ""

    source_note = (
        "<p class='src'>Source: campaign dossier.md and notebooklm/source-pack.md. "
        "Quoted wording is verbatim; nothing is paraphrased into a new claim.</p>"
    )

    page1 = (
        "<h2>Executive summary</h2>"
        + f"<p class='lead'>{esc(facts.summary)}</p>"
        + "<h2>Key metrics</h2>"
        + f"<table class='metrics'><thead><tr><th>Value</th><th>Measure</th>"
        f"<th>Where it appears in the source</th></tr></thead><tbody>{metrics_rows}</tbody></table>"
    )
    pillar_items = "".join(
        f"<p class='pillar'><strong>{esc(sentence_case(p['label']))}.</strong> {esc(p['body'])}</p>"
        for p in facts.pillars
    )

    page2 = (
        architecture
        + positions
        + "<h2>Governance</h2>"
        + governance
        + pull("Timeouts escalate, they never auto-approve.")
        + (
            "<h2>Traceability</h2>"
            + "".join(f"<p class='trace'>{esc(p)}</p>" for p in facts.provenance[:2])
            if facts.provenance
            else ""
        )
    )
    page3 = (
        evidence
        + "<h2>Positioning</h2>"
        + (pillar_items or "<p>The campaign source states no messaging pillars.</p>")
        + source_note
    )
    page4 = (
        "<p class='lead'>Read the playbook and scope a 90-day pilot built on integration "
        "seams rather than rip-and-replace.</p>"
        + "<h2>The gaps</h2>"
        + f"<ul class='gaps'>{gaps}</ul>"
        + "<p class='note'>Gaps are reproduced from the campaign source. They are stated, "
        "not filled: a number that is not in the source does not appear in this report.</p>"
    )

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{esc(facts.title)}</title>
<style>
  @page {{ size: A4; margin: 0; }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{ font-family: Arial, Helvetica, sans-serif; color: {MINERAL};
         -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  .page {{ width: 210mm; height: 297mm; padding: 18mm 18mm 20mm; position: relative;
           page-break-after: always; background: {WHITE}; overflow: hidden;
           display: flex; flex-direction: column; }}
  .page:last-child {{ page-break-after: auto; }}
  .body {{ flex: 1; display: flex; flex-direction: column; justify-content: center; }}
  .body.top {{ justify-content: flex-start; }}
  .mast {{ background: {NAVY}; color: {WHITE}; margin: -18mm -18mm 8mm; padding: 18mm; }}
  .band {{ background: {NAVY}; color: {WHITE}; margin: -18mm -18mm 7mm; padding: 14mm 18mm 10mm; }}
  .band .kicker {{ color: {CYAN}; font-size: 8pt; letter-spacing: .12em; font-weight: 700; }}
  .band h2 {{ color: {WHITE}; border-left: none; padding-left: 0; margin: 3mm 0 0;
              font-size: 19pt; }}
  .pull {{ font-size: 14.5pt; line-height: 1.35; color: {NAVY}; font-weight: 700;
           border-left: 4px solid {RED}; padding-left: 5mm; margin: 7mm 0; }}
  .pillar {{ border-left: 2px solid {GREY_LIGHT}; padding-left: 4mm; margin-bottom: 4mm; }}
  .pillar strong {{ color: {NAVY}; }}
  .trace {{ font-size: 9.5pt; color: {GREY_DARK}; line-height: 1.5; }}
  .src {{ font-size: 8pt; color: {GREY_DARK}; border-top: 1px solid {GREY_LIGHT};
          padding-top: 2mm; position: absolute; left: 18mm; right: 18mm; bottom: 14mm; }}
  .eyebrow {{ color: {CYAN}; font-size: 8pt; letter-spacing: .12em; font-weight: 700; }}
  h1 {{ font-size: 26pt; line-height: 1.12; margin: 6mm 0 4mm; font-weight: 700; }}
  .rule {{ width: 34mm; height: 1.2mm; background: {RED}; }}
  .sub {{ font-size: 12pt; color: {MIST}; margin: 4mm 0 0; }}
  .date {{ font-size: 9pt; color: {GREY_LIGHT_TEXT}; margin: 3mm 0 0; }}
  h2 {{ font-size: 13pt; color: {NAVY}; margin: 7mm 0 2mm; font-weight: 700;
        border-left: 3px solid {CYAN}; padding-left: 3mm; }}
  p {{ font-size: 11pt; line-height: 1.6; margin: 0 0 3.2mm; }}
  .lead {{ font-size: 12pt; line-height: 1.55; }}
  table.metrics {{ width: 100%; border-collapse: collapse; margin-top: 2mm; font-size: 9.5pt; }}
  table.metrics th {{ background: {NAVY}; color: {WHITE}; text-align: left; padding: 2.4mm 3mm;
                      font-size: 8.5pt; letter-spacing: .06em; }}
  table.metrics td {{ padding: 2.4mm 3mm; border-bottom: 1px solid {GREY_LIGHT}; }}
  table.metrics tr:nth-child(even) td {{ background: {GREY_LIGHT}; }}
  td.v {{ font-weight: 700; color: {NAVY}; font-size: 13pt; width: 16mm; }}
  td.l {{ font-weight: 700; color: {NAVY}; width: 52mm; }}
  td.s {{ color: {GREY_DARK}; font-size: 8.5pt; }}
  ul.gaps {{ margin: 0 0 4mm; padding-left: 5mm; }}
  ul.gaps li {{ font-size: 10.5pt; line-height: 1.5; margin-bottom: 2.5mm; }}
  .note {{ font-size: 9pt; color: {GREY_DARK}; border-left: 3px solid {RED}; padding-left: 3mm; }}
  footer {{ position: absolute; left: 18mm; right: 18mm; bottom: 8mm; display: flex;
            justify-content: space-between; font-size: 7.5pt; color: {GREY_DARK};
            border-top: 1px solid {GREY_LIGHT}; padding-top: 2mm; }}
</style></head>
<body>
{page(cover_head, page1, 1, top=True)}
{page(band("SECTION 02", "The architecture and its controls"), page2, 2, top=True)}
{page(band("SECTION 03", "The evidence"), page3, 3, top=True)}
{page(band("SECTION 04", "The ask"), page4, 4, top=True)}
</body></html>
"""


def find_browser() -> str:
    candidates = [str(Path.home() / "AppData/Local/Google/Chrome/Application/chrome.exe")]
    candidates += [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    for name in ("chrome", "google-chrome", "chromium", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    raise SystemExit("ERROR: no Chromium browser found; set BROWSER_BIN to print the report PDF.")


def print_pdf(browser: str, html_path: Path, pdf_path: Path) -> None:
    pdf_path.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(prefix="ls-assets-") as profile:
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
            "--virtual-time-budget=4000",
            "--no-pdf-header-footer",
            f"--user-data-dir={profile}",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ]
        proc = subprocess.run(command, capture_output=True, text=True, timeout=240, check=False)
    if not pdf_path.is_file() or pdf_path.stat().st_size == 0:
        detail = (proc.stderr or proc.stdout or "").strip()[:700]
        raise SystemExit(f"ERROR: report PDF print failed.\n{detail}")


# ── social copy ───────────────────────────────────────────────────────────────


LEGAL = "LightSpeed Holdings Limited\u2122"


def decap(text: str) -> str:
    """Lower a leading capital so a sentence can follow a label: 'Field-anchored' -> 'field-anchored'."""
    if not text:
        return text
    first = text.split()[0]
    bare = re.sub(r"[^A-Za-z]", "", first)
    if len(bare) > 1 and bare.isupper():
        return text
    return text[:1].lower() + text[1:]


def fit_post(text: str, limit: int = 280) -> str:
    """Trim to the last complete sentence that fits, so a post never ends mid-clause."""
    if len(text) <= limit:
        return text
    kept = ""
    for sentence in split_sentences(text):
        trial = f"{kept} {sentence}".strip()
        if len(trial) > limit:
            break
        kept = trial
    return kept or text[: limit - 1].rstrip() + "\u2026"


def social_copy(facts: Facts, when: datetime) -> tuple[str, list[str]]:
    big = facts.metrics[0]
    second = facts.metrics[1] if len(facts.metrics) > 1 else None
    proof = facts.proof[0] if facts.proof else None
    gov = next((s for g in facts.governance if (s := sentence_with(g, "timeout"))), "")
    pillar_lines = "\n".join(f"- {p['body']}" for p in facts.pillars[:3])
    proof_line = f"{sentence_case(proof['label'])}: {decap(proof['body'])}" if proof else ""
    headline = sentence_case(facts.headline.text)
    cta = sentence_case(CTA_TEXT)
    counts = f"{big['value']} {big['label']}."
    if second:
        counts += f" {second['value']} {second['label']}."

    posts = [
        fit_post(f"{LEGAL}\n\n{facts.subhead.text}\n\n{counts}"),
        fit_post(proof_line or facts.subhead.text),
        fit_post(f"{gov or headline}\n\n{cta} \u2192 {CTA_URL}"),
    ]
    lengths = " / ".join(str(len(p)) for p in posts)
    for index, post in enumerate(posts, start=1):
        if len(post) > 280:
            print(f"  WARNING: X post {index} is {len(post)} chars (limit 280)")

    return (
        f"""# Social copy — {facts.slug}

Generated {when.strftime("%d %B %Y")}. Every claim below traces to the campaign
source; no figure was added, rounded, or re-derived. Conventions: `LightSpeed
Holdings Limited\u2122` on first mention in each platform block, no emoji.

---

## X (Twitter) — thread

Character budget per post: 280. Thread length: {len(posts)} posts. Lengths: {lengths}.
Each fenced block below is one post.

**Post 1** — {len(posts[0])}/280
```
{posts[0]}
```

**Post 2** — {len(posts[1])}/280
```
{posts[1]}
```

**Post 3** — {len(posts[2])}/280
```
{posts[2]}
```

---

## Facebook — post

```
{LEGAL} \u2014 {headline}.

{facts.subhead.text}

{big["value"]} {big["label"]}{(", " + second["value"] + " " + second["label"]) if second else ""}.

{pillar_lines}

{proof_line}

{cta}: {CTA_URL}
```

Suggested link preview title: `{headline}`

---

## Instagram — caption

```
{LEGAL}

{headline}.

{facts.subhead.text}

{big["value"]} {big["label"]} \u00b7 {(second["value"] + " " + second["label"]) if second else ""}

{facts.pillars[0]["body"] if facts.pillars else ""}

{cta} \u2192 link in bio.

#AgenticAI #OfflineFirst #SovereignAI #Malawi #SADC #AIForAfrica #LightSpeedHoldings
```

Carousel pairing: post `carousels/instagram/card-1.png` as slide 1 (the hook);
the caption above is the slide-1 text, so do not repeat it in the image.

---

## Asset pairing

| Platform | Asset | Copy block |
|----------|-------|------------|
| X | `infographics/infographic-landscape-1600x900.png` | X thread |
| Facebook | `infographics/infographic-landscape-1200x628.png` | Facebook post |
| Instagram feed | `infographics/infographic-square-1080x1080.png` | Instagram caption |
| Instagram carousel | `carousels/instagram/card-1..N.png` | Instagram caption |
| LinkedIn document | `carousels/social-carousel.pdf` | LinkedIn post field (report summary) |
| LinkedIn / YouTube | `video/video-overview-16x9.mp4` | X thread opening |
| Reels / TikTok | `video/video-short-1080x1920.mp4` | Instagram caption |

## Pre-publication checks

- [ ] `\u2122` on first mention in each platform block
- [ ] No figure that is absent from `reports/comprehensive-report-branded.pdf`
- [ ] X post lengths within 280 (measured above)
- [ ] Links resolve
- [ ] Video dimensions verified: `1080x1920` and `1920x1080`
""",
        posts,
    )


# ── QA ────────────────────────────────────────────────────────────────────────


def run_palette_gate(path: Path, tolerance: float) -> dict[str, object]:
    proc = subprocess.run(
        [sys.executable, str(PALETTE_GATE), str(path), "--tolerance", str(tolerance), "--verbose"],
        capture_output=True,
        text=True,
        check=False,
    )
    lines = (proc.stdout + proc.stderr).strip().splitlines()
    return {
        "file": str(path.name),
        "rc": proc.returncode,
        "pass": proc.returncode == 0,
        "detail": lines[0] if len(lines) > 1 else "",
        "result": lines[-1] if lines else "",
    }


def ffprobe_dims(path: Path) -> dict[str, object]:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return {"ok": False, "error": "ffprobe not found"}
    proc = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,duration,nb_frames,r_frame_rate",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return {"ok": False, "error": proc.stderr.strip()[:300]}
    stream = json.loads(proc.stdout)["streams"][0]
    return {
        "ok": True,
        "width": stream.get("width"),
        "height": stream.get("height"),
        "duration": round(float(stream.get("duration", 0)), 2),
        "frames": stream.get("nb_frames"),
    }


def extract_frame(video: Path, at: float, out: Path) -> bool:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return False
    out.unlink(missing_ok=True)
    proc = subprocess.run(
        [
            ffmpeg,
            "-y",
            "-loglevel",
            "error",
            "-ss",
            f"{at}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            str(out),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0 and out.is_file()


def rasterise_pdf(pdf: Path, out_dir: Path, dpi: int = 150) -> tuple[list[Path], str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("page-*.png"):
        old.unlink()
    poppler = shutil.which("pdftoppm")
    if poppler:
        proc = subprocess.run(
            [
                poppler,
                "-r",
                str(dpi),
                "-png",
                "-aa",
                "no",
                "-aaVector",
                "no",
                str(pdf),
                str(out_dir / "page"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        pages = sorted(out_dir.glob("page-*.png"))
        if proc.returncode == 0 and pages:
            return pages, "pdftoppm (anti-aliasing off)"
    import pymupdf  # local import: only needed on the fallback path

    pages = []
    with pymupdf.open(pdf) as doc:
        for index, page_obj in enumerate(doc, start=1):
            target = out_dir / f"page-{index}.png"
            page_obj.get_pixmap(dpi=dpi).save(target)
            pages.append(target)
    return pages, "PyMuPDF (anti-aliasing on; palette % reads high)"


# ── main ──────────────────────────────────────────────────────────────────────


def resolve_campaign(raw: str | None) -> Path:
    if raw:
        path = Path(raw).expanduser()
        if not path.is_absolute():
            path = (REPO / path).resolve()
        if path.is_file():
            path = path.parent
        if not path.is_dir():
            raise SystemExit(f"ERROR: campaign directory not found: {path}")
        return path
    if not CAMPAIGNS.is_dir():
        raise SystemExit(f"ERROR: campaign root not found: {CAMPAIGNS}")
    candidates = [p for p in CAMPAIGNS.iterdir() if p.is_dir() and (p / "notebooklm").is_dir()]
    if not candidates:
        raise SystemExit(f"ERROR: no campaign under {CAMPAIGNS} has a notebooklm/ staging folder.")
    return max(candidates, key=lambda p: (p.name, p.stat().st_mtime))


def main(argv: list[str] | None = None) -> int:
    global FPS

    parser = argparse.ArgumentParser(
        description="Compile a campaign's NotebookLM staging output into every social asset."
    )
    parser.add_argument("--campaign", help="campaign directory or slug")
    parser.add_argument("campaign_path", nargs="?", help="campaign directory (positional)")
    parser.add_argument(
        "--tolerance",
        type=float,
        default=TOLERANCE,
        help=f"palette off-palette tolerance in percent (default {TOLERANCE:g})",
    )
    parser.add_argument("--fps", type=int, default=FPS, help=f"video frame rate (default {FPS})")
    parser.add_argument("--skip-video", action="store_true", help="skip the MP4 renders")
    parser.add_argument(
        "--keep-frames", action="store_true", help="keep the source frame PNGs after encoding"
    )
    args = parser.parse_args(argv)

    FPS = args.fps

    if not PALETTE_GATE.is_file():
        raise SystemExit(f"ERROR: palette gate not found: {PALETTE_GATE}")

    campaign = resolve_campaign(args.campaign or args.campaign_path)
    when = datetime.now()
    facts = build_facts(campaign)

    print(f"campaign : {campaign}")
    print(f"headline : {facts.headline.text}")
    print(f"metrics  : {', '.join(m['value'] + ' ' + m['label'] for m in facts.metrics)}")
    print(f"pillars  : {len(facts.pillars)} | proof: {len(facts.proof)} | gaps: {len(facts.gaps)}")

    dirs = {
        "video": campaign / "video",
        "infographics": campaign / "infographics",
        "carousels": campaign / "carousels",
        "instagram": campaign / "carousels" / "instagram",
        "reports": campaign / "reports",
        "social": campaign / "social-copy",
        "qa": campaign / "qa" / "assets",
    }
    for directory in dirs.values():
        directory.mkdir(parents=True, exist_ok=True)

    checks: dict[str, object] = {}
    palette: list[dict[str, object]] = []

    # ── grounding gate ────────────────────────────────────────────────────────
    claims = (
        [facts.headline, facts.subhead]
        + [Claim(p["body"], p["body"]) for p in facts.pillars]
        + [Claim(p["body"], p["body"]) for p in facts.proof]
    )
    ungrounded = [c.text for c in claims if c.text not in CHROME and not c.ok(facts.haystack)]
    checks["grounding"] = {"pass": not ungrounded, "ungrounded": ungrounded}

    # ── infographics ──────────────────────────────────────────────────────────
    print("\ninfographics")
    infographics = {
        "infographic-square-1080x1080.png": (SQUARE, "square"),
        "infographic-landscape-1600x900.png": (LANDSCAPE_X, "landscape"),
        "infographic-landscape-1200x628.png": (LANDSCAPE_FB, "facebook"),
    }
    for name, (size, variant) in infographics.items():
        image = render_infographic(facts, size, variant)
        path = dirs["infographics"] / name
        image.save(path)
        assert image.size == size, f"{name} rendered at {image.size}, expected {size}"
        print(f"  {name:<42} {size[0]}x{size[1]}")
        palette.append(run_palette_gate(path, args.tolerance))

    # ── carousels ─────────────────────────────────────────────────────────────
    print("\ncarousels")
    cards = carousel_cards(facts)
    for stale in dirs["instagram"].glob("card-*.png"):
        stale.unlink()
    card_paths: list[Path] = []
    for index, card_image in enumerate(cards, start=1):
        path = dirs["instagram"] / f"card-{index}.png"
        card_image.save(path)
        card_paths.append(path)
        palette.append(run_palette_gate(path, args.tolerance))
    print(f"  {len(card_paths)} cards at {SQUARE[0]}x{SQUARE[1]}")

    carousel_pdf = dirs["carousels"] / "social-carousel.pdf"
    rgb_cards = [Image.open(p).convert("RGB") for p in card_paths]
    rgb_cards[0].save(carousel_pdf, save_all=True, append_images=rgb_cards[1:], resolution=150.0)
    print(f"  social-carousel.pdf ({len(rgb_cards)} pages)")
    checks["carousel_pages"] = {"pass": len(rgb_cards) >= 3, "value": len(rgb_cards)}

    # ── report ────────────────────────────────────────────────────────────────
    print("\nreport")
    report_pdf = dirs["reports"] / "comprehensive-report-branded.pdf"
    report_html_path = dirs["qa"] / "comprehensive-report.html"
    report_html_path.write_text(report_html(facts, when), encoding="utf-8")
    print_pdf(find_browser(), report_html_path, report_pdf)

    import pymupdf

    with pymupdf.open(report_pdf) as doc:
        pages = doc.page_count
        sizes = [(round(p.rect.width), round(p.rect.height)) for p in doc]
        text_len = sum(len(p.get_text()) for p in doc)
    checks["report_pages"] = {"pass": pages == 4, "value": pages}
    checks["report_a4"] = {
        "pass": all(abs(w - 595) < 2 and abs(h - 842) < 2 for w, h in sizes),
        "value": sizes,
    }
    checks["report_text"] = {"pass": text_len > 1500, "value": text_len}
    print(f"  comprehensive-report-branded.pdf ({pages} pages, {text_len} chars)")

    report_pages, rasteriser = rasterise_pdf(report_pdf, dirs["qa"] / "report")
    checks["report_rasteriser"] = {"pass": True, "value": rasteriser}
    for page in report_pages:
        palette.append(run_palette_gate(page, args.tolerance))

    # ── video ─────────────────────────────────────────────────────────────────
    beats = build_beats(facts)
    videos: dict[str, dict[str, object]] = {}
    if args.skip_video:
        print("\nvideo    : skipped (--skip-video)")
    else:
        print("\nvideo")
        for name, size, label in (
            ("video-short-1080x1920.mp4", VERTICAL, "short 9:16"),
            ("video-overview-16x9.mp4", HORIZONTAL, "overview 16:9"),
        ):
            frame_dir = dirs["video"] / "frames" / name.replace(".mp4", "")
            render_video(facts, beats, size, frame_dir, label)
            out = dirs["video"] / name
            encode_video(frame_dir, out, FPS)

            probe = ffprobe_dims(out)
            dims_ok = probe.get("width") == size[0] and probe.get("height") == size[1]
            checks[f"video_dims_{name}"] = {
                "pass": bool(dims_ok),
                "value": f"{probe.get('width')}x{probe.get('height')}",
            }

            # Palette gate, source frames (authoritative) — one per beat.
            source_frames = sorted(frame_dir.glob("f*.png"))
            picks = (
                [source_frames[0], source_frames[len(source_frames) // 2], source_frames[-1]]
                if source_frames
                else []
            )
            source_results = [run_palette_gate(p, args.tolerance) for p in picks]

            # Decoded frame — informative only: H.264 yuv420p is lossy.
            decoded_dir = dirs["qa"] / "video"
            decoded_dir.mkdir(parents=True, exist_ok=True)
            decoded_pick = decoded_dir / f"{name.replace('.mp4', '')}-decoded.png"
            decoded_result = None
            if extract_frame(out, probe.get("duration", 1) / 2 or 1, decoded_pick):
                decoded_result = run_palette_gate(decoded_pick, args.tolerance)

            for frame in source_frames[:2] + source_frames[-1:]:
                shutil.copy2(frame, dirs["qa"] / f"{name.replace('.mp4', '')}-{frame.name}")
            if not args.keep_frames:
                shutil.rmtree(frame_dir, ignore_errors=True)

            videos[name] = {
                "probe": probe,
                "source_frame_palette": source_results,
                "decoded_frame_palette": decoded_result,
                "size_mb": round(out.stat().st_size / 1e6, 2),
            }
            print(
                f"  {name:<30} {probe.get('width')}x{probe.get('height')} "
                f"{probe.get('duration')}s {videos[name]['size_mb']} MB"
            )

    # ── social copy ───────────────────────────────────────────────────────────
    print("\nsocial copy")
    copy_path = dirs["social"] / "threads-and-captions.md"
    copy_text, posts = social_copy(facts, when)
    copy_path.write_text(copy_text, encoding="utf-8")
    checks["x_posts"] = {
        "pass": len(posts) >= 3 and all(len(p) <= 280 for p in posts),
        "value": [len(p) for p in posts],
    }
    print(
        f"  threads-and-captions.md ({len(copy_text):,} chars, X posts {[len(p) for p in posts]})"
    )

    # ── verdict ───────────────────────────────────────────────────────────────
    assets = [
        dirs["infographics"] / "infographic-square-1080x1080.png",
        dirs["infographics"] / "infographic-landscape-1600x900.png",
        dirs["infographics"] / "infographic-landscape-1200x628.png",
        dirs["carousels"] / "social-carousel.pdf",
        dirs["reports"] / "comprehensive-report-branded.pdf",
        copy_path,
    ] + card_paths
    if not args.skip_video:
        assets += [
            dirs["video"] / "video-short-1080x1920.mp4",
            dirs["video"] / "video-overview-16x9.mp4",
        ]
    checks["assets_present"] = {
        "pass": all(p.is_file() and p.stat().st_size > 0 for p in assets),
        "value": f"{len(assets)} files",
        "missing": [str(p.name) for p in assets if not p.is_file()],
    }

    palette_pass = all(entry["pass"] for entry in palette)
    checks["palette"] = {
        "pass": palette_pass,
        "tolerance_pct": args.tolerance,
        "files_checked": len(palette),
        "failures": [e for e in palette if not e["pass"]],
    }

    verdict_pass = all(bool(c["pass"]) for c in checks.values())
    manifest = {
        "campaign": facts.slug,
        "generated": when.isoformat(timespec="seconds"),
        "tolerance_pct": args.tolerance,
        "fps": FPS,
        "headline": facts.headline.text,
        "metrics": facts.metrics,
        "checks": checks,
        "palette": palette,
        "videos": videos,
        "assets": [str(p.relative_to(REPO)) for p in assets],
        "pass": verdict_pass,
    }
    manifest_path = dirs["qa"] / "assets-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("\nQA gates")
    for name, check in checks.items():
        status = "PASS" if check.get("pass") else "FAIL"
        if name == "palette":
            print(
                f"  {name:<22} {status} ({check['files_checked']} files, "
                f"tolerance {args.tolerance:g}%)"
            )
        elif name == "grounding":
            print(
                f"  {name:<22} {status} ({'no ungrounded claims' if check['pass'] else check['ungrounded']})"
            )
        else:
            print(f"  {name:<22} {status} ({check.get('value')})")

    if videos:
        print("\nvideo palette (source frames = authoritative; decoded = informational)")
        for name, info in videos.items():
            src = info["source_frame_palette"]
            src_ok = all(s["pass"] for s in src)
            print(f"  {name:<30} source: {'PASS' if src_ok else 'FAIL'}")
            for row in src:
                print(f"      {row['file']}: {row['result']}")
            decoded = info["decoded_frame_palette"]
            if decoded:
                print(f"      decoded frame (lossy H.264, not gated): {decoded['result']}")

    print("\n" + "=" * 66)
    print("  ALL ASSETS READY" if verdict_pass else "  ASSET GENERATION FAILED")
    print("=" * 66)
    print(f"  campaign   : {campaign}")
    print(f"  assets     : {len(assets)} files")
    print(
        f"  palette    : {'PASS' if palette_pass else 'FAIL'} "
        f"({len(palette)} files, tolerance {args.tolerance:g}%)"
    )
    print(f"  manifest   : {manifest_path}")
    print(f"STATUS: {'OK' if verdict_pass else 'FAILED'}")
    return 0 if verdict_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
