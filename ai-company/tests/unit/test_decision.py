"""Tests for the Decision engine."""

from __future__ import annotations

import pytest

from ai_company.decision.engine import DecisionEngine
from ai_company.models import (
    ApprovalEntry,
    CompanyRegistry,
    Company,
    DecisionNode,
    DecisionTreeConfig,
    RiskMatrixConfig,
    RiskLevelConfig,
)


@pytest.fixture()
def registry() -> CompanyRegistry:
    return CompanyRegistry(
        company=Company(id="test", name="Test"),
        approval_matrix=[
            ApprovalEntry(
                action="budget_over_1m",
                risk_level="high",
                required_approvals=["cfo", "ceo"],
                sla_hours=48,
            ),
            ApprovalEntry(
                action="emergency_deployment",
                risk_level="critical",
                required_approvals=["cto"],
                sla_hours=4,
                auto_approve=False,
            ),
            ApprovalEntry(
                action="daily_config_update",
                risk_level="low",
                required_approvals=[],
                sla_hours=1,
                auto_approve=True,
            ),
        ],
        risk_matrix=RiskMatrixConfig(
            risk_levels=[
                RiskLevelConfig(min_score=0, max_score=1, level="low", action="auto_approve"),
                RiskLevelConfig(min_score=2, max_score=3, level="medium", action="review"),
                RiskLevelConfig(min_score=4, max_score=5, level="high", action="approve"),
            ]
        ),
        decision_tree=DecisionTreeConfig(
            nodes=[
                DecisionNode(id="start", question="Is this a budget request?", type="branch", children=["budget_yes", "budget_no"]),
                DecisionNode(id="budget_yes", question="Amount over 1M?", type="branch", children=["high_value", "low_value"]),
                DecisionNode(id="budget_no", action="auto_approve", authority="manager", type="action"),
                DecisionNode(id="high_value", action="require_board_approval", authority="board", type="action"),
                DecisionNode(id="low_value", action="require_cfo_approval", authority="cfo", type="action"),
            ]
        ),
    )


@pytest.fixture()
def engine(registry: CompanyRegistry) -> DecisionEngine:
    return DecisionEngine(registry)


class TestDecisionEngine:
    def test_evaluate_auto_approve(self, engine: DecisionEngine):
        result = engine.evaluate_action("daily_config_update")
        assert result["requires_approval"] is False
        assert result["auto_approve"] is True

    def test_evaluate_requires_approval(self, engine: DecisionEngine):
        result = engine.evaluate_action("budget_over_1m")
        assert result["requires_approval"] is True
        assert "cfo" in result["approvers"]
        assert "ceo" in result["approvers"]
        assert result["sla_hours"] == 48

    def test_evaluate_unknown_action(self, engine: DecisionEngine):
        result = engine.evaluate_action("unknown_action")
        assert result["requires_approval"] is False
        assert result["auto_approve"] is True

    def test_risk_assessment_critical(self, engine: DecisionEngine):
        result = engine.evaluate_action("emergency_security_fix")
        assert result["risk_level"] == "critical"

    def test_risk_assessment_high(self, engine: DecisionEngine):
        result = engine.evaluate_action("budget_increase")
        assert result["risk_level"] == "high"

    def test_risk_assessment_medium(self, engine: DecisionEngine):
        result = engine.evaluate_action("deploy_new_version")
        assert result["risk_level"] == "medium"

    def test_risk_assessment_low(self, engine: DecisionEngine):
        result = engine.evaluate_action("update_readme")
        assert result["risk_level"] == "low"

    def test_navigate_tree_to_action(self, engine: DecisionEngine):
        result = engine.navigate_tree("start", {"start": "budget_no"})
        assert result["action"] == "auto_approve"
        assert result["authority"] == "manager"
        assert "start" in result["visited"]
        assert "budget_no" in result["visited"]

    def test_navigate_tree_deep(self, engine: DecisionEngine):
        result = engine.navigate_tree("start", {"start": "budget_yes", "budget_yes": "high_value"})
        assert result["action"] == "require_board_approval"
        assert result["authority"] == "board"

    def test_navigate_tree_unknown_node(self, engine: DecisionEngine):
        result = engine.navigate_tree("nonexistent", {})
        assert "error" in result

    def test_list_actions(self, engine: DecisionEngine):
        actions = engine.list_actions()
        assert len(actions) == 3
        action_ids = [a["action"] for a in actions]
        assert "budget_over_1m" in action_ids
