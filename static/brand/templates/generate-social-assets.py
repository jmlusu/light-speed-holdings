"""
LightSpeed Holdings â€” Social Media Asset Generator
Creates LinkedIn and Twitter/X profile and banner images using Pillow.
Brand: LightSpeed Holdings Limited | Tagline: Aspire. Act. Achieve.
Colors: Navy #070A40, Red #E63946, Cyan #00BFFF, Grey #F2F2F2
"""

import os

from PIL import Image, ImageDraw, ImageFont

# Brand Colors
NAVY = (7, 10, 64)
RED = (230, 57, 70)
CYAN = (0, 191, 255)
WHITE = (255, 255, 255)
GREY = (242, 242, 242)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_DIR = os.path.join(SCRIPT_DIR, "..", "logos", "icononly")
FULL_LOGO_DIR = os.path.join(SCRIPT_DIR, "..", "logos", "fulllogo")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "social")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def create_profile_image(size, output_path, variant="default"):
    """Create a profile image with the icon logo on navy background."""
    img = Image.new("RGB", (size, size), NAVY)
    draw = ImageDraw.Draw(img)

    # Load icon logo
    icon_path = os.path.join(LOGO_DIR, "icononly_transparent.png")
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA")
        # Calculate size to fit (60% of canvas)
        icon_size = int(size * 0.5)
        icon = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        # Center
        offset = (size - icon_size) // 2
        img.paste(icon, (offset, offset), icon)
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

    img.save(output_path, quality=95)
    print(f"Created: {output_path}")


def main():
    print("Generating social media assets...\n")

    # LinkedIn
    print("=== LinkedIn ===")
    create_profile_image(400, os.path.join(OUTPUT_DIR, "linkedin-profile.png"))
    create_banner_image(
        1584, 396, os.path.join(OUTPUT_DIR, "linkedin-banner.png"), platform="linkedin"
    )

    # Twitter/X
    print("\n=== Twitter/X ===")
    create_profile_image(400, os.path.join(OUTPUT_DIR, "twitter-profile.png"))
    create_banner_image(
        1500, 500, os.path.join(OUTPUT_DIR, "twitter-header.png"), platform="twitter"
    )

    # GitHub
    print("\n=== GitHub ===")
    create_profile_image(400, os.path.join(OUTPUT_DIR, "github-profile.png"))

    # General purpose
    print("\n=== General ===")
    create_profile_image(1024, os.path.join(OUTPUT_DIR, "avatar-1024.png"))

    print(f"\nAll assets saved to: {OUTPUT_DIR}")
    print("\nUpload instructions:")
    print("  LinkedIn Profile: https://www.linkedin.com/in/settings/profile-photo/")
    print("  LinkedIn Banner:  https://www.linkedin.com/in/settings/background-photo/")
    print("  Twitter Profile:  https://twitter.com/settings/profile")
    print("  Twitter Header:   https://twitter.com/settings/header")
    print("  GitHub Avatar:    https://github.com/settings/profile")


if __name__ == "__main__":
    main()
