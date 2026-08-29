"""Unified agent onboarding service with full lifecycle management.

Merges the best of HR and Services onboarding implementations:
- Full 7-state lifecycle: requested → config_review → security_review → generating → testing → approval → active
- Terminal states: rejected, failed, archived
- Registry integration with validation, backup, and rollback
- HITL integration via ApprovalGate
- BaseService pattern with audit trail and event recording
- WebSocket broadcasting for real-time updates
- FileStore-backed persistence

Design decisions from grilling session:
- Canonical module: This file replaces both hr/onboarding.py and services/onboarding.py
- State machine: 7-state flow with optional security review for low-risk agents
- Security review: Optional for tier 1 tools only
- Error handling: Rollback + alert on failure
"""

from __future__ import annotations

import logging
import shutil
import uuid
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, cast

from pydantic import BaseModel, Field

from ai_company.audit.events import AuditEventType
from ai_company.models.task import TaskPriority
from ai_company.services.base import BaseService, ServiceResult
from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------


class OnboardingState(str, Enum):
    """Lifecycle states for an agent onboarding request.

    Maps to SOP-HR-001 steps:
      requested (step 1) → config_review (step 2) → security_review (step 3)
      → generating (step 4) → testing (step 5) → approval (step 6)
      → active (step 7)
    """

    REQUESTED = "requested"
    CONFIG_REVIEW = "config_review"
    SECURITY_REVIEW = "security_review"
    GENERATING = "generating"
    TESTING = "testing"
    APPROVAL = "approval"
    ACTIVE = "active"
    # Terminal states
    REJECTED = "rejected"
    FAILED = "failed"
    ARCHIVED = "archived"


# Valid forward transitions. Terminal states have no outgoing edges.
_TRANSITIONS: dict[OnboardingState, frozenset[OnboardingState]] = {
    OnboardingState.REQUESTED: frozenset(
        {
            OnboardingState.CONFIG_REVIEW,
            OnboardingState.REJECTED,
        }
    ),
    OnboardingState.CONFIG_REVIEW: frozenset(
        {
            OnboardingState.SECURITY_REVIEW,
            OnboardingState.REJECTED,
        }
    ),
    OnboardingState.SECURITY_REVIEW: frozenset(
        {
            OnboardingState.GENERATING,
            OnboardingState.REJECTED,
        }
    ),
    OnboardingState.GENERATING: frozenset(
        {
            OnboardingState.TESTING,
            OnboardingState.FAILED,
            OnboardingState.REJECTED,
        }
    ),
    OnboardingState.TESTING: frozenset(
        {
            OnboardingState.APPROVAL,
            OnboardingState.FAILED,
            OnboardingState.REJECTED,
        }
    ),
    OnboardingState.APPROVAL: frozenset(
        {
            OnboardingState.ACTIVE,
            OnboardingState.REJECTED,
        }
    ),
    OnboardingState.ACTIVE: frozenset({OnboardingState.ARCHIVED}),
    OnboardingState.REJECTED: frozenset(),
    OnboardingState.FAILED: frozenset({OnboardingState.GENERATING}),
    OnboardingState.ARCHIVED: frozenset(),
}

# Human-readable labels for CLI display.
STATE_LABELS: dict[OnboardingState, str] = {
    OnboardingState.REQUESTED: "Staffing request submitted",
    OnboardingState.CONFIG_REVIEW: "Agent configuration under review",
    OnboardingState.SECURITY_REVIEW: "Security review (CTO sign-off)",
    OnboardingState.GENERATING: "Generating agent files",
    OnboardingState.TESTING: "Running validation tests",
    OnboardingState.APPROVAL: "Awaiting human approval",
    OnboardingState.ACTIVE: "Agent deployed and active",
    OnboardingState.REJECTED: "Request rejected",
    OnboardingState.FAILED: "Generation/testing failed",
    OnboardingState.ARCHIVED: "Agent archived",
}


def valid_transitions(state: OnboardingState) -> frozenset[OnboardingState]:
    """Return the set of states reachable from *state*."""
    return _TRANSITIONS[state]


def can_transition(current: OnboardingState, target: OnboardingState) -> bool:
    """Check whether a transition from *current* to *target* is valid."""
    return target in _TRANSITIONS[current]


def is_terminal(state: OnboardingState) -> bool:
    """Return True if *state* has no outgoing transitions."""
    return not bool(_TRANSITIONS[state])


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class OnboardingRequest(BaseModel):
    """An agent onboarding request tracked through the HITL gate."""

    id: str = ""
    agent_id: str = ""
    name: str = ""
    role: str = ""
    department: str = ""
    agent_type: str = "specialist"
    reports_to: str = ""
    responsibilities: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    guidelines: str = ""
    state: OnboardingState = OnboardingState.REQUESTED
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    security_reviewer: str = ""
    security_reviewed_at: datetime | None = None
    approval_request_id: str = ""
    hitl_tier: int = 2
    error: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **data: Any) -> None:
        if not data.get("id"):
            data["id"] = f"onb-{uuid.uuid4().hex[:12]}"
        super().__init__(**data)

    def transition_to(self, target: OnboardingState) -> None:
        """Execute a state transition, raising ValueError if invalid."""
        if not can_transition(self.state, target):
            raise ValueError(
                f"Invalid transition: {self.state.value} → {target.value}. "
                f"Allowed: {sorted(t.value for t in valid_transitions(self.state))}"
            )
        self.state = target
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a YAML-friendly dict."""
        return self.model_dump(mode="json")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OnboardingRequest:
        """Deserialize from a YAML-loaded dict."""
        return cls(**data)


# ---------------------------------------------------------------------------
# Registry helpers
# ---------------------------------------------------------------------------


def _request_to_registry_entry(req: OnboardingRequest) -> dict[str, Any]:
    """Convert an OnboardingRequest to a company-registry.yaml agent entry."""
    entry: dict[str, Any] = {
        "id": req.agent_id,
        "name": req.name,
        "title": req.role,
        "description": req.role,
        "type": req.agent_type,
        "department": req.department,
        "reports_to": req.reports_to,
        "responsibilities": req.responsibilities,
        "guidelines": req.guidelines,
        "tools": req.tools,
    }
    return entry


# ---------------------------------------------------------------------------
# WebSocket broadcast helper
# ---------------------------------------------------------------------------


def _broadcast_onboarding_event(request_id: str, event: str, payload: dict[str, Any]) -> None:
    """Fire-and-forget WS broadcast for onboarding lifecycle events.

    Schedules the async broadcast on the running event loop. Gracefully
    skips when no event loop is available (CLI usage, tests).
    """
    try:
        import asyncio

        from ai_company.dashboard.ws import broadcast_onboarding_update

        loop = asyncio.get_running_loop()
        loop.create_task(broadcast_onboarding_update(request_id, event, payload))
    except (RuntimeError, ImportError):
        logger.debug("No event loop or ws module; onboarding broadcast skipped")


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------


class OnboardingService(BaseService):
    """Unified service layer for HITL-gated agent onboarding.

    Bridges the onboarding flow to the ApprovalGate so that onboarding
    requests appear in the dashboard Approvals tab with WS alerts.
    """

    # Tier 2 = standard approval; tier 3 for agents with sensitive tools
    SENSITIVE_TOOLS = frozenset({"bash", "edit", "delete"})

    def __init__(
        self,
        registry_path: str = "company-registry.yaml",
        templates_dir: str = "templates",
        output_dir: str = ".opencode/agents",
        data_dir: str | Path = ".",
        **kwargs: Any,
    ) -> None:
        self._registry_path = Path(registry_path)
        self._templates_dir = Path(templates_dir)
        self._output_dir = Path(output_dir)
        super().__init__(department_id="hr", data_dir=data_dir, **kwargs)
        self._onboarding_store = FileStore(Path(data_dir) / "hr", backup=True)

    # ── Persistence ────────────────────────────────────────────────────

    def _load_requests(self) -> dict[str, Any]:
        data = self._onboarding_store.read_yaml("onboarding_requests.yaml")
        if data is None:
            return {"requests": []}
        return cast(dict[str, Any], data)

    def _save_requests(self, data: dict[str, Any]) -> None:
        self._onboarding_store.write_yaml("onboarding_requests.yaml", data)

    def _get_request(self, request_id: str) -> OnboardingRequest | None:
        data = self._load_requests()
        for r in data.get("requests", []):
            if r.get("id") == request_id:
                return OnboardingRequest(**r)
        return None

    def _save_request(self, req: OnboardingRequest) -> None:
        data = self._load_requests()
        requests = data.get("requests", [])
        for i, r in enumerate(requests):
            if r.get("id") == req.id:
                requests[i] = req.to_dict()
                break
        else:
            requests.append(req.to_dict())
        data["requests"] = requests
        self._save_requests(data)

    # ── Registry helpers ───────────────────────────────────────────────

    def _load_registry_yaml(self) -> dict[str, Any]:
        """Load the raw company-registry.yaml."""
        if not self._registry_path.exists():
            raise FileNotFoundError(f"Registry not found: {self._registry_path}")
        import yaml

        with open(self._registry_path, encoding="utf-8") as f:
            data: dict[str, Any] = yaml.safe_load(f)
        if data is None:
            return {"company": {"name": "AI Company", "agents": []}}
        return data

    def _save_registry_yaml(self, data: dict[str, Any]) -> None:
        """Persist the raw company-registry.yaml."""
        import yaml

        with open(self._registry_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    def _backup_registry(self) -> Path:
        """Create a timestamped backup of company-registry.yaml for rollback."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup_path = self._registry_path.with_suffix(f".yaml.bak.{timestamp}")
        shutil.copy2(self._registry_path, backup_path)
        return backup_path

    def _get_existing_ids(self, data: dict[str, Any]) -> set[str]:
        """Extract all agent IDs from the registry."""
        agents = data.get("company", {}).get("agents", [])
        return {a.get("id", "") for a in agents if isinstance(a, dict)}

    # ── Validation ─────────────────────────────────────────────────────

    def validate_draft(self, req: OnboardingRequest) -> list[str]:
        """Validate an onboarding request against the current registry.

        Returns a list of error strings. Empty list means valid.
        Checks:
        - Agent ID is not already taken
        - Required fields are present
        - reports_to references a valid agent (if specified)
        """
        errors: list[str] = []

        if not req.agent_id:
            errors.append("agent_id is required")
        if not req.name:
            errors.append("name is required")
        if not req.department:
            errors.append("department is required")

        try:
            data = self._load_registry_yaml()
            existing_ids = self._get_existing_ids(data)

            if req.agent_id in existing_ids:
                errors.append(f"Agent ID '{req.agent_id}' already exists in the registry")

            if req.reports_to:
                agents = data.get("company", {}).get("agents", [])
                known_ids = {a.get("id", "") for a in agents if isinstance(a, dict)}
                known_names = {
                    a.get("name", "").lower(): a.get("id", "")
                    for a in agents
                    if isinstance(a, dict)
                }
                if req.reports_to not in known_ids and req.reports_to.lower() not in known_names:
                    errors.append(
                        f"reports_to '{req.reports_to}' does not match any agent ID or name"
                    )

            if req.agent_type not in ("executive", "specialist", "board", "default"):
                errors.append(f"Invalid agent_type: '{req.agent_type}'")
        except FileNotFoundError:
            errors.append("Registry file not found")

        return errors

    # ── Registry integration ───────────────────────────────────────────

    def add_to_registry(self, req: OnboardingRequest) -> ServiceResult[dict[str, Any]]:
        """Add the onboarding request as a new agent entry in company-registry.yaml.

        Validates first, then appends. Returns ServiceResult with success status.
        Does NOT generate agent files — call generate() separately.
        """
        errors = self.validate_draft(req)
        if errors:
            for err in errors:
                logger.error("Validation failed: %s", err)
            return ServiceResult.fail(*errors, request_id=req.id)

        try:
            data = self._load_registry_yaml()
            entry = _request_to_registry_entry(req)

            agents = data.setdefault("company", {}).setdefault("agents", [])
            agents.append(entry)

            self._save_registry_yaml(data)
            logger.info("Added agent '%s' to registry", req.agent_id)
            return ServiceResult.ok(
                {"agent_id": req.agent_id, "registry_entry": entry},
                request_id=req.id,
            )
        except OSError as exc:
            return ServiceResult.fail(
                f"Failed to add to registry: {exc}",
                request_id=req.id,
            )

    def generate(self, req: OnboardingRequest) -> ServiceResult[list[str]]:
        """Run the full agent generation pipeline.

        1. Backs up company-registry.yaml.
        2. Ensures the agent entry is in the registry (adds if missing).
        3. Calls AgentGenerator().generate_all() for full regeneration.
        4. Syncs company/agent-registry.json.
        5. On failure: rolls back registry and raises.

        Returns ServiceResult with list of generated file paths.
        """
        from ai_company.generator import AgentGenerator
        from ai_company.registry.sync import sync_registry

        backup_path = self._backup_registry()
        logger.info("Registry backed up to %s", backup_path)

        try:
            data = self._load_registry_yaml()
            existing_ids = self._get_existing_ids(data)

            if req.agent_id not in existing_ids:
                add_result = self.add_to_registry(req)
                if not add_result.success:
                    raise RuntimeError(f"Failed to add agent '{req.agent_id}' to registry")

            gen = AgentGenerator(
                registry_path=str(self._registry_path),
                templates_dir=str(self._templates_dir),
                output_dir=str(self._output_dir),
            )
            generated = gen.generate_all()
            logger.info("Generated %d agent files", len(generated))

            sync_registry(yaml_path=str(self._registry_path))
            logger.info("Synced registry to JSON")

            generated_paths = [str(p) for p in generated]
            return ServiceResult.ok(generated_paths, request_id=req.id)

        except (OSError, RuntimeError) as exc:
            logger.error("Generation failed — rolling back registry to %s", backup_path)
            shutil.copy2(backup_path, self._registry_path)
            return ServiceResult.fail(
                f"Generation failed: {exc}",
                request_id=req.id,
            )

    # ── Approval tier determination ────────────────────────────────────

    def _compute_tier(self, tools: list[str]) -> int:
        """Determine the approval tier based on requested tools.

        Tier 2 = standard (default).
        Tier 3 = two-person rule (if agent requests sensitive tools).
        """
        if any(t in self.SENSITIVE_TOOLS for t in tools):
            return 3
        return 2

    # ── HITL integration ──────────────────────────────────────────────

    def _create_hitl_approval(self, req: OnboardingRequest) -> None:
        """Create an ApprovalGate request for the APPROVAL step (HITL integration)."""
        from ai_company.orchestrator.approval import ApprovalGate

        gate = ApprovalGate.get_instance()

        # Determine tier based on tools (sensitive tools = tier 3)
        tier = self._compute_tier(req.tools)
        req.hitl_tier = tier

        description = (
            f"Agent onboarding approval: {req.agent_id} as {req.role} in {req.department}\n"
            f"Type: {req.agent_type}\n"
            f"Reports to: {req.reports_to or 'none'}\n"
            f"Tools: {', '.join(req.tools) if req.tools else 'none specified'}\n"
            f"Tier: {tier}"
        )

        try:
            approval = gate.request_approval(
                request_id=req.id,
                task_id="",
                agent_id="hr",
                action="agent_onboarding",
                description=description,
                expires_in_minutes=2880,  # 48 hours
                tier=tier,
            )
            req.approval_request_id = approval.id
            logger.info("Created HITL approval request %s for onboarding %s", approval.id, req.id)
        except ValueError as exc:
            logger.error("Failed to create HITL approval for %s: %s", req.id, exc)
            req.error = f"HITL approval creation failed: {exc}"

    def check_approval_status(self, req: OnboardingRequest) -> str | None:
        """Check the HITL approval status for a request in APPROVAL state.

        Returns:
            'approved' if approved, 'rejected' if rejected, 'expired' if expired,
            'pending' if still pending, None if not in APPROVAL state or no approval request.
        """
        if req.state != OnboardingState.APPROVAL or not req.approval_request_id:
            return None

        from ai_company.orchestrator.approval import ApprovalGate, ApprovalStatus

        gate = ApprovalGate.get_instance()
        gate.reload()  # Reload from disk to get latest status
        approval = gate.get_request(req.approval_request_id)

        if approval is None:
            return "pending"

        if approval.status == ApprovalStatus.APPROVED:
            return "approved"
        elif approval.status == ApprovalStatus.REJECTED:
            return "rejected"
        elif approval.status == ApprovalStatus.EXPIRED:
            return "expired"
        else:
            return "pending"

    def resolve_approval(self, req: OnboardingRequest) -> OnboardingRequest:
        """Resolve the HITL approval and transition to ACTIVE or REJECTED.

        Should be called after check_approval_status returns 'approved' or 'rejected'.
        """
        if req.state != OnboardingState.APPROVAL:
            raise ValueError(f"resolve_approval requires state APPROVAL, got '{req.state.value}'")

        status = self.check_approval_status(req)
        if status == "approved":
            req.transition_to(OnboardingState.ACTIVE)
            logger.info("Agent '%s' activated via HITL approval", req.agent_id)
        elif status in ("rejected", "expired"):
            req.transition_to(OnboardingState.REJECTED)
            req.error = f"HITL approval {status}"
            logger.info("Request %s rejected via HITL: %s", req.id, status)
        else:
            raise ValueError(f"Cannot resolve approval: status is '{status}'")

        self._save_request(req)
        return req

    # ── Public API ─────────────────────────────────────────────────────

    def request_onboarding(
        self,
        agent_id: str,
        role: str,
        department: str,
        name: str = "",
        tools: list[str] | None = None,
        responsibilities: list[str] | None = None,
        reports_to: str = "",
        guidelines: str = "",
        expires_in_hours: int = 48,
    ) -> ServiceResult[dict[str, Any]]:
        """Submit a new agent onboarding request through the HITL gate.

        Creates an ApprovalRequest in approvals.yaml (visible in dashboard
        Approvals tab) and an OnboardingRequest to track the full lifecycle.

        Args:
            agent_id: The new agent's unique identifier.
            role: Agent role (e.g. 'backend-engineer').
            department: Department the agent belongs to.
            name: Human-readable agent name (defaults to agent_id with underscores replaced).
            tools: List of tool permissions the agent needs.
            responsibilities: List of responsibilities.
            reports_to: Parent agent ID or name.
            guidelines: Free-text guidelines.
            expires_in_hours: Approval window (default 48h).
        """
        tools = tools or []
        responsibilities = responsibilities or []
        name = name or agent_id.replace("_", " ").title()

        # Check for duplicate active request
        existing = self._find_active_by_agent(agent_id)
        if existing is not None:
            return ServiceResult.fail(
                f"Agent '{agent_id}' already has an active onboarding request ({existing.id})",
                agent_id=agent_id,
            )

        # Create the onboarding request
        req = OnboardingRequest(
            agent_id=agent_id,
            name=name,
            role=role,
            department=department,
            tools=tools,
            responsibilities=responsibilities,
            reports_to=reports_to,
            guidelines=guidelines,
        )

        # Create the HITL approval request via ApprovalGate
        from ai_company.orchestrator.approval import ApprovalGate

        gate = ApprovalGate.get_instance()
        tier = self._compute_tier(tools)
        req.hitl_tier = tier

        description = (
            f"Agent onboarding: {agent_id} as {role} in {department}\n"
            f"Tools: {', '.join(tools) if tools else 'none specified'}\n"
            f"Tier: {tier}"
        )
        expires_minutes = expires_in_hours * 60

        try:
            approval = gate.request_approval(
                request_id=req.id,
                task_id="",
                agent_id="hr",
                action="agent_onboarding",
                description=description,
                expires_in_minutes=expires_minutes,
                tier=tier,
            )
            req.approval_request_id = approval.id
        except ValueError as exc:
            return ServiceResult.fail(str(exc), request_id=req.id)

        self._save_request(req)

        # Audit trail
        self._audit_log(
            action="request_onboarding",
            event_type=AuditEventType.APPROVAL_REQUESTED,
            entity_id=req.id,
            result={
                "agent_id": agent_id,
                "role": role,
                "department": department,
                "tools": tools,
                "tier": tier,
                "expires_in_hours": expires_in_hours,
            },
        )

        self.record_event(
            f"Onboarding request submitted for agent '{agent_id}' as {role} in {department}",
            tags=["onboarding", "requested", agent_id],
            request_id=req.id,
            tier=tier,
        )

        # WS broadcast
        _broadcast_onboarding_event(
            req.id,
            "requested",
            {
                "agent_id": agent_id,
                "role": role,
                "department": department,
                "tier": tier,
            },
        )

        # Create a task for the executor to process this onboarding request
        self.create_task(
            receiver_id="chief_of_staff",
            instruction=f"Onboarding request for agent '{agent_id}' as {role} in {department}. "
            f"Tier: {tier}. Please review and process.",
            priority=TaskPriority.HIGH if tier >= 3 else TaskPriority.MEDIUM,
            sender_id="hr-service",
        )

        return ServiceResult.ok(
            {
                "request_id": req.id,
                "approval_request_id": req.approval_request_id,
                "agent_id": agent_id,
                "name": name,
                "role": role,
                "department": department,
                "tier": tier,
                "state": req.state.value,
            },
            request_id=req.id,
        )

    def approve_onboarding(
        self,
        request_id: str,
        approved_by: str,
        notes: str = "",
    ) -> ServiceResult[dict[str, Any]]:
        """Approve an onboarding request via the HITL gate.

        Transitions the onboarding state from pending_approval to generating.
        """
        req = self._get_request(request_id)
        if req is None:
            return ServiceResult.fail(f"Onboarding request '{request_id}' not found")

        if req.state != OnboardingState.APPROVAL:
            return ServiceResult.fail(
                f"Request '{request_id}' is in state '{req.state.value}', expected 'approval'"
            )

        # Approve through ApprovalGate
        from ai_company.orchestrator.approval import ApprovalGate

        gate = ApprovalGate.get_instance()
        ok = gate.approve(request_id, approved_by, notes=notes)
        if not ok:
            return ServiceResult.fail(
                f"Approval failed for '{request_id}' — request not found or not pending"
            )

        # Transition state
        req.transition_to(OnboardingState.ACTIVE)
        self._save_request(req)

        self._audit_log(
            action="approve_onboarding",
            event_type=AuditEventType.APPROVAL_RESOLVED,
            entity_id=request_id,
            result={"decision": "approved", "approved_by": approved_by},
        )

        self.record_event(
            f"Onboarding request '{request_id}' approved by {approved_by}",
            tags=["onboarding", "approved", req.agent_id],
            approved_by=approved_by,
        )

        # WS broadcast
        _broadcast_onboarding_event(
            request_id,
            "approved",
            {
                "agent_id": req.agent_id,
                "state": req.state.value,
                "approved_by": approved_by,
            },
        )

        # Create a task for the agent to be activated
        self.create_task(
            receiver_id=req.agent_id,
            instruction=f"Onboarding approved. Agent '{req.agent_id}' is now active. "
            f"Please complete any final setup steps.",
            priority=TaskPriority.HIGH,
            sender_id="hr-service",
        )

        return ServiceResult.ok(
            {
                "request_id": request_id,
                "agent_id": req.agent_id,
                "state": req.state.value,
                "approved_by": approved_by,
            },
            request_id=request_id,
        )

    def reject_onboarding(
        self,
        request_id: str,
        rejected_by: str,
        reason: str = "",
    ) -> ServiceResult[dict[str, Any]]:
        """Reject an onboarding request via the HITL gate.

        Transitions the onboarding state to rejected with the rejection reason.
        """
        req = self._get_request(request_id)
        if req is None:
            return ServiceResult.fail(f"Onboarding request '{request_id}' not found")

        if req.state not in (OnboardingState.REQUESTED, OnboardingState.APPROVAL):
            return ServiceResult.fail(
                f"Request '{request_id}' is in state '{req.state.value}', expected 'requested' or 'approval'"
            )

        # Reject through ApprovalGate
        from ai_company.orchestrator.approval import ApprovalGate

        gate = ApprovalGate.get_instance()
        ok = gate.reject(request_id, rejected_by, notes=reason)
        if not ok:
            return ServiceResult.fail(
                f"Rejection failed for '{request_id}' — request not found or not pending"
            )

        # Transition state
        req.transition_to(OnboardingState.REJECTED)
        req.error = reason
        self._save_request(req)

        self._audit_log(
            action="reject_onboarding",
            event_type=AuditEventType.APPROVAL_RESOLVED,
            entity_id=request_id,
            result={"decision": "rejected", "rejected_by": rejected_by, "reason": reason},
        )

        self.record_event(
            f"Onboarding request '{request_id}' rejected by {rejected_by}: {reason}",
            tags=["onboarding", "rejected", req.agent_id],
            rejected_by=rejected_by,
        )

        # WS broadcast
        _broadcast_onboarding_event(
            request_id,
            "rejected",
            {
                "agent_id": req.agent_id,
                "state": req.state.value,
                "rejected_by": rejected_by,
                "reason": reason,
            },
        )

        return ServiceResult.ok(
            {
                "request_id": request_id,
                "agent_id": req.agent_id,
                "state": req.state.value,
                "rejection_reason": reason,
            },
            request_id=request_id,
        )

    def advance_to_next(self, request_id: str) -> ServiceResult[dict[str, Any]]:
        """Advance an onboarding request to its next logical state.

        The 'next state' is determined by the happy-path order:
        requested → config_review → security_review → generating → testing → approval → active
        """
        req = self._get_request(request_id)
        if req is None:
            return ServiceResult.fail(f"Onboarding request '{request_id}' not found")

        happy_path = [
            OnboardingState.CONFIG_REVIEW,
            OnboardingState.SECURITY_REVIEW,
            OnboardingState.GENERATING,
            OnboardingState.TESTING,
            OnboardingState.APPROVAL,
            OnboardingState.ACTIVE,
        ]
        current_idx = -1
        for i, state in enumerate(happy_path):
            if req.state == state or (req.state == OnboardingState.REQUESTED and i == 0):
                current_idx = i
                break

        if req.state == OnboardingState.REQUESTED:
            next_state = OnboardingState.CONFIG_REVIEW
        elif current_idx >= 0 and current_idx < len(happy_path) - 1:
            next_state = happy_path[current_idx + 1]
        else:
            return ServiceResult.fail(
                f"Cannot advance from state '{req.state.value}' — no next state in happy path"
            )

        # Special handling: when entering APPROVAL, create HITL approval request
        if next_state == OnboardingState.APPROVAL:
            self._create_hitl_approval(req)

        req.transition_to(next_state)
        self._save_request(req)

        self._audit_log(
            action="advance_onboarding",
            event_type=AuditEventType.DELEGATION,
            entity_id=request_id,
            result={"new_state": req.state.value},
        )

        # WS broadcast
        _broadcast_onboarding_event(
            request_id,
            "advanced",
            {
                "agent_id": req.agent_id,
                "state": req.state.value,
            },
        )

        # Create a task for the next step in the onboarding workflow
        receiver = "chief_of_staff"
        if req.state == OnboardingState.GENERATING:
            receiver = "cto"
        elif req.state == OnboardingState.TESTING:
            receiver = "qa-lead"
        elif req.state == OnboardingState.APPROVAL:
            receiver = "human-ceo"

        self.create_task(
            receiver_id=receiver,
            instruction=f"Onboarding for agent '{req.agent_id}' advanced to {req.state.value}. "
            f"Please process the next step.",
            priority=TaskPriority.MEDIUM,
            sender_id="hr-service",
        )

        logger.info("Advanced request %s to %s", request_id, req.state.value)
        return ServiceResult.ok(
            {
                "request_id": request_id,
                "agent_id": req.agent_id,
                "state": req.state.value,
            },
            request_id=request_id,
        )

    def security_review(
        self,
        request_id: str,
        reviewer: str,
        approved: bool,
        reason: str = "",
    ) -> ServiceResult[dict[str, Any]]:
        """Record the CTO security review outcome.

        If approved, transitions to GENERATING. If rejected, transitions to REJECTED.
        """
        req = self._get_request(request_id)
        if req is None:
            return ServiceResult.fail(f"Onboarding request '{request_id}' not found")

        if req.state != OnboardingState.SECURITY_REVIEW:
            return ServiceResult.fail(
                f"Security review requires state SECURITY_REVIEW, got '{req.state.value}'"
            )

        req.security_reviewer = reviewer
        req.security_reviewed_at = datetime.now(timezone.utc)
        if approved:
            req.transition_to(OnboardingState.GENERATING)
        else:
            req.transition_to(OnboardingState.REJECTED)
            req.error = reason or f"Security review rejected by {reviewer}"

        self._save_request(req)

        self._audit_log(
            action="security_review",
            event_type=AuditEventType.APPROVAL_RESOLVED,
            entity_id=request_id,
            result={
                "reviewer": reviewer,
                "approved": approved,
                "reason": reason,
            },
        )

        self.record_event(
            f"Security review for '{request_id}' by {reviewer}: {'approved' if approved else 'rejected'}",
            tags=["onboarding", "security_review", req.agent_id],
            reviewer=reviewer,
            approved=approved,
        )

        # WS broadcast
        _broadcast_onboarding_event(
            request_id,
            "security_review",
            {
                "agent_id": req.agent_id,
                "state": req.state.value,
                "reviewer": reviewer,
                "approved": approved,
            },
        )

        return ServiceResult.ok(
            {
                "request_id": request_id,
                "agent_id": req.agent_id,
                "state": req.state.value,
                "reviewer": reviewer,
                "approved": approved,
            },
            request_id=request_id,
        )

    def complete_generation(
        self, request_id: str, result: str = ""
    ) -> ServiceResult[dict[str, Any]]:
        """Complete the generation step and advance to TESTING."""
        req = self._get_request(request_id)
        if req is None:
            return ServiceResult.fail(f"Onboarding request '{request_id}' not found")

        if req.state != OnboardingState.GENERATING:
            return ServiceResult.fail(
                f"Cannot complete generation from state '{req.state.value}', expected 'generating'"
            )

        req.transition_to(OnboardingState.TESTING)
        self._save_request(req)

        self._audit_log(
            action="complete_generation",
            event_type=AuditEventType.DELEGATION,
            entity_id=request_id,
            result={"step": "generating", "new_state": req.state.value, "result": result},
        )

        # WS broadcast
        _broadcast_onboarding_event(
            request_id,
            "step_completed",
            {
                "agent_id": req.agent_id,
                "state": req.state.value,
                "step": "generating",
                "result": result,
            },
        )

        return ServiceResult.ok(
            {
                "request_id": request_id,
                "agent_id": req.agent_id,
                "state": req.state.value,
                "step_completed": "generating",
            },
            request_id=request_id,
        )

    def complete_testing(
        self, request_id: str, passed: bool = True, result: str = ""
    ) -> ServiceResult[dict[str, Any]]:
        """Complete the testing step and advance to APPROVAL or FAILED."""
        req = self._get_request(request_id)
        if req is None:
            return ServiceResult.fail(f"Onboarding request '{request_id}' not found")

        if req.state != OnboardingState.TESTING:
            return ServiceResult.fail(
                f"Cannot complete testing from state '{req.state.value}', expected 'testing'"
            )

        if passed:
            # When entering APPROVAL, create HITL approval request
            self._create_hitl_approval(req)
            req.transition_to(OnboardingState.APPROVAL)
        else:
            req.error = f"Testing failed: {result}" if result else "Testing failed"
            req.transition_to(OnboardingState.FAILED)

        self._save_request(req)

        self._audit_log(
            action="complete_testing",
            event_type=AuditEventType.DELEGATION,
            entity_id=request_id,
            result={
                "step": "testing",
                "passed": passed,
                "new_state": req.state.value,
                "result": result,
            },
        )

        # WS broadcast
        _broadcast_onboarding_event(
            request_id,
            "step_completed",
            {
                "agent_id": req.agent_id,
                "state": req.state.value,
                "step": "testing",
                "passed": passed,
                "result": result,
            },
        )

        return ServiceResult.ok(
            {
                "request_id": request_id,
                "agent_id": req.agent_id,
                "state": req.state.value,
                "step_completed": "testing",
                "passed": passed,
            },
            request_id=request_id,
        )

    def archive(self, request_id: str) -> ServiceResult[dict[str, Any]]:
        """Archive an onboarding request (agent deactivated or removed)."""
        req = self._get_request(request_id)
        if req is None:
            return ServiceResult.fail(f"Onboarding request '{request_id}' not found")

        if not can_transition(req.state, OnboardingState.ARCHIVED):
            return ServiceResult.fail(f"Cannot archive from state '{req.state.value}'")

        req.transition_to(OnboardingState.ARCHIVED)
        self._save_request(req)

        self._audit_log(
            action="archive_onboarding",
            event_type=AuditEventType.DELEGATION,
            entity_id=request_id,
            result={"new_state": req.state.value},
        )

        # WS broadcast
        _broadcast_onboarding_event(
            request_id,
            "archived",
            {
                "agent_id": req.agent_id,
                "state": req.state.value,
            },
        )

        return ServiceResult.ok(
            {
                "request_id": request_id,
                "agent_id": req.agent_id,
                "state": req.state.value,
            },
            request_id=request_id,
        )

    def retry_from_failure(self, request_id: str) -> ServiceResult[dict[str, Any]]:
        """Retry a failed onboarding request by transitioning back to GENERATING."""
        req = self._get_request(request_id)
        if req is None:
            return ServiceResult.fail(f"Onboarding request '{request_id}' not found")

        if req.state != OnboardingState.FAILED:
            return ServiceResult.fail(
                f"Cannot retry from state '{req.state.value}', expected 'failed'"
            )

        # Reset error and transition back to GENERATING
        req.error = ""
        req.transition_to(OnboardingState.GENERATING)
        self._save_request(req)

        self._audit_log(
            action="retry_onboarding",
            event_type=AuditEventType.DELEGATION,
            entity_id=request_id,
            result={"new_state": req.state.value},
        )

        # WS broadcast
        _broadcast_onboarding_event(
            request_id,
            "retry",
            {
                "agent_id": req.agent_id,
                "state": req.state.value,
            },
        )

        return ServiceResult.ok(
            {
                "request_id": request_id,
                "agent_id": req.agent_id,
                "state": req.state.value,
            },
            request_id=request_id,
        )

    def get_status(self, request_id: str) -> ServiceResult[dict[str, Any]]:
        """Get the current status of an onboarding request."""
        req = self._get_request(request_id)
        if req is None:
            return ServiceResult.fail(f"Onboarding request '{request_id}' not found")
        return ServiceResult.ok(req.to_dict())

    def list_requests(self, state: str = "") -> ServiceResult[list[dict[str, Any]]]:
        """List all onboarding requests, optionally filtered by state."""
        data = self._load_requests()
        requests = data.get("requests", [])
        if state:
            requests = [r for r in requests if r.get("state") == state]
        return ServiceResult.ok(requests)

    def _find_active_by_agent(self, agent_id: str) -> OnboardingRequest | None:
        """Find an active (non-terminal) onboarding request for an agent."""
        data = self._load_requests()
        for r in data.get("requests", []):
            if r.get("agent_id") == agent_id and r.get("state") not in (
                OnboardingState.REJECTED.value,
                OnboardingState.FAILED.value,
                OnboardingState.ARCHIVED.value,
            ):
                return OnboardingRequest(**r)
        return None

    def sweep_expired(self) -> int:
        """Transition expired pending onboarding requests to archived.

        Called by the daemon's governance cadence to prevent stale
        onboarding requests from blocking indefinitely.
        """
        from ai_company.orchestrator.approval import ApprovalGate

        gate = ApprovalGate.get_instance()
        expired_count = gate.sweep_expired()

        # Archive any onboarding requests whose approval expired
        data = self._load_requests()
        archived = 0
        for r in data.get("requests", []):
            if r.get("state") != OnboardingState.APPROVAL.value:
                continue
            req_id = r.get("id", "")
            approval = gate.get_request(req_id)
            if approval is not None and approval.status.value == "expired":
                r["state"] = OnboardingState.ARCHIVED.value
                r["updated_at"] = datetime.now(timezone.utc).isoformat()
                archived += 1

        if archived:
            self._save_requests(data)
            logger.info("Archived %d expired onboarding requests", archived)

        return expired_count + archived
