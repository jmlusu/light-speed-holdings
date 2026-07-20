"""Task complexity scoring — classify and score incoming tasks.

Scores tasks on a continuous 0.0–1.0 scale and buckets them into
simple/medium/complex categories.  Used by the model router to
assign appropriate LLM tiers (fast for simple, premium for complex).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


# ── Heuristic signals ─────────────────────────────────────────────

# Keywords that suggest higher complexity
COMPLEX_KEYWORDS: set[str] = {
    "architecture", "refactor", "migration", "security audit", "compliance",
    "regulation", "multi-step", "cross-team", "dependency", "optimization",
    "performance", "scalability", "distributed", "concurrent", "parallel",
    "machine learning", "neural", "training", "inference", "pipeline",
    "integration", "microservice", "kubernetes", "terraform", "database schema",
    "api design", "contract", "nda", "legal", "financial model", "forecast",
    "budget", "audit", "penetration test", "incident response",
}

# Keywords that suggest simpler tasks
SIMPLE_KEYWORDS: set[str] = {
    "read", "list", "show", "print", "display", "summarize", "count",
    "search", "find", "check", "verify", "status", "info", "help",
    "explain", "define", "what is", "who is",
}

# Patterns that increase complexity
COMPLEX_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\b(implement|build|create|design)\b.*\b(system|service|module)\b", re.IGNORECASE),
    re.compile(r"\b(multiple|several|all)\b.*\b(components|files|modules|services)\b", re.IGNORECASE),
    re.compile(r"\b(integration|migration|refactor)\b", re.IGNORECASE),
    re.compile(r"\b(and|plus|also|additionally)\b", re.IGNORECASE),  # Multiple requirements
]

# Tools that imply complexity
COMPLEX_TOOLS: set[str] = {
    "execute", "code_interpreter", "delegate",
}

SIMPLE_TOOLS: set[str] = {
    "read", "list", "grep", "glob", "search", "view",
}


@dataclass
class ComplexityScore:
    """Result of task complexity scoring."""

    score: float  # 0.0 (simple) to 1.0 (complex)
    level: str  # "simple", "medium", "complex"
    signals: dict[str, float]  # Breakdown of scoring signals
    recommended_tier: str  # "fast", "standard", "premium"
    reasoning: str  # Human-readable explanation

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": round(self.score, 3),
            "level": self.level,
            "signals": self.signals,
            "recommended_tier": self.recommended_tier,
            "reasoning": self.reasoning,
        }


class TaskComplexityScorer:
    """Score incoming tasks by complexity using multi-signal analysis.

    Combines keyword heuristics, structural analysis, and optional
    historical data to produce a continuous complexity score and a
    categorical level (simple/medium/complex).

    The score drives model tier routing:
      - simple (0.0–0.33) → fast tier
      - medium (0.34–0.66) → standard tier
      - complex (0.67–1.0) → premium tier

    Args:
        custom_complex_keywords: Additional keywords that increase complexity.
        custom_simple_keywords: Additional keywords that decrease complexity.
    """

    def __init__(
        self,
        custom_complex_keywords: set[str] | None = None,
        custom_simple_keywords: set[str] | None = None,
    ) -> None:
        self.complex_keywords = COMPLEX_KEYWORDS | (custom_complex_keywords or set())
        self.simple_keywords = SIMPLE_KEYWORDS | (custom_simple_keywords or set())

    def score_task(
        self,
        instruction: str,
        tools_requested: list[str] | None = None,
        priority: str = "medium",
        agent_type: str = "specialist",
        metadata: dict[str, Any] | None = None,
    ) -> ComplexityScore:
        """Score a task for complexity.

        Args:
            instruction: The task instruction / prompt text.
            tools_requested: List of tools the task may need.
            priority: Task priority level.
            agent_type: Type of agent handling the task.
            metadata: Optional additional context.

        Returns:
            ComplexityScore with score, level, and recommended tier.
        """
        signals: dict[str, float] = {}

        # Signal 1: Keyword density
        keyword_score = self._keyword_signal(instruction)
        signals["keyword_density"] = keyword_score

        # Signal 2: Instruction length and structure
        structural_score = self._structural_signal(instruction)
        signals["structural"] = structural_score

        # Signal 3: Pattern matching
        pattern_score = self._pattern_signal(instruction)
        signals["pattern_match"] = pattern_score

        # Signal 4: Tool complexity
        tool_score = self._tool_signal(tools_requested or [])
        signals["tool_complexity"] = tool_score

        # Signal 5: Priority weight
        priority_score = self._priority_signal(priority)
        signals["priority"] = priority_score

        # Signal 6: Agent type adjustment
        agent_score = self._agent_signal(agent_type)
        signals["agent_type"] = agent_score

        # Weighted combination
        weights = {
            "keyword_density": 0.25,
            "structural": 0.15,
            "pattern_match": 0.20,
            "tool_complexity": 0.15,
            "priority": 0.10,
            "agent_type": 0.15,
        }

        raw_score = sum(signals[k] * weights[k] for k in weights)
        score = max(0.0, min(1.0, raw_score))

        # Classify
        if score <= 0.33:
            level = "simple"
            tier = "fast"
        elif score <= 0.66:
            level = "medium"
            tier = "standard"
        else:
            level = "complex"
            tier = "premium"

        reasoning = self._build_reasoning(signals, level)

        return ComplexityScore(
            score=score,
            level=level,
            signals=signals,
            recommended_tier=tier,
            reasoning=reasoning,
        )

    def score_batch(
        self,
        tasks: list[dict[str, Any]],
    ) -> list[ComplexityScore]:
        """Score multiple tasks at once.

        Args:
            tasks: List of task dicts with at least 'instruction' key.

        Returns:
            List of ComplexityScore objects.
        """
        return [
            self.score_task(
                instruction=t.get("instruction", t.get("description", "")),
                tools_requested=t.get("tools_requested"),
                priority=t.get("priority", "medium"),
                agent_type=t.get("agent_type", "specialist"),
                metadata=t.get("metadata"),
            )
            for t in tasks
        ]

    def suggest_tier(self, score: ComplexityScore) -> str:
        """Suggest a model tier based on complexity score.

        Maps the score to tier while considering that medium-complexity
        tasks on high priority may benefit from standard tier.

        Args:
            score: The complexity score result.

        Returns:
            Recommended tier name: "fast", "standard", or "premium".
        """
        return score.recommended_tier

    # ── Signal functions ───────────────────────────────────────────

    def _keyword_signal(self, instruction: str) -> float:
        """Score based on presence of complexity/simple keywords."""
        lower = instruction.lower()
        complex_hits = sum(1 for kw in self.complex_keywords if kw in lower)
        simple_hits = sum(1 for kw in self.simple_keywords if kw in lower)

        # Normalize by instruction length (per 100 words)
        word_count = max(1, len(instruction.split()))
        complex_density = complex_hits / (word_count / 100)
        simple_density = simple_hits / (word_count / 100)

        signal = 0.5 + (complex_density * 0.15) - (simple_density * 0.15)
        return max(0.0, min(1.0, signal))

    def _structural_signal(self, instruction: str) -> float:
        """Score based on instruction structure (length, lists, code blocks)."""
        lines = instruction.strip().split("\n")
        word_count = len(instruction.split())

        # Longer instructions tend to be more complex
        length_score = min(1.0, word_count / 200)

        # Multiple bullet points or numbered lists suggest multi-step tasks
        list_items = sum(
            1 for line in lines
            if re.match(r"^\s*[-*•]\s|^\s*\d+[.)]\s", line)
        )
        list_score = min(1.0, list_items / 5)

        # Code blocks suggest technical tasks
        code_blocks = instruction.count("```")
        code_score = min(1.0, code_blocks / 4)

        return 0.3 * length_score + 0.35 * list_score + 0.35 * code_score

    def _pattern_signal(self, instruction: str) -> float:
        """Score based on regex pattern matching."""
        matches = sum(1 for p in COMPLEX_PATTERNS if p.search(instruction))
        return min(1.0, matches / len(COMPLEX_PATTERNS))

    def _tool_signal(self, tools: list[str]) -> float:
        """Score based on requested tool types."""
        if not tools:
            return 0.4  # Neutral default

        complex_count = sum(1 for t in tools if t in COMPLEX_TOOLS)
        simple_count = sum(1 for t in tools if t in SIMPLE_TOOLS)
        total = len(tools)

        if total == 0:
            return 0.4

        ratio = (complex_count - simple_count) / total
        return 0.5 + ratio * 0.5

    @staticmethod
    def _priority_signal(priority: str) -> float:
        """Map priority to a complexity-adjacent signal."""
        mapping = {"low": 0.2, "medium": 0.5, "high": 0.7, "critical": 0.9}
        return mapping.get(priority, 0.5)

    @staticmethod
    def _agent_signal(agent_type: str) -> float:
        """Map agent type to complexity expectation."""
        mapping = {
            "specialist": 0.4,
            "lead": 0.6,
            "executive": 0.7,
            "board": 0.8,
        }
        return mapping.get(agent_type.lower(), 0.5)

    @staticmethod
    def _build_reasoning(signals: dict[str, float], level: str) -> str:
        """Build human-readable reasoning for the score."""
        top_signals = sorted(signals.items(), key=lambda x: x[1], reverse=True)[:3]
        parts = [f"Task classified as {level}."]

        for name, val in top_signals:
            if val > 0.6:
                parts.append(f"High {name.replace('_', ' ')} ({val:.2f})")
            elif val < 0.4:
                parts.append(f"Low {name.replace('_', ' ')} ({val:.2f})")

        return " ".join(parts)
