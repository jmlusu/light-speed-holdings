"""Scoring engine for prompt evaluation results.

Evaluates LLM outputs on multiple dimensions:
- **Format compliance**: valid JSON, required fields present
- **Tool usage**: correct tools chosen, valid args
- **Reasoning quality**: thought field is substantive and logical
- **Result quality**: result field is clear and actionable
- **Constraint adherence**: follows rules (no markdown, no disallowed content)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from ai_company.prompts.evals.eval_dataset import ExpectedFormat, EvalTestCase
from ai_company.llm.json_parser import parse_llm_json


@dataclass
class ScoreBreakdown:
    """Detailed scoring breakdown for a single evaluation."""

    format_compliance: float = 0.0  # 0-1: valid JSON + required fields
    tool_usage: float = 0.0  # 0-1: correct tools chosen
    reasoning_quality: float = 0.0  # 0-1: thought field quality
    result_quality: float = 0.0  # 0-1: result field quality
    constraint_adherence: float = 0.0  # 0-1: follows all rules
    total: float = 0.0  # weighted total
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def compute_total(self, weights: dict[str, float] | None = None) -> float:
        """Compute weighted total score."""
        w = weights or {
            "format_compliance": 0.30,
            "tool_usage": 0.25,
            "reasoning_quality": 0.20,
            "result_quality": 0.15,
            "constraint_adherence": 0.10,
        }
        self.total = (
            w["format_compliance"] * self.format_compliance
            + w["tool_usage"] * self.tool_usage
            + w["reasoning_quality"] * self.reasoning_quality
            + w["result_quality"] * self.result_quality
            + w["constraint_adherence"] * self.constraint_adherence
        )
        return round(self.total, 4)


@dataclass
class EvalResult:
    """Full evaluation result for a single test case."""

    test_case_id: str
    raw_output: str
    parsed_output: dict[str, Any] | None
    score: ScoreBreakdown
    latency_ms: float = 0.0
    tokens_used: int = 0


class EvalScorer:
    """Score LLM outputs against test case expectations.

    Usage::

        scorer = EvalScorer()
        result = scorer.score(test_case, llm_output)
        print(result.score.total)  # 0.0 to 1.0
    """

    def score(self, test_case: EvalTestCase, raw_output: str) -> EvalResult:
        """Score a single LLM output against a test case."""
        parsed = parse_llm_json(raw_output)
        breakdown = ScoreBreakdown()

        # 1. Format compliance
        breakdown.format_compliance = self._score_format(
            raw_output, parsed, test_case.expected, breakdown
        )

        # 2. Tool usage
        breakdown.tool_usage = self._score_tools(
            parsed, test_case.expected, breakdown
        )

        # 3. Reasoning quality
        breakdown.reasoning_quality = self._score_reasoning(parsed, breakdown)

        # 4. Result quality
        breakdown.result_quality = self._score_result(parsed, breakdown)

        # 5. Constraint adherence
        breakdown.constraint_adherence = self._score_constraints(
            raw_output, parsed, test_case.expected, breakdown
        )

        breakdown.compute_total()

        return EvalResult(
            test_case_id=test_case.id,
            raw_output=raw_output,
            parsed_output=parsed,
            score=breakdown,
        )

    def score_batch(
        self, test_cases: list[EvalTestCase], outputs: dict[str, str]
    ) -> list[EvalResult]:
        """Score multiple outputs keyed by test case ID."""
        results: list[EvalResult] = []
        for tc in test_cases:
            raw = outputs.get(tc.id, "")
            results.append(self.score(tc, raw))
        return results

    # ------------------------------------------------------------------
    # Scoring dimensions
    # ------------------------------------------------------------------

    def _score_format(
        self,
        raw: str,
        parsed: dict[str, Any] | None,
        expected: ExpectedFormat,
        breakdown: ScoreBreakdown,
    ) -> float:
        """Score format compliance: valid JSON + required fields."""
        score = 0.0

        if expected.must_contain_json:
            if parsed is None:
                breakdown.errors.append("Response is not valid JSON")
                return 0.0
            score += 0.4  # base score for valid JSON
        else:
            score = 0.4  # full base if JSON not required

        if parsed is None:
            return score

        # Check required fields
        required_fields = []
        if expected.must_have_thought:
            required_fields.append("thought")
        if expected.must_have_plan:
            required_fields.append("plan")
        if expected.must_have_result:
            required_fields.append("result")
        if expected.must_have_done:
            required_fields.append("done")

        fields_present = sum(1 for f in required_fields if f in parsed)
        field_score = fields_present / max(len(required_fields), 1)
        score += 0.6 * field_score

        if field_score < 1.0:
            missing = [f for f in required_fields if f not in parsed]
            breakdown.warnings.append(f"Missing fields: {', '.join(missing)}")

        return min(score, 1.0)

    def _score_tools(
        self,
        parsed: dict[str, Any] | None,
        expected: ExpectedFormat,
        breakdown: ScoreBreakdown,
    ) -> float:
        """Score tool usage: correct tools chosen with valid structure."""
        if parsed is None:
            return 0.0

        plan = parsed.get("plan", [])
        if not isinstance(plan, list):
            breakdown.errors.append("Plan is not a list")
            return 0.0

        if not expected.plan_must_use_tools:
            # No specific tools required — just check plan structure
            return 1.0 if plan else 0.5

        # Check that required tools appear in the plan
        plan_tools = set()
        for step in plan:
            if isinstance(step, dict):
                tool = step.get("tool", "")
                if tool:
                    plan_tools.add(tool)

        required = set(expected.plan_must_use_tools)
        covered = required.intersection(plan_tools)
        score = len(covered) / len(required) if required else 1.0

        if score < 1.0:
            missing = required - plan_tools
            breakdown.warnings.append(f"Missing tools in plan: {', '.join(missing)}")

        # Bonus for valid step structure
        valid_steps = sum(
            1 for s in plan
            if isinstance(s, dict) and "tool" in s and "args" in s
        )
        if plan:
            structure_bonus = valid_steps / len(plan) * 0.2
            score = min(score + structure_bonus, 1.0)

        return round(score, 4)

    def _score_reasoning(
        self,
        parsed: dict[str, Any] | None,
        breakdown: ScoreBreakdown,
    ) -> float:
        """Score the quality of the 'thought' field."""
        if parsed is None:
            return 0.0

        thought = parsed.get("thought", "")
        if not thought or not isinstance(thought, str):
            breakdown.warnings.append("Thought field is empty or missing")
            return 0.1

        score = 0.0

        # Length indicator (more substantive = higher score, with diminishing returns)
        length = len(thought)
        if length > 200:
            score += 0.3
        elif length > 50:
            score += 0.2
        elif length > 10:
            score += 0.1
        else:
            score += 0.05
            breakdown.warnings.append("Thought is very short — may lack depth")

        # Check for reasoning indicators
        reasoning_patterns = [
            r"\b(because|therefore|since|given|considering)\b",
            r"\b(first|next|then|finally)\b",
            r"\b(if|when|unless|assuming)\b",
            r"\b(risk|benefit|trade.?off|alternative)\b",
            r"\b(plan|approach|strategy|step)\b",
        ]
        matches = sum(
            1 for p in reasoning_patterns if re.search(p, thought, re.IGNORECASE)
        )
        score += min(matches * 0.15, 0.5)

        return round(min(score, 1.0), 4)

    def _score_result(
        self,
        parsed: dict[str, Any] | None,
        breakdown: ScoreBreakdown,
    ) -> float:
        """Score the quality of the 'result' field."""
        if parsed is None:
            return 0.0

        result = parsed.get("result", "")
        if not result or not isinstance(result, str):
            breakdown.warnings.append("Result field is empty or missing")
            return 0.1

        score = 0.0

        # Length and specificity
        length = len(result)
        if length > 100:
            score += 0.3
        elif length > 30:
            score += 0.2
        elif length > 5:
            score += 0.1

        # Check for actionable content
        actionable_patterns = [
            r"\b(completed|finished|done|accomplished)\b",
            r"\b(created|updated|modified|fixed)\b",
            r"\b(recommend|suggest|next step)\b",
            r"\b(\d+ (file|test|task|change))\b",
        ]
        matches = sum(
            1 for p in actionable_patterns if re.search(p, result, re.IGNORECASE)
        )
        score += min(matches * 0.15, 0.5)

        # Check it's not just echoing the input
        if len(result) > 20:
            score += 0.2

        return round(min(score, 1.0), 4)

    def _score_constraints(
        self,
        raw: str,
        parsed: dict[str, Any] | None,
        expected: ExpectedFormat,
        breakdown: ScoreBreakdown,
    ) -> float:
        """Score adherence to constraints (no markdown, no disallowed content)."""
        score = 1.0

        # Check for markdown fences when JSON was required
        if expected.must_contain_json:
            if "```" in raw and parsed is not None:
                # If JSON was extracted from markdown, it's OK but not ideal
                breakdown.warnings.append(
                    "Response contains markdown fences — JSON was extracted but "
                    "direct JSON output is preferred"
                )
                score -= 0.1

        # Check for disallowed content
        for pattern in expected.must_not_contain:
            if pattern.lower() in raw.lower():
                breakdown.errors.append(f"Contains disallowed content: '{pattern}'")
                score -= 0.3

        # Check for prose outside JSON when JSON required
        if expected.must_contain_json and parsed is not None:
            # Simple heuristic: if there's significant text before/after the JSON
            json_start = raw.find("{")
            json_end = raw.rfind("}")
            if json_start > 0 and json_end > 0:
                prefix = raw[:json_start].strip()
                if len(prefix) > 50:
                    breakdown.warnings.append("Significant prose before JSON block")
                    score -= 0.1

        return round(max(score, 0.0), 4)


def compute_aggregate_scores(results: list[EvalResult]) -> dict[str, float]:
    """Compute aggregate statistics across multiple evaluation results."""
    if not results:
        return {}

    n = len(results)
    return {
        "count": n,
        "avg_total": round(sum(r.score.total for r in results) / n, 4),
        "avg_format": round(
            sum(r.score.format_compliance for r in results) / n, 4
        ),
        "avg_tools": round(sum(r.score.tool_usage for r in results) / n, 4),
        "avg_reasoning": round(
            sum(r.score.reasoning_quality for r in results) / n, 4
        ),
        "avg_result": round(sum(r.score.result_quality for r in results) / n, 4),
        "avg_constraints": round(
            sum(r.score.constraint_adherence for r in results) / n, 4
        ),
        "min_total": round(min(r.score.total for r in results), 4),
        "max_total": round(max(r.score.total for r in results), 4),
        "total_errors": sum(len(r.score.errors) for r in results),
        "total_warnings": sum(len(r.score.warnings) for r in results),
    }
