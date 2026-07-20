"""Hardened MessageBus for the AI Company Builder.

Provides a JSON-backed task queue with:
- Atomic writes via FileStore (write-to-temp-then-rename)
- File locking for concurrent access
- Correlation IDs for tracing
- Parent/child task linkage
- ACK tracking
- Backup file on every write
- Query helpers for subtasks, unacknowledged tasks, and status counts
- Dashboard broadcast hooks for real-time WebSocket updates
"""

from __future__ import annotations

import logging
import uuid
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, List

from ai_company.models.task import Task
from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)

# Type alias for the optional broadcast callback
BroadcastCallback = Callable[[dict[str, Any], str], None] | None


class MessageBus:
    """JSON-backed task queue with atomic writes and correlation tracking.

    All file I/O is delegated to :class:`FileStore` for atomic writes and
    file locking, eliminating the risk of partial writes from concurrent
    access.

    Args:
        storage_path: Path to the inbox JSON file.
        broadcast_callback: Optional synchronous callback invoked after
            task mutations.  Receives ``(task_dict, event_type)`` where
            *event_type* is one of ``"created"``, ``"completed"``,
            ``"failed"``, ``"escalated"``.
    """

    def __init__(
        self,
        storage_path: str = ".opencode/inbox.json",
        broadcast_callback: BroadcastCallback = None,
    ) -> None:
        self.storage_path = Path(storage_path)
        self._store = FileStore(self.storage_path.parent, backup=True)
        self._inbox_name = self.storage_path.name
        self._broadcast_callback = broadcast_callback

        # Ensure the inbox file exists
        if not self._store.exists(self._inbox_name):
            self._store.write_json(self._inbox_name, [])

    # ── Internal persistence helpers ──────────────────────────────────

    def _load_tasks(self) -> List[dict]:
        data = self._store.read_json(self._inbox_name)
        if data is None:
            return []
        if not isinstance(data, list):
            logger.warning("Corrupt inbox data — returning empty list.")
            return []
        return data

    def _save_tasks(self, tasks: List[dict]) -> None:
        self._store.write_json(self._inbox_name, tasks)

    def _mutate_tasks(self, updater: Callable[[List[dict]], List[dict]]) -> List[dict]:
        """Apply *updater* to the inbox under an exclusive file lock.

        Serialises the read-modify-write cycle so concurrent executor and
        dashboard access cannot corrupt :file:`inbox.json` or lose updates
        (GAP-002).
        """
        return self._store.update_json(self._inbox_name, lambda data: updater(data or []))

    # ── Broadcast helper ─────────────────────────────────────────────

    def _emit(self, task_dict: dict, event: str) -> None:
        """Invoke the broadcast callback if one was configured.

        Errors are logged but never raised -- broadcasting is best-effort.
        """
        if self._broadcast_callback is None:
            return
        try:
            self._broadcast_callback(task_dict, event)
        except Exception:
            logger.debug("Broadcast callback failed for event '%s'", event, exc_info=True)

    # ── Core API ─────────────────────────────────────────────────────

    def send_task(self, task: Task) -> None:
        """Append *task* to the inbox, auto-generating a correlation_id if missing.

        If a *broadcast_callback* was provided at construction, it is
        called with ``(task_dict, "created")`` after the write succeeds.
        """
        if not task.correlation_id:
            task.correlation_id = str(uuid.uuid4())
        task_dict = task.model_dump()

        def _updater(tasks: List[dict]) -> List[dict]:
            tasks.append(task_dict)
            return tasks

        self._mutate_tasks(_updater)
        logger.info(
            "Task %s sent from [%s] to [%s] (correlation=%s).",
            task.id,
            task.sender_id,
            task.receiver_id,
            task.correlation_id,
        )
        self._emit(task_dict, "created")

    def get_inbox(self, agent_id: str) -> List[Task]:
        """Return all tasks addressed to *agent_id*."""
        tasks = self._load_tasks()
        return [Task(**t) for t in tasks if t.get("receiver_id") == agent_id]

    def get_sent(self, agent_id: str) -> List[Task]:
        """Return all tasks sent by *agent_id*."""
        tasks = self._load_tasks()
        return [Task(**t) for t in tasks if t.get("sender_id") == agent_id]

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks in the inbox (public method for integration)."""
        tasks = self._load_tasks()
        return [Task(**t) for t in tasks]

    # ── Pending tasks (executor integration) ──────────────────────────

    def get_pending_tasks(self) -> List[Task]:
        """Return all tasks with status ``pending``.

        This is the primary method used by the executor loop to fetch
        work, replacing direct ``inbox.json`` reads.
        """
        tasks = self._load_tasks()
        return [Task(**t) for t in tasks if t.get("status") == "pending"]

    # ── Task status mutation ─────────────────────────────────────────

    def update_task_status(
        self,
        task_id: str,
        status: str,
        *,
        result: str = "",
    ) -> Task | None:
        """Update the status (and optionally result) of a task by id.

        Emits a broadcast event matching the new status:
        - ``"completed"`` -> ``"completed"``
        - ``"failed"``     -> ``"failed"``
        - ``"escalated"``  -> ``"escalated"``
        - anything else    -> ``"status_changed"``

        Returns the updated ``Task`` or ``None`` if not found.
        """
        event_map: dict[str, str] = {
            "completed": "completed",
            "failed": "failed",
            "escalated": "escalated",
        }
        now = datetime.now().isoformat()

        def _updater(tasks: List[dict]) -> List[dict]:
            for i, t in enumerate(tasks):
                if t.get("id") == task_id:
                    old_status = t.get("status", "")
                    tasks[i]["status"] = status
                    tasks[i]["updated_at"] = now
                    if result:
                        tasks[i]["result"] = result
                    if not tasks[i].get("created_at"):
                        tasks[i]["created_at"] = now
                    if status in ("completed", "failed"):
                        tasks[i]["completed_at"] = now
                    task_dict = tasks[i]
                    event = event_map.get(status, "status_changed")
                    self._emit(task_dict, event)
                    logger.info(
                        "Task %s status: %s -> %s",
                        task_id, old_status, status,
                    )
            return tasks

        updated = self._mutate_tasks(_updater)
        for t in updated:
            if t.get("id") == task_id:
                return Task(**t)
        return None

    # ── Query helpers ────────────────────────────────────────────────

    def get_task_by_id(self, task_id: str) -> Task | None:
        """Find a specific task by its ``id`` field."""
        tasks = self._load_tasks()
        for t in tasks:
            if t.get("id") == task_id:
                return Task(**t)
        return None

    def get_subtasks(self, parent_task_id: str) -> List[Task]:
        """Return all tasks whose ``parent_task_id`` matches."""
        tasks = self._load_tasks()
        return [
            Task(**t) for t in tasks if t.get("parent_task_id") == parent_task_id
        ]

    def get_unacknowledged(self, agent_id: str) -> List[Task]:
        """Return tasks assigned to *agent_id* that have not been ACKed yet."""
        tasks = self._load_tasks()
        return [
            Task(**t)
            for t in tasks
            if t.get("receiver_id") == agent_id and not t.get("acknowledged_by")
        ]

    def acknowledge_task(self, task_id: str, agent_id: str) -> Task | None:
        """Mark a task as acknowledged by *agent_id*.

        Returns the updated ``Task`` or ``None`` if not found.
        """
        def _updater(tasks: List[dict]) -> List[dict]:
            for i, t in enumerate(tasks):
                if t.get("id") == task_id:
                    tasks[i]["acknowledged_by"] = agent_id
            return tasks

        updated = self._mutate_tasks(_updater)
        for t in updated:
            if t.get("id") == task_id:
                return Task(**t)
        return None

    def count_by_status(self) -> dict[str, int]:
        """Return a mapping of status name -> count across all tasks."""
        tasks = self._load_tasks()
        counter: Counter[str] = Counter()
        for t in tasks:
            status = t.get("status", "pending")
            counter[status] += 1
        return dict(counter)
