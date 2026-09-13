"""Unit tests for the dashboard backlog / queue observability (C3)."""

from __future__ import annotations

import json
from pathlib import Path

from ai_company.dashboard.backlog import (
    DEFAULT_STALE_THRESHOLD_S,
    _parse_ts,
    backlog_summary,
)


def _write_inbox(root: Path, tasks: list[dict[str, object]]) -> None:
    inbox_dir = root / ".opencode"
    inbox_dir.mkdir(parents=True, exist_ok=True)
    (inbox_dir / "inbox.json").write_text(json.dumps(tasks), encoding="utf-8")


def _write_dlq(root: Path, entries: list[dict[str, object]]) -> None:
    dlq_path = root / ".opencode" / "dead_letter.json"
    dlq_path.parent.mkdir(parents=True, exist_ok=True)
    dlq_path.write_text(json.dumps(entries), encoding="utf-8")


class TestParseTs:
    def test_naive_is_utc(self) -> None:
        parsed = _parse_ts("2024-01-01T00:00:00")
        assert parsed is not None
        assert parsed.utcoffset() is not None

    def test_z_suffix(self) -> None:
        parsed = _parse_ts("2024-01-01T00:00:00Z")
        assert parsed is not None

    def test_invalid_returns_none(self) -> None:
        assert _parse_ts("not-a-date") is None
        assert _parse_ts(None) is None
        assert _parse_ts(123) is None


class TestBacklogSummary:
    def test_empty_queue(self, tmp_path: Path) -> None:
        _write_inbox(tmp_path, [])
        summary = backlog_summary(tmp_path)
        assert summary["total"] == 0
        assert summary["by_status"] == {}
        assert summary["dead_letter_count"] == 0
        assert summary["stale_pending_count"] == 0

    def test_status_spread_and_totals(self, tmp_path: Path) -> None:
        _write_inbox(
            tmp_path,
            [
                {"id": "t1", "status": "pending", "created_at": "2024-01-01T00:00:00Z"},
                {"id": "t2", "status": "pending", "created_at": "2024-01-01T00:00:00Z"},
                {"id": "t3", "status": "in_progress", "created_at": "2024-01-01T00:00:00Z"},
                {"id": "t4", "status": "completed", "created_at": "2024-01-01T00:00:00Z"},
                {"id": "t5", "status": "cancelled", "created_at": "2024-01-01T00:00:00Z"},
            ],
        )
        summary = backlog_summary(tmp_path)
        assert summary["total"] == 5
        assert summary["pending"] == 2
        assert summary["in_progress"] == 1
        assert summary["completed"] == 1
        assert summary["cancelled"] == 1
        assert summary["failed"] == 0

    def test_oldest_pending(self, tmp_path: Path) -> None:
        _write_inbox(
            tmp_path,
            [
                {"id": "old", "status": "pending", "created_at": "2024-01-01T00:00:00Z"},
                {"id": "new", "status": "pending", "created_at": "2024-01-01T00:00:00Z"},
                {"id": "done", "status": "completed", "created_at": "2024-01-01T00:00:00Z"},
            ],
        )
        summary = backlog_summary(tmp_path)
        # Both pending share a timestamp; oldest_pending_age_s is > 0
        assert summary["oldest_pending_age_s"] is not None
        assert summary["oldest_pending_age_s"] > 0
        assert summary["oldest_pending_created_at"] == "2024-01-01T00:00:00Z"

    def test_stale_pending_uses_threshold(self, tmp_path: Path) -> None:
        _write_inbox(
            tmp_path,
            [
                {"id": "old", "status": "pending", "created_at": "2024-01-01T00:00:00Z"},
                {"id": "fresh", "status": "pending", "created_at": "2099-01-01T00:00:00Z"},
            ],
        )
        # Default threshold of 24h: the 2024 task is stale, the 2099 task is not.
        summary = backlog_summary(tmp_path)
        assert summary["stale_pending_count"] == 1

    def test_custom_stale_threshold(self, tmp_path: Path) -> None:
        _write_inbox(
            tmp_path,
            [
                {"id": "old", "status": "pending", "created_at": "2024-01-01T00:00:00Z"},
                # Far-future "now" proxy: never stale at any realistic threshold.
                {"id": "future", "status": "pending", "created_at": "2999-01-01T00:00:00Z"},
            ],
        )
        # A threshold of one hour: the 2024 task is stale, the future task is not.
        summary = backlog_summary(tmp_path, stale_threshold_s=3600)
        assert summary["stale_pending_count"] == 1

    def test_dead_letter_count(self, tmp_path: Path) -> None:
        _write_inbox(tmp_path, [])
        _write_dlq(tmp_path, [{"id": "d1"}, {"id": "d2"}])
        summary = backlog_summary(tmp_path)
        assert summary["dead_letter_count"] == 2

    def test_dead_letter_missing_is_zero(self, tmp_path: Path) -> None:
        _write_inbox(tmp_path, [])
        summary = backlog_summary(tmp_path)
        assert summary["dead_letter_count"] == 0

    def test_missing_inbox_is_empty(self, tmp_path: Path) -> None:
        summary = backlog_summary(tmp_path)
        assert summary["total"] == 0
        assert summary["by_status"] == {}

    def test_default_threshold_constant(self) -> None:
        assert DEFAULT_STALE_THRESHOLD_S == 24 * 3600

    def test_inbox_path_reported(self, tmp_path: Path) -> None:
        _write_inbox(tmp_path, [{"id": "a", "status": "pending"}])
        summary = backlog_summary(tmp_path)
        assert str(tmp_path / ".opencode" / "inbox.json") == summary["inbox_path"]
