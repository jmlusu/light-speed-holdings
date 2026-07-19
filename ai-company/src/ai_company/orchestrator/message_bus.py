"""Hardened MessageBus for the AI Company Builder.

Provides a JSON-backed task queue with:
- Atomic writes (write-to-temp-then-rename)
- Correlation IDs for tracing
- Parent/child task linkage
- ACK tracking
- Backup file on every write
- Query helpers for subtasks, unacknowledged tasks, and status counts
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
import uuid
from collections import Counter
from pathlib import Path
from typing import List

from ai_company.models.task import Task

logger = logging.getLogger(__name__)


class MessageBus:
    """JSON-backed task queue with atomic writes and correlation tracking.

    Args:
        storage_path: Path to the inbox JSON file.
    """

    def __init__(self, storage_path: str = ".opencode/inbox.json") -> None:
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self._atomic_write(self.storage_path, "[]")

    # ── Persistence helpers ──────────────────────────────────────────

    def _atomic_write(self, path: Path, data: str) -> None:
        """Write to a temp file in the same directory, then atomically rename.

        On failure the temp file is cleaned up and the exception re-raised.
        """
        tmp_fd, tmp_path = tempfile.mkstemp(
            dir=str(path.parent), suffix=".tmp"
        )
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                f.write(data)
            os.replace(tmp_path, str(path))
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise
        self._write_backup(path)

    def _write_backup(self, path: Path) -> None:
        """Write a ``.bak`` copy of the file after every successful write."""
        bak_path = path.with_suffix(".json.bak")
        try:
            bak_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        except OSError:
            # Backup failure is non-fatal — log and move on.
            logger.warning("Failed to write backup %s", bak_path)

    def _load_tasks(self) -> List[dict]:
        try:
            raw = self.storage_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return []
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            logger.warning("Corrupt inbox file %s — starting fresh.", self.storage_path)
            return []

    def _save_tasks(self, tasks: List[dict]) -> None:
        self._atomic_write(self.storage_path, json.dumps(tasks, indent=2))

    # ── Core API (backward-compatible) ───────────────────────────────

    def send_task(self, task: Task) -> None:
        """Append *task* to the inbox, auto-generating a correlation_id if missing."""
        if not task.correlation_id:
            task.correlation_id = str(uuid.uuid4())
        tasks = self._load_tasks()
        tasks.append(task.model_dump())
        self._save_tasks(tasks)
        logger.info(
            "Task %s sent from [%s] to [%s] (correlation=%s).",
            task.id,
            task.sender_id,
            task.receiver_id,
            task.correlation_id,
        )

    def get_inbox(self, agent_id: str) -> List[Task]:
        """Return all tasks addressed to *agent_id*."""
        tasks = self._load_tasks()
        return [Task(**t) for t in tasks if t.get("receiver_id") == agent_id]

    def get_sent(self, agent_id: str) -> List[Task]:
        """Return all tasks sent by *agent_id*."""
        tasks = self._load_tasks()
        return [Task(**t) for t in tasks if t.get("sender_id") == agent_id]

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
        tasks = self._load_tasks()
        for i, t in enumerate(tasks):
            if t.get("id") == task_id:
                tasks[i]["acknowledged_by"] = agent_id
                self._save_tasks(tasks)
                return Task(**tasks[i])
        return None

    def count_by_status(self) -> dict[str, int]:
        """Return a mapping of status name → count across all tasks."""
        tasks = self._load_tasks()
        counter: Counter[str] = Counter()
        for t in tasks:
            status = t.get("status", "pending")
            counter[status] += 1
        return dict(counter)
