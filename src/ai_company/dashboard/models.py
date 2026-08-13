"""API response schemas for the CEO dashboard."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class KPIs(BaseModel):
    pending_tasks: int = 0
    in_progress_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    escalated_tasks: int = 0
    pending_approvals: int = 0
    open_escalations: int = 0
    total_agents: int = 0
    scheduled_tasks: int = 0
    uptime_seconds: float = 0


class AgentSummary(BaseModel):
    name: str
    role: str
    type: str
    department: str = ""
    reports_to: str = ""
    direct_reports: list[str] = Field(default_factory=list)
    description: str = ""
    model: Optional[str] = None


class TaskItem(BaseModel):
    id: str
    sender_id: str
    receiver_id: str
    instruction: str
    status: str = "pending"
    priority: str = "medium"
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[str] = None


class TaskAssign(BaseModel):
    receiver_id: str
    instruction: str
    priority: str = "medium"
    sender_id: str = "human-ceo"


class TaskUpdate(BaseModel):
    """Partial update body for PATCH /api/tasks/{task_id}.

    All fields are optional — only supplied fields are applied.
    """

    status: Optional[str] = None
    priority: Optional[str] = None
    instruction: Optional[str] = None
    receiver_id: Optional[str] = None


class ApprovalItem(BaseModel):
    id: str
    task_id: str
    agent_id: str
    action: str
    description: str
    status: str = "pending"
    requested_at: Optional[str] = None
    expires_at: Optional[str] = None


class ApprovalDecision(BaseModel):
    approved_by: str = "human-ceo"
    notes: Optional[str] = None


class EscalationItem(BaseModel):
    task_id: str
    rule_id: str
    from_agent: str
    to_agent: str
    reason: str
    timestamp: Optional[str] = None
    resolved: bool = False


class DepartmentInfo(BaseModel):
    name: str
    executive: str
    agents: list[str] = Field(default_factory=list)
    total_agents: int = 0


class ModelRouteItem(BaseModel):
    agent: str
    provider: str
    model: str
    tier: str
    reason: str = ""


class TierInfo(BaseModel):
    id: str
    description: str
    providers: list[dict[str, str]] = Field(default_factory=list)


class OrgNode(BaseModel):
    name: str
    role: str
    type: str
    department: str = ""
    children: list[OrgNode] = Field(default_factory=list)


class PaginatedTasks(BaseModel):
    """Server-side paginated task response."""

    items: list[TaskItem]
    total: int
    page: int
    page_size: int
    total_pages: int
    counts_by_status: dict[str, int] = Field(default_factory=dict)
