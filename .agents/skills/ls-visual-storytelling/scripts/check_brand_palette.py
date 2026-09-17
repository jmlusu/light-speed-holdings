#!/usr/bin/env python3
"""Deterministic LightSpeed brand palette gate for rendered visuals.

Loads the canonical palette from brand/tokens/brand-tokens.json and checks an
image: every visible pixel must exactly match a brand token color. Pixels that
fall off-palette (anti-aliasing, gradients, foreign colors) are counted and
reported as a percentage; PASS/FAIL is decided against --tolerance (default 3%).

Usage:
    uv run python .agents/skills/ls-visual-storytelling/scripts/check_brand_palette.py IMAGE [--tolerance PCT] [--verbose]

Exit codes: 0 = PASS, 1 = FAIL, 2 = error (missing file / bad image / no tokens).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

DEFAULT_TOLERANCE = 3.0


def default_tokens_path() -> Path:
    """Locate the canonical brand-tokens.json by walking up from this script."""
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "brand" / "tokens" / "brand-tokens.json"
        if candidate.is_file():
            return candidate
    return Path(__file__).resolve().parents[4] / "brand" / "tokens" / "brand-tokens.json"


def load_palette(tokens_path: Path) -> list[tuple[int, int, int]]:
    """Read the exact token palette from brand-tokens.json (deduplicated)."""
    if not tokens_path.is_file():
        raise FileNotFoundError(f"brand tokens not found: {tokens_path}")
    data = json.loads(tokens_path.read_text(encoding="utf-8"))
    colors = data.get("color", {})
    if not colors:
        raise ValueError(f"no color tokens in {tokens_path}")
    palette: list[tuple[int, int, int]] = []
    seen: set[tuple[int, int, int]] = set()
    for spec in colors.values():
        value = spec.get("value", "")
        if not value.startswith("#"):
            continue
        rgb = tuple(int(value.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
        if rgb not in seen:
            seen.add(rgb)
            palette.append(rgb)
    if not palette:
        raise ValueError(f"no parseable hex color tokens in {tokens_path}")
    return palette


def check_image(path: Path, palette: list[tuple[int, int, int]]) -> tuple[int, int]:
    """Return (visible_pixels, off_palette_pixels)."""
    with Image.open(path) as img:
        img = img.convert("RGBA")
    palette_set = set(palette)
    raw = img.tobytes()
    visible = 0
    off = 0
    for i in range(0, len(raw), 4):
        r, g, b, a = raw[i], raw[i + 1], raw[i + 2], raw[i + 3]
        if a == 0:
            continue
        visible += 1
        if (r, g, b) not in palette_set:
            off += 1
    return visible, off


def main() -> int:
    parser = argparse.ArgumentParser(description="LightSpeed brand palette checker")
    parser.add_argument("image", help="path to the image to check (PNG/JPEG/WebP/...)")
    parser.add_argument(
        "--tolerance",
        type=float,
        default=DEFAULT_TOLERANCE,
        help=f"maximum allowed percent of off-palette pixels (default: {DEFAULT_TOLERANCE:g})",
    )
    parser.add_argument("--verbose", action="store_true", help="print pixel counts")
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.is_file():
        print(f"ERROR: image not found: {image_path}", file=sys.stderr)
        return 2

    try:
        palette = load_palette(default_tokens_path())
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    try:
        visible, off = check_image(image_path, palette)
    except (OSError, ValueError) as exc:  # PIL raises per-format errors
        print(f"ERROR: could not read image {image_path}: {exc}", file=sys.stderr)
        return 2

    if visible == 0:
        print(f"ERROR: image has no visible pixels: {image_path}", file=sys.stderr)
        return 2

    off_pct = off * 100.0 / visible
    on_pct = 100.0 - off_pct
    if args.verbose:
        print(f"visible pixels: {visible}; off-palette: {off} ({off_pct:.2f}%)")

    if off_pct <= args.tolerance:
        print(
            f"PASS: {on_pct:.2f}% of visible pixels on brand palette "
            f"({off_pct:.2f}% off, tolerance {args.tolerance:g}%)"
        )
        return 0
    print(
        f"FAIL: {off_pct:.2f}% of visible pixels off brand palette (tolerance {args.tolerance:g}%)"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
