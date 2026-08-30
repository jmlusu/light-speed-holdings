"""Tests for the drift sweep integrity check (Task 8)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from ai_company.audit.events import AuditEventType
from ai_company.doctor import drift_sweep
from ai_company.doctor.checks import check_drift_sweep


def _write_event(path: str, after_hash: str) -> dict:
    return {
        "event_type": AuditEventType.TOOL_CALL.value,
        "agent_id": "tester",
        "result": {"path": path, "after_hash": after_hash},
    }


def _make_audit(tmp_path: Path, events: list[dict]) -> Path:
    audit = tmp_path / "audit"
    audit.write_text(
        "\n".join(json.dumps(e) for e in events),
        encoding="utf-8",
    )
    return audit


class TestComputeDigest:
    def test_missing_file_returns_none(self, tmp_path: Path):
        assert drift_sweep.compute_digest(tmp_path / "nope.txt") is None

    def test_matches_sha256(self, tmp_path: Path):
        p = tmp_path / "f.txt"
        p.write_text("hello", encoding="utf-8")
        d = drift_sweep.compute_digest(p)
        assert d is not None
        assert len(d) == 64


class TestRunSweep:
    def test_no_events_is_empty_report(self, tmp_path: Path):
        audit = _make_audit(tmp_path, [])
        report = drift_sweep.run_sweep(tracked_paths=[], audit_path=audit)
        assert report["total_checked"] == 0
        assert report["mismatches"] == []
        assert report["audit_entries"] == 0

    def test_matching_file_passes(self, tmp_path: Path):
        # Build the file under a subdir so it isn't ignored by prefixes.
        target = tmp_path / "src" / "app.py"
        target.parent.mkdir(parents=True)
        target.write_text("code", encoding="utf-8")
        digest = drift_sweep.compute_digest(target)
        audit = _make_audit(tmp_path, [_write_event("src/app.py", digest)])
        report = drift_sweep.run_sweep(tracked_paths=[target], audit_path=audit)
        assert report["total_checked"] == 1
        assert report["mismatches"] == []

    def test_mismatch_detected(self, tmp_path: Path):
        target = tmp_path / "src" / "app.py"
        target.parent.mkdir(parents=True)
        target.write_text("code", encoding="utf-8")
        # Event carries the absolute path so it resolves to the tracked file.
        audit = _make_audit(
            tmp_path,
            [_write_event(str(target), "0" * 64)],
        )
        report = drift_sweep.run_sweep(tracked_paths=[target], audit_path=audit)
        assert len(report["mismatches"]) == 1
        assert report["mismatches"][0]["expected_digest"] == "0" * 64


class TestCheckDriftSweep:
    @patch(
        "ai_company.doctor.drift_sweep.run_sweep",
        return_value={
            "total_checked": 3,
            "mismatches": [],
            "unrecorded": [{"path": "x"}],
            "audit_entries": 3,
        },
    )
    def test_passes_when_no_mismatch(self, _mock):
        r = check_drift_sweep()
        assert r.passed is True
        assert r.name == "Drift Sweep"

    @patch(
        "ai_company.doctor.drift_sweep.run_sweep",
        return_value={
            "total_checked": 2,
            "mismatches": [{"path": "a"}],
            "unrecorded": [],
            "audit_entries": 2,
        },
    )
    def test_fails_on_mismatch(self, _mock):
        r = check_drift_sweep()
        assert r.passed is False
        assert r.severity == "error"

    @patch(
        "ai_company.doctor.drift_sweep.run_sweep",
        side_effect=RuntimeError("boom"),
    )
    def test_handles_sweep_failure(self, _mock):
        r = check_drift_sweep()
        assert r.passed is False
        assert "boom" in r.message


class TestDeriveTrackedPaths:
    def test_ignores_runtime_dirs(self, tmp_path: Path):
        digest = "a" * 64
        events = [
            _write_event(".opencode/audit", digest),
            _write_event("src/app.py", digest),
        ]
        audit = _make_audit(tmp_path, events)
        paths = drift_sweep.derive_tracked_paths(audit)
        names = {p.name for p in paths}
        assert names == {"app.py"}
