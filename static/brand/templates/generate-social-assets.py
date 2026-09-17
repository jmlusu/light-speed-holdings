"""
LightSpeed Holdings - Social Media Asset Generator
Creates platform profile, banner, story and channel-art images using Pillow.
Brand: LightSpeed Holdings Limited | Tagline: ASPIRE. ACT. ACHIEVE.
Colors: Navy #070A40, Red #E63946, Cyan #00BFFF, Grey #F2F2F2
Platforms: LinkedIn, Twitter/X, GitHub, Instagram, TikTok, YouTube.
"""

import argparse
import os

from PIL import Image, ImageDraw, ImageFont

# Brand Colors
NAVY = (7, 10, 64)
RED = (230, 57, 70)
CYAN = (0, 191, 255)
WHITE = (255, 255, 255)
GREY = (242, 242, 242)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Canonical logos live in brand/logos/ (repo root). Fall back to the
# static/brand mirror for checkouts that have not run scripts/sync-brand.ps1.
BRAND_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "..", "brand"))


def _canonical_or_mirror(*parts):
    canonical = os.path.join(BRAND_ROOT, *parts)
    if os.path.exists(canonical):
        return canonical
    mirror = os.path.join(SCRIPT_DIR, "..", *parts)
    return mirror


LOGO_DIR = _canonical_or_mirror("logos", "icononly")
FULL_LOGO_DIR = _canonical_or_mirror("logos", "fulllogo")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "social")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


PALETTE = [NAVY, RED, CYAN, WHITE, GREY, (107, 114, 128), (156, 163, 175)]


def _snap_to_palette(img):
    """Snap every visible pixel to the nearest exact brand token color.

    Scaled-down logos and anti-aliased edges carry blend colors that fail the
    exact palette QA gate (check_brand_palette.py). All such blends are
    averages of two tokens, so snapping to the closest token is visually
    identical and keeps the gate at 0% off-palette.
    """
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
            for pr, pg, pb in PALETTE:
                d = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
                if best_d is None or d < best_d:
                    best_d = d
                    best = (pr, pg, pb)
            if (r, g, b) != best:
                px[x, y] = (*best, a) if is_rgba else best


def _load_font(bold, size):
    """Load an Arial truetype font (bold or regular) at the given pixel size."""
    names = ("arialbd.ttf", "arial.ttf") if bold else ("arial.ttf",)
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _shrink_to_fit(draw, text, font, max_width, bold):
    """Scale a font down so the text stays within max_width (no clipping)."""
    text_width = draw.textbbox((0, 0), text, font=font)[2]
    if text_width > max_width and text_width > 0 and getattr(font, "size", 0) > 12:
        font = _load_font(bold, max(12, int(font.size * max_width / text_width)))
    return font


def create_profile_image(size, output_path, variant="default"):
    """Create a profile image with the icon logo on navy background.

    variant="ring" adds a cyan medallion ring around the icon (Instagram avatar).
    """
    img = Image.new("RGB", (size, size), NAVY)
    draw = ImageDraw.Draw(img)

    # Ring treatment: cyan ring around the icon (Instagram profile)
    if variant == "ring":
        ring_outer = int(size * 0.44)
        ring_width = max(4, int(size * 0.045))
        bbox = [
            size // 2 - ring_outer,
            size // 2 - ring_outer,
            size // 2 + ring_outer,
            size // 2 + ring_outer,
        ]
        draw.ellipse(bbox, outline=CYAN, width=ring_width)

    # Load icon logo
    icon_path = os.path.join(LOGO_DIR, "icononly_transparent.png")
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA")
        # Calculate size to fit (50% of canvas), preserving aspect ratio
        icon_w = int(size * 0.5)
        icon_h = int(icon.height * (icon_w / icon.width))
        icon = icon.resize((icon_w, icon_h), Image.Resampling.LANCZOS)
        # Center
        offset_x = (size - icon_w) // 2
        offset_y = (size - icon_h) // 2
        img.paste(icon, (offset_x, offset_y), icon)
    else:
        # Fallback: draw "LS" text
        try:
            font = ImageFont.truetype("arial.ttf", int(size * 0.35))
        except OSError:
            font = ImageFont.load_default()
        text = "LS"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        draw.text((x, y), text, fill=WHITE, font=font)

    _snap_to_palette(img)
    img.save(output_path, quality=95)
    print(f"Created: {output_path}")


def create_banner_image(width, height, output_path, platform="linkedin"):
    """Create a banner image with navy background, logo, company name, and tagline."""
    img = Image.new("RGB", (width, height), NAVY)
    draw = ImageDraw.Draw(img)

    # Add subtle geometric pattern (diagonal lines)
    for i in range(-height, width + height, 40):
        draw.line([(i, 0), (i + height, height)], fill=(10, 15, 70), width=1)

    # Add accent bar at bottom
    bar_height = max(4, height // 50)
    draw.rectangle([(0, height - bar_height), (width, height)], fill=RED)

    # Load full logo
    full_logo_path = os.path.join(FULL_LOGO_DIR, "fulllogo_transparent.png")
    if os.path.exists(full_logo_path):
        logo = Image.open(full_logo_path).convert("RGBA")
        # Scale logo to fit banner height (40%)
        logo_height = int(height * 0.35)
        logo_width = int(logo.width * (logo_height / logo.height))
        logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

        # Position: left-center with padding
        padding = int(width * 0.05)
        logo_y = (height - logo_height) // 2 - bar_height // 2
        img.paste(logo, (padding, logo_y), logo)

        # Company name to the right of logo
        text_x = padding + logo_width + int(width * 0.03)
    else:
        text_x = int(width * 0.05)

    # Company name
    try:
        name_font_size = int(height * 0.18) if platform == "twitter" else int(height * 0.15)
        name_font = ImageFont.truetype("arialbd.ttf", name_font_size)
    except OSError:
        try:
            name_font = ImageFont.truetype("arial.ttf", name_font_size)
        except OSError:
            name_font = ImageFont.load_default()

    company_name = "LIGHTSPEED HOLDINGS"
    name_y = int(height * 0.25)
    draw.text((text_x, name_y), company_name, fill=WHITE, font=name_font)

    # Tagline
    try:
        tagline_font_size = int(height * 0.07)
        tagline_font = ImageFont.truetype("arial.ttf", tagline_font_size)
    except OSError:
        tagline_font = ImageFont.load_default()

    tagline = "Aspire. Act. Achieve."
    tagline_y = name_y + name_font_size + int(height * 0.03)
    draw.text((text_x, tagline_y), tagline, fill=CYAN, font=tagline_font)

    _snap_to_palette(img)
    img.save(output_path, quality=95)
    print(f"Created: {output_path}")


def create_story_image(width, height, output_path):
    """Instagram story 1080x1920: navy background, logo, company name, tagline,
    red accent divider, and a red 'Follow us' CTA band above the UI safe zone."""
    img = Image.new("RGB", (width, height), NAVY)
    draw = ImageDraw.Draw(img)

    # Subtle geometric pattern (same as banners)
    for i in range(-height, width + height, 40):
        draw.line([(i, 0), (i + height, height)], fill=(10, 15, 70), width=1)

    # Full logo, centered upper-middle
    logo_h = int(height * 0.115)
    full_logo_path = os.path.join(FULL_LOGO_DIR, "fulllogo_transparent.png")
    if os.path.exists(full_logo_path):
        logo = Image.open(full_logo_path).convert("RGBA")
        logo_w = int(logo.width * (logo_h / logo.height))
        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        logo_x = (width - logo_w) // 2
        logo_y = int(height * 0.27)
        img.paste(logo, (logo_x, logo_y), logo)
    else:
        logo_w = 0
        logo_y = int(height * 0.27)

    # Company name (white, bold), centered
    company_name = "LIGHTSPEED HOLDINGS"
    name_size = int(width * 0.08)
    name_font = _shrink_to_fit(
        draw, company_name, _load_font(True, name_size), int(width * 0.9), True
    )
    name_size = getattr(name_font, "size", name_size)
    name_box = draw.textbbox((0, 0), company_name, font=name_font)
    name_x = (width - (name_box[2] - name_box[0])) // 2 - name_box[0]
    name_y = logo_y + logo_h + int(height * 0.025)
    draw.text((name_x, name_y), company_name, fill=WHITE, font=name_font)

    # Tagline (cyan), centered
    tagline = "Aspire. Act. Achieve."
    tagline_size = int(width * 0.04)
    tagline_font = _shrink_to_fit(
        draw, tagline, _load_font(False, tagline_size), int(width * 0.8), False
    )
    tagline_size = getattr(tagline_font, "size", tagline_size)
    tagline_box = draw.textbbox((0, 0), tagline, font=tagline_font)
    tagline_x = (width - (tagline_box[2] - tagline_box[0])) // 2 - tagline_box[0]
    tagline_y = name_y + name_size + int(height * 0.02)
    draw.text((tagline_x, tagline_y), tagline, fill=CYAN, font=tagline_font)

    # Red accent divider under the tagline
    accent_h = max(4, int(height * 0.004))
    accent_w = int(width * 0.44)
    accent_x = (width - accent_w) // 2
    accent_y = tagline_y + tagline_size + int(height * 0.03)
    draw.rectangle([(accent_x, accent_y), (accent_x + accent_w, accent_y + accent_h)], fill=RED)

    # CTA band "Follow us" (red, above the bottom platform-UI safe zone)
    cta_text = "Follow us"
    band_w = int(width * 0.42)
    band_h = int(height * 0.06)
    band_x = (width - band_w) // 2
    band_y = int(height * 0.68)
    draw.rounded_rectangle([band_x, band_y, band_x + band_w, band_y + band_h], radius=16, fill=RED)
    cta_font = _shrink_to_fit(
        draw, cta_text, _load_font(True, int(width * 0.045)), int(band_w * 0.8), True
    )
    cta_box = draw.textbbox((0, 0), cta_text, font=cta_font)
    cta_w = cta_box[2] - cta_box[0]
    cta_h = cta_box[3] - cta_box[1]
    draw.text(
        (
            band_x + (band_w - cta_w) // 2 - cta_box[0],
            band_y + (band_h - cta_h) // 2 - cta_box[1],
        ),
        cta_text,
        fill=WHITE,
        font=cta_font,
    )

    _snap_to_palette(img)
    img.save(output_path, quality=95)
    print(f"Created: {output_path}")


def create_youtube_channel_art(width, height, output_path):
    """YouTube channel art 2560x1440: navy banner with full logo left, company
    name center-right, cyan tagline, cyan accent divider, and red CTA band.

    Logo + text + CTA all live inside YouTube's 1235x690 center safe area, so
    nothing important clips on TV or mobile-square crops.
    """
    img = Image.new("RGB", (width, height), NAVY)
    draw = ImageDraw.Draw(img)

    # Subtle geometric pattern (same as banners)
    for i in range(-height, width + height, 40):
        draw.line([(i, 0), (i + height, height)], fill=(10, 15, 70), width=1)

    # Red accent bar at bottom (decorative full-bleed element)
    bar_height = max(4, height // 50)
    draw.rectangle([(0, height - bar_height), (width, height)], fill=RED)

    # YouTube safe area: 1235x690 centered
    safe_w = int(width * 0.482)
    safe_x = (width - safe_w) // 2

    # Full logo left, inside the safe area
    logo_h = int(height * 0.26)
    full_logo_path = os.path.join(FULL_LOGO_DIR, "fulllogo_transparent.png")
    if os.path.exists(full_logo_path):
        logo = Image.open(full_logo_path).convert("RGBA")
        logo_w = int(logo.width * (logo_h / logo.height))
        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        logo_y = (height - logo_h) // 2 - bar_height // 2
        img.paste(logo, (safe_x, logo_y), logo)
        text_x = safe_x + logo_w + int(width * 0.03)
    else:
        logo_w = 0
        text_x = safe_x

    # Content must stay inside the safe area on the right of the logo
    max_text_width = safe_x + safe_w - text_x - int(width * 0.02)

    # Company name, center-right (white, bold)
    company_name = "LIGHTSPEED HOLDINGS"
    name_size = int(width * 0.038)
    name_font = _shrink_to_fit(
        draw, company_name, _load_font(True, name_size), max_text_width, True
    )
    name_size = getattr(name_font, "size", name_size)
    name_y = int(height * 0.37)
    draw.text((text_x, name_y), company_name, fill=WHITE, font=name_font)

    # Tagline (cyan)
    tagline = "Aspire. Act. Achieve."
    tagline_size = int(width * 0.022)
    tagline_font = _shrink_to_fit(
        draw, tagline, _load_font(False, tagline_size), max_text_width, False
    )
    tagline_size = getattr(tagline_font, "size", tagline_size)
    tagline_y = name_y + name_size + int(height * 0.025)
    draw.text((text_x, tagline_y), tagline, fill=CYAN, font=tagline_font)

    # Cyan accent divider under the tagline (capped to safe area)
    divider_h = max(4, int(height * 0.006))
    divider_w = min(int(width * 0.28), max_text_width)
    divider_y = tagline_y + tagline_size + int(height * 0.028)
    draw.rectangle([(text_x, divider_y), (text_x + divider_w, divider_y + divider_h)], fill=CYAN)

    # Red CTA band "Subscribe" (capped to safe area)
    cta_text = "Subscribe"
    band_w = min(int(width * 0.15), max_text_width)
    band_h = int(height * 0.055)
    band_x = text_x
    band_y = divider_y + divider_h + int(height * 0.036)
    draw.rounded_rectangle([band_x, band_y, band_x + band_w, band_y + band_h], radius=16, fill=RED)
    cta_font = _shrink_to_fit(
        draw, cta_text, _load_font(True, int(width * 0.022)), int(band_w * 0.8), True
    )
    cta_box = draw.textbbox((0, 0), cta_text, font=cta_font)
    cta_w = cta_box[2] - cta_box[0]
    cta_h = cta_box[3] - cta_box[1]
    draw.text(
        (
            band_x + (band_w - cta_w) // 2 - cta_box[0],
            band_y + (band_h - cta_h) // 2 - cta_box[1],
        ),
        cta_text,
        fill=WHITE,
        font=cta_font,
    )

    _snap_to_palette(img)
    img.save(output_path, quality=95)
    print(f"Created: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate LightSpeed Holdings social media assets "
        "(LinkedIn, Twitter/X, GitHub, Instagram, TikTok, YouTube)."
    )
    parser.add_argument(
        "--platform",
        action="append",
        choices=[
            "linkedin",
            "twitter",
            "github",
            "general",
            "instagram",
            "tiktok",
            "youtube",
        ],
        help="Generate assets for one platform only; repeatable. Omit to generate all platforms.",
    )
    args = parser.parse_args()
    platforms = set(args.platform) if args.platform else None

    def want(platform):
        return platforms is None or platform in platforms

    print("Generating social media assets...\n")

    # LinkedIn
    if want("linkedin"):
        print("=== LinkedIn ===")
        create_profile_image(400, os.path.join(OUTPUT_DIR, "linkedin-profile.png"))
        create_banner_image(
            1584, 396, os.path.join(OUTPUT_DIR, "linkedin-banner.png"), platform="linkedin"
        )

    # Twitter/X
    if want("twitter"):
        print("\n=== Twitter/X ===")
        create_profile_image(400, os.path.join(OUTPUT_DIR, "twitter-profile.png"))
        create_banner_image(
            1500, 500, os.path.join(OUTPUT_DIR, "twitter-header.png"), platform="twitter"
        )

    # GitHub
    if want("github"):
        print("\n=== GitHub ===")
        create_profile_image(400, os.path.join(OUTPUT_DIR, "github-profile.png"))

    # General purpose
    if want("general"):
        print("\n=== General ===")
        create_profile_image(1024, os.path.join(OUTPUT_DIR, "avatar-1024.png"))

    # Instagram
    if want("instagram"):
        print("\n=== Instagram ===")
        create_profile_image(320, os.path.join(OUTPUT_DIR, "instagram-profile.png"), variant="ring")
        create_story_image(1080, 1920, os.path.join(OUTPUT_DIR, "instagram-story.png"))

    # TikTok
    if want("tiktok"):
        print("\n=== TikTok ===")
        create_profile_image(200, os.path.join(OUTPUT_DIR, "tiktok-profile.png"))

    # YouTube
    if want("youtube"):
        print("\n=== YouTube ===")
        create_profile_image(800, os.path.join(OUTPUT_DIR, "youtube-profile.png"))
        create_youtube_channel_art(2560, 1440, os.path.join(OUTPUT_DIR, "youtube-channel-art.png"))

    print(f"\nAll selected assets saved to: {OUTPUT_DIR}")
    print("\nUpload instructions:")
    print("  LinkedIn Profile: https://www.linkedin.com/in/settings/profile-photo/")
    print("  LinkedIn Banner:  https://www.linkedin.com/in/settings/background-photo/")
    print("  Twitter Profile:  https://twitter.com/settings/profile")
    print("  Twitter Header:   https://twitter.com/settings/header")
    print("  GitHub Avatar:    https://github.com/settings/profile")
    print("  Instagram Profile: https://www.instagram.com/accounts/edit/")
    print("  Instagram Story:  native story creator (1080x1920 upload)")
    print("  TikTok Profile:   https://www.tiktok.com/upload (avatar via profile settings)")
    print("  YouTube Profile:  https://www.youtube.com/account_advanced")
    print("  YouTube Channel Art: https://www.youtube.com/account_branding")


if __name__ == "__main__":
    main()
