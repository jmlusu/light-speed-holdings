"""Render the AI Venture Studio deck and probe the cover and closing slides.

LibreOffice is the reference renderer: it ignores ``a:srcRect`` on pictures and
honours ``a:clrChange``, so a headless PDF export reproduces what a client
actually sees. This gate fails when a lockup overruns its frame, a navy plate
shows behind the logo, or the artwork loses its clear space to the text.

Every expected position comes from ``scripts/presentation/deck_geometry.py``,
the same module the generator places the artwork from.

Usage:
    uv run --with pymupdf python scripts/presentation/render-venture-studio-deck.py [deck.pptx]

Requires LibreOffice. Set SOFFICE to the binary when it is not on PATH or in
the default Windows install location.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

try:
    import pymupdf
except ImportError:  # PyMuPDF < 1.24 exposes only the fitz alias
    import fitz as pymupdf

from deck_geometry import (
    CLOSING_LOGO_BOTTOM_IN,
    CLOSING_LOGO_W_IN,
    CLOSING_LOGO_X_IN,
    CLOSING_LOGO_Y_IN,
    COVER_LOGO_BOTTOM_IN,
    COVER_LOGO_W_IN,
    COVER_LOGO_X_IN,
    COVER_LOGO_Y_IN,
    COVER_TITLE_Y_IN,
    MIN_GAP_IN,
    SLIDE_H_IN,
    SLIDE_W_IN,
    TAGLINE_Y_IN,
)

# --------------------------------------------------------------- design intent
# Every expected value comes from scripts/presentation/deck_geometry.py, the
# same module the generator places the artwork from.

NAVY = (7, 10, 63)  # #070A40 as rendered by LibreOffice
LOGO_BG = (2, 6, 47)  # #02062F plate that a:clrChange is meant to remove
TOL = 14
MAX_PLATE_RATIO = 0.10

DEFAULT_DPI = 150
COVER_INDEX = 0
CLOSING_INDEX = 12
# How far the rendered tagline may sit from its declared position. Font
# substitution changes glyph ascent, not the layout, so the clearance is
# measured against the declared top edge while the tagline is still located
# in the rendered pixels.
TAGLINE_POS_TOL_IN = 0.12


def find_soffice() -> str:
    env = os.environ.get("SOFFICE")
    if env:
        return env
    for name in ("soffice.com", "soffice"):
        found = shutil.which(name)
        if found:
            return found
    for candidate in (
        r"C:\Program Files\LibreOffice\program\soffice.com",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.com",
    ):
        if os.path.exists(candidate):
            return candidate
    raise SystemExit("ERROR: LibreOffice not found. Install it or set SOFFICE to soffice.com.")


def to_pdf(deck: Path, out_dir: Path) -> Path:
    with tempfile.TemporaryDirectory(prefix="lo-profile-") as profile:
        cmd = [
            find_soffice(),
            f"-env:UserInstallation={Path(profile).as_uri()}",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(out_dir),
            str(deck),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        raise SystemExit(f"ERROR: LibreOffice conversion failed:\n{result.stderr}")
    pdf = out_dir / (deck.stem + ".pdf")
    if not pdf.exists():
        raise SystemExit(f"ERROR: expected PDF not produced: {pdf}")
    return pdf


def pixel(pix, x_in: float, y_in: float, dpi: int) -> tuple[int, int, int]:
    x = min(pix.width - 1, max(0, int(round(x_in * dpi))))
    y = min(pix.height - 1, max(0, int(round(y_in * dpi))))
    offset = (y * pix.width + x) * pix.n
    samples = pix.samples
    return samples[offset], samples[offset + 1], samples[offset + 2]


def near(rgb: tuple[int, int, int], target: tuple[int, int, int], tol: int = TOL) -> bool:
    return all(abs(a - b) <= tol for a, b in zip(rgb, target, strict=True))


def is_white(r: int, g: int, b: int) -> bool:
    return r >= 200 and g >= 200 and b >= 200


def is_cyan(r: int, g: int, b: int) -> bool:
    return b >= 200 and g >= 140 and r <= 90


def bbox(pix, predicate, x0: float, y0: float, x1: float, y1: float, dpi: int):
    samples = pix.samples
    n = pix.n
    left, top, right, bottom = pix.width, pix.height, -1, -1
    for y in range(max(0, int(y0 * dpi)), min(pix.height, int(y1 * dpi))):
        row = y * pix.width
        for x in range(max(0, int(x0 * dpi)), min(pix.width, int(x1 * dpi))):
            offset = (row + x) * n
            if predicate(samples[offset], samples[offset + 1], samples[offset + 2]):
                left = min(left, x)
                right = max(right, x)
                top = min(top, y)
                bottom = max(bottom, y)
    if right < 0:
        return None
    return (left / dpi, top / dpi, right / dpi, bottom / dpi)


def plate_ratio(pix, x0: float, y0: float, x1: float, y1: float, dpi: int) -> float:
    samples = pix.samples
    n = pix.n
    total = plate = 0
    for y in range(int(y0 * dpi), int(y1 * dpi)):
        row = y * pix.width
        for x in range(int(x0 * dpi), int(x1 * dpi)):
            offset = (row + x) * n
            total += 1
            if near((samples[offset], samples[offset + 1], samples[offset + 2]), LOGO_BG):
                plate += 1
    return plate / total if total else 0.0


def probe_closing(pix, dpi: int) -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []

    bg_a = pixel(pix, 0.20, 0.20, dpi)
    bg_b = pixel(pix, SLIDE_W_IN - 0.30, SLIDE_H_IN - 0.30, dpi)
    results.append(("navy background", near(bg_a, NAVY) and near(bg_b, NAVY), f"{bg_a} / {bg_b}"))

    # Search from above the frame down to just above the tagline, so artwork
    # that spills past the frame bottom is still measured.
    glyphs = bbox(
        pix,
        is_white,
        CLOSING_LOGO_X_IN - 0.10,
        CLOSING_LOGO_Y_IN - 0.10,
        CLOSING_LOGO_X_IN + CLOSING_LOGO_W_IN + 0.10,
        TAGLINE_Y_IN - 0.02,
        dpi,
    )
    if glyphs is None:
        results.append(("logo present", False, "no white artwork in the logo band"))
        return results

    left, top, right, bottom = glyphs
    inside = (
        bottom <= CLOSING_LOGO_BOTTOM_IN + 0.05
        and top >= CLOSING_LOGO_Y_IN - 0.05
        and left >= CLOSING_LOGO_X_IN - 0.05
        and right <= CLOSING_LOGO_X_IN + CLOSING_LOGO_W_IN + 0.05
        and (right - left) >= 0.8 * CLOSING_LOGO_W_IN
    )
    results.append(
        (
            "logo inside frame",
            inside,
            f"artwork x {left:.2f}-{right:.2f} y {top:.2f}-{bottom:.2f} in; "
            f"frame y {CLOSING_LOGO_Y_IN:.2f}-{CLOSING_LOGO_BOTTOM_IN:.2f}",
        )
    )

    ratio = plate_ratio(
        pix,
        CLOSING_LOGO_X_IN,
        CLOSING_LOGO_Y_IN,
        CLOSING_LOGO_X_IN + CLOSING_LOGO_W_IN,
        CLOSING_LOGO_BOTTOM_IN,
        dpi,
    )
    results.append(("no navy plate", ratio <= MAX_PLATE_RATIO, f"{ratio:.1%} of logo frame"))

    tagline = bbox(
        pix,
        is_cyan,
        1.0,
        TAGLINE_Y_IN - 0.10,
        SLIDE_W_IN - 1.0,
        TAGLINE_Y_IN + 0.45,
        dpi,
    )
    if tagline is None:
        results.append(("tagline present", False, "no cyan pixels in the tagline band"))
        return results

    t_left, t_top, t_right, t_bottom = tagline
    results.append(
        (
            "tagline present",
            (t_right - t_left) >= 2.0,
            f"x {t_left:.2f}-{t_right:.2f} y {t_top:.2f}-{t_bottom:.2f} in",
        )
    )
    results.append(
        (
            "tagline position",
            abs(t_top - TAGLINE_Y_IN) <= TAGLINE_POS_TOL_IN,
            f"rendered {t_top:.2f}in vs declared {TAGLINE_Y_IN:.2f}in "
            f"(+/-{TAGLINE_POS_TOL_IN:.2f})",
        )
    )
    # Clearance is measured against the declared tagline top edge, so font
    # substitution cannot mask a real overlap.
    gap = TAGLINE_Y_IN - bottom
    results.append(
        (
            "logo / tagline clear space",
            gap >= MIN_GAP_IN,
            f"gap {gap:+.2f} in (min {MIN_GAP_IN:.2f})",
        )
    )
    return results


def probe_cover(pix, dpi: int) -> list[tuple[str, bool, str]]:
    """Check the cover lockup: the artwork must stay inside its own frame and
    keep clear of the cover title.

    The cover lockup is part white, part cyan, so the artwork is found as
    "anything that is not the navy background and not the #02062F plate".
    """
    results: list[tuple[str, bool, str]] = []

    bg = pixel(pix, 0.20, 0.20, dpi)
    results.append(("cover navy background", near(bg, NAVY), f"{bg}"))

    def is_artwork(r: int, g: int, b: int) -> bool:
        return not near((r, g, b), NAVY) and not near((r, g, b), LOGO_BG)

    band = (
        COVER_LOGO_X_IN - 0.15,
        COVER_LOGO_Y_IN - 0.15,
        COVER_LOGO_X_IN + COVER_LOGO_W_IN + 0.15,
        COVER_LOGO_BOTTOM_IN + 0.15,
    )
    artwork = bbox(pix, is_artwork, band[0], band[1], band[2], band[3], dpi)
    if artwork is None:
        results.append(("cover logo present", False, "no artwork in the cover logo band"))
        return results

    left, top, right, bottom = artwork
    inside = (
        bottom <= COVER_LOGO_BOTTOM_IN + 0.05
        and top >= COVER_LOGO_Y_IN - 0.05
        and left >= COVER_LOGO_X_IN - 0.05
        and right <= COVER_LOGO_X_IN + COVER_LOGO_W_IN + 0.05
    )
    results.append(
        (
            "cover logo inside frame",
            inside,
            f"artwork x {left:.2f}-{right:.2f} y {top:.2f}-{bottom:.2f} in; "
            f"frame y {COVER_LOGO_Y_IN:.2f}-{COVER_LOGO_BOTTOM_IN:.2f}",
        )
    )

    gap = COVER_TITLE_Y_IN - bottom
    results.append(
        (
            "cover logo / title clear space",
            gap >= MIN_GAP_IN,
            f"gap {gap:+.2f} in (min {MIN_GAP_IN:.2f})",
        )
    )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", nargs="?", default="ai_venture_studio_client_presentation.pptx")
    parser.add_argument("--out-dir", default="qa-render")
    parser.add_argument("--dpi", type=int, default=DEFAULT_DPI)
    parser.add_argument("--keep-pdf", action="store_true")
    args = parser.parse_args()

    deck = Path(args.deck).resolve()
    if not deck.exists():
        print(f"ERROR: deck not found: {deck}")
        return 1

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    pdf = to_pdf(deck, out_dir)
    doc = pymupdf.open(pdf)
    scale = args.dpi / 72.0
    print(f"=== render: {deck.name} -> {pdf.name} ({doc.page_count} pages) ===")
    if doc.page_count < CLOSING_INDEX + 1:
        print(f"ERROR: expected at least {CLOSING_INDEX + 1} pages")
        return 1

    pix_cache = {}
    for index in (COVER_INDEX, CLOSING_INDEX):
        pix = doc[index].get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False)
        target = out_dir / f"qa-deck-s{index + 1:02d}.png"
        pix.save(target)
        print(f"saved {target.name} ({pix.width}x{pix.height})")
        pix_cache[index] = pix

    failed = 0
    for name, ok, detail in probe_cover(pix_cache[COVER_INDEX], args.dpi):
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
        if not ok:
            failed += 1
    for name, ok, detail in probe_closing(pix_cache[CLOSING_INDEX], args.dpi):
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
        if not ok:
            failed += 1

    doc.close()
    if not args.keep_pdf:
        pdf.unlink(missing_ok=True)

    print()
    if failed:
        print(f">> {failed} RENDER CHECK(S) FAILED <<")
        return 1
    print(">> ALL RENDER CHECKS PASSED <<")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
