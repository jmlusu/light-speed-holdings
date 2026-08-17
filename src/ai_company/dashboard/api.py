"""REST API endpoints for the CEO dashboard."""

from __future__ import annotations

import logging
import math
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from pydantic import BaseModel

if TYPE_CHECKING:
    from ai_company.orchestrator.message_bus import MessageBus

from ai_company.dashboard.models import (
    AgentSummary,
    ApprovalDecision,
    ApprovalItem,
    DepartmentInfo,
    EscalationItem,
    KPIs,
    ModelRouteItem,
    OrgNode,
    PaginatedTasks,
    TaskAssign,
    TaskItem,
    TaskUpdate,
    TierInfo,
    WorkflowActionRequest,
    WorkflowSummary,
)
from ai_company.dashboard.repository import get_state_store
from ai_company.data import get_database
from ai_company.security.rbac import Role, require_role

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["dashboard"])

# Module-level MessageBus instance. All task read/write operations are routed
# through this bus instead of touching `.opencode/inbox.json` directly (GAP-011).
# A broadcast callback forwards task lifecycle events to WebSocket clients.
_bus = None


def get_bus() -> MessageBus:
    """Return the shared :class:`MessageBus` instance (lazily created)."""
    global _bus
    if _bus is None:
        from ai_company.dashboard.repository import get_state_store
        from ai_company.orchestrator.message_bus import MessageBus

        _bus = MessageBus(
            str(Path(get_state_store().base_dir) / ".opencode" / "inbox.json"),
            broadcast_callback=_bus_broadcast,
            database=get_database(),
        )
    return _bus


def _bus_broadcast(task_dict: dict[str, Any], event: str) -> None:
    """MessageBus broadcast callback — fire-and-forget to WebSocket clients."""
    try:
        loop = __import__("asyncio").get_running_loop()
        loop.create_task(_broadcast_task(task_dict, event))
    except RuntimeError:
        logger.debug("No event loop; broadcast skipped")


def _read_all_tasks() -> list[dict[str, Any]]:
    """Return all tasks as plain dicts — SQLite-first, inbox-file fallback.

    The file fallback reads through :func:`get_bus` so writes and reads stay
    on the same bus (tests override ``_bus`` to an isolated inbox).
    """
    from ai_company.dashboard.data_service import get_all_tasks

    tasks = get_all_tasks()
    if tasks is not None:
        return tasks
    return [task.model_dump() for task in get_bus().get_all_tasks()]


def _load_tasks_dicts() -> list[dict[str, Any]]:
    """Backwards-compatible alias used by endpoints that need raw task dicts."""
    return _read_all_tasks()


def _per_agent_costs_from_audit() -> list[dict[str, Any]]:
    """Per-agent LLM cost breakdown derived from the audit JSONL (file fallback)."""
    agent_costs: dict[str, dict[str, Any]] = {}
    for event in _get_store().iter_jsonl(".opencode/audit"):
        try:
            meta = event.get("metadata", {})
            cost = float(meta.get("cost", 0))
            agent = meta.get("agent_id", event.get("agent_id", "unknown"))
            if agent not in agent_costs:
                agent_costs[agent] = {"total_cost": 0.0, "calls": 0}
            agent_costs[agent]["total_cost"] += cost
            agent_costs[agent]["calls"] += 1
        except (TypeError, ValueError):
            continue

    per_agent: list[dict[str, Any]] = []
    for agent_name, cost_info in sorted(
        agent_costs.items(), key=lambda x: x[1]["total_cost"], reverse=True
    ):
        calls = cost_info["calls"]
        total = cost_info["total_cost"]
        per_agent.append(
            {
                "agent": agent_name,
                "total_cost": round(total, 6),
                "calls": calls,
                "avg_cost_per_call": round(total / calls, 6) if calls > 0 else 0.0,
            }
        )
    return per_agent


def _registry_agent_stats(
    tasks: list[dict[str, Any]], registry: list[dict]
) -> list[dict[str, Any]]:
    """Per-agent task stats for every registered agent.

    Shared by :func:`get_agent_performance` and :func:`get_agent` so the
    registry-based figures stay consistent with the legacy contract.
    """
    agent_stats: dict[str, dict[str, Any]] = {}
    for agent in registry:
        agent_stats[agent["name"]] = {
            "name": agent["name"],
            "role": agent.get("role", ""),
            "department": agent.get("department", ""),
            "type": agent.get("type", ""),
            "total_received": 0,
            "total_sent": 0,
            "completed": 0,
            "failed": 0,
            "in_progress": 0,
            "pending": 0,
            "escalated": 0,
            "completion_rate": 0.0,
            "failure_rate": 0.0,
        }

    for task in tasks:
        receiver = task.get("receiver_id", "")
        sender = task.get("sender_id", "")
        status = task.get("status", "pending")

        if receiver in agent_stats:
            agent_stats[receiver]["total_received"] += 1
            if status == "completed":
                agent_stats[receiver]["completed"] += 1
            elif status == "failed":
                agent_stats[receiver]["failed"] += 1
            elif status == "in_progress":
                agent_stats[receiver]["in_progress"] += 1
            elif status == "pending":
                agent_stats[receiver]["pending"] += 1
            elif status == "escalated":
                agent_stats[receiver]["escalated"] += 1

        if sender in agent_stats:
            agent_stats[sender]["total_sent"] += 1

    for stats in agent_stats.values():
        total = stats["total_received"]
        if total > 0:
            stats["completion_rate"] = round((stats["completed"] / total) * 100, 1)
            stats["failure_rate"] = round((stats["failed"] / total) * 100, 1)

    return sorted(
        agent_stats.values(),
        key=lambda a: a["completion_rate"],
        reverse=True,
    )


def _duration_stats(durations_by_agent: dict[str, list[float]]) -> dict[str, Any]:
    """Overall + per-agent duration stats, matching ``task_duration_stats``."""
    all_durations = [d for durs in durations_by_agent.values() for d in durs]
    if not all_durations:
        return {"count": 0, "avg_seconds": 0, "median_seconds": 0, "by_agent": {}}

    def summarize(durs: list[float]) -> dict[str, Any]:
        s = sorted(durs)
        mid = len(s) // 2
        median = s[mid] if len(s) % 2 else (s[mid - 1] + s[mid]) / 2
        return {
            "count": len(s),
            "avg_seconds": round(sum(s) / len(s), 2),
            "median_seconds": round(median, 2),
            "min_seconds": round(min(s), 2),
            "max_seconds": round(max(s), 2),
        }

    return {
        **summarize(all_durations),
        "by_agent": {agent: summarize(durs) for agent, durs in sorted(durations_by_agent.items())},
    }


def _file_agent_analytics(days: int = 30) -> dict[str, Any]:
    """File-derived agent analytics matching ``AgentPerformanceAnalytics.full_report``.

    Fallback used when SQLite holds no backfilled data, so the analytics
    endpoints never render blank (Sprint 3, item 1 of the dashboard plan).
    """
    from datetime import datetime, timedelta, timezone

    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    tasks = _read_all_tasks()

    stats: dict[str, dict[str, Any]] = {}
    durations_by_agent: dict[str, list[float]] = {}
    failed_tasks_by_agent: dict[str, int] = {}

    def entry(agent_id: str) -> dict[str, Any]:
        return stats.setdefault(
            agent_id,
            {
                "agent_id": agent_id,
                "tasks_sent": 0,
                "tasks_received": 0,
                "tasks_completed": 0,
                "tasks_failed": 0,
                "completion_rate_pct": 0.0,
                "error_rate_pct": 0.0,
                "sent_by_status": {},
                "received_by_status": {},
                "audit_events": {},
                "tool_usage": {},
                "cost": {
                    "total_usd": 0.0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "llm_calls": 0,
                },
                "error_events": 0,
            },
        )

    for task in tasks:
        created = task.get("created_at", "")
        if created and created < cutoff:
            continue
        sender = task.get("sender_id", "") or "unknown"
        receiver = task.get("receiver_id", "") or "unknown"
        status = task.get("status", "pending")

        s = entry(sender)
        s["tasks_sent"] += 1
        s["sent_by_status"][status] = s["sent_by_status"].get(status, 0) + 1

        r = entry(receiver)
        r["tasks_received"] += 1
        r["received_by_status"][status] = r["received_by_status"].get(status, 0) + 1
        if status == "completed":
            r["tasks_completed"] += 1
        elif status == "failed":
            r["tasks_failed"] += 1
            failed_tasks_by_agent[receiver] = failed_tasks_by_agent.get(receiver, 0) + 1

        completed = task.get("completed_at", "")
        if created and completed:
            try:
                duration = (
                    datetime.fromisoformat(completed) - datetime.fromisoformat(created)
                ).total_seconds()
                if duration >= 0:
                    durations_by_agent.setdefault(receiver, []).append(duration)
            except (ValueError, TypeError):
                continue

    model_usage: dict[tuple[str, str, str], dict[str, Any]] = {}
    error_events_by_agent: dict[tuple[str, str], int] = {}
    severity_dist: dict[str, int] = {}
    for event in _get_store().iter_jsonl(".opencode/audit"):
        try:
            ts = event.get("timestamp", "")
            if ts and ts < cutoff:
                continue
            meta = event.get("metadata", {}) or {}
            agent = event.get("agent_id", "") or meta.get("agent_id", "") or "unknown"
            etype = event.get("event_type", "")

            e = entry(agent)
            e["audit_events"][etype] = e["audit_events"].get(etype, 0) + 1
            is_error = etype == "error" or event.get("severity", "info") in ("error", "critical")
            if is_error:
                e["error_events"] += 1
            tool = event.get("tool")
            if tool:
                e["tool_usage"][tool] = e["tool_usage"].get(tool, 0) + 1
            e["cost"]["total_usd"] += float(meta.get("cost", 0) or 0)
            e["cost"]["prompt_tokens"] += int(meta.get("prompt_tokens", 0) or 0)
            e["cost"]["completion_tokens"] += int(meta.get("completion_tokens", 0) or 0)
            e["cost"]["llm_calls"] += 1

            model = meta.get("model", "") or event.get("model", "") or "unknown"
            provider = meta.get("provider", "") or event.get("provider", "") or "unknown"
            m = model_usage.setdefault(
                (model, provider, agent),
                {
                    "model": model,
                    "provider": provider,
                    "agent_name": agent,
                    "calls": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "cost_usd": 0.0,
                },
            )
            m["calls"] += 1
            m["prompt_tokens"] += int(meta.get("prompt_tokens", 0) or 0)
            m["completion_tokens"] += int(meta.get("completion_tokens", 0) or 0)
            m["cost_usd"] += float(meta.get("cost", 0) or 0)

            if is_error:
                key = (agent, etype or "error")
                error_events_by_agent[key] = error_events_by_agent.get(key, 0) + 1

            sev = event.get("severity", "info")
            severity_dist[sev] = severity_dist.get(sev, 0) + 1
        except (TypeError, ValueError):
            continue

    for s in stats.values():
        finished = s["tasks_completed"] + s["tasks_failed"]
        s["completion_rate_pct"] = (
            round(s["tasks_completed"] / finished * 100, 2) if finished else 0.0
        )
        s["error_rate_pct"] = round(s["tasks_failed"] / finished * 100, 2) if finished else 0.0
        s["tool_usage"] = [
            {"tool": tool, "calls": n}
            for tool, n in sorted(s["tool_usage"].items(), key=lambda kv: kv[1], reverse=True)
        ]
        s["cost"]["total_usd"] = round(s["cost"]["total_usd"], 6)
        s["period_days"] = days

    leaderboard = sorted(
        stats.values(),
        key=lambda s: (s["completion_rate_pct"], s["tasks_completed"]),
        reverse=True,
    )
    for i, s in enumerate(leaderboard):
        s["rank"] = i + 1

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "period_days": days,
        "leaderboard": leaderboard,
        "task_durations": _duration_stats(durations_by_agent),
        "model_usage": sorted(model_usage.values(), key=lambda m: m["cost_usd"], reverse=True),
        "error_analysis": {
            "period_days": days,
            "failed_tasks_by_agent": [
                {"agent_id": a, "count": n}
                for a, n in sorted(
                    failed_tasks_by_agent.items(), key=lambda kv: kv[1], reverse=True
                )
            ],
            "error_events_by_agent": [
                {"agent_id": a, "event_type": etype, "count": n}
                for (a, etype), n in sorted(
                    error_events_by_agent.items(), key=lambda kv: kv[1], reverse=True
                )
            ],
            "severity_distribution": severity_dist,
        },
    }


def _file_agent_summary(agent_id: str, days: int = 30) -> dict[str, Any]:
    """File-derived single-agent summary (mirrors ``agent_summary``)."""
    for row in _file_agent_analytics(days)["leaderboard"]:
        if row["agent_id"] == agent_id:
            return cast(dict[str, Any], row)
    return {
        "agent_id": agent_id,
        "period_days": days,
        "tasks_sent": 0,
        "tasks_received": 0,
        "tasks_completed": 0,
        "tasks_failed": 0,
        "completion_rate_pct": 0.0,
        "error_rate_pct": 0.0,
        "sent_by_status": {},
        "received_by_status": {},
        "audit_events": {},
        "tool_usage": [],
        "cost": {"total_usd": 0.0, "prompt_tokens": 0, "completion_tokens": 0, "llm_calls": 0},
        "error_events": 0,
    }


_START_TIME = time.time()


# ── Helpers ─────────────────────────────────────────────────────────


# GAP-011: all dashboard state I/O is routed through StateStore, which
# wraps the atomic FileStore and rejects forbidden paths. The store is
# fetched lazily so the boot-time explicit configuration (Option B) takes
# effect for request handling rather than being frozen at import time.
def _get_store() -> Any:
    return get_state_store()


def _load_json(path: str | Path) -> Any:
    return _get_store().read_json(path, default={})


def _load_yaml(path: str | Path) -> Any:
    return _get_store().read_yaml(path, default={})


def _save_json(path: str | Path, data: Any) -> None:
    _get_store().write_json(path, data)


def _save_yaml(path: str, data: Any) -> None:
    _get_store().write_yaml(path, data)


def _load_registry() -> list[dict]:
    raw = _load_json("company/agent-registry.json") or []
    return [_normalize_agent(a) for a in raw]


_CAMEL_TO_SNAKE: dict[str, str] = {
    "reportsTo": "reports_to",
    "directReports": "direct_reports",
}


def _normalize_agent(agent: dict[str, Any]) -> dict[str, Any]:
    """Convert camelCase keys from the legacy JSON registry to snake_case."""
    out = dict(agent)
    for camel, snake in _CAMEL_TO_SNAKE.items():
        if camel in out:
            out[snake] = out.pop(camel)
    return out


# ── WebSocket broadcast helpers ─────────────────────────────────────


async def _broadcast_kpis(data: dict[str, Any]) -> None:
    """Fire-and-forget broadcast of KPI data to WebSocket clients."""
    try:
        from ai_company.dashboard.ws import broadcast_kpi_update

        await broadcast_kpi_update(data)
    except Exception:  # noqa: BLE001 - fire-and-forget: must never crash the caller
        logger.debug("WebSocket broadcast skipped (no event loop or clients)")


async def _broadcast_task(task: dict[str, Any], event: str) -> None:
    """Fire-and-forget broadcast of a task lifecycle event."""
    try:
        from ai_company.dashboard.ws import broadcast_task_update

        await broadcast_task_update(task, event)
    except Exception:  # noqa: BLE001 - fire-and-forget: must never crash the caller
        logger.debug("WebSocket broadcast skipped (no event loop or clients)")


async def _broadcast_approval_alert(request: dict[str, Any]) -> None:
    """Fire-and-forget broadcast of an approval request to WebSocket clients."""
    try:
        from ai_company.dashboard.ws import broadcast_alert

        await broadcast_alert(
            {
                "category": "approval",
                "request_id": request.get("id", ""),
                "action": request.get("action", ""),
                "agent_id": request.get("agent_id", ""),
                "tier": request.get("tier", 2),
            }
        )
    except Exception:  # noqa: BLE001 - fire-and-forget: must never crash the caller
        logger.debug("WebSocket broadcast skipped")


async def _broadcast_escalation_alert(event: dict[str, Any]) -> None:
    """Fire-and-forget broadcast of an escalation event to WebSocket clients."""
    try:
        from ai_company.dashboard.ws import broadcast_alert

        await broadcast_alert(
            {
                "category": "escalation",
                "task_id": event.get("task_id", ""),
                "reason": event.get("reason", ""),
                "agent_id": event.get("agent_id", ""),
            }
        )
    except Exception:  # noqa: BLE001 - fire-and-forget: must never crash the caller
        logger.debug("WebSocket broadcast skipped")


def _schedule_broadcast(background_tasks: BackgroundTasks, task_dict: dict, event: str) -> None:
    """Schedule a task-broadcast as a FastAPI background task.

    This is the synchronous helper used by MessageBus callbacks.
    """
    # We can't call background_tasks.add_task from outside a request,
    # but when called from API endpoints we have access to them.
    # For the MessageBus callback path we use a standalone async helper.
    try:
        loop = __import__("asyncio").get_running_loop()
        loop.create_task(_broadcast_task(task_dict, event))
    except RuntimeError:
        # No running event loop — likely during tests or CLI usage; skip.
        logger.debug("No event loop; broadcast skipped")


# ── Dashboard / KPIs ────────────────────────────────────────────────


@router.get("/dashboard", response_model=KPIs, tags=["dashboard"])
def get_dashboard(background_tasks: BackgroundTasks) -> KPIs:
    """Return a snapshot of all CEO-level KPIs.

    Aggregates task, approval, escalation, agent, and scheduler data
    into a single KPI payload and broadcasts to WebSocket clients.
    """
    tasks = _read_all_tasks()
    approvals_data = _load_yaml("orchestrator/approvals.yaml")
    escalations_data = _load_yaml("orchestrator/escalation.yaml")
    scheduler_data = _load_yaml("orchestrator/scheduler.yaml")
    registry = _load_registry()

    approval_requests = approvals_data.get("requests", [])
    escalation_events = escalations_data.get("events", [])
    scheduled = scheduler_data.get("tasks", [])

    now = datetime.now(timezone.utc).isoformat()
    pending_approvals = [
        r
        for r in approval_requests
        if r.get("status") == "pending" and (not r.get("expires_at") or r["expires_at"] > now)
    ]
    open_escalations = [e for e in escalation_events if not e.get("resolved", False)]

    kpis = KPIs(
        pending_tasks=sum(1 for t in tasks if t.get("status") == "pending"),
        in_progress_tasks=sum(1 for t in tasks if t.get("status") == "in_progress"),
        completed_tasks=sum(1 for t in tasks if t.get("status") == "completed"),
        failed_tasks=sum(1 for t in tasks if t.get("status") == "failed"),
        escalated_tasks=sum(1 for t in tasks if t.get("status") == "escalated"),
        pending_approvals=len(pending_approvals),
        open_escalations=len(open_escalations),
        total_agents=len(registry),
        scheduled_tasks=len(scheduled),
        uptime_seconds=time.time() - _START_TIME,
    )

    # Broadcast KPI snapshot to WebSocket clients
    kpi_payload = kpis.model_dump()
    background_tasks.add_task(_broadcast_kpis, kpi_payload)

    # Broadcast alerts for urgent items
    for req in pending_approvals[:3]:
        background_tasks.add_task(_broadcast_approval_alert, req)
    for evt in open_escalations[:3]:
        background_tasks.add_task(_broadcast_escalation_alert, evt)

    return kpis


@router.get("/kpis/live", tags=["kpis"])
def get_live_kpis(background_tasks: BackgroundTasks) -> dict[str, Any]:
    """Return live KPI values computed from operational data.

    Uses the KPI collectors to produce real-time snapshots for all
    7 departments (engineering, HR, finance, marketing, sales, CS, legal).
    Broadcasts the result to WebSocket clients.
    """
    from ai_company.dashboard.kpis import collect_all_kpis

    result = collect_all_kpis(database=get_database())
    background_tasks.add_task(_broadcast_kpis, result)
    return result


# ── Agents ──────────────────────────────────────────────────────────


@router.get("/agents", response_model=list[AgentSummary], tags=["agents"])
def list_agents() -> list[AgentSummary]:
    """List all registered agents from the company registry."""
    return [AgentSummary(**a) for a in _load_registry()]


@router.get("/agents/performance")
def get_agent_performance(days: int = Query(30, ge=1, le=365)) -> dict[str, Any]:
    """Return per-agent performance metrics computed from task history.

    Returns a summary with:
    - Registry-based per-agent task counts (legacy contract)
    - Leaderboard ranked by completion rate
    - Model usage distribution
    - Task duration statistics
    - Error analysis (failed tasks + error events)

    SQLite-first (Sprint 3, item 1): when backfilled data exists, the
    leaderboard / model usage / durations / error analysis come from
    :class:`~ai_company.data.AgentPerformanceAnalytics`; otherwise they are
    derived from the legacy inbox + audit files so the endpoint never renders
    blank.  ``source`` reports which backend produced the figures.
    """
    from ai_company.dashboard.data_service import get_agent_performance_report

    tasks = _read_all_tasks()
    agents = _registry_agent_stats(tasks, _load_registry())

    report = get_agent_performance_report(days=days)
    if report is None:
        report = _file_agent_analytics(days)
        source = "files"
    else:
        source = "sqlite"

    return {
        "agents": agents,
        "total_tasks": len(tasks),
        "agents_with_tasks": sum(1 for a in agents if a["total_received"] > 0),
        "leaderboard": report["leaderboard"],
        "task_durations": report["task_durations"],
        "model_usage": report["model_usage"],
        "error_analysis": report["error_analysis"],
        "period_days": days,
        "source": source,
    }


@router.get("/agents/{name}/performance")
def get_agent_performance_detail(
    name: str,
    days: int = Query(30, ge=1, le=365),
) -> dict[str, Any]:
    """Return a single agent's performance summary (SQLite-first)."""
    from ai_company.dashboard.data_service import get_agent_performance_summary

    summary = get_agent_performance_summary(name, days=days)
    if summary is not None:
        summary["source"] = "sqlite"
        return summary
    summary = _file_agent_summary(name, days)
    summary["source"] = "files"
    return summary


@router.get("/agents/{name}", response_model=AgentSummary, tags=["agents"])
def get_agent(name: str) -> AgentSummary:
    """Retrieve details for a single agent by name."""
    registry = {a["name"]: a for a in _load_registry()}
    if name not in registry:
        raise HTTPException(status_code=404, detail=f"Agent '{name}' not found")
    return AgentSummary(**registry[name])


# ── Org Chart ───────────────────────────────────────────────────────


@router.get("/org-chart", response_model=list[OrgNode], tags=["agents"])
def get_org_chart() -> list[OrgNode]:
    """Return the hierarchical org chart rooted at the CEO."""
    registry = {a["name"]: a for a in _load_registry()}
    children_map: dict[str, list[str]] = {}
    for a in _load_registry():
        parent = a.get("reports_to", "")
        children_map.setdefault(parent, []).append(a["name"])

    def build_node(name: str) -> OrgNode:
        a = registry.get(name, {})
        kids = [build_node(c) for c in children_map.get(name, [])]
        return OrgNode(
            name=name,
            role=a.get("role", name),
            type=a.get("type", "Unknown"),
            department=a.get("department", ""),
            children=kids,
        )

    roots = children_map.get("human-ceo", [])
    if not roots and "chief-of-staff" in registry:
        roots = ["chief-of-staff"]
    return [build_node(r) for r in roots]


# ── Tasks ───────────────────────────────────────────────────────────


_PRIORITY_ORDER: dict[str, int] = {"critical": 0, "high": 1, "medium": 2, "low": 3}
_STATUS_ORDER: dict[str, int] = {
    "escalated": 0,
    "failed": 1,
    "pending": 2,
    "in_progress": 3,
    "completed": 4,
}

_TRIVIAL_INSTRUCTION_RE = re.compile(r"^do [a-z]$", re.IGNORECASE)
_TEST_PREFIX_RE = re.compile(r"^test\s", re.IGNORECASE)


@router.get("/tasks", response_model=list[TaskItem], tags=["tasks"])
def list_tasks(
    status: str = "",
    agent: str = "",
) -> list[TaskItem]:
    """List all tasks with optional filters for status and agent."""
    tasks = _read_all_tasks()
    if status:
        tasks = [t for t in tasks if t.get("status") == status]
    if agent:
        tasks = [t for t in tasks if t.get("receiver_id") == agent or t.get("sender_id") == agent]
    return [TaskItem(**t) for t in tasks]


@router.get("/tasks/paginated", response_model=PaginatedTasks, tags=["tasks"])
def list_tasks_paginated(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=10, le=100),
    status: str = "",
    priority: str = "",
    department: str = "",
    agent: str = "",
    sort_by: str = "created_at",
    sort_dir: str = "desc",
) -> PaginatedTasks:
    """List tasks with server-side pagination, filtering, and sorting.

    Returns a page of tasks plus metadata (total, counts, total_pages).
    The ``counts_by_status`` field always reflects the filtered (but
    un-paginated) result set so Kanban column headers stay accurate.
    """
    # Page size must be one of the allowed values
    if page_size not in (10, 20, 50, 100):
        page_size = 20

    tasks = _read_all_tasks()

    # ── Filter: status (comma-separated) ──
    if status:
        allowed_statuses = {s.strip() for s in status.split(",") if s.strip()}
        tasks = [t for t in tasks if t.get("status") in allowed_statuses]

    # ── Filter: priority (comma-separated) ──
    if priority:
        allowed_priorities = {p.strip() for p in priority.split(",") if p.strip()}
        tasks = [t for t in tasks if t.get("priority") in allowed_priorities]

    # ── Filter: department (via agent registry lookup) ──
    if department:
        registry = _load_registry()
        dept_agent_names = {
            a["name"]
            for a in registry
            if (a.get("department") or "").lower() == department.lower()
            or (a.get("department") or "").replace(" ", "_").lower() == department.lower()
        }
        tasks = [
            t
            for t in tasks
            if t.get("receiver_id") in dept_agent_names or t.get("sender_id") in dept_agent_names
        ]

    # ── Filter: agent (substring match on sender_id or receiver_id) ──
    if agent:
        agent_lower = agent.lower()
        tasks = [
            t
            for t in tasks
            if agent_lower in t.get("receiver_id", "").lower()
            or agent_lower in t.get("sender_id", "").lower()
        ]

    # ── Counts by status (before pagination) ──
    counts: dict[str, int] = {}
    for t in tasks:
        s = t.get("status", "pending")
        counts[s] = counts.get(s, 0) + 1

    # ── Sort ──
    valid_sort_fields = {"created_at", "priority", "status", "receiver_id"}
    if sort_by not in valid_sort_fields:
        sort_by = "created_at"
    if sort_dir not in ("asc", "desc"):
        sort_dir = "desc"

    reverse = sort_dir == "desc"

    if sort_by == "priority":
        tasks.sort(
            key=lambda t: (
                _PRIORITY_ORDER.get(t.get("priority", "medium"), 2),
                t.get("created_at", "") or "",
            ),
            reverse=reverse,
        )
    elif sort_by == "status":
        tasks.sort(
            key=lambda t: (_STATUS_ORDER.get(t.get("status", ""), 5),),
            reverse=reverse,
        )
    elif sort_by == "created_at":
        tasks.sort(key=lambda t: t.get("created_at", "") or "", reverse=reverse)
    elif sort_by == "receiver_id":
        tasks.sort(key=lambda t: t.get("receiver_id", ""), reverse=reverse)

    # ── Paginate ──
    total = len(tasks)
    total_pages = max(1, math.ceil(total / page_size))
    start = (page - 1) * page_size
    end = start + page_size
    page_items = tasks[start:end]

    return PaginatedTasks(
        items=[TaskItem(**t) for t in page_items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        counts_by_status=counts,
    )


@router.post("/tasks", response_model=TaskItem, status_code=201, tags=["tasks"])
def create_task(
    assign: TaskAssign,
    background_tasks: BackgroundTasks,
    _: Role = Depends(require_role("run")),
) -> TaskItem:
    """Create a new task and send it through the MessageBus."""
    # Validate: reject trivial instructions
    stripped = assign.instruction.strip()
    if len(stripped) <= 5:
        raise HTTPException(
            status_code=400,
            detail="Instruction too short. Please provide a meaningful task description.",
        )
    if _TRIVIAL_INSTRUCTION_RE.match(stripped):
        raise HTTPException(
            status_code=400,
            detail="Instruction appears to be a placeholder. Please provide a meaningful task description.",
        )
    if _TEST_PREFIX_RE.match(stripped):
        raise HTTPException(
            status_code=400,
            detail="Instruction appears to be a test placeholder. Please provide a meaningful task description.",
        )

    import uuid

    from ai_company.models import Task, TaskPriority

    priority = assign.priority
    if isinstance(priority, str):
        priority = TaskPriority(priority)

    task = Task(
        id=str(uuid.uuid4()),
        sender_id=assign.sender_id,
        receiver_id=assign.receiver_id,
        instruction=assign.instruction,
        status="pending",  # type: ignore[arg-type]
        priority=priority,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    get_bus().send_task(task)

    # Broadcast task creation to WebSocket clients
    background_tasks.add_task(_broadcast_task, task.model_dump(), "created")

    return TaskItem(**task.model_dump())


@router.patch("/tasks/{task_id}", response_model=TaskItem, tags=["tasks"])
def update_task(
    task_id: str,
    update: TaskUpdate,
    background_tasks: BackgroundTasks,
    _: Role = Depends(require_role("run")),
) -> TaskItem:
    """Partially update a task (e.g. drag-and-drop status change).

    Only fields present in the request body are updated.  A
    ``task_update`` WebSocket event is broadcast after the mutation.
    """
    # Build the updates dict — skip None values (not provided)
    updates = update.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    updated = get_bus().update_task(task_id, updates)
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")

    # Broadcast the updated task to WebSocket clients
    background_tasks.add_task(_broadcast_task, updated.model_dump(), "updated")

    return TaskItem(**updated.model_dump())


@router.delete("/tasks/{task_id}", tags=["tasks"])
def delete_task(
    task_id: str,
    background_tasks: BackgroundTasks,
    _: Role = Depends(require_role("run")),
) -> dict[str, str]:
    """Delete a task by id.

    Returns ``{"ok": true, "id": "<task_id>"}`` on success.
    """
    removed = get_bus().delete_task(task_id)
    if removed is None:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")

    # Broadcast the deletion to WebSocket clients
    background_tasks.add_task(_broadcast_task, removed.model_dump(), "deleted")

    return {"ok": "true", "id": task_id}


# ── Approvals ───────────────────────────────────────────────────────


@router.get("/approvals", response_model=list[ApprovalItem], tags=["approvals"])
def list_approvals() -> list[ApprovalItem]:
    """List all pending approval requests that have not expired."""
    data = _load_yaml("orchestrator/approvals.yaml")
    now = datetime.now(timezone.utc)
    requests = data.get("requests", [])
    result: list[ApprovalItem] = []
    for r in requests:
        if r.get("status") != "pending":
            continue
        expires = r.get("expires_at")
        if expires:
            try:
                expires_dt = datetime.fromisoformat(expires)
            except (ValueError, TypeError):
                expires_dt = None
            if expires_dt is not None:
                if expires_dt.tzinfo is None:
                    expires_dt = expires_dt.replace(tzinfo=timezone.utc)
                if expires_dt <= now:
                    continue
        result.append(ApprovalItem(**r))
    return result


@router.post("/approvals/{request_id}/approve", tags=["approvals"])
def approve_request(
    request_id: str,
    body: ApprovalDecision | None = None,
    _: Role = Depends(require_role("approve")),
) -> dict:
    """Approve a pending approval request by ID."""
    data = _load_yaml("orchestrator/approvals.yaml")
    requests = data.get("requests", [])
    for r in requests:
        if r["id"] == request_id and r.get("status") == "pending":
            r["status"] = "approved"
            r["responded_at"] = datetime.now(timezone.utc).isoformat()
            r["response_by"] = body.approved_by if body else "human-ceo"
            if body and body.notes:
                r["notes"] = body.notes
            _save_yaml("orchestrator/approvals.yaml", data)
            return {"ok": True, "id": request_id}
    raise HTTPException(
        status_code=404, detail=f"Request '{request_id}' not found or already processed"
    )


@router.post("/approvals/{request_id}/reject", tags=["approvals"])
def reject_request(
    request_id: str,
    body: ApprovalDecision | None = None,
    _: Role = Depends(require_role("approve")),
) -> dict:
    """Reject a pending approval request by ID."""
    data = _load_yaml("orchestrator/approvals.yaml")
    requests = data.get("requests", [])
    for r in requests:
        if r["id"] == request_id and r.get("status") == "pending":
            r["status"] = "rejected"
            r["responded_at"] = datetime.now(timezone.utc).isoformat()
            r["response_by"] = body.approved_by if body else "human-ceo"
            if body and body.notes:
                r["notes"] = body.notes
            _save_yaml("orchestrator/approvals.yaml", data)
            return {"ok": True, "id": request_id}
    raise HTTPException(
        status_code=404, detail=f"Request '{request_id}' not found or already processed"
    )


# ── Escalations ─────────────────────────────────────────────────────


@router.get("/escalations", response_model=list[EscalationItem], tags=["escalations"])
def list_escalations() -> list[EscalationItem]:
    """List all unresolved escalation events."""
    data = _load_yaml("orchestrator/escalation.yaml")
    events = data.get("events", [])
    return [EscalationItem(**e) for e in events if not e.get("resolved", False)]


@router.post("/escalations/{task_id}/resolve", tags=["escalations"])
def resolve_escalation(
    task_id: str,
    _: Role = Depends(require_role("approve")),
) -> dict:
    """Resolve an open escalation event and log to the audit trail."""
    data = _load_yaml("orchestrator/escalation.yaml")
    events = data.get("events", [])
    for e in events:
        if e.get("task_id") == task_id and not e.get("resolved", False):
            e["resolved"] = True
            _save_yaml("orchestrator/escalation.yaml", data)
            # GAP-008: persist the escalation resolution to the audit trail.
            try:
                from ai_company.audit.integration import log_escalation

                log_escalation(
                    task_id=task_id,
                    from_agent=e.get("from_agent", ""),
                    to_agent=e.get("to_agent", ""),
                    reason=e.get("reason", "resolved via dashboard"),
                    rule_id=e.get("rule_id", ""),
                    resolved=True,
                )
            except Exception:  # noqa: BLE001 - audit hook must not break resolution
                logger.debug("audit hook skipped for escalation resolution")
            return {"ok": True, "task_id": task_id}
    raise HTTPException(status_code=404, detail=f"No open escalation for task '{task_id}'")


# ── Departments ─────────────────────────────────────────────────────


@router.get("/departments", response_model=list[DepartmentInfo], tags=["departments"])
def list_departments() -> list[DepartmentInfo]:
    """List all registered departments."""
    data = _load_yaml("company/departments.yaml")
    return [DepartmentInfo(**d) for d in data.get("departments", [])]


# ── Models ──────────────────────────────────────────────────────────


@router.get("/models", response_model=list[ModelRouteItem], tags=["models"])
def list_model_routes() -> list[ModelRouteItem]:
    """List model routing assignments for all registered agents."""
    from ai_company.model_router import ModelRouter

    router_instance = ModelRouter()
    results = router_instance.resolve_all_agents()
    return [
        ModelRouteItem(agent=name, provider=r.provider, model=r.model, tier=r.tier, reason=r.reason)
        for name, r in sorted(results.items())
    ]


@router.get("/models/tiers", response_model=list[TierInfo], tags=["models"])
def list_model_tiers() -> list[TierInfo]:
    """List available model tiers and their provider configurations."""
    from ai_company.model_router import ModelRouter

    router_instance = ModelRouter()
    return [
        TierInfo(
            id=t.id,
            description=t.description,
            providers=[{"provider": p.provider, "model": p.model} for p in t.providers],
        )
        for t in router_instance.list_tiers()
    ]


# ── Scheduler ───────────────────────────────────────────────────────


@router.get("/scheduler", tags=["scheduler"])
def list_scheduled() -> list[dict]:
    """List all scheduled and recurring tasks."""
    data = _load_yaml("orchestrator/scheduler.yaml")
    return cast(list[dict], data.get("tasks", []))


# ── Department KPIs ────────────────────────────────────────────────


@router.get("/departments/{dept_name}/kpis", tags=["departments", "kpis"])
def get_department_kpis(dept_name: str) -> dict:
    """Return KPI definitions for a specific department."""
    kpi_data = _load_yaml("company/config/kpis.yaml")
    departments = kpi_data.get("departments", {})
    if dept_name not in departments:
        raise HTTPException(
            status_code=404, detail=f"Department '{dept_name}' not found in KPI config"
        )
    return cast(dict, departments[dept_name])


@router.get("/kpis")
def list_all_kpis() -> dict:
    """Return all department KPI definitions."""
    kpi_data = _load_yaml("company/config/kpis.yaml")
    return cast(dict, kpi_data.get("departments", {}))


@router.get("/kpis/summary")
def kpi_summary() -> list[dict]:
    """Return a flat summary of all KPIs across departments."""
    kpi_data = _load_yaml("company/config/kpis.yaml")
    summary = []
    for dept_id, dept in kpi_data.get("departments", {}).items():
        for kpi in dept.get("kpis", []):
            summary.append(
                {
                    "department": dept_id,
                    "department_name": dept.get("name", dept_id),
                    "kpi_id": kpi["id"],
                    "name": kpi["name"],
                    "target": kpi.get("target"),
                    "unit": kpi.get("unit", ""),
                    "frequency": kpi.get("frequency", ""),
                }
            )
    return summary


# ── Company-level KPIs ──────────────────────────────────────────────


@router.get("/company-kpis", tags=["kpis"])
def list_company_kpis(days: int = Query(30, ge=1, le=365)) -> dict[str, Any]:
    """Return company-level KPIs vs targets from real telemetry.

    SQLite-first, inbox-file fallback (Sprint 3, item 2).  Build Success Rate
    and Agent Utilization are computed from the task telemetry window; the
    remaining KPIs report their configured ``current`` values.  Always returns
    the full summary shape and never raises.
    """
    from ai_company.dashboard.data_service import get_company_kpi_summary

    return get_company_kpi_summary(days=days)


# ── CEO Dashboard (aggregate view) ─────────────────────────────────


@router.get("/ceo-dashboard")
def get_ceo_dashboard(background_tasks: BackgroundTasks) -> dict[str, Any]:
    """CEO-wide overview aggregating all departments.

    Returns a consolidated view including:
    - Company health (all KPIs across departments)
    - Agent performance summary
    - Cost tracking
    - Task pipeline status
    - Escalation alerts
    """
    from ai_company.dashboard.kpis import collect_all_kpis

    # Live KPIs from all departments
    kpi_snapshot = collect_all_kpis()
    departments = kpi_snapshot.get("departments", {})

    # Task pipeline
    tasks = _read_all_tasks()
    task_summary = {
        "pending": sum(1 for t in tasks if t.get("status") == "pending"),
        "in_progress": sum(1 for t in tasks if t.get("status") == "in_progress"),
        "completed": sum(1 for t in tasks if t.get("status") == "completed"),
        "failed": sum(1 for t in tasks if t.get("status") == "failed"),
        "escalated": sum(1 for t in tasks if t.get("status") == "escalated"),
        "total": len(tasks),
    }

    # Agent performance
    registry = _load_registry()
    agent_summary: dict[str, Any] = {
        "total_agents": len(registry),
        "by_type": {},
        "by_department": {},
    }
    for agent in registry:
        atype = agent.get("type", "unknown")
        dept = agent.get("department", "unassigned")
        agent_summary["by_type"][atype] = agent_summary["by_type"].get(atype, 0) + 1
        agent_summary["by_department"][dept] = agent_summary["by_department"].get(dept, 0) + 1

    # Cost tracking
    cost_data = _load_json("orchestrator/cost_tracker.json")
    cost_summary: dict[str, Any] = {"total_budget": 0, "total_spent": 0, "llm_spend": 0}
    if isinstance(cost_data, dict):
        cost_summary["total_budget"] = cost_data.get("total_budget", 0)
        cost_summary["total_spent"] = cost_data.get("total_spent", 0)
        cost_summary["llm_spend"] = cost_data.get("llm_spend", 0)

    # Escalation alerts
    escalation_data = _load_yaml("orchestrator/escalation.yaml")
    escalation_events = escalation_data.get("events", [])
    open_escalations = [e for e in escalation_events if not e.get("resolved", False)]

    # Approvals pending
    approvals_data = _load_yaml("orchestrator/approvals.yaml")
    approval_requests = approvals_data.get("requests", [])
    now_iso = datetime.now(timezone.utc).isoformat()
    pending_approvals = [
        r
        for r in approval_requests
        if r.get("status") == "pending" and (not r.get("expires_at") or r["expires_at"] > now_iso)
    ]

    # Scheduled tasks
    scheduler_data = _load_yaml("orchestrator/scheduler.yaml")
    scheduled = scheduler_data.get("tasks", [])

    # Company-level KPIs
    company_kpi_data = _load_yaml("config/company/kpis.yaml")
    company_kpis = company_kpi_data.get("kpis", {}).get("company", [])

    result = {
        "collected_at": kpi_snapshot["collected_at"],
        "company_health": {
            "departments": {dept: data.get("kpis", {}) for dept, data in departments.items()},
            "company_kpis": company_kpis,
        },
        "agent_performance": agent_summary,
        "cost_tracking": cost_summary,
        "task_pipeline": task_summary,
        "escalation_alerts": open_escalations,
        "pending_approvals": pending_approvals,
        "scheduled_tasks": scheduled,
        "uptime_seconds": time.time() - _START_TIME,
    }

    # Broadcast to WebSocket
    background_tasks.add_task(_broadcast_kpis, result)
    return result


# ── Department Dashboard (per-department drill-down) ────────────────


@router.get("/departments/{dept_name}/dashboard")
def get_department_dashboard(
    dept_name: str,
    background_tasks: BackgroundTasks,
) -> dict[str, Any]:
    """Per-department dashboard with KPIs, agent activity, and task stats.

    Returns:
    - Department KPI values (live)
    - Agent list for this department
    - Task completion rates (total and department-specific)
    - Escalations involving department agents
    """
    from ai_company.dashboard.kpis import ALL_COLLECTORS, KPICollector

    # Find the collector for this department
    collector_cls: type[KPICollector] | None = None
    for cls in ALL_COLLECTORS:
        if cls.department == dept_name:
            collector_cls = cls
            break

    if collector_cls is None:
        # Fall back to KPI config for unknown departments
        kpi_data = _load_yaml("company/config/kpis.yaml")
        dept_config = kpi_data.get("departments", {}).get(dept_name)
        if dept_config is None:
            raise HTTPException(status_code=404, detail=f"Department '{dept_name}' not found")
        return {
            "department": dept_name,
            "kpis": dept_config,
            "agents": [],
            "task_stats": {},
        }

    # Collect live KPIs
    collector = collector_cls()
    dept_kpis = collector.collect()

    # Agents in this department
    registry = _load_registry()
    dept_agents = [
        a
        for a in registry
        if (a.get("department") or "").lower() == dept_name.lower()
        or (a.get("department") or "").replace(" ", "_").lower() == dept_name.lower()
    ]

    # Task stats for this department
    tasks = _read_all_tasks()
    dept_agent_names = {a["name"] for a in dept_agents}
    dept_tasks = [
        t
        for t in tasks
        if t.get("receiver_id") in dept_agent_names or t.get("sender_id") in dept_agent_names
    ]
    task_stats = {
        "pending": sum(1 for t in dept_tasks if t.get("status") == "pending"),
        "in_progress": sum(1 for t in dept_tasks if t.get("status") == "in_progress"),
        "completed": sum(1 for t in dept_tasks if t.get("status") == "completed"),
        "failed": sum(1 for t in dept_tasks if t.get("status") == "failed"),
        "total": len(dept_tasks),
    }

    # Escalations involving this department
    escalation_data = _load_yaml("orchestrator/escalation.yaml")
    escalation_events = escalation_data.get("events", [])
    dept_escalations = [
        e
        for e in escalation_events
        if e.get("from_agent") in dept_agent_names or e.get("to_agent") in dept_agent_names
    ]

    result = {
        "department": dept_name,
        "collected_at": dept_kpis.get("collected_at", datetime.now(timezone.utc).isoformat()),
        "kpis": dept_kpis.get("kpis", {}),
        "agents": dept_agents,
        "task_stats": task_stats,
        "escalations": [e for e in dept_escalations if not e.get("resolved", False)],
    }

    # Broadcast per-department KPIs
    background_tasks.add_task(_broadcast_kpis, {dept_name: result})
    return result


# ── KPI Analytics Endpoints ────────────────────────────────────────


@router.get("/kpis/history/{department}")
def get_kpi_history(
    department: str,
    kpi_key: str = "",
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Retrieve KPI history for a department from the analytics store.

    Parameters
    ----------
    department:
        Department id (e.g. ``"engineering"``).
    kpi_key:
        Optional filter for a specific KPI.
    limit:
        Max entries to return (default 100).
    """
    from ai_company.dashboard.data_service import get_kpi_history as get_sqlite_kpi_history

    sqlite_entries = get_sqlite_kpi_history(
        department,
        kpi_key or None,
        limit=limit,
    )
    if sqlite_entries is not None:
        return sqlite_entries

    from ai_company.dashboard.analytics import KPIHistoryStore

    store = KPIHistoryStore()
    entries = store.get_history(
        department,
        kpi_key=kpi_key or None,
        limit=limit,
    )
    return [
        {
            "timestamp": e.timestamp,
            "department": e.department,
            "kpi_key": e.kpi_key,
            "current": e.current,
            "target": e.target,
            "unit": e.unit,
            "status": e.status,
        }
        for e in entries
    ]


@router.get("/kpis/trends/{department}")
def get_kpi_trends(
    department: str,
    kpi_keys: str = "",
    previous_period_minutes: int = 60,
) -> list[dict[str, Any]]:
    """Compute trend analysis for a department's KPIs.

    Parameters
    ----------
    department:
        Department id.
    kpi_keys:
        Comma-separated list of KPI keys to analyse. Empty = all.
    previous_period_minutes:
        How far back to look for the comparison period.
    """
    from ai_company.dashboard.analytics import KPIHistoryStore, compute_trends

    store = KPIHistoryStore()
    keys = [k.strip() for k in kpi_keys.split(",") if k.strip()] or None
    trends = compute_trends(
        store,
        department,
        kpi_keys=keys,
        previous_period_minutes=previous_period_minutes,
    )
    return [
        {
            "kpi_key": t.kpi_key,
            "department": t.department,
            "current_value": t.current_value,
            "previous_value": t.previous_value,
            "absolute_change": t.absolute_change,
            "percentage_change": t.percentage_change,
            "direction": t.direction,
            "unit": t.unit,
        }
        for t in trends
    ]


@router.get("/kpis/alerts")
def get_kpi_alerts() -> dict[str, Any]:
    """Evaluate default alert rules against the latest KPI snapshot.

    Returns fired alerts and the rules that were evaluated.
    """
    from ai_company.dashboard.analytics import AlertEngine, AlertRule, KPIHistoryStore
    from ai_company.dashboard.kpis import collect_all_kpis

    # Default alert rules for common thresholds
    default_rules = [
        AlertRule(
            name="High failure rate",
            department="*",
            kpi_key="failure_rate",
            operator="gt",
            threshold=10.0,
            severity="critical",
        ),
        AlertRule(
            name="High failure rate warning",
            department="*",
            kpi_key="failure_rate",
            operator="gt",
            threshold=5.0,
            severity="warning",
        ),
        AlertRule(
            name="Low task completion",
            department="*",
            kpi_key="task_completion_rate",
            operator="lt",
            threshold=80.0,
            severity="warning",
        ),
        AlertRule(
            name="Open escalations",
            department="*",
            kpi_key="open_escalations",
            operator="gt",
            threshold=3,
            severity="warning",
        ),
        AlertRule(
            name="Budget overage",
            department="finance",
            kpi_key="budget_utilization",
            operator="gt",
            threshold=95.0,
            severity="critical",
        ),
        AlertRule(
            name="Low customer satisfaction",
            department="customer_success",
            kpi_key="customer_satisfaction",
            operator="lt",
            threshold=7.0,
            severity="warning",
        ),
        AlertRule(
            name="Low compliance score",
            department="legal",
            kpi_key="compliance_score",
            operator="lt",
            threshold=90.0,
            severity="critical",
        ),
    ]

    engine = AlertEngine(rules=default_rules)
    snapshot = collect_all_kpis()
    alerts = engine.evaluate(snapshot)

    # Also store snapshot for history
    try:
        from ai_company.dashboard.analytics import KPIHistoryStore

        store = KPIHistoryStore()
        store.store_snapshot(snapshot)
    except Exception:  # noqa: BLE001 - history storage is best-effort
        logger.debug("Failed to store KPI snapshot for history")

    return {
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "rules_evaluated": len(default_rules),
        "alerts_fired": [
            {
                "rule_name": a.rule_name,
                "department": a.department,
                "kpi_key": a.kpi_key,
                "current_value": a.current_value,
                "threshold": a.threshold,
                "operator": a.operator,
                "severity": a.severity,
                "fired_at": a.fired_at,
                "message": a.message,
            }
            for a in alerts
        ],
        "alert_count": len(alerts),
    }


@router.get("/kpis/collect")
def collect_and_store_kpis(background_tasks: BackgroundTasks) -> dict[str, Any]:
    """Manually trigger a KPI collection cycle, store the snapshot, and return it.

    This is useful for on-demand data collection or for the auto-collect
    background loop to push data.
    """
    from ai_company.dashboard.analytics import KPIHistoryStore
    from ai_company.dashboard.kpis import collect_all_kpis

    snapshot = collect_all_kpis(database=get_database())

    # Store in history (file-based)
    store = KPIHistoryStore()
    stored_count = store.store_snapshot(snapshot)

    # Also ingest into SQLite when the data layer is available (S1.3)
    sqlite_stored = 0
    try:
        from ai_company.data import KPIPipeline

        db = get_database()
        if db is not None and db.get_schema_version() > 0:
            pipeline = KPIPipeline(db)
            sqlite_stored = pipeline.ingest_snapshot(snapshot)
    except Exception:  # noqa: BLE001 - SQLite ingest is best-effort
        logger.debug("SQLite KPI ingest skipped (non-critical)", exc_info=True)

    result = {
        **snapshot,
        "stored_entries": stored_count,
        "sqlite_stored_entries": sqlite_stored,
        "history_departments": store.list_departments(),
    }

    # Broadcast to WebSocket
    background_tasks.add_task(_broadcast_kpis, result)
    return result


@router.get("/kpis/summary-stats/{department}")
def get_kpi_summary_stats(
    department: str,
    period: str = "daily",
) -> list[dict[str, Any]]:
    """Return rollup statistics (min/max/mean/count) for a department.

    Parameters
    ----------
    department:
        Department id.
    period:
        ``"daily"``, ``"weekly"``, or ``"monthly"``.
    """
    from ai_company.dashboard.analytics import KPIHistoryStore, compute_summary

    store = KPIHistoryStore()
    if period not in ("daily", "weekly", "monthly"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid period '{period}'. Must be daily, weekly, or monthly.",
        )
    summaries = compute_summary(store, department, period=period)  # type: ignore[arg-type]
    return [
        {
            "department": s.department,
            "kpi_key": s.kpi_key,
            "period": s.period,
            "period_start": s.period_start,
            "period_end": s.period_end,
            "min_value": s.min_value,
            "max_value": s.max_value,
            "mean_value": s.mean_value,
            "count": s.count,
            "unit": s.unit,
        }
        for s in summaries
    ]


# ── Cost Tracking ─────────────────────────────────────────────────


@router.get("/costs/summary")
def get_cost_summary(background_tasks: BackgroundTasks) -> dict[str, Any]:
    """Return cost tracking summary from cost tracker and audit log.

    Includes:
    - Budget utilization
    - LLM spend breakdown by provider
    - Per-agent cost breakdown
    - Historical cost trend (from KPI history store)

    When the SQLite data layer holds cost records (after ``dashboard backfill``),
    spend / per-agent / trend figures come from there; otherwise they are
    derived from the legacy cost tracker and audit log (S1.2/S1.3).
    """
    tasks = _read_all_tasks()
    cost_data = _load_json("orchestrator/cost_tracker.json")

    # Parse cost tracker
    total_budget: float = 0.0
    if isinstance(cost_data, dict):
        total_budget = cost_data.get("total_budget", 0.0)

    # SQLite-derived figures (spend, per-agent, trend) when available
    from ai_company.dashboard.data_service import get_cost_summary as get_sqlite_cost_summary

    sqlite_summary = get_sqlite_cost_summary()

    if sqlite_summary is not None:
        total_spent = float(sqlite_summary["total_spent"])
        llm_spend = float(sqlite_summary["llm_spend"])
        per_agent = sqlite_summary["per_agent_costs"]
        trend_data = sqlite_summary["cost_trend"]
        total_tasks = int(sqlite_summary["total_tasks"])
        completed = int(sqlite_summary["completed_tasks"])
        avg_per_task = float(sqlite_summary["avg_cost_per_task"])
    else:
        total_spent = cost_data.get("total_spent", 0.0) if isinstance(cost_data, dict) else 0.0
        llm_spend = cost_data.get("llm_spend", 0.0) if isinstance(cost_data, dict) else 0.0
        per_agent = _per_agent_costs_from_audit()

        # Total completed tasks for cost-per-task calc
        completed = sum(1 for t in tasks if t.get("status") == "completed")
        total_tasks = len(tasks)
        avg_per_task = round(total_spent / completed, 6) if completed > 0 else 0.0

        # KPI history for trend
        from ai_company.dashboard.analytics import KPIHistoryStore

        store = KPIHistoryStore()
        finance_history = store.get_history("finance", kpi_key="budget_utilization", limit=50)
        trend_data = [{"timestamp": e.timestamp, "value": e.current} for e in finance_history]

    budget_utilization = round((total_spent / total_budget * 100), 1) if total_budget > 0 else 0.0

    result = {
        "total_budget": total_budget,
        "total_spent": total_spent,
        "llm_spend": llm_spend,
        "budget_utilization": budget_utilization,
        "avg_cost_per_task": avg_per_task,
        "total_tasks": total_tasks,
        "completed_tasks": completed,
        "per_agent_costs": per_agent,
        "cost_trend": trend_data,
    }

    # Broadcast to WebSocket
    background_tasks.add_task(_broadcast_kpis, {"cost_summary": result})
    return result


# ── Governance ──────────────────────────────────────────────────────


@router.get("/governance", tags=["governance"])
def governance_report_api() -> dict[str, Any]:
    """Return the data governance report (Sprint 3, item 3).

    SQLite-first: returns the full DataGovernance report when the database
    is available, else an empty shape with available=False. Never raises.
    """
    from datetime import datetime, timezone

    from ai_company.data import DataGovernance, database_is_usable, get_database

    empty_shape = {
        "available": False,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tables": {},
        "owners": [],
        "policies": [],
    }
    db = get_database()
    if db is None or not database_is_usable(db):
        return empty_shape
    try:
        report = DataGovernance(db).governance_report()
        report["available"] = True
        return report
    except Exception:  # noqa: BLE001 - governance report must never raise
        return empty_shape


# ── Payment Capture & Revenue Ledger ────────────────────────────────


class PaymentEntry(BaseModel):
    """Manual payment entry for the revenue ledger."""

    client_id: str = ""
    project_id: str = ""
    offer_id: str = ""
    service_name: str = ""
    currency: str = "MWK"
    amount: float = 0.0
    payment_method: str = ""
    status: str = "confirmed"
    installment_type: str = ""
    exchange_rate: float = 0.0
    linked_task_id: str = ""
    reference: str = ""
    recorded_by: str = "human-ceo"


class ProjectCostEntry(BaseModel):
    """Project cost entry for the cost ledger."""

    project_id: str = ""
    cost_type: str = ""
    amount_usd: float = 0.0
    amount_mwk: float = 0.0
    description: str = ""
    agent_id: str = ""
    model: str = ""
    tokens: int = 0


@router.post("/payments", status_code=201, tags=["payments"])
def create_payment(entry: PaymentEntry) -> dict[str, Any]:
    """Record a manual payment in the revenue ledger."""
    import uuid

    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    txn_id = f"REV-{uuid.uuid4().hex[:12].upper()}"
    now = datetime.now(timezone.utc).isoformat()

    conn = db.connect()
    conn.execute(
        """INSERT INTO revenue_transactions
           (id, client_id, project_id, offer_id, service_name, currency,
            amount, payment_method, status, installment_type, exchange_rate,
            linked_task_id, reference, recorded_by, timestamp)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            txn_id,
            entry.client_id,
            entry.project_id,
            entry.offer_id,
            entry.service_name,
            entry.currency,
            entry.amount,
            entry.payment_method,
            entry.status,
            entry.installment_type,
            entry.exchange_rate,
            entry.linked_task_id,
            entry.reference,
            entry.recorded_by,
            now,
        ),
    )
    conn.commit()

    return {
        "id": txn_id,
        "status": "recorded",
        "timestamp": now,
        "amount": entry.amount,
        "currency": entry.currency,
    }


@router.get("/revenue", tags=["revenue"])
def list_revenue_transactions(
    project_id: str | None = None,
    offer_id: str | None = None,
    status: str | None = None,
) -> list[dict[str, Any]]:
    """List revenue transactions with optional filters."""
    db = get_database()
    if db is None:
        return []

    conn = db.connect()
    query = "SELECT * FROM revenue_transactions WHERE 1=1"
    params: list[Any] = []

    if project_id:
        query += " AND project_id = ?"
        params.append(project_id)
    if offer_id:
        query += " AND offer_id = ?"
        params.append(offer_id)
    if status:
        query += " AND status = ?"
        params.append(status)

    query += " ORDER BY timestamp DESC"
    rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]


@router.get("/revenue/summary", tags=["revenue"])
def revenue_summary(
    project_id: str | None = None,
) -> dict[str, Any]:
    """Revenue summary with contribution margin computation."""
    db = get_database()
    if db is None:
        return {
            "total_revenue_mwk": 0,
            "total_revenue_usd": 0,
            "total_costs_usd": 0,
            "contribution_margin": 0,
            "margin_percent": 0,
            "transaction_count": 0,
            "cost_count": 0,
        }

    conn = db.connect()

    # Revenue totals
    rev_query = "SELECT SUM(amount) as total, COUNT(*) as count FROM revenue_transactions WHERE status = 'confirmed'"
    rev_params: list[Any] = []
    if project_id:
        rev_query += " AND project_id = ?"
        rev_params.append(project_id)
    rev_row = conn.execute(rev_query, rev_params).fetchone()
    total_revenue = float(rev_row["total"] or 0) if rev_row else 0
    txn_count = int(rev_row["count"] or 0) if rev_row else 0

    # Cost totals
    cost_query = "SELECT SUM(amount_usd) as total, COUNT(*) as count FROM project_costs WHERE 1=1"
    cost_params: list[Any] = []
    if project_id:
        cost_query += " AND project_id = ?"
        cost_params.append(project_id)
    cost_row = conn.execute(cost_query, cost_params).fetchone()
    total_costs = float(cost_row["total"] or 0) if cost_row else 0
    cost_count = int(cost_row["count"] or 0) if cost_row else 0

    # Contribution margin (revenue - costs, both in USD for comparison)
    # For MWK revenue, apply exchange rate (approx 1800 MWK = 1 USD)
    revenue_usd = total_revenue / 1800 if total_revenue > 0 else 0
    margin = revenue_usd - total_costs
    margin_pct = (margin / revenue_usd * 100) if revenue_usd > 0 else 0

    return {
        "total_revenue_mwk": total_revenue,
        "total_revenue_usd": round(revenue_usd, 2),
        "total_costs_usd": round(total_costs, 2),
        "contribution_margin": round(margin, 2),
        "margin_percent": round(margin_pct, 1),
        "transaction_count": txn_count,
        "cost_count": cost_count,
    }


@router.post("/project-costs", status_code=201, tags=["costs"])
def create_project_cost(entry: ProjectCostEntry) -> dict[str, Any]:
    """Record a project cost in the cost ledger."""
    import uuid

    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    cost_id = f"COST-{uuid.uuid4().hex[:12].upper()}"
    now = datetime.now(timezone.utc).isoformat()

    conn = db.connect()
    conn.execute(
        """INSERT INTO project_costs
           (id, project_id, cost_type, amount_usd, amount_mwk,
            description, agent_id, model, tokens, timestamp)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            cost_id,
            entry.project_id,
            entry.cost_type,
            entry.amount_usd,
            entry.amount_mwk,
            entry.description,
            entry.agent_id,
            entry.model,
            entry.tokens,
            now,
        ),
    )
    conn.commit()

    return {
        "id": cost_id,
        "status": "recorded",
        "timestamp": now,
        "amount_usd": entry.amount_usd,
    }


# ── Webhook Stubs (for gateway confirmations) ──────────────────────


@router.post("/webhooks/paychangu", tags=["webhooks"])
def paychangu_webhook_stub(payload: dict[str, Any]) -> dict[str, Any]:
    """Stub for PayChangu webhook — ready for merchant onboarding.

    When PayChangu is onboarded, this endpoint will:
    1. Verify the webhook signature (X-PayChangu-Signature header)
    2. Extract payment details from payload
    3. Write to revenue_transactions table
    4. Return 200 OK to acknowledge receipt

    Credentials will be stored in environment variables, never in the repo.
    """
    logger.info("PayChangu webhook received (stub): %s", payload.get("type", "unknown"))
    return {
        "status": "received",
        "message": "Webhook stub — merchant onboarding pending",
        "payload_type": payload.get("type", "unknown"),
    }


@router.post("/webhooks/airtel", tags=["webhooks"])
def airtel_webhook_stub(payload: dict[str, Any]) -> dict[str, Any]:
    """Stub for Airtel Money webhook — ready for merchant onboarding.

    When Airtel Money merchant is set up, this endpoint will:
    1. Verify the transaction via Airtel API
    2. Extract payment details
    3. Write to revenue_transactions table
    4. Return 200 OK

    Merchant number stored in AIRTEL_MERCHANT_NUMBER env var.
    """
    logger.info("Airtel Money webhook received (stub): %s", payload.get("type", "unknown"))
    return {
        "status": "received",
        "message": "Webhook stub — merchant onboarding pending",
        "payload_type": payload.get("type", "unknown"),
    }


@router.post("/webhooks/tnm", tags=["webhooks"])
def tnm_webhook_stub(payload: dict[str, Any]) -> dict[str, Any]:
    """Stub for TNM Mpamba webhook — ready for merchant onboarding.

    When TNM Mpamba merchant is set up, this endpoint will:
    1. Verify the transaction via TNM API
    2. Extract payment details
    3. Write to revenue_transactions table
    4. Return 200 OK

    Merchant number stored in TNM_MERCHANT_NUMBER env var.
    """
    logger.info("TNM Mpamba webhook received (stub): %s", payload.get("type", "unknown"))
    return {
        "status": "received",
        "message": "Webhook stub — merchant onboarding pending",
        "payload_type": payload.get("type", "unknown"),
    }


# ── Executive Briefing Aggregation ─────────────────────────────────


@router.get("/briefing", tags=["briefing"])
def get_executive_briefing() -> dict[str, Any]:
    """Aggregated executive briefing — priority-ordered attention items.

    Combines real data from:
    - Escalation alerts (high priority)
    - Pending approvals (medium priority)
    - Failed tasks (high priority)
    - Revenue/cost alerts (medium priority)
    - Workflow step failures (high priority)

    Returns a prioritized list of items that need CEO attention,
    plus summary metrics for the Company Core surface.
    """
    items: list[dict[str, Any]] = []
    item_id = 0

    # --- Escalations (high priority) ---
    try:
        db = get_database()
        if db is not None:
            conn = db.connect()
            rows = conn.execute(
                "SELECT task_id, rule_id, from_agent, to_agent, reason, timestamp "
                "FROM escalation_events WHERE resolved = 0 "
                "ORDER BY timestamp DESC LIMIT 10"
            ).fetchall()
            for row in rows:
                items.append(
                    {
                        "id": item_id,
                        "title": f"Escalation: {row['reason'][:80]}",
                        "source": f"{row['from_agent']} → {row['to_agent']}",
                        "priority": "high",
                        "type": "escalation",
                        "timestamp": row["timestamp"],
                        "task_id": row["task_id"],
                    }
                )
                item_id += 1
    except Exception:  # noqa: BLE001
        pass

    # Fallback: load from YAML if DB empty
    if not items:
        escalation_data = _load_yaml("orchestrator/escalation.yaml")
        for evt in escalation_data.get("events", [])[-10:]:
            if not evt.get("resolved", False):
                items.append(
                    {
                        "id": item_id,
                        "title": f"Escalation: {evt.get('reason', 'Unknown')[:80]}",
                        "source": f"{evt.get('from_agent', '?')} → {evt.get('to_agent', '?')}",
                        "priority": "high",
                        "type": "escalation",
                        "timestamp": evt.get("timestamp", ""),
                        "task_id": evt.get("task_id", ""),
                    }
                )
                item_id += 1

    # --- Pending approvals (medium priority) ---
    approvals_data = _load_yaml("orchestrator/approvals.yaml")
    now_iso = datetime.now(timezone.utc).isoformat()
    for req in approvals_data.get("requests", []):
        if req.get("status") == "pending" and (
            not req.get("expires_at") or req["expires_at"] > now_iso
        ):
            items.append(
                {
                    "id": item_id,
                    "title": req.get("action", "Approval pending")[:80],
                    "source": f"Agent: {req.get('agent_id', 'unknown')}",
                    "priority": "medium",
                    "type": "approval",
                    "timestamp": req.get("requested_at", ""),
                    "request_id": req.get("request_id", ""),
                }
            )
            item_id += 1

    # --- Failed tasks (high priority) ---
    tasks = _read_all_tasks()
    failed_tasks = [t for t in tasks if t.get("status") == "failed"][-5:]
    for task in failed_tasks:
        items.append(
            {
                "id": item_id,
                "title": f"Task failed: {task.get('instruction', task.get('name', 'Unknown'))[:60]}",
                "source": f"Agent: {task.get('receiver_id', 'unknown')}",
                "priority": "high",
                "type": "task_failed",
                "timestamp": task.get("updated_at", ""),
                "task_id": task.get("id", ""),
            }
        )
        item_id += 1

    # --- Revenue alerts (medium priority) ---
    try:
        if db is not None:
            conn = db.connect()
            rev_row = conn.execute(
                "SELECT SUM(amount) as total FROM revenue_transactions WHERE status = 'confirmed'"
            ).fetchone()
            cost_row = conn.execute("SELECT SUM(amount_usd) as total FROM project_costs").fetchone()
            total_rev = float(rev_row["total"] or 0) if rev_row else 0
            total_cost = float(cost_row["total"] or 0) if cost_row else 0

            if total_rev > 0 and total_cost > 0:
                margin_pct = ((total_rev / 1800) - total_cost) / (total_rev / 1800) * 100
                if margin_pct < 20:
                    items.append(
                        {
                            "id": item_id,
                            "title": f"Margin alert: {margin_pct:.1f}% (target: 50%+)",
                            "source": "Finance",
                            "priority": "medium",
                            "type": "finance",
                            "timestamp": now_iso,
                        }
                    )
                    item_id += 1
    except Exception:  # noqa: BLE001
        pass

    # --- Sort by priority ---
    priority_order = {"high": 0, "medium": 1, "low": 2}
    items.sort(key=lambda x: (priority_order.get(x["priority"], 3),), reverse=False)

    # --- Summary metrics for Company Core ---
    task_pipeline = {
        "pending": sum(1 for t in tasks if t.get("status") == "pending"),
        "in_progress": sum(1 for t in tasks if t.get("status") == "in_progress"),
        "completed": sum(1 for t in tasks if t.get("status") == "completed"),
        "failed": sum(1 for t in tasks if t.get("status") == "failed"),
    }

    # Compute health score via OrgHealthCalculator
    try:
        from ai_company.dashboard.org_health import OrgHealthCalculator

        health = OrgHealthCalculator().compute(database=get_database()).score
    except Exception:  # noqa: BLE001
        health = 85  # Fallback

    return {
        "items": items[:20],  # Cap at 20 items
        "summary": {
            "total_items": len(items),
            "high_priority": sum(1 for i in items if i["priority"] == "high"),
            "medium_priority": sum(1 for i in items if i["priority"] == "medium"),
            "low_priority": sum(1 for i in items if i["priority"] == "low"),
        },
        "company_health": health,
        "task_pipeline": task_pipeline,
        "generated_at": now_iso,
    }


# ── Org Health ────────────────────────────────────────────────────


@router.get("/org-health", tags=["org-health"])
def get_org_health(
    trend_limit: int = Query(30, ge=1, le=365, description="Number of trend data points"),
    component_detail: bool = Query(True, description="Include component breakdown"),
) -> dict[str, Any]:
    """Composite organisational health score.

    Returns a weighted score (0-100), health band (green/amber/red),
    per-component breakdown, and trend history from the KPI pipeline.
    """
    from ai_company.dashboard.org_health import OrgHealthCalculator

    calculator = OrgHealthCalculator()
    db = get_database()
    result = calculator.compute(database=db)

    trend: list[dict[str, Any]] = []
    if db is not None:
        try:
            from ai_company.data.kpi_pipeline import KPIPipeline

            pipeline = KPIPipeline(db)
            history = pipeline.get_history(
                "org_health", kpi_key="composite_score", limit=trend_limit
            )
            trend = [
                {"timestamp": row["timestamp"], "score": row["current_value"]}
                for row in reversed(history)
            ]
        except Exception:  # noqa: BLE001
            logger.debug("Org health trend unavailable")

    return result.to_dict(include_components=component_detail, trend=trend)


# ── Workflows / Mission Control ────────────────────────────────────


@router.get("/workflows", response_model=list[WorkflowSummary], tags=["workflows"])
def list_workflow_definitions() -> list[WorkflowSummary]:
    """List all registered workflow definitions."""
    from ai_company.dashboard.workflow_api import list_workflows

    return [WorkflowSummary(**w) for w in list_workflows()]


@router.get("/workflows/instances", tags=["workflows"])
def list_workflow_instances(
    workflow_id: str = "",
) -> list[dict[str, Any]]:
    """List running workflow instances, optionally filtered by workflow ID."""
    from ai_company.dashboard.workflow_api import list_instances

    return list_instances(workflow_id=workflow_id)


@router.get("/workflows/instances/{instance_id}", tags=["workflows"])
def get_workflow_instance(instance_id: str) -> dict[str, Any]:
    """Return full status + step detail for a workflow instance."""
    from ai_company.dashboard.workflow_api import (
        _build_instance_detail,
        get_instance_status,
    )

    status = get_instance_status(instance_id)
    if status is None:
        raise HTTPException(status_code=404, detail=f"Instance '{instance_id}' not found")
    return _build_instance_detail(status)


@router.post(
    "/workflows/{workflow_id}/start",
    status_code=201,
    tags=["workflows"],
)
def start_workflow_endpoint(
    workflow_id: str,
    _: Role = Depends(require_role("run")),
) -> dict[str, str]:
    """Start a new instance of a workflow definition."""
    from ai_company.dashboard.workflow_api import start_workflow

    try:
        instance_id = start_workflow(workflow_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"instance_id": instance_id}


@router.post(
    "/workflows/instances/{instance_id}/advance",
    tags=["workflows"],
)
def advance_workflow_endpoint(
    instance_id: str,
    _: Role = Depends(require_role("run")),
) -> dict[str, Any]:
    """Advance a workflow instance to its next step."""
    from ai_company.dashboard.workflow_api import advance_workflow

    try:
        result = advance_workflow(instance_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return result


@router.post(
    "/workflows/instances/{instance_id}/complete-step",
    tags=["workflows"],
)
def complete_step_endpoint(
    instance_id: str,
    body: WorkflowActionRequest | None = None,
    _: Role = Depends(require_role("run")),
) -> dict[str, Any]:
    """Mark the current step as completed with an optional result string."""
    from ai_company.dashboard.workflow_api import complete_step

    try:
        result = complete_step(instance_id, result=body.result if body else "")
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return result


@router.post(
    "/workflows/instances/{instance_id}/cancel",
    tags=["workflows"],
)
def cancel_workflow_endpoint(
    instance_id: str,
    _: Role = Depends(require_role("run")),
) -> dict[str, Any]:
    """Cancel a running workflow instance."""
    from ai_company.dashboard.workflow_api import cancel_workflow

    try:
        result = cancel_workflow(instance_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return result


# ── Agent Onboarding (HITL-gated) ──────────────────────────────────


@router.get("/onboarding", tags=["onboarding"])
def list_onboarding_requests(
    state: str = "",
) -> list[dict[str, Any]]:
    """List all agent onboarding requests, optionally filtered by state.

    States: pending_approval, generating, testing, active, archived.
    """
    from ai_company.services.onboarding import OnboardingService

    svc = OnboardingService()
    result = svc.list_requests(state=state)
    if not result.success:
        return []
    return result.data or []


@router.get("/onboarding/{request_id}", tags=["onboarding"])
def get_onboarding_status(request_id: str) -> dict[str, Any]:
    """Get the status of a specific onboarding request."""
    from ai_company.services.onboarding import OnboardingService

    svc = OnboardingService()
    result = svc.get_status(request_id)
    if not result.success:
        raise HTTPException(status_code=404, detail=f"Onboarding request '{request_id}' not found")
    return result.data or {}
