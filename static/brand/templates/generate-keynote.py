"""
LightSpeed Holdings — Keynote Template Generator

Creates a 13-slide executive keynote deck using python-pptx.
Brand: LightSpeed Holdings Limited | Colors: Navy #070A40, Red #E63946, Cyan #00BFFF, Grey #F2F2F2
"""

import os
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

# Brand Colors (80/10/10 rule)
NAVY = RGBColor(0x07, 0x0A, 0x40)   # 80% — primary, left rail, main text
RED = RGBColor(0xE6, 0x39, 0x46)    # 10% — highlights, key decisions, calls to action
CYAN = RGBColor(0x00, 0xBF, 0xFF)   # 10% — secondary highlights, tech emphasis
WHITE = RGBColor(0xFF, 0xFF, 0xFF)  # Content backgrounds
GREY = RGBColor(0xF2, 0xF2, 0xF2)   # Non-brand backgrounds, KPI boxes
DARK_GREY = RGBColor(0x6B, 0x72, 0x80)  # Secondary text


def set_slide_bg(slide, color):
    """Set solid background color on a slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape(slide, shape_type, left, top, width, height, fill_color=None, line_color=None):
    """Add a shaped rectangle to a slide with optional fill/line colors."""
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
    """Add a text box with formatted paragraph."""
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
    return txBox


def add_bullet_list(slide, left, top, width, height, items, font_size=12, color=NAVY):
    """Add a bullet list to a slide text box."""
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
    return txBox


def add_navy_rail(slide):
    """Add the standard navy left rail (1/4 width) to a content slide."""
    add_shape(
        slide,
        MSO_SHAPE.RECTANGLE,
        Inches(0),
        Inches(0),
        Inches(3.333),
        Inches(7.5),
        fill_color=NAVY,
    )


def add_title_bar(slide, title, subtitle=None):
    """Add navy title bar with title and optional subtitle."""
    add_shape(
        slide,
        MSO_SHAPE.RECTANGLE,
        Inches(0),
        Inches(0),
        Inches(13.333),
        Inches(0.7),
        fill_color=NAVY,
    )
    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.1),
        Inches(12),
        Inches(0.5),
        title,
        font_size=28,
        bold=True,
        color=WHITE,
        alignment=PP_ALIGN.LEFT,
    )
    if subtitle:
        add_text_box(
            slide,
            Inches(0.5),
            Inches(0.5),
            Inches(12),
            Inches(0.4),
            subtitle,
            font_size=14,
            color=RGBColor(0xAA, 0xBB, 0xCC),
            alignment=PP_ALIGN.LEFT,
        )


def create_opening_slide(prs):
    """Slide 1: Opening & Vision — why this moment matters now."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    set_slide_bg(slide, NAVY)

    add_text_box(
        slide,
        Inches(1),
        Inches(1.5),
        Inches(11),
        Inches(1.0),
        "Opening & Vision",
        font_size=44,
        bold=True,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
    )
    add_text_box(
        slide,
        Inches(1),
        Inches(2.8),
        Inches(11),
        Inches(0.8),
        "Why this moment matters now",
        font_size=24,
        color=CYAN,
        alignment=PP_ALIGN.CENTER,
    )
    # Navy accent line
    add_shape(
        slide,
        MSO_SHAPE.RECTANGLE,
        Inches(4.5),
        Inches(3.8),
        Inches(4.333),
        Inches(0.04),
        fill_color=RED,
    )


def create_market_opportunity_slide(prs):
    """Slide 2: Market Opportunity — size and growth trajectory."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(12),
        Inches(0.6),
        "Market Opportunity",
        font_size=32,
        bold=True,
        color=NAVY,
    )
    add_text_box(
        slide,
        Inches(0.5),
        Inches(1.2),
        Inches(12),
        Inches(0.5),
        "Size and growth trajectory",
        font_size=16,
        color=RGBColor(0x66, 0x66, 0x66),
    )

    add_text_box(
        slide,
        Inches(0.8),
        Inches(2.0),
        Inches(8.5),
        Inches(1.5),
        "TAM: $65B — Enterprise AI agent platforms & orchestration by 2028",
        font_size=14,
        bold=False,
        color=NAVY,
    )
    add_text_box(
        slide,
        Inches(0.8),
        Inches(2.8),
        Inches(8.5),
        Inches(1.0),
        "SAM: $12B — Mid-market companies deploying AI agents",
        font_size=13,
        color=NAVY,
    )
    add_text_box(
        slide,
        Inches(0.8),
        Inches(3.4),
        Inches(8.5),
        Inches(1.0),
        "SOM: $120M — Developer-led, self-serve AI company builder",
        font_size=13,
        color=NAVY,
    )

    # Red highlight for key stat
    add_text_box(
        slide,
        Inches(0.8),
        Inches(4.5),
        Inches(8.5),
        Inches(0.6),
        ">>> 65% of enterprises will deploy AI agents by 2027 (IDC)",
        font_size=14,
        bold=True,
        color=RED,
    )


def create_our_solution_slide(prs):
    """Slide 3: Our Solution — unique approach and value proposition."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(12),
        Inches(0.6),
        "Our Solution",
        font_size=32,
        bold=True,
        color=NAVY,
    )
    add_text_box(
        slide,
        Inches(0.5),
        Inches(1.2),
        Inches(12),
        Inches(0.5),
        "Unique approach and value proposition",
        font_size=16,
        color=RGBColor(0x66, 0x66, 0x66),
    )

    add_text_box(
        slide,
        Inches(0.8),
        Inches(2.0),
        Inches(8.5),
        Inches(1.0),
        "AI Company Builder — CLI platform that generates, orchestrates, and manages",
        font_size=14,
        color=NAVY,
    )
    add_text_box(
        slide,
        Inches(0.8),
        Inches(2.6),
        Inches(8.5),
        Inches(1.0),
        "complete AI agent organizations from a single YAML registry",
        font_size=14,
        color=NAVY,
    )

    features = [
        "✓  Registry-driven: Define agents in YAML, generate OpenCode markdown files",
        "✓  Multi-provider LLM routing with automatic fallback chain",
        "✓  Built-in cost tracking & budget enforcement per agent",
        "✓  Human-in-the-loop approval gates for irreversible operations",
        "✓  MessageBus task queue for cross-agent coordination",
        "✓  Local-first option (Ollama) for zero-cost inference",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(3.5), Inches(8.5), Inches(3), features, font_size=13, color=NAVY)

    # Cyan accent for key differentiator
    add_text_box(
        slide,
        Inches(0.8),
        Inches(6.2),
        Inches(8.5),
        Inches(0.6),
        "Differentiation: end-to-end organization generation, not just a tool",
        font_size=13,
        bold=True,
        color=CYAN,
    )


def create_customer_success_slide(prs):
    """Slide 4: Customer Success Stories — real-world results and case studies."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(12),
        Inches(0.6),
        "Customer Success Stories",
        font_size=32,
        bold=True,
        color=NAVY,
    )
    add_text_box(
        slide,
        Inches(0.5),
        Inches(1.2),
        Inches(12),
        Inches(0.5),
        "Real-world results and case studies",
        font_size=16,
        color=RGBColor(0x66, 0x66, 0x66),
    )

    cases = [
        "•  NGO pilot: 3× Offer A deployment, 40% operational cost reduction",
        "•  SMB SaaS: 1× Offer B integration, 25% faster onboarding",
        "•  Enterprise: 1× Offer C fleet management, 70% automation rate",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(2.3), Inches(8.5), Inches(3), cases, font_size=13, color=NAVY)

    # Red callout for impact
    add_shape(
        slide,
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.8),
        Inches(5.0),
        Inches(8.5),
        Inches(1.5),
        fill_color=GREY,
    )
    add_text_box(
        slide,
        Inches(1.1),
        Inches(5.1),
        Inches(8.0),
        Inches(1.3),
        '"Building an AI-native company shouldn\'t require a team of ML engineers."',
        font_size=14,
        bold=True,
        color=NAVY,
        alignment=PP_ALIGN.CENTER,
    )


def create_competitive_differentiation_slide(prs):
    """Slide 5: Competitive Differentiation — differentiators in the market."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(12),
        Inches(0.6),
        "Competitive Differentiation",
        font_size=32,
        bold=True,
        color=NAVY,
    )
    add_text_box(
        slide,
        Inches(0.5),
        Inches(1.2),
        Inches(12),
        Inches(0.5),
        "Our differentiators in the market",
        font_size=16,
        color=RGBColor(0x66, 0x66, 0x66),
    )

    competitors = [
        "Direct: Agent frameworks (LangGraph, CrewAI) — dev tools, no org layer or governance",
        "Workflow automation (n8n, Zapier) — task pipelines, not multi-agent organizations",
        "Single-assistant SaaS (ChatGPT Business, Copilot) — no role hierarchy or cost control",
        "",
        "Indirect: Custom-built agent frameworks (high engineering cost)",
        "Enterprise ML platforms (overkill for most orgs)",
        "ChatGPT/Claude for single tasks (no orchestration)",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(2.2), Inches(8.5), Inches(4), competitors, font_size=12, color=NAVY)

    # Cyan for our differentiation
    differentiation = [
        "Our Differentiation:",
        "  ✓  AI-native company structure (not just a tool)",
        "  ✓  Built-in cost transparency & budget enforcement",
        "  ✓  Human-in-the-loop safety gates",
        "  ✓  Multi-provider with automatic fallback",
        "  ✓  Local-first option (Ollama) for zero-cost inference",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(5.5), Inches(8.5), Inches(2), differentiation, font_size=12, color=CYAN)


def create_technology_innovation_slide(prs):
    """Slide 6: Technology & Innovation — competitive advantage and IP."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(12),
        Inches(0.6),
        "Technology & Innovation",
        font_size=32,
        bold=True,
        color=NAVY,
    )
    add_text_box(
        slide,
        Inches(0.5),
        Inches(1.2),
        Inches(12),
        Inches(0.5),
        "Competitive advantage and IP",
        font_size=16,
        color=RGBColor(0x66, 0x66, 0x66),
    )

    tech_items = [
        "Architecture:",
        "  •  Python 3.12+ CLI (Typer) — no web server required",
        "  •  Registry YAML → Jinja2 template → OpenCode agent files",
        "  •  ReAct agentic loop with tool routing and cost tracking",
        "",
        "Core Components:",
        "  •  AgentLoop — Multi-turn reasoning with tool execution and governance",
        "  •  CostTracker — Real-time LLM spend monitoring with 80/10/10 rule enforcement",
        "  •  HITLGate — Human approval for irreversible actions",
        "  •  MessageBus — JSON task queue for agent coordination",
        "  •  ModelRouter — Provider fallback chain (OpenAI → Anthropic → DeepSeek → Gemini)",
        "",
        "Security:",
        "  •  Bandit static analysis, pre-commit hooks (ruff, mypy, bandit clean)",
        "  •  Principle-of-least-privilege agent permissions",
        "  •  Encrypted credential storage",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.8), Inches(8.5), Inches(5), tech_items, font_size=12, color=NAVY)

    # Cyan for core component
    add_text_box(
        slide,
        Inches(0.8),
        Inches(6.5),
        Inches(8.5),
        Inches(0.5),
        "ModelRouter: automatic provider fallback",
        font_size=13,
        bold=True,
        color=CYAN,
    )


def create_roadmap_slide(prs):
    """Slide 7: Roadmap & Milestones — key milestones over coming quarters."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(12),
        Inches(0.6),
        "Roadmap & Milestones",
        font_size=32,
        bold=True,
        color=NAVY,
    )
    add_text_box(
        slide,
        Inches(0.5),
        Inches(1.2),
        Inches(12),
        Inches(0.5),
        "Key milestones over coming quarters",
        font_size=16,
        color=RGBColor(0x66, 0x66, 0x66),
    )

    milestones = [
        "•  Q4 2026 — Platform bootstrapped; Phase 1–2 core architecture shipped",
        "•  Q1 2027 — 5 flagship offers priced & governance gates ratified",
        "•  Q1 2027 — Corporate Blueprint adopted; $500K capital guidance signed",
        "•  Q2 2027 — 2,000+ automated tests; ruff, mypy & bandit clean",
        "•  Q2 2027 — Multi-region deployment; local-first (Ollama) support",
        "•  Q3 2027 — Autonomous mode live — self-governing AI company",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(2.3), Inches(8.5), Inches(3.5), milestones, font_size=13, color=NAVY)

    # Grey for roadmap planning
    add_text_box(
        slide,
        Inches(0.8),
        Inches(5.8),
        Inches(8.5),
        Inches(0.5),
        "80/10/10 rule enforced across all visual elements",
        font_size=12,
        color=GREY,
    )


def create_key_decisions_slide(prs):
    """Slide 8: Key Decisions Required — decisions needed from leadership today."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(12),
        Inches(0.6),
        "Key Decisions Required",
        font_size=32,
        bold=True,
        color=NAVY,
    )
    add_text_box(
        slide,
        Inches(0.5),
        Inches(1.2),
        Inches(12),
        Inches(0.5),
        "Decisions needed from leadership today",
        font_size=16,
        color=RGBColor(0x66, 0x66, 0x66),
    )

    decisions = [
        "•  Approve $500K seed raise (Corporate Blueprint §7)",
        "•  Authorize 3× Offer A pilot clients post-governance gates",
        "•  Green-light hardware lab for offline-first proof",
        "•  Compliance sign-off: Malawi DPA 2017, GDPR opinion, SOC 2 Type II",
        "•  Hire Platform Licensing Sales Lead (Offer E) — Priority 1",
        "•  Approve BPA/Chatbot Delivery Lead (Offer B) for NGO USD revenue",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(2.3), Inches(8.5), Inches(4), decisions, font_size=13, color=NAVY)

    # Red for approval items
    add_text_box(
        slide,
        Inches(0.8),
        Inches(6.0),
        Inches(8.5),
        Inches(0.5),
        "All items require CEO signature before proceeding",
        font_size=12,
        bold=True,
        color=RED,
    )


def create_financial_overview_slide(prs):
    """Slide 9: Financial Overview — unit economics and trajectory."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(12),
        Inches(0.6),
        "Financial Overview",
        font_size=32,
        bold=True,
        color=NAVY,
    )
    add_text_box(
        slide,
        Inches(0.5),
        Inches(1.2),
        Inches(12),
        Inches(0.5),
        "Unit economics and trajectory",
        font_size=16,
        color=RGBColor(0x66, 0x66, 0x66),
    )

    # KPI boxes in grey
    kpis = [
        ("5", "Years to autonomy"),
        ("$500K", "Seed raise target"),
        ("3", "Offer families (A, B, C)"),
        ("80/10/10", "Brand color rule"),
    ]
    for i, (value, label) in enumerate(kpis):
        col = i % 2
        row = i // 2
        x = Inches(1 + col * 4.5)
        y = Inches(2.0 + row * 1.8)
        add_shape(
            slide,
            MSO_SHAPE.ROUNDED_RECTANGLE,
            x,
            y,
            Inches(3.5),
            Inches(1.2),
            fill_color=GREY,
        )
        add_text_box(
            slide,
            x + Inches(0.2),
            y + Inches(0.15),
            Inches(3.1),
            Inches(0.7),
            value,
            font_size=24,
            bold=True,
            color=NAVY,
            alignment=PP_ALIGN.CENTER,
        )
        add_text_box(
            slide,
            x + Inches(0.2),
            y + Inches(0.8),
            Inches(3.1),
            Inches(0.4),
            label,
            font_size=11,
            color=DARK_GREY,
            alignment=PP_ALIGN.CENTER,
        )

    # Cyan for trajectory
    add_text_box(
        slide,
        Inches(0.8),
        Inches(5.0),
        Inches(8.5),
        Inches(0.5),
        "Trajectory: $120K ARR → $500K → $2M+ by Q3 2027",
        font_size=13,
        bold=True,
        color=CYAN,
    )


def create_team_execution_slide(prs):
    """Slide 10: Team Capabilities — execution capacity and team strengths."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(12),
        Inches(0.6),
        "Team Capabilities",
        font_size=32,
        bold=True,
        color=NAVY,
    )
    add_text_box(
        slide,
        Inches(0.5),
        Inches(1.2),
        Inches(12),
        Inches(0.5),
        "Execution capacity and team strengths",
        font_size=16,
        color=RGBColor(0x66, 0x66, 0x66),
    )

    team = [
        "Leadership:",
        "  •  Jack Mlusu — Founder & CEO — builder-operator; runs a 5-agent AI org",
        "  •  AI Executive Cabinet — CTO, CFO, CMO, CLO, CSO, COO, CAIO (7 executives)",
        "  •  Board of Directors — 7 standing committees (Strategy, Finance, Risk, Technology, Product, Customer, Governance)",
        "",
        "Hiring Plan (per 90-day Blueprint):",
        "  •  Platform Licensing Sales Lead (Offer E) — Priority 1, breakout revenue line",
        "  •  BPA/Chatbot Delivery Lead (Offer B) — NGO USD revenue",
        "  •  Compliance Officer + DevRel Engineer — unblock Offer B/C & developer adoption",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(2.3), Inches(8.5), Inches(4), team, font_size=13, color=NAVY)

    # Cyan for developer adoption
    add_text_box(
        slide,
        Inches(0.8),
        Inches(5.8),
        Inches(8.5),
        Inches(0.5),
        "Focus: developer experience + compliance-first design",
        font_size=12,
        bold=True,
        color=CYAN,
    )


def create_future_outlook_slide(prs):
    """Slide 11: Future Outlook — where we're headed."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(12),
        Inches(0.6),
        "Future Outlook",
        font_size=32,
        bold=True,
        color=NAVY,
    )
    add_text_box(
        slide,
        Inches(0.5),
        Inches(1.2),
        Inches(12),
        Inches(0.5),
        "Where we're headed",
        font_size=16,
        color=RGBColor(0x66, 0x66, 0x66),
    )

    outlook = [
        "•  Q2 2027 — Multi-region deployment; local-first (Ollama) support",
        "•  Q3 2027 — Autonomous mode live — self-governing AI company",
        "•  2028 — $2M+ ARR with 5+ paying pilot clients",
        "•  2028 — Phase 5: fully autonomous AI company operation",
        "•  Ongoing — 80/10/10 brand rule enforced across all artifacts",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(2.3), Inches(8.5), Inches(3.5), outlook, font_size=13, color=NAVY)


def create_call_to_action_slide(prs):
    """Slide 12: Call to Action — what happens next."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    set_slide_bg(slide, NAVY)

    add_text_box(
        slide,
        Inches(1),
        Inches(1.5),
        Inches(11),
        Inches(1.0),
        "Call to Action",
        font_size=44,
        bold=True,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
    )
    add_text_box(
        slide,
        Inches(1),
        Inches(2.8),
        Inches(11),
        Inches(0.8),
        "What happens next",
        font_size=24,
        color=CYAN,
        alignment=PP_ALIGN.CENTER,
    )
    # Red accent line
    add_shape(
        slide,
        MSO_SHAPE.RECTANGLE,
        Inches(4.5),
        Inches(3.8),
        Inches(4.333),
        Inches(0.04),
        fill_color=RED,
    )

    cta_items = [
        "•  Schedule stakeholder alignment session (CEO + Cabinets)",
        "•  Review and approve $500K seed raise terms (§7 Corporate Blueprint)",
        "•  Authorize 3× Offer A pilot clients post-governance gates",
        "•  Green-light compliance sign-off: DPA, GDPR, SOC 2 Type II",
        "•  Kick-off hardware lab for offline-first proof of concept",
    ]
    add_bullet_list(slide, Inches(2), Inches(4.0), Inches(9.5), Inches(3), cta_items, font_size=15, color=WHITE)

    # CTA emphasis
    add_text_box(
        slide,
        Inches(1),
        Inches(7.2),
        Inches(11),
        Inches(0.4),
        "Aspire. Act. Achieve.",
        font_size=18,
        bold=True,
        color=CYAN,
        alignment=PP_ALIGN.CENTER,
    )


def create_closing_thesis_slide(prs):
    """Slide 13: Closing thesis — aspirational but grounded."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    set_slide_bg(slide, NAVY)

    add_text_box(
        slide,
        Inches(1),
        Inches(2.0),
        Inches(11),
        Inches(1.0),
        "Closing Thesis",
        font_size=44,
        bold=True,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
    )
    add_text_box(
        slide,
        Inches(1),
        Inches(3.2),
        Inches(11),
        Inches(1.0),
        "Aspirational but grounded",
        font_size=24,
        color=CYAN,
        alignment=PP_ALIGN.CENTER,
    )
    # Red accent line
    add_shape(
        slide,
        MSO_SHAPE.RECTANGLE,
        Inches(4.5),
        Inches(4.5),
        Inches(4.333),
        Inches(0.04),
        fill_color=RED,
    )

    thesis_items = [
        "The moment is right for AI-native company building — ",
        "and Lightspeed Holdings is the vehicle.",
        "",
        "•  80/10/10 brand rule: navy dominance, red/cyan accents, grey filler",
        "•  Governance gated: all decisions flow through 5-tier approval matrix",
        "•  Cost-transparent: built-in LLM spend monitoring per agent",
        "•  Human-over-automated: HITL gates on irreversible operations",
    ]
    add_bullet_list(
        slide,
        Inches(2),
        Inches(4.8),
        Inches(9.5),
        Inches(3),
        thesis_items,
        font_size=14,
        color=WHITE,
    )


def main():
    """Generate the 13-slide keynote deck."""
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 widescreen
    prs.slide_height = Inches(7.5)

    # Build deck (13 slides)
    create_opening_slide(prs)          # Slide 1
    create_market_opportunity_slide(prs)  # Slide 2
    create_our_solution_slide(prs)      # Slide 3
    create_customer_success_slide(prs)  # Slide 4
    create_competitive_differentiation_slide(prs)  # Slide 5
    create_technology_innovation_slide(prs)  # Slide 6
    create_roadmap_slide(prs)           # Slide 7
    create_key_decisions_slide(prs)    # Slide 8
    create_financial_overview_slide(prs)  # Slide 9
    create_team_execution_slide(prs)    # Slide 10
    create_future_outlook_slide(prs)    # Slide 11
    create_call_to_action_slide(prs)    # Slide 12
    create_closing_thesis_slide(prs)    # Slide 13

    # Save
    output_path = os.path.join(os.path.dirname(__file__), "..", "templates", "keynote-deck.pptx")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Keynote deck saved to: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    main()