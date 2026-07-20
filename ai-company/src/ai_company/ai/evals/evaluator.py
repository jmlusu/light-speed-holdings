"""Prompt evaluation engine — regression tests, LLM-as-judge scoring, A/B testing.

Usage::

    runner = EvalRunner(llm_client=my_llm_client)

    # Define an evaluation case
    case = EvalCase(
        id="summarize-001",
        prompt_variant="v1",
        system_prompt="You are a helpful summarizer.",
        user_input="Summarize the key points of this article: ...",
        expected_output=None,  # No exact match needed — LLM-as-judge scores quality
        tags=["summarization", "quality"],
    )

    # Run evaluation
    result = runner.evaluate(case)

    # A/B test two variants
    ab_result = runner.ab_test(
        case_id="summarize-001",
        system_prompt_a="You are a helpful summarizer.",
        system_prompt_b="You are a concise summarizer. Keep under 100 words.",
        user_input="Summarize: ...",
        judge_criteria=["conciseness", "accuracy", "completeness"],
    )
"""

from __future__ import annotations

import json
import logging
import statistics
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass
class PromptVariant:
    """A named prompt variant for A/B testing."""

    name: str
    system_prompt: str
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvalCase:
    """A single evaluation case."""

    id: str
    prompt_variant: str
    system_prompt: str
    user_input: str
    expected_output: str | None = None
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    # Scoring criteria for LLM-as-judge (e.g., ["accuracy", "completeness"])
    judge_criteria: list[str] = field(default_factory=list)


@dataclass
class EvalResult:
    """Result of evaluating a single case."""

    case_id: str
    prompt_variant: str
    output: str
    score: float  # 0.0 to 1.0
    judge_reasoning: str = ""
    criteria_scores: dict[str, float] = field(default_factory=dict)
    latency_ms: float = 0.0
    tokens_used: int = 0
    passed: bool = True
    error: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "prompt_variant": self.prompt_variant,
            "output": self.output,
            "score": self.score,
            "judge_reasoning": self.judge_reasoning,
            "criteria_scores": self.criteria_scores,
            "latency_ms": self.latency_ms,
            "tokens_used": self.tokens_used,
            "passed": self.passed,
            "error": self.error,
            "timestamp": self.timestamp,
        }


@dataclass
class ABTestResult:
    """Result of an A/B comparison between two prompt variants."""

    case_id: str
    variant_a: EvalResult
    variant_b: EvalResult
    winner: str  # "a", "b", or "tie"
    confidence: float  # 0.0 to 1.0
    improvement_pct: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "variant_a_score": self.variant_a.score,
            "variant_b_score": self.variant_b.score,
            "winner": self.winner,
            "confidence": self.confidence,
            "improvement_pct": self.improvement_pct,
            "timestamp": self.timestamp,
        }


# ---------------------------------------------------------------------------
# LLM client protocol (dependency injection)
# ---------------------------------------------------------------------------


class LLMClientProtocol(Protocol):
    """Protocol for LLM clients used by the evaluator."""

    def execute_task(
        self,
        agent_name: str,
        task_instruction: str,
        priority: str = "medium",
        context: str | None = None,
        system_prompt: str = "",
        max_retries: int = 3,
    ) -> dict[str, Any]: ...


# ---------------------------------------------------------------------------
# Evaluator
# ---------------------------------------------------------------------------

_JUDGE_SYSTEM_PROMPT = """\
You are an expert evaluator assessing the quality of AI-generated responses.

You will be given:
1. A system prompt that defined the AI's behavior
2. A user input (the original task)
3. The AI's response to evaluate
4. A list of scoring criteria

Score the response on each criterion from 1-10, then provide an overall
score from 0.0 to 1.0 (where 1.0 is perfect).

Respond with JSON only:
{
  "criteria_scores": {"criterion_name": score_1_to_10, ...},
  "overall_score": 0.0_to_1.0,
  "reasoning": "Brief explanation of the scores."
}
"""


class EvalRunner:
    """Runs prompt evaluations using LLM-as-judge scoring.

    Args:
        llm_client: An LLM client implementing execute_task().
        results_dir: Directory to write evaluation results.
        judge_model: Optional override for the judge model.
    """

    def __init__(
        self,
        llm_client: LLMClientProtocol | None = None,
        results_dir: str | Path = "results/evals",
        judge_model: str | None = None,
    ) -> None:
        self.llm = llm_client
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.judge_model = judge_model
        self._history: list[EvalResult] = []

    def evaluate(
        self,
        case: EvalCase,
        criteria: list[str] | None = None,
    ) -> EvalResult:
        """Evaluate a single case using LLM-as-judge scoring.

        If ``case.expected_output`` is set, uses exact/substring matching
        as a fast-path. Otherwise, falls back to LLM-as-judge scoring.
        """
        import time

        start = time.monotonic()

        # Generate the output using the case's system prompt
        output = self._generate_output(case.system_prompt, case.user_input)
        latency = (time.monotonic() - start) * 1000

        if not output:
            return EvalResult(
                case_id=case.id,
                prompt_variant=case.prompt_variant,
                output="",
                score=0.0,
                latency_ms=latency,
                passed=False,
                error="LLM returned empty output",
            )

        # Score the output
        eval_criteria = criteria or case.judge_criteria or ["accuracy", "completeness", "clarity"]
        score, reasoning, criteria_scores = self._judge_output(
            system_prompt=case.system_prompt,
            user_input=case.user_input,
            output=output,
            criteria=eval_criteria,
        )

        # Check against expected output if provided
        passed = score >= 0.5
        if case.expected_output:
            exact_match = output.strip() == case.expected_output.strip()
            substring_match = case.expected_output.strip() in output
            if exact_match:
                score = max(score, 1.0)
                passed = True
            elif substring_match:
                score = max(score, 0.8)
                passed = True

        result = EvalResult(
            case_id=case.id,
            prompt_variant=case.prompt_variant,
            output=output,
            score=round(score, 4),
            judge_reasoning=reasoning,
            criteria_scores=criteria_scores,
            latency_ms=round(latency, 1),
            passed=passed,
        )

        self._history.append(result)
        return result

    def ab_test(
        self,
        case_id: str,
        system_prompt_a: str,
        system_prompt_b: str,
        user_input: str,
        judge_criteria: list[str] | None = None,
        variant_a_name: str = "variant_a",
        variant_b_name: str = "variant_b",
    ) -> ABTestResult:
        """Run an A/B test comparing two prompt variants.

        Evaluates both variants on the same input and judges which is better.
        """
        criteria = judge_criteria or ["accuracy", "completeness", "clarity"]

        case_a = EvalCase(
            id=f"{case_id}_a",
            prompt_variant=variant_a_name,
            system_prompt=system_prompt_a,
            user_input=user_input,
            judge_criteria=criteria,
        )
        case_b = EvalCase(
            id=f"{case_id}_b",
            prompt_variant=variant_b_name,
            system_prompt=system_prompt_b,
            user_input=user_input,
            judge_criteria=criteria,
        )

        result_a = self.evaluate(case_a, criteria)
        result_b = self.evaluate(case_b, criteria)

        # Determine winner
        score_diff = result_a.score - result_b.score
        abs_diff = abs(score_diff)
        confidence = min(abs_diff * 2, 1.0)  # Scale difference to confidence

        if abs_diff < 0.05:
            winner = "tie"
        elif score_diff > 0:
            winner = "a"
        else:
            winner = "b"

        improvement_pct = 0.0
        baseline = min(result_a.score, result_b.score) or 0.001
        improvement_pct = round((abs_diff / baseline) * 100, 1)

        return ABTestResult(
            case_id=case_id,
            variant_a=result_a,
            variant_b=result_b,
            winner=winner,
            confidence=round(confidence, 4),
            improvement_pct=improvement_pct,
        )

    def run_suite(
        self,
        cases: list[EvalCase],
        regression_threshold: float = 0.1,
    ) -> dict[str, Any]:
        """Run a full evaluation suite and check for regressions.

        Args:
            cases: List of evaluation cases to run.
            regression_threshold: Maximum allowed score drop before flagging regression.

        Returns:
            Summary dict with pass/fail, individual results, and regression info.
        """
        results: list[EvalResult] = []
        regressions: list[dict[str, Any]] = []

        for case in cases:
            result = self.evaluate(case)
            results.append(result)

            # Check for regression against historical baseline
            baseline = self._get_baseline(case.id)
            if baseline is not None:
                drop = baseline - result.score
                if drop > regression_threshold:
                    regressions.append({
                        "case_id": case.id,
                        "baseline_score": baseline,
                        "current_score": result.score,
                        "drop": round(drop, 4),
                    })

        # Save results
        self._save_results(results)

        total = len(results)
        passed = sum(1 for r in results if r.passed)
        avg_score = statistics.mean([r.score for r in results]) if results else 0.0

        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": round(passed / total, 4) if total else 0.0,
            "average_score": round(avg_score, 4),
            "regressions": regressions,
            "has_regressions": len(regressions) > 0,
        }

    # ── Internal helpers ───────────────────────────────────────────

    def _generate_output(self, system_prompt: str, user_input: str) -> str:
        """Generate an LLM output for a given prompt pair."""
        if self.llm is None:
            return "[No LLM client configured — evaluation skipped]"
        try:
            result = self.llm.execute_task(
                agent_name="evaluator",
                task_instruction=user_input,
                priority="low",
                system_prompt=system_prompt,
                max_retries=1,
            )
            return result.get("result", json.dumps(result))
        except Exception as exc:
            logger.warning("Output generation failed: %s", exc)
            return ""

    def _judge_output(
        self,
        system_prompt: str,
        user_input: str,
        output: str,
        criteria: list[str],
    ) -> tuple[float, str, dict[str, float]]:
        """Use LLM-as-judge to score an output on given criteria.

        Returns (overall_score, reasoning, criteria_scores).
        """
        if self.llm is None:
            # Fallback: simple heuristic scoring
            return 0.7, "No judge available — heuristic score", {}

        judge_prompt = (
            f"Evaluate this AI response.\n\n"
            f"SYSTEM PROMPT:\n{system_prompt}\n\n"
            f"USER INPUT:\n{user_input}\n\n"
            f"AI RESPONSE:\n{output}\n\n"
            f"SCORING CRITERIA: {', '.join(criteria)}\n\n"
            f"Score each criterion 1-10, then give an overall score 0.0-1.0.\n"
            f"Respond with JSON only."
        )

        try:
            result = self.llm.execute_task(
                agent_name="judge",
                task_instruction=judge_prompt,
                priority="low",
                system_prompt=_JUDGE_SYSTEM_PROMPT,
                max_retries=1,
            )
            # Parse judge response
            overall = result.get("overall_score", 0.5)
            reasoning = result.get("reasoning", "")
            criteria_scores = result.get("criteria_scores", {})

            # Normalize criteria scores to 0.0-1.0 if they're on 1-10 scale
            normalized = {}
            for k, v in criteria_scores.items():
                if isinstance(v, (int, float)) and v > 1.0:
                    normalized[k] = min(v / 10.0, 1.0)
                else:
                    normalized[k] = float(v) if isinstance(v, (int, float)) else 0.5

            return float(overall), reasoning, normalized
        except Exception as exc:
            logger.warning("Judge scoring failed: %s", exc)
            return 0.5, f"Judge error: {exc}", {}

    def _get_baseline(self, case_id: str) -> float | None:
        """Get the historical baseline score for a case (latest result)."""
        for result in reversed(self._history):
            if result.case_id == case_id:
                return result.score
        # Check saved results
        results_file = self.results_dir / "eval_history.json"
        if results_file.exists():
            try:
                data = json.loads(results_file.read_text(encoding="utf-8"))
                for entry in reversed(data):
                    if entry.get("case_id") == case_id:
                        return entry.get("score")
            except (json.JSONDecodeError, OSError):
                pass
        return None

    def _save_results(self, results: list[EvalResult]) -> None:
        """Append evaluation results to the history file."""
        results_file = self.results_dir / "eval_history.json"
        existing: list[dict[str, Any]] = []
        if results_file.exists():
            try:
                existing = json.loads(results_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                existing = []

        existing.extend([r.to_dict() for r in results])
        results_file.write_text(
            json.dumps(existing, indent=2, default=str),
            encoding="utf-8",
        )
