"""Prompt optimization — analyze and improve LLM prompt effectiveness.

Reads audit logs to identify prompt patterns that correlate with success
or failure, suggests prompt improvements, and supports A/B testing of
prompt variants.
"""

from __future__ import annotations

import json
import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class PromptVariant:
    """A prompt variant for A/B testing."""

    variant_id: str
    prompt_template: str
    description: str = ""
    created_at: str = ""
    impressions: int = 0
    successes: int = 0
    failures: int = 0

    @property
    def success_rate(self) -> float:
        if self.impressions == 0:
            return 0.0
        return self.successes / self.impressions

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["success_rate"] = round(self.success_rate, 3)
        return d


@dataclass
class PromptInsight:
    """An insight derived from prompt performance analysis."""

    insight_type: str  # "keyword_impact", "length_correlation", "pattern_success"
    description: str
    impact_score: float  # -1.0 (harmful) to +1.0 (helpful)
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class PromptOptimizer:
    """Analyze prompt effectiveness and suggest improvements.

    Reads audit event logs to correlate prompt characteristics with
    task outcomes, then generates actionable insights for prompt
    refinement.

    Args:
        audit_log_path: Path to the JSONL audit log.
        results_dir: Directory for storing optimization data.
    """

    def __init__(
        self,
        audit_log_path: str | Path = ".opencode/audit.jsonl",
        results_dir: str | Path = "results/prompt_optimization",
    ) -> None:
        self.audit_log_path = Path(audit_log_path)
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

        self._variants: dict[str, PromptVariant] = {}
        self._insights: list[PromptInsight] = []
        self._active_variant: str | None = None

        self._load_variants()

    def analyze_prompt_effectiveness(self) -> dict[str, Any]:
        """Analyze audit logs to identify prompt patterns correlated with outcomes.

        Returns:
            Dict with insights, keyword analysis, and recommendations.
        """
        events = self._load_audit_events()
        if not events:
            return {"insights": [], "recommendations": [], "data_points": 0}

        # Separate task completions and failures
        completions = [e for e in events if e.get("event_type") == "task_completed"]
        failures = [e for e in events if e.get("event_type") == "task_failed"]

        insights: list[PromptInsight] = []

        # Analyze keyword impact
        keyword_insight = self._analyze_keyword_impact(completions, failures)
        if keyword_insight:
            insights.append(keyword_insight)

        # Analyze instruction length correlation
        length_insight = self._analyze_length_correlation(completions, failures)
        if length_insight:
            insights.append(length_insight)

        # Analyze tool usage patterns
        tool_insight = self._analyze_tool_patterns(completions, failures)
        if tool_insight:
            insights.append(tool_insight)

        # Generate recommendations
        recommendations = self._generate_recommendations(insights)

        self._insights.extend(insights)
        self._save_insights()

        return {
            "insights": [i.to_dict() for i in insights],
            "recommendations": recommendations,
            "data_points": len(events),
            "success_rate": round(len(completions) / max(1, len(completions) + len(failures)), 3),
        }

    def suggest_improvements(self, prompt: str, context: dict[str, Any] | None = None) -> list[str]:
        """Suggest improvements for a given prompt based on historical patterns.

        Args:
            prompt: The prompt text to improve.
            context: Optional context (agent_id, task_type, etc.).

        Returns:
            List of improvement suggestions.
        """
        suggestions: list[str] = []
        lower = prompt.lower()

        # Check length
        word_count = len(prompt.split())
        if word_count < 10:
            suggestions.append(
                "Prompt is very short. Consider adding more specific instructions "
                "or context to improve task success rates."
            )
        elif word_count > 500:
            suggestions.append(
                "Prompt is very long. Consider breaking it into smaller, focused "
                "instructions for better LLM comprehension."
            )

        # Check for action verbs
        action_verbs = {"create", "build", "implement", "fix", "update", "analyze", "review"}
        has_action = any(verb in lower for verb in action_verbs)
        if not has_action:
            suggestions.append(
                "Prompt lacks clear action verbs. Start with a direct action "
                "(e.g., 'Create...', 'Fix...', 'Analyze...') for clearer instructions."
            )

        # Check for success criteria
        criteria_words = {"should", "must", "ensure", "verify", "validate", "check"}
        has_criteria = any(w in lower for w in criteria_words)
        if not has_criteria:
            suggestions.append(
                "Consider adding explicit success criteria or acceptance conditions "
                "to help the agent understand when the task is complete."
            )

        # Check for constraints
        constraint_words = {"without", "must not", "avoid", "do not", "limit"}
        has_constraints = any(w in lower for w in constraint_words)
        if not has_constraints and word_count > 50:
            suggestions.append(
                "For complex tasks, adding constraints or limitations helps prevent "
                "the agent from over-engineering or going off-scope."
            )

        # Apply insight-based suggestions
        for insight in self._insights:
            if insight.impact_score < -0.3 and insight.insight_type == "keyword_impact":
                harmful_kw = insight.evidence.get("harmful_keywords", [])
                for kw in harmful_kw[:3]:
                    if kw in lower:
                        suggestions.append(
                            f"Keyword '{kw}' is correlated with task failures. "
                            "Consider rephrasing to be more specific."
                        )

        return suggestions

    def create_variant(
        self,
        variant_id: str,
        prompt_template: str,
        description: str = "",
    ) -> PromptVariant:
        """Create a new prompt variant for A/B testing.

        Args:
            variant_id: Unique identifier for this variant.
            prompt_template: The prompt template text.
            description: Human-readable description of the variant.

        Returns:
            The created PromptVariant.
        """
        from datetime import datetime

        variant = PromptVariant(
            variant_id=variant_id,
            prompt_template=prompt_template,
            description=description,
            created_at=datetime.now().isoformat(),
        )
        self._variants[variant_id] = variant
        self._save_variants()
        return variant

    def record_variant_outcome(
        self,
        variant_id: str,
        success: bool,
    ) -> None:
        """Record the outcome of using a prompt variant.

        Args:
            variant_id: The variant that was used.
            success: Whether the task succeeded.
        """
        if variant_id not in self._variants:
            logger.warning("Unknown variant: %s", variant_id)
            return

        variant = self._variants[variant_id]
        variant.impressions += 1
        if success:
            variant.successes += 1
        else:
            variant.failures += 1
        self._save_variants()

    def get_variant_performance(self) -> list[dict[str, Any]]:
        """Get performance comparison of all variants.

        Returns:
            List of variant performance dicts sorted by success rate.
        """
        variants = sorted(
            self._variants.values(),
            key=lambda v: v.success_rate,
            reverse=True,
        )
        return [v.to_dict() for v in variants]

    def select_variant(self) -> PromptVariant | None:
        """Select the best-performing variant for use.

        Returns the variant with the highest success rate (minimum 3
        impressions), or None if no variant qualifies.
        """
        qualified = [
            v for v in self._variants.values()
            if v.impressions >= 3
        ]
        if not qualified:
            return None
        return max(qualified, key=lambda v: v.success_rate)

    # ── Analysis methods ───────────────────────────────────────────

    def _analyze_keyword_impact(
        self,
        completions: list[dict],
        failures: list[dict],
    ) -> PromptInsight | None:
        """Analyze which keywords correlate with success vs failure."""
        completion_words: dict[str, int] = defaultdict(int)
        failure_words: dict[str, int] = defaultdict(int)

        stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been",
                       "being", "have", "has", "had", "do", "does", "did", "will",
                       "would", "could", "should", "may", "might", "can", "shall",
                       "to", "of", "in", "for", "on", "with", "at", "by", "from",
                       "as", "into", "through", "during", "before", "after", "and",
                       "but", "or", "if", "that", "this", "it", "not", "no"}

        for e in completions:
            instruction = e.get("args", {}).get("instruction", "") or e.get("metadata", {}).get("instruction", "")
            for word in re.findall(r"\b[a-z]+\b", instruction.lower()):
                if word not in stop_words and len(word) > 2:
                    completion_words[word] += 1

        for e in failures:
            instruction = e.get("args", {}).get("instruction", "") or e.get("metadata", {}).get("instruction", "")
            for word in re.findall(r"\b[a-z]+\b", instruction.lower()):
                if word not in stop_words and len(word) > 2:
                    failure_words[word] += 1

        # Find keywords with disproportionate failure rates
        all_words = set(completion_words.keys()) | set(failure_words.keys())
        harmful: list[str] = []
        helpful: list[str] = []

        for word in all_words:
            c_count = completion_words.get(word, 0)
            f_count = failure_words.get(word, 0)
            total = c_count + f_count
            if total < 3:
                continue
            failure_rate = f_count / total
            if failure_rate > 0.7:
                harmful.append(word)
            elif failure_rate < 0.3 and total >= 5:
                helpful.append(word)

        if not harmful and not helpful:
            return None

        return PromptInsight(
            insight_type="keyword_impact",
            description=(
                f"Identified {len(harmful)} harmful keywords and "
                f"{len(helpful)} helpful keywords in task prompts."
            ),
            impact_score=0.5 if helpful else -0.5,
            evidence={
                "harmful_keywords": harmful[:10],
                "helpful_keywords": helpful[:10],
                "completion_count": len(completions),
                "failure_count": len(failures),
            },
        )

    def _analyze_length_correlation(
        self,
        completions: list[dict],
        failures: list[dict],
    ) -> PromptInsight | None:
        """Analyze correlation between prompt length and success."""
        import numpy as np

        completion_lengths = []
        for e in completions:
            instruction = e.get("args", {}).get("instruction", "") or e.get("metadata", {}).get("instruction", "")
            completion_lengths.append(len(instruction.split()))

        failure_lengths = []
        for e in failures:
            instruction = e.get("args", {}).get("instruction", "") or e.get("metadata", {}).get("instruction", "")
            failure_lengths.append(len(instruction.split()))

        if not completion_lengths or not failure_lengths:
            return None

        avg_success = float(np.mean(completion_lengths))
        avg_failure = float(np.mean(failure_lengths))

        diff = avg_success - avg_failure
        impact = max(-1.0, min(1.0, diff / 100))

        optimal_range = (
            round(max(10, avg_success - 30)),
            round(avg_success + 30),
        )

        return PromptInsight(
            insight_type="length_correlation",
            description=(
                f"Successful prompts average {avg_success:.0f} words; "
                f"failed prompts average {avg_failure:.0f} words. "
                f"Optimal range: {optimal_range[0]}–{optimal_range[1]} words."
            ),
            impact_score=round(impact, 3),
            evidence={
                "avg_success_words": round(avg_success, 1),
                "avg_failure_words": round(avg_failure, 1),
                "optimal_range": optimal_range,
            },
        )

    def _analyze_tool_patterns(
        self,
        completions: list[dict],
        failures: list[dict],
    ) -> PromptInsight | None:
        """Analyze which tool usage patterns correlate with success."""
        tool_success: dict[str, int] = defaultdict(int)
        tool_failure: dict[str, int] = defaultdict(int)

        for e in completions:
            for tool in e.get("metadata", {}).get("tools_used", []):
                tool_success[tool] += 1

        for e in failures:
            for tool in e.get("metadata", {}).get("tools_used", []):
                tool_failure[tool] += 1

        all_tools = set(tool_success.keys()) | set(tool_failure.keys())
        if not all_tools:
            return None

        patterns: dict[str, str] = {}
        for tool in all_tools:
            s = tool_success.get(tool, 0)
            f = tool_failure.get(tool, 0)
            total = s + f
            if total >= 2:
                rate = s / total
                patterns[tool] = "reliable" if rate > 0.8 else "unreliable" if rate < 0.5 else "moderate"

        return PromptInsight(
            insight_type="pattern_success",
            description=f"Analyzed tool reliability across {len(patterns)} tools.",
            impact_score=0.3,
            evidence={"tool_reliability": patterns},
        )

    def _generate_recommendations(self, insights: list[PromptInsight]) -> list[str]:
        """Generate actionable recommendations from insights."""
        recs: list[str] = []

        for insight in insights:
            if insight.insight_type == "keyword_impact":
                harmful = insight.evidence.get("harmful_keywords", [])
                if harmful:
                    recs.append(
                        f"Avoid these keywords in prompts (correlated with failures): "
                        f"{', '.join(harmful[:5])}"
                    )
                helpful = insight.evidence.get("helpful_keywords", [])
                if helpful:
                    recs.append(
                        f"Include these keywords for better results: "
                        f"{', '.join(helpful[:5])}"
                    )

            elif insight.insight_type == "length_correlation":
                opt_range = insight.evidence.get("optimal_range", (50, 150))
                recs.append(
                    f"Aim for {opt_range[0]}–{opt_range[1]} words in task instructions "
                    f"for optimal success rates."
                )

            elif insight.insight_type == "pattern_success":
                unreliable = [
                    t for t, r in insight.evidence.get("tool_reliability", {}).items()
                    if r == "unreliable"
                ]
                if unreliable:
                    recs.append(
                        f"Tasks using these tools have higher failure rates: "
                        f"{', '.join(unreliable)}. Consider adding guardrails."
                    )

        return recs

    # ── Persistence ────────────────────────────────────────────────

    def _load_audit_events(self) -> list[dict]:
        """Load audit events from JSONL file."""
        if not self.audit_log_path.exists():
            return []

        events: list[dict] = []
        try:
            with open(self.audit_log_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        except OSError:
            pass
        return events

    def _save_variants(self) -> None:
        """Persist variants to disk."""
        path = self.results_dir / "variants.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {k: v.to_dict() for k, v in self._variants.items()},
                f,
                indent=2,
                default=str,
            )

    def _load_variants(self) -> None:
        """Load variants from disk."""
        path = self.results_dir / "variants.json"
        if not path.exists():
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in data.items():
                self._variants[k] = PromptVariant(**{kk: vv for kk, vv in v.items() if kk != "success_rate"})
        except (json.JSONDecodeError, KeyError, OSError) as exc:
            logger.warning("Failed to load prompt variants: %s", exc)

    def _save_insights(self) -> None:
        """Persist insights to disk."""
        path = self.results_dir / "insights.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                [i.to_dict() for i in self._insights],
                f,
                indent=2,
                default=str,
            )
