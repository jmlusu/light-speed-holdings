"""Tests for idempotency guarantees in MessageBus and CostAnalytics.

QW-1: MessageBus.send_task() deduplicates by task ID.
QW-3: CostAnalytics.record_usage() deduplicates by composite key.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pytest

from ai_company.data.cost_analytics import CostAnalytics
from ai_company.data.database import Database
from ai_company.models.task import Task
from ai_company.orchestrator.message_bus import MessageBus


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def db(tmp_path: Path) -> Database:
    """Create a temporary database with schema."""
    database = Database(tmp_path / "test_idempotency.db")
    database.init_schema()
    yield database
    database.close()


@pytest.fixture
def cost_analytics(db: Database) -> CostAnalytics:
    """Create a CostAnalytics backed by the test database."""
    return CostAnalytics(db)


# ---------------------------------------------------------------------------
# QW-1 — MessageBus.send_task() deduplication
# ---------------------------------------------------------------------------


class TestMessageBusDeduplication:
    """send_task() must skip duplicates with the same task ID."""

    def test_send_task_deduplicates_by_id(self, tmp_path: Path) -> None:
        """Sending the same task twice should result in only one entry."""
        bus = MessageBus(storage_path=str(tmp_path / "inbox.json"))
        task = Task(
            id="dedup-1",
            sender_id="agent-a",
            receiver_id="agent-b",
            instruction="do something",
        )

        bus.send_task(task)
        bus.send_task(task)  # duplicate

        all_tasks = bus.get_all_tasks()
        assert len(all_tasks) == 1
        assert all_tasks[0].id == "dedup-1"

    def test_send_task_different_ids(self, tmp_path: Path) -> None:
        """Tasks with different IDs should both be stored."""
        bus = MessageBus(storage_path=str(tmp_path / "inbox.json"))
        task_a = Task(
            id="unique-a",
            sender_id="agent-a",
            receiver_id="agent-b",
            instruction="task A",
        )
        task_b = Task(
            id="unique-b",
            sender_id="agent-a",
            receiver_id="agent-b",
            instruction="task B",
        )

        bus.send_task(task_a)
        bus.send_task(task_b)

        all_tasks = bus.get_all_tasks()
        assert len(all_tasks) == 2
        ids = {t.id for t in all_tasks}
        assert ids == {"unique-a", "unique-b"}

    def test_send_task_logs_warning_on_duplicate(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A duplicate send should log a warning message."""
        bus = MessageBus(storage_path=str(tmp_path / "inbox.json"))
        task = Task(
            id="warn-dup",
            sender_id="agent-a",
            receiver_id="agent-b",
            instruction="test warning",
        )

        bus.send_task(task)
        with caplog.at_level(logging.WARNING, logger="ai_company.orchestrator.message_bus"):
            bus.send_task(task)  # duplicate

        assert "already exists in inbox" in caplog.text
        assert "warn-dup" in caplog.text

    def test_send_task_does_not_emit_broadcast_for_duplicate(
        self, tmp_path: Path
    ) -> None:
        """Duplicate send_task should not fire the broadcast callback."""
        events: list[tuple[dict, str]] = []

        def callback(task_dict: dict[str, str], event: str) -> None:
            events.append((task_dict, event))

        bus = MessageBus(
            storage_path=str(tmp_path / "inbox.json"),
            broadcast_callback=callback,
        )
        task = Task(
            id="no-broadcast-dup",
            sender_id="agent-a",
            receiver_id="agent-b",
            instruction="test",
        )

        bus.send_task(task)  # first — fires "created"
        bus.send_task(task)  # duplicate — should NOT fire

        assert len(events) == 1
        assert events[0][1] == "created"

    def test_send_task_after_completion_still_deduplicates(
        self, tmp_path: Path
    ) -> None:
        """Even after a task is completed, sending the same ID should be skipped."""
        bus = MessageBus(storage_path=str(tmp_path / "inbox.json"))
        task = Task(
            id="completed-dup",
            sender_id="agent-a",
            receiver_id="agent-b",
            instruction="test",
        )

        bus.send_task(task)
        bus.update_task_status("completed-dup", "completed")
        bus.send_task(task)  # should be skipped

        all_tasks = bus.get_all_tasks()
        assert len(all_tasks) == 1
        assert all_tasks[0].status.value == "completed"


# ---------------------------------------------------------------------------
# QW-3 — CostAnalytics.record_usage() deduplication
# ---------------------------------------------------------------------------


class TestCostAnalyticsDeduplication:
    """record_usage() must deduplicate identical records."""

    def test_record_usage_deduplicates_identical_call(
        self, cost_analytics: CostAnalytics
    ) -> None:
        """Recording the same usage twice should return the same row ID."""
        row_id_1 = cost_analytics.record_usage(
            model="gpt-4o",
            provider="openai",
            agent_name="agent-a",
            task_id="task-dedup",
            prompt_tokens=100,
            completion_tokens=50,
            cost_usd=0.01,
            iteration=1,
        )
        row_id_2 = cost_analytics.record_usage(
            model="gpt-4o",
            provider="openai",
            agent_name="agent-a",
            task_id="task-dedup",
            prompt_tokens=100,
            completion_tokens=50,
            cost_usd=0.01,
            iteration=1,
        )

        assert row_id_1 == row_id_2
        assert cost_analytics.total_records() == 1

    def test_record_usage_allows_different_iterations(
        self, cost_analytics: CostAnalytics
    ) -> None:
        """Different iterations of the same call should create separate records."""
        row_id_1 = cost_analytics.record_usage(
            model="gpt-4o",
            provider="openai",
            agent_name="agent-a",
            task_id="task-iter",
            prompt_tokens=100,
            completion_tokens=50,
            cost_usd=0.01,
            iteration=1,
        )
        row_id_2 = cost_analytics.record_usage(
            model="gpt-4o",
            provider="openai",
            agent_name="agent-a",
            task_id="task-iter",
            prompt_tokens=200,
            completion_tokens=80,
            cost_usd=0.02,
            iteration=2,
        )

        assert row_id_1 != row_id_2
        assert cost_analytics.total_records() == 2

    def test_record_usage_allows_same_task_different_models(
        self, cost_analytics: CostAnalytics
    ) -> None:
        """Same task but different models should create separate records."""
        row_id_1 = cost_analytics.record_usage(
            model="gpt-4o",
            provider="openai",
            agent_name="agent-a",
            task_id="task-model",
            prompt_tokens=100,
            completion_tokens=50,
            cost_usd=0.01,
            iteration=1,
        )
        row_id_2 = cost_analytics.record_usage(
            model="gpt-4o-mini",
            provider="openai",
            agent_name="agent-a",
            task_id="task-model",
            prompt_tokens=100,
            completion_tokens=50,
            cost_usd=0.001,
            iteration=1,
        )

        assert row_id_1 != row_id_2
        assert cost_analytics.total_records() == 2

    def test_record_usage_allows_same_task_different_providers(
        self, cost_analytics: CostAnalytics
    ) -> None:
        """Same model on different providers should create separate records."""
        row_id_1 = cost_analytics.record_usage(
            model="claude-3",
            provider="anthropic",
            agent_name="agent-a",
            task_id="task-provider",
            prompt_tokens=100,
            completion_tokens=50,
            cost_usd=0.01,
            iteration=1,
        )
        row_id_2 = cost_analytics.record_usage(
            model="claude-3",
            provider="bedrock",
            agent_name="agent-a",
            task_id="task-provider",
            prompt_tokens=100,
            completion_tokens=50,
            cost_usd=0.01,
            iteration=1,
        )

        assert row_id_1 != row_id_2
        assert cost_analytics.total_records() == 2

    def test_record_usage_logs_debug_on_duplicate(
        self, cost_analytics: CostAnalytics, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A duplicate record should log a debug message."""
        cost_analytics.record_usage(
            model="gpt-4o",
            provider="openai",
            agent_name="agent-a",
            task_id="task-debug",
            prompt_tokens=100,
            completion_tokens=50,
            cost_usd=0.01,
            iteration=1,
        )
        with caplog.at_level(logging.DEBUG, logger="ai_company.data.cost_analytics"):
            cost_analytics.record_usage(
                model="gpt-4o",
                provider="openai",
                agent_name="agent-a",
                task_id="task-debug",
                prompt_tokens=100,
                completion_tokens=50,
                cost_usd=0.01,
                iteration=1,
            )

        assert "Cost dedup" in caplog.text
        assert "task-debug" in caplog.text
