"""REST API endpoints for the CEO dashboard."""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml
from fastapi import APIRouter, BackgroundTasks, HTTPException

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
    TaskAssign,
    TaskItem,
    TierInfo,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api")

# Module-level MessageBus instance. All task read/write operations are routed
# through this bus instead of touching `.opencode/inbox.json` directly (GAP-011).
# A broadcast callback forwards task lifecycle events to WebSocket clients.
_bus = None


def get_bus() -> MessageBus:
    """Return the shared :class:`MessageBus` instance (lazily created)."""
    global _bus
    if _bus is None:
        from ai_company.orchestrator.message_bus import MessageBus

        _bus = MessageBus(
            ".opencode/inbox.json",
            broadcast_callback=_bus_broadcast,
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
    """Return all tasks from the inbox as plain dicts via MessageBus."""
    return get_bus()._load_tasks()


def _load_tasks_dicts() -> list[dict[str, Any]]:
    """Backwards-compatible alias used by endpoints that need raw task dicts."""
    return _read_all_tasks()

_START_TIME = time.time()


# ── Helpers ─────────────────────────────────────────────────────────


def _load_json(path: str | Path) -> Any:
    p = Path(path)
    if not p.exists():
        return [] if str(p).endswith("json") else {}
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_yaml(path: str | Path) -> Any:
    p = Path(path)
    if not p.exists():
        return {}
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _save_json(path: str | Path, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)


def _save_yaml(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def _load_registry() -> list[dict]:
    return _load_json("company/agent-registry.json")


# ── WebSocket broadcast helpers ─────────────────────────────────────


async def _broadcast_kpis(data: dict[str, Any]) -> None:
    """Fire-and-forget broadcast of KPI data to WebSocket clients."""
    try:
        from ai_company.dashboard.ws import broadcast_kpi_update
        await broadcast_kpi_update(data)
    except Exception:
        logger.debug("WebSocket broadcast skipped (no event loop or clients)")


async def _broadcast_task(task: dict[str, Any], event: str) -> None:
    """Fire-and-forget broadcast of a task lifecycle event."""
    try:
        from ai_company.dashboard.ws import broadcast_task_update
        await broadcast_task_update(task, event)
    except Exception:
        logger.debug("WebSocket broadcast skipped (no event loop or clients)")


async def _broadcast_approval_alert(request: dict[str, Any]) -> None:
    """Fire-and-forget broadcast of an approval request to WebSocket clients."""
    try:
        from ai_company.dashboard.ws import broadcast_alert
        await broadcast_alert({
            "category": "approval",
            "request_id": request.get("id", ""),
            "action": request.get("action", ""),
            "agent_id": request.get("agent_id", ""),
            "tier": request.get("tier", 2),
        })
    except Exception:
        logger.debug("WebSocket broadcast skipped")


async def _broadcast_escalation_alert(event: dict[str, Any]) -> None:
    """Fire-and-forget broadcast of an escalation event to WebSocket clients."""
    try:
        from ai_company.dashboard.ws import broadcast_alert
        await broadcast_alert({
            "category": "escalation",
            "task_id": event.get("task_id", ""),
            "reason": event.get("reason", ""),
            "agent_id": event.get("agent_id", ""),
        })
    except Exception:
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


@router.get("/dashboard", response_model=KPIs)
def get_dashboard(background_tasks: BackgroundTasks) -> KPIs:
    tasks = _read_all_tasks()
    approvals_data = _load_yaml("orchestrator/approvals.yaml")
    escalations_data = _load_yaml("orchestrator/escalation.yaml")
    scheduler_data = _load_yaml("orchestrator/scheduler.yaml")
    registry = _load_registry()

    approval_requests = approvals_data.get("requests", [])
    escalation_events = escalations_data.get("events", [])
    scheduled = scheduler_data.get("tasks", [])

    now = datetime.now().isoformat()
    pending_approvals = [
        r for r in approval_requests
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


@router.get("/kpis/live")
def get_live_kpis(background_tasks: BackgroundTasks) -> dict[str, Any]:
    """Return live KPI values computed from operational data.

    Uses the KPI collectors to produce real-time snapshots for all
    7 departments (engineering, HR, finance, marketing, sales, CS, legal).
    Broadcasts the result to WebSocket clients.
    """
    from ai_company.dashboard.kpis import collect_all_kpis

    result = collect_all_kpis()
    background_tasks.add_task(_broadcast_kpis, result)
    return result


# ── Agents ──────────────────────────────────────────────────────────


@router.get("/agents", response_model=list[AgentSummary])
def list_agents() -> list[AgentSummary]:
    return [AgentSummary(**a) for a in _load_registry()]


@router.get("/agents/{name}", response_model=AgentSummary)
def get_agent(name: str) -> AgentSummary:
    registry = {a["name"]: a for a in _load_registry()}
    if name not in registry:
        raise HTTPException(status_code=404, detail=f"Agent '{name}' not found")
    return AgentSummary(**registry[name])


# ── Org Chart ───────────────────────────────────────────────────────


@router.get("/org-chart", response_model=list[OrgNode])
def get_org_chart() -> list[OrgNode]:
    registry = {a["name"]: a for a in _load_registry()}
    children_map: dict[str, list[str]] = {}
    for a in _load_registry():
        parent = a.get("reportsTo", "")
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


@router.get("/tasks", response_model=list[TaskItem])
def list_tasks(
    status: str = "",
    agent: str = "",
) -> list[TaskItem]:
    tasks = _read_all_tasks()
    if status:
        tasks = [t for t in tasks if t.get("status") == status]
    if agent:
        tasks = [t for t in tasks if t.get("receiver_id") == agent or t.get("sender_id") == agent]
    return [TaskItem(**t) for t in tasks]


@router.post("/tasks", response_model=TaskItem, status_code=201)
def create_task(assign: TaskAssign, background_tasks: BackgroundTasks) -> TaskItem:
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
        created_at=datetime.now().isoformat(),
    )
    get_bus().send_task(task)

    # Broadcast task creation to WebSocket clients
    background_tasks.add_task(_broadcast_task, task.model_dump(), "created")

    return TaskItem(**task.model_dump())


# ── Approvals ───────────────────────────────────────────────────────


@router.get("/approvals", response_model=list[ApprovalItem])
def list_approvals() -> list[ApprovalItem]:
    data = _load_yaml("orchestrator/approvals.yaml")
    now = datetime.now().isoformat()
    requests = data.get("requests", [])
    return [
        ApprovalItem(**r)
        for r in requests
        if r.get("status") == "pending" and (not r.get("expires_at") or r["expires_at"] > now)
    ]


@router.post("/approvals/{request_id}/approve")
def approve_request(request_id: str, body: ApprovalDecision | None = None) -> dict:
    data = _load_yaml("orchestrator/approvals.yaml")
    requests = data.get("requests", [])
    for r in requests:
        if r["id"] == request_id and r.get("status") == "pending":
            r["status"] = "approved"
            r["responded_at"] = datetime.now().isoformat()
            r["response_by"] = (body.approved_by if body else "human-ceo")
            if body and body.notes:
                r["notes"] = body.notes
            _save_yaml("orchestrator/approvals.yaml", data)
            return {"ok": True, "id": request_id}
    raise HTTPException(status_code=404, detail=f"Request '{request_id}' not found or already processed")


@router.post("/approvals/{request_id}/reject")
def reject_request(request_id: str, body: ApprovalDecision | None = None) -> dict:
    data = _load_yaml("orchestrator/approvals.yaml")
    requests = data.get("requests", [])
    for r in requests:
        if r["id"] == request_id and r.get("status") == "pending":
            r["status"] = "rejected"
            r["responded_at"] = datetime.now().isoformat()
            r["response_by"] = (body.approved_by if body else "human-ceo")
            if body and body.notes:
                r["notes"] = body.notes
            _save_yaml("orchestrator/approvals.yaml", data)
            return {"ok": True, "id": request_id}
    raise HTTPException(status_code=404, detail=f"Request '{request_id}' not found or already processed")


# ── Escalations ─────────────────────────────────────────────────────


@router.get("/escalations", response_model=list[EscalationItem])
def list_escalations() -> list[EscalationItem]:
    data = _load_yaml("orchestrator/escalation.yaml")
    events = data.get("events", [])
    return [EscalationItem(**e) for e in events if not e.get("resolved", False)]


@router.post("/escalations/{task_id}/resolve")
def resolve_escalation(task_id: str) -> dict:
    data = _load_yaml("orchestrator/escalation.yaml")
    events = data.get("events", [])
    for e in events:
        if e.get("task_id") == task_id and not e.get("resolved", False):
            e["resolved"] = True
            _save_yaml("orchestrator/escalation.yaml", data)
            return {"ok": True, "task_id": task_id}
    raise HTTPException(status_code=404, detail=f"No open escalation for task '{task_id}'")


# ── Departments ─────────────────────────────────────────────────────


@router.get("/departments", response_model=list[DepartmentInfo])
def list_departments() -> list[DepartmentInfo]:
    data = _load_yaml("company/departments.yaml")
    return [DepartmentInfo(**d) for d in data.get("departments", [])]


# ── Models ──────────────────────────────────────────────────────────


@router.get("/models", response_model=list[ModelRouteItem])
def list_model_routes() -> list[ModelRouteItem]:
    from ai_company.model_router import ModelRouter

    router_instance = ModelRouter()
    results = router_instance.resolve_all_agents()
    return [
        ModelRouteItem(agent=name, provider=r.provider, model=r.model, tier=r.tier, reason=r.reason)
        for name, r in sorted(results.items())
    ]


@router.get("/models/tiers", response_model=list[TierInfo])
def list_model_tiers() -> list[TierInfo]:
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


@router.get("/scheduler")
def list_scheduled() -> list[dict]:
    data = _load_yaml("orchestrator/scheduler.yaml")
    return data.get("tasks", [])


# ── Department KPIs ────────────────────────────────────────────────


@router.get("/departments/{dept_name}/kpis")
def get_department_kpis(dept_name: str) -> dict:
    """Return KPI definitions for a specific department."""
    kpi_data = _load_yaml("company/config/kpis.yaml")
    departments = kpi_data.get("departments", {})
    if dept_name not in departments:
        raise HTTPException(status_code=404, detail=f"Department '{dept_name}' not found in KPI config")
    return departments[dept_name]


@router.get("/kpis")
def list_all_kpis() -> dict:
    """Return all department KPI definitions."""
    kpi_data = _load_yaml("company/config/kpis.yaml")
    return kpi_data.get("departments", {})


@router.get("/kpis/summary")
def kpi_summary() -> list[dict]:
    """Return a flat summary of all KPIs across departments."""
    kpi_data = _load_yaml("company/config/kpis.yaml")
    summary = []
    for dept_id, dept in kpi_data.get("departments", {}).items():
        for kpi in dept.get("kpis", []):
            summary.append({
                "department": dept_id,
                "department_name": dept.get("name", dept_id),
                "kpi_id": kpi["id"],
                "name": kpi["name"],
                "target": kpi.get("target"),
                "unit": kpi.get("unit", ""),
                "frequency": kpi.get("frequency", ""),
            })
    return summary


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
    now_iso = datetime.now().isoformat()
    pending_approvals = [
        r for r in approval_requests
        if r.get("status") == "pending"
        and (not r.get("expires_at") or r["expires_at"] > now_iso)
    ]

    # Scheduled tasks
    scheduler_data = _load_yaml("orchestrator/scheduler.yaml")
    scheduled = scheduler_data.get("tasks", [])

    result = {
        "collected_at": kpi_snapshot["collected_at"],
        "company_health": {
            "departments": {
                dept: data.get("kpis", {})
                for dept, data in departments.items()
            },
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
        a for a in registry
        if (a.get("department") or "").lower() == dept_name.lower()
        or (a.get("department") or "").replace(" ", "_").lower() == dept_name.lower()
    ]

    # Task stats for this department
    tasks = _read_all_tasks()
    dept_agent_names = {a["name"] for a in dept_agents}
    dept_tasks = [
        t for t in tasks
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
        e for e in escalation_events
        if e.get("from_agent") in dept_agent_names or e.get("to_agent") in dept_agent_names
    ]

    result = {
        "department": dept_name,
        "collected_at": dept_kpis.get("collected_at", datetime.now().isoformat()),
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
    except Exception:
        logger.debug("Failed to store KPI snapshot for history")

    return {
        "evaluated_at": datetime.now().isoformat(),
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

    snapshot = collect_all_kpis()

    # Store in history
    store = KPIHistoryStore()
    stored_count = store.store_snapshot(snapshot)

    result = {
        **snapshot,
        "stored_entries": stored_count,
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


# ── Agent Performance ─────────────────────────────────────────────


@router.get("/agents/performance")
def get_agent_performance() -> dict[str, Any]:
    """Return per-agent performance metrics computed from task history.

    Returns a summary with:
    - Total tasks assigned/received per agent
    - Completion rate, failure rate
    - Average response time estimates
    """
    tasks = _read_all_tasks()
    registry = _load_registry()

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

    # Compute rates
    for stats in agent_stats.values():
        total = stats["total_received"]
        if total > 0:
            stats["completion_rate"] = round((stats["completed"] / total) * 100, 1)
            stats["failure_rate"] = round((stats["failed"] / total) * 100, 1)

    # Sort by completion rate descending
    sorted_agents = sorted(
        agent_stats.values(),
        key=lambda a: a["completion_rate"],
        reverse=True,
    )

    return {
        "agents": sorted_agents,
        "total_tasks": len(tasks),
        "agents_with_tasks": sum(1 for a in sorted_agents if a["total_received"] > 0),
    }


# ── Cost Tracking ─────────────────────────────────────────────────


@router.get("/costs/summary")
def get_cost_summary(background_tasks: BackgroundTasks) -> dict[str, Any]:
    """Return cost tracking summary from cost tracker and audit log.

    Includes:
    - Budget utilization
    - LLM spend breakdown by provider
    - Per-agent cost breakdown
    - Historical cost trend (from KPI history store)
    """
    tasks = _read_all_tasks()
    cost_data = _load_json("orchestrator/cost_tracker.json")

    # Parse cost tracker
    total_budget: float = 0.0
    total_spent: float = 0.0
    llm_spend: float = 0.0
    if isinstance(cost_data, dict):
        total_budget = cost_data.get("total_budget", 0.0)
        total_spent = cost_data.get("total_spent", 0.0)
        llm_spend = cost_data.get("llm_spend", 0.0)

    budget_utilization = (
        round((total_spent / total_budget * 100), 1) if total_budget > 0 else 0.0
    )

    # Per-agent cost breakdown from audit log
    agent_costs: dict[str, dict[str, Any]] = {}
    audit_path = Path(".opencode/audit.jsonl")
    if audit_path.exists():
        try:
            with open(audit_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        event = json.loads(line)
                        meta = event.get("metadata", {})
                        cost = float(meta.get("cost", 0))
                        agent = meta.get("agent_id", event.get("agent_id", "unknown"))
                        if agent not in agent_costs:
                            agent_costs[agent] = {"total_cost": 0.0, "calls": 0}
                        agent_costs[agent]["total_cost"] += cost
                        agent_costs[agent]["calls"] += 1
                    except (json.JSONDecodeError, TypeError, ValueError):
                        continue
        except OSError:
            pass

    # Build per-agent cost list
    per_agent = []
    for agent_name, cost_info in sorted(
        agent_costs.items(), key=lambda x: x[1]["total_cost"], reverse=True
    ):
        calls = cost_info["calls"]
        total = cost_info["total_cost"]
        per_agent.append({
            "agent": agent_name,
            "total_cost": round(total, 6),
            "calls": calls,
            "avg_cost_per_call": round(total / calls, 6) if calls > 0 else 0.0,
        })

    # Total completed tasks for cost-per-task calc
    completed = sum(1 for t in tasks if t.get("status") == "completed")
    total_tasks = len(tasks)
    avg_per_task = (
        round(total_spent / completed, 6) if completed > 0 else 0.0
    )

    # KPI history for trend
    from ai_company.dashboard.analytics import KPIHistoryStore

    store = KPIHistoryStore()
    finance_history = store.get_history("finance", kpi_key="budget_utilization", limit=50)
    trend_data = [
        {"timestamp": e.timestamp, "value": e.current}
        for e in finance_history
    ]

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


# ── Prometheus-compatible metrics ────────────────────────────────────


@router.get("/metrics")
def prometheus_metrics() -> str:
    """Expose Prometheus-compatible metrics in text format.

    Metrics exposed:
      - ai_company_tasks_total{status="..."}   — task count by status
      - ai_company_agents_total                  — registered agent count
      - ai_company_llm_calls_total               — LLM call count (from audit log)
      - ai_company_cost_total_usd                — estimated total cost
      - ai_company_errors_total                  — error event count
      - ai_company_uptime_seconds                — dashboard uptime
    """
    tasks = _read_all_tasks()
    registry = _load_registry()
    uptime = time.time() - _START_TIME

    # Task counts by status
    task_status_counts: dict[str, int] = {}
    for t in tasks:
        status = t.get("status", "unknown")
        task_status_counts[status] = task_status_counts.get(status, 0) + 1

    # Audit-based metrics
    llm_calls = 0
    error_count = 0
    cost_total = 0.0

    audit_path = Path(".opencode/audit.jsonl")
    if audit_path.exists():
        try:
            with open(audit_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        event = json.loads(line)
                        event_type = event.get("event_type", "")
                        if event_type in ("tool_call", "tool_result"):
                            llm_calls += 1
                        if event_type == "error":
                            error_count += 1
                        # Extract cost from metadata if present
                        meta = event.get("metadata", {})
                        if "cost" in meta:
                            cost_total += float(meta["cost"])
                    except (json.JSONDecodeError, TypeError):
                        continue
        except OSError:
            pass

    # Build Prometheus text format
    lines: list[str] = []
    lines.append("# HELP ai_company_tasks_total Total tasks by status")
    lines.append("# TYPE ai_company_tasks_total gauge")
    for status, count in task_status_counts.items():
        lines.append(f'ai_company_tasks_total{{status="{status}"}} {count}')

    lines.append("# HELP ai_company_agents_total Total registered agents")
    lines.append("# TYPE ai_company_agents_total gauge")
    lines.append(f"ai_company_agents_total {len(registry)}")

    lines.append("# HELP ai_company_llm_calls_total Total LLM invocations")
    lines.append("# TYPE ai_company_llm_calls_total counter")
    lines.append(f"ai_company_llm_calls_total {llm_calls}")

    lines.append("# HELP ai_company_cost_total_usd Estimated total cost in USD")
    lines.append("# TYPE ai_company_cost_total_usd gauge")
    lines.append(f"ai_company_cost_total_usd {cost_total:.4f}")

    lines.append("# HELP ai_company_errors_total Total error events")
    lines.append("# TYPE ai_company_errors_total counter")
    lines.append(f"ai_company_errors_total {error_count}")

    lines.append("# HELP ai_company_uptime_seconds Dashboard uptime in seconds")
    lines.append("# TYPE ai_company_uptime_seconds gauge")
    lines.append(f"ai_company_uptime_seconds {uptime:.1f}")

    return "\n".join(lines) + "\n"
