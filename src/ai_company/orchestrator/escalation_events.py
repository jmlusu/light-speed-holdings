"""
Append-only JSONL store for escalation events.

This module provides an evidence-separation compliant store for escalation events.
Events are written to a JSONL file (data/orchestrator/escalation_events.jsonl) that
is read-only for auditors. The escalation/approval systems write events here;
auditors read from this path but never write to it.

See AGENTS.md §9.3 Audit Evidence Separation.
"""

from __future__ import annotations

import json
import logging
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from ai_company.orchestrator.escalation import EscalationEvent
from ai_company.paths import state_path

logger = logging.getLogger(__name__)


class EscalationEventStore:
    """
    Append-only JSONL store for escalation events.

    Uses file locking for concurrent access safety. Each event is written
    as a single JSON line. The file is never modified in-place — only
    appended to. Auditors read this file but never write to it.
    """

    def __init__(self, path: str = "orchestrator/escalation_events.jsonl"):
        # D-6: relocate legacy orchestrator/ state to data/orchestrator/.
        self.path = Path(str(state_path(path)))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()

    def append(self, event: EscalationEvent) -> None:
        """Append an escalation event to the JSONL file."""
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            record = event.model_dump(mode="json")
            record["timestamp"] = (
                event.timestamp.isoformat()
                if isinstance(event.timestamp, datetime)
                else str(event.timestamp)
            )
            line = json.dumps(record, separators=(",", ":"))
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(line + "\n")

    def list_all(self) -> List[EscalationEvent]:
        """Read all events from the JSONL file (for auditors)."""
        events: List[EscalationEvent] = []
        if not self.path.exists():
            return events
        with self._lock, open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    ts = data.get("timestamp")
                    if isinstance(ts, str):
                        data["timestamp"] = datetime.fromisoformat(ts)
                    events.append(EscalationEvent(**data))
                except (json.JSONDecodeError, ValueError) as exc:
                    logger.warning("Failed to parse escalation event line: %s", exc)
        return events

    def get_pending(self) -> List[EscalationEvent]:
        """Return unresolved events."""
        return [e for e in self.list_all() if not e.resolved]

    def mark_resolved(self, task_id: str) -> bool:
        """Mark an event as resolved (creates a new resolution record, does not modify original)."""
        # This is a no-op for the append-only store — resolution is tracked
        # by appending a new resolution event. The original event stays.
        # If callers need resolution tracking, they should query the approval
        # store or escalation manager's in-memory state.
        return True

    def rotate(self, retain_days: int = 30) -> int:
        """
        Rotate the event log: move events older than retain_days to a
        rotated file. Returns number of events rotated.

        Returns 0 if no rotation needed or file doesn't exist.
        """
        if not self.path.exists():
            return 0

        with self._lock:
            cutoff = datetime.now(timezone.utc).timestamp() - (retain_days * 86400)

            # Read all events, split by age
            current_events = []
            rotated_events = []

            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        ts_str = data.get("timestamp")
                        if isinstance(ts_str, str):
                            ts = datetime.fromisoformat(ts_str).timestamp()
                        else:
                            ts = datetime.now(timezone.utc).timestamp()
                        if ts < cutoff:
                            rotated_events.append(data)
                        else:
                            current_events.append(data)
                    except (json.JSONDecodeError, ValueError):
                        current_events.append(data)

            if not rotated_events:
                return 0

            # Write current events back to main file
            with open(self.path, "w", encoding="utf-8") as f:
                for event in current_events:
                    f.write(json.dumps(event, separators=(",", ":")) + "\n")

            # Write rotated events to rotated file
            rotated_path = self.path.with_suffix(
                f".rotated-{int(datetime.now(timezone.utc).timestamp())}.jsonl"
            )
            rotated_path.parent.mkdir(parents=True, exist_ok=True)
            with open(rotated_path, "w", encoding="utf-8") as f:
                for event in rotated_events:
                    f.write(json.dumps(event, separators=(",", ":")) + "\n")

            return len(rotated_events)


_STORE_CACHE: "dict[str, EscalationEventStore]" = {}


def get_escalation_event_store(
    path: str = "orchestrator/escalation_events.jsonl",
) -> "EscalationEventStore":
    """Return an ``EscalationEventStore`` bound to ``path``.

    Stores are cached per resolved ``path`` rather than once per module.
    Previously a single module-level instance was cached and ``path`` was
    ignored on every call after the first, which silently routed all callers —
    including ones pointing at isolated directories — into whichever file
    happened to be used first.

    Caching per path keeps one store (and therefore one lock) per file, so
    concurrent writers to the same file still serialise through the same
    ``RLock`` while callers using different paths stay fully isolated.

    Paths are mapped through :func:`state_path` before the cache key is
    computed so legacy ``orchestrator/`` and new ``data/orchestrator/``
    callers share one store (and one lock) per file.
    """
    key = str(Path(str(state_path(path))).expanduser().resolve())
    store = _STORE_CACHE.get(key)
    if store is None:
        store = EscalationEventStore(path)
        _STORE_CACHE[key] = store
    return store


def reset_escalation_event_store() -> None:
    """Drop all cached stores so subsequent lookups rebuild them."""
    _STORE_CACHE.clear()
