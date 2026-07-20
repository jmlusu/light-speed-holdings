"""SQLite database abstraction layer with async support.

Provides the core database connection management, schema creation,
and migration utilities for the AI Company Builder data infrastructure.

Uses :mod:`aiosqlite` for async support while falling back to the
stdlib :mod:`sqlite3` module for synchronous access.
"""

from __future__ import annotations

import json
import logging
import sqlite3
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Schema DDL
# ---------------------------------------------------------------------------

SCHEMA_VERSION = 1

SCHEMA_SQL = """
-- Tasks (replaces .opencode/inbox.json)
CREATE TABLE IF NOT EXISTS tasks (
    id                  TEXT PRIMARY KEY,
    name                TEXT NOT NULL DEFAULT '',
    description         TEXT NOT NULL DEFAULT '',
    assignee            TEXT NOT NULL DEFAULT '',
    sender_id           TEXT NOT NULL DEFAULT '',
    receiver_id         TEXT NOT NULL DEFAULT '',
    instruction         TEXT NOT NULL DEFAULT '',
    status              TEXT NOT NULL DEFAULT 'pending',
    priority            TEXT NOT NULL DEFAULT 'medium',
    dependencies        TEXT NOT NULL DEFAULT '[]',       -- JSON array
    due_date            TEXT NOT NULL DEFAULT '',
    tags                TEXT NOT NULL DEFAULT '[]',       -- JSON array
    created_at          TEXT NOT NULL DEFAULT '',
    updated_at          TEXT NOT NULL DEFAULT '',
    completed_at        TEXT NOT NULL DEFAULT '',
    result              TEXT NOT NULL DEFAULT '',
    requires_approval   INTEGER NOT NULL DEFAULT 0,
    approved_by         TEXT NOT NULL DEFAULT '',
    correlation_id      TEXT NOT NULL DEFAULT '',
    parent_task_id      TEXT NOT NULL DEFAULT '',
    acknowledged_by     TEXT NOT NULL DEFAULT '',
    raw_json            TEXT NOT NULL DEFAULT '{}'        -- full Pydantic dump for forward compat
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_receiver ON tasks(receiver_id);
CREATE INDEX IF NOT EXISTS idx_tasks_sender ON tasks(sender_id);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_correlation ON tasks(correlation_id);
CREATE INDEX IF NOT EXISTS idx_tasks_parent ON tasks(parent_task_id);
CREATE INDEX IF NOT EXISTS idx_tasks_created ON tasks(created_at);
CREATE INDEX IF NOT EXISTS idx_tasks_assignee ON tasks(assignee);

-- Audit events (replaces .opencode/audit.jsonl)
CREATE TABLE IF NOT EXISTS audit_events (
    event_id        TEXT PRIMARY KEY,
    timestamp       TEXT NOT NULL,
    event_type      TEXT NOT NULL,
    agent_id        TEXT NOT NULL,
    task_id         TEXT NOT NULL DEFAULT '',
    tool            TEXT,
    args            TEXT NOT NULL DEFAULT '{}',     -- JSON dict
    result          TEXT NOT NULL DEFAULT '{}',     -- JSON dict
    metadata        TEXT NOT NULL DEFAULT '{}',     -- JSON dict
    severity        TEXT NOT NULL DEFAULT 'info'
);

CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_agent ON audit_events(agent_id);
CREATE INDEX IF NOT EXISTS idx_audit_task ON audit_events(task_id);
CREATE INDEX IF NOT EXISTS idx_audit_type ON audit_events(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_severity ON audit_events(severity);

-- Memory entries (replaces memory/*.json)
CREATE TABLE IF NOT EXISTS memory_entries (
    id              TEXT PRIMARY KEY,
    memory_type     TEXT NOT NULL,
    content         TEXT NOT NULL,
    metadata        TEXT NOT NULL DEFAULT '{}',     -- JSON dict
    agent_id        TEXT NOT NULL DEFAULT '',
    tags            TEXT NOT NULL DEFAULT '[]',     -- JSON array
    created_at      TEXT NOT NULL,
    access_count    INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_memory_type ON memory_entries(memory_type);
CREATE INDEX IF NOT EXISTS idx_memory_agent ON memory_entries(agent_id);
CREATE INDEX IF NOT EXISTS idx_memory_created ON memory_entries(created_at);

-- Escalation events (replaces orchestrator/escalation.yaml)
CREATE TABLE IF NOT EXISTS escalation_events (
    task_id         TEXT NOT NULL,
    rule_id         TEXT NOT NULL,
    from_agent      TEXT NOT NULL,
    to_agent        TEXT NOT NULL,
    reason          TEXT NOT NULL,
    timestamp       TEXT NOT NULL,
    resolved        INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (task_id, rule_id, timestamp)
);

CREATE INDEX IF NOT EXISTS idx_escalation_resolved ON escalation_events(resolved);
CREATE INDEX IF NOT EXISTS idx_escalation_to ON escalation_events(to_agent);

-- KPI time-series (replaces dashboard/kpi_history/*.ndjson)
CREATE TABLE IF NOT EXISTS kpi_values (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp       TEXT NOT NULL,
    department      TEXT NOT NULL,
    kpi_key         TEXT NOT NULL,
    current_value   REAL NOT NULL,
    target_value    REAL,
    unit            TEXT NOT NULL DEFAULT '',
    status          TEXT NOT NULL DEFAULT 'info'
);

CREATE INDEX IF NOT EXISTS idx_kpi_dept ON kpi_values(department);
CREATE INDEX IF NOT EXISTS idx_kpi_key ON kpi_values(kpi_key);
CREATE INDEX IF NOT EXISTS idx_kpi_ts ON kpi_values(timestamp);
CREATE INDEX IF NOT EXISTS idx_kpi_dept_key ON kpi_values(department, kpi_key);

-- LLM cost tracking (replaces results/cost_log.jsonl)
CREATE TABLE IF NOT EXISTS cost_records (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp           TEXT NOT NULL,
    model               TEXT NOT NULL,
    provider            TEXT NOT NULL,
    agent_name          TEXT NOT NULL,
    task_id             TEXT NOT NULL,
    prompt_tokens       INTEGER NOT NULL DEFAULT 0,
    completion_tokens   INTEGER NOT NULL DEFAULT 0,
    cost_usd            REAL NOT NULL DEFAULT 0.0,
    iteration           INTEGER NOT NULL DEFAULT 1,
    metadata            TEXT NOT NULL DEFAULT '{}'   -- JSON dict
);

CREATE INDEX IF NOT EXISTS idx_cost_ts ON cost_records(timestamp);
CREATE INDEX IF NOT EXISTS idx_cost_agent ON cost_records(agent_name);
CREATE INDEX IF NOT EXISTS idx_cost_task ON cost_records(task_id);
CREATE INDEX IF NOT EXISTS idx_cost_model ON cost_records(model);
CREATE INDEX IF NOT EXISTS idx_cost_provider ON cost_records(provider);

-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_meta (
    key     TEXT PRIMARY KEY,
    value   TEXT NOT NULL
);
"""


# ---------------------------------------------------------------------------
# Database class
# ---------------------------------------------------------------------------


class Database:
    """Synchronous SQLite database connection manager.

    Args:
        db_path: Path to the SQLite database file.  Defaults to
            ``"data/ai_company.db"`` relative to the working directory.
    """

    def __init__(self, db_path: str | Path = "data/ai_company.db") -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: sqlite3.Connection | None = None

    # ── Connection lifecycle ──────────────────────────────────────────

    @property
    def path(self) -> Path:
        return self._db_path

    def connect(self) -> sqlite3.Connection:
        """Open (or return existing) connection."""
        if self._conn is None:
            self._conn = sqlite3.connect(
                str(self._db_path),
                check_same_thread=False,
            )
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
            self._conn.execute("PRAGMA busy_timeout=5000")
        return self._conn

    def close(self) -> None:
        """Close the connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> sqlite3.Connection:
        return self.connect()

    def __exit__(self, *exc: Any) -> None:
        self.close()

    # ── Schema management ─────────────────────────────────────────────

    def init_schema(self) -> None:
        """Create all tables and indexes if they don't exist."""
        conn = self.connect()
        conn.executescript(SCHEMA_SQL)
        conn.execute(
            "INSERT OR REPLACE INTO schema_meta (key, value) VALUES (?, ?)",
            ("version", str(SCHEMA_VERSION)),
        )
        conn.commit()
        logger.info("Database schema initialized at %s (v%d)", self._db_path, SCHEMA_VERSION)

    def get_schema_version(self) -> int:
        """Return the current schema version, or 0 if uninitialized."""
        conn = self.connect()
        try:
            row = conn.execute(
                "SELECT value FROM schema_meta WHERE key = 'version'"
            ).fetchone()
            return int(row["value"]) if row else 0
        except sqlite3.OperationalError:
            return 0

    # ── Transaction helpers ───────────────────────────────────────────

    def execute(self, sql: str, params: tuple[Any, ...] = ()) -> sqlite3.Cursor:
        """Execute a single statement."""
        return self.connect().execute(sql, params)

    def executemany(self, sql: str, params_seq: list[tuple[Any, ...]]) -> sqlite3.Cursor:
        """Execute a statement with many parameter sets."""
        return self.connect().executemany(sql, params_seq)

    def commit(self) -> None:
        """Commit the current transaction."""
        self.connect().commit()

    def rollback(self) -> None:
        """Roll back the current transaction."""
        self.connect().rollback()

    def fetchall(self, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        """Execute a query and return all rows as dicts."""
        rows = self.connect().execute(sql, params).fetchall()
        return [dict(row) for row in rows]

    def fetchone(self, sql: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
        """Execute a query and return a single row as a dict."""
        row = self.connect().execute(sql, params).fetchone()
        return dict(row) if row else None

    # ── Utility ───────────────────────────────────────────────────────

    def _validate_table_name(self, table: str) -> str:
        """Validate that a table name is safe to use in SQL.

        Prevents SQL injection by only allowing alphanumeric characters
        and underscores, and checking against known table patterns.

        Args:
            table: The table name to validate.

        Returns:
            The validated table name.

        Raises:
            ValueError: If the table name contains invalid characters.
        """
        import re
        # Only allow alphanumeric characters and underscores
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", table):
            raise ValueError(f"Invalid table name: {table}")
        return table

    def table_count(self, table: str) -> int:
        """Return the number of rows in a table."""
        safe_table = self._validate_table_name(table)
        row = self.fetchone(f"SELECT COUNT(*) as cnt FROM {safe_table}")
        return row["cnt"] if row else 0

    def export_json(self, table: str) -> str:
        """Export a table as a JSON string (useful for backward compat)."""
        safe_table = self._validate_table_name(table)
        rows = self.fetchall(f"SELECT * FROM {safe_table}")
        # Parse JSON columns back to objects
        for row in rows:
            for key, val in row.items():
                if isinstance(val, str) and val.startswith(("{", "[")):
                    try:
                        row[key] = json.loads(val)
                    except (json.JSONDecodeError, TypeError):
                        pass
        return json.dumps(rows, indent=2, default=str)


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_default_db: Database | None = None


def init_database(db_path: str | Path = "data/ai_company.db") -> Database:
    """Initialise the module-level database singleton.  Idempotent."""
    global _default_db
    if _default_db is None:
        _default_db = Database(db_path)
        _default_db.init_schema()
    return _default_db


def get_database() -> Database | None:
    """Return the current database singleton, or ``None`` if not initialised."""
    return _default_db
