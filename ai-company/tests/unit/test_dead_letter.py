"""Tests for GAP-017 — task timeout detection and dead-letter queue."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from ai_company.executor.dead_letter import (
    DeadLetterQueue,
    detect_stale_tasks,
)


# ── DeadLetterQueue unit tests ────────────────────────────────────────


class TestDeadLetterQueue:
    def test_creates_dlq_file(self, tmp_path: Path) -> None:
        dlq_path = tmp_path / "dlq.json"
        dlq = DeadLetterQueue(dlq_path=str(dlq_path))
        assert dlq_path.exists()
        assert dlq.list_entries() == []

    def test_move_task_adds_entry(self, tmp_path: Path) -> None:
        dlq = DeadLetterQueue(dlq_path=str(tmp_path / "dlq.json"))
        task = {"id": "t1", "receiver_id": "agent", "instruction": "do stuff"}
        entry = dlq.move_task(task, reason="stale timeout")
        assert entry["task"]["id"] == "t1"
        assert entry["reason"] == "stale timeout"
        assert "moved_at" in entry
        assert len(dlq.list_entries()) == 1

    def test_list_entries_returns_all(self, tmp_path: Path) -> None:
        dlq = DeadLetterQueue(dlq_path=str(tmp_path / "dlq.json"))
        dlq.move_task({"id": "t1"}, "reason1")
        dlq.move_task({"id": "t2"}, "reason2")
        entries = dlq.list_entries()
        assert len(entries) == 2

    def test_get_task_by_id(self, tmp_path: Path) -> None:
        dlq = DeadLetterQueue(dlq_path=str(tmp_path / "dlq.json"))
        dlq.move_task({"id": "t-abc", "instruction": "test"}, "stale")
        found = dlq.get_task("t-abc")
        assert found is not None
        assert found["task"]["instruction"] == "test"

    def test_get_task_not_found(self, tmp_path: Path) -> None:
        dlq = DeadLetterQueue(dlq_path=str(tmp_path / "dlq.json"))
        assert dlq.get_task("nonexistent") is None

    def test_retry_task_removes_from_dlq(self, tmp_path: Path) -> None:
        dlq = DeadLetterQueue(dlq_path=str(tmp_path / "dlq.json"))
        dlq.move_task({"id": "t1", "instruction": "retry me"}, "timeout")
        restored = dlq.retry_task("t1")
        assert restored is not None
        assert restored["id"] == "t1"
        # Should be removed from DLQ
        assert dlq.get_task("t1") is None

    def test_retry_task_not_found(self, tmp_path: Path) -> None:
        dlq = DeadLetterQueue(dlq_path=str(tmp_path / "dlq.json"))
        assert dlq.retry_task("nonexistent") is None

    def test_clear_removes_all(self, tmp_path: Path) -> None:
        dlq = DeadLetterQueue(dlq_path=str(tmp_path / "dlq.json"))
        dlq.move_task({"id": "t1"}, "r1")
        dlq.move_task({"id": "t2"}, "r2")
        count = dlq.clear()
        assert count == 2
        assert dlq.list_entries() == []


# ── Stale task detection ─────────────────────────────────────────────


class TestStaleDetection:
    def _make_task(
        self,
        task_id: str,
        status: str = "in_progress",
        created_at: str = "",
        updated_at: str = "",
    ) -> dict:
        return {
            "id": task_id,
            "sender_id": "ceo",
            "receiver_id": "agent",
            "instruction": f"Task {task_id}",
            "status": status,
            "priority": "medium",
            "created_at": created_at,
            "updated_at": updated_at,
        }

    def test_no_stale_tasks_when_recent(self, tmp_path: Path) -> None:
        """Tasks with recent timestamps should not be detected as stale."""
        inbox = tmp_path / "inbox.json"
        now = datetime.now().isoformat()
        tasks = [self._make_task("t1", created_at=now)]
        inbox.write_text(json.dumps(tasks), encoding="utf-8")

        dlq = DeadLetterQueue(dlq_path=str(tmp_path / "dlq.json"))
        moved = detect_stale_tasks(inbox, dlq, threshold_minutes=30)
        assert len(moved) == 0
        assert dlq.list_entries() == []

    def test_stale_task_detected_and_moved(self, tmp_path: Path) -> None:
        """Task older than threshold should be moved to DLQ."""
        inbox = tmp_path / "inbox.json"
        stale_time = (datetime.now() - timedelta(minutes=60)).isoformat()
        tasks = [self._make_task("t-stale", created_at=stale_time)]
        inbox.write_text(json.dumps(tasks), encoding="utf-8")

        dlq = DeadLetterQueue(dlq_path=str(tmp_path / "dlq.json"))
        moved = detect_stale_tasks(inbox, dlq, threshold_minutes=30)
        assert len(moved) == 1
        assert moved[0]["id"] == "t-stale"

        # Task should be removed from inbox
        remaining = json.loads(inbox.read_text(encoding="utf-8"))
        assert len(remaining) == 0

        # Task should be in DLQ
        entry = dlq.get_task("t-stale")
        assert entry is not None

    def test_updated_at_preferred_over_created_at(self, tmp_path: Path) -> None:
        """When updated_at is present, it should be used for staleness check."""
        inbox = tmp_path / "inbox.json"
        # created_at is recent, but updated_at is old
        recent = datetime.now().isoformat()
        old = (datetime.now() - timedelta(minutes=60)).isoformat()
        tasks = [self._make_task("t-upd", created_at=recent, updated_at=old)]
        inbox.write_text(json.dumps(tasks), encoding="utf-8")

        dlq = DeadLetterQueue(dlq_path=str(tmp_path / "dlq.json"))
        moved = detect_stale_tasks(inbox, dlq, threshold_minutes=30)
        assert len(moved) == 1

    def test_pending_tasks_not_moved(self, tmp_path: Path) -> None:
        """Only in_progress tasks should be considered stale."""
        inbox = tmp_path / "inbox.json"
        old = (datetime.now() - timedelta(minutes=60)).isoformat()
        tasks = [
            self._make_task("t-pending", status="pending", created_at=old),
            self._make_task("t-completed", status="completed", created_at=old),
        ]
        inbox.write_text(json.dumps(tasks), encoding="utf-8")

        dlq = DeadLetterQueue(dlq_path=str(tmp_path / "dlq.json"))
        moved = detect_stale_tasks(inbox, dlq, threshold_minutes=30)
        assert len(moved) == 0

    def test_no_timestamp_treated_as_stale(self, tmp_path: Path) -> None:
        """Task with no timestamps should be treated as stale."""
        inbox = tmp_path / "inbox.json"
        tasks = [self._make_task("t-nots", created_at="", updated_at="")]
        inbox.write_text(json.dumps(tasks), encoding="utf-8")

        dlq = DeadLetterQueue(dlq_path=str(tmp_path / "dlq.json"))
        moved = detect_stale_tasks(inbox, dlq, threshold_minutes=30)
        assert len(moved) == 1

    def test_unparseable_timestamp_treated_as_stale(self, tmp_path: Path) -> None:
        """Task with garbage timestamp should be treated as stale."""
        inbox = tmp_path / "inbox.json"
        tasks = [self._make_task("t-bad", created_at="not-a-date")]
        inbox.write_text(json.dumps(tasks), encoding="utf-8")

        dlq = DeadLetterQueue(dlq_path=str(tmp_path / "dlq.json"))
        moved = detect_stale_tasks(inbox, dlq, threshold_minutes=30)
        assert len(moved) == 1

    def test_nonexistent_inbox_returns_empty(self, tmp_path: Path) -> None:
        dlq = DeadLetterQueue(dlq_path=str(tmp_path / "dlq.json"))
        moved = detect_stale_tasks(tmp_path / "nope.json", dlq)
        assert moved == []

    def test_mixed_tasks_partial_move(self, tmp_path: Path) -> None:
        """Only stale in_progress tasks should be moved; others stay."""
        inbox = tmp_path / "inbox.json"
        now = datetime.now().isoformat()
        old = (datetime.now() - timedelta(minutes=60)).isoformat()

        tasks = [
            self._make_task("t-recent", status="in_progress", created_at=now),
            self._make_task("t-stale", status="in_progress", created_at=old),
            self._make_task("t-pending-old", status="pending", created_at=old),
        ]
        inbox.write_text(json.dumps(tasks), encoding="utf-8")

        dlq = DeadLetterQueue(dlq_path=str(tmp_path / "dlq.json"))
        moved = detect_stale_tasks(inbox, dlq, threshold_minutes=30)
        assert len(moved) == 1
        assert moved[0]["id"] == "t-stale"

        # Two tasks should remain in inbox
        remaining = json.loads(inbox.read_text(encoding="utf-8"))
        assert len(remaining) == 2
        ids = {t["id"] for t in remaining}
        assert "t-stale" not in ids


# ── Executor loop integration ─────────────────────────────────────────


class TestExecutorStaleDetection:
    """Integration test: verify Executor.tick() triggers stale detection."""

    def test_tick_moves_stale_tasks(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)

        # Setup required files
        (tmp_path / "company").mkdir(exist_ok=True)
        (tmp_path / "company" / "models.yaml").write_text(
            json.dumps({"providers": {}, "tiers": {}, "routing": []}), encoding="utf-8"
        )
        (tmp_path / "company" / "agent-registry.json").write_text("[]", encoding="utf-8")
        (tmp_path / ".opencode").mkdir(exist_ok=True)
        (tmp_path / "orchestrator").mkdir(exist_ok=True)
        (tmp_path / "orchestrator" / "approvals.yaml").write_text("requests: []", encoding="utf-8")

        # Put a stale in_progress task in the inbox
        stale_time = (datetime.now() - timedelta(minutes=60)).isoformat()
        inbox = tmp_path / ".opencode" / "inbox.json"
        tasks = [
            {
                "id": "stale-task-001",
                "sender_id": "ceo",
                "receiver_id": "agent",
                "instruction": "Old task that timed out",
                "status": "in_progress",
                "priority": "medium",
                "created_at": stale_time,
            }
        ]
        inbox.write_text(json.dumps(tasks), encoding="utf-8")

        from ai_company.executor.loop import Executor

        executor = Executor(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
            agents_dir=str(tmp_path / ".opencode" / "agents"),
            results_dir=str(tmp_path / "results"),
        )

        count = executor.tick()
        assert count == 0  # No pending tasks

        # The stale task should have been moved to DLQ
        dlq_entries = executor.dlq.list_entries()
        assert len(dlq_entries) == 1
        assert dlq_entries[0]["task"]["id"] == "stale-task-001"

        # Inbox should be empty now
        remaining = json.loads(inbox.read_text(encoding="utf-8"))
        assert len(remaining) == 0
