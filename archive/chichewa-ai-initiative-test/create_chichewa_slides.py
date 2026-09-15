#!/usr/bin/env python3
"""
Generate Google Slides-compatible PowerPoint presentation for Chichewa AI Initiative.
Run: python create_chichewa_slides.py
Output: chichewa_ai_initiative.pptx (upload to Google Slides → File → Import Slides)
"""

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

# ─── Color Palette ───
DARK_NAVY = RGBColor(0x0B, 0x1D, 0x3A)
MEDIUM_BLUE = RGBColor(0x1A, 0x3C, 0x6E)
ACCENT_TEAL = RGBColor(0x00, 0xB4, 0xD8)
ACCENT_GOLD = RGBColor(0xFF, 0xB7, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF0, 0xF2, 0xF5)
MEDIUM_GRAY = RGBColor(0x6C, 0x75, 0x7D)
DARK_GRAY = RGBColor(0x34, 0x3A, 0x40)
RED_RISK = RGBColor(0xDC, 0x35, 0x45)
GREEN_GOOD = RGBColor(0x28, 0xA7, 0x45)
ORANGE_WARN = RGBColor(0xFD, 0x7E, 0x14)


# ─── Slide Layout Helpers ───
def add_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape_bg(slide, left, top, width, height, color, transparency=0):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_text_box(
    slide,
    left,
    top,
    width,
    height,
    text,
    font_size=18,
    bold=False,
    color=WHITE,
    alignment=PP_ALIGN.LEFT,
    font_name="Calibri",
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


def add_bullet_list(
    slide,
    left,
    top,
    width,
    height,
    items,
    font_size=16,
    color=WHITE,
    bold_first=False,
    spacing=6,
    font_name="Calibri",
):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = font_name
        p.space_after = Pt(spacing)
        p.level = 0
        if bold_first and i == 0:
            p.font.bold = True
    return txBox


def add_table(
    slide,
    left,
    top,
    width,
    height,
    rows,
    cols,
    data,
    col_widths=None,
    header_color=MEDIUM_BLUE,
    header_font_color=WHITE,
    body_font_color=DARK_GRAY,
    font_size=12,
):
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = w

    for r in range(rows):
        for c in range(cols):
            cell = table.cell(r, c)
            cell.text = str(data[r][c]) if r < len(data) and c < len(data[r]) else ""
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.size = Pt(font_size)
                paragraph.font.name = "Calibri"
                if r == 0:
                    paragraph.font.bold = True
                    paragraph.font.color.rgb = header_font_color
                else:
                    paragraph.font.color.rgb = body_font_color
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            if r == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_color
            elif r % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = LIGHT_GRAY
    return table_shape


# ─── Create Presentation ───
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ============================================================
# SLIDE 1: TITLE SLIDE
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
add_background(slide, DARK_NAVY)

# Accent bar at top
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.08), ACCENT_TEAL)

# Main title
add_text_box(
    slide,
    Inches(1),
    Inches(1.5),
    Inches(11),
    Inches(1.5),
    "THE CHICHEWA AI INITIATIVE",
    44,
    True,
    WHITE,
    PP_ALIGN.CENTER,
)

# Subtitle
add_text_box(
    slide,
    Inches(1.5),
    Inches(3.0),
    Inches(10),
    Inches(0.8),
    "Executive Presentation — Light Speed Holdings",
    24,
    False,
    ACCENT_TEAL,
    PP_ALIGN.CENTER,
)

# Divider line
add_shape_bg(slide, Inches(4.5), Inches(4.0), Inches(4), Inches(0.04), ACCENT_GOLD)

# Details
add_text_box(
    slide,
    Inches(1.5),
    Inches(4.3),
    Inches(10),
    Inches(0.5),
    "CONFIDENTIAL  •  Board & CEO Only  •  August 2026",
    16,
    False,
    MEDIUM_GRAY,
    PP_ALIGN.CENTER,
)

# Bottom tag
add_text_box(
    slide,
    Inches(1.5),
    Inches(5.5),
    Inches(10),
    Inches(0.5),
    "Strategic Platform Partnership for Africa's First National Language Data Trust",
    18,
    False,
    WHITE,
    PP_ALIGN.CENTER,
)


# ============================================================
# SLIDE 2: THE OPPORTUNITY IN ONE SENTENCE
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, DARK_NAVY)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.08), ACCENT_TEAL)

add_text_box(
    slide,
    Inches(0.8),
    Inches(0.4),
    Inches(11.5),
    Inches(0.6),
    "THE OPPORTUNITY IN ONE SENTENCE",
    28,
    True,
    ACCENT_TEAL,
    PP_ALIGN.LEFT,
)

# Big quote box
quote_box = add_shape_bg(slide, Inches(1.5), Inches(1.5), Inches(10.3), Inches(2.5), MEDIUM_BLUE)
add_text_box(
    slide,
    Inches(2),
    Inches(1.7),
    Inches(9.3),
    Inches(2.1),
    '"Malawi has built the world\'s first National Language Data Trust for\nChichewa (12M speakers). We can provide the agent orchestration platform\nthat turns this data into scalable, multi-modal AI services for African\nagriculture — starting with 10,000 farmers in 9 months."',
    26,
    False,
    WHITE,
    PP_ALIGN.CENTER,
)

# Three pillars
pillars = [
    ("📊  DATA READY", "7,000+ hrs Chichewa audio/text\nWorld Bank + Gates Foundation funded"),
    ("🌍  MASSIVE NEED", "80% in agriculture; <30% smartphone\nVoice-first AI required"),
    (
        "⚡  TECH READY",
        "LLaMA-3 + Whisper + Piper + Our Platform\nProduction-grade low-resource stack",
    ),
]

for i, (title, desc) in enumerate(pillars):
    x = Inches(1.5 + i * 3.8)
    box = add_shape_bg(slide, x, Inches(4.5), Inches(3.5), Inches(2.2), RGBColor(0x12, 0x2A, 0x50))
    add_text_box(
        slide, x + Inches(0.3), Inches(4.7), Inches(3), Inches(0.5), title, 18, True, ACCENT_GOLD
    )
    add_text_box(
        slide, x + Inches(0.3), Inches(5.2), Inches(3), Inches(1.3), desc, 15, False, LIGHT_GRAY
    )

# Footer
add_text_box(
    slide,
    Inches(0.8),
    Inches(6.9),
    Inches(11.5),
    Inches(0.4),
    "First-mover advantage: No one has deployed multi-agent orchestration for African language AI at national scale.",
    14,
    True,
    ACCENT_TEAL,
    PP_ALIGN.CENTER,
)


# ============================================================
# SLIDE 3: WHY NOW — CONVERGENCE OF THREE FORCES
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, DARK_NAVY)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.08), ACCENT_TEAL)

add_text_box(
    slide,
    Inches(0.8),
    Inches(0.4),
    Inches(11.5),
    Inches(0.6),
    "WHY NOW — CONVERGENCE OF THREE FORCES",
    28,
    True,
    ACCENT_TEAL,
)

# Table
data = [
    ["FORCE", "SIGNAL", "OUR WINDOW"],
    [
        "SUPPLY",
        "7,000+ hrs Chichewa audio/text (ZBS, Govt archives) — World Bank + Gates funded",
        "DATA READY NOW",
    ],
    [
        "DEMAND",
        "80% of Malawi in agriculture; <30% smartphone penetration; voice-first required",
        "MASSIVE UNMET NEED",
    ],
    [
        "TECH READINESS",
        "LLaMA-3 + Whisper + Piper + our Agent Platform = production-grade low-resource language stack",
        "WE CAN BUILD FIRST",
    ],
]

add_table(
    slide,
    Inches(0.8),
    Inches(1.2),
    Inches(11.7),
    Inches(3.5),
    4,
    3,
    data,
    col_widths=[Inches(2), Inches(7), Inches(2.7)],
    font_size=14,
)

# Key insight box
insight_box = add_shape_bg(
    slide, Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.5), RGBColor(0x12, 0x2A, 0x50)
)
add_text_box(
    slide,
    Inches(1.2),
    Inches(5.3),
    Inches(11),
    Inches(1.3),
    "🎯 FIRST-MOVER ADVANTAGE: No competitor has deployed multi-agent orchestration for African language AI at national scale.\nOur agent factory pattern (YAML → OpenCode agents + MessageBus) is uniquely positioned to operationalize this Data Trust.",
    16,
    False,
    WHITE,
    PP_ALIGN.LEFT,
)


# ============================================================
# SLIDE 4: STRATEGIC FIT
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, DARK_NAVY)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.08), ACCENT_TEAL)

add_text_box(
    slide,
    Inches(0.8),
    Inches(0.4),
    Inches(11.5),
    Inches(0.6),
    "STRATEGIC FIT — OUR PLATFORM MEETS THEIR NEED",
    28,
    True,
    ACCENT_TEAL,
)

data = [
    ["INITIATIVE NEED", "OUR PLATFORM CAPABILITY", "COMPETITIVE MOAT"],
    [
        "UlangiziAI is monolithic → needs specialist agents",
        "Agent Registry + Orchestration + MessageBus (YAML-defined, generated)",
        "PLATFORM, NOT PROJECT",
    ],
    [
        "Voice + WhatsApp + IVR + USSD channels",
        "Channel-agnostic adapters (single agent logic, multi-interface)",
        "WRITE ONCE, DEPLOY EVERYWHERE",
    ],
    [
        "Scale Chichewa → Tumbuka, Yao, Sena, Lomwe",
        "Agent Factory pattern (80% registry reuse)",
        "REPLICABLE ACROSS 50+ BANTU LANGUAGES",
    ],
    [
        "Public developer access planned",
        "Developer Portal + SDK + API (our core product)",
        "OWN THE ECOSYSTEM LAYER",
    ],
]

add_table(
    slide,
    Inches(0.8),
    Inches(1.2),
    Inches(11.7),
    Inches(4.5),
    5,
    3,
    data,
    col_widths=[Inches(3.5), Inches(5), Inches(3.2)],
    font_size=13,
)

add_text_box(
    slide,
    Inches(0.8),
    Inches(6.2),
    Inches(11.7),
    Inches(0.5),
    "Core Insight: We don't just build a chatbot — we provide the orchestration layer that makes ANY African language AI scalable.",
    16,
    True,
    ACCENT_GOLD,
    PP_ALIGN.CENTER,
)


# ============================================================
# SLIDE 5: THE ASK
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, DARK_NAVY)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.08), ACCENT_TEAL)

add_text_box(
    slide,
    Inches(0.8),
    Inches(0.4),
    Inches(11.5),
    Inches(0.6),
    'THE ASK — "PLATFORM PARTNER" ENGAGEMENT',
    28,
    True,
    ACCENT_TEAL,
)

# Key metrics boxes
metrics = [
    ("ROLE", "Technology/Platform Partner\n(not vendor, not grantee)"),
    ("INVESTMENT", "$2.8M direct + $1.6M contingency\n= $4.4M over 12 months"),
    ("TEAM", "12.5 FTE\n(7 ML/Backend, 2 Voice, 1.5 DevOps, 1 Frontend, 1 PM)"),
    ("TARGET", "10,000 active farmers by Month 9\nMSA with Malawi Govt by Month 12"),
    (
        "REVENUE PATH",
        "Platform SaaS ($300k Y1)\n+ Prof Services ($400k) + Grants ($1M)\n= $1.85M Y1",
    ),
]

for i, (label, value) in enumerate(metrics):
    x = Inches(0.6 + i * 2.5)
    box = add_shape_bg(slide, x, Inches(1.3), Inches(2.3), Inches(3.5), MEDIUM_BLUE)
    add_text_box(
        slide, x + Inches(0.15), Inches(1.4), Inches(2), Inches(0.4), label, 14, True, ACCENT_GOLD
    )
    add_text_box(
        slide,
        x + Inches(0.15),
        Inches(1.8),
        Inches(2),
        Inches(2.8),
        value,
        16,
        False,
        WHITE,
        PP_ALIGN.CENTER,
    )


# ============================================================
# SLIDE 6: 3-PHASE ROADMAP
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, DARK_NAVY)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.08), ACCENT_TEAL)

add_text_box(
    slide,
    Inches(0.8),
    Inches(0.4),
    Inches(11.5),
    Inches(0.6),
    "3-PHASE ROADMAP",
    28,
    True,
    ACCENT_TEAL,
)

phases = [
    (
        "PHASE 1: FOUNDATION (M1-3)",
        ACCENT_TEAL,
        [
            "Data pipeline (1,000 hrs processed)",
            "Tokenizer + Continued Pretraining",
            "Agent Registry v1 (6 agents)",
            "Dev Sandbox (API + SDK)",
            "🎯 GATE 1: OI MoU signed",
        ],
    ),
    (
        "PHASE 2: INTEGRATION (M4-6)",
        ACCENT_GOLD,
        [
            "SFT Chichewa model (50k QA pairs)",
            "6 specialist agents + orchestrator",
            "Whisper FT + Piper TTS",
            "WhatsApp voice E2E",
            "🎯 GATE 2: Pilot ready",
        ],
    ),
    (
        "PHASE 3: SCALE (M7-12)",
        GREEN_GOOD,
        [
            "IVR production (1,000 calls/day)",
            "RLHF from farmer feedback",
            "Dialect LoRAs (3 regions)",
            "Public API GA + Hackathon",
            "🎯 GATE 3: Scale decision + MSA",
        ],
    ),
]

for i, (title, color, items) in enumerate(phases):
    x = Inches(0.6 + i * 4.1)
    # Phase header
    header_box = add_shape_bg(slide, x, Inches(1.2), Inches(3.8), Inches(0.6), color)
    add_text_box(
        slide,
        x + Inches(0.15),
        Inches(1.22),
        Inches(3.5),
        Inches(0.5),
        title,
        16,
        True,
        WHITE,
        PP_ALIGN.CENTER,
    )
    # Content box
    content_box = add_shape_bg(
        slide, x, Inches(1.8), Inches(3.8), Inches(3.8), RGBColor(0x12, 0x2A, 0x50)
    )
    y = Inches(1.9)
    for item in items:
        is_gate = item.startswith("🎯")
        add_text_box(
            slide,
            x + Inches(0.2),
            y,
            Inches(3.4),
            Inches(0.5),
            item,
            13,
            is_gate,
            ACCENT_GOLD if is_gate else WHITE,
        )
        y += Inches(0.55)

# Arrow indicators
for i in range(2):
    x = Inches(4.2 + i * 4.1)
    add_text_box(
        slide, x, Inches(1.3), Inches(0.5), Inches(0.5), "→", 28, True, ACCENT_TEAL, PP_ALIGN.CENTER
    )


# ============================================================
# SLIDE 7: KEY PARTNERSHIPS
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, DARK_NAVY)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.08), ACCENT_TEAL)

add_text_box(
    slide,
    Inches(0.8),
    Inches(0.4),
    Inches(11.5),
    Inches(0.6),
    "KEY PARTNERSHIPS — TIER 1 (MUST CLOSE DAYS 1-30)",
    28,
    True,
    ACCENT_TEAL,
)

data = [
    ["PARTNER", "WHAT WE NEED", "WHAT THEY GET", "STRUCTURE"],
    [
        "Opportunity International",
        "Co-dev UlangiziAI v2; farmer access; ag knowledge base",
        "Multi-agent architecture; scale to new languages; platform ownership",
        "JDA — Revenue share on premium; grant-funded core",
    ],
    [
        "Zodiak Broadcasting (ZBS)",
        "7,000hr audio archive license",
        'Revenue share; co-branded "ZBS AI" hotline; digital transformation',
        "Data License + Co-Marketing — $50k/yr + 10% rev share",
    ],
    [
        "Malawi Ministry of Agriculture",
        "National integration; extension officer network; Govt dashboard",
        "2,000+ officers AI-enabled; policy insights; capacity building",
        "MoU → MSA — $200-500k/yr + WB co-financing",
    ],
    [
        "World Bank (Digital Dev)",
        "Technical partner designation; co-funding",
        "Implementation capacity; innovation showcase; sustainability",
        "Trust Fund / DGF — $1M target",
    ],
]

add_table(
    slide,
    Inches(0.5),
    Inches(1.1),
    Inches(12.3),
    Inches(5.5),
    5,
    4,
    data,
    col_widths=[Inches(2.5), Inches(3.5), Inches(3.5), Inches(2.8)],
    font_size=12,
)


# ============================================================
# SLIDE 8: MVP — ULANGIZIAI v2
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, DARK_NAVY)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.08), ACCENT_TEAL)

add_text_box(
    slide,
    Inches(0.8),
    Inches(0.4),
    Inches(11.5),
    Inches(0.6),
    "MVP — ULANGIZIAI v2 (90-DAY PILOT)",
    28,
    True,
    ACCENT_TEAL,
)

add_text_box(
    slide,
    Inches(0.8),
    Inches(1.0),
    Inches(11.5),
    Inches(0.5),
    "6 Specialist Agents + Orchestrator → WhatsApp (Text + Voice) → 50 Farmers",
    18,
    False,
    ACCENT_GOLD,
    PP_ALIGN.CENTER,
)

# Agent cards
agents = [
    ("🌤️ WEATHER", "Forecasts, planting windows, alerts", "MET Malawi + satellite"),
    ("💰 MARKETS", "Commodity prices, buyer contacts, transport", "MACE + RATIN + farmer reports"),
    ("🌱 CROPS", "Varieties, calendars, intercropping", "Ministry of Ag + CGIAR"),
    ("🐛 PESTS", "ID, IPM, pesticide safety (regulated)", "CABI + Ministry bulletins"),
    ("🏦 FINANCE", "Input loans, insurance, mobile money", "NBS Bank + Airtel Money + NGOs"),
    ("🎫 SUBSIDIES", "AIP eligibility, depot stock, redemption", "Ministry + Logistics Unit"),
]

for i, (name, domain, source) in enumerate(agents):
    col = i % 3
    row = i // 3
    x = Inches(0.6 + col * 4.1)
    y = Inches(1.7 + row * 2.6)

    card = add_shape_bg(slide, x, y, Inches(3.8), Inches(2.3), MEDIUM_BLUE)
    add_text_box(
        slide,
        x + Inches(0.2),
        y + Inches(0.1),
        Inches(3.4),
        Inches(0.4),
        name,
        16,
        True,
        ACCENT_GOLD,
    )
    add_text_box(
        slide, x + Inches(0.2), y + Inches(0.55), Inches(3.4), Inches(0.8), domain, 13, False, WHITE
    )
    add_text_box(
        slide,
        x + Inches(0.2),
        y + Inches(1.4),
        Inches(3.4),
        Inches(0.6),
        f"Source: {source}",
        11,
        False,
        ACCENT_TEAL,
    )

# Human-in-loop note
add_text_box(
    slide,
    Inches(0.8),
    Inches(6.2),
    Inches(11.5),
    Inches(0.8),
    "🔄 Human-in-loop: Extension officers review <70% confidence responses • Farmer feedback → RLHF training loop",
    14,
    False,
    MEDIUM_GRAY,
    PP_ALIGN.CENTER,
)


# ============================================================
# SLIDE 9: FINANCIAL SNAPSHOT
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, DARK_NAVY)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.08), ACCENT_TEAL)

add_text_box(
    slide,
    Inches(0.8),
    Inches(0.4),
    Inches(11.5),
    Inches(0.6),
    "FINANCIAL SNAPSHOT",
    28,
    True,
    ACCENT_TEAL,
)

# Investment breakdown (left)
add_text_box(
    slide,
    Inches(0.8),
    Inches(1.2),
    Inches(5.5),
    Inches(0.4),
    "12-MONTH INVESTMENT: $4.43M",
    20,
    True,
    ACCENT_GOLD,
)

inv_data = [
    ["CATEGORY", "AMOUNT", "%"],
    ["Personnel (12.5 FTE)", "$2.98M", "67%"],
    ["GPU Compute (Training + Inference)", "$0.42M", "9%"],
    ["Telecom (IVR, WhatsApp, SMS)", "$0.06M", "1%"],
    ["Legal, Travel, Malawi Office", "$0.24M", "6%"],
    ["Contingency (20%)", "$0.59M", "13%"],
    ["TOTAL", "$4.43M", "100%"],
]
add_table(
    slide,
    Inches(0.8),
    Inches(1.7),
    Inches(5.5),
    Inches(3.2),
    6,
    3,
    inv_data,
    col_widths=[Inches(3), Inches(1.5), Inches(1)],
    font_size=12,
)

# Revenue projection (right)
add_text_box(
    slide,
    Inches(7),
    Inches(1.2),
    Inches(5.5),
    Inches(0.4),
    "REVENUE PROJECTION (BASE CASE)",
    20,
    True,
    ACCENT_GOLD,
)

rev_data = [
    ["STREAM", "Y1", "Y2", "Y3"],
    ["Platform SaaS", "$300k", "$800k", "$2.0M"],
    ["Professional Services", "$400k", "$600k", "$800k"],
    ["API/Usage", "$150k", "$500k", "$1.2M"],
    ["Grants/Contracts", "$1.0M", "$500k", "$200k"],
    ["TOTAL REVENUE", "$1.85M", "$2.4M", "$4.2M"],
]
add_table(
    slide,
    Inches(7),
    Inches(1.7),
    Inches(5.5),
    Inches(3.2),
    6,
    4,
    rev_data,
    col_widths=[Inches(2.5), Inches(1), Inches(1), Inches(1)],
    font_size=12,
)

# Unit economics
add_text_box(
    slide,
    Inches(0.8),
    Inches(5.3),
    Inches(11.7),
    Inches(1.5),
    "📈 UNIT ECONOMICS AT SCALE (Y3):  $0.80/farmer/yr cost  •  3.0x LTV/CAC  •  78% gross margin  •  Break-even: 15,000 farmers",
    16,
    True,
    WHITE,
    PP_ALIGN.CENTER,
)


# ============================================================
# SLIDE 10: TOP 5 RISKS
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, DARK_NAVY)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.08), ACCENT_TEAL)

add_text_box(
    slide,
    Inches(0.8),
    Inches(0.4),
    Inches(11.5),
    Inches(0.6),
    "TOP 5 RISKS & MITIGATIONS",
    28,
    True,
    ACCENT_TEAL,
)

risks = [
    (
        "1",
        "Political/Policy Reversal",
        "Medium × Critical",
        "Multi-stakeholder MoUs; WB backing; portable architecture",
    ),
    (
        "2",
        "Data Access Delayed",
        "Medium × High",
        "Synthetic data pipeline; Common Voice fallback; legal escalation",
    ),
    (
        "3",
        "Model Quality Insufficient",
        "Medium × High",
        "Ensemble with English; human-in-loop; continuous eval",
    ),
    (
        "4",
        "Compute Cost Overrun",
        "High × Medium",
        "Reserved instances; model distillation; CPU fallback",
    ),
    (
        "5",
        "Farmer Adoption < Target",
        "Medium × High",
        "Co-design with farmers; community liaisons; voice-first UX",
    ),
]

y = Inches(1.3)
for num, risk, likelihood, mitigation in risks:
    # Number circle
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.8), y, Inches(0.5), Inches(0.5))
    circle.fill.solid()
    circle.fill.fore_color.rgb = (
        RED_RISK if "Critical" in likelihood or "High" in likelihood else ORANGE_WARN
    )
    circle.line.fill.background()
    tf = circle.text_frame
    tf.paragraphs[0].text = num
    tf.paragraphs[0].font.size = Pt(16)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = WHITE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    add_text_box(
        slide, Inches(1.5), y - Inches(0.02), Inches(4), Inches(0.5), risk, 18, True, WHITE
    )
    add_text_box(
        slide,
        Inches(5.5),
        y - Inches(0.02),
        Inches(2.5),
        Inches(0.5),
        likelihood,
        14,
        True,
        ORANGE_WARN,
    )
    add_text_box(
        slide,
        Inches(8.2),
        y - Inches(0.02),
        Inches(4.5),
        Inches(0.5),
        mitigation,
        14,
        False,
        LIGHT_GRAY,
    )
    y += Inches(0.7)

# Philosophy box
phil_box = add_shape_bg(
    slide, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.2), RGBColor(0x12, 0x2A, 0x50)
)
add_text_box(
    slide,
    Inches(1.2),
    Inches(5.4),
    Inches(11),
    Inches(1),
    "🛡️ RISK PHILOSOPHY: Speed to pilot (90 days) de-risks technical, adoption, and partner risks simultaneously.\nPortfolio approach: Multiple partners (OI, Govt, ZBS, Telcos) — no single point of failure.",
    15,
    False,
    WHITE,
    PP_ALIGN.LEFT,
)


# ============================================================
# SLIDE 11: GOVERNANCE & DECISION RIGHTS
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, DARK_NAVY)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.08), ACCENT_TEAL)

add_text_box(
    slide,
    Inches(0.8),
    Inches(0.4),
    Inches(11.5),
    Inches(0.6),
    "GOVERNANCE & DECISION RIGHTS",
    28,
    True,
    ACCENT_TEAL,
)

# Governance structure
gov_text = """
STEERING COMMITTEE (Monthly)     → Budget >$100k, Strategic pivots, Partner MSAs
  CEO (Chair) • CTO • COO • CLO • CSO • CFO • CoS
           │
PMO (Bi-weekly)                  → Sprint scope, Resources, Risk escalation
  CoS • PM • Workstream Leads
           │
├── TECH (CTO)     ├── BUSINESS (BD)     ├── PRODUCT (CPO)
├── LEGAL (CLO)    ├── RESEARCH (ML)     └── COMMS (CMO)
"""

add_text_box(
    slide,
    Inches(0.8),
    Inches(1.1),
    Inches(7),
    Inches(4.5),
    gov_text.strip(),
    14,
    False,
    WHITE,
    PP_ALIGN.LEFT,
    "Consolas",
)

# Gate reviews
add_text_box(
    slide,
    Inches(8),
    Inches(1.1),
    Inches(4.5),
    Inches(0.5),
    "GATE REVIEWS (CEO/Board)",
    18,
    True,
    ACCENT_GOLD,
)

gates = [
    ("GATE 1 (Day 30)", "OI MoU signed + ZBS NDA", "Release budget + hiring"),
    ("GATE 2 (Day 60)", "Technical feasibility confirmed", "Phase 2 go-ahead"),
    ("GATE 3 (Day 90)", "Pilot results reviewed", "Scale / Pivot / Pause + MSA negotiation"),
]

y = Inches(1.7)
for gate, condition, action in gates:
    add_text_box(slide, Inches(8), y, Inches(4.5), Inches(0.35), gate, 14, True, ACCENT_TEAL)
    add_text_box(
        slide,
        Inches(8),
        y + Inches(0.3),
        Inches(4.5),
        Inches(0.35),
        f"Trigger: {condition}",
        12,
        False,
        LIGHT_GRAY,
    )
    add_text_box(
        slide,
        Inches(8),
        y + Inches(0.55),
        Inches(4.5),
        Inches(0.35),
        f"Decision: {action}",
        12,
        False,
        WHITE,
    )
    y += Inches(1.0)


# ============================================================
# SLIDE 12: IMMEDIATE ACTIONS — THIS WEEK
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, DARK_NAVY)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.08), ACCENT_TEAL)

add_text_box(
    slide,
    Inches(0.8),
    Inches(0.4),
    Inches(11.5),
    Inches(0.6),
    "IMMEDIATE ACTIONS — THIS WEEK",
    28,
    True,
    ACCENT_TEAL,
)

actions = [
    ("1", "CEO calls: OI CEO, ZBS Director, WB Task Team Leader", "CEO/CoS", "Day 3"),
    ("2", "Tiger Team formed + charter signed", "CoS", "Day 3"),
    ("3", "Technical deep-dive with OI/Gooey.AI engineering", "CTO/Lead Backend", "Day 7"),
    ("4", "MoU templates drafted (OI, ZBS, Govt)", "CLO", "Day 7"),
    ("5", "Malawi visas + local counsel retained", "COO/Ops", "Day 10"),
    ("6", "GPU quota reserved (A100/H100)", "CTO/DevOps", "Day 10"),
    ("7", "GATE 1 TARGET: Signed OI JDA", "CEO/BD", "Day 30"),
]

y = Inches(1.3)
for num, action, owner, deadline in actions:
    # Number
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.8), y, Inches(0.4), Inches(0.4))
    circle.fill.solid()
    circle.fill.fore_color.rgb = ACCENT_TEAL
    circle.line.fill.background()
    tf = circle.text_frame
    tf.paragraphs[0].text = num
    tf.paragraphs[0].font.size = Pt(14)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = WHITE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    add_text_box(
        slide, Inches(1.4), y - Inches(0.02), Inches(7), Inches(0.4), action, 16, False, WHITE
    )
    add_text_box(
        slide,
        Inches(8.5),
        y - Inches(0.02),
        Inches(2),
        Inches(0.4),
        owner,
        14,
        False,
        ACCENT_GOLD,
        PP_ALIGN.RIGHT,
    )
    add_text_box(
        slide,
        Inches(10.5),
        y - Inches(0.02),
        Inches(1.8),
        Inches(0.4),
        deadline,
        14,
        True,
        WHITE,
        PP_ALIGN.RIGHT,
    )
    y += Inches(0.6)


# ============================================================
# SLIDE 13: 5-YEAR VISION
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, DARK_NAVY)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.08), ACCENT_TEAL)

add_text_box(
    slide,
    Inches(0.8),
    Inches(0.4),
    Inches(11.5),
    Inches(0.6),
    "THE VISION — BEYOND CHICHEWA",
    28,
    True,
    ACCENT_TEAL,
)

# Timeline
years = [
    ("YEAR 1", "Chichewa → 10K farmers → Malawi national platform", ACCENT_TEAL),
    ("YEAR 2", "+Tumbuka (2M) + Yao (2M) → 100K farmers → Regional platform", ACCENT_GOLD),
    ("YEAR 3", "+Sena, Lomwe, Bemba, Shona → 1M farmers → Continental platform", GREEN_GOOD),
    (
        "YEAR 5",
        "Agent Factory for 50+ African languages → $100M ARR potential",
        RGBColor(0x6F, 0x42, 0xC1),
    ),
]

for i, (year, desc, color) in enumerate(years):
    x = Inches(0.6 + i * 3.1)
    # Year badge
    badge = add_shape_bg(slide, x, Inches(1.5), Inches(2.8), Inches(0.6), color)
    add_text_box(
        slide, x, Inches(1.5), Inches(2.8), Inches(0.6), year, 20, True, WHITE, PP_ALIGN.CENTER
    )
    # Description
    desc_box = add_shape_bg(slide, x, Inches(2.2), Inches(2.8), Inches(2.5), MEDIUM_BLUE)
    add_text_box(
        slide,
        x + Inches(0.2),
        Inches(2.4),
        Inches(2.4),
        Inches(2.1),
        desc,
        15,
        False,
        WHITE,
        PP_ALIGN.CENTER,
    )
    # Arrow
    if i < 3:
        add_text_box(
            slide,
            x + Inches(2.8),
            Inches(2.5),
            Inches(0.4),
            Inches(0.4),
            "→",
            28,
            True,
            ACCENT_TEAL,
            PP_ALIGN.CENTER,
        )

# Vision statement
vision_box = add_shape_bg(
    slide, Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.5), RGBColor(0x12, 0x2A, 0x50)
)
add_text_box(
    slide,
    Inches(1.2),
    Inches(5.3),
    Inches(11),
    Inches(1.3),
    '🚀 WE BECOME THE "AWS FOR AFRICAN LANGUAGE AI" — THE ORCHESTRATION LAYER EVERYONE BUILDS ON.\n\nReplicable agent factory + multi-modal deployment + developer ecosystem = defensible platform moat.',
    18,
    True,
    WHITE,
    PP_ALIGN.CENTER,
)


# ============================================================
# SLIDE 14: DECISION REQUEST
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, DARK_NAVY)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.08), ACCENT_TEAL)

add_text_box(
    slide,
    Inches(0.8),
    Inches(0.4),
    Inches(11.5),
    Inches(0.6),
    "DECISION REQUESTED",
    28,
    True,
    ACCENT_TEAL,
)

# Main ask box
ask_box = add_shape_bg(slide, Inches(1), Inches(1.3), Inches(11.3), Inches(2.5), MEDIUM_BLUE)
add_text_box(
    slide,
    Inches(1.5),
    Inches(1.5),
    Inches(10.3),
    Inches(2.1),
    'Approve $4.4M / 12-month investment for "The Chichewa AI Initiative" as a strategic\nPlatform Partner engagement, authorizing Gate 1 execution (Week 1-4)\nwith go/no-go at Day 30.',
    24,
    True,
    WHITE,
    PP_ALIGN.CENTER,
)

# Options
add_text_box(
    slide,
    Inches(0.8),
    Inches(4.2),
    Inches(11.5),
    Inches(0.5),
    "OPTIONS FOR BOARD VOTE:",
    20,
    True,
    ACCENT_GOLD,
)

options = [
    ("✅ APPROVE", "Full engagement per this plan", GREEN_GOOD),
    ("✏️ APPROVE WITH MODIFICATIONS", "Specify: budget, scope, timeline, partners", ACCENT_TEAL),
    ("🧪 PILOT ONLY", "$1.5M / 6 months to Gate 2 (technical validation only)", ACCENT_GOLD),
    ("⏸️ DEFER", "Revisit in Q1 2027 with more market data", ORANGE_WARN),
    ("❌ DECLINE", "Not a strategic priority", RED_RISK),
]

y = Inches(4.8)
for label, desc, color in options:
    opt_box = add_shape_bg(
        slide, Inches(1), y, Inches(11.3), Inches(0.45), RGBColor(0x12, 0x2A, 0x50)
    )
    add_text_box(
        slide, Inches(1.2), y + Inches(0.02), Inches(3.5), Inches(0.4), label, 14, True, color
    )
    add_text_box(
        slide, Inches(4.8), y + Inches(0.02), Inches(7), Inches(0.4), desc, 14, False, LIGHT_GRAY
    )
    y += Inches(0.5)


# ============================================================
# SLIDE 15: THANK YOU / CONTACT
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, DARK_NAVY)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.08), ACCENT_TEAL)

add_text_box(
    slide,
    Inches(1),
    Inches(2.0),
    Inches(11),
    Inches(1),
    "THANK YOU",
    52,
    True,
    WHITE,
    PP_ALIGN.CENTER,
)

add_shape_bg(slide, Inches(4.5), Inches(3.2), Inches(4), Inches(0.04), ACCENT_GOLD)

add_text_box(
    slide,
    Inches(1.5),
    Inches(3.5),
    Inches(10),
    Inches(0.8),
    "Questions?  •  Deep-dive materials available  •  Appendix: Full risk register, financial model,\nlegal framework, competitive landscape, technical architecture",
    18,
    False,
    LIGHT_GRAY,
    PP_ALIGN.CENTER,
)

add_text_box(
    slide,
    Inches(1.5),
    Inches(5.0),
    Inches(10),
    Inches(0.5),
    "Prepared by: Chief of Staff  |  August 2026  |  CONFIDENTIAL",
    14,
    False,
    MEDIUM_GRAY,
    PP_ALIGN.CENTER,
)

add_text_box(
    slide,
    Inches(1.5),
    Inches(5.8),
    Inches(10),
    Inches(0.5),
    "Light Speed Holdings  •  AI Company Builder  •  lightspeed.ai",
    16,
    False,
    ACCENT_TEAL,
    PP_ALIGN.CENTER,
)


# ─── Save ───
output_path = "chichewa_ai_initiative.pptx"
prs.save(output_path)
print("Presentation saved to " + output_path)
print("Upload to Google Slides: File -> Import Slides -> Upload -> Select file")
