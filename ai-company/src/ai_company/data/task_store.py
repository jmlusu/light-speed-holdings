"""SQLite-backed task store — drop-in replacement for MessageBus.

Provides the same public interface as :class:`MessageBus` but uses
SQLite for persistence, enabling atomic transactions and efficient
queries on large task sets.

Backward compatibility:
  - ``export_json()`` writes the legacy ``inbox.json`` format.
  - ``import_json()`` loads data from the legacy file.
"""

from __future__ import annotations

import json
import logging
import uuid
from pathlib import Path
from typing import Any

from ai_company.data.database import Database
from ai_company.models.task import Task

logger = logging.getLogger(__name__)


class TaskStore:
    """SQLite-backed task queue with the same interface as MessageBus.

    Args:
        database: An initialised :class:`Database` instance.
    """

    def __init__(self, database: Database) -> None:
        self._db = database

    # ── Core API (backward-compatible with MessageBus) ────────────────

    def send_task(self, task: Task) -> None:
        """Insert a task into the store, auto-generating a correlation_id if missing."""
        if not task.correlation_id:
            task.correlation_id = str(uuid.uuid4())

        self._db.execute(
            """INSERT OR REPLACE INTO tasks
               (id, name, description, assignee, sender_id, receiver_id,
                instruction, status, priority, dependencies, due_date, tags,
                created_at, updated_at, completed_at, result,
                requires_approval, approved_by, correlation_id,
                parent_task_id, acknowledged_by, raw_json)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                task.id,
                task.name,
                task.description,
                task.assignee,
                task.sender_id,
                task.receiver_id,
                task.instruction,
                task.status.value if hasattr(task.status, "value") else task.status,
                task.priority.value if hasattr(task.priority, "value") else task.priority,
                json.dumps(task.dependencies),
                task.due_date,
                json.dumps(task.tags),
                task.created_at,
                task.updated_at,
                task.completed_at,
                task.result,
                int(task.requires_approval),
                task.approved_by,
                task.correlation_id,
                task.parent_task_id,
                task.acknowledged_by,
                task.model_dump_json(),
            ),
        )
        self._db.commit()
        logger.info(
            "Task %s sent from [%s] to [%s] (correlation=%s).",
            task.id,
            task.sender_id,
            task.receiver_id,
            task.correlation_id,
        )

    def get_inbox(self, agent_id: str) -> list[Task]:
        """Return all tasks addressed to *agent_id*."""
        rows = self._db.fetchall(
            "SELECT raw_json FROM tasks WHERE receiver_id = ?",
            (agent_id,),
        )
        return [Task.model_validate_json(r["raw_json"]) for r in rows]

    def get_sent(self, agent_id: str) -> list[Task]:
        """Return all tasks sent by *agent_id*."""
        rows = self._db.fetchall(
            "SELECT raw_json FROM tasks WHERE sender_id = ?",
            (agent_id,),
        )
        return [Task.model_validate_json(r["raw_json"]) for r in rows]

    def get_task_by_id(self, task_id: str) -> Task | None:
        """Find a specific task by its ``id`` field."""
        row = self._db.fetchone(
            "SELECT raw_json FROM tasks WHERE id = ?",
            (task_id,),
        )
        if row is None:
            return None
        return Task.model_validate_json(row["raw_json"])

    def get_subtasks(self, parent_task_id: str) -> list[Task]:
        """Return all tasks whose ``parent_task_id`` matches."""
        rows = self._db.fetchall(
            "SELECT raw_json FROM tasks WHERE parent_task_id = ?",
            (parent_task_id,),
        )
        return [Task.model_validate_json(r["raw_json"]) for r in rows]

    def get_unacknowledged(self, agent_id: str) -> list[Task]:
        """Return tasks assigned to *agent_id* that have not been ACKed yet."""
        rows = self._db.fetchall(
            "SELECT raw_json FROM tasks WHERE receiver_id = ? AND (acknowledged_by = '' OR acknowledged_by IS NULL)",
            (agent_id,),
        )
        return [Task.model_validate_json(r["raw_json"]) for r in rows]

    def acknowledge_task(self, task_id: str, agent_id: str) -> Task | None:
        """Mark a task as acknowledged by *agent_id*.

        Returns the updated Task or ``None`` if not found.
        """
        self._db.execute(
            "UPDATE tasks SET acknowledged_by = ? WHERE id = ?",
            (agent_id, task_id),
        )
        self._db.commit()
        # Rebuild raw_json so reads reflect the update
        self._rebuild_raw_json(task_id)
        return self.get_task_by_id(task_id)

    def count_by_status(self) -> dict[str, int]:
        """Return a mapping of status name -> count across all tasks."""
        rows = self._db.fetchall(
            "SELECT status, COUNT(*) as cnt FROM tasks GROUP BY status"
        )
        return {r["status"]: r["cnt"] for r in rows}

    # ── Extended query API ────────────────────────────────────────────

    def get_tasks_by_status(self, status: str) -> list[Task]:
        """Return all tasks with the given status."""
        rows = self._db.fetchall(
            "SELECT raw_json FROM tasks WHERE status = ?",
            (status,),
        )
        return [Task.model_validate_json(r["raw_json"]) for r in rows]

    def get_tasks_by_priority(self, priority: str) -> list[Task]:
        """Return all tasks with the given priority."""
        rows = self._db.fetchall(
            "SELECT raw_json FROM tasks WHERE priority = ?",
            (priority,),
        )
        return [Task.model_validate_json(r["raw_json"]) for r in rows]

    def update_task_status(self, task_id: str, status: str) -> Task | None:
        """Update the status of a task. Returns the updated task."""
        self._db.execute(
            "UPDATE tasks SET status = ? WHERE id = ?",
            (status, task_id),
        )
        self._db.commit()
        # Rebuild raw_json so reads reflect the update
        self._rebuild_raw_json(task_id)
        return self.get_task_by_id(task_id)

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID. Returns True if a row was deleted."""
        cursor = self._db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self._db.commit()
        return cursor.rowcount > 0

    def get_all_tasks(self) -> list[Task]:
        """Return every task in the store."""
        rows = self._db.fetchall("SELECT raw_json FROM tasks")
        return [Task.model_validate_json(r["raw_json"]) for r in rows]

    def count(self) -> int:
        """Total number of tasks."""
        return self._db.table_count("tasks")

    # ── Internal helpers ──────────────────────────────────────────────

    def _rebuild_raw_json(self, task_id: str) -> None:
        """Rebuild the raw_json column from SQL columns after an update."""
        row = self._db.fetchone(
            """SELECT id, name, description, assignee, sender_id, receiver_id,
                      instruction, status, priority, dependencies, due_date, tags,
                      created_at, updated_at, completed_at, result,
                      requires_approval, approved_by, correlation_id,
                      parent_task_id, acknowledged_by
               FROM tasks WHERE id = ?""",
            (task_id,),
        )
        if row is None:
            return
        task_dict = dict(row)
        task_dict["dependencies"] = json.loads(task_dict.get("dependencies", "[]"))
        task_dict["tags"] = json.loads(task_dict.get("tags", "[]"))
        task_dict["requires_approval"] = bool(task_dict.get("requires_approval", 0))
        # Remove raw_json key if present
        task_dict.pop("raw_json", None)
        self._db.execute(
            "UPDATE tasks SET raw_json = ? WHERE id = ?",
            (json.dumps(task_dict, default=str), task_id),
        )
        self._db.commit()

    # ── Migration helpers ─────────────────────────────────────────────

    def import_json(self, json_path: str | Path) -> int:
        """Import tasks from the legacy ``inbox.json`` file.

        Returns the number of tasks imported.
        """
        path = Path(json_path)
        if not path.exists():
            logger.warning("Legacy inbox file not found: %s", path)
            return 0

        with open(path, "r", encoding="utf-8") as f:
            raw_tasks: list[dict[str, Any]] = json.load(f)

        count = 0
        for task_dict in raw_tasks:
            try:
                task = Task(**task_dict)
                self.send_task(task)
                count += 1
            except Exception:
                logger.warning("Skipping invalid task during import: %s", task_dict.get("id", "?"))

        logger.info("Imported %d tasks from %s", count, path)
        return count

    def export_json(self, json_path: str | Path) -> Path:
        """Export all tasks to the legacy ``inbox.json`` format.

        Useful for backward compatibility with consumers that still read the
        JSON file directly.
        """
        tasks = self.get_all_tasks()
        path = Path(json_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = [t.model_dump() for t in tasks]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info("Exported %d tasks to %s", len(data), path)
        return path
