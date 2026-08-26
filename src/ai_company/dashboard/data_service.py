"""Read-through data access for the dashboard — SQLite-first, file-fallback.

Sprint 1 (S1.3) of docs/CEO-DASHBOARD-OPERATIONALIZATION-PLAN.md.  Every
accessor here prefers the SQLite data layer (:mod:`ai_company.data`) when it
holds data and falls back to the legacy file-based stores (inbox.json, KPI
history NDJSON) so the dashboard never renders blank before a backfill has run.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

from ai_company.data import (
    AgentPerformanceAnalytics,
    CostAnalytics,
    KPIPipeline,
    TaskStore,
    get_database,
)
from ai_company.data.database import Database
from ai_company.paths import get_project_root

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
        logger.warning("SQLite task read failed; using inbox file", exc_info=True)
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
        logger.warning("SQLite cost records check failed; using file fallback", exc_info=True)
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
        logger.warning("SQLite task counts unavailable for cost summary", exc_info=True)

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
        logger.warning("SQLite KPI history read failed; using file fallback", exc_info=True)
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


# ---------------------------------------------------------------------------
# Agent analytics
# ---------------------------------------------------------------------------


def get_agent_performance_report(
    database: Database | None = None,
    *,
    days: int = 30,
) -> dict[str, Any] | None:
    """Return a full agent performance report from SQLite, or ``None`` when empty.

    Wraps :class:`~ai_company.data.AgentPerformanceAnalytics` behind the
    read-through pattern (Sprint 3, item 1 of the dashboard plan) so callers
    fall back to file-derived figures when SQLite has not been backfilled.

    The report mirrors :meth:`AgentPerformanceAnalytics.full_report` — with
    ``leaderboard``, ``task_durations``, ``model_usage``, and ``error_analysis``
    sections.  Returns ``None`` when every section is empty.
    """
    db = _usable_database(database)
    if db is None:
        return None

    analytics = AgentPerformanceAnalytics(db)
    try:
        report = analytics.full_report(days)
    except Exception:  # noqa: BLE001 - read-through must never raise
        logger.warning("SQLite agent analytics failed; using file fallback", exc_info=True)
        return None

    if (
        not report["leaderboard"]
        and report["task_durations"]["count"] == 0
        and not report["model_usage"]
        and not report["error_analysis"]["failed_tasks_by_agent"]
        and not report["error_analysis"]["error_events_by_agent"]
    ):
        return None
    return report


def get_agent_performance_summary(
    agent_id: str,
    database: Database | None = None,
    *,
    days: int = 30,
) -> dict[str, Any] | None:
    """Return a single-agent performance summary from SQLite, or ``None``.

    Mirrors :meth:`AgentPerformanceAnalytics.agent_summary`; returns ``None``
    when SQLite holds no data for the agent so callers can fall back to
    file-derived figures.
    """
    db = _usable_database(database)
    if db is None:
        return None

    analytics = AgentPerformanceAnalytics(db)
    try:
        summary = analytics.agent_summary(agent_id, days)
    except Exception:  # noqa: BLE001 - read-through must never raise
        logger.warning("SQLite agent summary failed; using file fallback", exc_info=True)
        return None

    if (
        not summary["tasks_sent"]
        and not summary["tasks_received"]
        and not summary["error_events"]
        and not summary["tool_usage"]
        and summary["cost"]["llm_calls"] == 0
    ):
        return None
    return summary


# ---------------------------------------------------------------------------
# Company KPI summary (Sprint 3, item 2)
# ---------------------------------------------------------------------------


def get_company_kpi_summary(
    days: int = 30,
    project_root: Path | None = None,
) -> dict[str, Any]:
    """Return company-level KPIs vs targets from real telemetry.

    Reads ``config/company/kpis.yaml`` for the target/current definitions and
    computes live ``current`` values for the telemetry-backed KPIs:

    - ``KPI-004`` Build Success Rate: completed / (completed + failed) over
      the ``days``-long task window.
    - ``KPI-003`` Agent Utilization Rate: distinct active agents (sender or
      receiver across window tasks) / registered agents in ``company-registry.yaml``.

    Tasks are read SQLite-first (mirroring :func:`get_all_tasks` /
    ``KPICollector._tasks_from_sqlite``) and fall back to
    ``.opencode/inbox.json``.  Every other KPI keeps its configured
    ``current`` value.  Never raises — a missing/unparseable config returns an
    empty summary.
    """
    root = project_root or get_project_root()
    collected_at = datetime.now(timezone.utc).isoformat()
    empty_summary = {
        "collected_at": collected_at,
        "period_days": days,
        "kpis": [],
        "summary": {"total": 0, "on_track": 0, "below_target": 0, "info": 0},
    }

    config_path = root / "config" / "company" / "kpis.yaml"
    if not config_path.is_file():
        logger.debug("Company KPI config not found, returning empty: %s", config_path)
        return empty_summary
    try:
        with open(config_path, "r", encoding="utf-8") as fh:
            config = yaml.safe_load(fh) or {}
    except (yaml.YAMLError, OSError) as exc:
        logger.warning("Failed to load company KPI config %s: %s", config_path, exc)
        return empty_summary
    if not isinstance(config, dict):
        logger.warning("Company KPI config is not a mapping: %s", config_path)
        return empty_summary

    company_kpis = config.get("kpis", {}).get("company", [])
    if not isinstance(company_kpis, list) or not company_kpis:
        return empty_summary

    window_tasks, task_source = _company_window_tasks(root, days)

    kpis: list[dict[str, Any]] = []
    for kpi in company_kpis:
        if not isinstance(kpi, dict):
            continue
        kpi_id = kpi.get("id", "")
        target = kpi.get("target")
        current = kpi.get("current")
        computed = False
        source = "config"

        if kpi_id == "KPI-004":
            completed = sum(1 for t in window_tasks if t.get("status") == "completed")
            failed = sum(1 for t in window_tasks if t.get("status") == "failed")
            if completed + failed > 0:
                current = round(completed / (completed + failed) * 100, 1)
                computed = True
                source = task_source
        elif kpi_id == "KPI-003":
            total_registered = _count_registered_agents(root)
            active_agents = {
                agent
                for task in window_tasks
                for agent in (task.get("sender_id"), task.get("receiver_id"))
                if agent
            }
            if total_registered > 0 and active_agents:
                current = round(len(active_agents) / total_registered * 100, 1)
                computed = True
                source = task_source

        if target is None:
            status = "info"
            gap = None
        elif isinstance(current, (int, float)) and isinstance(target, (int, float)):
            status = "on_track" if current >= target else "below_target"
            gap = round(target - current, 2)
        else:
            status = "info"
            gap = None

        # Determine data_quality
        if computed:
            data_quality = "real"
        elif current is None:
            data_quality = "no_data"
        elif target is not None:
            data_quality = "config"
        else:
            data_quality = "config"

        data_gap = "No data source available" if current is None else ""

        kpis.append(
            {
                "id": kpi_id,
                "name": kpi.get("name", kpi_id),
                "category": kpi.get("category", ""),
                "owner": kpi.get("owner", ""),
                "frequency": kpi.get("frequency", ""),
                "unit": kpi.get("unit", ""),
                "target": target,
                "current": current,
                "status": status,
                "gap": gap,
                "computed": computed,
                "source": source,
                "data_quality": data_quality,
                "data_gap": data_gap,
                "computed_at": collected_at,
            }
        )

    summary: dict[str, int] = {
        "total": len(kpis),
        "on_track": 0,
        "below_target": 0,
        "info": 0,
        "no_data": 0,
    }
    for kpi in kpis:
        summary[kpi["status"]] += 1
        if kpi["data_quality"] == "no_data":
            summary["no_data"] += 1

    return {
        "collected_at": collected_at,
        "period_days": days,
        "kpis": kpis,
        "summary": summary,
    }


def _company_window_tasks(root: Path, days: int) -> tuple[list[dict[str, Any]], str]:
    """Return ``(tasks within *days* window, source)`` from SQLite or files.

    Mirrors ``KPICollector._tasks_from_sqlite``: SQLite first via
    :func:`get_all_tasks`, then ``.opencode/inbox.json``.  ``source`` is
    ``"sqlite"`` or ``"files"``.  Tasks with unparseable ``created_at`` are
    ignored; naive timestamps are treated as UTC.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    sqlite_tasks = get_all_tasks()
    if sqlite_tasks is not None:
        raw_tasks = sqlite_tasks
        source = "sqlite"
    else:
        raw_tasks = _load_inbox_tasks(root)
        source = "files"

    windowed: list[dict[str, Any]] = []
    for task in raw_tasks:
        if not isinstance(task, dict):
            continue
        created_raw = task.get("created_at", "")
        if not created_raw:
            continue
        try:
            created = datetime.fromisoformat(str(created_raw))
        except (ValueError, TypeError):
            continue
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        if created >= cutoff:
            windowed.append(task)
    return windowed, source


def _load_inbox_tasks(root: Path) -> list[dict[str, Any]]:
    """Load task dicts from the shared MessageBus (GAP-011).

    Falls back to ``.opencode/inbox.json`` only if the bus is unavailable so
    the summary can never raise.  Accepts a top-level JSON list of task dicts
    (the MessageBus layout) and, defensively, a ``{"tasks": [...]}`` wrapper.
    """
    try:
        from ai_company.dashboard.api import get_bus

        data = get_bus().get_all_tasks_raw()
    except Exception:  # noqa: BLE001 - summary must never raise
        logger.debug("MessageBus unavailable; falling back to inbox file")
        data = _read_inbox_file(root)
    if isinstance(data, list):
        return [task for task in data if isinstance(task, dict)]
    if isinstance(data, dict):
        tasks = data.get("tasks")
        if isinstance(tasks, list):
            return [task for task in tasks if isinstance(task, dict)]
    return []


def _read_inbox_file(root: Path) -> list[dict[str, Any]]:
    """Direct-file fallback for task loading (only when the bus is down)."""
    inbox_path = root / ".opencode" / "inbox.json"
    if not inbox_path.is_file():
        logger.debug("Inbox file not found, returning empty: %s", inbox_path)
        return []
    try:
        with open(inbox_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to read inbox %s: %s", inbox_path, exc)
        return []
    if isinstance(data, list):
        return [task for task in data if isinstance(task, dict)]
    if isinstance(data, dict):
        tasks = data.get("tasks")
        if isinstance(tasks, list):
            return [task for task in tasks if isinstance(task, dict)]
    return []


def _count_registered_agents(root: Path) -> int:
    """Count unique agent ``id``s in ``company-registry.yaml``.

    Supports the documented layout (``executives``, ``specialists``, and
    ``departments[].agents``) plus the current repo layout (``company.agents``);
    ids are deduplicated across containers.  Returns ``0`` when the file is
    missing or holds no agents so callers fall back to the config value.
    """
    registry_path = root / "company-registry.yaml"
    if not registry_path.is_file():
        logger.debug("Agent registry not found, returning 0: %s", registry_path)
        return 0
    try:
        with open(registry_path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except (yaml.YAMLError, OSError) as exc:
        logger.warning("Failed to read agent registry %s: %s", registry_path, exc)
        return 0
    if not isinstance(data, dict):
        return 0

    agent_ids: set[str] = set()

    for key in ("executives", "specialists"):
        group = data.get(key)
        if isinstance(group, list):
            for entry in group:
                if isinstance(entry, dict) and entry.get("id"):
                    agent_ids.add(str(entry["id"]))

    departments = data.get("departments")
    if isinstance(departments, list):
        for dept in departments:
            if not isinstance(dept, dict):
                continue
            dept_agents = dept.get("agents")
            if isinstance(dept_agents, list):
                for entry in dept_agents:
                    if isinstance(entry, dict) and entry.get("id"):
                        agent_ids.add(str(entry["id"]))

    company = data.get("company")
    if isinstance(company, dict):
        company_agents = company.get("agents")
        if isinstance(company_agents, list):
            for entry in company_agents:
                if isinstance(entry, dict) and entry.get("id"):
                    agent_ids.add(str(entry["id"]))

    return len(agent_ids)


__all__ = [
    "get_all_tasks",
    "get_cost_summary",
    "get_kpi_history",
    "get_agent_performance_report",
    "get_agent_performance_summary",
    "get_company_kpi_summary",
]
