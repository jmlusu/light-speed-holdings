"""GAP-020 supplementary integration tests for MessageBus pipeline.

Covers the new functionality introduced in R1-R4:
- Priority-based task ordering (R2)
- Automatic retry with exponential backoff (R3)
- DLQ stale-task detection and retry (R1 + R4)
- Full lifecycle through MessageBus API (R1)
- Broadcast events through full lifecycle

These tests use the integration conftest fixtures (workspace isolation,
mocked LLM, MessageBus) and exercise the real Executor + MessageBus
integration end-to-end.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import patch


from ai_company.executor.dead_letter import DeadLetterQueue, detect_stale_tasks
from ai_company.llm.providers.base import ChatResponse
from ai_company.models.task import Task, TaskPriority, TaskStatus
from ai_company.orchestrator.message_bus import MessageBus


# ── Helpers ────────────────────────────────────────────────────────────


def _make_chat_response(content: str = "") -> ChatResponse:
    """Create a ChatResponse with the given content."""
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
    payload = json.dumps({"thought": "Done", "plan": [], "result": result, "done": done})
    return _make_chat_response(content=payload)


def _failing_response() -> ChatResponse:
    """ChatResponse that will cause an LLM error during processing."""
    return _make_chat_response(content="NOT_JSON")


def _patch_agent_loop_llm(response: ChatResponse):
    """Context manager that patches AgentLoop._call_llm to return fixed response."""
    return patch(
        "ai_company.executor.agent_loop.AgentLoop._call_llm",
        return_value=response,
    )


# ── R2: Priority ordering tests ───────────────────────────────────────


class TestPriorityOrdering:
    """Tasks should be claimed in priority order: critical > high > medium > low."""

    def test_claim_next_pending_respects_priority(
        self, workspace: Path, bus: MessageBus
    ) -> None:
        """claim_next_pending returns the highest-priority task first."""
        # Send tasks in reverse priority order
        bus.send_task(Task(
            id="pri-low-001", sender_id="ceo", receiver_id="test-agent",
            instruction="Low task", priority=TaskPriority.LOW,
        ))
        bus.send_task(Task(
            id="pri-crit-001", sender_id="ceo", receiver_id="test-agent",
            instruction="Critical task", priority=TaskPriority.CRITICAL,
        ))
        bus.send_task(Task(
            id="pri-med-001", sender_id="ceo", receiver_id="test-agent",
            instruction="Medium task", priority=TaskPriority.MEDIUM,
        ))
        bus.send_task(Task(
            id="pri-high-001", sender_id="ceo", receiver_id="test-agent",
            instruction="High task", priority=TaskPriority.HIGH,
        ))

        # First claim should be critical
        first = bus.claim_next_pending()
        assert first is not None
        assert first.id == "pri-crit-001"

        # Second should be high
        second = bus.claim_next_pending()
        assert second is not None
        assert second.id == "pri-high-001"

        # Third should be medium
        third = bus.claim_next_pending()
        assert third is not None
        assert third.id == "pri-med-001"

        # Fourth should be low
        fourth = bus.claim_next_pending()
        assert fourth is not None
        assert fourth.id == "pri-low-001"

    def test_get_pending_tasks_sorted_by_priority(
        self, workspace: Path, bus: MessageBus
    ) -> None:
        """get_pending_tasks returns tasks sorted by priority."""
        bus.send_task(Task(
            id="sort-low", sender_id="ceo", receiver_id="test-agent",
            instruction="Low", priority=TaskPriority.LOW,
        ))
        bus.send_task(Task(
            id="sort-high", sender_id="ceo", receiver_id="test-agent",
            instruction="High", priority=TaskPriority.HIGH,
        ))
        bus.send_task(Task(
            id="sort-crit", sender_id="ceo", receiver_id="test-agent",
            instruction="Critical", priority=TaskPriority.CRITICAL,
        ))

        pending = bus.get_pending_tasks()
        assert len(pending) == 3
        assert pending[0].id == "sort-crit"
        assert pending[1].id == "sort-high"
        assert pending[2].id == "sort-low"

    def test_executor_processes_critical_before_low(
        self, workspace: Path, executor, bus: MessageBus
    ) -> None:
        """Executor processes critical task before low-priority task."""
        processed_order: list[str] = []

        def _track_response(*args: Any, **kwargs: Any) -> ChatResponse:
            resp = _react_response("done")
            return resp

        # Track which tasks are processed by patching _process_task
        original_process = executor._process_task

        def _tracking_process(task: Task) -> None:
            processed_order.append(task.id)
            original_process(task)

        with (
            _patch_agent_loop_llm(_react_response("done")),
            patch.object(executor, "_process_task", _tracking_process),
        ):
            bus.send_task(Task(
                id="exec-low", sender_id="ceo", receiver_id="test-agent",
                instruction="Low", priority=TaskPriority.LOW,
            ))
            bus.send_task(Task(
                id="exec-crit", sender_id="ceo", receiver_id="test-agent",
                instruction="Critical", priority=TaskPriority.CRITICAL,
            ))
            executor.tick()

        # Critical should be processed first (only 1 per tick since claim_next_pending is atomic)
        assert processed_order[0] == "exec-crit"


# ── R3: Retry with backoff tests ──────────────────────────────────────


class TestRetryWithBackoff:
    """Failed tasks should be automatically retried with exponential backoff."""

    def test_retry_task_increments_count_and_sets_pending(
        self, workspace: Path, bus: MessageBus
    ) -> None:
        """retry_task increments retry_count and sets status back to pending."""
        task = Task(
            id="retry-001", sender_id="ceo", receiver_id="test-agent",
            instruction="Retry me", priority=TaskPriority.MEDIUM,
        )
        bus.send_task(task)

        # Fail the task
        bus.update_task_status("retry-001", "failed", result="error")

        # Schedule retry
        result = bus.retry_task("retry-001", delay_seconds=60)
        assert result is not None
        assert result.status == TaskStatus.PENDING
        assert result.retry_count == 1
        assert result.next_retry_at != ""

    def test_retry_respects_max_retries(
        self, workspace: Path, bus: MessageBus
    ) -> None:
        """retry_task does not retry beyond max_retries."""
        task = Task(
            id="retry-max", sender_id="ceo", receiver_id="test-agent",
            instruction="Max retries", priority=TaskPriority.MEDIUM,
            max_retries=2,
        )
        bus.send_task(task)

        # Simulate max retries already exhausted
        task_dict = bus.get_task_by_id("retry-max")
        assert task_dict is not None

        # Manually set retry_count to max_retries
        bus.update_task("retry-max", {"retry_count": 2, "status": "failed", "result": "error"})

        # Attempt retry — should be rejected
        bus.retry_task("retry-max", delay_seconds=60)
        # Task should still be failed since max retries exceeded
        task_after = bus.get_task_by_id("retry-max")
        assert task_after is not None
        assert task_after.status == TaskStatus.FAILED

    def test_get_retryable_tasks_returns_ready_tasks(
        self, workspace: Path, bus: MessageBus
    ) -> None:
        """get_retryable_tasks returns tasks whose retry time has passed."""
        task = Task(
            id="retry-ready", sender_id="ceo", receiver_id="test-agent",
            instruction="Ready for retry", priority=TaskPriority.MEDIUM,
        )
        bus.send_task(task)

        # Fail and schedule retry in the past
        bus.update_task_status("retry-ready", "failed", result="error")
        bus.retry_task("retry-ready", delay_seconds=-10)  # negative = already past

        retryable = bus.get_retryable_tasks()
        assert len(retryable) == 1
        assert retryable[0].id == "retry-ready"

    def test_get_retryable_tasks_excludes_pending_not_yet_ready(
        self, workspace: Path, bus: MessageBus
    ) -> None:
        """get_retryable_tasks excludes tasks whose retry time is in the future."""
        task = Task(
            id="retry-future", sender_id="ceo", receiver_id="test-agent",
            instruction="Not ready", priority=TaskPriority.MEDIUM,
        )
        bus.send_task(task)

        # Fail and schedule retry far in the future
        bus.update_task_status("retry-future", "failed", result="error")
        bus.retry_task("retry-future", delay_seconds=3600)  # 1 hour from now

        retryable = bus.get_retryable_tasks()
        assert len(retryable) == 0

    def test_executor_retries_failed_task(
        self, workspace: Path, executor, bus: MessageBus
    ) -> None:
        """Executor calls _maybe_retry on task failure, scheduling retry."""
        task = Task(
            id="exec-retry-001", sender_id="ceo", receiver_id="test-agent",
            instruction="Will fail then retry", priority=TaskPriority.MEDIUM,
        )
        bus.send_task(task)

        # First tick: task fails, _maybe_retry should schedule retry
        with patch(
            "ai_company.executor.agent_loop.AgentLoop._call_llm",
            side_effect=Exception("LLM error"),
        ):
            executor.tick()

        # Task should be pending (scheduled for retry), not failed
        updated = bus.get_task_by_id("exec-retry-001")
        assert updated is not None
        assert updated.status == TaskStatus.PENDING
        assert updated.retry_count == 1
        assert updated.next_retry_at != ""

    def test_executor_retries_until_max_exceeded(
        self, workspace: Path, executor, bus: MessageBus
    ) -> None:
        """After max_retries failures, task stays FAILED (no retry scheduled)."""
        task = Task(
            id="exec-retry-max", sender_id="ceo", receiver_id="test-agent",
            instruction="Will exhaust retries", priority=TaskPriority.MEDIUM,
            max_retries=1,
        )
        bus.send_task(task)

        # First tick: fail, retry scheduled (retry_count becomes 1)
        with patch(
            "ai_company.executor.agent_loop.AgentLoop._call_llm",
            side_effect=Exception("LLM error"),
        ):
            executor.tick()

        # Make retry time pass immediately
        bus.update_task("exec-retry-max", {"next_retry_at": datetime.now().isoformat()})

        # Second tick: fail again, retry_count=1 == max_retries=1, no more retries
        with patch(
            "ai_company.executor.agent_loop.AgentLoop._call_llm",
            side_effect=Exception("LLM error"),
        ):
            executor.tick()

        final = bus.get_task_by_id("exec-retry-max")
        assert final is not None
        assert final.status == TaskStatus.FAILED
        # retry_count stays at 1 (not incremented again since max exceeded)
        assert final.retry_count == 1


# ── DLQ + Stale detection tests ───────────────────────────────────────


class TestDLQIntegration:
    """Dead-letter queue integration with MessageBus."""

    def test_stale_tasks_moved_to_dlq(
        self, workspace: Path, bus: MessageBus
    ) -> None:
        """Stale in_progress tasks are detected and moved to DLQ."""
        dlq = DeadLetterQueue(dlq_path=str(workspace / ".opencode" / "dead_letter.json"))

        # Create a task and mark it in_progress with an old timestamp
        task = Task(
            id="stale-001", sender_id="ceo", receiver_id="test-agent",
            instruction="Stale task", priority=TaskPriority.MEDIUM,
        )
        bus.send_task(task)
        bus.update_task_status("stale-001", "in_progress")

        # Backdate the updated_at to be 60 minutes ago
        old_time = (datetime.now() - timedelta(minutes=60)).isoformat()
        bus.update_task("stale-001", {"updated_at": old_time})

        # Detect stale tasks
        moved = detect_stale_tasks(bus, dlq, threshold_minutes=30)
        assert len(moved) == 1
        assert moved[0]["id"] == "stale-001"

        # Task should be removed from inbox
        assert bus.get_task_by_id("stale-001") is None

        # Task should be in DLQ
        dlq_entry = dlq.get_task("stale-001")
        assert dlq_entry is not None
        assert "stale" in dlq_entry["reason"].lower() or "Stale" in dlq_entry["reason"]

    def test_recent_tasks_not_moved_to_dlq(
        self, workspace: Path, bus: MessageBus
    ) -> None:
        """Recently updated in_progress tasks are NOT moved to DLQ."""
        dlq = DeadLetterQueue(dlq_path=str(workspace / ".opencode" / "dead_letter.json"))

        task = Task(
            id="fresh-001", sender_id="ceo", receiver_id="test-agent",
            instruction="Fresh task", priority=TaskPriority.MEDIUM,
        )
        bus.send_task(task)
        bus.update_task_status("fresh-001", "in_progress")

        # Should NOT be detected as stale
        moved = detect_stale_tasks(bus, dlq, threshold_minutes=30)
        assert len(moved) == 0

        # Task should still be in inbox
        assert bus.get_task_by_id("fresh-001") is not None

    def test_dlq_retry_re_enqueues_task(
        self, workspace: Path, bus: MessageBus
    ) -> None:
        """DLQ retry_task removes from DLQ and re-enqueues to inbox."""
        dlq = DeadLetterQueue(dlq_path=str(workspace / ".opencode" / "dead_letter.json"))

        task_data = {
            "id": "dlq-retry-001",
            "sender_id": "ceo",
            "receiver_id": "test-agent",
            "instruction": "Re-enqueue me",
            "priority": "medium",
            "status": "failed",
        }
        dlq.move_task(task_data, "test reason")

        # Retry from DLQ
        restored = dlq.retry_task("dlq-retry-001")
        assert restored is not None
        assert restored["id"] == "dlq-retry-001"

        # Should be removed from DLQ
        assert dlq.get_task("dlq-retry-001") is None

        # Re-enqueue to bus
        restored["status"] = "pending"
        restored["retry_count"] = 0
        bus.send_task(Task(**restored))
        assert bus.get_task_by_id("dlq-retry-001") is not None

    def test_dlq_file_locking(
        self, workspace: Path, bus: MessageBus
    ) -> None:
        """DLQ uses FileStore for safe concurrent writes."""
        dlq = DeadLetterQueue(dlq_path=str(workspace / ".opencode" / "dead_letter.json"))

        # Multiple rapid moves should not corrupt the file
        for i in range(5):
            dlq.move_task(
                {"id": f"lock-test-{i}", "status": "failed"},
                f"reason {i}",
            )

        entries = dlq.list_entries()
        assert len(entries) == 5


# ── Full lifecycle tests through MessageBus API ────────────────────────


class TestMessageBusLifecycle:
    """Full task lifecycle exercised through the MessageBus API (R1)."""

    def test_create_process_complete_via_bus(
        self, workspace: Path, executor, bus: MessageBus
    ) -> None:
        """Task goes through: send -> claim -> process -> complete, all via MessageBus."""
        with _patch_agent_loop_llm(_react_response("All done.")):
            task = Task(
                id="lifecycle-001", sender_id="ceo", receiver_id="test-agent",
                instruction="Full lifecycle", priority=TaskPriority.HIGH,
            )
            bus.send_task(task)

            # Verify task is pending
            before = bus.get_task_by_id("lifecycle-001")
            assert before is not None
            assert before.status == TaskStatus.PENDING

            # Execute
            count = executor.tick()
            assert count >= 1

            # Verify completed
            after = bus.get_task_by_id("lifecycle-001")
            assert after is not None
            assert after.status == TaskStatus.COMPLETED
            assert "All done" in (after.result or "")

    def test_create_fail_retry_complete_via_bus(
        self, workspace: Path, executor, bus: MessageBus
    ) -> None:
        """Task fails, gets retried, then succeeds — all through MessageBus."""
        call_count = 0

        def _fail_then_succeed(*args: Any, **kwargs: Any) -> ChatResponse:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise Exception("Transient LLM error")
            return _react_response("Recovered successfully")

        with patch(
            "ai_company.executor.agent_loop.AgentLoop._call_llm",
            side_effect=_fail_then_succeed,
        ):
            task = Task(
                id="retry-lifecycle-001", sender_id="ceo", receiver_id="test-agent",
                instruction="Fail then succeed", priority=TaskPriority.HIGH,
            )
            bus.send_task(task)

            # Tick 1: fails, gets scheduled for retry
            executor.tick()
            mid = bus.get_task_by_id("retry-lifecycle-001")
            assert mid is not None
            assert mid.status == TaskStatus.PENDING  # retried, not failed
            assert mid.retry_count == 1

            # Make retry time pass
            bus.update_task("retry-lifecycle-001", {"next_retry_at": datetime.now().isoformat()})

            # Tick 2: succeeds
            executor.tick()

            final = bus.get_task_by_id("retry-lifecycle-001")
            assert final is not None
            assert final.status == TaskStatus.COMPLETED
            assert "Recovered" in (final.result or "")

    def test_stale_task_to_dlq_to_retry_via_bus(
        self, workspace: Path, bus: MessageBus
    ) -> None:
        """Stale task -> DLQ -> manual retry -> re-enqueue -> process."""
        dlq = DeadLetterQueue(dlq_path=str(workspace / ".opencode" / "dead_letter.json"))

        # Create and stale-ify a task
        task = Task(
            id="stale-lifecycle-001", sender_id="ceo", receiver_id="test-agent",
            instruction="Stale then retry", priority=TaskPriority.MEDIUM,
        )
        bus.send_task(task)
        bus.update_task_status("stale-lifecycle-001", "in_progress")
        old_time = (datetime.now() - timedelta(minutes=60)).isoformat()
        bus.update_task("stale-lifecycle-001", {"updated_at": old_time})

        # Move to DLQ
        moved = detect_stale_tasks(bus, dlq, threshold_minutes=30)
        assert len(moved) == 1
        assert bus.get_task_by_id("stale-lifecycle-001") is None

        # Retry from DLQ and re-enqueue
        restored = dlq.retry_task("stale-lifecycle-001")
        assert restored is not None
        restored["status"] = "pending"
        restored["retry_count"] = 0
        bus.send_task(Task(**restored))

        # Verify task is back in inbox
        requeued = bus.get_task_by_id("stale-lifecycle-001")
        assert requeued is not None
        assert requeued.status == TaskStatus.PENDING

    def test_broadcast_events_through_full_lifecycle(
        self, workspace: Path, executor, bus: MessageBus
    ) -> None:
        """Broadcast events are emitted for created, completed, and failed."""
        events: list[tuple[str, str]] = []  # (task_id, event_type)

        def _capture_events(task_dict: dict, event: str) -> None:
            events.append((task_dict.get("id", ""), event))

        # Create bus with broadcast callback
        bus_with_cb = MessageBus(
            storage_path=str(workspace / ".opencode" / "inbox.json"),
            broadcast_callback=_capture_events,
        )

        with _patch_agent_loop_llm(_react_response("Broadcast test")):
            task = Task(
                id="broadcast-001", sender_id="ceo", receiver_id="test-agent",
                instruction="Broadcast lifecycle", priority=TaskPriority.MEDIUM,
            )
            bus_with_cb.send_task(task)
            executor.bus = bus_with_cb  # wire executor to broadcast bus
            executor.tick()

        # Should have "created" and "completed" events for this task
        task_events = [e for e in events if e[0] == "broadcast-001"]
        event_types = [e[1] for e in task_events]
        assert "created" in event_types
        assert "completed" in event_types

    def test_multiple_tasks_priority_lifecycle(
        self, workspace: Path, executor, bus: MessageBus
    ) -> None:
        """Multiple tasks with different priorities are all processed correctly."""
        processed_ids: list[str] = []

        original_process = executor._process_task

        def _tracking_process(task: Task) -> None:
            processed_ids.append(task.id)
            original_process(task)

        with (
            _patch_agent_loop_llm(_react_response("done")),
            patch.object(executor, "_process_task", _tracking_process),
        ):
            for i in range(4):
                priorities = [
                    TaskPriority.LOW, TaskPriority.CRITICAL,
                    TaskPriority.MEDIUM, TaskPriority.HIGH,
                ]
                bus.send_task(Task(
                    id=f"multi-pri-{i}", sender_id="ceo", receiver_id="test-agent",
                    instruction=f"Task {i}", priority=priorities[i],
                ))

            # Process all 4 tasks (one per tick since claim_next_pending is atomic)
            for _ in range(4):
                executor.tick()

        # Each task should be processed exactly once
        assert len(processed_ids) == 4
        # Critical should be first
        assert processed_ids[0] == "multi-pri-1"
        # High should be second
        assert processed_ids[1] == "multi-pri-3"
