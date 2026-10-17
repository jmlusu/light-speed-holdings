"""Tests for MessageBus event log and retry support (M8.2).

Verifies:
- log_event persists lifecycle events on tasks
- get_events retrieves event history
- retry_task requeues failed tasks with budget enforcement
"""

from __future__ import annotations

from pathlib import Path

from ai_company.models.task import Task, TaskEventType, TaskResult, TaskStatus
from ai_company.orchestrator.message_bus import MessageBus


def _make_bus(tmp_path: Path) -> MessageBus:
    return MessageBus(storage_path=str(tmp_path / "inbox.json"))


def _send_task(bus: MessageBus, task_id: str = "t1", **kwargs) -> Task:
    task = Task(id=task_id, sender_id="a", receiver_id="b", instruction="x", **kwargs)
    bus.send_task(task)
    return task


# ---------------------------------------------------------------------------
# Event log
# ---------------------------------------------------------------------------


class TestEventLog:
    def test_log_event_persists(self, tmp_path: Path) -> None:
        bus = _make_bus(tmp_path)
        _send_task(bus)
        bus.log_event("t1", TaskEventType.CLAIMED, detail="by worker-1")
        events = bus.get_events("t1")
        assert len(events) == 1
        assert events[0]["event"] == "claimed"
        assert events[0]["detail"] == "by worker-1"
        assert "timestamp" in events[0]

    def test_log_event_with_result(self, tmp_path: Path) -> None:
        bus = _make_bus(tmp_path)
        _send_task(bus)
        result = TaskResult(
            task_id="t1",
            status=TaskStatus.COMPLETED,
            output="Done",
            duration_seconds=1.5,
            tokens_used=500,
            cost_usd=0.001,
        )
        bus.log_event("t1", TaskEventType.COMPLETED, result=result)
        events = bus.get_events("t1")
        assert len(events) == 1
        assert events[0]["event"] == "completed"
        assert events[0]["result"]["output"] == "Done"
        assert events[0]["result"]["tokens_used"] == 500

    def test_log_event_accumulates(self, tmp_path: Path) -> None:
        bus = _make_bus(tmp_path)
        _send_task(bus)
        bus.log_event("t1", TaskEventType.QUEUED)
        bus.log_event("t1", TaskEventType.CLAIMED)
        bus.log_event("t1", TaskEventType.RUNNING)
        bus.log_event("t1", TaskEventType.COMPLETED)
        events = bus.get_events("t1")
        assert len(events) == 4
        assert [e["event"] for e in events] == [
            "queued",
            "claimed",
            "running",
            "completed",
        ]

    def test_get_events_unknown_task(self, tmp_path: Path) -> None:
        bus = _make_bus(tmp_path)
        assert bus.get_events("nonexistent") == []

    def test_log_event_unknown_task_no_error(self, tmp_path: Path) -> None:
        bus = _make_bus(tmp_path)
        # Should not raise — event log is best-effort
        bus.log_event("nonexistent", TaskEventType.COMPLETED)


# ---------------------------------------------------------------------------
# Retry
# ---------------------------------------------------------------------------


class TestRetryTask:
    def test_retry_failed_task(self, tmp_path: Path) -> None:
        bus = _make_bus(tmp_path)
        _send_task(bus)
        bus.update_task_status("t1", "failed", result="boom")
        retried = bus.retry_task("t1", reason="transient error")
        assert retried is not None
        assert retried.status == TaskStatus.PENDING
        assert retried.retry_count == 1
        assert retried.claimed_by == ""
        assert retried.lease_expires_at == ""

    def test_retry_timeout_task(self, tmp_path: Path) -> None:
        bus = _make_bus(tmp_path)
        _send_task(bus)
        bus.update_task_status("t1", "timeout")
        retried = bus.retry_task("t1")
        assert retried is not None
        assert retried.status == TaskStatus.PENDING

    def test_retry_budget_exhausted(self, tmp_path: Path) -> None:
        bus = _make_bus(tmp_path)
        _send_task(bus, retry_budget=2)
        bus.update_task_status("t1", "failed", result="e1")
        bus.retry_task("t1")  # retry_count -> 1
        bus.update_task_status("t1", "failed", result="e2")
        bus.retry_task("t1")  # retry_count -> 2 (budget met)
        bus.update_task_status("t1", "failed", result="e3")
        result = bus.retry_task("t1", reason="permanent failure")
        assert result is None  # budget exhausted, escalated
        task = bus.get_task_by_id("t1")
        assert task is not None
        assert task.status == TaskStatus.ESCALATED
        events = bus.get_events("t1")
        escalated = [e for e in events if e["event"] == "escalated"]
        assert len(escalated) == 1
        assert escalated[0]["detail"] == "permanent failure"

    def test_retry_non_retryable_status(self, tmp_path: Path) -> None:
        bus = _make_bus(tmp_path)
        _send_task(bus)
        assert bus.retry_task("t1") is None  # pending, not failed/timeout

    def test_retry_unknown_task(self, tmp_path: Path) -> None:
        bus = _make_bus(tmp_path)
        assert bus.retry_task("nonexistent") is None

    def test_retry_emits_retrying_event(self, tmp_path: Path) -> None:
        bus = _make_bus(tmp_path)
        _send_task(bus)
        bus.update_task_status("t1", "failed")
        bus.retry_task("t1")
        events = bus.get_events("t1")
        retrying = [e for e in events if e["event"] == "retrying"]
        assert len(retrying) == 1
        assert "1/3" in retrying[0]["detail"]

    def test_retry_default_budget(self, tmp_path: Path) -> None:
        """When retry_budget is 0 (unset), default 3 applies."""
        bus = _make_bus(tmp_path)
        _send_task(bus, retry_budget=0)
        for _ in range(3):
            bus.update_task_status("t1", "failed")
            bus.retry_task("t1")
        # 4th retry should exhaust budget
        bus.update_task_status("t1", "failed")
        result = bus.retry_task("t1")
        assert result is None
