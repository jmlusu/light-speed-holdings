#!/usr/bin/env python3
"""P2 public-SPA token confinement sweep (site ticket #303).

Remaps every off-palette colour on the public SPA onto the LightSpeed ls-*
token surface (navy #070A40 / red #E63946 / cyan #00BFFF / white #FFFFFF /
grey-light #F2F2F2, plus user-sanctioned grey-dark #6B7280 and
grey-light-text #9CA3AF, Arial type scale) — then prunes the now-unused
CSS infrastructure in the same pass.

Scope decisions (user-confirmed):
  * On-palette re-skin, KEEP the tactile/motif design language.
  * PRUNE everything unused in this ticket: unreferenced classes,
    keyframes, comments, @theme aliases (amber/orange/tectonic/gilded),
    font-mono/font-serif, and inlined colour variables.

Files touched: *.tsx under src/ (className literal contents only), the
Vite entry index.html, and src/index.css (which owns all custom classes).
Out of scope: command-bar / command-center / jarvis internal sheets.

Usage:
    python scripts/p2-token-sweep.py            # dry-run plan
    python scripts/p2-token-sweep.py --apply    # write changes
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "src"
INDEX_HTML = ROOT / "index.html"
CSS_PATH = SRC_DIR / "index.css"

NAVY = "#070a40"
RED = "#e63946"
CYAN = "#00bfff"
WHITE = "#ffffff"
GREY_LIGHT = "#f2f2f2"
GREY_DARK = "#6b7280"
GREY_LIGHT_TEXT = "#9ca3af"

MONO_STACK = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
ARIAL_STACK = 'Arial, "Helvetica Neue", Helvetica, sans-serif'

audit_notes: list[str] = []
dropped_selectors: list[str] = []
TEMPLATE_PREFIXES: set[str] = set()


# ── palette helpers ───────────────────────────────────────────────────
def fmt_alpha(a: float) -> str:
    return "1" if a == 1 else f"{a:.2f}".rstrip("0").rstrip(".")


def rgba(hexish: str, alpha: float) -> str:
    h = hexish.lstrip("#")[:6]
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{fmt_alpha(alpha)})"


def _nearest_neutral(r: int, g: int, b: int, a: float) -> str:
    """Nearest-anchor classifier used for anything not in the explicit table."""
    anchors = {
        "navy": (7, 10, 64),
        "red": (230, 57, 70),
        "cyan": (0, 191, 255),
        "white": (255, 255, 255),
        "grey-light": (242, 242, 242),
        "grey-dark": (107, 114, 128),
        "grey-light-text": (156, 163, 175),
    }

    def dist(c1, c2):
        dr, dg, db = c1[0] - c2[0], c1[1] - c2[1], c1[2] - c2[2]
        return dr * dr * 0.7 + dg * dg * 0.7 + db * db * 0.4

    best = min(anchors, key=lambda k: dist((r, g, b), anchors[k]))
    base = {
        "navy": NAVY,
        "red": RED,
        "cyan": CYAN,
        "white": WHITE,
        "grey-light": GREY_LIGHT,
        "grey-dark": GREY_DARK,
        "grey-light-text": GREY_LIGHT_TEXT,
    }[best]
    audit_notes.append(f"nearest-anchor fallback: rgb({r},{g},{b}) -> {base}")
    return rgba(base, a)


def rgba_remap(r: int, g: int, b: int, a: float) -> str:
    if (r, g, b) == (0, 0, 0):
        return rgba(NAVY, a)
    if (r, g, b) == (7, 10, 64) or (r, g, b) == (5, 7, 45):
        return rgba(NAVY, a)
    if (r, g, b) == (230, 57, 70):
        return rgba(RED, a)
    if (r, g, b) == (0, 191, 255):
        return rgba(CYAN, a)
    if (r, g, b) == (255, 255, 255):
        return rgba(WHITE, a)
    if (r, g, b) == (16, 185, 129):
        return rgba(CYAN, a)  # emerald/green -> cyan
    if (r, g, b) == (239, 68, 68):  # red-500
        return rgba(RED, a)
    if (r, g, b) == (239, 86, 103):  # amber-400
        return rgba(RED, a)
    if (r, g, b) == (251, 122, 133):  # gilded gold bright
        return rgba(RED, a)
    if (r, g, b) == (250, 204, 21):  # amber-400 base
        return rgba(RED, a)
    if (r, g, b) == (252, 214, 217):  # pale pink highlight
        return rgba(RED, 0.40)
    if (r, g, b) == (255, 170, 180):  # bright pink
        return rgba(RED, 0.60)
    if (r, g, b) == (106, 10, 15):  # gilded shadow
        return rgba(RED, a)
    if (r, g, b) == (143, 15, 26):  # gilded bronze
        return rgba(RED, a)
    if (r, g, b) == (193, 18, 31):  # gilded deep
        return rgba(RED, a)
    if (r, g, b) == (11, 15, 85) or (r, g, b) == (16, 22, 94):  # tectonic
        return rgba(NAVY, a)
    if (r, g, b) == (24, 24, 27):  # zinc-900 deck
        return rgba(NAVY, a)
    if (r, g, b) == (51, 65, 85):  # slate-700 well
        return rgba(NAVY, a)
    if (r, g, b) == (100, 116, 139) or (r, g, b) == (148, 163, 184):
        return rgba(GREY_LIGHT_TEXT, a)  # slate-500/400
    if (r, g, b) == (155, 179, 196):  # steel border
        return rgba(GREY_LIGHT_TEXT, a)
    if (r, g, b) == (226, 232, 240):  # slate-200 glass
        return rgba(WHITE, a)
    return _nearest_neutral(r, g, b, a)


def norm_hex(h: str) -> str:
    h = h.lower()
    if len(h) == 3:
        return "".join(c * 2 for c in h)
    if len(h) == 4:
        return h[0] * 2 + h[1] * 2 + h[2] * 2 + h[3] * 2
    return h[:6]


def hex_to_palette(value: str) -> str | None:
    key = norm_hex(value.lstrip("#"))
    return HEX_MAP.get(key)


# ── CSS literal hex → palette ─────────────────────────────────────────
HEX_MAP = {
    "000000": NAVY,
    "070a40": NAVY,
    "ffffff": WHITE,
    "f2f2f2": GREY_LIGHT,
    # navy family (tectonic ramp) -> navy at depth
    "0b0f55": rgba(NAVY, 0.95),
    "10165e": rgba(NAVY, 0.90),
    "1a2170": rgba(NAVY, 0.85),
    "262c91": rgba(NAVY, 0.80),
    "3740ac": rgba(NAVY, 0.75),
    "4953b8": rgba(NAVY, 0.70),
    # dark metal / charcoal -> navy
    "040810": rgba(NAVY, 0.98),
    "0a0b10": rgba(NAVY, 0.95),
    "0d0f15": rgba(NAVY, 0.92),
    "0d0d10": rgba(NAVY, 0.95),
    "18181b": rgba(NAVY, 0.92),
    "141720": rgba(NAVY, 0.90),
    "171922": rgba(NAVY, 0.88),
    "1e222e": rgba(NAVY, 0.90),
    "27272a": rgba(NAVY, 0.92),
    "2a2e3d": rgba(NAVY, 0.92),
    "2a2f3e": rgba(NAVY, 0.90),
    "3b4255": rgba(NAVY, 0.88),
    "3f3f46": rgba(NAVY, 0.90),
    # steel petrol -> navy
    "0c1c28": rgba(NAVY, 0.95),
    "102434": rgba(NAVY, 0.93),
    "1d3e56": rgba(NAVY, 0.90),
    "132737": rgba(NAVY, 0.93),
    # slate navy-greys -> navy
    "1e293b": rgba(NAVY, 0.85),
    "334155": rgba(NAVY, 0.80),
    "475569": rgba(NAVY, 0.70),
    # light steel / light greys -> grey-light surfaces
    "e2e2e2": GREY_LIGHT,
    "e2e6ec": GREY_LIGHT,
    "edf3f8": GREY_LIGHT,
    "f3f5f8": GREY_LIGHT,
    "f4f8fb": GREY_LIGHT,
    "dbe7f0": rgba(NAVY, 0.08),
    "f0f6fa": WHITE,
    "f1f5f9": GREY_LIGHT,
    "f8fafc": WHITE,
    # steel borders -> grey-light-text
    "9bb3c4": GREY_LIGHT_TEXT,
    "9ca3af": GREY_LIGHT_TEXT,
    "a1a1aa": GREY_LIGHT_TEXT,
    "b3b3b3": GREY_LIGHT_TEXT,
    "c2d5e3": GREY_LIGHT_TEXT,
    "cbd5e1": GREY_LIGHT_TEXT,
    "d0d5de": GREY_LIGHT_TEXT,
    "94a3b8": GREY_LIGHT_TEXT,
    # red family -> ls-red derived
    "e63946": RED,
    "c1121f": rgba(RED, 0.85),
    "ef4444": RED,
    "ef5667": rgba(RED, 0.90),
    "f26e7e": rgba(RED, 0.82),
    "f5838f": rgba(RED, 0.75),
    "f8b4ba": rgba(RED, 0.55),
    "f8c2c2": rgba(RED, 0.50),
    "fbd9dc": rgba(RED, 0.30),
    "fdf1f2": rgba(RED, 0.08),
    "fb7a85": rgba(RED, 0.65),
    "ffaab4": rgba(RED, 0.60),
    "6a0a0f": rgba(RED, 0.75),
    "8f0f1a": rgba(RED, 0.85),
    "9e0e18": rgba(RED, 0.85),
    "6f0b12": rgba(RED, 0.72),
    "4a080c": rgba(RED, 0.65),
    # greens -> cyan
    "10b981": CYAN,
    # amber tailwind hexes (in @theme, pruned anyway)
    "fdc5d0": rgba(RED, 0.40),
    "fec5cc": rgba(RED, 0.45),
    "fdeef0": rgba(RED, 0.08),
    "fdb2bc": rgba(RED, 0.55),
    "fd8fa0": rgba(RED, 0.70),
    "fd6f85": rgba(RED, 0.80),
    "fb5d75": rgba(RED, 0.82),
    "f94d68": rgba(RED, 0.85),
    "f63255": rgba(RED, 0.90),
    "d61f45": rgba(RED, 0.90),
}


# ── Tailwind utility remap rules ──────────────────────────────────────
_PROPS = (
    r"(?:bg|text|border(?:-t|-b|-l|-r|-x|-y)?|from|via|to|"
    r"ring(?:-offset)?|shadow|outline(?:-color)?|divide(?:-x|-y)?|"
    r"decoration|caret|accent|placeholder|fill|stroke)"
)
UTIL_RE = re.compile(
    rf"(?<![\w-])(?P<prop>{_PROPS})-"
    r"(?P<color>[a-z]+)-(?P<shade>\d{2,3})(?P<op>/[\d.]+)?"
)
ARB_RE = re.compile(
    rf"(?<![\w-])(?P<prop>{_PROPS})-"
    r"\[#(?P<hex>[0-9a-fA-F]{3,8})\](?P<op>/[\d.]+)?"
)
EXTRA_UTIL_RE = re.compile(rf"(?<![\w-])(?P<prop>{_PROPS})-(?P<color>black|white)(?P<op>/[\d.]+)?")
INK_RE = re.compile(r"text-\[var\(--ink-primary\)\]")

_TEXT = {
    "slate": {
        50: "ls-white",
        100: "ls-white",
        200: "ls-white",
        300: "ls-grey-light-text",
        400: "ls-grey-light-text",
        500: "ls-grey-dark",
        600: "ls-grey-dark",
        700: "ls-grey-dark",
        800: "ls-navy",
        900: "ls-navy",
        950: "ls-navy",
    },
    "zinc": {
        100: "ls-white",
        200: "ls-white",
        300: "ls-grey-light-text",
        400: "ls-grey-light-text",
        500: "ls-grey-light-text",
        600: "ls-grey-dark",
        700: "ls-grey-dark",
        800: "ls-navy",
        900: "ls-navy",
        950: "ls-navy",
    },
    "gray": {
        50: "ls-white",
        100: "ls-white",
        200: "ls-white",
        300: "ls-grey-light-text",
        400: "ls-grey-light-text",
        500: "ls-grey-dark",
        600: "ls-grey-dark",
        700: "ls-grey-dark",
        800: "ls-navy",
        900: "ls-navy",
        950: "ls-navy",
    },
    "neutral": {
        50: "ls-white",
        100: "ls-white",
        200: "ls-white",
        300: "ls-grey-light-text",
        400: "ls-grey-light-text",
        500: "ls-grey-dark",
        600: "ls-grey-dark",
        700: "ls-grey-dark",
        800: "ls-navy",
        900: "ls-navy",
        950: "ls-navy",
    },
    "stone": {
        50: "ls-white",
        100: "ls-white",
        200: "ls-white",
        300: "ls-grey-light-text",
        400: "ls-grey-light-text",
        500: "ls-grey-dark",
        600: "ls-grey-dark",
        700: "ls-grey-dark",
        800: "ls-navy",
        900: "ls-navy",
        950: "ls-navy",
    },
}
_BG = {
    "slate": {
        50: "ls-grey-light",
        100: "ls-grey-light",
        200: "ls-grey-light",
        300: "ls-grey-dark",
        400: "ls-grey-dark",
        500: "ls-grey-dark",
        600: "ls-grey-dark",
        700: "ls-navy",
        800: "ls-navy",
        900: "ls-navy",
        950: "ls-navy",
    },
    "zinc": {600: "ls-white", 700: "ls-white", 800: "ls-navy", 900: "ls-navy", 950: "ls-navy"},
}
_BORDER = {
    "slate": {
        100: "ls-grey-dark",
        200: "ls-grey-dark",
        300: "ls-grey-dark",
        400: "ls-grey-light-text",
        500: "ls-grey-dark",
        600: "ls-grey-dark",
        700: "ls-white",
        800: "ls-white",
        900: "ls-white",
    },
    "zinc": {600: "ls-grey-dark", 700: "ls-grey-dark", 800: "ls-grey-dark", 900: "ls-grey-dark"},
}

_SEMANTIC = {
    scale: (
        "ls-red",
        {
            50: "0.05",
            100: "0.10",
            200: "0.20",
            300: "0.30",
            400: "0.40",
            500: "1",
            600: "0.85",
            700: "0.80",
            800: "0.72",
            900: "0.70",
            950: "0.30",
        },
    )
    for scale in ("amber", "orange", "yellow", "red", "rose", "fuchsia", "pink", "purple", "violet")
}
for scale in ("emerald", "teal", "green", "lime", "sky", "blue", "cyan", "indigo"):
    _SEMANTIC[scale] = (
        "ls-cyan",
        {
            50: "0.05",
            100: "0.10",
            200: "0.20",
            300: "0.30",
            400: "0.80",
            500: "1",
            600: "0.85",
            700: "0.80",
            800: "0.72",
            900: "0.70",
            950: "0.30",
        },
    )

_TEXT_PROPS = {"text", "placeholder", "caret", "decoration", "fill", "stroke"}
_BG_PROPS = {"bg", "from", "via", "to"}
_BORDER_PROPS = {
    "border",
    "border-t",
    "border-b",
    "border-l",
    "border-r",
    "border-x",
    "border-y",
    "divide",
    "divide-x",
    "divide-y",
    "ring",
    "ring-offset",
    "outline",
    "outline-color",
    "shadow",
}


def _map_util(m: re.Match) -> str:
    prop, color, shade, op = m.group("prop"), m.group("color"), int(m.group("shade")), m.group("op")
    if color.startswith("ls-"):
        return m.group(0)
    if color in _SEMANTIC:
        base, alpha_map = _SEMANTIC[color]
        if op:
            return f"{prop}-{base}{op}"
        a = float(alpha_map.get(shade, "1"))
        if a >= 1.0:
            return f"{prop}-{base}"
        pct = int(round(a * 100))
        return f"{prop}-{base}/{pct}"
    if color in _TEXT:
        if prop in _TEXT_PROPS:
            stem = _TEXT[color].get(shade, "ls-grey-dark")
        elif prop in _BG_PROPS:
            stem = _BG.get(color, _TEXT).get(shade, "ls-navy")
        elif prop in _BORDER_PROPS:
            ramp = _BORDER.get(color, _TEXT)
            stem = ramp.get(shade, "ls-grey-dark")
        else:
            stem = _TEXT[color].get(shade, "ls-grey-dark")
        return f"{prop}-{stem}{op or ''}"
    audit_notes.append(f"unmapped utility: {m.group(0)}")
    return m.group(0)


def _map_arb(m: re.Match) -> str:
    prop, hexval, op = m.group("prop"), m.group("hex"), m.group("op")
    repl = hex_to_palette(hexval)
    if repl is None:
        h = norm_hex(hexval)
        repl = rgba_remap(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
    return f"{prop}-[{repl}]{op or ''}"


def _map_extra(m: re.Match) -> str:
    prop, color, op = m.group("prop"), m.group("color"), m.group("op") or ""
    return f"{prop}-ls-navy{op}" if color == "black" else f"{prop}-ls-white{op}"


def map_classname(content: str) -> str:
    content = UTIL_RE.sub(_map_util, content)
    content = ARB_RE.sub(_map_arb, content)
    content = EXTRA_UTIL_RE.sub(_map_extra, content)
    content = INK_RE.sub("text-ls-grey-light-text", content)
    content = re.sub(r"\bfont-mono\b", "font-body", content)
    content = re.sub(
        r"rgba\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*([\d.]+)\s*\)",
        lambda m: rgba_remap(int(m.group(1)), int(m.group(2)), int(m.group(3)), float(m.group(4))),
        content,
    )
    return content


# ── tsx / html remap ──────────────────────────────────────────────────

_CLASSY = re.compile(
    r"\b(?:bg|text|border|from|via|to|ring|shadow|outline|divide|decoration|caret|accent|placeholder|fill|stroke)-[a-z]+(?:-\d+)?(?:/[\d.]+)?\b"
)


def _should_map_class_literal(inner: str) -> bool:
    return bool(_CLASSY.search(inner)) or "font-mono" in inner or "font-serif" in inner


def remap_class_literals(text: str) -> str:
    """Remap class-shaped strings stored in JS constants/object literals.

    Covers patterns like ``const x = 'border-slate-200/80'`` or
    ``badge: 'bg-slate-400/10 text-slate-400'`` that are later injected into a
    ``className``. Token-shaped substrings are absent from prose, so this is
    safe. Overlapping/surrounding quotes are kept as-is.
    """
    out: list[str] = []
    i = 0
    n = len(text)
    while True:
        m = re.search(r"['\"`]", text[i:])
        if m is None:
            out.append(text[i:])
            break
        j = i + m.start()
        q = m.group(0)
        end = j + 1
        while end < n:
            c = text[end]
            if c == "\\":
                end += 2
            elif c == q:
                break
            else:
                end += 1
        if end >= n:
            out.append(text[i:])
            break
        out.append(text[i:j])
        inner = text[j + 1 : end]
        if _should_map_class_literal(inner):
            out.append(q + map_classname(inner) + q)
        else:
            out.append(q + inner + q)
        i = end + 1
    return "".join(out)


def tsx_remap(apply: bool) -> tuple[list[Path], dict[str, int]]:
    changed: list[Path] = []
    counts: dict[str, int] = {}

    def remap_classnames(text: str) -> str:
        out: list[str] = []
        i = 0
        n = len(text)
        KEY = "className"
        while True:
            j = text.find(KEY, i)
            if j == -1:
                out.append(text[i:])
                break
            out.append(text[i:j])
            k = j + len(KEY)
            while k < n and text[k] in " \t\r\n":
                k += 1
            if k >= n or text[k] != "=":
                out.append(KEY)
                i = j + len(KEY)
                continue
            k += 1
            while k < n and text[k] in " \t\r\n":
                k += 1
            if k >= n:
                out.append(KEY)
                i = j + len(KEY)
                continue
            ch = text[k]
            if ch in "\"'`":
                end = k + 1
                while end < n and text[end] != ch:
                    if text[end] == "\\":
                        end += 2
                    else:
                        end += 1
                if end >= n:
                    out.append(KEY)
                    i = j + len(KEY)
                    continue
                out.append(KEY + "=" + ch + map_classname(text[k + 1 : end]) + text[end])
                i = end + 1
            elif ch == "{":
                depth = 1
                end = k + 1
                q: str | None = None
                interp = 0
                while end < n and depth > 0:
                    c = text[end]
                    if q == "`":
                        if c == "\\":
                            end += 2
                            continue
                        if c == "`":
                            q = None
                        elif c == "$" and end + 1 < n and text[end + 1] == "{":
                            depth += 1
                            interp += 1
                            end += 2
                            continue
                        elif c == "}" and interp:
                            depth -= 1
                            interp -= 1
                    elif q == '"':
                        if c == "\\":
                            end += 2
                            continue
                        if c == '"':
                            q = None
                    elif q == "'":
                        if c == "\\":
                            end += 2
                            continue
                        if c == "'":
                            q = None
                    elif c == "{":
                        depth += 1
                    elif c == "}":
                        depth -= 1
                    elif c in "\"'`":
                        q = c
                    end += 1
                if end >= n:
                    out.append(KEY)
                    i = j + len(KEY)
                    continue
                out.append(KEY + "={" + map_classname(text[k + 1 : end - 1]) + "}")
                i = end
            else:
                out.append(KEY)
                i = j + len(KEY)
        return "".join(out)

    for path in SRC_DIR.rglob("*.tsx"):
        text = path.read_text(encoding="utf-8")
        out = remap_class_literals(remap_classnames(text))
        if out != text:
            counts[path.relative_to(ROOT).as_posix()] = sum(
                1
                for x, y in zip(
                    re.findall(
                        r"\b(?:bg|text|border|from|via|to|ring|shadow|outline|divide|decoration|caret|accent|placeholder|fill|stroke)-[a-z]+(?:-\d+)?(?:/[\d.]+)?\b",
                        text,
                    ),
                    re.findall(
                        r"\b(?:bg|text|border|from|via|to|ring|shadow|outline|divide|decoration|caret|accent|placeholder|fill|stroke)-[a-z]+(?:-\d+)?(?:/[\d.]+)?\b",
                        out,
                    ),
                    strict=False,
                )
                if x != y
            )
            changed.append(path)
            if apply:
                path.write_text(out, encoding="utf-8")
    return changed, counts


def html_remap(apply: bool) -> bool:
    if not INDEX_HTML.exists():
        return False
    text = INDEX_HTML.read_text(encoding="utf-8")
    original = text
    # Only touch colour-ish attributes and inline styles; never href/id hashes.
    text = re.sub(
        r'(style="[^"]*)#([0-9a-fA-F]{6})(?![\w-])([^"]*")',
        lambda m: m.group(1) + (hex_to_palette(m.group(2)) or m.group(2)) + m.group(3),
        text,
    )
    text = re.sub(
        r'(content="[^"]*)#([0-9a-fA-F]{6})(?![\w-])([^"]*")',
        lambda m: m.group(1) + (hex_to_palette(m.group(2)) or m.group(2)) + m.group(3),
        text,
    )
    text = re.sub(
        r'(class=")([^"]*)(")',
        lambda m: m.group(1) + map_classname(m.group(2)) + m.group(3),
        text,
    )
    if text != original and apply:
        INDEX_HTML.write_text(text, encoding="utf-8")
    return text != original


# ── CSS remap ─────────────────────────────────────────────────────────
ROOT_VARS = {
    "--tectonic-abyss": "#070a40",
    "--tectonic-canyon": "#0b0f55",
    "--tectonic-plate": "#10165e",
    "--tectonic-terrace": "#1a2170",
    "--tectonic-facet": "#262c91",
    "--tectonic-facet-light": "#3740ac",
    "--tectonic-mist": "#4953b8",
    "--gilded-gold-bright": "#fb7a85",
    "--gilded-gold": "#e63946",
    "--gilded-gold-deep": "#c1121f",
    "--gilded-bronze": "#8f0f1a",
    "--gilded-shadow": "#6a0a0f",
    "--gilded-glow": "rgba(230, 57, 70, 0.45)",
    "--gilded-glow-ambient": "rgba(0, 191, 255, 0.2)",
    "--analog-silver": "#e2e2e2",
    "--analog-silver-light": "#f2f2f2",
    "--analog-silver-dark": "#b3b3b3",
    "--analog-dark": "#10165e",
    "--analog-dark-deep": "#070a40",
    "--analog-orange": "#e63946",
    "--analog-green": "#10b981",
    "--surface-dark-base": "var(--tectonic-abyss)",
    "--surface-dark-card": "var(--tectonic-plate)",
    "--surface-dark-well": "var(--tectonic-canyon)",
    "--surface-light-base": "var(--analog-silver)",
    "--surface-light-card": "#ffffff",
    "--surface-light-well": "var(--analog-silver-dark)",
    "--accent-orange": "var(--gilded-gold)",
    "--accent-orange-glow": "var(--gilded-glow)",
    "--accent-amber": "#f26e7e",
    "--accent-green": "#10b981",
}


def css_remap(text: str) -> str:
    # resolve var() chains iteratively
    prev = None
    while prev != text:
        prev = text
        text = re.sub(
            r"var\((--[a-z0-9-]+)\)", lambda m: ROOT_VARS.get(m.group(1), m.group(0)), text
        )

    def map_rgba(m: re.Match) -> str:
        return rgba_remap(int(m.group(1)), int(m.group(2)), int(m.group(3)), float(m.group(4)))

    text = re.sub(
        r"rgba\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*([\d.]+)\s*\)", map_rgba, text
    )

    def map_hex(m: re.Match) -> str:
        got = hex_to_palette(m.group(1))
        if got is not None:
            return got
        h = m.group(1)
        return rgba_remap(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)

    text = re.sub(r"(?i)#([0-9a-fA-F]{6})(?![\w-])", map_hex, text)
    return text.replace(MONO_STACK, ARIAL_STACK)


# ── CSS pruning ───────────────────────────────────────────────────────
def collect_used_classes() -> set[str]:
    used: set[str] = set()
    files = (
        list(SRC_DIR.rglob("*.tsx")) + list(SRC_DIR.rglob("*.ts")) + list(SRC_DIR.rglob("*.html"))
    )
    if INDEX_HTML.exists():
        files.append(INDEX_HTML)
    tok_re = re.compile(r"\b[a-z][a-z0-9_-]*(?:-[a-z0-9_]+)+\b")
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in tok_re.finditer(text):
            used.add(m.group(0))
        # dark/light are real helper classes (html.dark, :not(.dark))
        used.update(re.findall(r"\b(dark|light)\b", text))
        # template-literal classnames like tactile-chassis-${...} cannot be
        # captured as full tokens; register their static prefix as a keep-family.
        for m in re.finditer(r"([a-z][a-z0-9_-]*)-\$\{", text):
            TEMPLATE_PREFIXES.add(m.group(1) + "-")
    expanded: set[str] = set()
    for tok in list(used):
        parts = tok.split("-")
        for i in range(1, len(parts) + 1):
            expanded.add("-".join(parts[:i]))
    return used | expanded


def find_top_blocks(text: str) -> list[tuple[int, int]]:
    blocks: list[tuple[int, int]] = []
    start: int | None = None
    depth = 0
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            j = text.find("*/", i + 2)
            i = j + 2 if j != -1 else n
            continue
        if ch == "{":
            if start is None:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                blocks.append((start, i + 1))
                start = None
        i += 1
    return blocks


def css_prune(text: str, used: set[str]) -> str:
    kf_names = re.compile(r"@keyframes\s+([a-zA-Z0-9_-]+)")

    def used_animations(src: str) -> set[str]:
        pat = r"animation(?:-name)?:\s*([a-zA-Z0-9_-]+)"
        return set(re.findall(pat, src))

    def filter_pass(src: str) -> str:
        blocks = find_top_blocks(src)
        if not blocks:
            return src
        head = src[: blocks[0][0]]
        out = [head]
        prev = blocks[0][0]
        for bs, be in blocks:
            lead = src[prev:bs]
            body = src[bs + 1 : be - 1]

            kf = kf_names.search(lead)
            if kf:
                if kf.group(1) in anims:
                    out.append(lead)
                    out.append(src[bs:be])
                prev = be
                continue

            at_rule = re.search(r"@(?:media|layer|supports|container|scope|starting-style)\b", lead)
            if at_rule:
                inner = filter_pass(body)
                if inner.strip():
                    out.append(lead)
                    out.append("{" + inner + "}")
                prev = be
                continue

            clean = re.sub(r"/\*.*?\*/", "", lead, flags=re.DOTALL)
            classes = [c[1:] for c in re.findall(r"\.[a-zA-Z_][\w-]*", clean)]
            kept = not classes or all(
                c in used or any(c.startswith(p) for p in TEMPLATE_PREFIXES) for c in classes
            )
            if kept:
                out.append(lead)
                out.append(src[bs:be])
            else:
                dropped_selectors.append(", ".join(classes))
            prev = be
        return "".join(out).rstrip() + "\n"

    text_prev = None
    anims: set[str] = set()
    while text_prev != text:
        text_prev = text
        anims = used_animations(text)
        text = filter_pass(text)
    # strip empty containers left behind
    text = re.sub(
        r"@(?:media|layer|supports|container|scope|starting-style)[^{]*\{\s*\}\s*", "", text
    )
    return text


def prune_theme_tokens(text: str, used: set[str]) -> str:
    # Re-emit surviving @theme / :root var lines only.
    # gather all var() references surviving in the file
    refs = set(re.findall(r"var\((--[a-z0-9-]+)\)", text))

    lines = text.splitlines()
    out: list[str] = []
    drop_fonts = {"--font-mono", "--font-serif"}
    for ln in lines:
        m = re.match(r"\s*(--[\w-]+)\s*:", ln)
        if m:
            name = m.group(1)
            if name in drop_fonts:
                continue
            if name.startswith("--font-"):
                out.append(ln)
                continue
            if name.startswith("--color-"):
                if name in refs:
                    out.append(ln)
                continue
            if name in ROOT_VARS and name not in refs:
                continue
        out.append(ln)
    text = "\n".join(out)

    # collapse emptied blocks
    text = re.sub(r":root\s*\{\s*\}", "", text)
    text = re.sub(r"@theme\s*\{\s*\}", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply", action="store_true", help="write changes to disk (default: dry-run)"
    )
    args = parser.parse_args()
    apply = args.apply

    print(
        "P2 token confinement sweep — dry run"
        if not apply
        else "P2 token confinement sweep — applying"
    )

    changed_tsx, counts = tsx_remap(apply)
    if changed_tsx:
        print(f"\nTSX: {len(changed_tsx)} files changed")
        for p, c in sorted(counts.items()):
            print(f"  {p}: ~{c} token edits")

    changed_html = html_remap(apply)
    if changed_html:
        print("index.html: colour remap")

    css = CSS_PATH.read_text(encoding="utf-8")
    orig_lines = css.count("\n") + 1
    used = collect_used_classes()

    css2 = css_remap(css)
    css2 = css_prune(css2, used)
    css2 = prune_theme_tokens(css2, used)
    new_lines = css2.count("\n") + 1

    # top-level directives (@import / @layer ...;) must never be lost by pruning
    for directive in reversed(re.findall(r"^[ \t]*@(?:import|charset)[^{}]*;[ \t]*$", css, re.M)):
        if directive.strip() not in css2:
            css2 = directive + "\n" + css2

    print(f"\nCSS: {orig_lines} -> {new_lines} lines (delta {new_lines - orig_lines})")
    dropped = sorted(set(dropped_selectors))
    if dropped:
        print(f"  {len(dropped)} unreferenced class rules dropped:")
        for sel in dropped[:200]:
            print("    -", sel)
    if not apply:
        # show sample of what would change
        if audit_notes:
            print("\nAudit notes (manual review):")
            for n in audit_notes:
                print("  !", n)
        print("\nDry run complete — no files written. Re-run with --apply to commit.")
        return

    if css2 != css:
        CSS_PATH.write_text(css2, encoding="utf-8")
        print("CSS written.")
    else:
        print("CSS unchanged.")

    if audit_notes:
        print("\nAudit notes (manual review):")
        for n in audit_notes:
            print("  !", n)


if __name__ == "__main__":
    main()
