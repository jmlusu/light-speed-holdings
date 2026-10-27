"""Geometry + accessibility audit for the campaign schematic SVG.

Checks every rect/line/text stays inside the 1200x640 canvas and that no text
run is estimated to overflow its container. Also confirms brand palette usage.
"""

import xml.etree.ElementTree as ET

SVG = "artifacts/campaigns/2026-10-26-pipeline-test/open-design/schematic.svg"
W, H = 1200, 640
BRAND = {
    "#070A40",
    "#E63946",
    "#00BFFF",
    "#F7F8F9",
    "#121518",
    "#F2F2F2",
    "#FFFFFF",
    "#6B7280",
    "#9CA3AF",
    "#02062F",
}

# Conservative Arial average advance widths (em fraction) by weight.
ADV = {"normal": 0.52, "700": 0.60}

tree = ET.parse(SVG)
root = tree.getroot()
ns = "{http://www.w3.org/2000/svg}"
issues, checked = [], 0
colours_used = set()

for el in root.iter():
    tag = el.tag.replace(ns, "")
    if tag in ("rect",):
        x, y = float(el.get("x", 0)), float(el.get("y", 0))
        w, h = float(el.get("width", 0)), float(el.get("height", 0))
        if x < 0 or y < 0 or x + w > W or y + h > H:
            issues.append(f"rect out of bounds: x={x} y={y} w={w} h={h}")
        checked += 1
    elif tag == "line":
        for k in ("x1", "x2"):
            if not (0 <= float(el.get(k)) <= W):
                issues.append(f"line {k} out of bounds: {el.get(k)}")
        for k in ("y1", "y2"):
            if not (0 <= float(el.get(k)) <= H):
                issues.append(f"line {k} out of bounds: {el.get(k)}")
        checked += 1
    elif tag == "image":
        x, y = float(el.get("x", 0)), float(el.get("y", 0))
        w, h = float(el.get("width", 0)), float(el.get("height", 0))
        if x < 0 or y < 0 or x + w > W or y + h > H:
            issues.append(f"image out of bounds: x={x} y={y} w={w} h={h}")
        href = el.get("{http://www.w3.org/1999/xlink}href") or el.get("href") or ""
        if not href.startswith("data:image/"):
            issues.append("image is not inlined (external asset dependency)")
        checked += 1
    elif tag == "text":
        txt = "".join(el.itertext())
        size = float(el.get("font-size", 12))
        weight = el.get("font-weight", "normal")
        anchor = el.get("text-anchor", "start")
        x, y = float(el.get("x", 0)), float(el.get("y", 0))
        est = len(txt) * size * ADV["700" if weight == "700" else "normal"]
        left, right = (x - est, x) if anchor == "end" else (x, x + est)
        if left < 0 or right > W:
            issues.append(f"text overflow ({anchor}): '{txt[:42]}' est_right={right:.0f}")
        if y > H:
            issues.append(f"text below canvas: '{txt[:42]}' y={y}")
        checked += 1

    fill = el.get("fill")
    if fill and fill.startswith("#"):
        colours_used.add(fill.upper())
    stroke = el.get("stroke")
    if stroke and stroke.startswith("#"):
        colours_used.add(stroke.upper())

off_brand = sorted(c for c in colours_used if c not in {b.upper() for b in BRAND})

print("SCHEMATIC GEOMETRY AUDIT")
print("-" * 52)
print(f"elements checked      : {checked}")
print(f"canvas                : {W}x{H}")
print(f"colours used          : {len(colours_used)} -> {sorted(colours_used)}")
print(f"off-brand colours     : {off_brand or 'none'}")
print(
    f"a11y: <title>/<desc>  : "
    f"{'present' if root.find(f'{ns}title') is not None and root.find(f'{ns}desc') is not None else 'MISSING'}"
)
print(f"layout issues         : {len(issues)}")
for i in issues:
    print(f"   - {i}")
print("-" * 52)
print("RESULT:", "PASS" if not issues and not off_brand else "FAIL")
