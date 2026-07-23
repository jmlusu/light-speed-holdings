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

    def test_update_task_status_with_result(self, store: TaskStore) -> None:
        """update_task_status stores result and sets completed_at for terminal statuses."""
        store.send_task(_make_task(task_id="res"))
        updated = store.update_task_status("res", "completed", result="All done")
        assert updated is not None
        assert updated.status == TaskStatus.COMPLETED
        assert updated.result == "All done"
        assert updated.completed_at != ""

    def test_get_pending_tasks(self, store: TaskStore) -> None:
        """get_pending_tasks returns only tasks with status 'pending'."""
        store.send_task(_make_task(task_id="p1", status=TaskStatus.PENDING))
        store.send_task(_make_task(task_id="p2", status=TaskStatus.PENDING))
        store.send_task(_make_task(task_id="c1", status=TaskStatus.COMPLETED))

        pending = store.get_pending_tasks()
        assert len(pending) == 2
        ids = {t.id for t in pending}
        assert ids == {"p1", "p2"}

    def test_claim_next_pending(self, store: TaskStore) -> None:
        """claim_next_pending atomically claims the oldest pending task."""
        store.send_task(_make_task(task_id="first", status=TaskStatus.PENDING))
        store.send_task(_make_task(task_id="second", status=TaskStatus.PENDING))

        claimed = store.claim_next_pending()
        assert claimed is not None
        assert claimed.id == "first"
        assert claimed.status == TaskStatus.IN_PROGRESS

        # Second claim gets the next one
        claimed2 = store.claim_next_pending()
        assert claimed2 is not None
        assert claimed2.id == "second"

        # No more pending
        assert store.claim_next_pending() is None

    def test_claim_next_pending_empty(self, store: TaskStore) -> None:
        """claim_next_pending returns None when no pending tasks exist."""
        store.send_task(_make_task(task_id="done", status=TaskStatus.COMPLETED))
        assert store.claim_next_pending() is None

    def test_claim_next_pending_respects_order(self, store: TaskStore) -> None:
        """claim_next_pending claims the oldest task first (FIFO)."""
        # Send in reverse order
        store.send_task(_make_task(task_id="third", status=TaskStatus.PENDING))
        store.send_task(_make_task(task_id="first", status=TaskStatus.PENDING))
        store.send_task(_make_task(task_id="second", status=TaskStatus.PENDING))

        claimed1 = store.claim_next_pending()
        assert claimed1 is not None
        assert claimed1.id == "third"  # oldest by created_at

        claimed2 = store.claim_next_pending()
        assert claimed2 is not None
        assert claimed2.id == "first"

        claimed3 = store.claim_next_pending()
        assert claimed3 is not None
        assert claimed3.id == "second"

        assert store.claim_next_pending() is None

    def test_detect_stale_tasks(self, store: TaskStore, tmp_path: Path) -> None:
        """detect_stale_tasks moves old in_progress tasks to DLQ."""
        from datetime import datetime, timedelta
        from ai_company.executor.dead_letter import DeadLetterQueue

        dlq = DeadLetterQueue(dlq_path=str(tmp_path / "dlq.json"))

        # Create a task with an old updated_at
        store.send_task(_make_task(task_id="old", status=TaskStatus.IN_PROGRESS))
        old_time = (datetime.now() - timedelta(hours=2)).isoformat()
        store._db.execute(
            "UPDATE tasks SET updated_at = ? WHERE id = ?",
            (old_time, "old"),
        )
        store._db.commit()
        store._rebuild_raw_json("old")

        # Create a fresh task with a recent timestamp
        now_str = datetime.now().isoformat()
        fresh_task = _make_task(task_id="fresh", status=TaskStatus.IN_PROGRESS)
        fresh_task.created_at = now_str
        fresh_task.updated_at = now_str
        store.send_task(fresh_task)

        moved = store.detect_stale_tasks(dlq, threshold_minutes=30)
        assert len(moved) == 1
        assert moved[0]["id"] == "old"

        # Old task removed from store
        assert store.get_task_by_id("old") is None
        assert store.get_task_by_id("fresh") is not None

        # Old task is in DLQ
        entries = dlq.list_entries()
        assert len(entries) == 1
        assert entries[0]["task"]["id"] == "old"

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
