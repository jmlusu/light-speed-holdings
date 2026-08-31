"""API response schemas for the CEO dashboard."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


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
    computed_at: Optional[str] = None
    source: dict[str, str] = Field(default_factory=dict)
    data_quality: dict[str, str] = Field(default_factory=dict)


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
    receiver_id: str = Field(..., min_length=1, max_length=200)
    instruction: str = Field(..., min_length=1, max_length=20000)
    priority: str = "medium"
    sender_id: str = "human-ceo"

    @field_validator("priority")
    @classmethod
    def _validate_priority(cls, value: str) -> str:
        priority = (value or "").lower()
        if priority not in {"low", "medium", "high", "critical"}:
            raise ValueError(
                f"Invalid priority '{value}'. Must be one of: low, medium, high, critical"
            )
        return priority

    @field_validator("receiver_id", "sender_id")
    @classmethod
    def _validate_agent_id(cls, value: str) -> str:
        if any(ch in value for ch in "\r\n\t"):
            raise ValueError("agent id must not contain control characters")
        v = (value or "").strip()
        if not v:
            raise ValueError("agent id must not be empty")
        return v


class TaskUpdate(BaseModel):
    """Partial update body for PATCH /api/tasks/{task_id}.

    All fields are optional — only supplied fields are applied.
    """

    status: Optional[str] = None
    priority: Optional[str] = None
    instruction: Optional[str] = None
    receiver_id: Optional[str] = None

    @field_validator("priority")
    @classmethod
    def _validate_priority(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        priority = value.lower()
        if priority not in {"low", "medium", "high", "critical"}:
            raise ValueError(
                f"Invalid priority '{value}'. Must be one of: low, medium, high, critical"
            )
        return priority

    @field_validator("status")
    @classmethod
    def _validate_status(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        status = value.lower()
        if status not in {
            "pending",
            "in_progress",
            "completed",
            "failed",
            "escalated",
            "cancelled",
        }:
            raise ValueError(
                f"Invalid status '{value}'. Must be one of: "
                "pending, in_progress, completed, failed, escalated, cancelled"
            )
        return status

    @field_validator("receiver_id")
    @classmethod
    def _validate_receiver_id(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        v = (value or "").strip()
        if not v:
            raise ValueError("receiver_id must not be empty")
        if any(ch in v for ch in "\r\n\t"):
            raise ValueError("receiver_id must not contain control characters")
        return v


class ApprovalItem(BaseModel):
    id: str
    task_id: str
    agent_id: str
    action: str
    description: str
    status: str = "pending"
    requested_at: Optional[str] = None
    expires_at: Optional[str] = None
    risk_level: Optional[str] = None
    cost_estimate: Optional[float] = None


class ApprovalDecision(BaseModel):
    approved_by: str = "human-ceo"
    notes: Optional[str] = None

    @field_validator("approved_by")
    @classmethod
    def _validate_approved_by(cls, value: str) -> str:
        v = (value or "").strip()
        if not v:
            raise ValueError("approved_by must not be empty")
        if any(ch in v for ch in "\r\n\t"):
            raise ValueError("approved_by must not contain control characters")
        return v


class ApprovalUpdate(BaseModel):
    """Partial update body for PATCH /api/v1/approvals/{request_id}.

    All fields are optional — only supplied fields are applied.
    """

    risk_level: Optional[str] = None
    cost_estimate: Optional[float] = Field(None, ge=0.0)

    @field_validator("risk_level")
    @classmethod
    def _validate_risk_level(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        risk = (value or "").lower()
        if risk not in {"low", "medium", "high", "critical"}:
            raise ValueError(
                f"Invalid risk_level '{value}'. Must be one of: low, medium, high, critical"
            )
        return risk


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


class ModelTelemetryItem(BaseModel):
    """Per-model telemetry summary for the command center."""

    model_id: str
    request_count: int = 0
    success_rate: float = 0.0
    avg_latency_ms: float = 0.0
    total_cost_usd: float = 0.0


class TierInfo(BaseModel):
    id: str
    description: str
    providers: list[dict[str, str]] = Field(default_factory=list)


class OrgNode(BaseModel):
    name: str
    role: str
    type: str
    department: str = ""
    reports_to: str = ""
    children: list[OrgNode] = Field(default_factory=list)
    metrics: dict[str, Any] | None = None
    risk: dict[str, Any] | None = None


class PaginatedTasks(BaseModel):
    """Server-side paginated task response."""

    items: list[TaskItem]
    total: int
    page: int
    page_size: int
    total_pages: int
    counts_by_status: dict[str, int] = Field(default_factory=dict)


class WorkflowSummary(BaseModel):
    """Workflow definition summary."""

    id: str
    name: str
    trigger: str = ""
    owner: str = ""
    steps: int = 0


class WorkflowStepItem(BaseModel):
    """Single step inside a workflow instance."""

    id: str
    name: str
    action: str = ""
    owner: str = ""
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    status: str = "pending"
    result: str = ""
    sla_hours: int = 0
    sla_minutes: int = 0
    sla_days: int = 0


class WorkflowInstanceItem(BaseModel):
    """Workflow instance status for API responses."""

    instance_id: str
    workflow_id: str
    workflow_name: str
    status: str = "running"
    current_step: Optional[str] = None
    current_step_index: int = 0
    total_steps: int = 0
    completed_steps: int = 0
    steps: list[WorkflowStepItem] = Field(default_factory=list)
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    context: dict[str, Any] = Field(default_factory=dict)


class WorkflowActionRequest(BaseModel):
    """Request body for workflow step actions."""

    result: str = ""
