# ─────────────────────────────────────────────────────────────
# VillageReach CHOICE Project – USSD Consultant Proposal (PPTX)
# Companion deck for financial proposal presentation
# ─────────────────────────────────────────────────────────────

from contextlib import suppress
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

_ALIGN_MAP = {0: PP_ALIGN.LEFT, 1: PP_ALIGN.CENTER, 2: PP_ALIGN.RIGHT}

OUT = Path("VillageReach-USSD-Consultant-Proposal-Slides.pptx")

# Last updated: 2026-09-18
# ── Palette ──────────────────────────────────────────────────
TEAL = RGBColor(0x1C, 0x6B, 0x6B)
DARK = RGBColor(0x10, 0x18, 0x20)
CORAL = RGBColor(0xE8, 0x4D, 0x4D)
GREY = RGBColor(0x6B, 0x70, 0x80)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LTGREY = RGBColor(0xF5, 0xF5, 0xF5)
LTCYAN = RGBColor(0xE6, 0xF4, 0xF1)
GREEN = RGBColor(0x2E, 0x7D, 0x32)
AMBER = RGBColor(0xF5, 0x7F, 0x17)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def _apply(run, size=14, bold=False, italic=False, color=DARK, name="Calibri"):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = name


def _text_box(
    slide,
    left,
    top,
    width,
    height,
    text,
    size=14,
    bold=False,
    italic=False,
    color=DARK,
    align=1,
    anchor=1,
    name="Calibri",
):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    p = tf.paragraphs[0]
    if isinstance(align, int):
        align = _ALIGN_MAP.get(align, PP_ALIGN.LEFT)
    p.alignment = align
    run = p.add_run()
    run.text = text
    _apply(run, size=size, bold=bold, italic=italic, color=color, name=name)
    with suppress(AttributeError, ValueError, NotImplementedError):
        tf.vertical_anchor = anchor
    return txBox


def box(slide, left, top, width, height, bg=WHITE, line_color=None, line_w=1):
    shape = slide.shapes.add_shape(
        1,
        left,
        top,
        width,
        height,  # MSO_SHAPE_TYPE.RECTANGLE
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_w)
    else:
        shape.line.fill.background()
    return shape


def _add_bullet_list(tf, items, size=11, color=DARK, bold_prefixes=True, name="Calibri"):
    for i, item in enumerate(items):
        p = tf.add_paragraph() if i > 0 or tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(4)
        p.space_before = Pt(2)
        run = p.add_run()
        run.text = f"  •  {item}"
        _apply(run, size=size, color=color, name=name)


# ─────────────────────────────────────────────────────────────
# BUILD
# ─────────────────────────────────────────────────────────────


def build():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    # ── Slide 1: Title ──────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box(slide, Inches(0), Inches(0), SLIDE_W, SLIDE_H, bg=TEAL)
    # Accent bar
    box(slide, Inches(0), Inches(3.1), SLIDE_W, Inches(0.06), bg=CORAL)

    _text_box(
        slide,
        Inches(1.5),
        Inches(1.4),
        Inches(10),
        Inches(1),
        "VillageReach",
        size=40,
        bold=True,
        color=WHITE,
        align=1,
    )
    _text_box(
        slide,
        Inches(1.5),
        Inches(2.3),
        Inches(10),
        Inches(0.7),
        "CHOICE Project – USSD Health Messaging Consultant",
        size=20,
        color=WHITE,
        align=1,
    )
    _text_box(
        slide,
        Inches(1.5),
        Inches(3.5),
        Inches(10),
        Inches(0.5),
        "Financial Proposal & Technical Approach",
        size=16,
        bold=True,
        color=LTCYAN,
        align=1,
    )
    _text_box(
        slide,
        Inches(1.5),
        Inches(5.5),
        Inches(10),
        Inches(0.4),
        "Prepared by Light Speed Holdings  |  September 2026  |  Last updated: 2026-09-18",
        size=12,
        color=WHITE,
        align=1,
    )
    _text_box(
        slide,
        Inches(1.5),
        Inches(6.0),
        Inches(10),
        Inches(0.4),
        "Malawi  ·  Nairobi  ·  Washington DC",
        size=11,
        color=LTCYAN,
        align=1,
    )
    _text_box(
        slide,
        Inches(1.5),
        Inches(6.5),
        Inches(10),
        Inches(0.3),
        "Confidential – For VillageReach Evaluation Use Only",
        size=10,
        italic=True,
        color=CORAL,
        align=1,
    )

    # ── Slide 2: Agenda ─────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box(slide, Inches(0), Inches(0), SLIDE_W, Inches(1.1), bg=TEAL)
    _text_box(
        slide,
        Inches(0.8),
        Inches(0.2),
        Inches(11),
        Inches(0.7),
        "Agenda",
        size=28,
        bold=True,
        color=WHITE,
        align=0,
    )

    agenda_items = [
        ("01", "Executive Summary & Value Proposition"),
        ("02", "Understanding of Requirements"),
        ("03", "Technical Approach & USSD Architecture"),
        ("04", "Team Composition"),
        ("05", "Project Timeline & Milestones"),
        ("06", "Budget & Financial Proposal"),
        ("07", "Data Privacy & Security"),
        ("08", "Next Steps"),
    ]
    y = 1.5
    for num, title in agenda_items:
        box(slide, Inches(1), Inches(y), Inches(0.7), Inches(0.55), bg=TEAL)
        _text_box(
            slide,
            Inches(1.05),
            Inches(y + 0.05),
            Inches(0.6),
            Inches(0.45),
            num,
            size=14,
            bold=True,
            color=WHITE,
            align=1,
        )
        _text_box(
            slide,
            Inches(1.9),
            Inches(y + 0.05),
            Inches(9),
            Inches(0.45),
            title,
            size=14,
            color=DARK,
            align=0,
        )
        y += 0.7

    # ── Slide 3: Executive Summary ──────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box(slide, Inches(0), Inches(0), SLIDE_W, Inches(1.1), bg=TEAL)
    _text_box(
        slide,
        Inches(0.8),
        Inches(0.2),
        Inches(11),
        Inches(0.7),
        "Executive Summary",
        size=28,
        bold=True,
        color=WHITE,
        align=0,
    )

    # Left column: The Ask
    box(
        slide,
        Inches(0.8),
        Inches(1.5),
        Inches(5.5),
        Inches(5.2),
        bg=LTGREY,
        line_color=RGBColor(0xDD, 0xDD, 0xDD),
    )
    _text_box(
        slide,
        Inches(1.1),
        Inches(1.7),
        Inches(5),
        Inches(0.5),
        "The Engagement",
        size=16,
        bold=True,
        color=TEAL,
        align=0,
    )
    tf = _text_box(
        slide, Inches(1.1), Inches(2.3), Inches(5), Inches(4), "", size=11, color=DARK, align=0
    )
    _add_bullet_list(
        tf.text_frame,
        [
            "USSD health messaging service on short code 54747",
            "TNM and Airtel networks in Malawi",
            "Chichewa-language content for women in Balaka & Lilongwe",
            "4-week technical setup + 24-month maintenance",
            "CHOICE Project (Global Affairs Canada / Oxfam Canada)",
        ],
        size=11,
    )

    # Right column: Why Us
    box(
        slide,
        Inches(6.7),
        Inches(1.5),
        Inches(5.8),
        Inches(5.2),
        bg=LTCYAN,
        line_color=RGBColor(0xBB, 0xDD, 0xDD),
    )
    _text_box(
        slide,
        Inches(7),
        Inches(1.7),
        Inches(5.2),
        Inches(0.5),
        "Why Light Speed Holdings",
        size=16,
        bold=True,
        color=TEAL,
        align=0,
    )
    tf = _text_box(
        slide, Inches(7), Inches(2.3), Inches(5.2), Inches(4), "", size=11, color=DARK, align=0
    )
    _add_bullet_list(
        tf.text_frame,
        [
            "Proven USSD & mobile health deployments in Malawi",
            "Full-stack team: developers, UX researchers, integration engineers",
            "Local Malawi presence with international standards",
            "Single accountable partner—no subcontracting",
            "Value for money: milestone-based payments",
        ],
        size=11,
    )

    # ── Slide 4: Requirements Understanding ─────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box(slide, Inches(0), Inches(0), SLIDE_W, Inches(1.1), bg=TEAL)
    _text_box(
        slide,
        Inches(0.8),
        Inches(0.2),
        Inches(11),
        Inches(0.7),
        "Understanding of Requirements",
        size=28,
        bold=True,
        color=WHITE,
        align=0,
    )

    # Core deliverables
    _text_box(
        slide,
        Inches(0.8),
        Inches(1.4),
        Inches(11),
        Inches(0.5),
        "Core Deliverables",
        size=16,
        bold=True,
        color=TEAL,
        align=0,
    )

    deliverables = [
        (
            "USSD Menu Design & Deploy",
            "Short code 54747 (TNM + Airtel)\nChichewa-language menus\n≤182 chars/screen, ≤4 levels deep",
        ),
        (
            "User Acceptance Testing",
            "Minimum 20 participants\nBalaka & Lilongwe districts\nLow-literacy user validation",
        ),
        (
            "Data Pipeline Integration",
            "REST API to VillageReach systems\nMonthly uptime & usage reports\n≥99% availability target",
        ),
        (
            "Training & Handover",
            "Documentation for VillageReach staff\n24-month support commitment\nCompletion report at engagement end",
        ),
    ]
    x_positions = [0.8, 3.7, 6.6, 9.5]
    for i, (title, desc) in enumerate(deliverables):
        x = Inches(x_positions[i])
        box(
            slide,
            x,
            Inches(2.0),
            Inches(2.7),
            Inches(4.5),
            bg=LTGREY,
            line_color=RGBColor(0xDD, 0xDD, 0xDD),
        )
        box(slide, x, Inches(2.0), Inches(2.7), Inches(0.06), bg=CORAL)
        _text_box(
            slide,
            x + Inches(0.2),
            Inches(2.2),
            Inches(2.3),
            Inches(0.5),
            title,
            size=12,
            bold=True,
            color=TEAL,
            align=0,
        )
        _text_box(
            slide,
            x + Inches(0.2),
            Inches(2.8),
            Inches(2.3),
            Inches(3.5),
            desc,
            size=10,
            color=DARK,
            align=0,
        )

    # ── Slide 5: Technical Approach ──────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box(slide, Inches(0), Inches(0), SLIDE_W, Inches(1.1), bg=TEAL)
    _text_box(
        slide,
        Inches(0.8),
        Inches(0.2),
        Inches(11),
        Inches(0.7),
        "Technical Approach – 4-Phase Methodology",
        size=28,
        bold=True,
        color=WHITE,
        align=0,
    )

    phases = [
        (
            "Phase 1",
            "Discovery & Design",
            "Week 1",
            "Stakeholder interviews\nContent architecture\nWireframe development\nTechnical architecture",
            TEAL,
        ),
        (
            "Phase 2",
            "Build & Test",
            "Weeks 2–3",
            "USSD application dev\nREST API implementation\nInternal QA\nPerformance testing",
            RGBColor(0x0D, 0x47, 0x47),
        ),
        (
            "Phase 3",
            "UAT & Launch",
            "Week 4",
            "UAT with 20+ users\nIterative refinement\nProduction deployment\nGo-live monitoring",
            RGBColor(0x1C, 0x6B, 0x6B),
        ),
        (
            "Phase 4",
            "Maintain & Report",
            "Months 2–24",
            "Monthly reports\nContent updates\nBug fixes & optimization\nCompletion report",
            RGBColor(0x2E, 0x7D, 0x32),
        ),
    ]

    for i, (phase, title, duration, desc, bg) in enumerate(phases):
        x = Inches(0.8 + i * 3.1)
        # Phase card
        box(slide, x, Inches(1.5), Inches(2.8), Inches(5.2), bg=bg)
        _text_box(
            slide,
            x + Inches(0.2),
            Inches(1.7),
            Inches(2.4),
            Inches(0.4),
            phase,
            size=12,
            bold=True,
            color=LTCYAN,
            align=0,
        )
        _text_box(
            slide,
            x + Inches(0.2),
            Inches(2.1),
            Inches(2.4),
            Inches(0.5),
            title,
            size=16,
            bold=True,
            color=WHITE,
            align=0,
        )
        _text_box(
            slide,
            x + Inches(0.2),
            Inches(2.7),
            Inches(2.4),
            Inches(0.4),
            duration,
            size=11,
            italic=True,
            color=LTCYAN,
            align=0,
        )
        _text_box(
            slide,
            x + Inches(0.2),
            Inches(3.3),
            Inches(2.4),
            Inches(3),
            desc,
            size=11,
            color=WHITE,
            align=0,
        )

    # ── Slide 6: USSD Menu Wireframe ────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box(slide, Inches(0), Inches(0), SLIDE_W, Inches(1.1), bg=TEAL)
    _text_box(
        slide,
        Inches(0.8),
        Inches(0.2),
        Inches(11),
        Inches(0.7),
        "USSD Menu Wireframe – Short Code 54747",
        size=28,
        bold=True,
        color=WHITE,
        align=0,
    )

    # Simulate USSD screens
    screens = [
        (
            "Main Menu",
            "Welcome to CHOICE\n1. Thanzi la thanzi\n2. Kukhala ndi moyo\n3. Ubwenzi bwino\n4. Zambiri\n99. Main Menu",
            0.8,
        ),
        (
            "1. Thanzi la thanzi",
            "Thanzi la thanzi\n1. Thanzi la amai\n2. Thanzi la ana\n3. Matenda osowa\n4. Mphamvu ya chakudya\n99. Main Menu",
            3.9,
        ),
        (
            "1.1 Thanzi la amai",
            "Kukhala ndi moyo wa thanzi:\n• Kusamba pochapa\n• Kudya zakudya zoyenera\n• Kuchita masewera\n99. Main Menu",
            7.0,
        ),
    ]

    for title, content, x_pos in screens:
        x = Inches(x_pos)
        # Phone frame
        box(
            slide,
            x,
            Inches(1.5),
            Inches(2.5),
            Inches(4.5),
            bg=DARK,
            line_color=RGBColor(0x44, 0x44, 0x44),
            line_w=2,
        )
        # Screen
        box(
            slide,
            x + Inches(0.15),
            Inches(1.7),
            Inches(2.2),
            Inches(3.8),
            bg=RGBColor(0x00, 0x33, 0x00),
        )
        _text_box(
            slide,
            x + Inches(0.25),
            Inches(1.8),
            Inches(2),
            Inches(0.3),
            title,
            size=9,
            bold=True,
            color=RGBColor(0x00, 0xFF, 0x00),
            align=0,
        )
        _text_box(
            slide,
            x + Inches(0.25),
            Inches(2.2),
            Inches(2),
            Inches(3),
            content,
            size=9,
            color=RGBColor(0x00, 0xFF, 0x00),
            align=0,
        )

    # Arrow connectors
    _text_box(
        slide,
        Inches(3.3),
        Inches(3.5),
        Inches(0.6),
        Inches(0.5),
        "→",
        size=24,
        bold=True,
        color=TEAL,
        align=1,
    )
    _text_box(
        slide,
        Inches(6.4),
        Inches(3.5),
        Inches(0.6),
        Inches(0.5),
        "→",
        size=24,
        bold=True,
        color=TEAL,
        align=1,
    )

    _text_box(
        slide,
        Inches(0.8),
        Inches(6.3),
        Inches(11),
        Inches(0.5),
        'All screens: ≤182 characters  |  Number-driven navigation  |  "99. Main Menu" on every screen  |  ≤4 levels deep',
        size=10,
        italic=True,
        color=GREY,
        align=1,
    )

    # ── Slide 7: Team Composition ───────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box(slide, Inches(0), Inches(0), SLIDE_W, Inches(1.1), bg=TEAL)
    _text_box(
        slide,
        Inches(0.8),
        Inches(0.2),
        Inches(11),
        Inches(0.7),
        "Team Composition",
        size=28,
        bold=True,
        color=WHITE,
        align=0,
    )

    team = [
        ("Consulting Lead", "Jmlus", "Project management\nMalawi health sector", "30%"),
        (
            "Solution Architect",
            "Senior Backend",
            "USSD gateway integrations\nREST API design",
            "25%",
        ),
        ("Mobile Developer", "USSD Specialist", "USSD app development\nChichewa systems", "40%"),
        ("Integration Engineer", "API Specialist", "REST API pipelines\nData quality", "20%"),
        ("UX Research Lead", "Low-Literacy UX", "User research Malawi\nInterface design", "15%"),
        ("Data Privacy Officer", "Compliance", "GDPR/NDPR\nHealth data protection", "10%"),
        ("QA Engineer", "Test Lead", "USSD testing\nUAT coordination", "20%"),
        ("Financial Analyst", "Budget Lead", "NGO budgeting\nUSD/MWK forecasting", "5%"),
        ("Document Designer", "Deliverables", "Reports & documentation\nTraining materials", "10%"),
        (
            "Business Developer",
            "Client Relations",
            "VillageReach management\nStakeholder coordination",
            "5%",
        ),
    ]

    for i, (role, name, quals, alloc) in enumerate(team):
        col = i % 5
        row = i // 5
        x = Inches(0.6 + col * 2.5)
        y = Inches(1.4 + row * 2.9)
        bg = LTCYAN if row == 0 else LTGREY
        box(slide, x, y, Inches(2.3), Inches(2.6), bg=bg, line_color=RGBColor(0xDD, 0xDD, 0xDD))
        box(slide, x, y, Inches(2.3), Inches(0.05), bg=TEAL)
        _text_box(
            slide,
            x + Inches(0.1),
            y + Inches(0.15),
            Inches(2.1),
            Inches(0.35),
            role,
            size=10,
            bold=True,
            color=TEAL,
            align=0,
        )
        _text_box(
            slide,
            x + Inches(0.1),
            y + Inches(0.5),
            Inches(2.1),
            Inches(0.3),
            name,
            size=9,
            italic=True,
            color=GREY,
            align=0,
        )
        _text_box(
            slide,
            x + Inches(0.1),
            y + Inches(0.9),
            Inches(2.1),
            Inches(1),
            quals,
            size=9,
            color=DARK,
            align=0,
        )
        _text_box(
            slide,
            x + Inches(0.1),
            y + Inches(2.1),
            Inches(2.1),
            Inches(0.3),
            f"Allocation: {alloc}",
            size=9,
            bold=True,
            color=TEAL,
            align=0,
        )

    # ── Slide 8: Timeline ───────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box(slide, Inches(0), Inches(0), SLIDE_W, Inches(1.1), bg=TEAL)
    _text_box(
        slide,
        Inches(0.8),
        Inches(0.2),
        Inches(11),
        Inches(0.7),
        "Project Timeline – 24 Months",
        size=28,
        bold=True,
        color=WHITE,
        align=0,
    )

    # Phase bars (chevron style)
    phase_data = [
        ("Phase 1", "Discovery & Design", "Week 1", 0.8, 1.5, TEAL),
        ("Phase 2", "Build & Test", "Weeks 2–3", 2.5, 2.5, RGBColor(0x0D, 0x47, 0x47)),
        ("Phase 3", "UAT & Launch", "Week 4", 5.2, 1.5, RGBColor(0x1C, 0x6B, 0x6B)),
        ("Phase 4", "Maintain & Report", "Months 2–24", 6.9, 5.5, RGBColor(0x2E, 0x7D, 0x32)),
    ]

    for phase, title, duration, x_pos, width, bg in phase_data:
        x = Inches(x_pos)
        w = Inches(width)
        box(slide, x, Inches(1.8), w, Inches(1.2), bg=bg)
        _text_box(
            slide,
            x + Inches(0.2),
            Inches(1.9),
            w - Inches(0.4),
            Inches(0.35),
            phase,
            size=10,
            bold=True,
            color=LTCYAN,
            align=0,
        )
        _text_box(
            slide,
            x + Inches(0.2),
            Inches(2.2),
            w - Inches(0.4),
            Inches(0.4),
            title,
            size=13,
            bold=True,
            color=WHITE,
            align=0,
        )
        _text_box(
            slide,
            x + Inches(0.2),
            Inches(2.6),
            w - Inches(0.4),
            Inches(0.3),
            duration,
            size=9,
            italic=True,
            color=LTCYAN,
            align=0,
        )

    # Milestones
    _text_box(
        slide,
        Inches(0.8),
        Inches(3.4),
        Inches(11),
        Inches(0.5),
        "Key Milestones",
        size=16,
        bold=True,
        color=TEAL,
        align=0,
    )

    milestones = [
        ("Contract Signing", "Day 0", "40% payment"),
        ("Wireframes Approved", "End of Week 1", "—"),
        ("USSD Build Complete", "End of Week 3", "—"),
        ("Go-Live on 54747", "End of Week 4", "20% payment"),
        ("Monthly Reports", "Months 1–24", "40% in monthly installments"),
        ("Engagement Complete", "Month 24", "—"),
    ]

    for i, (milestone, timing, payment) in enumerate(milestones):
        x = Inches(0.8 + i * 2.05)
        y = Inches(4.0)
        bg = TEAL if i in [0, 3] else LTGREY
        tc = WHITE if i in [0, 3] else DARK
        box(slide, x, y, Inches(1.9), Inches(1.8), bg=bg, line_color=RGBColor(0xDD, 0xDD, 0xDD))
        _text_box(
            slide,
            x + Inches(0.1),
            y + Inches(0.15),
            Inches(1.7),
            Inches(0.5),
            milestone,
            size=10,
            bold=True,
            color=tc,
            align=0,
        )
        _text_box(
            slide,
            x + Inches(0.1),
            y + Inches(0.65),
            Inches(1.7),
            Inches(0.35),
            timing,
            size=9,
            color=tc if i in [0, 3] else GREY,
            align=0,
        )
        _text_box(
            slide,
            x + Inches(0.1),
            y + Inches(1.1),
            Inches(1.7),
            Inches(0.5),
            payment,
            size=9,
            bold=True,
            color=CORAL if payment != "—" else (tc if i in [0, 3] else GREY),
            align=0,
        )

    # ── Slide 9: Budget Summary ─────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box(slide, Inches(0), Inches(0), SLIDE_W, Inches(1.1), bg=TEAL)
    _text_box(
        slide,
        Inches(0.8),
        Inches(0.2),
        Inches(11),
        Inches(0.7),
        "Budget & Financial Proposal",
        size=28,
        bold=True,
        color=WHITE,
        align=0,
    )

    # Three main cards
    cards = [
        (
            "Phase 1: Setup",
            "$13,350",
            "4 weeks\nUSSD design & development\nUAT & launch\nDocumentation",
            TEAL,
        ),
        (
            "Phase 2: Maintenance",
            "$25,633",
            "24 months\nMonthly reporting\nContent updates\nBug fixes & optimization",
            RGBColor(0x0D, 0x47, 0x47),
        ),
        (
            "Reimbursables",
            "$1,926",
            "Travel & logistics\nTesting SIMs\nUAT participant incentives",
            RGBColor(0x2E, 0x7D, 0x32),
        ),
    ]

    for i, (title, amount, desc, bg) in enumerate(cards):
        x = Inches(0.8 + i * 4.1)
        box(slide, x, Inches(1.5), Inches(3.8), Inches(3.5), bg=bg)
        _text_box(
            slide,
            x + Inches(0.3),
            Inches(1.7),
            Inches(3.2),
            Inches(0.5),
            title,
            size=14,
            bold=True,
            color=LTCYAN,
            align=0,
        )
        _text_box(
            slide,
            x + Inches(0.3),
            Inches(2.3),
            Inches(3.2),
            Inches(0.7),
            amount,
            size=32,
            bold=True,
            color=WHITE,
            align=0,
        )
        _text_box(
            slide,
            x + Inches(0.3),
            Inches(3.2),
            Inches(3.2),
            Inches(1.5),
            desc,
            size=11,
            color=LTCYAN,
            align=0,
        )

    # Total bar
    box(slide, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.5), bg=DARK)
    _text_box(
        slide,
        Inches(1.2),
        Inches(5.5),
        Inches(4),
        Inches(0.5),
        "TOTAL ENGAGEMENT VALUE",
        size=18,
        bold=True,
        color=LTCYAN,
        align=0,
    )
    _text_box(
        slide,
        Inches(5.5),
        Inches(5.3),
        Inches(3),
        Inches(1.5),
        "$45,000",
        size=40,
        bold=True,
        color=CORAL,
        align=1,
    )
    _text_box(
        slide,
        Inches(8.5),
        Inches(5.5),
        Inches(3.5),
        Inches(0.5),
        "Incl. 10% contingency ($4,091)",
        size=12,
        italic=True,
        color=GREY,
        align=0,
    )
    _text_box(
        slide,
        Inches(8.5),
        Inches(5.9),
        Inches(3.5),
        Inches(0.5),
        "≈ $1,875/mo all-in",
        size=12,
        italic=True,
        color=GREY,
        align=0,
    )
    _text_box(
        slide,
        Inches(8.5),
        Inches(6.1),
        Inches(3.5),
        Inches(0.5),
        "Payment: 40% signing | 20% go-live | 40% monthly",
        size=11,
        color=WHITE,
        align=0,
    )

    # ── Slide 10: Payment Schedule ──────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box(slide, Inches(0), Inches(0), SLIDE_W, Inches(1.1), bg=TEAL)
    _text_box(
        slide,
        Inches(0.8),
        Inches(0.2),
        Inches(11),
        Inches(0.7),
        "Payment Schedule",
        size=28,
        bold=True,
        color=WHITE,
        align=0,
    )

    payments = [
        ("Payment 1", "Contract Signing", "Day 0", "$18,000", "40%", TEAL),
        ("Payment 2", "Go-Live", "End of Week 4", "$9,000", "20%", RGBColor(0x0D, 0x47, 0x47)),
        (
            "Payments 3–26",
            "Monthly Maintenance",
            "Months 1–24",
            "$750/mo",
            "40% (× 24)",
            RGBColor(0x1C, 0x6B, 0x6B),
        ),
    ]

    for i, (payment, timing, date, amount, pct, bg) in enumerate(payments):
        y = Inches(1.5 + i * 1.4)
        box(slide, Inches(0.8), y, Inches(11.7), Inches(1.2), bg=bg)
        _text_box(
            slide,
            Inches(1.2),
            y + Inches(0.15),
            Inches(2.5),
            Inches(0.4),
            payment,
            size=14,
            bold=True,
            color=WHITE,
            align=0,
        )
        _text_box(
            slide,
            Inches(1.2),
            y + Inches(0.6),
            Inches(2.5),
            Inches(0.4),
            timing,
            size=11,
            color=LTCYAN,
            align=0,
        )
        _text_box(
            slide,
            Inches(4),
            y + Inches(0.15),
            Inches(2),
            Inches(0.9),
            date,
            size=11,
            color=WHITE,
            align=0,
        )
        _text_box(
            slide,
            Inches(6.5),
            y + Inches(0.15),
            Inches(2.5),
            Inches(0.9),
            amount,
            size=20,
            bold=True,
            color=WHITE,
            align=1,
        )
        _text_box(
            slide,
            Inches(9.5),
            y + Inches(0.15),
            Inches(2.5),
            Inches(0.9),
            pct,
            size=14,
            bold=True,
            color=LTCYAN,
            align=1,
        )

    # ── Slide 11: Data Privacy & Security ───────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box(slide, Inches(0), Inches(0), SLIDE_W, Inches(1.1), bg=TEAL)
    _text_box(
        slide,
        Inches(0.8),
        Inches(0.2),
        Inches(11),
        Inches(0.7),
        "Data Privacy & Security",
        size=28,
        bold=True,
        color=WHITE,
        align=0,
    )

    security_items = [
        (
            "Data Minimization",
            "USSD collects only minimum required data; no PII stored unless authorized",
        ),
        ("Encryption", "TLS 1.3 in transit; AES-256 at rest; OAuth 2.0 API authentication"),
        ("Access Controls", "Role-based access (RBAC); principle of least privilege enforced"),
        ("Audit Logging", "Complete audit trail; 12-month log retention per VillageReach policy"),
        ("Incident Response", "24-hour breach notification; documented response plan"),
        (
            "Compliance",
            "Malawi Data Protection Act (2024); GDPR best practices; VillageReach governance",
        ),
    ]

    for i, (title, desc) in enumerate(security_items):
        col = i % 3
        row = i // 3
        x = Inches(0.8 + col * 4.1)
        y = Inches(1.5 + row * 2.8)
        box(slide, x, y, Inches(3.8), Inches(2.5), bg=LTGREY, line_color=RGBColor(0xDD, 0xDD, 0xDD))
        box(slide, x, y, Inches(3.8), Inches(0.06), bg=TEAL)
        _text_box(
            slide,
            x + Inches(0.2),
            y + Inches(0.2),
            Inches(3.4),
            Inches(0.4),
            title,
            size=13,
            bold=True,
            color=TEAL,
            align=0,
        )
        _text_box(
            slide,
            x + Inches(0.2),
            y + Inches(0.7),
            Inches(3.4),
            Inches(1.5),
            desc,
            size=11,
            color=DARK,
            align=0,
        )

    # ── Slide 12: Risk Register ─────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box(slide, Inches(0), Inches(0), SLIDE_W, Inches(1.1), bg=TEAL)
    _text_box(
        slide,
        Inches(0.8),
        Inches(0.2),
        Inches(11),
        Inches(0.7),
        "Risk Register & Mitigation",
        size=28,
        bold=True,
        color=WHITE,
        align=0,
    )

    risks = [
        (
            "USSD Gateway Downtime",
            "Medium",
            "High",
            "Dual-network redundancy; proactive monitoring",
            CORAL,
        ),
        (
            "Low UAT Participation",
            "Low",
            "Medium",
            "Pre-recruit 30 participants; airtime incentives",
            AMBER,
        ),
        (
            "Chichewa Content Ambiguity",
            "Medium",
            "Medium",
            "Local language specialist; community review",
            AMBER,
        ),
        (
            "Data Pipeline Delays",
            "Low",
            "High",
            "API-first design; mock endpoints; integration testing Week 2",
            CORAL,
        ),
        (
            "Scope Creep",
            "Medium",
            "Medium",
            "Change request process; MWK 60,000/hr out-of-scope",
            AMBER,
        ),
        (
            "Key Personnel Unavailability",
            "Low",
            "High",
            "Cross-trained team; documented handover; 48-hr coverage",
            CORAL,
        ),
    ]

    # Header
    box(slide, Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.6), bg=TEAL)
    _text_box(
        slide,
        Inches(1),
        Inches(1.45),
        Inches(3),
        Inches(0.5),
        "Risk",
        size=11,
        bold=True,
        color=WHITE,
        align=0,
    )
    _text_box(
        slide,
        Inches(4.2),
        Inches(1.45),
        Inches(1.2),
        Inches(0.5),
        "Likelihood",
        size=11,
        bold=True,
        color=WHITE,
        align=1,
    )
    _text_box(
        slide,
        Inches(5.5),
        Inches(1.45),
        Inches(1),
        Inches(0.5),
        "Impact",
        size=11,
        bold=True,
        color=WHITE,
        align=1,
    )
    _text_box(
        slide,
        Inches(6.8),
        Inches(1.45),
        Inches(5.5),
        Inches(0.5),
        "Mitigation",
        size=11,
        bold=True,
        color=WHITE,
        align=0,
    )

    for i, (risk, likelihood, impact, mitigation, indicator) in enumerate(risks):
        y = Inches(2.1 + i * 0.85)
        bg = LTGREY if i % 2 == 0 else WHITE
        box(
            slide,
            Inches(0.8),
            y,
            Inches(11.7),
            Inches(0.75),
            bg=bg,
            line_color=RGBColor(0xEE, 0xEE, 0xEE),
        )
        box(slide, Inches(0.8), y, Inches(0.08), Inches(0.75), bg=indicator)
        _text_box(
            slide,
            Inches(1.1),
            y + Inches(0.15),
            Inches(3),
            Inches(0.45),
            risk,
            size=10,
            bold=True,
            color=DARK,
            align=0,
        )
        _text_box(
            slide,
            Inches(4.2),
            y + Inches(0.15),
            Inches(1.2),
            Inches(0.45),
            likelihood,
            size=10,
            color=DARK,
            align=1,
        )
        _text_box(
            slide,
            Inches(5.5),
            y + Inches(0.15),
            Inches(1),
            Inches(0.45),
            impact,
            size=10,
            color=DARK,
            align=1,
        )
        _text_box(
            slide,
            Inches(6.8),
            y + Inches(0.15),
            Inches(5.5),
            Inches(0.45),
            mitigation,
            size=10,
            color=DARK,
            align=0,
        )

    # ── Slide 13: Terms & Conditions ────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box(slide, Inches(0), Inches(0), SLIDE_W, Inches(1.1), bg=TEAL)
    _text_box(
        slide,
        Inches(0.8),
        Inches(0.2),
        Inches(11),
        Inches(0.7),
        "Terms & Conditions",
        size=28,
        bold=True,
        color=WHITE,
        align=0,
    )

    terms = [
        (
            "Payment Terms",
            [
                "Currency: USD (MWK equivalent at prevailing rate)",
                "Schedule: 40% signing → 20% go-live → 40% monthly",
                "Payment window: Net 30 days from invoice",
                "Invoicing: Monthly with time sheets & completion certs",
            ],
        ),
        (
            "Intellectual Property",
            [
                "All code & documentation become VillageReach property",
                "LSH retains proprietary framework rights",
                "Open-source components under their respective licenses",
            ],
        ),
        (
            "Confidentiality & Termination",
            [
                "All project data treated as strictly confidential",
                "30-day written notice for termination",
                "Completed work delivered upon termination",
            ],
        ),
    ]

    for i, (title, items) in enumerate(terms):
        x = Inches(0.8 + i * 4.1)
        box(
            slide,
            x,
            Inches(1.5),
            Inches(3.8),
            Inches(5.2),
            bg=LTGREY,
            line_color=RGBColor(0xDD, 0xDD, 0xDD),
        )
        box(slide, x, Inches(1.5), Inches(3.8), Inches(0.06), bg=CORAL)
        _text_box(
            slide,
            x + Inches(0.2),
            Inches(1.7),
            Inches(3.4),
            Inches(0.5),
            title,
            size=14,
            bold=True,
            color=TEAL,
            align=0,
        )
        tf = _text_box(
            slide,
            x + Inches(0.2),
            Inches(2.3),
            Inches(3.4),
            Inches(4),
            "",
            size=10,
            color=DARK,
            align=0,
        )
        _add_bullet_list(tf.text_frame, items, size=10)

    _text_box(
        slide,
        Inches(0.8),
        Inches(6.8),
        Inches(11.7),
        Inches(0.5),
        "This proposal is valid for 30 days from date of submission.",
        size=10,
        italic=True,
        color=GREY,
        align=1,
    )

    # ── Slide 14: Next Steps ────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box(slide, Inches(0), Inches(0), SLIDE_W, Inches(1.1), bg=TEAL)
    _text_box(
        slide,
        Inches(0.8),
        Inches(0.2),
        Inches(11),
        Inches(0.7),
        "Next Steps",
        size=28,
        bold=True,
        color=WHITE,
        align=0,
    )

    next_steps = [
        (
            "1",
            "Proposal Review",
            "VillageReach evaluates technical approach and financial proposal",
        ),
        (
            "2",
            "Clarification Meeting",
            "Address questions; align on scope, timeline, and expectations",
        ),
        ("3", "Contract Negotiation", "Finalize terms, payment schedule, and NDA execution"),
        ("4", "Kick-Off", "Phase 1 begins: stakeholder interviews and wireframe development"),
    ]

    for i, (num, title, desc) in enumerate(next_steps):
        y = Inches(1.5 + i * 1.4)
        # Number circle
        box(slide, Inches(1.5), y, Inches(0.8), Inches(0.8), bg=TEAL)
        _text_box(
            slide,
            Inches(1.5),
            y + Inches(0.1),
            Inches(0.8),
            Inches(0.6),
            num,
            size=24,
            bold=True,
            color=WHITE,
            align=1,
        )
        # Content
        _text_box(
            slide,
            Inches(2.6),
            y + Inches(0.05),
            Inches(8),
            Inches(0.4),
            title,
            size=16,
            bold=True,
            color=DARK,
            align=0,
        )
        _text_box(
            slide,
            Inches(2.6),
            y + Inches(0.5),
            Inches(8),
            Inches(0.4),
            desc,
            size=11,
            color=GREY,
            align=0,
        )
        # Connector line
        if i < 3:
            box(slide, Inches(1.85), y + Inches(0.85), Inches(0.06), Inches(0.55), bg=LTCYAN)

    # ── Slide 15: Thank You ─────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box(slide, Inches(0), Inches(0), SLIDE_W, SLIDE_H, bg=TEAL)
    box(slide, Inches(0), Inches(3.1), SLIDE_W, Inches(0.06), bg=CORAL)

    _text_box(
        slide,
        Inches(1.5),
        Inches(1.5),
        Inches(10),
        Inches(1),
        "Thank You",
        size=44,
        bold=True,
        color=WHITE,
        align=1,
    )
    _text_box(
        slide,
        Inches(1.5),
        Inches(2.4),
        Inches(10),
        Inches(0.6),
        "Light Speed Holdings",
        size=22,
        bold=True,
        color=LTCYAN,
        align=1,
    )

    _text_box(
        slide,
        Inches(1.5),
        Inches(3.6),
        Inches(10),
        Inches(0.8),
        "Committed to the success of the CHOICE Project\nand the communities it serves.",
        size=14,
        color=WHITE,
        align=1,
    )

    _text_box(
        slide,
        Inches(1.5),
        Inches(5.0),
        Inches(10),
        Inches(0.4),
        "info@lightspeedholdings.com  |  lightspeedholdings.com",
        size=12,
        color=LTCYAN,
        align=1,
    )
    _text_box(
        slide,
        Inches(1.5),
        Inches(5.5),
        Inches(10),
        Inches(0.4),
        "Malawi  ·  Nairobi  ·  Washington DC",
        size=11,
        color=WHITE,
        align=1,
    )
    _text_box(
        slide,
        Inches(1.5),
        Inches(6.3),
        Inches(10),
        Inches(0.4),
        "Confidential – Prepared for VillageReach CHOICE Project Evaluation",
        size=10,
        italic=True,
        color=CORAL,
        align=1,
    )

    prs.save(OUT)
    print(f"  Saved: {OUT}")


if __name__ == "__main__":
    build()
