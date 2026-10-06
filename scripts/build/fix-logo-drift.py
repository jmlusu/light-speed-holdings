#!/usr/bin/env python3
"""Snap brand logo PNGs to the exact canonical palette (fix #318-brand drift).

The colour logo exports (icononly, fulllogo, textonly) carry off-token accents
(red #F23838 vs #E63946, cyan #05C7F2 vs #00BFFF) plus a two-tone grey ramp
(around #A5A6A5 / #737373) that does not match the brand grey tokens. This
script deterministically snaps every visible pixel to its nearest token from
brand/tokens/brand-tokens.json, preserving alpha exactly.

Enterprise source / grayscale variants are intentionally excluded:
  - grayscale/*  is a monochrome set by design (the palette gate is not for it);
  - *.jpg / *.pdf / *.eps exports are lossy or vector-native and are left for a
    vector-source pass (SVG accent fills are fixed too via hex replacement).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "brand" / "tokens" / "brand-tokens.json"
LOGO_DIR = ROOT / "brand" / "logos"

EXCLUDE_DIRS = {"grayscale"}
SVG_ACCENT_FIX = {
    "#F23838": "#E63946",
    "#05C7F2": "#00BFFF",
    "F23838": "E63946",
    "05C7F2": "00BFFF",
}


def load_palette() -> list[tuple[int, int, int]]:
    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    palette: list[tuple[int, int, int]] = []
    seen: set[tuple[int, int, int]] = set()
    for spec in data.get("color", {}).values():
        value = spec.get("value", "")
        if not value.startswith("#"):
            continue
        rgb = tuple(int(value.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
        if rgb not in seen:
            seen.add(rgb)
            palette.append(rgb)
    return palette


def off_pct(img: Image.Image, palette: list[tuple[int, int, int]]) -> float:
    palette_set = set(palette)
    raw = img.tobytes()
    visible = off = 0
    for i in range(0, len(raw), 4):
        a = raw[i + 3]
        if a == 0:
            continue
        visible += 1
        if (raw[i], raw[i + 1], raw[i + 2]) not in palette_set:
            off += 1
    return off * 100.0 / visible if visible else 0.0


def snap_image(src: Path, palette: list[tuple[int, int, int]]) -> None:
    with Image.open(src) as img:
        rgba = img.convert("RGBA")
    before = off_pct(rgba, palette)
    px = rgba.load()
    w, h = rgba.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            best = palette[0]
            bd = abs(r - best[0]) + abs(g - best[1]) + abs(b - best[2])
            for token in palette[1:]:
                d = abs(r - token[0]) + abs(g - token[1]) + abs(b - token[2])
                if d < bd:
                    best, bd = token, d
            if (r, g, b) != best:
                px[x, y] = (best[0], best[1], best[2], a)
    after = off_pct(rgba, palette)
    # Preserve original PNG mode when lossless-compatible, else PNG.
    rgba.save(src, format="PNG", optimize=True)
    print(f"  {src.relative_to(ROOT)}: off-palette {before:.2f}% -> {after:.2f}%")


def snap_svg(src: Path) -> None:
    text = src.read_text(encoding="utf-8", errors="replace")
    before = text
    for needle, repl in SVG_ACCENT_FIX.items():
        text = text.replace(needle, repl)
    if text != before:
        src.write_text(text, encoding="utf-8")
        print(f"  {src.relative_to(ROOT)}: accent fills replaced to tokens")
    else:
        print(f"  {src.relative_to(ROOT)}: no accent fills to fix")


def main() -> int:
    parser = argparse.ArgumentParser(description="Snap color logo PNGs to the brand palette")
    parser.add_argument("--dry-run", action="store_true", help="report only; write nothing")
    args = parser.parse_args()

    if not TOKENS.is_file():
        print(f"ERROR: tokens not found: {TOKENS}", file=sys.stderr)
        return 2

    palette = load_palette()
    targets = sorted(
        p for p in LOGO_DIR.rglob("*.png") if p.relative_to(LOGO_DIR).parts[0] not in EXCLUDE_DIRS
    )
    svgs = sorted(LOGO_DIR.rglob("*.svg"))
    print(f"palette tokens: {palette}")
    print(f"PNG targets: {len(targets)} | SVG targets: {len(svgs)}")
    for png in targets:
        if args.dry_run:
            with Image.open(png) as img:
                print(
                    f"  {png.relative_to(ROOT)}: off-palette {off_pct(img.convert('RGBA'), palette):.2f}%"
                )
        else:
            snap_image(png, palette)
    if not args.dry_run:
        for svg in svgs:
            snap_svg(svg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
