"""Evaluation runner — executes prompts against test scenarios.

The runner:
1. Loads test cases from the dataset
2. Builds system prompts using the prompt builder
3. Calls the LLM (or a mock for unit tests)
4. Scores outputs using EvalScorer
5. Aggregates results for reporting

Supports both live LLM evaluation and deterministic mock mode for CI.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Protocol

from ai_company.prompts.evals.eval_dataset import (
    EvalTestCase,
    get_test_cases,
    AgentType,
    Difficulty,
)
from ai_company.prompts.evals.eval_scorer import (
    EvalResult,
    EvalScorer,
    compute_aggregate_scores,
)

logger = logging.getLogger(__name__)


class LLMProvider(Protocol):
    """Protocol for LLM providers used in evaluation."""

    def chat(
        self, system_prompt: str, user_prompt: str, model: str | None = None
    ) -> Any:
        """Send a chat request and return a response with .content attribute."""
        ...


@dataclass
class EvalConfig:
    """Configuration for an evaluation run."""

    max_test_cases: int = 100
    timeout_seconds: float = 30.0
    retry_count: int = 1
    model_override: str | None = None
    agent_type_filter: AgentType | None = None
    difficulty_filter: Difficulty | None = None
    tag_filter: list[str] | None = None


@dataclass
class EvalRunResult:
    """Aggregate result of an evaluation run."""

    config: EvalConfig
    test_results: list[EvalResult]
    aggregates: dict[str, float]
    duration_seconds: float
    prompt_versions_used: dict[str, str] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


class EvalRunner:
    """Execute prompt evaluations against test scenarios.

    Usage::

        runner = EvalRunner(llm_provider=my_llm)
        result = runner.run()
        print(f"Average score: {result.aggregates['avg_total']}")
    """

    def __init__(
        self,
        llm_provider: LLMProvider | None = None,
        scorer: EvalScorer | None = None,
        config: EvalConfig | None = None,
    ) -> None:
        self.llm = llm_provider
        self.scorer = scorer or EvalScorer()
        self.config = config or EvalConfig()

    def run(
        self,
        test_cases: list[EvalTestCase] | None = None,
        prompt_builder: Any | None = None,
    ) -> EvalRunResult:
        """Run evaluation on all matching test cases."""
        start_time = time.time()

        # Select test cases
        if test_cases is None:
            test_cases = get_test_cases(
                agent_type=self.config.agent_type_filter,
                difficulty=self.config.difficulty_filter,
                tags=self.config.tag_filter,
            )

        # Apply limit
        test_cases = test_cases[: self.config.max_test_cases]

        if not test_cases:
            return EvalRunResult(
                config=self.config,
                test_results=[],
                aggregates={},
                duration_seconds=0.0,
                errors=["No test cases matched the configured filters"],
            )

        logger.info("Running evaluation on %d test cases", len(test_cases))

        results: list[EvalResult] = []
        errors: list[str] = []

        for tc in test_cases:
            try:
                raw_output = self._execute_single(tc, prompt_builder)
                eval_result = self.scorer.score(tc, raw_output)
                results.append(eval_result)

                logger.debug(
                    "Test %s: score=%.3f", tc.id, eval_result.score.total
                )
            except Exception as exc:
                error_msg = f"Test {tc.id} failed: {exc}"
                errors.append(error_msg)
                logger.warning(error_msg)

        aggregates = compute_aggregate_scores(results)
        duration = time.time() - start_time

        return EvalRunResult(
            config=self.config,
            test_results=results,
            aggregates=aggregates,
            duration_seconds=round(duration, 2),
            errors=errors,
        )

    def run_single(
        self,
        test_case: EvalTestCase,
        prompt_builder: Any | None = None,
    ) -> EvalResult:
        """Run evaluation on a single test case."""
        raw_output = self._execute_single(test_case, prompt_builder)
        return self.scorer.score(test_case, raw_output)

    def _execute_single(
        self,
        test_case: EvalTestCase,
        prompt_builder: Any | None = None,
    ) -> str:
        """Execute a single test case and return raw LLM output."""
        system_prompt = test_case.system_prompt

        # If a prompt builder is provided, use it to generate the system prompt
        if prompt_builder and not system_prompt:
            system_prompt = prompt_builder(test_case.agent_type.value)

        # If no LLM provider, return a mock response for testing
        if self.llm is None:
            return self._mock_response(test_case)

        user_prompt = (
            f"PRIORITY: MEDIUM\n\n"
            f"TASK: {test_case.task_instruction}\n\n"
            "Analyze the task, think through your approach, and respond with "
            "your first set of tool calls."
        )

        start = time.time()
        response = self.llm.chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=self.config.model_override,
        )
        elapsed = (time.time() - start) * 1000

        if elapsed > self.config.timeout_seconds * 1000:
            logger.warning(
                "Test %s took %.0fms (limit: %.0fms)",
                test_case.id,
                elapsed,
                self.config.timeout_seconds * 1000,
            )

        return response.content if hasattr(response, "content") else str(response)

    def _mock_response(self, test_case: EvalTestCase) -> str:
        """Generate a deterministic mock response for CI/testing."""
        # Minimal valid responses per agent type
        tool = "read"
        args = '{"path": "docs/report.md"}'

        if test_case.agent_type == AgentType.EXECUTIVE:
            tool = "delegate"
            args = '{"receiver": "lead-backend", "instruction": "Review code"}'
        elif test_case.agent_type == AgentType.SPECIALIST:
            tool = "read"
            args = '{"path": "src/main.py"}'
        elif test_case.agent_type == AgentType.BOARD:
            tool = "read"
            args = '{"path": "docs/strategy.md"}'
        elif test_case.agent_type == AgentType.DEPARTMENT:
            tool = "delegate"
            args = '{"receiver": "engineer-1", "instruction": "Implement feature"}'

        return (
            '{"thought": "I need to analyze the task and take appropriate action. '
            f'{test_case.task_instruction[:100]}'
            ' Let me start by reviewing available information.", '
            f'"plan": [{{"tool": "{tool}", "args": {args}}}], '
            '"result": "Task initiated — reviewing information and delegating as needed.", '
            '"done": false}'
        )
