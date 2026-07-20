"""Autonomous decision engine — confidence scoring, tier-based autonomy, and
self-healing retry intelligence.

For low-risk actions (Tier 0-1), agents can execute autonomously without
HITL approval. The engine scores decision confidence and applies
intelligent retry strategies when failures occur.

Usage::

    engine = AutonomousDecisionEngine(tier_rules=tier_rules)

    # Check if an action can be autonomous
    decision = engine.evaluate(
        tool="write",
        args={"path": "docs/README.md", "content": "..."},
        agent_seniority="executive",
        task_risk="low",
    )

    if decision.autonomous:
        # Execute without HITL
        execute_action(tool, args)
        engine.record_outcome(decision, success=True)
    else:
        # Request HITL approval
        request_approval(tool, args)
"""

from __future__ import annotations

import json
import logging
import random
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass
class ConfidenceScore:
    """A confidence assessment for an autonomous decision."""

    score: float  # 0.0 to 1.0
    factors: dict[str, float] = field(default_factory=dict)
    reasoning: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": round(self.score, 4),
            "factors": {k: round(v, 4) for k, v in self.factors.items()},
            "reasoning": self.reasoning,
        }


@dataclass
class AutonomousDecision:
    """Result of evaluating whether an action can be executed autonomously."""

    tool: str
    args: dict[str, Any]
    autonomous: bool
    confidence: ConfidenceScore
    tier: int  # Approval tier (0-4)
    requires_hitl: bool
    reasoning: str = ""
    retry_strategy: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool": self.tool,
            "autonomous": self.autonomous,
            "confidence": self.confidence.to_dict(),
            "tier": self.tier,
            "requires_hitl": self.requires_hitl,
            "reasoning": self.reasoning,
            "retry_strategy": self.retry_strategy,
            "timestamp": self.timestamp,
        }


@dataclass
class RetryAttempt:
    """Record of a single retry attempt."""

    attempt: int
    timestamp: str
    error: str
    strategy: str
    delay_seconds: float


@dataclass
class SelfHealingPolicy:
    """Configuration for self-healing retry behavior."""

    max_retries: int = 3
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 60.0
    backoff_multiplier: float = 2.0
    jitter: bool = True
    # Strategies in order of escalation
    strategies: list[str] = field(default_factory=lambda: [
        "retry_same",       # Retry with same parameters
        "simplify",         # Simplify the request
        "alternative_tool", # Use an alternative tool
        "escalate",         # Escalate to human
    ])


# ---------------------------------------------------------------------------
# Confidence scoring factors
# ---------------------------------------------------------------------------

# Weight for each factor in confidence calculation
FACTOR_WEIGHTS: dict[str, float] = {
    "tool_safety": 0.25,       # How safe is the tool (read=high, execute=low)
    "path_safety": 0.20,       # How safe is the target path
    "agent_seniority": 0.15,   # Agent's authority level
    "task_risk": 0.15,         # Overall task risk level
    "historical_success": 0.15, # Past success rate for similar actions
    "time_of_day": 0.05,       # Business hours vs off-hours
    "recent_failures": 0.05,   # Recent failure streak
}

# Tool safety scores (higher = safer)
TOOL_SAFETY: dict[str, float] = {
    "read": 1.0,
    "list": 1.0,
    "grep": 1.0,
    "glob": 1.0,
    "search": 1.0,
    "ping": 1.0,
    "view": 1.0,
    "delegate": 0.8,
    "write": 0.5,
    "edit": 0.5,
    "code_interpreter": 0.4,
    "execute": 0.3,
}

# Seniority authority scores
SENIORITY_AUTHORITY: dict[str, float] = {
    "executive": 1.0,
    "lead": 0.8,
    "senior": 0.7,
    "mid": 0.5,
    "junior": 0.3,
}

# Risk level scores (higher = less risky)
RISK_SAFETY: dict[str, float] = {
    "low": 1.0,
    "medium": 0.6,
    "high": 0.3,
    "critical": 0.1,
}


# ---------------------------------------------------------------------------
# Autonomous decision engine
# ---------------------------------------------------------------------------


class AutonomousDecisionEngine:
    """Evaluates whether actions can be executed autonomously.

    Considers approval tiers, agent seniority, confidence scoring,
    and historical success rates to make autonomous execution decisions.
    Also provides self-healing retry intelligence.

    Args:
        confidence_threshold: Minimum confidence score for autonomous execution.
        history_dir: Directory for persisting decision history and stats.
    """

    # Tier thresholds: autonomous if tier <= this value and confidence is high enough
    AUTONOMOUS_TIER_LIMIT = 1  # Tier 0 (auto-approve) and Tier 1 (notify)

    def __init__(
        self,
        confidence_threshold: float = 0.7,
        history_dir: str | Path = "results/decisions",
    ) -> None:
        self.confidence_threshold = confidence_threshold
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(parents=True, exist_ok=True)

        # Historical success rates: tool -> success count / total count
        self._success_history: dict[str, deque[bool]] = {}
        self._max_history = 100

        # Recent failure tracking per tool
        self._recent_failures: dict[str, deque[float]] = {}

        # Decision log
        self._decision_log: list[dict[str, Any]] = []

        self._load_history()

    def evaluate(
        self,
        tool: str,
        args: dict[str, Any],
        agent_seniority: str = "mid",
        task_risk: str = "low",
        approval_tier: int = 0,
        task_context: dict[str, Any] | None = None,
    ) -> AutonomousDecision:
        """Evaluate whether an action can be executed autonomously.

        Args:
            tool: The tool being invoked (read, write, execute, etc.).
            args: The tool arguments.
            agent_seniority: The agent's seniority level.
            task_risk: Overall risk level of the task.
            approval_tier: The pre-computed approval tier (0-4).
            task_context: Additional task context.

        Returns:
            ``AutonomousDecision`` with autonomy verdict and confidence.
        """
        # Calculate confidence factors
        factors = self._calculate_factors(
            tool=tool,
            args=args,
            agent_seniority=agent_seniority,
            task_risk=task_risk,
            approval_tier=approval_tier,
        )

        # Weighted confidence score
        confidence_score = sum(
            factors.get(name, 0.0) * weight
            for name, weight in FACTOR_WEIGHTS.items()
        )
        confidence_score = min(max(confidence_score, 0.0), 1.0)

        # Determine autonomy
        is_low_tier = approval_tier <= self.AUTONOMOUS_TIER_LIMIT
        is_confident = confidence_score >= self.confidence_threshold
        autonomous = is_low_tier and is_confident

        # Build reasoning
        reasoning_parts = []
        if not is_low_tier:
            reasoning_parts.append(
                f"Tier {approval_tier} requires HITL (limit: {self.AUTONOMOUS_TIER_LIMIT})"
            )
        if not is_confident:
            reasoning_parts.append(
                f"Confidence {confidence_score:.2f} below threshold {self.confidence_threshold}"
            )
        if autonomous:
            reasoning_parts.append("Low-tier action with high confidence — autonomous OK")

        # Select retry strategy
        retry_strategy = self._select_retry_strategy(tool, agent_seniority)

        decision = AutonomousDecision(
            tool=tool,
            args=args,
            autonomous=autonomous,
            confidence=ConfidenceScore(
                score=confidence_score,
                factors=factors,
                reasoning="; ".join(reasoning_parts),
            ),
            tier=approval_tier,
            requires_hitl=not autonomous,
            reasoning="; ".join(reasoning_parts),
            retry_strategy=retry_strategy,
        )

        # Log decision
        self._decision_log.append(decision.to_dict())
        self._save_decision_log()

        return decision

    def record_outcome(
        self,
        decision: AutonomousDecision,
        success: bool,
        error: str = "",
    ) -> None:
        """Record the outcome of an autonomous decision for learning.

        Updates success rates and failure tracking for future confidence
        calculations.
        """
        tool = decision.tool

        # Update success history
        if tool not in self._success_history:
            self._success_history[tool] = deque(maxlen=self._max_history)
        self._success_history[tool].append(success)

        # Update failure tracking
        if not success:
            if tool not in self._recent_failures:
                self._recent_failures[tool] = deque(maxlen=self._max_history)
            self._recent_failures[tool].append(time.time())
        else:
            # Clear recent failures on success
            if tool in self._recent_failures:
                self._recent_failures[tool].clear()

        self._save_history()

    def get_success_rate(self, tool: str) -> float:
        """Get the historical success rate for a tool (0.0 to 1.0)."""
        history = self._success_history.get(tool, deque())
        if not history:
            return 0.5  # Default: neutral
        return sum(history) / len(history)

    def get_retry_policy(self, tool: str, attempt: int) -> SelfHealingPolicy:
        """Get the self-healing retry policy for a tool.

        Escalates strategy based on attempt number:
        - Attempt 1: retry_same (immediate retry)
        - Attempt 2: simplify (simplify the request)
        - Attempt 3: alternative_tool (try different approach)
        - Attempt 4+: escalate (notify human)
        """
        policy = SelfHealingPolicy()

        # Calculate delay with exponential backoff
        delay = policy.base_delay_seconds * (
            policy.backoff_multiplier ** (attempt - 1)
        )
        delay = min(delay, policy.max_delay_seconds)

        # Add jitter if enabled
        if policy.jitter:
            delay *= (0.5 + random.random())

        policy.base_delay_seconds = delay
        return policy

    def suggest_retry(
        self,
        tool: str,
        error: str,
        attempt: int,
        original_args: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Suggest modified args for a retry based on the error and attempt.

        Returns suggested args for the next attempt, or None if escalation
        is recommended.
        """
        policy = self.get_retry_policy(tool, attempt)
        strategy_idx = min(attempt - 1, len(policy.strategies) - 1)
        strategy = policy.strategies[strategy_idx]

        if strategy == "retry_same":
            return original_args  # No change
        elif strategy == "simplify":
            return self._simplify_args(tool, original_args, error)
        elif strategy == "alternative_tool":
            return self._suggest_alternative(tool, original_args, error)
        else:
            # Escalate to human — GAP-008: persist the escalation decision
            # to the audit trail so it is not silently dropped.
            self._audit_escalation(tool, attempt, error)
            return None  # Escalate to human

    # ── Factor calculation ─────────────────────────────────────────

    def _calculate_factors(
        self,
        tool: str,
        args: dict[str, Any],
        agent_seniority: str,
        task_risk: str,
        approval_tier: int,
    ) -> dict[str, float]:
        """Calculate all confidence factors for a decision."""
        factors: dict[str, float] = {}

        # Tool safety
        factors["tool_safety"] = TOOL_SAFETY.get(tool, 0.3)

        # Path safety (check args for dangerous paths)
        factors["path_safety"] = self._assess_path_safety(args)

        # Agent seniority
        factors["agent_seniority"] = SENIORITY_AUTHORITY.get(agent_seniority, 0.5)

        # Task risk
        factors["task_risk"] = RISK_SAFETY.get(task_risk, 0.5)

        # Historical success
        factors["historical_success"] = self.get_success_rate(tool)

        # Time of day (business hours = safer)
        hour = datetime.now().hour
        factors["time_of_day"] = 1.0 if 9 <= hour <= 17 else 0.7

        # Recent failures (fewer = better)
        recent = self._recent_failures.get(tool, deque())
        factors["recent_failures"] = max(0.0, 1.0 - (len(recent) * 0.2))

        return factors

    def _assess_path_safety(self, args: dict[str, Any]) -> float:
        """Assess how safe the target path in args is."""
        # Collect all string values from args
        candidates = []
        for v in args.values():
            if isinstance(v, str):
                candidates.append(v)
            elif isinstance(v, list):
                candidates.extend(x for x in v if isinstance(x, str))

        if not candidates:
            return 0.8  # No paths = relatively safe

        dangerous_patterns = [
            "/secrets/", "/.env", "config/secrets", "private_key",
            "security/", "audit/", "legal/", "compliance/",
            "/production/", "/prod/", "deploy/",
        ]
        safe_patterns = [
            "docs/", "config/", ".github/", ".md", ".rst",
            "tests/", "README",
        ]

        max_safety = 1.0
        for candidate in candidates:
            lower = candidate.lower()
            for pattern in dangerous_patterns:
                if pattern in lower:
                    max_safety = min(max_safety, 0.2)
            for pattern in safe_patterns:
                if pattern in lower:
                    max_safety = max(max_safety, 0.9)

        return max_safety

    # ── Retry intelligence ─────────────────────────────────────────

    def _audit_escalation(self, tool: str, attempt: int, error: str) -> None:
        """Best-effort audit hook for autonomous escalation (GAP-008).

        Imported lazily and wrapped in try/except so a failure in the audit
        subsystem can never break the self-healing retry flow itself.
        """
        try:
            from ai_company.audit.integration import log_escalation

            log_escalation(
                task_id="",
                from_agent="autonomous_decision_engine",
                to_agent="human",
                reason=(
                    f"Autonomous retry exhausted self-healing strategies "
                    f"(tool={tool}, attempt={attempt}): {error}"
                ),
                rule_id="autonomous-escalation",
            )
        except Exception:  # pragma: no cover - defensive
            logger.debug("audit hook skipped for autonomous escalation", exc_info=True)

    def _select_retry_strategy(self, tool: str, seniority: str) -> str:
        """Select the initial retry strategy based on tool and seniority."""
        if tool in ("read", "list", "grep"):
            return "retry_same"  # Read-only tools are safe to retry
        if seniority in ("executive", "lead"):
            return "simplify"
        return "retry_same"

    def _simplify_args(
        self,
        tool: str,
        args: dict[str, Any],
        error: str,
    ) -> dict[str, Any]:
        """Simplify tool arguments for a retry attempt."""
        simplified = dict(args)
        if tool == "execute":
            cmd = simplified.get("command", "")
            # Remove potentially dangerous flags
            for flag in ["-rf", "--force", "sudo"]:
                cmd = cmd.replace(flag, "")
            simplified["command"] = cmd.strip()
        elif tool == "write":
            content = simplified.get("content", "")
            if len(content) > 10000:
                simplified["content"] = content[:10000] + "\n... [truncated for retry]"
        return simplified

    def _suggest_alternative(
        self,
        tool: str,
        args: dict[str, Any],
        error: str,
    ) -> dict[str, Any]:
        """Suggest an alternative tool/approach."""
        alternatives: dict[str, dict[str, Any]] = {
            "execute": {"tool": "read", "args": {"path": args.get("path", ".")}},
            "write": {"tool": "write", "args": {**args, "content": "# Placeholder\n"}},
            "edit": {"tool": "write", "args": {"path": args.get("path", ""), "content": ""}},
        }
        alt = alternatives.get(tool)
        if alt:
            result: dict[str, Any] = alt.get("args", {})
            return result
        return args

    # ── Persistence ────────────────────────────────────────────────

    def _save_history(self) -> None:
        history_file = self.history_dir / "success_history.json"
        data = {
            tool: list(history)
            for tool, history in self._success_history.items()
        }
        history_file.write_text(json.dumps(data), encoding="utf-8")

    def _load_history(self) -> None:
        history_file = self.history_dir / "success_history.json"
        if not history_file.exists():
            return
        try:
            data = json.loads(history_file.read_text(encoding="utf-8"))
            for tool, history in data.items():
                self._success_history[tool] = deque(history, maxlen=self._max_history)
        except (json.JSONDecodeError, OSError):
            pass

    def _save_decision_log(self) -> None:
        log_file = self.history_dir / "decision_log.jsonl"
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                latest = self._decision_log[-1]
                f.write(json.dumps(latest, default=str) + "\n")
        except OSError:
            pass
