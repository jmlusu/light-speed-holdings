"""Human approval gates for critical actions.

Uses FileStore for atomic persistence of approval requests.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, Field

from ai_company.audit.events import AuditEventType
from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)


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
        self._store = FileStore(_path_parent(config_path), backup=True)
        self._config_name = _path_name(config_path)
        self.requests: List[ApprovalRequest] = []
        self._load_config()

    def _load_config(self):
        data = self._store.read_yaml(self._config_name)
        if data and isinstance(data, dict):
            self.requests = [ApprovalRequest(**r) for r in data.get("requests", [])]

    def _save_config(self):
        data = {"requests": [r.model_dump(mode="json") for r in self.requests]}
        self._store.write_yaml(self._config_name, data)

    def reload(self) -> None:
        """Reload approval requests from disk.

        Call this after external writes (e.g. from another process or the
        dashboard) to ensure the in-memory state reflects the latest YAML.
        """
        self._load_config()

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
        _audit_approval_event(
            AuditEventType.APPROVAL_REQUESTED,
            request,
            expires_at=request.expires_at.isoformat() if request.expires_at else None,
            tier=request.tier,
        )
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
        if request.status == ApprovalStatus.APPROVED:
            _audit_approval_event(
                AuditEventType.APPROVAL_RESOLVED,
                request,
                decision="approved",
                approved_by=approved_by,
            )
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
        _audit_approval_event(
            AuditEventType.APPROVAL_RESOLVED,
            request,
            decision="rejected",
            rejected_by=rejected_by,
        )
        return True

    def expire(self, request_id: str) -> bool:
        """Expire a single pending request whose deadline has passed.

        Mirrors :meth:`approve` / :meth:`reject` in style: no-op (``False``)
        unless the request exists, is still pending, and is actually past its
        ``expires_at`` deadline.
        """
        request = next((r for r in self.requests if r.id == request_id), None)
        if not request or request.status != ApprovalStatus.PENDING:
            return False
        if request.expires_at is None or request.expires_at >= datetime.now():
            return False

        request.status = ApprovalStatus.EXPIRED
        request.responded_at = datetime.now()
        self._save_config()
        _audit_approval_event(
            AuditEventType.APPROVAL_RESOLVED,
            request,
            decision="expired",
        )
        return True

    def sweep_expired(self) -> int:
        """Transition every expired pending request to ``EXPIRED`` (Sprint 7).

        A request qualifies when it is still pending and its ``expires_at``
        is in the past, using the same naive-local comparison convention as
        :meth:`get_pending_requests`.  Returns the number of requests
        transitioned.

        Best-effort: transitions are persisted once; if persistence fails
        the in-memory changes are reverted and the exception is logged so
        the next sweep retries.  Each durable expiry is written to the audit
        trail through the same hook the HITL gate uses (GAP-008).
        """
        now = datetime.now()
        expired = [
            r
            for r in self.requests
            if r.status == ApprovalStatus.PENDING
            and r.expires_at is not None
            and r.expires_at < now
        ]
        if not expired:
            return 0

        originals = {r.id: (r.status, r.responded_at) for r in expired}
        for request in expired:
            request.status = ApprovalStatus.EXPIRED
            request.responded_at = datetime.now()

        try:
            self._save_config()
        except Exception:  # noqa: BLE001 - sweep is best-effort
            logger.exception("Failed to persist approval expiry sweep; will retry next interval")
            for request in expired:
                request.status, request.responded_at = originals[request.id]
            return 0

        for request in expired:
            _audit_approval_expiry(request)
        return len(expired)

    def get_pending_requests(self) -> List[ApprovalRequest]:
        now = datetime.now()
        return [
            r
            for r in self.requests
            if r.status == ApprovalStatus.PENDING and (not r.expires_at or r.expires_at > now)
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


def _audit_approval_expiry(request: ApprovalRequest) -> None:
    """Best-effort audit hook for an approval expiring (GAP-008, G3).

    Logged as ``APPROVAL_RESOLVED`` with ``decision=expired``. The audit
    write is best-effort so a failure can never break the expiry sweep.
    """
    _audit_approval_event(
        AuditEventType.APPROVAL_RESOLVED,
        request,
        decision="expired",
    )


def _audit_approval_event(
    event_type: AuditEventType,
    request: ApprovalRequest,
    **metadata: Any,
) -> None:
    """Best-effort audit hook for approval lifecycle events (G3).

    Writes directly through the global audit writer (imported lazily and
    wrapped in try/except, mirroring :func:`_audit_approval_expiry`) so a
    failure in the audit subsystem can never break the approval flow.
    """
    try:
        from ai_company.audit.events import AuditEvent
        from ai_company.audit.integration import get_writer

        writer = get_writer()
        if writer is None:
            return
        writer.write(
            AuditEvent(
                event_type=event_type,
                task_id=request.task_id,
                agent_id=request.agent_id,
                tool=request.action,
                metadata=metadata,
            )
        )
    except Exception:  # noqa: BLE001 - audit is best-effort
        logger.debug("audit hook skipped for approval event", exc_info=True)
