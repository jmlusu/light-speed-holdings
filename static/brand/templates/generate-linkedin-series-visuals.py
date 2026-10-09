#!/usr/bin/env python3
"""Generate the AI-Native Organizations LinkedIn series visuals.

Produces 12 PNGs (1200x627) — one hero + three carousel cards per post — for
Posts 1-3 of the series, into docs/Pharos/linkedin-series/post-0N/visuals/.

Brand: colors and type scale are read from brand/tokens/brand-tokens.json
(canonical-first, mirrors per generate-post-templates.py). Every rendered pixel
is snapped to the exact token palette so check_brand_palette.py passes at 0%.

Logo policy (same as generate-post-templates.py): icon-only logo on dark
surfaces, full logo on light surfaces. Logos are official assets, never
recolored beyond nearest-token snapping of resize blends.

Usage:
    uv run python static/brand/templates/generate-linkedin-series-visuals.py
    uv run python static/brand/templates/generate-linkedin-series-visuals.py --verify
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- constants

W, H = 1200, 627
RAIL = 48  # brand left rail (content cards)
PAD = 64  # content inset
CARD_PAD = 64  # card content inset (from canvas edge, rail excluded)
BAR_H = 12  # red accent bar height (bottom, navy surfaces)
CHIP = 44  # framework chip size
CHIP_GAP = 12

# Type scale: tokens are pt; Pillow takes px (pt * 4/3 at 96dpi).
S = {
    "display": 48,  # 36pt displayXl
    "titlexl": 43,  # 32pt titleXl
    "titlelg": 37,  # 28pt titleLg
    "titlemd": 32,  # 24pt titleMd
    "titlesm": 24,  # 18pt titleSm
    "subtitle": 21,  # 16pt subtitle / bodyLg
    "body": 19,  # 14pt body
    "bodysm": 17,  # 13pt bodySm
    "caption": 16,  # 12pt caption
}

FRAMEWORK = ["H", "A", "O", "M", "T", "G", "V"]
LAYER_NAMES = {
    "H": "H — HUMAN PURPOSE & AUTHORITY",
    "A": "A — AGENTIC WORKFORCE",
    "O": "O — ORCHESTRATION & ORGANIZATION",
}
TAGLINE = "ASPIRE. ACT. ACHIEVE."
SERIES_URL = "lightspeedholdings.com"
BUTTON_LABEL = "Download the Malawi Agentic AI Monitor"

POSTS = [
    {
        "n": 1,
        "layer": "H",
        "title": "What is an AI-Native Organization?",
        "stat": "5-tier approval matrix  ·  cryptographic human sign-off  ·  reversible delegation",
        "cover_title": [("What is an AI-Native Organization?", "titlexl", "white")],
        "cover_body": (
            "It's a systematically engineered ecosystem where AI agents perform "
            "coordinated work under human accountability — not just a company "
            "that uses AI tools."
        ),
        "card2": {
            "headline": [("5-Tier HITL Approval", "titlemd", "navy")],
            "body": (
                "Every agentic decision flows through five approval tiers. "
                "Audit trails ensure accountability at every tier."
            ),
            "pills": ["autonomous", "HITL-approved", "reviewed", "snoozed", "cleared"],
        },
        "cta_sub": "Explore how AI-native patterns apply in Malawi.",
    },
    {
        "n": 2,
        "layer": "A",
        "title": "What does 90 AI agents actually mean?",
        "stat": "90 personas in one registry  ·  20 departments  ·  RACI reporting chains",
        "cover_title": [("90", "titlexl", "red"), (" Agents, 20 Departments", "titlexl", "white")],
        "cover_body": (
            "LightSpeed Holdings Limited™ operates exactly 90 AI agents across "
            "20 departments, orchestrated via a MessageBus task queue."
        ),
        "card2": {
            "headline": [
                ("8", "titlemd", "red"),
                (" Recurring Revenue Products", "titlemd", "navy"),
            ],
            "body": (
                "Eight recurring revenue products sustain the agent economy "
                "without upfront capital requirements."
            ),
            "pills": [],
        },
        "cta_sub": "Explore how agentic patterns apply in Malawi.",
    },
    {
        "n": 3,
        "layer": "O",
        "title": "LightSpeed™ AI-native org structure",
        "stat": "1 message bus  ·  JSON task queue  ·  dead-letter replay  ·  computable org topology",
        "cover_title": [("The Orchestration Layer", "titlexl", "white")],
        "cover_body": (
            "The orchestration layer coordinates 90 agents across 20 departments "
            "via a MessageBus task queue — the operational backbone of the "
            "AI-native organization."
        ),
        "card2": {
            "headline": [("Org Metrics per Department", "titlemd", "navy")],
            "body": (
                "graph/engine.py OrgNode returns capacity, activity, trend, "
                "and risk for every department."
            ),
            "stat_big": ("30s", "TTL cache per department metric"),
            "pills": ["capacity", "activity", "trend", "risk"],
        },
        "cta_sub": "Explore how orchestration patterns apply in Malawi.",
    },
]

# ------------------------------------------------------------- brand helpers


def _canonical_or_mirror(*parts: str) -> str:
    """Canonical brand/ path first, runtime static/brand mirror second."""
    root = Path(__file__).resolve().parents[3]
    for base in (root / "brand", root / "static" / "brand"):
        candidate = base.joinpath(*parts)
        if candidate.exists():
            return str(candidate)
    raise FileNotFoundError(f"brand asset not found: {'/'.join(parts)}")


def load_tokens() -> dict:
    path = Path(_canonical_or_mirror("tokens", "brand-tokens.json"))
    return json.loads(path.read_text(encoding="utf-8"))


COLORS = {
    "navy": "#070A40",
    "red": "#DC3641",
    "cyan": "#00BFFF",
    "grey-light": "#F2F2F2",
    "white": "#FFFFFF",
    "grey-dark": "#6B7280",
    "grey-light-text": "#9CA3AF",
}


def hex_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def palette_from_tokens() -> list[tuple[int, int, int]]:
    """Exact token palette (same source as check_brand_palette.py)."""
    data = load_tokens()
    palette: list[tuple[int, int, int]] = []
    seen: set[tuple[int, int, int]] = set()
    for spec in data.get("color", {}).values():
        value = spec.get("value", "")
        if value.startswith("#"):
            rgb = hex_rgb(value)
            if rgb not in seen:
                seen.add(rgb)
                palette.append(rgb)
    return palette


PALETTE = palette_from_tokens()
PALETTE_CACHE: dict[tuple[int, int, int], tuple[int, int, int]] = {}


def snap(r: int, g: int, b: int) -> tuple[int, int, int]:
    key = (r, g, b)
    if key not in PALETTE_CACHE:
        PALETTE_CACHE[key] = min(
            PALETTE,
            key=lambda c: (c[0] - r) ** 2 + (c[1] - g) ** 2 + (c[2] - b) ** 2,
        )
    return PALETTE_CACHE[key]


def snap_to_palette(img: Image.Image) -> Image.Image:
    """Map every pixel to the nearest brand token color (0% off-palette)."""
    rgba = img.convert("RGBA")
    data = [(*snap(r, g, b), a) if a else (r, g, b, a) for r, g, b, a in rgba.getdata()]
    rgba.putdata(data)
    return rgba.convert("RGB")


def _font_file(bold: bool) -> str:
    name = "arialbd.ttf" if bold else "arial.ttf"
    windir = Path(os.environ.get("WINDIR", r"C:\Windows"))
    for candidate in (Path(name), windir / "Fonts" / name, Path("C:/Windows/Fonts") / name):
        if candidate.is_file():
            return str(candidate)
    raise FileNotFoundError(f"Arial font not found: {name} (set WINDIR or install Arial)")


def font(size_key: str, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(_font_file(bold), S[size_key])


def wrap(
    draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_w: int
) -> list[str]:
    lines: list[str] = []
    for raw in text.split("\n"):
        line = ""
        for word in raw.split(" "):
            trial = f"{line} {word}".strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill: str,
    x: int,
    y: int,
    max_w: int,
    lh: int,
    max_lines: int | None = None,
) -> int:
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def draw_segments(
    draw: ImageDraw.ImageDraw,
    segments: list[tuple[str, str, str]],
    x: int,
    y: int,
) -> int:
    """Single-line rich text: [(text, size_key, color_key)]."""
    cursor = x
    for text, size_key, color in segments:
        fnt = font(size_key, bold=True)
        draw.text((cursor, y), text, font=fnt, fill=COLORS[color])
        cursor += int(draw.textlength(text, font=fnt))
    return cursor


def paste_logo(dark_surface: bool, target_h: int) -> Image.Image:
    """Official logo: icon-only on dark, full logo on light (per brand spec).

    Transparent padding is trimmed to the alpha bbox so the visible mark
    fills target_h. On light surfaces the full logo's baked near-white
    background (>=240 per channel) is normalized to pure white so it does
    not snap to grey-light against the white content card.
    """
    if dark_surface:
        path = _canonical_or_mirror("logo", "logo-mark.png")
    else:
        path = _canonical_or_mirror("logo", "logo-full.png")
    logo = Image.open(path).convert("RGBA")
    bbox = logo.getbbox()
    if bbox:
        logo = logo.crop(bbox)
    if not dark_surface:
        px = logo.load()
        for i in range(logo.width):
            for j in range(logo.height):
                r, g, b, a = px[i, j]
                if a and r >= 240 and g >= 240 and b >= 240:
                    px[i, j] = (255, 255, 255, a)
    target_w = int(logo.width * (target_h / logo.height))
    return logo.resize((target_w, target_h), Image.Resampling.LANCZOS)


def footer_navy(draw: ImageDraw.ImageDraw, img: Image.Image) -> None:
    """Navy surfaces: tagline bottom-left (caption), icon logo bottom-right."""
    fnt = font("caption")
    draw.text((PAD, H - BAR_H - 40), TAGLINE, font=fnt, fill=COLORS["grey-light-text"])
    logo = paste_logo(dark_surface=True, target_h=56)
    img.paste(logo, (W - PAD - logo.width, H - BAR_H - 40 + 16 - 56), logo)
    draw.rectangle([0, H - BAR_H, W, H], fill=COLORS["red"])


def eyebrow_navy(draw: ImageDraw.ImageDraw, post_n: int, card_idx: int, total: int) -> None:
    fnt = font("caption", bold=True)
    draw.text(
        (PAD, 44), f"AI-NATIVE ORGANIZATIONS  ·  POST {post_n}", font=fnt, fill=COLORS["cyan"]
    )
    ind = font("caption")
    label = f"{card_idx} / {total}"
    draw.text(
        (W - PAD - draw.textlength(label, font=ind), 44),
        label,
        font=ind,
        fill=COLORS["grey-light-text"],
    )


# ----------------------------------------------------------------- builders


def build_hero(post: dict) -> Image.Image:
    img = Image.new("RGB", (W, H), COLORS["navy"])
    draw = ImageDraw.Draw(img)

    # Eyebrow row
    fnt = font("caption", bold=True)
    draw.text(
        (PAD, 40),
        "AI-NATIVE ORGANIZATIONS  ·  COMPANY BUILDER",
        font=fnt,
        fill=COLORS["cyan"],
    )
    ind = f"{post['n']} / 11"
    draw.text(
        (W - PAD - draw.textlength(ind, font=font("caption")), 40),
        ind,
        font=font("caption"),
        fill=COLORS["grey-light-text"],
    )

    # Framework chip row (7 layers, active layer in red)
    x = PAD
    for letter in FRAMEWORK:
        active = letter == post["layer"]
        box = [x, 80, x + CHIP, 80 + CHIP]
        if active:
            draw.rounded_rectangle(box, radius=8, fill=COLORS["red"])
        else:
            draw.rounded_rectangle(box, radius=8, outline=COLORS["grey-dark"], width=2)
        tf = font("subtitle", bold=True)
        tw = draw.textlength(letter, font=tf)
        draw.text(
            (x + (CHIP - tw) / 2, 80 + (CHIP - S["subtitle"]) / 2 - 2),
            letter,
            font=tf,
            fill=COLORS["white"],
        )
        x += CHIP + CHIP_GAP
    draw.text(
        (x + 16, 80 + 12),
        LAYER_NAMES[post["layer"]],
        font=font("caption", bold=True),
        fill=COLORS["cyan"],
    )

    # Headline (title-xl, max 2 lines) + cyan layer question + white stat row
    y = draw_wrapped(
        draw,
        post["title"],
        font("titlexl", bold=True),
        COLORS["white"],
        PAD,
        185,
        W - 2 * PAD,
        54,
        max_lines=2,
    )
    layer_q = {
        "H": "H — Human Purpose & Authority: what should humans remain accountable for?",
        "A": "A — Agentic Workforce: what work can AI agents perform?",
        "O": "O — Orchestration & Organization: how do agents coordinate?",
    }[post["layer"]]
    y = draw_wrapped(
        draw, layer_q, font("subtitle"), COLORS["cyan"], PAD, y + 24, W - 2 * PAD, 30, max_lines=2
    )
    draw_wrapped(
        draw, post["stat"], font("body"), COLORS["white"], PAD, y + 24, W - 2 * PAD, 26, max_lines=2
    )

    footer_navy(draw, img)
    return img


def build_cover(post: dict, card_idx: int) -> Image.Image:
    """Navy cover card (carousel card 1)."""
    img = Image.new("RGB", (W, H), COLORS["navy"])
    draw = ImageDraw.Draw(img)
    eyebrow_navy(draw, post["n"], card_idx, 3)

    cursor = draw_segments(draw, post["cover_title"], PAD, 150)
    if cursor > W - PAD:  # overflow guard (segments too wide) -> wrap fallback
        title_text = "".join(t for t, _, _ in post["cover_title"])
        y = draw_wrapped(
            draw,
            title_text,
            font("titlexl", bold=True),
            COLORS["white"],
            PAD,
            150,
            W - 2 * PAD,
            54,
            max_lines=2,
        )
    else:
        y = 150 + S["titlexl"]
    draw_wrapped(
        draw,
        post["cover_body"],
        font("subtitle"),
        COLORS["grey-light-text"],
        PAD,
        y + 28,
        W - 2 * PAD,
        32,
        max_lines=4,
    )

    footer_navy(draw, img)
    return img


def build_content_card(post: dict, card_idx: int) -> Image.Image:
    """White content card (navy rail, full logo bottom-right)."""
    spec = post["card2"]
    img = Image.new("RGB", (W, H), COLORS["white"])
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, RAIL, H], fill=COLORS["navy"])

    x0 = RAIL + PAD
    max_w = W - x0 - PAD

    # Eyebrow: red tick + series label (navy), part indicator right
    draw.rectangle([x0, 48, x0 + 4, 66], fill=COLORS["red"])
    fnt = font("caption", bold=True)
    draw.text(
        (x0 + 16, 48),
        f"AI-NATIVE ORGANIZATIONS  ·  POST {post['n']}",
        font=fnt,
        fill=COLORS["navy"],
    )
    ind = f"{card_idx} / 3"
    draw.text(
        (W - PAD - draw.textlength(ind, font=font("caption")), 48),
        ind,
        font=font("caption"),
        fill=COLORS["grey-dark"],
    )

    # Headline (navy, key number in red)
    y = draw_segments(draw, spec["headline"], x0, 96)
    if y > W - PAD:
        y = draw_wrapped(
            draw,
            "".join(t for t, _, _ in spec["headline"]),
            font("titlemd", bold=True),
            COLORS["navy"],
            x0,
            96,
            max_w,
            42,
            max_lines=2,
        )
    else:
        y = 96 + S["titlemd"]
    y += 24

    # Body (grey-dark, on-palette 4.8:1)
    y = draw_wrapped(
        draw, spec["body"], font("subtitle"), COLORS["grey-dark"], x0, y, max_w, 32, max_lines=4
    )

    # Optional big stat (red display number + caption)
    if "stat_big" in spec:
        number, caption = spec["stat_big"]
        draw.text((x0, y + 28), number, font=font("display", bold=True), fill=COLORS["red"])
        draw.text(
            (x0 + int(draw.textlength(number, font=font("display", bold=True))) + 24, y + 54),
            caption,
            font=font("body"),
            fill=COLORS["grey-dark"],
        )
        y += 28 + S["display"]

    # Pill row (navy pills, white caption text)
    if spec.get("pills"):
        px = x0
        py = min(y + 36, H - 200)
        pill_fnt = font("caption", bold=True)
        for i, pill in enumerate(spec["pills"]):
            if i:
                arrow = "→"
                draw.text((px + 10, py + 8), arrow, font=font("caption"), fill=COLORS["grey-dark"])
                px += 10 + int(draw.textlength(arrow, font=font("caption"))) + 10
            pw = int(draw.textlength(pill, font=pill_fnt)) + 36
            draw.rounded_rectangle([px, py, px + pw, py + 40], radius=8, fill=COLORS["navy"])
            draw.text((px + 18, py + 9), pill, font=pill_fnt, fill=COLORS["white"])
            px += pw + 8

    # Footer: tagline (in the full logo lockup) + full logo bottom-right
    logo = paste_logo(dark_surface=False, target_h=86)
    img.paste(logo, (W - PAD - logo.width, H - PAD - logo.height), logo)
    return img


def build_cta_card(post: dict, card_idx: int) -> Image.Image:
    img = Image.new("RGB", (W, H), COLORS["navy"])
    draw = ImageDraw.Draw(img)
    eyebrow_navy(draw, post["n"], card_idx, 3)

    draw.text(
        (PAD, 140), "Download the Monitor", font=font("titlelg", bold=True), fill=COLORS["white"]
    )
    y = draw_wrapped(
        draw,
        post["cta_sub"],
        font("subtitle"),
        COLORS["grey-light-text"],
        PAD,
        200,
        W - 2 * PAD,
        32,
        max_lines=2,
    )

    # Red CTA button (white 21px bold on red = large text, brand onRed)
    btn_fnt = font("subtitle", bold=True)
    btn_w = int(draw.textlength(BUTTON_LABEL, font=btn_fnt)) + 64
    btn_y = y + 40
    draw.rounded_rectangle([PAD, btn_y, PAD + btn_w, btn_y + 60], radius=8, fill=COLORS["red"])
    draw.text((PAD + 32, btn_y + 15), BUTTON_LABEL, font=btn_fnt, fill=COLORS["white"])

    draw.text((PAD, btn_y + 92), SERIES_URL, font=font("caption"), fill=COLORS["cyan"])

    footer_navy(draw, img)
    return img


# -------------------------------------------------------------------- main


def out_dir(post_n: int) -> Path:
    root = Path(__file__).resolve().parents[3]
    return root / "docs" / "Pharos" / "linkedin-series" / f"post-{post_n:02d}" / "visuals"


def generate() -> list[Path]:
    written: list[Path] = []
    for post in POSTS:
        target = out_dir(post["n"])
        target.mkdir(parents=True, exist_ok=True)
        assets = {
            "hero-1200x627.png": build_hero(post),
            "carousel-1-1200x627.png": build_cover(post, 1),
            "carousel-2-1200x627.png": build_content_card(post, 2),
            "carousel-3-1200x627.png": build_cta_card(post, 3),
        }
        for name, img in assets.items():
            img = snap_to_palette(img)
            path = target / name
            img.save(path)
            written.append(path)
    return written


def verify(paths: list[Path]) -> int:
    """Re-open each PNG: exact dimensions + off-palette pixel percent <= 0.5%."""
    failures = 0
    pal = set(PALETTE)
    for path in paths:
        img = Image.open(path).convert("RGB")
        if img.size != (W, H):
            print(f"FAIL {path.name}: size {img.size} != {(W, H)}")
            failures += 1
            continue
        total = 0
        off = 0
        for r, g, b in img.getdata():
            total += 1
            if (r, g, b) not in pal:
                off += 1
        pct = 100.0 * off / total if total else 100.0
        status = "PASS" if pct <= 0.5 else "FAIL"
        if status == "FAIL":
            failures += 1
        print(f"{status} {path.parent.parent.name}/{path.name}: {100 - pct:.2f}% on-palette")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate LinkedIn series visuals (Posts 1-3)")
    parser.add_argument(
        "--verify", action="store_true", help="re-open outputs and check dims + palette"
    )
    args = parser.parse_args()

    paths = generate()
    print(f"generated {len(paths)} assets")
    if args.verify:
        return verify(paths)
    return 0


if __name__ == "__main__":
    sys.exit(main())
