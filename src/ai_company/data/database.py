"""SQLite database abstraction layer with async support.

Provides the core database connection management, schema creation,
and migration utilities for the AI Company Builder data infrastructure.

Uses :mod:`aiosqlite` for async support while falling back to the
stdlib :mod:`sqlite3` module for synchronous access.
"""

from __future__ import annotations

import contextlib
import json
import logging
import sqlite3
import threading
from pathlib import Path
from typing import Any, cast

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Schema DDL
# ---------------------------------------------------------------------------

SCHEMA_VERSION = 4

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
    content_search  TEXT NOT NULL DEFAULT '',
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

-- Cost aggregations (daily/weekly/monthly summaries from CostAggregationPipeline)
CREATE TABLE IF NOT EXISTS cost_aggregations (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    period              TEXT NOT NULL,          -- 'daily', 'weekly', 'monthly'
    period_key          TEXT NOT NULL,          -- '2025-06-15', '2025-06-09', '2025-06'
    period_type         TEXT NOT NULL,          -- 'daily', 'weekly', 'monthly' (redundant with period for querying)
    total_cost_usd      REAL NOT NULL DEFAULT 0.0,
    total_prompt_tokens INTEGER NOT NULL DEFAULT 0,
    total_completion_tokens INTEGER NOT NULL DEFAULT 0,
    total_calls         INTEGER NOT NULL DEFAULT 0,
    by_model            TEXT NOT NULL DEFAULT '{}',     -- JSON dict
    by_agent            TEXT NOT NULL DEFAULT '{}',     -- JSON dict
    computed_at         TEXT NOT NULL,
    UNIQUE(period, period_key)
);

CREATE INDEX IF NOT EXISTS idx_cost_agg_period ON cost_aggregations(period);
CREATE INDEX IF NOT EXISTS idx_cost_agg_period_key ON cost_aggregations(period_key);

-- Agent performance metrics (from AgentPerformancePipeline)
CREATE TABLE IF NOT EXISTS agent_performance_metrics (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id            TEXT NOT NULL,
    period_days         INTEGER NOT NULL,
    period_start        TEXT NOT NULL,
    period_end          TEXT NOT NULL,
    tasks_sent          INTEGER NOT NULL DEFAULT 0,
    tasks_received      INTEGER NOT NULL DEFAULT 0,
    tasks_completed     INTEGER NOT NULL DEFAULT 0,
    tasks_failed        INTEGER NOT NULL DEFAULT 0,
    completion_rate_pct REAL NOT NULL DEFAULT 0.0,
    error_rate_pct      REAL NOT NULL DEFAULT 0.0,
    sent_by_status      TEXT NOT NULL DEFAULT '{}',     -- JSON dict
    received_by_status  TEXT NOT NULL DEFAULT '{}',     -- JSON dict
    audit_events        TEXT NOT NULL DEFAULT '{}',     -- JSON dict
    tool_usage          TEXT NOT NULL DEFAULT '[]',     -- JSON array
    total_cost_usd      REAL NOT NULL DEFAULT 0.0,
    prompt_tokens       INTEGER NOT NULL DEFAULT 0,
    completion_tokens   INTEGER NOT NULL DEFAULT 0,
    llm_calls           INTEGER NOT NULL DEFAULT 0,
    error_events        INTEGER NOT NULL DEFAULT 0,
    computed_at         TEXT NOT NULL,
    UNIQUE(agent_id, period_days, period_start)
);

CREATE INDEX IF NOT EXISTS idx_agent_perf_agent ON agent_performance_metrics(agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_perf_period ON agent_performance_metrics(period_start);
CREATE INDEX IF NOT EXISTS idx_agent_perf_composite ON agent_performance_metrics(agent_id, period_days, period_start);

-- Revenue transactions (client billing ledger)
CREATE TABLE IF NOT EXISTS revenue_transactions (
    id                  TEXT PRIMARY KEY,
    client_id           TEXT NOT NULL DEFAULT '',
    project_id          TEXT NOT NULL DEFAULT '',
    offer_id            TEXT NOT NULL DEFAULT '',
    service_name        TEXT NOT NULL DEFAULT '',
    currency            TEXT NOT NULL DEFAULT 'MWK',
    amount              REAL NOT NULL DEFAULT 0.0,
    payment_method      TEXT NOT NULL DEFAULT '',
    status              TEXT NOT NULL DEFAULT 'pending',
    installment_type    TEXT NOT NULL DEFAULT '',
    exchange_rate       REAL NOT NULL DEFAULT 0.0,
    linked_task_id      TEXT NOT NULL DEFAULT '',
    reference           TEXT NOT NULL DEFAULT '',
    recorded_by         TEXT NOT NULL DEFAULT '',
    timestamp           TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_revenue_client ON revenue_transactions(client_id);
CREATE INDEX IF NOT EXISTS idx_revenue_project ON revenue_transactions(project_id);
CREATE INDEX IF NOT EXISTS idx_revenue_offer ON revenue_transactions(offer_id);
CREATE INDEX IF NOT EXISTS idx_revenue_status ON revenue_transactions(status);
CREATE INDEX IF NOT EXISTS idx_revenue_ts ON revenue_transactions(timestamp);

-- Project costs (delivery cost tracking, separate from LLM cost_records)
CREATE TABLE IF NOT EXISTS project_costs (
    id                  TEXT PRIMARY KEY,
    project_id          TEXT NOT NULL DEFAULT '',
    cost_type           TEXT NOT NULL DEFAULT '',
    amount_usd          REAL NOT NULL DEFAULT 0.0,
    amount_mwk          REAL NOT NULL DEFAULT 0.0,
    description         TEXT NOT NULL DEFAULT '',
    agent_id            TEXT NOT NULL DEFAULT '',
    model               TEXT NOT NULL DEFAULT '',
    tokens              INTEGER NOT NULL DEFAULT 0,
    timestamp           TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_pcost_project ON project_costs(project_id);
CREATE INDEX IF NOT EXISTS idx_pcost_type ON project_costs(cost_type);
CREATE INDEX IF NOT EXISTS idx_pcost_ts ON project_costs(timestamp);

-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_meta (
    key     TEXT PRIMARY KEY,
    value   TEXT NOT NULL
);
"""

# Ordered migrations keyed by target version.  Migration 1 creates the base
# schema; future migrations add one entry per version.  Applied via
# ``PRAGMA user_version`` so an existing database is never silently left on
# a stale schema.
MIGRATIONS: dict[int, list[str]] = {
    1: [SCHEMA_SQL],
    2: [
        # Task leases: track which executor claimed a task and until when,
        # so stale-detection can verify ownership instead of racing live work.
        "ALTER TABLE tasks ADD COLUMN claimed_by TEXT NOT NULL DEFAULT '';",
        "ALTER TABLE tasks ADD COLUMN lease_expires_at TEXT NOT NULL DEFAULT '';",
    ],
    3: [
        # Revenue transactions + project costs (ledger for order-to-cash)
        """
                CREATE TABLE IF NOT EXISTS revenue_transactions (
                    id                  TEXT PRIMARY KEY,
                    client_id           TEXT NOT NULL DEFAULT '',
                    project_id          TEXT NOT NULL DEFAULT '',
                    offer_id            TEXT NOT NULL DEFAULT '',
                    service_name        TEXT NOT NULL DEFAULT '',
                    currency            TEXT NOT NULL DEFAULT 'MWK',
                    amount              REAL NOT NULL DEFAULT 0.0,
                    payment_method      TEXT NOT NULL DEFAULT '',
                    status              TEXT NOT NULL DEFAULT 'pending',
                    installment_type    TEXT NOT NULL DEFAULT '',
                    exchange_rate       REAL NOT NULL DEFAULT 0.0,
                    linked_task_id      TEXT NOT NULL DEFAULT '',
                    reference           TEXT NOT NULL DEFAULT '',
                    recorded_by         TEXT NOT NULL DEFAULT '',
                    timestamp           TEXT NOT NULL DEFAULT ''
                );
                """,
        "CREATE INDEX IF NOT EXISTS idx_revenue_client ON revenue_transactions(client_id);",
        "CREATE INDEX IF NOT EXISTS idx_revenue_project ON revenue_transactions(project_id);",
        "CREATE INDEX IF NOT EXISTS idx_revenue_offer ON revenue_transactions(offer_id);",
        "CREATE INDEX IF NOT EXISTS idx_revenue_status ON revenue_transactions(status);",
        "CREATE INDEX IF NOT EXISTS idx_revenue_ts ON revenue_transactions(timestamp);",
        """
                CREATE TABLE IF NOT EXISTS project_costs (
                    id                  TEXT PRIMARY KEY,
                    project_id          TEXT NOT NULL DEFAULT '',
                    cost_type           TEXT NOT NULL DEFAULT '',
                    amount_usd          REAL NOT NULL DEFAULT 0.0,
                    amount_mwk          REAL NOT NULL DEFAULT 0.0,
                    description         TEXT NOT NULL DEFAULT '',
                    agent_id            TEXT NOT NULL DEFAULT '',
                    model               TEXT NOT NULL DEFAULT '',
                    tokens              INTEGER NOT NULL DEFAULT 0,
                    timestamp           TEXT NOT NULL DEFAULT ''
                );
                """,
        "CREATE INDEX IF NOT EXISTS idx_pcost_project ON project_costs(project_id);",
        "CREATE INDEX IF NOT EXISTS idx_pcost_type ON project_costs(cost_type);",
        "CREATE INDEX IF NOT EXISTS idx_pcost_ts ON project_costs(timestamp);",
    ],
    4: [
        # Cost aggregations table for CostAggregationPipeline
        """
                CREATE TABLE IF NOT EXISTS cost_aggregations (
                    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                    period              TEXT NOT NULL,
                    period_key          TEXT NOT NULL,
                    period_type         TEXT NOT NULL,
                    total_cost_usd      REAL NOT NULL DEFAULT 0.0,
                    total_prompt_tokens INTEGER NOT NULL DEFAULT 0,
                    total_completion_tokens INTEGER NOT NULL DEFAULT 0,
                    total_calls         INTEGER NOT NULL DEFAULT 0,
                    by_model            TEXT NOT NULL DEFAULT '{}',
                    by_agent            TEXT NOT NULL DEFAULT '{}',
                    computed_at         TEXT NOT NULL,
                    UNIQUE(period, period_key)
                );
                """,
        "CREATE INDEX IF NOT EXISTS idx_cost_agg_period ON cost_aggregations(period);",
        "CREATE INDEX IF NOT EXISTS idx_cost_agg_period_key ON cost_aggregations(period_key);",
        # Agent performance metrics table for AgentPerformancePipeline
        """
                CREATE TABLE IF NOT EXISTS agent_performance_metrics (
                    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id            TEXT NOT NULL,
                    period_days         INTEGER NOT NULL,
                    period_start        TEXT NOT NULL,
                    period_end          TEXT NOT NULL,
                    tasks_sent          INTEGER NOT NULL DEFAULT 0,
                    tasks_received      INTEGER NOT NULL DEFAULT 0,
                    tasks_completed     INTEGER NOT NULL DEFAULT 0,
                    tasks_failed        INTEGER NOT NULL DEFAULT 0,
                    completion_rate_pct REAL NOT NULL DEFAULT 0.0,
                    error_rate_pct      REAL NOT NULL DEFAULT 0.0,
                    sent_by_status      TEXT NOT NULL DEFAULT '{}',
                    received_by_status  TEXT NOT NULL DEFAULT '{}',
                    audit_events        TEXT NOT NULL DEFAULT '{}',
                    tool_usage          TEXT NOT NULL DEFAULT '[]',
                    total_cost_usd      REAL NOT NULL DEFAULT 0.0,
                    prompt_tokens       INTEGER NOT NULL DEFAULT 0,
                    completion_tokens   INTEGER NOT NULL DEFAULT 0,
                    llm_calls           INTEGER NOT NULL DEFAULT 0,
                    error_events        INTEGER NOT NULL DEFAULT 0,
                    computed_at         TEXT NOT NULL,
                    UNIQUE(agent_id, period_days, period_start)
                );
                """,
        "CREATE INDEX IF NOT EXISTS idx_agent_perf_agent ON agent_performance_metrics(agent_id);",
        "CREATE INDEX IF NOT EXISTS idx_agent_perf_period ON agent_performance_metrics(period_start);",
        "CREATE INDEX IF NOT EXISTS idx_agent_perf_composite ON agent_performance_metrics(agent_id, period_days, period_start);",
    ],
}


# ---------------------------------------------------------------------------
# Database class
# ---------------------------------------------------------------------------


class Database:
    """Synchronous SQLite database connection manager.

    Each thread gets its own connection (thread-local), so concurrent
    daemon-loop, HITL-poll, audit/cost write-through, and dashboard threads
    never interleave statements on a single shared handle.

    Schema is managed through real, ordered migrations keyed on
    ``PRAGMA user_version``.

    Args:
        db_path: Path to the SQLite database file.  Defaults to
            ``"data/ai_company.db"`` relative to the working directory.
    """

    def __init__(self, db_path: str | Path = "data/ai_company.db") -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._local = threading.local()
        self._conns: set[sqlite3.Connection] = set()
        self._conn_lock = threading.Lock()
        self._generation = 0

    # ── Connection lifecycle ──────────────────────────────────────────

    @property
    def path(self) -> Path:
        return self._db_path

    def connect(self) -> sqlite3.Connection:
        """Open (or return existing) connection for the current thread."""
        gen = getattr(self._local, "generation", None)
        if gen is None or gen != self._generation:
            conn = sqlite3.connect(
                str(self._db_path),
                check_same_thread=False,
            )
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA foreign_keys=ON")
            conn.execute("PRAGMA busy_timeout=5000")
            self._local.conn = conn
            self._local.generation = self._generation
            with self._conn_lock:
                self._conns.add(conn)
            return conn
        return cast(sqlite3.Connection, self._local.conn)

    def close(self) -> None:
        """Close all connections across all threads.

        Subsequent ``connect()`` calls (from any thread) create fresh
        connections.
        """
        with self._conn_lock:
            self._generation += 1
            conns = list(self._conns)
            self._conns.clear()
        for conn in conns:
            with contextlib.suppress(sqlite3.Error):
                conn.close()

    def __enter__(self) -> sqlite3.Connection:
        return self.connect()

    def __exit__(self, *exc: Any) -> None:
        self.close()

    # ── Schema management ─────────────────────────────────────────────

    @staticmethod
    def _get_user_version(conn: sqlite3.Connection) -> int:
        row = conn.execute("PRAGMA user_version").fetchone()
        return int(row[0]) if row else 0

    def init_schema(self) -> None:
        """Apply all pending migrations in order (idempotent)."""
        conn = self.connect()
        current = self._get_user_version(conn)
        for target in range(current + 1, SCHEMA_VERSION + 1):
            for sql in MIGRATIONS.get(target, []):
                try:
                    conn.executescript(sql)
                except sqlite3.OperationalError as exc:
                    # Allow re-running idempotently if a statement was
                    # already applied by an interrupted earlier attempt.
                    if "duplicate column name" in str(exc).lower():
                        logger.warning(
                            "Migration %d statement already applied, skipping: %s",
                            target,
                            str(exc)[:100],
                        )
                        continue
                    raise
            conn.execute(f"PRAGMA user_version = {target}")
            conn.commit()
            logger.info("Database migrated to schema v%d at %s", target, self._db_path)
        if current == 0 and self._get_user_version(conn) == 0:
            logger.info("No migrations to apply at %s", self._db_path)

    def get_schema_version(self) -> int:
        """Return the current schema version, or 0 if uninitialized."""
        try:
            return self._get_user_version(self.connect())
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
        # safe_table validated via _validate_table_name() regex allowlist.
        row = self.fetchone(f"SELECT COUNT(*) as cnt FROM {safe_table}")  # nosec B608
        return row["cnt"] if row else 0

    def export_json(self, table: str) -> str:
        """Export a table as a JSON string (useful for backward compat)."""
        safe_table = self._validate_table_name(table)
        # safe_table validated via _validate_table_name() regex allowlist.
        rows = self.fetchall(f"SELECT * FROM {safe_table}")  # nosec B608
        # Parse JSON columns back to objects
        for row in rows:
            for key, val in row.items():
                if isinstance(val, str) and val.startswith(("{", "[")):
                    with contextlib.suppress(json.JSONDecodeError, TypeError):
                        row[key] = json.loads(val)
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


def reset_database() -> None:
    """Reset the module-level singleton (used by tests)."""
    global _default_db
    _default_db = None


# Tables every consumer relies on; used by ``database_is_usable``.
_REQUIRED_TABLES = frozenset(
    {
        "tasks",
        "audit_events",
        "memory_entries",
        "escalation_events",
        "kpi_values",
        "cost_records",
        "schema_meta",
        "cost_aggregations",
        "agent_performance_metrics",
    }
)


def database_is_usable(db: Database | None) -> bool:
    """Return True if *db* is initialised with a valid schema.

    Safe against uninitialised databases and broken connections — callers
    (MessageBus, AuditWriter, CostTracker) use this to decide whether the
    SQLite write-through mirror should be active.  Verifies the schema
    version *and* that every required table actually exists, so a partially
    migrated database is never treated as healthy.
    """
    if db is None:
        return False
    try:
        if db.get_schema_version() <= 0:
            return False
        rows = db.fetchall(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        names = {row["name"] for row in rows}
        return _REQUIRED_TABLES.issubset(names)
    except Exception:  # noqa: BLE001 - usability probe must never raise
        return False
