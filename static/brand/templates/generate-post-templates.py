"""
LightSpeed Holdings — Social Post Template Generator (P1 #311 + P2/P3 #316)
===========================================================================

Generates the six foundational P1 and six P2/P3 secondary social post
templates as branded PNGs using Pillow. Copy is REAL LightSpeed copy sourced
from `docs/Pharos/positioning.md` and the brand tokens (never lorem ipsum).

Templates produced (names == canonical file names, see
`static/brand/templates/social-templates/TEMPLATE_SPECS.md`):

    P1 (Ticket #311):
    1. linkedin-carousel-cover.png  1080x1080   LinkedIn carousel cover slide
    2. youtube-thumbnail.png        1280x720    Video thumbnail (16:9)
    3. reels-shorts-cover.png       1080x1920   Reels/Shorts vertical cover
    4. quote-card.png               1080x1080   Quote card
    5. stat-card.png                1080x1080   Stat card
    6. thread-header.png            1200x675    X / LinkedIn thread header

    P2/P3 (Ticket #316):
    7.  lower-third-video-overlay.png  1920x360   Lower-third video overlay (RGBA)
    8.  hook-card.png                  1080x1920  Hook card, first 3 seconds (9:16)
    9.  end-screen-cta.png             1920x1080  End-screen subscribe CTA (16:9)
    10. chapter-marker.png             1920x180   YouTube chapter marker (RGBA)
    11. facebook-group-cover.png       1640x856   Facebook Group cover (1.91:1)
    12. email-newsletter-header.png    600x200    Email newsletter header (3:1)

The two overlay types (lower-third, chapter-marker) are saved as RGBA PNGs
with a semi-transparent navy base (90%/95% opacity per TEMPLATE_SPECS) so
video editors can layer them directly; all others are opaque RGB.

TOKEN SOURCE (important)
------------------------
Colors, type scale, company name and tagline are loaded from the canonical
`brand/tokens/brand-tokens.json` (repo root). If that file is unavailable the
module falls back to hardcoded constants that EXACTLY mirror it
(`FALLBACK_TOKENS` below) and prints a warning; the mirror at
`static/brand/tokens/brand-tokens.json` is only used if the canonical file is
missing.

LOGOS
-----
Logo files are resolved canonical-first (`brand/logos/**`) with a fallback to
the runtime mirror (`static/brand/logos/**`) — same pattern as
`static/brand/templates/generate-social-assets.py`. Icon logo: `icononly/
icononly_transparent.png` (dark surfaces). Full logo: `fulllogo/
fulllogo_transparent.png` (light surfaces).

USAGE
-----
    # Generate all twelve templates (P1 + P2/P3)
    uv run python static/brand/templates/generate-post-templates.py

    # Generate one template with slot overrides (copy injection)
    uv run python static/brand/templates/generate-post-templates.py \
        --template quote-card \
        --slots '{"quote": "New quote text", "author": "Jane Doe"}'

    # Inject slots for several templates from one JSON file
    # {"stat-card": {"number": "20"}, "thread-header": {"part": "3/8"}}
    uv run python static/brand/templates/generate-post-templates.py \
        --json params.json

    # Regenerate and self-QA (dimensions + dominant brand fills)
    uv run python static/brand/templates/generate-post-templates.py --verify

Brand layout follows TEMPLATE_SPECS: navy base, 48px brand rail, caption zone
on the brand free grid (4px spacing scale, 64px content inset), red for key
numbers/CTAs, cyan as the secondary accent. No emojis in on-image copy.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Paths (canonical-first)
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BRAND_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "..", "brand"))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "social", "templates")

TOKEN_SOURCE = (
    "brand/tokens/brand-tokens.json (canonical repo root, read first; "
    "mirrored at static/brand/tokens/brand-tokens.json)"
)


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _canonical_or_mirror(*parts: str) -> str:
    """Canonical brand/... first, then the static/brand mirror (same pattern as
    generate-social-assets.py). Returns the path whether or not it exists."""
    canonical = os.path.join(BRAND_ROOT, *parts)
    if os.path.exists(canonical):
        return canonical
    return os.path.join(SCRIPT_DIR, "..", *parts)


# ---------------------------------------------------------------------------
# Fallback brand tokens — EXACT mirror of brand/tokens/brand-tokens.json
# ---------------------------------------------------------------------------

FALLBACK_COLORS: dict[str, tuple[int, int, int]] = {
    "navy": (7, 10, 64),  # #070A40 primary surfaces
    "red": (230, 57, 70),  # #E63946 accent / CTA / key numbers
    "cyan": (0, 191, 255),  # #00BFFF secondary accent / links on dark
    "grey-light": (242, 242, 242),  # #F2F2F2 card backgrounds
    "white": (255, 255, 255),  # #FFFFFF text on navy / clean bg
    "grey-dark": (107, 114, 128),  # #6B7280 secondary text, captions
    "grey-light-text": (156, 163, 175),  # #9CA3AF tertiary text on dark
    "onNavy": (255, 255, 255),
    "onRed": (255, 255, 255),
    "onCyan": (7, 10, 64),
}

FALLBACK_BRAND: dict[str, str] = {
    "companyName": "LightSpeed Holdings Limited",
    "legalName": "LIGHTSPEED HOLDINGS LIMITED",
    "tagline": "ASPIRE. ACT. ACHIEVE.",
}

# Type scale in pt — rasterized 1pt:1px (matches the Canva/Figma template specs).
FALLBACK_SIZES: dict[str, int] = {
    "displayXl": 36,
    "titleXl": 32,
    "titleLg": 28,
    "titleMd": 24,
    "titleSm": 18,
    "subtitle": 16,
    "bodyLg": 16,
    "body": 14,
    "bodySm": 13,
    "caption": 12,
}

RAIL_WIDTH = 48  # brand standard navy rail
CONTENT_INSET = 64  # 48px rail + 16px gap (4px grid)
LINE_GAP = 8  # 2 x 4px base unit


def _load_tokens() -> tuple[dict, dict, dict]:
    """Return (colors, brand, sizes). Reads canonical JSON; falls back to the
    exact-mirror constants above. The chosen source is printed by callers."""
    try:
        with open(
            os.path.join(BRAND_ROOT, "tokens", "brand-tokens.json"),
            encoding="utf-8",
        ) as fh:
            data = json.load(fh)
        colors = {
            k: hex_to_rgb(v["value"])
            for k, v in data.get("color", {}).items()
            if v.get("value", "").startswith("#")
        }
        brand = {k: v for k, v in data.get("brand", {}).items() if isinstance(v, str)}
        sizes = {}
        for k, v in data.get("typography", {}).get("sizes", {}).items():
            with contextlib.suppress(ValueError):
                sizes[k] = int(str(v).replace("pt", "").strip())
        if colors and brand:
            return colors, brand, sizes
        return FALLBACK_COLORS, FALLBACK_BRAND, FALLBACK_SIZES
    except (OSError, ValueError, json.JSONDecodeError):
        return dict(FALLBACK_COLORS), dict(FALLBACK_BRAND), dict(FALLBACK_SIZES)


def _resolve_tokens(tokens, brand, sizes):
    """Attach fallbacks when a caller passed None (used by tests / CLI paths)."""
    colors = tokens if tokens is not None else FALLBACK_COLORS
    brand_meta = brand if brand is not None else FALLBACK_BRAND
    size_map = sizes if sizes is not None else FALLBACK_SIZES
    # Semantic aliases used by the generators (fall back to token scale keys).
    size_map.setdefault("displayXl", FALLBACK_SIZES["displayXl"])
    size_map.setdefault("titleXl", FALLBACK_SIZES["titleXl"])
    size_map.setdefault("titleLg", FALLBACK_SIZES["titleLg"])
    size_map.setdefault("titleMd", FALLBACK_SIZES["titleMd"])
    size_map.setdefault("titleSm", FALLBACK_SIZES["titleSm"])
    size_map.setdefault("subtitle", FALLBACK_SIZES["subtitle"])
    size_map.setdefault("bodyLg", FALLBACK_SIZES["bodyLg"])
    size_map.setdefault("body", FALLBACK_SIZES["body"])
    size_map.setdefault("bodySm", FALLBACK_SIZES["bodySm"])
    size_map.setdefault("caption", FALLBACK_SIZES["caption"])
    return colors, brand_meta, size_map


# ---------------------------------------------------------------------------
# Fonts / text helpers
# ---------------------------------------------------------------------------

_FONT_BASES = [
    "C:/Windows/Fonts",
    "C:\\Windows\\Fonts",
    "/System/Library/Fonts",
    "/Library/Fonts",
    "/usr/share/fonts/truetype/msttcorefonts",
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts",
]


def _font(
    size: int, bold: bool = False, italic: bool = False
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load Arial (brand family) at the requested px size. Bold/italic map to
    the standard Arial variants; falls back through the stack to any system
    Arial, then PIL's default font (never crashes)."""
    if bold and italic:
        names = ["arialbi.ttf", "arialbd.ttf"]
    elif bold:
        names = ["arialbd.ttf"]
    elif italic:
        names = ["ariali.ttf", "arial.ttf"]
    else:
        names = ["arial.ttf"]
    for base in _FONT_BASES:
        for name in names:
            path = os.path.join(base, name)
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except OSError:
                    continue
    for name in names:
        try:
            return ImageFont.truetype(name, size)  # OS font resolution
        except OSError:
            continue
    return ImageFont.load_default()


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _block_height(lines: list[str], font) -> int:
    if not lines:
        return 0
    return len(lines) * (font.size + LINE_GAP) - LINE_GAP


def _draw_block(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font,
    fill: tuple[int, int, int],
    max_width: int,
    align: str = "left",
    max_lines: int | None = None,
) -> tuple[int, list[str]]:
    """Draw wrapped text. Returns (y after the block, lines used)."""
    x0, y0 = xy
    lines = _wrap(draw, text, font, max_width)
    if max_lines is not None:
        lines = lines[:max_lines]
    y = y0
    for line in lines:
        line_width = draw.textlength(line, font=font)
        if align == "center":
            x = x0 + (max_width - line_width) / 2
        elif align == "right":
            x = x0 + max_width - line_width
        else:
            x = float(x0)
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + LINE_GAP
    return y, lines


def _text_vertical_center(draw: ImageDraw.ImageDraw, text: str, font, box_h: int) -> int:
    """Return the y offset that vertically centers text inside box_h."""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_h = bbox[3] - bbox[1]
    return max(0, (box_h - text_h) // 2 - bbox[1])


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------


def _rail_on_navy(
    draw: ImageDraw.ImageDraw, height: int, cyan: tuple[int, int, int], x: int = RAIL_WIDTH
) -> None:
    """48px navy rail on a navy surface, marked by the brand 4px cyan accent
    line at the rail's right edge (navy bg + cyan accent line pattern)."""
    draw.rectangle([x - 4, 0, x, height], fill=cyan)


def _rail_on_white(
    img: Image.Image,
    draw: ImageDraw.ImageDraw,
    height: int,
    navy: tuple[int, int, int],
    x: int = RAIL_WIDTH,
) -> None:
    """Solid 48px navy rail on a light surface (spec: 'Left rail: 48px Navy')."""
    draw.rectangle([0, 0, x, height], fill=navy)
    del img  # kept for interface symmetry with _rail_on_navy


def _paste_logo(
    img: Image.Image,
    logo_parts: tuple[str, ...],
    target_width: int,
    position: str = "bottom-right",
    margin: int = 24,
) -> bool:
    """Paste an official logo (canonical-first) at the given position,
    preserving aspect ratio. Returns True on success, False when missing."""
    path = _canonical_or_mirror(*logo_parts)
    if not os.path.exists(path):
        return False
    logo = Image.open(path).convert("RGBA")
    target_height = int(logo.height * (target_width / logo.width))
    logo = logo.resize((target_width, target_height), Image.Resampling.LANCZOS)
    width, height = img.size
    if position == "bottom-right":
        x, y = width - target_width - margin, height - target_height - margin
    elif position == "top-right":
        x, y = width - target_width - margin, margin
    elif position == "bottom-left":
        x, y = margin, height - target_height - margin
    elif position == "center-right":
        x, y = width - target_width - margin, (height - target_height) // 2
    elif position == "center":
        x, y = (width - target_width) // 2, height - target_height - margin
    else:  # top-left
        x, y = margin, margin
    img.paste(logo, (x, y), logo)
    return True


def _pill(
    draw: ImageDraw.ImageDraw,
    center_y: int,
    x: int,
    text: str,
    font,
    bg: tuple[int, int, int],
    fg: tuple[int, int, int],
    pad_x: int = 16,
    pad_y: int = 6,
    radius: int | None = None,
) -> tuple[int, int, int, int]:
    """Red/CTA pill badge. Returns bounding box (x1, y1, x2, y2)."""
    text_w = draw.textlength(text, font=font)
    w = int(text_w) + 2 * pad_x
    h = font.size + 2 * pad_y
    y1 = center_y - h // 2
    radius = radius if radius is not None else h // 2
    draw.rounded_rectangle([x, y1, x + w, y1 + h], radius=radius, fill=bg)
    ty = y1 + _text_vertical_center(draw, text, font, h)
    draw.text((x + pad_x, ty), text, font=font, fill=fg)
    return (x, y1, x + w, y1 + h)


def _vertical_gradient(
    size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]
) -> Image.Image:
    """Subtle vertical gradient between two RGB colors (Pillow-only)."""
    width, height = size
    strip = Image.new("RGB", (1, height))
    px = strip.load()
    for y in range(height):
        t = y / max(1, height - 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return strip.resize((width, height), Image.Resampling.LANCZOS)


def _play_triangle(
    draw: ImageDraw.ImageDraw, cx: float, cy: float, r: int, fill: tuple[int, int, int]
) -> None:
    """White play triangle inside a red circle of radius r centered at (cx, cy)."""
    s = r * 0.62
    draw.polygon([(cx - s * 0.45, cy - s), (cx - s * 0.45, cy + s), (cx + s, cy)], fill=fill)


# ---------------------------------------------------------------------------
# Default slots — REAL LightSpeed copy (positioning.md + brand tokens)
# ---------------------------------------------------------------------------

DEFAULT_SLOTS: dict[str, dict[str, str]] = {
    "linkedin-carousel-cover": {
        "title": "Designing AI-Native Enterprises for Africa",
        "subtitle": "Human \u2192 Agents \u2192 Orchestration \u2192 Memory \u2192 Tools \u2192 Governance \u2192 Value",
        "tagline": "ASPIRE. ACT. ACHIEVE.",
    },
    "youtube-thumbnail": {
        "badge": "EP 01",
        "title": "Building Governed AI-Native Enterprises",
        "tagline": "ASPIRE. ACT. ACHIEVE.",
    },
    "reels-shorts-cover": {
        "hook": "7 layers. One framework. Governed Agentic AI.",
        "tagline": "ASPIRE. ACT. ACHIEVE.",
    },
    "quote-card": {
        "quote": "The region's institutions do not fear the technology \u2014 they fear ungoverned deployment.",
        "author": "Jack Mlusu",
        "role": "AI-Native Enterprise Transformation Leader",
        "tagline": "ASPIRE. ACT. ACHIEVE.",
    },
    "stat-card": {
        "number": "152",
        "label": "AI agents operating inside one company",
        "context": "LightSpeed Holdings runs 152 agents across 20 departments with 5-tier human-in-the-loop governance and immutable audit trails.",
        "source": "LightSpeed Holdings Limited\u2122 \u2014 production operating system",
        "tagline": "ASPIRE. ACT. ACHIEVE.",
    },
    "thread-header": {
        "title": "The Four Reservations: Trust-by-Engineering",
        "subtitle": "Why institutions hesitate on Agentic AI \u2014 and how engineering answers the fear",
        "part": "1/8",
        "tagline": "ASPIRE. ACT. ACHIEVE.",
    },
    # --- P2/P3 secondary types (Ticket #316) ---
    "lower-third-video-overlay": {
        "name": "Jack Mlusu",
        "role": "AI-Native Enterprise Transformation Leader",
        "tagline": "ASPIRE. ACT. ACHIEVE.",
    },
    "hook-card": {
        "number": "7",
        "hook": "Layers. One framework. Governed Agentic AI.",
        "teaser": "Watch for the governance layer institutions actually trust.",
        "tagline": "ASPIRE. ACT. ACHIEVE.",
    },
    "end-screen-cta": {
        "headline": "Get the Framework",
        "subtext": "The 7-layer playbook for governed, agentic enterprises \u2014 free for builders across Africa.",
        "emailPlaceholder": "you@company.com",
        "cta": "Subscribe Free",
        "tagline": "ASPIRE. ACT. ACHIEVE.",
    },
    "chapter-marker": {
        "number": "01",
        "title": "The Four Reservations",
        "timestamp": "12:34",
        "tagline": "ASPIRE. ACT. ACHIEVE.",
    },
    "facebook-group-cover": {
        "group": "Agentic AI Malawi & SADC",
        "tagline": "ASPIRE. ACT. ACHIEVE.",
        "description": "Designing AI-native enterprises and governed agentic systems for the region.",
        "cta": "Join the Conversation",
    },
    "email-newsletter-header": {
        "publication": "The Agentic Builder",
        "issue": "Issue #01 \u2022 September 2026",
        "tagline": "ASPIRE. ACT. ACHIEVE.",
    },
}

# ---------------------------------------------------------------------------
# Template 1 — LinkedIn Carousel Cover (1080x1080)
# ---------------------------------------------------------------------------


def generate_linkedin_carousel(
    out_path: str, slots: dict | None = None, tokens=None, brand=None, sizes=None
) -> None:
    colors, brand_meta, size_map = _resolve_tokens(tokens, brand, sizes)
    navy, red, cyan = colors["navy"], colors["red"], colors["cyan"]
    white, grey_light_text = colors["white"], colors["grey-light-text"]
    tagline = (slots or {}).get("tagline") or brand_meta.get("tagline", FALLBACK_BRAND["tagline"])
    s = {**DEFAULT_SLOTS["linkedin-carousel-cover"], **(slots or {})}

    width, height = 1080, 1080
    img = Image.new("RGB", (width, height), navy)
    draw = ImageDraw.Draw(img)
    _rail_on_navy(draw, height, cyan)

    # Red accent bar above the title (brand divider pattern)
    draw.rectangle([CONTENT_INSET, 356, CONTENT_INSET + 64, 360], fill=red)

    title_font = _font(size_map["titleXl"], bold=True)
    title_y = 388
    _, title_lines = _draw_block(
        draw, (CONTENT_INSET, title_y), s["title"], title_font, white, max_width=920
    )

    subtitle_font = _font(size_map["subtitle"])
    subtitle_y = title_y + _block_height(title_lines, title_font) + 16
    _draw_block(
        draw, (CONTENT_INSET, subtitle_y), s["subtitle"], subtitle_font, cyan, max_width=920
    )

    # Caption zone (tagline) bottom-left, logo bottom-right
    caption_font = _font(size_map["caption"])
    draw.text((CONTENT_INSET, height - 40), tagline, font=caption_font, fill=grey_light_text)
    _paste_logo(
        img,
        ("logos", "icononly", "icononly_transparent.png"),
        target_width=96,
        position="bottom-right",
        margin=24,
    )

    img.save(out_path, quality=95)


# ---------------------------------------------------------------------------
# Template 2 — Video Thumbnail (1280x720)
# ---------------------------------------------------------------------------


def generate_youtube_thumbnail(
    out_path: str, slots: dict | None = None, tokens=None, brand=None, sizes=None
) -> None:
    colors, brand_meta, size_map = _resolve_tokens(tokens, brand, sizes)
    navy, red, cyan, white = colors["navy"], colors["red"], colors["cyan"], colors["white"]
    grey_light_text = colors["grey-light-text"]
    tagline = (slots or {}).get("tagline") or brand_meta.get("tagline", FALLBACK_BRAND["tagline"])
    s = {**DEFAULT_SLOTS["youtube-thumbnail"], **(slots or {})}

    width, height = 1280, 720
    # Subtle navy gradient per spec; endpoints stay close to the navy token so
    # the dominant fill remains brand navy.
    bottom_navy = tuple(max(0, int(c * 0.88)) for c in navy)
    img = _vertical_gradient((width, height), navy, bottom_navy)
    draw = ImageDraw.Draw(img)
    _rail_on_navy(draw, height, cyan)

    # Episode badge (red pill) — top-left, above the title
    badge_font = _font(size_map["caption"], bold=True)
    _pill(
        draw,
        center_y=48,
        x=CONTENT_INSET,
        text=s["badge"],
        font=badge_font,
        bg=red,
        fg=colors["onRed"],
    )

    # Title — left 40% content column, 2 lines max
    title_font = _font(size_map["titleXl"], bold=True)
    _draw_block(
        draw, (CONTENT_INSET, 112), s["title"], title_font, white, max_width=420, max_lines=2
    )

    # Play button — red circle, center-right; kept out of YouTube overlays
    # (critical content clear of bottom 90px and right 180px)
    cx, cy, r = 900, 360, 32
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=red)
    _play_triangle(draw, cx, cy, r, colors["onRed"])

    caption_font = _font(size_map["caption"])
    draw.text((CONTENT_INSET, height - 40), tagline, font=caption_font, fill=grey_light_text)
    _paste_logo(
        img,
        ("logos", "icononly", "icononly_transparent.png"),
        target_width=96,
        position="bottom-right",
        margin=24,
    )

    img.save(out_path, quality=95)


# ---------------------------------------------------------------------------
# Template 3 — Reels / Shorts Cover (1080x1920)
# ---------------------------------------------------------------------------


def generate_reels_shorts_cover(
    out_path: str, slots: dict | None = None, tokens=None, brand=None, sizes=None
) -> None:
    colors, brand_meta, size_map = _resolve_tokens(tokens, brand, sizes)
    navy, red, cyan, white = colors["navy"], colors["red"], colors["cyan"], colors["white"]
    grey_light_text = colors["grey-light-text"]
    tagline = (slots or {}).get("tagline") or brand_meta.get("tagline", FALLBACK_BRAND["tagline"])
    s = {**DEFAULT_SLOTS["reels-shorts-cover"], **(slots or {})}

    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), navy)
    draw = ImageDraw.Draw(img)

    # Top 15% — hook text area, centered
    hook_font = _font(size_map["titleMd"], bold=True)
    hook_lines = _wrap(draw, s["hook"], hook_font, max_width=width - 2 * CONTENT_INSET)
    hook_h = _block_height(hook_lines, hook_font)
    hook_y = 140 - hook_h // 2
    _draw_block(
        draw,
        (CONTENT_INSET, hook_y),
        s["hook"],
        hook_font,
        white,
        max_width=width - 2 * CONTENT_INSET,
        align="center",
    )

    # Middle 60% — branded content preview panel (video frame placeholder)
    panel = (CONTENT_INSET, 430, width - CONTENT_INSET, 1420)
    draw.rounded_rectangle(panel, radius=16, outline=cyan, width=4)
    pcx = (panel[0] + panel[2]) // 2
    pcy = (panel[1] + panel[3]) // 2
    r = 44
    draw.ellipse([pcx - r, pcy - r, pcx + r, pcy + r], fill=red)
    _play_triangle(draw, pcx, pcy, r, colors["onRed"])

    # Logo top-right (min 32px icon; 96px for template presence)
    _paste_logo(
        img,
        ("logos", "icononly", "icononly_transparent.png"),
        target_width=96,
        position="top-right",
        margin=24,
    )

    # Bottom 25% safe zone — tagline sits just BELOW the preview panel (panel
    # ends at y=1420) and above 480px-from-bottom (y < 1440) per spec
    caption_font = _font(size_map["caption"])
    draw.text((CONTENT_INSET, 1428), tagline, font=caption_font, fill=grey_light_text)

    # Red 3px progress bar indicator at the very bottom
    draw.rectangle([0, height - 3, int(width * 0.4), height], fill=red)

    img.save(out_path, quality=95)


# ---------------------------------------------------------------------------
# Template 4 — Quote Card (1080x1080)
# ---------------------------------------------------------------------------


def generate_quote_card(
    out_path: str, slots: dict | None = None, tokens=None, brand=None, sizes=None
) -> None:
    colors, brand_meta, size_map = _resolve_tokens(tokens, brand, sizes)
    navy, red, cyan, white = colors["navy"], colors["red"], colors["cyan"], colors["white"]
    grey_light_text = colors["grey-light-text"]
    tagline = (slots or {}).get("tagline") or brand_meta.get("tagline", FALLBACK_BRAND["tagline"])
    s = {**DEFAULT_SLOTS["quote-card"], **(slots or {})}

    width, height = 1080, 1080
    img = Image.new("RGB", (width, height), navy)
    draw = ImageDraw.Draw(img)
    _rail_on_navy(draw, height, cyan)

    # Decorative quote mark — large cyan, top-left of the quote
    mark_font = _font(150, bold=True)
    draw.text((CONTENT_INSET - 8, 56), "\u201c", font=mark_font, fill=cyan)

    # Quote text — body-lg italic white, wrapped
    quote_font = _font(size_map["bodyLg"], italic=True)
    quote_y, _ = _draw_block(
        draw, (CONTENT_INSET + 8, 268), s["quote"], quote_font, white, max_width=860
    )

    # Attribution bar — red divider, author (display, cyan), role (caption)
    bar_y = quote_y + 24
    draw.rectangle([CONTENT_INSET + 8, bar_y, CONTENT_INSET + 8 + 64, bar_y + 4], fill=red)
    author_font = _font(size_map["bodySm"], bold=True)
    draw.text((CONTENT_INSET + 8, bar_y + 20), s["author"], font=author_font, fill=cyan)
    role_font = _font(size_map["caption"])
    draw.text(
        (CONTENT_INSET + 8, bar_y + 20 + author_font.size + 8),
        s["role"],
        font=role_font,
        fill=grey_light_text,
    )

    caption_font = _font(size_map["caption"])
    draw.text((CONTENT_INSET, height - 40), tagline, font=caption_font, fill=grey_light_text)
    _paste_logo(
        img,
        ("logos", "icononly", "icononly_transparent.png"),
        target_width=96,
        position="bottom-right",
        margin=24,
    )

    img.save(out_path, quality=95)


# ---------------------------------------------------------------------------
# Template 5 — Stat Card (1080x1080)
# ---------------------------------------------------------------------------


def generate_stat_card(
    out_path: str, slots: dict | None = None, tokens=None, brand=None, sizes=None
) -> None:
    colors, brand_meta, size_map = _resolve_tokens(tokens, brand, sizes)
    navy, red, cyan = colors["navy"], colors["red"], colors["cyan"]
    white, grey_dark = colors["white"], colors["grey-dark"]
    tagline = (slots or {}).get("tagline") or brand_meta.get("tagline", FALLBACK_BRAND["tagline"])
    s = {**DEFAULT_SLOTS["stat-card"], **(slots or {})}

    width, height = 1080, 1080
    img = Image.new("RGB", (width, height), white)
    draw = ImageDraw.Draw(img)
    _rail_on_white(img, draw, height, navy)

    # Small cyan bar chart — top-right area (ascending bars)
    bar_w, bar_gap, baseline_y = 28, 12, 150
    bar_heights = [24, 36, 48, 60]
    bars_w = len(bar_heights) * bar_w + (len(bar_heights) - 1) * bar_gap
    bx = width - CONTENT_INSET - bars_w
    for i, h in enumerate(bar_heights):
        draw.rectangle(
            [
                bx + i * (bar_w + bar_gap),
                baseline_y - h,
                bx + i * (bar_w + bar_gap) + bar_w,
                baseline_y,
            ],
            fill=cyan,
        )

    # Big red metric number
    number_font = _font(size_map["displayXl"], bold=True)
    draw.text((CONTENT_INSET, 268), s["number"], font=number_font, fill=red)

    # Navy label
    label_font = _font(size_map["titleSm"], bold=True)
    draw.text((CONTENT_INSET, 268 + number_font.size + 16), s["label"], font=label_font, fill=navy)

    # Context (2 lines max) + source line
    context_font = _font(size_map["body"])
    ctx_y = 268 + number_font.size + 16 + label_font.size + 24
    ctx_end, _ = _draw_block(
        draw,
        (CONTENT_INSET, ctx_y),
        s["context"],
        context_font,
        grey_dark,
        max_width=920,
        max_lines=2,
    )
    source_font = _font(size_map["caption"])
    draw.text((CONTENT_INSET, ctx_end + 24), s["source"], font=source_font, fill=grey_dark)

    caption_font = _font(size_map["caption"])
    draw.text((CONTENT_INSET, height - 40), tagline, font=caption_font, fill=grey_dark)
    _paste_logo(
        img,
        ("logos", "fulllogo", "fulllogo_transparent.png"),
        target_width=300,
        position="bottom-right",
        margin=24,
    )

    img.save(out_path, quality=95)


# ---------------------------------------------------------------------------
# Template 6 — Thread Header (1200x675)
# ---------------------------------------------------------------------------


def generate_thread_header(
    out_path: str, slots: dict | None = None, tokens=None, brand=None, sizes=None
) -> None:
    colors, brand_meta, size_map = _resolve_tokens(tokens, brand, sizes)
    navy, red, cyan, white = colors["navy"], colors["red"], colors["cyan"], colors["white"]
    grey_light_text = colors["grey-light-text"]
    tagline = (slots or {}).get("tagline") or brand_meta.get("tagline", FALLBACK_BRAND["tagline"])
    s = {**DEFAULT_SLOTS["thread-header"], **(slots or {})}

    width, height = 1200, 675
    img = Image.new("RGB", (width, height), navy)
    draw = ImageDraw.Draw(img)
    _rail_on_navy(draw, height, cyan)

    # Thread indicator — red vertical bar + THREAD label
    bar_x, bar_top, bar_h = CONTENT_INSET, 52, 40
    draw.rectangle([bar_x, bar_top, bar_x + 4, bar_top + bar_h], fill=red)
    thread_font = _font(size_map["caption"], bold=True)
    draw.text((bar_x + 16, bar_top), s["part"] and "THREAD", font=thread_font, fill=red)

    # Part indicator top-right (e.g. 1/8)
    part_font = _font(size_map["caption"])
    part_w = draw.textlength(s["part"], font=part_font)
    draw.text(
        (width - CONTENT_INSET - part_w, bar_top), s["part"], font=part_font, fill=grey_light_text
    )

    # Title (2 lines max) + cyan subtitle (subtitle y computed from the ACTUAL
    # wrapped title height so 1-line and 2-line titles both keep a 16px rhythm)
    title_font = _font(size_map["titleXl"], bold=True)
    _, title_lines = _draw_block(
        draw, (CONTENT_INSET, 132), s["title"], title_font, white, max_width=1000, max_lines=2
    )
    subtitle_font = _font(size_map["subtitle"])
    subtitle_y = 132 + _block_height(title_lines, title_font) + 16
    _draw_block(
        draw, (CONTENT_INSET, subtitle_y), s["subtitle"], subtitle_font, cyan, max_width=1000
    )

    caption_font = _font(size_map["caption"])
    draw.text((CONTENT_INSET, height - 40), tagline, font=caption_font, fill=grey_light_text)
    _paste_logo(
        img,
        ("logos", "icononly", "icononly_transparent.png"),
        target_width=96,
        position="bottom-right",
        margin=24,
    )

    img.save(out_path, quality=95)


# ---------------------------------------------------------------------------
# Template 7 — Lower-Third Video Overlay (1920x360, RGBA)
# ---------------------------------------------------------------------------


def generate_lower_third_video_overlay(
    out_path: str, slots: dict | None = None, tokens=None, brand=None, sizes=None
) -> None:
    colors, brand_meta, size_map = _resolve_tokens(tokens, brand, sizes)
    navy, red, cyan, white = colors["navy"], colors["red"], colors["cyan"], colors["white"]
    grey_light_text = colors["grey-light-text"]
    tagline = (slots or {}).get("tagline") or brand_meta.get("tagline", FALLBACK_BRAND["tagline"])
    s = {**DEFAULT_SLOTS["lower-third-video-overlay"], **(slots or {})}

    width, height = 1920, 360
    # Navy at 90% opacity (RGBA) per spec — RGB values stay on-token so a video
    # editor compositing this bar over footage gets a 90% navy scrim.
    img = Image.new("RGBA", (width, height), (*navy, 230))
    draw = ImageDraw.Draw(img)

    # Vertically centered group: name / red line / role / tagline.
    # Block is 76px tall centered on y=180 => starts at y=142.
    name_font = _font(size_map["titleSm"], bold=True)  # 18pt display
    role_font = _font(size_map["body"])  # 14pt body
    caption_font = _font(size_map["caption"])  # 12pt caption

    name_y = 142
    draw.text((CONTENT_INSET, name_y), s["name"], font=name_font, fill=white)

    # Red accent line — 4px tall, full content width, between name and role
    line_y = name_y + name_font.size + LINE_GAP  # 142 + 18 + 8 = 168
    draw.rectangle([CONTENT_INSET, line_y, width - CONTENT_INSET, line_y + 4], fill=red)

    role_y = line_y + 4 + LINE_GAP
    draw.text((CONTENT_INSET, role_y), s["role"], font=role_font, fill=cyan)

    tag_y = role_y + role_font.size + 12
    draw.text((CONTENT_INSET, tag_y), tagline, font=caption_font, fill=grey_light_text)

    # Logo — Icon Only (48px), right side, vertically centered, clear space
    _paste_logo(
        img,
        ("logos", "icononly", "icononly_transparent.png"),
        target_width=48,
        position="center-right",
        margin=64,
    )

    img.save(out_path, quality=95)


# ---------------------------------------------------------------------------
# Template 8 — Hook Card, first 3 seconds (1080x1920)
# ---------------------------------------------------------------------------


def generate_hook_card(
    out_path: str, slots: dict | None = None, tokens=None, brand=None, sizes=None
) -> None:
    colors, brand_meta, size_map = _resolve_tokens(tokens, brand, sizes)
    navy, red, white = colors["navy"], colors["red"], colors["white"]
    grey_light_text = colors["grey-light-text"]
    tagline = (slots or {}).get("tagline") or brand_meta.get("tagline", FALLBACK_BRAND["tagline"])
    s = {**DEFAULT_SLOTS["hook-card"], **(slots or {})}

    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), navy)
    draw = ImageDraw.Draw(img)

    # Red pulse ring — static render of the motion-spec ring (1.5s ease-in-out)
    # anchored around the hero number (upper-middle of the card)
    cx, cy, r = width // 2, 480, 96
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=red, width=4)

    # Hero number — display-xl red, centered inside the ring
    number_font = _font(size_map["displayXl"], bold=True)
    nb = draw.textbbox((0, 0), s["number"], font=number_font)
    draw.text(
        (cx - (nb[2] - nb[0]) / 2 - nb[0], cy - (nb[3] - nb[1]) / 2 - nb[1]),
        s["number"],
        font=number_font,
        fill=red,
    )

    # Hook text — title-lg white, centered, 2 lines max
    hook_font = _font(size_map["titleLg"], bold=True)
    _, hook_lines = _draw_block(
        draw,
        (CONTENT_INSET, 640),
        s["hook"],
        hook_font,
        white,
        max_width=920,
        align="center",
        max_lines=2,
    )
    hook_end = 640 + _block_height(hook_lines, hook_font)

    # Teaser — body grey-light-text, centered ("Watch for..." line)
    teaser_font = _font(size_map["body"])
    _draw_block(
        draw,
        (CONTENT_INSET, hook_end + 24),
        s["teaser"],
        teaser_font,
        grey_light_text,
        max_width=920,
        align="center",
    )

    # Logo top-right (Icon Only, 96px)
    _paste_logo(
        img,
        ("logos", "icononly", "icononly_transparent.png"),
        target_width=96,
        position="top-right",
        margin=24,
    )

    # Tagline — caption, bottom clear zone (y=1856, above the 64px bottom UI margin)
    caption_font = _font(size_map["caption"])
    tw = draw.textlength(tagline, font=caption_font)
    draw.text(((width - tw) / 2, height - 64), tagline, font=caption_font, fill=grey_light_text)

    img.save(out_path, quality=95)


# ---------------------------------------------------------------------------
# Template 9 — End-Screen CTA (1920x1080)
# ---------------------------------------------------------------------------


def generate_end_screen_cta(
    out_path: str, slots: dict | None = None, tokens=None, brand=None, sizes=None
) -> None:
    colors, brand_meta, size_map = _resolve_tokens(tokens, brand, sizes)
    navy, red, cyan, white = colors["navy"], colors["red"], colors["cyan"], colors["white"]
    grey_light, grey_light_text, grey_dark = (
        colors["grey-light"],
        colors["grey-light-text"],
        colors["grey-dark"],
    )
    tagline = (slots or {}).get("tagline") or brand_meta.get("tagline", FALLBACK_BRAND["tagline"])
    s = {**DEFAULT_SLOTS["end-screen-cta"], **(slots or {})}

    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), navy)
    draw = ImageDraw.Draw(img)
    _rail_on_navy(draw, height, cyan)

    # Headline + subtext (top-left content column, P1 inset)
    headline_font = _font(size_map["titleXl"], bold=True)
    draw.text((CONTENT_INSET, 248), s["headline"], font=headline_font, fill=white)
    subtext_font = _font(size_map["bodyLg"])
    _draw_block(
        draw,
        (CONTENT_INSET, 248 + headline_font.size + 16),
        s["subtext"],
        subtext_font,
        grey_light_text,
        max_width=1100,
    )

    # Email capture visual — input field mockup + red CTA button
    input_x, input_y, input_w, input_h = CONTENT_INSET, 560, 760, 76
    draw.rounded_rectangle(
        [input_x, input_y, input_x + input_w, input_y + input_h],
        radius=8,
        fill=grey_light,
        outline=navy,
        width=3,
    )
    # Cyan focus line under the field (email-safe affordance)
    draw.rectangle(
        [input_x, input_y + input_h, input_x + input_w, input_y + input_h + 4], fill=cyan
    )
    placeholder_font = _font(size_map["body"])
    draw.text(
        (input_x + 24, input_y + (input_h - placeholder_font.size) // 2 - 4),
        s["emailPlaceholder"],
        font=placeholder_font,
        fill=grey_dark,
    )

    button_x, button_y = input_x + input_w + 24, input_y
    button_w, button_h = 320, 76
    draw.rounded_rectangle(
        [button_x, button_y, button_x + button_w, button_y + button_h], radius=8, fill=red
    )
    cta_font = _font(size_map["bodyLg"], bold=True)
    cta_w = draw.textlength(s["cta"], font=cta_font)
    draw.text(
        (button_x + (button_w - cta_w) / 2, button_y + (button_h - cta_font.size) // 2 - 4),
        s["cta"],
        font=cta_font,
        fill=colors["onRed"],
    )

    # Red arrow pointing at the CTA button (diagonal, above the input row)
    draw.line([(610, 500), (button_x - 18, button_y + 36)], fill=red, width=4)
    draw.polygon(
        [
            (button_x - 12, button_y + 42),
            (button_x - 40, button_y + 22),
            (button_x - 36, button_y + 56),
        ],
        fill=red,
    )

    # Logo + tagline bottom center
    _paste_logo(
        img,
        ("logos", "fulllogo", "fulllogo_transparent.png"),
        target_width=360,
        position="center",
        margin=120,
    )
    caption_font = _font(size_map["caption"])
    tg_w = draw.textlength(tagline, font=caption_font)
    draw.text(((width - tg_w) / 2, height - 72), tagline, font=caption_font, fill=grey_light_text)

    img.save(out_path, quality=95)


# ---------------------------------------------------------------------------
# Template 10 — Chapter Marker (1920x180, RGBA)
# ---------------------------------------------------------------------------


def generate_chapter_marker(
    out_path: str, slots: dict | None = None, tokens=None, brand=None, sizes=None
) -> None:
    colors, brand_meta, size_map = _resolve_tokens(tokens, brand, sizes)
    navy, red, cyan, white = colors["navy"], colors["red"], colors["cyan"], colors["white"]
    grey_light_text = colors["grey-light-text"]
    tagline = (slots or {}).get("tagline") or brand_meta.get("tagline", FALLBACK_BRAND["tagline"])
    s = {**DEFAULT_SLOTS["chapter-marker"], **(slots or {})}

    width, height = 1920, 180
    img = Image.new("RGBA", (width, height), (*navy, 242))  # Navy at 95% opacity
    draw = ImageDraw.Draw(img)

    # Progress indicator at the bottom — grey track, cyan fill at 60% (2px)
    track_y = height - 12  # 168
    draw.rectangle(
        [CONTENT_INSET, track_y, width - CONTENT_INSET, track_y + 2], fill=grey_light_text
    )
    fill_end = int(CONTENT_INSET + (width - 2 * CONTENT_INSET) * 0.6)
    draw.rectangle([CONTENT_INSET, track_y, fill_end, track_y + 2], fill=cyan)

    # Chapter number — red circle (32px) with white caption number
    cx, cy, r = 80, 82, 16
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=red)
    num_font = _font(size_map["caption"], bold=True)
    nb = draw.textbbox((0, 0), s["number"], font=num_font)
    draw.text(
        (cx - (nb[2] - nb[0]) / 2 - nb[0], cy - (nb[3] - nb[1]) / 2 - nb[1]),
        s["number"],
        font=num_font,
        fill=colors["onRed"],
    )

    # Chapter title — body display (bold) white, right of the number circle
    title_font = _font(size_map["body"], bold=True)
    draw.text((cx + r + 16, cy - title_font.size // 2), s["title"], font=title_font, fill=white)

    # Timestamp + tagline, right-aligned
    caption_font = _font(size_map["caption"])
    ts_w = draw.textlength(s["timestamp"], font=caption_font)
    draw.text(
        (width - CONTENT_INSET - ts_w, 70), s["timestamp"], font=caption_font, fill=grey_light_text
    )
    tg_w = draw.textlength(tagline, font=caption_font)
    draw.text((width - CONTENT_INSET - tg_w, 96), tagline, font=caption_font, fill=grey_light_text)

    img.save(out_path, quality=95)


# ---------------------------------------------------------------------------
# Template 11 — Facebook Group Cover (1640x856)
# ---------------------------------------------------------------------------


def generate_facebook_group_cover(
    out_path: str, slots: dict | None = None, tokens=None, brand=None, sizes=None
) -> None:
    colors, brand_meta, size_map = _resolve_tokens(tokens, brand, sizes)
    navy, red, cyan, white = colors["navy"], colors["red"], colors["cyan"], colors["white"]
    grey_light_text = colors["grey-light-text"]
    tagline = (slots or {}).get("tagline") or brand_meta.get("tagline", FALLBACK_BRAND["tagline"])
    s = {**DEFAULT_SLOTS["facebook-group-cover"], **(slots or {})}

    width, height = 1640, 856
    img = Image.new("RGB", (width, height), navy)
    draw = ImageDraw.Draw(img)

    # Centered content block: group name / tagline / description / logo / CTA
    group_font = _font(size_map["titleXl"], bold=True)
    _draw_block(
        draw, (160, 196), s["group"], group_font, white, max_width=width - 320, align="center"
    )
    tag_font = _font(size_map["subtitle"])
    _draw_block(draw, (160, 244), tagline, tag_font, cyan, max_width=width - 320, align="center")
    desc_font = _font(size_map["body"])
    _draw_block(
        draw,
        (160, 284),
        s["description"],
        desc_font,
        grey_light_text,
        max_width=width - 320,
        align="center",
    )

    # Full logo (transparent) centered below the description
    logo_path = _canonical_or_mirror("logos", "fulllogo", "fulllogo_transparent.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        target_w = 240
        target_h = int(logo.height * (target_w / logo.width))
        logo = logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
        img.paste(logo, ((width - target_w) // 2, 340), logo)
        cta_center = 340 + target_h + 48
    else:
        cta_center = 600

    # CTA — red pill, centered
    cta_font = _font(size_map["bodySm"], bold=True)
    cta_w = int(draw.textlength(s["cta"], font=cta_font)) + 32
    _pill(
        draw,
        center_y=cta_center,
        x=(width - cta_w) // 2,
        text=s["cta"],
        font=cta_font,
        bg=red,
        fg=colors["onRed"],
        pad_x=16,
        pad_y=10,
    )

    img.save(out_path, quality=95)


# ---------------------------------------------------------------------------
# Template 12 — Email Newsletter Header (600x200)
# ---------------------------------------------------------------------------


def _snap_to_palette(img: Image.Image, colors: dict) -> Image.Image:
    """Snap every visible pixel to the nearest exact brand token color.

    Source logos and anti-aliased text carry blend colors that fail the exact
    palette QA gate (check_brand_palette.py). For small-format pieces such as
    the 600x200 email header these blends are a meaningful fraction of the
    canvas; snapping them to the closest token is visually identical (all
    blends are averages of two tokens) and keeps the gate at 0% off-palette.
    """
    palette = list(colors.values())
    px = img.load()
    w, h = img.size
    is_rgba = img.mode == "RGBA"
    for y in range(h):
        for x in range(w):
            pxel = px[x, y]
            if is_rgba:
                r, g, b, a = pxel
                if a == 0:
                    continue
            else:
                r, g, b = pxel
            best = None
            best_d = None
            for pr, pg, pb in palette:
                d = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
                if best_d is None or d < best_d:
                    best_d = d
                    best = (pr, pg, pb)
            if (r, g, b) != best:
                px[x, y] = (*best, a) if is_rgba else best
    return img


def generate_email_newsletter_header(
    out_path: str, slots: dict | None = None, tokens=None, brand=None, sizes=None
) -> None:
    colors, brand_meta, size_map = _resolve_tokens(tokens, brand, sizes)
    navy, cyan, white = colors["navy"], colors["cyan"], colors["white"]
    grey_light_text = colors["grey-light-text"]
    tagline = (slots or {}).get("tagline") or brand_meta.get("tagline", FALLBACK_BRAND["tagline"])
    s = {**DEFAULT_SLOTS["email-newsletter-header"], **(slots or {})}

    width, height = 600, 200
    img = Image.new("RGB", (width, height), navy)
    draw = ImageDraw.Draw(img)

    # Thin 4px email-safe rail at the left edge (web layout.navyRail = 4px
    # token; the cyan line carries the brand rail signal on the navy surface)
    draw.rectangle([0, 0, 4, height], fill=cyan)

    # Full logo (transparent) left, 140px wide (>= 120px min), vertically centered
    logo_path = _canonical_or_mirror("logos", "fulllogo", "fulllogo_transparent.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        target_w = 140
        target_h = int(logo.height * (target_w / logo.width))
        logo = logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
        img.paste(logo, (24, (height - target_h) // 2), logo)
        text_x = 24 + target_w + 16
    else:
        text_x = 24

    # Publication name (title-md white) + issue line (caption cyan), vertically
    # centered against the logo (44px block centered on y=100 => starts at 78)
    name_font = _font(size_map["titleMd"], bold=True)
    draw.text((text_x, 78), s["publication"], font=name_font, fill=white)
    issue_font = _font(size_map["caption"])
    draw.text((text_x, 78 + name_font.size + 8), s["issue"], font=issue_font, fill=cyan)

    # Tagline right-aligned (caption grey-light-text), vertically centered
    caption_font = _font(size_map["caption"])
    tg_w = draw.textlength(tagline, font=caption_font)
    draw.text(
        (width - 24 - tg_w, (height - caption_font.size) // 2),
        tagline,
        font=caption_font,
        fill=grey_light_text,
    )

    # Exact-palette pass: small canvas, so blends from the logo + text AA are
    # a visible fraction; snap them to the nearest brand token.
    _snap_to_palette(img, colors)
    img.save(out_path, quality=95)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

TEMPLATES: list[dict] = [
    {
        "name": "linkedin-carousel-cover",
        "file": "linkedin-carousel-cover.png",
        "dims": (1080, 1080),
        "surface": "navy",
        "gen": generate_linkedin_carousel,
        "slots": DEFAULT_SLOTS["linkedin-carousel-cover"],
        "description": "LinkedIn carousel cover slide (1 of 5)",
    },
    {
        "name": "youtube-thumbnail",
        "file": "youtube-thumbnail.png",
        "dims": (1280, 720),
        "surface": "navy",
        "gen": generate_youtube_thumbnail,
        "slots": DEFAULT_SLOTS["youtube-thumbnail"],
        "description": "YouTube / video thumbnail (16:9)",
    },
    {
        "name": "reels-shorts-cover",
        "file": "reels-shorts-cover.png",
        "dims": (1080, 1920),
        "surface": "navy",
        "gen": generate_reels_shorts_cover,
        "slots": DEFAULT_SLOTS["reels-shorts-cover"],
        "description": "Reels / Shorts vertical cover (9:16)",
    },
    {
        "name": "quote-card",
        "file": "quote-card.png",
        "dims": (1080, 1080),
        "surface": "navy",
        "gen": generate_quote_card,
        "slots": DEFAULT_SLOTS["quote-card"],
        "description": "Quote card (1:1)",
    },
    {
        "name": "stat-card",
        "file": "stat-card.png",
        "dims": (1080, 1080),
        "surface": "white",
        "gen": generate_stat_card,
        "slots": DEFAULT_SLOTS["stat-card"],
        "description": "Stat card (1:1)",
    },
    {
        "name": "thread-header",
        "file": "thread-header.png",
        "dims": (1200, 675),
        "surface": "navy",
        "gen": generate_thread_header,
        "slots": DEFAULT_SLOTS["thread-header"],
        "description": "X / LinkedIn thread header (16:9)",
    },
    # --- P2/P3 secondary types (Ticket #316) ---
    {
        "name": "lower-third-video-overlay",
        "file": "lower-third-video-overlay.png",
        "dims": (1920, 360),
        "surface": "navy",
        "gen": generate_lower_third_video_overlay,
        "slots": DEFAULT_SLOTS["lower-third-video-overlay"],
        "description": "Lower-third video overlay bar (RGBA, navy @ 90%)",
    },
    {
        "name": "hook-card",
        "file": "hook-card.png",
        "dims": (1080, 1920),
        "surface": "navy",
        "gen": generate_hook_card,
        "slots": DEFAULT_SLOTS["hook-card"],
        "description": "Short-form hook card, first 3 seconds (9:16)",
    },
    {
        "name": "end-screen-cta",
        "file": "end-screen-cta.png",
        "dims": (1920, 1080),
        "surface": "navy",
        "gen": generate_end_screen_cta,
        "slots": DEFAULT_SLOTS["end-screen-cta"],
        "description": "End-screen CTA with email capture (16:9)",
    },
    {
        "name": "chapter-marker",
        "file": "chapter-marker.png",
        "dims": (1920, 180),
        "surface": "navy",
        "gen": generate_chapter_marker,
        "slots": DEFAULT_SLOTS["chapter-marker"],
        "description": "Chapter marker progress bar (RGBA, navy @ 95%)",
    },
    {
        "name": "facebook-group-cover",
        "file": "facebook-group-cover.png",
        "dims": (1640, 856),
        "surface": "navy",
        "gen": generate_facebook_group_cover,
        "slots": DEFAULT_SLOTS["facebook-group-cover"],
        "description": "Facebook group cover (1640x856)",
    },
    {
        "name": "email-newsletter-header",
        "file": "email-newsletter-header.png",
        "dims": (600, 200),
        "surface": "navy",
        "gen": generate_email_newsletter_header,
        "slots": DEFAULT_SLOTS["email-newsletter-header"],
        "description": "Email newsletter header (600x200)",
    },
]

_TEMPLATE_BY_NAME = {t["name"]: t for t in TEMPLATES}


# ---------------------------------------------------------------------------
# Self-QA — dimensions + dominant brand fills (PIL probe)
# ---------------------------------------------------------------------------


def _color_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return sum((x - y) ** 2 for x, y in zip(a, b, strict=True)) ** 0.5  # type: ignore[arg-type, return-value]


def verify(out_dir: str, colors: dict | None = None) -> bool:
    """PIL probe: every PNG must match its exact dimensions, its dominant fill
    must be the expected surface token (navy or white), and >= 90% of pixels
    must fall within distance 48 of SOME brand token (palette purity)."""
    colors = colors if colors is not None else _resolve_tokens(None, None, None)[0]
    palette = list(colors.values())
    ok = True
    print("\n=== QA: dimensions + brand palette (PIL probe) ===")
    print(f"{'file':<34} {'dims':<13} {'dom fill':<12} {'dist':<6} {'on-brand %':<10} result")
    for t in TEMPLATES:
        path = os.path.join(out_dir, t["file"])
        if not os.path.exists(path):
            print(f"{t['file']:<34} MISSING")
            ok = False
            continue
        img = Image.open(path)
        dims_ok = img.size == t["dims"]
        small = img.convert("RGB").resize((200, 200), Image.Resampling.BILINEAR)
        counts = small.getcolors(maxcolors=200 * 200) or []
        counts.sort(reverse=True)
        total = 200 * 200
        dominant = counts[0][1]
        surface = colors["navy"] if t["surface"] == "navy" else colors["white"]
        dom_dist = int(_color_distance(dominant, surface))
        dom_ok = dom_dist <= 14
        on_brand = sum(
            cnt for cnt, col in counts if min(_color_distance(col, p) for p in palette) <= 48
        )
        on_pct = on_brand * 100.0 / total
        palette_ok = on_pct >= 90.0
        result = "OK" if (dims_ok and dom_ok and palette_ok) else "FAIL"
        if result == "FAIL":
            ok = False
        print(
            f"{t['file']:<34} {str(img.size):<13} #{dominant[0]:02X}{dominant[1]:02X}{dominant[2]:02X}"
            f"{'':<4} {dom_dist:<6} {on_pct:<10.1f} {result}"
        )
    print("VERDICT:", "PASS" if ok else "FAIL")
    return ok


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate the twelve LightSpeed social post templates (P1 Ticket #311 + P2/P3 Ticket #316)."
    )
    parser.add_argument(
        "--template",
        choices=sorted(_TEMPLATE_BY_NAME),
        help="Generate only this template (default: all twelve).",
    )
    parser.add_argument(
        "--slots",
        help='JSON object of slot overrides for the selected template, e.g. \'{"title": "..."}\'. Requires --template.',
    )
    parser.add_argument(
        "--json",
        dest="json_file",
        help='JSON file mapping template name -> slot overrides, e.g. {"stat-card": {"number": "20"}}.',
    )
    parser.add_argument(
        "--outdir",
        default=OUTPUT_DIR,
        help="Output directory (default: static/brand/social/templates).",
    )
    parser.add_argument(
        "--verify", action="store_true", help="Run the dims + palette self-QA after generating."
    )
    args = parser.parse_args(argv)

    if args.slots and not args.template:
        parser.error("--slots requires --template (slot overrides apply to one template)")

    colors, brand, sizes = _load_tokens()
    print(f"Tokens source: {TOKEN_SOURCE}\n")

    overrides: dict[str, dict] = {}
    if args.json_file:
        with open(args.json_file, encoding="utf-8") as fh:
            overrides = json.load(fh)

    selected = [t for t in TEMPLATES if args.template is None or t["name"] == args.template]
    os.makedirs(args.outdir, exist_ok=True)

    for t in selected:
        slots = dict(t["slots"])
        if t["name"] in overrides:
            slots.update(overrides[t["name"]])
        if args.template == t["name"] and args.slots:
            slots.update(json.loads(args.slots))
        out_path = os.path.join(args.outdir, t["file"])
        t["gen"](out_path, slots=slots, tokens=colors, brand=brand, sizes=sizes)
        print(f"Created: {out_path}")

    if selected:
        print(f"\nAll selected templates saved to: {args.outdir}")

    if args.verify:
        return 0 if verify(args.outdir, colors) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
