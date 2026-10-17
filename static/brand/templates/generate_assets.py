#!/usr/bin/env python3
"""Generate Facebook + LinkedIn brand assets (spec: brand/digital/social-card-spec.md)."""

import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
OUT = os.path.join(ROOT, "static", "brand", "social")
os.makedirs(OUT, exist_ok=True)

NAVY = (7, 10, 64)
RED = (220, 54, 65)
CYAN = (0, 191, 255)
WHITE = (255, 255, 255)

LOGO_MARK = os.path.join(ROOT, "brand", "logo", "logo-mark.png")


def snap_to_palette(img):
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            p = px[x, y]
            r, g, b = p[:3]
            best = min(
                [NAVY, RED, CYAN, WHITE],
                key=lambda t: (r - t[0]) ** 2 + (g - t[1]) ** 2 + (b - t[2]) ** 2,
            )
            if (r, g, b) != best:
                px[x, y] = best


def mark_size(height):
    """Crop+size the keyed official mark; returns (image, pasted width).
    Logo is pasted AFTER snap so official artwork is never altered (spec)."""
    logo = Image.open(LOGO_MARK).convert("RGBA")
    px = logo.load()
    for y in range(logo.height):
        for x in range(logo.width):
            r, g, b, a = px[x, y]
            if r >= 245 and g >= 245 and b >= 245:
                px[x, y] = (0, 0, 0, 0)
    bbox = logo.getbbox()
    if bbox:
        logo = logo.crop(bbox)
    w = int(logo.width * (height / logo.height))
    return logo.resize((w, height), Image.Resampling.LANCZOS), w


def fnt(size, bold=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def draw_cta(d, img, text, margin=48):
    """Spec: red CTA bottom-right, 48px from edges, white text, generous padding."""
    f = fnt(15, bold=True)
    box = d.textbbox((0, 0), text, font=f)
    w = (box[2] - box[0]) + 48
    h = (box[3] - box[1]) + 28
    x = img.width - margin - w
    y = img.height - margin - h
    d.rectangle([(x, y), (x + w, y + h)], fill=RED)
    d.text((x + 24 - box[0], y + 14 - box[1]), text, fill=WHITE, font=f)


def base(width, height):
    img = Image.new("RGB", (width, height), NAVY)
    d = ImageDraw.Draw(img)
    return img, d


def stamp(img):
    """Paste official mark at spec position (48,48) h=80, after snap."""
    logo, _ = mark_size(80)
    img.paste(logo, (48, 48), logo)


def title_block(d, img, company="LightSpeed Holdings Limited™", tagline="ASPIRE. ACT. ACHIEVE."):
    name_f = fnt(34, bold=True)
    box = d.textbbox((0, 0), company, font=name_f)
    x = (img.width - box[2] + box[0]) // 2
    y = (img.height - box[3]) // 2 - 30
    d.text((x, y), company, fill=WHITE, font=name_f)
    tag_f = fnt(18, bold=True)
    tbox = d.textbbox((0, 0), tagline, font=tag_f)
    tx = (img.width - tbox[2] + tbox[0]) // 2
    ty = y + box[3] + 24
    d.text((tx, ty), tagline, fill=WHITE, font=tag_f)
    return y + box[3]


def facebook_post():
    img, d = base(1200, 628)
    title_block(d, img)
    draw_cta(d, img, "Download Whitepaper")
    snap_to_palette(img)
    stamp(img)
    img.save(os.path.join(OUT, "facebook-post.png"), quality=95)
    print("facebook-post.png (1200x628)")


def linkedin_post():
    img, d = base(1200, 627)
    title_block(d, img)
    copy_f = fnt(15)
    copy = "Governed agentic AI is the region's next growth lever for policymakers."
    cbox = d.textbbox((0, 0), copy, font=copy_f)
    d.text(((img.width - cbox[2] + cbox[0]) // 2, 430), copy, fill=WHITE, font=copy_f)
    draw_cta(d, img, "Download Report")
    snap_to_palette(img)
    stamp(img)
    img.save(os.path.join(OUT, "linkedin-post.png"), quality=95)
    print("linkedin-post.png (1200x627)")


def linkedin_carousel():
    titles = ["Agentic AI Governance", "SADC Policy Opportunity", "LightSpeed Solution"]
    ctas = ["Download", "Learn More", "Read Now"]
    for i, (title, cta) in enumerate(zip(titles, ctas, strict=True), 1):
        img, d = base(1200, 627)
        name_f = fnt(30, bold=True)
        text = title + "™"
        box = d.textbbox((0, 0), text, font=name_f)
        x = (img.width - box[2] + box[0]) // 2
        y = (img.height - box[3]) // 2 - 20
        d.text((x, y), text, fill=WHITE, font=name_f)
        step_f = fnt(16, bold=True)
        step = f"Card {i} of 3"
        sbox = d.textbbox((0, 0), step, font=step_f)
        d.text(
            ((img.width - sbox[2] + sbox[0]) // 2, y + box[3] + 20), step, fill=CYAN, font=step_f
        )
        draw_cta(d, img, cta)
        snap_to_palette(img)
        stamp(img)
        img.save(os.path.join(OUT, f"linkedin-carousel-{i}.png"), quality=95)
    print("linkedin-carousel-1..3.png (1200x627)")


if __name__ == "__main__":
    facebook_post()
    linkedin_post()
    linkedin_carousel()
