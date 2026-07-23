"""Dead-letter queue for stale tasks (GAP-017).

Tasks that remain ``in_progress`` beyond ``STALE_THRESHOLD_MINUTES`` are
considered dead and moved to ``.opencode/dead_letter.json`` for later
inspection or retry.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)

# Default threshold: 30 minutes
STALE_THRESHOLD_MINUTES: int = 30

DEFAULT_DLQ_PATH: str = ".opencode/dead_letter.json"


class DeadLetterQueue:
    """Manages the dead-letter file for stale / failed tasks.

    Uses FileStore for atomic, lock-safe persistence (R4 fix).
    """

    def __init__(self, dlq_path: str = DEFAULT_DLQ_PATH) -> None:
        self.dlq_path = Path(dlq_path)
        self.dlq_path.parent.mkdir(parents=True, exist_ok=True)
        self._store = FileStore(self.dlq_path.parent, backup=True)
        self._dlq_name = self.dlq_path.name
        if not self._store.exists(self._dlq_name):
            self._save_entries([])

    # ── Persistence ──────────────────────────────────────────────────

    def _load_entries(self) -> list[dict[str, Any]]:
        data = self._store.read_json(self._dlq_name)
        if data is None:
            return []
        if not isinstance(data, list):
            logger.warning("Corrupt DLQ data — returning empty list.")
            return []
        return data

    def _save_entries(self, entries: list[dict[str, Any]]) -> None:
        self._store.write_json(self._dlq_name, entries)

    # ── Public API ───────────────────────────────────────────────────

    def move_task(self, task_data: dict[str, Any], reason: str) -> dict[str, Any]:
        """Move *task_data* into the dead-letter queue.

        A ``dead_letter`` wrapper is returned containing the original task
        data plus metadata (moved_at, reason).
        """
        now = datetime.now().isoformat()
        entry = {
            "task": task_data,
            "moved_at": now,
            "reason": reason,
        }
        entries = self._load_entries()
        entries.append(entry)
        self._save_entries(entries)
        logger.warning("Task %s moved to DLQ: %s", task_data.get("id", "?"), reason)
        return entry

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
        """Remove a task from the DLQ and return it (for re-enqueueing).

        Returns the original task dict, or ``None`` if not found.
        """
        entries = self._load_entries()
        restored: dict[str, Any] | None = None
        new_entries: list[dict[str, Any]] = []
        for entry in entries:
            task = entry.get("task", {})
            if task.get("id") == task_id and restored is None:
                restored = task
            else:
                new_entries.append(entry)
        if restored is not None:
            self._save_entries(new_entries)
            logger.info("Task %s removed from DLQ for retry.", task_id)
        return restored

    def clear(self) -> int:
        """Remove all entries. Returns the number of entries removed."""
        count = len(self._load_entries())
        self._save_entries([])
        return count


def detect_stale_tasks(
    bus: Any,
    dlq: DeadLetterQueue,
    threshold_minutes: int = STALE_THRESHOLD_MINUTES,
) -> list[dict[str, Any]]:
    """Scan the task bus for ``in_progress`` tasks older than *threshold_minutes*.

    Each stale task is moved to the DLQ **and** removed from the inbox.
    Returns the list of moved task dicts.

    Args:
        bus: A MessageBus instance (or any object with `get_all_tasks_raw()`
            and `_mutate_tasks()` methods).
        dlq: The dead-letter queue to receive stale tasks.
        threshold_minutes: Minutes of inactivity before a task is stale.
    """
    tasks: list[dict[str, Any]] = bus.get_all_tasks_raw()

    now = datetime.now()
    cutoff = now - timedelta(minutes=threshold_minutes)
    stale_ids: set[str] = set()
    moved: list[dict[str, Any]] = []

    for task in tasks:
        if task.get("status") != "in_progress":
            continue

        # Check timestamps — prefer updated_at, fall back to created_at
        ts_str = task.get("updated_at") or task.get("created_at") or ""
        if not ts_str:
            # No timestamp at all → treat as stale
            stale_ids.add(task.get("id", ""))
            reason = "No timestamp — assumed stale"
            dlq.move_task(task, reason)
            moved.append(task)
            continue

        try:
            ts = datetime.fromisoformat(ts_str)
        except (ValueError, TypeError):
            stale_ids.add(task.get("id", ""))
            reason = f"Unparseable timestamp '{ts_str}'"
            dlq.move_task(task, reason)
            moved.append(task)
            continue

        if ts < cutoff:
            stale_ids.add(task.get("id", ""))
            elapsed = (now - ts).total_seconds() / 60
            reason = f"Stale after {elapsed:.0f} minutes (threshold: {threshold_minutes}m)"
            dlq.move_task(task, reason)
            moved.append(task)

    if stale_ids:
        # Remove stale tasks from the inbox via MessageBus
        def _remove_stale(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
            return [t for t in (data or []) if t.get("id") not in stale_ids]

        bus._mutate_tasks(_remove_stale)
        logger.info("Moved %d stale tasks to DLQ.", len(moved))

    return moved
