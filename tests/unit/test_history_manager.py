"""Tests for ConversationHistoryManager triggers, metrics, and summarization."""

from __future__ import annotations

from unittest.mock import MagicMock

from ai_company.executor.history_manager import (
    ConversationHistoryManager,
    create_history_manager,
)


def _make_manager(**kwargs) -> ConversationHistoryManager:
    """Create a history manager with small budgets so summarization triggers quickly."""
    defaults = dict(
        llm=None,
        max_full_turns=3,
        max_summary_tokens=500,
        max_total_tokens=6000,
        trigger_token_threshold=30000,
        trigger_cache_hit_rate=0.70,
        trigger_consecutive_failures=5,
        trigger_tool_call_count=20,
    )
    defaults.update(kwargs)
    return ConversationHistoryManager(**defaults)


class TestCacheTracking:
    def test_cache_hit_rate_defaults_to_one(self):
        m = _make_manager()
        assert m.cache_hit_rate == 1.0

    def test_record_cache_hit_increments(self):
        m = _make_manager()
        m.record_cache_hit()
        m.record_cache_hit()
        assert m.cache_hit_rate == 1.0
        assert m.get_metrics()["cache_hits"] == 2

    def test_record_cache_miss_lowers_rate(self):
        m = _make_manager()
        for _ in range(3):
            m.record_cache_hit()
        for _ in range(7):
            m.record_cache_miss()
        assert m.cache_hit_rate == 0.3
        assert m.get_metrics()["cache_misses"] == 7

    def test_mixed_hits_and_misses(self):
        m = _make_manager()
        for _ in range(7):
            m.record_cache_hit()
        for _ in range(3):
            m.record_cache_miss()
        assert m.cache_hit_rate == 0.7


class TestFailureTracking:
    def test_successful_feedback_resets_streak(self):
        m = _make_manager()
        m.add_tool_feedback("Operation completed successfully")
        assert m.consecutive_failures == 0
        assert m.tool_call_count == 1

    def test_error_feedback_increments_streak(self):
        m = _make_manager()
        m.add_tool_feedback("ERROR: something failed")
        m.add_tool_feedback("command exited with error")
        assert m.consecutive_failures == 2
        assert m.tool_call_count == 2

    def test_success_breaks_streak(self):
        m = _make_manager()
        m.add_tool_feedback("failed to open file")
        m.add_tool_feedback("exception in handler")
        m.add_tool_feedback("all good now")
        assert m.consecutive_failures == 0
        assert m.tool_call_count == 3

    def test_denied_and_exit1_are_failures(self):
        m = _make_manager()
        m.add_tool_feedback("Permission denied by approval gate")
        m.add_tool_feedback("process exited with exit 1")
        assert m.consecutive_failures == 2


class TestTriggerConditions:
    def test_token_threshold_triggers_summarization(self):
        m = _make_manager(
            max_full_turns=2,
            max_total_tokens=6000,
            trigger_token_threshold=100,
        )
        # Add turns with long text to exceed the tiny token threshold
        for i in range(5):
            m.add_turn(f"User message {i} " + "filler text " * 50)
        assert m.total_summarizations > 0

    def test_failure_streak_triggers_summarization(self):
        m = _make_manager(max_full_turns=2, trigger_consecutive_failures=3)
        # Seed enough history so max_full_turns gate is passed
        for i in range(5):
            m.add_turn(f"turn {i}")
        # Now cause consecutive failures
        for _ in range(3):
            m.add_tool_feedback("ERROR: failed")
        assert m.total_summarizations > 0
        # Streak is reset after summarization
        assert m.consecutive_failures == 0

    def test_tool_call_count_triggers_summarization(self):
        m = _make_manager(max_full_turns=2, trigger_tool_call_count=4)
        for i in range(5):
            m.add_turn(f"turn {i}")
        for _ in range(4):
            m.add_tool_feedback("did something fine")
        assert m.total_summarizations > 0

    def test_no_summarization_below_max_full_turns(self):
        m = _make_manager(max_full_turns=10, trigger_token_threshold=1)
        m.add_turn("short message")
        m.add_turn("another short message")
        assert m.total_summarizations == 0


class TestSummarization:
    def test_total_summarizations_increments(self):
        m = _make_manager(max_full_turns=2, trigger_tool_call_count=3)
        for i in range(6):
            m.add_turn(f"turn {i}")
        for _ in range(3):
            m.add_tool_feedback("op failed")
        assert m.total_summarizations >= 1

    def test_summary_preserved_in_context(self):
        m = _make_manager(
            max_full_turns=2,
            max_total_tokens=10,
            trigger_token_threshold=10,
        )
        # Force enough text to trigger
        for i in range(6):
            m.add_turn(f"Task goal: implement feature {i} in path: src/module.py")
        ctx = m.get_context()
        assert ctx  # non-empty
        # After summarization, summary section appears
        assert m.total_summarizations >= 1
        assert "Conversation Summary" in ctx
        assert "--- Recent History ---" in ctx

    def test_tool_call_count_decrements_after_summarize(self):
        m = _make_manager(max_full_turns=2, trigger_tool_call_count=5)
        for i in range(4):
            m.add_turn(f"turn {i}")
        for _ in range(5):
            m.add_tool_feedback("ok")
        # After summarization, count is reset to zero
        assert m.total_summarizations >= 1
        assert m.tool_call_count == 0

    def test_zero_max_full_turns_keeps_none(self):
        m = _make_manager(max_full_turns=0, trigger_tool_call_count=3)
        for i in range(4):
            m.add_turn(f"turn {i}")
        for _ in range(3):
            m.add_tool_feedback("ok")
        assert m.total_summarizations >= 1
        assert m.get_metrics()["full_history_turns"] == 0
        assert "Conversation Summary" in m.get_context()


class TestMetricsAndReset:
    def test_get_metrics_structure(self):
        m = _make_manager()
        m.add_turn("hello")
        m.record_cache_hit()
        m.add_tool_feedback("some output")
        metrics = m.get_metrics()
        assert set(metrics) >= {
            "tool_call_count",
            "consecutive_failures",
            "cache_hit_rate",
            "cache_hits",
            "cache_misses",
            "total_summarizations",
            "full_history_turns",
            "current_token_estimate",
            "summary_token_estimate",
        }

    def test_reset_clears_everything(self):
        m = _make_manager()
        m.add_turn("work")
        m.add_tool_feedback("ERROR: boom")
        m.record_cache_miss()
        m.reset()
        assert m.get_metrics()["tool_call_count"] == 0
        assert m.get_metrics()["cache_hits"] == 0
        assert m.get_metrics()["cache_misses"] == 0
        assert m.get_metrics()["total_summarizations"] == 0
        assert m.get_context() == ""


class TestFactory:
    def test_factory_defaults(self):
        m = create_history_manager()
        assert m.max_full_turns == 3
        assert m.trigger_token_threshold == 30000
        assert m.trigger_cache_hit_rate == 0.70
        assert m.trigger_consecutive_failures == 5
        assert m.trigger_tool_call_count == 20

    def test_factory_custom_config(self):
        m = create_history_manager(
            config={
                "max_full_turns": 5,
                "trigger_token_threshold": 5000,
                "trigger_cache_hit_rate": 0.5,
                "trigger_consecutive_failures": 3,
                "trigger_tool_call_count": 10,
            },
            task_id="t-123",
        )
        assert m.max_full_turns == 5
        assert m.trigger_token_threshold == 5000
        assert m.trigger_cache_hit_rate == 0.5
        assert m.trigger_consecutive_failures == 3
        assert m.trigger_tool_call_count == 10
        assert m.task_id == "t-123"

    def test_factory_with_llm_mock(self):
        mock_llm = MagicMock()
        m = create_history_manager(llm=mock_llm)
        assert m.llm is mock_llm
