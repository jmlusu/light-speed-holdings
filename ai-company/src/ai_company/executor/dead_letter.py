"""Dead-letter queue for stale tasks (GAP-017).

Tasks that remain ``in_progress`` beyond their lease (or, for legacy
tasks without a lease, beyond ``STALE_THRESHOLD_MINUTES``) are considered
dead and moved to ``.opencode/dead_letter.json`` for later inspection or
retry.

Persistence is lock-guarded and atomic via :class:`FileStore`, moves are
deduplicated by task id, and staleness is lease-aware so a live executor
whose heartbeat is refreshing its lease is never raced by the detector.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ai_company.models.task import Task
from ai_company.store.file_store import FileStore

if TYPE_CHECKING:
    from ai_company.orchestrator.message_bus import MessageBus

logger = logging.getLogger(__name__)

# Default fallback threshold for legacy tasks without a lease: 30 minutes
STALE_THRESHOLD_MINUTES: int = 30

DEFAULT_DLQ_PATH: str = ".opencode/dead_letter.json"


class DeadLetterQueue:
    """Manages the dead-letter file for stale / failed tasks."""

    def __init__(self, dlq_path: str = DEFAULT_DLQ_PATH) -> None:
        self.dlq_path = Path(dlq_path)
        self.dlq_path.parent.mkdir(parents=True, exist_ok=True)
        self._store = FileStore(self.dlq_path.parent, backup=True)
        self._name = self.dlq_path.name
        if not self._store.exists(self._name):
            self._store.write_json(self._name, [])

    # ── Persistence ──────────────────────────────────────────────────

    def _load_entries(self) -> list[dict[str, Any]]:
        data = self._store.read_json(self._name)
        if not isinstance(data, list):
            return []
        return data

    def _update_entries(self, updater: Any) -> list[dict[str, Any]]:
        """Apply *updater* to the DLQ under the exclusive sidecar lock."""
        return self._store.update_json(self._name, lambda data: updater(data or []))

    # ── Public API ───────────────────────────────────────────────────

    def move_task(self, task_data: dict[str, Any], reason: str) -> dict[str, Any]:
        """Move *task_data* into the dead-letter queue.

        Duplicate moves (same task id already present) are ignored so a
        crash between the DLQ move and the inbox deletion can never create
        duplicate entries.  A ``dead_letter`` wrapper is returned
        containing the original task data plus metadata (moved_at, reason).
        """
        now = datetime.now().isoformat()
        entry = {
            "task": task_data,
            "moved_at": now,
            "reason": reason,
        }
        task_id = task_data.get("id")

        def _updater(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
            for existing in entries:
                if existing.get("task", {}).get("id") == task_id:
                    return entries  # already queued -- dedupe
            entries.append(entry)
            return entries

        self._update_entries(_updater)
        logger.warning("Task %s moved to DLQ: %s", task_id, reason)
        return entry

    def has_task(self, task_id: str) -> bool:
        """Return True if a DLQ entry for *task_id* already exists."""
        return self.get_task(task_id) is not None

    def list_entries(self) -> list[dict[str, Any]]:
        """Return all dead-letter entries."""
        return self._load_entries()

    def get_task(self, task_id: str) -> dict[str, Any] | None:
        """Find a DLQ entry by its task id."""
        for entry in self._load_entries():
            task = entry.get("task", {})
            if task.get("id") == task_id:
                return entry
        return None

    def retry_task(self, task_id: str) -> dict[str, Any] | None:
        """Remove all DLQ entries for *task_id* and return the task.

        Returns the original task dict, or ``None`` if not found.
        """
        restored: dict[str, Any] | None = None

        def _updater(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
            nonlocal restored
            kept: list[dict[str, Any]] = []
            for entry in entries:
                task = entry.get("task", {})
                if task.get("id") == task_id:
                    if restored is None:
                        restored = task
                    # drop the entry (and any duplicates)
                else:
                    kept.append(entry)
            return kept

        self._update_entries(_updater)
        if restored is not None:
            logger.info("Task %s removed from DLQ for retry.", task_id)
        return restored

    def clear(self) -> int:
        """Remove all entries. Returns the number of entries removed."""
        count = len(self._load_entries())
        self._store.write_json(self._name, [])
        return count


def retry_dlq_task(
    bus: MessageBus,
    dlq: DeadLetterQueue,
    task_id: str,
) -> dict[str, Any] | None:
    """Re-enqueue a dead-lettered task back into the inbox as pending.

    The task is removed from the DLQ and re-injected through ``bus`` so the
    write is atomic, lock-guarded, and mirrored to SQLite. Claim/lease and
    completion fields are cleared so the task is claimable again. A stale
    inbox copy is removed first (belt-and-braces against a crash between the
    DLQ move and the inbox deletion) so ``send_task`` can never duplicate it.

    Returns the restored task dict, or ``None`` if not found in the DLQ.
    """
    restored = dlq.retry_task(task_id)
    if restored is None:
        return None

    restored["status"] = "pending"
    restored["updated_at"] = datetime.now().isoformat()
    restored.pop("completed_at", None)
    restored.pop("result", None)
    restored.pop("claimed_by", None)
    restored.pop("lease_expires_at", None)

    resolved_id = str(restored.get("id", ""))
    if resolved_id:
        bus.delete_task(resolved_id)
    bus.send_task(Task(**restored))
    logger.info("Task %s re-enqueued as pending after DLQ retry.", resolved_id)
    return restored


def _task_is_stale(
    task: dict[str, Any],
    now: datetime,
    threshold_minutes: int,
) -> str:
    """Return a stale reason string, or ``""`` if the task is not stale.

    Lease-aware: a task with an unexpired ``lease_expires_at`` (refreshed
    by the owning executor's heartbeat) is considered live and not stale.
    Legacy ``in_progress`` tasks without a lease fall back to the
    ``updated_at``/``created_at`` age threshold.
    """
    lease = task.get("lease_expires_at") or ""
    if lease:
        try:
            lease_ts = datetime.fromisoformat(lease)
        except (ValueError, TypeError):
            return "Unparseable lease timestamp"
        if lease_ts > now:
            return ""
        return f"Lease expired at {lease}"
    ts_str = task.get("updated_at") or task.get("created_at") or ""
    if not ts_str:
        return "No timestamp — assumed stale"
    try:
        ts = datetime.fromisoformat(ts_str)
    except (ValueError, TypeError):
        return f"Unparseable timestamp '{ts_str}'"
    if ts >= now - timedelta(minutes=threshold_minutes):
        return ""
    elapsed = (now - ts).total_seconds() / 60
    return f"Stale after {elapsed:.0f} minutes (threshold: {threshold_minutes}m)"


def detect_stale_tasks(
    bus: MessageBus,
    dlq: DeadLetterQueue,
    threshold_minutes: int = STALE_THRESHOLD_MINUTES,
) -> list[dict[str, Any]]:
    """Scan the inbox via *bus* for ``in_progress`` tasks with an expired lease.

    Each stale task is moved to the DLQ (deduplicated) **and** removed from
    the inbox.  If a task is already present in the DLQ (e.g. a previous
    run crashed between the move and the inbox deletion), the inbox copy is
    simply cleaned up and the task is not re-moved.

    Returns the list of moved task dicts.
    """
    try:
        tasks: list[dict[str, Any]] = bus.get_all_tasks_raw()
    except (OSError, json.JSONDecodeError):
        return []

    now = datetime.now()
    moved: list[dict[str, Any]] = []

    for task in tasks:
        if task.get("status") != "in_progress":
            continue
        task_id = str(task.get("id", ""))
        reason = _task_is_stale(task, now, threshold_minutes)
        if not reason:
            continue

        if dlq.has_task(task_id):
            # Crash recovery: the DLQ already holds this task; just remove
            # the stale inbox copy.
            bus.delete_task(task_id)
            continue

        dlq.move_task(task, reason)
        bus.delete_task(task_id)
        moved.append(task)

    if moved:
        logger.info("Moved %d stale tasks to DLQ.", len(moved))

    return moved
