"""Tests for the SQLite-backed TaskStore."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_company.data.database import Database
from ai_company.data.task_store import TaskStore
from ai_company.models.task import Task, TaskStatus, TaskPriority


@pytest.fixture
def db(tmp_path: Path) -> Database:
    """Create a temporary database."""
    database = Database(tmp_path / "test_tasks.db")
    database.init_schema()
    yield database
    database.close()


@pytest.fixture
def store(db: Database) -> TaskStore:
    """Create a TaskStore backed by the test database."""
    return TaskStore(db)


def _make_task(
    task_id: str = "task-1",
    sender: str = "agent-a",
    receiver: str = "agent-b",
    status: TaskStatus = TaskStatus.PENDING,
    priority: TaskPriority = TaskPriority.MEDIUM,
    **overrides,
) -> Task:
    """Helper to create a Task with defaults."""
    return Task(
        id=task_id,
        sender_id=sender,
        receiver_id=receiver,
        status=status,
        priority=priority,
        instruction="Do something",
        **overrides,
    )


class TestTaskStore:
    """Tests for TaskStore core API."""

    def test_send_and_receive(self, store: TaskStore) -> None:
        """send_task followed by get_inbox retrieves the task."""
        task = _make_task()
        store.send_task(task)

        inbox = store.get_inbox("agent-b")
        assert len(inbox) == 1
        assert inbox[0].id == "task-1"

    def test_get_sent(self, store: TaskStore) -> None:
        """get_sent returns tasks sent by an agent."""
        store.send_task(_make_task(sender="alice", receiver="bob"))
        store.send_task(_make_task(task_id="task-2", sender="alice", receiver="charlie"))

        sent = store.get_sent("alice")
        assert len(sent) == 2

    def test_correlation_id_auto_generated(self, store: TaskStore) -> None:
        """Missing correlation_id is auto-generated."""
        task = _make_task()
        assert task.correlation_id == ""
        store.send_task(task)

        inbox = store.get_inbox("agent-b")
        assert inbox[0].correlation_id != ""

    def test_get_task_by_id(self, store: TaskStore) -> None:
        """get_task_by_id finds a specific task."""
        store.send_task(_make_task(task_id="find-me"))
        result = store.get_task_by_id("find-me")
        assert result is not None
        assert result.id == "find-me"

    def test_get_task_by_id_missing(self, store: TaskStore) -> None:
        """get_task_by_id returns None for nonexistent IDs."""
        assert store.get_task_by_id("nope") is None

    def test_get_subtasks(self, store: TaskStore) -> None:
        """get_subtasks returns child tasks."""
        store.send_task(_make_task(task_id="parent"))
        store.send_task(_make_task(task_id="child-1", parent_task_id="parent"))
        store.send_task(_make_task(task_id="child-2", parent_task_id="parent"))

        subtasks = store.get_subtasks("parent")
        assert len(subtasks) == 2
        ids = {t.id for t in subtasks}
        assert ids == {"child-1", "child-2"}

    def test_get_unacknowledged(self, store: TaskStore) -> None:
        """get_unacknowledged returns tasks not yet ACKed."""
        store.send_task(_make_task(task_id="unacked"))
        result = store.get_unacknowledged("agent-b")
        assert len(result) == 1

    def test_acknowledge_task(self, store: TaskStore) -> None:
        """acknowledge_task marks the task as acknowledged."""
        store.send_task(_make_task(task_id="to-ack"))
        updated = store.acknowledge_task("to-ack", "agent-b")
        assert updated is not None
        assert updated.acknowledged_by == "agent-b"

        # No longer unacknowledged
        unacked = store.get_unacknowledged("agent-b")
        assert len(unacked) == 0

    def test_count_by_status(self, store: TaskStore) -> None:
        """count_by_status returns correct counts."""
        store.send_task(_make_task(task_id="p1", status=TaskStatus.PENDING))
        store.send_task(_make_task(task_id="p2", status=TaskStatus.PENDING))
        store.send_task(_make_task(task_id="c1", status=TaskStatus.COMPLETED))

        counts = store.count_by_status()
        assert counts["pending"] == 2
        assert counts["completed"] == 1

    def test_get_tasks_by_status(self, store: TaskStore) -> None:
        """get_tasks_by_status filters correctly."""
        store.send_task(_make_task(task_id="a", status=TaskStatus.FAILED))
        store.send_task(_make_task(task_id="b", status=TaskStatus.COMPLETED))

        failed = store.get_tasks_by_status("failed")
        assert len(failed) == 1
        assert failed[0].id == "a"

    def test_update_task_status(self, store: TaskStore) -> None:
        """update_task_status changes the status."""
        store.send_task(_make_task(task_id="flip"))
        updated = store.update_task_status("flip", "in_progress")
        assert updated is not None
        assert updated.status == TaskStatus.IN_PROGRESS

    def test_delete_task(self, store: TaskStore) -> None:
        """delete_task removes a task."""
        store.send_task(_make_task(task_id="doomed"))
        assert store.delete_task("doomed") is True
        assert store.get_task_by_id("doomed") is None

    def test_delete_task_nonexistent(self, store: TaskStore) -> None:
        """Deleting a nonexistent task returns False."""
        assert store.delete_task("ghost") is False

    def test_get_all_tasks(self, store: TaskStore) -> None:
        """get_all_tasks returns everything."""
        store.send_task(_make_task(task_id="x"))
        store.send_task(_make_task(task_id="y"))
        all_tasks = store.get_all_tasks()
        assert len(all_tasks) == 2

    def test_count(self, store: TaskStore) -> None:
        """count returns total number of tasks."""
        assert store.count() == 0
        store.send_task(_make_task())
        assert store.count() == 1


class TestTaskStoreMigration:
    """Tests for JSON import/export migration helpers."""

    def test_import_json(self, store: TaskStore, tmp_path: Path) -> None:
        """import_json loads tasks from the legacy inbox.json format."""
        legacy_tasks = [
            {
                "id": "legacy-1",
                "sender_id": "old-agent",
                "receiver_id": "new-agent",
                "status": "completed",
                "priority": "high",
                "instruction": "Legacy task",
                "dependencies": [],
                "tags": ["legacy"],
            },
            {
                "id": "legacy-2",
                "sender_id": "old-agent",
                "receiver_id": "another-agent",
                "status": "pending",
                "priority": "low",
                "instruction": "Another legacy task",
                "dependencies": [],
                "tags": [],
            },
        ]
        json_path = tmp_path / "inbox.json"
        json_path.write_text(json.dumps(legacy_tasks), encoding="utf-8")

        count = store.import_json(json_path)
        assert count == 2
        assert store.count() == 2

    def test_import_json_missing_file(self, store: TaskStore, tmp_path: Path) -> None:
        """import_json handles missing file gracefully."""
        count = store.import_json(tmp_path / "nonexistent.json")
        assert count == 0

    def test_export_json(self, store: TaskStore, tmp_path: Path) -> None:
        """export_json writes tasks to the legacy format."""
        store.send_task(_make_task(task_id="export-me"))
        export_path = tmp_path / "exported.json"
        store.export_json(export_path)

        assert export_path.exists()
        data = json.loads(export_path.read_text(encoding="utf-8"))
        assert len(data) == 1
        assert data[0]["id"] == "export-me"

    def test_roundtrip(self, store: TaskStore, tmp_path: Path) -> None:
        """Export then import preserves data."""
        store.send_task(_make_task(task_id="roundtrip"))
        export_path = tmp_path / "roundtrip.json"
        store.export_json(export_path)

        # Create fresh store
        fresh_db = Database(tmp_path / "fresh.db")
        fresh_db.init_schema()
        fresh_store = TaskStore(fresh_db)
        fresh_store.import_json(export_path)

        assert fresh_store.count() == 1
        task = fresh_store.get_task_by_id("roundtrip")
        assert task is not None

        fresh_db.close()
