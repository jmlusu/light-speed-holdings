"""Test wayfinder map structure validation.

Validates the existing design issue format across all map variants.
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

# Test existing wayfinder maps (design issue format - flexible)
existing_maps = [
    "docs/wayfinder/45-health-anomaly-monitor.md",
    "docs/wayfinder/46-revenue-attribution-model.md",
    "docs/wayfinder/48-searchable-execution-timeline.md",
    "docs/wayfinder/50-command-bar-and-voice-scope.md",
]

NEW_MAP = "docs/wayfinder/map2-scraper-discovery-gap-analysis.md"


@pytest.mark.parametrize("filepath", existing_maps)
def test_wayfinder_map_has_core_fields(filepath: str) -> None:
    """Validate existing wayfinder design issue format - checks for core fields.

    Field checks match the bold label in either layout used by existing maps:
    colon style (``**Status**:``) or markdown-table style (``| **Status** | ...``).
    """
    with open(REPO_ROOT / filepath, encoding="utf-8") as f:
        content = f.read()

    checks = {
        "has_issue_format": bool(re.search(r"Issue #\d+|F\d:|#\w+:", content)),
        "has_status_field": bool(re.search(r"\*\*Status\*\*", content)),
        "has_owner_field": bool(re.search(r"\*\*Owner\*\*", content)),
        "has_date_field": bool(re.search(r"\*\*Date\*\*", content)),
        "has_related_files": bool(re.search(r"\*\*Related [Ff]iles\*\*", content)),
    }

    # At minimum, should have status and owner
    assert checks["has_status_field"], "Missing status field"
    assert checks["has_owner_field"], "Missing owner field"
    assert checks["has_date_field"], "Missing date field"
    assert checks["has_related_files"], "Missing related files"


def test_wayfinder_map_new_format() -> None:
    """Validate new wayfinder map format (with wayfinder:map label).

    The map file must exist: a missing file fails the test (no skip by design).
    """
    with open(REPO_ROOT / NEW_MAP, encoding="utf-8") as f:
        content = f.read()

    checks = {
        "has_wayfinder_map_label": bool(re.search(r"wayfinder:map", content)),
        "has_ticket_labels": bool(
            re.search(r"wayfinder:(research|prototype|grilling|task)", content)
        ),
        "has_decisions_section": bool(re.search(r"Decisions so far", content)),
        "has_not_specified": bool(re.search(r"Not yet specified", content)),
        "has_out_of_scope": bool(re.search(r"Out of scope", content)),
        "has_destination_section": bool(re.search(r"## Destination", content)),
        "has_notes_section": bool(re.search(r"## Notes", content)),
    }

    # All checks must pass for new format
    for check_name, result in checks.items():
        assert result, f"Missing: {check_name}"
