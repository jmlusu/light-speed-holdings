"""Suspend-to-disk store for HITL-parked agent loop state.

When a task is parked in ``WAITING_APPROVAL`` the executor serialises the
agent loop's conversation history, iteration metadata, and cost accumulators
to ``.opencode/suspended_states/{task_id}.json``.  On resume the state is
loaded and passed back to ``AgentLoop.run()`` so the loop continues from
where it left off instead of re-executing every iteration from scratch.

Retention: the daemon's governance sweep calls :meth:`SuspendStore.sweep_expired`
to remove files older than 30 days.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator

from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)

_DEFAULT_DIR = ".opencode/suspended_states"
_MAX_STATE_BYTES = 1 * 1024 * 1024  # 1 MB cap


class SuspendedState(BaseModel):
    """Persisted agent loop state for a parked task.

    All fields are JSON-serialisable.  ``conversation_history`` is the
    list of strings that forms the LLM context window (initial user prompt,
    tool-result feedback, iteration feedback).  On resume the loop
    initialises from this list and continues from ``iterations_completed + 1``.
    """

    task_id: str
    conversation_history: list[str] = Field(default_factory=list)
    iterations_completed: int = 0
    tool_results: list[dict[str, Any]] = Field(default_factory=list)
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_cost_usd: float = 0.0
    parked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    agent_name: str = ""
    priority: str = "medium"

    @field_validator("parked_at", mode="after")
    @classmethod
    def _ensure_utc(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)


class SuspendStore:
    """File-backed store for suspended agent loop state.

    Uses ``FileStore`` for atomic writes (temp + rename) so a crash mid-write
    can never leave a truncated state file behind.

    Args:
        state_dir: Directory for suspended state files.
        retain_days: Days before a suspended state file is swept.
    """

    def __init__(
        self,
        state_dir: str = _DEFAULT_DIR,
        retain_days: int = 30,
    ) -> None:
        self._dir = Path(state_dir)
        self._store = FileStore(str(self._dir), backup=True)
        self.retain_days = retain_days

    def _file_name(self, task_id: str) -> str:
        """Return the JSON filename for a task's suspended state."""
        return f"{task_id}.json"

    def save(self, task_id: str, state: SuspendedState) -> None:
        """Persist suspended state to disk (atomic write).

        If the serialised state exceeds ``_MAX_STATE_BYTES`` the oldest
        iterations are truncated from the front of ``conversation_history``
        to fit.
        """
        state.task_id = task_id
        data = state.model_dump(mode="json")

        # Enforce size cap by truncating oldest conversation entries.
        serialised = _dumps_json(data)
        if len(serialised.encode("utf-8")) > _MAX_STATE_BYTES:
            state.conversation_history = _truncate_history(
                state.conversation_history, _MAX_STATE_BYTES
            )
            data = state.model_dump(mode="json")

        self._store.write_json(self._file_name(task_id), data)
        logger.info(
            "Suspended state saved for task %s (%d iterations, %d history entries)",
            task_id,
            state.iterations_completed,
            len(state.conversation_history),
        )

    def load(self, task_id: str) -> Optional[SuspendedState]:
        """Load suspended state from disk. Returns ``None`` if not found."""
        data = self._store.read_json(self._file_name(task_id))
        if data is None or not isinstance(data, dict):
            return None
        try:
            return SuspendedState(**data)
        except Exception:  # noqa: BLE001 - corrupt file treated as missing
            logger.warning(
                "Corrupt suspended state for task %s; treating as missing",
                task_id,
                exc_info=True,
            )
            return None

    def delete(self, task_id: str) -> None:
        """Remove a suspended state file after successful resume."""
        file_path = self._dir / self._file_name(task_id)
        try:
            if file_path.exists():
                file_path.unlink()
                logger.debug("Deleted suspended state for task %s", task_id)
        except OSError:  # pragma: no cover - best-effort cleanup
            logger.warning("Failed to delete suspended state for task %s", task_id)

    def sweep_expired(self, retain_days: int | None = None) -> int:
        """Remove suspended state files older than the retention window.

        Returns the number of files removed.  Best-effort: individual
        deletion failures are logged but do not stop the sweep.
        """
        window = retain_days if retain_days is not None else self.retain_days
        if window <= 0:
            return 0

        cutoff = datetime.now(timezone.utc) - timedelta(days=window)
        removed = 0

        if not self._dir.exists():
            return 0

        for file_path in self._dir.glob("*.json"):
            try:
                data = self._store.read_json(file_path.name)
                if not isinstance(data, dict):
                    continue
                parked_at_str = data.get("parked_at", "")
                if not parked_at_str:
                    continue
                parked_at = datetime.fromisoformat(str(parked_at_str))
                if parked_at.tzinfo is None:
                    parked_at = parked_at.replace(tzinfo=timezone.utc)
                if parked_at < cutoff:
                    file_path.unlink()
                    removed += 1
                    logger.info("Swept expired suspended state: %s", file_path.name)
            except Exception:  # noqa: BLE001 - best-effort sweep
                logger.debug("Skipping %s during sweep", file_path.name, exc_info=True)

        return removed

    def list_parked(self) -> list[str]:
        """Return task IDs with suspended state on disk."""
        if not self._dir.exists():
            return []
        return [f.stem for f in self._dir.glob("*.json")]


def _dumps_json(data: dict[str, Any]) -> str:
    """Minimal JSON serialise (stdlib only)."""
    import json

    return json.dumps(data, default=str)


def _truncate_history(history: list[str], max_bytes: int) -> list[str]:
    """Truncate oldest entries from conversation history to fit a byte cap.

    Keeps the most recent entries and the first entry (initial user prompt).
    Returns a new list; does not mutate the input.
    """
    if not history:
        return history

    # Always keep the first entry (initial user prompt).
    first = history[0]
    rest = history[1:]

    # Binary-search from the end to find how many recent entries fit.
    kept: list[str] = []
    total = len(first.encode("utf-8"))
    for entry in reversed(rest):
        entry_bytes = len(entry.encode("utf-8"))
        if total + entry_bytes > max_bytes:
            break
        kept.append(entry)
        total += entry_bytes

    kept.reverse()
    return [first] + kept
