"""SQLite-backed audit store — drop-in replacement for AuditWriter/AuditReader.

Provides append-only event storage with efficient indexed queries by
task, agent, date range, and event type.  Supports log rotation via
database archival (export old events, then delete).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from ai_company.audit.events import AuditEvent
from ai_company.data.database import Database

logger = logging.getLogger(__name__)


class AuditStore:
    """SQLite-backed audit event store.

    Args:
        database: An initialised :class:`Database` instance.
    """

    def __init__(self, database: Database) -> None:
        self._db = database

    # ── Write API (matches AuditWriter) ───────────────────────────────

    def write(self, event: AuditEvent) -> None:
        """Append a single event."""
        self.write_batch([event])

    def write_batch(self, events: list[AuditEvent]) -> None:
        """Append multiple events in one transaction."""
        if not events:
            return

        self._db.executemany(
            """INSERT OR REPLACE INTO audit_events
               (event_id, timestamp, event_type, agent_id, task_id,
                tool, args, result, metadata, severity)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            [
                (
                    e.event_id,
                    e.timestamp,
                    e.event_type.value if hasattr(e.event_type, "value") else e.event_type,
                    e.agent_id,
                    e.task_id,
                    e.tool,
                    json.dumps(e.args, default=str),
                    json.dumps(e.result, default=str),
                    json.dumps(e.metadata, default=str),
                    e.severity,
                )
                for e in events
            ],
        )
        self._db.commit()

    # ── Read API (matches AuditReader + extended queries) ─────────────

    def read_all(self) -> list[AuditEvent]:
        """Return every event."""
        rows = self._db.fetchall(
            "SELECT * FROM audit_events ORDER BY timestamp ASC"
        )
        return [self._row_to_event(r) for r in rows]

    def read_by_task(self, task_id: str) -> list[AuditEvent]:
        """Return events for a specific task."""
        rows = self._db.fetchall(
            "SELECT * FROM audit_events WHERE task_id = ? ORDER BY timestamp ASC",
            (task_id,),
        )
        return [self._row_to_event(r) for r in rows]

    def read_by_agent(self, agent_id: str) -> list[AuditEvent]:
        """Return events for a specific agent."""
        rows = self._db.fetchall(
            "SELECT * FROM audit_events WHERE agent_id = ? ORDER BY timestamp ASC",
            (agent_id,),
        )
        return [self._row_to_event(r) for r in rows]

    def read_by_type(self, event_type: str) -> list[AuditEvent]:
        """Return events matching an event type string."""
        rows = self._db.fetchall(
            "SELECT * FROM audit_events WHERE event_type = ? ORDER BY timestamp ASC",
            (event_type,),
        )
        return [self._row_to_event(r) for r in rows]

    def read_since(self, since: str) -> list[AuditEvent]:
        """Return events with timestamp >= *since* (ISO 8601)."""
        rows = self._db.fetchall(
            "SELECT * FROM audit_events WHERE timestamp >= ? ORDER BY timestamp ASC",
            (since,),
        )
        return [self._row_to_event(r) for r in rows]

    def read_date_range(self, start: str, end: str) -> list[AuditEvent]:
        """Return events within [start, end] (ISO 8601 strings)."""
        rows = self._db.fetchall(
            "SELECT * FROM audit_events WHERE timestamp >= ? AND timestamp <= ? ORDER BY timestamp ASC",
            (start, end),
        )
        return [self._row_to_event(r) for r in rows]

    def read_by_severity(self, severity: str) -> list[AuditEvent]:
        """Return events matching a severity level."""
        rows = self._db.fetchall(
            "SELECT * FROM audit_events WHERE severity = ? ORDER BY timestamp ASC",
            (severity,),
        )
        return [self._row_to_event(r) for r in rows]

    def count_by_type(self) -> dict[str, int]:
        """Return a mapping of event_type -> count."""
        rows = self._db.fetchall(
            "SELECT event_type, COUNT(*) as cnt FROM audit_events GROUP BY event_type"
        )
        return {r["event_type"]: r["cnt"] for r in rows}

    def count_by_agent(self) -> dict[str, int]:
        """Return a mapping of agent_id -> count."""
        rows = self._db.fetchall(
            "SELECT agent_id, COUNT(*) as cnt FROM audit_events GROUP BY agent_id"
        )
        return {r["agent_id"]: r["cnt"] for r in rows}

    def count(self) -> int:
        """Total number of audit events."""
        return self._db.table_count("audit_events")

    # ── Migration helpers ─────────────────────────────────────────────

    def import_jsonl(self, jsonl_path: str | Path) -> int:
        """Import events from the legacy ``audit.jsonl`` file.

        Returns the number of events imported.
        """
        path = Path(jsonl_path)
        if not path.exists():
            logger.warning("Legacy audit file not found: %s", path)
            return 0

        events: list[AuditEvent] = []
        with open(path, "r", encoding="utf-8") as fh:
            for line_no, raw_line in enumerate(fh, start=1):
                stripped = raw_line.strip()
                if not stripped:
                    continue
                try:
                    data = json.loads(stripped)
                    events.append(AuditEvent.model_validate(data))
                except (json.JSONDecodeError, ValueError) as exc:
                    logger.warning("Skipping malformed audit line %d: %s", line_no, exc)

        self.write_batch(events)
        logger.info("Imported %d audit events from %s", len(events), path)
        return len(events)

    def export_jsonl(self, jsonl_path: str | Path) -> Path:
        """Export all events to the legacy JSONL format."""
        events = self.read_all()
        path = Path(jsonl_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as fh:
            for event in events:
                fh.write(json.dumps(event.model_dump(), ensure_ascii=False) + "\n")

        logger.info("Exported %d audit events to %s", len(events), path)
        return path

    # ── Log rotation / archival ───────────────────────────────────────

    def archive_before(self, cutoff_date: str, archive_path: str | Path) -> int:
        """Export events older than *cutoff_date* to a JSON file, then delete them.

        Returns the number of events archived.
        """
        old_events = self.read_date_range("0000-01-01", cutoff_date)
        if not old_events:
            return 0

        # Export to archive
        archive = Path(archive_path)
        archive.parent.mkdir(parents=True, exist_ok=True)

        existing: list[dict[str, Any]] = []
        if archive.exists():
            with open(archive, "r", encoding="utf-8") as f:
                existing = json.load(f)

        new_data = [e.model_dump() for e in old_events]
        combined = existing + new_data

        with open(archive, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2, default=str)

        # Delete archived events
        self._db.execute(
            "DELETE FROM audit_events WHERE timestamp < ?",
            (cutoff_date,),
        )
        self._db.commit()

        logger.info(
            "Archived %d audit events (before %s) to %s",
            len(old_events),
            cutoff_date,
            archive,
        )
        return len(old_events)

    # ── Internal helpers ──────────────────────────────────────────────

    @staticmethod
    def _row_to_event(row: dict[str, Any]) -> AuditEvent:
        """Convert a database row dict to an AuditEvent."""
        return AuditEvent(
            event_id=row["event_id"],
            timestamp=row["timestamp"],
            event_type=row["event_type"],
            agent_id=row["agent_id"],
            task_id=row.get("task_id", ""),
            tool=row.get("tool"),
            args=json.loads(row.get("args", "{}")),
            result=json.loads(row.get("result", "{}")),
            metadata=json.loads(row.get("metadata", "{}")),
            severity=row.get("severity", "info"),
        )
