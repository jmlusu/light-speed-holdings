"""
LightSpeed Holdings - Social Card & Favicon Bundle Generator
Generates Open Graph (1200x630) and Twitter Card (1200x628) social cards
plus complete favicon bundle (ICO, PNG, Apple touch icon, Android Chrome).
Brand: LightSpeed Holdings Limited | Tagline: ASPIRE. ACT. ACHIEVE.
Colors: Navy #070A40, Red #E63946, Cyan #00BFFF
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Brand Colors
NAVY = (7, 10, 64)
RED = (230, 57, 70)
CYAN = (0, 191, 255)
WHITE = (255, 255, 255)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BRAND_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "..", "brand"))

def _canonical_or_mirror(*parts):
    canonical = os.path.join(BRAND_ROOT, *parts)
    if os.path.exists(canonical):
        return canonical
    mirror = os.path.join(SCRIPT_DIR, "..", *parts)
    return mirror

LOGO_DIR = _canonical_or_mirror("logos", "icononly")
FULL_LOGO_DIR = _canonical_or_mirror("logos", "fulllogo")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "digital")
FAVICON_DIR = os.path.join(OUTPUT_DIR, "favicon")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FAVICON_DIR, exist_ok=True)

PALETTE = [NAVY, RED, CYAN, WHITE, (242, 242, 242), (107, 114, 128), (156, 163, 175)]

def _snap_to_palette(img):
    """Snap every visible pixel to the nearest exact brand token color. Returns the modified image."""
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
    return img

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

def create_open_graph_image(width=1200, height=630, output_path=None):
    """Create Open Graph image (1200x630) with icon logo, company name, tagline."""
    if output_path is None:
        output_path = os.path.join(OUTPUT_DIR, "social-card-og.png")
    
    img = Image.new("RGB", (width, height), NAVY)
    draw = ImageDraw.Draw(img)
    
    # Grid: 4px base unit. Canvas 1200x630 = 300x157.5 grid units
    # Top margin: 32px (8 grid units)
    # Logo: 40x40px at (32, 32) - 10x10 grid units
    # Title: 32px below logo bottom
    # Tagline: 24px below title
    
    # Load icon-only logo
    icon_path = os.path.join(LOGO_DIR, "icononly_transparent.png")
    logo_size = 40
    logo_x = 32
    logo_y = 32
    
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA")
        icon = icon.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        img.paste(icon, (logo_x, logo_y), icon)
    else:
        # Fallback: draw "LS" text
        font = _load_font(True, int(logo_size * 0.6))
        text = "LS"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.text((logo_x + (logo_size - text_w) // 2, logo_y + (logo_size - text_h) // 2), 
                  text, fill=WHITE, font=font)
    
    # Company name: 32pt title-xl, white, positioned 32px below logo bottom
    company_name = "LightSpeed Holdings Limited™"
    name_y = logo_y + logo_size + 32
    max_name_width = width - 96  # 48px margins on each side
    
    name_font = _shrink_to_fit(draw, company_name, _load_font(True, 32), max_name_width, True)
    draw.text((48, name_y), company_name, fill=WHITE, font=name_font)
    
    # Tagline: 18pt body, white, centered, 24px below title
    tagline = "ASPIRE. ACT. ACHIEVE."
    tagline_y = name_y + getattr(name_font, "size", 32) + 24
    tagline_font = _shrink_to_fit(draw, tagline, _load_font(False, 18), width - 96, False)
    tagline_bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
    tagline_w = tagline_bbox[2] - tagline_bbox[0]
    draw.text(((width - tagline_w) // 2, tagline_y), tagline, fill=WHITE, font=tagline_font)
    
    # Description: 14pt body-sm, cyan accent, max 20 words
    description = "AI-native company building for Malawi and SADC"
    desc_y = tagline_y + getattr(tagline_font, "size", 18) + 16
    desc_font = _shrink_to_fit(draw, description, _load_font(False, 14), width - 96, False)
    desc_bbox = draw.textbbox((0, 0), description, font=desc_font)
    desc_w = desc_bbox[2] - desc_bbox[0]
    draw.text(((width - desc_w) // 2, desc_y), description, fill=CYAN, font=desc_font)
    
    # Bottom accent bar (red, 4px high at bottom)
    bar_height = 4
    draw.rectangle([(0, height - bar_height), (width, height)], fill=RED)
    
    _snap_to_palette(img)
    img.save(output_path, quality=95)
    print(f"Created: {output_path}")
    return output_path

def create_twitter_card_image(width=1200, height=628, output_path=None):
    """Create Twitter Card summary large image (1200x628)."""
    if output_path is None:
        output_path = os.path.join(OUTPUT_DIR, "social-card-twitter.png")
    # Same as OG but 2px shorter - reuse with adjusted height
    return create_open_graph_image(width, height, output_path)

def create_favicon_ico(output_path=None):
    """Create favicon.ico with 16x16, 32x32, 48x48 sizes."""
    if output_path is None:
        output_path = os.path.join(FAVICON_DIR, "favicon.ico")
    
    sizes = [(16, 16), (32, 32), (48, 48)]
    images = []
    
    icon_path = os.path.join(LOGO_DIR, "icononly_transparent.png")
    
    for size in sizes:
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        
        if os.path.exists(icon_path):
            icon = Image.open(icon_path).convert("RGBA")
            # Scale to fit with padding
            padding = max(1, size[0] // 8)
            icon_max = size[0] - 2 * padding
            icon_ratio = icon.width / icon.height
            if icon_ratio > 1:
                icon_w = icon_max
                icon_h = int(icon_max / icon_ratio)
            else:
                icon_h = icon_max
                icon_w = int(icon_max * icon_ratio)
            icon = icon.resize((icon_w, icon_h), Image.Resampling.LANCZOS)
            offset_x = (size[0] - icon_w) // 2
            offset_y = (size[1] - icon_h) // 2
            img.paste(icon, (offset_x, offset_y), icon)
        else:
            # Fallback: draw "LS"
            draw = ImageDraw.Draw(img)
            font = _load_font(True, max(8, size[0] // 2))
            text = "LS"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            draw.text(((size[0] - text_w) // 2, (size[1] - text_h) // 2), text, fill=WHITE, font=font)
        
        _snap_to_palette(img.convert("RGB")).convert("RGBA")
        images.append(img)
    
    # Save as ICO
    images[0].save(output_path, format="ICO", sizes=[(img.width, img.height) for img in images])
    print(f"Created: {output_path}")
    return output_path

def create_favicon_png(size=32, output_path=None):
    """Create favicon.png (32x32)."""
    if output_path is None:
        output_path = os.path.join(FAVICON_DIR, "favicon.png")
    
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    
    icon_path = os.path.join(LOGO_DIR, "icononly_transparent.png")
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA")
        padding = max(2, size // 8)
        icon_max = size - 2 * padding
        icon_ratio = icon.width / icon.height
        if icon_ratio > 1:
            icon_w = icon_max
            icon_h = int(icon_max / icon_ratio)
        else:
            icon_h = icon_max
            icon_w = int(icon_max * icon_ratio)
        icon = icon.resize((icon_w, icon_h), Image.Resampling.LANCZOS)
        offset_x = (size - icon_w) // 2
        offset_y = (size - icon_h) // 2
        img.paste(icon, (offset_x, offset_y), icon)
    else:
        draw = ImageDraw.Draw(img)
        font = _load_font(True, size // 2)
        text = "LS"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.text(((size - text_w) // 2, (size - text_h) // 2), text, fill=WHITE, font=font)
    
    _snap_to_palette(img.convert("RGB")).convert("RGBA").save(output_path)
    print(f"Created: {output_path}")
    return output_path

def create_apple_touch_icon(size=180, output_path=None):
    """Create apple-touch-icon.png (180x180)."""
    if output_path is None:
        output_path = os.path.join(FAVICON_DIR, "apple-touch-icon.png")
    
    img = Image.new("RGB", (size, size), NAVY)
    
    icon_path = os.path.join(LOGO_DIR, "icononly_transparent.png")
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA")
        padding = max(8, size // 8)
        icon_max = size - 2 * padding
        icon_ratio = icon.width / icon.height
        if icon_ratio > 1:
            icon_w = icon_max
            icon_h = int(icon_max / icon_ratio)
        else:
            icon_h = icon_max
            icon_w = int(icon_max * icon_ratio)
        icon = icon.resize((icon_w, icon_h), Image.Resampling.LANCZOS)
        offset_x = (size - icon_w) // 2
        offset_y = (size - icon_h) // 2
        img.paste(icon, (offset_x, offset_y), icon)
    else:
        draw = ImageDraw.Draw(img)
        font = _load_font(True, size // 2)
        text = "LS"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.text(((size - text_w) // 2, (size - text_h) // 2), text, fill=WHITE, font=font)
    
    _snap_to_palette(img)
    img.save(output_path, quality=95)
    print(f"Created: {output_path}")
    return output_path

def create_android_chrome_icon(size, output_path=None):
    """Create android-chrome-{size}x{size}.png."""
    if output_path is None:
        output_path = os.path.join(FAVICON_DIR, f"android-chrome-{size}x{size}.png")
    
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    
    icon_path = os.path.join(LOGO_DIR, "icononly_transparent.png")
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA")
        padding = max(8, size // 8)
        icon_max = size - 2 * padding
        icon_ratio = icon.width / icon.height
        if icon_ratio > 1:
            icon_w = icon_max
            icon_h = int(icon_max / icon_ratio)
        else:
            icon_h = icon_max
            icon_w = int(icon_max * icon_ratio)
        icon = icon.resize((icon_w, icon_h), Image.Resampling.LANCZOS)
        offset_x = (size - icon_w) // 2
        offset_y = (size - icon_h) // 2
        img.paste(icon, (offset_x, offset_y), icon)
    else:
        draw = ImageDraw.Draw(img)
        font = _load_font(True, size // 2)
        text = "LS"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.text(((size - text_w) // 2, (size - text_h) // 2), text, fill=WHITE, font=font)
    
    _snap_to_palette(img.convert("RGB")).convert("RGBA").save(output_path)
    print(f"Created: {output_path}")
    return output_path

def main():
    print("Generating Social Card & Favicon Bundle...\n")
    
    # Social Cards
    print("=== Social Cards ===")
    create_open_graph_image()
    create_twitter_card_image()
    
    # Favicon Bundle
    print("\n=== Favicon Bundle ===")
    create_favicon_ico()
    create_favicon_png()
    create_apple_touch_icon()
    create_android_chrome_icon(192)
    create_android_chrome_icon(512)
    
    print(f"\nAll assets saved to:")
    print(f"  Social cards: {OUTPUT_DIR}")
    print(f"  Favicons:     {FAVICON_DIR}")

if __name__ == "__main__":
    main()