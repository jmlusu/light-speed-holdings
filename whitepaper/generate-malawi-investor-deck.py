"""
LightSpeed Holdings — Malawi Investor Deck Generator
Creates a 14-slide investor deck focused on LightSpeed's potential in Malawi and the SADC region.
Brand: LightSpeed Holdings Limited | Tagline: Aspire. Act. Achieve.
Colors: Navy #070A40, Red #E63946, Cyan #00BFFF, Grey #F2F2F2
"""

import os
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

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


def add_text_box(slide, left, top, width, height, text, font_size=14, bold=False,
                 color=NAVY, alignment=PP_ALIGN.LEFT, font_name="Arial"):
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


def add_kpi_card(slide, x, y, value, label):
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(2.8), Inches(1.3), fill_color=GREY)
    add_text_box(slide, x + Inches(0.15), y + Inches(0.15), Inches(2.5), Inches(0.6),
                 value, font_size=26, bold=True, color=NAVY, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, x + Inches(0.15), y + Inches(0.75), Inches(2.5), Inches(0.4),
                 label, font_size=11, color=DARK_GREY, alignment=PP_ALIGN.CENTER)


# ── SLIDE 1: TITLE ──────────────────────────────────────────
def create_title_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)

    add_text_box(slide, Inches(1), Inches(1.5), Inches(8), Inches(0.6),
                 "LIGHTSPEED HOLDINGS LIMITED\u2122", font_size=32, bold=True, color=WHITE,
                 alignment=PP_ALIGN.CENTER)

    add_text_box(slide, Inches(1), Inches(2.2), Inches(8), Inches(0.5),
                 "Aspire. Act. Achieve.", font_size=18, color=CYAN,
                 alignment=PP_ALIGN.CENTER)

    add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(3.5), Inches(2.9), Inches(3), Inches(0.04),
              fill_color=RED)

    add_text_box(slide, Inches(1), Inches(3.3), Inches(8), Inches(1),
                 "AI-Native Company Building\nThe Malawi Opportunity",
                 font_size=24, bold=False, color=WHITE, alignment=PP_ALIGN.CENTER)

    add_text_box(slide, Inches(1), Inches(5.5), Inches(8), Inches(0.5),
                 "Investor Presentation — September 2026  |  Confidential",
                 font_size=12, color=LIGHT_TEXT, alignment=PP_ALIGN.CENTER)


# ── SLIDE 2: AGENDA ─────────────────────────────────────────
def create_agenda_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY)

    add_text_box(slide, Inches(0.5), Inches(0.4), Inches(9), Inches(0.6),
                 "AGENDA", font_size=28, bold=True, color=NAVY)

    items = [
        "1.  Why Malawi, Why Now",
        "2.  The Problem We Solve",
        "3.  Our Solution: AI-Native Companies",
        "4.  Market Opportunity: SADC Region",
        "5.  Service Offerings & Pricing",
        "6.  Technology & Platform",
        "7.  Traction & Milestones",
        "8.  Business Model",
        "9.  Team & Governance",
        "10. Financials & Use of Funds",
        "11. The Ask",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.2), Inches(8), Inches(5.5),
                    items, font_size=15, color=NAVY)


# ── SLIDE 3: WHY MALAWI ─────────────────────────────────────
def create_why_malawi_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY)

    add_text_box(slide, Inches(0.5), Inches(0.4), Inches(9), Inches(0.6),
                 "WHY MALAWI, WHY NOW", font_size=28, bold=True, color=NAVY)

    items = [
        "•  20M+ population, growing mobile penetration (50%+)",
        "•  Dual-currency market: MWK for local, USD for NGOs/international",
        "•  Limited IT talent pool — AI fills the gap",
        "•  Strong NGO/development sector (UN, donors, cooperatives)",
        "•  SADC gateway — 16-member regional bloc, 300M+ people",
        "•  Government pushing digital transformation agenda",
        "•  Low competition: no AI-native service providers in-market",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.2), Inches(8.5), Inches(4), items, font_size=14, color=NAVY)

    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(5.2), Inches(8), Inches(1.5),
              fill_color=GREY)
    add_text_box(slide, Inches(1.3), Inches(5.4), Inches(7.4), Inches(1.1),
                 "Malawi is not a market to skip — it is a market to prove the model.\n"
                 "If AI-native company building works here, it works anywhere.",
                 font_size=13, bold=True, color=NAVY, alignment=PP_ALIGN.CENTER)


# ── SLIDE 4: THE PROBLEM ────────────────────────────────────
def create_problem_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY)

    add_text_box(slide, Inches(0.5), Inches(0.4), Inches(9), Inches(0.6),
                 "THE PROBLEM", font_size=28, bold=True, color=NAVY)

    problems = [
        "•  SMEs can't afford full-time developers or agencies",
        "•  NGOs spend weeks on donor reports that could take days",
        "•  Schools, clinics, hotels have no digital presence",
        "•  Hiring is slow, expensive, and talent is scarce",
        "•  Traditional agencies charge $5K+ for basic websites",
        "•  24/7 customer service is impossible with manual staffing",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.2), Inches(8.5), Inches(3.5), problems, font_size=14, color=NAVY)

    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(4.8), Inches(8), Inches(2),
              fill_color=GREY)
    add_text_box(slide, Inches(1.3), Inches(5.0), Inches(7.4), Inches(1.6),
                 "The gap: Enterprise-grade digital services at SME prices.\n"
                 "LightSpeed fills it with 150+ AI agents, not 150+ employees.",
                 font_size=14, bold=True, color=NAVY, alignment=PP_ALIGN.CENTER)


# ── SLIDE 5: SOLUTION ───────────────────────────────────────
def create_solution_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY)

    add_text_box(slide, Inches(0.5), Inches(0.4), Inches(9), Inches(0.6),
                 "OUR SOLUTION", font_size=28, bold=True, color=NAVY)

    add_text_box(slide, Inches(0.8), Inches(1.2), Inches(8.5), Inches(0.7),
                 "AI-Native Company Building: One human CEO + 150 AI agents = enterprise output at SME cost.",
                 font_size=15, bold=False, color=NAVY)

    features = [
        "•  150+ agents across 20 departments — engineering, design, marketing, sales, legal",
        "•  5-tier approval system — human-in-the-loop for every high-stakes decision",
        "•  Multi-provider LLM routing — OpenAI, Anthropic, Gemini with automatic fallback",
        "•  Offline-first architecture — works on low bandwidth, local Ollama models",
        "•  WhatsApp-native flows — meet customers where they already are",
        "•  Full audit trail — every action logged, queryable, compliant",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(2.1), Inches(8.5), Inches(4), features, font_size=13, color=NAVY)

    add_kpi_card(slide, Inches(1), Inches(5.8), "150+", "AI Agents")
    add_kpi_card(slide, Inches(4.1), Inches(5.8), "20", "Departments")
    add_kpi_card(slide, Inches(7.2), Inches(5.8), "24/7", "Operations")


# ── SLIDE 6: MARKET OPPORTUNITY ─────────────────────────────
def create_market_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY)

    add_text_box(slide, Inches(0.5), Inches(0.4), Inches(9), Inches(0.6),
                 "MARKET OPPORTUNITY", font_size=28, bold=True, color=NAVY)

    add_text_box(slide, Inches(0.8), Inches(1.1), Inches(8.5), Inches(0.5),
                 "SADC Region: 300M+ people, 16 countries, rapidly digitizing.",
                 font_size=14, bold=False, color=NAVY)

    # TAM/SAM/SOM
    add_kpi_card(slide, Inches(0.8), Inches(1.8), "$65B", "TAM — Global AI Agent Platforms")
    add_kpi_card(slide, Inches(3.9), Inches(1.8), "$2.5B", "SAM — Africa & SADC Digital Services")
    add_kpi_card(slide, Inches(7), Inches(1.8), "$50M", "SOM — Malawi + SADC (Year 3)")

    segments = [
        "Target Segments:",
        "•  Local SMEs — websites, e-commerce, automation (MWK pricing)",
        "•  NGOs & Donors — data, analytics, reporting (USD pricing)",
        "•  Schools & Clinics — digital tools, patient/student systems",
        "•  Hotels & Tourism — booking systems, Google presence",
        "•  Cooperatives & Agri — market access, supply chain dashboards",
        "•  Diaspora Entrepreneurs — AI Company Builder license",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(3.5), Inches(8.5), Inches(3.5), segments, font_size=13, color=NAVY)


# ── SLIDE 7: SERVICE OFFERINGS ──────────────────────────────
def create_offerings_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY)

    add_text_box(slide, Inches(0.5), Inches(0.4), Inches(9), Inches(0.6),
                 "SERVICE OFFERINGS & PRICING", font_size=28, bold=True, color=NAVY)

    # Offer A
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.2), Inches(4.3), Inches(2.5),
              fill_color=GREY)
    add_text_box(slide, Inches(0.7), Inches(1.3), Inches(3.9), Inches(0.4),
                 "Offer A: Digital Presence", font_size=13, bold=True, color=RED)
    add_text_box(slide, Inches(0.7), Inches(1.7), Inches(3.9), Inches(0.3),
                 "From MWK 150,000 (~$85)", font_size=11, color=NAVY)
    add_text_box(slide, Inches(0.7), Inches(2.1), Inches(3.9), Inches(1.4),
                 "Websites, e-commerce, brand identity,\nGoogle Business, social media kit",
                 font_size=11, color=DARK_GREY)

    # Offer B
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.2), Inches(1.2), Inches(4.3), Inches(2.5),
              fill_color=GREY)
    add_text_box(slide, Inches(5.4), Inches(1.3), Inches(3.9), Inches(0.4),
                 "Offer B: Business Process Automation", font_size=13, bold=True, color=RED)
    add_text_box(slide, Inches(5.4), Inches(1.7), Inches(3.9), Inches(0.3),
                 "From MWK 900,000 (~$500)", font_size=11, color=NAVY)
    add_text_box(slide, Inches(5.4), Inches(2.1), Inches(3.9), Inches(1.4),
                 "WhatsApp chatbots, document generators,\nsurvey automation, custom dashboards",
                 font_size=11, color=DARK_GREY)

    # Offer C
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(4.0), Inches(4.3), Inches(2.5),
              fill_color=GREY)
    add_text_box(slide, Inches(0.7), Inches(4.1), Inches(3.9), Inches(0.4),
                 "Offer C: Data & Donor Reporting", font_size=13, bold=True, color=RED)
    add_text_box(slide, Inches(0.7), Inches(4.5), Inches(3.9), Inches(0.3),
                 "From MWK 700,000 (~$400)", font_size=11, color=NAVY)
    add_text_box(slide, Inches(0.7), Inches(4.9), Inches(3.9), Inches(1.4),
                 "Data cleaning, donor reports, interactive\nKPI dashboards, survey design",
                 font_size=11, color=DARK_GREY)

    # Offer D & E
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.2), Inches(4.0), Inches(4.3), Inches(2.5),
              fill_color=GREY)
    add_text_box(slide, Inches(5.4), Inches(4.1), Inches(3.9), Inches(0.4),
                 "Offer D: Digital Marketing", font_size=13, bold=True, color=RED)
    add_text_box(slide, Inches(5.4), Inches(4.5), Inches(3.9), Inches(0.3),
                 "From MWK 350,000/mo (~$200/mo)", font_size=11, color=NAVY)
    add_text_box(slide, Inches(5.4), Inches(4.9), Inches(3.9), Inches(1.4),
                 "Social media management, content packs,\nGoogle/Facebook ad campaigns",
                 font_size=11, color=DARK_GREY)

    add_text_box(slide, Inches(0.5), Inches(6.7), Inches(9), Inches(0.5),
                 "Dual-currency: MWK for local SMEs  |  USD for NGOs & international clients",
                 font_size=12, bold=True, color=NAVY, alignment=PP_ALIGN.CENTER)


# ── SLIDE 8: TECHNOLOGY ─────────────────────────────────────
def create_technology_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY)

    add_text_box(slide, Inches(0.5), Inches(0.4), Inches(9), Inches(0.6),
                 "TECHNOLOGY & PLATFORM", font_size=28, bold=True, color=NAVY)

    tech = [
        "Platform Stack:",
        "  •  Python 3.12+ CLI (Typer) — no web server required",
        "  •  FastAPI REST + WebSocket dashboard (port 8420)",
        "  •  Registry YAML → Jinja2 → OpenCode agent files",
        "  •  1800+ automated tests, ruff + mypy + bandit clean",
        "",
        "AI Capabilities:",
        "  •  6-type memory engine (episodic, semantic, procedural, relational, temporal, aggregate)",
        "  •  Knowledge graphs with BFS pathfinding",
        "  •  Model routing: 3 cost tiers with automatic fallback",
        "  •  Circuit breakers, dead-letter queues, SLA monitoring",
        "",
        "Low-Bandwidth Design:",
        "  •  Offline-first: local Ollama models when connectivity drops",
        "  •  WhatsApp-native: no app download required",
        "  •  PWA that queues work offline",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.2), Inches(8.5), Inches(5.5), tech, font_size=12, color=NAVY)


# ── SLIDE 9: TRACTION ───────────────────────────────────────
def create_traction_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY)

    add_text_box(slide, Inches(0.5), Inches(0.4), Inches(9), Inches(0.6),
                 "TRACTION & MILESTONES", font_size=28, bold=True, color=NAVY)

    add_kpi_card(slide, Inches(0.8), Inches(1.3), "150+", "Agents Deployed")
    add_kpi_card(slide, Inches(3.9), Inches(1.3), "5", "Service Offers")
    add_kpi_card(slide, Inches(7), Inches(1.3), "20+", "Departments")

    milestones = [
        "Milestones:",
        "  •  Jul 2026 — Platform bootstrapped; Phase 1-2 core architecture shipped",
        "  •  Aug 2026 — 5 flagship offers priced & governance gates ratified",
        "  •  Aug 2026 — Corporate Blueprint adopted; $500K capital guidance signed",
        "  •  Sep 2026 — Whitepaper published; Open Design integration live",
        "  •  Oct 2026 — Target: 3 pilot clients in Malawi",
        "",
        "Reference Implementations:",
        "  •  We Lead Out (WLO) — AI-native Salesforce consultancy, 5.0 AppExchange rating",
        "  •  20+ projects shipped, 4-week median time to first value",
        "  •  Proof that AI-native model wins on speed, cost, and quality",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(3.0), Inches(8.5), Inches(4), milestones, font_size=12, color=NAVY)


# ── SLIDE 10: BUSINESS MODEL ────────────────────────────────
def create_business_model_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY)

    add_text_box(slide, Inches(0.5), Inches(0.4), Inches(9), Inches(0.6),
                 "BUSINESS MODEL", font_size=28, bold=True, color=NAVY)

    model = [
        "Revenue Streams:",
        "  1.  Client Services — Project-based delivery (Offers A-D)",
        "  2.  Managed Services — Monthly retainers (chatbots, dashboards, marketing)",
        "  3.  Platform Licensing — AI Company Builder SaaS ($49-$299/mo)",
        "  4.  Enterprise — Custom deployment, SLAs, dedicated support",
        "",
        "Pricing Strategy:",
        "  •  Local SMEs: MWK pricing via Airtel Money / TNM Mpamba",
        "  •  NGOs/International: USD pricing (50% upfront, 50% on delivery)",
        "  •  Platform: USD-denominated SaaS for developers & agencies",
        "",
        "Unit Economics:",
        "  •  Target gross margin: 70%+",
        "  •  LLM cost: ~15% of revenue at scale",
        "  •  CAC payback target: < 6 months",
        "  •  Net retention target: 120%+",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.2), Inches(8.5), Inches(5.5), model, font_size=13, color=NAVY)


# ── SLIDE 11: TEAM ──────────────────────────────────────────
def create_team_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY)

    add_text_box(slide, Inches(0.5), Inches(0.4), Inches(9), Inches(0.6),
                 "TEAM & GOVERNANCE", font_size=28, bold=True, color=NAVY)

    team = [
        "Leadership:",
        "  •  Jack Mlusu — Founder & CEO — builder-operator; runs a 150-agent AI organization",
        "  •  AI Executive Cabinet — CTO, CFO, CMO, CLO, CSO, COO, CAIO (7 executives)",
        "",
        "Governance:",
        "  •  Board of Directors — 7 standing committees",
        "  •  5-Tier Approval Matrix — human-in-the-loop for every high-stakes decision",
        "  •  Corporate Constitution — principles, decision order, escalation SLAs",
        "  •  Full audit trail — every agent action logged and queryable",
        "",
        "AI-Augmented Team = 150+ agents across:",
        "  •  Engineering (backend, frontend, DevOps, QA)",
        "  •  Business (sales, marketing, customer success, finance)",
        "  •  Creative (design, content, presentation, brand)",
        "  •  Governance (compliance, legal, ethics, security)",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.2), Inches(8.5), Inches(5.5), team, font_size=12, color=NAVY)


# ── SLIDE 12: FINANCIALS ───────────────────────────────────
def create_financials_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5), fill_color=NAVY)

    add_text_box(slide, Inches(0.5), Inches(0.4), Inches(9), Inches(0.6),
                 "FINANCIALS & USE OF FUNDS", font_size=28, bold=True, color=NAVY)

    financials = [
        "Revenue Projections:",
        "  •  Year 1:  $120K ARR (monthly target $10K/mo)",
        "  •  Year 2:  $300K ARR (recurring contracts + SaaS)",
        "  •  Year 3:  $600K ARR (SaaS + managed workforce + platform licenses)",
        "",
        "Key Assumptions:",
        "  •  10-15% MoM revenue growth in ramp phase",
        "  •  70%+ gross margin; LLM cost ~15% of revenue at scale",
        "  •  Dual-currency: MWK for local, USD for international",
        "",
        "Use of Funds ($500K Seed):",
        "  •  40-50% — Talent (sales leads, compliance, DevRel)",
        "  •  20-30% — Client Pilots (3x Offer A, 1x Offer B, 1x Offer C)",
        "  •  15-25% — Hardware Lab (on-prem GPU, offline-first proof)",
        "  •  10-15% — Compliance (Malawi DPA, GDPR, SOC 2 prep)",
        "  •  $50K — Emergency Reserve (CEO-only release)",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.2), Inches(8.5), Inches(5.5), financials, font_size=13, color=NAVY)


# ── SLIDE 13: THE ASK ──────────────────────────────────────
def create_the_ask_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)

    add_text_box(slide, Inches(1), Inches(0.8), Inches(8), Inches(0.8),
                 "THE ASK", font_size=32, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

    add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(3.5), Inches(1.7), Inches(3), Inches(0.04),
              fill_color=RED)

    add_text_box(slide, Inches(1), Inches(2.0), Inches(8), Inches(0.8),
                 "Raising $500K Seed", font_size=24, bold=False, color=CYAN,
                 alignment=PP_ALIGN.CENTER)

    ask = [
        "What We Deliver With This Raise:",
        "  •  5 paying pilot clients across Offers A-C in Malawi",
        "  •  $120K ARR run-rate (SaaS + managed recurring)",
        "  •  Phase 5 autonomous mode — self-governing AI company",
        "  •  Proof that AI-native model works in low-bandwidth Africa",
        "",
        "What Investors Get:",
        "  •  Equity in the first AI-native company builder for SADC",
        "  •  A proven platform (1800+ tests, production-grade)",
        "  •  First-mover advantage in a $2.5B Africa digital services market",
        "  •  A model that scales across 16 SADC countries (300M+ people)",
    ]
    add_bullet_list(slide, Inches(1.5), Inches(3.2), Inches(7), Inches(3.5), ask, font_size=14, color=WHITE)


# ── SLIDE 14: THANK YOU ────────────────────────────────────
def create_thank_you_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)

    add_text_box(slide, Inches(1), Inches(2.0), Inches(8), Inches(1),
                 "THANK YOU", font_size=36, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

    add_text_box(slide, Inches(1), Inches(3.2), Inches(8), Inches(0.6),
                 "Aspire. Act. Achieve.", font_size=18, color=CYAN, alignment=PP_ALIGN.CENTER)

    add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(3.5), Inches(4.0), Inches(3), Inches(0.04),
              fill_color=RED)

    add_text_box(slide, Inches(1), Inches(4.3), Inches(8), Inches(1.5),
                 "Jack Mlusu, Founder & CEO\n"
                 "jmlusu@gmail.com\n"
                 "+265 (0) 980 016 004\n"
                 "lightspeedholdings.com",
                 font_size=14, color=WHITE, alignment=PP_ALIGN.CENTER)


def main():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    create_title_slide(prs)
    create_agenda_slide(prs)
    create_why_malawi_slide(prs)
    create_problem_slide(prs)
    create_solution_slide(prs)
    create_market_slide(prs)
    create_offerings_slide(prs)
    create_technology_slide(prs)
    create_traction_slide(prs)
    create_business_model_slide(prs)
    create_team_slide(prs)
    create_financials_slide(prs)
    create_the_ask_slide(prs)
    create_thank_you_slide(prs)

    output_path = os.path.join(os.path.dirname(__file__), "lightspeed-malawi-investor-deck.pptx")
    prs.save(output_path)
    print(f"Malawi investor deck saved to: {os.path.abspath(output_path)}")
    print(f"Slides: {len(prs.slides)}")


if __name__ == "__main__":
    main()
