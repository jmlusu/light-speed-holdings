"""Diagnose rasteriser colour drift: does the PDF or the rasteriser round colours?

Renders one swatch per brand token through the same Playwright -> PDF pipeline,
then reads back (a) the solid fill colour actually stored in the PDF content
stream and (b) the pixel value PyMuPDF produces when rasterising it.
"""

from pathlib import Path

import pymupdf
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
TOKENS = [
    "#070A40",
    "#E63946",
    "#00BFFF",
    "#F2F2F2",
    "#FFFFFF",
    "#6B7280",
    "#9CA3AF",
    "#F7F8F9",
    "#121518",
]


def build_html(tmp: Path) -> Path:
    cells = "".join(f'<div style="width:120px;height:60px;background:{c}"></div>' for c in TOKENS)
    html = f"<html><body style='margin:0'><div style='display:flex'>{cells}</div></body></html>"
    tmp.write_text(html, encoding="utf-8")
    return tmp


def main() -> None:
    tmp = HERE / "_probe_swatches.html"
    pdf = HERE / "_probe_swatches.pdf"
    build_html(tmp)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 200})
        page.goto(tmp.as_uri(), wait_until="load")
        page.pdf(
            path=str(pdf),
            width="1080px",
            height="200px",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
        browser.close()

    doc = pymupdf.open(pdf)
    page = doc[0]
    print("PDF fill colours in content stream:")
    seen = set()
    for _item in page.get_contents():
        pass
    raw = b"".join(doc.xref_stream(x) for x in page.get_contents())
    import re

    for m in re.finditer(rb"([\d.]+) ([\d.]+) ([\d.]+) rg", raw):
        rgb = tuple(round(float(v) * 255) for v in m.groups())
        if rgb not in seen:
            seen.add(rgb)
            print(f"   #{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}  raw={m.group(0)!r}")

    print("\nPyMuPDF raster values:")
    for kwargs in (
        {"dpi": 96},
        {"dpi": 96, "colorspace": pymupdf.csRGB, "alpha": False},
    ):
        pix = page.get_pixmap(**kwargs)
        img = pix.samples
        n = pix.n
        sample = []
        for i in range(len(TOKENS)):
            x = int((i * 120 + 60) * (pix.width / 1080))
            y = int(30 * (pix.height / 200))
            off = (y * pix.width + x) * n
            sample.append("#%02X%02X%02X" % (img[off], img[off + 1], img[off + 2]))
        print(f"   {kwargs} -> {sample}")

    print("\n   expected       ->", TOKENS)
    doc.close()
    tmp.unlink(missing_ok=True)
    pdf.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
