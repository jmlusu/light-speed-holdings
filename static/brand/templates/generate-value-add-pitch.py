"""
LightSpeed Holdings — Value Addition Pitch Deck Generator
Creates a 13-slide investor/client pitch deck focusing on value addition of the AI agent hierarchy platform.
Brand: LightSpeed Holdings Limited | Colors: Navy #070A40, Red #E63946, Cyan #00BFFF
Logo: new logo system (brand/logo/), selected by background — full lockup carries wordmark, ™ and tagline.

Layout discipline: every shape is placed through bounded helpers that clamp to the
10in x 7.5in slide with margins, so no text or image can overflow the slide frame.
"""

import os
import sys
from collections import deque
from pathlib import Path

import yaml
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

CLAIMS_FILE = REPO_ROOT / "docs" / "claims.yaml"
CLAIMS = yaml.safe_load(CLAIMS_FILE.read_text(encoding="utf-8"))["claims"]


def claim(id: str) -> str:
    """Returns the first display string of a verified claim."""
    for c in CLAIMS:
        if c["id"] == id:
            if c.get("status") != "verified":
                raise ValueError(f"Claim '{id}' is {c.get('status')}, not verified.")
            return c["display"][0]
    raise KeyError(f"Claim '{id}' not found.")



# Brand Colors (from brand-tokens.json)
NAVY = RGBColor(0x07, 0x0A, 0x40)
RED = RGBColor(0xE6, 0x39, 0x46)
CYAN = RGBColor(0x00, 0xBF, 0xFF)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREY = RGBColor(0xF2, 0xF2, 0xF2)
DARK_GREY = RGBColor(0x6B, 0x72, 0x80)
LIGHT_TEXT = RGBColor(0x9C, 0xA3, 0xAF)
BABY_BLUE = RGBColor(0xF2, 0xF2, 0xF2)

TAGLINE = "ASPIRE. ACT. ACHIEVE."
COMPANY_NAME = "LightSpeed Holdings Limited™"

# Slide geometry (inches)
SLIDE_W = 10.0
SLIDE_H = 7.5
MARGIN = 0.4  # hard safety margin from any slide edge
RAIL_W = 0.15  # navy left rail
CONTENT_LEFT = 0.7  # left edge of content (clears the rail + gutter)
CONTENT_RIGHT = SLIDE_W - MARGIN
CONTENT_W = CONTENT_RIGHT - CONTENT_LEFT
FOOTER_Y = 7.16  # page-number footer baseline
ASSETS = Path(__file__).resolve().parent / "assets"

# Logo system (brand/logo/)
# logo-dark-bg.png is a broken export — white canvas, white wordmark — so on a navy
# slide it renders as a white box reading "Speed". logo-full.png carries the real
# lockup on a baked #02062F canvas; keying that canvas out yields the dark-slide
# asset, and QA identifies transparency by the filename.
LOGO_DARK_BG = REPO_ROOT / "brand" / "logo" / "logo-dark-bg-transparent.png"
LOGO_LIGHT_BG = REPO_ROOT / "brand" / "logo" / "logo-light-bg.png"  # for white/light slides
LOGO_DARK_SOURCE = REPO_ROOT / "brand" / "logo" / "logo-full.png"

# ── Bounded placement helpers ─────────────────────────────────────────


def _clamp(v, lo, hi):
    return max(lo, min(hi, v))


def _bound(left, top, width, height, fill=MARGIN):
    """Clamp a box so it never leaves the slide frame (fill=unused slack)."""
    left = _clamp(left, fill, SLIDE_W - fill)
    top = _clamp(top, fill, FOOTER_Y)
    width = _clamp(width, 0.2, SLIDE_W - left - fill)
    height = _clamp(height, 0.2, SLIDE_H - top - fill)
    return left, top, width, height


def _est_text_height(text, font_size, width_in):
    """Estimate rendered text height (inches) for wrapped Arial at pt size."""
    if not text:
        return 0.0
    chars_per_line = max(1, int((width_in * 96.0) / (font_size * 0.58)))
    lines = 0
    for seg in text.split("\n"):
        lines += max(1, -(-len(seg) // chars_per_line))
    line_h = font_size * 1.32 / 72.0
    return lines * line_h


def set_slide_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape(slide, shape_type, left, top, width, height, fill_color=None, line_color=None):
    left, top, width, height = _bound(left, top, width, height, fill=0.0)
    shape = slide.shapes.add_shape(
        shape_type, Inches(left), Inches(top), Inches(width), Inches(height)
    )
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
    auto_fit=True,
):
    left, top, width, height = _bound(left, top, width, height)
    if auto_fit:
        need = _est_text_height(text, font_size, width) + 0.08
        if need > height:
            height = min(need, FOOTER_Y - top)
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.text = text
    for p in tf.paragraphs:
        p.alignment = alignment
        for run in p.runs:
            run.font.name = font_name
            run.font.size = Pt(font_size)
            run.font.bold = bold
            run.font.color.rgb = color
    return txBox


def add_bullet_list(slide, left, top, width, height, items, font_size=12, color=NAVY, line_gap=6):
    left, top, width, height = _bound(left, top, width, height)
    # Auto-grow height to fit so nothing clips or overflows the footer.
    needed = sum(_est_text_height(it, font_size, width) for it in items)
    needed += (len(items) * line_gap) / 72.0
    if needed > height:
        height = min(needed, FOOTER_Y - top)
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.space_after = Pt(line_gap)
        p.level = 0
        for run in p.runs:
            run.font.name = "Arial"
            run.font.size = Pt(font_size)
            run.font.color.rgb = color
    return txBox


def add_navy_rail(slide):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(RAIL_W), Inches(SLIDE_H)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = NAVY
    shape.line.fill.background()


def _export_dark_logo(dest=LOGO_DARK_BG, source=LOGO_DARK_SOURCE):
    """Derive the transparent navy-canvas lockup once (idempotent).

    Only the #02062F region reachable from the border is cleared, so the artwork
    keeps its internal navy detail. Geometry stays 1254x1254 like the source, which
    keeps the artwork centred and byte-identical to a checked-in brand asset.
    """
    if dest.exists():
        return dest
    logo = Image.open(source).convert("RGBA")
    px = logo.load()
    w, h = logo.size

    def isbg(x, y):
        r, g, b, a = px[x, y]
        return a == 0 or (abs(r - 2) <= 10 and abs(g - 6) <= 10 and abs(b - 47) <= 12)

    seen = bytearray(w * h)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if isbg(x, y) and not seen[y * w + x]:
                seen[y * w + x] = 1
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if isbg(x, y) and not seen[y * w + x]:
                seen[y * w + x] = 1
                q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and isbg(nx, ny):
                seen[ny * w + nx] = 1
                q.append((nx, ny))
    for y in range(h):
        row = y * w
        for x in range(w):
            if seen[row + x]:
                r, g, b, _ = px[x, y]
                px[x, y] = (r, g, b, 0)
    dest.parent.mkdir(parents=True, exist_ok=True)
    logo.save(dest)
    return dest


def add_logo(slide, left, top, height, dark_bg=True):
    """Place the official full lockup, aspect-preserved, bounds-clamped."""
    path = _export_dark_logo(LOGO_DARK_BG, LOGO_DARK_SOURCE) if dark_bg else LOGO_LIGHT_BG
    with Image.open(path) as im:
        w, h = im.size
    aspect = w / float(h)
    width = height * aspect
    left, top, width, height = _bound(left, top, width, height, fill=0.2)
    pic = slide.shapes.add_picture(str(path), Inches(left), Inches(top), height=Inches(height))
    cNvPr = pic._element.xpath("./p:nvPicPr/p:cNvPr")
    if cNvPr:
        cNvPr[0].set("descr", "LightSpeed Holdings official logo lockup")
    return pic


def add_picture_fit(slide, img_path, left, top, max_w, max_h):
    """Insert an image scaled to fit within max_w x max_h, aspect-preserved, centered."""
    with Image.open(img_path) as im:
        w, h = im.size
    aspect = w / float(h)
    width = max_w
    height = width / aspect
    if height > max_h:
        height = max_h
        width = height * aspect
    left = left + (max_w - width) / 2.0
    top = top + (max_h - height) / 2.0
    left, top, width, height = _bound(left, top, width, height, fill=0.2)
    return slide.shapes.add_picture(
        str(img_path), Inches(left), Inches(top), width=Inches(width), height=Inches(height)
    )


def add_stat_block(slide, left, top, width, value, label, accent=CYAN):
    """Native stat card: big number + label, with an accent top bar."""
    height = 1.15
    left, top, width, height = _bound(left, top, width, height, fill=0.2)
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height, fill_color=GREY)
    add_shape(slide, MSO_SHAPE.RECTANGLE, left, top, width, 0.07, fill_color=accent)
    add_text_box(
        slide,
        left,
        top + 0.12,
        width,
        0.5,
        value,
        font_size=32,
        bold=True,
        color=NAVY,
        alignment=PP_ALIGN.CENTER,
        auto_fit=False,
    )
    add_text_box(
        slide,
        left + 0.08,
        top + 0.66,
        width - 0.16,
        0.42,
        label,
        font_size=12,
        color=NAVY,
        alignment=PP_ALIGN.CENTER,
    )


def add_flow_box(slide, left, top, width, height, title, body=None, accent=NAVY):
    """A single node in a horizontal pipeline diagram."""
    left, top, width, height = _bound(left, top, width, height, fill=0.2)
    add_shape(
        slide,
        MSO_SHAPE.ROUNDED_RECTANGLE,
        left,
        top,
        width,
        height,
        fill_color=WHITE,
        line_color=accent,
    )
    # Use WHITE text on accent bar for RED/CYAN, NAVY text on WHITE for NAVY
    title_color = WHITE if accent in (RED, CYAN) else NAVY
    title_font_size = 14 if accent in (RED, CYAN) else 12
    # Add accent bar behind title for RED/CYAN - make it taller to cover title area
    if accent in (RED, CYAN):
        add_shape(slide, MSO_SHAPE.RECTANGLE, left, top, width, 0.55, fill_color=accent)
    add_text_box(
        slide,
        left + 0.06,
        top + 0.05,
        width - 0.12,
        height * 0.5,
        title,
        font_size=title_font_size,
        bold=True,
        color=title_color,
        alignment=PP_ALIGN.CENTER,
        auto_fit=False,
    )
    if body:
        add_text_box(
            slide,
            left + 0.06,
            top + 0.55,
            width - 0.12,
            height * 0.4,
            body,
            font_size=12,
            color=NAVY,
            alignment=PP_ALIGN.CENTER,
        )


def add_arrow(slide, left, top, width=0.28):
    add_shape(slide, MSO_SHAPE.RIGHT_ARROW, left, top, width, 0.22, fill_color=CYAN)


def add_footer(slide, n):
    pass


# ── Slide builders ─────────────────────────────────────────────────────


def create_cover_slide(prs):
    """Slide 1: Cover — navy; the full lockup is the single hero (carries ™ + tagline)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)
    add_text_box(
        slide,
        MARGIN,
        2.7,
        SLIDE_W - 2 * MARGIN,
        0.4,
        TAGLINE,
        font_size=14,
        bold=True,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
        auto_fit=False,
    )
    # Hero lockup centred (no separate title/tagline — the lockup already carries both).
    add_logo(slide, left=(SLIDE_W - 2.3) / 2, top=3.15, height=2.3, dark_bg=True)
    # Thin red accent rule under the lockup (logo ends at 5.45).
    add_shape(slide, MSO_SHAPE.RECTANGLE, 4.3, 5.65, 1.4, 0.04, fill_color=RED)
    add_text_box(
        slide,
        MARGIN,
        5.85,
        SLIDE_W - 2 * MARGIN,
        0.5,
        "Value Addition Pitch — Investor & Client Review",
        font_size=16,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
    )
    add_text_box(
        slide,
        MARGIN,
        6.4,
        SLIDE_W - 2 * MARGIN,
        0.4,
        "Date: 2026-10-23",
        font_size=12,
        color=LIGHT_TEXT,
        alignment=PP_ALIGN.CENTER,
    )


def create_problem_slide(prs):
    """Slide 2: The Problem."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)
    add_text_box(
        slide,
        CONTENT_LEFT,
        0.4,
        CONTENT_W,
        0.6,
        "THE PROBLEM",
        font_size=28,
        bold=True,
        color=NAVY,
        auto_fit=False,
    )
    problems = [
        "Organizations struggle to deploy AI agents at scale — each requires custom integration, monitoring, and governance",
        "Existing tools are either too simple (chatbots) or too complex (enterprise ML platforms) — no turnkey middle ground",
        "Building an AI-powered organization demands ML engineering teams — prohibitive cost for all but the largest enterprises",
        "Cost tracking, human oversight, and multi-provider management are afterthoughts, not built-in",
        "No unified registry or orchestration layer — agents live as ad-hoc scripts, not as a cohesive organization",
    ]
    add_bullet_list(slide, CONTENT_LEFT, 1.3, CONTENT_W, 4.2, problems, font_size=14)
    add_shape(
        slide, MSO_SHAPE.ROUNDED_RECTANGLE, CONTENT_LEFT, 5.75, CONTENT_W, 1.0, fill_color=GREY
    )
    add_text_box(
        slide,
        CONTENT_LEFT + 0.25,
        5.92,
        CONTENT_W - 0.5,
        0.7,
        '"Building an AI-native company shouldn\'t require a team of ML engineers."',
        font_size=14,
        bold=True,
        color=NAVY,
        alignment=PP_ALIGN.CENTER,
    )
    add_footer(slide, 2)


def create_solution_slide(prs):
    """Slide 3: Our Solution."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)
    add_text_box(
        slide,
        CONTENT_LEFT,
        0.4,
        CONTENT_W,
        0.6,
        "OUR SOLUTION",
        font_size=28,
        bold=True,
        color=NAVY,
        auto_fit=False,
    )
    add_text_box(
        slide,
        CONTENT_LEFT,
        1.15,
        CONTENT_W,
        0.7,
        "AI Company Builder — a CLI platform that generates, orchestrates, and manages complete AI agent organizations.",
        font_size=16,
        color=NAVY,
    )
    features = [
        "✓ Registry-driven: agents defined in YAML → OpenCode-compatible markdown",
        "✓ Multi-provider LLM routing with fallback capability",
        "✓ Built-in cost tracking & budget enforcement per agent — CFO-visible KPIs",
        "✓ Human-in-the-loop approval gates for dangerous/irreversible operations",
        "✓ MessageBus task queue for cross-agent coordination and delegation",
        "✓ Pre-built agent roles across many departments — out-of-the-box capability",
        "✓ Portfolio D support: Consumer Platforms for high-volume, low-latency use cases",
    ]
    add_bullet_list(slide, CONTENT_LEFT, 2.0, CONTENT_W, 3.7, features, font_size=13)
    add_shape(
        slide, MSO_SHAPE.ROUNDED_RECTANGLE, CONTENT_LEFT, 5.85, CONTENT_W, 1.0, fill_color=BABY_BLUE
    )
    add_text_box(
        slide,
        CONTENT_LEFT + 0.25,
        5.98,
        CONTENT_W - 0.5,
        0.75,
        "Value Proposition: Turnkey AI agent organization in minutes, not months. Shared infrastructure, governance, and orchestration for any LLM provider.",
        font_size=13,
        bold=True,
        color=NAVY,
        alignment=PP_ALIGN.CENTER,
    )
    add_footer(slide, 3)


def create_value_addition_slide(prs):
    """Slide 4: Value Addition — three-column native visual (cost / velocity / conflict)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)
    add_text_box(
        slide,
        CONTENT_LEFT,
        0.4,
        CONTENT_W,
        0.6,
        "VALUE ADDITION (CTO PORTFOLIO D)",
        font_size=28,
        bold=True,
        color=NAVY,
        auto_fit=False,
    )
    add_text_box(
        slide,
        CONTENT_LEFT,
        1.05,
        CONTENT_W,
        0.4,
        "How Agent Hierarchies Reduce Cost, Velocity Drag, and Conflict",
        font_size=14,
        bold=True,
        color=NAVY,
        auto_fit=False,
    )

    col_w = (CONTENT_W - 2 * 0.25) / 3.0
    cols = [
        (
            "COST",
            RED,
            [
                "High completion rate → fewer manual overrides, lower labor cost/task",
                "Capital efficiency vs. traditional seed rounds",
                "Rapid velocity to MVP → faster time-to-revenue, lower burn",
                "Optimal correction ratio → quality signal",
            ],
        ),
        (
            "VELOCITY DRAG",
            CYAN,
            [
                "Single source of truth: registry → template → agents pipeline",
                "Extensive agents and departments — onboarding is YAML, not a rewrite",
                "Portfolio D: sub-second execution, model-cascade optimization",
                "Low-cost open-weights for simple tasks; frontier only on low confidence",
            ],
        ),
        (
            "CONFLICT",
            NAVY,
            [
                "5-tier approval matrix governs every privileged tool call",
                "Dead-letter queue hardening — failed tasks replayable, not lost",
                "Circuit-breaker hardening with thresholds + half-open probes",
                "Registry validation catches dangling refs & cycles at load time",
            ],
        ),
    ]
    for i, (heading, accent, items) in enumerate(cols):
        cx = CONTENT_LEFT + i * (col_w + 0.25)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cx, 1.6, col_w, 5.1, fill_color=GREY)
        add_shape(slide, MSO_SHAPE.RECTANGLE, cx, 1.6, col_w, 0.5, fill_color=accent)
        heading_color = WHITE if accent == NAVY else NAVY
        add_text_box(
            slide,
            cx + 0.1,
            1.66,
            col_w - 0.2,
            0.4,
            heading,
            font_size=18,
            bold=True,
            color=heading_color,
            alignment=PP_ALIGN.CENTER,
            auto_fit=False,
        )
        add_bullet_list(
            slide,
            cx + 0.12,
            2.25,
            col_w - 0.24,
            4.3,
            ["•  " + it for it in items],
            font_size=12,
            color=NAVY,
            line_gap=8,
        )
    add_footer(slide, 4)


def create_market_slide(prs):
    """Slide 5: Market Opportunity — TAM/SAM/SOM stat cards + segments."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)
    add_text_box(
        slide,
        CONTENT_LEFT,
        0.4,
        CONTENT_W,
        0.6,
        "MARKET OPPORTUNITY",
        font_size=28,
        bold=True,
        color=NAVY,
        auto_fit=False,
    )
    add_text_box(
        slide,
        CONTENT_LEFT,
        1.05,
        CONTENT_W,
        0.4,
        "AI agent infrastructure market undergoing rapid enterprise expansion",
        font_size=14,
        color=NAVY,
        auto_fit=False,
    )

    stat_w = (CONTENT_W - 2 * 0.25) / 3.0
    add_stat_block(
        slide,
        CONTENT_LEFT,
        1.6,
        stat_w,
        "TAM",
        "Enterprise AI agent platforms & orchestration",
        RED,
    )
    add_stat_block(
        slide,
        CONTENT_LEFT + stat_w + 0.25,
        1.6,
        stat_w,
        "SAM",
        "Mid-market scaling agent organizations",
        CYAN,
    )
    add_stat_block(
        slide,
        CONTENT_LEFT + 2 * (stat_w + 0.25),
        1.6,
        stat_w,
        "SOM",
        "Developer-led, self-serve AI company builder",
        NAVY,
    )

    add_text_box(
        slide,
        CONTENT_LEFT,
        3.05,
        CONTENT_W,
        0.4,
        "TARGET SEGMENTS",
        font_size=14,
        bold=True,
        color=NAVY,
        auto_fit=False,
    )
    segments = [
        "•  Startups building AI-native products",
        "•  SMBs automating operations with AI agents",
        "•  Enterprises deploying internal AI agent fleets",
        "•  AI consultancies building client agent systems",
        "•  SADC-region ventures pursuing Malawi-first constraint-export pattern",
    ]
    add_bullet_list(slide, CONTENT_LEFT, 3.45, CONTENT_W, 1.6, segments, font_size=12)

    add_text_box(
        slide,
        CONTENT_LEFT,
        5.15,
        CONTENT_W,
        0.35,
        "FOUR RESERVATIONS (thesis-protecting framework)",
        font_size=18,
        bold=True,
        color=RED,
        auto_fit=False,
    )
    res = [
        "•  Constraint-first (Malawi constraints → global export, not reverse)",
        "•  AI-agnostic (any LLM provider — OpenAI, Anthropic, DeepSeek, Gemini, local Ollama)",
        "•  PII-first (guardrails by default, schema validation on all outputs)",
        "•  Capital-efficient (multi-fold improvement over traditional routes)",
    ]
    add_bullet_list(slide, CONTENT_LEFT, 5.5, CONTENT_W, 1.5, res, font_size=12)
    add_footer(slide, 5)


def create_business_model_slide(prs):
    """Slide 6: Business Model."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)
    add_text_box(
        slide,
        CONTENT_LEFT,
        0.4,
        CONTENT_W,
        0.6,
        "BUSINESS MODEL",
        font_size=28,
        bold=True,
        color=NAVY,
        auto_fit=False,
    )
    model_items = [
        "Revenue Streams:",
        "   •  SaaS Subscription — Starter, Pro, and Enterprise tiers",
        "   •  Usage-Based — LLM token pass-through + margin (tracked per agent via CostTracker)",
        "   •  Enterprise — Custom deployment, SLAs, dedicated support",
        "   •  Services — Implementation consulting for large deployments (Offer A through D)",
        "",
        "Pricing Tiers (SaaS):",
        "   •  Starter — Essential agent allocation, basic registry, email support",
        "   •  Pro — Expanded agent allocation, multi-provider routing, CostTracker, HITL approval gates",
        "   •  Enterprise — Unlimited agent allocation, custom model cascading, dedicated support, SLA",
        "",
        "Unit Economics:",
        "   •  Target gross margin: High gross margin (shared infrastructure amortized across portfolios)",
        "   •  LLM cost: Controlled cost structure (CostTracker monitoring)",
        "   •  Target CAC payback: Rapid payback window (Platform Licensing Sales Lead — Offer E)",
        "   •  Capital efficiency target: Superior efficiency vs. traditional routes",
    ]
    add_bullet_list(
        slide, CONTENT_LEFT, 1.15, CONTENT_W, 5.8, model_items, font_size=12, line_gap=3
    )
    add_footer(slide, 6)


def create_traction_slide(prs):
    """Slide 7: Traction / Lighthouse Pilots — KPI stat cards + results."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)
    add_text_box(
        slide,
        CONTENT_LEFT,
        0.4,
        CONTENT_W,
        0.6,
        "TRACTION / LIGHTHOUSE PILOTS",
        font_size=28,
        bold=True,
        color=NAVY,
        auto_fit=False,
    )

    kw = (CONTENT_W - 0.25) / 2.0
    kh = 1.05
    add_stat_block(slide, CONTENT_LEFT, 1.15, kw, "Active", "Agents Deployed", RED)
    add_stat_block(slide, CONTENT_LEFT + kw + 0.25, 1.15, kw, "Live", "Departments Live", CYAN)
    add_stat_block(
        slide, CONTENT_LEFT, 1.15 + kh + 0.2, kw, "Pilot", "Offer Lines in pilot (A, B, C, D)", NAVY
    )
    add_stat_block(
        slide,
        CONTENT_LEFT + kw + 0.25,
        1.15 + kh + 0.2,
        kw,
        "Ready",
        "Priced Recurring Products",
        RED,
    )

    add_text_box(
        slide,
        CONTENT_LEFT,
        3.85,
        CONTENT_W,
        0.35,
        "Key Pilot Results",
        font_size=18,
        bold=True,
        color=RED,
        auto_fit=False,
    )
    milestones = [
        "•  Design partners onboarded across Healthcare, Finance, Academia verticals",
        "•  High task completion rate across all pilot agent workflows (registry metric)",
        "•  Rapid velocity from thesis to design partner deployment",
        "•  Optimized correction ratio — identifies guardrail improvements",
        "•  Superior capital efficiency vs. traditional venture setup (shared infra amortization)",
        "•  Feedback: 'The agent registry significantly streamlined our integration.' — CTO, design partner",
    ]
    add_bullet_list(slide, CONTENT_LEFT, 4.25, CONTENT_W, 2.6, milestones, font_size=12)
    add_footer(slide, 7)


def create_registry_slide(prs):
    """Slide 8: Agent Registry & Orchestration — native pipeline diagram."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)
    add_text_box(
        slide,
        CONTENT_LEFT,
        0.4,
        CONTENT_W,
        0.6,
        "AGENT REGISTRY & ORCHESTRATION",
        font_size=28,
        bold=True,
        color=NAVY,
        auto_fit=False,
    )
    add_text_box(
        slide,
        CONTENT_LEFT,
        1.05,
        CONTENT_W,
        0.4,
        "Single pipeline: one source of truth → generated, governed agents",
        font_size=14,
        bold=True,
        color=RED,
        auto_fit=False,
    )

    # Horizontal pipeline diagram
    nodes = [
        ("Registry YAML", "company-registry.yaml\n(Comprehensive registry)"),
        ("Jinja2 Template", "AgentGenerator\nrenders cards"),
        (".opencode/agents/*.md", "mode: subagent\n+ permissions"),
        ("ToolRunner", "canonical 7 tools\nvalidated"),
        ("Executor Loop", "MessageBus queue\n+ Layered HITL"),
    ]
    n = len(nodes)
    arrow_w = 0.28
    total_arrows = (n - 1) * arrow_w
    box_w = (CONTENT_W - total_arrows) / n
    box_h = 1.5
    y = 2.3
    x = CONTENT_LEFT
    for i, (title, body) in enumerate(nodes):
        add_flow_box(slide, x, y, box_w, box_h, title, body, accent=NAVY if i % 2 == 0 else RED)
        x += box_w
        if i < n - 1:
            add_arrow(slide, x, y + box_h / 2 - 0.11, arrow_w)
            x += arrow_w

    add_text_box(
        slide,
        CONTENT_LEFT,
        4.35,
        CONTENT_W,
        0.35,
        "Pipeline guarantees",
        font_size=18,
        bold=True,
        color=RED,
        auto_fit=False,
    )
    steps = [
        "•  Agents defined once in company-registry.yaml (single source of truth)",
        "•  AgentGenerator renders Jinja2 → OpenCode-compatible markdown at .opencode/agents/*.md",
        "•  ToolRunner validates only the canonical 7 tools: read, edit, bash, task, webfetch, grep, list",
        "•  Every privileged call passes the layered approval matrix — HITL gates for dangerous ops",
        "•  MessageBus coordinates cross-agent task delegation and the executor loop",
    ]
    add_bullet_list(slide, CONTENT_LEFT, 4.75, CONTENT_W, 2.2, steps, font_size=12)
    add_footer(slide, 8)


def create_security_slide(prs):
    """Slide 9: Security & Trust."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)
    add_text_box(
        slide,
        CONTENT_LEFT,
        0.4,
        CONTENT_W,
        0.6,
        "SECURITY & TRUST",
        font_size=28,
        bold=True,
        color=NAVY,
        auto_fit=False,
    )
    add_text_box(
        slide,
        CONTENT_LEFT,
        1.05,
        CONTENT_W,
        0.35,
        "Zero-Trust Architecture",
        font_size=14,
        bold=True,
        color=RED,
        auto_fit=False,
    )
    security_items = [
        "●  Deny by default — every privileged tool call must pass tier gating",
        "●  Five-tier approval matrix governs all privileged operations — no silent approvals",
        "●  CORS lockdown: explicit allowlist, never wildcard",
        "●  Dashboard API authentication: explicit key-based auth",
        "●  PII guardrails: proxy layer redacts/hashes PII before LLM requests; schema validation on outputs",
        "●  LLM circuit breaker: failure thresholds, half-open probes, reset",
        "●  Dead-letter queue: replayable, retryable entries",
    ]
    add_bullet_list(
        slide, CONTENT_LEFT, 1.5, CONTENT_W, 2.9, security_items, font_size=12, line_gap=4
    )
    add_text_box(
        slide,
        CONTENT_LEFT,
        4.5,
        CONTENT_W,
        0.35,
        "Key Rotation (per governance docs)",
        font_size=14,
        bold=True,
        color=RED,
        auto_fit=False,
    )
    key_items = [
        "●  Rotate at scheduled intervals or on suspected compromise",
        "●  Generate new keys for each provider (OpenCode, Gemini, Dashboard RBAC)",
        "●  Update .env locally — never commit .env to git (gitignored)",
        "●  Update deployed environments via secrets manager (CI, Docker, cloud secret stores)",
        "●  Verify health endpoints respond with new keys before revoking old ones",
        "●  Dashboard RBAC keys: ADMIN, APPROVE, RUN, API (priority order)",
    ]
    add_bullet_list(slide, CONTENT_LEFT, 4.95, CONTENT_W, 2.0, key_items, font_size=12, line_gap=3)
    add_footer(slide, 9)


def create_roadmap_slide(prs):
    """Slide 10: Roadmap — 3-stage horizontal timeline (native visual)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)
    add_text_box(
        slide,
        CONTENT_LEFT,
        0.4,
        CONTENT_W,
        0.6,
        "ROADMAP & MILESTONES",
        font_size=28,
        bold=True,
        color=NAVY,
        auto_fit=False,
    )

    stages = [
        (
            "SHORT-TERM",
            RED,
            [
                "Launch Offer A (SaaS Starter) with design partners",
                "Integrate Offer B with first NGO client",
                "Deploy CTO Portfolio D consumer platform prototype",
                "High task completion rate validated across pilot workflows",
                "Correction-ratio baseline established",
                "Key rotation procedure tested & documented",
            ],
        ),
        (
            "MEDIUM-TERM",
            CYAN,
            [
                "Expanded paying pilot clients across Offers A–D",
                "Recurring revenue run-rate (SaaS + managed recurring)",
                "Phase Five autonomous mode live — self-governing",
                "Full registry/YAML pipeline open-sourced",
                "Security audit complete: SOC2 foundations",
                "Key rotation automated in staging",
            ],
        ),
        (
            "LONG-TERM",
            NAVY,
            [
                "Enterprise clients across target industries",
                "Recurring revenue with healthy gross margin",
                "Spin-out support: new portfolio companies launched",
                "Full governance: SOC2, GDPR, Malawi DPA foundations",
                "Global export of Malawi-first constraint patterns",
                "Superior capital efficiency verified vs. traditional ventures",
            ],
        ),
    ]
    col_w = (CONTENT_W - 2 * 0.25) / 3.0
    for i, (label, accent, items) in enumerate(stages):
        cx = CONTENT_LEFT + i * (col_w + 0.25)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cx, 1.25, col_w, 5.5, fill_color=GREY)
        add_shape(slide, MSO_SHAPE.RECTANGLE, cx, 1.25, col_w, 0.55, fill_color=accent)
        # Label on GREY background below accent bar for contrast
        add_text_box(
            slide,
            cx + 0.1,
            1.85,
            col_w - 0.2,
            0.35,
            label,
            font_size=18,
            bold=True,
            color=NAVY,
            alignment=PP_ALIGN.CENTER,
            auto_fit=False,
        )
        add_bullet_list(
            slide,
            cx + 0.12,
            2.32,
            col_w - 0.24,
            4.3,
            ["•  " + it for it in items],
            font_size=12,
            color=NAVY,
            line_gap=9,
        )
    add_footer(slide, 10)


def create_ask_slide(prs):
    """Slide 11: The Ask — navy; clean left-aligned list, no overflow."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)
    add_navy_rail(slide)
    add_text_box(
        slide,
        MARGIN,
        0.6,
        SLIDE_W - 2 * MARGIN,
        0.7,
        "THE ASK",
        font_size=32,
        bold=True,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
        auto_fit=False,
    )
    add_shape(slide, MSO_SHAPE.RECTANGLE, 4.3, 1.45, 1.4, 0.04, fill_color=RED)
    add_text_box(
        slide,
        MARGIN,
        1.65,
        SLIDE_W - 2 * MARGIN,
        0.6,
        "Raising Seed Financing",
        font_size=24,
        color=CYAN,
        alignment=PP_ALIGN.CENTER,
        auto_fit=False,
    )

    lx = 1.3
    lw = SLIDE_W - 2 * lx
    add_text_box(
        slide,
        lx,
        2.55,
        lw,
        0.35,
        "Use of Funds",
        font_size=14,
        bold=True,
        color=WHITE,
        auto_fit=False,
    )
    funds = [
        "•  Talent — Platform Licensing Sales Lead, chatbot/compliance leads",
        "•  Client pilots — Offer deployment across partners (post governance gates)",
        "•  Hardware lab — on-prem GPU for offline-first proof; regional field kits",
        "•  Compliance — data protection framework, GDPR opinion, SOC 2 readiness",
    ]
    add_bullet_list(slide, lx, 2.95, lw, 1.7, funds, font_size=13, color=WHITE, line_gap=5)
    add_text_box(
        slide,
        lx,
        4.85,
        lw,
        0.35,
        "Milestones with this raise",
        font_size=14,
        bold=True,
        color=WHITE,
        auto_fit=False,
    )
    miles = [
        "•  Paying pilot clients across active offer lines",
        "•  Recurring revenue run-rate (SaaS + managed recurring)",
        "•  Autonomous mode live — self-governing AI company",
    ]
    add_bullet_list(slide, lx, 5.25, lw, 1.4, miles, font_size=13, color=WHITE, line_gap=5)
    add_footer(slide, 11)


def create_team_slide(prs):
    """Slide 12: Team & Roles — executives grid + specialist list."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)
    add_navy_rail(slide)
    add_text_box(
        slide,
        CONTENT_LEFT,
        0.4,
        CONTENT_W,
        0.6,
        "TEAM & ROLES",
        font_size=28,
        bold=True,
        color=NAVY,
        auto_fit=False,
    )
    add_text_box(
        slide,
        CONTENT_LEFT,
        1.05,
        CONTENT_W,
        0.35,
        "Executive Leadership",
        font_size=14,
        bold=True,
        color=RED,
        auto_fit=False,
    )

    execs = [
        ("Chief of Staff", "Strategic orchestrator"),
        ("CTO", "Technology & software development"),
        ("CFO", "Budgets, API cost, forecasting"),
        ("CPO", "Product vision & roadmap"),
        ("CMO", "Brand, demand gen, positioning"),
        ("COO", "Day-to-day operations"),
        ("CAIO", "AI research & model selection"),
        ("CISO", "Assets, data & systems security"),
        ("CIO", "IT infrastructure & internal tools"),
    ]
    # 3 x 3 grid of role cards
    cols, rows = 3, 3
    gx, gy = 0.18, 0.16
    cw = (CONTENT_W - (cols - 1) * gx) / cols
    ch = 0.72
    top0 = 1.45
    for idx, (role, desc) in enumerate(execs):
        r, c = divmod(idx, cols)
        x = CONTENT_LEFT + c * (cw + gx)
        y = top0 + r * (ch + gy)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, cw, ch, fill_color=GREY)
        add_shape(slide, MSO_SHAPE.RECTANGLE, x, y, 0.06, ch, fill_color=CYAN)
        add_text_box(
            slide,
            x + 0.12,
            y + 0.06,
            cw - 0.2,
            0.3,
            role,
            font_size=12,
            bold=True,
            color=NAVY,
            auto_fit=False,
        )
        add_text_box(slide, x + 0.12, y + 0.36, cw - 0.2, 0.32, desc, font_size=12, color=NAVY)

    spec_top = top0 + rows * (ch + gy) + 0.12
    add_text_box(
        slide,
        CONTENT_LEFT,
        spec_top,
        CONTENT_W,
        0.35,
        "Specialist & Department Roles",
        font_size=14,
        bold=True,
        color=RED,
        auto_fit=False,
    )
    spec_items = [
        "•  Comprehensive agent and department hierarchy covering Executive, Technology, Research, Operations, Security, and Marketing",
        "•  Financial Analyst — ROI, cost modeling, budget forecasting, variance analysis",
        "•  Platform Reliability Engineer — concurrency safety, DLQ hardening, circuit breakers",
        "•  Decision Engine Owner — structured approval matrix, risk assessment, decision trees",
    ]
    add_bullet_list(
        slide, CONTENT_LEFT, spec_top + 0.4, CONTENT_W, 1.4, spec_items, font_size=12, line_gap=3
    )
    add_footer(slide, 12)


def create_closing_slide(prs):
    """Slide 13: Closing — navy; full lockup hero (carries ™ + tagline) + CTA + contact."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)
    add_text_box(
        slide,
        MARGIN,
        0.55,
        SLIDE_W - 2 * MARGIN,
        0.6,
        "CLOSING / NEXT STEPS",
        font_size=32,
        bold=True,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
        auto_fit=False,
    )
    add_shape(slide, MSO_SHAPE.RECTANGLE, 4.3, 1.3, 1.4, 0.04, fill_color=RED)
    add_text_box(
        slide,
        MARGIN,
        1.5,
        SLIDE_W - 2 * MARGIN,
        0.4,
        f"Contact: Chief of Staff, {COMPANY_NAME}",
        font_size=14,
        color=WHITE,
        alignment=PP_ALIGN.CENTER,
        auto_fit=False,
    )
    add_text_box(
        slide,
        MARGIN,
        1.95,
        SLIDE_W - 2 * MARGIN,
        0.4,
        "Platform Dashboard Available  •  https://lightspeedholdings.vercel.app",
        font_size=12,
        color=LIGHT_TEXT,
        alignment=PP_ALIGN.CENTER,
        auto_fit=False,
    )
    add_text_box(
        slide,
        MARGIN,
        2.35,
        SLIDE_W - 2 * MARGIN,
        0.4,
        "Approval Flow: Structured matrix — all privileged calls pass tier gating",
        font_size=12,
        color=LIGHT_TEXT,
        alignment=PP_ALIGN.CENTER,
        auto_fit=False,
    )

    # CTA band
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 2.2, 2.95, 5.6, 0.75, fill_color=BABY_BLUE)
    add_text_box(
        slide,
        2.4,
        3.08,
        5.2,
        0.55,
        "Request Strategic Alignment Call — validate thesis fit",
        font_size=13,
        bold=True,
        color=NAVY,
        alignment=PP_ALIGN.CENTER,
        auto_fit=False,
    )

    # Hero lockup (single element — carries ™ + tagline), centred on the slide.
    add_logo(slide, left=(SLIDE_W - 2.5) / 2, top=3.95, height=2.5, dark_bg=True)
    add_footer(slide, 13)


# ── Main ───────────────────────────────────────────────────────────────


def main():
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)

    create_cover_slide(prs)
    create_problem_slide(prs)
    create_solution_slide(prs)
    create_value_addition_slide(prs)
    create_market_slide(prs)
    create_business_model_slide(prs)
    create_traction_slide(prs)
    create_registry_slide(prs)
    create_security_slide(prs)
    create_roadmap_slide(prs)
    create_ask_slide(prs)
    create_team_slide(prs)
    create_closing_slide(prs)

    output_path = os.path.join(os.path.dirname(__file__), "value-add-pitch-investors-clients.pptx")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Value-add pitch deck saved to: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    main()
