#!/usr/bin/env python3
"""QA: verify dimensions and brand-palette compliance of generated assets.

Official logo pixels are exempt: logos are pasted AFTER snap_to_palette and
must never be altered (social-card spec), so their exact bboxes are excluded.
"""

import os

from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
OUT = os.path.join(ROOT, "static", "brand", "social")
MARK = os.path.join(ROOT, "brand", "logo", "logo-mark.png")

TOKENS = {(7, 10, 64), (220, 54, 65), (0, 191, 255), (255, 255, 255)}
TOL = 24  # nearest-token distance tolerance for anti-aliased glyph edges

EXPECTED = {
    "facebook-post.png": (1200, 628),
    "linkedin-post.png": (1200, 627),
    "linkedin-carousel-1.png": (1200, 627),
    "linkedin-carousel-2.png": (1200, 627),
    "linkedin-carousel-3.png": (1200, 627),
    "x-post.png": (1600, 900),
    "x-thread-1.png": (1600, 900),
    "x-thread-2.png": (1600, 900),
    "x-thread-3.png": (1600, 900),
    "x-thread-4.png": (1600, 900),
    "x-thread-5.png": (1600, 900),
    "ig-post.png": (1080, 1080),
    "ig-carousel-1.png": (1080, 1080),
    "ig-carousel-2.png": (1080, 1080),
    "ig-carousel-3.png": (1080, 1080),
    "ig-story.png": (1080, 1920),
    "letterhead.png": (2550, 3300),
    "business-card-front.png": (1050, 600),
    "business-card-back.png": (1050, 600),
}


def mark_box(x, y, h):
    """Bbox where the keyed/cropped official mark is pasted."""
    logo = Image.open(MARK).convert("RGBA")
    px = logo.load()
    for yy in range(logo.height):
        for xx in range(logo.width):
            r, g, b, _ = px[xx, yy]
            if r >= 245 and g >= 245 and b >= 245:
                px[xx, yy] = (0, 0, 0, 0)
    bbox = logo.getbbox()
    if bbox:
        logo = logo.crop(bbox)
    w = int(logo.width * (h / logo.height))
    return (x, y, x + w, y + h)


def square_box(x, y, h):
    """Bbox of the square 1254x1254 lockup pasted at height h."""
    return (x, y, x + h, y + h)


def logo_regions(name):
    if name in ("facebook-post.png", "linkedin-post.png") or name.startswith("linkedin-carousel"):
        return [mark_box(48, 48, 80)]
    if name.startswith("x-"):
        return [mark_box(48, 48, 56)]
    if name.startswith("ig-post") or name.startswith("ig-carousel"):
        return [mark_box(40, 40, 56)]
    if name == "ig-story.png":
        return [mark_box(48, 48, 56)]
    if name == "letterhead.png":
        return [square_box(180, 180, 220)]
    if name == "business-card-front.png":
        return [square_box(60, 60, 140)]
    return []


failures = []
for name, size in EXPECTED.items():
    path = os.path.join(OUT, name)
    if not os.path.exists(path):
        failures.append(f"MISSING {name}")
        continue
    img = Image.open(path).convert("RGB")
    if img.size != size:
        failures.append(f"DIM {name}: {img.size} != {size}")
    regions = logo_regions(name)
    exempt_area = sum((r[2] - r[0] + 1) * (r[3] - r[1] + 1) for r in regions)
    px = img.load()
    bad = 0
    checked = img.width * img.height - exempt_area
    for y in range(img.height):
        spans = [(r[0], r[2]) for r in regions if r[1] <= y <= r[3]]
        for x in range(img.width):
            if any(x0 <= x <= x1 for x0, x1 in spans):
                continue
            r, g, b = px[x, y]
            if min((r - t[0]) ** 2 + (g - t[1]) ** 2 + (b - t[2]) ** 2 for t in TOKENS) > TOL**2:
                bad += 1
    pct = 100.0 * bad / checked
    if pct > 0.05:
        failures.append(f"PALETTE {name}: {pct:.3f}% off-palette (limit 0.05%)")
    else:
        print(f"OK {name} {img.size} off-palette={pct:.4f}% exempt={exempt_area}px")

print()
if failures:
    print("FAILURES:")
    for f in failures:
        print("  " + f)
    raise SystemExit(1)
print("ALL QA CHECKS PASSED (19 assets)")
