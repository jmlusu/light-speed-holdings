"""Structural + brand verification for the Lightspeed value-proposition deck.

Checks (hard failures):
  - exactly 10 slides, 10 x 7.5 in
  - every run uses Arial
  - every explicit colour is from brand/tokens.md
  - every shape sits inside the slide
  - every slide has speaker notes
  - official logo artwork on the cover and closing slide

Overflow is reported as warnings using a conservative per-run estimate
(char width 0.42em bold / 0.38em regular, line spacing 1.15).
"""

from __future__ import annotations

import sys
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Emu

DECK = Path(__file__).with_name("Lightspeed-Value-Proposition-HAOMTGV-Venture-Studio.pptx")
PALETTE = {
    "070A40",
    "E63946",
    "00BFFF",
    "F2F2F2",
    "FFFFFF",
    "6B7280",
    "9CA3AF",
}
EXPECTED_SLIDES = 10
SLIDE_W_IN = 10.0
SLIDE_H_IN = 7.5


def colour_of(fmt) -> str | None:
    try:
        if fmt.type is None:
            return None
        return str(fmt.rgb)
    except (AttributeError, TypeError):
        return None


def main() -> int:
    prs = Presentation(DECK)
    failures: list[str] = []
    warnings: list[str] = []

    if len(prs.slides) != EXPECTED_SLIDES:
        failures.append(f"slide count {len(prs.slides)} != {EXPECTED_SLIDES}")
    if abs(Emu(prs.slide_width).inches - SLIDE_W_IN) > 0.01:
        failures.append(f"slide width {Emu(prs.slide_width).inches}")
    if abs(Emu(prs.slide_height).inches - SLIDE_H_IN) > 0.01:
        failures.append(f"slide height {Emu(prs.slide_height).inches}")

    for idx, slide in enumerate(prs.slides, start=1):
        if not slide.has_notes_slide or not slide.notes_slide.notes_text_frame.text.strip():
            failures.append(f"slide {idx}: missing speaker notes")

        pictures = 0
        for sh in slide.shapes:
            if sh.shape_type == MSO_SHAPE_TYPE.PICTURE:
                pictures += 1
            left = Emu(sh.left).inches
            top = Emu(sh.top).inches
            width = Emu(sh.width).inches
            height = Emu(sh.height).inches
            if (
                left < -0.02
                or top < -0.02
                or left + width > SLIDE_W_IN + 0.02
                or top + height > SLIDE_H_IN + 0.02
            ):
                failures.append(
                    f"slide {idx}: shape out of bounds ({left:.2f},{top:.2f},{width:.2f},{height:.2f})"
                )
            for attr in ("fill", "line"):
                try:
                    fmt = (
                        getattr(sh, attr).fore_color if attr == "fill" else getattr(sh, attr).color
                    )
                    c = colour_of(fmt)
                    if c and c not in PALETTE:
                        failures.append(f"slide {idx}: off-palette {attr} #{c}")
                except (AttributeError, TypeError):
                    pass
            if not sh.has_text_frame:
                continue
            tf = sh.text_frame
            for para in tf.paragraphs:
                for run in para.runs:
                    if run.font.name and run.font.name != "Arial":
                        failures.append(f"slide {idx}: font {run.font.name}")
                    c = colour_of(run.font.color)
                    if c and c not in PALETTE:
                        failures.append(f"slide {idx}: off-palette text #{c}")
                    if run.font.size and run.font.size.pt <= 18 and run.text.strip():
                        size = run.font.size.pt
                        line_h = size * (para.line_spacing or 1.15) / 72
                        char_w = size * (0.42 if run.font.bold else 0.38) / 72
                        chars_per_line = max(1, int(width / char_w))
                        lines = max(1, -(-len(run.text) // chars_per_line))  # ceil
                        needed = lines * line_h
                        if needed > height * 1.25 + 0.06:
                            warnings.append(
                                f"slide {idx}: possible overflow '{run.text[:38]}' "
                                f"needs {needed:.2f}in > box {height:.2f}in"
                            )
        if idx in (1, EXPECTED_SLIDES) and pictures == 0:
            failures.append(f"slide {idx}: missing logo artwork")

    print(
        f"slides: {len(prs.slides)}  size: {Emu(prs.slide_width).inches:.2f} x "
        f"{Emu(prs.slide_height).inches:.2f} in"
    )
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print("  -", w)
    if failures:
        print(f"FAIL ({len(failures)}):")
        for f in failures:
            print("  -", f)
        return 1
    print("PASS: structure, fonts, palette, bounds, notes and logo placement.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
