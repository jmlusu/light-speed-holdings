"""Tests that autonomous escalation decisions are written to the audit trail.

GAP-008 follow-up: ``AutonomousDecisionEngine.suggest_retry`` must emit an
ESCALATION audit event when its self-healing retry policy reaches the
"escalate" strategy (attempt >= 4).
"""

from __future__ import annotations

from unittest.mock import patch

from ai_company.executor.autonomous import AutonomousDecisionEngine



def _make_engine(tmp_path) -> AutonomousDecisionEngine:
    return AutonomousDecisionEngine(history_dir=tmp_path / "decisions")


def test_suggest_retry_logs_escalation_event(tmp_path):
    """An ESCALATION audit event is emitted when escalation is decided."""
    engine = _make_engine(tmp_path)

    captured: dict = {}

    def _fake_log(
        task_id, from_agent, to_agent, reason, rule_id="", resolved=False
    ):
        captured["called"] = True
        captured["from_agent"] = from_agent
        captured["to_agent"] = to_agent
        captured["reason"] = reason
        captured["rule_id"] = rule_id

    with patch(
        "ai_company.executor.autonomous"
        ".AutonomousDecisionEngine._audit_escalation"
    ) as spy:
        # Patch the underlying audit integration call directly.
        with patch(
            "ai_company.audit.integration.log_escalation", side_effect=_fake_log
        ):
            result = engine.suggest_retry(
                tool="execute",
                error="persistent failure",
                attempt=4,
                original_args={"command": "ls"},
            )

    assert result is None
    assert spy.called, "escalation audit hook should have been invoked"


def test_suggest_retry_no_escalation_before_attempt_4(tmp_path):
    """Below attempt 4 no escalation audit event is emitted."""
    engine = _make_engine(tmp_path)

    with patch(
        "ai_company.audit.integration.log_escalation"
    ) as mock_log:
        result = engine.suggest_retry(
            tool="execute",
            error="transient failure",
            attempt=1,
            original_args={"command": "ls"},
        )

    assert result is not None
    mock_log.assert_not_called()


def test_audit_escalation_helper_calls_log(tmp_path):
    """The helper itself delegates to log_escalation with expected fields."""
    engine = _make_engine(tmp_path)

    captured: dict = {}
    with patch(
        "ai_company.audit.integration.log_escalation",
        side_effect=lambda task_id, from_agent, to_agent, reason, rule_id="",
        resolved=False: captured.update(
            task_id=task_id, from_agent=from_agent, to_agent=to_agent,
            reason=reason, rule_id=rule_id,
        ),
    ):
        engine._audit_escalation(tool="execute", attempt=5, error="boom")

    assert captured["from_agent"] == "autonomous_decision_engine"
    assert captured["to_agent"] == "human"
    assert "attempt=5" in captured["reason"]
    assert captured["rule_id"] == "autonomous-escalation"
