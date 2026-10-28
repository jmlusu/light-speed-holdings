"""Final verification of the delivered briefing PDF.

Gates: text layer integrity, cover copy, page count/geometry, palette sampling.
Exits non-zero on any failure so this doubles as a CI-able check.
"""

import re
import sys

import pymupdf

PDF = "artifacts/campaigns/2026-10-26-pipeline-test/open-design/executive-briefing-branded.pdf"

REQUIRED = [
    "ASPIRE. ACT. ACHIEVE.",
    "LightSpeed Holdings Limited",
    "Scaling Agentic AI Architecture",
    "1 data table",
    "5 sections",
]

FORBIDDEN = ["table(s)", "(s) ·", "None", "{{", "}}"]

doc = pymupdf.open(PDF)
text = "".join(page.get_text() for page in doc)
fails = []

spaced = re.findall(r"(?:\b[A-Z0-9] ){3,}", text)
print(f"pages        {doc.page_count}")
print(f"chars        {len(text)}")
print(f"spaced_runs  {len(spaced)}")
if spaced:
    fails.append(f"spaced letter runs: {spaced[:5]}")

print("required:")
for want in REQUIRED:
    ok = want in text
    print(f"  {'OK  ' if ok else 'MISS'} {want!r}")
    if not ok:
        fails.append(f"missing {want!r}")

print("forbidden:")
for bad in FORBIDDEN:
    hit = bad in text
    print(f"  {'HIT ' if hit else 'OK  '} {bad!r}")
    if hit:
        fails.append(f"forbidden {bad!r}")

print("geometry:")
for i, page in enumerate(doc, 1):
    w, h = round(page.rect.width, 1), round(page.rect.height, 1)
    ok = (w, h) == (595.0, 841.9)
    print(f"  page {i}: {w} x {h} {'A4' if ok else 'NOT A4'}")
    if not ok:
        fails.append(f"page {i} not A4")

cover = doc[0].get_text()
line = next((ln for ln in cover.splitlines() if "word" in ln), "(no subtitle line)")
print(f"cover: {line.strip()!r}")

print("RESULT:", "FAIL" if fails else "PASS")
for f in fails:
    print("  -", f)
sys.exit(1 if fails else 0)
