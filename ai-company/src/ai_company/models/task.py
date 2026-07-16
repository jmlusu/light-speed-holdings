"""
Task model for the AI Company Builder.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ESCALATED = "escalated"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Task(BaseModel):
    id: str
    sender_id: str
    receiver_id: str
    instruction: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[str] = None
    requires_approval: bool = False
    approved_by: Optional[str] = None
