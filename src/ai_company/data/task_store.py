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

# ── Demo/test detection predicates ──────────────────────────────────
# These MUST stay in lock-step with TaskStore.is_test_task(). The refined
# contract is case-sensitive on demonstrable markers only:
#   - ``proj-acme-chatbot`` substring in id or instruction
#   - instruction starting with ``Test `` (capital T, trailing space)
#   - id starting with ``test-`` or ``verify-`` (lowercase)
# ``GLOB`` matches case-sensitively in SQLite and ``instr`` is a
# case-sensitive substring test — unlike ``LIKE``, which is
# case-insensitive and would over-delete a real task like
# ``test the new API endpoint`` (lowercase t) that the contract treats
# as genuine work.
_ACME_DEMO_PREDICATE = (
    "(instr(instruction, 'proj-acme-chatbot') > 0 OR instr(id, 'proj-acme-chatbot') > 0)"
)
_TEST_INSTRUCTION_PREDICATE = "instruction GLOB 'Test *'"
_TEST_ID_PREDICATE = "(id GLOB 'test-*' OR id GLOB 'verify-*')"
_TEST_TASK_WHERE = (
    f"({_ACME_DEMO_PREDICATE} OR {_TEST_INSTRUCTION_PREDICATE} OR {_TEST_ID_PREDICATE})"
)


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
                parent_task_id, acknowledged_by, claimed_by, lease_expires_at,
                raw_json)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
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
                task.claimed_by,
                task.lease_expires_at,
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
        rows = self._db.fetchall("SELECT status, COUNT(*) as cnt FROM tasks GROUP BY status")
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
                      parent_task_id, acknowledged_by, claimed_by, lease_expires_at
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
            except Exception:  # noqa: BLE001 - skip corrupt rows during import
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

    # ── Cleanup helpers ───────────────────────────────────────────────

    def test_task_breakdown(self) -> dict[str, int]:
        """Count tasks matching each demo/test class.

        Returns a dict with per-class counts before any deletion:

        - ``acme_demo``: id or instruction contains ``proj-acme-chatbot``
        - ``test_instruction``: instruction starts with ``Test ``
        - ``test_id``: id starts with ``test-`` or ``verify-``
        - ``total``: distinct rows matching any class (what
          :meth:`cleanup_test_tasks` will remove)

        Classes may overlap — a task matching two markers contributes to
        both per-class counts but only once to ``total``.
        """
        row = self._db.fetchone(
            f"""SELECT
                COALESCE(SUM({_ACME_DEMO_PREDICATE}), 0) AS acme_demo,
                COALESCE(SUM({_TEST_INSTRUCTION_PREDICATE}), 0) AS test_instruction,
                COALESCE(SUM({_TEST_ID_PREDICATE}), 0) AS test_id,
                COUNT(*) AS total
                FROM tasks WHERE {_TEST_TASK_WHERE}"""
        )
        if row is None:
            return {"acme_demo": 0, "test_instruction": 0, "test_id": 0, "total": 0}
        return {
            "acme_demo": int(row["acme_demo"] or 0),
            "test_instruction": int(row["test_instruction"] or 0),
            "test_id": int(row["test_id"] or 0),
            "total": int(row["total"] or 0),
        }

    def cleanup_test_tasks(self) -> int:
        """Remove tasks matching demo/test patterns.

        Deletes tasks where:
        - instruction or id references the Acme Corp demo project
          (``proj-acme-chatbot``)
        - instruction starts with 'Test ' (dummy instruction)
        - id starts with 'test-' or 'verify-' (dummy task IDs)

        Tasks routed to real agents whose name starts with 'test' (e.g.
        ``test-agent``) are NOT deleted — routing alone is not a demo marker.

        Returns the number of tasks deleted.
        """
        cursor = self._db.execute(f"DELETE FROM tasks WHERE {_TEST_TASK_WHERE}")
        deleted = cursor.rowcount
        self._db.commit()
        if deleted > 0:
            logger.info("Cleaned up %d test/demo tasks from database.", deleted)
        return deleted

    def purge_all_tasks(self) -> int:
        """Remove all tasks from the store.

        Returns the number of tasks deleted.
        """
        cursor = self._db.execute("DELETE FROM tasks")
        deleted = cursor.rowcount
        self._db.commit()
        if deleted > 0:
            logger.info("Purged all %d tasks from database.", deleted)
        return deleted

    @staticmethod
    def is_test_task(task_dict: dict[str, Any]) -> bool:
        """Check if a task dict represents a demo/test task.

        A task is considered demo/test data only when it matches a clear
        dummy/demo marker:
        - instruction or id references the Acme Corp demo project
          (``proj-acme-chatbot``)
        - instruction starts with ``Test `` (dummy instruction)
        - id starts with ``test-`` or ``verify-`` (dummy task ids)

        Routing to an agent whose name starts with ``test`` (e.g. the real
        ``test-agent``) is legitimate and does NOT mark a task as demo/test.
        """
        instruction: str = task_dict.get("instruction", "")
        task_id: str = task_dict.get("id", "")

        if "proj-acme-chatbot" in instruction or "proj-acme-chatbot" in task_id:
            return True
        if instruction.startswith("Test "):
            return True
        return task_id.startswith(("test-", "verify-"))
