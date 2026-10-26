"""
LightSpeed Holdings — Pitch Deck Template Generator
Creates an 11-slide investor pitch deck using python-pptx.
Brand: LightSpeed Holdings Limited | Tagline: Aspire. Act. Achieve.
Colors: Navy #070A40, Red #E63946, Cyan #00BFFF, Grey #F2F2F2

Structure (11 slides, down from 13):
    cover - problem - solution - why now - market - product & business model
    - traction - competition - team - the ask - risks

Structural decisions:
  * The agenda slide was removed; it repeated the section list and spent a slide
    of an investor's attention on navigation.
  * Product/architecture and business model were merged: both described the same
    product and neither needed a full slide.
  * Financials were merged into The Ask, which already duplicated "Use of Funds".
  * "Why now" and "Risks" were added: the deck had no urgency argument and no
    statement of what could go wrong.
  * Every figure on these slides traces to a `verified` claim in docs/claims.yaml.
    The CEO's ten decisions are recorded in docs/decisions/2026-10-26-deck-decisions.md;
    figures the repo could not support were retracted rather than estimated, so the
    market totals, the achieved ATC rate and the capital-efficiency multiples do not
    appear here at all.
"""

import io
import os
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_FILL
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))
from scripts.maintenance.company_counts import company_counts  # noqa: E402

COUNTS = company_counts()
AGENT_COUNT = COUNTS["agents"]
DEPARTMENT_COUNT = COUNTS["departments"]

# Brand Colors
NAVY = RGBColor(0x07, 0x0A, 0x40)
RED = RGBColor(0xE6, 0x39, 0x46)
CYAN = RGBColor(0x00, 0xBF, 0xFF)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREY = RGBColor(0xF2, 0xF2, 0xF2)
DARK_GREY = RGBColor(0x6B, 0x72, 0x80)
LIGHT_TEXT = RGBColor(0x9C, 0xA3, 0xAF)

# Canonical logo (brand/** is the single source of truth; legacy static/brand/logos
# suite was archived 2026-10-23 — see brand/CANONICAL_SOURCES.md)
OFFICIAL_LOGO = REPO_ROOT / "brand" / "logo" / "logo-light-bg.png"

DRAFT_NOTICE = "INTERNAL DRAFT — NOT FOR EXTERNAL DISTRIBUTION"
DRAFT_MONTH = "October 2026"


def set_slide_bg(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape(slide, shape_type, left, top, width, height, fill_color=None, line_color=None):
    shape = slide.shapes.add_shape(shape_type, left, top, width, height)
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
    else:
        shape.line.fill.background()
    return shape


def add_text_box(
    slide,
    left,
    top,
    width,
    height,
    text,
    font_size=14,
    bold=False,
    color=NAVY,
    alignment=PP_ALIGN.LEFT,
    font_name="Arial",
):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = alignment
    # Ensure font properties are set on the run explicitly
    for run in p.runs:
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.color.rgb = color
        run.font.name = font_name
    return txBox


def add_bullet_list(slide, left, top, width, height, items, font_size=12, color=NAVY):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = "Arial"
        p.space_after = Pt(6)
        p.level = 0
        # Hanging indents so a wrapped line aligns under its own text instead of
        # falling back to the left margin (which made sub-points read as new bullets).
        body = item.lstrip(" ")
        is_sub = item.startswith("  ")
        if body.startswith("•"):
            p._p.get_or_add_pPr().set("marL", str(int(Inches(0.24))))
            p._p.get_or_add_pPr().set("indent", str(int(-Inches(0.24))))
        elif is_sub:
            p._p.get_or_add_pPr().set("marL", str(int(Inches(0.44))))
            p._p.get_or_add_pPr().set("indent", str(int(-Inches(0.22))))
        # Ensure font properties are set on the run explicitly
        for run in p.runs:
            run.font.size = Pt(font_size)
            run.font.color.rgb = color
            run.font.name = "Arial"
    return txBox


def _slide_bg_rgb(slide):
    """Return the slide's solid background colour, or None when not explicitly set."""
    try:
        fill = slide.background.fill
        if fill.type is not None and fill.type == MSO_FILL.SOLID:
            return fill.fore_color.rgb
    except (AttributeError, ValueError, TypeError):
        return None
    return None


def mark_internal_draft(prs):
    """Stamp every slide as an internal draft and record that in document metadata.

    Generated here rather than hand-added so the marking survives regeneration and
    cannot be forgotten. The figures now trace to verified claims, but the deck has no
    independent QA verdict yet, so it must never be mistaken for an investor-ready
    document: verify-deck.py exits 2 until a bound APPROVE verdict exists.
    """
    for slide in prs.slides:
        bg = _slide_bg_rgb(slide)
        on_dark = bg is not None and bg != WHITE
        add_text_box(
            slide,
            Inches(0.5),
            Inches(7.12),
            Inches(9.0),
            Inches(0.3),
            DRAFT_NOTICE,
            font_size=12,
            bold=True,
            color=CYAN if on_dark else NAVY,
            alignment=PP_ALIGN.RIGHT,
        )

    props = prs.core_properties
    props.title = "LightSpeed Holdings — INTERNAL DRAFT pitch deck"
    props.subject = "Internal draft. Not for external distribution."
    props.category = "Internal draft"
    props.keywords = "internal draft; not for external distribution; pending QA verdict"
    props.comments = (
        "DRAFT ONLY. Figures trace to verified claims in docs/claims.yaml, but no "
        "independent QA verdict is bound to this build. Do not send to investors until "
        "verify-deck.py exits 0 with an APPROVE QA verdict."
    )


def _section_rail(slide):
    """Full-height navy rail on the left edge, used by every light content slide."""
    add_shape(
        slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY
    )


def _slide_title(slide, text):
    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(9),
        Inches(0.7),
        text,
        font_size=28,
        bold=True,
        color=NAVY,
    )


def _card_row(slide, cards, top, height=1.85, left=0.8, width=2.75, gap=0.2):
    """Three side-by-side cards. Used where a bullet list alone would leave the lower
    half of a slide empty."""
    for i, (heading, body) in enumerate(cards):
        x = Inches(left + i * (width + gap))
        add_shape(
            slide,
            MSO_SHAPE.ROUNDED_RECTANGLE,
            x,
            Inches(top),
            Inches(width),
            Inches(height),
            fill_color=GREY,
        )
        add_text_box(
            slide,
            x + Inches(0.2),
            Inches(top + 0.15),
            Inches(width - 0.4),
            Inches(0.35),
            heading,
            font_size=14,
            bold=True,
            color=NAVY,
        )
        add_text_box(
            slide,
            x + Inches(0.2),
            Inches(top + 0.5),
            Inches(width - 0.4),
            Inches(height - 0.6),
            body,
            font_size=12,
            color=NAVY,
        )


def _summary_band(slide, top, text, height=1.05, font_size=12):
    """Full-width closing note. Used where a two-column slide would otherwise trail
    off into empty space at the bottom."""
    add_shape(
        slide,
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.55),
        Inches(top),
        Inches(8.9),
        Inches(height),
        fill_color=GREY,
    )
    add_text_box(
        slide,
        Inches(0.8),
        Inches(top + 0.18),
        Inches(8.4),
        Inches(height - 0.3),
        text,
        font_size=font_size,
        bold=False,
        color=NAVY,
    )


# --------------------------------------------------------------------------- 1
def create_title_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    set_slide_bg(slide, NAVY)

    # White panel matching the square logo canvas (brand/logo/logo-light-bg.png is
    # the guideline-mandated variant for dark/navy backgrounds; it carries a white canvas)
    logo_panel = add_shape(
        slide,
        MSO_SHAPE.RECTANGLE,
        Inches(0.6),
        Inches(0.4),
        Inches(1.9),
        Inches(1.9),
        fill_color=WHITE,
    )
    logo_panel.line.fill.background()

    # Canonical logo (brand/logo is the single source of truth since 2026-10-23)
    logo_bytes = io.BytesIO(OFFICIAL_LOGO.read_bytes())
    logo = slide.shapes.add_picture(
        logo_bytes, Inches(0.6), Inches(0.4), width=Inches(1.9), height=Inches(1.9)
    )
    logo._element.xpath("./p:nvPicPr/p:cNvPr")[0].set("name", "Company Logo")
    logo._element.xpath("./p:nvPicPr/p:cNvPr")[0].set("descr", "LightSpeed Holdings logo")

    # Company name — 34pt in a 9.2in box keeps it on one line
    add_text_box(
        slide,
        Inches(0.4),
        Inches(2.7),
        Inches(9.2),
        Inches(0.8),
        "LIGHTSPEED HOLDINGS LIMITED™",
        font_size=36,
        bold=True,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
    )

    # Tagline
    add_text_box(
        slide,
        Inches(1),
        Inches(3.6),
        Inches(8),
        Inches(0.5),
        "ASPIRE. ACT. ACHIEVE.",
        font_size=18,
        bold=True,
        color=CYAN,
        alignment=PP_ALIGN.CENTER,
    )

    # Accent line
    add_shape(
        slide,
        MSO_SHAPE.RECTANGLE,
        Inches(3.5),
        Inches(4.3),
        Inches(3),
        Inches(0.04),
        fill_color=RED,
    )

    # Draft notice in place of the old, stale "Confidential — August 2026" line
    add_text_box(
        slide,
        Inches(1),
        Inches(4.62),
        Inches(8),
        Inches(0.3),
        "INTERNAL DRAFT — {month}".format(month=DRAFT_MONTH),
        font_size=12,
        bold=True,
        color=LIGHT_TEXT,
        alignment=PP_ALIGN.CENTER,
    )


# --------------------------------------------------------------------------- 2
def create_problem_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    _section_rail(slide)
    _slide_title(slide, "THE PROBLEM")

    problems = [
        "•  Deploying AI agents at scale means custom integration, monitoring and governance for every one",
        "•  Existing tools are either too simple (chatbots) or too complex (enterprise ML platforms)",
        "•  No turnkey way exists to stand up an entire AI-powered organization",
        "•  Cost tracking, human oversight and multi-provider management are afterthoughts",
        "•  Governance arrives late, if at all: approvals, audit trails and escalation rules live outside the tooling",
    ]
    add_bullet_list(
        slide,
        Inches(0.8),
        Inches(1.35),
        Inches(8.5),
        Inches(3.6),
        problems,
        font_size=14,
        color=NAVY,
    )

    # Pain point callout
    add_shape(
        slide,
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(1),
        Inches(5.15),
        Inches(8),
        Inches(1.15),
        fill_color=GREY,
    )
    add_text_box(
        slide,
        Inches(1.3),
        Inches(5.35),
        Inches(7.4),
        Inches(0.8),
        '"Building an AI-native company shouldn\'t require a team of ML engineers."',
        font_size=14,
        bold=True,
        color=NAVY,
        alignment=PP_ALIGN.CENTER,
    )


# --------------------------------------------------------------------------- 3
def create_solution_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    _section_rail(slide)
    _slide_title(slide, "OUR SOLUTION")

    add_text_box(
        slide,
        Inches(0.8),
        Inches(1.2),
        Inches(8.5),
        Inches(0.75),
        "AI Company Builder — a CLI platform that generates, orchestrates and manages "
        "complete AI agent organizations.",
        font_size=16,
        bold=False,
        color=NAVY,
    )

    features = [
        "✓  Registry-driven: define agents in YAML, generate OpenCode-compatible markdown",
        "✓  Multi-provider LLM routing — OpenAI, Anthropic, DeepSeek, Gemini — with fallback",
        "✓  Per-agent cost tracking and budget enforcement",
        "✓  Human-in-the-loop approval gates for irreversible actions",
        "✓  MessageBus task queue for cross-agent coordination",
        "✓  Pre-built agent roles across every department",
    ]
    add_bullet_list(
        slide,
        Inches(0.8),
        Inches(2.2),
        Inches(8.5),
        Inches(2.0),
        features,
        font_size=13,
        color=NAVY,
    )

    # How it works in practice: define -> generate -> run. Three boxes use the lower
    # half of the slide instead of leaving it blank.
    steps = [
        (
            "1.  Define",
            "One YAML registry lists every role, tool and permission the organization is "
            "allowed to use.",
        ),
        (
            "2.  Generate",
            "The CLI renders agent cards, permissions and prompts, so the organization is "
            "version-controlled like code.",
        ),
        (
            "3.  Run",
            "Work moves through a task queue under approval gates, with per-agent budgets "
            "and a full audit trail.",
        ),
    ]
    _card_row(slide, steps, 4.45)


# --------------------------------------------------------------------------- 4
def create_why_now_slide(prs):
    """New slide. The deck previously jumped from solution to market size with no
    argument for why this is worth doing now rather than in three years."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    _section_rail(slide)
    _slide_title(slide, "WHY NOW")

    add_text_box(
        slide,
        Inches(0.8),
        Inches(1.15),
        Inches(8.5),
        Inches(0.55),
        "Three shifts make an AI-native organization buildable today but not two years ago:",
        font_size=14,
        bold=False,
        color=NAVY,
    )

    reasons = [
        (
            "Capability",
            "Long-horizon tool use is now reliable enough to run multi-step work, not just "
            "answer questions.",
        ),
        (
            "Cost",
            "Inference has fallen far enough that per-agent budgets are a control problem, "
            "not a blocker.",
        ),
        (
            "Expectation",
            "Clients now ask how AI changes how they operate, not whether it will.",
        ),
    ]
    _card_row(slide, reasons, 1.95, height=2.0)

    _summary_band(
        slide,
        4.5,
        "Why us: we run this ourselves. The company operates on the same registry, "
        "governance gates and cost controls we sell — built for low-bandwidth, "
        "offline-capable deployment in Malawi and the wider SADC region.",
        height=1.4,
    )


# --------------------------------------------------------------------------- 5
def create_market_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    _section_rail(slide)
    _slide_title(slide, "MARKET OPPORTUNITY")

    add_text_box(
        slide,
        Inches(0.8),
        Inches(1.15),
        Inches(8.5),
        Inches(0.7),
        "Bottom-up sizing from our own rate card. TAM and SAM are shown as open "
        "questions: we will not print a market total we cannot cite to a report.",
        font_size=14,
        bold=False,
        color=NAVY,
    )

    # D-08: only the capacity-derived SOM is published. TAM ($65B) and SAM ($12B) were
    # retracted — no source for either exists in the repo.
    sizing = [
        "TAM / SAM:  Pending a cited report — not guessed",
        "SOM:  $44-85K — paid delivery we can staff in the next four quarters",
    ]
    add_bullet_list(
        slide, Inches(0.8), Inches(2.05), Inches(8.5), Inches(1.5), sizing, font_size=14, color=NAVY
    )

    add_text_box(
        slide,
        Inches(0.8),
        Inches(3.4),
        Inches(8.5),
        Inches(0.4),
        "TARGET SEGMENTS",
        font_size=14,
        bold=True,
        color=RED,
    )
    segments = [
        "•  Enterprises deploying internal AI agent fleets",
        "•  SMBs automating operations",
        "•  AI consultancies building client agent systems",
        "•  NGOs and development programs needing offline-capable tooling",
    ]
    add_bullet_list(
        slide,
        Inches(0.8),
        Inches(3.85),
        Inches(8.5),
        Inches(1.9),
        segments,
        font_size=13,
        color=NAVY,
    )

    _summary_band(
        slide,
        5.4,
        "We do not need the whole market. Paid delivery work from clients reachable from "
        "Lilongwe funds the platform, and the platform is what makes that delivery "
        "repeatable rather than bespoke.",
    )


# --------------------------------------------------------------------------- 6
def create_product_model_slide(prs):
    """Merged from the former separate Product and Business Model slides."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    _section_rail(slide)
    _slide_title(slide, "PRODUCT & BUSINESS MODEL")

    # Left column — what it does
    add_text_box(
        slide,
        Inches(0.55),
        Inches(1.15),
        Inches(4.3),
        Inches(0.4),
        "What it does",
        font_size=16,
        bold=True,
        color=NAVY,
    )
    tech_items = [
        "Python CLI — no web server required",
        "Registry YAML → template → agent files",
        "ReAct loop with tool routing",
        "AgentLoop, CostTracker, HITLGate",
        "MessageBus task queue",
        "ModelRouter with provider fallback",
        "Least-privilege agent permissions",
        "Bandit static analysis, pre-commit hooks",
    ]
    add_bullet_list(
        slide,
        Inches(0.55),
        Inches(1.65),
        Inches(4.35),
        Inches(4.6),
        tech_items,
        font_size=12,
        color=NAVY,
    )

    # Right column — how it earns
    add_text_box(
        slide,
        Inches(5.2),
        Inches(1.15),
        Inches(4.3),
        Inches(0.4),
        "How it earns",
        font_size=16,
        bold=True,
        color=NAVY,
    )
    model_items = [
        "Platform licence — $2,000 setup + $200/mo support",
        "Firm licence — $15K/yr + $250/mo for consulting firms",
        "Delivery — implementation engagements, priced per engagement",
        "",
        "Unit economics targets:",
        "  •  Gross margin — 70%+ platform, 55-60% services",
        "  •  LLM and infrastructure — ≤10% of revenue",
        "  •  CAC payback — pending CFO model",
    ]
    add_bullet_list(
        slide,
        Inches(5.2),
        Inches(1.65),
        Inches(4.35),
        Inches(4.6),
        model_items,
        font_size=12,
        color=NAVY,
    )

    _summary_band(
        slide,
        4.75,
        "Two licences and one service: a platform licence the client runs itself, a firm "
        "licence for agencies serving their own clients, and implementation work scoped per "
        f"engagement. The same system runs this company — {DEPARTMENT_COUNT}\u00a0departments, "
        f"{AGENT_COUNT - 1}\u00a0AI\u00a0agents, one Human CEO.",
    )


# --------------------------------------------------------------------------- 7
def create_traction_slide(prs):
    """No KPI cards. The former slide showed four grey boxes whose value slot held
    a word ("Agents / Deployed"), which read as a broken template. There is no
    external traction to quantify yet, so this states what exists and what does not."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    _section_rail(slide)
    _slide_title(slide, "TRACTION & STATUS")

    add_text_box(
        slide,
        Inches(0.55),
        Inches(1.15),
        Inches(4.3),
        Inches(0.4),
        "Built and working",
        font_size=16,
        bold=True,
        color=NAVY,
    )
    built = [
        "•  Platform built, running this company internally",
        "•  Multi-provider routing with cost enforcement",
        "•  Human approval gates enforced in code",
        "•  Audit trail and test suite in place",
        "•  Corporate Blueprint adopted",
    ]
    add_bullet_list(
        slide, Inches(0.55), Inches(1.65), Inches(4.3), Inches(3.2), built, font_size=12, color=NAVY
    )

    add_text_box(
        slide,
        Inches(5.2),
        Inches(1.15),
        Inches(4.3),
        Inches(0.4),
        "Not yet",
        font_size=16,
        bold=True,
        color=RED,
    )
    not_yet = [
        "•  No paying clients",
        "•  No signed pilots",
        "•  No revenue",
        "•  No external validation of the model",
    ]
    add_bullet_list(
        slide,
        Inches(5.2),
        Inches(1.65),
        Inches(4.3),
        Inches(2.4),
        not_yet,
        font_size=12,
        color=NAVY,
    )

    _summary_band(
        slide,
        4.6,
        "This raise funds the first paid pilots. Progress is measured by signed pilots, "
        "not by features shipped — so the next version of this slide should be a list of "
        "clients, not a list of capabilities.",
    )


# --------------------------------------------------------------------------- 8
def create_competition_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    _section_rail(slide)
    _slide_title(slide, "COMPETITIVE LANDSCAPE")

    add_text_box(
        slide,
        Inches(0.55),
        Inches(1.15),
        Inches(4.3),
        Inches(0.4),
        "Who else is in the space",
        font_size=16,
        bold=True,
        color=NAVY,
    )
    competitors = [
        "Agent frameworks (LangGraph, CrewAI) — developer tools, no organization layer or governance",
        "Workflow automation (n8n, Zapier) — task pipelines, not agent organizations",
        "Assistant SaaS (ChatGPT Business, Copilot) — single assistant, no role hierarchy or cost control",
        "Custom builds — high engineering cost, no reusable control plane",
    ]
    add_bullet_list(
        slide,
        Inches(0.55),
        Inches(1.65),
        Inches(4.35),
        Inches(4.4),
        competitors,
        font_size=12,
        color=NAVY,
    )

    add_text_box(
        slide,
        Inches(5.2),
        Inches(1.15),
        Inches(4.3),
        Inches(0.4),
        "What we do differently",
        font_size=16,
        bold=True,
        color=RED,
    )
    differentiation = [
        "✓  Organization structure, not a single agent",
        "✓  Cost transparency and budget enforcement built in",
        "✓  Human approval gates as a first-class feature",
        "✓  Multi-provider, with automatic fallback",
        "✓  Local-first inference for low-connectivity settings",
        "✓  Governance and escalation rules shipped as code",
    ]
    add_bullet_list(
        slide,
        Inches(5.2),
        Inches(1.65),
        Inches(4.35),
        Inches(4.4),
        differentiation,
        font_size=12,
        color=NAVY,
    )

    _summary_band(
        slide,
        4.85,
        "We are not competing on model access — the models are commodities and anyone can "
        "call them. We compete on the control plane around them: who may act, what it "
        "costs, and who signs off.",
    )


# --------------------------------------------------------------------------- 9
def create_team_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    _section_rail(slide)
    _slide_title(slide, "TEAM")

    add_text_box(
        slide,
        Inches(0.55),
        Inches(1.15),
        Inches(4.3),
        Inches(0.4),
        "Leadership",
        font_size=16,
        bold=True,
        color=NAVY,
    )
    # D-09: the founder only. The agent cabinet is a product feature (see the product
    # slide), not a leadership team, and no advisor or director has consented to be
    # named. Presenting registry entries as a board overstates governance.
    team = [
        "Jack Mlusu — Founder & CEO",
        "  Builder-operator; runs the company on the platform it sells",
        "",
        "The org chart is generated, not hired.",
        "  Twenty departments exist as registry entries, staffed by agents under human "
        "approval gates — shown on the product slide, not claimed as a leadership team.",
        "",
        "No advisor, contractor or director is named without their written consent.",
    ]
    add_bullet_list(
        slide, Inches(0.55), Inches(1.65), Inches(4.35), Inches(4.4), team, font_size=12, color=NAVY
    )

    add_text_box(
        slide,
        Inches(5.2),
        Inches(1.15),
        Inches(4.3),
        Inches(0.4),
        "Hiring with this raise",
        font_size=16,
        bold=True,
        color=RED,
    )
    hiring = [
        "•  Platform Licensing Sales Lead — priority one",
        "•  Delivery Lead for chatbot and compliance offers",
        "•  Compliance Officer",
        "•  Developer Relations Engineer",
        "",
        "Human hires, not agent seats: clients buy from people.",
    ]
    add_bullet_list(
        slide,
        Inches(5.2),
        Inches(1.65),
        Inches(4.35),
        Inches(4.0),
        hiring,
        font_size=12,
        color=NAVY,
    )

    _summary_band(
        slide,
        5.15,
        "The operating model already exists: a five-tier approval matrix, named escalation "
        "routes and an audit trail, applied to agents as well as people. The hiring plan "
        "adds the human roles that sell and deliver.",
    )


# -------------------------------------------------------------------------- 10
def create_ask_slide(prs):
    """Financials and The Ask merged — both previously listed the same Use of Funds."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)
    _section_rail(slide)

    add_text_box(
        slide,
        Inches(1),
        Inches(0.55),
        Inches(8),
        Inches(0.7),
        "THE ASK",
        font_size=32,
        bold=True,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
    )
    add_shape(
        slide,
        MSO_SHAPE.RECTANGLE,
        Inches(3.5),
        Inches(1.35),
        Inches(3),
        Inches(0.04),
        fill_color=RED,
    )

    add_text_box(
        slide,
        Inches(1),
        Inches(1.5),
        Inches(8),
        Inches(0.8),
        "$650K",
        font_size=36,
        bold=True,
        color=CYAN,
        alignment=PP_ALIGN.CENTER,
    )

    # D-05: the amount is decided; the instrument and the runway are not. The deck
    # states the gap instead of implying equity, a SAFE, or a runway length.
    add_text_box(
        slide,
        Inches(1),
        Inches(2.3),
        Inches(8),
        Inches(0.4),
        "Seed round — instrument and runway not yet set.",
        font_size=12,
        bold=True,
        color=LIGHT_TEXT,
        alignment=PP_ALIGN.CENTER,
    )

    add_text_box(
        slide,
        Inches(1.0),
        Inches(2.85),
        Inches(3.8),
        Inches(0.4),
        "Use of funds",
        font_size=14,
        bold=True,
        color=WHITE,
    )
    use_of_funds = [
        "Talent — sales, delivery, compliance, DevRel",
        "Client pilots — Offers A, B and C",
        "Hardware lab — on-prem GPU, field kits",
        "Compliance — DPA 2024 alignment, GDPR opinion, SOC 2 prep",
        "Emergency reserve",
    ]
    add_bullet_list(
        slide,
        Inches(1.0),
        Inches(3.3),
        Inches(3.9),
        Inches(3.2),
        use_of_funds,
        font_size=12,
        color=WHITE,
    )

    add_text_box(
        slide,
        Inches(5.3),
        Inches(2.85),
        Inches(3.8),
        Inches(0.4),
        "Milestones this buys",
        font_size=14,
        bold=True,
        color=WHITE,
    )
    milestones = [
        "Signed paying pilots across Offers A–C",
        "Recurring revenue run-rate established",
        "Governance gates live with tamper-evident audit trail",
        "Repeatable delivery playbook per offer",
    ]
    add_bullet_list(
        slide,
        Inches(5.3),
        Inches(3.3),
        Inches(3.9),
        Inches(3.2),
        milestones,
        font_size=12,
        color=WHITE,
    )

    # D-02: the revenue band is a target, and $120K is an exit ARR run-rate — it must
    # never be read as recognised revenue.
    add_text_box(
        slide,
        Inches(1),
        Inches(5.0),
        Inches(8),
        Inches(0.45),
        "Year-one target: $50-85K gross revenue. Exit ARR run-rate: $120K — not revenue.",
        font_size=12,
        bold=True,
        color=CYAN,
        alignment=PP_ALIGN.CENTER,
    )

    add_shape(
        slide,
        MSO_SHAPE.RECTANGLE,
        Inches(2.5),
        Inches(5.6),
        Inches(5),
        Inches(0.03),
        fill_color=CYAN,
    )
    add_text_box(
        slide,
        Inches(1),
        Inches(5.75),
        Inches(8),
        Inches(0.9),
        "We are asking for $650K to fund paying pilots across Offers A, B and C, and to "
        "make the four hires above.",
        font_size=14,
        bold=True,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
    )


# -------------------------------------------------------------------------- 11
def create_risks_slide(prs):
    """New slide. A deck that lists no risks reads as either naive or evasive."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    _section_rail(slide)
    _slide_title(slide, "RISKS & HOW WE MITIGATE THEM")

    risks = [
        (
            "Dependence on third-party models",
            "Multi-provider routing with automatic fallback; local inference option",
        ),
        (
            "Regulatory and data-protection exposure",
            "Built to DPA 2024 and GDPR-grade handling; SOC 2 planned, not certified",
        ),
        (
            "Single-founder execution risk",
            "Named hiring plan; agent cabinet under human approval gates",
        ),
        (
            "Selling ahead of proof",
            "Pilots capped in scope and budget; no scale claims before delivery",
        ),
        (
            "Cost overrun on inference",
            "Per-agent budgets and cost enforcement, not after-the-fact reporting",
        ),
        ("Concentration in one market", "SADC-first, with offers designed for remote delivery"),
    ]
    y = 1.3
    for risk, mitigation in risks:
        add_shape(
            slide,
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.55),
            Inches(y),
            Inches(8.9),
            Inches(0.78),
            fill_color=GREY,
        )
        add_text_box(
            slide,
            Inches(0.75),
            Inches(y + 0.08),
            Inches(3.3),
            Inches(0.6),
            risk,
            font_size=12,
            bold=True,
            color=NAVY,
        )
        add_text_box(
            slide,
            Inches(4.15),
            Inches(y + 0.08),
            Inches(5.1),
            Inches(0.6),
            mitigation,
            font_size=12,
            color=NAVY,
        )
        y += 0.9


def main():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # Set theme fonts to Arial to avoid inherited Calibri
    try:
        theme = prs.slide_master.part.part_related_by(
            "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme"
        )
        if theme:
            theme_xml = theme.blob
            from lxml import etree

            root = etree.fromstring(theme_xml)
            ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
            # Set major (heading) font to Arial
            major_latin = root.find(".//a:fontScheme/a:majorFont/a:latin", ns)
            if major_latin is not None:
                major_latin.set("typeface", "Arial")
            # Set minor (body) font to Arial
            minor_latin = root.find(".//a:fontScheme/a:minorFont/a:latin", ns)
            if minor_latin is not None:
                minor_latin.set("typeface", "Arial")
            # Write back
            theme.blob = etree.tostring(root)
    except OSError:
        pass  # Best effort; verify-deck.py will catch if not working

    # Build deck — 11 slides
    create_title_slide(prs)  # 1
    create_problem_slide(prs)  # 2
    create_solution_slide(prs)  # 3
    create_why_now_slide(prs)  # 4  (new)
    create_market_slide(prs)  # 5
    create_product_model_slide(prs)  # 6  (merged from two slides)
    create_traction_slide(prs)  # 7
    create_competition_slide(prs)  # 8
    create_team_slide(prs)  # 9
    create_ask_slide(prs)  # 10 (financials merged in)
    create_risks_slide(prs)  # 11 (new)

    # Every slide must carry the draft notice; see module constants.
    mark_internal_draft(prs)

    # Save
    output_path = os.path.join(os.path.dirname(__file__), "..", "templates", "pitch-deck.pptx")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Pitch deck saved to: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    main()
