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


def get_all_tasks_fallback(database: Database | None = None) -> list[dict[str, Any]]:
    """Return all tasks as plain dicts — SQLite-first, MessageBus fallback.

    This is the single SQLite-first read-through for task data across the
    dashboard.  It prefers the SQLite data layer when it holds tasks,
    otherwise reads through the shared MessageBus (the single source of
    truth for task state).  Bus tasks are returned as raw dicts, filtered to
    ``dict`` entries, so every read-through (API endpoints, KPI collectors,
    company window summaries) stays on one code path instead of drifting
    into three divergent chains.  Never raises: returns ``[]`` when nothing
    is recoverable.
    """
    sqlite_tasks = get_all_tasks(database)
    if sqlite_tasks is not None:
        return sqlite_tasks
    try:
        from ai_company.dashboard.api import get_bus

        data = get_bus().get_all_tasks_raw()
    except Exception:  # noqa: BLE001 - read-through must never raise
        logger.debug("MessageBus unavailable while reading tasks", exc_info=True)
        return []
    if isinstance(data, list):
        return [t for t in data if isinstance(t, dict)]
    return []


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

    # Load budget from cost_tracker.json
    budget = 0.0
    try:
        from ai_company.paths import get_project_root

        cost_tracker_path = get_project_root() / "orchestrator" / "cost_tracker.json"
        if cost_tracker_path.exists():
            import json

            with open(cost_tracker_path) as f:
                cost_tracker = json.load(f)
            budget = float(cost_tracker.get("total_budget", 0) or 0)
    except Exception:  # noqa: BLE001
        pass

    return {
        "total_spent": round(total_spent, 6),
        "llm_spend": round(total_spent, 6),
        "avg_cost_per_task": round(total_spent / completed_tasks, 6) if completed_tasks else 0.0,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "per_agent_costs": per_agent_costs,
        "cost_trend": cost_trend,
        "budget": budget,
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


def get_executive_scorecard(
    days: int = 30,
    project_root: Path | None = None,
) -> dict[str, Any]:
    """Return a unified executive health scorecard from live telemetry.

    Reads ``kpis.executive`` from ``config/company/kpis.yaml`` and computes each
    executive KPI's ``current`` value from the live task window (SQLite-first,
    then the shared MessageBus).  For every KPI it reports:

    - ``status`` — ``on_track`` / ``attention`` / ``critical`` relative to the
      configured ``target`` (honouring ``higher_is_better``).
    - ``trend`` — ``up`` / ``stable`` / ``down`` from :func:`ai_company.
      dashboard.analytics.compute_period_comparison` versus the prior window.
    - ``source`` — ``real_telemetry`` when computed, else ``configured``.
    - an overall ``health_score`` (0-100) weighted by each KPI's ``weight``.

    Never raises: missing config or empty telemetry returns a safe empty
    scorecard rather than an error, so the CEO dashboard degrades gracefully.
    """
    from ai_company.dashboard.analytics import compute_period_comparison

    root = project_root or get_project_root()
    collected_at = datetime.now(timezone.utc).isoformat()
    empty = {
        "collected_at": collected_at,
        "period_days": days,
        "health_score": None,
        "executive_kpis": [],
        "departments": [],
        "summary": {"total": 0, "on_track": 0, "attention": 0, "critical": 0, "info": 0},
    }

    exec_config = _load_executive_config(root)
    if not exec_config:
        return empty

    current_tasks, _ = _company_window_tasks(root, days)
    prior_tasks, _ = _company_window_tasks_prior(root, days)
    window_source = "sqlite" if current_tasks else "files"

    kpis: list[dict[str, Any]] = []
    weights: list[tuple[float, float]] = []  # (attainment 0..1, weight)

    for kpi in exec_config:
        kpi_id = kpi.get("id", "")
        target = kpi.get("target")
        weight = float(kpi.get("weight", 0) or 0)
        higher_is_better = bool(kpi.get("higher_is_better", True))

        current = _compute_executive_kpi(kpi_id, current_tasks, root, days)
        previous = _compute_executive_kpi(kpi_id, prior_tasks, root, days)

        status, attainment = _executive_status(current, target, higher_is_better)
        if attainment is not None:
            weights.append((attainment, weight))

        pct_change = compute_period_comparison(current, previous)
        trend = "up" if (pct_change or 0) > 0 else ("down" if (pct_change or 0) < 0 else "stable")
        if previous is None:
            trend = "stable"

        kpis.append(
            {
                "id": kpi_id,
                "name": kpi.get("name", kpi_id),
                "category": kpi.get("category", ""),
                "owner": kpi.get("owner", ""),
                "unit": kpi.get("unit", ""),
                "frequency": kpi.get("frequency", ""),
                "target": target,
                "current": current,
                "status": status,
                "trend": trend,
                "trend_pct": pct_change,
                "source": "real_telemetry" if current is not None else "configured",
                "higher_is_better": higher_is_better,
                "computed_at": collected_at,
            }
        )

    health_score = None
    total_weight = sum(w for _, w in weights)
    if total_weight > 0:
        health_score = round(sum(a * w for a, w in weights) / total_weight * 100, 1)
        health_score = max(0.0, min(100.0, health_score))

    summary: dict[str, int] = {"total": 0, "on_track": 0, "attention": 0, "critical": 0, "info": 0}
    for kpi in kpis:
        summary[kpi["status"]] += 1
        summary["total"] += 1

    return {
        "collected_at": collected_at,
        "period_days": days,
        "health_score": health_score,
        "executive_kpis": kpis,
        "departments": _department_health_rollup(root),
        "window_source": window_source,
        "summary": summary,
    }


def _load_executive_config(root: Path) -> list[dict[str, Any]]:
    """Load the ``kpis.executive`` block from ``config/company/kpis.yaml``."""
    config_path = root / "config" / "company" / "kpis.yaml"
    if not config_path.is_file():
        return []
    try:
        with open(config_path, "r", encoding="utf-8") as fh:
            config = yaml.safe_load(fh) or {}
    except (yaml.YAMLError, OSError):
        return []
    if not isinstance(config, dict):
        return []
    block = config.get("kpis", {}).get("executive", [])
    if not isinstance(block, list):
        return []
    return [kpi for kpi in block if isinstance(kpi, dict)]


def _company_window_tasks_prior(root: Path, days: int) -> tuple[list[dict[str, Any]], str]:
    """Return the task window immediately *before* the current ``days`` window."""
    now = datetime.now(timezone.utc)
    current_cutoff = now - timedelta(days=days)
    prior_cutoff = now - timedelta(days=2 * days)

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
        if prior_cutoff <= created < current_cutoff:
            windowed.append(task)
    return windowed, source


def _compute_executive_kpi(
    kpi_id: str,
    tasks: list[dict[str, Any]],
    root: Path,
    days: int,
) -> float | None:
    """Compute the live ``current`` value for one executive KPI id.

    ``None`` when there is no data to compute a real value from — the caller
    falls back to ``configured`` sourcing.
    """
    if kpi_id == "task_throughput":
        return float(len(tasks))
    if kpi_id == "agent_utilization":
        total_registered = _count_registered_agents(root)
        active_agents = {
            agent
            for task in tasks
            for agent in (task.get("sender_id"), task.get("receiver_id"))
            if agent
        }
        if total_registered > 0 and active_agents:
            return round(len(active_agents) / total_registered * 100, 1)
        return None
    if kpi_id == "build_success_rate":
        completed = sum(1 for t in tasks if t.get("status") == "completed")
        failed = sum(1 for t in tasks if t.get("status") == "failed")
        if completed + failed > 0:
            return round(completed / (completed + failed) * 100, 1)
        return None
    if kpi_id == "cost_efficiency":
        cost = get_cost_summary()
        if cost:
            budget = float(cost.get("budget", 0) or 0)
            spent = float(cost.get("total_spent", 0) or 0)
            if budget > 0:
                return round(max(0.0, min(100.0, (budget - spent) / budget * 100)), 1)
        return None
    if kpi_id == "escalation_resolution_time":
        return _avg_resolution_seconds(tasks, resolved={"resolved", "closed", "completed"})
    if kpi_id == "approval_turnaround":
        return _avg_resolution_seconds(
            tasks,
            resolved={"approved", "rejected"},
            lookup=("approved_at", "resolved_at", "updated_at"),
        )
    return None


def _avg_resolution_seconds(
    tasks: list[dict[str, Any]],
    resolved: set[str],
    lookup: tuple[str, ...] = ("updated_at", "resolved_at"),
) -> float | None:
    """Return the mean seconds between task creation and resolution.

    Uses ``created_at`` for the start and the first present field in *lookup*
    for the end.  Returns ``None`` when no resolved task has both timestamps.
    """
    durations: list[float] = []
    for task in tasks:
        if task.get("status") not in resolved:
            continue
        created_raw = task.get("created_at", "")
        if not created_raw:
            continue
        try:
            created = datetime.fromisoformat(str(created_raw))
        except (ValueError, TypeError):
            continue
        end_raw = next((task.get(key) for key in lookup if task.get(key)), None)
        if not end_raw:
            continue
        try:
            end = datetime.fromisoformat(str(end_raw))
        except (ValueError, TypeError):
            continue
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        if end.tzinfo is None:
            end = end.replace(tzinfo=timezone.utc)
        durations.append((end - created).total_seconds())
    if not durations:
        return None
    return round(sum(durations) / len(durations), 1)


def _executive_status(
    current: float | None,
    target: float | None,
    higher_is_better: bool,
) -> tuple[str, float | None]:
    """Map a current value to ``status`` and an attainment ratio (0..1).

    Attainment is ``None`` (and status ``info``) when either side is missing.
    """
    if current is None or target is None or target == 0:
        return "info", None
    ratio = current / target if higher_is_better else target / current
    if ratio >= 1.0:
        return "on_track", 1.0
    if ratio >= 0.7:
        return "attention", float(ratio)
    return "critical", float(ratio)


def _department_health_rollup(root: Path) -> list[dict[str, Any]]:
    """Roll up per-department health from the existing company KPI summary."""
    summary = get_company_kpi_summary(days=30, project_root=root)
    by_dept: dict[str, dict[str, Any]] = {}
    for kpi in summary.get("kpis", []):
        if not isinstance(kpi, dict):
            continue
        dept = str(kpi.get("owner", "") or "unassigned")
        bucket = by_dept.setdefault(
            dept,
            {"department": dept, "total": 0, "on_track": 0, "attention": 0, "critical": 0},
        )
        bucket["total"] += 1
        status = kpi.get("status")
        if status in bucket:
            bucket[status] += 1
    return list(by_dept.values())


def run_alert_evaluation() -> list[dict[str, Any]]:
    """Evaluate the default alert rules against the latest KPI snapshot and persist.

    Uses the stateless :class:`AlertEngine` from ``analytics`` plus the durable
    :class:`AlertStore` so fired alerts are recorded for the CEO Alert Center.
    Idempotent: ``AlertStore.add`` dedupes identical active/snoozed alerts, so
    repeated evaluations (manual GET + scheduler) never duplicate rows.

    Returns the newly-persisted alert dicts (for callers that want to broadcast
    them live).
    """
    from ai_company.dashboard.alert_store import AlertStore, default_alert_rules
    from ai_company.dashboard.analytics import AlertEngine
    from ai_company.dashboard.kpis import collect_all_kpis

    engine = AlertEngine(rules=default_alert_rules())
    snapshot = collect_all_kpis()
    fired = engine.evaluate(snapshot)
    if not fired:
        return []
    store = AlertStore()
    new_ids = store.add(fired)
    by_id = {a["id"]: a for a in store.list_alerts(limit=1000)}
    return [by_id[i] for i in new_ids if i in by_id]


__all__ = [
    "get_all_tasks",
    "get_cost_summary",
    "get_kpi_history",
    "get_agent_performance_report",
    "get_agent_performance_summary",
    "get_company_kpi_summary",
    "get_executive_scorecard",
    "run_alert_evaluation",
]
