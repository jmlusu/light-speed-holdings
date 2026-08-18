"""SQLite-backed audit store — drop-in replacement for AuditWriter/AuditReader.

Provides append-only event storage with efficient indexed queries by
task, agent, date range, and event type.  Supports log rotation via
database archival (export old events, then delete).
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone
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
        rows = self._db.fetchall("SELECT * FROM audit_events ORDER BY timestamp ASC")
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

    # ── FTS5 Search API ──────────────────────────────────────────────────

    def search_events(self, query: str, limit: int = 50) -> list[dict[str, Any]]:
        """Search audit events using FTS5 full-text search."""
        if self._db:
            try:
                import sqlite3

                fts_rows = self._db.fetchall(
                    """SELECT e.* FROM audit_events e
                       JOIN audit_events_fts f ON f.rowid = e.rowid
                       WHERE audit_events_fts MATCH ?
                       ORDER BY e.timestamp DESC
                       LIMIT ?""",
                    (query, limit),
                )
                return [dict(r) for r in fts_rows]
            except (sqlite3.OperationalError, AttributeError):
                # FTS5 not available, fallback to LIKE search
                pass
        # Fallback: simple LIKE search on file-based audit
        all_events = self.read_all()
        query_lower = query.lower()
        matching_events: list[AuditEvent] = [
            e
            for e in all_events
            if query_lower in str(e.args).lower()
            or query_lower in str(e.result).lower()
            or query_lower in str(e.tool or "").lower()
        ][:limit]
        return [e.model_dump() for e in matching_events]

    def get_timeline(
        self,
        limit: int = 100,
        agent_id: str | None = None,
        status: str | None = None,
        task_type: str | None = None,
        time_range: str = "24h",
    ) -> list[dict[str, Any]]:
        """Get execution timeline entries with filtering."""
        # Calculate time range
        now = datetime.now(timezone.utc)
        if time_range.endswith("h"):
            hours = int(time_range[:-1])
            start = now - timedelta(hours=hours)
        elif time_range.endswith("d"):
            days = int(time_range[:-1])
            start = now - timedelta(days=days)
        else:
            start = now - timedelta(hours=24)

        start_str = start.strftime("%Y-%m-%d %H:%M:%S")

        query = "SELECT * FROM audit_events WHERE timestamp >= ?"
        params = [start_str]

        if agent_id:
            query += " AND agent_id = ?"
            params.append(agent_id)
        if task_type:
            query += " AND event_type = ?"
            params.append(task_type)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(str(limit))

        if self._db:
            rows = self._db.fetchall(query, tuple(params))
            return [dict(r) for r in rows]
        else:
            all_events = self.read_all()
            filtered = [e for e in all_events if e.timestamp >= start_str]
            if agent_id:
                filtered = [e for e in filtered if e.agent_id == agent_id]
            if task_type:
                filtered = [e for e in filtered if e.event_type == task_type]
            return [e.model_dump() for e in filtered[:limit]]

    def get_execution_detail(self, task_id: str) -> dict[str, Any]:
        """Get full execution detail for a specific task."""
        events = self.read_by_task(task_id)

        tool_calls = []
        llm_calls = []
        first_event = None
        last_event = None

        for event in events:
            if not first_event or event.timestamp < first_event.timestamp:
                first_event = event
            if not last_event or event.timestamp > last_event.timestamp:
                last_event = event

            if event.event_type == "tool_call":
                tool_calls.append(
                    {
                        "tool": event.tool or "",
                        "timestamp": event.timestamp,
                        "args": event.args,
                    }
                )
            if event.event_type in ("llm_call", "llm_result"):
                llm_calls.append(
                    {
                        "model": event.args.get("model", ""),
                        "timestamp": event.timestamp,
                        "prompt_tokens": event.args.get("prompt_tokens", 0),
                        "completion_tokens": event.args.get("completion_tokens", 0),
                    }
                )

        duration = 0.0
        if first_event and last_event:
            try:
                t1 = datetime.fromisoformat(first_event.timestamp)
                t2 = datetime.fromisoformat(last_event.timestamp)
                duration = (t2 - t1).total_seconds()
            except (ValueError, TypeError):
                pass

        return {
            "task_id": task_id,
            "duration_seconds": duration,
            "tool_calls": tool_calls,
            "llm_calls": llm_calls,
            "events": [e.model_dump() for e in events],
        }

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

    def _get_metadata_path(self, archive_path: Path) -> Path:
        """Get the path to the archive metadata file."""
        return archive_path.with_suffix(archive_path.suffix + ".meta.json")

    def _read_last_archive_time(self, archive_path: Path) -> str | None:
        """Read the last archive timestamp from metadata file."""
        meta_path = self._get_metadata_path(archive_path)
        if not meta_path.exists():
            return None
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta: dict[str, Any] = json.load(f)
            value = meta.get("last_archive_timestamp")
            return value if isinstance(value, str) else None
        except (json.JSONDecodeError, OSError):
            return None

    def _write_last_archive_time(self, archive_path: Path, timestamp: str) -> None:
        """Write the last archive timestamp to metadata file."""
        meta_path = self._get_metadata_path(archive_path)
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump({"last_archive_timestamp": timestamp}, f)

    def archive_before(self, cutoff_date: str, archive_path: str | Path) -> int:
        """Export events on or before *cutoff_date* to a JSON file, then delete them.

        The export and delete use the same inclusive boundary, so an event at
        exactly ``cutoff_date`` is archived exactly once and never re-exported
        on a subsequent run.

        Tracks the last archive timestamp to only export new events since the
        previous run, avoiding re-scanning already-archived events.

        Returns the number of *newly* archived events.
        """
        archive = Path(archive_path)
        archive.parent.mkdir(parents=True, exist_ok=True)

        # Determine the start timestamp: either the last archive time or the beginning of time
        last_archive_time = self._read_last_archive_time(archive)
        start_time = last_archive_time if last_archive_time is not None else "0000-01-01"

        # Read events since last archive up to cutoff_date
        old_events = self.read_date_range(start_time, cutoff_date)
        if not old_events:
            # Still update the metadata to advance the cursor
            self._write_last_archive_time(archive, cutoff_date)
            return 0

        # Export to archive
        # Load existing archive (for cumulative archive file)
        existing: list[dict[str, Any]] = []
        existing_ids: set[str] = set()
        if archive.exists():
            with open(archive, "r", encoding="utf-8") as f:
                existing = json.load(f)
            for entry in existing:
                if isinstance(entry, dict) and "event_id" in entry:
                    existing_ids.add(entry["event_id"])

        # Filter out events already in archive (safety net for edge cases)
        new_events = [e for e in old_events if e.event_id not in existing_ids]
        if not new_events:
            logger.info(
                "No new events to archive (all %d events already in archive)", len(old_events)
            )
            # Still advance the cursor
            self._write_last_archive_time(archive, cutoff_date)
            return 0

        new_data = [e.model_dump() for e in new_events]
        combined = existing + new_data

        with open(archive, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2, default=str)

        # Delete archived events (inclusive, matching the export boundary)
        self._db.execute(
            "DELETE FROM audit_events WHERE timestamp <= ?",
            (cutoff_date,),
        )
        self._db.commit()

        # Update the last archive timestamp
        self._write_last_archive_time(archive, cutoff_date)

        logger.info(
            "Archived %d new audit events (before %s) to %s",
            len(new_events),
            cutoff_date,
            archive,
        )
        return len(new_events)

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
