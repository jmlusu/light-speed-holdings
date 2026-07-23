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
from ai_company.utils.logging import get_correlation_id

logger = logging.getLogger(__name__)

# Type alias for the optional broadcast callback
BroadcastCallback = Callable[[dict[str, Any], str], None] | None

# Priority sort order for task ordering (R2 fix)
PRIORITY_ORDER: dict[str, int] = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}


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

        appended = False

        def _updater(tasks: List[dict]) -> List[dict]:
            nonlocal appended
            existing_ids = {t.get("id") for t in tasks}
            if task.id in existing_ids:
                logger.warning(
                    "Task %s already exists in inbox — skipping duplicate (correlation=%s).",
                    task.id, task.correlation_id,
                )
                appended = False
                return tasks
            tasks.append(task_dict)
            appended = True
            return tasks

        self._mutate_tasks(_updater)
        if appended:
            logger.info(
                "Task %s sent from [%s] to [%s] (correlation=%s, caller_correlation=%s).",
                task.id,
                task.sender_id,
                task.receiver_id,
                task.correlation_id,
                get_correlation_id(),
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

    def get_all_tasks_raw(self) -> List[dict]:
        """Return raw task dictionaries from the inbox (public method for backward compatibility)."""
        return self._load_tasks()

    # ── Pending tasks (executor integration) ──────────────────────────

    def get_pending_tasks(self) -> List[Task]:
        """Return all tasks with status ``pending``, sorted by priority.

        Priority order: critical > high > medium > low.
        Tasks with a future ``next_retry_at`` are excluded — they are
        waiting for their scheduled retry window.
        This is the primary method used by the executor loop to fetch
        work, replacing direct ``inbox.json`` reads.
        """
        from datetime import datetime as _dt

        now = _dt.now()
        tasks = self._load_tasks()
        pending: list[Task] = []
        for t in tasks:
            if t.get("status") != "pending":
                continue
            next_retry = t.get("next_retry_at", "")
            if next_retry:
                try:
                    retry_time = _dt.fromisoformat(next_retry)
                    if retry_time > now:
                        continue  # not yet ready for retry
                except (ValueError, TypeError):
                    pass
            pending.append(Task(**t))
        pending.sort(key=lambda t: PRIORITY_ORDER.get(t.priority.value, 99))
        return pending

    def claim_next_pending(self) -> Task | None:
        """Atomically find and claim the next pending task by priority.

        For the JSON-backed MessageBus this is an approximation: we load,
        find the highest-priority pending task, mark it ``in_progress``, and save.
        The file lock in ``_mutate_tasks`` serialises concurrent callers,
        so at most one executor wins per tick.

        For true atomic compare-and-swap, use the SQLite-backed TaskStore.
        """
        now = datetime.now().isoformat()
        claimed: Task | None = None

        def _updater(tasks: List[dict]) -> List[dict]:
            nonlocal claimed
            # Sort pending tasks by priority (R2 fix)
            # Skip tasks with a future next_retry_at (R3 fix)
            now_dt = datetime.now()
            pending_indices: list[tuple[int, int]] = []
            for i, t in enumerate(tasks):
                if t.get("status") != "pending":
                    continue
                next_retry = t.get("next_retry_at", "")
                if next_retry:
                    try:
                        retry_time = datetime.fromisoformat(next_retry)
                        if retry_time > now_dt:
                            continue  # not yet ready for retry
                    except (ValueError, TypeError):
                        pass
                pending_indices.append((i, PRIORITY_ORDER.get(t.get("priority", "medium"), 99)))
            pending_indices.sort(key=lambda x: x[1])
            if pending_indices:
                idx = pending_indices[0][0]
                tasks[idx]["status"] = "in_progress"
                tasks[idx]["updated_at"] = now
                claimed = Task(**tasks[idx])
            return tasks

        self._mutate_tasks(_updater)
        if claimed is not None:
            self._emit(claimed.model_dump(), "status_changed")
        return claimed

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

    # ── Task field update (PATCH-style) ──────────────────────────────

    def update_task(self, task_id: str, updates: dict[str, Any]) -> Task | None:
        """Apply arbitrary field updates to a task by id.

        Only keys present in *updates* are written; the rest are left
        untouched.  A ``"status_changed"`` (or matching) event is emitted
        when the status field changes.  Returns the updated ``Task`` or
        ``None`` if not found.
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
                    tasks[i].update(updates)
                    # Only auto-set updated_at if caller didn't provide one
                    if "updated_at" not in updates:
                        tasks[i]["updated_at"] = now
                    if not tasks[i].get("created_at"):
                        tasks[i]["created_at"] = now
                    # If status is being set, track completed_at
                    new_status = tasks[i].get("status", "")
                    if new_status in ("completed", "failed"):
                        tasks[i]["completed_at"] = now
                    event = event_map.get(new_status, "status_changed")
                    self._emit(tasks[i], event)
                    logger.info("Task %s updated: %s", task_id, list(updates.keys()))
            return tasks

        updated = self._mutate_tasks(_updater)
        for t in updated:
            if t.get("id") == task_id:
                return Task(**t)
        return None

    def delete_task(self, task_id: str) -> Task | None:
        """Remove a task from the inbox by id.

        Emits a ``"deleted"`` broadcast event and returns the removed
        ``Task`` object, or ``None`` if not found.
        """
        removed: Task | None = None

        def _updater(tasks: List[dict]) -> List[dict]:
            nonlocal removed
            new_tasks = []
            for t in tasks:
                if t.get("id") == task_id:
                    removed = Task(**t)
                else:
                    new_tasks.append(t)
            return new_tasks

        self._mutate_tasks(_updater)
        if removed is not None:
            logger.info("Task %s deleted", task_id)
            self._emit(removed.model_dump(), "deleted")
        return removed

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

    # ── Retry support (R3 fix) ─────────────────────────────────────

    def retry_task(self, task_id: str, delay_seconds: float) -> Task | None:
        """Schedule a failed task for retry after *delay_seconds*.

        Increments retry_count, computes next_retry_at, and sets status
        back to pending.  Returns the updated Task or None if not found
        or max retries exceeded.
        """
        from datetime import datetime as _dt, timedelta

        def _updater(tasks: List[dict]) -> List[dict]:
            for i, t in enumerate(tasks):
                if t.get("id") == task_id:
                    retry_count = t.get("retry_count", 0) + 1
                    max_retries = t.get("max_retries", 3)
                    if retry_count > max_retries:
                        logger.warning(
                            "Task %s exceeded max retries (%d) — not retrying.",
                            task_id, max_retries,
                        )
                        return tasks
                    next_retry = _dt.now() + timedelta(seconds=delay_seconds)
                    tasks[i]["retry_count"] = retry_count
                    tasks[i]["next_retry_at"] = next_retry.isoformat()
                    tasks[i]["status"] = "pending"
                    tasks[i]["updated_at"] = _dt.now().isoformat()
                    logger.info(
                        "Task %s scheduled for retry %d/%d at %s",
                        task_id, retry_count, max_retries, next_retry.isoformat(),
                    )
                    break
            return tasks

        updated = self._mutate_tasks(_updater)
        for t in updated:
            if t.get("id") == task_id:
                return Task(**t)
        return None

    def get_retryable_tasks(self) -> List[Task]:
        """Return tasks whose next_retry_at has passed and status is pending."""
        from datetime import datetime as _dt

        now = _dt.now()
        tasks = self._load_tasks()
        result = []
        for t in tasks:
            if t.get("status") != "pending":
                continue
            next_retry = t.get("next_retry_at", "")
            if not next_retry:
                continue
            try:
                retry_time = _dt.fromisoformat(next_retry)
                if retry_time <= now:
                    result.append(Task(**t))
            except (ValueError, TypeError):
                continue
        return result

    def count_by_status(self) -> dict[str, int]:
        """Return a mapping of status name -> count across all tasks."""
        tasks = self._load_tasks()
        counter: Counter[str] = Counter()
        for t in tasks:
            status = t.get("status", "pending")
            counter[status] += 1
        return dict(counter)
