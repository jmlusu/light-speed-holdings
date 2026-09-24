"""Permission Gateway — Default-Deny External Access Control.

Implements architecture §9: 5-gate chain with human approval.
"""

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class GateResult(str, Enum):
    """Result of a gate check."""

    PASS = "pass"
    BLOCK = "block"
    REQUIRE_HUMAN = "require_human"


@dataclass
class GatewayConfig:
    """Gateway configuration (architecture §9.1 schema)."""

    enabled: bool = False
    approved_providers: List[str] = field(default_factory=list)
    approved_domains: List[str] = field(default_factory=list)
    approved_operations: List[str] = field(default_factory=list)
    data_classes_allowed: Dict[str, bool] = field(
        default_factory=lambda: {
            "public": False,
            "internal": False,
            "confidential": False,
            "restricted": False,
        }
    )

    @classmethod
    def from_file(cls, path: Path) -> "GatewayConfig":
        """Load config from JSON file."""
        with open(path) as f:
            data = json.load(f)
        return cls(**data.get("external_access", {}))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GatewayConfig":
        """Create config from dictionary (e.g., from EngineConfig.gateway)."""
        ext_access = data.get("external_access", {})
        return cls(
            enabled=ext_access.get("enabled", False),
            approved_providers=ext_access.get("approved_providers", []),
            approved_domains=ext_access.get("approved_domains", []),
            approved_operations=ext_access.get("approved_operations", []),
            data_classes_allowed=ext_access.get(
                "data_classes_allowed",
                {
                    "public": False,
                    "internal": False,
                    "confidential": False,
                    "restricted": False,
                },
            ),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "external_access": {
                "enabled": self.enabled,
                "approved_providers": self.approved_providers,
                "approved_domains": self.approved_domains,
                "approved_operations": self.approved_operations,
                "data_classes_allowed": self.data_classes_allowed,
            }
        }


@dataclass
class GatewayDecision:
    """Result of a gateway evaluation."""

    allowed: bool
    reason: str
    requires_human_approval: bool
    approval_token: Optional[str] = None
    audit_event: Optional[Dict[str, Any]] = None
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_audit_dict(self) -> Dict[str, Any]:
        return {
            "event_type": "gateway_approved" if self.allowed else "gateway_denied",
            "correlation_id": self.correlation_id,
            "details": {
                "reason": self.reason,
                "requires_human_approval": self.requires_human_approval,
                "approval_token": self.approval_token,
            },
        }


class PermissionGateway:
    """
    Permission Gateway implementing 5-gate chain (architecture §9):

    1. enabled? — Is external access enabled globally?
    2. provider approved? — Is the provider in approved_providers?
    3. domain approved? — Is the destination domain in approved_domains?
    4. operation approved? — Is the operation in approved_operations?
    5. classification permitted? — Is the data class allowed?

    If all pass → human approval with payload preview → transmit → audit.
    Any NO → BLOCK + audit denial.
    When uncertain → BLOCK (locked decision 3).
    """

    def __init__(self, config: Optional[GatewayConfig] = None):
        self.config = config or GatewayConfig()
        self._pending_approvals: Dict[str, Dict[str, Any]] = {}

    def evaluate(
        self,
        agent_id: str,
        provider: str,
        operation: str,
        destination: str,
        data_classification: str,
        payload_preview: str,
        correlation_id: Optional[str] = None,
    ) -> GatewayDecision:
        """
        Evaluate the 5-gate chain.

        Returns GatewayDecision with audit_event pre-populated.
        """
        corr_id = correlation_id or str(uuid.uuid4())
        classification = data_classification.lower()

        # Gate 1: Enabled
        if not self.config.enabled:
            return self._block(
                corr_id,
                "External access disabled globally",
                agent_id,
                provider,
                operation,
                destination,
                classification,
                payload_preview,
            )

        # Gate 2: Provider approved
        if provider not in self.config.approved_providers:
            return self._block(
                corr_id,
                f"Provider '{provider}' not approved",
                agent_id,
                provider,
                operation,
                destination,
                classification,
                payload_preview,
            )

        # Gate 3: Domain approved
        domain_allowed = any(domain in destination for domain in self.config.approved_domains)
        if not domain_allowed:
            return self._block(
                corr_id,
                f"Destination domain not approved: {destination}",
                agent_id,
                provider,
                operation,
                destination,
                classification,
                payload_preview,
            )

        # Gate 4: Operation approved
        if operation not in self.config.approved_operations:
            return self._block(
                corr_id,
                f"Operation '{operation}' not approved",
                agent_id,
                provider,
                operation,
                destination,
                classification,
                payload_preview,
            )

        # Gate 5: Classification permitted
        if not self.config.data_classes_allowed.get(classification, False):
            return self._block(
                corr_id,
                f"Data classification '{classification}' not permitted for egress",
                agent_id,
                provider,
                operation,
                destination,
                classification,
                payload_preview,
            )

        # All gates passed — require human approval
        approval_token = str(uuid.uuid4())

        # Store pending approval
        self._pending_approvals[approval_token] = {
            "agent_id": agent_id,
            "provider": provider,
            "operation": operation,
            "destination": destination,
            "classification": classification,
            "payload_preview": payload_preview,
            "correlation_id": corr_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        audit_event = {
            "event_type": "gateway_request",
            "correlation_id": corr_id,
            "details": {
                "agent_id": agent_id,
                "provider": provider,
                "operation": operation,
                "destination": destination,
                "data_classification": classification,
                "payload_preview": payload_preview,
                "approval_token": approval_token,
                "status": "pending_human_approval",
            },
        }

        return GatewayDecision(
            allowed=False,  # Not allowed until human approves
            reason="All gates passed; awaiting human approval",
            requires_human_approval=True,
            approval_token=approval_token,
            audit_event=audit_event,
            correlation_id=corr_id,
        )

    def submit_human_approval(
        self,
        approval_token: str,
        approved_by: str,
        approved: bool,
    ) -> GatewayDecision:
        """
        Submit human approval/denial for a pending request.

        Called by human via CLI/dashboard.
        """
        pending = self._pending_approvals.pop(approval_token, None)
        if not pending:
            return GatewayDecision(
                allowed=False,
                reason="Invalid or expired approval token",
                requires_human_approval=False,
                correlation_id=str(uuid.uuid4()),
            )

        corr_id = pending["correlation_id"]

        if approved:
            audit_event = {
                "event_type": "gateway_approved",
                "correlation_id": corr_id,
                "details": {
                    **pending,
                    "approved_by": approved_by,
                    "approved_at": datetime.now(timezone.utc).isoformat(),
                    "status": "approved",
                },
            }
            return GatewayDecision(
                allowed=True,
                reason="Human approved",
                requires_human_approval=False,
                approval_token=approval_token,
                audit_event=audit_event,
                correlation_id=corr_id,
            )
        else:
            audit_event = {
                "event_type": "gateway_denied",
                "correlation_id": corr_id,
                "details": {
                    **pending,
                    "denied_by": approved_by,
                    "denied_at": datetime.now(timezone.utc).isoformat(),
                    "status": "denied",
                },
            }
            return GatewayDecision(
                allowed=False,
                reason="Human denied",
                requires_human_approval=False,
                approval_token=approval_token,
                audit_event=audit_event,
                correlation_id=corr_id,
            )

    def get_pending_approvals(self) -> List[Dict[str, Any]]:
        """Get all pending approvals for UI polling."""
        return [
            {"approval_token": token, **details}
            for token, details in self._pending_approvals.items()
        ]

    def _block(
        self,
        correlation_id: str,
        reason: str,
        agent_id: str,
        provider: str,
        operation: str,
        destination: str,
        classification: str,
        payload_preview: str,
    ) -> GatewayDecision:
        """Create a BLOCK decision with audit event."""
        audit_event = {
            "event_type": "gateway_denied",
            "correlation_id": correlation_id,
            "details": {
                "agent_id": agent_id,
                "provider": provider,
                "operation": operation,
                "destination": destination,
                "data_classification": classification,
                "payload_preview": payload_preview,
                "reason": reason,
                "status": "blocked",
            },
        }
        return GatewayDecision(
            allowed=False,
            reason=reason,
            requires_human_approval=False,
            audit_event=audit_event,
            correlation_id=correlation_id,
        )

    def check_local_operation(self) -> GatewayDecision:
        """Local operations (store, search, inject) auto-allowed."""
        return GatewayDecision(
            allowed=True,
            reason="Local operation — no external access",
            requires_human_approval=False,
            correlation_id=str(uuid.uuid4()),
        )
