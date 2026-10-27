#!/usr/bin/env python3
"""Verify the transparent logo variants in brand/logo/.

An independent check of what the Node generator produced. It does not trust the
generator's output: every assertion is measured from the files on disk.

Checks, per transparent PNG:
  1. It carries a real alpha channel.
  2. All four corner pixels are fully transparent â€” the regression test for the
     "pasted the wrong logo and got a white box on navy" failure.
  3. A meaningful share of the canvas is alpha=0.
  4. Some pixels are fully opaque, i.e. the artwork actually rendered (a
     renderer that dropped the masked wordmarks would leave a bare symbol).
  5. It is not byte-identical to an opaque sibling.

Checks, per transparent SVG:
  6. It parses as XML.
  7. It has no full-canvas background rect.

Usage:
  python scripts/qa/verify-logo-transparency.py
Exit code 0 = all checks pass.
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[2]
LOGO = REPO_ROOT / "brand" / "logo"

# concept -> (file, opaque sibling or None, expected size, min alpha=0 share)
PNG_CASES = [
    ("avatar", "logo-avatar-transparent.png", "logo-avatar.png", (1024, 1024), 0.50),
    ("dark-bg", "logo-dark-bg-transparent.png", "logo-dark-bg.png", (1254, 1254), 0.50),
    ("favicon", "logo-favicon-transparent.png", "logo-favicon.png", (512, 512), 0.30),
    ("full", "logo-full-transparent.png", "logo-full.png", (1254, 1254), 0.50),
    ("light-bg", "logo-light-bg-transparent.png", "logo-light-bg.png", (1254, 1254), 0.50),
    ("mark", "logo-mark-transparent.png", "logo-mark.png", (609, 388), 0.25),
    ("mark-mono", "logo-mark-mono-transparent.png", "logo-mark-mono.png", (609, 388), 0.25),
    ("og", "logo-og-transparent.png", "logo-og.png", (1200, 630), 0.50),
    ("no-background", "logo-no-background.png", None, (1024, 1024), 0.40),
]

SVG_CASES = [
    ("avatar", "logo-avatar-transparent.svg", (1024, 1024)),
    ("favicon", "logo-favicon-transparent.svg", (512, 512)),
    ("full", "logo-full-transparent.svg", (1254, 1254)),
    ("og", "logo-og-transparent.svg", (1200, 630)),
    ("no-background", "logo-no-background.svg", (1024, 1024)),
]

failures: list[str] = []


def check_png(concept, name, sibling, size, min_transparent):
    path = LOGO / name
    if not path.is_file():
        failures.append(f"{name}: missing")
        return None

    im = Image.open(path)
    if im.mode != "RGBA":
        failures.append(f"{name}: mode is {im.mode}, expected RGBA")
        return None
    if im.size != size:
        failures.append(f"{name}: size {im.size}, expected {size}")

    w, h = im.size
    alpha = im.getchannel("A")
    hist = alpha.histogram()
    total = w * h
    transparent = hist[0] / total
    opaque = hist[255] / total

    corners = [alpha.getpixel(p) for p in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
    if any(c != 0 for c in corners):
        failures.append(f"{name}: corner alpha {corners} â€” not transparent")
    if transparent < min_transparent:
        failures.append(
            f"{name}: only {transparent:.1%} of pixels are alpha=0 (floor {min_transparent:.0%})"
        )
    if opaque < 0.005:
        failures.append(f"{name}: only {opaque:.2%} fully opaque â€” artwork did not render")

    if sibling:
        sib = LOGO / sibling
        if sib.is_file() and sib.read_bytes() == path.read_bytes():
            failures.append(f"{name}: byte-identical to {sibling}")

    return {
        "concept": concept,
        "file": name,
        "size": f"{w}x{h}",
        "transparent": transparent,
        "opaque": opaque,
        "corners": "ok" if all(c == 0 for c in corners) else "FAIL",
    }


def check_svg(concept, name, size):
    path = LOGO / name
    if not path.is_file():
        failures.append(f"{name}: missing")
        return None

    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        failures.append(f"{name}: not well-formed XML ({exc})")
        return None

    root = tree.getroot()
    vb = root.get("viewBox", "")
    w, h = size
    if vb.split() != ["0", "0", str(w), str(h)]:
        failures.append(f"{name}: viewBox {vb!r}, expected '0 0 {w} {h}'")

    # A full-canvas background rect is exactly what makes a logo opaque.
    for el in root.iter():
        if el.tag.split("}")[-1] != "rect":
            continue
        try:
            rw, rh = float(el.get("width", 0)), float(el.get("height", 0))
        except (TypeError, ValueError):
            continue
        has_pos = el.get("x") is not None or el.get("y") is not None
        if rw >= w and rh >= h and not has_pos:
            failures.append(f"{name}: still has a full-canvas background rect ({rw}x{rh})")
            break

    return {
        "concept": concept,
        "file": name,
        "viewBox": vb,
        "elements": sum(1 for _ in root.iter()),
    }


def main() -> int:
    print("TRANSPARENT LOGO VARIANTS â€” verification")
    print("-" * 96)

    rows = []
    for case in PNG_CASES:
        r = check_png(*case)
        if r:
            rows.append(r)
    print(f"{'concept':<15}{'file':<34}{'size':<11}{'alpha0':>8}{'opaque':>8}  corners")
    for r in rows:
        print(
            f"{r['concept']:<15}{r['file']:<34}{r['size']:<11}"
            f"{r['transparent']:>7.1%}{r['opaque']:>8.1%}  {r['corners']}"
        )

    print()
    print("TRANSPARENT SVGs")
    for case in SVG_CASES:
        r = check_svg(*case)
        if r:
            print(f"  {r['file']:<34}{r['viewBox']:<18}{r['elements']:>4} elements")

    print("-" * 96)
    if failures:
        print(f"RESULT: FAIL ({len(failures)} issues)")
        for f in failures:
            print("  - " + f)
        return 1
    print(
        f"RESULT: PASS â€” {len(rows)} transparent PNGs and {len(SVG_CASES)} transparent SVGs verified."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
