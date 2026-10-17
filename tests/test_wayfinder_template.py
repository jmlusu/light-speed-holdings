"""Test wayfinder map template structure validation."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

TEMPLATE_FILE = ".agents/skills/wayfinder/map_template.md"


def test_wayfinder_map_template_has_required_sections() -> None:
    """Validate the wayfinder map template has all required sections."""
    with open(REPO_ROOT / TEMPLATE_FILE, encoding="utf-8") as f:
        content = f.read()

    checks = {
        "has_destination": bool(re.search(r"## Destination", content)),
        "has_notes": bool(re.search(r"## Notes", content)),
        "has_decisions_so_far": bool(re.search(r"Decisions so far", content)),
        "has_not_yet_specified": bool(re.search(r"Not yet specified", content)),
        "has_out_of_scope": bool(re.search(r"Out of scope", content)),
        "has_scraper_sources": bool(re.search(r"Scraper Sources", content)),
        "has_data_quality_gaps": bool(re.search(r"Data Quality Gaps", content)),
        "has_integration_points": bool(re.search(r"Integration Points", content)),
    }

    # All checks must pass
    for check_name, result in checks.items():
        assert result, f"Missing: {check_name}"


def test_wayfinder_map_template_has_front_matter() -> None:
    """Validate front matter: labels and introductory text."""
    with open(REPO_ROOT / TEMPLATE_FILE, encoding="utf-8") as f:
        content = f.read()

    checks = {
        "has_wayfinder_map_label": bool(re.search(r"wayfinder:map", content)),
        "has_destination_label_text": bool(re.search(r"Labels:", content)),
        "has_destination_section": bool(re.search(r"Destination", content)),
        "has_notes_section": bool(re.search(r"Notes", content)),
    }

    for check_name, result in checks.items():
        assert result, f"Missing: {check_name}"
