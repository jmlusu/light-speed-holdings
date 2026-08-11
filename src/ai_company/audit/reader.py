"""JSONL reader for audit events with flexible filtering."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from ai_company.audit.events import AuditEvent, AuditEventType

logger = logging.getLogger(__name__)


class AuditReader:
    """Reads AuditEvents from a JSONL file with optional filters.

    Malformed lines are skipped with a warning rather than raising so
    that partial corruption does not block the entire read.
    """

    def __init__(self, path: str | Path = ".opencode/audit.jsonl") -> None:
        self._path = Path(path)

    @property
    def path(self) -> Path:
        """Return the path of the JSONL file."""
        return self._path

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def read_all(self) -> list[AuditEvent]:
        """Return every valid event in the file."""
        return self._read_lines()

    def read_by_task(self, task_id: str) -> list[AuditEvent]:
        """Return events whose task_id matches *task_id*."""
        return [e for e in self._read_lines() if e.task_id == task_id]

    def read_by_agent(self, agent_id: str) -> list[AuditEvent]:
        """Return events whose agent_id matches *agent_id*."""
        return [e for e in self._read_lines() if e.agent_id == agent_id]

    def read_by_type(self, event_type: str) -> list[AuditEvent]:
        """Return events whose event_type matches *event_type*.

        *event_type* is a plain string (e.g. ``"tool_call"``) that will
        be validated against the ``AuditEventType`` enum.
        """
        target = AuditEventType(event_type)
        return [e for e in self._read_lines() if e.event_type == target]

    def read_since(self, since: str) -> list[AuditEvent]:
        """Return events whose timestamp is >= *since* (ISO 8601 string)."""
        return [e for e in self._read_lines() if e.timestamp >= since]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _read_lines(self) -> list[AuditEvent]:
        """Parse the JSONL file into a list of AuditEvent objects."""
        if not self._path.exists():
            return []

        events: list[AuditEvent] = []

        with open(self._path, "r", encoding="utf-8") as fh:
            for line_no, raw_line in enumerate(fh, start=1):
                stripped = raw_line.strip()
                if not stripped:
                    continue
                try:
                    data = json.loads(stripped)
                    events.append(AuditEvent.model_validate(data))
                except (json.JSONDecodeError, ValueError) as exc:
                    logger.warning(
                        "Skipping malformed audit line %d in %s: %s",
                        line_no,
                        self._path,
                        exc,
                    )

        return events
