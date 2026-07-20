"""Human approval gates for critical actions.

Uses FileStore for atomic persistence of approval requests.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from ai_company.store.file_store import FileStore


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
    tier: int = 2
    required_approvers: int = 1
    approved_by_list: list[str] = Field(default_factory=list)
    status: ApprovalStatus = ApprovalStatus.PENDING
    requested_at: datetime = Field(default_factory=datetime.now)
    responded_at: Optional[datetime] = None
    response_by: Optional[str] = None
    notes: Optional[str] = None
    expires_at: Optional[datetime] = None


class ApprovalGate:
    def __init__(self, config_path: str = "orchestrator/approvals.yaml"):
        self._store = FileStore(
            _path_parent(config_path), backup=True
        )
        self._config_name = _path_name(config_path)
        self.requests: List[ApprovalRequest] = []
        self._load_config()

    def _load_config(self):
        data = self._store.read_yaml(self._config_name)
        if data and isinstance(data, dict):
            self.requests = [ApprovalRequest(**r) for r in data.get("requests", [])]

    def _save_config(self):
        data = {"requests": [r.model_dump() for r in self.requests]}
        self._store.write_yaml(self._config_name, data)

    def request_approval(
        self,
        request_id: str,
        task_id: str,
        agent_id: str,
        action: str,
        description: str,
        expires_in_minutes: int = 60,
        tier: int = 2,
        required_approvers: int = 1,
    ) -> ApprovalRequest:
        request = ApprovalRequest(
            id=request_id,
            task_id=task_id,
            agent_id=agent_id,
            action=action,
            description=description,
            tier=tier,
            required_approvers=required_approvers,
            expires_at=datetime.now() + timedelta(minutes=expires_in_minutes),
        )
        self.requests.append(request)
        self._save_config()
        return request

    def approve(self, request_id: str, approved_by: str, notes: Optional[str] = None) -> bool:
        request = next((r for r in self.requests if r.id == request_id), None)
        if not request or request.status != ApprovalStatus.PENDING:
            return False

        if approved_by not in request.approved_by_list:
            request.approved_by_list.append(approved_by)

        if len(request.approved_by_list) >= request.required_approvers:
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


def _path_parent(config_path: str) -> str:
    """Return the parent directory of a file path."""
    from pathlib import Path
    return str(Path(config_path).parent)


def _path_name(config_path: str) -> str:
    """Return the filename component of a file path."""
    from pathlib import Path
    return Path(config_path).name
