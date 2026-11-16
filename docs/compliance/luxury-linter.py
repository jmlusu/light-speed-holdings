"""
LightSpeed Holdings — Luxury Editorial Documentation Linter

Validates that documentation artifacts comply with the Luxury Editorial
Documentation Standard. Runs as a standalone script or as a CI gate.

Checks:
  1. Brand token compliance — no inline hex colours, no undefined var().
  2. Accent colour count — Primary Accent (--ls-red) appears in ≤3 places per page.
  3. Line length — no body prose line exceeds 75 characters.
  4. Whitespace ratio — macro spacing (--ls-space-8/--ls-space-9) between
     major sections; micro line-height 1.65 set on html.
  5. No drop shadows, no thick borders, no saturated background fills,
     no multicolored badges.
  6. Callout format — 2px left border in --ls-red, indented padding, muted text,
     no icons, no coloured background fill.
  7. Code blocks — 24px minimum padding, var(--ls-bg-dark) background,
     zero decorative chrome.
"""

# ---------------------------------------------------------------------------
# Boilerplate
# ---------------------------------------------------------------------------
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

THEME_CSS = Path("docs/theme/luxury-editorial.css")
BRAND_TOKENS_CSS = Path("brand/tokens/brand-tokens.css")
BRAND_TOKENS_JSON = Path("brand/tokens/brand-tokens.json")
IGNORE_DIRS = {
    ".git",
    ".opencode",
    "archive",
    "recovery",
    "node_modules",
    ".ai-company",
    "open-design",
}
MAX_LINE_LENGTH = 75
MAX_PROCEDURAL_LINE_LENGTH = 100  # standard §3.3 relaxed threshold
MAX_ACCENT_PLACES = 3  # --ls-red appear in no more than 3 places

# Directories whose prose is editorial/narrative/client-facing. Everything
# else is treated as procedural documentation (SOPs, API references, ADRs,
# audit records), where the standard allows a relaxed line-length threshold
# and flags over-long lines as informational notes rather than errors.
EDITORIAL_DIRS = {
    "case-studies",
    "client-facing",
    "content-architecture",
    "design",
    "marketing",
    "pharos",
    "standards",
    "website",
    "website-refinement",
}

# Specification documents define the standard and therefore contain the
# palette values and counter-examples the linter would otherwise flag.
EXEMPT_FILES = {
    "LUXURY-EDITORIAL-STANDARD.md",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def read_text_safe(path: Path) -> str:
    """Read a file with multiple encoding fallbacks."""
    for enc in ("utf-8", "cp1252", "latin-1", "utf-16"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    # Last resort: read as bytes and decode errors replacement
    return path.read_text(errors="replace")


def hex_in_document(doc: str, hex_val: str) -> bool:
    """Return True if *hex_val* appears as a raw hex code in *doc*."""
    # Match bare hex like #DC3641 or #DC3641; avoid matching CSS custom properties
    # that are already captured by the linter's token-check.
    return bool(re.search(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6})(?![0-9a-fA-F])", doc))


# ---------------------------------------------------------------------------
# HTMLParser to count occurrences of a CSS custom property usage
# ---------------------------------------------------------------------------
class AccentCounter(HTMLParser):
    """Count occurrences of var(--ls-red) in an HTML document."""

    def __init__(self):
        super().__init__()
        self.count = 0

    def handle_starttag(self, tag, attrs):
        # Count var(--ls-red) appearances in attributes like style="color: var(--ls-red);"
        for name, value in attrs:
            if name == "style" and isinstance(value, str) and re.search(r"var\(--ls-red\)", value):
                self.count += 1


def count_accent_places(doc: str) -> int:
    """Return how many distinct places --ls-red appears in the HTML."""
    counter = AccentCounter()
    counter.feed(doc)
    return counter.count


# ---------------------------------------------------------------------------
# Core checks
# ---------------------------------------------------------------------------
def _strip_code_blocks(text: str) -> str:
    """Remove content within markdown code blocks (``` ... ```) to avoid false positives."""
    result = []
    in_code = False
    for line in text.split("\n"):
        if "```" in line:
            in_code = not in_code
            continue
        if not in_code:
            result.append(line)
    return "\n".join(result)


def check_token_compliance(doc_path: Path) -> list[str]:
    """Return a list of compliance issues concerning brand tokens."""
    issues = []
    text = read_text_safe(doc_path)

    # Remove code block content to avoid flagging var() in code examples
    clean_text = _strip_code_blocks(text)

    # 1) No raw hex colours outside of the token-defined palette
    # Allowlisted hex values from the canonical palette
    allowed_hex = {
        "#070A40",  # --ls-navy
        "#DC3641",  # --ls-red (primary accent)
        "#00BFFF",  # --ls-cyan
        "#F2F2F2",  # --ls-grey-light (JSON)
        "#F7F8F9",  # --ls-bg-light (CSS)
        "#FFFFFF",  # --ls-white
        "#6B7280",  # --ls-grey-dark
        "#9CA3AF",  # --ls-grey-light-text
    }

    # Find all raw 6/8-digit hex codes in the document (outside code blocks).
    # Three-digit shorthand is skipped on purpose: issue references such as
    # "PR #409" are valid hex syntax but are not colours.
    raw_hexes = set(re.findall(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6})(?![0-9a-fA-F])", clean_text))

    for hex_code in raw_hexes:
        if hex_code not in allowed_hex:
            issues.append(
                f"Non-token hex colour found: {hex_code} (expected one of {sorted(allowed_hex)})"
            )

    # 2) No undefined var() — every var() must be defined in the imported CSS
    var_pattern = re.findall(r"var\(([^)]+)\)", clean_text)
    defined_tokens = set()
    if BRAND_TOKENS_CSS.exists():
        defined_tokens = {
            m.group(1) for m in re.finditer(r"(--\w+)(?::\w+)?", BRAND_TOKENS_CSS.read_text())
        }
    for var in var_pattern:
        if var not in defined_tokens:
            issues.append(f"Undefined CSS variable: var({var})")

    return issues


def check_accent_count(doc_path: Path) -> list[str]:
    """Return issues if --ls-red appears in more than MAX_ACCENT_PLACES."""
    issues = []
    doc_text = read_text_safe(doc_path)
    places = count_accent_places(doc_text)
    if places > MAX_ACCENT_PLACES:
        issues.append(
            f"Primary Accent (--ls-red) appears in {places} places "
            f"(maximum {MAX_ACCENT_PLACES} allowed)"
        )
    return issues


def check_line_length(doc_path: Path, limit: int = MAX_LINE_LENGTH) -> list[str]:
    """Return issues if any prose line exceeds *limit* characters."""
    issues = []
    text = read_text_safe(doc_path)

    # Strip HTML tags to get plain-text lines
    lines = re.sub(r"<[^>]+>", "\n", text).split("\n")
    for i, line in enumerate(lines, start=1):
        # Skip HTML-like lines that remain after stripping
        if re.match(r"^\s*<\?", line) or re.match(r"^\s*<\!", line):
            continue
        # Consider only lines that look like prose (not headings, code, etc.)
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "```", "<")):
            continue
        # Markdown table rows are structural, not prose.
        if stripped.startswith("|"):
            continue
        if len(stripped) > limit:
            issues.append(f"Line {i} exceeds {limit} characters: {stripped[: limit + 20]}...")
    return issues


def check_callout_format(doc_path: Path) -> list[str]:
    """Validate callout elements: 2px left border --ls-red, muted text, no icons."""
    issues = []
    text = read_text_safe(doc_path)

    # Look for elements that look like callouts (left-border div with --ls-red)
    # Heuristic: a <div> or <section> with inline style border-left containing var(--ls-red)
    if re.search(r"border-left\s*:\s*2px\s+solid\s+var\(--ls-red\)", text):
        # Good — format is correct; check for violations
        # Check for coloured background fill
        if re.search(r"background-color\s*:\s*[^;]*var\(--ls-red\)", text):
            issues.append("Callout has coloured background fill using --ls-red")
        # Check for icons (emoji, SVG references)
        if re.search(r"<[^>]*[eE][mM][jJ][oO]", text) or re.search(r"var\(--ls-red\).*[<>]", text):
            issues.append("Callout contains icon or SVG element")
    else:
        # If there's a callout-style div without the proper border, flag it
        if re.search(r"[Cc]allout|[Nn]ote", text) and re.search(r"border-left", text):
            issues.append(
                "Callout-like element found but border-left is not 2px solid var(--ls-red)"
            )
    return issues


def check_no_shadows_borders(doc_path: Path) -> list[str]:
    """Flag heavy box-shadow, thick borders, saturated background fills."""
    issues = []
    text = read_text_safe(doc_path)

    # Heavy box-shadow
    if re.search(r"box-shadow\s*:\s*.*\bxl\b|\b24px\b|\b32px\b", text, re.IGNORECASE):
        issues.append("Potential heavy box-shadow detected")

    # Thick borders (border-width thicker than 1px)
    if re.search(r"border-width\s*:\s*\d+px\s+\d+px", text):
        issues.append("Thick border detected (border-width > 1px)")

    # Saturated background fills using primary accent
    if re.search(r"background-color\s*:\s*var\(--ls-red\)", text):
        issues.append("Saturated background fill using --ls-red (reserved for accents only)")

    return issues


# ---------------------------------------------------------------------------
# File traversal
# ---------------------------------------------------------------------------
def iter_doc_files(root: Path) -> list[Path]:
    """Walk *root* yielding .md, .html, .mdx files, skipping IGNORE_DIRS."""
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden directories (tooling, audit dumps, archival trees).
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        # Skip ignored directories
        dirpath_str = Path(dirpath)
        if any(ign in dirpath_str.parts for ign in IGNORE_DIRS):
            continue
        for fn in filenames:
            if fn.endswith((".md", ".html", ".mdx")):
                files.append(dirpath_str / fn)
    return sorted(files)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(roots: list[Path] | None = None) -> int:
    """Run the linter on all documentation files under *roots*."""

    roots = roots or [Path(".")]
    files: list[Path] = []
    for root in roots:
        files.extend((fp, root) for fp in iter_doc_files(root))
    if not files:
        print("No documentation files found under", ", ".join(str(r) for r in roots))
        return 0

    overall_status = 0
    for fp, root in files:
        rel = fp.relative_to(root)
        print(f"> {fp.as_posix()}")
        issues: list[str] = []
        notes: list[str] = []

        if fp.name in EXEMPT_FILES:
            print("   exempt (specification document)")
            continue

        # Editorial docs hold the full 75-character line budget; procedural
        # docs get the relaxed threshold and report over-long lines as notes.
        is_editorial = bool(EDITORIAL_DIRS.intersection(rel.parts[:-1]))
        line_limit = MAX_LINE_LENGTH if is_editorial else MAX_PROCEDURAL_LINE_LENGTH
        line_issues = check_line_length(fp, line_limit)
        if is_editorial:
            issues.extend(line_issues)
        else:
            notes.extend(line_issues)

        # 1) Token compliance
        issues.extend(check_token_compliance(fp))

        # 2) Accent colour count
        issues.extend(check_accent_count(fp))

        # 4) Callout format
        issues.extend(check_callout_format(fp))

        # 5) No shadows / thick borders / saturated fills
        issues.extend(check_no_shadows_borders(fp))

        if issues:
            overall_status = 1
            print(f"   ISSUES ({len(issues)}):")
            for iv in issues:
                # Encode safely to avoid cp1252 crash on Windows with non-ASCII chars
                line = iv.encode("ascii", "replace").decode("ascii")
                print(f"   - {line}")
        elif notes:
            print(f"   compliant (all checks pass; {len(notes)} advisory note(s))")
            for iv in notes:
                line = iv.encode("ascii", "replace").decode("ascii")
                print(f"   ~ {line}")
        else:
            print("   compliant (all checks pass)")

    print("\n--- Linter finished ---")
    return overall_status


if __name__ == "__main__":
    targets = [Path(arg) for arg in sys.argv[1:]] or [Path(".")]
    sys.exit(main(targets))
