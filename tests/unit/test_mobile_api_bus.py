"""Mobile API task reads routed through the MessageBus (GAP-011).

Regression lock: every ``/api/mobile`` read path that previously opened
``.opencode/inbox.json`` directly must now read through the shared
dashboard MessageBus so mobile clients see the same live task state as the
REST API and the executor.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from ai_company.dashboard import api as dash_api
from ai_company.dashboard import mobile_api
from ai_company.dashboard.repository import configure_state_store, reset_state_store
from ai_company.models import Task, TaskPriority


def _make_task(task_id: str, status: str, receiver: str = "test-agent") -> Task:
    return Task(
        id=task_id,
        sender_id="human-ceo",
        receiver_id=receiver,
        instruction=f"Task {task_id}",
        status=status,
        priority=TaskPriority.MEDIUM,
        created_at=datetime.now().isoformat(),
    )


@pytest.fixture()
def seeded_bus(tmp_path: Path):
    """Bind the dashboard StateStore + shared bus to an isolated tmp root.

    Seeds two tasks through the bus itself, then returns the shared bus so
    tests can assert on the persisted task state.
    """
    reset_state_store()
    configure_state_store(tmp_path)
    dash_api._bus = None
    bus = dash_api.get_bus()
    for task in [_make_task("mob-1", "pending"), _make_task("mob-2", "completed")]:
        bus.send_task(task)
    yield bus
    dash_api._bus = None
    reset_state_store()


def test_mobile_tasks_reads_through_bus(seeded_bus) -> None:
    result = mobile_api.mobile_tasks()
    assert result["total_count"] == 2
    ids = {item["id"] for item in result["items"]}
    assert ids == {"mob-1", "mob-2"}


def test_mobile_dashboard_counts_through_bus(seeded_bus) -> None:
    summary = mobile_api.mobile_dashboard()
    assert summary.kpis.pending == 1
    assert summary.kpis.completed == 1
    assert summary.urgent.failed_count == 0


def test_compact_kpis_reads_through_bus(seeded_bus) -> None:
    kpis = mobile_api.compact_kpis()
    assert kpis["pending"] == 1
    assert kpis["failed"] == 0
    assert kpis["completed_today"] == 0  # no completed_at timestamps set


def test_mobile_sync_reads_through_bus(seeded_bus) -> None:
    result = mobile_api.mobile_sync(mobile_api.SyncRequest())
    assert result["updates"]["tasks_changed"] == 2
    assert result["dashboard_delta"]["pending"] == 1


def test_delegate_task_updates_through_bus(seeded_bus) -> None:
    result = mobile_api._delegate_task("mob-1", "other-agent")
    assert result["ok"] is True
    assert result["delegated_to"] == "other-agent"

    task = seeded_bus.get_task_by_id("mob-1")
    assert task is not None
    assert task.receiver_id == "other-agent"


def test_mobile_endpoints_never_read_inbox_file_directly(
    seeded_bus, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Guard: if a mobile endpoint starts opening inbox.json again, fail."""

    original_load_json = mobile_api._load_json

    def _guarded_load_json(path, default=None):
        if "inbox.json" in str(path).replace("\\", "/"):
            raise AssertionError(f"mobile endpoint read inbox.json directly: {path}")
        return original_load_json(path)

    monkeypatch.setattr(mobile_api, "_load_json", _guarded_load_json)

    summary = mobile_api.mobile_dashboard()
    assert summary.kpis.pending == 1

    assert mobile_api.mobile_tasks()["total_count"] == 2
    assert mobile_api.compact_kpis()["pending"] == 1

    sync = mobile_api.mobile_sync(mobile_api.SyncRequest())
    assert sync["updates"]["tasks_changed"] == 2
