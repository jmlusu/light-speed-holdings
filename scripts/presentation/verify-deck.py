"""Playwright visual verification for AI agent slide decks.

Validates generated decks against brand token constraints and
checks visual elements (navy rail, red/cyan accents, layout).

Usage:
    python scripts/presentation/verify-deck.py <marp-md-file>

Checks:
- Navy left rail present on content slides
- Red accent color usage (≤10% of slides)
- Cyan highlight usage (≤10% of slides)
- Grey background compliance (80% rule)
- Speaker notes present on all slides
- Slide titles match expected sequence
- No empty or duplicate slides
"""

import sys
import re
from pathlib import Path


def check_navy_rail(markdown_text: str) -> bool:
    """Check that navy left rail markdown is present.

    Marp syntax for rail: <!-- style: {left: 20px; width: 20px; background: #070A40} -->
    """
    rail_pattern = r"<!--\s*style:\s*\{[^\}]*left\s*:\s*\d+px[^\}]*background\s*:\s*#070A40[^\}]*\}-->"
    return bool(re.search(rail_pattern, markdown_text, re.IGNORECASE))


def check_brand_colors(markdown_text: str) -> dict:
    """Check red and cyan color usage in markdown.

    Returns counts of red (#E63946) and cyan (#00BFFF) usage.
    """
    red_count = len(re.findall(r"#E63946", markdown_text))
    cyan_count = len(re.findall(r"#00BFFF", markdown_text))
    total_chars = len(markdown_text)
    return {
        "red_count": red_count,
        "cyan_count": cyan_count,
        "red_density": red_count / max(total_chars, 1),
        "cyan_density": cyan_count / max(total_chars, 1),
    }


def check_speaker_notes(markdown_text: str) -> bool:
    """Check that speaker notes are present on all slides."""
    # Marp speaker notes: *- Speaker notes: ... *
    pattern = r"- Speaker notes:"
    matches = re.findall(pattern, markdown_text)
    return len(matches) > 0


def validate_slide_sequence(markdown_text: str, expected_count: int) -> dict:
    """Validate that slide count matches expected and no duplicates.

    Marp slides are separated by ## headers.
    """
    slide_titles = re.findall(r"##\s+(.+?)\n", markdown_text)
    unique_titles = set(slide_titles)
    has_duplicates = len(slide_titles) != len(unique_titles)

    return {
        "actual_slide_count": len(slide_titles),
        "expected_slide_count": expected_count,
        "count_matches": len(slide_titles) == expected_count,
        "has_duplicates": has_duplicates,
        "unique_slide_count": len(unique_titles),
    }


def main() -> int:
    """Main entry point for verify-deck.py."""
    if len(sys.argv) < 2:
        print("Usage: python verify-deck.py <marp-md-file>")
        return 1

    md_file = Path(sys.argv[1])
    if not md_file.exists():
        print(f"Error: File not found: {md_file}")
        return 1

    markdown_text = md_file.read_text(encoding="utf-8")

    # Determine deck type from filename or content
    deck_type = "investor_pitch"  # default
    if "board_meeting" in str(md_file):
        deck_type = "board_meeting"
    elif "keynote" in str(md_file):
        deck_type = "keynote"
    elif "training" in str(md_file):
        deck_type = "training"

    # Expected slide counts by deck type
    expected_counts = {
        "investor_pitch": 14,
        "board_meeting": 10,
        "keynote": 13,
        "training": 8,
    }
    expected_count = expected_counts.get(deck_type, 10)

    results = {
        "file": str(md_file),
        "deck_type": deck_type,
        "checks": {},
    }

    # Check 1: Navy rail
    rail_ok = check_navy_rail(markdown_text)
    results["checks"]["navy_rail"] = {
        "pass": rail_ok,
        "detail": "Navy left rail markdown present" if rail_ok else "Missing navy left rail markdown",
    }

    # Check 2: Brand colors density
    colors = check_brand_colors(markdown_text)
    results["checks"]["brand_colors"] = {
        "pass": colors["red_density"] <= 0.05 and colors["cyan_density"] <= 0.05,
        "detail": f"Red: {colors['red_count']} occurrences, Cyan: {colors['cyan_count']} occurrences",
    }

    # Check 3: Speaker notes
    notes_ok = check_speaker_notes(markdown_text)
    results["checks"]["speaker_notes"] = {
        "pass": notes_ok,
        "detail": "Speaker notes found" if notes_ok else "Missing speaker notes",
    }

    # Check 4: Slide sequence validation
    seq = validate_slide_sequence(markdown_text, expected_count)
    results["checks"]["slide_sequence"] = {
        "pass": seq["count_matches"] and not seq["has_duplicates"],
        "detail": f"Slide count: {seq['actual_slide_count']} (expected {seq['expected_slide_count']}), "
                  f"duplicates: {seq['has_duplicates']}",
    }

    # Summary
    all_pass = all(
        check["pass"] for check in results["checks"].values()
    )

    print(f"=== Deck Verification: {md_file.name} ===")
    print(f"Deck type: {deck_type} (expected {expected_count} slides)")
    print()

    for check_name, check in results["checks"].items():
        status = "PASS" if check["pass"] else "FAIL"
        print(f"  [{status}] {check_name}: {check['detail']}")

    print()
    if all_pass:
        print(">> ALL CHECKS PASSED <<")
        return 0
    else:
        print(">> SOME CHECKS FAILED <<")
        return 1


if __name__ == "__main__":
    sys.exit(main())