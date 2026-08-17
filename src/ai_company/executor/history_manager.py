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
    """

    def __init__(
        self,
        llm: LLMClient | None = None,
        max_full_turns: int = 3,
        max_summary_tokens: int = 1000,
        max_total_tokens: int = 6000,
    ):
        self.llm = llm
        self.max_full_turns = max_full_turns
        self.max_summary_tokens = max_summary_tokens
        self.max_total_tokens = max_total_tokens
        self._summary: str = ""
        self._full_history: list[str] = []  # Recent turns kept in full

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
        self._maybe_summarize()

    def _maybe_summarize(self) -> None:
        """Check if summarization is needed and trigger it."""
        if len(self._full_history) <= self.max_full_turns:
            return

        # Estimate tokens
        total_text = "\n\n".join(self._full_history)
        estimated_tokens = count_tokens(total_text)

        if estimated_tokens > self.max_total_tokens:
            self._summarize_old_turns()

    def _summarize_old_turns(self) -> None:
        """Summarize older turns, keeping only recent ones in full."""
        if len(self._full_history) <= self.max_full_turns:
            return

        # Split into old and recent
        old_turns = self._full_history[: -self.max_full_turns]
        recent_turns = self._full_history[-self.max_full_turns :]

        # Create summary of old turns
        old_text = "\n\n".join(old_turns)
        summary = self._create_summary(old_text)

        # Update state
        self._summary = summary
        self._full_history = recent_turns

        logger.debug(
            "Summarized %d old turns into %d tokens", len(old_turns), count_tokens(summary)
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
            )

            # Extract result from parsed JSON or use raw
            if isinstance(response, dict) and "result" in response:
                return str(response["result"])
            return str(response)[: self.max_summary_tokens]
        except (LLMProviderError, LLMResponseError, KeyError, TypeError) as e:
            logger.warning("LLM summarization failed, using heuristic: %s", e)
            return self._heuristic_summarize(text)

    def _heuristic_summarize(self, text: str) -> str:
        """Heuristic summarization — extract key information without LLM."""
        lines = text.split("\n")
        key_info: list[str] = []

        # Extract key patterns
        for line in lines:
            line_lower = line.lower()
            # File operations
            if any(kw in line_lower for kw in ["read", "edit", "write", "file", "path:"]):
                if len(line) < 200:  # Skip huge outputs
                    key_info.append(line.strip())
            # Errors
            elif any(kw in line_lower for kw in ["error", "failed", "exception", "traceback"]):
                key_info.append(line.strip()[:200])
            # Tool results
            elif any(
                kw in line_lower for kw in ["tool:", "step", "status: ok", "status: error"]
            ) or any(kw in line_lower for kw in ["done", "complete", "finished", "result:"]):
                key_info.append(line.strip()[:150])

        # Limit summary size
        summary_lines = key_info[-20:]  # Last 20 key items
        summary = "Conversation Summary:\n" + "\n".join(summary_lines)

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

    def get_token_estimate(self) -> int:
        """Estimate total tokens in current context."""
        return count_tokens(self.get_context())

    def reset(self) -> None:
        """Reset history."""
        self._summary = ""
        self._full_history = []


def create_history_manager(
    llm: LLMClient | None = None,
    config: dict[str, Any] | None = None,
) -> ConversationHistoryManager:
    """Factory function to create a history manager with config."""
    cfg = config or {}
    return ConversationHistoryManager(
        llm=llm,
        max_full_turns=cfg.get("max_full_turns", 3),
        max_summary_tokens=cfg.get("max_summary_tokens", 1000),
        max_total_tokens=cfg.get("max_total_tokens", 6000),
    )
