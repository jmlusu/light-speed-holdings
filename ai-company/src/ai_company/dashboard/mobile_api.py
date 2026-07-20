"""Mobile-optimized API endpoints for the CEO dashboard.

Provides condensed payloads, pagination, batch actions, and offline sync
for mobile and low-bandwidth clients.
"""

from __future__ import annotations

import json
import logging
import uuid
from base64 import b64decode, b64encode
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_company.dashboard.repository import get_state_store

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/mobile")

# ── Helpers (shared with main api.py) ───────────────────────────────
# GAP-011: route all state I/O through the StateStore repository.
_store = get_state_store()


def _load_json(path: str | Path) -> Any:
    return _store.read_json(path, default={})


def _load_yaml(path: str | Path) -> Any:
    return _store.read_yaml(path, default={})


def _save_json(path: str | Path, data: Any) -> None:
    _store.write_json(path, data)


def _save_yaml(path: str | Path, data: Any) -> None:
    _store.write_yaml(path, data)


def _load_registry() -> list[dict]:
    return _load_json("company/agent-registry.json") or []


def _truncate(text: str, max_len: int = 60) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def _format_short_time(iso_str: str | None) -> str:
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%H:%M")
    except (ValueError, TypeError):
        return ""


def _encode_cursor(data: dict) -> str:
    return b64encode(json.dumps(data, default=str).encode()).decode()


def _decode_cursor(cursor: str) -> dict:
    try:
        return json.loads(b64decode(cursor.encode()).decode())
    except Exception:
        return {}


# ── Request / Response Models ────────────────────────────────────────


class MobileDashboardKPIs(BaseModel):
    pending: int = 0
    completed: int = 0
    escalations: int = 0
    approvals: int = 0
    agents: int = 0


class MobileUrgentAlerts(BaseModel):
    approval_count: int = 0
    escalation_count: int = 0
    failed_count: int = 0


class MobileTaskSummary(BaseModel):
    id: str
    to: str
    instruction: str
    priority: str
    status: str
    created: str


class MobileDashboardSummary(BaseModel):
    kpis: MobileDashboardKPIs
    urgent: MobileUrgentAlerts
    recent_tasks: list[MobileTaskSummary] = Field(default_factory=list)
    connection: str = "live"
    updated_at: str = ""


class PaginatedTaskItem(BaseModel):
    id: str
    from_: str = Field(alias="from")
    to: str
    instruction: str
    priority: str
    status: str
    created: str
    has_result: bool = False

    model_config = {"populate_by_name": True}


class PaginatedTaskList(BaseModel):
    items: list[dict[str, Any]] = Field(default_factory=list)
    next_cursor: str | None = None
    total_count: int = 0
    page_size: int = 20
    has_more: bool = False


class BatchAction(BaseModel):
    type: str
    target_id: str
    notes: str | None = None
    delegate_to: str | None = None


class BatchRequest(BaseModel):
    actions: list[BatchAction] = Field(default_factory=list)
    continue_on_error: bool = False


class SwipeDecision(BaseModel):
    request_id: str
    decision: str  # "approve" | "reject" | "skip"
    gesture: dict[str, Any] | None = None
    notes: str = ""


class DeviceRegistration(BaseModel):
    device_token: str
    platform: str = "web"
    app_version: str = ""
    device_name: str = ""
    preferences: dict[str, Any] = Field(default_factory=dict)


class QuickApproveRequest(BaseModel):
    confirm: bool = False
    notes: str = ""


class SyncRequest(BaseModel):
    last_sync_at: str | None = None
    pending_actions: list[dict[str, Any]] = Field(default_factory=list)
    device_token: str | None = None


# ── Device Store ─────────────────────────────────────────────────────

DEVICE_STORE = Path("orchestrator/devices.yaml")


def _load_devices() -> list[dict]:
    data = _load_yaml(DEVICE_STORE)
    return data.get("devices", [])


def _save_devices(devices: list[dict]) -> None:
    _save_yaml(DEVICE_STORE, {"devices": devices})


# ── Mobile Dashboard Summary ─────────────────────────────────────────


@router.get("/dashboard", response_model=MobileDashboardSummary)
def mobile_dashboard(compact: bool = True) -> MobileDashboardSummary:
    """Condensed dashboard summary for mobile clients."""
    tasks = _load_json(".opencode/inbox.json")
    approvals_data = _load_yaml("orchestrator/approvals.yaml")
    escalations_data = _load_yaml("orchestrator/escalation.yaml")
    registry = _load_registry()

    approval_requests = approvals_data.get("requests", [])
    escalation_events = escalations_data.get("events", [])

    now = datetime.now(timezone.utc).isoformat()
    pending_approvals = [
        r for r in approval_requests
        if r.get("status") == "pending" and (not r.get("expires_at") or r["expires_at"] > now)
    ]
    open_escalations = [e for e in escalation_events if not e.get("resolved", False)]

    pending_tasks = sum(1 for t in tasks if t.get("status") == "pending")
    completed_tasks = sum(1 for t in tasks if t.get("status") == "completed")
    failed_tasks = sum(1 for t in tasks if t.get("status") == "failed")

    # Recent tasks (max 5, compact format)
    recent = []
    for t in tasks[:5]:
        recent.append(MobileTaskSummary(
            id=t.get("id", "")[:8],
            to=t.get("receiver_id", ""),
            instruction=_truncate(t.get("instruction", "")),
            priority=t.get("priority", "medium"),
            status=t.get("status", "pending"),
            created=_format_short_time(t.get("created_at")),
        ))

    return MobileDashboardSummary(
        kpis=MobileDashboardKPIs(
            pending=pending_tasks,
            completed=completed_tasks,
            escalations=len(open_escalations),
            approvals=len(pending_approvals),
            agents=len(registry),
        ),
        urgent=MobileUrgentAlerts(
            approval_count=len(pending_approvals),
            escalation_count=len(open_escalations),
            failed_count=failed_tasks,
        ),
        recent_tasks=recent,
        connection="live",
        updated_at=datetime.now(timezone.utc).isoformat(),
    )


# ── Paginated Task List ─────────────────────────────────────────────


@router.get("/tasks")
def mobile_tasks(
    status: str = "",
    agent: str = "",
    priority: str = "",
    cursor: str = "",
    limit: int = 20,
) -> dict[str, Any]:
    """Paginated task list with cursor-based navigation."""
    limit = min(limit, 50)
    tasks = _load_json(".opencode/inbox.json")

    # Apply filters
    if status:
        tasks = [t for t in tasks if t.get("status") == status]
    if agent:
        tasks = [t for t in tasks if t.get("receiver_id") == agent or t.get("sender_id") == agent]
    if priority:
        tasks = [t for t in tasks if t.get("priority") == priority]

    total_count = len(tasks)

    # Cursor-based pagination
    start_idx = 0
    if cursor:
        cursor_data = _decode_cursor(cursor)
        after_id = cursor_data.get("after_id", "")
        if after_id:
            for i, t in enumerate(tasks):
                if t.get("id") == after_id:
                    start_idx = i + 1
                    break

    page = tasks[start_idx: start_idx + limit]
    has_more = (start_idx + limit) < total_count

    next_cursor = None
    if has_more and page:
        next_cursor = _encode_cursor({"after_id": page[-1].get("id", "")})

    items = []
    for t in page:
        items.append({
            "id": t.get("id", "")[:8],
            "from": t.get("sender_id", ""),
            "to": t.get("receiver_id", ""),
            "instruction": _truncate(t.get("instruction", ""), 80),
            "priority": t.get("priority", "medium"),
            "status": t.get("status", "pending"),
            "created": t.get("created_at", ""),
            "has_result": bool(t.get("result")),
        })

    return {
        "items": items,
        "next_cursor": next_cursor,
        "total_count": total_count,
        "page_size": limit,
        "has_more": has_more,
    }


# ── Batch Actions ───────────────────────────────────────────────────


@router.post("/actions/batch")
def batch_actions(req: BatchRequest) -> dict[str, Any]:
    """Execute multiple approve/reject/resolve actions in one request."""
    results = []
    succeeded = 0
    failed = 0

    for action in req.actions[:10]:
        result = _execute_action(action)
        results.append(result)
        if result.get("ok"):
            succeeded += 1
        else:
            failed += 1
            if not req.continue_on_error:
                break

    return {
        "results": results,
        "succeeded": succeeded,
        "failed": failed,
    }


def _execute_action(action: BatchAction) -> dict[str, Any]:
    """Execute a single action and return its result."""
    if action.type == "approve":
        return _approve_request(action.target_id, action.notes)
    elif action.type == "reject":
        return _reject_request(action.target_id, action.notes)
    elif action.type == "resolve_escalation":
        return _resolve_escalation(action.target_id)
    elif action.type == "delegate":
        return _delegate_task(action.target_id, action.delegate_to or "")
    else:
        return {"type": action.type, "target_id": action.target_id, "ok": False, "error": "Unknown action type"}


def _approve_request(request_id: str, notes: str | None = None) -> dict[str, Any]:
    data = _load_yaml("orchestrator/approvals.yaml")
    for r in data.get("requests", []):
        if r["id"] == request_id and r.get("status") == "pending":
            r["status"] = "approved"
            r["responded_at"] = datetime.now(timezone.utc).isoformat()
            r["response_by"] = "human-ceo"
            if notes:
                r["notes"] = notes
            _save_yaml("orchestrator/approvals.yaml", data)
            return {"type": "approve", "target_id": request_id, "ok": True}
    return {"type": "approve", "target_id": request_id, "ok": False, "error": "Not found or already processed"}


def _reject_request(request_id: str, notes: str | None = None) -> dict[str, Any]:
    data = _load_yaml("orchestrator/approvals.yaml")
    for r in data.get("requests", []):
        if r["id"] == request_id and r.get("status") == "pending":
            r["status"] = "rejected"
            r["responded_at"] = datetime.now(timezone.utc).isoformat()
            r["response_by"] = "human-ceo"
            if notes:
                r["notes"] = notes
            _save_yaml("orchestrator/approvals.yaml", data)
            return {"type": "reject", "target_id": request_id, "ok": True}
    return {"type": "reject", "target_id": request_id, "ok": False, "error": "Not found or already processed"}


def _resolve_escalation(task_id: str) -> dict[str, Any]:
    data = _load_yaml("orchestrator/escalation.yaml")
    for e in data.get("events", []):
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
                    reason=e.get("reason", "resolved via mobile"),
                    rule_id=e.get("rule_id", ""),
                    resolved=True,
                )
            except Exception:
                logger.debug("audit hook skipped for escalation resolution")
            return {"type": "resolve_escalation", "target_id": task_id, "ok": True}
    return {"type": "resolve_escalation", "target_id": task_id, "ok": False, "error": "No open escalation found"}


def _delegate_task(task_id: str, delegate_to: str) -> dict[str, Any]:
    if not delegate_to:
        return {"type": "delegate", "target_id": task_id, "ok": False, "error": "No delegate target specified"}
    tasks = _load_json(".opencode/inbox.json")
    for t in tasks:
        if t.get("id", "")[:8] == task_id or t.get("id") == task_id:
            t["receiver_id"] = delegate_to
            _save_json(".opencode/inbox.json", tasks)
            return {"type": "delegate", "target_id": task_id, "ok": True, "delegated_to": delegate_to}
    return {"type": "delegate", "target_id": task_id, "ok": False, "error": "Task not found"}


# ── Quick Approve All ────────────────────────────────────────────────


@router.post("/actions/quick-approve")
def quick_approve(req: QuickApproveRequest) -> dict[str, Any]:
    """One-tap approve all pending approvals."""
    if not req.confirm:
        raise HTTPException(status_code=400, detail="Must set confirm=true to quick-approve")

    data = _load_yaml("orchestrator/approvals.yaml")
    now = datetime.now(timezone.utc).isoformat()
    approved_ids = []

    for r in data.get("requests", []):
        if r.get("status") == "pending" and (not r.get("expires_at") or r["expires_at"] > now):
            r["status"] = "approved"
            r["responded_at"] = now
            r["response_by"] = "human-ceo"
            if req.notes:
                r["notes"] = req.notes
            approved_ids.append(r["id"])

    _save_yaml("orchestrator/approvals.yaml", data)
    return {"approved_count": len(approved_ids), "ids": approved_ids}


# ── Swipe Approvals Stack ────────────────────────────────────────────


@router.get("/approvals/stack")
def approval_stack(limit: int = 5) -> dict[str, Any]:
    """Return approval requests as a swipe stack."""
    limit = min(limit, 10)
    data = _load_yaml("orchestrator/approvals.yaml")
    now = datetime.now(timezone.utc).isoformat()

    pending = [
        r for r in data.get("requests", [])
        if r.get("status") == "pending" and (not r.get("expires_at") or r["expires_at"] > now)
    ]

    current = None
    stack = []

    if pending:
        first = pending[0]
        current = {
            "id": first.get("id", ""),
            "agent_id": first.get("agent_id", ""),
            "action": first.get("action", ""),
            "description": first.get("description", ""),
            "priority": first.get("priority", "medium"),
            "requested_at": first.get("requested_at", ""),
            "expires_at": first.get("expires_at", ""),
            "context": {
                "department": first.get("department", ""),
                "estimated_impact": first.get("impact", "unknown"),
            },
        }
        for p in pending[1: limit + 1]:
            stack.append({
                "id": p.get("id", ""),
                "agent_id": p.get("agent_id", ""),
                "action": p.get("action", ""),
                "description": _truncate(p.get("description", ""), 40),
                "priority": p.get("priority", "medium"),
            })

    return {
        "current": current,
        "stack": stack,
        "remaining_count": max(0, len(pending) - 1 - len(stack)),
        "total_pending": len(pending),
    }


@router.post("/approvals/swipe")
def swipe_approval(req: SwipeDecision) -> dict[str, Any]:
    """Process a swipe gesture on an approval request."""
    next_item = None
    remaining = 0

    if req.decision == "approve":
        result = _approve_request(req.request_id, req.notes or None)
    elif req.decision == "reject":
        result = _reject_request(req.request_id, req.notes or None)
    elif req.decision == "skip":
        result = {"type": "skip", "target_id": req.request_id, "ok": True}
    else:
        raise HTTPException(status_code=400, detail=f"Invalid decision: {req.decision}")

    if not result.get("ok") and req.decision != "skip":
        raise HTTPException(status_code=404, detail=result.get("error", "Action failed"))

    # Fetch next item in stack
    data = _load_yaml("orchestrator/approvals.yaml")
    now = datetime.now(timezone.utc).isoformat()
    pending = [
        r for r in data.get("requests", [])
        if r.get("status") == "pending" and (not r.get("expires_at") or r["expires_at"] > now)
    ]

    if pending:
        first = pending[0]
        next_item = {
            "id": first.get("id", ""),
            "agent_id": first.get("agent_id", ""),
            "action": first.get("action", ""),
            "description": _truncate(first.get("description", ""), 40),
            "priority": first.get("priority", "medium"),
        }
        remaining = len(pending) - 1

    return {
        "ok": True,
        "decision": req.decision,
        "next": next_item,
        "remaining_count": remaining,
    }


# ── Compact KPIs ─────────────────────────────────────────────────────


@router.get("/kpis/compact")
def compact_kpis() -> dict[str, Any]:
    """Minimal KPI payload for widgets and badges."""
    tasks = _load_json(".opencode/inbox.json")
    approvals_data = _load_yaml("orchestrator/approvals.yaml")
    escalations_data = _load_yaml("orchestrator/escalation.yaml")

    now = datetime.now(timezone.utc).isoformat()
    pending_approvals = sum(
        1 for r in approvals_data.get("requests", [])
        if r.get("status") == "pending" and (not r.get("expires_at") or r["expires_at"] > now)
    )
    open_escalations = sum(
        1 for e in escalations_data.get("events", [])
        if not e.get("resolved", False)
    )

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    completed_today = sum(
        1 for t in tasks
        if t.get("status") == "completed"
        and t.get("completed_at", "").startswith(today)
    )

    return {
        "pending": sum(1 for t in tasks if t.get("status") == "pending"),
        "approvals": pending_approvals,
        "escalations": open_escalations,
        "completed_today": completed_today,
        "failed": sum(1 for t in tasks if t.get("status") == "failed"),
    }


# ── KPI Trend (sparkline data) ───────────────────────────────────────


@router.get("/kpis/trend")
def kpi_trend(metric: str = "pending", hours: int = 24) -> dict[str, Any]:
    """Return trend data points for a KPI metric (for sparkline charts)."""
    if not _store.list_snapshot_files():
        return {
            "metric": metric,
            "unit": "count",
            "data_points": [],
            "current": 0,
            "min": 0,
            "max": 0,
            "trend": "stable",
        }

    # Collect snapshot values
    data_points = []
    cutoff = datetime.now(timezone.utc).timestamp() - (hours * 3600)

    for snap_file in _store.list_snapshot_files("snapshot-*.json"):
        try:
            snap = _store.read_snapshot(snap_file)
            if snap is None:
                continue
            ts_str = snap_file.stem.replace("snapshot-", "")
            # Parse timestamp
            ts = datetime.strptime(ts_str, "%Y%m%d-%H%M%S")
            if ts.timestamp() >= cutoff:
                # Extract metric value from engineering KPIs for now
                eng = snap.get("departments", {}).get("engineering", {}).get("kpis", {})
                value = eng.get(metric, {}).get("current", 0) if isinstance(eng.get(metric), dict) else 0
                data_points.append({
                    "ts": ts.isoformat() + "Z",
                    "v": value,
                })
        except Exception:
            continue

    values = [dp["v"] for dp in data_points if isinstance(dp["v"], (int, float))]
    current = values[-1] if values else 0

    # Simple trend detection
    trend = "stable"
    if len(values) >= 2:
        recent_avg = sum(values[-3:]) / min(3, len(values))
        older_avg = sum(values[:3]) / min(3, len(values))
        if recent_avg > older_avg * 1.1:
            trend = "increasing"
        elif recent_avg < older_avg * 0.9:
            trend = "decreasing"

    return {
        "metric": metric,
        "unit": "count",
        "data_points": data_points,
        "current": current,
        "min": min(values) if values else 0,
        "max": max(values) if values else 0,
        "trend": trend,
    }


# ── Push Notification Registration ───────────────────────────────────


@router.post("/notifications/register")
def register_device(reg: DeviceRegistration) -> dict[str, Any]:
    """Register a device for push notifications."""
    devices = _load_devices()

    # Check for existing device (update token if same device_id)
    existing = None
    for d in devices:
        if d.get("device_token") == reg.device_token:
            existing = d
            break

    if existing:
        existing["app_version"] = reg.app_version
        existing["device_name"] = reg.device_name
        existing["preferences"] = reg.preferences
        existing["last_active_at"] = datetime.now(timezone.utc).isoformat()
    else:
        device_entry = {
            "device_id": f"dev_{uuid.uuid4().hex[:12]}",
            "device_token": reg.device_token,
            "platform": reg.platform,
            "app_version": reg.app_version,
            "device_name": reg.device_name,
            "preferences": reg.preferences or {
                "escalations": True,
                "approvals": True,
                "budget_alerts": True,
                "task_complete": False,
                "daily_summary": True,
            },
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "last_active_at": datetime.now(timezone.utc).isoformat(),
            "is_active": True,
        }
        devices.append(device_entry)
        existing = device_entry

    _save_devices(devices)
    return {
        "ok": True,
        "device_id": existing.get("device_id", ""),
        "registered_at": existing.get("registered_at", ""),
    }


@router.delete("/notifications/unregister")
def unregister_device(body: dict[str, Any]) -> dict[str, Any]:
    """Remove a device from push notification delivery."""
    token = body.get("device_token", "")
    if not token:
        raise HTTPException(status_code=400, detail="device_token required")

    devices = _load_devices()
    before = len(devices)
    devices = [d for d in devices if d.get("device_token") != token]
    _save_devices(devices)

    return {"ok": True, "removed": before - len(devices)}


@router.patch("/notifications/preferences")
def update_preferences(body: dict[str, Any]) -> dict[str, Any]:
    """Update notification preferences for a device."""
    token = body.get("device_token", "")
    prefs = body.get("preferences", {})
    if not token:
        raise HTTPException(status_code=400, detail="device_token required")

    devices = _load_devices()
    updated_fields = []

    for d in devices:
        if d.get("device_token") == token:
            current_prefs = d.get("preferences", {})
            for key, value in prefs.items():
                if key in current_prefs:
                    if current_prefs[key] != value:
                        current_prefs[key] = value
                        updated_fields.append(key)
                else:
                    current_prefs[key] = value
                    updated_fields.append(key)
            d["preferences"] = current_prefs
            break
    else:
        raise HTTPException(status_code=404, detail="Device not found")

    _save_devices(devices)
    return {"ok": True, "updated_fields": updated_fields}


@router.get("/notifications/status")
def notification_status(device_token: str = "", since: str = "") -> dict[str, Any]:
    """Check notification delivery status for a device."""
    devices = _load_devices()
    device = next((d for d in devices if d.get("device_token") == device_token), None)

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # In production, query notification delivery logs
    return {
        "device_token": device_token,
        "last_delivery": device.get("last_active_at", ""),
        "notifications_sent_24h": 0,
        "notifications_delivered_24h": 0,
        "delivery_rate": 1.0,
    }


# ── Offline Sync ─────────────────────────────────────────────────────


@router.post("/sync")
def mobile_sync(req: SyncRequest) -> dict[str, Any]:
    """Sync locally queued actions and fetch updates since last sync."""
    processed_actions = []

    # Process queued actions
    for action in req.pending_actions:
        action_type = action.get("type", "")
        target_id = action.get("target_id", "")
        client_id = action.get("client_id", "")

        if action_type == "approve":
            result = _approve_request(target_id)
        elif action_type == "reject":
            result = _reject_request(target_id)
        elif action_type == "resolve_escalation":
            result = _resolve_escalation(target_id)
        else:
            result = {"ok": False, "error": f"Unknown action: {action_type}"}

        result["client_id"] = client_id
        if result.get("ok"):
            result["server_id"] = target_id
        processed_actions.append(result)

    # Compute dashboard delta
    tasks = _load_json(".opencode/inbox.json")
    approvals_data = _load_yaml("orchestrator/approvals.yaml")
    escalations_data = _load_yaml("orchestrator/escalation.yaml")

    now = datetime.now(timezone.utc).isoformat()
    pending_approvals = sum(
        1 for r in approvals_data.get("requests", [])
        if r.get("status") == "pending" and (not r.get("expires_at") or r["expires_at"] > now)
    )
    open_escalations = sum(
        1 for e in escalations_data.get("events", [])
        if not e.get("resolved", False)
    )
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    completed_today = sum(
        1 for t in tasks
        if t.get("status") == "completed"
        and t.get("completed_at", "").startswith(today)
    )

    return {
        "synced_at": now,
        "processed_actions": processed_actions,
        "updates": {
            "new_approvals": pending_approvals,
            "new_escalations": open_escalations,
            "tasks_changed": len(tasks),
        },
        "dashboard_delta": {
            "pending": sum(1 for t in tasks if t.get("status") == "pending"),
            "approvals": pending_approvals,
            "escalations": open_escalations,
            "completed_today": completed_today,
        },
    }


# ── Batch Endpoint ───────────────────────────────────────────────────


@router.post("/batch")
def mobile_batch(req: dict[str, Any]) -> dict[str, Any]:
    """Execute multiple GET requests in a single round trip."""
    requests = req.get("requests", [])[:5]
    results: list[dict[str, Any]] = []
    body: object

    for sub_req in requests:
        path = sub_req.get("path", "")
        # Route to the appropriate handler based on path
        if "/mobile/dashboard" in path:
            body = mobile_dashboard()
            results.append({"status": 200, "body": body.model_dump()})
        elif "/mobile/approvals/stack" in path:
            body = approval_stack()
            results.append({"status": 200, "body": body})
        elif "/mobile/kpis/compact" in path:
            body = compact_kpis()
            results.append({"status": 200, "body": body})
        elif "/mobile/tasks" in path:
            body = mobile_tasks()
            results.append({"status": 200, "body": body})
        else:
            results.append({"status": 404, "body": {"detail": f"Unknown path: {path}"}})

    return {"results": results}
