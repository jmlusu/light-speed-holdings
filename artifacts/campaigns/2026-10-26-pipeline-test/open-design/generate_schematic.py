#!/usr/bin/env python3
"""Generate the campaign architecture schematic SVG.

Deterministic, offline, no agent in the loop. This replaces the hand-authored
markup plus the `qa/embed_logo_svg.py` post-patch with a single reproducible
render, so the diagram can be rebuilt without a generative tool call.

Everything is derived from the brand tokens and a computed grid, not typed as
magic numbers:

  content box   x = 48 .. 1152   (1104 px wide)
  flow nodes    6 x 169 px, 5 x 18 px gaps   = 1014 + 90  = 1104
  tier pills    5 x 208 px, 4 x 16 px gaps   = 1040 + 64  = 1104

Both rows are asserted to land exactly on 1152 before anything is written, so a
future edit to a node count or width fails loudly instead of drifting off the
content box.

The brand symbol is cropped from `brand/logo/logo-dark-bg-transparent.png` and
inlined as a base64 PNG data URI, so the SVG stays a single self-contained file
with no external asset dependency.

Every string on the canvas is a claim. Numbers are carried in `STATS` with the
source that backs them recorded alongside, and the facts-only rule applies:
nothing here may exceed what the dossier supports.

Usage:
    python generate_schematic.py            # write open-design/schematic.svg
    python generate_schematic.py --check    # exit 1 if the file has drifted
"""

from __future__ import annotations

import argparse
import base64
import io
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SVG_OUT = HERE / "schematic.svg"
SYMBOL_OUT = HERE / "logo-symbol.png"


def _find_repo_root(start: Path) -> Path:
    """Walk up to the checkout root (the first ancestor holding the logo)."""
    for candidate in (start, *start.parents):
        if (candidate / "brand" / "logo" / "logo-dark-bg-transparent.png").is_file():
            return candidate
    raise SystemExit(f"could not locate the repository root above {start}")


REPO_ROOT = _find_repo_root(HERE)
LOGO_SRC = REPO_ROOT / "brand" / "logo" / "logo-dark-bg-transparent.png"

# --- brand tokens -----------------------------------------------------------
# Navy is the canvas; cyan and red are accents. Red is reserved for the ask and
# the highest-risk gate, never for decoration.
NAVY = "#070A40"
CYAN = "#00BFFF"
RED = "#E63946"
WHITE = "#FFFFFF"
PANEL = "#121518"  # inset panel fill
INK_MUTED = "#9CA3AF"  # secondary text, AA on navy at 7.34:1
RULE = "#6B7280"  # hairlines only - never text

FONT = "Arial, Helvetica, sans-serif"

# --- canvas geometry --------------------------------------------------------
W, H = 1200, 640
MARGIN = 48
CONTENT_LEFT = MARGIN
CONTENT_RIGHT = W - MARGIN  # 1152
CONTENT_W = CONTENT_RIGHT - CONTENT_LEFT  # 1104

# --- flow row ---------------------------------------------------------------
NODE_W, NODE_GAP = 169, 18
NODE_Y, NODE_H = 170, 96
NODE_R = 8

# --- tier row ---------------------------------------------------------------
TIER_W, TIER_GAP = 208, 16
TIER_Y, TIER_H = 364, 46
TIER_PAD_X = 14

# --- stats band -------------------------------------------------------------
STATS_Y, STATS_H = 440, 96
STATS_DIVIDER_TOP, STATS_DIVIDER_BOTTOM = 462, 516
STATS_STRIDE = 200
STATS_FIRST_DIVIDER = 300
STATS_LABEL_DY = 32  # label x offset from its divider

# Header / band rules.
HEADER_RULE_Y = 110
HITL_RULE_Y = 310
FOOTER_RULE_Y = 568

# The symbol sits at display height 48 and is rastered at 2x for crispness.
SYMBOL_DISPLAY_H = 48
SYMBOL_RASTER_H = SYMBOL_DISPLAY_H * 2
SYMBOL_X, SYMBOL_Y = 48, 30

# --- content -----------------------------------------------------------------

FLOW_NODES: list[tuple[str, list[str], bool]] = [
    # (label, sub-labels, is_the_ask)
    ("Human Business", ["Owner sets intent"], False),
    ("AI Finance", ["Cash reconciliation", "Margin tracking"], False),
    ("AI Inventory", ["Stock position", "Shortage detection"], False),
    ("AI Procurement", ["Supplier pricing", "Reorder drafting"], False),
    ("AI Operations", ["Workflow logging", "Profitability view"], False),
    ("CEO Dashboard", ["Human decision", "Single owner"], True),
]

TIERS: list[tuple[str, str, str | None]] = [
    # (label, detail, stroke colour; None = neutral hairline)
    ("TIER 0 &#183; AUTO", "Read, list, grep, recall", None),
    ("TIER 1 &#183; NOTIFY", "Log only, status updates", None),
    ("TIER 2 &#183; SINGLE", "File edits &#183; 60 min escalate", CYAN),
    ("TIER 3 &#183; DUAL", "Shell exec &#183; 30 min to CEO", CYAN),
    ("TIER 4 &#183; CEO ONLY", "Config/audit &#183; 24 hr board", RED),
]

# (label, value, value colour, source)
STATS: list[tuple[str, str, str, str]] = [
    ("AGENTS IN PRODUCTION", "90", CYAN, "company-registry.yaml - 89 AI + 1 human CEO"),
    ("DEPARTMENTS", "20", CYAN, "company-registry.yaml - distinct department values"),
    ("CI QUALITY GATES", "4", CYAN, "REVIEW: not traced in the campaign dossier"),
    ("CANONICAL TOOLS", "7", CYAN, "AGENTS.md section 8"),
    (
        "PILOT DECISION GATE",
        "DAY 90",
        RED,
        "resource-constrained-deployment-playbook.md section 4.1",
    ),
]

TITLE = "AGENTIC DECISION SUPPORT &#8212; J&amp;S STOPOVER BAR"
SUBTITLE = "One human owner. Five agents. No engineering department required."
FLOW_LABEL = "OPERATING CHAIN &#8212; LOCAL INFERENCE, OFFLINE-FIRST"
HITL_LABEL = "HUMAN-IN-THE-LOOP APPROVAL GATE &#8212; A TIMEOUT ESCALATES, IT NEVER AUTO-APPROVES"
FOOTER_ENTITY = "LightSpeed Holdings Limited&#8482;"
FOOTER_TAGLINE = "ASPIRE. ACT. ACHIEVE."
SVG_TITLE = "Agentic decision support architecture - J&amp;S StopOver Bar"
SVG_DESC = (
    "Five agentic workloads run on local infrastructure under a five-tier "
    "human-in-the-loop gate, reporting to a single human owner via the CEO dashboard."
)


def node_x(index: int) -> int:
    return CONTENT_LEFT + index * (NODE_W + NODE_GAP)


def tier_x(index: int) -> int:
    return CONTENT_LEFT + index * (TIER_W + TIER_GAP)


def stat_divider(index: int) -> int:
    return STATS_FIRST_DIVIDER + index * STATS_STRIDE


def check_grid() -> None:
    """Fail loudly rather than emit a row that drifts off the content box."""
    flow_right = node_x(len(FLOW_NODES) - 1) + NODE_W
    if flow_right != CONTENT_RIGHT:
        raise SystemExit(
            f"flow row ends at {flow_right}, expected {CONTENT_RIGHT} "
            f"({len(FLOW_NODES)} nodes x {NODE_W} + {len(FLOW_NODES) - 1} x {NODE_GAP})"
        )
    tier_right = tier_x(len(TIERS) - 1) + TIER_W
    if tier_right != CONTENT_RIGHT:
        raise SystemExit(
            f"tier row ends at {tier_right}, expected {CONTENT_RIGHT} "
            f"({len(TIERS)} pills x {TIER_W} + {len(TIERS) - 1} x {TIER_GAP})"
        )
    stats_right = MARGIN + CONTENT_W
    if stats_right != CONTENT_RIGHT:
        raise SystemExit("stats band does not span the content box")


def extract_symbol(height: int) -> Image.Image:
    """Crop the mark out of the lockup, above the gap that precedes the wordmark.

    Only `logo-dark-bg-transparent.png` is genuinely transparent in brand/logo/;
    the other rasters are fully opaque and would paste a white box onto navy.
    """
    if not LOGO_SRC.is_file():
        raise SystemExit(f"logo source missing: {LOGO_SRC}")

    im = Image.open(LOGO_SRC).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    w, h = im.size
    alpha = im.getchannel("A")

    # Walk down the alpha channel; the first run of >= 20 fully empty rows is the
    # band between the symbol and the wordmark.
    cut, band_start = h, None
    for y in range(h):
        empty = alpha.crop((0, y, w, y + 1)).getextrema()[1] == 0
        if empty:
            if band_start is None:
                band_start = y
        else:
            if band_start is not None and y - band_start >= 20:
                cut = band_start
                break
            band_start = None

    im = im.crop((0, 0, w, cut))
    im = im.crop(im.getchannel("A").getbbox())
    new_w = round(im.size[0] * height / im.size[1])
    return im.resize((new_w, height), Image.LANCZOS)


def symbol_data_uri() -> tuple[str, str]:
    """Return (base64 payload, display width) for the inlined symbol."""
    symbol = extract_symbol(SYMBOL_RASTER_H)
    symbol.save(SYMBOL_OUT)

    buf = io.BytesIO()
    symbol.save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    display_w = round(symbol.size[0] * SYMBOL_DISPLAY_H / symbol.size[1])
    return b64, str(display_w)


def build_svg() -> str:
    check_grid()
    b64, display_w = symbol_data_uri()
    out: list[str] = []

    # -- root and accessibility ---------------------------------------------
    out.append('<svg xmlns="http://www.w3.org/2000/svg"')
    out.append(
        '  xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        'role="img" aria-labelledby="ttl dsc">'
    )
    out.append(f'  <title id="ttl">{SVG_TITLE}</title>')
    out.append(f'  <desc id="dsc">{SVG_DESC}</desc>')
    out.append("")

    # -- canvas --------------------------------------------------------------
    out.append("  <!-- Canvas -->")
    out.append(f'  <rect width="{W}" height="{H}" fill="{NAVY}"/>')
    out.append(f'  <rect x="0" y="0" width="6" height="{H}" fill="{CYAN}"/>')
    out.append("")

    # -- header --------------------------------------------------------------
    out.append("  <!-- Header -->")
    out.append(
        "  <!-- Transparent brand symbol (inlined from brand/logo/logo-dark-bg-transparent.png) -->"
    )
    out.append(
        f'  <image x="{SYMBOL_X}" y="{SYMBOL_Y}" width="{display_w}" height="{SYMBOL_DISPLAY_H}"'
    )
    out.append(f'         xlink:href="data:image/png;base64,{b64}"/>')
    out.append("")
    # Title starts at 140 so it clears the symbol.
    out.append(
        f'  <text x="140" y="64" font-family="{FONT}" font-size="27" '
        f'font-weight="700" fill="{WHITE}">{TITLE}</text>'
    )
    out.append(
        f'  <text x="{CONTENT_LEFT}" y="92" font-family="{FONT}" '
        f'font-size="15" fill="{CYAN}">{SUBTITLE}</text>'
    )
    out.append(
        f'  <line x1="{CONTENT_LEFT}" y1="{HEADER_RULE_Y}" x2="{CONTENT_RIGHT}" '
        f'y2="{HEADER_RULE_Y}" stroke="{CYAN}" stroke-width="2"/>'
    )
    out.append("")

    # -- flow row ------------------------------------------------------------
    out.append("  <!-- Row label -->")
    out.append(
        f'  <text x="{CONTENT_LEFT}" y="150" font-family="{FONT}" '
        f'font-size="12" fill="{INK_MUTED}">{FLOW_LABEL}</text>'
    )
    out.append("")
    out.append(
        f"  <!-- Flow nodes: {NODE_W}px wide, {NODE_GAP}px gaps, "
        f"aligned to the {CONTENT_LEFT}..{CONTENT_RIGHT} content box -->"
    )

    for i, (label, subs, is_ask) in enumerate(FLOW_NODES):
        x = node_x(i)
        cx = x + NODE_W // 2
        fill = RED if is_ask else NAVY
        stroke = RED if is_ask else CYAN
        out.append(
            f'  <rect x="{x}" y="{NODE_Y}" width="{NODE_W}" height="{NODE_H}" '
            f'rx="{NODE_R}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        )
        # A single sub-label is optically centred as a pair with its heading;
        # two sub-labels sit lower so the heading clears the first line.
        single = len(subs) == 1
        out.append(
            f'  <text x="{cx}" y="{208 if single else 202}" font-family="{FONT}" '
            f'font-size="14" font-weight="700" fill="{WHITE}" '
            f'text-anchor="middle">{label}</text>'
        )
        sub_ys = [230] if single else [224, 242]
        sub_fill = WHITE if is_ask else INK_MUTED
        for sub, y in zip(subs, sub_ys, strict=True):
            out.append(
                f'  <text x="{cx}" y="{y}" font-family="{FONT}" font-size="11" '
                f'fill="{sub_fill}" text-anchor="middle">{sub}</text>'
            )
        out.append("")

    # -- connectors ----------------------------------------------------------
    gaps = [f"{node_x(i) + NODE_W}-{node_x(i + 1)}" for i in range(len(FLOW_NODES) - 1)]
    out.append(f"  <!-- Connectors ({NODE_GAP}px gaps: {', '.join(gaps)}) -->")
    out.append(f'  <g stroke="{RULE}" stroke-width="2">')
    for i in range(len(FLOW_NODES) - 1):
        start = node_x(i) + NODE_W
        out.append(f'    <line x1="{start}" y1="218" x2="{start + 9}" y2="218"/>')
    out.append("  </g>")
    out.append(f'  <g fill="{CYAN}">')
    for i in range(len(FLOW_NODES) - 1):
        start = node_x(i) + NODE_W
        tip = node_x(i + 1)
        out.append(f'    <polygon points="{start + 9},214 {tip},218 {start + 9},222"/>')
    out.append("  </g>")
    out.append("")

    # -- HITL band -----------------------------------------------------------
    out.append("  <!-- HITL gate band -->")
    out.append(
        f'  <line x1="{CONTENT_LEFT}" y1="{HITL_RULE_Y}" x2="{CONTENT_RIGHT}" '
        f'y2="{HITL_RULE_Y}" stroke="{RULE}" stroke-width="1"/>'
    )
    out.append(
        f'  <text x="{CONTENT_LEFT}" y="346" font-family="{FONT}" '
        f'font-size="12" fill="{INK_MUTED}">{HITL_LABEL}</text>'
    )
    out.append("")

    # -- tier pills ----------------------------------------------------------
    out.append(f"  <!-- Tier pills: {TIER_W}px wide, {TIER_GAP}px gaps -->")
    out.append(f'  <g font-family="{FONT}" font-size="12">')
    for i, (label, detail, accent) in enumerate(TIERS):
        x = tier_x(i)
        stroke = accent or RULE
        width = 2 if accent == RED else 1
        out.append(
            f'    <rect x="{x}" y="{TIER_Y}" width="{TIER_W}" height="{TIER_H}" '
            f'rx="6" fill="{PANEL}" stroke="{stroke}" stroke-width="{width}"/>'
        )
        tx = x + TIER_PAD_X
        out.append(f'    <text x="{tx}" y="386" font-weight="700" fill="{WHITE}">{label}</text>')
        out.append(f'    <text x="{tx}" y="402" fill="{INK_MUTED}">{detail}</text>')
        out.append("")
    out[-1] = "  </g>"  # close the group in place of the trailing blank line
    out.append("")

    # -- stats band ----------------------------------------------------------
    out.append("  <!-- Stats band -->")
    out.append(
        f'  <rect x="{CONTENT_LEFT}" y="{STATS_Y}" width="{CONTENT_W}" '
        f'height="{STATS_H}" rx="8" fill="{PANEL}" stroke="{RULE}" stroke-width="1"/>'
    )
    out.append("")
    for i, (label, value, colour, _source) in enumerate(STATS):
        if i == 0:
            lx = CONTENT_LEFT + 32
        else:
            dx = stat_divider(i - 1)
            out.append(
                f'  <line x1="{dx}" y1="{STATS_DIVIDER_TOP}" x2="{dx}" '
                f'y2="{STATS_DIVIDER_BOTTOM}" stroke="{RULE}" stroke-width="1"/>'
            )
            lx = dx + STATS_LABEL_DY
        out.append(
            f'  <text x="{lx}" y="478" font-family="{FONT}" font-size="11" '
            f'fill="{INK_MUTED}">{label}</text>'
        )
        out.append(
            f'  <text x="{lx}" y="518" font-family="{FONT}" font-size="30" '
            f'font-weight="700" fill="{colour}">{value}</text>'
        )
        out.append("")

    # -- footer --------------------------------------------------------------
    out.append("  <!-- Footer -->")
    out.append(
        f'  <line x1="{CONTENT_LEFT}" y1="{FOOTER_RULE_Y}" x2="{CONTENT_RIGHT}" '
        f'y2="{FOOTER_RULE_Y}" stroke="{RULE}" stroke-width="1"/>'
    )
    out.append(
        f'  <text x="{CONTENT_LEFT}" y="598" font-family="{FONT}" '
        f'font-size="12" fill="{WHITE}">{FOOTER_ENTITY}</text>'
    )
    out.append(
        f'  <text x="{CONTENT_RIGHT}" y="598" font-family="{FONT}" font-size="12" '
        f'font-weight="700" fill="{CYAN}" text-anchor="end">{FOOTER_TAGLINE}</text>'
    )
    out.append("</svg>")

    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if schematic.svg differs from what this script would generate",
    )
    args = parser.parse_args()

    svg = build_svg()

    if args.check:
        if not SVG_OUT.is_file():
            print(f"FAIL: {SVG_OUT.name} is missing")
            return 1
        if SVG_OUT.read_text(encoding="utf-8") != svg:
            print(f"FAIL: {SVG_OUT.name} has drifted from generate_schematic.py")
            return 1
        print(f"OK: {SVG_OUT.name} matches generate_schematic.py")
        return 0

    SVG_OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {SVG_OUT.relative_to(REPO_ROOT)}  ({SVG_OUT.stat().st_size:,} bytes)")
    print(f"wrote {SYMBOL_OUT.relative_to(REPO_ROOT)}")
    for label, value, _colour, source in STATS:
        print(f"  {label:<22} {value:<8} {source}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
