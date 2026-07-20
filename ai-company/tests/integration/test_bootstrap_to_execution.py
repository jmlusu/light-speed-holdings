"""Integration test: bootstrap -> submit Task -> executor tick -> state transition.

Exercises the real MessageBus and audit trail end-to-end. The LLM layer is
mocked (via the ``executor`` fixture) so no network is required.
"""

from __future__ import annotations

import json
from pathlib import Path


from ai_company.models import Task, TaskPriority, TaskStatus
from ai_company.orchestrator.message_bus import MessageBus


def _inbox_tasks(workspace: Path) -> list[dict]:
    raw = (workspace / ".opencode" / "inbox.json").read_text(encoding="utf-8")
    return json.loads(raw)


def _audit_events(workspace: Path) -> list[dict]:
    # init_audit() treats the passed dir as the JSONL file path directly.
    path = workspace / ".opencode" / "audit"
    if not path.exists():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            events.append(json.loads(line))
    return events


class TestBootstrapToExecution:
    def test_submit_task_via_message_bus(self, bus: MessageBus, workspace: Path) -> None:
        task = Task(
            id="task-001",
            sender_id="human-ceo",
            receiver_id="test-agent",
            instruction="Read test.py and report contents",
            status=TaskStatus.PENDING.value,
            priority=TaskPriority.MEDIUM,
        )
        bus.send_task(task)
        tasks = _inbox_tasks(workspace)
        assert len(tasks) == 1
        assert tasks[0]["status"] == "pending"

    def test_tick_transitions_created_to_completed(self, executor, workspace: Path) -> None:
        # Submit a pending task directly to the inbox.
        inbox = workspace / ".opencode" / "inbox.json"
        inbox.write_text(
            json.dumps([
                {
                    "id": "task-001",
                    "sender_id": "human-ceo",
                    "receiver_id": "test-agent",
                    "instruction": "Summarise the report",
                    "status": "pending",
                    "priority": "medium",
                }
            ]),
            encoding="utf-8",
        )

        # Mock the agent loop so the LLM never runs.
        from tests.integration.conftest import FakeLoopResult

        executor.agent_loop.run = lambda *a, **k: FakeLoopResult(
            final_response="Summary produced.", done=True
        )

        count = executor.tick()
        assert count == 1

        tasks = _inbox_tasks(workspace)
        assert tasks[0]["status"] == "completed"
        assert "Summary" in tasks[0]["result"]

    def test_tick_writes_audit_events(self, executor, workspace: Path) -> None:
        inbox = workspace / ".opencode" / "inbox.json"
        inbox.write_text(
            json.dumps([
                {
                    "id": "task-audit",
                    "sender_id": "human-ceo",
                    "receiver_id": "test-agent",
                    "instruction": "Produce a deliverable",
                    "status": "pending",
                    "priority": "high",
                }
            ]),
            encoding="utf-8",
        )

        from tests.integration.conftest import FakeLoopResult

        executor.agent_loop.run = lambda *a, **k: FakeLoopResult(
            final_response="Deliverable ready.", done=True
        )

        executor.tick()

        events = _audit_events(workspace)
        assert events, "expected audit events to be written"
        event_types = {e["event_type"] for e in events}
        assert "task_created" in event_types
        assert "task_completed" in event_types

    def test_tick_handles_failure_gracefully(self, executor, workspace: Path) -> None:
        inbox = workspace / ".opencode" / "inbox.json"
        inbox.write_text(
            json.dumps([
                {
                    "id": "task-fail",
                    "sender_id": "human-ceo",
                    "receiver_id": "test-agent",
                    "instruction": "Break things",
                    "status": "pending",
                    "priority": "medium",
                }
            ]),
            encoding="utf-8",
        )

        from tests.integration.conftest import FakeLoopResult

        executor.agent_loop.run = lambda *a, **k: FakeLoopResult(
            final_response="", done=False, error="loop did not finish"
        )

        executor.tick()

        tasks = _inbox_tasks(workspace)
        assert tasks[0]["status"] == "failed"
        assert "loop did not finish" in tasks[0]["result"]
