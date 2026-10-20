"""Generate the AI Venture Studio client presentation (13 slides, 10x7.5in).

Source of truth: ai_venture_studio_client_presentation_deck_spec.md
Brand tokens:    brand/tokens/brand-tokens.json (palette + Arial type scale)

Run:
    uv run --with python-pptx python scripts/presentation/generate-ai-venture-studio-deck.py
"""

from __future__ import annotations

import argparse
import os
import tempfile

from deck_geometry import (
    CLOSING_LOGO_W_IN,
    CLOSING_LOGO_X_IN,
    CLOSING_LOGO_Y_IN,
    COVER_LOGO_W_IN,
    COVER_LOGO_X_IN,
    COVER_LOGO_Y_IN,
    LOGO_ASPECT,
    LOGO_BG_HEX,
    LOGO_SRC_BOX,
    LOGO_SRC_SIZE,
)
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls, qn
from pptx.util import Inches, Pt

# ---------------------------------------------------------------- brand tokens
NAVY = RGBColor(0x07, 0x0A, 0x40)
RED = RGBColor(0xE6, 0x39, 0x46)
CYAN = RGBColor(0x00, 0xBF, 0xFF)
GREY_LIGHT = RGBColor(0xF2, 0xF2, 0xF2)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREY_DARK = RGBColor(0x6B, 0x72, 0x80)

# type scale (pt)
T_DISPLAY_XL = 36
T_TITLE_XL = 32
T_TITLE_LG = 28
T_TITLE_MD = 24
T_TITLE_SM = 18
T_SUBTITLE = 16
T_BODY_LG = 16
T_BODY = 14
T_BODY_SM = 13
T_CAPTION = 12

FONT = "Arial"

# --------------------------------------------------------------------- layout
SLIDE_W = 10.0
SLIDE_H = 7.5
RAIL_W = 0.15
X0 = 0.65
X1 = 9.50
CONTENT_W = X1 - X0  # 8.85
TITLE_Y = 0.50
TOP = 1.25
BOTTOM = 6.85
FOOTER_Y = 6.96

LOGO_PATH = os.path.join("brand", "logo", "logo-full.png")


# --------------------------------------------------------------------- helpers
def slide_bg(slide, color: RGBColor) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def rect(slide, x, y, w, h, color, line=None):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.shadow.inherit = False
    if color is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = color
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(0.75)
    sh.text_frame.word_wrap = True
    return sh


def text(
    slide,
    x,
    y,
    w,
    h,
    paras,
    size=T_BODY,
    color=GREY_DARK,
    bold=False,
    align=PP_ALIGN.LEFT,
    anchor=MSO_ANCHOR.TOP,
    line_spacing=1.18,
    space_after=0,
):
    """paras: list of str or list of (text, {overrides})."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    for i, para_spec in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        para.line_spacing = line_spacing
        para.space_after = Pt(space_after)
        runs = para_spec if isinstance(para_spec, list) else [(para_spec, {})]
        for txt, kw in runs:
            run = para.add_run()
            run.text = txt
            f = run.font
            f.name = FONT
            f.size = Pt(kw.get("size", size))
            f.bold = kw.get("bold", bold)
            f.italic = kw.get("italic", False)
            f.color.rgb = kw.get("color", color)
    return tb


def _no_border(cell) -> None:
    tcPr = cell._tc.get_or_add_tcPr()
    for i, tag in enumerate(("a:lnL", "a:lnR", "a:lnT", "a:lnB")):
        ln = tcPr.find(qn(tag))
        if ln is None:
            ln = parse_xml(f'<{tag} {nsdecls("a")} w="0"/>')
            tcPr.insert(i, ln)
        for child in list(ln):
            ln.remove(child)
        ln.set("w", "0")
        ln.append(parse_xml(f"<a:noFill {nsdecls('a')}/>"))


def table(slide, x, y, col_w, rows, body=T_CAPTION, header=T_CAPTION, row_h=0.42, head_h=0.40):
    """rows[0] is the header row. Returns the table shape."""
    n_rows, n_cols = len(rows), len(col_w)
    height = head_h + row_h * (n_rows - 1)
    shape = slide.shapes.add_table(
        n_rows, n_cols, Inches(x), Inches(y), Inches(sum(col_w)), Inches(height)
    )
    tbl = shape.table
    tbl.first_row = False
    tbl.horz_banding = False
    for i, w in enumerate(col_w):
        tbl.columns[i].width = Inches(w)
    tbl.rows[0].height = Inches(head_h)
    for r in range(1, n_rows):
        tbl.rows[r].height = Inches(row_h)

    for r, row in enumerate(rows):
        for c, value in enumerate(row):
            cell = tbl.cell(r, c)
            _no_border(cell)
            cell.margin_left = cell.margin_right = Inches(0.08)
            cell.margin_top = cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = NAVY
            else:
                cell.fill.fore_color.rgb = GREY_LIGHT if r % 2 == 0 else WHITE
            tf = cell.text_frame
            tf.word_wrap = True
            para = tf.paragraphs[0]
            para.line_spacing = 1.0
            run = para.add_run()
            run.text = value
            f = run.font
            f.name = FONT
            f.size = Pt(header if r == 0 else body)
            f.bold = r == 0 or (c == 0)
            f.color.rgb = WHITE if r == 0 else (NAVY if c == 0 else GREY_DARK)
    return shape


def _make_logo_bg_transparent(pic) -> None:
    """Turn the logo's flat navy plate transparent (PowerPoint clrChange)."""
    blip = pic._element.blipFill.blip
    blip.append(
        parse_xml(
            f'<a:clrChange {nsdecls("a")} useAlpha="1">'
            f'<a:clrFrom><a:srgbClr val="{LOGO_BG_HEX}"><a:alpha val="100000"/></a:srgbClr></a:clrFrom>'
            f'<a:clrTo><a:srgbClr val="{LOGO_BG_HEX}"><a:alpha val="0"/></a:srgbClr></a:clrTo>'
            f"</a:clrChange>"
        )
    )


def _cropped_logo() -> str:
    """Crop the lockup to its artwork box, once, and return the cached path.

    The picture frame must equal the visible artwork in every renderer. Setting
    `a:srcRect` only works where the renderer honours it: LibreOffice ignores it
    and stretches the full square, which draws the baked-in tagline down over
    the slide text. Cropping the asset up front keeps the two identical.

    The cropped file is cached in the temp dir under a stable name (it ends up
    in the deck as the picture's description, so it must not vary between
    machines). It is re-cut whenever the brand asset is newer than the cache,
    so a replaced logo can never be shipped from a stale crop.
    """
    from PIL import Image

    if not os.path.exists(LOGO_PATH):
        raise SystemExit(f"Missing logo asset: {LOGO_PATH}")
    left, top, right, bottom = LOGO_SRC_BOX
    name = f"ai-venture-studio-lockup-{right - left}x{bottom - top}.png"
    out = os.path.join(tempfile.gettempdir(), name)
    source_mtime = os.stat(LOGO_PATH).st_mtime_ns
    if not os.path.exists(out) or source_mtime > os.stat(out).st_mtime_ns:
        with Image.open(LOGO_PATH) as im:
            if im.size != LOGO_SRC_SIZE:
                raise SystemExit(
                    f"Logo asset is {im.size}, expected {LOGO_SRC_SIZE}. "
                    "Update LOGO_SRC_BOX and LOGO_SRC_SIZE in "
                    "scripts/presentation/deck_geometry.py."
                )
            im.crop(LOGO_SRC_BOX).save(out)
    return out


def logo(slide, x, y, content_w: float):
    """Place the lockup so the artwork is content_w inches wide at (x, y)."""
    pic = slide.shapes.add_picture(
        _cropped_logo(),
        Inches(x),
        Inches(y),
        width=Inches(content_w),
        height=Inches(content_w / LOGO_ASPECT),
    )
    _make_logo_bg_transparent(pic)
    return pic


def new_slide(prs, navy: bool = False, chrome: bool = True, number: int | None = None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(slide, NAVY if navy else WHITE)
    if chrome:
        rect(slide, 0, 0, RAIL_W, SLIDE_H, NAVY)
    if number is not None:
        text(
            slide,
            8.90,
            FOOTER_Y,
            0.60,
            0.25,
            [f"{number:02d}"],
            size=T_CAPTION,
            color=GREY_DARK,
            align=PP_ALIGN.RIGHT,
        )
    return slide


def title(slide, txt, size=T_TITLE_LG):
    text(slide, X0, TITLE_Y, CONTENT_W, 0.52, [txt], size=size, color=NAVY, bold=True)


def caption(slide, txt, y=6.55, color=GREY_DARK):
    text(slide, X0, y, CONTENT_W, 0.30, [txt], size=T_CAPTION, color=color)


def bullets(slide, x, y, w, items, size=T_BODY_SM, gap=0.34, marker=CYAN):
    for i, item in enumerate(items):
        top = y + i * gap
        rect(slide, x, top + 0.055, 0.09, 0.09, marker)
        text(
            slide,
            x + 0.22,
            top,
            w - 0.22,
            gap,
            [item],
            size=size,
            color=GREY_DARK,
            line_spacing=1.1,
        )


def notes(slide, txt):
    slide.notes_slide.notes_text_frame.text = txt


# ---------------------------------------------------------------------- slides
def build(out_path: str) -> None:
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)

    # ---------------------------------------------------------- 1. Cover (navy)
    s = new_slide(prs, navy=True, chrome=False)
    logo(s, COVER_LOGO_X_IN, COVER_LOGO_Y_IN, COVER_LOGO_W_IN)
    text(s, X0, 2.50, 8.00, 1.10, ["AI Venture Studio"], size=T_DISPLAY_XL, color=WHITE, bold=True)
    rect(s, X0, 3.95, 0.90, 0.04, RED)
    text(
        s,
        3.30,
        6.80,
        3.40,
        0.30,
        ["Client Presentation"],
        size=T_CAPTION,
        color=GREY_LIGHT,
        align=PP_ALIGN.CENTER,
    )
    text(
        s,
        7.10,
        6.80,
        2.25,
        0.30,
        ["2026-10-12"],
        size=T_CAPTION,
        color=GREY_LIGHT,
        align=PP_ALIGN.RIGHT,
    )
    notes(
        s,
        "Cover. LightSpeed Holdings Limited(TM) lockup top-left, deck title, red accent rule. "
        "No tagline on this slide; the tagline appears once, on the closing slide.",
    )

    # ------------------------------------------------------ 2. Executive Summary
    s = new_slide(prs, number=2)
    title(s, "Executive Summary")
    table(
        s,
        X0,
        1.30,
        [1.05, 1.15, 6.65],
        [
            ["Part", "Delivered", "Core Deliverable"],
            ["1", "Shipped", "Website brand psychology"],
            ["2", "Shipped", "Sector landscape"],
            ["3", "Shipped", "AI-Company Builder engine"],
            ["4", "Shipped", "Technical architecture"],
            ["5", "Shipped", "Core metrics"],
        ],
        row_h=0.38,
        head_h=0.38,
    )
    text(
        s,
        X0,
        3.85,
        4.30,
        2.00,
        [
            "Since shipping Parts 1\u20135 in September 2026, the studio has delivered a stage-gated, "
            "repeatable engine: shared infrastructure, agent stacks, data pipelines, and go-to-market "
            "engines that co-found, validate, build, and launch AI-native entities."
        ],
        size=T_BODY_SM,
        color=GREY_DARK,
    )
    rect(s, 5.20, 3.85, 0.06, 1.90, RED)
    rect(s, 5.26, 3.85, 4.24, 1.90, GREY_LIGHT)
    text(s, 5.50, 4.03, 3.80, 0.28, ["Why it matters"], size=T_CAPTION, color=NAVY, bold=True)
    text(
        s,
        5.50,
        4.37,
        3.80,
        1.20,
        [
            "Each venture gets access to capital-efficient infrastructure, governance that scales "
            "without chaos, and a clear path from thesis to spin-out."
        ],
        size=T_CAPTION,
        color=GREY_DARK,
    )
    caption(
        s,
        "Parts 1\u20135 shipped September 2026. Several are internal build milestones, not client deliverables.",
    )
    notes(
        s,
        "Walk the five shipped parts, then land the point: this is one repeatable engine, not five "
        "separate projects. Note that some parts are internal milestones.",
    )

    # -------------------------------------------- 3. The Studio Operating Engine
    s = new_slide(prs, number=3)
    title(s, "The Studio Operating Engine")
    rect(s, X0, TOP, 3.30, 2.35, GREY_LIGHT)
    rect(s, X0, TOP, 3.30, 0.34, NAVY)
    text(
        s,
        X0 + 0.14,
        TOP + 0.07,
        3.00,
        0.24,
        ["Studio Operating Engine"],
        size=T_CAPTION,
        color=WHITE,
        bold=True,
    )
    for i, label in enumerate(["Strategic Validation", "Agent Orchestration", "Shared Services"]):
        y = TOP + 0.44 + i * 0.62
        rect(s, X0 + 0.14, y, 3.02, 0.52, WHITE)
        text(s, X0 + 0.28, y + 0.15, 2.80, 0.24, [label], size=T_CAPTION, color=NAVY, bold=True)

    arrow = s.shapes.add_shape(
        MSO_SHAPE.RIGHT_ARROW, Inches(4.02), Inches(TOP + 1.05), Inches(0.55), Inches(0.26)
    )
    arrow.shadow.inherit = False
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = NAVY
    arrow.line.fill.background()

    ports = [
        ("Portfolio A", "Enterprise Agent", []),
        ("Portfolio B", "B2B AI Workflow", [("B2B", {"color": RED})]),
        ("Portfolio C", "Sovereign Data", [("Sovereign", {"color": CYAN})]),
    ]
    for i, (pname, pdesc, accent) in enumerate(ports):
        y = TOP + i * 0.80
        rect(s, 4.75, y, 2.00, 0.66, WHITE, line=NAVY)
        text(s, 4.88, y + 0.06, 1.80, 0.22, [pname], size=T_CAPTION, color=NAVY, bold=True)
        runs = [(pdesc, {})]
        if accent:
            head = accent[0][0]
            rest = pdesc[len(head) :]
            runs = [(head, accent[0][1]), (rest, {})]
        text(s, 4.88, y + 0.30, 1.80, 0.22, [runs], size=T_CAPTION, color=GREY_DARK)

    res = ["Constraint-first", "AI-agnostic", "PII-first", "Capital-efficient"]
    for i, label in enumerate(res):
        cx = 6.95 + (i % 2) * 1.28
        cy = TOP + (i // 2) * 1.20
        rect(s, cx, cy, 1.18, 1.08, GREY_LIGHT)
        rect(s, cx + 0.10, cy + 0.14, 0.09, 0.09, RED)
        text(s, cx + 0.10, cy + 0.36, 0.98, 0.60, [label], size=T_CAPTION, color=NAVY, bold=True)

    descs = [
        (
            "Portfolio A \u2014 Enterprise Agent",
            "Deep workflow integration inside a single large organisation.",
        ),
        (
            "Portfolio B \u2014 B2B AI Workflow",
            "Vertical AI fine-tuned on a sector's recurring workflow.",
        ),
        (
            "Portfolio C \u2014 Sovereign Data",
            "On-prem / sovereign deployment where data cannot leave jurisdiction.",
        ),
    ]
    for i, (head, body) in enumerate(descs):
        x = X0 + i * 2.98
        rect(s, x, 3.95, 2.78, 1.55, WHITE, line=GREY_LIGHT)
        text(s, x + 0.16, 4.06, 2.46, 0.44, [head], size=T_CAPTION, color=NAVY, bold=True)
        text(s, x + 0.16, 4.54, 2.46, 0.86, [body], size=T_CAPTION, color=GREY_DARK)
    caption(
        s,
        "\u201cThree\u201d (Portfolios A\u2013C) and \u201cfour\u201d (reservations) are distinct frameworks, not a count error.",
    )
    notes(
        s,
        "One engine, three delivery portfolios. The left column is the engine; the right blocks are the "
        "constraint-first design principles that keep a portfolio buildable inside real limits.",
    )

    # ------------------------------------------------- 4. Portfolio Archetypes
    s = new_slide(prs, number=4)
    title(s, "Portfolio Archetypes A\u2013D")
    cards = [
        (
            "Portfolio A",
            "Enterprise",
            "Deep workflow integration for large organisations; long sales cycles, high contract value.",
            [],
            "Frontier tier",
        ),
        (
            "Portfolio B",
            "B2B Workflow",
            "Vertical AI fine-tuned on sector workflows, sold to operators who already own the process.",
            [("Vertical AI fine-tuned", {"color": RED})],
            "Fine-tuned tier",
        ),
        (
            "Portfolio C",
            "Sovereign Data",
            "On-prem / sovereign deployment where regulated data cannot leave the jurisdiction.",
            [("On-prem / sovereign", {"color": CYAN})],
            "Sovereign tier",
        ),
        (
            "Portfolio D",
            "Consumer Platforms",
            "High-volume, low-latency consumer surfaces where unit cost decides the business model.",
            [("High-volume, low-latency", {"color": CYAN})],
            "Cost-cascaded tier",
        ),
    ]
    for i, (pname, arch, body, accent, tier) in enumerate(cards):
        x = X0 + i * 2.225
        w = 2.025
        rect(s, x, TOP, w, 3.30, WHITE, line=GREY_LIGHT)
        rect(s, x, TOP, w, 0.42, NAVY)
        text(
            s, x + 0.12, TOP + 0.10, w - 0.24, 0.24, [pname], size=T_CAPTION, color=WHITE, bold=True
        )
        text(
            s, x + 0.12, TOP + 0.62, w - 0.24, 0.52, [arch], size=T_SUBTITLE, color=NAVY, bold=True
        )
        runs = (
            accent + [(body[len(accent[0][0]) :] if accent else body, {})]
            if accent
            else [(body, {})]
        )
        text(s, x + 0.12, TOP + 1.32, w - 0.24, 1.38, [runs], size=T_CAPTION, color=GREY_DARK)
        rect(s, x + 0.12, TOP + 2.78, w - 0.24, 0.36, GREY_LIGHT)
        text(
            s,
            x + 0.12,
            TOP + 2.88,
            w - 0.24,
            0.22,
            [tier],
            size=T_CAPTION,
            color=NAVY,
            align=PP_ALIGN.CENTER,
        )

    text(
        s,
        X0,
        4.78,
        CONTENT_W,
        0.24,
        ["Four reservations, applied to every archetype"],
        size=T_CAPTION,
        color=NAVY,
        bold=True,
    )
    for i, label in enumerate(res):
        x = X0 + i * 2.225
        rect(s, x, 5.10, 0.09, 0.09, RED)
        text(s, x + 0.20, 5.04, 1.85, 0.24, [label], size=T_CAPTION, color=GREY_DARK)
    caption(
        s,
        "Portfolio D added per CTO validation. The \u201cthree\u201d and \u201cfour\u201d refer to distinct frameworks.",
    )
    notes(
        s,
        "Four archetypes, one engine. Emphasise that D was added on technical validation, and that the "
        "four reservations apply to all four archetypes.",
    )

    # ------------------------------------------- 5. Stage-Gated Lifecycle
    s = new_slide(prs, number=5)
    title(s, "Stage-Gated Development Lifecycle")
    table(
        s,
        X0,
        TOP,
        [1.55, 0.95, 3.55, 2.80],
        [
            ["Phase", "Duration", "Key Deliverables", "Gate Criteria"],
            [
                "1. Discovery",
                "Weeks 1\u20132",
                "Problem discovery & thesis definition",
                "3+ problem statements validated",
            ],
            [
                "2. Validation",
                "Weeks 3\u20136",
                "POC + 15\u201320 buyer calls",
                "3+ positive commitments; feasibility confirmed",
            ],
            [
                "3. Build",
                "Weeks 7\u201314",
                "MVA deployed to 2\u20133 design partners",
                "MVA running; ATC \u226580% gate",
            ],
            [
                "4. Scale",
                "Month 4+",
                "Spin-out, leadership recruitment",
                "Entity formed; term sheet issued",
            ],
        ],
        row_h=0.80,
        head_h=0.40,
    )
    text(
        s,
        X0,
        5.42,
        CONTENT_W,
        0.24,
        ["Tracked across all phases"],
        size=T_CAPTION,
        color=NAVY,
        bold=True,
    )
    for i, label in enumerate(
        ["ATC Rate", "Correction Ratio", "Velocity to MVP", "Capital Efficiency"]
    ):
        x = X0 + i * 2.225
        rect(s, x, 5.74, 2.10, 0.42, GREY_LIGHT)
        text(s, x, 5.85, 2.10, 0.24, [label], size=T_CAPTION, color=NAVY, align=PP_ALIGN.CENTER)
    caption(
        s,
        "Key metrics tracked across all phases. Velocity to MVP is measured from validation approval.",
    )
    notes(
        s,
        "Four gates, each with a hard criterion. The point for a client is that capital is only released "
        "after a gate is cleared, not on a calendar.",
    )

    # --------------------------------- 6. Technical Architecture (AI-Agnostic)
    s = new_slide(prs, number=6)
    title(s, "Technical Architecture (AI-Agnostic System)")
    rect(s, X0, TOP, CONTENT_W, 0.46, NAVY)
    text(
        s,
        X0 + 0.16,
        TOP + 0.11,
        CONTENT_W - 0.32,
        0.24,
        ["L1 \u00b7 Unified API Standard \u2014 one interface for every model provider"],
        size=T_CAPTION,
        color=WHITE,
        bold=True,
    )

    def down_arrow(x, y):
        a = s.shapes.add_shape(
            MSO_SHAPE.DOWN_ARROW, Inches(x), Inches(y), Inches(0.20), Inches(0.22)
        )
        a.shadow.inherit = False
        a.fill.solid()
        a.fill.fore_color.rgb = NAVY
        a.line.fill.background()

    def right_arrow(x, y):
        a = s.shapes.add_shape(
            MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(0.22), Inches(0.18)
        )
        a.shadow.inherit = False
        a.fill.solid()
        a.fill.fore_color.rgb = NAVY
        a.line.fill.background()

    down_arrow(4.90, 1.75)
    l2 = [
        ("Guardrail Proxy (inbound)", "Redacts or hashes PII; validates schema", 0.65, 2.75),
        ("Cost / Latency Router", "The only fan-out point in the mesh", 3.62, 2.55),
        ("Fallback Chains", "Deterministic retry and failover", 6.39, 1.95),
    ]
    for label, sub, x, w in l2:
        rect(s, x, 1.98, w, 0.78, GREY_LIGHT)
        text(s, x + 0.10, 2.06, w - 0.20, 0.24, [label], size=T_CAPTION, color=NAVY, bold=True)
        text(s, x + 0.10, 2.32, w - 0.20, 0.42, [sub], size=T_CAPTION, color=GREY_DARK)
    right_arrow(3.42, 2.28)
    right_arrow(6.19, 2.28)
    down_arrow(4.90, 2.82)

    tiers = [
        ("Frontier models", "Highest capability, highest unit cost"),
        ("Open-weights models", "Fine-tuned, self-hosted, margin control"),
        ("Local / Sovereign", "On-prem or in-jurisdiction deployment"),
    ]
    for i, (head, body) in enumerate(tiers):
        x = X0 + i * 2.98
        rect(s, x, 3.08, 2.78, 0.74, WHITE, line=NAVY)
        text(s, x + 0.12, 3.15, 2.54, 0.24, [head], size=T_CAPTION, color=NAVY, bold=True)
        text(s, x + 0.12, 3.40, 2.54, 0.40, [body], size=T_CAPTION, color=GREY_DARK)

    text(
        s,
        X0,
        3.98,
        CONTENT_W,
        0.24,
        ["Engineering directives"],
        size=T_CAPTION,
        color=NAVY,
        bold=True,
    )
    directives = [
        (
            "Universal Protocol Proxy",
            "Every provider speaks one contract; swapping a model is a config change.",
        ),
        (
            "Model Cascade & Dynamic Router",
            "Route by cost and latency budget, escalate only when quality demands it.",
        ),
        (
            "Deterministic Execution & State",
            "Every agent action is logged, replayable, and attributable.",
        ),
        (
            "Security & PII Guardrails",
            "Nothing reaches a model before redaction and schema validation.",
        ),
    ]
    for i, (head, body) in enumerate(directives):
        x = X0 + (i % 2) * 4.55
        y = 4.28 + (i // 2) * 0.78
        text(s, x, y, 0.28, 0.24, [f"0{i + 1}"], size=T_CAPTION, color=RED, bold=True)
        text(s, x + 0.30, y, 4.00, 0.24, [head], size=T_CAPTION, color=NAVY, bold=True)
        text(s, x + 0.30, y + 0.24, 4.00, 0.44, [body], size=T_CAPTION, color=GREY_DARK)

    rect(s, X0, 5.98, 0.08, 0.62, RED)
    rect(s, X0 + 0.08, 5.98, CONTENT_W - 0.08, 0.62, GREY_LIGHT)
    text(
        s,
        X0 + 0.26,
        6.10,
        CONTENT_W - 0.44,
        0.40,
        [
            "The intermediary proxy layer redacts or hashes PII before every LLM request, and validates schema on all outputs."
        ],
        size=T_CAPTION,
        color=NAVY,
        bold=True,
    )
    notes(
        s,
        "One interface, one guardrail, one routing point. The stack is AI-agnostic: it works with any "
        "LLM provider and with local models. Red is used only for the PII directive.",
    )

    # -------------------------------------------- 7. Core Performance Metrics
    s = new_slide(prs, number=7)
    title(s, "Core Performance Metrics")
    table(
        s,
        X0,
        1.25,
        [1.85, 1.55, 2.60, 2.85],
        [
            ["Metric", "Goal", "Why It Matters", "CFO KPI Mapping"],
            [
                "ATC Rate",
                "\u226590% trailing 30 days",
                "Autonomous agent efficacy",
                "Cost per Agent; ROI per Dept",
            ],
            ["Velocity to MVP", "<60 days", "Speed-to-market", "Budget Utilization"],
            ["Manual Correction Ratio", "Per 1,000 actions", "Quality signal", "Revenue per Task"],
            [
                "Capital Efficiency",
                "3\u20135\u00d7 (modeled)",
                "Shared infrastructure",
                "Cost per Agent; Budget Utilization",
            ],
        ],
        row_h=0.80,
        head_h=0.42,
    )
    blocks = [
        (
            "Studio vs. company KPIs",
            "Studio metrics measure delivery. CFO registry KPIs: Budget Utilization, Cost per Agent, ROI per Dept, Total Revenue, Revenue Margin, Revenue per Task.",
        ),
        (
            "Velocity scope",
            "The <60-day goal measures Phase 2 validation approval to Phase 3 minimal MVP deployment, not idea to revenue.",
        ),
        (
            "3\u20135\u00d7 basis",
            "Modeled estimate from traditional seed-round cost structures versus shared-infrastructure economics. Assumptions available on request.",
        ),
    ]
    for i, (head, body) in enumerate(blocks):
        x = X0 + i * 3.03
        text(s, x, 5.10, 2.78, 0.24, [head], size=T_CAPTION, color=NAVY, bold=True)
        text(s, x, 5.36, 2.78, 1.10, [body], size=T_CAPTION, color=GREY_DARK)
    notes(
        s,
        "Four metrics, each mapped to a CFO KPI. Be explicit that 3-5x is a modeled estimate, and that "
        "velocity is measured from validation approval, not from idea.",
    )

    # ------------------------------------------ 8. Go-to-Market & Acquisition
    s = new_slide(prs, number=8)
    title(s, "Go-to-Market & Client Acquisition")
    text(s, X0, TOP, 3.90, 0.24, ["Target industries"], size=T_CAPTION, color=NAVY, bold=True)
    industries = [
        "Healthcare",
        "Finance",
        "Government & Public Policy",
        "Donor & Non-Profit Sector",
        "Academia & Education",
    ]
    for i, label in enumerate(industries):
        y = 1.58 + i * 0.46
        text(s, X0, y, 0.30, 0.26, [f"{i + 1}"], size=T_BODY_SM, color=CYAN, bold=True)
        text(s, X0 + 0.30, y, 3.55, 0.26, [label], size=T_BODY_SM, color=GREY_DARK)

    rect(s, 4.95, TOP, 4.55, 1.60, GREY_LIGHT)
    text(
        s, 5.12, 1.38, 4.20, 0.24, ["Competitive landscape"], size=T_CAPTION, color=NAVY, bold=True
    )
    text(
        s,
        5.12,
        1.66,
        4.20,
        0.90,
        [
            [
                ("The \u201cAI company builder\u201d category has ", {}),
                ("no direct local equivalent identified", {"color": CYAN, "bold": True}),
                (".", {}),
            ],
            [("Key players: BCG, Deloitte Africa, Accenture, Qhala.", {})],
        ],
        size=T_CAPTION,
        color=GREY_DARK,
    )

    text(
        s,
        4.95,
        3.02,
        4.55,
        0.24,
        ["Client acquisition model"],
        size=T_CAPTION,
        color=NAVY,
        bold=True,
    )
    flow = [
        "15\u201320 buyer discovery calls",
        "Design partner program (2\u20133)",
        "Spin-out with dedicated leadership",
        "Ongoing studio support",
    ]
    for i, label in enumerate(flow):
        y = 3.32 + i * 0.45
        rect(s, 4.95, y, 4.55, 0.38, WHITE, line=GREY_LIGHT)
        text(s, 5.07, y + 0.08, 0.30, 0.22, [f"{i + 1}"], size=T_CAPTION, color=RED, bold=True)
        text(s, 5.35, y + 0.08, 4.05, 0.22, [label], size=T_CAPTION, color=NAVY)

    text(
        s,
        X0,
        5.16,
        CONTENT_W,
        0.24,
        ["Four reservations, applied to every client engagement"],
        size=T_CAPTION,
        color=NAVY,
        bold=True,
    )
    theses = [
        ("Constraint-first", "Design inside real bandwidth, budget, and data limits."),
        ("AI-agnostic", "Any provider, including local models."),
        ("PII-first", "Redaction before inference, by default."),
        ("Capital-efficient", "Shared infrastructure instead of duplicated builds."),
    ]
    for i, (head, body) in enumerate(theses):
        x = X0 + (i % 2) * 4.45
        y = 5.50 + (i // 2) * 0.56
        rect(s, x, y + 0.04, 0.09, 0.09, RED)
        text(s, x + 0.20, y, 1.70, 0.24, [head], size=T_CAPTION, color=NAVY, bold=True)
        text(s, x + 1.95, y, 2.35, 0.44, [body], size=T_CAPTION, color=GREY_DARK)
    notes(
        s,
        "Lead with the empty category, not with a first-mover boast: no direct local equivalent was "
        "identified. The acquisition path is discovery calls, design partners, spin-out, support.",
    )

    # ---------------------------------------------- 9. Governance & Compliance
    s = new_slide(prs, number=9)
    title(s, "Governance & Compliance")
    for i in range(5):
        x = X0 + i * 1.79
        rect(s, x, TOP, 1.70, 0.56, NAVY)
        text(
            s,
            x,
            TOP + 0.16,
            1.70,
            0.24,
            [f"Tier {i + 1}"],
            size=T_CAPTION,
            color=WHITE,
            bold=True,
            align=PP_ALIGN.CENTER,
        )
    text(
        s,
        X0,
        1.90,
        CONTENT_W,
        0.24,
        [
            "5-tier approval matrix (GAP-003): every privileged tool call passes tier gating before execution."
        ],
        size=T_CAPTION,
        color=GREY_DARK,
    )

    gov = [
        "Deny by default. Assume breach. Every finding gets a severity rating and a remediation timeline.",
        [
            ("Dashboard CORS: explicit allowlist, ", {}),
            ("never wildcard", {"color": RED, "bold": True}),
            (" (GAP-010/011).", {}),
        ],
        "PII guardrails: the proxy redacts or hashes PII before LLM requests; schema validation on all outputs (GAP-002/011).",
        "Compliance coverage: SOC 2 Type II controls mapped, certification pending; GDPR and industry-specific regulations mapped to agent actions.",
        "Dashboard auth is fail-closed by default; open mode is loopback-only and must be explicitly opted in (ADR-013).",
    ]
    for i, item in enumerate(gov):
        y = 2.30 + i * 0.62
        rect(s, X0, y + 0.05, 0.09, 0.09, RED if i in (1, 2) else NAVY)
        text(s, X0 + 0.24, y, 8.50, 0.56, [item], size=T_BODY_SM, color=GREY_DARK)

    rect(s, X0, 5.86, 0.08, 0.66, RED)
    rect(s, X0 + 0.08, 5.86, CONTENT_W - 0.08, 0.66, GREY_LIGHT)
    text(
        s,
        X0 + 0.26,
        5.98,
        CONTENT_W - 0.44,
        0.44,
        ["Security by default. Governance is enforced in code and CI, not in policy documents."],
        size=T_CAPTION,
        color=NAVY,
        bold=True,
    )
    notes(
        s,
        "Governance is concrete: five approval tiers, an explicit CORS allowlist, a PII proxy, and "
        "fail-closed auth. Two claims are worth spelling out: never a wildcard, and deny by default.",
    )

    # -------------------------------------- 10. What You Get as a Studio Partner
    s = new_slide(prs, number=10)
    title(s, "What You Get as a Studio Partner")
    table(
        s,
        X0,
        TOP,
        [2.90, 1.90, 4.05],
        [
            ["Deliverable", "Phase", "Scope & Timing"],
            ["Strategic validation", "1 (Discovery)", "Weeks 1\u20132"],
            ["Proof-of-concept", "2 (Validation)", "Weeks 3\u20136"],
            ["Minimum Viable Architecture", "3 (Build)", "Weeks 7\u201314"],
            ["Spin-out support", "4 (Scale)", "Month 4+"],
            [
                "Shared infrastructure",
                "Ongoing",
                "Model mesh, agent stacks, data pipelines, GTM engines",
            ],
            ["KPI dashboard", "Ongoing", "7-department real-time monitoring (planned)"],
            ["Governance compliance", "Ongoing", "5-tier approval, PII guardrails, CORS lockdown"],
        ],
        row_h=0.545,
        head_h=0.40,
    )
    caption(s, "All Parts 1\u20135 shipped September 2026.")
    notes(
        s,
        "This is the commercial summary: one table, phased, with the ongoing layer called out "
        "separately from the gated deliverables.",
    )

    # ------------------------------------------------------------- 11. Next Steps
    s = new_slide(prs, number=11)
    title(s, "Next Steps")
    steps = [
        ("Strategic alignment call", "60 min", "Validate thesis fit and portfolio archetype."),
        ("Discovery phase", "2 weeks", "Problem discovery and thesis definition."),
        ("Buyer discovery", "15\u201320 calls", "Structured calls across target accounts."),
        (
            "Go / No-Go decision",
            "After gate",
            "Based on positive commitments and technical feasibility.",
        ),
        (
            "Spin-out execution",
            "Month 4+",
            "Dedicated leadership, capitalization, and studio transition.",
        ),
    ]
    for i, (head, when, body) in enumerate(steps):
        y = TOP + i * 0.90
        text(s, X0, y + 0.02, 0.36, 0.30, [f"{i + 1}"], size=T_SUBTITLE, color=NAVY, bold=True)
        text(s, X0 + 0.40, y, 3.30, 0.26, [head], size=T_BODY_SM, color=NAVY, bold=True)
        text(s, X0 + 0.40, y + 0.28, 3.60, 0.44, [body], size=T_CAPTION, color=GREY_DARK)
        rect(s, 4.35, y + 0.04, 1.05, 0.30, GREY_LIGHT)
        text(
            s, 4.35, y + 0.09, 1.05, 0.22, [when], size=T_CAPTION, color=NAVY, align=PP_ALIGN.CENTER
        )

    rect(s, 5.75, TOP, 3.75, 1.50, NAVY)
    text(s, 5.95, 1.40, 3.35, 0.24, ["Contact"], size=T_CAPTION, color=CYAN, bold=True)
    text(s, 5.95, 1.70, 3.35, 0.30, ["Chief of Staff"], size=T_SUBTITLE, color=WHITE, bold=True)
    text(
        s,
        5.95,
        2.06,
        3.35,
        0.50,
        ["Lightspeed Holdings Limited\u2122"],
        size=T_CAPTION,
        color=WHITE,
    )
    text(
        s,
        5.75,
        2.95,
        3.75,
        0.80,
        ["AI Venture Studio Execution Plan Parts 1\u20135 (September 2026)"],
        size=T_CAPTION,
        color=GREY_DARK,
    )
    text(
        s,
        X0,
        5.85,
        CONTENT_W,
        0.85,
        [
            "This presentation is based on the AI Venture Studio execution plan documented in "
            "brand/ai_venture_studio_execution_plan.md and docs/venture-studio/. All Parts 1\u20135 shipped "
            "September 2026. AI-agnostic: works with any LLM provider (OpenAI, Anthropic, DeepSeek, local "
            "Ollama). Malawi-first constraint-export pattern applies."
        ],
        size=T_CAPTION,
        color=GREY_DARK,
    )
    notes(
        s,
        "Close on the next five moves. The first is a decision, not a workshop: a 60-minute alignment "
        "call that picks the archetype.",
    )

    # ------------------------------------------- 12. Brand Compliance Checklist
    s = new_slide(prs, number=12)
    title(s, "Brand Compliance Checklist")
    checks = [
        "Logo from official assets, never recreated",
        'Logo clear space respected (1\u00d7 "L" height on all sides)',
        "Only palette colors used (navy #070A40, red #E63946, cyan #00BFFF, grey-light #F2F2F2, white #FFFFFF)",
        "Vector format for print; transparent treatment on dark",
        "\u2122 on first mention of the company name",
        "Type sizes from the brand scale in brand-tokens.json",
        "Spacing multiples of 4px (base unit)",
        'Tagline spelled exactly "ASPIRE. ACT. ACHIEVE."',
    ]
    for i, item in enumerate(checks):
        x = X0 + (i % 2) * 4.55
        y = TOP + (i // 2) * 1.15
        rect(s, x, y + 0.06, 0.11, 0.11, RED)
        text(s, x + 0.26, y, 3.95, 0.95, [item], size=T_BODY_SM, color=NAVY)
    caption(
        s,
        "Any deviation requires a documented brand decision approved by the Brand Strategist / CMO.",
    )
    notes(
        s,
        "Appendix: the checklist used to sign this deck off against brand guidelines section 9. "
        "Deviations are documented, not silent.",
    )

    # ------------------------------------------------------ 13. Closing (navy)
    s = new_slide(prs, navy=True, chrome=False)
    text(
        s,
        X0,
        2.20,
        CONTENT_W,
        0.80,
        ["Thank You"],
        size=T_DISPLAY_XL,
        color=WHITE,
        bold=True,
        align=PP_ALIGN.CENTER,
    )
    rect(s, 4.20, 3.30, 1.60, 0.04, CYAN)
    logo(s, CLOSING_LOGO_X_IN, CLOSING_LOGO_Y_IN, CLOSING_LOGO_W_IN)
    text(
        s,
        X0,
        6.24,
        CONTENT_W,
        0.30,
        ["ASPIRE. ACT. ACHIEVE."],
        size=T_SUBTITLE,
        color=CYAN,
        align=PP_ALIGN.CENTER,
    )
    notes(
        s,
        "Closing. Full navy, official lockup, cyan tagline. No new content on this slide.",
    )

    prs.save(out_path)
    print(f"wrote {out_path} ({len(prs.slides.__iter__.__self__._sldIdLst)} slides)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="ai_venture_studio_client_presentation.pptx")
    args = parser.parse_args()
    build(args.output)


if __name__ == "__main__":
    main()
