"""Embed the transparent LightSpeed symbol into the schematic SVG.

The symbol is cropped from `logo-dark-bg-transparent.png` (the only genuinely
transparent variant in brand/logo/), inlined as a base64 data URI so the SVG
stays a single self-contained file with no external asset dependency.
"""

import base64
import io
import re
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[4]
SRC = REPO_ROOT / "brand" / "logo" / "logo-dark-bg-transparent.png"
SVG = (
    REPO_ROOT
    / "artifacts"
    / "campaigns"
    / "2026-10-26-pipeline-test"
    / "open-design"
    / "schematic.svg"
)
SYMBOL_OUT = SVG.parent / "logo-symbol.png"

# Rendered height in CSS px, and the raster height used for crispness (2x)
DISPLAY_H = 48
RASTER_H = DISPLAY_H * 2


def extract_symbol(height: int) -> Image.Image:
    im = Image.open(SRC).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    w, h = im.size
    alpha = im.getchannel("A")

    cut, band_start = h, None
    for y in range(h):
        empty = alpha.crop((0, y, w, y + 1)).getextrema()[1] == 0
        if empty:
            if band_start is None:
                band_start = y
        else:
            if band_start is not None and y - band_start >= 20:
                cut = band_start
                break
            band_start = None

    im = im.crop((0, 0, w, cut))
    im = im.crop(im.getchannel("A").getbbox())
    new_w = round(im.size[0] * height / im.size[1])
    return im.resize((new_w, height), Image.LANCZOS)


symbol = extract_symbol(RASTER_H)
symbol.save(SYMBOL_OUT)

buf = io.BytesIO()
symbol.save(buf, format="PNG", optimize=True)
b64 = base64.b64encode(buf.getvalue()).decode("ascii")

display_w = round(symbol.size[0] * DISPLAY_H / symbol.size[1])

svg = SVG.read_text(encoding="utf-8")

# 1. Declare xlink so the embedded raster works in strict SVG 1.1 renderers.
if "xmlns:xlink" not in svg:
    svg = svg.replace(
        'xmlns="http://www.w3.org/2000/svg"',
        'xmlns="http://www.w3.org/2000/svg"\n  xmlns:xlink="http://www.w3.org/1999/xlink"',
        1,
    )

# 2. Insert the symbol at the top-left of the header band.
image_el = (
    f"  <!-- Transparent brand symbol (inlined from brand/logo/logo-dark-bg-transparent.png) -->\n"
    f'  <image x="48" y="30" width="{display_w}" height="{DISPLAY_H}"\n'
    f'         xlink:href="data:image/png;base64,{b64}"/>\n\n'
)
if "<image" not in svg:
    svg = svg.replace("  <!-- Header -->\n", "  <!-- Header -->\n" + image_el, 1)

# 3. Shift the title clear of the symbol.
svg = re.sub(
    r'<text x="48" y="64" (font-family="Arial[^>]*font-size="27")',
    r'<text x="140" y="64" \1',
    svg,
    count=1,
)

SVG.write_text(svg, encoding="utf-8")

print(f"symbol saved      : {SYMBOL_OUT.name} ({symbol.size[0]}x{symbol.size[1]} px)")
print(f"svg <image>       : x=48 y=30 w={display_w} h={DISPLAY_H}")
print(f"base64 payload    : {len(b64):,} chars")
print(f"svg size          : {SVG.stat().st_size:,} bytes")
