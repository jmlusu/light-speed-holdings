"""Wiring tests: every LLM call site carries a task_id so cost_tracker
records it (empty task_id is silently dropped in ``LLMClient._record_usage``).
"""

from __future__ import annotations

from typing import Any

from ai_company.dashboard import api
from ai_company.executor.history_manager import (
    ConversationHistoryManager,
    create_history_manager,
)


class _RecordingLLM:
    """Minimal LLMClient stand-in that records execute_task kwargs."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def execute_task(self, **kwargs: Any) -> dict[str, Any]:
        self.calls.append(kwargs)
        return {"result": "ok", "subtasks": [{"instruction": "Step one"}]}


class TestHistoryManagerTaskId:
    def test_summarize_passes_task_id_to_execute_task(self) -> None:
        llm = _RecordingLLM()
        mgr = ConversationHistoryManager(llm=llm, task_id="task-123")  # type: ignore[arg-type]

        mgr._llm_summarize("User: hello\nAssistant: hi")

        assert len(llm.calls) == 1
        assert llm.calls[0]["task_id"] == "task-123"
        assert llm.calls[0]["agent_name"] == "summarizer"

    def test_summarize_without_task_id_keeps_empty_string(self) -> None:
        llm = _RecordingLLM()
        mgr = ConversationHistoryManager(llm=llm)  # type: ignore[arg-type]

        mgr._llm_summarize("some history")

        assert llm.calls[0]["task_id"] == ""

    def test_factory_propagates_task_id(self) -> None:
        mgr = create_history_manager(llm=_RecordingLLM(), task_id="task-abc")  # type: ignore[arg-type]
        assert mgr.task_id == "task-abc"

    def test_factory_defaults_to_empty_task_id(self) -> None:
        mgr = create_history_manager(llm=_RecordingLLM())  # type: ignore[arg-type]
        assert mgr.task_id == ""


class TestDecompositionTaskId:
    def test_generate_decomposition_passes_task_id(self, monkeypatch: Any) -> None:
        llm = _RecordingLLM()
        monkeypatch.setattr(api, "_get_llm_client", lambda: llm)

        items = api._generate_decomposition("Build an API endpoint", task_id="task-42")

        assert len(llm.calls) == 1
        assert llm.calls[0]["task_id"] == "task-42"
        assert llm.calls[0]["agent_name"] == "task-decomposer"
        assert items and items[0].instruction == "Step one"

    def test_generate_decomposition_defaults_to_empty_task_id(self, monkeypatch: Any) -> None:
        llm = _RecordingLLM()
        monkeypatch.setattr(api, "_get_llm_client", lambda: llm)

        api._generate_decomposition("Build an API endpoint")

        assert llm.calls[0]["task_id"] == ""
