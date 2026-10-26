"""Render a deck to per-slide images and write an ls-artifact-qa verdict.

Two subcommands, deliberately split so that a verdict can never exist without
renders of the exact build it describes:

    render-verdict.py render <deck> [--out DIR]
    render-verdict.py verdict <deck> --reviewed-by <id> \
        --pass visual=PASS --pass brand=PASS --pass ux=PASS \
        --pass accessibility=PASS --pass content=PASS \
        [--note visual="..."] [--out FILE]

``render`` writes one PNG per slide plus ``manifest.json`` into ``<deck>.renders/``;
the manifest records the deck's sha256. ``verdict`` refuses to run unless the
manifest still matches the deck's current bytes, so a verdict cannot be bound to a
stale build. Neither command edits the deck, and neither can be used to skip the
review: ``verdict`` requires the five ls-artifact-qa passes as explicit arguments.

This exists because AGENTS.md forbids hand-writing ``<deck>.qa-verdict.json``: the
verdict is evidence, and evidence that can be typed is not evidence.

Exit codes: 0 success, 1 usage/verification error, 2 refused (stale or missing renders).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "qa-verdict.schema.json"

PASSES = ("visual", "brand", "ux", "accessibility", "content")
TARGET_WIDTH_PX = 1280
MIN_WIDTH_PX = 640
SOFFICE_CANDIDATES = (
    os.environ.get("SOFFICE"),
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    "/usr/bin/soffice",
    "/usr/local/bin/soffice",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
)


class Refused(Exception):
    """A precondition for producing trustworthy evidence failed."""


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def renders_dir_for(deck: Path) -> Path:
    """`pitch-deck.pptx` -> `pitch-deck.renders/`, a sibling of the deck."""
    return Path(str(deck.with_suffix("")) + ".renders")


def find_soffice() -> Path | None:
    for candidate in SOFFICE_CANDIDATES:
        if candidate and Path(candidate).is_file():
            return Path(candidate)
    found = shutil.which("soffice") or shutil.which("libreoffice")
    return Path(found) if found else None


def load_manifest(renders_dir: Path) -> dict:
    manifest_path = renders_dir / "manifest.json"
    if not manifest_path.is_file():
        raise Refused(f"no render manifest at {manifest_path}; run `render` first")
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise Refused(f"cannot read {manifest_path}: {e}") from e


def image_width(path: Path) -> int:
    from PIL import Image

    with Image.open(path) as img:
        return img.size[0]


TOKEN_RE = None


def _tokens(text: str):
    """Case-folded alphanumeric token multiset, for comparing a slide with its render."""
    global TOKEN_RE
    if TOKEN_RE is None:
        import re

        TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)
    from collections import Counter

    return Counter(t.casefold() for t in TOKEN_RE.findall(text.replace("\u00a0", " ")))


def _deck_page_texts(deck: Path) -> list[str]:
    from pptx import Presentation

    prs = Presentation(str(deck))
    return [
        "\n".join(
            shape.text_frame.text
            for shape in slide.shapes
            if shape.has_text_frame and shape.text_frame.text.strip()
        )
        for slide in prs.slides
    ]


def _assert_pdf_matches_deck(pdf_pages: list[str], deck_pages: list[str]) -> None:
    """Refuse to publish renders whose text does not match the deck slide-for-slide.

    LibreOffice occasionally emits a page twice-laid-out (autofit text drawn at two
    sizes). That has been observed on this machine, so the PDF is checked before any
    image is committed as evidence: a duplicated or truncated page fails here rather
    than being reviewed as if it were the artifact.
    """
    if len(pdf_pages) != len(deck_pages):
        raise Refused(
            f"render has {len(pdf_pages)} pages but the deck has {len(deck_pages)} slides"
        )
    for index, (pdf_text, deck_text) in enumerate(
        zip(pdf_pages, deck_pages, strict=True), start=1
    ):
        pdf_tokens, deck_tokens = _tokens(pdf_text), _tokens(deck_text)
        if pdf_tokens == deck_tokens:
            continue
        missing = {k: v for k, v in deck_tokens.items() if pdf_tokens.get(k, 0) < v}
        extra = {k: v for k, v in pdf_tokens.items() if deck_tokens.get(k, 0) < v}
        raise Refused(
            f"rendered slide {index} does not match the deck's text "
            f"(deck {sum(deck_tokens.values())} tokens, render {sum(pdf_tokens.values())}); "
            f"missing={dict(list(missing.items())[:6])} extra={dict(list(extra.items())[:6])}. "
            "Re-run `render`; do not issue a verdict against this output."
        )


def cmd_render(args: argparse.Namespace) -> int:
    import pymupdf

    deck = Path(args.deck).resolve()
    if not deck.is_file():
        raise Refused(f"deck not found: {deck}")

    soffice = find_soffice()
    if soffice is None:
        raise Refused(
            "LibreOffice (soffice) not found; set SOFFICE to its path. "
            "Rendering is required before a verdict can be issued."
        )

    out_dir = Path(args.out).resolve() if args.out else renders_dir_for(deck)
    out_dir.mkdir(parents=True, exist_ok=True)

    deck_sha = sha256_file(deck)
    with tempfile.TemporaryDirectory(prefix="deck-render-") as tmp:
        tmp_dir = Path(tmp)
        profile = tmp_dir / "lo-profile"
        cmd = [
            str(soffice),
            f"-env:UserInstallation={profile.as_uri()}",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(tmp_dir),
            str(deck),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        pdf_path = tmp_dir / (deck.stem + ".pdf")
        if proc.returncode != 0 or not pdf_path.is_file():
            raise Refused(
                "LibreOffice conversion failed "
                f"(exit {proc.returncode}): {(proc.stderr or proc.stdout).strip()[:400]}"
            )

        doc = pymupdf.open(pdf_path)
        try:
            # Check the converted pages against the deck BEFORE any image becomes
            # evidence. A corrupt conversion must never be reviewable.
            _assert_pdf_matches_deck(
                [page.get_text() for page in doc], _deck_page_texts(deck)
            )

            # Only ever remove this tool's own outputs, and only once a good
            # conversion exists; a refused render leaves the previous set intact.
            for stale in [*out_dir.glob("slide-*.png"), out_dir / "manifest.json"]:
                if stale.is_file():
                    stale.unlink()

            pages = []
            for index, page in enumerate(doc, start=1):
                zoom = TARGET_WIDTH_PX / page.rect.width
                pixmap = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
                name = f"slide-{index:02d}.png"
                png_path = out_dir / name
                pixmap.save(png_path)
                pages.append(
                    {
                        "index": index,
                        "path": name,
                        "sha256": sha256_file(png_path),
                        "width_px": pixmap.width,
                        "height_px": pixmap.height,
                    }
                )
        finally:
            doc.close()

    manifest = {
        "schema_version": 1,
        "deck": {"path": _display_path(deck), "sha256": deck_sha},
        "rendered_on": args.today or _today(),
        "renderer": f"render-verdict.py:libreoffice+pymupdf (target width {TARGET_WIDTH_PX}px)",
        "slide_count": len(pages),
        "pages": pages,
    }
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"deck      {_display_path(deck)}")
    print(f"sha256    {deck_sha}")
    print(f"slides    {len(pages)}")
    for page in pages:
        print(f"  {page['path']}  {page['width_px']}x{page['height_px']}px")
    print(f"manifest  {_display_path(manifest_path)}")
    return 0


def cmd_verdict(args: argparse.Namespace) -> int:
    deck = Path(args.deck).resolve()
    if not deck.is_file():
        raise Refused(f"deck not found: {deck}")

    renders_dir = (
        Path(args.renders).resolve() if args.renders else renders_dir_for(deck)
    )
    manifest = load_manifest(renders_dir)

    deck_sha = sha256_file(deck)
    rendered_sha = (manifest.get("deck") or {}).get("sha256")
    if rendered_sha != deck_sha:
        raise Refused(
            "renders are stale: they were made from a different build "
            f"(rendered {rendered_sha}, deck {deck_sha}). Re-run `render`."
        )

    results: dict[str, str] = {}
    for item in args.pass_ or []:
        name, _, value = item.partition("=")
        name, value = name.strip().lower(), value.strip().upper()
        if name not in PASSES:
            raise Refused(f"unknown pass '{name}'; expected one of {', '.join(PASSES)}")
        if value not in ("PASS", "FAIL"):
            raise Refused(f"pass '{name}' must be PASS or FAIL, got '{value}'")
        if name in results:
            raise Refused(f"pass '{name}' given twice")
        results[name] = value

    missing = [p for p in PASSES if p not in results]
    if missing:
        raise Refused(
            "the verdict must record all five ls-artifact-qa passes; missing: "
            + ", ".join(missing)
        )

    notes: dict[str, str] = {}
    for item in args.note or []:
        name, _, text = item.partition("=")
        name = name.strip().lower()
        if name not in PASSES:
            raise Refused(f"--note for unknown pass '{name}'")
        notes[name] = text.strip()

    out_path = Path(args.out).resolve() if args.out else deck.with_suffix(".qa-verdict.json")

    slides = manifest.get("slide_count") or len(manifest.get("pages") or [])
    evidence = []
    for page in manifest.get("pages") or []:
        png = renders_dir / page["path"]
        if not png.is_file():
            raise Refused(f"render missing: {png}")
        if sha256_file(png) != page.get("sha256"):
            raise Refused(f"render changed after it was made: {png}")
        width = image_width(png)
        if width < MIN_WIDTH_PX:
            raise Refused(f"render too small to inspect ({width}px): {png}")
        # verify-deck.py resolves evidence relative to the verdict file, so record
        # the path from there (e.g. pitch-deck.renders/slide-01.png), not from cwd.
        evidence.append(
            {"path": _evidence_path(png, out_path.parent), "sha256": page["sha256"]}
        )
    if len(evidence) < slides or slides == 0:
        raise Refused(
            f"need one render per slide: manifest says {slides}, found {len(evidence)}"
        )

    verdict = "APPROVE" if all(v == "PASS" for v in results.values()) else "FIX"
    payload = {
        "schema_version": 1,
        "verdict": verdict,
        "generated_by": f"scripts/deck-gate/render-verdict.py; reviewed_by {args.reviewed_by}",
        "artifact": {"path": _display_path(deck), "sha256": deck_sha},
        "checks": [
            {"pass": name, "result": results[name], **({"notes": notes[name]} if name in notes else {})}
            for name in PASSES
        ],
        "evidence": evidence,
    }

    _validate(payload)

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"verdict   {verdict}  ({len(evidence)} renders, deck {deck_sha[:16]}...)")
    for name in PASSES:
        print(f"  {name:14} {results[name]}")
    print(f"written   {_display_path(out_path)}")
    return 0 if verdict == "APPROVE" else 1


def _validate(payload: dict) -> None:
    if not SCHEMA_PATH.is_file():
        raise Refused(f"schema not found: {SCHEMA_PATH}")
    import jsonschema

    try:
        jsonschema.validate(payload, json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))
    except jsonschema.ValidationError as e:
        raise Refused(f"verdict does not satisfy {SCHEMA_PATH.name}: {e.message}") from e


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def _evidence_path(png: Path, verdict_dir: Path) -> str:
    """Path from the verdict file to the render, which is how the gate resolves it."""
    try:
        return Path(os.path.relpath(png, verdict_dir)).as_posix()
    except ValueError:  # different drives on Windows: relpath is impossible
        return str(png)


def _today() -> str:
    import datetime as dt

    return dt.date.today().isoformat()


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="render-verdict.py",
        description="Render a deck and issue an ls-artifact-qa verdict bound to its sha256.",
    )
    sub = ap.add_subparsers(dest="command", required=True)

    render = sub.add_parser("render", help="render one PNG per slide plus manifest.json")
    render.add_argument("deck")
    render.add_argument("--out", help="output directory (default: <deck>.renders)")
    render.add_argument("--today", help="ISO date to record (default: today)")
    render.set_defaults(func=cmd_render)

    verdict = sub.add_parser("verdict", help="write <deck>.qa-verdict.json from the renders")
    verdict.add_argument("deck")
    verdict.add_argument(
        "--reviewed-by",
        required=True,
        help="who reviewed the renders, e.g. human:jack.mlusu or agent:opencode",
    )
    verdict.add_argument(
        "--pass",
        dest="pass_",
        action="append",
        metavar="PASS=RESULT",
        help="one of visual|brand|ux|accessibility|content = PASS|FAIL (all five required)",
    )
    verdict.add_argument(
        "--note",
        action="append",
        metavar="PASS=TEXT",
        help="optional note attached to that pass",
    )
    verdict.add_argument("--renders", help="renders directory (default: <deck>.renders)")
    verdict.add_argument("--out", help="verdict path (default: <deck>.qa-verdict.json)")
    verdict.set_defaults(func=cmd_verdict)
    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except Refused as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
