"""
LightSpeed Holdings — Board Meeting Template Generator
Creates a 10-slide board meeting deck using python-pptx.
Brand: LightSpeed Holdings Limited | Tagline: Aspire. Act. Achieve.
Colors: Navy #070A40, Red #E63946, Cyan #00BFFF, Grey #F2F2F2
"""

import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

NAVY = RGBColor(0x07, 0x0A, 0x40)
RED = RGBColor(0xE6, 0x39, 0x46)
CYAN = RGBColor(0x00, 0xBF, 0xFF)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREY = RGBColor(0xF2, 0xF2, 0xF2)
DARK_GREY = RGBColor(0x6B, 0x72, 0x80)


def set_slide_bg(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape(slide, shape_type, left, top, width, height, fill_color=None):
    shape = slide.shapes.add_shape(shape_type, left, top, width, height)
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
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
):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = "Arial"
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
    return txBox


def create_cover_slide(prs, date="August 27, 2026"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)
    add_text_box(
        slide,
        Inches(1),
        Inches(1.5),
        Inches(8),
        Inches(1),
        "LIGHTSPEED HOLDINGS LIMITED",
        font_size=32,
        bold=True,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
    )
    add_text_box(
        slide,
        Inches(1),
        Inches(2.8),
        Inches(8),
        Inches(0.6),
        "Board of Directors Meeting",
        font_size=20,
        color=CYAN,
        alignment=PP_ALIGN.CENTER,
    )
    add_shape(
        slide,
        MSO_SHAPE.RECTANGLE,
        Inches(3.5),
        Inches(3.6),
        Inches(3),
        Inches(0.04),
        fill_color=RED,
    )
    add_text_box(
        slide,
        Inches(1),
        Inches(3.8),
        Inches(8),
        Inches(0.5),
        date,
        font_size=14,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
    )
    add_text_box(
        slide,
        Inches(1),
        Inches(4.5),
        Inches(8),
        Inches(0.4),
        "CONFIDENTIAL",
        font_size=11,
        color=DARK_GREY,
        alignment=PP_ALIGN.CENTER,
    )


def create_agenda_slide(prs):
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
        "AGENDA",
        font_size=28,
        bold=True,
        color=NAVY,
    )
    items = [
        "1.  Approval of Previous Minutes",
        "2.  CEO Report",
        "3.  Financial Summary",
        "4.  Product & Engineering Update",
        "5.  Sales & Marketing Update",
        "6.  Customer Success Report",
        "7.  Key Decisions Required",
        "8.  Next Meeting",
    ]
    add_bullet_list(
        slide, Inches(0.8), Inches(1.2), Inches(8), Inches(5.5), items, font_size=16, color=NAVY
    )


def create_ceo_report_slide(prs):
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
        "CEO REPORT",
        font_size=28,
        bold=True,
        color=NAVY,
    )
    items = [
        "Strategic Priorities This Quarter:",
        "  •  Activate Platform Licensing Sales Lead (Offer E) — 2026 breakout revenue",
        "  •  Unblock Offer B/C governance gates (G4 security review + liability cap)",
        "  •  Complete Phase 3 growth modules (Marketing, Sales, CS, Legal, HR)",
        "",
        "Key Accomplishments:",
        "  •  Phases 1–2 complete — 183 tests passing, ruff & mypy clean",
        "  •  Corporate Blueprint adopted (DIR-CEO-2026-001) — $500K capital guidance",
        "  •  Brand & investor materials ready — pitch deck, one-pager, social assets",
        "",
        "Challenges & Risks:",
        "  •  Revenue ledger not yet live — no audited customer revenue",
        "  •  Offer B/C still gated on security review (target Sep 5, 2026)",
    ]
    add_bullet_list(
        slide, Inches(0.8), Inches(1.2), Inches(8.5), Inches(5.5), items, font_size=13, color=NAVY
    )


def create_financial_summary_slide(prs):
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
        "FINANCIAL SUMMARY",
        font_size=28,
        bold=True,
        color=NAVY,
    )

    kpis = [
        ("$500K", "Capital Guidance"),
        ("$120K", "Y1 Revenue Target"),
        ("10–15%", "MoM Growth Target"),
        ("70%+", "Gross Margin Target"),
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

    items = [
        "Notes:",
        "  •  All figures are TARGETS — no audited customer revenue yet (pre-pilot)",
        "  •  $500K capital allocation ratified under Corporate Blueprint §7",
        "  •  Phase 3–5 LLM test costs are minimal (~$120 total) — local Ollama strategy",
    ]
    add_bullet_list(
        slide, Inches(0.8), Inches(5.2), Inches(8.5), Inches(2), items, font_size=12, color=NAVY
    )


def create_product_update_slide(prs):
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
        "PRODUCT & ENGINEERING UPDATE",
        font_size=28,
        bold=True,
        color=NAVY,
    )
    items = [
        "Shipped This Quarter:",
        "  •  Agent registry + generator — 19 YAML configs, 30+ CLI commands",
        "  •  Multi-provider LLM routing — 5 providers, 3-tier model routing",
        "  •  ReAct agent loop, HITL approval gates, cost tracking",
        "",
        "In Progress:",
        "  •  Phase 3 growth modules — Marketing, Sales, CS, Legal, HR",
        "  •  Dashboard auth + live KPIs (dashboard API hardening)",
        "",
        "Upcoming (Next Quarter):",
        "  •  Phase 4 — specialist agents (Financial Analyst, DevOps, Data Scientist, Compliance)",
        "  •  Phase 5 — autonomous coordination (scheduler, escalation, self-healing)",
        "",
        "Technical Debt & Reliability:",
        "  •  20 known architecture gaps (2 CRITICAL, 5 HIGH)",
        "  •  In-memory budget accumulators reset on restart — rebuild from JSONL log",
    ]
    add_bullet_list(
        slide, Inches(0.8), Inches(1.2), Inches(8.5), Inches(5.5), items, font_size=12, color=NAVY
    )


def create_sales_marketing_slide(prs):
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
        "SALES & MARKETING UPDATE",
        font_size=28,
        bold=True,
        color=NAVY,
    )
    items = [
        "Pipeline:",
        "  •  0 qualified leads yet — pre-pilot, pipeline forming",
        "  •  5 flagship offers priced (Digital Presence, AI Growth, Automation, Data, Builder)",
        "  •  Offer E (Platform Licensing) designated 2026 breakout revenue line",
        "",
        "Customer Wins:",
        "  •  None booked yet — pilots planned: 3× Offer A, 1× Offer B, 1× Offer C",
        "",
        "Marketing:",
        "  •  Brand rollout complete — logos, pitch deck, one-pager, social assets",
        "  •  Investor readiness plan live (22-task checklist)",
        "",
        "Key Initiatives:",
        "  •  Activate Platform Licensing Sales Lead — Week 1–2",
        "  •  Offer B/C governance unblock (Sep 5, 2026 security review)",
    ]
    add_bullet_list(
        slide, Inches(0.8), Inches(1.2), Inches(8.5), Inches(5.5), items, font_size=12, color=NAVY
    )


def create_customer_success_slide(prs):
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
        "CUSTOMER SUCCESS REPORT",
        font_size=28,
        bold=True,
        color=NAVY,
    )
    items = [
        "Health Metrics (targets — tools incoming in Phase 3/4):",
        "  •  NPS: target ≥ 70 | CSAT: target ≥ 4.5/5.0",
        "  •  Churn: target < 5% | Net retention: target ≥ 120%",
        "",
        "Support:",
        "  •  No customer tickets yet — pre-pilot",
        "  •  Slack + MessageBus broadcast for escalations",
        "",
        "Customer Feedback Highlights:",
        "  •  N/A — awaiting first pilots",
        "  •  Pilot success metrics defined: NPS ≥ 4.5, Time-to-Value < 2 weeks",
    ]
    add_bullet_list(
        slide, Inches(0.8), Inches(1.2), Inches(8.5), Inches(5.5), items, font_size=12, color=NAVY
    )


def create_decisions_slide(prs):
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
        "KEY DECISIONS REQUIRED",
        font_size=28,
        bold=True,
        color=NAVY,
    )
    items = [
        "Decision 1: Authorize first client pilots (3× Offer A, 1× Offer B, 1× Offer C)",
        "  •  Context: Pilots are gated on ratified G1–G4 governance + signed MSA/DPA",
        "  •  Options: Proceed now (cash-flow + referenceable) vs wait for full SOC 2",
        "  •  Recommendation: Proceed with Offer A pilots now; Offer B/C after Sep 5 review",
        "  •  Deadline: Sep 1, 2026",
        "",
        "Decision 2: Ratify SaaS pricing band $49–$299/mo for Offer E (AI Company Builder)",
        "  •  Context: Fee-based pricing in catalog; needs CFO + CEO sign-off to publish",
        "  •  Options: $49–$299 band vs $99–$499 premium",
        "  •  Recommendation: Approve $49–$299 to maximize developer-led adoption",
        "  •  Deadline: Sep 1, 2026",
        "",
        "Decision 3: Confirm Y1 revenue target ($120K ARR) for investor materials",
        "  •  Context: DIR-CEO-2026-001 §6.2 requires CFO sign-off on revenue projections",
        "  •  Options: $120K target vs conservative ($60K) vs stretch ($200K)",
        "  •  Recommendation: $120K ARR ($10K/mo) — consistent with finance KPI",
        "  •  Deadline: Before next fundraise pitch",
    ]
    add_bullet_list(
        slide, Inches(0.8), Inches(1.2), Inches(8.5), Inches(5.5), items, font_size=12, color=NAVY
    )


def create_closing_slide(prs, next_date="[Next Date]"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)
    add_text_box(
        slide,
        Inches(1),
        Inches(1.8),
        Inches(8),
        Inches(0.8),
        "NEXT BOARD MEETING",
        font_size=28,
        bold=True,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
    )
    add_text_box(
        slide,
        Inches(1),
        Inches(2.8),
        Inches(8),
        Inches(0.5),
        next_date,
        font_size=18,
        color=CYAN,
        alignment=PP_ALIGN.CENTER,
    )
    add_shape(
        slide,
        MSO_SHAPE.RECTANGLE,
        Inches(3.5),
        Inches(3.5),
        Inches(3),
        Inches(0.04),
        fill_color=RED,
    )
    add_text_box(
        slide,
        Inches(1),
        Inches(3.8),
        Inches(8),
        Inches(0.5),
        "Aspire. Act. Achieve.",
        font_size=16,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
    )
    add_text_box(
        slide,
        Inches(1),
        Inches(5.0),
        Inches(8),
        Inches(0.4),
        "CONFIDENTIAL — For Board Members Only",
        font_size=11,
        color=DARK_GREY,
        alignment=PP_ALIGN.CENTER,
    )


def main():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    create_cover_slide(prs)
    create_agenda_slide(prs)
    create_ceo_report_slide(prs)
    create_financial_summary_slide(prs)
    create_product_update_slide(prs)
    create_sales_marketing_slide(prs)
    create_customer_success_slide(prs)
    create_decisions_slide(prs)
    create_closing_slide(prs, next_date="September 15, 2026 — Q3 Strategy Pivot Review")

    output_path = os.path.join(os.path.dirname(__file__), "..", "templates", "board-meeting.pptx")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Board meeting template saved to: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    main()
