"""Audit Logger — Tamper-Evident Local Audit Trail.

Implements architecture §10, §10.1: hash-preferring audit with SHA256 chaining.
"""

import hashlib
import json
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import TracebackType
from typing import Any, Dict, List, Optional, Type


@dataclass
class AuditEvent:
    """Audit event record (architecture §10.1 schema)."""

    event_id: str
    event_type: str
    timestamp: str
    actor: str
    correlation_id: str
    details: Dict[str, Any]
    payload_hash: str
    prev_hash: str


class AuditLogger:
    """
    Local-only, hash-preferring audit trail (architecture §10, §10.1).

    Features:
    - SHA256 chain (prev_hash = hash of previous record)
    - Configurable retention (90 days CRUD, 365 days gateway)
    - FTS over audit events
    - Chain verification
    - Export with hashes
    """

    EVENT_TYPES = {
        "memory_create",
        "memory_update",
        "memory_delete",
        "memory_search",
        "gateway_request",
        "gateway_approved",
        "gateway_denied",
        "export",
        "import",
        "rebuild",
        "session_inject",
    }

    def __init__(
        self,
        db_path: Path,
        retention_days_crud: int = 90,
        retention_days_gateway: int = 365,
    ):
        self.db_path = Path(db_path)
        self.retention_days_crud = retention_days_crud
        self.retention_days_gateway = retention_days_gateway
        self._conn: Optional[sqlite3.Connection] = None
        self._initialized = False
        self._chain_head: Optional[str] = None

    def initialize(self) -> None:
        """Initialize audit database and verify chain."""
        if self._initialized:
            return

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._conn.row_factory = sqlite3.Row

        self._create_schema()
        self._load_chain_head()
        self._initialized = True

    def _create_schema(self) -> None:
        assert self._conn is not None
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS audit_log (
                rowid INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL UNIQUE,
                event_type TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                actor TEXT NOT NULL,
                correlation_id TEXT NOT NULL,
                details TEXT DEFAULT '{}',
                payload_hash TEXT NOT NULL,
                prev_hash TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_audit_correlation ON audit_log(correlation_id);
            CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp);
            CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit_log(actor);
            CREATE INDEX IF NOT EXISTS idx_audit_event_type ON audit_log(event_type);

            CREATE VIRTUAL TABLE IF NOT EXISTS audit_fts USING fts5(
                event_type, actor, correlation_id,
                content='audit_log',
                content_rowid='rowid'
            );
        """)
        self._conn.commit()

    def _load_chain_head(self) -> None:
        assert self._conn is not None
        row = self._conn.execute(
            "SELECT payload_hash FROM audit_log ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()
        self._chain_head = row["payload_hash"] if row else None

    def _compute_event_hash(self, event: AuditEvent) -> str:
        """Compute SHA256 of canonical event for chain linking."""
        canonical = {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "timestamp": event.timestamp,
            "actor": event.actor,
            "correlation_id": event.correlation_id,
            "details": event.details,
            "payload_hash": event.payload_hash,
        }
        data = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
        return f"sha256:{hashlib.sha256(data.encode()).hexdigest()}"

    def log(
        self,
        event_type: str,
        actor: str,
        correlation_id: str,
        details: Dict[str, Any],
        payload: Optional[Any] = None,
    ) -> AuditEvent:
        """
        Log an audit event.

        Args:
            event_type: One of EVENT_TYPES
            actor: Agent ID or "human"
            correlation_id: UUID linking related operations
            details: Event details (JSON-serializable)
            payload: Optional payload to hash (not stored, only hashed)

        Returns:
            The created AuditEvent
        """
        if not self._initialized:
            self.initialize()

        assert self._conn is not None

        if event_type not in self.EVENT_TYPES:
            raise ValueError(f"Invalid event_type: {event_type}")

        event_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()

        # Compute payload hash
        payload_data = json.dumps(payload, sort_keys=True) if payload is not None else "{}"
        payload_hash = f"sha256:{hashlib.sha256(payload_data.encode()).hexdigest()}"

        # Previous hash in chain
        prev_hash = self._chain_head or "sha256:" + "0" * 64

        event = AuditEvent(
            event_id=event_id,
            event_type=event_type,
            timestamp=timestamp,
            actor=actor,
            correlation_id=correlation_id,
            details=details,
            payload_hash=payload_hash,
            prev_hash=prev_hash,
        )

        # Compute this event's hash for next link
        event_hash = self._compute_event_hash(event)
        self._chain_head = event_hash

        # Insert
        self._conn.execute(
            """
            INSERT INTO audit_log (event_id, event_type, timestamp, actor, correlation_id, details, payload_hash, prev_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                event_id,
                event_type,
                timestamp,
                actor,
                correlation_id,
                json.dumps(details),
                payload_hash,
                prev_hash,
            ),
        )

        # FTS insert - use the auto-generated rowid
        fts_rowid = self._conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        self._conn.execute(
            """
            INSERT INTO audit_fts(rowid, event_type, actor, correlation_id)
            VALUES (?, ?, ?, ?)
        """,
            (fts_rowid, event_type, actor, correlation_id),
        )

        self._conn.commit()
        return event

    def query(
        self,
        event_types: Optional[List[str]] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        actor: Optional[str] = None,
        correlation_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[AuditEvent]:
        """Query audit events with FTS filtering."""
        if not self._initialized:
            self.initialize()

        assert self._conn is not None

        conditions = []
        params: List[Any] = []

        if event_types:
            placeholders = ",".join(["?"] * len(event_types))
            conditions.append(f"event_type IN ({placeholders})")
            params.extend(event_types)

        if start:
            conditions.append("timestamp >= ?")
            params.append(start)
        if end:
            conditions.append("timestamp <= ?")
            params.append(end)
        if actor:
            conditions.append("actor = ?")
            params.append(actor)
        if correlation_id:
            conditions.append("correlation_id = ?")
            params.append(correlation_id)

        where = " AND ".join(conditions) if conditions else "1=1"

        sql = f"""
            SELECT * FROM audit_log
            WHERE {where}
            ORDER BY timestamp DESC
            LIMIT ?
        """
        params.append(limit)

        rows = self._conn.execute(sql, params).fetchall()
        return [self._row_to_event(row) for row in rows]

    def verify_chain(self) -> bool:
        """
        Verify the audit chain integrity.

        Recomputes hash chain from genesis; returns True if valid.
        """
        if not self._initialized:
            self.initialize()

        assert self._conn is not None

        rows = self._conn.execute("SELECT * FROM audit_log ORDER BY timestamp ASC").fetchall()

        expected_prev = "sha256:" + "0" * 64
        for row in rows:
            event = self._row_to_event(row)
            computed_hash = self._compute_event_hash(event)

            if event.prev_hash != expected_prev:
                return False

            expected_prev = computed_hash

        return True

    def export(self, format: str = "jsonl") -> str:
        """Export full audit chain with hashes."""
        if not self._initialized:
            self.initialize()

        assert self._conn is not None

        rows = self._conn.execute("SELECT * FROM audit_log ORDER BY timestamp ASC").fetchall()

        events = [self._row_to_event(row) for row in rows]

        if format == "jsonl":
            lines = []
            for event in events:
                lines.append(
                    json.dumps(
                        {
                            "event_id": event.event_id,
                            "event_type": event.event_type,
                            "timestamp": event.timestamp,
                            "actor": event.actor,
                            "correlation_id": event.correlation_id,
                            "details": event.details,
                            "payload_hash": event.payload_hash,
                            "prev_hash": event.prev_hash,
                        }
                    )
                )
            return "\n".join(lines)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def prune(self) -> int:
        """
        Prune old audit records per retention policy.

        Rewrites chain with new CHAIN_HEAD anchor; preserves old anchor.
        """
        if not self._initialized:
            self.initialize()

        assert self._conn is not None

        # Determine cutoff dates
        now = datetime.now(timezone.utc)
        crud_cutoff = (now - timedelta(days=self.retention_days_crud)).isoformat()
        gateway_cutoff = (now - timedelta(days=self.retention_days_gateway)).isoformat()

        # Archive old anchors
        old_head = self._chain_head
        if old_head:
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_anchors (
                    anchor_hash TEXT PRIMARY KEY,
                    archived_at TEXT NOT NULL
                )
            """)
            self._conn.execute(
                "INSERT OR IGNORE INTO audit_anchors VALUES (?, ?)", (old_head, now.isoformat())
            )

        # Delete old records (keep gateway events longer)
        self._conn.execute(
            """
            DELETE FROM audit_log
            WHERE event_type NOT IN ('gateway_request', 'gateway_approved', 'gateway_denied')
            AND timestamp < ?
        """,
            (crud_cutoff,),
        )

        self._conn.execute(
            """
            DELETE FROM audit_log
            WHERE event_type IN ('gateway_request', 'gateway_approved', 'gateway_denied')
            AND timestamp < ?
        """,
            (gateway_cutoff,),
        )

        # Rebuild chain head
        self._load_chain_head()
        self._conn.commit()

        return int(self._conn.execute("SELECT changes()").fetchone()[0])

    def _row_to_event(self, row: sqlite3.Row) -> AuditEvent:
        return AuditEvent(
            event_id=row["event_id"],
            event_type=row["event_type"],
            timestamp=row["timestamp"],
            actor=row["actor"],
            correlation_id=row["correlation_id"],
            details=json.loads(row["details"]),
            payload_hash=row["payload_hash"],
            prev_hash=row["prev_hash"],
        )

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None
            self._initialized = False

    def __enter__(self) -> "AuditLogger":
        self.initialize()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()
