"""Audit event types and the core AuditEvent Pydantic model."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AuditEventType(str, Enum):
    """Classification of auditable events."""

    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    HITL_APPROVED = "hitl_approved"
    HITL_DENIED = "hitl_denied"
    TASK_CREATED = "task_created"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    ERROR = "error"
    DELEGATION = "delegation"


class AuditEvent(BaseModel):
    """A single immutable audit record for an agent action.

    Events are append-only and designed for JSONL serialization.
    """

    model_config = {"extra": "ignore"}

    event_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique event identifier (UUID).",
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp.",
    )
    event_type: AuditEventType = Field(
        ...,
        description="Classification of this event.",
    )
    agent_id: str = Field(
        ...,
        description="ID of the agent that produced this event.",
    )
    task_id: str = Field(
        default="",
        description="ID of the associated task, if any.",
    )
    tool: str | None = Field(
        default=None,
        description="Tool name when the event relates to a tool invocation.",
    )
    args: dict[str, Any] = Field(
        default_factory=dict,
        description="Arguments passed to the tool or action.",
    )
    result: dict[str, Any] = Field(
        default_factory=dict,
        description="Result payload returned by the tool or action.",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Arbitrary extra context for the event.",
    )
    severity: str = Field(
        default="info",
        description="Severity level (info, warning, error, critical).",
    )
