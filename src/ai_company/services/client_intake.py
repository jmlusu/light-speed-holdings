"""Client intake service for Lightspeed Malawi service portfolio.

Manages client onboarding with governance gate enforcement, offer classification,
and inbox.json task creation. Integrates with the MessageBus for task delegation.

Governance Model (POL-CL-001):
  - G1: Signed contract (legal_owner)
  - G2: Data Processing Agreement + data classification (data_privacy_officer)
  - G3: Compliance risk assessment (compliance_officer)
  - G4: Security review (ciso)

Offers B and C are BLOCKED until board-ratified governance policies are active.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import Any, cast

import yaml

from ai_company.audit.events import AuditEventType
from ai_company.models.task import Task, TaskPriority
from ai_company.paths import get_project_root
from ai_company.services.base import BaseService, ServiceResult

logger = logging.getLogger(__name__)


class GovernanceGateError(Exception):
    """Raised when a governance gate is not satisfied for client onboarding."""


class ClientIntakeService(BaseService):
    """Service layer for client onboarding and offer engagement management.

    Manages the full client lifecycle from initial onboarding through delivery task
    creation, enforcing the Client Onboarding Approval Policy (POL-CL-001).
    """

    # Offers blocked until governance policies are ratified
    BLOCKED_OFFERS = frozenset({"offer_b", "offer_c"})

    # Required gates for all client work
    REQUIRED_GATES = ("contract", "dpa", "compliance", "security")

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(department_id="sales", **kwargs)
        self._offers = self._load_offers()

    def _load_offers(self) -> dict[str, Any]:
        """Load the Malawi offers config from config/company/malawi_offers.yaml."""
        offer_path = get_project_root() / "config" / "company" / "malawi_offers.yaml"
        if offer_path.exists():
            with open(offer_path, "r", encoding="utf-8") as f:
                return cast(dict[str, Any], yaml.safe_load(f) or {})
        logger.debug("Could not load malawi_offers.yaml; using defaults")
        return {}

    def _load_clients(self) -> dict[str, Any]:
        """Load client records from data store."""
        data = self._load_data("clients.yaml")
        if "clients" not in data:
            data["clients"] = []
        return data

    def _save_clients(self, data: dict[str, Any]) -> None:
        """Persist client records."""
        self._save_data("clients.yaml", data)

    def _check_gate_status(self, client_id: str) -> dict[str, bool]:
        """Check the status of all 4 governance gates for a client.

        Reads the same bare gate keys that ``_set_gate`` and the CLI
        ``client gate`` command write (``contract``, ``dpa``, ``compliance``,
        ``security``).  This is the single key vocabulary for gate storage.
        """
        data = self._load_data("governance_gates.yaml")
        gates = cast(dict[str, Any], data.get("gates", {}))
        client_gates = gates.get(client_id, {})
        return {gate: bool(client_gates.get(gate, False)) for gate in self.REQUIRED_GATES}

    def _set_gate(self, client_id: str, gate: str, passed: bool, reviewer: str = "") -> None:
        """Record a governance gate pass/fail."""
        data = self._load_data("governance_gates.yaml")
        gates = data.get("gates", {})
        client_gates = gates.setdefault(client_id, {})
        client_gates[gate] = passed
        if reviewer:
            client_gates[f"{gate}_by"] = reviewer
            client_gates[f"{gate}_at"] = datetime.now().isoformat()
        data["gates"] = gates
        self._save_data("governance_gates.yaml", data)

    # ── Public API ─────────────────────────────────────────────────────

    def create_client(
        self,
        client_id: str,
        client_name: str,
        client_type: str = "ngo",
        contact_email: str = "",
        currency: str = "USD",
    ) -> ServiceResult[dict[str, Any]]:
        """Create a new client record.

        Args:
            client_id: Unique client identifier.
            client_name: Client organization name.
            client_type: 'ngo', 'sme', 'agency', 'individual'.
            contact_email: Primary contact email.
            currency: 'USD' or 'MWK'.
        """
        data = self._load_clients()
        clients = cast(list[dict[str, Any]], data.get("clients", []))

        for client in clients:
            if client["id"] == client_id:
                return ServiceResult.fail(
                    f"Client '{client_id}' already exists",
                    client_id=client_id,
                )

        new_client = {
            "id": client_id,
            "name": client_name,
            "type": client_type,
            "contact_email": contact_email,
            "currency": currency,
            "created_at": datetime.now().isoformat(),
            "governance_gates_passed": False,
        }
        clients.append(new_client)
        data["clients"] = clients
        self._save_clients(data)

        self.record_event(
            f"Client '{client_name}' ({client_type}) registered",
            tags=["client", "created", client_type],
            client_id=client_id,
            currency=currency,
        )

        return ServiceResult.ok(new_client, client_id=client_id)

    def check_governance_gates(self, client_id: str) -> ServiceResult[dict[str, Any]]:
        """Check all 4 governance gates for a client.

        Returns a result with the gate status dict. If all gates pass,
        the client is cleared for engagement.
        """
        gates = self._check_gate_status(client_id)
        all_passed = all(gates.values())

        if not all_passed:
            missing = [g for g, passed in gates.items() if not passed]
            return ServiceResult.fail(
                f"Governance gates not satisfied: {missing}",
                client_id=client_id,
                gates=gates,
                missing=missing,
            )

        self._set_gate(client_id, "all_gates_passed", True, "system")
        data = self._load_clients()
        clients = cast(list[dict[str, Any]], data.get("clients", []))
        for c in clients:
            if c["id"] == client_id:
                c["governance_gates_passed"] = True
        self._save_clients(data)

        return ServiceResult.ok(
            {"gates": gates, "all_passed": True},
            client_id=client_id,
        )

    def create_engagement(
        self,
        client_id: str,
        offer_code: str,
        description: str,
        lead_agent: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM,
        **gate_evidence: Any,
    ) -> ServiceResult[Task]:
        """Create a client engagement task and push it to the inbox.

        Enforces offer-blocking (Offers B/C) and governance gate checks
        before task creation.

        Args:
            client_id: The registered client ID.
            offer_code: One of 'offer_a', 'offer_b', 'offer_c', 'offer_d', 'offer_e'.
            description: Project description / brief.
            lead_agent: The primary agent to receive the task.
            priority: Task priority.
            **gate_evidence: Evidence IDs for each governance gate
                             (e.g. contract='signed-2026-001').

        Raises:
            GovernanceGateError: If the offer is blocked or governance gates fail.
        """
        # Check if offer is blocked
        if offer_code in self.BLOCKED_OFFERS:
            blocked_info = self._offers.get("offers", {}).get(offer_code, {})
            reason = blocked_info.get("blocked_reason", "unknown")
            logger.warning(
                "Attempted to create engagement for blocked offer %s (client=%s). Reason: %s",
                offer_code,
                client_id,
                reason,
            )
            raise GovernanceGateError(
                f"Offer {offer_code} is BLOCKED. Reason: {reason}. "
                f"See config/company/malawi_offers.yaml for unblock conditions."
            )

        # Check governance gates
        gates = self._check_gate_status(client_id)
        missing = [g for g, passed in gates.items() if not passed]
        if missing:
            raise GovernanceGateError(
                f"Governance gates not satisfied for client {client_id}: {missing}. "
                f"All gates must pass before client work begins."
            )

        # Record gate evidence
        for gate, evidence in gate_evidence.items():
            self._set_gate(client_id, gate, True, str(evidence))

        # Create the inbox task with proper tags
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            name=f"Client engagement: {client_id}",
            description=description,
            sender_id="client_intake_service",
            receiver_id=lead_agent or "chief_of_staff",
            instruction=(
                f"Execute client engagement for {client_id} under {offer_code}.\n"
                f"Description: {description}\n"
                f"Lead agent: {lead_agent or 'chief_of_staff'}\n"
                f"Governance gates verified: {', '.join(self.REQUIRED_GATES)}\n"
                f"Offer: {offer_code}\n"
                f"Client: {client_id}"
            ),
            priority=priority,
            tags=[offer_code, f"client_{client_id}", "client_work"],
            correlation_id=f"eng-{client_id}-{task_id[:8]}",
            requires_approval=True,
        )

        self.bus.send_task(task)
        self._audit_log(
            action="create_engagement",
            event_type=AuditEventType.TASK_CREATED,
            entity_id=client_id,
            result={
                "task_id": task_id,
                "offer_code": offer_code,
                "lead_agent": lead_agent,
                "gates_verified": list(self.REQUIRED_GATES),
            },
            task_id=task_id,
        )

        self.record_event(
            f"Engagement created for client '{client_id}' under {offer_code}",
            tags=["engagement", "created", offer_code, client_id],
            task_id=task_id,
            offer=offer_code,
        )

        return ServiceResult.ok(
            task,
            task_id=task_id,
            client_id=client_id,
            offer_code=offer_code,
            gates_verified=True,
        )

    def list_clients(self, client_type: str = "") -> ServiceResult[list[dict[str, Any]]]:
        """List all registered clients, optionally filtered by type."""
        data = self._load_clients()
        clients = cast(list[dict[str, Any]], data.get("clients", []))
        if client_type:
            clients = [c for c in clients if c.get("type") == client_type]
        return ServiceResult.ok(clients)

    def list_engagements(self) -> ServiceResult[list[dict[str, Any]]]:
        """List all client engagements from the inbox."""
        tasks = self.bus.get_pending_tasks()
        client_tasks = [t for t in tasks if "client_work" in (t.tags or [])]
        engagements: list[dict[str, Any]] = []
        for t in client_tasks:
            client_tag = next(
                (tag.replace("client_", "") for tag in (t.tags or []) if tag.startswith("client_")),
                "unknown",
            )
            offer_tag = t.tags[0] if t.tags else "unknown"
            engagements.append(
                {
                    "task_id": t.id,
                    "client": client_tag,
                    "offer": offer_tag,
                    "description": t.description,
                    "priority": t.priority.value,
                    "requires_approval": t.requires_approval,
                }
            )
        return ServiceResult.ok(engagements)

    def set_gate(
        self,
        client_id: str,
        gate: str,
        passed: bool,
        reviewer: str = "",
    ) -> ServiceResult[bool]:
        """Manually set a governance gate status.

        Used to record evidence that G1-G4 gates have passed.
        """
        if gate not in self.REQUIRED_GATES:
            return ServiceResult.fail(
                f"Invalid gate '{gate}'. Must be one of: {self.REQUIRED_GATES}",
            )

        self._set_gate(client_id, gate, passed, reviewer)
        self.record_event(
            f"Governance gate '{gate}' for client '{client_id}': {'PASSED' if passed else 'FAILED'}",
            tags=["governance", "gate", gate, client_id],
            reviewer=reviewer,
        )
        return ServiceResult.ok(True, client_id=client_id, gate=gate, passed=passed)

    def get_summary(self) -> dict[str, Any]:
        """Return a summary of client intake state."""
        return {
            **super().get_summary(),
            "blocked_offers": list(self.BLOCKED_OFFERS),
            "offers_config_loaded": bool(self._offers),
        }
