"""Tests for MessageBus broadcast integration (GAP-006).

Verifies that task lifecycle events trigger broadcast callbacks:
- send_task → "created"
- update_task_status("completed") → "completed"
- update_task_status("failed") → "failed"
- update_task_status("escalated") → "escalated"
- update_task_status("in_progress") → "status_changed"
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from ai_company.models.task import Task
from ai_company.orchestrator.message_bus import MessageBus


class TestMessageBusBroadcast:
    """Verify broadcast_callback is invoked on task mutations."""

    def test_send_task_emits_created(self, tmp_path: Path) -> None:
        events: list[tuple[dict, str]] = []

        def callback(task_dict: dict[str, Any], event: str) -> None:
            events.append((task_dict, event))

        bus = MessageBus(
            storage_path=str(tmp_path / "inbox.json"),
            broadcast_callback=callback,
        )
        task = Task(
            id="t1",
            sender_id="a",
            receiver_id="b",
            instruction="do something",
        )
        bus.send_task(task)

        assert len(events) == 1
        assert events[0][1] == "created"
        assert events[0][0]["id"] == "t1"

    def test_update_task_status_completed(self, tmp_path: Path) -> None:
        events: list[tuple[dict, str]] = []

        def callback(task_dict: dict[str, Any], event: str) -> None:
            events.append((task_dict, event))

        bus = MessageBus(
            storage_path=str(tmp_path / "inbox.json"),
            broadcast_callback=callback,
        )
        task = Task(id="t1", sender_id="a", receiver_id="b", instruction="x")
        bus.send_task(task)
        # send_task emits "created"
        assert len(events) == 1

        result = bus.update_task_status("t1", "completed", result="done")
        assert result is not None
        assert result.status.value == "completed"
        assert result.result == "done"
        assert result.completed_at  # Should be set

        # Should have emitted "completed"
        assert len(events) == 2
        assert events[1][1] == "completed"
        assert events[1][0]["status"] == "completed"

    def test_update_task_status_failed(self, tmp_path: Path) -> None:
        events: list[tuple[dict, str]] = []

        def callback(task_dict: dict[str, Any], event: str) -> None:
            events.append((task_dict, event))

        bus = MessageBus(
            storage_path=str(tmp_path / "inbox.json"),
            broadcast_callback=callback,
        )
        task = Task(id="t1", sender_id="a", receiver_id="b", instruction="x")
        bus.send_task(task)

        bus.update_task_status("t1", "failed", result="error occurred")

        assert len(events) == 2
        assert events[1][1] == "failed"
        assert events[1][0]["result"] == "error occurred"

    def test_update_task_status_escalated(self, tmp_path: Path) -> None:
        events: list[tuple[dict, str]] = []

        def callback(task_dict: dict[str, Any], event: str) -> None:
            events.append((task_dict, event))

        bus = MessageBus(
            storage_path=str(tmp_path / "inbox.json"),
            broadcast_callback=callback,
        )
        task = Task(id="t1", sender_id="a", receiver_id="b", instruction="x")
        bus.send_task(task)

        bus.update_task_status("t1", "escalated")

        assert len(events) == 2
        assert events[1][1] == "escalated"

    def test_update_task_status_in_progress(self, tmp_path: Path) -> None:
        events: list[tuple[dict, str]] = []

        def callback(task_dict: dict[str, Any], event: str) -> None:
            events.append((task_dict, event))

        bus = MessageBus(
            storage_path=str(tmp_path / "inbox.json"),
            broadcast_callback=callback,
        )
        task = Task(id="t1", sender_id="a", receiver_id="b", instruction="x")
        bus.send_task(task)

        bus.update_task_status("t1", "in_progress")

        assert len(events) == 2
        assert events[1][1] == "status_changed"

    def test_no_broadcast_when_no_callback(self, tmp_path: Path) -> None:
        """When no callback is configured, operations still work."""
        bus = MessageBus(storage_path=str(tmp_path / "inbox.json"))
        task = Task(id="t1", sender_id="a", receiver_id="b", instruction="x")
        bus.send_task(task)
        result = bus.update_task_status("t1", "completed")
        assert result is not None

    def test_broadcast_callback_error_does_not_propagate(self, tmp_path: Path) -> None:
        """Errors in the broadcast callback are logged but not raised."""

        def bad_callback(task_dict: dict[str, Any], event: str) -> None:
            raise RuntimeError("broadcast boom")

        bus = MessageBus(
            storage_path=str(tmp_path / "inbox.json"),
            broadcast_callback=bad_callback,
        )
        task = Task(id="t1", sender_id="a", receiver_id="b", instruction="x")
        # Should not raise
        bus.send_task(task)
        result = bus.update_task_status("t1", "completed")
        assert result is not None

    def test_update_task_status_not_found(self, tmp_path: Path) -> None:
        events: list[tuple[dict, str]] = []

        def callback(task_dict: dict[str, Any], event: str) -> None:
            events.append((task_dict, event))

        bus = MessageBus(
            storage_path=str(tmp_path / "inbox.json"),
            broadcast_callback=callback,
        )
        result = bus.update_task_status("nonexistent", "completed")
        assert result is None
        assert len(events) == 0  # No broadcast for missing task
