#!/usr/bin/env python3
"""Generate remaining LightSpeed brand assets: X, Instagram, email, letterhead, business card."""

import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
OUT = os.path.join(ROOT, "static", "brand", "social")
os.makedirs(OUT, exist_ok=True)

NAVY = (7, 10, 64)
RED = (220, 54, 65)
CYAN = (0, 191, 255)
WHITE = (255, 255, 255)
LIGHT = (242, 242, 242)

LOGO_MARK = os.path.join(ROOT, "brand", "logo", "logo-mark.png")
LOGO_FULL_LIGHT = os.path.join(ROOT, "brand", "logo", "logo-light-bg.png")
# logo-dark-bg.png rasterised white-on-white (unusable); logo-full.png has the
# navy lockup whose baked #02062F tile snaps to #070A40 on paste+snap
LOGO_FULL_DARK = os.path.join(ROOT, "brand", "logo", "logo-full.png")


def snap_to_palette(img):
    px = img.load()
    w, h = img.size
    tokens = [NAVY, RED, CYAN, WHITE]
    for y in range(h):
        for x in range(w):
            p = px[x, y]
            if len(p) == 4 and p[3] < 128:
                continue
            r, g, b = p[:3]
            best = min(tokens, key=lambda t: (r - t[0]) ** 2 + (g - t[1]) ** 2 + (b - t[2]) ** 2)
            if (r, g, b) != best:
                px[x, y] = best if len(p) == 3 else (*best, p[3])


def fnt(size, bold=False):
    for name in ("arialbd.ttf" if bold else "arial.ttf", "segoeuib.ttf" if bold else "segoeui.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def load_mark(height):
    """Official logo-mark with white background keyed to transparent (all-white
    pixels in logo-mark.png are border-connected, so keying removes only bg)."""
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
    return logo.resize((w, height), Image.Resampling.LANCZOS)


def paste_logo_mark(img, x, y, h):
    logo = load_mark(h)
    img.paste(logo, (x, y), logo)
    return logo.width


def load_lockup_dark(height):
    """logo-full.png with its baked #02062F canvas keyed to transparent
    (border-connected flood fill only, artwork untouched), same 1254x1254
    geometry so QA exemption bbox stays valid."""
    logo = Image.open(LOGO_FULL_DARK).convert("RGBA")
    px = logo.load()
    w, h = logo.size

    def isbg(x, y):
        r, g, b, a = px[x, y]
        return a == 0 or (abs(r - 2) <= 10 and abs(g - 6) <= 10 and abs(b - 47) <= 12)

    seen = bytearray(w * h)
    from collections import deque

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
        base = y * w
        for x in range(w):
            if seen[base + x]:
                px[x, y] = (0, 0, 0, 0)
    return logo.resize((int(w * (height / h)), height), Image.Resampling.LANCZOS)


def paste_logo_lockup(img, x, y, h, dark_bg=True):
    if dark_bg:
        logo = load_lockup_dark(h)
    else:
        src = LOGO_FULL_LIGHT
        if not os.path.exists(src):
            return paste_logo_mark(img, x, y, h)
        logo = Image.open(src).convert("RGBA")
        logo = logo.resize((int(logo.width * (h / logo.height)), h), Image.Resampling.LANCZOS)
    img.paste(logo, (x, y), logo)
    return logo.width


def stamp_card(img, margin):
    """Paste official keyed mark after snap at (margin, margin) h=56."""
    logo = load_mark(56)
    img.paste(logo, (margin, margin), logo)


def base_card(width, height, dark=True, margin=48):
    bg = NAVY if dark else LIGHT
    img = Image.new("RGB", (width, height), bg)
    d = ImageDraw.Draw(img)
    return img, d


def draw_cta(d, img, text, dark=True):
    f = fnt(15, bold=True)
    box = d.textbbox((0, 0), text, font=f)
    w = box[2] - box[0] + 48
    h = box[3] - box[1] + 24
    x = img.width - 48 - w
    y = img.height - 48 - h
    d.rectangle([(x, y), (x + w, y + h)], fill=RED)
    d.text((x + 24 - box[0], y + 12 - box[1]), text, fill=WHITE, font=f)


def headline_block(d, img, eyebrow, headline, dark=True, y0=160):
    fg = WHITE if dark else NAVY
    ey = CYAN if dark else RED
    ef = fnt(18, bold=True)
    d.text((48, y0), eyebrow.upper(), fill=ey, font=ef)
    hf = fnt(56, bold=True)
    words = headline.split()
    lines, cur = [], ""
    maxw = img.width - 96
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textbbox((0, 0), trial, font=hf)[2] <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    y = y0 + 44
    for line in lines:
        d.text((48, y), line, fill=fg, font=hf)
        y += hf.size + 16
    return y


def x_post():
    img, d = base_card(1600, 900, dark=True)
    headline_block(d, img, "Whitepaper", "Governed Agentic AI for Southern Africa")
    draw_cta(d, img, "Download the report")
    snap_to_palette(img)
    stamp_card(img, 48)
    img.save(os.path.join(OUT, "x-post.png"), quality=95)
    print("x-post.png (1600x900)")


def x_thread():
    cards = [
        ("Thread 1/5", "Why agentic AI needs governance now"),
        ("Thread 2/5", "Four skeptic objections, answered"),
        ("Thread 3/5", "Bandwidth, data protection, tech debt"),
        ("Thread 4/5", "A SADC policy framework proposal"),
        ("Thread 5/5", "Read the full whitepaper"),
    ]
    for i, (eyebrow, head) in enumerate(cards, 1):
        img, d = base_card(1600, 900, dark=(i % 2 == 1))
        headline_block(d, img, eyebrow, head, dark=(i % 2 == 1))
        draw_cta(d, img, "Read more", dark=(i % 2 == 1))
        snap_to_palette(img)
        stamp_card(img, 48)
        img.save(os.path.join(OUT, f"x-thread-{i}.png"), quality=95)
    print("x-thread-1..5.png (1600x900)")


def ig_post():
    img, d = base_card(1080, 1080, dark=True, margin=40)
    headline_block(d, img, "LightSpeed Holdings", "ASPIRE. ACT. ACHIEVE.")
    draw_cta(d, img, "Visit lightspeedholdings.vercel.app")
    snap_to_palette(img)
    stamp_card(img, 40)
    img.save(os.path.join(OUT, "ig-post.png"), quality=95)
    print("ig-post.png (1080x1080)")


def ig_carousel():
    titles = ["The Opportunity", "The Framework", "The Next Step"]
    for i, t in enumerate(titles, 1):
        img, d = base_card(1080, 1080, dark=True, margin=40)
        headline_block(d, img, f"Card {i} of 3", t)
        draw_cta(d, img, "Swipe")
        snap_to_palette(img)
        stamp_card(img, 40)
        img.save(os.path.join(OUT, f"ig-carousel-{i}.png"), quality=95)
    print("ig-carousel-1..3.png (1080x1080)")


def ig_story():
    img, d = base_card(1080, 1920, dark=True, margin=48)
    headline_block(d, img, "Story", "Build with governed AI", y0=700)
    draw_cta(d, img, "Learn more")
    snap_to_palette(img)
    stamp_card(img, 48)
    img.save(os.path.join(OUT, "ig-story.png"), quality=95)
    print("ig-story.png (1080x1920)")


def letterhead():
    W, H = 2550, 3300
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle([(0, H - 260), (W, H)], fill=NAVY)
    d.text((180, H - 190), "ASPIRE. ACT. ACHIEVE.", fill=CYAN, font=fnt(40, bold=True))
    d.text(
        (180, H - 120),
        "Jack Mlusu  |  jmlusu@gmail.com  |  +265 (0) 980 016 004  |  lightspeedholdings.vercel.app",
        fill=WHITE,
        font=fnt(32),
    )
    d.line([(180, 520), (W - 180, 520)], fill=RED, width=8)
    snap_to_palette(img)
    paste_logo_lockup(img, 180, 180, 220, dark_bg=False)
    img.save(os.path.join(OUT, "letterhead.png"), quality=95)
    print("letterhead.png (2550x3300)")


def business_card():
    W, H = 1050, 600
    front = Image.new("RGB", (W, H), NAVY)
    fd = ImageDraw.Draw(front)
    fd.text((60, H - 160), "ASPIRE. ACT. ACHIEVE.", fill=CYAN, font=fnt(36, bold=True))
    snap_to_palette(front)
    paste_logo_lockup(front, 60, 60, 140, dark_bg=True)
    front.save(os.path.join(OUT, "business-card-front.png"), quality=95)

    back = Image.new("RGB", (W, H), LIGHT)
    bd = ImageDraw.Draw(back)
    bd.rectangle([(0, 0), (16, H)], fill=RED)
    bd.text((60, 90), "Jack Mlusu", fill=NAVY, font=fnt(52, bold=True))
    bd.text((60, 170), "Chief Executive Officer", fill=RED, font=fnt(34))
    bd.text((60, 300), "jmlusu@gmail.com", fill=NAVY, font=fnt(32))
    bd.text((60, 360), "+265 (0) 980 016 004", fill=NAVY, font=fnt(32))
    bd.text((60, 420), "lightspeedholdings.vercel.app", fill=CYAN, font=fnt(32))
    snap_to_palette(back)
    back.save(os.path.join(OUT, "business-card-back.png"), quality=95)
    print("business-card-front.png, business-card-back.png (1050x600)")


def email_html():
    html = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LightSpeed Holdings</title></head>
<body style="margin:0;padding:0;background-color:#F2F2F2;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#F2F2F2">
<tr><td align="center" style="padding:24px 8px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#FFFFFF;">
<tr><td bgcolor="#070A40" style="padding:32px;">
<img src="https://lightspeedholdings.vercel.app/brand/logo/logo-light-bg.png" alt="LightSpeed Holdings logo" width="220" style="display:block;border:0;">
</td></tr>
<tr><td style="padding:32px;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:1.6;color:#070A40;">
<h1 style="margin:0 0 16px 0;font-size:24px;color:#070A40;">Governed agentic AI for Southern Africa</h1>
<p style="margin:0 0 16px 0;">Our new whitepaper sets out a policy-ready framework for deploying agentic AI across the SADC region — addressing bandwidth, data protection, technology debt, and AI skepticism head-on.</p>
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
<td bgcolor="#DC3641" style="border-radius:4px;">
<a href="https://lightspeedholdings.vercel.app" style="display:inline-block;padding:14px 32px;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;color:#FFFFFF;text-decoration:none;">Download the whitepaper</a>
</td></tr></table>
</td></tr>
<tr><td bgcolor="#070A40" style="padding:24px 32px;font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.6;color:#FFFFFF;">
<strong style="color:#00BFFF;">ASPIRE. ACT. ACHIEVE.</strong><br>
LightSpeed Holdings Limited&trade;<br>
Jack Mlusu &middot; jmlusu@gmail.com &middot; +265 (0) 980 016 004<br>
<a href="https://lightspeedholdings.vercel.app" style="color:#00BFFF;">lightspeedholdings.vercel.app</a>
</td></tr>
</table>
</td></tr></table>
</body></html>"""
    with open(os.path.join(OUT, "email-whitepaper.html"), "w", encoding="utf-8") as fh:
        fh.write(html)
    txt = """ASPIRE. ACT. ACHIEVE.

Governed agentic AI for Southern Africa

Our new whitepaper sets out a policy-ready framework for deploying agentic AI
across the SADC region - addressing bandwidth, data protection, technology
debt, and AI skepticism head-on.

Download the whitepaper: https://lightspeedholdings.vercel.app

--
LightSpeed Holdings Limited
Jack Mlusu | jmlusu@gmail.com | +265 (0) 980 016 004
https://lightspeedholdings.vercel.app
"""
    with open(os.path.join(OUT, "email-whitepaper.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt)
    print("email-whitepaper.html + .txt (600px table layout)")


if __name__ == "__main__":
    x_post()
    x_thread()
    ig_post()
    ig_carousel()
    ig_story()
    letterhead()
    business_card()
    email_html()
    print("\nAll remaining assets written to", OUT)
