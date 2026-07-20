"""SQLite-backed escalation store — replaces YAML-based EscalationManager storage.

Persists escalation rules and events in SQLite while providing a
compatible interface for the existing EscalationManager.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from ai_company.data.database import Database

logger = logging.getLogger(__name__)


class EscalationStore:
    """SQLite-backed escalation event storage.

    Args:
        database: An initialised :class:`Database` instance.
    """

    def __init__(self, database: Database) -> None:
        self._db = database

    # ── Event CRUD ────────────────────────────────────────────────────

    def add_event(
        self,
        task_id: str,
        rule_id: str,
        from_agent: str,
        to_agent: str,
        reason: str,
        timestamp: str | None = None,
        resolved: bool = False,
    ) -> None:
        """Persist an escalation event."""
        ts = timestamp or datetime.now().isoformat()
        self._db.execute(
            """INSERT OR REPLACE INTO escalation_events
               (task_id, rule_id, from_agent, to_agent, reason, timestamp, resolved)
               VALUES (?,?,?,?,?,?,?)""",
            (task_id, rule_id, from_agent, to_agent, reason, ts, int(resolved)),
        )
        self._db.commit()

    def get_pending(self) -> list[dict[str, Any]]:
        """Return all unresolved escalation events."""
        return self._db.fetchall(
            "SELECT * FROM escalation_events WHERE resolved = 0 ORDER BY timestamp DESC"
        )

    def get_resolved(self) -> list[dict[str, Any]]:
        """Return all resolved escalation events."""
        return self._db.fetchall(
            "SELECT * FROM escalation_events WHERE resolved = 1 ORDER BY timestamp DESC"
        )

    def get_by_task(self, task_id: str) -> list[dict[str, Any]]:
        """Return all escalation events for a task."""
        return self._db.fetchall(
            "SELECT * FROM escalation_events WHERE task_id = ? ORDER BY timestamp ASC",
            (task_id,),
        )

    def get_by_agent(self, agent_id: str) -> list[dict[str, Any]]:
        """Return escalation events where *agent_id* is the target."""
        return self._db.fetchall(
            "SELECT * FROM escalation_events WHERE to_agent = ? ORDER BY timestamp DESC",
            (agent_id,),
        )

    def resolve(self, task_id: str) -> int:
        """Mark all events for a task as resolved. Returns count updated."""
        cursor = self._db.execute(
            "UPDATE escalation_events SET resolved = 1 WHERE task_id = ?",
            (task_id,),
        )
        self._db.commit()
        return cursor.rowcount

    def count_pending(self) -> int:
        """Count unresolved escalations."""
        row = self._db.fetchone(
            "SELECT COUNT(*) as cnt FROM escalation_events WHERE resolved = 0"
        )
        return row["cnt"] if row else 0

    def count(self) -> int:
        """Total number of escalation events."""
        return self._db.table_count("escalation_events")

    def delete_before(self, cutoff_date: str) -> int:
        """Delete resolved events older than *cutoff_date*. Returns count deleted."""
        cursor = self._db.execute(
            "DELETE FROM escalation_events WHERE resolved = 1 AND timestamp < ?",
            (cutoff_date,),
        )
        self._db.commit()
        return cursor.rowcount

    # ── Migration helpers ─────────────────────────────────────────────

    def import_from_yaml(self, yaml_path: str | Path) -> int:
        """Import escalation events from the legacy YAML config.

        Returns the number of events imported.
        """
        import yaml

        path = Path(yaml_path)
        if not path.exists():
            logger.warning("Legacy escalation config not found: %s", path)
            return 0

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        raw_events = data.get("events", [])
        count = 0
        for e in raw_events:
            ts = e.get("timestamp", "")
            if isinstance(ts, datetime):
                ts = ts.isoformat()
            self.add_event(
                task_id=e.get("task_id", ""),
                rule_id=e.get("rule_id", ""),
                from_agent=e.get("from_agent", ""),
                to_agent=e.get("to_agent", ""),
                reason=e.get("reason", ""),
                timestamp=str(ts),
                resolved=e.get("resolved", False),
            )
            count += 1

        logger.info("Imported %d escalation events from %s", count, path)
        return count

    def export_to_yaml(self, yaml_path: str | Path) -> Path:
        """Export all escalation events to the legacy YAML format.

        Returns the path of the written file.
        """
        import yaml

        events = self._db.fetchall(
            "SELECT * FROM escalation_events ORDER BY timestamp ASC"
        )
        path = Path(yaml_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "events": [
                {
                    "task_id": e["task_id"],
                    "rule_id": e["rule_id"],
                    "from_agent": e["from_agent"],
                    "to_agent": e["to_agent"],
                    "reason": e["reason"],
                    "timestamp": e["timestamp"],
                    "resolved": bool(e["resolved"]),
                }
                for e in events
            ]
        }

        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

        logger.info("Exported %d escalation events to %s", len(events), path)
        return path
