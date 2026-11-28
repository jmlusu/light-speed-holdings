"""Build the Lightspeed Holdings value-proposition deck (10 slides, 10 x 7.5 in).

Content sources (all in this repository):
  - content/drafts/homepage.md sections 01-05, 06, 12
  - docs/venture-studio/02-sector-positioning.md
  - docs/venture-studio/03-operating-model.md
  - docs/venture-studio/05-kpi-scorecard.md
  - ai_venture_studio_client_presentation.md
  - src/components/haomtgv/layers.ts

Brand contract: brand/tokens.md and brand/guidelines/brand-guidelines.md
  - Navy #070A40 dominant; red #E63946 and cyan #00BFFF as bounded accents.
  - Arial only; sizes from the 36/32/28/24/18/16/14/13/12 pt scale.
  - Official logo assets only; 0.15 in navy rail on content slides.

Run:
    python presentations/lightspeed-value-proposition-2026/build_deck.py
"""

from __future__ import annotations

import argparse
import io
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls, qn
from pptx.util import Inches, Pt

# ----------------------------------------------------------------- brand tokens
NAVY = RGBColor(0x07, 0x0A, 0x40)
RED = RGBColor(0xE6, 0x39, 0x46)
CYAN = RGBColor(0x00, 0xBF, 0xFF)
GREY_LIGHT = RGBColor(0xF2, 0xF2, 0xF2)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREY_DARK = RGBColor(0x6B, 0x72, 0x80)
GREY_TEXT_DARK = RGBColor(0x9C, 0xA3, 0xAF)

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

# ---------------------------------------------------------------------- layout
SLIDE_W = 10.0
SLIDE_H = 7.5
RAIL_W = 0.15
X0 = 0.65
X1 = 9.35
CONTENT_W = X1 - X0
FOOTER_Y = 6.98

REPO = Path(__file__).resolve().parents[2]
LOGO_DARK = REPO / "brand" / "logo" / "logo-dark-bg-transparent.png"
LOGO_LIGHT = REPO / "brand" / "logo" / "logo-light-bg-transparent.png"

DEFAULT_OUT = Path(__file__).with_name("Lightspeed-Value-Proposition-HAOMTGV-Venture-Studio.pptx")

COMPANY = "LightSpeed Holdings Limited"


# -------------------------------------------------------------------- helpers
def slide_bg(slide, color: RGBColor) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def box(
    slide,
    x,
    y,
    w,
    h,
    fill: RGBColor | None = None,
    line: RGBColor | None = None,
    line_w: float = 1.0,
    shape=MSO_SHAPE.RECTANGLE,
    dash: bool = False,
):
    sh = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.shadow.inherit = False
    style = sh._element.find(qn("p:style"))
    if style is not None:
        sh._element.remove(style)
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(line_w)
        if dash:
            sh.line.dash_style = MSO_LINE.DASH
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
    line_spacing=1.16,
    space_after=0,
):
    """paras: list of str | (str, overrides) | list of (str, overrides)."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    for i, spec in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        para.line_spacing = line_spacing
        para.space_after = Pt(space_after)
        runs = spec if isinstance(spec, list) else [(spec, {})]
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


def logo(slide, path: Path, x: float, width: float, top: float | None = None):
    """Place an official transparent lockup, cropped to its visible pixels."""
    with Image.open(path) as im:
        alpha = im.convert("RGBA").getchannel("A")
        bbox = alpha.getbbox()
        buf = io.BytesIO()
        im.convert("RGBA").crop(bbox).save(buf, format="PNG")
    buf.seek(0)
    pic = slide.shapes.add_picture(buf, Inches(x), Inches(top or 0.0), width=Inches(width))
    return pic


def header(slide, eyebrow: str, title: str, number: int, title_size=T_TITLE_LG):
    """Standard content-slide chrome: navy rail, eyebrow, title, accent rule."""
    box(slide, 0, 0, RAIL_W, SLIDE_H, NAVY)
    text(slide, X0, 0.42, CONTENT_W, 0.24, [eyebrow], size=T_CAPTION, color=RED, bold=True)
    text(slide, X0, 0.68, CONTENT_W, 0.55, [title], size=title_size, color=NAVY, bold=True)
    box(slide, X0, 1.30, 0.55, 0.035, CYAN)
    footer(slide, number)


def footer(slide, number: int, color=GREY_DARK):
    text(
        slide,
        X0,
        FOOTER_Y,
        6.2,
        0.22,
        [COMPANY + "  \u00b7  Executive briefing"],
        size=T_CAPTION,
        color=color,
    )
    text(
        slide,
        8.60,
        FOOTER_Y,
        0.75,
        0.22,
        [f"{number:02d}"],
        size=T_CAPTION,
        color=color,
        align=PP_ALIGN.RIGHT,
    )


def caption(slide, txt: str, y: float = 6.52, color=GREY_DARK):
    text(slide, X0, y, CONTENT_W, 0.30, [txt], size=T_CAPTION, color=color)


def notes(slide, txt: str):
    slide.notes_slide.notes_text_frame.text = txt


def bullet_list(slide, x, y, w, items, size=T_BODY_SM, gap=0.36, marker=CYAN, color=GREY_DARK):
    for i, item in enumerate(items):
        top = y + i * gap
        box(slide, x, top + 0.06, 0.075, 0.075, marker)
        text(slide, x + 0.20, top, w - 0.20, gap, [item], size=size, color=color, line_spacing=1.12)


def arrow_down(slide, cx: float, y: float, h: float = 0.26):
    box(slide, cx - 0.045, y, 0.09, h, NAVY)
    box(
        slide, cx - 0.13, y + h, 0.26, 0.14, NAVY, shape=MSO_SHAPE.ISOSCELES_TRIANGLE
    ).rotation = 180


def connector(slide, pts, color=CYAN, width=1.5):
    """Draw a polyline through pts [(x, y), ...]; arrowhead on the final segment."""
    last = None
    for (x1, y1), (x2, y2) in zip(pts, pts[1:], strict=False):
        last = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2)
        )
        last.line.color.rgb = color
        last.line.width = Pt(width)
    if last is not None:
        ln = last.line._get_or_add_ln()
        ln.append(parse_xml(f'<a:tailEnd {nsdecls("a")} type="triangle" w="med" len="med"/>'))


# ----------------------------------------------------------------------- deck
def build(out_path: Path) -> None:
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)

    # ------------------------------------------------------------ 1. cover
    s = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(s, NAVY)
    box(s, 0, 0, 0.15, SLIDE_H, RED)
    logo(s, LOGO_DARK, 0.65, 2.55, 0.52)

    text(
        s,
        0.65,
        3.16,
        8.6,
        0.24,
        ["EXECUTIVE BRIEFING  \u00b7  NOVEMBER 2026"],
        size=T_CAPTION,
        color=CYAN,
        bold=True,
    )
    text(
        s,
        0.65,
        3.48,
        8.7,
        1.55,
        ["The LightSpeed value proposition"],
        size=T_DISPLAY_XL,
        color=WHITE,
        bold=True,
        line_spacing=1.05,
    )
    box(s, 0.65, 4.62, 0.90, 0.04, RED)
    text(
        s,
        0.65,
        4.86,
        8.0,
        0.70,
        ["One governed operating model. Proven on ourselves. Packaged for you to own."],
        size=T_SUBTITLE,
        color=GREY_TEXT_DARK,
        line_spacing=1.25,
    )
    text(
        s,
        0.65,
        5.62,
        6.0,
        0.30,
        [[("HAOMTGV operating framework  \u00b7  AI Venture Studio", {"color": CYAN})]],
        size=T_BODY_SM,
        color=CYAN,
    )
    text(s, 0.65, 6.62, 5.0, 0.24, ["Lilongwe, Malawi"], size=T_CAPTION, color=GREY_TEXT_DARK)
    notes(
        s,
        "We are LightSpeed Holdings. We build and govern AI-native operations from Lilongwe. "
        "I am going to show you one thing: how we run our own company, and how that becomes "
        "something you can own. Not a pitch about models. A description of decision rights, "
        "audit trails, and what it costs to operate. Then you decide whether it fits.",
    )

    # -------------------------------------------------------------- 2. gap
    s = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(s, WHITE)
    header(s, "THE GAP", "AI adoption is not the problem.", 2)
    text(
        s,
        X0,
        1.55,
        7.9,
        0.55,
        [
            "The binding constraint is decision rights: who authorises what, and what record remains afterwards."
        ],
        size=T_BODY_LG,
        color=GREY_DARK,
        line_spacing=1.2,
    )

    gap_cards = [
        (
            "01",
            "Experiments multiply",
            "Pilots run outside an operating model, so each teaches the organisation little.",
        ),
        (
            "02",
            "Authority is unnamed",
            "No one can say which agent may act, at what risk, and who must approve it.",
        ),
        (
            "03",
            "Evidence is thin",
            "When the board asks what happened, there is no tamper-evident record to show.",
        ),
    ]
    for i, (num, head, body) in enumerate(gap_cards):
        x = X0 + i * 2.95
        box(s, x, 2.35, 2.72, 2.55, GREY_LIGHT)
        box(s, x, 2.35, 2.72, 0.045, RED if i == 0 else (CYAN if i == 1 else NAVY))
        text(
            s,
            x + 0.26,
            2.60,
            0.7,
            0.33,
            [num],
            size=T_TITLE_SM,
            color=RED if i == 0 else NAVY,
            bold=True,
        )
        text(s, x + 0.26, 2.96, 2.20, 0.62, [head], size=T_TITLE_SM, color=NAVY, bold=True)
        text(
            s,
            x + 0.26,
            3.72,
            2.22,
            1.10,
            [body],
            size=T_BODY_SM,
            color=GREY_DARK,
            line_spacing=1.20,
        )

    box(s, X0, 5.02, CONTENT_W, 1.12, NAVY)
    text(
        s,
        X0 + 0.32,
        5.22,
        5.55,
        0.75,
        [
            [
                ("The region has AI projects.", {"color": WHITE, "bold": True}),
                (
                    "It does not yet have a governed agentic operating model.",
                    {"color": GREY_TEXT_DARK},
                ),
            ]
        ],
        size=T_BODY_LG,
        line_spacing=1.22,
    )
    text(
        s,
        X0 + 6.05,
        5.22,
        2.35,
        0.75,
        ["Category \u201cAI company builder\u201d is empty locally (internal 2026-09 scan)."],
        size=T_CAPTION,
        color=CYAN,
        line_spacing=1.15,
    )
    caption(
        s,
        "Sources: docs/venture-studio/02-sector-positioning.md \u00a73; docs/venture-studio/03-operating-model.md \u00a71.",
    )
    notes(
        s,
        "Most AI programmes stall because authority was never assigned, so nothing is auditable. "
        "Three symptoms: experiments multiply, authority stays unnamed, and evidence is thin. "
        "The fix is not a better model. It is an operating model with named gates. That begins with the letter H.",
    )

    # ----------------------------------------------------- 3. value proposition
    s = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(s, NAVY)
    box(s, 0, 0, 0.15, SLIDE_H, RED)
    text(s, X0, 0.55, 8.0, 0.24, ["THE VALUE PROPOSITION"], size=T_CAPTION, color=CYAN, bold=True)
    text(
        s,
        X0,
        0.92,
        8.6,
        1.75,
        ["One operating model.", "Proven on ourselves.", "Packaged for you to own."],
        size=T_TITLE_XL,
        color=WHITE,
        bold=True,
        line_spacing=1.12,
    )
    text(
        s,
        X0,
        2.66,
        8.6,
        0.34,
        ["Proven in-house today. Studio targets ahead. No client deployments yet."],
        size=T_BODY_LG,
        color=CYAN,
    )
    box(s, X0, 3.08, 0.90, 0.04, RED)

    pillars = [
        (
            "GOVERNED BY DESIGN",
            "Five tiers of human approval sit above every agent action, with an append-only audit record.",
            CYAN,
        ),
        (
            "PROVEN IN-HOUSE",
            "The same framework runs LightSpeed: 89 AI agents and one Human CEO across 20 departments.",
            RED,
        ),
        (
            "PACKAGED TO SPIN OUT",
            "The Venture Studio reuses one governed core, so each new venture inherits the gates.",
            CYAN,
        ),
    ]
    for i, (head, body, accent) in enumerate(pillars):
        x = X0 + i * 2.95
        box(s, x, 3.42, 0.045, 2.10, accent)
        text(s, x + 0.22, 3.42, 2.45, 0.28, [head], size=T_CAPTION, color=accent, bold=True)
        text(
            s,
            x + 0.22,
            3.82,
            2.45,
            1.65,
            [body],
            size=T_BODY_SM,
            color=GREY_TEXT_DARK,
            line_spacing=1.28,
        )

    text(
        s,
        X0,
        5.80,
        8.6,
        0.28,
        ["AI executes. Humans decide."],
        size=T_BODY_LG,
        color=WHITE,
        bold=True,
    )
    caption(
        s,
        "Sources: content/drafts/homepage.md \u00a704-\u00a706, \u00a712; all counts labelled PROVEN IN-HOUSE.",
        y=6.46,
        color=GREY_TEXT_DARK,
    )
    notes(
        s,
        "This is the whole proposition in three lines. One operating model, not a tool. "
        "Proven on ourselves, not on a slide. Packaged to spin out, not bespoke forever. "
        "The phrase to hold onto is: AI executes, humans decide. Everything that follows is evidence for that sentence.",
    )

    # --------------------------------------------------------- 4. HAOMTGV
    s = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(s, WHITE)
    header(s, "THE OPERATING FRAMEWORK", "H-A-O-M-T-G-V: seven layers.", 4)
    text(
        s,
        X0,
        1.52,
        6.0,
        0.30,
        ["Human authority at the top. Value at the bottom, returning to intent."],
        size=T_BODY,
        color=GREY_DARK,
    )

    layers = [
        (
            "H",
            "Human authority",
            "People set intent and hold final decision authority.",
            NAVY,
            WHITE,
            CYAN,
        ),
        ("A", "Agents", "89 specialised AI roles plus one Human CEO.", GREY_LIGHT, NAVY, NAVY),
        (
            "O",
            "Orchestration",
            "Deterministic routing of tasks, handoffs and decisions.",
            GREY_LIGHT,
            NAVY,
            NAVY,
        ),
        ("M", "Memory", "Persistent context across long-running work.", GREY_LIGHT, NAVY, NAVY),
        ("T", "Tools", "Isolated execution environments for API actions.", GREY_LIGHT, NAVY, NAVY),
        (
            "G",
            "Governance",
            "Five-tier approval and append-only sealed logging.",
            RED,
            WHITE,
            WHITE,
        ),
        (
            "V",
            "Value",
            "Measured outcomes become evidence for the next decision.",
            NAVY,
            WHITE,
            CYAN,
        ),
    ]
    top0, bar_h, gap = 1.95, 0.50, 0.105
    for i, (letter, name, desc, fill, fg, letter_color) in enumerate(layers):
        y = top0 + i * (bar_h + gap)
        box(s, X0, y, 5.20, bar_h, fill, line=None if fill != GREY_LIGHT else GREY_LIGHT)
        text(
            s,
            X0 + 0.16,
            y,
            0.38,
            bar_h,
            [letter],
            size=T_TITLE_MD,
            color=letter_color,
            bold=True,
            anchor=MSO_ANCHOR.MIDDLE,
        )
        text(
            s,
            X0 + 0.60,
            y,
            1.72,
            bar_h,
            [name],
            size=T_BODY,
            color=fg,
            bold=True,
            anchor=MSO_ANCHOR.MIDDLE,
        )
        text(
            s,
            X0 + 2.42,
            y,
            2.62,
            bar_h,
            [desc],
            size=T_CAPTION,
            color=fg if fg == WHITE else GREY_DARK,
            anchor=MSO_ANCHOR.MIDDLE,
            line_spacing=1.05,
        )

    # closed loop from Value back to Human
    y_h = top0 + bar_h / 2
    y_v = top0 + 6 * (bar_h + gap) + bar_h / 2
    connector(s, [(X0 + 5.20, y_v), (5.98, y_v), (5.98, y_h), (X0 + 5.20, y_h)])
    text(
        s,
        X0,
        y_v + 0.30,
        5.2,
        0.24,
        ["Value returns to Human as evidence, not as a report."],
        size=T_CAPTION,
        color=CYAN,
        bold=True,
    )

    text(s, 6.45, 1.95, 2.90, 0.24, ["HOW TO READ IT"], size=T_CAPTION, color=RED, bold=True)
    bullet_list(
        s,
        6.45,
        2.30,
        2.90,
        [
            "Authority flows down: intent becomes bounded work.",
            "Control is vertical: governance gates every layer.",
            "Value flows up: outcomes become evidence.",
        ],
        size=T_BODY_SM,
        gap=0.78,
    )

    box(s, 6.45, 4.88, 2.90, 1.45, NAVY)
    text(
        s,
        6.65,
        5.08,
        2.55,
        0.82,
        ["This is our own architecture. It runs LightSpeed every day."],
        size=T_BODY,
        color=WHITE,
        bold=True,
        line_spacing=1.20,
    )
    text(s, 6.65, 6.04, 2.55, 0.22, ["PROVEN IN-HOUSE"], size=T_CAPTION, color=CYAN, bold=True)
    caption(s, "Sources: src/components/haomtgv/layers.ts; content/drafts/homepage.md \u00a704.")
    notes(
        s,
        "Read this top-down. H is not a mascot; it is the decision layer. A does bounded work, O routes it, "
        "M keeps state, T acts on the world, and G gates every step. V is not the end of the diagram. "
        "It returns to H as evidence, which is why the loop closes. This is the architecture we run.",
    )

    # -------------------------------------------------------------- 5. H + A
    s = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(s, WHITE)
    header(s, "H + A", "Intent above. Execution below.", 5)
    text(
        s,
        X0,
        1.52,
        8.4,
        0.30,
        ["The human layer is not a reviewer at the end. It is the authority at the start."],
        size=T_BODY,
        color=GREY_DARK,
    )

    box(s, X0, 1.98, 4.20, 3.35, GREY_LIGHT)
    text(s, X0 + 0.28, 2.12, 0.60, 0.60, ["H"], size=T_DISPLAY_XL, color=RED, bold=True)
    text(
        s, X0 + 0.28, 2.78, 3.60, 0.30, ["Human authority"], size=T_TITLE_SM, color=NAVY, bold=True
    )
    bullet_list(
        s,
        X0 + 0.28,
        3.22,
        3.62,
        [
            "People set operational intent.",
            "The Human CEO holds vision, budgets, culture and accountability.",
            "Agents act at explicit direction, never above the human layer.",
        ],
        size=T_BODY_SM,
        gap=0.66,
        marker=RED,
    )

    box(s, 5.15, 1.98, 4.20, 3.35, NAVY)
    text(s, 5.43, 2.12, 0.60, 0.60, ["A"], size=T_DISPLAY_XL, color=CYAN, bold=True)
    text(
        s, 5.43, 2.70, 3.60, 0.34, ["89 AI agents. 1 CEO."], size=T_TITLE_SM, color=WHITE, bold=True
    )
    text(
        s,
        5.43,
        3.34,
        3.62,
        0.50,
        ["Ninety roles across twenty departments, each with an explicit, bounded scope."],
        size=T_BODY_SM,
        color=GREY_TEXT_DARK,
        line_spacing=1.20,
    )

    stats = [
        ("89", "AI agents"),
        ("1", "Human CEO"),
        ("20", "departments"),
        ("5", "approval tiers"),
    ]
    for i, (num, label) in enumerate(stats):
        x = 5.43 + (i % 2) * 1.78
        y = 3.98 + (i // 2) * 0.62
        text(s, x, y, 0.62, 0.34, [num], size=T_TITLE_MD, color=CYAN, bold=True)
        text(s, x + 0.58, y + 0.09, 1.15, 0.24, [label], size=T_CAPTION, color=GREY_TEXT_DARK)

    text(
        s,
        X0,
        5.72,
        8.4,
        0.34,
        ["90 roles. One accountable human."],
        size=T_TITLE_SM,
        color=NAVY,
        bold=True,
    )
    caption(s, "Sources: homepage.md \u00a706; operating-model.md \u00a71. PROVEN IN-HOUSE.")
    notes(
        s,
        "Authority sits above the system. The Human CEO holds vision, budget, culture and accountability. "
        "Below that are 89 specialised agents across twenty departments, each bounded. "
        "The number that matters is not 89. It is one accountable human. Now, specialisation only pays "
        "if the handoffs are deterministic.",
    )

    # ---------------------------------------------------------- 6. O + M + T
    s = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(s, WHITE)
    header(s, "O + M + T", "The work survives the model.", 6)
    text(
        s,
        X0,
        1.52,
        8.4,
        0.30,
        ["Routing, state and execution are what make long-running agentic work dependable."],
        size=T_BODY,
        color=GREY_DARK,
    )

    cols = [
        (
            "O",
            "Orchestration",
            "Deterministic routing of data, tasks and decisions across workflows.",
            [
                "Handoffs are explicit, not improvised.",
                "Workflow logic is decoupled from model inference.",
            ],
            RED,
        ),
        (
            "M",
            "Memory",
            "Persistent contextual state across long-running work.",
            [
                "Context survives API failures and interruptions.",
                "Long-horizon tasks keep their place.",
            ],
            CYAN,
        ),
        (
            "T",
            "Tools",
            "Isolated execution environments for APIs and actions.",
            [
                "Actions run in bounded sandboxes.",
                "Every tool call is observable and attributable.",
            ],
            NAVY,
        ),
    ]
    for i, (letter, name, lead, points, accent) in enumerate(cols):
        x = X0 + i * 2.95
        box(s, x, 1.98, 2.68, 3.40, GREY_LIGHT)
        box(s, x, 1.98, 2.68, 0.045, accent)
        text(s, x + 0.25, 2.14, 0.55, 0.50, [letter], size=T_TITLE_XL, color=accent, bold=True)
        text(s, x + 0.25, 2.72, 2.18, 0.30, [name], size=T_TITLE_SM, color=NAVY, bold=True)
        text(
            s,
            x + 0.25,
            3.10,
            2.18,
            0.78,
            [lead],
            size=T_BODY_SM,
            color=GREY_DARK,
            line_spacing=1.20,
        )
        bullet_list(s, x + 0.25, 3.98, 2.18, points, size=T_CAPTION, gap=0.62, marker=accent)

    box(s, X0, 5.55, CONTENT_W, 0.72, NAVY)
    text(
        s,
        X0 + 0.26,
        5.66,
        8.15,
        0.52,
        [
            [
                ("Model-agnostic by design.", {"color": WHITE, "bold": True}),
                (
                    "Open and local first; commercial only when materially better.",
                    {"color": GREY_TEXT_DARK},
                ),
            ]
        ],
        size=T_BODY_SM,
        line_spacing=1.15,
    )
    caption(
        s,
        "Sources: content/drafts/homepage.md \u00a704, \u00a707; docs/venture-studio/04-technical-architecture.md.",
    )
    notes(
        s,
        "Specialisation only pays if the handoffs hold. O makes routing deterministic. M keeps state across "
        "failures. T confines action to sandboxes. None of these are model features; they are systems features. "
        "And all three are worthless without an approval layer over them.",
    )

    # ---------------------------------------------------------------- 7. G
    s = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(s, NAVY)
    box(s, 0, 0, 0.15, SLIDE_H, RED)
    text(s, X0, 0.44, 8.0, 0.24, ["GOVERNANCE"], size=T_CAPTION, color=CYAN, bold=True)
    text(
        s,
        X0,
        0.70,
        8.6,
        0.55,
        [
            "G is the product.",
        ],
        size=T_TITLE_LG,
        color=WHITE,
        bold=True,
    )
    text(
        s,
        X0,
        1.38,
        8.6,
        0.32,
        ["Five tiers of approval, four mandatory gates, one append-only record."],
        size=T_BODY_LG,
        color=GREY_TEXT_DARK,
    )
    box(s, X0, 1.86, 0.55, 0.035, RED)

    tiers = [("1", "Auto"), ("2", "Lead"), ("3", "Executive"), ("4", "CEO"), ("5", "Board")]
    for i, (num, name) in enumerate(tiers):
        x = X0 + i * 1.77
        h = 0.85 + i * 0.12
        y = 3.55 - h
        box(s, x, y, 1.52, h, RED if i == 4 else NAVY, line=CYAN if i < 4 else RED, line_w=1.0)
        text(
            s,
            x + 0.14,
            y + 0.10,
            0.35,
            0.24,
            [num],
            size=T_CAPTION,
            color=CYAN if i < 4 else WHITE,
            bold=True,
        )
        text(s, x + 0.14, y + h - 0.38, 1.24, 0.30, [name], size=T_TITLE_SM, color=WHITE, bold=True)
    text(
        s,
        X0,
        3.70,
        8.6,
        0.24,
        ["Low risk  \u2192  escalating human authority  \u2192  high-stakes decisions"],
        size=T_CAPTION,
        color=GREY_TEXT_DARK,
    )

    gov = [
        ("FOUR GATES", "Contract, DPA, Compliance and Security reviews run before work begins."),
        (
            "SEALED RECORD",
            "Append-only SHA-256 audit trails of prompts, tools, outputs and approvals.",
        ),
        ("HUMAN SIGN-OFF", "No client-facing deliverable ships without a human decision."),
    ]
    for i, (head, body) in enumerate(gov):
        x = X0 + i * 2.95
        text(s, x, 4.05, 2.60, 0.24, [head], size=T_CAPTION, color=CYAN, bold=True)
        text(
            s, x, 4.35, 2.62, 1.05, [body], size=T_BODY_SM, color=GREY_TEXT_DARK, line_spacing=1.22
        )

    text(
        s,
        X0,
        5.66,
        8.6,
        0.30,
        ["Governance is not a cost centre. It is what makes autonomy defensible."],
        size=T_TITLE_SM,
        color=WHITE,
        bold=True,
    )
    caption(
        s,
        "Sources: content/drafts/homepage.md \u00a712; all controls labelled PROVEN IN-HOUSE.",
        color=GREY_TEXT_DARK,
    )
    notes(
        s,
        "This is the layer that sells. Five tiers, from automatic to Board. Four gates before work begins. "
        "One append-only record that cannot be rewritten. No client-facing deliverable leaves without a human "
        "signature. Governance is not a cost centre; it is what makes autonomy defensible.",
    )

    # ------------------------------------------------------ 8. venture studio
    s = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(s, WHITE)
    header(s, "THE VENTURE STUDIO", "A repeatable engine, not a pipeline.", 8)
    text(
        s,
        X0,
        1.50,
        8.4,
        0.28,
        ["The studio does not replace the operating company. It packages it."],
        size=T_BODY,
        color=GREY_DARK,
    )

    engine = [
        ("Strategic validation", "Thesis pressure-test, buyer discovery, kill/continue gates."),
        ("Agent orchestration", "MessageBus, router, HITL approvals, memory, tools."),
        ("Shared services & GTM", "Pricing, onboarding, proof pack, KPI dashboard, brand."),
    ]
    for i, (head, body) in enumerate(engine):
        x = X0 + i * 2.93
        box(s, x, 1.88, 2.76, 0.90, NAVY)
        text(s, x + 0.18, 1.98, 2.40, 0.26, [head], size=T_BODY_SM, color=WHITE, bold=True)
        text(
            s,
            x + 0.18,
            2.27,
            2.40,
            0.40,
            [body],
            size=T_CAPTION,
            color=GREY_TEXT_DARK,
            line_spacing=1.10,
        )

    box(s, 4.93, 2.86, 0.14, 0.28, NAVY, shape=MSO_SHAPE.DOWN_ARROW)

    ports = [
        (
            "A",
            "Enterprise Agent",
            "Department-scale agent workforce inside a client organisation.",
            False,
        ),
        (
            "B",
            "B2B AI Workflow",
            "Repeatable multi-step process: procurement, reporting, reconciliation.",
            False,
        ),
        (
            "C",
            "Sovereign Data",
            "In-country or on-prem deployment with data-residency controls.",
            False,
        ),
        ("D", "Consumer Platforms", "Opens only when A\u2013C score green for two quarters.", True),
    ]
    for i, (letter, name, body, gated) in enumerate(ports):
        x = X0 + i * 2.20
        box(
            s,
            x,
            3.18,
            2.06,
            1.86,
            WHITE,
            line=NAVY if not gated else GREY_DARK,
            line_w=1.0,
            dash=gated,
        )
        box(
            s,
            x + 0.16,
            3.32,
            0.38,
            0.38,
            NAVY if not gated else WHITE,
            line=None if not gated else GREY_DARK,
        )
        text(
            s,
            x + 0.16,
            3.32,
            0.38,
            0.38,
            [letter],
            size=T_BODY,
            color=WHITE if not gated else GREY_DARK,
            bold=True,
            align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.MIDDLE,
        )
        text(
            s,
            x + 0.16,
            3.82,
            1.78,
            0.24,
            [name],
            size=T_BODY_SM,
            color=NAVY if not gated else GREY_DARK,
            bold=True,
        )
        text(
            s,
            x + 0.16,
            4.12,
            1.78,
            0.82,
            [body],
            size=T_CAPTION,
            color=GREY_DARK,
            line_spacing=1.15,
        )
        if gated:
            text(s, x + 0.62, 3.40, 1.26, 0.22, ["GATED"], size=T_CAPTION, color=RED, bold=True)

    text(
        s,
        X0,
        5.28,
        8.4,
        0.24,
        ["FOUR RESERVATIONS THE STUDIO MUST SATISFY"],
        size=T_CAPTION,
        color=RED,
        bold=True,
    )
    reservations = ["Constraint-first", "AI-agnostic", "PII-first", "Capital-efficient"]
    for i, item in enumerate(reservations):
        x = X0 + i * 2.20
        box(s, x, 5.58, 0.075, 0.075, RED)
        text(s, x + 0.18, 5.50, 1.85, 0.24, [item], size=T_BODY_SM, color=NAVY, bold=True)

    text(
        s,
        X0,
        5.98,
        8.6,
        0.30,
        [
            [
                ("Shared core before differentiation.", {"color": RED, "bold": True}),
                ("  No venture forks its own approval, audit or model routing.", {"color": NAVY}),
            ]
        ],
        size=T_BODY,
        line_spacing=1.15,
    )
    caption(
        s,
        "Sources: docs/venture-studio/03-operating-model.md \u00a72-\u00a75; ai_venture_studio_client_presentation.md \u00a72.",
    )
    notes(
        s,
        "The studio is not a project pipeline. It is an engine with three reusable parts: validation, "
        "orchestration and shared services. A, B and C are the venture shapes. D is deliberately gated. "
        "The discipline is shared core before differentiation: no venture forks its own approval, audit or router.",
    )

    # ---------------------------------------------------- 9. gates + metrics
    s = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(s, WHITE)
    header(s, "THE METHOD", "Four gates. Four numbers.", 9)
    text(
        s,
        X0,
        1.52,
        8.4,
        0.28,
        [
            "No venture advances without a written exit criterion. A failed gate parks or kills the work."
        ],
        size=T_BODY,
        color=GREY_DARK,
    )

    phases = [
        ("1", "Discovery", "Weeks 1\u20132", "Written thesis, sector fit and a named owner."),
        (
            "2",
            "Validation",
            "Weeks 3\u20136",
            "PoC on real data; 15\u201320 structured buyer calls.",
        ),
        (
            "3",
            "Build",
            "Weeks 7\u201314",
            "MVA deployed to 2\u20133 design partners; ATC baseline.",
        ),
        ("4", "Scale", "Month 4+", "Spin-out formed; leadership and capital in place."),
    ]
    for i, (num, name, when, gate) in enumerate(phases):
        x = X0 + i * 2.20
        box(s, x, 1.92, 0.42, 0.42, NAVY)
        text(
            s,
            x,
            1.92,
            0.42,
            0.42,
            [num],
            size=T_BODY_SM,
            color=WHITE,
            bold=True,
            align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.MIDDLE,
        )
        if i < 3:
            box(s, x + 0.52, 2.11, 1.55, 0.02, CYAN)
        text(s, x, 2.48, 2.05, 0.30, [name], size=T_TITLE_SM, color=NAVY, bold=True)
        text(s, x, 2.82, 2.05, 0.22, [when], size=T_CAPTION, color=RED, bold=True)
        text(s, x, 3.10, 2.02, 0.90, [gate], size=T_CAPTION, color=GREY_DARK, line_spacing=1.18)

    box(s, X0, 4.12, CONTENT_W, 0.02, GREY_LIGHT)

    metrics = [
        (
            ">90%",
            "Agentic completion",
            "Tasks completed without manual intervention. PROVEN IN-HOUSE goal.",
        ),
        ("<60 days", "Velocity to MVP", "Thesis approval to deployment. Studio target."),
        ("Tracked", "Manual correction", "Human overrides per 1,000 actions. Governance measure."),
        ("3\u20135\u00d7", "Capital Efficiency", "Output per capital unit vs seed. Studio target."),
    ]
    for i, (num, label, body) in enumerate(metrics):
        x = X0 + i * 2.20
        text(s, x, 4.32, 2.05, 0.42, [num], size=T_TITLE_LG, color=NAVY, bold=True)
        text(
            s,
            x,
            4.82,
            2.02,
            0.30,
            [label],
            size=T_BODY_SM,
            color=RED if i == 3 else NAVY,
            bold=True,
        )
        text(s, x, 5.14, 2.02, 0.68, [body], size=T_CAPTION, color=GREY_DARK, line_spacing=1.15)

    box(s, X0, 6.00, CONTENT_W, 0.40, GREY_LIGHT)
    text(
        s,
        X0 + 0.18,
        6.07,
        8.35,
        0.26,
        [
            "Studio commitments are internal goals. The 3\u20135\u00d7 figure is a baseline comparison, not a client result."
        ],
        size=T_CAPTION,
        color=GREY_DARK,
    )
    caption(
        s,
        "Sources: docs/venture-studio/05-kpi-scorecard.md \u00a71-\u00a72; docs/venture-studio/03-operating-model.md \u00a73.",
        y=6.52,
    )
    notes(
        s,
        "Discovery, validation, build, scale. Each has a written exit criterion, and a failed gate parks or "
        "kills the venture. Four numbers keep it honest: ATC above ninety percent, velocity under sixty days, "
        "correction ratio tracked, and capital efficiency targeting three to five times. Each figure is a studio "
        "goal or measure, not a client outcome; the three-to-five times figure is a baseline comparison. This is the second half: "
        "the studio packages the method.",
    )

    # -------------------------------------------------------------- 10. close
    s = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(s, NAVY)
    box(s, 0, 0, 0.15, SLIDE_H, RED)
    logo(s, LOGO_DARK, 0.65, 2.20, 0.50)

    text(
        s, 0.65, 2.86, 8.6, 0.24, ["THE FIRST CONVERSATION"], size=T_CAPTION, color=CYAN, bold=True
    )
    text(
        s,
        0.65,
        3.18,
        8.6,
        0.70,
        ["Start with a gate, not a pilot."],
        size=T_DISPLAY_XL,
        color=WHITE,
        bold=True,
    )
    box(s, 0.65, 4.02, 0.90, 0.04, RED)

    steps = [
        (
            "01",
            "Strategic alignment",
            "Sixty minutes to validate thesis fit and portfolio archetype.",
        ),
        ("02", "Discovery", "Two weeks of problem discovery and a written thesis."),
        ("03", "Go / no-go", "A decision against written criteria, not enthusiasm."),
    ]
    for i, (num, head, body) in enumerate(steps):
        x = 0.65 + i * 2.95
        text(s, x, 4.32, 0.45, 0.24, [num], size=T_CAPTION, color=CYAN, bold=True)
        text(s, x, 4.62, 2.55, 0.28, [head], size=T_TITLE_SM, color=WHITE, bold=True)
        text(
            s, x, 4.98, 2.55, 0.80, [body], size=T_CAPTION, color=GREY_TEXT_DARK, line_spacing=1.18
        )

    text(
        s,
        0.65,
        6.05,
        5.5,
        0.26,
        [[("Chief of Staff, LightSpeed Holdings Limited", {"color": WHITE, "bold": True})]],
        size=T_BODY_SM,
    )
    text(
        s,
        0.65,
        6.33,
        7.9,
        0.24,
        ["Status: internal proof and fieldable governance. No paying-client deployments yet."],
        size=T_CAPTION,
        color=GREY_TEXT_DARK,
    )
    text(s, 0.65, 6.72, 6.0, 0.26, ["ASPIRE. ACT. ACHIEVE."], size=T_SUBTITLE, color=CYAN)
    notes(
        s,
        "The question is whether your next AI decision should be a pilot or an operating model. "
        "If it is an operating model, we begin with alignment, then discovery, then a go/no-go against written "
        "criteria. Aspire is intent, and intent stays human. Act is execution inside gates you can inspect. "
        "Achieve is a number you can defend in a board meeting.",
    )

    prs.core_properties.title = "The LightSpeed Value Proposition - HAOMTGV and the Venture Studio"
    prs.core_properties.author = "LightSpeed Holdings Limited"
    prs.core_properties.subject = (
        "Executive briefing: governed AI-native operating model and venture studio"
    )
    prs.core_properties.comments = (
        "Sources: content/drafts/homepage.md; docs/venture-studio/02,03,04,05; "
        "ai_venture_studio_client_presentation.md; src/components/haomtgv/layers.ts. "
        "Brand: brand/tokens.md."
    )
    prs.core_properties.keywords = "HAOMTGV, Venture Studio, agentic AI, governance, Malawi, SADC"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out_path)
    print(f"Wrote {out_path} ({len(prs.slides._sldIdLst)} slides)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    build(args.out)


if __name__ == "__main__":
    main()
