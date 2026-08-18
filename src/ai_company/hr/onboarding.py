"""Onboarding integration: wires the onboarding flow to the registry pipeline.

Issue #29 decisions:
- company-registry.yaml is the source of truth.
- Validate draft entries via RegistryValidator before committing.
- Use AgentGenerator().generate_all() (full regen) — safer, <5s for 127 agents.
- Rollback registry change if generation fails.
- Agent card output: .opencode/agents/<id>.md with canonical tool vocabulary.
- Agent appears in `ai-company agents list` and dashboard immediately after generation.

Issue #28 additions:
- SECURITY_REVIEW state (CTO sign-off) between config_review and generating.
- REJECTED terminal state with transitions from any non-terminal state.
- State transition validation via _TRANSITIONS table.
- FileStore persistence for onboarding requests (hr/onboarding_requests.yaml).
- HITL integration via ApprovalGate for the approval step.
"""

from __future__ import annotations

import logging
import shutil
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------


class OnboardingStatus(str, Enum):
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
    REJECTED = "rejected"
    FAILED = "failed"
    ARCHIVED = "archived"


# Valid forward transitions.  Terminal states have no outgoing edges.
_TRANSITIONS: dict[OnboardingStatus, frozenset[OnboardingStatus]] = {
    OnboardingStatus.REQUESTED: frozenset(
        {
            OnboardingStatus.CONFIG_REVIEW,
            OnboardingStatus.REJECTED,
        }
    ),
    OnboardingStatus.CONFIG_REVIEW: frozenset(
        {
            OnboardingStatus.SECURITY_REVIEW,
            OnboardingStatus.REJECTED,
        }
    ),
    OnboardingStatus.SECURITY_REVIEW: frozenset(
        {
            OnboardingStatus.GENERATING,
            OnboardingStatus.REJECTED,
        }
    ),
    OnboardingStatus.GENERATING: frozenset(
        {
            OnboardingStatus.TESTING,
            OnboardingStatus.FAILED,
            OnboardingStatus.REJECTED,
        }
    ),
    OnboardingStatus.TESTING: frozenset(
        {
            OnboardingStatus.APPROVAL,
            OnboardingStatus.FAILED,
            OnboardingStatus.REJECTED,
        }
    ),
    OnboardingStatus.APPROVAL: frozenset(
        {
            OnboardingStatus.ACTIVE,
            OnboardingStatus.REJECTED,
        }
    ),
    OnboardingStatus.ACTIVE: frozenset({OnboardingStatus.ARCHIVED}),
    OnboardingStatus.REJECTED: frozenset(),
    OnboardingStatus.FAILED: frozenset(),
    OnboardingStatus.ARCHIVED: frozenset(),
}

# Human-readable labels for CLI display.
STATE_LABELS: dict[OnboardingStatus, str] = {
    OnboardingStatus.REQUESTED: "Staffing request submitted",
    OnboardingStatus.CONFIG_REVIEW: "Agent configuration under review",
    OnboardingStatus.SECURITY_REVIEW: "Security review (CTO sign-off)",
    OnboardingStatus.GENERATING: "Generating agent files",
    OnboardingStatus.TESTING: "Running validation tests",
    OnboardingStatus.APPROVAL: "Awaiting human approval",
    OnboardingStatus.ACTIVE: "Agent deployed and active",
    OnboardingStatus.REJECTED: "Request rejected",
    OnboardingStatus.FAILED: "Generation/testing failed",
    OnboardingStatus.ARCHIVED: "Agent archived",
}


def valid_transitions(state: OnboardingStatus) -> frozenset[OnboardingStatus]:
    """Return the set of states reachable from *state*."""
    return _TRANSITIONS[state]


def can_transition(current: OnboardingStatus, target: OnboardingStatus) -> bool:
    """Check whether a transition from *current* to *target* is valid."""
    return target in _TRANSITIONS[current]


def is_terminal(state: OnboardingStatus) -> bool:
    """Return True if *state* has no outgoing transitions."""
    return not bool(_TRANSITIONS[state])


# ---------------------------------------------------------------------------
# Request model
# ---------------------------------------------------------------------------


@dataclass
class OnboardingRequest:
    """A single onboarding request tracked through the pipeline.

    Attributes:
        request_id: Unique request identifier (auto-generated if empty).
        agent_id: snake_case agent identifier.
        name: Human-readable agent name.
        role: Role title.
        department: Target department.
        agent_type: One of executive, specialist, board, default.
        reports_to: Parent agent ID or name.
        responsibilities: List of responsibility strings.
        tools: Tool vocabulary list.
        guidelines: Free-text guidelines.
        status: Current lifecycle state.
        created_at: ISO timestamp of creation.
        updated_at: ISO timestamp of last change.
        security_reviewer: Agent ID of CTO who reviewed security.
        security_reviewed_at: ISO timestamp of security review.
        approval_request_id: ApprovalGate request ID for HITL step.
        error: Error message if state transition failed.
    """

    request_id: str = ""
    agent_id: str = ""
    name: str = ""
    role: str = ""
    department: str = ""
    agent_type: str = "specialist"
    reports_to: str = ""
    responsibilities: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    guidelines: str = ""
    status: OnboardingStatus = OnboardingStatus.REQUESTED
    created_at: str = ""
    updated_at: str = ""
    security_reviewer: str = ""
    security_reviewed_at: str = ""
    approval_request_id: str = ""
    hitl_tier: int = 2
    error: str = ""

    def __post_init__(self) -> None:
        now = datetime.now(timezone.utc).isoformat()
        if not self.request_id:
            self.request_id = f"onb-{uuid.uuid4().hex[:12]}"
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now

    def transition_to(self, target: OnboardingStatus) -> None:
        """Execute a state transition, raising ValueError if invalid."""
        if not can_transition(self.status, target):
            raise ValueError(
                f"Invalid transition: {self.status.value} → {target.value}. "
                f"Allowed: {sorted(t.value for t in valid_transitions(self.status))}"
            )
        self.status = target
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a YAML-friendly dict."""
        return {
            "request_id": self.request_id,
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "department": self.department,
            "agent_type": self.agent_type,
            "reports_to": self.reports_to,
            "responsibilities": self.responsibilities,
            "tools": self.tools,
            "guidelines": self.guidelines,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "security_reviewer": self.security_reviewer,
            "security_reviewed_at": self.security_reviewed_at,
            "approval_request_id": self.approval_request_id,
            "hitl_tier": self.hitl_tier,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OnboardingRequest:
        """Deserialize from a YAML-loaded dict."""
        return cls(
            request_id=data.get("request_id", ""),
            agent_id=data.get("agent_id", ""),
            name=data.get("name", ""),
            role=data.get("role", ""),
            department=data.get("department", ""),
            agent_type=data.get("agent_type", "specialist"),
            reports_to=data.get("reports_to", ""),
            responsibilities=data.get("responsibilities", []),
            tools=data.get("tools", []),
            guidelines=data.get("guidelines", ""),
            status=OnboardingStatus(data.get("status", "requested")),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            security_reviewer=data.get("security_reviewer", ""),
            security_reviewed_at=data.get("security_reviewed_at", ""),
            approval_request_id=data.get("approval_request_id", ""),
            hitl_tier=data.get("hitl_tier", 2),
            error=data.get("error", ""),
        )


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
# Persistence
# ---------------------------------------------------------------------------

_REQUESTS_FILE = "onboarding_requests.yaml"


class _RequestStore:
    """FileStore-backed persistence for onboarding requests."""

    def __init__(self, data_dir: str | Path = "hr") -> None:
        self._store = FileStore(Path(data_dir), backup=True)

    def load_all(self) -> list[OnboardingRequest]:
        data = self._store.read_yaml(_REQUESTS_FILE)
        if not data or not isinstance(data, dict):
            return []
        return [
            OnboardingRequest.from_dict(r) for r in data.get("requests", []) if isinstance(r, dict)
        ]

    def save_all(self, requests: list[OnboardingRequest]) -> None:
        data = {"requests": [r.to_dict() for r in requests]}
        self._store.write_yaml(_REQUESTS_FILE, data)

    def save_one(self, req: OnboardingRequest) -> None:
        requests = self.load_all()
        for i, existing in enumerate(requests):
            if existing.request_id == req.request_id:
                requests[i] = req
                break
        else:
            requests.append(req)
        self.save_all(requests)

    def get(self, request_id: str) -> OnboardingRequest | None:
        for req in self.load_all():
            if req.request_id == request_id:
                return req
        return None

    def get_by_agent_id(self, agent_id: str) -> list[OnboardingRequest]:
        return [r for r in self.load_all() if r.agent_id == agent_id]


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------


class OnboardingManager:
    """Orchestrates the onboarding flow through the registry pipeline.

    Integrates with:
    - company-registry.yaml (source of truth for agent entries)
    - RegistryValidator (pre-commit validation)
    - AgentGenerator (full regeneration of .opencode/agents/*.md)
    - registry.sync (JSON sync for dashboard/executor)
    - ApprovalGate (HITL approval for the approval step)
    - FileStore persistence for onboarding requests
    """

    def __init__(
        self,
        registry_path: str | Path = "company-registry.yaml",
        templates_dir: str = "templates",
        output_dir: str = ".opencode/agents",
        data_dir: str | Path = "hr",
    ) -> None:
        self.registry_path = Path(registry_path)
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self._store = _RequestStore(data_dir)

    # ── Registry helpers ───────────────────────────────────────────────

    def _load_registry_yaml(self) -> dict[str, Any]:
        """Load the raw company-registry.yaml."""
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry not found: {self.registry_path}")
        with open(self.registry_path, encoding="utf-8") as f:
            data: dict[str, Any] = yaml.safe_load(f)
        if data is None:
            return {"company": {"name": "AI Company", "agents": []}}
        return data

    def _save_registry_yaml(self, data: dict[str, Any]) -> None:
        """Persist the raw company-registry.yaml."""
        with open(self.registry_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    def _backup_registry(self) -> Path:
        """Create a timestamped backup of company-registry.yaml for rollback."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup_path = self.registry_path.with_suffix(f".yaml.bak.{timestamp}")
        shutil.copy2(self.registry_path, backup_path)
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

        data = self._load_registry_yaml()
        existing_ids = self._get_existing_ids(data)

        if req.agent_id in existing_ids:
            errors.append(f"Agent ID '{req.agent_id}' already exists in the registry")

        if req.reports_to:
            agents = data.get("company", {}).get("agents", [])
            known_ids = {a.get("id", "") for a in agents if isinstance(a, dict)}
            known_names = {
                a.get("name", "").lower(): a.get("id", "") for a in agents if isinstance(a, dict)
            }
            if req.reports_to not in known_ids and req.reports_to.lower() not in known_names:
                errors.append(f"reports_to '{req.reports_to}' does not match any agent ID or name")

        if req.agent_type not in ("executive", "specialist", "board", "default"):
            errors.append(f"Invalid agent_type: '{req.agent_type}'")

        return errors

    # ── Registry integration ───────────────────────────────────────────

    def add_to_registry(self, req: OnboardingRequest) -> bool:
        """Add the onboarding request as a new agent entry in company-registry.yaml.

        Validates first, then appends. Returns True on success, False on validation error.
        Does NOT generate agent files — call generate() separately.
        """
        errors = self.validate_draft(req)
        if errors:
            for err in errors:
                logger.error("Validation failed: %s", err)
            return False

        data = self._load_registry_yaml()
        entry = _request_to_registry_entry(req)

        agents = data.setdefault("company", {}).setdefault("agents", [])
        agents.append(entry)

        self._save_registry_yaml(data)
        logger.info("Added agent '%s' to registry", req.agent_id)
        return True

    def generate(self, req: OnboardingRequest) -> list[Path]:
        """Run the full agent generation pipeline.

        1. Backs up company-registry.yaml.
        2. Ensures the agent entry is in the registry (adds if missing).
        3. Calls AgentGenerator().generate_all() for full regeneration.
        4. Syncs company/agent-registry.json.
        5. On failure: rolls back registry and raises.

        Returns list of generated file paths.
        """
        from ai_company.generator import AgentGenerator
        from ai_company.registry.sync import sync_registry

        backup_path = self._backup_registry()
        logger.info("Registry backed up to %s", backup_path)

        try:
            data = self._load_registry_yaml()
            existing_ids = self._get_existing_ids(data)

            if req.agent_id not in existing_ids and not self.add_to_registry(req):
                raise RuntimeError(f"Failed to add agent '{req.agent_id}' to registry")

            gen = AgentGenerator(
                registry_path=str(self.registry_path),
                templates_dir=str(self.templates_dir),
                output_dir=str(self.output_dir),
            )
            generated = gen.generate_all()
            logger.info("Generated %d agent files", len(generated))

            sync_registry(yaml_path=str(self.registry_path))
            logger.info("Synced registry to JSON")

            return generated

        except Exception:
            logger.error("Generation failed — rolling back registry to %s", backup_path)
            shutil.copy2(backup_path, self.registry_path)
            raise

    # ── Lifecycle transitions ──────────────────────────────────────────

    def create_request(
        self,
        agent_id: str,
        name: str,
        role: str,
        department: str,
        *,
        agent_type: str = "specialist",
        reports_to: str = "",
        responsibilities: list[str] | None = None,
        tools: list[str] | None = None,
        guidelines: str = "",
        requested_by: str = "operator",
    ) -> OnboardingRequest:
        """Create a new onboarding request in REQUESTED state and persist it."""
        req = OnboardingRequest(
            agent_id=agent_id,
            name=name,
            role=role,
            department=department,
            agent_type=agent_type,
            reports_to=reports_to,
            responsibilities=responsibilities or [],
            tools=tools or [],
            guidelines=guidelines,
        )
        self._store.save_one(req)
        logger.info("Created onboarding request %s for agent '%s'", req.request_id, agent_id)
        return req

    def advance(self, req: OnboardingRequest) -> OnboardingRequest:
        """Advance a request to its next logical state.

        The 'next state' is determined by the happy-path order:
        requested → config_review → security_review → generating → testing → approval → active
        """
        happy_path = [
            OnboardingStatus.CONFIG_REVIEW,
            OnboardingStatus.SECURITY_REVIEW,
            OnboardingStatus.GENERATING,
            OnboardingStatus.TESTING,
            OnboardingStatus.APPROVAL,
            OnboardingStatus.ACTIVE,
        ]
        current_idx = -1
        for i, state in enumerate(happy_path):
            if req.status == state or (req.status == OnboardingStatus.REQUESTED and i == 0):
                current_idx = i
                break

        if req.status == OnboardingStatus.REQUESTED:
            next_state = OnboardingStatus.CONFIG_REVIEW
        elif current_idx >= 0 and current_idx < len(happy_path) - 1:
            next_state = happy_path[current_idx + 1]
        else:
            raise ValueError(
                f"Cannot advance from state '{req.status.value}' — no next state in happy path"
            )

        # Special handling: when entering APPROVAL, create HITL approval request
        if next_state == OnboardingStatus.APPROVAL:
            self._create_hitl_approval(req)

        req.transition_to(next_state)
        self._store.save_one(req)
        logger.info("Advanced request %s to %s", req.request_id, next_state.value)
        return req

    def _create_hitl_approval(self, req: OnboardingRequest) -> None:
        """Create an ApprovalGate request for the APPROVAL step (HITL integration)."""
        from ai_company.orchestrator.approval import ApprovalGate

        gate = ApprovalGate.get_instance()

        # Determine tier based on tools (sensitive tools = tier 3)
        sensitive_tools = frozenset({"bash", "edit", "delete"})
        tier = 3 if any(t in sensitive_tools for t in req.tools) else 2
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
                request_id=req.request_id,
                task_id="",
                agent_id="hr",
                action="agent_onboarding",
                description=description,
                expires_in_minutes=2880,  # 48 hours
                tier=tier,
            )
            req.approval_request_id = approval.id
            logger.info(
                "Created HITL approval request %s for onboarding %s", approval.id, req.request_id
            )
        except ValueError as exc:
            logger.error("Failed to create HITL approval for %s: %s", req.request_id, exc)
            req.error = f"HITL approval creation failed: {exc}"

    def check_approval_status(self, req: OnboardingRequest) -> str | None:
        """Check the HITL approval status for a request in APPROVAL state.

        Returns:
            'approved' if approved, 'rejected' if rejected, 'expired' if expired,
            'pending' if still pending, None if not in APPROVAL state or no approval request.
        """
        if req.status != OnboardingStatus.APPROVAL or not req.approval_request_id:
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
        if req.status != OnboardingStatus.APPROVAL:
            raise ValueError(f"resolve_approval requires state APPROVAL, got '{req.status.value}'")

        status = self.check_approval_status(req)
        if status == "approved":
            req.transition_to(OnboardingStatus.ACTIVE)
            logger.info("Agent '%s' activated via HITL approval", req.agent_id)
        elif status in ("rejected", "expired"):
            req.transition_to(OnboardingStatus.REJECTED)
            req.error = f"HITL approval {status}"
            logger.info("Request %s rejected via HITL: %s", req.request_id, status)
        else:
            raise ValueError(f"Cannot resolve approval: status is '{status}'")

        self._store.save_one(req)
        return req

    def security_review(
        self, req: OnboardingRequest, reviewer: str, approved: bool
    ) -> OnboardingRequest:
        """Record the CTO security review outcome.

        If approved, transitions to GENERATING. If rejected, transitions to REJECTED.
        """
        if req.status != OnboardingStatus.SECURITY_REVIEW:
            raise ValueError(
                f"Security review requires state SECURITY_REVIEW, got '{req.status.value}'"
            )
        req.security_reviewer = reviewer
        req.security_reviewed_at = datetime.now(timezone.utc).isoformat()
        if approved:
            req.transition_to(OnboardingStatus.GENERATING)
        else:
            req.transition_to(OnboardingStatus.REJECTED)
            req.error = f"Security review rejected by {reviewer}"
        self._store.save_one(req)
        return req

    def approve(self, req: OnboardingRequest) -> OnboardingRequest:
        """Mark a request as approved (ACTIVE)."""
        req.transition_to(OnboardingStatus.ACTIVE)
        self._store.save_one(req)
        logger.info("Agent '%s' activated", req.agent_id)
        return req

    def reject(self, req: OnboardingRequest, reason: str = "") -> OnboardingRequest:
        """Reject a request from any non-terminal state."""
        req.transition_to(OnboardingStatus.REJECTED)
        if reason:
            req.error = reason
        self._store.save_one(req)
        logger.info("Request %s rejected: %s", req.request_id, reason or "no reason given")
        return req

    def activate(self, req: OnboardingRequest) -> OnboardingRequest:
        """Mark an onboarding request as active after successful generation + approval.

        Alias for approve() for backward compatibility.
        """
        return self.approve(req)

    def archive(self, req: OnboardingRequest) -> OnboardingRequest:
        """Archive an onboarding request (agent deactivated or removed)."""
        req.transition_to(OnboardingStatus.ARCHIVED)
        self._store.save_one(req)
        return req

    def record_failure(self, req: OnboardingRequest, error: str) -> OnboardingRequest:
        """Record a failure during generating or testing."""
        req.error = error
        if req.status in (OnboardingStatus.GENERATING, OnboardingStatus.TESTING):
            req.transition_to(OnboardingStatus.FAILED)
        self._store.save_one(req)
        return req

    # ── Query ──────────────────────────────────────────────────────────

    def get_request(self, request_id: str) -> OnboardingRequest | None:
        """Look up a request by its ID."""
        return self._store.get(request_id)

    def get_requests_by_agent(self, agent_id: str) -> list[OnboardingRequest]:
        """Return all requests for a given agent ID."""
        return self._store.get_by_agent_id(agent_id)

    def list_requests(self, status: OnboardingStatus | None = None) -> list[OnboardingRequest]:
        """List all requests, optionally filtered by status."""
        requests = self._store.load_all()
        if status is not None:
            requests = [r for r in requests if r.status == status]
        return requests
