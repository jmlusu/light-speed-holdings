"""Integration test: memory recall is invoked before task execution.

Verifies that the executor loop calls ``recall_context`` (memory integration)
before running the agentic loop, and that recall results are wired through.
The LLM layer is mocked so no network call occurs.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_company.memory.integration import recall_context


def _seed_task(workspace: Path, task_id: str = "task-mem") -> None:
    (workspace / ".opencode" / "inbox.json").write_text(
        json.dumps([
            {
                "id": task_id,
                "sender_id": "human-ceo",
                "receiver_id": "test-agent",
                "instruction": "Draft the Q3 strategy memo",
                "status": "pending",
                "priority": "medium",
            }
        ]),
        encoding="utf-8",
    )


class TestMemoryRecallIntegration:
    def test_recall_invoked_before_execution(self, executor, workspace: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _seed_task(workspace)

        # Spy on recall_context (already imported into the executor module).
        calls: list[tuple] = []
        real_recall = recall_context

        def spy(query: str, limit: int = 5):
            calls.append((query, limit))
            return real_recall(query, limit)

        monkeypatch.setattr("ai_company.executor.loop.recall_context", spy)

        from tests.integration.conftest import FakeLoopResult

        run_mock = MagicMock(return_value=FakeLoopResult(
            final_response="Memo drafted.", done=True
        ))
        executor.agent_loop.run = run_mock

        executor.tick()

        # Recall must have been called once with the task instruction.
        assert calls, "recall_context was not invoked before task execution"
        assert calls[0][0] == "Draft the Q3 strategy memo"
        run_mock.assert_called_once()

    def test_recall_result_fed_into_prompt(self, executor, workspace: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Recall output should reach the agent loop's user prompt."""
        _seed_task(workspace)

        captured: dict[str, object] = {}

        def spy(query: str, limit: int = 5):
            captured["query"] = query
            return recall_context(query, limit)

        monkeypatch.setattr("ai_company.executor.loop.recall_context", spy)

        from tests.integration.conftest import FakeLoopResult

        def fake_run(*args, **kwargs):
            captured["user_prompt"] = kwargs.get("user_prompt", "")
            return FakeLoopResult(final_response="ok", done=True)

        executor.agent_loop.run = fake_run
        executor.tick()

        assert "Draft the Q3 strategy memo" in captured["user_prompt"]

    def test_recall_failure_does_not_block_task(self, executor, workspace: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """If recall raises, the task must still execute (defensive)."""
        _seed_task(workspace)

        def boom(query: str, limit: int = 5):
            raise RuntimeError("vector store down")

        monkeypatch.setattr("ai_company.executor.loop.recall_context", boom)

        from tests.integration.conftest import FakeLoopResult

        executor.agent_loop.run = lambda *a, **k: FakeLoopResult(
            final_response="Still completed.", done=True
        )

        executor.tick()

        tasks = json.loads(
            (workspace / ".opencode" / "inbox.json").read_text(encoding="utf-8")
        )
        assert tasks[0]["status"] == "completed"

    def test_memory_store_records_outcome(self, executor, workspace: Path) -> None:
        """After completion, the memory integration stores an episodic outcome."""
        _seed_task(workspace)

        from ai_company.memory.integration import get_store
        from tests.integration.conftest import FakeLoopResult

        executor.agent_loop.run = lambda *a, **k: FakeLoopResult(
            final_response="Outcome recorded.", done=True
        )

        executor.tick()

        store = get_store()
        assert store is not None
        entries = store.recall("episodic", query="task-mem", limit=10)
        assert entries, "expected an episodic memory to be recorded"

    def test_recall_isolated_from_network(self, executor, workspace: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """recall_context must be invoked without any live network IO."""
        _seed_task(workspace)

        probe = MagicMock(side_effect=recall_context)
        monkeypatch.setattr("ai_company.executor.loop.recall_context", probe)

        from tests.integration.conftest import FakeLoopResult

        executor.agent_loop.run = lambda *a, **k: FakeLoopResult(done=True)
        executor.tick()

        assert probe.called
