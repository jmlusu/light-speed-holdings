"""Render the LightSpeed executive briefing (HTML/CSS) to a branded A4 PDF.

Render path: Playwright Chromium -> page.pdf() (Path A in ls-document-design).
The HTML is self-contained apart from the official logo, which is referenced by
its canonical path (brand/logo/logo-full.png).

Outputs
-------
executive-briefing-branded.pdf   2-page A4 deliverable
qa/page-1@300.png, page-2@300.png  rasterised pages for the visual + palette gates

Usage
-----
    python artifacts/campaigns/2026-10-26-pipeline-test/open-design/render_briefing.py
"""

from pathlib import Path

import pymupdf
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
HTML = HERE / "executive-briefing.html"
PDF = HERE / "executive-briefing-branded.pdf"
QA = HERE.parent / "qa"
DPI = 300


def render_pdf() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(HTML.as_uri(), wait_until="load")
        # Arial must be resolved (no fallback substitution) before printing.
        page.wait_for_function("document.fonts.status === 'loaded'")
        page.pdf(
            path=str(PDF),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()


def rasterise() -> list[Path]:
    QA.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(PDF)
    outs: list[Path] = []
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(dpi=DPI)
        out = QA / f"page-{i}@{DPI}.png"
        pix.save(out)
        outs.append(out)
    doc.close()
    return outs


def report() -> None:
    doc = pymupdf.open(PDF)
    print(f"PDF      : {PDF}")
    print(f"bytes    : {PDF.stat().st_size:,}")
    print(f"pages    : {doc.page_count}")
    for i, page in enumerate(doc, start=1):
        r = page.rect
        print(
            f"  page {i}  {r.width:.1f} x {r.height:.1f} pt  "
            f"({r.width / 72 * 25.4:.1f} x {r.height / 72 * 25.4:.1f} mm)"
        )
    doc.close()


if __name__ == "__main__":
    render_pdf()
    report()
    for path in rasterise():
        print(f"raster   : {path}")
