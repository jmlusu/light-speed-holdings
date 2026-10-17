"""Regression tests for ECL change lifecycle — duplicate detection and validation.

These tests prevent the recurrence of the duplicate-archive issue where:
  - Two archive directories shared the same session_id and title
  - The duplicate had inconsistent metadata (phase: intake, validation_status: unknown)
  - The lint script (lint-ecl.ps1) exited 1 because the duplicate failed its gates.

Run from repo root:
    uv run pytest tests/unit/test_ecl_change_lifecycle.py
"""

from __future__ import annotations

import json
import shutil
from collections import Counter
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = REPO_ROOT / "harness" / "changes" / "INDEX.json"


def _load_index() -> list[dict]:
    with open(INDEX_PATH, encoding="utf-8-sig") as f:
        raw = f.read()
    if raw.startswith("\ufeff"):
        raw = raw[1:]
    data = json.loads(raw)
    return data


def _archive_entries(index_entries: list[dict]) -> list[dict]:
    return [e for e in index_entries if e.get("location") == "archive"]


class TestNoDuplicateArchiveEntries:
    """Ensure the INDEX.json contains no duplicate change slugs/ids."""

    def test_no_duplicate_slugs(self) -> None:
        index_entries = _load_index()
        archive = _archive_entries(index_entries)
        # Each entry should have a 'slug' field
        slugs = [e["slug"] for e in archive]
        assert len(slugs) == len(set(slugs)), f"Duplicate slugs found in INDEX.json: {slugs}"


class TestCompletedChangeMetadata:
    """Ensure every completed archive change has valid metadata."""

    VALID_PHASES = {"validate", "implement"}

    def _completed_entries(self) -> list[dict]:
        index_entries = _load_index()
        return [e for e in index_entries if e.get("status") == "completed"]

    def test_completed_has_validation_status_pass(self) -> None:
        for entry in self._completed_entries():
            assert entry.get("validation_status") == "pass", (
                f"Completed change '{entry.get('title')}' has "
                f"validation_status='{entry.get('validation_status')}', expected 'pass'"
            )

    def test_completed_has_valid_phase(self) -> None:
        for entry in self._completed_entries():
            assert entry.get("phase") in self.VALID_PHASES, (
                f"Change '{entry.get('title')}' has phase='{entry.get('phase')}', "
                f"expected one of {self.VALID_PHASES}"
            )

    def test_completed_not_spec_review_pending(self) -> None:
        for entry in self._completed_entries():
            assert entry.get("spec_review") != "pending", (
                f"Completed change '{entry.get('title')}' has spec_review='{entry.get('spec_review')}', "
                f"expected not 'pending'"
            )


class TestDuplicateSessionIdDetection:
    """Ensure no two archive changes share the same session_id."""

    def test_no_duplicate_session_ids(self) -> None:
        index_entries = _load_index()
        archive = _archive_entries(index_entries)
        # Entries may omit session_id (null); only flag real duplicates.
        session_ids = [e["session_id"] for e in archive if e.get("session_id")]
        counts = Counter(session_ids)
        duplicated = {sid: n for sid, n in counts.items() if n > 1}
        assert not duplicated, f"Duplicate session_ids found in INDEX.json: {duplicated}"


def test_reindex_preserves_integrity() -> None:
    """Integration-style test: reindexing should preserve index integrity.

    After running the reindex command, the INDEX.json should have:
    - No duplicate slugs
    - All completed changes with proper metadata (validation_status=pass,
      phase in {validate, implement}, spec_review != pending)
    """
    import subprocess

    ps = shutil.which("powershell") or shutil.which("pwsh")
    if ps is None:
        pytest.skip("PowerShell not available on this platform")

    result = subprocess.run(
        [
            ps,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(REPO_ROOT / "scripts" / "maintenance" / "harness-change.ps1"),
            "reindex",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"reindex failed: {result.stdout}{result.stderr}"

    index_entries = _load_index()
    archive = _archive_entries(index_entries)

    # No duplicate slugs
    slugs = [e["slug"] for e in archive]
    assert len(slugs) == len(set(slugs)), f"Duplicate slugs after reindex: {slugs}"

    # All completed changes have proper metadata
    completed = [e for e in archive if e.get("status") == "completed"]
    val_statuses = [e["validation_status"] for e in completed]
    assert all(vs == "pass" for vs in val_statuses), (
        f"Completed changes missing validation_status=pass: {val_statuses}"
    )
    phases = [e["phase"] for e in completed]
    assert all(p in {"validate", "implement"} for p in phases), (
        f"Completed changes with invalid phase: {phases}"
    )
    spec_reviews = [e["spec_review"] for e in completed]
    assert all(sr != "pending" for sr in spec_reviews), (
        f"Completed changes with spec_review=pending: {spec_reviews}"
    )
