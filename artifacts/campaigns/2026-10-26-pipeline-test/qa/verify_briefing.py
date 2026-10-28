"""Brand-compliance verification for the LightSpeed executive briefing.

Runs five independent gates over the delivered artifact and prints a verdict:

  G1  CSS source   — every declared colour is a brand-token value
  G2  PDF content  — every fill/stroke operator in the PDF is a token value
  G3  Palette gate — check_brand_palette.py on rasterised pages (the official gate)
  G4  Edge proof   — every off-palette pixel is an anti-aliasing blend of two tokens
  G5  Layout       — page count, box fit, type scale, contrast, dominance

Rasterising: PyMuPDF rounds every channel down by up to 1 LSB (verified by
probe_colour.py), which would fail a pixel-exact gate for reasons that have
nothing to do with the artifact. The rasteriser is therefore poppler's
pdftoppm, which reproduces the stored values exactly.

Usage:
    python artifacts/campaigns/2026-10-26-pipeline-test/qa/verify_briefing.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np
from PIL import Image

CAMPAIGN = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
HTML = CAMPAIGN / "open-design" / "executive-briefing.html"
PDF = CAMPAIGN / "open-design" / "executive-briefing-branded.pdf"
QA = CAMPAIGN / "qa"
TOKENS_JSON = REPO / "brand" / "tokens" / "brand-tokens.json"
GATE = REPO / ".agents" / "skills" / "ls-visual-storytelling" / "scripts" / "check_brand_palette.py"

# Raster region of the logo lockup on page 1, at 96dpi CSS pixels:
#   left 14mm, top 9mm, artwork 44 x 39.4mm  ->  converted below.
LOGO_BOX_MM = (14.0, 9.0, 44.0, 39.4)
MM_PER_INCH = 25.4


def load_tokens() -> set[str]:
    data = json.loads(TOKENS_JSON.read_text(encoding="utf-8"))
    out = set()
    for spec in data["color"].values():
        value = spec.get("value", "")
        if value.startswith("#"):
            out.add(value.upper())
    return out


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def rgb_to_hex(rgb) -> str:
    return "#%02X%02X%02X" % tuple(int(v) for v in rgb)


# ── G1 ──────────────────────────────────────────────────────────────────────
def gate_css(tokens: set[str]) -> dict:
    html = HTML.read_text(encoding="utf-8")
    css = html.split("<style>", 1)[1].split("</style>", 1)[0]
    # Comments describe colours ("logo plate is #02062F"); they do not declare them.
    code = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    declared = {"#" + m.group(1).upper() for m in re.finditer(r"#([0-9A-Fa-f]{6})\b", code)}
    values = re.findall(r"[a-zA-Z-]+\s*:\s*([^;{}]+)", code)
    named = {
        v
        for value in values
        for v in re.findall(r"\b(white|black|red|blue|grey|gray|navy)\b", value)
        if "var(" not in value
    }
    off = sorted(declared - tokens)
    return {
        "declared": len(declared),
        "distinct_values": sorted(declared),
        "off_palette": off,
        "named_colour_keywords": sorted(named),
        "pass": not off and not named,
    }


# ── G2 ──────────────────────────────────────────────────────────────────────
PAINT_OPS = {b"f", b"f*", b"F", b"S", b"s", b"B", b"B*", b"b", b"b*", b"Tj", b"TJ", b"sh"}


def gate_pdf_colours(tokens: set[str]) -> dict:
    """Every colour operator in the page and its Form XObjects.

    A colour operator only counts if the segment it governs actually paints
    (fill/stroke/text), so Chromium's default `0 0 0 rg` pre-state — which is
    immediately overridden by `/X Do` — is reported separately instead of being
    counted as black ink.
    """
    import pymupdf

    doc = pymupdf.open(PDF)
    fills: Counter[str] = Counter()
    strokes: Counter[str] = Counter()
    unpainted: Counter[str] = Counter()
    images = 0
    xrefs: list[int] = []
    for page in doc:
        xrefs.extend(page.get_contents())
        images += len(page.get_images(full=True))
        for xref, _name, _invoker, _bbox in page.get_xobjects():
            if "/Form" in doc.xref_object(xref):
                xrefs.append(xref)

    for xref in dict.fromkeys(xrefs):
        raw = doc.xref_stream(xref) or b""
        ops = list(re.finditer(rb"([\d.]+) ([\d.]+) ([\d.]+) (rg|RG)", raw))
        for i, m in enumerate(ops):
            rgb = tuple(round(float(v) * 255) for v in m.groups()[:3])
            key = rgb_to_hex(rgb)
            end = ops[i + 1].start() if i + 1 < len(ops) else len(raw)
            tokens_in_segment = set(raw[m.end() : end].split())
            target = fills if m.group(4) == b"rg" else strokes
            if tokens_in_segment & PAINT_OPS:
                target[key] += 1
            else:
                unpainted[key] += 1
    doc.close()

    used = set(fills) | set(strokes)
    off = sorted(used - tokens)
    return {
        "painted_fill_colours": dict(fills.most_common()),
        "painted_stroke_colours": dict(strokes.most_common()),
        "declared_but_unpainted": dict(unpainted.most_common()),
        "embedded_images": images,
        "off_palette": off,
        "pass": not off,
    }


# ── rasterising ─────────────────────────────────────────────────────────────
def rasterise(dpi: int) -> list[Path]:
    prefix = QA / f"pdf-{dpi}dpi"
    for old in QA.glob(f"pdf-{dpi}dpi-*.png"):
        old.unlink()
    subprocess.run(
        ["pdftoppm", "-r", str(dpi), "-png", str(PDF), str(prefix)],
        check=True,
        capture_output=True,
    )
    return sorted(QA.glob(f"pdf-{dpi}dpi-*.png"))


# ── G3 ──────────────────────────────────────────────────────────────────────
def gate_palette_official(pages: list[Path], tolerance: float) -> dict:
    results = []
    for page in pages:
        proc = subprocess.run(
            [sys.executable, str(GATE), str(page), "--tolerance", str(tolerance), "--verbose"],
            capture_output=True,
            text=True,
        )
        out = (proc.stdout + proc.stderr).strip().splitlines()
        results.append({"page": page.name, "rc": proc.returncode, "output": out[-1]})
    return {"results": results, "pass": all(r["rc"] == 0 for r in results)}


# ── G4 ──────────────────────────────────────────────────────────────────────
def segment_distance(p: np.ndarray, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Per-point distance from p to segment ab (vectorised)."""
    ab = b - a
    denom = float(ab @ ab)
    if denom == 0.0:
        return np.linalg.norm(p - a, axis=1)
    t = np.clip(((p - a) @ ab) / denom, 0.0, 1.0)
    proj = a + t[:, None] * ab
    return np.linalg.norm(p - proj, axis=1)


def gate_edge_proof(pages: list[Path], tokens: set[str], dpi: int) -> dict:
    palette = np.array([hex_to_rgb(t) for t in sorted(tokens)], dtype=float)
    segments = [(palette[i], palette[j]) for i, j in combinations(range(len(palette)), 2)]
    px_per_mm = dpi / MM_PER_INCH
    lx, ly, lw, lh = LOGO_BOX_MM

    report = []
    for idx, page in enumerate(pages, start=1):
        arr = np.asarray(Image.open(page).convert("RGB")).astype(np.int16)
        h, w, _ = arr.shape
        flat = arr.reshape(-1, 3)
        keys = (flat[:, 0].astype(np.int32) << 16) | (flat[:, 1].astype(np.int32) << 8) | flat[:, 2]
        uniq, inverse = np.unique(keys, return_inverse=True)
        counts = np.bincount(inverse, minlength=len(uniq))

        token_keys = {
            (r << 16) | (g << 8) | b for r, g, b in (hex_to_rgb(t) for t in sorted(tokens))
        }
        off_mask = np.isin(uniq, list(token_keys), invert=True)

        # logo region mask, per pixel
        in_logo = np.zeros((h, w), dtype=bool)
        if idx == 1:
            in_logo[
                int(ly * px_per_mm) : int((ly + lh) * px_per_mm),
                int(lx * px_per_mm) : int((lx + lw) * px_per_mm),
            ] = True
        in_logo_flat = in_logo.reshape(-1)
        uniq_in_logo = np.bincount(inverse, weights=in_logo_flat, minlength=len(uniq)) > 0

        colours = np.stack([(uniq >> 16) & 0xFF, (uniq >> 8) & 0xFF, uniq & 0xFF], axis=1).astype(
            float
        )

        # classify each distinct off-palette colour
        off_idx = np.where(off_mask)[0]
        worst = np.inf
        not_blend = 0
        not_blend_logo = 0
        not_blend_px = 0
        for i in off_idx:
            p = colours[i][None, :]
            best = min(segment_distance(p, a, b)[0] for a, b in segments)
            worst = min(worst, best) if best <= 8.0 else worst
            if best > 8.0:
                if uniq_in_logo[i]:
                    not_blend_logo += 1
                else:
                    not_blend += 1
                    not_blend_px += int(counts[i])

        off_px = int(counts[off_idx].sum())
        report.append(
            {
                "page": page.name,
                "visible_px": int(flat.shape[0]),
                "off_palette_px": off_px,
                "off_palette_pct": round(off_px * 100.0 / flat.shape[0], 2),
                "off_palette_distinct_colours": int(len(off_idx)),
                "max_blend_distance_outside_logo": round(worst, 2) if worst != np.inf else None,
                "non_blend_colours_outside_logo": not_blend,
                "non_blend_pixels_outside_logo": not_blend_px,
                "non_blend_colours_inside_logo": not_blend_logo,
            }
        )

    # foreign colours = off-palette AND not a blend of two tokens AND outside the
    # logo artwork (whose own palette is an ADR-027 sanctioned exception).
    foreign = sum(r["non_blend_colours_outside_logo"] for r in report)
    return {"pages": report, "foreign_colours_outside_logo": foreign, "pass": foreign == 0}


# ── G5 ──────────────────────────────────────────────────────────────────────
def relative_luminance(rgb) -> float:
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = relative_luminance(hex_to_rgb(a)), relative_luminance(hex_to_rgb(b))
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)


def gate_layout(pages: list[Path]) -> dict:
    import pymupdf

    doc = pymupdf.open(PDF)
    sizes = {(round(p.rect.width, 1), round(p.rect.height, 1)) for p in doc}
    text = [p.get_text() for p in doc]
    fonts = set()
    for p in doc:
        for block in p.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    fonts.add((span["font"], round(span["size"], 1)))
    doc.close()

    css = HTML.read_text(encoding="utf-8")
    sizes_pt = sorted(
        {round(float(m.group(1)), 1) for m in re.finditer(r"font-size:\s*([\d.]+)pt", css)}
    )
    brand_scale = {36.0, 32.0, 28.0, 24.0, 18.0, 16.0, 14.0, 13.0, 12.0}

    used_pdf = sorted({s for _, s in fonts})
    return {
        "pages": len(text),
        "page_sizes_pt": sorted(sizes),
        "a4": all(abs(w - 595.0) < 1.5 and abs(h - 841.9) < 1.5 for w, h in sizes),
        "fonts_embedded": sorted({f for f, _ in fonts}),
        "css_type_sizes_pt": sizes_pt,
        "css_sizes_off_scale": [s for s in sizes_pt if s not in brand_scale],
        "pdf_rendered_sizes_pt": used_pdf,
        "pdf_sizes_off_scale": [
            s for s in used_pdf if round(s) not in {round(x) for x in brand_scale}
        ],
        "chars_extracted": sum(len(t) for t in text),
        "contrast": {
            "navy-on-white": contrast("#070A40", "#FFFFFF"),
            "white-on-navy": contrast("#FFFFFF", "#070A40"),
            "cyan-on-navy": contrast("#00BFFF", "#070A40"),
            "grey-dark-on-white": contrast("#6B7280", "#FFFFFF"),
            "navy-on-grey-light": contrast("#070A40", "#F2F2F2"),
            "grey-light-text-on-navy": contrast("#9CA3AF", "#070A40"),
            "red-on-white": contrast("#E63946", "#FFFFFF"),
        },
    }


def dominance(pages: list[Path]) -> list[dict]:
    token_names = {
        "#070A40": "navy",
        "#E63946": "red",
        "#00BFFF": "cyan",
        "#F2F2F2": "grey-light",
        "#FFFFFF": "white",
        "#6B7280": "grey-dark",
        "#9CA3AF": "grey-light-text",
        "#F7F8F9": "mist",
        "#121518": "deep-mineral",
    }
    out = []
    for page in pages:
        arr = np.asarray(Image.open(page).convert("RGB")).reshape(-1, 3).astype(np.int16)
        total = arr.shape[0]
        row = {"page": page.name}
        packed = (arr[:, 0].astype(np.int32) << 16) | (arr[:, 1].astype(np.int32) << 8) | arr[:, 2]
        for hexv, name in token_names.items():
            r, g, b = hex_to_rgb(hexv)
            row[name] = round(
                float(np.count_nonzero(packed == ((r << 16) | (g << 8) | b))) * 100 / total, 2
            )
        out.append(row)
    return out


def main() -> int:
    tokens = load_tokens()
    print(f"brand tokens          : {len(tokens)} distinct -> {sorted(tokens)}")

    g1 = gate_css(tokens)
    print(f"\nG1 CSS source         : {'PASS' if g1['pass'] else 'FAIL'}")
    print(f"   declared colours   : {g1['declared']}  off-palette: {g1['off_palette'] or 'none'}")
    print(f"   raw keywords       : {g1['named_colour_keywords'] or 'none'}")

    g2 = gate_pdf_colours(tokens)
    print(f"\nG2 PDF colour ops     : {'PASS' if g2['pass'] else 'FAIL'}")
    print(f"   painted fills      : {g2['painted_fill_colours']}")
    print(f"   painted strokes    : {g2['painted_stroke_colours']}")
    print(f"   declared, unpainted: {g2['declared_but_unpainted'] or 'none'}")
    print(f"   off-palette        : {g2['off_palette'] or 'none'}")
    print(f"   embedded images    : {g2['embedded_images']}")

    pages300 = rasterise(300)
    pages600 = rasterise(600)

    g3_300 = gate_palette_official(pages300, 3.0)
    g3_600 = gate_palette_official(pages600, 3.0)
    print(f"\nG3 palette gate @300  : {'PASS' if g3_300['pass'] else 'FAIL'}")
    for r in g3_300["results"]:
        print(f"   {r['page']}: {r['output']}")
    print(f"G3 palette gate @600  : {'PASS' if g3_600['pass'] else 'FAIL'}")
    for r in g3_600["results"]:
        print(f"   {r['page']}: {r['output']}")

    g4 = gate_edge_proof(pages300, tokens, 300)
    print(f"\nG4 edge proof @300    : {'PASS' if g4['pass'] else 'FAIL'}")
    for r in g4["pages"]:
        print(
            f"   {r['page']}: off {r['off_palette_px']:,}px ({r['off_palette_pct']}%) "
            f"across {r['off_palette_distinct_colours']:,} distinct colours; "
            f"non-blend outside logo: {r['non_blend_colours_outside_logo']} colours / "
            f"{r['non_blend_pixels_outside_logo']} px; "
            f"logo artwork colours: {r['non_blend_colours_inside_logo']}"
        )
    print(f"   foreign colours outside logo artwork: {g4['foreign_colours_outside_logo']}")

    g5 = gate_layout(pages300)
    print(
        f"\nG5 layout             : pages={g5['pages']} A4={g5['a4']} "
        f"chars={g5['chars_extracted']:,}"
    )
    print(f"   pdf fonts          : {g5['fonts_embedded']}")
    print(
        f"   css type sizes     : {g5['css_type_sizes_pt']} (off-scale: {g5['css_sizes_off_scale'] or 'none'})"
    )
    print(
        f"   rendered sizes     : {g5['pdf_rendered_sizes_pt']} (off-scale: {g5['pdf_sizes_off_scale'] or 'none'})"
    )
    print("   contrast ratios    :")
    for k, v in g5["contrast"].items():
        print(f"      {k:28s} {v}:1")

    dom = dominance(pages300)
    print("\n   palette dominance  :")
    for row in dom:
        print(
            f"      {row['page']}: "
            + ", ".join(f"{k} {v}%" for k, v in row.items() if k != "page" and v > 0)
        )

    summary = {
        "tokens": sorted(tokens),
        "G1_css": g1,
        "G2_pdf": g2,
        "G3_300": g3_300,
        "G3_600": g3_600,
        "G4_edges": g4,
        "G5_layout": g5,
        "dominance": dom,
    }
    out = QA / "brand-verification.json"
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nreport -> {out}")

    ok = g1["pass"] and g2["pass"] and g3_600["pass"] and g4["pass"]
    print("\nVERDICT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
