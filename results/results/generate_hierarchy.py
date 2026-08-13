#!/usr/bin/env python3
"""Generate Light Speed Holdings Organizational Hierarchy PowerPoint deck.

Usage:
    python results/generate_hierarchy.py

Creates results/light-speed-holdings-hierarchy.pptx with a dark blue executive theme.
127 AI agents across 17 departments — full organizational hierarchy.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.util import Inches, Pt
except ImportError:
    print("python-pptx not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-pptx"])
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.util import Inches, Pt

# ── Theme colors ──────────────────────────────────────────────────────────[...]
BG_DARK = RGBColor(0x0B, 0x19, 0x29)
BG_CARD = RGBColor(0x12, 0x2B, 0x45)
BG_CARD_ALT = RGBColor(0x0E, 0x23, 0x3B)
ACCENT = RGBColor(0x00, 0xD4, 0xAA)
ACCENT_DIM = RGBColor(0x00, 0x9E, 0x7E)
ACCENT_GOLD = RGBColor(0xFF, 0xB8, 0x47)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xB8, 0xC9, 0xE0)
MID_GRAY = RGBColor(0x7A, 0x8F, 0xA8)
DARK_TEXT = RGBColor(0x0B, 0x19, 0x29)
CORAL = RGBColor(0xFF, 0x6B, 0x6B)
PURPLE = RGBColor(0xA8, 0x78, 0xFF)
BLUE = RGBColor(0x4E, 0xA8, 0xFF)

SLIDE_W = Inches(10)
SLIDE_H = Inches(5.625)


def set_slide_bg(slide, color: RGBColor) -> None:
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape_rect(slide, x, y, w, h, fill_color, border_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.fill.solid()
        shape.line.fill.fore_color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape


def add_accent_bar(slide, x, y, w, h, color=ACCENT):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    return bar


def add_textbox(
    slide,
    x,
    y,
    w,
    h,
    text,
    font_size=14,
    color=WHITE,
    bold=False,
    align=PP_ALIGN.LEFT,
    font_name="Calibri",
    valign=MSO_ANCHOR.TOP,
):
    txBox = slide.shapes.add_textbox(x, y, w, h)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = align
    tf.auto_size = None
    txBox.text_frame.paragraphs[0].space_before = Pt(0)
    txBox.text_frame.paragraphs[0].space_after = Pt(0)
    return txBox


def add_bullet_list(
    slide, x, y, w, h, items, font_size=13, color=LIGHT_GRAY, bullet_color=ACCENT, spacing=6
):
    txBox = slide.shapes.add_textbox(x, y, w, h)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(spacing)
        p.space_after = Pt(spacing)
        run_bullet = p.add_run()
        run_bullet.text = "\u25cf  "
        run_bullet.font.size = Pt(font_size - 1)
        run_bullet.font.color.rgb = bullet_color
        run_bullet.font.name = "Calibri"
        run_text = p.add_run()
        run_text.text = item
        run_text.font.size = Pt(font_size)
        run_text.font.color.rgb = color
        run_text.font.name = "Calibri"
    return txBox


def add_stat_card(slide, x, y, w, h, number, label, num_color=ACCENT):
    add_shape_rect(slide, x, y, w, h, BG_CARD)
    add_textbox(
        slide,
        x + Inches(0.2),
        y + Inches(0.15),
        w - Inches(0.4),
        Inches(0.6),
        number,
        font_size=36,
        color=num_color,
        bold=True,
        align=PP_ALIGN.CENTER,
        font_name="Georgia",
    )
    add_textbox(
        slide,
        x + Inches(0.2),
        y + Inches(0.7),
        w - Inches(0.4),
        Inches(0.4),
        label,
        font_size=11,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
        font_name="Calibri",
    )


def add_title_bar(slide, title: str, accent_width: float = 2.0):
    """Standard dark title bar with accent underline."""
    add_shape_rect(slide, Inches(0), Inches(0), SLIDE_W, Inches(0.85), BG_CARD)
    add_textbox(
        slide,
        Inches(0.6),
        Inches(0.15),
        Inches(8),
        Inches(0.6),
        title,
        font_size=26,
        color=WHITE,
        bold=True,
        font_name="Georgia",
    )
    add_accent_bar(slide, Inches(0.6), Inches(0.75), Inches(accent_width), Inches(0.04))


def add_page_number(slide, num: int, total: int):
    add_textbox(
        slide,
        Inches(9.0),
        Inches(5.2),
        Inches(0.8),
        Inches(0.3),
        f"{num}/{total}",
        font_size=9,
        color=MID_GRAY,
        align=PP_ALIGN.RIGHT,
    )


# ── Slide builders ─────────────────────────────────────────────────────────[...]

TOTAL_SLIDES = 16


def build_slide_01_title(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)
    add_accent_bar(slide, Inches(0), Inches(0), SLIDE_W, Inches(0.06))

    add_shape_rect(slide, Inches(0.8), Inches(1.0), Inches(8.4), Inches(3.6), BG_CARD)

    add_textbox(
        slide,
        Inches(1.2),
        Inches(1.3),
        Inches(7.6),
        Inches(1.0),
        "Light Speed Holdings",
        font_size=42,
        color=WHITE,
        bold=True,
        align=PP_ALIGN.LEFT,
        font_name="Georgia",
    )
    add_accent_bar(slide, Inches(1.2), Inches(2.15), Inches(2.5), Inches(0.05))

    add_textbox(
        slide,
        Inches(1.2),
        Inches(2.4),
        Inches(7.6),
        Inches(0.5),
        "Organizational Hierarchy",
        font_size=28,
        color=ACCENT,
        bold=False,
        align=PP_ALIGN.LEFT,
        font_name="Georgia",
    )

    add_textbox(
        slide,
        Inches(1.2),
        Inches(3.1),
        Inches(7.6),
        Inches(0.5),
        "127 AI Agents  |  17 Departments  |  v0.3.0",
        font_size=16,
        color=MID_GRAY,
        align=PP_ALIGN.LEFT,
    )

    add_textbox(
        slide,
        Inches(1.2),
        Inches(3.7),
        Inches(7.6),
        Inches(0.4),
        "AI Company Builder \u2014 Building the Future of Work",
        font_size=13,
        color=LIGHT_GRAY,
        align=PP_ALIGN.LEFT,
    )

    add_accent_bar(slide, Inches(0), Inches(5.565), SLIDE_W, Inches(0.06))
    add_page_number(slide, 1, TOTAL_SLIDES)


def build_slide_02_overview(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)
    add_title_bar(slide, "Company Overview", 2.0)

    card_w = Inches(2.05)
    card_h = Inches(1.3)
    gap = Inches(0.15)
    start_x = Inches(0.5)
    y_cards = Inches(1.15)

    stats = [
        ("127", "AI Agents"),
        ("17", "Departments"),
        ("4", "Org Tiers"),
        ("1,205", "Tests Passing"),
    ]
    for i, (num, label) in enumerate(stats):
        x = start_x + i * (card_w + gap)
        add_stat_card(slide, x, y_cards, card_w, card_h, num, label)

    # Org tiers description
    add_shape_rect(slide, Inches(0.5), Inches(2.7), Inches(9.0), Inches(2.5), BG_CARD)
    add_accent_bar(slide, Inches(0.5), Inches(2.7), Inches(0.06), Inches(2.5), ACCENT)

    tiers = [
        "Tier 1: Board of Directors \u2014 Board Chair + 6 Committee Chairs (governance)",
        "Tier 2: Executive Team \u2014 Human CEO, Chief of Staff, 10 C-Suite + CEO Advisor",
        "Tier 3: Department Heads \u2014 CTO, COO, CAIO, CPO, CMO, CHRO, CFO, CISO, CLO, CSO",
        "Tier 4: Specialists & Leads \u2014 100+ specialist agents across all departments",
    ]
    add_bullet_list(
        slide, Inches(0.8), Inches(2.85), Inches(8.5), Inches(2.2), tiers, font_size=13, spacing=8
    )
    add_page_number(slide, 2, TOTAL_SLIDES)


def build_slide_03_board(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)
    add_title_bar(slide, "Board of Directors", 2.2)

    # Board Chair card (centered, prominent)
    add_shape_rect(slide, Inches(3.2), Inches(1.1), Inches(3.6), Inches(1.0), BG_CARD)
    add_accent_bar(slide, Inches(3.2), Inches(1.1), Inches(3.6), Inches(0.05), ACCENT_GOLD)
    add_textbox(
        slide,
        Inches(3.4),
        Inches(1.25),
        Inches(3.2),
        Inches(0.35),
        "Board Chair",
        font_size=16,
        color=WHITE,
        bold=True,
        align=PP_ALIGN.CENTER,
    )
    add_textbox(
        slide,
        Inches(3.4),
        Inches(1.6),
        Inches(3.2),
        Inches(0.3),
        "board_chair",
        font_size=11,
        color=ACCENT_GOLD,
        align=PP_ALIGN.CENTER,
        font_name="Consolas",
    )

    committees = [
        ("Finance Committee", "board_finance", ACCENT),
        ("Risk Committee", "board_risk", ACCENT),
        ("Strategy Committee", "board_strategy", ACCENT),
        ("Technology Committee", "board_technology", ACCENT),
        ("Customer Committee", "board_customer", ACCENT),
        ("Product Committee", "board_product", ACCENT),
    ]

    card_w = Inches(1.35)
    card_h = Inches(1.5)
    gap = Inches(0.12)
    start_x = Inches(0.5)
    y_cards = Inches(2.5)

    for i, (name, agent_id, color) in enumerate(committees):
        x = start_x + i * (card_w + gap)
        add_shape_rect(slide, x, y_cards, card_w, card_h, BG_CARD)
        add_accent_bar(slide, x, y_cards, card_w, Inches(0.04), color)
        add_textbox(
            slide,
            x + Inches(0.1),
            y_cards + Inches(0.15),
            card_w - Inches(0.2),
            Inches(0.6),
            name,
            font_size=11,
            color=WHITE,
            bold=True,
            align=PP_ALIGN.CENTER,
        )
        add_textbox(
            slide,
            x + Inches(0.1),
            y_cards + Inches(0.8),
            card_w - Inches(0.2),
            Inches(0.4),
            agent_id,
            font_size=9,
            color=color,
            align=PP_ALIGN.CENTER,
            font_name="Consolas",
        )

    # Reporting line note
    add_textbox(
        slide,
        Inches(0.5),
        Inches(4.3),
        Inches(9.0),
        Inches(0.4),
        "All committees report to the Board Chair. Human CEO reports directly to Board Chair.",
        font_size=11,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
    )
    add_page_number(slide, 3, TOTAL_SLIDES)


def build_slide_04_executive(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)
    add_title_bar(slide, "Executive Team", 1.8)

    # Human CEO (top center)
    add_shape_rect(slide, Inches(3.5), Inches(1.1), Inches(3.0), Inches(0.9), BG_CARD)
    add_accent_bar(slide, Inches(3.5), Inches(1.1), Inches(3.0), Inches(0.05), ACCENT_GOLD)
    add_textbox(
        slide,
        Inches(3.7),
        Inches(1.2),
        Inches(2.6),
        Inches(0.3),
        "Human CEO",
        font_size=16,
        color=ACCENT_GOLD,
        bold=True,
        align=PP_ALIGN.CENTER,
    )
    add_textbox(
        slide,
        Inches(3.7),
        Inches(1.55),
        Inches(2.6),
        Inches(0.3),
        "human_ceo",
        font_size=10,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
        font_name="Consolas",
    )

    # Chief of Staff
    add_shape_rect(slide, Inches(3.5), Inches(2.1), Inches(3.0), Inches(0.7), BG_CARD)
    add_accent_bar(slide, Inches(3.5), Inches(2.1), Inches(3.0), Inches(0.04), ACCENT)
    add_textbox(
        slide,
        Inches(3.7),
        Inches(2.15),
        Inches(2.6),
        Inches(0.3),
        "Chief of Staff (Orchestrator)",
        font_size=12,
        color=ACCENT,
        bold=True,
        align=PP_ALIGN.CENTER,
    )
    add_textbox(
        slide,
        Inches(3.7),
        Inches(2.45),
        Inches(2.6),
        Inches(0.25),
        "chief_of_staff",
        font_size=9,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
        font_name="Consolas",
    )

    # C-Suite row
    c_suite = [
        ("CTO", "cto", ACCENT),
        ("COO", "coo", ACCENT),
        ("CAIO", "caio", PURPLE),
        ("CPO", "cpo", BLUE),
        ("CMO", "cmo", ACCENT_GOLD),
        ("CHRO", "hr", ACCENT),
        ("CFO", "cfo", ACCENT_GOLD),
        ("CISO", "ciso", CORAL),
        ("CLO", "clo", BLUE),
        ("CSO", "cso", PURPLE),
    ]

    card_w = Inches(0.88)
    card_h = Inches(1.1)
    gap = Inches(0.06)
    start_x = Inches(0.3)
    y_exec = Inches(3.1)

    for i, (title, agent_id, color) in enumerate(c_suite):
        x = start_x + i * (card_w + gap)
        add_shape_rect(slide, x, y_exec, card_w, card_h, BG_CARD)
        add_accent_bar(slide, x, y_exec, card_w, Inches(0.04), color)
        add_textbox(
            slide,
            x + Inches(0.05),
            y_exec + Inches(0.1),
            card_w - Inches(0.1),
            Inches(0.3),
            title,
            font_size=13,
            color=WHITE,
            bold=True,
            align=PP_ALIGN.CENTER,
        )
        add_textbox(
            slide,
            x + Inches(0.05),
            y_exec + Inches(0.45),
            card_w - Inches(0.1),
            Inches(0.25),
            agent_id,
            font_size=8,
            color=color,
            align=PP_ALIGN.CENTER,
            font_name="Consolas",
        )

    # CEO Advisor (separate, right side)
    add_shape_rect(slide, Inches(8.5), Inches(1.1), Inches(1.3), Inches(0.7), BG_CARD_ALT)
    add_textbox(
        slide,
        Inches(8.55),
        Inches(1.15),
        Inches(1.2),
        Inches(0.3),
        "CEO Advisor",
        font_size=10,
        color=LIGHT_GRAY,
        bold=True,
        align=PP_ALIGN.CENTER,
    )
    add_textbox(
        slide,
        Inches(8.55),
        Inches(1.45),
        Inches(1.2),
        Inches(0.2),
        "advisor",
        font_size=8,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
        font_name="Consolas",
    )

    add_textbox(
        slide,
        Inches(0.5),
        Inches(4.5),
        Inches(9.0),
        Inches(0.35),
        "10 C-Suite executives  |  Chief of Staff orchestrates cross-functional work",
        font_size=11,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
    )
    add_page_number(slide, 4, TOTAL_SLIDES)


def build_slide_05_technology(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)
    add_title_bar(slide, "Technology Department (CTO)", 2.5)

    # VP Engineering card
    add_shape_rect(slide, Inches(0.5), Inches(1.1), Inches(2.8), Inches(0.7), BG_CARD)
    add_accent_bar(slide, Inches(0.5), Inches(1.1), Inches(2.8), Inches(0.04), ACCENT)
    add_textbox(
        slide,
        Inches(0.6),
        Inches(1.15),
        Inches(2.6),
        Inches(0.3),
        "VP of Engineering",
        font_size=13,
        color=WHITE,
        bold=True,
    )
    add_textbox(
        slide,
        Inches(0.6),
        Inches(1.45),
        Inches(2.6),
        Inches(0.25),
        "vp_engineering",
        font_size=9,
        color=ACCENT,
        font_name="Consolas",
    )

    # Sub-teams (3 columns)
    teams = [
        (
            "Platform & QA",
            ACCENT,
            [
                "DevOps Lead",
                "Platform Reliability Eng",
                "Audit Trail Owner",
                "Graph / Dashboard Owners",
                "QA Lead",
                "\u2192 Test Eng Lead",
                "\u2192 QA Automation Eng",
                "\u2192 Release Manager",
                "\u2192 QA Engineer",
            ],
        ),
        (
            "Engineering Leads",
            BLUE,
            [
                "Lead Backend Engineer",
                "\u2192 Senior Backend Eng",
                "\u2192 Backend Engineer",
                "\u2192 Full Stack Engineer",
                "Lead Frontend Engineer",
                "\u2192 Senior Frontend Eng",
                "\u2192 Frontend Engineer",
                "\u2192 Mobile Developer",
            ],
        ),
        (
            "Architecture & Data",
            PURPLE,
            [
                "Solution Architect",
                "Lead DevOps Engineer",
                "Platform / Frontend Arch",
                "API Architect",
                "Observability Engineer",
                "Scalability Architect",
                "Software / Cloud Architect",
                "CDO \u2192 Data Engineer",
                "Data Scientist / BI Engineer",
            ],
        ),
    ]

    col_w = Inches(3.0)
    col_gap = Inches(0.15)
    start_x = Inches(0.5)
    start_y = Inches(2.0)

    for i, (team_name, color, roles) in enumerate(teams):
        x = start_x + i * (col_w + col_gap)
        add_shape_rect(slide, x, start_y, col_w, Inches(3.2), BG_CARD)
        add_accent_bar(slide, x, start_y, col_w, Inches(0.04), color)
        add_textbox(
            slide,
            x + Inches(0.15),
            start_y + Inches(0.1),
            col_w - Inches(0.3),
            Inches(0.3),
            team_name,
            font_size=12,
            color=color,
            bold=True,
        )
        add_bullet_list(
            slide,
            x + Inches(0.15),
            start_y + Inches(0.4),
            col_w - Inches(0.3),
            Inches(2.7),
            roles,
            font_size=10,
            spacing=3,
            color=LIGHT_GRAY,
            bullet_color=color,
        )

    add_textbox(
        slide,
        Inches(0.5),
        Inches(5.2),
        Inches(9.0),
        Inches(0.3),
        "20+ specialists  |  VP Engineering, CDO, 3 Lead Engineers, 8+ Architects",
        font_size=10,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
    )
    add_page_number(slide, 5, TOTAL_SLIDES)


def build_slide_06_operations(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)
    add_title_bar(slide, "Operations Department (COO)", 2.5)

    roles = [
        ("Workflow Owner", "Core operations workflows"),
        ("Orchestration Owner", "Agent orchestration systems"),
        ("Doctor Owner", "System health & diagnostics"),
        ("Decision Engine Owner", "Automated decision pipelines"),
        ("Memory Owner", "Memory & knowledge systems"),
        ("Audit Trail Owner", "Audit logging & compliance"),
        ("Capacity Planner", "Resource capacity planning"),
        ("Business Continuity Mgr", "Disaster recovery & BCP"),
        ("Vendor Manager", "Third-party vendor relations"),
        ("Process Quality Mgr", "Process improvement & QA"),
        ("SOP Owner", "Standard operating procedures"),
        ("Program Manager", "Cross-functional programs"),
        ("Knowledge Manager", "Knowledge base management"),
    ]

    col_w = Inches(4.4)
    col_gap = Inches(0.2)
    card_h = Inches(0.3)
    card_gap = Inches(0.05)
    start_y = Inches(1.1)

    for i, (role, desc) in enumerate(roles):
        col = i % 2
        row = i // 2
        x = Inches(0.5) + col * (col_w + col_gap)
        y = start_y + row * (card_h + card_gap)

        add_shape_rect(slide, x, y, col_w, card_h, BG_CARD)
        add_accent_bar(slide, x, y, Inches(0.05), card_h, ACCENT)
        add_textbox(
            slide,
            x + Inches(0.15),
            y + Inches(0.02),
            Inches(2.2),
            Inches(0.25),
            role,
            font_size=11,
            color=WHITE,
            bold=True,
        )
        add_textbox(
            slide,
            x + Inches(2.4),
            y + Inches(0.02),
            Inches(1.9),
            Inches(0.25),
            desc,
            font_size=9,
            color=MID_GRAY,
        )

    add_textbox(
        slide,
        Inches(0.5),
        Inches(5.0),
        Inches(9.0),
        Inches(0.3),
        "13 specialists  |  Full operational lifecycle coverage",
        font_size=11,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
    )
    add_page_number(slide, 6, TOTAL_SLIDES)


def build_slide_07_ai_research(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)
    add_title_bar(slide, "AI Research Department (CAIO)", 2.5)

    # Main roles
    left_roles = [
        "ML Engineer",
        "ML Services Owner",
        "Memory Owner",
        "LLM Platform Owner",
        "Eval Benchmarks Engineer",
        "Prompt Engineer",
        "MLOps Engineer",
    ]

    # AI Safety sub-team
    safety_roles = [
        "AI Safety Lead",
        "\u2192 Red Team Engineer",
        "\u2192 Constitutional AI Owner",
        "\u2192 AI Ethics Officer",
        "\u2192 Human-AI Interaction Designer",
    ]

    # Left panel
    add_shape_rect(slide, Inches(0.5), Inches(1.1), Inches(4.3), Inches(3.5), BG_CARD)
    add_accent_bar(slide, Inches(0.5), Inches(1.1), Inches(4.3), Inches(0.04), PURPLE)
    add_textbox(
        slide,
        Inches(0.7),
        Inches(1.2),
        Inches(3.0),
        Inches(0.3),
        "Core AI Research",
        font_size=13,
        color=PURPLE,
        bold=True,
    )
    add_bullet_list(
        slide,
        Inches(0.7),
        Inches(1.55),
        Inches(3.9),
        Inches(2.8),
        left_roles,
        font_size=12,
        spacing=6,
        bullet_color=PURPLE,
    )

    # Right panel - Safety sub-team
    add_shape_rect(slide, Inches(5.0), Inches(1.1), Inches(4.5), Inches(2.5), BG_CARD)
    add_accent_bar(slide, Inches(5.0), Inches(1.1), Inches(4.5), Inches(0.04), CORAL)
    add_textbox(
        slide,
        Inches(5.2),
        Inches(1.2),
        Inches(3.0),
        Inches(0.3),
        "AI Safety Sub-Team",
        font_size=13,
        color=CORAL,
        bold=True,
    )
    add_bullet_list(
        slide,
        Inches(5.2),
        Inches(1.55),
        Inches(4.1),
        Inches(1.8),
        safety_roles,
        font_size=11,
        spacing=5,
        bullet_color=CORAL,
    )

    add_textbox(
        slide,
        Inches(0.5),
        Inches(4.8),
        Inches(9.0),
        Inches(0.3),
        "10 specialists  |  ML, LLM Platform, Safety, Ethics, and MLOps",
        font_size=11,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
    )
    add_page_number(slide, 7, TOTAL_SLIDES)


def build_slide_08_product(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)
    add_title_bar(slide, "Product Department (CPO)", 2.0)

    roles = [
        ("UX Research Lead", "User research & insights"),
        ("UX Analytics Lead", "Usage analytics & metrics"),
        ("Technical Documentation", "Docs & knowledge base"),
        ("Growth Product Manager", "Growth experiments"),
        ("Developer Experience Eng", "DX tooling & workflows"),
        ("Product Designer", "UI/UX design"),
        ("Product Owner", "Backlog & priorities"),
        ("Technical Writer", "Technical content"),
    ]

    card_w = Inches(4.3)
    card_h = Inches(0.45)
    col_gap = Inches(0.3)

    for i, (role, desc) in enumerate(roles):
        col = i % 2
        row = i // 2
        x = Inches(0.5) + col * (card_w + col_gap)
        y = Inches(1.15) + row * (card_h + Inches(0.08))

        add_shape_rect(slide, x, y, card_w, card_h, BG_CARD)
        add_accent_bar(slide, x, y, Inches(0.05), card_h, BLUE)
        add_textbox(
            slide,
            x + Inches(0.15),
            y + Inches(0.05),
            Inches(2.3),
            Inches(0.3),
            role,
            font_size=12,
            color=WHITE,
            bold=True,
        )
        add_textbox(
            slide,
            x + Inches(2.5),
            y + Inches(0.05),
            Inches(1.7),
            Inches(0.3),
            desc,
            font_size=10,
            color=MID_GRAY,
        )

    add_textbox(
        slide,
        Inches(0.5),
        Inches(4.6),
        Inches(9.0),
        Inches(0.3),
        "8 specialists  |  UX, Growth, Documentation, and Design",
        font_size=11,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
    )
    add_page_number(slide, 8, TOTAL_SLIDES)


def build_slide_09_marketing(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)
    add_title_bar(slide, "Marketing Department (CMO)", 2.0)

    roles = [
        ("Marketing Owner", "Marketing strategy & ops"),
        ("Head of Developer Relations", "Dev community & advocacy"),
        ("Product Marketing Manager", "Go-to-market & positioning"),
        ("Industry Analyst Relations", "Analyst briefings & IR"),
        ("Content Writer", "Written content production"),
        ("Content Creator", "Visual & multimedia content"),
        ("Growth Hacker", "Growth experiments & hacks"),
    ]

    card_w = Inches(4.3)
    card_h = Inches(0.45)
    col_gap = Inches(0.3)

    for i, (role, desc) in enumerate(roles):
        col = i % 2
        row = i // 2
        x = Inches(0.5) + col * (card_w + col_gap)
        y = Inches(1.15) + row * (card_h + Inches(0.08))

        add_shape_rect(slide, x, y, card_w, card_h, BG_CARD)
        add_accent_bar(slide, x, y, Inches(0.05), card_h, ACCENT_GOLD)
        add_textbox(
            slide,
            x + Inches(0.15),
            y + Inches(0.05),
            Inches(2.5),
            Inches(0.3),
            role,
            font_size=12,
            color=WHITE,
            bold=True,
        )
        add_textbox(
            slide,
            x + Inches(2.7),
            y + Inches(0.05),
            Inches(1.5),
            Inches(0.3),
            desc,
            font_size=10,
            color=MID_GRAY,
        )

    add_textbox(
        slide,
        Inches(0.5),
        Inches(4.5),
        Inches(9.0),
        Inches(0.3),
        "7 specialists  |  Content, DevRel, Product Marketing, Growth",
        font_size=11,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
    )
    add_page_number(slide, 9, TOTAL_SLIDES)


def build_slide_10_people(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)
    add_title_bar(slide, "People Department (CHRO)", 1.8)

    roles = [
        ("HR Owner", "HR operations & policy"),
        ("Learning & Development Lead", "Training & upskilling programs"),
        ("Employee Experience Lead", "Engagement & retention"),
        ("Culture & Values Officer", "Culture & DEI initiatives"),
        ("Recruiter", "Talent acquisition"),
    ]

    card_w = Inches(8.5)
    card_h = Inches(0.55)
    start_y = Inches(1.2)

    for i, (role, desc) in enumerate(roles):
        y = start_y + i * (card_h + Inches(0.1))
        add_shape_rect(slide, Inches(0.75), y, card_w, card_h, BG_CARD)
        add_accent_bar(slide, Inches(0.75), y, Inches(0.05), card_h, ACCENT)
        add_textbox(
            slide,
            Inches(1.0),
            y + Inches(0.08),
            Inches(3.5),
            Inches(0.35),
            role,
            font_size=14,
            color=WHITE,
            bold=True,
        )
        add_textbox(
            slide,
            Inches(4.8),
            y + Inches(0.08),
            Inches(4.0),
            Inches(0.35),
            desc,
            font_size=12,
            color=MID_GRAY,
        )

    add_textbox(
        slide,
        Inches(0.5),
        Inches(4.8),
        Inches(9.0),
        Inches(0.3),
        "5 specialists  |  HR, L&D, Culture, Employee Experience",
        font_size=11,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
    )
    add_page_number(slide, 10, TOTAL_SLIDES)


def build_slide_11_security(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)
    add_title_bar(slide, "Security Department (CISO)", 2.0)

    # Main roles
    main_roles = [
        "Security Architect",
        "AI Security Specialist",
        "Penetration Testing Lead",
        "Incident Response Lead",
        "DevSecOps Lead",
        "Supply Chain Security Eng",
        "Threat Intelligence Analyst",
    ]

    # Compliance sub-team
    compliance_roles = [
        "Security & Compliance Lead",
        "\u2192 SOC 2 Audit Readiness Analyst",
    ]

    # Left panel
    add_shape_rect(slide, Inches(0.5), Inches(1.1), Inches(5.5), Inches(3.4), BG_CARD)
    add_accent_bar(slide, Inches(0.5), Inches(1.1), Inches(5.5), Inches(0.04), CORAL)
    add_textbox(
        slide,
        Inches(0.7),
        Inches(1.2),
        Inches(3.0),
        Inches(0.3),
        "Core Security",
        font_size=13,
        color=CORAL,
        bold=True,
    )
    add_bullet_list(
        slide,
        Inches(0.7),
        Inches(1.55),
        Inches(5.1),
        Inches(2.8),
        main_roles,
        font_size=12,
        spacing=6,
        bullet_color=CORAL,
    )

    # Right panel - Compliance
    add_shape_rect(slide, Inches(6.2), Inches(1.1), Inches(3.3), Inches(1.5), BG_CARD)
    add_accent_bar(slide, Inches(6.2), Inches(1.1), Inches(3.3), Inches(0.04), ACCENT_GOLD)
    add_textbox(
        slide,
        Inches(6.4),
        Inches(1.2),
        Inches(2.5),
        Inches(0.3),
        "Compliance Sub-Team",
        font_size=12,
        color=ACCENT_GOLD,
        bold=True,
    )
    add_bullet_list(
        slide,
        Inches(6.4),
        Inches(1.55),
        Inches(2.9),
        Inches(0.8),
        compliance_roles,
        font_size=11,
        spacing=5,
        bullet_color=ACCENT_GOLD,
    )

    add_textbox(
        slide,
        Inches(0.5),
        Inches(4.8),
        Inches(9.0),
        Inches(0.3),
        "8 specialists  |  Security architecture, pen testing, compliance, threat intel",
        font_size=11,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
    )
    add_page_number(slide, 11, TOTAL_SLIDES)


def build_slide_12_strategy(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)
    add_title_bar(slide, "Strategy Department (CSO)", 1.8)

    roles = [
        ("Head of Competitive Intelligence", "Market & competitor analysis"),
        ("Corporate Development Lead", "M&A and partnerships"),
        ("Revenue Operations Analyst", "RevOps & pipeline analytics"),
        ("Solutions Engineer", "Technical sales solutions"),
        ("Market Analyst", "Market research & trends"),
    ]

    card_w = Inches(8.5)
    card_h = Inches(0.55)
    start_y = Inches(1.2)

    for i, (role, desc) in enumerate(roles):
        y = start_y + i * (card_h + Inches(0.1))
        add_shape_rect(slide, Inches(0.75), y, card_w, card_h, BG_CARD)
        add_accent_bar(slide, Inches(0.75), y, Inches(0.05), card_h, PURPLE)
        add_textbox(
            slide,
            Inches(1.0),
            y + Inches(0.08),
            Inches(3.8),
            Inches(0.35),
            role,
            font_size=14,
            color=WHITE,
            bold=True,
        )
        add_textbox(
            slide,
            Inches(5.0),
            y + Inches(0.08),
            Inches(4.0),
            Inches(0.35),
            desc,
            font_size=12,
            color=MID_GRAY,
        )

    add_textbox(
        slide,
        Inches(0.5),
        Inches(4.8),
        Inches(9.0),
        Inches(0.3),
        "5 specialists  |  Competitive intelligence, corp dev, RevOps, market analysis",
        font_size=11,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
    )
    add_page_number(slide, 12, TOTAL_SLIDES)


def build_slide_13_sales_cs(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)
    add_title_bar(slide, "Sales & Customer Success", 2.5)

    # Sales column
    add_shape_rect(slide, Inches(0.5), Inches(1.1), Inches(4.3), Inches(3.2), BG_CARD)
    add_accent_bar(slide, Inches(0.5), Inches(1.1), Inches(4.3), Inches(0.04), ACCENT_GOLD)
    add_textbox(
        slide,
        Inches(0.7),
        Inches(1.2),
        Inches(3.0),
        Inches(0.3),
        "Sales",
        font_size=15,
        color=ACCENT_GOLD,
        bold=True,
    )

    sales_roles = [
        "Head of Sales",
        "\u2192 Sales Owner",
        "\u2192 Business Developer",
    ]
    add_bullet_list(
        slide,
        Inches(0.7),
        Inches(1.6),
        Inches(3.9),
        Inches(1.5),
        sales_roles,
        font_size=13,
        spacing=8,
        bullet_color=ACCENT_GOLD,
    )

    # Customer Success column
    add_shape_rect(slide, Inches(5.1), Inches(1.1), Inches(4.4), Inches(3.2), BG_CARD)
    add_accent_bar(slide, Inches(5.1), Inches(1.1), Inches(4.4), Inches(0.04), ACCENT)
    add_textbox(
        slide,
        Inches(5.3),
        Inches(1.2),
        Inches(3.0),
        Inches(0.3),
        "Customer Success",
        font_size=15,
        color=ACCENT,
        bold=True,
    )

    cs_roles = [
        "Head of Customer Success",
        "\u2192 Customer Success Owner",
        "\u2192 Support Agent",
    ]
    add_bullet_list(
        slide,
        Inches(5.3),
        Inches(1.6),
        Inches(4.0),
        Inches(1.5),
        cs_roles,
        font_size=13,
        spacing=8,
        bullet_color=ACCENT,
    )

    add_textbox(
        slide,
        Inches(0.5),
        Inches(4.8),
        Inches(9.0),
        Inches(0.3),
        "5 agents  |  Sales pipeline + Customer retention & support",
        font_size=11,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
    )
    add_page_number(slide, 13, TOTAL_SLIDES)


def build_slide_14_finance_legal(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)
    add_title_bar(slide, "Finance & Legal", 1.8)

    # Finance column
    add_shape_rect(slide, Inches(0.5), Inches(1.1), Inches(4.3), Inches(3.0), BG_CARD)
    add_accent_bar(slide, Inches(0.5), Inches(1.1), Inches(4.3), Inches(0.04), ACCENT_GOLD)
    add_textbox(
        slide,
        Inches(0.7),
        Inches(1.2),
        Inches(3.0),
        Inches(0.3),
        "Finance (CFO)",
        font_size=14,
        color=ACCENT_GOLD,
        bold=True,
    )

    finance_roles = [
        "Financial Analyst",
        "Investor Relations Lead",
    ]
    add_bullet_list(
        slide,
        Inches(0.7),
        Inches(1.6),
        Inches(3.9),
        Inches(1.2),
        finance_roles,
        font_size=12,
        spacing=6,
        bullet_color=ACCENT_GOLD,
    )

    # Legal column
    add_shape_rect(slide, Inches(5.1), Inches(1.1), Inches(4.4), Inches(3.0), BG_CARD)
    add_accent_bar(slide, Inches(5.1), Inches(1.1), Inches(4.4), Inches(0.04), BLUE)
    add_textbox(
        slide,
        Inches(5.3),
        Inches(1.2),
        Inches(3.0),
        Inches(0.3),
        "Legal (CLO + Legal Advisor)",
        font_size=14,
        color=BLUE,
        bold=True,
    )

    legal_roles = [
        "Compliance Officer (CLO)",
        "Data Privacy Officer (CLO)",
        "Legal Owner (Legal Advisor)",
        "Compliance Officer (Legal Advisor)",
    ]
    add_bullet_list(
        slide,
        Inches(5.3),
        Inches(1.6),
        Inches(4.0),
        Inches(1.5),
        legal_roles,
        font_size=12,
        spacing=6,
        bullet_color=BLUE,
    )

    add_textbox(
        slide,
        Inches(0.5),
        Inches(4.6),
        Inches(9.0),
        Inches(0.3),
        "6 agents  |  CFO (2 specialists) + CLO (2) + Legal Advisor (2)",
        font_size=11,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
    )
    add_page_number(slide, 14, TOTAL_SLIDES)


def build_slide_15_data_it(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)
    add_title_bar(slide, "Data & IT", 1.5)

    # Data column (CDO)
    add_shape_rect(slide, Inches(0.5), Inches(1.1), Inches(4.3), Inches(3.0), BG_CARD)
    add_accent_bar(slide, Inches(0.5), Inches(1.1), Inches(4.3), Inches(0.04), PURPLE)
    add_textbox(
        slide,
        Inches(0.7),
        Inches(1.2),
        Inches(3.0),
        Inches(0.3),
        "Data (CDO)",
        font_size=14,
        color=PURPLE,
        bold=True,
    )

    data_roles = [
        "Data Engineer",
        "Data Scientist",
        "Business Intelligence Engineer",
    ]
    add_bullet_list(
        slide,
        Inches(0.7),
        Inches(1.6),
        Inches(3.9),
        Inches(1.2),
        data_roles,
        font_size=12,
        spacing=6,
        bullet_color=PURPLE,
    )

    # IT column (CIO)
    add_shape_rect(slide, Inches(5.1), Inches(1.1), Inches(4.4), Inches(3.0), BG_CARD)
    add_accent_bar(slide, Inches(5.1), Inches(1.1), Inches(4.4), Inches(0.04), MID_GRAY)
    add_textbox(
        slide,
        Inches(5.3),
        Inches(1.2),
        Inches(3.0),
        Inches(0.3),
        "IT (CIO)",
        font_size=14,
        color=MID_GRAY,
        bold=True,
    )

    add_textbox(
        slide,
        Inches(5.3),
        Inches(1.7),
        Inches(3.8),
        Inches(0.8),
        "CIO \u2014 No direct reports yet\nInfrastructure and IT services placeholder",
        font_size=12,
        color=LIGHT_GRAY,
    )

    add_textbox(
        slide,
        Inches(0.5),
        Inches(4.6),
        Inches(9.0),
        Inches(0.3),
        "3 data specialists  |  CIO role established, reports pending",
        font_size=11,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
    )
    add_page_number(slide, 15, TOTAL_SLIDES)


def build_slide_16_summary(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)

    add_accent_bar(slide, Inches(0), Inches(0), SLIDE_W, Inches(0.06))

    add_shape_rect(slide, Inches(1.5), Inches(0.8), Inches(7.0), Inches(4.0), BG_CARD)
    add_accent_bar(slide, Inches(1.5), Inches(0.8), Inches(7.0), Inches(0.05), ACCENT)

    add_textbox(
        slide,
        Inches(2.0),
        Inches(1.2),
        Inches(6.0),
        Inches(0.8),
        "127 Agents.",
        font_size=38,
        color=WHITE,
        bold=True,
        align=PP_ALIGN.CENTER,
        font_name="Georgia",
    )

    add_textbox(
        slide,
        Inches(2.0),
        Inches(1.9),
        Inches(6.0),
        Inches(0.5),
        "17 Departments.",
        font_size=28,
        color=ACCENT,
        align=PP_ALIGN.CENTER,
        font_name="Georgia",
    )

    add_accent_bar(slide, Inches(4.2), Inches(2.45), Inches(1.6), Inches(0.04))

    add_textbox(
        slide,
        Inches(2.0),
        Inches(2.65),
        Inches(6.0),
        Inches(0.5),
        "One Mission.",
        font_size=28,
        color=ACCENT_GOLD,
        align=PP_ALIGN.CENTER,
        font_name="Georgia",
    )

    add_textbox(
        slide,
        Inches(2.0),
        Inches(3.4),
        Inches(6.0),
        Inches(0.4),
        "Building the Future of Work with AI",
        font_size=16,
        color=LIGHT_GRAY,
        align=PP_ALIGN.CENTER,
    )

    add_textbox(
        slide,
        Inches(2.0),
        Inches(3.9),
        Inches(6.0),
        Inches(0.3),
        "Light Speed Holdings  |  v0.3.0",
        font_size=13,
        color=MID_GRAY,
        align=PP_ALIGN.CENTER,
    )

    add_accent_bar(slide, Inches(0), Inches(5.565), SLIDE_W, Inches(0.06))
    add_page_number(slide, 16, TOTAL_SLIDES)


# ── Main ────────────────────────────────────────────────────────────[...]


def main():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    builders = [
        build_slide_01_title,
        build_slide_02_overview,
        build_slide_03_board,
        build_slide_04_executive,
        build_slide_05_technology,
        build_slide_06_operations,
        build_slide_07_ai_research,
        build_slide_08_product,
        build_slide_09_marketing,
        build_slide_10_people,
        build_slide_11_security,
        build_slide_12_strategy,
        build_slide_13_sales_cs,
        build_slide_14_finance_legal,
        build_slide_15_data_it,
        build_slide_16_summary,
    ]

    for builder in builders:
        builder(prs)

    output_dir = Path(__file__).parent
    output_path = output_dir / "light-speed-holdings-hierarchy.pptx"
    output_dir.mkdir(parents=True, exist_ok=True)

    prs.save(str(output_path))
    print(f"Presentation saved to: {output_path.resolve()}")
    print(f"  {len(prs.slides)} slides generated")
    print("  Theme: Dark blue executive")
    print("  Layout: 16:9")
    print("  Content: 127 agents, 17 departments, full hierarchy")


if __name__ == "__main__":
    main()
