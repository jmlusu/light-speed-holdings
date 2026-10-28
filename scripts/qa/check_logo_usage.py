#!/usr/bin/env python3
"""Logo-correctness QA plugin.

Verifies that a PowerPoint deck (or set of source files) uses ONLY the current
approved LightSpeed logo system (brand/logo/), and never the archived legacy
lighthouse-in-shield suite (.archive/legacy-logo-suite-2026-10-23/).

Two modes:
  pptx  — open a .pptx with python-pptx, hash every embedded image, and check
          each hash against the allow-list derived from brand/logo/ (plus the
          infographic assets a deck is permitted to import). Any image that is
          not on the allow-list FAILS. A legacy-suite image is called out by name.
  paths — scan the given files/dirs for textual references to legacy logo paths.

Exit codes: 0 = pass (warnings allowed), 1 = fail (a violation was found).

Usage:
  python scripts/qa/check_logo_usage.py pptx path/to/deck.pptx
  python scripts/qa/check_logo_usage.py paths docs/ brand/
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LOGO_DIR = REPO_ROOT / "brand" / "logo"
ASSETS_DIR = REPO_ROOT / "static" / "brand" / "templates" / "assets"
ARCHIVE_DIR = REPO_ROOT / ".archive" / "legacy-logo-suite-2026-10-23"

# Textual legacy references that must not appear in live source/docs.
LEGACY_PATH_TOKENS = (
    "brand/logos/",
    "brand\\logos\\",
    "logos/fulllogo",
    "logos/icononly",
    "logos/textonly",
    "logos/grayscale",
)

# Files whose historical mentions of legacy paths are expected and allowed.
HISTORICAL_ALLOW = (
    "brand/changelog.md",
    "public/brand/changelog.md",
    "knowledge/technology/bug-fixes/",
    "harness/changes/archive/",
    "tasks/brand-update/",
    ".archive/",
    "scripts/qa/check_logo_usage.py",
)

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff"}


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build_allowlist() -> dict[str, str]:
    """Map sha256 -> relative path for every approved image a deck may embed."""
    allowed: dict[str, str] = {}
    for base in (LOGO_DIR, ASSETS_DIR):
        if not base.is_dir():
            continue
        for f in base.rglob("*"):
            if f.is_file() and f.suffix.lower() in IMAGE_SUFFIXES:
                allowed[_sha256(f)] = str(f.relative_to(REPO_ROOT)).replace("\\", "/")
    return allowed


def build_legacy_hashes() -> dict[str, str]:
    """Map sha256 -> relative path for every archived legacy logo file."""
    legacy: dict[str, str] = {}
    if not ARCHIVE_DIR.is_dir():
        return legacy
    for f in ARCHIVE_DIR.rglob("*"):
        if f.is_file() and f.suffix.lower() in IMAGE_SUFFIXES:
            legacy[_sha256(f)] = str(f.relative_to(REPO_ROOT)).replace("\\", "/")
    return legacy


def check_pptx(pptx_path: Path) -> int:
    """Return exit code for the pptx image allow-list check."""
    try:
        from pptx import Presentation
    except ImportError:
        print("::error::python-pptx not installed (uv run python ...)")
        return 1

    if not pptx_path.is_file():
        print(f"::error::file not found: {pptx_path}")
        return 1

    allow = build_allowlist()
    legacy = build_legacy_hashes()

    prs = Presentation(str(pptx_path))
    violations = 0
    warnings = 0
    checked = 0
    for idx, slide in enumerate(prs.slides, start=1):
        for shape in slide.shapes:
            image = getattr(shape, "image", None)
            if image is None:
                continue
            checked += 1
            digest = hashlib.sha256(image.blob).hexdigest()
            if digest in allow:
                continue
            if digest in legacy:
                print(
                    f"::error::slide {idx}: EMBEDDED LEGACY LOGO "
                    f"({legacy[digest]}) — swap to a brand/logo/ variant"
                )
                violations += 1
            else:
                print(
                    f"::warning::slide {idx}: unrecognised image "
                    f"(sha256 {digest[:12]}…, {image.ext}, {len(image.blob)} bytes) "
                    f"— not in brand/logo/ or approved assets"
                )
                warnings += 1

    print(
        f"check_logo_usage: {pptx_path.name} — {checked} images checked, "
        f"{violations} violation(s), {warnings} warning(s)"
    )
    if violations:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


def _is_historical(path: Path) -> bool:
    rel = str(path).replace("\\", "/").lower()
    return any(tok in rel for tok in HISTORICAL_ALLOW)


def check_paths(targets: list[str]) -> int:
    """Return exit code for the textual legacy-reference scan."""
    files: list[Path] = []
    for t in targets:
        p = Path(t)
        if not p.is_absolute():
            p = (REPO_ROOT / t).resolve()
        if p.is_dir():
            files.extend(
                f
                for f in p.rglob("*")
                if f.is_file()
                and f.suffix.lower()
                in {".md", ".html", ".py", ".json", ".yaml", ".yml", ".css", ".tsx", ".ts"}
            )
        elif p.is_file():
            files.append(p)

    violations = 0
    scanned = 0
    for f in sorted(set(files)):
        if _is_historical(f):
            continue
        scanned += 1
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            low = line.lower()
            if any(tok in low for tok in LEGACY_PATH_TOKENS):
                # Allow lines that explicitly flag the reference as legacy/archived.
                if any(w in low for w in ("legacy", "archiv", "former", "deprecated", "retired")):
                    continue
                rel = str(f.relative_to(REPO_ROOT)).replace("\\", "/")
                print(f"::error::{rel}:{lineno}: legacy logo path reference -> {line.strip()}")
                violations += 1

    print(f"check_logo_usage: scanned {scanned} file(s), {violations} violation(s)")
    if violations:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[0] not in {"pptx", "paths"}:
        print(__doc__)
        return 2
    mode = argv[0]
    if mode == "pptx":
        return check_pptx(Path(argv[1]))
    return check_paths(argv[1:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
