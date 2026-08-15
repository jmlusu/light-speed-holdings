"""Tests for the prompt engineering subsystem.

Covers:
- Prompt registry (versioning, A/B test, rollback)
- Prompt templates (component rendering)
- Optimized prompt templates (executor/prompts.py)
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Prompt Registry tests
# ---------------------------------------------------------------------------


class TestPromptRegistry:
    """Tests for PromptRegistry versioning system."""

    def test_register_creates_version(self, tmp_path: Path) -> None:
        from ai_company.prompts.registry import PromptRegistry

        registry = PromptRegistry(storage_dir=str(tmp_path))
        v1 = registry.register("test.prompt", "Hello world")

        assert v1.version == 1
        assert v1.content == "Hello world"
        assert v1.prompt_id == "test.prompt"
        assert v1.hash  # non-empty

    def test_register_deduplicates(self, tmp_path: Path) -> None:
        from ai_company.prompts.registry import PromptRegistry

        registry = PromptRegistry(storage_dir=str(tmp_path))
        v1 = registry.register("test.prompt", "Hello world")
        v2 = registry.register("test.prompt", "Hello world")

        assert v1.version == v2.version
        assert v1.hash == v2.hash

    def test_register_new_version(self, tmp_path: Path) -> None:
        from ai_company.prompts.registry import PromptRegistry

        registry = PromptRegistry(storage_dir=str(tmp_path))
        v1 = registry.register("test.prompt", "v1 content")
        v2 = registry.register("test.prompt", "v2 content")

        assert v2.version == 2
        assert v1.content != v2.content

    def test_get_returns_latest(self, tmp_path: Path) -> None:
        from ai_company.prompts.registry import PromptRegistry

        registry = PromptRegistry(storage_dir=str(tmp_path))
        registry.register("test.prompt", "v1")
        registry.register("test.prompt", "v2")
        registry.register("test.prompt", "v3")

        latest = registry.get("test.prompt")
        assert latest is not None
        assert latest.version == 3
        assert latest.content == "v3"

    def test_get_specific_version(self, tmp_path: Path) -> None:
        from ai_company.prompts.registry import PromptRegistry

        registry = PromptRegistry(storage_dir=str(tmp_path))
        registry.register("test.prompt", "v1 content")
        registry.register("test.prompt", "v2 content")

        v1 = registry.get("test.prompt", version=1)
        assert v1 is not None
        assert v1.content == "v1 content"

    def test_get_nonexistent(self, tmp_path: Path) -> None:
        from ai_company.prompts.registry import PromptRegistry

        registry = PromptRegistry(storage_dir=str(tmp_path))
        result = registry.get("nonexistent.prompt")
        assert result is None

    def test_rollback(self, tmp_path: Path) -> None:
        from ai_company.prompts.registry import PromptRegistry

        registry = PromptRegistry(storage_dir=str(tmp_path))
        registry.register("test.prompt", "v1")
        registry.register("test.prompt", "v2")
        registry.register("test.prompt", "v3")

        rolled = registry.rollback("test.prompt", target_version=1)
        assert rolled is not None
        assert rolled.version == 1

        # Latest should now be v1 (v2, v3 deactivated)
        latest = registry.get_active_version("test.prompt")
        assert latest is not None
        assert latest.version == 1

    def test_list_prompts(self, tmp_path: Path) -> None:
        from ai_company.prompts.registry import PromptRegistry

        registry = PromptRegistry(storage_dir=str(tmp_path))
        registry.register("prompt.a", "content a")
        registry.register("prompt.b", "content b")

        prompts = registry.list_prompts()
        assert "prompt.a" in prompts
        assert "prompt.b" in prompts

    def test_ab_test(self, tmp_path: Path) -> None:
        from ai_company.prompts.registry import PromptRegistry

        registry = PromptRegistry(storage_dir=str(tmp_path))
        registry.register("test.prompt", "variant A")
        registry.register("test.prompt", "variant B")

        registry.start_ab_test("test.prompt", variant_a=1, variant_b=2)

        # get() should randomly pick a variant
        result = registry.get("test.prompt")
        assert result is not None
        assert result.version in (1, 2)

    def test_stop_ab_test(self, tmp_path: Path) -> None:
        from ai_company.prompts.registry import PromptRegistry

        registry = PromptRegistry(storage_dir=str(tmp_path))
        registry.register("test.prompt", "v1")
        registry.register("test.prompt", "v2")

        registry.start_ab_test("test.prompt", variant_a=1, variant_b=2)
        registry.stop_ab_test("test.prompt")

        # After stopping, get() returns latest (v2)
        result = registry.get("test.prompt")
        assert result is not None
        assert result.version == 2

    def test_export_import(self, tmp_path: Path) -> None:
        from ai_company.prompts.registry import PromptRegistry

        registry = PromptRegistry(storage_dir=str(tmp_path))
        registry.register("prompt.x", "content x")
        registry.register("prompt.y", "content y")

        exported = registry.export_all()
        assert "prompt.x" in exported
        assert "prompt.y" in exported

        # Import into a new registry
        registry2 = PromptRegistry(storage_dir=str(tmp_path / "import"))
        count = registry2.import_from_dict(exported)
        assert count == 2


# ---------------------------------------------------------------------------
# Prompt Templates tests
# ---------------------------------------------------------------------------


class TestPromptTemplates:
    """Tests for prompt template components."""

    def test_role_template_renders(self) -> None:
        from ai_company.prompts.templates import build_role_prompt

        result = build_role_prompt(
            role="senior AI executive",
            company="Light Speed Holdings",
            persona="strategic decision-maker",
            delegate=True,
        )
        assert "senior AI executive" in result
        assert "Light Speed Holdings" in result
        assert "Delegate" in result

    def test_role_template_no_delegate(self) -> None:
        from ai_company.prompts.templates import build_role_prompt

        result = build_role_prompt(
            role="board member",
            company="Light Speed Holdings",
            persona="governance expert",
            delegate=False,
        )
        assert "board member" in result
        assert "Delegate" not in result

    def test_format_template_structure(self) -> None:
        from ai_company.prompts.templates import FORMAT_TEMPLATE

        result = FORMAT_TEMPLATE.format(
            thought_placeholder="My reasoning...",
            tool_example="read",
            tool_arg="path",
            tool_arg_value="src/main.py",
            result_placeholder="What was accomplished",
        )
        assert '"thought"' in result
        assert '"plan"' in result
        assert '"done"' in result
        assert "My reasoning..." in result

    def test_error_handling_template(self) -> None:
        from ai_company.prompts.templates import ERROR_HANDLING_TEMPLATE

        assert "Error Recovery" in ERROR_HANDLING_TEMPLATE
        assert "diagnose" in ERROR_HANDLING_TEMPLATE.lower()

    def test_escalation_template(self) -> None:
        from ai_company.prompts.templates import ESCALATION_TEMPLATE

        assert "Escalation" in ESCALATION_TEMPLATE
        assert "escalate" in ESCALATION_TEMPLATE.lower()


# ---------------------------------------------------------------------------
# Prompt Optimized Prompts tests
# ---------------------------------------------------------------------------


class TestOptimizedPrompts:
    """Tests for the optimized prompt templates in executor/prompts.py."""

    def test_role_prefixes_all_types(self) -> None:
        from ai_company.executor.prompts import ROLE_PREFIXES

        for agent_type in ["Executive", "Specialist", "Board", "Department"]:
            prefix = ROLE_PREFIXES[agent_type]
            assert "Light Speed Holdings" in prefix
            assert "BEHAVIORAL RULES" in prefix
            assert len(prefix) > 100  # substantive content

    def test_tool_instructions_all_types(self) -> None:
        from ai_company.executor.prompts import TOOL_INSTRUCTIONS

        for agent_type in ["Executive", "Specialist", "Board", "Department"]:
            instructions = TOOL_INSTRUCTIONS[agent_type]
            assert "ERROR RECOVERY" in instructions
            assert (
                "WORKFLOW" in instructions
                or "DELEGATION PATTERN" in instructions
                or "COORDINATION PATTERN" in instructions
            )

    def test_response_formats_all_types(self) -> None:
        from ai_company.executor.prompts import RESPONSE_FORMATS

        for agent_type in ["Executive", "Specialist", "Board", "Department"]:
            fmt = RESPONSE_FORMATS[agent_type]
            assert "thought" in fmt
            assert "plan" in fmt
            assert "result" in fmt
            assert "done" in fmt
            assert "RULES" in fmt

    def test_build_system_prompt_typed(self) -> None:
        from ai_company.executor.context import AgentContext
        from ai_company.executor.prompts import build_system_prompt_typed

        agent = AgentContext(
            name="test-exec",
            role="Test Executive",
            type="Executive",
            mission="Test mission",
            responsibilities=["Do things"],
            tools=["read", "delegate"],
        )

        prompt = build_system_prompt_typed(agent)
        assert "test-exec" in prompt
        assert "senior AI executive" in prompt  # from ROLE_PREFIXES["Executive"]
        assert "Test mission" in prompt
        assert "Do things" in prompt
        assert "Error Recovery" in prompt
        assert "Escalation Rules" in prompt

    def test_build_user_prompt_typed(self) -> None:
        from ai_company.executor.prompts import build_user_prompt_typed

        prompt = build_user_prompt_typed("Do something important", priority="high")
        assert "PRIORITY: HIGH" in prompt
        assert "Do something important" in prompt

    def test_build_iteration_feedback_with_errors(self) -> None:
        from ai_company.executor.prompts import build_iteration_feedback

        step_results = [
            {
                "step": 0,
                "tool": "read",
                "status": "error",
                "error": "File not found: src/missing.py",
            },
            {"step": 1, "tool": "write", "status": "ok", "path": "output.txt"},
        ]

        feedback = build_iteration_feedback(step_results, iteration=1, max_iterations=5)
        assert "File not found" in feedback
        assert "Recovery" in feedback
        assert "Remaining budget" in feedback

    def test_build_iteration_feedback_denied(self) -> None:
        from ai_company.executor.prompts import build_iteration_feedback

        step_results = [
            {"step": 0, "tool": "execute", "status": "denied", "error": "HITL denied"},
        ]

        feedback = build_iteration_feedback(step_results, iteration=2, max_iterations=5)
        assert "denied" in feedback
        assert "IMPORTANT" in feedback
