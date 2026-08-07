"""Read-through data access for the dashboard — SQLite-first, file-fallback.

Sprint 1 (S1.3) of docs/CEO-DASHBOARD-OPERATIONALIZATION-PLAN.md.  Every
accessor here prefers the SQLite data layer (:mod:`ai_company.data`) when it
holds data and falls back to the legacy file-based stores (inbox.json, KPI
history NDJSON) so the dashboard never renders blank before a backfill has run.
"""

from __future__ import annotations

import logging
from typing import Any

from ai_company.data import CostAnalytics, KPIPipeline, TaskStore, get_database
from ai_company.data.database import Database

logger = logging.getLogger(__name__)


def _usable_database(database: Database | None) -> Database | None:
    """Return a usable database instance, or ``None``.

    Falls back to the module-level singleton and validates the schema so a
    missing or empty database degrades gracefully to file-based reads.
    """
    db = database or get_database()
    if db is None:
        return None
    try:
        if db.get_schema_version() > 0:
            return db
    except Exception:  # noqa: BLE001 - read-through must never raise
        logger.debug("Database not usable; falling back to files", exc_info=True)
    return None


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------


def get_all_tasks(database: Database | None = None) -> list[dict[str, Any]] | None:
    """Return all tasks as plain dicts from SQLite.

    Returns ``None`` when SQLite holds no tasks, signalling the caller to fall
    back to the legacy ``.opencode/inbox.json`` (via the dashboard's
    :func:`~ai_company.dashboard.api.get_bus`, which keeps read/write paths
    consistent).
    """
    db = _usable_database(database)
    if db is None:
        return None
    try:
        store = TaskStore(db)
        if store.count() > 0:
            return [task.model_dump() for task in store.get_all_tasks()]
    except Exception:  # noqa: BLE001 - fall back on any read failure
        logger.debug("SQLite task read failed; using inbox file", exc_info=True)
    return None


# ---------------------------------------------------------------------------
# Costs
# ---------------------------------------------------------------------------


def get_cost_summary(database: Database | None = None) -> dict[str, Any] | None:
    """Return a cost summary derived from SQLite, or ``None`` when empty.

    The caller (``api.py``) keeps file-derived budget fields and merges these
    SQLite-derived spend / per-agent / trend figures when this is not ``None``.
    """
    db = _usable_database(database)
    if db is None:
        return None

    cost = CostAnalytics(db)
    try:
        if cost.total_records() == 0:
            return None
    except Exception:  # noqa: BLE001
        return None

    total_spent = cost.total_cost()

    per_agent_costs: list[dict[str, Any]] = []
    for row in cost.breakdown_by_agent():
        calls = row.get("calls", 0)
        agent_total = row.get("cost_usd", 0.0) or 0.0
        per_agent_costs.append(
            {
                "agent": row.get("agent_name", "unknown"),
                "total_cost": round(agent_total, 6),
                "calls": calls,
                "avg_cost_per_call": round(agent_total / calls, 6) if calls else 0.0,
            }
        )

    cost_trend = [
        {"timestamp": row.get("day", ""), "value": row.get("total_cost", 0.0) or 0.0}
        for row in cost.daily_cost_trend()
    ]

    total_tasks = 0
    completed_tasks = 0
    try:
        task_store = TaskStore(db)
        if task_store.count() > 0:
            statuses = task_store.count_by_status()
            total_tasks = sum(statuses.values())
            completed_tasks = statuses.get("completed", 0)
    except Exception:  # noqa: BLE001 - task counts are best-effort here
        logger.debug("SQLite task counts unavailable for cost summary", exc_info=True)

    return {
        "total_spent": round(total_spent, 6),
        "llm_spend": round(total_spent, 6),
        "avg_cost_per_task": round(total_spent / completed_tasks, 6) if completed_tasks else 0.0,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "per_agent_costs": per_agent_costs,
        "cost_trend": cost_trend,
    }


# ---------------------------------------------------------------------------
# KPI history
# ---------------------------------------------------------------------------


def get_kpi_history(
    department: str,
    kpi_key: str | None = None,
    *,
    limit: int = 100,
    database: Database | None = None,
) -> list[dict[str, Any]] | None:
    """Return KPI history entries from SQLite, or ``None`` when empty.

    Entries share the shape produced by the file-based ``KPIHistoryStore``:
    ``timestamp`` / ``department`` / ``kpi_key`` / ``current`` / ``target`` /
    ``unit`` / ``status``.
    """
    db = _usable_database(database)
    if db is None:
        return None

    pipeline = KPIPipeline(db)
    try:
        if pipeline.total_entries() == 0:
            return None
        rows = pipeline.get_history(department, kpi_key=kpi_key, limit=limit)
    except Exception:  # noqa: BLE001
        return None

    return [
        {
            "timestamp": row["timestamp"],
            "department": row["department"],
            "kpi_key": row["kpi_key"],
            "current": row["current_value"],
            "target": row["target_value"],
            "unit": row["unit"],
            "status": row["status"],
        }
        for row in rows
    ]


__all__ = ["get_all_tasks", "get_cost_summary", "get_kpi_history"]
