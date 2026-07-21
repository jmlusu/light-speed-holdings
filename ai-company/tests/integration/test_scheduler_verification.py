"""Integration tests — scheduler verification (Phase 3C).

Validates the Executor's Scheduler and ConsolidationScheduler wiring:
1. Scheduler initialization and stats
2. Tick count increments across executor ticks
3. ConsolidationScheduler stats and config defaults
4. Consolidation runs after task processing
5. ConsolidationConfig has reasonable defaults
"""

from __future__ import annotations

import json

from ai_company.llm.providers.base import ChatResponse
from ai_company.memory.consolidation import ConsolidationConfig, ConsolidationScheduler
from ai_company.models.task import Task, TaskPriority
from ai_company.orchestrator.message_bus import MessageBus
from ai_company.orchestrator.scheduler import Scheduler


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_chat_response(content: str = "") -> ChatResponse:
    """Create a ChatResponse with the given content and default usage stats."""
    return ChatResponse(
        content=content,
        model="test-model",
        provider="test-provider",
        prompt_tokens=50,
        completion_tokens=50,
        total_tokens=100,
        usage={"prompt_tokens": 50, "completion_tokens": 50},
    )


def _react_response(result: str, done: bool = True) -> ChatResponse:
    """Build a ChatResponse whose content is valid ReAct JSON."""
    payload = json.dumps({
        "thought": "Done",
        "plan": [],
        "result": result,
        "done": done,
    })
    return _make_chat_response(content=payload)


def _patch_agent_loop_llm(response: ChatResponse):
    """Context manager that patches AgentLoop._call_llm to return fixed response."""
    from unittest.mock import patch

    return patch(
        "ai_company.executor.agent_loop.AgentLoop._call_llm",
        return_value=response,
    )


def _submit_task(bus: MessageBus, task_id: str, instruction: str = "test task") -> Task:
    """Submit a task to the message bus and return it."""
    task = Task(
        id=task_id,
        sender_id="human-ceo",
        receiver_id="test-agent",
        instruction=instruction,
        priority=TaskPriority.MEDIUM,
    )
    bus.send_task(task)
    return task


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestSchedulerInitialization:
    """Verify Executor wires up the Scheduler correctly."""

    def test_scheduler_initializes(self, executor, bus: MessageBus) -> None:
        """Executor has a scheduler instance; scheduler list_tasks returns valid list."""
        # 1. Executor has a Scheduler instance
        assert hasattr(executor, "scheduler")
        assert isinstance(executor.scheduler, Scheduler)

        # 2. Scheduler starts with an empty task list (no scheduled tasks in workspace)
        tasks = executor.scheduler.list_tasks()
        assert isinstance(tasks, list)

        # 3. Executor stats (companion to scheduler) return valid dict
        stats = executor.stats.to_dict()
        assert isinstance(stats, dict)
        assert "tasks_processed" in stats
        assert "tasks_succeeded" in stats
        assert "tasks_failed" in stats
        assert "uptime_seconds" in stats
        assert "running" in stats

    def test_scheduler_tick_increments(self, executor, bus: MessageBus) -> None:
        """Each executor.tick() increments the consolidation scheduler tick_count.

        The Executor's tick() calls ``_consolidation_scheduler.on_tick()``
        which increments its internal tick counter on every pass.
        """
        consolidation = executor._consolidation_scheduler
        assert isinstance(consolidation, ConsolidationScheduler)

        initial_tick = consolidation.tick_count

        # First tick with empty inbox
        count1 = executor.tick()
        assert count1 == 0
        assert consolidation.tick_count == initial_tick + 1

        # Second tick — tick_count should increment again
        count2 = executor.tick()
        assert count2 == 0
        assert consolidation.tick_count == initial_tick + 2


class TestConsolidationScheduler:
    """Verify ConsolidationScheduler stats and config wiring."""

    def test_consolidation_scheduler_stats(self, executor, bus: MessageBus) -> None:
        """Consolidation scheduler stats() returns expected keys."""
        stats = executor._consolidation_scheduler.stats()
        assert isinstance(stats, dict)

        expected_keys = {
            "tick_count",
            "last_consolidated",
            "running",
            "tick_interval",
            "time_interval_seconds",
            "entry_threshold",
        }
        assert expected_keys.issubset(set(stats.keys())), (
            f"Missing keys: {expected_keys - set(stats.keys())}"
        )

        # Initial state
        assert stats["tick_count"] == 0
        assert stats["last_consolidated"] is None
        assert stats["running"] is False

    def test_consolidation_runs_after_tasks(
        self, executor, bus: MessageBus
    ) -> None:
        """After processing tasks, the consolidation scheduler has ticked.

        Each executor.tick() calls _consolidation_scheduler.on_tick(),
        which increments the tick counter regardless of whether consolidation
        actually runs.
        """
        consolidation = executor._consolidation_scheduler
        assert consolidation.tick_count == 0

        # Submit and process a task
        with _patch_agent_loop_llm(_react_response("Task done")):
            _submit_task(bus, "consol-001", "Verify consolidation runs")
            executor.tick()

        # Tick count should be 1 after one tick
        assert consolidation.tick_count == 1

        # Process another task to confirm monotonicity
        with _patch_agent_loop_llm(_react_response("Second task done")):
            _submit_task(bus, "consol-002", "Second consolidation check")
            executor.tick()

        assert consolidation.tick_count == 2

        # Stats should reflect the updated tick count
        stats = consolidation.stats()
        assert stats["tick_count"] == 2

    def test_consolidation_config_defaults(self) -> None:
        """ConsolidationConfig() has reasonable defaults for tick/time thresholds."""
        config = ConsolidationConfig()

        # Tick-based: run consolidation every 50 executor ticks
        assert isinstance(config.tick_interval, int)
        assert config.tick_interval > 0, "tick_interval should be positive"
        assert config.tick_interval == 50

        # Time-based: run consolidation every hour (3600 seconds)
        assert isinstance(config.time_interval_seconds, int)
        assert config.time_interval_seconds > 0, "time_interval_seconds should be positive"
        assert config.time_interval_seconds == 3600

        # Entry threshold for triggering consolidation on memory growth
        assert isinstance(config.entry_threshold, int)
        assert config.entry_threshold > 0, "entry_threshold should be positive"
        assert config.entry_threshold == 500

        # Episodic pruning: keep memories for 90 days
        assert isinstance(config.max_episodic_age_days, int)
        assert config.max_episodic_age_days > 0
        assert config.max_episodic_age_days == 90

        # Max entries per memory type
        assert isinstance(config.max_entries_per_type, int)
        assert config.max_entries_per_type > 0
        assert config.max_entries_per_type == 2000

    def test_consolidation_scheduler_custom_config(self) -> None:
        """ConsolidationScheduler accepts custom ConsolidationConfig values."""
        custom = ConsolidationConfig(
            tick_interval=10,
            time_interval_seconds=600,
            entry_threshold=100,
        )
        scheduler = ConsolidationScheduler(store=None, config=custom)

        stats = scheduler.stats()
        assert stats["tick_interval"] == 10
        assert stats["time_interval_seconds"] == 600
        assert stats["entry_threshold"] == 100

    def test_consolidation_scheduler_tracks_last_consolidated(
        self, executor, bus: MessageBus
    ) -> None:
        """Consolidation scheduler records last_consolidated after run_once."""
        consolidation = executor._consolidation_scheduler

        # Before any ticks, last_consolidated is None
        assert consolidation.last_consolidated is None

        # After a tick (tick_interval=50, so no consolidation runs yet)
        executor.tick()
        assert consolidation.last_consolidated is None

        # Force a single consolidation run via on_tick with low interval
        consolidation._config.tick_interval = 1
        executor.tick()

        # Now consolidation should have run
        assert consolidation.last_consolidated is not None
