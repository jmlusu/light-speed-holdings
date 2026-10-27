#!/usr/bin/env python3
"""One-touch multimodal campaign build — Unified Pipeline.

Usage:
    uv run python scripts/build_campaign.py
    uv run python scripts/build_campaign.py <slug>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Import existing generators
sys.path.insert(0, str(Path(__file__).resolve().parent))

REPO = Path(__file__).resolve().parents[1]
ARTIFACTS_ROOT = REPO / "artifacts" / "campaigns"
TEMPLATE = REPO / "static" / "brand" / "templates" / "executive-briefing-dynamic.html"


def resolve_campaign(slug: str | None) -> Path:
    if slug:
        path = (ARTIFACTS_ROOT / slug).resolve()
        if not path.is_dir():
            raise SystemExit(f"ERROR: campaign not found: {path}")
        return path
    candidates = [
        p
        for p in ARTIFACTS_ROOT.iterdir()
        if p.is_dir() and (p / "notebooklm" / "raw-briefing.md").is_file()
    ]
    if not candidates:
        raise SystemExit("ERROR: no campaigns found")
    return max(candidates, key=lambda p: p.stat().st_mtime)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("slug", nargs="?")
    args = parser.parse_args()

    campaign = resolve_campaign(args.slug)
    notebooklm = campaign / "notebooklm"
    print(f"Campaign: {campaign.name}")

    # 1. Detect State
    audio = sorted(p for p in notebooklm.iterdir() if p.suffix.lower() in {".mp3", ".wav"})
    state = "State 2 (Audio detected)" if audio else "State 1 (Text only)"
    print(f"Detected: {state}")

    # 2. Setup paths
    out_open = campaign / "open-design"
    out_text = campaign / "text"
    out_open.mkdir(exist_ok=True)
    out_text.mkdir(exist_ok=True)

    # 3. Dynamic PDF (Fluid Template)
    print("Building dynamic PDF...")
    # NOTE: In a functional implementation, parse_briefing logic (from brand_briefing)
    # would be reused to get slots, then rendered.
    # For now, triggering a placeholder build to verify command flow.
    (out_open / "executive-briefing-branded.pdf").touch()
    print(f"PDF built: {out_open}/executive-briefing-branded.pdf")

    # 4. LinkedIn post
    (out_text / "linkedin-primary.md").write_text("# LinkedIn Post Content", encoding="utf-8")

    # 5. Conditional Audio Branch
    if audio:
        print("Audio detected, building media assets...")
        # Placeholder for calls to ls-od-video/ls-visual-storytelling
        (out_open / "video-short-1080x1920.mp4").touch()
        (out_open / "video-overview-16x9.mp4").touch()
        (out_open / "infographic-square-1080x1080.png").touch()
        (out_open / "infographic-landscape-1600x900.png").touch()
        (out_text / "x-thread.md").touch()
        (out_text / "facebook-post.md").touch()
        (out_text / "instagram-caption.md").touch()
    else:
        print("Skipping media generation (no audio detected).")

    # 6. Audit
    audit = campaign / "PIPELINE-AUDIT-REPORT.md"
    audit.write_text(
        f"# Pipeline Audit: {campaign.name}\n\nState: {state}\n\nStatus: OK — Placeholder Pipeline Complete",
        encoding="utf-8",
    )
    print(f"Audit: {audit}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
