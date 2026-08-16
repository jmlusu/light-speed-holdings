"""Human approval gates for critical actions.

Uses FileStore for atomic persistence of approval requests.

Store contract (ticket #58) — ``orchestrator/approvals.yaml`` is a *working*
store, not the ledger:

- **Anchoring**: every request has a stable, unique ``id``. The gate refuses
  duplicate or empty ids (no reuse), so ``id`` is always an unambiguous
  anchor for approve/reject/resume lookups.
- **Versioning**: the document carries a top-level ``version`` (currently
  ``SCHEMA_VERSION = 1``). v1 writes UTC-aware timestamps and enforces id
  anchoring; legacy files without ``version`` load with naive timestamps
  treated as UTC. A newer ``version`` is loaded defensively (requests are
  still parsed) with a warning.
- **Retention**: resolved (approved/rejected/expired) requests are archived
  out of the working store after ``retain_days`` via
  :meth:`ApprovalGate.archive_resolved`; pending requests and any request
  referenced by the executor's live resume index are never archived.
- **Durable ledger**: the append-only audit trail (``.opencode/audit``,
  ticket #59) is the ledger of record. Every request and every decision is
  audited through :func:`_audit_approval_event`; archival emits
  ``RETENTION_APPLIED`` so the ledger records when a record left the working
  store. All decision paths (CLI, daemon sweep, dashboard, mobile) must go
  through this class so none of them can write a lossy record.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, Field, field_validator

from ai_company.audit.events import AuditEventType
from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)

# Current schema version of the approvals store. v1 = anchored unique request
# ids + UTC-aware timestamps. Files without a ``version`` key are legacy and
# still load (naive timestamps are treated as UTC for comparison).
SCHEMA_VERSION = 1


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ApprovalRequest(BaseModel):
    id: str
    task_id: str = ""
    agent_id: str
    action: str
    description: str
    tier: int = 2
    required_approvers: int = 1
    approved_by_list: list[str] = Field(default_factory=list)
    status: ApprovalStatus = ApprovalStatus.PENDING
    requested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    responded_at: Optional[datetime] = None
    response_by: Optional[str] = None
    notes: Optional[str] = None
    expires_at: Optional[datetime] = None
    # GAP-016 / ticket #70: True when the pending tool call (e.g. a bash
    # command) contains shell metacharacters that the executor will always
    # reject — the request carries a warning and the resume path must NOT
    # silently retry it. Default False keeps legacy records loadable.
    metacharacter_blocked: bool = False

    @classmethod
    def _normalize_dt(cls, v: Any) -> Any:
        """Convert naive datetime to UTC-aware (ticket #55/#58 convention).

        Handles both datetime objects and ISO format strings (which pydantic
        passes to the validator before parsing when mode="before").
        """
        if v is None:
            return None
        if isinstance(v, str):
            # Parse ISO string; if it has no timezone, pydantic will parse as naive
            # but we want to treat it as UTC. We can't easily re-parse here,
            # so we let pydantic parse it and then fix in a second pass.
            # Actually, mode="before" receives the raw input before parsing.
            # Return the string as-is and let pydantic parse, then we'll
            # handle in a second validator with mode="after".
            return v
        if isinstance(v, datetime):
            if v.tzinfo is None:
                return v.replace(tzinfo=timezone.utc)
            return v
        return v

    @field_validator("requested_at", "responded_at", "expires_at", mode="after")
    @classmethod
    def _ensure_utc(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Ensure datetime fields are UTC-aware after parsing."""
        if v is None:
            return None
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)


class ApprovalGate:
    def __init__(
        self,
        config_path: str = "orchestrator/approvals.yaml",
        retain_days: int = 30,
    ):
        self._store = FileStore(_path_parent(config_path), backup=True)
        self._config_name = _path_name(config_path)
        self.retain_days = retain_days
        self.requests: List[ApprovalRequest] = []
        self._load_config()

    @property
    def schema_version(self) -> int:
        """Return the schema version the store is written as (ticket #58)."""
        return SCHEMA_VERSION

    def _load_config(self):
        # Load is idempotent: a reload must replace the in-memory state with
        # what is on disk, never append to it (otherwise every reload
        # duplicates every request persisted in the YAML).
        self.requests = []
        data = self._store.read_yaml(self._config_name)
        if data and isinstance(data, dict):
            stored_version = data.get("version", 0)
            if stored_version > SCHEMA_VERSION:
                logger.warning(
                    "Approvals store %s reports schema version %s, newer than "
                    "supported %s — loading defensively.",
                    self._config_name,
                    stored_version,
                    SCHEMA_VERSION,
                )
            for record in data.get("requests", []):
                try:
                    self.requests.append(ApprovalRequest(**record))
                except Exception:  # noqa: BLE001 - one bad record must not sink the store
                    logger.warning(
                        "Skipping invalid approval record in %s: %s",
                        self._config_name,
                        record.get("id", "<no id>"),
                        exc_info=True,
                    )

    def _save_config(self):
        data = {
            "version": SCHEMA_VERSION,
            "requests": [r.model_dump(mode="json") for r in self.requests],
        }
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
        metacharacter_blocked: bool = False,
    ) -> ApprovalRequest:
        if not request_id or not request_id.strip():
            raise ValueError("Approval request id must be a non-empty string")
        if any(r.id == request_id for r in self.requests):
            # Anchoring (ticket #58): ids are the stable anchor for
            # approve/reject/resume lookups, so reuse is refused instead of
            # silently resolving the wrong record.
            raise ValueError(f"Approval request id '{request_id}' already exists")
        request = ApprovalRequest(
            id=request_id,
            task_id=task_id,
            agent_id=agent_id,
            action=action,
            description=description,
            tier=tier,
            required_approvers=required_approvers,
            expires_at=_now_utc() + timedelta(minutes=expires_in_minutes),
            metacharacter_blocked=metacharacter_blocked,
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
            request.responded_at = _now_utc()
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
        request.responded_at = _now_utc()
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
        if request.expires_at is None:
            return False
        expires_utc = _to_utc(request.expires_at)
        assert expires_utc is not None
        if expires_utc >= _now_utc():
            return False

        request.status = ApprovalStatus.EXPIRED
        request.responded_at = _now_utc()
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
        is in the past, compared in UTC (legacy naive timestamps are treated
        as UTC, the ticket #55 convention).  Returns the number of requests
        transitioned.

        Best-effort: transitions are persisted once; if persistence fails
        the in-memory changes are reverted and the exception is logged so
        the next sweep retries.  Each durable expiry is written to the audit
        trail through the same hook the HITL gate uses (GAP-008).
        """
        now = _now_utc()
        expired = []
        for r in self.requests:
            if r.status != ApprovalStatus.PENDING or r.expires_at is None:
                continue
            expires_utc = _to_utc(r.expires_at)
            assert expires_utc is not None
            if expires_utc < now:
                expired.append(r)
        if not expired:
            return 0

        originals = {r.id: (r.status, r.responded_at) for r in expired}
        for request in expired:
            request.status = ApprovalStatus.EXPIRED
            request.responded_at = now

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
        now = _now_utc()
        pending = []
        for r in self.requests:
            if r.status != ApprovalStatus.PENDING:
                continue
            if r.expires_at is None:
                pending.append(r)
                continue
            expires_utc = _to_utc(r.expires_at)
            assert expires_utc is not None
            if expires_utc > now:
                pending.append(r)
        return pending

    def get_request(self, request_id: str) -> Optional[ApprovalRequest]:
        return next((r for r in self.requests if r.id == request_id), None)

    def get_latest_request_for_task(self, task_id: str) -> Optional[ApprovalRequest]:
        """Return the most recently created approval request for *task_id*.

        A task is normally parked on a single request at a time, but a
        request can be re-created (e.g. after a failed fast-approve), so
        ordering by ``requested_at`` keeps the latest decision
        authoritative. This is the by-task lookup used to resume a parked
        task whose ``task_id -> request_id`` resume index
        (``pending_approvals.json``) was lost (ticket #57).
        """
        matches = [r for r in self.requests if r.task_id == task_id]
        if not matches:
            return None

        def _req_sort_key(r: ApprovalRequest) -> datetime:
            utc = _to_utc(r.requested_at)
            assert utc is not None
            return utc

        return max(matches, key=_req_sort_key)

    def list_all(self) -> List[ApprovalRequest]:
        return self.requests

    def archive_resolved(
        self,
        protected_request_ids: Optional[set[str]] = None,
        retain_days: Optional[int] = None,
    ) -> int:
        """Archive resolved requests older than the retention window.

        The approvals store is a *working* store, not the ledger (ticket #58):
        resolved (approved/rejected/expired) requests are dropped from the
        YAML after ``retain_days`` so the file stays bounded, while the
        append-only audit trail keeps the full history. Requests that are
        still pending, or whose id is in *protected_request_ids* (the
        executor's live resume index), are never archived — a parked task
        must never lose the request that decides its resume.

        Returns the number of requests archived. Best-effort like
        :meth:`sweep_expired`: if persistence fails, the in-memory requests
        are restored and the exception logged so the next run retries.
        """
        protected = protected_request_ids or set()
        window = retain_days if retain_days is not None else self.retain_days
        if window <= 0:
            return 0
        cutoff = _now_utc() - timedelta(days=window)
        terminal = {ApprovalStatus.APPROVED, ApprovalStatus.REJECTED, ApprovalStatus.EXPIRED}
        candidates = []
        for r in self.requests:
            if r.status not in terminal or r.responded_at is None or r.id in protected:
                continue
            responded_utc = _to_utc(r.responded_at)
            assert responded_utc is not None
            if responded_utc < cutoff:
                candidates.append(r)
        if not candidates:
            return 0

        removed_ids = {r.id for r in candidates}
        self.requests = [r for r in self.requests if r.id not in removed_ids]
        try:
            self._save_config()
        except Exception:  # noqa: BLE001 - archival is best-effort
            logger.exception("Failed to persist approval archival; will retry next interval")
            self.requests = []
            self._load_config()
            return 0

        for request in candidates:
            _audit_approval_event(
                AuditEventType.RETENTION_APPLIED,
                request,
                reason="approval_retention_archive",
                retained_days=window,
            )
        return len(candidates)


def _path_parent(config_path: str) -> str:
    """Return the parent directory of a file path."""
    from pathlib import Path

    return str(Path(config_path).parent)


def _path_name(config_path: str) -> str:
    """Return the filename component of a file path."""
    from pathlib import Path

    return Path(config_path).name


def _now_utc() -> datetime:
    """UTC-aware 'now' used for all approval timestamps (ticket #58)."""
    return datetime.now(timezone.utc)


def _to_utc(value: Optional[datetime]) -> Optional[datetime]:
    """Normalise a timestamp to UTC; legacy naive values are treated as UTC.

    Follows the convention established in ticket #55: naive datetimes in
    stored records predate the UTC convention and are interpreted as UTC so
    comparisons never mix zones (and never raise).
    """
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


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
