"""REST API endpoints for the CEO dashboard."""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from fastapi import APIRouter, BackgroundTasks, HTTPException

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


# ── Dashboard / KPIs ────────────────────────────────────────────────


@router.get("/dashboard", response_model=KPIs)
def get_dashboard(background_tasks: BackgroundTasks) -> KPIs:
    tasks = _load_json(".opencode/inbox.json")
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
    tasks = _load_json(".opencode/inbox.json")
    if status:
        tasks = [t for t in tasks if t.get("status") == status]
    if agent:
        tasks = [t for t in tasks if t.get("receiver_id") == agent or t.get("sender_id") == agent]
    return [TaskItem(**t) for t in tasks]


@router.post("/tasks", response_model=TaskItem, status_code=201)
def create_task(assign: TaskAssign) -> TaskItem:
    import uuid

    task = {
        "id": str(uuid.uuid4()),
        "sender_id": assign.sender_id,
        "receiver_id": assign.receiver_id,
        "instruction": assign.instruction,
        "status": "pending",
        "priority": assign.priority,
        "created_at": datetime.now().isoformat(),
    }
    tasks = _load_json(".opencode/inbox.json")
    tasks.append(task)
    _save_json(".opencode/inbox.json", tasks)
    return TaskItem(**task)


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
