"""Conversation history management — summarization and token-aware truncation."""

from __future__ import annotations

import logging
from typing import Any

from ai_company.llm.client import LLMClient
from ai_company.llm.providers.base import LLMProviderError, LLMResponseError
from ai_company.llm.token_counter import count_tokens

logger = logging.getLogger(__name__)


class ConversationHistoryManager:
    """Manages conversation history with automatic summarization to stay within token budgets.

    Strategy:
    - Keep last N turns in full detail
    - Summarize older turns into a compact summary
    - Automatically trigger summarization when token budget is exceeded
    - Preserve critical information (errors, decisions, file paths)
    - Track tool-call patterns and consecutive failures
    - Trigger summarization on multiple conditions: token count, cache efficiency, failure streaks
    """

    def __init__(
        self,
        llm: LLMClient | None = None,
        max_full_turns: int = 3,
        max_summary_tokens: int = 1000,
        max_total_tokens: int = 6000,
        task_id: str = "",
        trigger_token_threshold: int = 30000,
        trigger_cache_hit_rate: float = 0.70,
        trigger_consecutive_failures: int = 5,
        trigger_tool_call_count: int = 20,
    ):
        self.llm = llm
        self.max_full_turns = max_full_turns
        self.max_summary_tokens = max_summary_tokens
        self.max_total_tokens = max_total_tokens
        # Task ID for cost attribution — summarizer LLM calls only get
        # recorded in cost_tracker when they carry the owning task_id.
        self.task_id = task_id
        self._summary: str = ""
        self._full_history: list[str] = []  # Recent turns kept in full

        # ── Enhanced trigger conditions ──
        self.trigger_token_threshold = trigger_token_threshold
        self.trigger_cache_hit_rate = trigger_cache_hit_rate
        self.trigger_consecutive_failures = trigger_consecutive_failures
        self.trigger_tool_call_count = trigger_tool_call_count

        # ── Metrics tracking ──
        self._tool_call_count: int = 0
        self._consecutive_failures: int = 0
        self._cache_hits: int = 0
        self._cache_misses: int = 0
        self._total_summarizations: int = 0

    def add_turn(self, user_message: str, assistant_response: str = "") -> None:
        """Add a conversation turn."""
        turn = f"User: {user_message}"
        if assistant_response:
            turn += f"\nAssistant: {assistant_response}"
        self._full_history.append(turn)
        self._maybe_summarize()

    def add_tool_feedback(self, feedback: str) -> None:
        """Add tool execution feedback as a turn."""
        self._full_history.append(f"Tool Feedback: {feedback}")
        self._track_tool_call(feedback)
        self._maybe_summarize()

    def record_cache_hit(self) -> None:
        """Record a prefix cache hit (for cache efficiency tracking)."""
        self._cache_hits += 1

    def record_cache_miss(self) -> None:
        """Record a prefix cache miss."""
        self._cache_misses += 1

    @property
    def cache_hit_rate(self) -> float:
        """Calculate current cache hit rate."""
        total = self._cache_hits + self._cache_misses
        if total == 0:
            return 1.0
        return self._cache_hits / total

    @property
    def tool_call_count(self) -> int:
        """Total tool calls tracked."""
        return self._tool_call_count

    @property
    def consecutive_failures(self) -> int:
        """Current consecutive failure streak."""
        return self._consecutive_failures

    @property
    def total_summarizations(self) -> int:
        """Number of summarizations performed."""
        return self._total_summarizations

    def _track_tool_call(self, feedback: str) -> None:
        """Track tool call count and consecutive failure streak."""
        self._tool_call_count += 1
        feedback_lower = feedback.lower()
        if any(kw in feedback_lower for kw in ["error", "failed", "exception", "denied", "exit 1"]):
            self._consecutive_failures += 1
        else:
            self._consecutive_failures = 0

    def _maybe_summarize(self) -> None:
        """Check all trigger conditions and summarize if any is met.

        Token figures are approximate estimates from count_tokens (tool
        outputs are truncated and summaries are not counted); they gate
        triggering only, while max_total_tokens bounds the live history.
        """
        if len(self._full_history) <= self.max_full_turns:
            return

        total_text = "\n\n".join(self._full_history)
        estimated_tokens = count_tokens(total_text)

        # Trigger condition 1: Token threshold exceeded
        tokens_exceeded = estimated_tokens > self.trigger_token_threshold

        # Trigger condition 2: Cache hit rate degraded
        cache_degraded = (
            self._cache_hits + self._cache_misses > 5
            and self.cache_hit_rate < self.trigger_cache_hit_rate
        )

        # Trigger condition 3: Consecutive failure streak
        failure_streak = self._consecutive_failures >= self.trigger_consecutive_failures

        # Trigger condition 4: Too many tool calls
        too_many_tool_calls = self._tool_call_count >= self.trigger_tool_call_count

        # Also keep the original budget check
        budget_exceeded = estimated_tokens > self.max_total_tokens

        if (
            tokens_exceeded
            or cache_degraded
            or failure_streak
            or too_many_tool_calls
            or budget_exceeded
        ):
            logger.debug(
                "Summarization triggered: tokens=%d (thr=%d), cache_rate=%.2f (thr=%.2f), "
                "failures=%d (thr=%d), tool_calls=%d (thr=%d), budget=%d (thr=%d)",
                estimated_tokens,
                self.trigger_token_threshold,
                self.cache_hit_rate,
                self.trigger_cache_hit_rate,
                self._consecutive_failures,
                self.trigger_consecutive_failures,
                self._tool_call_count,
                self.trigger_tool_call_count,
                estimated_tokens,
                self.max_total_tokens,
            )
            self._summarize_old_turns()

    def _summarize_old_turns(self) -> None:
        """Summarize older turns, keeping only recent ones in full."""
        if len(self._full_history) <= self.max_full_turns:
            return

        # Split into old and recent
        if self.max_full_turns <= 0:
            old_turns = list(self._full_history)
            recent_turns: list[str] = []
        else:
            old_turns = self._full_history[: -self.max_full_turns]
            recent_turns = self._full_history[-self.max_full_turns :]

        # Create summary of old turns
        old_text = "\n\n".join(old_turns)
        new_summary = self._create_summary(old_text)

        # Merge with existing summary to avoid losing earlier context
        if self._summary:
            self._summary = f"{self._summary}\n{new_summary}"
            # Re-truncate merged summary if it grows too large
            if count_tokens(self._summary) > self.max_summary_tokens * 2:
                self._summary = self._summary[-self.max_summary_tokens * 8 :]
        else:
            self._summary = new_summary

        # Update state
        self._full_history = recent_turns
        self._total_summarizations += 1

        # Reset tool-call tracking after summarization — all tracked calls
        # now live in the summarized older turns, so the count restarts at
        # zero with the retained recent context, like the sibling counters.
        self._tool_call_count = 0
        self._consecutive_failures = 0
        self._cache_hits = 0
        self._cache_misses = 0

        logger.debug(
            "Summarized %d old turns into %d tokens (total summarizations: %d)",
            len(old_turns),
            count_tokens(self._summary),
            self._total_summarizations,
        )

    def _create_summary(self, text: str) -> str:
        """Create a concise summary of conversation history.

        Uses LLM if available, otherwise falls back to heuristic extraction.
        """
        if self.llm:
            return self._llm_summarize(text)
        return self._heuristic_summarize(text)

    def _llm_summarize(self, text: str) -> str:
        """Use LLM to create a summary."""
        if self.llm is None:
            return self._heuristic_summarize(text)
        try:
            prompt = (
                "Summarize the following conversation history for a coding agent. "
                "Focus on: key decisions made, files modified, errors encountered and resolved, "
                "current task state, and any pending actions. Be concise.\n\n"
                f"{text}\n\n"
                "Summary:"
            )

            # Use a simple completion (non-streaming)
            response = self.llm.execute_task(
                agent_name="summarizer",
                task_instruction=prompt,
                priority="low",
                system_prompt="You are a concise summarizer for agent conversation history.",
                max_retries=2,
                task_id=self.task_id,
            )

            # Extract result from parsed JSON or use raw
            if isinstance(response, dict) and "result" in response:
                return str(response["result"])
            return str(response)[: self.max_summary_tokens]
        except (LLMProviderError, LLMResponseError, KeyError, TypeError) as e:
            logger.warning("LLM summarization failed, using heuristic: %s", e)
            return self._heuristic_summarize(text)

    def _heuristic_summarize(self, text: str) -> str:
        """Heuristic summarization — extract key information without LLM.

        Preserves: task goal, file paths, decisions, errors, successful tool outputs.
        Compresses: verbose errors, repeated listings, intermediate reasoning.
        """
        lines = text.split("\n")
        key_info: list[str] = []
        file_paths: set[str] = set()
        decisions: list[str] = []
        errors: list[str] = []
        successes: list[str] = []

        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
            line_lower = line_stripped.lower()

            # Preserve file paths (extract and deduplicate)
            if any(
                kw in line_lower
                for kw in ["path:", "file:", ".py", ".js", ".ts", ".md", ".json", ".yaml"]
            ):
                if len(line_stripped) < 200:
                    key_info.append(line_stripped)
                    # Extract path-like tokens
                    for word in line_stripped.split():
                        if ("/" in word or "\\" in word or "." in word) and 3 < len(word) < 120:
                            file_paths.add(word.strip(".,;:()[]{}\"'"))

            # Preserve errors (but compress verbose stack traces)
            elif any(
                kw in line_lower for kw in ["error", "failed", "exception", "traceback", "denied"]
            ):
                # Compress: keep first line of error only
                compressed = line_stripped[:150]
                if compressed not in errors:
                    errors.append(compressed)

            # Preserve successful tool outcomes
            elif any(
                kw in line_lower
                for kw in ["status: ok", "done", "complete", "finished", "success", "ok ("]
            ):
                if len(line_stripped) < 150:
                    successes.append(line_stripped)

            # Preserve decisions and task state
            elif (
                any(
                    kw in line_lower
                    for kw in ["decision", "plan", "next", "task", "goal", "objective", "approach"]
                )
                and len(line_stripped) < 200
            ):
                decisions.append(line_stripped)

        # Build summary preserving priority order: task goal > decisions > errors > successes > paths
        summary_parts: list[str] = ["Conversation Summary:"]

        if decisions:
            summary_parts.append("Key decisions/state:")
            summary_parts.extend(decisions[-10:])

        if errors:
            summary_parts.append("Errors encountered:")
            summary_parts.extend(errors[-8:])

        if successes:
            summary_parts.append("Successful operations:")
            summary_parts.extend(successes[-8:])

        if file_paths:
            summary_parts.append(f"Files touched ({len(file_paths)}):")
            # Show up to 15 file paths
            for fp in sorted(file_paths)[:15]:
                summary_parts.append(f"  {fp}")

        # Fallback: if nothing extracted, keep last few lines
        if len(summary_parts) == 1:
            summary_parts.append("Recent activity:")
            summary_parts.extend(line.strip()[:100] for line in lines[-10:] if line.strip())

        summary = "\n".join(summary_parts)

        # Truncate if still too long
        if count_tokens(summary) > self.max_summary_tokens:
            summary = summary[: self.max_summary_tokens * 4] + "... [truncated]"

        return summary

    def get_context(self) -> str:
        """Get the full context for the next LLM call."""
        parts = []
        if self._summary:
            parts.append(self._summary)
            parts.append("--- Recent History ---")
        parts.extend(self._full_history)
        return "\n\n".join(parts)

    def get_metrics(self) -> dict[str, Any]:
        """Return current metrics for observability."""
        return {
            "tool_call_count": self._tool_call_count,
            "consecutive_failures": self._consecutive_failures,
            "cache_hit_rate": round(self.cache_hit_rate, 3),
            "cache_hits": self._cache_hits,
            "cache_misses": self._cache_misses,
            "total_summarizations": self._total_summarizations,
            "full_history_turns": len(self._full_history),
            "current_token_estimate": self.get_token_estimate(),
            "summary_token_estimate": count_tokens(self._summary) if self._summary else 0,
        }

    def get_token_estimate(self) -> int:
        """Estimate total tokens in current context."""
        return count_tokens(self.get_context())

    def reset(self) -> None:
        """Reset history."""
        self._summary = ""
        self._full_history = []
        self._tool_call_count = 0
        self._consecutive_failures = 0
        self._cache_hits = 0
        self._cache_misses = 0
        self._total_summarizations = 0


def create_history_manager(
    llm: LLMClient | None = None,
    config: dict[str, Any] | None = None,
    task_id: str = "",
) -> ConversationHistoryManager:
    """Factory function to create a history manager with config."""
    cfg = config or {}
    return ConversationHistoryManager(
        llm=llm,
        max_full_turns=cfg.get("max_full_turns", 3),
        max_summary_tokens=cfg.get("max_summary_tokens", 1000),
        max_total_tokens=cfg.get("max_total_tokens", 6000),
        task_id=task_id,
        trigger_token_threshold=cfg.get("trigger_token_threshold", 30000),
        trigger_cache_hit_rate=cfg.get("trigger_cache_hit_rate", 0.70),
        trigger_consecutive_failures=cfg.get("trigger_consecutive_failures", 5),
        trigger_tool_call_count=cfg.get("trigger_tool_call_count", 20),
    )
