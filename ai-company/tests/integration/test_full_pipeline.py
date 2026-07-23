"""E2E pipeline test — full lifecycle with mocked LLM.

GAP-020 fix: validates the complete path from task submission through
executor processing, memory storage, and audit trail creation.

The AgentLoop._call_llm() bypasses LLMClient.execute_task() and accesses
self.llm.router.resolve_with_fallback() + self.llm.get_provider() directly.
We mock _call_llm to return a proper ChatResponse with ReAct JSON.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import patch

from ai_company.llm.providers.base import ChatResponse
from ai_company.models.task import Task, TaskPriority, TaskStatus
from ai_company.orchestrator.message_bus import MessageBus


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
    import json

    payload = json.dumps({"thought": "Done", "plan": [], "result": result, "done": done})
    return _make_chat_response(content=payload)


def _patch_agent_loop_llm(response: ChatResponse):
    """Context manager that patches AgentLoop._call_llm to return fixed response."""
    return patch(
        "ai_company.executor.agent_loop.AgentLoop._call_llm",
        return_value=response,
    )


class TestFullPipeline:
    """End-to-end test of the complete task lifecycle."""

    def test_task_lifecycle_happy_path(
        self, workspace: Path, executor, bus: MessageBus
    ) -> None:
        """Full lifecycle: submit task -> executor processes -> completed -> memory stored."""
        with _patch_agent_loop_llm(_react_response("Config validated successfully.")):
            task = Task(
                id="e2e-happy-001",
                sender_id="human-ceo",
                receiver_id="test-agent",
                instruction="Validate the config file",
                priority=TaskPriority.MEDIUM,
            )
            bus.send_task(task)

            count = executor.tick()

        assert count >= 1
        updated = bus.get_task_by_id("e2e-happy-001")
        assert updated is not None
        assert updated.status == TaskStatus.COMPLETED
        assert "Config validated" in (updated.result or "")

    def test_task_failure_handling(
        self, workspace: Path, executor, bus: MessageBus
    ) -> None:
        """Task that fails due to LLM error should be marked FAILED."""
        with _patch_agent_loop_llm(_react_response("partial")):
            # Override: raise an exception from _call_llm
            with patch(
                "ai_company.executor.agent_loop.AgentLoop._call_llm",
                side_effect=Exception("LLM unavailable"),
            ):
                task = Task(
                    id="e2e-fail-001",
                    sender_id="human-ceo",
                    receiver_id="test-agent",
                    instruction="Failing task",
                    priority=TaskPriority.LOW,
                    max_retries=0,
                )
                bus.send_task(task)
                count = executor.tick()

        assert count >= 1
        updated = bus.get_task_by_id("e2e-fail-001")
        assert updated is not None
        assert updated.status == TaskStatus.FAILED

    def test_multiple_tasks_processed(
        self, workspace: Path, executor, bus: MessageBus
    ) -> None:
        """Multiple tasks in the inbox are all processed in one tick."""
        with _patch_agent_loop_llm(_react_response("done")):
            for i in range(3):
                bus.send_task(
                    Task(
                        id=f"e2e-multi-{i:03d}",
                        sender_id="human-ceo",
                        receiver_id="test-agent",
                        instruction=f"Task number {i}",
                        priority=TaskPriority.MEDIUM,
                    )
                )

            count = executor.tick()

        assert count == 3
        for i in range(3):
            updated = bus.get_task_by_id(f"e2e-multi-{i:03d}")
            assert updated is not None
            assert updated.status == TaskStatus.COMPLETED

    def test_memory_stored_after_completion(
        self, workspace: Path, executor, bus: MessageBus
    ) -> None:
        """Completed task outcome is stored in memory."""
        from ai_company.memory.integration import get_store

        with _patch_agent_loop_llm(_react_response("Memory test complete")):
            task = Task(
                id="e2e-memory-001",
                sender_id="human-ceo",
                receiver_id="test-agent",
                instruction="Test memory storage",
                priority=TaskPriority.MEDIUM,
            )
            bus.send_task(task)
            executor.tick()

        store = get_store()
        assert store is not None
        episodic = store.recall("episodic", limit=10)
        assert any("e2e-memory-001" in e.content for e in episodic)

    def test_consolidation_scheduler_runs(
        self, workspace: Path, executor, bus: MessageBus
    ) -> None:
        """Consolidation scheduler runs during tick and doesn't break processing."""
        from ai_company.memory.integration import get_store

        store = get_store()
        assert store is not None
        for i in range(5):
            store.store("episodic", f"Test entry {i}", agent_id="test-agent")

        with _patch_agent_loop_llm(_react_response("consolidation test")):
            task = Task(
                id="e2e-consolidate-001",
                sender_id="human-ceo",
                receiver_id="test-agent",
                instruction="Trigger consolidation",
                priority=TaskPriority.MEDIUM,
            )
            bus.send_task(task)
            count = executor.tick()

        assert count >= 1
        assert hasattr(executor, "_consolidation_scheduler")
        stats = executor._consolidation_scheduler.stats()
        assert stats["tick_count"] >= 1

    def test_empty_inbox_no_op(self, workspace: Path, executor, bus: MessageBus) -> None:
        """Tick with empty inbox returns 0 and doesn't crash."""
        count = executor.tick()
        assert count == 0

    def test_audit_trail_recorded(
        self, workspace: Path, executor, bus: MessageBus
    ) -> None:
        """Task completion creates audit trail entries."""
        with _patch_agent_loop_llm(_react_response("Audit test complete")):
            task = Task(
                id="e2e-audit-001",
                sender_id="human-ceo",
                receiver_id="test-agent",
                instruction="Test audit trail",
                priority=TaskPriority.MEDIUM,
            )
            bus.send_task(task)
            executor.tick()

        # AuditWriter writes to .opencode/audit (single file, not a directory)
        audit_file = workspace / ".opencode" / "audit"
        assert audit_file.exists(), f"Audit file not found at {audit_file}"
        content = audit_file.read_text(encoding="utf-8")
        assert "e2e-audit-001" in content

    def test_task_with_tool_execution(
        self, workspace: Path, executor, bus: MessageBus
    ) -> None:
        """Task that requires tool execution: plan has steps, then done."""
        import json

        tool_plan = [
            {"tool": "read", "args": {"path": "config.yaml"}},
        ]
        iteration1 = _make_chat_response(
            content=json.dumps({
                "thought": "Need to read config",
                "plan": tool_plan,
                "result": "",
                "done": False,
            })
        )
        iteration2 = _react_response("Config looks good")

        call_count = 0
        responses = [iteration1, iteration2]

        def _mock_call_llm(*args: Any, **kwargs: Any) -> ChatResponse:
            nonlocal call_count
            resp = responses[min(call_count, len(responses) - 1)]
            call_count += 1
            return resp

        with patch(
            "ai_company.executor.agent_loop.AgentLoop._call_llm",
            side_effect=_mock_call_llm,
        ):
            task = Task(
                id="e2e-tools-001",
                sender_id="human-ceo",
                receiver_id="test-agent",
                instruction="Read and validate config",
                priority=TaskPriority.MEDIUM,
            )
            bus.send_task(task)
            executor.tick()

        updated = bus.get_task_by_id("e2e-tools-001")
        assert updated is not None
        assert updated.status == TaskStatus.COMPLETED
        assert "Config looks good" in (updated.result or "")

    def test_max_iterations_stops_loop(
        self, workspace: Path, executor, bus: MessageBus
    ) -> None:
        """Loop stops after max iterations even if not done."""
        import json

        never_done = _make_chat_response(
            content=json.dumps({
                "thought": "Still working",
                "plan": [{"tool": "read", "args": {"path": "."}}],
                "result": "",
                "done": False,
            })
        )

        with patch(
            "ai_company.executor.agent_loop.AgentLoop._call_llm",
            return_value=never_done,
        ):
            task = Task(
                id="e2e-maxiter-001",
                sender_id="human-ceo",
                receiver_id="test-agent",
                instruction="Long running task",
                priority=TaskPriority.MEDIUM,
                max_retries=0,
            )
            bus.send_task(task)
            executor.tick()

        updated = bus.get_task_by_id("e2e-maxiter-001")
        assert updated is not None
        # Should be FAILED because loop ran out of iterations
        assert updated.status == TaskStatus.FAILED

    def test_task_status_transitions(
        self, workspace: Path, executor, bus: MessageBus
    ) -> None:
        """Verify task goes through pending -> in_progress -> completed."""
        with _patch_agent_loop_llm(_react_response("done")):
            task = Task(
                id="e2e-transitions-001",
                sender_id="human-ceo",
                receiver_id="test-agent",
                instruction="Status transition test",
                priority=TaskPriority.HIGH,
            )
            bus.send_task(task)

            # Before tick, should be pending
            before = bus.get_task_by_id("e2e-transitions-001")
            assert before is not None
            assert before.status == TaskStatus.PENDING

            executor.tick()

        # After tick, should be completed
        after = bus.get_task_by_id("e2e-transitions-001")
        assert after is not None
        assert after.status == TaskStatus.COMPLETED
