"""Tests for the 5-tier approval system (prompts and tier rules).

Covers:
- Tier classification for each tool type
- Path-based escalation (writing to sensitive paths)
- Command-based escalation (dangerous commands)
- Agent seniority de-escalation
- Task context escalation
- Notification template rendering
- Escalation template rendering
- Dashboard summary prompt
"""

from __future__ import annotations

from typing import Any, cast

import pytest

from ai_company.orchestrator.approval_prompts import (
    TIER_CLASSIFICATION_PROMPT,
    DASHBOARD_SUMMARY_PROMPT,
    TIER_NOTIFICATIONS,
    ESCALATION_TEMPLATES,
    build_tier_classification_prompt,
    build_notification,
    build_escalation,
)
from ai_company.orchestrator.tier_rules import (
    ApprovalTier,
    SENIORITY_AUTO_APPROVE_TIER,
    TOOL_DEFAULT_TIERS,
    classify_tool_action,
    get_tier_config,
    _check_sensitive_path,
    _check_command_sensitivity,
)


# ─── Helpers ────────────────────────────────────────────────────────────────


def _make_request(
    *,
    tool: str = "read",
    args: dict[str, Any] | None = None,
    agent_id: str = "agent-1",
    action_description: str = "Read a file",
    request_id: str = "req-1",
    timestamp: str = "2026-07-19T10:00:00",
    expires_at: str = "2026-07-19T12:00:00",
    timeout_minutes: int = 120,
) -> dict[str, Any]:
    return {
        "tool": tool,
        "args": args or {},
        "agent_id": agent_id,
        "action_description": action_description,
        "request_id": request_id,
        "timestamp": timestamp,
        "expires_at": expires_at,
        "timeout_minutes": timeout_minutes,
    }


# ─── Enum tests ─────────────────────────────────────────────────────────────


class TestApprovalTier:
    def test_enum_values(self) -> None:
        assert int(ApprovalTier.AUTO_APPROVE) == 0
        assert int(ApprovalTier.NOTIFY) == 1
        assert int(ApprovalTier.SINGLE_APPROVER) == 2
        assert int(ApprovalTier.TWO_PERSON) == 3
        assert int(ApprovalTier.CEO_ONLY) == 4

    def test_enum_ordering(self) -> None:
        tiers = list(ApprovalTier)
        assert tiers == [
            ApprovalTier.AUTO_APPROVE,
            ApprovalTier.NOTIFY,
            ApprovalTier.SINGLE_APPROVER,
            ApprovalTier.TWO_PERSON,
            ApprovalTier.CEO_ONLY,
        ]


# ─── Tool default tier tests ────────────────────────────────────────────────


class TestToolDefaultTiers:
    def test_read_is_auto_approve(self) -> None:
        assert TOOL_DEFAULT_TIERS["read"] == ApprovalTier.AUTO_APPROVE

    def test_list_is_auto_approve(self) -> None:
        assert TOOL_DEFAULT_TIERS["list"] == ApprovalTier.AUTO_APPROVE

    def test_grep_is_auto_approve(self) -> None:
        assert TOOL_DEFAULT_TIERS["grep"] == ApprovalTier.AUTO_APPROVE

    def test_write_is_single_approver(self) -> None:
        assert TOOL_DEFAULT_TIERS["write"] == ApprovalTier.SINGLE_APPROVER

    def test_execute_is_single_approver(self) -> None:
        assert TOOL_DEFAULT_TIERS["execute"] == ApprovalTier.SINGLE_APPROVER

    def test_code_interpreter_is_single_approver(self) -> None:
        assert TOOL_DEFAULT_TIERS["code_interpreter"] == ApprovalTier.SINGLE_APPROVER

    def test_delegate_is_notify(self) -> None:
        assert TOOL_DEFAULT_TIERS["delegate"] == ApprovalTier.NOTIFY

    def test_edit_is_single_approver(self) -> None:
        assert TOOL_DEFAULT_TIERS["edit"] == ApprovalTier.SINGLE_APPROVER

    def test_glob_is_auto_approve(self) -> None:
        assert TOOL_DEFAULT_TIERS["glob"] == ApprovalTier.AUTO_APPROVE

    def test_unknown_tool_defaults_to_single_approver(self) -> None:
        result = classify_tool_action("unknown_tool", {})
        assert result == ApprovalTier.SINGLE_APPROVER


# ─── Classification with no escalation ──────────────────────────────────────


class TestClassifyBasic:
    def test_read_classifies_as_auto(self) -> None:
        result = classify_tool_action("read", {"path": "src/main.py"})
        assert result == ApprovalTier.AUTO_APPROVE

    def test_list_classifies_as_auto(self) -> None:
        result = classify_tool_action("list", {"path": "src/"})
        assert result == ApprovalTier.AUTO_APPROVE

    def test_grep_classifies_as_auto(self) -> None:
        result = classify_tool_action("grep", {"pattern": "TODO", "path": "src/"})
        assert result == ApprovalTier.AUTO_APPROVE

    def test_write_basic(self) -> None:
        result = classify_tool_action("write", {"path": "output.txt"})
        assert result == ApprovalTier.SINGLE_APPROVER

    def test_execute_basic(self) -> None:
        result = classify_tool_action("execute", {"command": "pytest tests/"})
        assert result == ApprovalTier.SINGLE_APPROVER

    def test_code_interpreter_basic(self) -> None:
        result = classify_tool_action("code_interpreter", {"code": "print('hello')"})
        assert result == ApprovalTier.SINGLE_APPROVER

    def test_delegate_classifies_as_notify(self) -> None:
        result = classify_tool_action("delegate", {"agent_id": "specialist-1"})
        assert result == ApprovalTier.NOTIFY


# ─── Path-based escalation ──────────────────────────────────────────────────


class TestPathEscalation:
    def test_write_to_secrets_path_escalates_to_ceo(self) -> None:
        result = classify_tool_action("write", {"path": "config/secrets/prod.yaml"})
        assert result == ApprovalTier.CEO_ONLY

    def test_write_to_env_file_escalates_to_ceo(self) -> None:
        result = classify_tool_action("write", {"path": "/etc/.env"})
        assert result == ApprovalTier.CEO_ONLY

    def test_write_to_security_path_escalates_to_ceo(self) -> None:
        result = classify_tool_action("write", {"path": "security/policy.yaml"})
        assert result == ApprovalTier.CEO_ONLY

    def test_write_to_production_path_escalates_to_two_person(self) -> None:
        result = classify_tool_action("write", {"path": "deploy/config.yaml"})
        assert result == ApprovalTier.TWO_PERSON

    def test_write_to_terraform_path_escalates_to_two_person(self) -> None:
        result = classify_tool_action("write", {"path": "terraform/main.tf"})
        assert result == ApprovalTier.TWO_PERSON

    def test_write_to_k8s_path_escalates_to_two_person(self) -> None:
        result = classify_tool_action("write", {"path": "k8s/deployment.yaml"})
        assert result == ApprovalTier.TWO_PERSON

    def test_write_to_dockerfile_escalates_to_two_person(self) -> None:
        result = classify_tool_action("write", {"path": "Dockerfile"})
        assert result == ApprovalTier.TWO_PERSON

    def test_write_to_src_path_is_single_approver(self) -> None:
        result = classify_tool_action("write", {"path": "src/main.py"})
        assert result == ApprovalTier.SINGLE_APPROVER

    def test_write_to_tests_path_is_single_approver(self) -> None:
        result = classify_tool_action("write", {"path": "tests/test_main.py"})
        assert result == ApprovalTier.SINGLE_APPROVER

    def test_write_to_app_path_is_single_approver(self) -> None:
        result = classify_tool_action("write", {"path": "app/routes.py"})
        assert result == ApprovalTier.SINGLE_APPROVER

    def test_write_to_config_path_is_notify(self) -> None:
        result = classify_tool_action("write", {"path": "config/app.yaml"})
        assert result == ApprovalTier.NOTIFY

    def test_write_to_docs_path_is_notify(self) -> None:
        result = classify_tool_action("write", {"path": "docs/readme.md"})
        assert result == ApprovalTier.NOTIFY

    def test_write_to_markdown_file_is_notify(self) -> None:
        result = classify_tool_action("write", {"path": "CHANGELOG.md"})
        assert result == ApprovalTier.NOTIFY

    def test_edit_to_secrets_escalates_to_ceo(self) -> None:
        result = classify_tool_action("edit", {"filePath": "/secrets/api_key.txt"})
        assert result == ApprovalTier.CEO_ONLY

    def test_code_interpreter_on_secret_file_escalates(self) -> None:
        result = classify_tool_action(
            "code_interpreter",
            {"path": "config/secrets/db_password.txt"},
        )
        assert result == ApprovalTier.CEO_ONLY

    def test_read_to_secrets_path_stays_auto(self) -> None:
        """Read access to secrets should still be auto-approved (no write)."""
        result = classify_tool_action("read", {"path": "config/secrets/secret.yaml"})
        assert result == ApprovalTier.AUTO_APPROVE

    def test_path_in_list_arg(self) -> None:
        result = classify_tool_action("write", {"files": ["src/main.py", "tests/test.py"]})
        assert result == ApprovalTier.SINGLE_APPROVER

    def test_path_in_dict_arg(self) -> None:
        result = classify_tool_action("write", {"source": {"path": "deploy/config.yaml"}})
        assert result == ApprovalTier.TWO_PERSON


# ─── Command-based escalation ──────────────────────────────────────────────


class TestCommandEscalation:
    def test_rm_rf_escalates_to_ceo(self) -> None:
        result = classify_tool_action("execute", {"command": "rm -rf /"})
        assert result == ApprovalTier.CEO_ONLY

    def test_drop_table_escalates_to_ceo(self) -> None:
        result = classify_tool_action("execute", {"command": "DROP TABLE users;"})
        assert result == ApprovalTier.CEO_ONLY

    def test_sudo_rm_escalates_to_ceo(self) -> None:
        result = classify_tool_action("execute", {"command": "sudo rm -rf /var/log"})
        assert result == ApprovalTier.CEO_ONLY

    def test_docker_push_escalates_to_two_person(self) -> None:
        result = classify_tool_action("execute", {"command": "docker push myrepo/app:latest"})
        assert result == ApprovalTier.TWO_PERSON

    def test_kubectl_apply_escalates_to_two_person(self) -> None:
        result = classify_tool_action("execute", {"command": "kubectl apply -f deploy.yaml"})
        assert result == ApprovalTier.TWO_PERSON

    def test_terraform_apply_escalates_to_two_person(self) -> None:
        result = classify_tool_action("execute", {"command": "terraform apply -auto-approve"})
        assert result == ApprovalTier.TWO_PERSON

    def test_npm_publish_escalates_to_two_person(self) -> None:
        result = classify_tool_action("execute", {"command": "npm publish"})
        assert result == ApprovalTier.TWO_PERSON

    def test_pytest_does_not_escalate(self) -> None:
        result = classify_tool_action("execute", {"command": "pytest tests/"})
        assert result == ApprovalTier.SINGLE_APPROVER

    def test_ls_command_stays_default(self) -> None:
        result = classify_tool_action("execute", {"command": "ls -la"})
        assert result == ApprovalTier.SINGLE_APPROVER

    def test_chmod_777_escalates_to_ceo(self) -> None:
        result = classify_tool_action("execute", {"command": "chmod 777 /etc/config"})
        assert result == ApprovalTier.CEO_ONLY


# ─── Combined path and command escalation ──────────────────────────────────


class TestCombinedEscalation:
    def test_write_to_production_and_dangerous_command(self) -> None:
        """The highest tier wins."""
        result = classify_tool_action("execute", {"command": "rm -rf /prod/data"})
        assert result == ApprovalTier.CEO_ONLY  # rm -rf wins over /prod

    def test_write_to_secret_path_with_safe_command(self) -> None:
        result = classify_tool_action(
            "execute",
            {"command": "cat config/secrets/api_key.txt"},
        )
        assert result == ApprovalTier.CEO_ONLY  # path escalates

    def test_terraform_destroy_escalates_to_two_person(self) -> None:
        result = classify_tool_action("execute", {"command": "terraform destroy"})
        assert result == ApprovalTier.TWO_PERSON


# ─── Agent seniority de-escalation ──────────────────────────────────────────


class TestSeniorityDeescalation:
    def test_executive_can_auto_approve_write_to_config(self) -> None:
        """Executives can auto-approve config writes (Tier 1)."""
        result = classify_tool_action(
            "write",
            {"path": "config/app.yaml"},
            task_context={"seniority": "executive"},
        )
        assert result == ApprovalTier.NOTIFY

    def test_executive_still_needs_approval_for_code_changes(self) -> None:
        """Executives can auto-approve up to Tier 2; code is Tier 2 so gets notify."""
        result = classify_tool_action(
            "write",
            {"path": "src/main.py"},
            task_context={"seniority": "executive"},
        )
        assert result == ApprovalTier.NOTIFY

    def test_executive_cannot_bypass_production(self) -> None:
        """Executives can only bypass tiers <= 2; production is Tier 3."""
        result = classify_tool_action(
            "write",
            {"path": "deploy/config.yaml"},
            task_context={"seniority": "executive"},
        )
        assert result == ApprovalTier.TWO_PERSON

    def test_executive_cannot_bypass_ceo_tier(self) -> None:
        result = classify_tool_action(
            "write",
            {"path": "config/secrets/api_key.txt"},
            task_context={"seniority": "executive"},
        )
        assert result == ApprovalTier.CEO_ONLY

    def test_junior_cannot_auto_approve_anything(self) -> None:
        """Junior can only auto-approve Tier 0 (read-only).

        With no path pattern matched, a basic write stays at SINGLE_APPROVER.
        """
        result = classify_tool_action(
            "write",
            {"path": "output.txt"},
            task_context={"seniority": "junior"},
        )
        assert result == ApprovalTier.SINGLE_APPROVER  # Not de-escalated

    def test_lead_can_auto_approve_single_approver(self) -> None:
        result = classify_tool_action(
            "write",
            {"path": "output.txt"},
            task_context={"seniority": "lead"},
        )
        assert result == ApprovalTier.NOTIFY

    def test_seniority_unknown_does_not_deescalate(self) -> None:
        result = classify_tool_action("write", {"path": "output.txt"})
        assert result == ApprovalTier.SINGLE_APPROVER


# ─── Task context escalation ────────────────────────────────────────────────


class TestTaskContextEscalation:
    def test_high_risk_escalates_to_two_person_for_code(self) -> None:
        """High-risk tasks escalate Tier 2 to Tier 3."""
        result = classify_tool_action(
            "write",
            {"path": "src/main.py"},
            task_context={"risk_level": "high"},
        )
        assert result == ApprovalTier.TWO_PERSON

    def test_critical_risk_escalates_to_ceo(self) -> None:
        result = classify_tool_action(
            "write",
            {"path": "src/main.py"},
            task_context={"risk_level": "critical"},
        )
        assert result == ApprovalTier.CEO_ONLY

    def test_low_risk_does_not_escalate(self) -> None:
        result = classify_tool_action(
            "write",
            {"path": "src/main.py"},
            task_context={"risk_level": "low"},
        )
        assert result == ApprovalTier.SINGLE_APPROVER


# ─── Internal helpers ────────────────────────────────────────────────────────


class TestCheckSensitivePath:
    def test_empty_args_returns_zero(self) -> None:
        assert _check_sensitive_path({}) == 0

    def test_no_path_returns_zero(self) -> None:
        assert _check_sensitive_path({"pattern": "hello"}) == 0

    def test_secret_path_returns_4(self) -> None:
        assert _check_sensitive_path({"path": "config/secrets/db.yaml"}) == 4

    def test_production_path_returns_3(self) -> None:
        assert _check_sensitive_path({"path": "deploy/config.yaml"}) == 3

    def test_code_path_returns_2(self) -> None:
        assert _check_sensitive_path({"path": "src/main.py"}) == 2

    def test_config_path_returns_1(self) -> None:
        assert _check_sensitive_path({"path": "config/app.yaml"}) == 1

    def test_docs_path_returns_1(self) -> None:
        assert _check_sensitive_path({"path": "docs/readme.md"}) == 1

    def test_highest_tier_wins(self) -> None:
        """If a path matches multiple patterns, return the highest."""
        # "config/secrets/deploy/" matches both secrets (4) and deploy (3)
        assert _check_sensitive_path({"path": "config/secrets/deploy/"}) == 4


class TestCheckCommandSensitivity:
    def test_safe_command_returns_zero(self) -> None:
        assert _check_command_sensitivity("pytest tests/") == 0

    def test_dangerous_rm_returns_4(self) -> None:
        assert _check_command_sensitivity("rm -rf /") == 4

    def test_drop_table_returns_4(self) -> None:
        assert _check_command_sensitivity("DROP TABLE users;") == 4

    def test_docker_push_returns_3(self) -> None:
        assert _check_command_sensitivity("docker push myapp:latest") == 3

    def test_terraform_apply_returns_3(self) -> None:
        assert _check_command_sensitivity("terraform apply") == 3

    def test_destructive_returns_highest(self) -> None:
        """Dangerous commands (4) take priority over production (3)."""
        assert _check_command_sensitivity("sudo rm -rf / && docker push app") == 4


# ─── Tier config ────────────────────────────────────────────────────────────


class TestTierConfig:
    def test_auto_approve_config(self) -> None:
        cfg = get_tier_config(ApprovalTier.AUTO_APPROVE)
        assert cfg["required_approvers"] == 0
        assert cfg["notify"] is False

    def test_notify_config(self) -> None:
        cfg = get_tier_config(ApprovalTier.NOTIFY)
        assert cfg["required_approvers"] == 0
        assert cfg["notify"] is True

    def test_single_approver_config(self) -> None:
        cfg = get_tier_config(ApprovalTier.SINGLE_APPROVER)
        assert cfg["required_approvers"] == 1
        assert cfg["timeout_minutes"] == 240

    def test_two_person_config(self) -> None:
        cfg = get_tier_config(ApprovalTier.TWO_PERSON)
        assert cfg["required_approvers"] == 2
        assert cfg["timeout_minutes"] == 120

    def test_ceo_only_config(self) -> None:
        cfg = get_tier_config(ApprovalTier.CEO_ONLY)
        assert cfg["required_approvers"] == 1
        assert cfg["timeout_minutes"] == 60
        assert "sms" in cfg["notify_channels"]

    def test_invalid_tier_falls_back(self) -> None:
        # Use cast to create a fake invalid ApprovalTier value.
        cfg = get_tier_config(cast(ApprovalTier, 99))
        assert cfg["required_approvers"] == 1


# ─── Build tier classification prompt ──────────────────────────────────────


class TestBuildTierClassificationPrompt:
    def test_includes_tool_name(self) -> None:
        prompt = build_tier_classification_prompt(
            "write", {"path": "src/main.py"}, {"seniority": "mid"},
        )
        assert "write" in prompt
        assert "src/main.py" in prompt
        assert "mid" in prompt
        assert "Tier (0-4):" in prompt

    def test_includes_classification_prompt(self) -> None:
        prompt = build_tier_classification_prompt(
            "read", {"path": "file.txt"}, {"seniority": "junior"},
        )
        # Should contain the classification rules
        assert "Auto-Approve" in prompt
        assert "Tier 0" in prompt or "Tier 1" in prompt

    def test_summarises_long_args(self) -> None:
        long_path = "/very/long/path/" + "a" * 200
        prompt = build_tier_classification_prompt(
            "write",
            {"path": long_path},
            {"seniority": "mid"},
        )
        # Should not contain the full 200-char string, should be truncated
        assert len(prompt) < 3000


# ─── Notification templates ────────────────────────────────────────────────


class TestTierNotifications:
    def test_all_tiers_have_notifications(self) -> None:
        for tier in range(5):
            assert tier in TIER_NOTIFICATIONS, f"Missing notification for tier {tier}"

    def test_tier_0_auto_approve_notification(self) -> None:
        request = _make_request(tool="read", args={"path": "file.txt"})
        msg = build_notification(0, request)
        assert "Auto-Approved" in msg
        assert "read" in msg
        assert "agent-1" in msg

    def test_tier_1_notify_notification(self) -> None:
        request = _make_request(tool="write", args={"path": "docs/readme.md"})
        msg = build_notification(1, request)
        assert "Notification" in msg
        assert "low-risk" in msg
        assert "docs/readme.md" in msg

    def test_tier_2_single_approver_notification(self) -> None:
        request = _make_request(
            tool="write",
            args={"path": "src/main.py"},
            request_id="req-42",
        )
        msg = build_notification(2, request)
        assert "Approval Required" in msg
        assert "Single Approver" in msg
        assert "req-42" in msg
        assert "ai-company approval approve" in msg
        assert "ai-company approval reject" in msg
        assert "120" in msg  # timeout_minutes

    def test_tier_3_two_person_notification(self) -> None:
        request = _make_request(
            tool="execute",
            args={"command": "terraform apply"},
            request_id="req-99",
        )
        msg = build_notification(3, request)
        assert "Two-Person Rule" in msg
        assert "TWO approvers" in msg
        assert "approver 1" in msg
        assert "approver 2" in msg

    def test_tier_4_ceo_notification(self) -> None:
        request = _make_request(
            tool="write",
            args={"path": "config/secrets/api_key.txt"},
            request_id="req-ceo",
        )
        msg = build_notification(4, request)
        assert "CEO Only" in msg
        assert 'by "ceo"' in msg
        assert "req-ceo" in msg

    def test_notification_with_timestamp(self) -> None:
        request = _make_request(timestamp="2026-07-19T15:30:00")
        msg = build_notification(2, request)
        assert "2026-07-19T15:30:00" in msg

    def test_invalid_tier_raises_key_error(self) -> None:
        with pytest.raises(KeyError, match="No notification template"):
            build_notification(99, _make_request())


# ─── Escalation templates ──────────────────────────────────────────────────


class TestEscalationTemplates:
    def test_tier_2_escalation(self) -> None:
        request = _make_request(
            tool="write",
            args={"path": "src/main.py"},
            request_id="req-42",
            action_description="Modify main module",
        )
        msg = build_escalation(2, request, timeout_minutes=240, escalated_to="chief-of-staff")
        assert "Escalation" in msg
        assert "TIMED OUT" in msg
        assert "req-42" in msg
        assert "chief-of-staff" in msg
        assert "240" in msg

    def test_tier_3_escalation(self) -> None:
        request = _make_request(
            tool="execute",
            args={"command": "terraform apply"},
            request_id="req-77",
        )
        msg = build_escalation(3, request, timeout_minutes=120, escalated_to="vp-engineering")
        assert "Two-Person" in msg or "Tier 3" in msg
        assert "vp-engineering" in msg

    def test_tier_4_escalation(self) -> None:
        request = _make_request(
            tool="write",
            args={"path": "config/secrets/prod.yaml"},
            request_id="req-ceo-1",
        )
        msg = build_escalation(4, request, timeout_minutes=60, escalated_to="board")
        assert "CEO" in msg
        assert "req-ceo-1" in msg
        assert "board" in msg
        assert "Board of Directors" in msg

    def test_escalation_default_escalated_to(self) -> None:
        request = _make_request(request_id="req-1")
        msg = build_escalation(2, request, timeout_minutes=30)
        assert "chief-of-staff" in msg

    def test_invalid_tier_raises_key_error(self) -> None:
        with pytest.raises(KeyError, match="No escalation template"):
            build_escalation(99, _make_request(), timeout_minutes=30)

    def test_tier_0_and_1_have_no_escalation(self) -> None:
        assert 0 not in ESCALATION_TEMPLATES
        assert 1 not in ESCALATION_TEMPLATES


# ─── Dashboard summary prompt ──────────────────────────────────────────────


class TestDashboardSummaryPrompt:
    def test_prompt_is_defined(self) -> None:
        assert DASHBOARD_SUMMARY_PROMPT is not None
        assert len(DASHBOARD_SUMMARY_PROMPT) > 100

    def test_prompt_contains_key_sections(self) -> None:
        assert "Approval Dashboard" in DASHBOARD_SUMMARY_PROMPT
        assert "Total pending" in DASHBOARD_SUMMARY_PROMPT
        assert "Urgent Actions" in DASHBOARD_SUMMARY_PROMPT
        assert "Escalated Items" in DASHBOARD_SUMMARY_PROMPT
        assert "Recommendations" in DASHBOARD_SUMMARY_PROMPT

    def test_prompt_contains_sla_guidance(self) -> None:
        assert "SLA" in DASHBOARD_SUMMARY_PROMPT
        assert "at risk" in DASHBOARD_SUMMARY_PROMPT

    def test_prompt_mentions_all_tiers(self) -> None:
        assert "Tier 4" in DASHBOARD_SUMMARY_PROMPT
        assert "Tier 3" in DASHBOARD_SUMMARY_PROMPT
        assert "Tier 2" in DASHBOARD_SUMMARY_PROMPT
        assert "Tier 1" in DASHBOARD_SUMMARY_PROMPT


# ─── Classification prompt constants ────────────────────────────────────────


class TestClassificationPrompt:
    def test_prompt_is_defined(self) -> None:
        assert TIER_CLASSIFICATION_PROMPT is not None
        assert len(TIER_CLASSIFICATION_PROMPT) > 200

    def test_prompt_describes_all_tiers(self) -> None:
        for tier_label in ["Auto-Approve", "Notify", "Single Approver", "Two-Person Rule", "CEO Only"]:
            assert tier_label in TIER_CLASSIFICATION_PROMPT

    def test_prompt_instructs_numeric_response(self) -> None:
        assert "Tier number" in TIER_CLASSIFICATION_PROMPT or "0-4" in TIER_CLASSIFICATION_PROMPT


# ─── Edge cases ────────────────────────────────────────────────────────────


class TestEdgeCases:
    def test_empty_args_classification(self) -> None:
        result = classify_tool_action("write", {})
        assert result == ApprovalTier.SINGLE_APPROVER

    def test_none_args_classification(self) -> None:
        result = classify_tool_action("write", {})  # type: ignore[arg-type]
        assert result == ApprovalTier.SINGLE_APPROVER

    def test_non_string_args_classification(self) -> None:
        result = classify_tool_action("execute", {"command": 12345})
        assert result == ApprovalTier.SINGLE_APPROVER

    def test_seniority_auto_approve_tier_values(self) -> None:
        assert SENIORITY_AUTO_APPROVE_TIER["junior"] == 0
        assert SENIORITY_AUTO_APPROVE_TIER["mid"] == 1
        assert SENIORITY_AUTO_APPROVE_TIER["senior"] == 1
        assert SENIORITY_AUTO_APPROVE_TIER["lead"] == 2
        assert SENIORITY_AUTO_APPROVE_TIER["executive"] == 2
