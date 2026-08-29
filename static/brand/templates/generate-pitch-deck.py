"""
LightSpeed Holdings — Pitch Deck Template Generator
Creates a 14-slide investor pitch deck using python-pptx.
Brand: LightSpeed Holdings Limited | Tagline: Aspire. Act. Achieve.
Colors: Navy #070A40, Red #E63946, Cyan #00BFFF, Grey #F2F2F2
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
from scripts.company_counts import company_counts  # noqa: E402

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
    return txBox


def create_title_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    set_slide_bg(slide, NAVY)

    # Title
    add_text_box(
        slide,
        Inches(1),
        Inches(1.8),
        Inches(8),
        Inches(1.2),
        "LIGHTSPEED HOLDINGS LIMITED",
        font_size=36,
        bold=True,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
    )

    # Tagline
    add_text_box(
        slide,
        Inches(1),
        Inches(3.0),
        Inches(8),
        Inches(0.6),
        "Aspire. Act. Achieve.",
        font_size=18,
        color=CYAN,
        alignment=PP_ALIGN.CENTER,
    )

    # Accent line
    add_shape(
        slide,
        MSO_SHAPE.RECTANGLE,
        Inches(3.5),
        Inches(3.7),
        Inches(3),
        Inches(0.04),
        fill_color=RED,
    )

    # Subtitle
    add_text_box(
        slide,
        Inches(1),
        Inches(4.0),
        Inches(8),
        Inches(0.5),
        "Confidential — August 2026",
        font_size=12,
        color=LIGHT_TEXT,
        alignment=PP_ALIGN.CENTER,
    )


def create_agenda_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    # Section bar
    add_shape(
        slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY
    )

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(9),
        Inches(0.6),
        "AGENDA",
        font_size=28,
        bold=True,
        color=NAVY,
    )

    agenda_items = [
        "1.  The Problem",
        "2.  Our Solution",
        "3.  Market Opportunity",
        "4.  Product & Technology",
        "5.  Business Model",
        "6.  Traction & Metrics",
        "7.  Competitive Landscape",
        "8.  Team",
        "9.  Financials",
        "10. The Ask",
    ]
    add_bullet_list(
        slide,
        Inches(0.8),
        Inches(1.2),
        Inches(8),
        Inches(5.5),
        agenda_items,
        font_size=16,
        color=NAVY,
    )


def create_problem_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(
        slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY
    )

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(9),
        Inches(0.6),
        "THE PROBLEM",
        font_size=28,
        bold=True,
        color=NAVY,
    )

    problems = [
        "•  Organizations struggle to deploy AI agents at scale — each requires custom integration, monitoring, and governance",
        "•  Existing tools are either too simple (chatbots) or too complex (enterprise ML platforms)",
        "•  No turnkey solution exists for building an entire AI-powered organization",
        "•  Cost tracking, human oversight, and multi-provider management are afterthoughts",
    ]
    add_bullet_list(
        slide, Inches(0.8), Inches(1.3), Inches(8.5), Inches(4), problems, font_size=14, color=NAVY
    )

    # Pain point callout
    add_shape(
        slide,
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(1),
        Inches(5.2),
        Inches(8),
        Inches(1.2),
        fill_color=GREY,
    )
    add_text_box(
        slide,
        Inches(1.3),
        Inches(5.4),
        Inches(7.4),
        Inches(0.9),
        '"Building an AI-native company shouldn\'t require a team of ML engineers."',
        font_size=14,
        bold=True,
        color=NAVY,
        alignment=PP_ALIGN.CENTER,
    )


def create_solution_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(
        slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY
    )

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(9),
        Inches(0.6),
        "OUR SOLUTION",
        font_size=28,
        bold=True,
        color=NAVY,
    )

    add_text_box(
        slide,
        Inches(0.8),
        Inches(1.2),
        Inches(8.5),
        Inches(0.8),
        "AI Company Builder — a CLI platform that generates, orchestrates, and manages complete AI agent organizations.",
        font_size=16,
        bold=False,
        color=NAVY,
    )

    features = [
        "✓  Registry-driven: Define agents in YAML, generate OpenCode-compatible markdown files",
        "✓  Multi-provider LLM routing: OpenAI, Anthropic, DeepSeek, Gemini with automatic fallback",
        "✓  Built-in cost tracking & budget enforcement per agent",
        "✓  Human-in-the-loop approval gates for dangerous operations",
        "✓  MessageBus task queue for cross-agent coordination",
        "✓  "
        + str(AGENT_COUNT)
        + " pre-built agent roles across "
        + str(DEPARTMENT_COUNT)
        + " departments",
    ]
    add_bullet_list(
        slide,
        Inches(0.8),
        Inches(2.2),
        Inches(8.5),
        Inches(4.5),
        features,
        font_size=13,
        color=NAVY,
    )


def create_market_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(
        slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY
    )

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(9),
        Inches(0.6),
        "MARKET OPPORTUNITY",
        font_size=28,
        bold=True,
        color=NAVY,
    )

    add_text_box(
        slide,
        Inches(0.8),
        Inches(1.2),
        Inches(8.5),
        Inches(0.6),
        "The AI agent infrastructure market is projected to reach $65B by 2028.",
        font_size=16,
        bold=False,
        color=NAVY,
    )

    tam_items = [
        "TAM:  $65B — Enterprise AI agent platforms & orchestration",
        "SAM:  $12B — Mid-market companies deploying AI agents",
        "SOM:  $120M — Developer-led, self-serve AI company builder",
    ]
    add_bullet_list(
        slide,
        Inches(0.8),
        Inches(2.0),
        Inches(8.5),
        Inches(2.5),
        tam_items,
        font_size=14,
        color=NAVY,
    )

    # Target segments
    add_text_box(
        slide,
        Inches(0.8),
        Inches(4.0),
        Inches(8.5),
        Inches(0.5),
        "TARGET SEGMENTS",
        font_size=14,
        bold=True,
        color=RED,
    )
    segments = [
        "•  Startups building AI-native products",
        "•  SMBs automating operations with AI agents",
        "•  Enterprises deploying internal AI agent fleets",
        "•  AI consultancies building client agent systems",
    ]
    add_bullet_list(
        slide,
        Inches(0.8),
        Inches(4.5),
        Inches(8.5),
        Inches(2.5),
        segments,
        font_size=13,
        color=NAVY,
    )


def create_product_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(
        slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY
    )

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(9),
        Inches(0.6),
        "PRODUCT & TECHNOLOGY",
        font_size=28,
        bold=True,
        color=NAVY,
    )

    tech_items = [
        "Architecture:",
        "  •  Python 3.12+ CLI (Typer) — no web server required",
        "  •  Registry YAML → Jinja2 template → OpenCode agent files",
        "  •  ReAct agentic loop with tool routing",
        "",
        "Core Components:",
        "  •  AgentLoop — Multi-turn reasoning with tool execution",
        "  •  CostTracker — Real-time LLM spend monitoring",
        "  •  HITLGate — Human approval for irreversible actions",
        "  •  MessageBus — JSON task queue for agent coordination",
        "  •  ModelRouter — Provider fallback chain (OpenAI → Anthropic → DeepSeek → Gemini)",
        "",
        "Security:",
        "  •  Bandit static analysis, pre-commit hooks",
        "  •  Principle-of-least-privilege agent permissions",
        "  •  Encrypted credential storage",
    ]
    add_bullet_list(
        slide,
        Inches(0.8),
        Inches(1.2),
        Inches(8.5),
        Inches(5.5),
        tech_items,
        font_size=12,
        color=NAVY,
    )


def create_business_model_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(
        slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY
    )

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(9),
        Inches(0.6),
        "BUSINESS MODEL",
        font_size=28,
        bold=True,
        color=NAVY,
    )

    model_items = [
        "Revenue Streams:",
        "  1.  SaaS Subscription — Monthly/annual plans for platform access",
        "  2.  Usage-Based — LLM token pass-through + margin",
        "  3.  Enterprise — Custom deployment, SLAs, dedicated support",
        "  4.  Services — Implementation consulting for large deployments",
        "",
        "Pricing Tiers:",
        "  •  AI Company Builder SaaS — $49 / $149 / $299 per month (Starter/Pro/Enterprise)",
        "  •  Managed AI Workforce — MWK 2M+ / mo (highest-value recurring service)",
        "",
        "Unit Economics:",
        "  •  Target gross margin: 70%+",
        "  •  LLM cost: ~15% of revenue at scale",
        "  •  Target CAC payback: < 6 months",
    ]
    add_bullet_list(
        slide,
        Inches(0.8),
        Inches(1.2),
        Inches(8.5),
        Inches(5.5),
        model_items,
        font_size=12,
        color=NAVY,
    )


def create_traction_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(
        slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY
    )

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(9),
        Inches(0.6),
        "TRACTION & METRICS",
        font_size=28,
        bold=True,
        color=NAVY,
    )

    # KPI boxes
    kpis = [
        (str(AGENT_COUNT), "Agents Deployed"),
        (str(DEPARTMENT_COUNT), "Departments Live"),
        ("5", "Flagship Offers"),
        ("8", "Priced Recurring Products"),
    ]
    for i, (value, label) in enumerate(kpis):
        col = i % 2
        row = i // 2
        x = Inches(1 + col * 4)
        y = Inches(1.3 + row * 1.8)
        add_shape(
            slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.5), Inches(1.4), fill_color=GREY
        )
        add_text_box(
            slide,
            x + Inches(0.2),
            y + Inches(0.2),
            Inches(3.1),
            Inches(0.6),
            value,
            font_size=28,
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
            font_size=12,
            color=DARK_GREY,
            alignment=PP_ALIGN.CENTER,
        )

    milestones = [
        "Key Milestones:",
        "  •  Jul 2026 — Platform bootstrapped; Phase 1–2 core architecture shipped",
        "  •  Aug 2026 — 5 flagship offers priced & governance gates ratified",
        "  •  Aug 2026 — Corporate Blueprint adopted; $500K capital guidance signed",
        "  •  2,000+ automated tests; ruff, mypy & bandit clean",
    ]
    add_bullet_list(
        slide,
        Inches(0.8),
        Inches(5.0),
        Inches(8.5),
        Inches(2),
        milestones,
        font_size=12,
        color=NAVY,
    )


def create_competition_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(
        slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY
    )

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(9),
        Inches(0.6),
        "COMPETITIVE LANDSCAPE",
        font_size=28,
        bold=True,
        color=NAVY,
    )

    competitors = [
        "Direct Competitors:",
        "  •  Agent frameworks (LangGraph, CrewAI) — dev tools, no org layer or governance",
        "  •  Workflow automation (n8n, Zapier) — task pipelines, not multi-agent organizations",
        "  •  Single-assistant SaaS (ChatGPT Business, Copilot) — no role hierarchy or cost control",
        "",
        "Indirect Alternatives:",
        "  •  Custom-built agent frameworks (high engineering cost)",
        "  •  ChatGPT/Claude for single tasks (no orchestration)",
        "  •  Enterprise ML platforms (overkill for most orgs)",
        "",
        "Our Differentiation:",
        "  ✓  AI-native company structure (not just a tool)",
        "  ✓  Built-in cost transparency & budget enforcement",
        "  ✓  Human-in-the-loop safety gates",
        "  ✓  Multi-provider with automatic fallback",
        "  ✓  Local-first option (Ollama) for zero-cost inference",
    ]
    add_bullet_list(
        slide,
        Inches(0.8),
        Inches(1.2),
        Inches(8.5),
        Inches(5.5),
        competitors,
        font_size=12,
        color=NAVY,
    )


def create_team_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(
        slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY
    )

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(9),
        Inches(0.6),
        "TEAM",
        font_size=28,
        bold=True,
        color=NAVY,
    )

    team = [
        "Leadership:",
        "  •  Jack Mlusu — Founder & CEO — builder-operator; runs a "
        + str(AGENT_COUNT)
        + "-agent AI organization",
        "  •  AI Executive Cabinet — CTO, CFO, CMO, CLO, CSO, COO, CAIO (7 executives)",
        "  •  Board of Directors — 7 standing committees (Strategy, Finance, Risk, Technology, Product, Customer, Governance)",
        "",
        "Advisors:",
        "  •  Board Chair — governance & escalation authority",
        "  •  Corporate Constitution — 5-tier approval matrix, decision order, escalation SLAs",
        "",
        "Hiring Plan (per 90-day Blueprint):",
        "  •  Platform Licensing Sales Lead (Offer E) — Priority 1, breakout revenue line",
        "  •  BPA/Chatbot Delivery Lead (Offer B) — NGO USD revenue",
        "  •  Compliance Officer + DevRel Engineer — unblock Offer B/C & developer adoption",
    ]
    add_bullet_list(
        slide, Inches(0.8), Inches(1.2), Inches(8.5), Inches(5.5), team, font_size=13, color=NAVY
    )


def create_financials_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(
        slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY
    )

    add_text_box(
        slide,
        Inches(0.5),
        Inches(0.4),
        Inches(9),
        Inches(0.6),
        "FINANCIALS",
        font_size=28,
        bold=True,
        color=NAVY,
    )

    financials = [
        "Revenue Projections (targets, pending CFO validation):",
        "  •  Year 1:  $120K ARR (monthly revenue target $10K/mo)",
        "  •  Year 2:  $300K ARR (recurring contracts + SaaS)",
        "  •  Year 3:  $600K ARR (SaaS $49–$299/mo + managed workforce)",
        "",
        "Key Assumptions:",
        "  •  10–15% MoM revenue growth in ramp (target)",
        "  •  70%+ gross margin target; LLM cost ~15% of revenue at scale",
        "  •  120% net retention target (per Mission success metrics)",
        "",
        "Use of Funds (First $500K — Corporate Blueprint §7):",
        "  •  40–50% — Talent (sales leads, compliance, DevRel)",
        "  •  20–30% — Client Pilots (3× Offer A, 1× Offer B, 1× Offer C)",
        "  •  15–25% — Hardware Lab (on-prem GPU, offline-first proof)",
        "  •  10–15% — Compliance & Legal (Malawi DPA 2017, GDPR, SOC 2 prep)",
        "  •  $50K — Emergency Reserve (CEO-only release)",
    ]
    add_bullet_list(
        slide,
        Inches(0.8),
        Inches(1.2),
        Inches(8.5),
        Inches(5.5),
        financials,
        font_size=13,
        color=NAVY,
    )


def create_the_ask_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)

    add_text_box(
        slide,
        Inches(1),
        Inches(0.8),
        Inches(8),
        Inches(0.8),
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
        Inches(1.7),
        Inches(3),
        Inches(0.04),
        fill_color=RED,
    )

    add_text_box(
        slide,
        Inches(1),
        Inches(2.0),
        Inches(8),
        Inches(0.8),
        "Raising $500K Seed",
        font_size=24,
        bold=False,
        color=CYAN,
        alignment=PP_ALIGN.CENTER,
    )

    ask_items = [
        "Use of Funds (aligned to Corporate Blueprint §7):",
        "  •  Talent — Platform Licensing Sales Lead (Offer E), chatbot/compliance leads",
        "  •  Client pilots — 3× Offer A, 1× Offer B, 1× Offer C (post governance gates)",
        "  •  Hardware lab — on-prem GPU for offline-first proof; Malawi field kits",
        "  •  Compliance — Malawi DPA 2017, GDPR opinion, SOC 2 Type II readiness",
        "",
        "Milestones with this raise:",
        "  •  5 paying pilot clients across Offers A–C",
        "  •  $120K ARR run-rate (SaaS + managed recurring)",
        "  •  Phase 5 autonomous mode live — self-governing AI company",
    ]
    add_bullet_list(
        slide,
        Inches(1.5),
        Inches(3.2),
        Inches(7),
        Inches(3.5),
        ask_items,
        font_size=14,
        color=WHITE,
    )


def create_thank_you_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)

    add_text_box(
        slide,
        Inches(1),
        Inches(2.0),
        Inches(8),
        Inches(1),
        "THANK YOU",
        font_size=36,
        bold=True,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
    )

    add_text_box(
        slide,
        Inches(1),
        Inches(3.2),
        Inches(8),
        Inches(0.6),
        "Aspire. Act. Achieve.",
        font_size=18,
        color=CYAN,
        alignment=PP_ALIGN.CENTER,
    )

    add_shape(
        slide,
        MSO_SHAPE.RECTANGLE,
        Inches(3.5),
        Inches(4.0),
        Inches(3),
        Inches(0.04),
        fill_color=RED,
    )

    add_text_box(
        slide,
        Inches(1),
        Inches(4.3),
        Inches(8),
        Inches(1.5),
        "Jack Mlusu, Founder & CEO\njmlusu@gmail.com\n+265 (0) 980 016 004\nlightspeedholdings.com",
        font_size=14,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
    )


def main():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # Build deck
    create_title_slide(prs)
    create_agenda_slide(prs)
    create_problem_slide(prs)
    create_solution_slide(prs)
    create_market_slide(prs)
    create_product_slide(prs)
    create_business_model_slide(prs)
    create_traction_slide(prs)
    create_competition_slide(prs)
    create_team_slide(prs)
    create_financials_slide(prs)
    create_the_ask_slide(prs)
    create_thank_you_slide(prs)

    # Save
    output_path = os.path.join(os.path.dirname(__file__), "..", "templates", "pitch-deck.pptx")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Pitch deck saved to: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    main()
