"""Legal department service layer.

Provides contract management, compliance tracking, and legal review with
MessageBus integration for task delegation.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from ai_company.models.task import TaskPriority
from ai_company.services.base import BaseService

logger = logging.getLogger(__name__)


class LegalService(BaseService):
    """Service layer for the Legal department.

    Manages contracts, compliance, and legal review workflows.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(department_id="legal", **kwargs)

    # ── Contract management ───────────────────────────────────────────

    def list_contracts(self, status: str = "") -> list[dict[str, Any]]:
        """List all contracts, optionally filtered by status."""
        data = self._load_data("contracts.yaml")
        contracts = data.get("contracts", [])
        if status:
            contracts = [c for c in contracts if c.get("status") == status]
        return contracts

    def add_contract(
        self,
        contract_id: str,
        name: str,
        party: str,
        contract_type: str = "service",
        value: float = 0.0,
    ) -> dict[str, Any]:
        """Add a new contract and delegate review task."""
        data = self._load_data("contracts.yaml")
        contracts = data.get("contracts", [])

        for c in contracts:
            if c["id"] == contract_id:
                raise ValueError(f"Contract '{contract_id}' already exists")

        new_contract = {
            "id": contract_id,
            "name": name,
            "party": party,
            "type": contract_type,
            "value": value,
            "status": "draft",
            "created_at": datetime.now().isoformat(),
        }
        contracts.append(new_contract)
        data["contracts"] = contracts
        self._save_data("contracts.yaml", data)

        self.record_event(
            f"Contract '{name}' added with {party} (type={contract_type})",
            tags=["contract", "created", contract_type],
            contract_id=contract_id,
        )

        # Delegate review task
        priority = TaskPriority.HIGH if value > 50000 else TaskPriority.MEDIUM
        self.create_task(
            receiver_id="legal-specialist",
            instruction=(
                f"Review contract '{name}' with {party}. "
                f"Type: {contract_type}. Value: ${value:,.2f}. "
                f"Check terms, identify risks, and prepare approval recommendation."
            ),
            priority=priority,
        )

        return new_contract

    def approve_contract(self, contract_id: str, approver: str = "") -> dict[str, Any]:
        """Approve a contract."""
        data = self._load_data("contracts.yaml")
        contracts = data.get("contracts", [])

        contract = next((c for c in contracts if c["id"] == contract_id), None)
        if not contract:
            raise ValueError(f"Contract '{contract_id}' not found")

        contract["status"] = "approved"
        contract["approved_at"] = datetime.now().isoformat()
        contract["approved_by"] = approver
        data["contracts"] = contracts
        self._save_data("contracts.yaml", data)

        self.record_event(
            f"Contract '{contract['name']}' approved by {approver or 'system'}",
            tags=["contract", "approved"],
            contract_id=contract_id,
        )

        # Record knowledge
        self.record_knowledge(
            topic="contract_approval",
            content=f"Contract '{contract['name']}' with {contract.get('party', 'unknown')} approved. Value: ${contract.get('value', 0):,.2f}",
        )

        return contract

    def terminate_contract(self, contract_id: str, reason: str = "") -> dict[str, Any]:
        """Terminate a contract."""
        data = self._load_data("contracts.yaml")
        contracts = data.get("contracts", [])

        contract = next((c for c in contracts if c["id"] == contract_id), None)
        if not contract:
            raise ValueError(f"Contract '{contract_id}' not found")

        contract["status"] = "terminated"
        contract["terminated_at"] = datetime.now().isoformat()
        contract["termination_reason"] = reason
        data["contracts"] = contracts
        self._save_data("contracts.yaml", data)

        self.record_event(
            f"Contract '{contract['name']}' terminated: {reason or 'unspecified'}",
            tags=["contract", "terminated"],
            contract_id=contract_id,
        )

        return contract

    # ── Compliance ────────────────────────────────────────────────────

    def compliance_check(self) -> dict[str, Any]:
        """Run compliance checks on active contracts."""
        data = self._load_data("contracts.yaml")
        contracts = data.get("contracts", [])

        active = [c for c in contracts if c.get("status") == "approved"]
        draft = [c for c in contracts if c.get("status") == "draft"]
        terminated = [c for c in contracts if c.get("status") == "terminated"]

        return {
            "total_contracts": len(contracts),
            "active": len(active),
            "draft_pending": len(draft),
            "terminated": len(terminated),
        }

    def get_summary(self) -> dict[str, Any]:
        """Legal department summary."""
        return {
            **super().get_summary(),
            **self.compliance_check(),
        }
