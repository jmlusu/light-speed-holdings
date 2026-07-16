"""Decision engine — evaluates requests against approval matrix, risk matrix, and decision tree."""

from __future__ import annotations

from typing import Any

from ai_company.models import (
    ApprovalEntry,
    CompanyRegistry,
    RiskLevel,
)


class DecisionEngine:
    """Evaluates decisions against governance rules."""

    def __init__(self, registry: CompanyRegistry) -> None:
        self.registry = registry
        self._approval_map: dict[str, ApprovalEntry] = {
            a.action: a for a in registry.approval_matrix
        }

    def evaluate_action(self, action: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Evaluate whether an action requires approval and from whom.

        Returns a dict with:
            - action: the original action
            - requires_approval: bool
            - approvers: list of required approver IDs
            - sla_hours: SLA for approval
            - risk_level: assessed risk level
            - auto_approve: whether it can be auto-approved
        """
        ctx = context or {}
        risk_level = self._assess_risk(action, ctx)
        entry = self._find_approval_entry(action)

        if entry is None:
            return {
                "action": action,
                "requires_approval": False,
                "approvers": [],
                "sla_hours": 0,
                "risk_level": risk_level.value,
                "auto_approve": True,
            }

        return {
            "action": action,
            "requires_approval": not entry.auto_approve,
            "approvers": entry.required_approvals,
            "sla_hours": entry.sla_hours,
            "risk_level": risk_level.value,
            "auto_approve": entry.auto_approve,
        }

    def navigate_tree(self, start_node_id: str, answers: dict[str, str]) -> dict[str, Any]:
        """Navigate the decision tree from a start node, following answers.

        Returns the final decision node reached.
        """
        nodes = {n.id: n for n in self.registry.decision_tree.nodes}
        current = nodes.get(start_node_id)
        if current is None:
            return {"error": f"Node '{start_node_id}' not found", "node": None}

        visited = [current.id]
        while current and current.type == "branch":
            answer = answers.get(current.id, "")
            next_id = answer if answer in current.children else (current.children[0] if current.children else None)
            if next_id is None:
                break
            current = nodes.get(next_id)
            if current:
                visited.append(current.id)

        return {
            "node": current.id if current else None,
            "action": current.action if current else None,
            "authority": current.authority if current else None,
            "visited": visited,
        }

    def list_actions(self) -> list[dict[str, Any]]:
        """List all actions in the approval matrix with their requirements."""
        results = []
        for entry in self.registry.approval_matrix:
            results.append({
                "action": entry.action,
                "risk_level": entry.risk_level,
                "required_approvals": entry.required_approvals,
                "sla_hours": entry.sla_hours,
                "auto_approve": entry.auto_approve,
            })
        return results

    def _assess_risk(self, action: str, context: dict[str, Any]) -> RiskLevel:
        """Assess the risk level of an action based on risk matrix rules."""
        # Check if any risk level config matches
        for level_config in self.registry.risk_matrix.risk_levels:
            if level_config.level.lower() in action.lower():
                try:
                    return RiskLevel(level_config.level.lower())
                except ValueError:
                    pass

        # Default: match by keyword
        action_lower = action.lower()
        if any(w in action_lower for w in ("critical", "emergency", "security")):
            return RiskLevel.CRITICAL
        if any(w in action_lower for w in ("budget", "hire", "acquisition", "legal")):
            return RiskLevel.HIGH
        if any(w in action_lower for w in ("procurement", "deploy", "config")):
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def _find_approval_entry(self, action: str) -> ApprovalEntry | None:
        """Find the matching approval entry for an action."""
        # Exact match
        if action in self._approval_map:
            return self._approval_map[action]

        # Partial match
        action_lower = action.lower()
        for entry in self.registry.approval_matrix:
            if entry.action.lower() in action_lower or action_lower in entry.action.lower():
                return entry

        return None
