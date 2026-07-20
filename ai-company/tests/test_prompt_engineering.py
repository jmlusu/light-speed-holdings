"""Tests for the prompt engineering subsystem.

Covers:
- Prompt registry (versioning, A/B test, rollback)
- Prompt templates (component rendering)
- Evaluation dataset (test case filtering)
- Evaluation scoring (format, tools, reasoning, constraints)
- Evaluation runner (mock mode)
- Evaluation report (markdown, JSON, console)
- LLM-as-Judge (heuristic scoring)
- Prompt analytics (recording, trends, insights)
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from typing import Any

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
# Evaluation Dataset tests
# ---------------------------------------------------------------------------


class TestEvalDataset:
    """Tests for evaluation test case dataset."""

    def test_all_test_cases_loaded(self) -> None:
        from ai_company.prompts.evals.eval_dataset import ALL_TEST_CASES

        assert len(ALL_TEST_CASES) >= 10

    def test_filter_by_agent_type(self) -> None:
        from ai_company.prompts.evals.eval_dataset import (
            AgentType,
            get_test_cases,
        )

        exec_cases = get_test_cases(agent_type=AgentType.EXECUTIVE)
        assert len(exec_cases) >= 3
        for tc in exec_cases:
            assert tc.agent_type == AgentType.EXECUTIVE

    def test_filter_by_difficulty(self) -> None:
        from ai_company.prompts.evals.eval_dataset import (
            Difficulty,
            get_test_cases,
        )

        easy_cases = get_test_cases(difficulty=Difficulty.EASY)
        assert len(easy_cases) >= 3
        for tc in easy_cases:
            assert tc.difficulty == Difficulty.EASY

    def test_filter_by_tags(self) -> None:
        from ai_company.prompts.evals.eval_dataset import get_test_cases

        delegation_cases = get_test_cases(tags=["delegation"])
        assert len(delegation_cases) >= 1

    def test_combined_filter(self) -> None:
        from ai_company.prompts.evals.eval_dataset import (
            AgentType,
            Difficulty,
            get_test_cases,
        )

        result = get_test_cases(
            agent_type=AgentType.SPECIALIST, difficulty=Difficulty.EASY
        )
        assert len(result) >= 1
        for tc in result:
            assert tc.agent_type == AgentType.SPECIALIST
            assert tc.difficulty == Difficulty.EASY


# ---------------------------------------------------------------------------
# Evaluation Scorer tests
# ---------------------------------------------------------------------------


class TestEvalScorer:
    """Tests for evaluation scoring engine."""

    def _make_test_case(self) -> Any:
        from ai_company.prompts.evals.eval_dataset import (
            AgentType,
            Difficulty,
            EvalTestCase,
            ExpectedFormat,
        )

        return EvalTestCase(
            id="test-001",
            name="Basic test",
            agent_type=AgentType.EXECUTIVE,
            difficulty=Difficulty.EASY,
            task_instruction="Do something",
            system_prompt="You are a test agent.",
            expected=ExpectedFormat(
                must_contain_json=True,
                plan_must_use_tools=["delegate"],
            ),
        )

    def test_score_valid_json(self) -> None:
        from ai_company.prompts.evals.eval_scorer import EvalScorer

        scorer = EvalScorer()
        tc = self._make_test_case()

        output = json.dumps({
            "thought": "I need to delegate this task to the specialist because it requires expertise.",
            "plan": [{"tool": "delegate", "args": {"receiver": "lead-backend", "instruction": "Do the thing"}}],
            "result": "Delegated task to lead-backend. Waiting for completion.",
            "done": False,
        })

        result = scorer.score(tc, output)
        assert result.score.total > 0.5
        assert result.parsed_output is not None

    def test_score_invalid_json(self) -> None:
        from ai_company.prompts.evals.eval_scorer import EvalScorer

        scorer = EvalScorer()
        tc = self._make_test_case()

        result = scorer.score(tc, "This is not JSON at all.")
        assert result.score.format_compliance == 0.0
        assert result.score.total < 0.3

    def test_score_missing_fields(self) -> None:
        from ai_company.prompts.evals.eval_scorer import EvalScorer

        scorer = EvalScorer()
        tc = self._make_test_case()

        output = json.dumps({"thought": "I think about things"})
        result = scorer.score(tc, output)
        # Missing plan, result, done — should penalize format
        assert result.score.format_compliance < 0.8

    def test_score_empty_plan(self) -> None:
        from ai_company.prompts.evals.eval_scorer import EvalScorer

        scorer = EvalScorer()
        tc = self._make_test_case()

        output = json.dumps({
            "thought": "No tools needed for this.",
            "plan": [],
            "result": "Task complete without tools.",
            "done": True,
        })

        result = scorer.score(tc, output)
        # Tool score should be lower since delegate was expected
        assert result.score.tool_usage < 1.0

    def test_score_batch(self) -> None:
        from ai_company.prompts.evals.eval_scorer import EvalScorer

        scorer = EvalScorer()
        tc = self._make_test_case()

        outputs = {
            "test-001": json.dumps({
                "thought": "Delegating",
                "plan": [{"tool": "delegate", "args": {"receiver": "x", "instruction": "y"}}],
                "result": "Done",
                "done": True,
            }),
        }

        results = scorer.score_batch([tc], outputs)
        assert len(results) == 1

    def test_aggregate_scores(self) -> None:
        from ai_company.prompts.evals.eval_scorer import (
            EvalResult,
            ScoreBreakdown,
            compute_aggregate_scores,
        )

        # Create mock results
        r1 = EvalResult(
            test_case_id="t1",
            raw_output="{}",
            parsed_output={},
            score=ScoreBreakdown(
                format_compliance=0.8,
                tool_usage=0.7,
                reasoning_quality=0.6,
                result_quality=0.9,
                constraint_adherence=1.0,
            ),
        )
        r1.score.compute_total()

        r2 = EvalResult(
            test_case_id="t2",
            raw_output="{}",
            parsed_output={},
            score=ScoreBreakdown(
                format_compliance=0.6,
                tool_usage=0.8,
                reasoning_quality=0.7,
                result_quality=0.8,
                constraint_adherence=0.9,
            ),
        )
        r2.score.compute_total()

        agg = compute_aggregate_scores([r1, r2])
        assert agg["count"] == 2
        assert agg["avg_total"] > 0


# ---------------------------------------------------------------------------
# Evaluation Runner tests
# ---------------------------------------------------------------------------


class TestEvalRunner:
    """Tests for evaluation runner in mock mode."""

    def test_runner_mock_mode(self) -> None:
        from ai_company.prompts.evals.eval_dataset import (
            AgentType,
        )
        from ai_company.prompts.evals.eval_runner import EvalConfig, EvalRunner

        runner = EvalRunner(
            config=EvalConfig(
                agent_type_filter=AgentType.EXECUTIVE,
                max_test_cases=2,
            )
        )
        result = runner.run()

        assert len(result.test_results) >= 1
        assert result.aggregates["count"] >= 1
        assert result.duration_seconds >= 0

    def test_runner_single_test(self) -> None:
        from ai_company.prompts.evals.eval_dataset import (
            AgentType,
            Difficulty,
            EvalTestCase,
            ExpectedFormat,
        )
        from ai_company.prompts.evals.eval_runner import EvalRunner

        tc = EvalTestCase(
            id="single-001",
            name="Single test",
            agent_type=AgentType.SPECIALIST,
            difficulty=Difficulty.EASY,
            task_instruction="Read a file",
            system_prompt="You are a specialist.",
            expected=ExpectedFormat(must_contain_json=True),
        )

        runner = EvalRunner()
        result = runner.run_single(tc)
        assert result.test_case_id == "single-001"
        assert result.score.total >= 0

    def test_runner_empty_dataset(self) -> None:
        from ai_company.prompts.evals.eval_runner import EvalConfig, EvalRunner

        runner = EvalRunner(
            config=EvalConfig(agent_type_filter=None, max_test_cases=0)
        )
        result = runner.run(test_cases=[])
        assert len(result.test_results) == 0


# ---------------------------------------------------------------------------
# Evaluation Report tests
# ---------------------------------------------------------------------------


class TestEvalReport:
    """Tests for evaluation report generation."""

    def test_markdown_report(self, tmp_path: Path) -> None:
        from ai_company.prompts.evals.eval_report import EvalReport
        from ai_company.prompts.evals.eval_runner import EvalConfig, EvalRunResult

        run_result = EvalRunResult(
            config=EvalConfig(),
            test_results=[],
            aggregates={"count": 0, "avg_total": 0.0},
            duration_seconds=1.0,
        )

        report = EvalReport(run_result)
        output = report.to_markdown(str(tmp_path / "report.md"))

        assert "Prompt Evaluation Report" in output
        assert (tmp_path / "report.md").exists()

    def test_json_report(self, tmp_path: Path) -> None:
        from ai_company.prompts.evals.eval_report import EvalReport
        from ai_company.prompts.evals.eval_runner import EvalConfig, EvalRunResult

        run_result = EvalRunResult(
            config=EvalConfig(),
            test_results=[],
            aggregates={"count": 0},
            duration_seconds=0.5,
        )

        report = EvalReport(run_result)
        output = report.to_json(str(tmp_path / "report.json"))

        data = json.loads(output)
        assert "timestamp" in data
        assert (tmp_path / "report.json").exists()

    def test_console_report(self) -> None:
        from ai_company.prompts.evals.eval_report import EvalReport
        from ai_company.prompts.evals.eval_runner import EvalConfig, EvalRunResult

        run_result = EvalRunResult(
            config=EvalConfig(),
            test_results=[],
            aggregates={"count": 5, "avg_total": 0.75, "min_total": 0.5, "max_total": 0.9},
            duration_seconds=2.0,
        )

        report = EvalReport(run_result)
        output = report.to_console()

        assert "PROMPT EVALUATION SUMMARY" in output
        assert "5" in output


# ---------------------------------------------------------------------------
# LLM Judge tests
# ---------------------------------------------------------------------------


class TestLLMJudge:
    """Tests for LLM-as-Judge evaluator."""

    def test_heuristic_scoring(self) -> None:
        from ai_company.prompts.evals.judge import LLMJudge

        judge = LLMJudge(llm_provider=None)

        output = json.dumps({
            "thought": "I need to analyze this task carefully and provide a comprehensive solution.",
            "plan": [{"tool": "read", "args": {"path": "src/main.py"}}],
            "result": "Completed the task. Read main.py and identified 3 issues to fix.",
            "done": False,
        })

        result = judge.evaluate(
            system_prompt="You are a specialist.",
            task_instruction="Read and analyze main.py",
            agent_output=output,
        )

        assert result.scores.format_score >= 4
        assert result.scores.overall >= 3
        assert result.judge_model == "heuristic"

    def test_heuristic_invalid_json(self) -> None:
        from ai_company.prompts.evals.judge import LLMJudge

        judge = LLMJudge(llm_provider=None)

        result = judge.evaluate(
            system_prompt="You are a specialist.",
            task_instruction="Do something",
            agent_output="This is not JSON at all.",
        )

        assert result.scores.format_score == 1
        assert len(result.scores.issues) > 0

    def test_aggregate_judge_results(self) -> None:
        from ai_company.prompts.evals.judge import (
            JudgeResult,
            JudgeScores,
            aggregate_judge_results,
        )

        r1 = JudgeResult(
            test_case_id="t1",
            scores=JudgeScores(
                accuracy=4, helpfulness=5, safety=5, format_score=4, clarity=4, overall=4
            ),
        )
        r2 = JudgeResult(
            test_case_id="t2",
            scores=JudgeScores(
                accuracy=3, helpfulness=4, safety=5, format_score=5, clarity=3, overall=4
            ),
        )

        agg = aggregate_judge_results([r1, r2])
        assert agg["count"] == 2
        assert agg["avg_accuracy"] == 3.5
        assert agg["avg_safety"] == 5.0


# ---------------------------------------------------------------------------
# Prompt Analytics tests
# ---------------------------------------------------------------------------


class TestPromptAnalytics:
    """Tests for prompt analytics and trend tracking."""

    def test_record_and_retrieve(self, tmp_path: Path) -> None:
        from ai_company.prompts.analytics import PromptAnalytics, PromptMetric

        analytics = PromptAnalytics(storage_dir=str(tmp_path))

        analytics.record(PromptMetric(
            prompt_id="test.prompt",
            version=1,
            avg_score=0.8,
            format_score=0.9,
            tool_score=0.7,
        ))

        metrics = analytics.get_metrics(prompt_id="test.prompt")
        assert len(metrics) == 1
        assert metrics[0].avg_score == 0.8

    def test_get_trends(self, tmp_path: Path) -> None:
        from ai_company.prompts.analytics import PromptAnalytics, PromptMetric

        analytics = PromptAnalytics(storage_dir=str(tmp_path))

        # Record metrics for two versions
        for i in range(3):
            analytics.record(PromptMetric(
                prompt_id="test.prompt",
                version=1,
                avg_score=0.7 + i * 0.01,
            ))
        for i in range(3):
            analytics.record(PromptMetric(
                prompt_id="test.prompt",
                version=2,
                avg_score=0.8 + i * 0.01,
            ))

        trends = analytics.get_trends("test.prompt")
        assert trends["data_points"] == 6
        assert trends["latest_version"] == 2
        assert trends["trend_direction"] == "improving"

    def test_get_insights_degradation(self, tmp_path: Path) -> None:
        from ai_company.prompts.analytics import PromptAnalytics, PromptMetric

        analytics = PromptAnalytics(storage_dir=str(tmp_path))

        # Record improving v1 then degrading v2
        for i in range(5):
            analytics.record(PromptMetric(
                prompt_id="test.prompt",
                version=1,
                avg_score=0.9,
            ))
        for i in range(5):
            analytics.record(PromptMetric(
                prompt_id="test.prompt",
                version=2,
                avg_score=0.5,
            ))

        insights = analytics.get_insights("test.prompt")
        degradation = [i for i in insights if i.insight_type == "degradation"]
        assert len(degradation) >= 1

    def test_compare_versions(self, tmp_path: Path) -> None:
        from ai_company.prompts.analytics import PromptAnalytics, PromptMetric

        analytics = PromptAnalytics(storage_dir=str(tmp_path))

        for _ in range(5):
            analytics.record(PromptMetric(prompt_id="p", version=1, avg_score=0.6))
            analytics.record(PromptMetric(prompt_id="p", version=2, avg_score=0.8))

        comparison = analytics.compare_versions("p", 1, 2)
        assert comparison["winner"] == 2

    def test_filter_by_time(self, tmp_path: Path) -> None:
        from ai_company.prompts.analytics import PromptAnalytics, PromptMetric

        analytics = PromptAnalytics(storage_dir=str(tmp_path))

        # Record old metric
        old = PromptMetric(prompt_id="p", version=1, avg_score=0.5)
        old.timestamp = time.time() - 86400 * 10  # 10 days ago
        analytics.record(old)

        # Record recent metric
        analytics.record(PromptMetric(prompt_id="p", version=1, avg_score=0.8))

        recent = analytics.get_metrics(prompt_id="p", since=time.time() - 3600)
        assert len(recent) == 1
        assert recent[0].avg_score == 0.8


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
            assert "WORKFLOW" in instructions or "DELEGATION PATTERN" in instructions or "COORDINATION PATTERN" in instructions

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
        from ai_company.executor.prompts import build_system_prompt_typed
        from ai_company.executor.context import AgentContext

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
            {"step": 0, "tool": "read", "status": "error", "error": "File not found: src/missing.py"},
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
