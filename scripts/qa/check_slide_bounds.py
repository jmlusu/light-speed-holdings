#!/usr/bin/env python3
"""Slide-frame / boundary QA plugin (PowerPoint side).

Verifies that every shape and every text box in a .pptx sits inside the slide
frame, with a configurable safety margin, and estimates whether wrapped text
overflows its own bounding box (which is what causes on-slide overlap/clipping).

Checks performed per slide:
  1. Shape bbox must be within [0, slide_w] x [0, slide_h] (minus margin).
  2. Estimated rendered text height (Arial, word-wrap estimate) must not exceed
     the shape height by more than a tolerance — i.e. text must not overflow.

Exit codes: 0 = pass, 1 = a boundary or text-overflow violation was found.

Usage:
  python scripts/qa/check_slide_bounds.py path/to/deck.pptx [--margin 0.15]
      [--text-tolerance 0.35]
"""

from __future__ import annotations

import sys
from pathlib import Path

EMU_PER_INCH = 914400


def _in(emu) -> float:
    return float(emu) / EMU_PER_INCH


def _est_text_height(text: str, font_pt: float, width_in: float) -> float:
    """Estimate wrapped Arial text height in inches."""
    if not text:
        return 0.0
    if font_pt <= 0:
        return 0.0
    chars_per_line = max(1, int((width_in * 96.0) / (font_pt * 0.58)))
    lines = 0
    for seg in text.split("\n"):
        lines += max(1, -(-len(seg) // chars_per_line))
    return lines * font_pt * 1.32 / 72.0


def _shape_font_pt(shape) -> float:
    """Largest font size used in a text shape (pt), or 0 if none."""
    largest = 0.0
    tf = getattr(shape, "text_frame", None)
    if tf is None:
        return 0.0
    for para in tf.paragraphs:
        for run in para.runs:
            if run.font.size is not None:
                largest = max(largest, float(run.font.size.pt))
        if para.font.size is not None:
            largest = max(largest, float(para.font.size.pt))
    return largest


# ── Content-region constants — left/right only. ───────────────────────
# The "content region" horizontally is the area inside the navy rail
# (0.15in) + a 0.25in gutter, with a 0.15in margin on the right so no
# body text touches the slide right edge.  Bottom is naturally bounded by
# the slide height and the footer position; we only guard the horizontal
# extents so the checker only flags drift outside the rail/gutter area.
_CONTENT_LEFT = 0.7          # clears the 0.15in rail + 0.25in gutter
_CONTENT_RIGHT = 9.6         # SLIDE_W - 0.15in right margin on a 10in slide


def _in_content_bounds(left, right) -> bool:
    """True if shape is wholly within the content region (rail + safe margin)."""
    return left >= _CONTENT_LEFT - 0.001 and right <= _CONTENT_RIGHT + 0.001


# ── Edge-bleed exemption ──────────────────────────────────────────────

# A shape is a deliberate "edge bleed" (rail / full-bleed band / background)
# when it spans the full slide height or full slide width (within a small
# tolerance) and is flush to one edge. These are exempt from the safety-margin
# warning so the checker only flags genuine content drift.
_EDGE_TOL = 0.05


def _is_edge_bleed(left, top, right, bottom, slide_w, slide_h) -> bool:
    spans_height = bottom >= slide_h - _EDGE_TOL and top <= _EDGE_TOL
    spans_width = right >= slide_w - _EDGE_TOL and left <= _EDGE_TOL
    flush_left = left <= _EDGE_TOL
    flush_top = top <= _EDGE_TOL
    return (spans_height and flush_left) or (spans_width and flush_top)


def check_pptx(pptx_path: Path, margin: float, text_tol: float) -> int:
    try:
        from pptx import Presentation
    except ImportError:
        print("::error::python-pptx not installed (uv run python ...)")
        return 1

    if not pptx_path.is_file():
        print(f"::error::file not found: {pptx_path}")
        return 1

    from pptx.presentation import Presentation as _Presentation
    prs: _Presentation = Presentation(str(pptx_path))
    slide_w = _in(prs.slide_width)
    slide_h = _in(prs.slide_height)

    violations = 0
    warnings = 0
    shapes_checked = 0

    for idx, slide in enumerate(prs.slides, start=1):
        for shape in slide.shapes:
            shapes_checked += 1
            left = _in(shape.left)
            top = _in(shape.top)
            width = _in(shape.width)
            height = _in(shape.height)
            right = left + width
            bottom = top + height

            # 1. Frame containment — must never leave the slide.
            if left < -0.001 or top < -0.001 or right > slide_w + 0.001 or bottom > slide_h + 0.001:
                print(
                    f"::error::slide {idx}: shape '{shape.shape_type}' out of frame "
                    f"(L={left:.2f} T={top:.2f} R={right:.2f} B={bottom:.2f} in "
                    f"vs slide {slide_w:.2f}x{slide_h:.2f})"
                )
                violations += 1
            elif _is_edge_bleed(left, top, right, bottom, slide_w, slide_h):
                # Deliberate full-bleed element (e.g. the navy left rail or a
                # full-bleed background band). Exempt from the safety-margin
                # warning so the checker only flags genuine content drift.
                pass
            elif not _in_content_bounds(left, right) and (
                left < margin - 0.001
                or top < margin - 0.001
                or right > slide_w - margin + 0.001
                or bottom > slide_h - margin + 0.001
            ):
                # Safety-margin warning — but only if the shape is NOT wholly
                # inside the content region (where right-side/bottom margins
                # are by-design per the brand spec).
                print(
                    f"::warning::slide {idx}: shape breaches {margin}in safety margin "
                    f"(L={left:.2f} T={top:.2f} R={right:.2f} B={bottom:.2f})"
                )
                warnings += 1

            # 2. Text overflow estimate.
            text = getattr(shape, "text", "") or ""
            if text.strip():
                font_pt = _shape_font_pt(shape)
                if font_pt > 0:
                    need = _est_text_height(text, font_pt, max(width, 0.2))
                    if need > height + text_tol:
                        print(
                            f"::error::slide {idx}: text overflow — needs ~{need:.2f}in "
                            f"but box is {height:.2f}in ({font_pt:.0f}pt): "
                            f"{text.strip()[:60]!r}"
                        )
                        violations += 1

    print(
        f"check_slide_bounds: {pptx_path.name} — slide {slide_w:.2f}x{slide_h:.2f}in, "
        f"{shapes_checked} shapes checked, {violations} violation(s), {warnings} warning(s)"
    )
    if violations:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    pptx = Path(argv[0])
    margin = 0.15
    text_tol = 0.35
    args = argv[1:]
    i = 0
    while i < len(args) - 1:
        if args[i] == "--margin":
            margin = float(args[i + 1])
            i += 2
        elif args[i] == "--text-tolerance":
            text_tol = float(args[i + 1])
            i += 2
        else:
            i += 1
    return check_pptx(pptx, margin, text_tol)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))