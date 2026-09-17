"""
LightSpeed Holdings - Social Post Template Generator (P1 set)
Builds the top-6 social post templates from static/brand/templates/
social-templates/TEMPLATE_SPECS.md as programmatic Pillow generators.

Templates:
  1. LinkedIn Carousel (1080x1080, 5 slides)  -- cover / 3 content / CTA
  2. Video Thumbnail (1280x720, 16:9)
  3. Reels/Shorts Cover (1080x1920, 9:16)
  4. Quote Card (1080x1080, 1:1)
  5. Stat Card (1080x1080, 1:1)
  6. Thread Header (1200x675, 16:9)

Brand: LightSpeed Holdings Limited | Tagline: ASPIRE. ACT. ACHIEVE.
Tokens: brand/tokens/brand-tokens.json (navy #070A40, red #E63946, cyan #00BFFF).

Usage:
  python generate-social-templates.py                        # all 6 demo set
  python generate-social-templates.py --type carousel --type stat \\
      --title "..." --body "..." --metric "8.4x" --visual chart.png
"""

import argparse
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

# Brand colors (from brand/tokens/brand-tokens.json)
NAVY = (7, 10, 64)
RED = (230, 57, 70)
CYAN = (0, 191, 255)
WHITE = (255, 255, 255)
GREY_LIGHT = (242, 242, 242)
GREY_DARK = (107, 114, 128)
GREY_LIGHT_TEXT = (156, 163, 175)
# Subtle near-navy used for rails/pattern on navy surfaces (repo convention,
# mirrors generate-social-assets.py diagonal pattern).
NAVY_SUBTLE = (10, 15, 70)

TAGLINE = "ASPIRE. ACT. ACHIEVE."

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BRAND_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "..", "..", "brand"))


def _canonical_or_mirror(*parts):
    canonical = os.path.join(BRAND_ROOT, *parts)
    if os.path.exists(canonical):
        return canonical
    mirror = os.path.join(SCRIPT_DIR, "..", "..", *parts)
    return mirror


LOGO_DIR = _canonical_or_mirror("logos", "icononly")
FULL_LOGO_DIR = _canonical_or_mirror("logos", "fulllogo")
DEFAULT_OUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "social", "templates"))

RAIL_W = 48  # brand standard navy left rail


def _load_font(bold, size, italic=False):
    """Load an Arial variant (bold/regular/italic) at the given pixel size."""
    if italic:
        names = ("ariali.ttf", "arial.ttf")
    elif bold:
        names = ("arialbd.ttf", "arial.ttf")
    else:
        names = ("arial.ttf",)
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size)
    except TypeError:
        return ImageFont.load_default()


def _fit_font(draw, text, bold, size, max_width, italic=False):
    font = _load_font(bold, size, italic)
    text_width = draw.textbbox((0, 0), text, font=font)[2]
    if text_width > max_width and text_width > 0 and size > 12:
        size = max(12, int(size * max_width / text_width))
        font = _load_font(bold, size, italic)
    return font


def _wrap(draw, text, font, max_width):
    """Wrap text to lines fitting max_width, preserving words."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return textwrap.shorten("\n".join(lines), width=100000) and lines


def _text(draw, xy, text, font, fill, anchor="la"):
    """Draw text at xy (left baseline anchored), using bbox offsets so the
    baseline lands at the requested y."""
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=font)
    draw.text((x - bbox[0], y - bbox[1]), text, font=font, fill=fill)


def _paste_icon(img, x, y, height):
    """Paste the icon-only logo at (x, y) with given height; returns (w, h)."""
    icon_path = os.path.join(LOGO_DIR, "icononly_transparent.png")
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA")
        w = int(icon.width * (height / icon.height))
        icon = icon.resize((w, height), Image.Resampling.LANCZOS)
        img.paste(icon, (x, y), icon)
        return w, height
    return 0, height


def _paste_full_logo(img, x, y, height):
    """Paste the full transparent logo at (x, y) with given height."""
    logo_path = os.path.join(FULL_LOGO_DIR, "fulllogo_transparent.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        w = int(logo.width * (height / logo.height))
        logo = logo.resize((w, height), Image.Resampling.LANCZOS)
        img.paste(logo, (x, y), logo)
        return w, height
    return 0, height


def _footer(draw, img, width, height, icon_only=True):
    """Common bottom-left tagline + bottom-right logo footer."""
    tag_font = _load_font(False, 12)
    _text(draw, (RAIL_W + 16, height - 48), TAGLINE, tag_font, GREY_LIGHT_TEXT)
    if icon_only:
        _paste_icon(img, width - 48 - 48, height - 48 - 48, 48)
    else:
        _paste_full_logo(img, width - 48 - 200, height - 48 - 32, 40)


# ---------------------------------------------------------------------------
# Template 1: LinkedIn Carousel (1080x1080, 5 slides)
# ---------------------------------------------------------------------------


def _carousel_cover(img, draw, title, subtitle):
    draw.rectangle([(0, 0), (RAIL_W, 1080)], fill=NAVY_SUBTLE)
    title_font = _fit_font(draw, title, True, 32, 1080 - RAIL_W - 96)
    _text(draw, (RAIL_W + 48, 300), title, title_font, WHITE)
    if subtitle:
        sub_font = _fit_font(draw, subtitle, False, 16, 1080 - RAIL_W - 96)
        _text(draw, (RAIL_W + 48, 360), subtitle, sub_font, CYAN)
        draw.rectangle([(RAIL_W + 48, 392), (RAIL_W + 48 + 48, 396)], fill=RED)
    _footer(draw, img, 1080, 1080)


def _carousel_content(img, draw, headline, body, stat=None, visual=None):
    draw.rectangle([(0, 0), (RAIL_W, 1080)], fill=NAVY)
    x = RAIL_W + 96
    head_font = _fit_font(draw, headline, True, 24, 1080 - RAIL_W - 96)
    _text(draw, (x, 220), headline, head_font, NAVY)

    y = 300
    if stat:
        stat_font = _fit_font(draw, stat, True, 36, 1080 - RAIL_W - 96)
        _text(draw, (x, y), stat, stat_font, RED)
        y += 52
    if body:
        body_font = _fit_font(draw, body, False, 14, 1080 - RAIL_W - 96)
        lines = _wrap(draw, body, body_font, 1080 - RAIL_W - 96)
        for i, line in enumerate(lines[:6]):
            _text(draw, (x, y + i * 20), line, body_font, GREY_DARK)
        y += len(lines[:6]) * 20 + 16

    # Visual area: centered, max 80% width.
    vis_w = int((1080 - RAIL_W) * 0.8)
    vis_h = 360
    vis_x = RAIL_W + (1080 - RAIL_W - vis_w) // 2
    vis_y = max(y + 24, 480)
    if visual and os.path.exists(visual):
        v = Image.open(visual).convert("RGB")
        v = v.resize((vis_w, vis_h), Image.Resampling.LANCZOS)
        img.paste(v, (vis_x, vis_y))
    else:
        draw.rounded_rectangle(
            [vis_x, vis_y, vis_x + vis_w, vis_y + vis_h],
            radius=16,
            fill=GREY_LIGHT,
            outline=GREY_DARK,
            width=2,
        )
        ph_font = _load_font(False, 14)
        ph = "DIAGRAM / CHART / STAT"
        bbox = draw.textbbox((0, 0), ph, font=ph_font)
        _text(
            draw,
            (
                vis_x + (vis_w - (bbox[2] - bbox[0])) // 2,
                vis_y + (vis_h - (bbox[3] - bbox[1])) // 2,
            ),
            ph,
            ph_font,
            GREY_DARK,
        )
    _footer(draw, img, 1080, 1080, icon_only=False)


def _carousel_cta(img, draw, headline, subtext, url, cta):
    draw.rectangle([(0, 0), (RAIL_W, 1080)], fill=NAVY_SUBTLE)
    x = RAIL_W + 48
    head_font = _fit_font(draw, headline, True, 28, 1080 - RAIL_W - 96)
    _text(draw, (x, 320), headline, head_font, WHITE)
    if subtext:
        sub_font = _fit_font(draw, subtext, False, 14, 1080 - RAIL_W - 96)
        y = 400
        for line in _wrap(draw, subtext, sub_font, 1080 - RAIL_W - 96)[:3]:
            _text(draw, (x, y), line, sub_font, GREY_LIGHT_TEXT)
            y += 20
    # CTA button
    bw, bh = 240, 56
    by = 480 + (140 if subtext else 0)
    draw.rounded_rectangle([x, by, x + bw, by + bh], radius=8, fill=RED)
    btn_font = _fit_font(draw, cta, True, 13, bw - 24)
    bbox = draw.textbbox((0, 0), cta, font=btn_font)
    _text(
        draw,
        (x + (bw - (bbox[2] - bbox[0])) // 2, by + (bh - (bbox[3] - bbox[1])) // 2),
        cta,
        btn_font,
        WHITE,
    )
    if url:
        url_font = _load_font(False, 12)
        _text(draw, (x, by + bh + 24), url, url_font, CYAN)
    _footer(draw, img, 1080, 1080)


def generate_carousel(out_dir, title, subtitle, bodies, stat=None, ctas=None, visual=None):
    """Write the 5-slide carousel set. bodies: list of 3 content headlines,
    each optionally "Headline||body". ctas: (headline, subtext, url, cta)."""
    ctas = ctas or ("Ready to Build?", None, "lightspeedholdings.com", "Get Started")
    files = []
    img = Image.new("RGB", (1080, 1080), NAVY)
    _carousel_cover(img, ImageDraw.Draw(img), title, subtitle)
    p = os.path.join(out_dir, "linkedin-carousel-cover.png")
    img.save(p, quality=95)
    files.append(p)

    for i, item in enumerate(bodies, start=2):
        if "||" in item:
            head, body = item.split("||", 1)
        else:
            head, body = item, None
        img = Image.new("RGB", (1080, 1080), WHITE)
        _carousel_content(img, ImageDraw.Draw(img), head, body, stat=stat, visual=visual)
        p = os.path.join(out_dir, f"linkedin-carousel-{i}.png")
        img.save(p, quality=95)
        files.append(p)

    img = Image.new("RGB", (1080, 1080), NAVY)
    _carousel_cta(img, ImageDraw.Draw(img), *ctas)
    p = os.path.join(out_dir, "linkedin-carousel-cta.png")
    img.save(p, quality=95)
    files.append(p)
    return files


# ---------------------------------------------------------------------------
# Template 2: Video Thumbnail (1280x720, 16:9)
# ---------------------------------------------------------------------------


def generate_thumbnail(out_dir, title, episode="EP 01"):
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), NAVY)
    # Subtle navy gradient
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        c = tuple(int(NAVY[i] + (NAVY_SUBTLE[i] - NAVY[i]) * t) for i in range(3))
        draw.line([(0, y), (w, y)], fill=c)
    # Left 40% navy rail area
    rail_w = int(w * 0.40)
    draw.rectangle([(0, 0), (rail_w, h)], fill=(5, 7, 44))

    cx = rail_w + 48
    max_w = w - 180 - cx  # keep clear of right 180px safe zone

    # Episode badge (red pill)
    badge_h = 34
    badge = "   " + episode + "   "
    badge_font = _fit_font(draw, badge, True, 12, 240)
    bbox = draw.textbbox((0, 0), badge, font=badge_font)
    bw = bbox[2] - bbox[0] + 24
    draw.rounded_rectangle([cx, 96, cx + bw, 96 + badge_h], radius=17, fill=RED)
    _text(
        draw,
        (cx + 12, 96 + (badge_h - (bbox[3] - bbox[1])) // 2),
        episode,
        _load_font(True, 12),
        WHITE,
    )

    # Title (2 lines max)
    title_font = _fit_font(draw, title, True, 32, max_w)
    lines = _wrap(draw, title, title_font, max_w)[:2]
    ty = 170
    for line in lines:
        _text(draw, (cx, ty), line, title_font, WHITE)
        ty += 44

    # Play button (red circle 64px, center-right)
    pcx, pcy, pr = cx + int(max_w * 0.5), int(h * 0.62), 32
    draw.ellipse([pcx - pr, pcy - pr, pcx + pr, pcy + pr], fill=RED)
    tri = [(pcx - 10, pcy - 16), (pcx - 10, pcy + 16), (pcx + 18, pcy)]
    draw.polygon(tri, fill=WHITE)

    # Footer: tagline bottom-left, logo icon bottom-right
    tag_font = _load_font(False, 12)
    _text(draw, (40, h - 40), TAGLINE, tag_font, GREY_LIGHT_TEXT)
    _paste_icon(img, w - 48 - 48, h - 40 - 48, 48)

    p = os.path.join(out_dir, "youtube-thumbnail.png")
    img.save(p, quality=95)
    return [p]


# ---------------------------------------------------------------------------
# Template 3: Reels/Shorts Cover (1080x1920, 9:16)
# ---------------------------------------------------------------------------


def generate_reels_cover(out_dir, title, visual=None):
    w, h = 1080, 1920
    img = Image.new("RGB", (w, h), NAVY)
    draw = ImageDraw.Draw(img)

    # Top 15% hook text (24pt white, centered)
    hook_font = _fit_font(draw, title, True, 24, w - 160)
    lines = _wrap(draw, title, hook_font, w - 160)[:2]
    hy = 160
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=hook_font)
        _text(draw, ((w - (bbox[2] - bbox[0])) // 2, hy), line, hook_font, WHITE)
        hy += 40

    # Middle 60% visual area (y 288..1440)
    vis_ym = 288
    vis_h = 1440 - 288 - 96
    vis_x, vis_w = 96, w - 192
    if visual and os.path.exists(visual):
        v = Image.open(visual).convert("RGB")
        v = v.resize((vis_w, vis_h), Image.Resampling.LANCZOS)
        img.paste(v, (vis_x, vis_ym))
    else:
        draw.rounded_rectangle(
            [vis_x, vis_ym, vis_x + vis_w, vis_ym + vis_h],
            radius=24,
            fill=(12, 16, 84),
            outline=GREY_DARK,
            width=2,
        )
        ph_font = _load_font(False, 18)
        ph = "VIDEO / DIAGRAM"
        bbox = draw.textbbox((0, 0), ph, font=ph_font)
        _text(
            draw,
            (
                vis_x + (vis_w - (bbox[2] - bbox[0])) // 2,
                vis_ym + (vis_h - (bbox[3] - bbox[1])) // 2,
            ),
            ph,
            ph_font,
            GREY_LIGHT_TEXT,
        )

    # Logo top-right (icon only, 32px min)
    _paste_icon(img, w - 48 - 48, 48, 48)

    # Red 3px progress bar at bottom
    bar_w = int(w * 0.4)
    bar_x = (w - bar_w) // 2
    draw.rectangle([(bar_x, h - 6), (bar_x + bar_w, h - 3)], fill=RED)

    p = os.path.join(out_dir, "instagram-reels-cover.png")
    img.save(p, quality=95)
    return [p]


# ---------------------------------------------------------------------------
# Template 4: Quote Card (1080x1080, 1:1)
# ---------------------------------------------------------------------------


def generate_quote(out_dir, quote, author, role=None):
    img = Image.new("RGB", (1080, 1080), NAVY)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (48, 1080)], fill=NAVY_SUBTLE)
    x = 148

    # Large decorative cyan quote mark
    q_font = _load_font(True, 120)
    _text(draw, (x - 40, 140), '"', q_font, CYAN)

    # Quote text (16pt white italic)
    q_font = _load_font(False, 16, italic=True)
    lines = _wrap(draw, quote, q_font, 1080 - x - 80)[:8]
    qy = 360
    for line in lines:
        _text(draw, (x, qy), line, q_font, WHITE)
        qy += 30

    if author:
        a_font = _fit_font(draw, author, True, 13, 1080 - x - 80)
        _text(draw, (x, qy + 24), author, a_font, CYAN)
        if role:
            r_font = _load_font(False, 12)
            _text(draw, (x, qy + 48), role, r_font, GREY_LIGHT_TEXT)

    _footer(draw, img, 1080, 1080)
    p = os.path.join(out_dir, "quote-card.png")
    img.save(p, quality=95)
    return [p]


# ---------------------------------------------------------------------------
# Template 5: Stat Card (1080x1080, 1:1)
# ---------------------------------------------------------------------------


def generate_stat(out_dir, metric, label, context=None):
    img = Image.new("RGB", (1080, 1080), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (48, 1080)], fill=NAVY)
    x = 148

    # Small cyan chart top-right
    bars = [(0.18, 0.5), (0.34, 0.75), (0.5, 0.3), (0.66, 0.85), (0.82, 0.6)]
    bx0, by0, bw, bh = 760, 180, 240, 160
    for i, (_, frac) in enumerate(bars):
        bw_i = 36
        bx = bx0 + i * (bw // 5)
        bh_i = int(bh * frac)
        draw.rectangle([(bx, by0 + bh - bh_i), (bx + bw_i, by0 + bh)], fill=CYAN)

    metric_font = _fit_font(draw, metric, True, 36, 1080 - x - 80)
    _text(draw, (x, 420), metric, metric_font, RED)

    label_font = _fit_font(draw, label, True, 18, 1080 - x - 80)
    _text(draw, (x, 500), label, label_font, NAVY)

    if context:
        c_font = _fit_font(draw, context, False, 14, 1080 - x - 80)
        cy = 560
        for line in _wrap(draw, context, c_font, 1080 - x - 80)[:2]:
            _text(draw, (x, cy), line, c_font, GREY_DARK)
            cy += 22

    _footer(draw, img, 1080, 1080, icon_only=False)
    p = os.path.join(out_dir, "stat-card.png")
    img.save(p, quality=95)
    return [p]


# ---------------------------------------------------------------------------
# Template 6: Thread Header (1200x675, 16:9)
# ---------------------------------------------------------------------------


def generate_thread_header(out_dir, title, subtitle=None, part="1/8"):
    w, h = 1200, 675
    img = Image.new("RGB", (w, h), NAVY)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (48, h)], fill=NAVY_SUBTLE)
    x = 148

    # Thread indicator: red vertical bar (4px) + "THREAD" caption
    draw.rectangle([(x, 150), (x + 4, 186)], fill=RED)
    th_font = _load_font(True, 12)
    _text(draw, (x + 20, 150), "THREAD", th_font, RED)

    # Part indicator top-right
    part_font = _load_font(False, 12)
    pbbox = draw.textbbox((0, 0), part, font=part_font)
    _text(draw, (w - 48 - (pbbox[2] - pbbox[0]), 40), part, part_font, GREY_LIGHT_TEXT)

    # Title
    title_font = _fit_font(draw, title, True, 32, w - x - 96)
    _text(draw, (x, 220), title, title_font, WHITE)

    # Subtitle
    if subtitle:
        sub_font = _fit_font(draw, subtitle, False, 16, w - x - 96)
        _text(draw, (x, 320), subtitle, sub_font, CYAN)

    _footer(draw, img, w, h)
    p = os.path.join(out_dir, "thread-header.png")
    img.save(p, quality=95)
    return [p]


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

TYPES = ["carousel", "thumbnail", "reels", "quote", "stat", "thread"]


def main():
    parser = argparse.ArgumentParser(
        description="Generate LightSpeed Holdings P1 social post templates."
    )
    parser.add_argument(
        "--type",
        action="append",
        choices=TYPES,
        help="Template type to generate; repeatable. Omit for all 6.",
    )
    parser.add_argument("--out-dir", default=DEFAULT_OUT_DIR)
    parser.add_argument("--title", default="We built the AI-Native Company")
    parser.add_argument("--subtitle", default="Agentic AI, in production — a real P&L, not a demo.")
    parser.add_argument(
        "--body",
        default="144 agents, 20 departments, one verified cost ledger. Here is the architecture — and what broke.",
    )
    parser.add_argument("--metric", default="144")
    parser.add_argument("--metric-label", default="agents operating today")
    parser.add_argument("--context", default="Running the full company, not just the slide deck.")
    parser.add_argument(
        "--quote", default="We built this. Here is the architecture, the cost, and what broke."
    )
    parser.add_argument("--author", default="Matt Lyusi")
    parser.add_argument("--role", default="CEO, LightSpeed Holdings")
    parser.add_argument("--episode", default="EP 01")
    parser.add_argument("--part", default="1/8")
    parser.add_argument(
        "--visual", default=None, help="Optional image path pasted into visual areas."
    )

    args = parser.parse_args()
    types = set(args.type) if args.type else set(TYPES)
    os.makedirs(args.out_dir, exist_ok=True)
    created = []

    if "carousel" in types:
        bodies = [
            "We run on our own agents||" + args.body,
            "144 agents, 20 departments||One orchestrated org, not a tool demo.",
            "The cost ledger is public||Every API call counted, every failure logged.",
        ]
        created += generate_carousel(
            args.out_dir,
            args.title,
            args.subtitle,
            bodies,
            stat=args.metric,
            visual=args.visual,
        )
    if "thumbnail" in types:
        created += generate_thumbnail(args.out_dir, args.title, args.episode)
    if "reels" in types:
        created += generate_reels_cover(args.out_dir, args.subtitle, args.visual)
    if "quote" in types:
        created += generate_quote(args.out_dir, args.quote, args.author, args.role)
    if "stat" in types:
        created += generate_stat(args.out_dir, args.metric, args.metric_label, args.context)
    if "thread" in types:
        created += generate_thread_header(args.out_dir, args.title, args.subtitle, args.part)

    print(f"Created {len(created)} template asset(s) in {args.out_dir}:")
    for c in created:
        print("  -", os.path.basename(c))


if __name__ == "__main__":
    main()
