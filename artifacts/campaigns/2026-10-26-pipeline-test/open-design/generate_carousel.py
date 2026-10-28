"""Generate the 5-card LightSpeed LinkedIn carousel (1200x627) + merged PDF.

Palette discipline: only exact brand token hex values are used, and text is
rendered with Pillow's ``fontmode="1"`` (anti-aliasing disabled) so every
visible pixel lands exactly on a token colour. This is what lets the
check_brand_palette.py gate pass at its strict 3% off-palette tolerance.

Layout discipline: each content card measures its own text block and centres
the whole group inside the content area, so no card carries dead space.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Paths resolve from the repo root so the script runs from any working directory:
# <root>/artifacts/campaigns/<slug>/open-design/generate_carousel.py
REPO_ROOT = Path(__file__).resolve().parents[4]
OUT = (
    REPO_ROOT / "artifacts" / "campaigns" / "2026-10-26-pipeline-test" / "open-design" / "carousel"
)
OUT.mkdir(parents=True, exist_ok=True)

# Canonical tokens (brand/tokens/brand-tokens.json)
NAVY = "#070A40"
CYAN = "#00BFFF"
RED = "#E63946"
WHITE = "#FFFFFF"
GREY_DARK = "#6B7280"
GREY_LIGHT_TEXT = "#9CA3AF"
DEEP_MINERAL = "#121518"
MORNING_MIST = "#F7F8F9"

W, H = 1200, 627
MARGIN = 56
COL_W = W - 2 * MARGIN

FONT_DIR = Path("C:/Windows/Fonts")
REG = FONT_DIR / "arial.ttf"
BOLD = FONT_DIR / "arialbd.ttf"
if not REG.is_file():
    raise SystemExit(f"Arial not found at {REG}")

# Transparent brand symbol (RGBA). Only logo-dark-bg-transparent.png is
# genuinely transparent in brand/logo/ (85.6% alpha=0); the other PNGs carry an
# opaque white background. We take its stacked lockup and crop the symbol that
# sits above the first wide empty band (the gap before the wordmark).
LOGO_SRC = REPO_ROOT / "brand" / "logo" / "logo-dark-bg-transparent.png"
LOGO_H = 34


def load_logo(height: int) -> Image.Image:
    im = Image.open(LOGO_SRC).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    w, h = im.size
    alpha = im.getchannel("A")

    # Locate the first empty band >=20px tall: the gap between symbol and wordmark.
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
    im = im.crop(im.getchannel("A").getbbox())  # tighten to the symbol itself
    new_w = max(1, round(im.size[0] * height / im.size[1]))
    return im.resize((new_w, height), Image.LANCZOS)


LOGO = load_logo(LOGO_H)

_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    key = (str(path), size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(str(path), size)
    return _cache[key]


def wrap(draw, text, fnt, max_width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = f"{cur} {w}".strip()
        if draw.textlength(test, font=fnt) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def new_card():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    d.fontmode = "1"  # disable anti-aliasing -> exact palette pixels
    return img, d


def chrome(img, d, idx: int):
    d.rectangle([0, 0, 6, H], fill=CYAN)
    d.rectangle([MARGIN, 84, W - MARGIN, 86], fill=CYAN)
    d.text(
        (W - MARGIN, 40), f"{idx:02d} / 05", font=font(BOLD, 18), fill=GREY_LIGHT_TEXT, anchor="ra"
    )
    # Transparent brand symbol, then the wordmark text (trademark requirement)
    img.paste(LOGO, (MARGIN, 28), LOGO)
    d.text(
        (MARGIN + LOGO.size[0] + 14, 40),
        "LIGHTSPEED HOLDINGS LIMITED",
        font=font(BOLD, 15),
        fill=CYAN,
        anchor="la",
    )
    d.rectangle([MARGIN, H - 76, W - MARGIN, H - 74], fill=GREY_DARK)
    d.text(
        (MARGIN, H - 56),
        "LightSpeed Holdings Limited\u2122",
        font=font(REG, 14),
        fill=WHITE,
        anchor="la",
    )
    d.text(
        (W - MARGIN, H - 56), "ASPIRE. ACT. ACHIEVE.", font=font(BOLD, 14), fill=CYAN, anchor="ra"
    )


AREA_TOP, AREA_BOTTOM = 108, 540


def content_card(
    idx,
    eyebrow,
    heading,
    para,
    strip_label,
    items,
    outline_last_red=False,
    item_w=None,
    item_gap=16,
):
    """Measured + vertically centred content card."""
    img, d = new_card()
    chrome(img, d, idx)

    f_eb = font(BOLD, 18)
    f_h = font(BOLD, 37)
    f_p = font(REG, 19)
    f_lbl = font(BOLD, 15)

    h_lines = wrap(d, heading, f_h, COL_W)
    p_lines = wrap(d, para, f_p, COL_W)

    EB_H, H_STEP, P_STEP = 32, 46, 30
    GAP_AFTER_PARA, LABEL_H, CHIP_H = 34, 28, 68

    total = EB_H + len(h_lines) * H_STEP + 8 + len(p_lines) * P_STEP
    if items:
        total += GAP_AFTER_PARA + LABEL_H + CHIP_H

    y = AREA_TOP + max(24, (AREA_BOTTOM - AREA_TOP - total) // 2)

    d.text((MARGIN, y), eyebrow, font=f_eb, fill=CYAN)
    y += EB_H
    for line in h_lines:
        d.text((MARGIN, y), line, font=f_h, fill=WHITE)
        y += H_STEP
    y += 8
    for line in p_lines:
        d.text((MARGIN, y), line, font=f_p, fill=MORNING_MIST)
        y += P_STEP

    if items:
        y += GAP_AFTER_PARA
        d.text((MARGIN, y), strip_label, font=f_lbl, fill=GREY_LIGHT_TEXT)
        y += LABEL_H
        n = len(items)
        gap = item_gap
        w = item_w or (COL_W - gap * (n - 1)) // n
        for i, (tag, label) in enumerate(items):
            x = MARGIN + i * (w + gap)
            is_last = i == n - 1
            colour = RED if (outline_last_red and is_last) else CYAN
            d.rectangle(
                [x, y, x + w, y + CHIP_H],
                fill=DEEP_MINERAL,
                outline=colour,
                width=2 if (is_last and outline_last_red) else 1,
            )
            d.text((x + 13, y + 12), tag, font=font(BOLD, 16), fill=colour)
            d.text((x + 13, y + 38), label, font=font(REG, 14), fill=MORNING_MIST)

    return img


# ---------------------------------------------------------------- card 1
img, d = new_card()
chrome(img, d, 1)
d.text((MARGIN, 148), "AGENTIC AI", font=font(BOLD, 17), fill=CYAN)
y = 184
for line in ["AGENTIC AI AS", "DIGITAL", "INFRASTRUCTURE"]:
    d.text((MARGIN, y), line, font=font(BOLD, 62), fill=WHITE)
    y += 66
d.rectangle([MARGIN, y + 16, MARGIN + 120, y + 22], fill=RED)
d.text(
    (MARGIN, y + 48),
    "Sovereign, offline-first deployment for African institutions.",
    font=font(REG, 20),
    fill=MORNING_MIST,
)
d.text((MARGIN, y + 86), "Malawi \u00b7 SADC \u00b7 2026", font=font(REG, 15), fill=GREY_LIGHT_TEXT)
img.save(OUT / "card-1.png")

# ---------------------------------------------------------------- card 2
content_card(
    2,
    "PILLAR 01",
    "SOVEREIGNTY-BY-DESIGN",
    "Data residency is not a policy add-on. It is hard-coded into the "
    "architecture. Local hosting removes reliance on external, high-latency "
    "cloud providers, so sensitive information does not leave the "
    "institution's own environment.",
    "DESIGN PRINCIPLES",
    [
        ("OFFLINE-FIRST", "Sync when available"),
        ("LOCAL INFERENCE", "Ollama / llama.cpp"),
        ("SOVEREIGN", "Data stays in-region"),
    ],
).save(OUT / "card-2.png")

# ---------------------------------------------------------------- card 3
content_card(
    3,
    "PILLAR 02",
    "PRACTICAL IMPLEMENTATION",
    "A 90-day pilot, not a transformation programme. We integrate agentic "
    "workflows into existing processes through thin, reversible seams, with "
    "an explicit decision gate at day 90: continue, adjust, or stop.",
    "90-DAY PILOT \u2014 FOUR PHASES",
    [
        ("DAYS 1-14", "Seam mapping"),
        ("DAYS 15-45", "Gated build"),
        ("DAYS 46-75", "Shadowed operations"),
        ("DAYS 76-90", "Decision gate"),
    ],
).save(OUT / "card-3.png")

# ---------------------------------------------------------------- card 4
content_card(
    4,
    "PILLAR 03",
    "ACCOUNTABILITY IN OPERATIONS",
    "Technology debt is treated as a transparent business metric. 90 agents "
    "(89 AI, 1 human CEO) run on a canonical seven-tool runtime under a "
    "five-tier human-in-the-loop gate. A timeout escalates. It never "
    "auto-approves.",
    "APPROVAL TIERS \u2014 ESCALATION, NOT AUTO-APPROVAL",
    [
        ("TIER 0", "Auto"),
        ("TIER 1", "Notify"),
        ("TIER 2", "Single"),
        ("TIER 3", "Dual"),
        ("TIER 4", "CEO only"),
    ],
    outline_last_red=True,
    item_gap=10,
).save(OUT / "card-4.png")

# ---------------------------------------------------------------- card 5
img, d = new_card()
chrome(img, d, 5)
d.text((MARGIN, 128), "THE WINDOW", font=font(BOLD, 17), fill=CYAN)
y = 164
for line in ["MALAWI IS DRAFTING", "ITS NATIONAL AI", "STRATEGY NOW."]:
    d.text((MARGIN, y), line, font=font(BOLD, 52), fill=WHITE)
    y += 60
d.rectangle([MARGIN, y + 10, MARGIN + 120, y + 16], fill=RED)

para = (
    "We recommend open-weight, locally hosted models and air-gapped "
    "inference. Sovereignty and budget are the same design constraint."
)
yy = y + 40
for line in wrap(d, para, font(REG, 18), COL_W):
    d.text((MARGIN, yy), line, font=font(REG, 18), fill=MORNING_MIST)
    yy += 28

yy += 22
d.rectangle([MARGIN, yy, MARGIN + 372, yy + 56], fill=RED)
d.text((MARGIN + 26, yy + 17), "READ THE PLAYBOOK", font=font(BOLD, 20), fill=WHITE)
d.text((MARGIN + 400, yy + 20), "lightspeedholdings.vercel.app", font=font(REG, 16), fill=CYAN)
img.save(OUT / "card-5.png")

# ---------------------------------------------------------------- PDF
cards = [Image.open(OUT / f"card-{i}.png").convert("RGB") for i in range(1, 6)]
cards[0].save(OUT / "carousel.pdf", save_all=True, append_images=cards[1:], resolution=150.0)
print(f"Wrote 5 PNGs + carousel.pdf to {OUT}")
