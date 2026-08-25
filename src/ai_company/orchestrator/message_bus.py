"""Hardened MessageBus for the AI Company Builder.

Provides a JSON-backed task queue with:
- Atomic writes via FileStore (write-to-temp-then-rename)
- File locking for concurrent access
- Correlation IDs for tracing
- Parent/child task linkage
- ACK tracking
- Backup file on every write
- Dashboard broadcast hooks for real-time WebSocket updates
"""

from __future__ import annotations

import contextlib
import json
import logging
import os
import time
import uuid
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, List, cast

from ai_company.dashboard.monitoring import inc_metric
from ai_company.data import TaskStore, database_is_usable
from ai_company.models.task import Task, TaskEventType, TaskResult, TaskStatus
from ai_company.paths import get_data_root
from ai_company.store.file_store import FileStore
from ai_company.utils.logging import get_correlation_id

logger = logging.getLogger(__name__)


def _iso_from_timestamp(ts: float) -> str:
    """Format a unix timestamp as ISO-8601 (naive local, matching the rest)."""
    return datetime.fromtimestamp(ts).isoformat()


def _read_text_with_retry(path: Path) -> str | None:
    """Read a text file, retrying transient Windows locking errors.

    Returns the file contents, or ``None`` if the file could not be read
    after several attempts (e.g. another process holds an open handle).
    """
    for _ in range(5):
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, PermissionError):
            time.sleep(0.01)
    return None


# Type alias for the optional broadcast callback
BroadcastCallback = Callable[[dict[str, Any], str], None] | None


class MessageBus:
    """JSON-backed task queue with atomic writes and correlation tracking.

    All file I/O is delegated to :class:`FileStore` for atomic writes and
    file locking, eliminating the risk of partial writes from concurrent
    access.

    SQLite write-through (Sprint 2, S2.1): when a usable :class:`Database`
    is supplied via *database*, every task mutation is also mirrored to the
    SQLite ``tasks`` table (through :class:`TaskStore`) so the data layer
    stays live. The mirror is best-effort — a SQLite failure is logged and
    never breaks the file write. Without *database* the bus behaves exactly
    as before (file only).

    Args:
        storage_path: Path to the inbox JSON file. Defaults to
            ``<data root>/.opencode/inbox.json`` (data root resolved via
            :func:`ai_company.paths.get_data_root`, i.e. ``DASHBOARD_DATA_DIR``
            or the project root) rather than the process CWD.
        broadcast_callback: Optional synchronous callback invoked after
            task mutations.  Receives ``(task_dict, event_type)`` where
            *event_type* is one of ``"created"``, ``"completed"``,
            ``"failed"``, ``"escalated"``.
        database: Optional SQLite database to mirror mutations to.
    """

    def __init__(
        self,
        storage_path: str | None = None,
        broadcast_callback: BroadcastCallback = None,
        database: Any = None,
    ) -> None:
        if storage_path is None:
            # Root-aware default: resolve against the deterministic data root
            # (AI_COMPANY_ROOT / DASHBOARD_DATA_DIR aware) instead of the CWD so
            # the bus can never silently write to an unrelated working directory.
            storage_path = str(get_data_root() / ".opencode" / "inbox.json")
        self.storage_path = Path(storage_path)
        self._store = FileStore(self.storage_path.parent, backup=True)
        self._inbox_name = self.storage_path.name
        self._broadcast_callback = broadcast_callback
        self._task_store = None
        if database_is_usable(database):
            self._task_store = TaskStore(database)

        # Ensure the inbox file exists
        if not self._store.exists(self._inbox_name):
            self._store.write_json(self._inbox_name, [])

    # ── Internal persistence helpers ──────────────────────────────────

    def _load_tasks(self) -> List[dict[str, Any]]:
        """Load tasks from the inbox file, quarantining corrupt JSON.

        On a JSON decode failure (or a non-list payload) the corrupt file is
        renamed to ``inbox.json.bak-<timestamp>`` — never silently dropped —
        and the last good ``inbox.json.bak`` backup is loaded instead.
        Returns the recovered tasks, or ``[]`` only when nothing is
        recoverable.
        """
        # Read under the same sidecar lock used by _mutate_tasks so we can
        # never race a concurrent atomic write, and so quarantine/recovery
        # is serialised with other bus operations.
        with self._store.lock_atomic(self._inbox_name) as full_path:
            raw = _read_text_with_retry(full_path)
            if raw is None:
                return []
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                return self._recover_from_backup(full_path)
            if not isinstance(data, list):
                logger.error(
                    "Corrupt inbox data at %s (expected a JSON list) — "
                    "quarantining and attempting recovery from .bak.",
                    full_path,
                )
                return self._recover_from_backup(full_path)
            return data

    def _recover_from_backup(self, full_path: Path) -> List[dict[str, Any]]:
        """Quarantine a corrupt inbox file and recover tasks from its .bak.

        The corrupt file is atomically renamed to ``<name>.bak-<timestamp>``
        so a crash mid-recovery still leaves the original bytes on disk, then
        the last good ``.bak`` backup is parsed when present.  Returns ``[]``
        only when nothing is recoverable.
        """
        quarantine = full_path.with_name(full_path.name + f".bak-{int(time.time())}")
        logger.error(
            "Corrupt inbox JSON at %s — quarantining to %s and attempting recovery from .bak.",
            full_path,
            quarantine,
        )
        with contextlib.suppress(OSError):
            os.replace(full_path, quarantine)

        bak_path = full_path.with_suffix(full_path.suffix + ".bak")
        if not bak_path.exists():
            return []
        try:
            bak_data = json.loads(bak_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            logger.error("Recovery backup %s is also corrupt.", bak_path)
            return []
        if not isinstance(bak_data, list):
            logger.error("Recovery backup %s is not a JSON list.", bak_path)
            return []
        return bak_data

    def _save_tasks(self, tasks: List[dict[str, Any]]) -> None:
        self._store.write_json(self._inbox_name, tasks)

    def _mutate_tasks(
        self, updater: Callable[[List[dict[str, Any]]], List[dict[str, Any]]]
    ) -> List[dict[str, Any]]:
        """Apply *updater* to the inbox under an exclusive file lock.

        Serialises the read-modify-write cycle so concurrent executor and
        dashboard access cannot corrupt :file:`inbox.json` or lose updates
        (GAP-002).
        """
        return cast(
            List[dict[Any, Any]],
            self._store.update_json(self._inbox_name, lambda data: updater(data or [])),
        )

    def _mirror_task_to_sqlite(self, task_dict: dict[str, Any]) -> None:
        """Upsert a single task into SQLite (write-through mirror)."""
        if self._task_store is None:
            return
        try:
            self._task_store.send_task(Task(**task_dict))
        except Exception:  # noqa: BLE001 - mirror is best-effort
            logger.debug(
                "SQLite task mirror failed for %s", task_dict.get("id", "?"), exc_info=True
            )

    def _mirror_delete_to_sqlite(self, task_id: str) -> None:
        """Delete a task from SQLite (write-through mirror)."""
        if self._task_store is None:
            return
        try:
            self._task_store.delete_task(task_id)
        except Exception:  # noqa: BLE001 - mirror is best-effort
            logger.debug("SQLite task delete mirror failed for %s", task_id, exc_info=True)

    # ── Broadcast helper ─────────────────────────────────────────────

    def _emit(self, task_dict: dict[str, Any], event: str) -> None:
        """Invoke the broadcast callback if one was configured.

        Errors are logged but never raised -- broadcasting is best-effort.
        """
        if self._broadcast_callback is None:
            return
        try:
            self._broadcast_callback(task_dict, event)
        except Exception:  # noqa: BLE001 - broadcasting is best-effort, errors are logged
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
        inc_metric("messages_published_total")

        def _updater(tasks: List[dict[str, Any]]) -> List[dict[str, Any]]:
            tasks.append(task_dict)
            return tasks

        self._mutate_tasks(_updater)
        self._mirror_task_to_sqlite(task_dict)
        logger.info(
            "Task %s sent from [%s] to [%s] (correlation=%s, caller_correlation=%s).",
            task.id,
            task.sender_id,
            task.receiver_id,
            task.correlation_id,
            get_correlation_id(),
        )
        self._emit(task_dict, "created")

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks in the inbox (public method for integration)."""
        tasks = self._load_tasks()
        return [Task(**t) for t in tasks]

    def get_all_tasks_raw(self) -> List[dict[str, Any]]:
        """Return raw task dictionaries from the inbox (public method for backward compatibility)."""
        return self._load_tasks()

    # ── Pending tasks (executor integration) ──────────────────────────

    def get_pending_tasks(self) -> List[Task]:
        """Return all tasks with status ``pending``.

        This is the primary method used by the executor loop to fetch
        work, replacing direct ``inbox.json`` reads.
        """
        tasks = self._load_tasks()
        return [Task(**t) for t in tasks if t.get("status") == "pending"]

    # ── Task claim / lease (executor integration) ─────────────────────

    def claim_task(self, task_id: str, worker_id: str, lease_seconds: int = 1800) -> Task | None:
        """Atomically claim a pending task for *worker_id*.

        Transitions ``pending`` -> ``in_progress`` *only if* the task is
        still pending, so two executors can never claim and process the
        same task.  The claim records the owner and a lease expiry used by
        stale-detection.

        Returns the claimed ``Task``, or ``None`` if the task is missing or
        already claimed/completed.
        """
        now = datetime.now().isoformat()
        expiry = _iso_from_timestamp(time.time() + lease_seconds)
        claimed: list[Task] = []

        def _updater(tasks: List[dict[str, Any]]) -> List[dict[str, Any]]:
            for t in tasks:
                if t.get("id") == task_id:
                    if t.get("status") != "pending":
                        break  # CAS failure -- not claimable
                    t["status"] = "in_progress"
                    t["updated_at"] = now
                    t["claimed_by"] = worker_id
                    t["lease_expires_at"] = expiry
                    claimed.append(Task(**t))
                    break
            return tasks

        self._mutate_tasks(_updater)
        if claimed:
            self._mirror_task_to_sqlite(claimed[0].model_dump())
            logger.info("Task %s claimed by %s (lease %s)", task_id, worker_id, expiry)
            self._emit(claimed[0].model_dump(), "claimed")
            return claimed[0]
        return None

    def heartbeat_task(self, task_id: str, worker_id: str, lease_seconds: int = 1800) -> bool:
        """Refresh the lease on an in-progress task owned by *worker_id*.

        Returns ``True`` if the heartbeat was accepted (task exists, is
        ``in_progress``, and is owned by *worker_id*), ``False`` otherwise.
        """
        now = datetime.now().isoformat()
        expiry = _iso_from_timestamp(time.time() + lease_seconds)
        refreshed = False

        def _updater(tasks: List[dict[str, Any]]) -> List[dict[str, Any]]:
            nonlocal refreshed
            for t in tasks:
                if t.get("id") == task_id:
                    if t.get("status") == "in_progress" and t.get("claimed_by") == worker_id:
                        t["updated_at"] = now
                        t["lease_expires_at"] = expiry
                        refreshed = True
                    break
            return tasks

        updated = self._mutate_tasks(_updater)
        if refreshed:
            for t in updated:
                if t.get("id") == task_id:
                    self._mirror_task_to_sqlite(t)
                    break
        return refreshed

    def resume_task(self, task_id: str, expected_status: str = "waiting_approval") -> Task | None:
        """CAS-guarded transition from *expected_status* to ``pending``.

        Returns the updated ``Task`` if the transition succeeded, or
        ``None`` if the task is missing or not in *expected_status*
        (another executor already resumed it).  This prevents two
        concurrent tick loops from both resuming the same parked task
        (ADR-015 double-resume guard).
        """
        now = datetime.now().isoformat()
        resumed: list[Task] = []

        def _updater(tasks: List[dict[str, Any]]) -> List[dict[str, Any]]:
            for i, t in enumerate(tasks):
                if t.get("id") == task_id:
                    if t.get("status") != expected_status:
                        break  # CAS failure — already resumed or moved
                    tasks[i]["status"] = "pending"
                    tasks[i]["updated_at"] = now
                    resumed.append(Task(**tasks[i]))
                    break
            return tasks

        updated = self._mutate_tasks(_updater)
        if resumed:
            for t in updated:
                if t.get("id") == task_id:
                    self._mirror_task_to_sqlite(t)
                    self._emit(t, "status_changed")
                    break
            logger.info("Task %s resumed (CAS: %s -> pending).", task_id, expected_status)
        return resumed[0] if resumed else None

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
        emitted: list[tuple[dict[str, Any], str]] = []

        def _updater(tasks: List[dict[str, Any]]) -> List[dict[str, Any]]:
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
                        # Terminal states end the lease.
                        tasks[i]["claimed_by"] = ""
                        tasks[i]["lease_expires_at"] = ""
                    task_dict = tasks[i]
                    emitted.append((task_dict, event_map.get(status, "status_changed")))
                    logger.info(
                        "Task %s status: %s -> %s",
                        task_id,
                        old_status,
                        status,
                    )
            return tasks

        updated = self._mutate_tasks(_updater)
        result_task: Task | None = None
        for t in updated:
            if t.get("id") == task_id:
                self._mirror_task_to_sqlite(t)
                result_task = Task(**t)
                break
        # Emit after the lock is released so a slow/stuck callback never
        # stalls task mutations.
        for task_dict, event in emitted:
            self._emit(task_dict, event)
        return result_task

    # ── Query helpers ────────────────────────────────────────────────

    def update_task(self, task_id: str, updates: dict[str, Any]) -> Task | None:
        """Apply a partial update to a task by id.

        Only keys present in *updates* are merged into the task dict.
        Returns the updated ``Task`` or ``None`` if not found.
        """
        now = datetime.now().isoformat()
        emitted: list[tuple[dict[str, Any], str]] = []

        def _updater(tasks: List[dict[str, Any]]) -> List[dict[str, Any]]:
            for i, t in enumerate(tasks):
                if t.get("id") == task_id:
                    tasks[i].update(updates)
                    tasks[i]["updated_at"] = now
                    emitted.append((tasks[i], "updated"))
                    logger.info("Task %s updated: %s", task_id, list(updates.keys()))
            return tasks

        updated = self._mutate_tasks(_updater)
        result_task: Task | None = None
        for t in updated:
            if t.get("id") == task_id:
                self._mirror_task_to_sqlite(t)
                result_task = Task(**t)
                break
        for task_dict, event in emitted:
            self._emit(task_dict, event)
        return result_task

    def delete_task(self, task_id: str) -> Task | None:
        """Remove a task by id.

        Returns the deleted ``Task`` or ``None`` if not found.
        """
        deleted: Task | None = None

        def _updater(tasks: List[dict[str, Any]]) -> List[dict[str, Any]]:
            nonlocal deleted
            new_tasks = []
            for t in tasks:
                if t.get("id") == task_id:
                    deleted = Task(**t)
                else:
                    new_tasks.append(t)
            return new_tasks

        self._mutate_tasks(_updater)
        if deleted:
            self._mirror_delete_to_sqlite(task_id)
            self._emit(deleted.model_dump(), "deleted")
            logger.info("Task %s deleted", task_id)
        return deleted

    def get_task_by_id(self, task_id: str) -> Task | None:
        """Find a specific task by its ``id`` field."""
        tasks = self._load_tasks()
        for t in tasks:
            if t.get("id") == task_id:
                return Task(**t)
        return None

    def acknowledge_task(self, task_id: str, agent_id: str) -> Task | None:
        """Mark a task as acknowledged by *agent_id*.

        Returns the updated ``Task`` or ``None`` if not found.
        """

        def _updater(tasks: List[dict[str, Any]]) -> List[dict[str, Any]]:
            for i, t in enumerate(tasks):
                if t.get("id") == task_id:
                    tasks[i]["acknowledged_by"] = agent_id
            return tasks

        updated = self._mutate_tasks(_updater)
        for t in updated:
            if t.get("id") == task_id:
                self._mirror_task_to_sqlite(t)
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

    # ── Event log (persistent lifecycle history) ─────────────────────

    def log_event(
        self,
        task_id: str,
        event_type: TaskEventType,
        detail: str = "",
        result: TaskResult | None = None,
    ) -> None:
        """Append a lifecycle event to the task's ``_events`` list.

        The event is persisted in the inbox JSON alongside the task so
        consumers (briefing generator, dashboard) can reconstruct the
        full execution history.  Best-effort — errors are logged, not raised.
        """
        entry: dict[str, Any] = {
            "event": event_type.value,
            "timestamp": datetime.now().isoformat(),
        }
        if detail:
            entry["detail"] = detail
        if result is not None:
            entry["result"] = result.model_dump()

        def _updater(tasks: List[dict[str, Any]]) -> List[dict[str, Any]]:
            for t in tasks:
                if t.get("id") == task_id:
                    events = t.setdefault("_events", [])
                    events.append(entry)
                    break
            return tasks

        try:
            self._mutate_tasks(_updater)
            logger.debug("Event logged for task %s: %s", task_id, event_type.value)
        except Exception:  # noqa: BLE001
            logger.debug("Event log failed for task %s", task_id, exc_info=True)

    def get_events(self, task_id: str) -> list[dict[str, Any]]:
        """Return the event history for a task."""
        tasks = self._load_tasks()
        for t in tasks:
            if t.get("id") == task_id:
                raw = t.get("_events", [])
                return cast(list[dict[str, Any]], raw)
        return []

    # ── Retry support ────────────────────────────────────────────────

    def retry_task(self, task_id: str, reason: str = "") -> Task | None:
        """Requeue a failed or timed-out task for retry.

        Increments ``retry_count``, checks against ``retry_budget``, and
        transitions the task back to ``pending``.  Returns the updated
        ``Task`` if retried, or ``None`` if the task is missing,
        not retryable, or the budget is exhausted.

        When the budget is exhausted the task is left in ``failed``
        status and an ``escalated`` event is logged.
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return None
        if task.status not in (TaskStatus.FAILED, TaskStatus.TIMEOUT):
            return None

        budget = task.retry_budget or 3  # default from ADR-015
        if task.retry_count >= budget:
            self.log_event(
                task_id,
                TaskEventType.ESCALATED,
                detail=reason or "Retry budget exhausted",
            )
            self.update_task_status(task_id, "escalated")
            return None

        now = datetime.now().isoformat()

        def _updater(tasks: List[dict[str, Any]]) -> List[dict[str, Any]]:
            for i, t in enumerate(tasks):
                if t.get("id") == task_id:
                    tasks[i]["status"] = "pending"
                    tasks[i]["retry_count"] = t.get("retry_count", 0) + 1
                    tasks[i]["updated_at"] = now
                    tasks[i]["claimed_by"] = ""
                    tasks[i]["lease_expires_at"] = ""
                    break
            return tasks

        updated = self._mutate_tasks(_updater)
        retried: Task | None = None
        for t in updated:
            if t.get("id") == task_id:
                self._mirror_task_to_sqlite(t)
                retried = Task(**t)
                break
        if retried:
            self.log_event(
                task_id,
                TaskEventType.RETRYING,
                detail=reason or f"Retry {retried.retry_count}/{budget}",
            )
            self._emit(retried.model_dump(), "retrying")
            logger.info("Task %s retried (%d/%d)", task_id, retried.retry_count, budget)
        return retried
