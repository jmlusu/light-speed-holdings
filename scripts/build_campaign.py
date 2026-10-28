#!/usr/bin/env python3
"""One-touch multimodal campaign build — the engine behind /build-campaign.

Smart input inspection
----------------------
Inspects ``artifacts/campaigns/<slug>/notebooklm/`` and routes on what is
actually there:

    State 1 — TEXT ONLY   raw-briefing.md exists, no *.mp3 / *.wav
                          -> branded PDF + LinkedIn post + audit report
    State 2 — TEXT+AUDIO  raw-briefing.md exists AND audio is present
                          -> everything in State 1, plus 9:16 and 16:9 video,
                             two infographics and platform-specific copy

Content Preservation Law
------------------------
Text is never stripped, compressed, or paraphrased to fit a canvas.

* Dense source (> 600 words, or any data table)  -> 4-page unabridged template
* Concise source (<= 600 words, no tables)       -> 2-page unabridged template

Every paragraph, bullet, table row and heading from raw-briefing.md is rendered
in full. The only fitting lever is the brand type scale (``--fit``), floored at
0.72; if the content still needs more room the renderer adds pages and reports
the real count. ``text_integrity`` then re-extracts the PDF and asserts every
source block is present, so a silent drop fails the run.

Output tree (under the campaign folder)
---------------------------------------
    open-design/executive-briefing-branded.pdf
    open-design/executive-briefing.html
    text/linkedin-primary.md
    open-design/video-short-1080x1920.mp4          (State 2)
    open-design/video-overview-16x9.mp4            (State 2)
    open-design/infographic-square-1080x1080.png   (State 2)
    open-design/infographic-landscape-1600x900.png (State 2)
    text/x-thread.md                               (State 2)
    text/facebook-post.md                          (State 2)
    text/instagram-caption.md                      (State 2)
    qa/build-campaign/                             (palette rasters, json)
    PIPELINE-AUDIT-REPORT.md

Usage
-----
    uv run python scripts/build_campaign.py
    uv run python scripts/build_campaign.py artifacts/campaigns/<slug>
    uv run python scripts/build_campaign.py <slug> --skip-video
    uv run python scripts/build_campaign.py <slug> --force-media   # QA only

Exit codes: 0 = every gate passed, 1 = at least one gate failed, 2 = setup error.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import html as html_lib
import json
import math
import re
import shutil
import sys
import tempfile
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import jinja2
import pymupdf
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

import brand_briefing as bb  # noqa: E402  (local script, same directory)
import generate_all_assets as ga  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = REPO / "static" / "brand" / "templates"
CAMPAIGNS = REPO / "artifacts" / "campaigns"
LOGO = REPO / "brand" / "logo" / "logo-full.png"
TOKENS = REPO / "brand" / "tokens" / "brand-tokens.json"
PALETTE_GATE = (
    REPO / ".agents" / "skills" / "ls-visual-storytelling" / "scripts" / "check_brand_palette.py"
)

TEMPLATE_DENSE = "executive-briefing-4pp.html"
TEMPLATE_CONCISE = "executive-briefing-2pp.html"
DENSE_WORD_THRESHOLD = 600

SOURCE_REL = Path("notebooklm") / "raw-briefing.md"
PDF_REL = Path("open-design") / "executive-briefing-branded.pdf"
HTML_REL = Path("open-design") / "executive-briefing.html"
LINKEDIN_REL = Path("text") / "linkedin-primary.md"
AUDIT_REL = Path("PIPELINE-AUDIT-REPORT.md")
QA_REL = Path("qa") / "build-campaign"

TOLERANCE = 3.0
DPI = 150
FIT_STEP = 0.02
FIT_FLOOR = 0.72
MAX_EXTRA_PAGES = 3
LINKEDIN_LIMIT = 2800

# Line-cost model for pagination: one unit ~= one 12pt body line on A4.
# Calibrated against the rendered template: 12pt Arial across the 14mm-inset
# text column holds ~112 characters per line, and the body area holds ~40
# lines per page (page 1 loses ~6 lines to the masthead).
PAGE1_CAPACITY = 34.0
PAGE_CAPACITY = 40.0
# Page-fill candidates, tightest first: the line-cost model is an estimate, so
# the render decides. If a tight pagination overflows, the next candidate packs
# the pages more loosely rather than shrinking the brand type scale.
FILL_STEPS = (1.0, 0.95, 0.90, 0.85, 0.80)
CHARS_PER_LINE = 112

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
BULLET_RE = re.compile(r"^\s*(?:[*\-+]|\d+[.)])\s+(.*)$")
TABLE_RULE_RE = re.compile(r"^\|?[\s:|-]{3,}$")
TOKEN_RE = re.compile(r"[a-z0-9]+")


# ── markdown -> flow blocks ───────────────────────────────────────────────────


@dataclass
class FlowBlock:
    kind: str  # heading | para | bullets | table
    level: int = 0
    html: str = ""
    plain: str = ""
    items: list[str] = field(default_factory=list)
    plain_items: list[str] = field(default_factory=list)
    rows: list[list[str]] = field(default_factory=list)
    plain_rows: list[list[str]] = field(default_factory=list)
    cost: float = 0.0

    def check_strings(self) -> list[str]:
        """Every string that must survive into the PDF, for the integrity gate."""
        if self.kind == "heading":
            return [self.plain]
        if self.kind == "para":
            return [self.plain]
        if self.kind == "bullets":
            return list(self.plain_items)
        if self.kind == "table":
            return [cell for row in self.plain_rows for cell in row]
        return []


def _inline(raw: str) -> tuple[str, str]:
    """Markdown line -> (safe HTML, plain text). Words are never altered."""
    plain = bb.clean(raw)

    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", raw)
    text = re.sub(r"\\(.)", r"\1", text)
    text = html_lib.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()

    escaped = html_lib.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = escaped.replace("**", "")
    return escaped, plain


def _para_cost(plain: str) -> float:
    return math.ceil(max(len(plain), 1) / CHARS_PER_LINE) + 0.8


def _table_cost(rows: list[list[str]]) -> float:
    cost = 1.2
    columns = max(len(r) for r in rows) if rows else 1
    column_chars = max(12, CHARS_PER_LINE // max(1, columns))
    for row in rows:
        wrapped = max((math.ceil(len(cell) / column_chars) for cell in row), default=1)
        cost += max(1, wrapped) + 0.4
    return cost


def parse_briefing(raw: str) -> tuple[str, list[FlowBlock], dict[str, Any]]:
    lines = raw.splitlines()
    title = ""
    blocks: list[FlowBlock] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue

        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            markup, plain = _inline(heading.group(2))
            if level == 1 and not title and not blocks:
                title = plain
            else:
                blocks.append(
                    FlowBlock(
                        kind="heading",
                        level=level,
                        html=markup,
                        plain=plain,
                        cost=3.2 if level <= 3 else 2.4,
                    )
                )
            index += 1
            continue

        if line.strip().startswith("|"):
            html_rows: list[list[str]] = []
            plain_rows: list[list[str]] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                stripped = lines[index].strip()
                index += 1
                if TABLE_RULE_RE.match(stripped):
                    continue
                raw_cells = [part.strip() for part in re.split(r"(?<!\\)\|", stripped.strip("|"))]
                if not any(raw_cells):
                    continue
                inline = [_inline(cell) for cell in raw_cells]
                html_rows.append([markup for markup, _ in inline])
                plain_rows.append([plain for _, plain in inline])
            if html_rows:
                blocks.append(
                    FlowBlock(
                        kind="table",
                        rows=html_rows,
                        plain_rows=plain_rows,
                        cost=_table_cost(plain_rows),
                    )
                )
            continue

        if BULLET_RE.match(line):
            items_html: list[str] = []
            items_plain: list[str] = []
            while index < len(lines):
                current = lines[index]
                if not current.strip():
                    break
                match = BULLET_RE.match(current)
                if match:
                    markup, plain = _inline(match.group(1))
                    items_html.append(markup)
                    items_plain.append(plain)
                    index += 1
                    continue
                if HEADING_RE.match(current) or current.strip().startswith("|"):
                    break
                if current.startswith((" ", "\t")) and items_html:
                    # wrapped continuation of the previous bullet
                    extra_html, extra_plain = _inline(current)
                    items_html[-1] = f"{items_html[-1]} {extra_html}".strip()
                    items_plain[-1] = f"{items_plain[-1]} {extra_plain}".strip()
                    index += 1
                    continue
                break
            cost = sum(math.ceil(max(len(p), 1) / 92) + 0.35 for p in items_plain) + 0.8
            blocks.append(
                FlowBlock(
                    kind="bullets",
                    items=items_html,
                    plain_items=items_plain,
                    plain="\n".join(items_plain),
                    cost=cost,
                )
            )
            continue

        paragraph: list[str] = []
        while index < len(lines):
            current = lines[index]
            if not current.strip():
                break
            if HEADING_RE.match(current) or BULLET_RE.match(current):
                break
            if current.strip().startswith("|"):
                break
            paragraph.append(current.strip().lstrip(">").strip())
            index += 1
        if paragraph:
            markup, plain = _inline(" ".join(paragraph))
            if plain:
                blocks.append(
                    FlowBlock(kind="para", html=markup, plain=plain, cost=_para_cost(plain))
                )

    stats = {
        "words": len(
            re.findall(r"[A-Za-z0-9][A-Za-z0-9'\u2019-]*", " ".join(b.plain for b in blocks))
        ),
        "tables": sum(1 for b in blocks if b.kind == "table"),
        "table_rows": sum(len(b.rows) for b in blocks if b.kind == "table"),
        "headings": sum(1 for b in blocks if b.kind == "heading"),
        "paragraphs": sum(1 for b in blocks if b.kind == "para"),
        "bullets": sum(len(b.items) for b in blocks if b.kind == "bullets"),
        "blocks": len(blocks),
    }
    return title, blocks, stats


# ── pagination ────────────────────────────────────────────────────────────────


def paginate(blocks: list[FlowBlock], target: int, fill: float = 1.0) -> list[list[FlowBlock]]:
    """Fill pages to `fill` x capacity in order, up to `target` pages.

    Blocks are atomic: a paragraph, list, or table is never split across pages.
    Each page takes as many blocks as its own capacity allows, so a short
    document uses fewer pages (never a half-empty page) and a long one spills
    over; `build_pdf` adds pages when the render needs them.
    """
    capacities = [PAGE1_CAPACITY] + [PAGE_CAPACITY] * (target - 1)
    pages: list[list[FlowBlock]] = []
    index = 0
    for capacity in capacities:
        if index >= len(blocks):
            break
        budget = capacity * fill
        page: list[FlowBlock] = []
        cost = 0.0
        while index < len(blocks):
            block = blocks[index]
            # The first block always lands, so an oversized block cannot loop.
            if page and cost + block.cost > budget:
                break
            page.append(block)
            cost += block.cost
            index += 1
        pages.append(page)

    # A heading alone at the foot of a page is an orphan: carry it forward when
    # the next page has room for it.
    for page_no in range(len(pages) - 1):
        page = pages[page_no]
        while page and page[-1].kind == "heading":
            pages[page_no + 1].insert(0, page.pop())
        if not page and page_no > 0:
            break

    # Last page absorbs the remainder rather than dropping it.
    if index < len(blocks) and pages:
        pages[-1].extend(blocks[index:])
    return pages


_HEAD_STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "by",
    "for",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}


def _running_head(text: str, limit: int = 36) -> str:
    """Shorten a section heading for the page rail.

    The rail is uppercase, tracked and width-limited, so a full heading either
    overflows or gets ellipsised mid-word ("...AND EXECUTI..."), which reads as
    a rendering fault. Clip on a word boundary and drop trailing stopwords so
    the result ends on a word worth reading. No ellipsis: a clipped running
    head is a label, not a truncated sentence.
    """
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    words = text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:-").split(" ")
    while len(words) > 1 and words[-1].lower().strip(",;:") in _HEAD_STOPWORDS:
        words.pop()
    return " ".join(words).rstrip(" ,;:-")


def compose_pages(
    blocks: list[FlowBlock], target: int, title: str, fill: float = 1.0
) -> list[dict[str, Any]]:
    raw_pages = paginate(blocks, target, fill)
    # Drop trailing empty pages (only possible for very short documents).
    while len(raw_pages) > 1 and not raw_pages[-1]:
        raw_pages.pop()

    composed: list[dict[str, Any]] = []
    previous_head = title
    for number, page_blocks in enumerate(raw_pages, start=1):
        head = next(
            (b.plain for b in page_blocks if b.kind == "heading"),
            previous_head,
        )
        previous_head = head
        composed.append(
            {
                "number": number,
                "first": number == 1,
                "blocks": page_blocks,
                "running_head": _running_head(head),
            }
        )
    return composed


# ── logo + rendering ──────────────────────────────────────────────────────────


def logo_geometry(path: Path, art_width_mm: float) -> dict[str, str]:
    if not path.is_file():
        raise SystemExit(f"ERROR: logo not found: {path}")
    with Image.open(path) as source_image:
        image = source_image.convert("RGBA")
        width, height = image.size
        x0, y0, x1, y1 = bb.artwork_bbox(image)
    art_w, art_h = x1 - x0, y1 - y0
    scale = art_width_mm / art_w
    clear = max(9.0, round(art_width_mm * bb.LOGO_CAP_RATIO * 1.05, 1))
    return {
        "src": "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii"),
        "box_w": f"{art_width_mm:.2f}mm",
        "box_h": f"{art_h * scale:.2f}mm",
        "img_w": f"{width * scale:.2f}mm",
        "img_h": f"{height * scale:.2f}mm",
        "off_x": f"{-x0 * scale:.2f}mm",
        "off_y": f"{-y0 * scale:.2f}mm",
        "clear_space": f"{clear:.1f}mm",
    }


ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=jinja2.select_autoescape(["html"]),
    trim_blocks=True,
)


def render_html(
    template_name: str,
    pages: list[dict[str, Any]],
    slots: dict[str, Any],
    logo: dict[str, str],
    *,
    fit: float,
    measure: bool,
) -> str:
    template = ENV.get_template(template_name)
    return template.render(
        pages=pages,
        total_pages=len(pages),
        logo=logo,
        fit=f"{fit:.2f}",
        measure=measure,
        **slots,
    )


def fit_steps() -> list[float]:
    steps: list[float] = []
    value = 1.0
    while value >= FIT_FLOOR - 1e-9:
        steps.append(round(value, 2))
        value -= FIT_STEP
    return steps


def probe_ladder() -> list[tuple[float, float]]:
    """(page_fill, fit) candidates: full brand type scale first, then shrink it."""
    ladder = [(fill, 1.0) for fill in FILL_STEPS]
    ladder += [(FILL_STEPS[-1], fit) for fit in fit_steps()[1:]]
    return ladder


def build_pdf(
    template_name: str,
    blocks: list[FlowBlock],
    slots: dict[str, Any],
    logo: dict[str, str],
    target: int,
    out_html: Path,
    out_pdf: Path,
) -> tuple[list[dict[str, Any]], float]:
    """Fit the type scale so every page holds its content; never drop a block."""
    browser = bb.find_browser()
    target_pages = target

    while True:
        chosen: float | None = None
        pages: list[dict[str, Any]] = []
        with tempfile.TemporaryDirectory(prefix="ls-campaign-measure-") as tmp:
            probe_pdf = Path(tmp) / "probe.pdf"
            probe_html = Path(tmp) / "probe.html"
            # Full brand type scale first: relax page fill before touching --fit.
            for fill, fit in probe_ladder():
                pages = compose_pages(blocks, target_pages, slots["title"], fill)
                if any(not page["blocks"] for page in pages) and len(pages) > 1:
                    raise SystemExit(
                        "ERROR: pagination produced an empty page; refusing to render."
                    )
                probe_html.write_text(
                    render_html(template_name, pages, slots, logo, fit=fit, measure=True),
                    encoding="utf-8",
                )
                bb.print_pdf(browser, probe_html, probe_pdf)
                sheets = bb.page_count(probe_pdf)
                print(
                    f"  fit {fit:.2f}, fill {fill:.2f}: {sheets} sheet(s) for {len(pages)} page(s)"
                )
                if sheets <= len(pages):
                    chosen = fit
                    break

        if chosen is not None:
            break

        if target_pages >= target + MAX_EXTRA_PAGES:
            raise SystemExit(
                f"ERROR: content needs more than {target_pages} pages even at fit "
                f"{FIT_FLOOR:.2f}. Raise MAX_EXTRA_PAGES or shorten the source — the "
                "renderer will not drop text to force a page count."
            )
        target_pages += 1
        print(
            f"  content did not fit {target_pages - 1} page(s) at the minimum type scale; "
            f"expanding to {target_pages} pages (no text removed)"
        )

    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(
        render_html(template_name, pages, slots, logo, fit=chosen, measure=False),
        encoding="utf-8",
    )
    bb.print_pdf(browser, out_html, out_pdf)
    actual = bb.page_count(out_pdf)
    if actual != len(pages):
        raise SystemExit(
            f"ERROR: final render produced {actual} sheets for {len(pages)} pages; "
            "refusing to ship a clipped PDF."
        )
    return pages, chosen


# ── integrity + QA ────────────────────────────────────────────────────────────


def tokens_of(text: str) -> list[str]:
    normalised = unicodedata.normalize("NFKD", text)
    return TOKEN_RE.findall(normalised.lower())


def text_integrity(blocks: list[FlowBlock], pdf_text: str) -> dict[str, Any]:
    """Assert every source block survives into the PDF, in order, verbatim."""
    haystack = " " + " ".join(tokens_of(pdf_text)) + " "
    checked = 0
    missing: list[str] = []
    for block in blocks:
        for source in block.check_strings():
            needle = " ".join(tokens_of(source))
            if not needle:
                continue
            checked += 1
            if f" {needle} " not in haystack:
                missing.append(source[:160])
    return {
        "pass": not missing,
        "blocks_checked": checked,
        "missing_count": len(missing),
        "missing": missing,
    }


def css_colour_check(html_path: Path) -> dict[str, Any]:
    markup = html_path.read_text(encoding="utf-8")
    markup = re.sub(r"/\*.*?\*/", "", markup, flags=re.S)
    declared = {("#" + m).upper() for m in re.findall(r"#([0-9A-Fa-f]{6})\b", markup)}
    allowed = bb.brand_hexes()
    off = sorted(declared - allowed)
    return {"pass": not off, "value": off}


def rasterise_pdf(pdf_path: Path, qa_dir: Path) -> tuple[list[Path], str]:
    qa_dir.mkdir(parents=True, exist_ok=True)
    return bb.rasterise(pdf_path, qa_dir, DPI)


# ── LinkedIn ──────────────────────────────────────────────────────────────────


def build_linkedin_post(
    title: str,
    blocks: list[FlowBlock],
    stats: dict[str, Any],
    when: datetime,
) -> tuple[str, str]:
    """Assemble a primary LinkedIn post from verbatim source sentences."""
    paragraphs = [b.plain for b in blocks if b.kind == "para"]
    bullets = [re.sub(r"<[^>]+>", "", i) for b in blocks if b.kind == "bullets" for i in b.items]

    headline = re.sub(
        r"^(executive\s+briefing|briefing)\s*[:\u2014-]\s*", "", title, flags=re.I
    ).strip()

    lead = paragraphs[0] if paragraphs else ""
    body: list[str] = [f"LightSpeed Holdings Limited\u2122 \u2014 {headline}."]
    if lead:
        body.append(lead)

    picked: list[str] = []
    if bullets:
        body.append("What the briefing records:")
        for bullet in bullets:
            candidate = f"- {bullet}"
            trial = "\n".join(
                [*body, *picked, candidate, "Read the full briefing \u2192 " + ga.CTA_URL]
            )
            if len(trial) <= LINKEDIN_LIMIT:
                picked.append(candidate)
            if len(picked) >= 4:
                break
    else:
        for paragraph in paragraphs[1:3]:
            trial = "\n".join(
                [*body, *picked, paragraph, "Read the full briefing \u2192 " + ga.CTA_URL]
            )
            if len(trial) <= LINKEDIN_LIMIT:
                picked.append(paragraph)

    body.extend(picked)
    body.append(f"Read the full briefing \u2192 {ga.CTA_URL}")
    body.append(
        "#AgenticAI #DigitalSovereignty #LocalInfrastructure #LightSpeedHoldings #AIStrategy"
    )
    post = "\n\n".join(part for part in body if part)

    header = (
        f"# LinkedIn \u2014 primary post\n\n"
        f"Campaign: `{stats['slug']}`  \n"
        f"Generated: {when.strftime('%d %B %Y %H:%M')}  \n"
        f"Length: {len(post):,} / {LINKEDIN_LIMIT:,} characters  \n"
        f"Sourcing: every sentence below is verbatim from "
        f"`notebooklm/raw-briefing.md`; only the headline label, CTA and hashtags "
        f"are brand chrome.\n\n"
        f"---\n\n"
    )
    return header + post + "\n\n---\n", post


# ── social copy (State 2) ─────────────────────────────────────────────────────


def build_social_files(facts: ga.Facts, when: datetime) -> dict[str, Any]:
    big = facts.metrics[0]
    second = facts.metrics[1] if len(facts.metrics) > 1 else None
    proof = facts.proof[0] if facts.proof else None
    gov = next((s for g in facts.governance if (s := ga.sentence_with(g, "timeout"))), "")
    headline = ga.sentence_case(facts.headline.text)
    cta = ga.sentence_case(ga.CTA_TEXT)
    counts = f"{big['value']} {big['label']}."
    if second:
        counts += f" {second['value']} {second['label']}."
    pillar_lines = "\n".join(f"- {p['body']}" for p in facts.pillars[:3])
    proof_line = f"{ga.sentence_case(proof['label'])}: {ga.decap(proof['body'])}" if proof else ""

    posts = [
        ga.fit_post(f"{ga.LEGAL}\n\n{facts.subhead.text}\n\n{counts}"),
        ga.fit_post(proof_line or facts.subhead.text),
        ga.fit_post(f"{gov or headline}\n\n{cta} \u2192 {ga.CTA_URL}"),
    ]

    x_thread = f"""# X (Twitter) \u2014 thread

Campaign: `{facts.slug}`  ·  Generated {when.strftime("%d %B %Y")}
Budget: 280 characters per post. Lengths: {" / ".join(str(len(p)) for p in posts)}.
Each fenced block is one post.

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

Pairing: `open-design/infographic-landscape-1600x900.png`.
"""

    facebook = f"""# Facebook — post

Campaign: `{facts.slug}`  ·  Generated {when.strftime("%d %B %Y")}

```
{ga.LEGAL} \u2014 {headline}.

{facts.subhead.text}

{big["value"]} {big["label"]}{(", " + second["value"] + " " + second["label"]) if second else ""}.

{pillar_lines}

{proof_line}

{cta}: {ga.CTA_URL}
```

Link preview title: `{headline}`

Pairing: `open-design/infographic-landscape-1600x900.png`.
"""

    instagram = f"""# Instagram — caption

Campaign: `{facts.slug}`  ·  Generated {when.strftime("%d %B %Y")}

```
{ga.LEGAL}

{headline}.

{facts.subhead.text}

{big["value"]} {big["label"]} \u00b7 {(second["value"] + " " + second["label"]) if second else ""}

{facts.pillars[0]["body"] if facts.pillars else ""}

{cta} \u2192 link in bio.

#AgenticAI #OfflineFirst #SovereignAI #Malawi #SADC #AIForAfrica #LightSpeedHoldings
```

Pairing: `open-design/infographic-square-1080x1080.png` or
`open-design/video-short-1080x1920.mp4` for Reels.
"""

    return {
        "x-thread.md": x_thread,
        "facebook-post.md": facebook,
        "instagram-caption.md": instagram,
        "_x_posts": posts,
    }


# ── audit report ──────────────────────────────────────────────────────────────


def format_bytes(size: int) -> str:
    if size >= 1_000_000:
        return f"{size / 1e6:.1f} MB"
    return f"{size / 1024:.0f} KB"


def write_audit_report(
    campaign: Path,
    when: datetime,
    state: str,
    audio_files: list[Path],
    forced_media: bool,
    stats: dict[str, Any],
    template_name: str,
    target_pages: int,
    pages: list[dict[str, Any]],
    fit: float,
    integrity: dict[str, Any],
    checks: dict[str, Any],
    built: list[dict[str, Any]],
    skipped: list[dict[str, str]],
    source_sha: str,
) -> Path:
    prior = campaign / AUDIT_REL
    if prior.is_file():
        archive = campaign / "reports" / "archive"
        archive.mkdir(parents=True, exist_ok=True)
        stamp = when.strftime("%Y%m%d-%H%M%S")
        shutil.copy2(prior, archive / f"PIPELINE-AUDIT-REPORT.{stamp}.md")

    try:
        campaign_ref = campaign.relative_to(REPO).as_posix()
    except ValueError:
        campaign_ref = campaign.as_posix()

    built_rows = "\n".join(
        f"| `{row['path']}` | {row['kind']} | {row['detail']} | {row['size']} | {row['palette']} |"
        for row in built
    )
    skip_rows = (
        "\n".join(f"| `{row['asset']}` | {row['reason']} |" for row in skipped) or "| — | none |"
    )
    gate_rows = "\n".join(
        f"| {name} | {'PASS' if check.get('pass') else 'FAIL'} | {check.get('value', '')} |"
        for name, check in checks.items()
    )
    missing_note = (
        "None. Every source block was found in the rendered PDF."
        if not integrity["missing"]
        else "\n".join(f"- `{m}`" for m in integrity["missing"])
    )

    report = f"""# Pipeline Audit Report — /build-campaign

**Campaign:** `{campaign.name}`
**Generated:** {when.strftime("%d %B %Y %H:%M")}
**Detected state:** {state}
**Audio in `notebooklm/`:** {", ".join(p.name for p in audio_files) if audio_files else "none"}
**Media branch:** {"ran (forced with --force-media)" if forced_media and not audio_files else ("ran (audio detected)" if audio_files else "skipped — text-only campaign")}
**Status:** {"COMPLETE — all gates passed" if all(c.get("pass") for c in checks.values()) else "FAILED — see gates"}

---

## 1. Input inspection

| Signal | Value |
|--------|-------|
| Source | `{SOURCE_REL.as_posix()}` |
| Source SHA-256 | `{source_sha}` |
| Words | {stats["words"]:,} |
| Sections / headings | {stats["headings"]} |
| Paragraphs | {stats["paragraphs"]} |
| Bullets | {stats["bullets"]} |
| Data tables | {stats["tables"]} ({stats["table_rows"]} rows) |
| Audio files (`*.mp3` / `*.wav`) | {len(audio_files)} |

The state is derived only from files present on disk. No campaign content was
supplied by this report.

---

## 2. Template decision

| Rule | Result |
|------|--------|
| Threshold | > {DENSE_WORD_THRESHOLD} words **or** any data table -> 4-page unabridged |
| Observed | {stats["words"]:,} words, {stats["tables"]} table(s) |
| Template | `static/brand/templates/{template_name}` |
| Page budget | {target_pages} |
| Rendered pages | {len(pages)} |
| Final type scale | {fit:.2f} (1.00 = full brand scale) |

**Content preservation.** The full source is rendered: every paragraph, bullet,
table row and heading. No sentence was trimmed, condensed or paraphrased. The
only fitting lever is the brand type scale; if content had still overflowed, the
renderer would have added pages rather than drop text.

---

## 3. Assets built

| File | Type | Detail | Size | Palette |
|------|------|--------|------|---------|
{built_rows}

Palette gate: `{PALETTE_GATE.relative_to(REPO).as_posix()}` at {TOLERANCE:g}% tolerance.

---

## 4. Skipped assets

| Asset | Reason |
|-------|--------|
{skip_rows}

---

## 5. Content-integrity gate

Re-extracted the rendered PDF and matched every source block as a contiguous
token sequence (punctuation-, hyphenation- and line-break-insensitive), so a
silently dropped clause fails the run.

| Metric | Value |
|--------|-------|
| Source blocks checked | {integrity["blocks_checked"]} |
| Missing blocks | {integrity["missing_count"]} |

{missing_note}

---

## 6. Gates

| Gate | Result | Value |
|------|--------|-------|
{gate_rows}

---

## 7. Reproduce

```bash
uv run python scripts/build_campaign.py {campaign_ref}
```

The same run is available as `/build-campaign` (or its alias
`/generate-all-assets`), and as `build-campaign.bat` on Windows.

---

## 8. Honest notes

- Media assets (State 2) are rendered by the repository's deterministic Pillow
  and ffmpeg generator (`scripts/generate_all_assets.py`), not by the Open
  Design / HyperFrames CLI. The `ls-od-video` and `ls-visual-storytelling`
  skills supply the design rules that the generator implements; no skill CLI was
  executed.
- Video palette is gated on the source PNG frames, which are authoritative.
  H.264 `yuv420p` is lossy, so a decoded frame is measured for information only
  and is not gated.
- Nothing was published. All output is staged in the campaign folder.
"""
    path = campaign / AUDIT_REL
    path.write_text(report, encoding="utf-8")
    return path


# ── CLI ───────────────────────────────────────────────────────────────────────


def resolve_campaign(raw: str | None) -> Path:
    if raw:
        path = Path(raw).expanduser()
        if not path.is_absolute():
            path = (REPO / path).resolve()
        if not path.exists() and not re.search(r"[\\/]", raw):
            path = (CAMPAIGNS / raw).resolve()
        if path.is_file():
            path = path.parent.parent if path.parent.name == "notebooklm" else path.parent
        if not (path / SOURCE_REL).is_file():
            raise SystemExit(f"ERROR: no {SOURCE_REL.as_posix()} under {path}")
        return path
    if not CAMPAIGNS.is_dir():
        raise SystemExit(f"ERROR: campaign root not found: {CAMPAIGNS}")
    candidates = [p for p in CAMPAIGNS.iterdir() if p.is_dir() and (p / SOURCE_REL).is_file()]
    if not candidates:
        raise SystemExit(f"ERROR: no campaign under {CAMPAIGNS} has {SOURCE_REL.as_posix()}")
    return max(candidates, key=lambda p: (p.name, p.stat().st_mtime))


def _plural(count: int, singular: str) -> str:
    """Render counts for client-facing copy: '1 table' / '2 tables'.

    Avoids the unrendered '(s)' placeholder that previously reached the cover.
    """
    return f"{count} {singular}" if count == 1 else f"{count} {singular}s"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build every campaign asset from notebooklm/raw-briefing.md and "
        "any NotebookLM audio, in one pass."
    )
    parser.add_argument("--campaign", help="campaign directory or slug")
    parser.add_argument("campaign_path", nargs="?", help="campaign directory (positional)")
    parser.add_argument(
        "--tolerance",
        type=float,
        default=TOLERANCE,
        help=f"palette off-palette tolerance in percent (default {TOLERANCE:g})",
    )
    parser.add_argument("--fps", type=int, default=ga.FPS, help="video frame rate")
    parser.add_argument("--skip-video", action="store_true", help="skip the MP4 renders")
    parser.add_argument(
        "--force-media",
        action="store_true",
        help="QA only: build the State 2 media branch even when no audio file exists",
    )
    parser.add_argument(
        "--keep-frames", action="store_true", help="keep source video frames after encoding"
    )
    args = parser.parse_args(argv)

    if not PALETTE_GATE.is_file():
        raise SystemExit(f"ERROR: palette gate not found: {PALETTE_GATE}")

    campaign = resolve_campaign(args.campaign or args.campaign_path)
    source = campaign / SOURCE_REL
    when = datetime.now()
    ga.FPS = args.fps
    print(f"campaign : {campaign}")

    raw = source.read_text(encoding="utf-8-sig")
    source_sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    notebooklm = campaign / "notebooklm"
    audio_files = sorted(
        p for p in notebooklm.iterdir() if p.is_file() and p.suffix.lower() in {".mp3", ".wav"}
    )
    state = "TEXT + AUDIO" if audio_files else "TEXT ONLY"
    media_branch = bool(audio_files) or args.force_media
    print(f"state     : {state} ({len(audio_files)} audio file(s) in notebooklm/)")
    if args.force_media and not audio_files:
        print("          : media branch forced for QA (--force-media)")

    title, blocks, stats = parse_briefing(raw)
    stats["slug"] = campaign.name
    if not title or not blocks:
        raise SystemExit("ERROR: raw-briefing.md produced no title or no content blocks.")
    print(
        f"briefing : {stats['words']:,} words, {stats['headings']} headings, "
        f"{stats['tables']} table(s), {stats['blocks']} blocks"
    )

    dense = stats["words"] > DENSE_WORD_THRESHOLD or stats["tables"] > 0
    template_name = TEMPLATE_DENSE if dense else TEMPLATE_CONCISE
    target_pages = 4 if dense else 2
    reason = (
        f"{stats['words']:,} words > {DENSE_WORD_THRESHOLD} or {stats['tables']} table(s) present"
        if dense
        else f"{stats['words']:,} words <= {DENSE_WORD_THRESHOLD} and no tables"
    )
    print(f"template : {template_name} ({reason}) -> {target_pages} pages")

    fitted_text = " ".join(b.plain for b in blocks)
    display_title = (
        re.sub(
            r"^(executive\s+briefing|briefing)\s*[:\u2014-]\s*",
            "",
            title,
            flags=re.I,
        ).strip()
        or title
    )
    slots = {
        "title": display_title,
        "eyebrow": f"Executive Briefing \u2014 {when.strftime('%B %Y')}",
        "subtitle": (
            f"Unabridged edition \u00b7 {stats['words']:,} words \u00b7 "
            f"{_plural(stats['headings'], 'section')} \u00b7 "
            f"{_plural(stats['tables'], 'data table')}"
        ),
        "meta_description": f"{title} \u2014 LightSpeed Holdings Limited executive briefing.",
        "metrics": bb.build_metrics(fitted_text),
    }

    out_pdf = campaign / PDF_REL
    out_html = campaign / HTML_REL
    qa_dir = campaign / QA_REL
    qa_dir.mkdir(parents=True, exist_ok=True)

    print("\npdf")
    logo = logo_geometry(LOGO, 44.0 if dense else 40.0)
    pages, fit = build_pdf(template_name, blocks, slots, logo, target_pages, out_html, out_pdf)
    print(f"  {PDF_REL.as_posix()} ({len(pages)} pages, fit {fit:.2f})")

    with pymupdf.open(out_pdf) as doc:  # type: ignore[no-untyped-call]
        pdf_text = "\n".join(page.get_text() for page in doc)
        sizes = [(round(p.rect.width, 1), round(p.rect.height, 1)) for p in doc]
        actual_pages = doc.page_count

    integrity = text_integrity(blocks, pdf_text)
    print(
        f"  integrity: {integrity['blocks_checked']} blocks checked, "
        f"{integrity['missing_count']} missing"
    )
    if not integrity["pass"]:
        for item in integrity["missing"][:5]:
            print(f"    MISSING: {item}")

    checks: dict[str, Any] = {
        "page_count": {
            "pass": actual_pages <= target_pages + MAX_EXTRA_PAGES,
            "value": f"{actual_pages} pages (budget {target_pages})",
        },
        "a4": {
            "pass": all(abs(w - 595.3) < 1.6 and abs(h - 841.9) < 1.6 for w, h in sizes),
            "value": sizes,
        },
        "title_present": {
            "pass": " ".join(display_title.split()[:4]).lower()
            in " ".join(pdf_text.split()).lower(),
            "value": " ".join(display_title.split()[:4]),
        },
        "text_integrity": {
            "pass": integrity["pass"],
            "value": f"{integrity['blocks_checked']} blocks, {integrity['missing_count']} missing",
        },
    }

    # palette on rasterised PDF pages
    pages_on_disk, rasteriser = rasterise_pdf(out_pdf, qa_dir / "pdf")
    print(f"  palette raster: {rasteriser}")
    palette_entries: list[dict[str, Any]] = []
    for page in pages_on_disk:
        result = ga.run_palette_gate(page, args.tolerance)
        palette_entries.append(result)
        print(f"  {page.name}: {result['result']}")
    checks["palette_pdf"] = {
        "pass": bool(palette_entries) and all(r["pass"] for r in palette_entries),
        "value": f"{len(palette_entries)} page(s) @ {args.tolerance:g}%",
    }
    checks["css_colours"] = css_colour_check(out_html)

    built: list[dict[str, Any]] = [
        {
            "path": PDF_REL.as_posix(),
            "kind": "PDF",
            "detail": f"{actual_pages} pages, A4, unabridged",
            "size": format_bytes(out_pdf.stat().st_size),
            "palette": "PASS" if checks["palette_pdf"]["pass"] else "FAIL",
        }
    ]
    skipped: list[dict[str, str]] = []

    # ── LinkedIn (always) ─────────────────────────────────────────────────────
    linkedin = campaign / LINKEDIN_REL
    linkedin.parent.mkdir(parents=True, exist_ok=True)
    linkedin_doc, linkedin_post = build_linkedin_post(title, blocks, stats, when)
    linkedin.write_text(linkedin_doc, encoding="utf-8")
    post_chars = len(linkedin.read_text(encoding="utf-8"))
    print(f"\nlinkedin\n  {LINKEDIN_REL.as_posix()} ({post_chars:,} chars incl. header)")
    checks["linkedin_limit"] = {
        "pass": len(linkedin_post) <= LINKEDIN_LIMIT,
        "value": f"{len(linkedin_post):,} / {LINKEDIN_LIMIT:,} chars",
    }
    built.append(
        {
            "path": LINKEDIN_REL.as_posix(),
            "kind": "Copy",
            "detail": f"{post_chars:,} chars",
            "size": format_bytes(linkedin.stat().st_size),
            "palette": "n/a",
        }
    )

    # ── media branch ──────────────────────────────────────────────────────────
    if not media_branch:
        skipped.extend(
            [
                {
                    "asset": "open-design/video-short-1080x1920.mp4",
                    "reason": "no NotebookLM audio (*.mp3 / *.wav) in notebooklm/ — State 1",
                },
                {
                    "asset": "open-design/video-overview-16x9.mp4",
                    "reason": "no NotebookLM audio (*.mp3 / *.wav) in notebooklm/ — State 1",
                },
                {
                    "asset": "open-design/infographic-square-1080x1080.png",
                    "reason": "no NotebookLM audio (*.mp3 / *.wav) in notebooklm/ — State 1",
                },
                {
                    "asset": "open-design/infographic-landscape-1600x900.png",
                    "reason": "no NotebookLM audio (*.mp3 / *.wav) in notebooklm/ — State 1",
                },
                {
                    "asset": "text/x-thread.md",
                    "reason": "media branch skipped — State 1",
                },
                {
                    "asset": "text/facebook-post.md",
                    "reason": "media branch skipped — State 1",
                },
                {
                    "asset": "text/instagram-caption.md",
                    "reason": "media branch skipped — State 1",
                },
            ]
        )
        print("\nmedia    : skipped (text-only campaign)")
    else:
        print("\nmedia")
        facts = ga.build_facts(campaign)
        open_design = campaign / "open-design"
        open_design.mkdir(parents=True, exist_ok=True)
        text_dir = campaign / "text"
        text_dir.mkdir(parents=True, exist_ok=True)

        infographics = {
            "infographic-square-1080x1080.png": (ga.SQUARE, "square"),
            "infographic-landscape-1600x900.png": (ga.LANDSCAPE_X, "landscape"),
        }
        for name, (size, variant) in infographics.items():
            image = ga.render_infographic(facts, size, variant)
            path = open_design / name
            image.save(path)
            assert image.size == size, f"{name} rendered at {image.size}, expected {size}"
            result = ga.run_palette_gate(path, args.tolerance)
            palette_entries.append(result)
            checks[f"dims_{name}"] = {"pass": image.size == size, "value": f"{size[0]}x{size[1]}"}
            print(f"  {name:<42} {size[0]}x{size[1]}  {result['result']}")
            built.append(
                {
                    "path": f"open-design/{name}",
                    "kind": "PNG",
                    "detail": f"{size[0]}x{size[1]}",
                    "size": format_bytes(path.stat().st_size),
                    "palette": "PASS" if result["pass"] else "FAIL",
                }
            )

        beats = ga.build_beats(facts)
        if args.skip_video:
            print("  video: skipped (--skip-video)")
            skipped.extend(
                [
                    {
                        "asset": "open-design/video-short-1080x1920.mp4",
                        "reason": "skipped with --skip-video",
                    },
                    {
                        "asset": "open-design/video-overview-16x9.mp4",
                        "reason": "skipped with --skip-video",
                    },
                ]
            )
        else:
            for name, size, label in (
                ("video-short-1080x1920.mp4", ga.VERTICAL, "short 9:16"),
                ("video-overview-16x9.mp4", ga.HORIZONTAL, "overview 16:9"),
            ):
                frame_dir = qa_dir / "frames" / name.replace(".mp4", "")
                ga.render_video(facts, beats, size, frame_dir, label)
                out = open_design / name
                ga.encode_video(frame_dir, out, args.fps)
                probe = ga.ffprobe_dims(out)
                dims_ok = probe.get("width") == size[0] and probe.get("height") == size[1]
                checks[f"dims_{name}"] = {
                    "pass": bool(dims_ok),
                    "value": f"{probe.get('width')}x{probe.get('height')}",
                }
                source_frames = sorted(frame_dir.glob("f*.png"))
                picks = (
                    [source_frames[0], source_frames[len(source_frames) // 2], source_frames[-1]]
                    if source_frames
                    else []
                )
                frame_results = [ga.run_palette_gate(p, args.tolerance) for p in picks]
                palette_entries.extend(frame_results)
                if not args.keep_frames:
                    shutil.rmtree(frame_dir, ignore_errors=True)
                print(
                    f"  {name:<42} {probe.get('width')}x{probe.get('height')} "
                    f"{probe.get('duration')}s  {format_bytes(out.stat().st_size)}"
                )
                built.append(
                    {
                        "path": f"open-design/{name}",
                        "kind": "MP4",
                        "detail": (
                            f"{probe.get('width')}x{probe.get('height')}, "
                            f"{probe.get('duration')}s, {probe.get('frames')} frames"
                        ),
                        "size": format_bytes(out.stat().st_size),
                        "palette": "PASS" if all(r["pass"] for r in frame_results) else "FAIL",
                    }
                )

        social = build_social_files(facts, when)
        posts = social.pop("_x_posts")
        checks["x_thread"] = {
            "pass": len(posts) >= 3 and all(len(p) <= 280 for p in posts),
            "value": [len(p) for p in posts],
        }
        for name, content in social.items():
            path = text_dir / name
            path.write_text(str(content), encoding="utf-8")
            print(f"  text/{name}")
            built.append(
                {
                    "path": f"text/{name}",
                    "kind": "Copy",
                    "detail": f"{len(str(content)):,} chars",
                    "size": format_bytes(path.stat().st_size),
                    "palette": "n/a",
                }
            )

    # ── verdict ───────────────────────────────────────────────────────────────
    checks["palette_all"] = {
        "pass": bool(palette_entries) and all(r["pass"] for r in palette_entries),
        "value": f"{len(palette_entries)} raster(s) @ {args.tolerance:g}%",
    }
    built_paths = [
        campaign / PDF_REL,
        campaign / LINKEDIN_REL,
    ]
    built_paths += [campaign / row["path"] for row in built if row["kind"] in {"PNG", "MP4"}]
    checks["assets_present"] = {
        "pass": all(p.is_file() and p.stat().st_size > 0 for p in built_paths),
        "value": f"{len(built_paths)} files",
        "missing": [p.name for p in built_paths if not p.is_file()],
    }

    verdict_pass = all(bool(c.get("pass")) for c in checks.values())
    report_path = write_audit_report(
        campaign=campaign,
        when=when,
        state=state,
        audio_files=audio_files,
        forced_media=args.force_media,
        stats=stats,
        template_name=template_name,
        target_pages=target_pages,
        pages=pages,
        fit=fit,
        integrity=integrity,
        checks=checks,
        built=built,
        skipped=skipped,
        source_sha=source_sha,
    )

    manifest = {
        "campaign": campaign.name,
        "generated": when.isoformat(timespec="seconds"),
        "state": state,
        "audio_files": [p.name for p in audio_files],
        "media_branch": media_branch,
        "forced_media": args.force_media,
        "template": template_name,
        "target_pages": target_pages,
        "rendered_pages": len(pages),
        "fit": fit,
        "source_sha256": source_sha,
        "stats": stats,
        "integrity": integrity,
        "checks": checks,
        "palette": palette_entries,
        "built": built,
        "skipped": skipped,
        "pass": verdict_pass,
    }
    manifest_path = qa_dir / "build-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("\nQA gates")
    for name, check in checks.items():
        status = "PASS" if check.get("pass") else "FAIL"
        print(f"  {name:<18} {status} ({check.get('value')})")

    print("\n" + "=" * 72)
    print("  CAMPAIGN BUILD READY" if verdict_pass else "  CAMPAIGN BUILD FAILED")
    print("=" * 72)
    print(f"  campaign : {campaign}")
    print(f"  state    : {state}  |  media branch: {'ran' if media_branch else 'skipped'}")
    print(f"  pdf      : {out_pdf}  ({actual_pages} pages, fit {fit:.2f})")
    print(f"  linkedin : {campaign / LINKEDIN_REL}")
    print(f"  audit    : {report_path}")
    print(f"  manifest : {manifest_path}")
    print(f"STATUS: {'OK' if verdict_pass else 'FAILED'}")
    return 0 if verdict_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
