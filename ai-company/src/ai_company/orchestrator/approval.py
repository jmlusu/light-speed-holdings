"""
Human approval gates for critical actions.
"""

from pathlib import Path
from typing import List, Optional
import yaml
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ApprovalRequest(BaseModel):
    id: str
    task_id: str
    agent_id: str
    action: str
    description: str
    status: ApprovalStatus = ApprovalStatus.PENDING
    requested_at: datetime = Field(default_factory=datetime.now)
    responded_at: Optional[datetime] = None
    response_by: Optional[str] = None
    notes: Optional[str] = None
    expires_at: Optional[datetime] = None


class ApprovalGate:
    def __init__(self, config_path: str = "orchestrator/approvals.yaml"):
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.requests: List[ApprovalRequest] = []
        self._load_config()

    def _load_config(self):
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                self.requests = [ApprovalRequest(**r) for r in data.get("requests", [])]

    def _save_config(self):
        data = {"requests": [r.model_dump() for r in self.requests]}
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False)

    def request_approval(
        self,
        request_id: str,
        task_id: str,
        agent_id: str,
        action: str,
        description: str,
        expires_in_minutes: int = 60,
    ) -> ApprovalRequest:
        from datetime import timedelta

        request = ApprovalRequest(
            id=request_id,
            task_id=task_id,
            agent_id=agent_id,
            action=action,
            description=description,
            expires_at=datetime.now() + timedelta(minutes=expires_in_minutes),
        )
        self.requests.append(request)
        self._save_config()
        return request

    def approve(self, request_id: str, approved_by: str, notes: Optional[str] = None) -> bool:
        request = next((r for r in self.requests if r.id == request_id), None)
        if not request or request.status != ApprovalStatus.PENDING:
            return False

        request.status = ApprovalStatus.APPROVED
        request.responded_at = datetime.now()
        request.response_by = approved_by
        request.notes = notes
        self._save_config()
        return True

    def reject(self, request_id: str, rejected_by: str, notes: Optional[str] = None) -> bool:
        request = next((r for r in self.requests if r.id == request_id), None)
        if not request or request.status != ApprovalStatus.PENDING:
            return False

        request.status = ApprovalStatus.REJECTED
        request.responded_at = datetime.now()
        request.response_by = rejected_by
        request.notes = notes
        self._save_config()
        return True

    def get_pending_requests(self) -> List[ApprovalRequest]:
        now = datetime.now()
        return [
            r
            for r in self.requests
            if r.status == ApprovalStatus.PENDING
            and (not r.expires_at or r.expires_at > now)
        ]

    def get_request(self, request_id: str) -> Optional[ApprovalRequest]:
        return next((r for r in self.requests if r.id == request_id), None)

    def list_all(self) -> List[ApprovalRequest]:
        return self.requests
