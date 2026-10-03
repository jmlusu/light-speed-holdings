"""
Append-only JSONL store for dead-letter queue entries.

This module provides an evidence-separation compliant store for dead-letter
queue entries. Entries are written to a JSONL file (orchestrator/dead_letter.jsonl)
that is read-only for auditors. The executor writes entries here; auditors
read from this path but never write to it.

See AGENTS.md §9.3 Audit Evidence Separation.
"""

from __future__ import annotations

import json
import logging
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class DeadLetterEntry(BaseModel):
    """A single dead-letter queue entry."""

    id: str
    task_id: str
    agent_id: str
    payload: dict[str, Any]
    failure_reason: str
    attempt_count: int = 1
    first_failed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_failed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    resolution_note: Optional[str] = None
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class DeadLetterStore:
    """
    Append-only JSONL store for dead-letter queue entries.

    Uses file locking for concurrent access safety. Each entry is written
    as a single JSON line. The file is never modified in-place — only
    appended to. Auditors read this file but never write to it.

    See AGENTS.md §9.3 Audit Evidence Separation.
    """

    def __init__(self, path: str = "orchestrator/dead_letter.jsonl"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()

    def append(self, entry: DeadLetterEntry) -> None:
        """Append a dead-letter entry to the JSONL file."""
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            record = entry.model_dump(mode="json")
            # Ensure datetime fields are ISO format strings
            for field in ("first_failed_at", "last_failed_at", "resolved_at"):
                val = record.get(field)
                if isinstance(val, datetime):
                    record[field] = val.isoformat()
            line = json.dumps(record, separators=(",", ":"))
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(line + "\n")

    def list_all(self) -> List[DeadLetterEntry]:
        """Read all entries from the JSONL file (for auditors)."""
        entries: List[DeadLetterEntry] = []
        if not self.path.exists():
            return entries
        with self._lock, open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    for field in ("first_failed_at", "last_failed_at", "resolved_at"):
                        ts = data.get(field)
                        if isinstance(ts, str):
                            data[field] = datetime.fromisoformat(ts)
                    entries.append(DeadLetterEntry(**data))
                except (json.JSONDecodeError, ValueError) as exc:
                    logger.warning("Failed to parse dead-letter entry line: %s", exc)
        return entries

    def list_unresolved(self) -> List[DeadLetterEntry]:
        """Return unresolved entries."""
        return [e for e in self.list_all() if not e.resolved]

    def mark_resolved(self, entry_id: str, resolution_note: str = "") -> bool:
        """
        Mark an entry as resolved by appending a resolution record.
        Does not modify the original entry (append-only).
        """
        with self._lock:
            entries = self.list_all()
            for entry in entries:
                if entry.id == entry_id and not entry.resolved:
                    resolved_entry = entry.model_copy(
                        update={
                            "resolved": True,
                            "resolved_at": datetime.now(timezone.utc),
                            "resolution_note": resolution_note,
                        }
                    )
                    self.append(resolved_entry)
                    return True
        return False

    def retry(self, entry_id: str) -> Optional[DeadLetterEntry]:
        """
        Mark an entry for retry by appending a new entry with incremented attempt count.
        Returns the new entry or None if not found.
        """
        with self._lock:
            entries = self.list_all()
            for entry in entries:
                if entry.id == entry_id and not entry.resolved:
                    new_entry = entry.model_copy(
                        update={
                            "id": f"{entry.id}-retry-{entry.attempt_count + 1}",
                            "attempt_count": entry.attempt_count + 1,
                            "last_failed_at": datetime.now(timezone.utc),
                        }
                    )
                    self.append(new_entry)
                    return new_entry
        return None

    def rotate(self, retain_days: int = 90) -> int:
        """
        Rotate the dead-letter log: move entries older than retain_days
        to a rotated file. Returns number of entries rotated.

        Per operations-sop.md §7: rotate monthly; archive older than 90 days.
        """
        if not self.path.exists():
            return 0

        with self._lock:
            cutoff = datetime.now(timezone.utc).timestamp() - (retain_days * 86400)

            current_entries = []
            rotated_entries = []

            if not self.path.exists():
                return 0

            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        ts_str = data.get("first_failed_at")
                        if isinstance(ts_str, str):
                            ts = datetime.fromisoformat(ts_str).timestamp()
                        else:
                            ts = datetime.now(timezone.utc).timestamp()
                        if ts < cutoff:
                            rotated_entries.append(data)
                        else:
                            current_entries.append(data)
                    except (json.JSONDecodeError, ValueError):
                        current_entries.append(data)

            if not rotated_entries:
                return 0

            # Write current entries back to main file
            with open(self.path, "w", encoding="utf-8") as f:
                for entry in current_entries:
                    f.write(json.dumps(entry, separators=(",", ":")) + "\n")

            # Write rotated entries to rotated file
            rotated_path = self.path.with_suffix(
                f".rotated-{int(datetime.now(timezone.utc).timestamp())}.jsonl"
            )
            rotated_path.parent.mkdir(parents=True, exist_ok=True)
            with open(rotated_path, "w", encoding="utf-8") as f:
                for entry in rotated_entries:
                    f.write(json.dumps(entry, separators=(",", ":")) + "\n")

            return len(rotated_entries)


# Module-level singleton
_dead_letter_store: Optional["DeadLetterStore"] = None


def get_dead_letter_store(path: str = "orchestrator/dead_letter.jsonl") -> "DeadLetterStore":
    """Get the module-level singleton DeadLetterStore."""
    global _dead_letter_store
    if _dead_letter_store is None:
        _dead_letter_store = DeadLetterStore(path)
    return _dead_letter_store


def reset_dead_letter_store() -> None:
    """Reset the module-level singleton (used by tests)."""
    global _dead_letter_store
    _dead_letter_store = None
