"""Tests for the memory integration module."""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_company.memory import integration as mod
from ai_company.memory.engine import MemoryStore


@pytest.fixture(autouse=True)
def _reset_store() -> None:
    """Reset the module-level _store before and after each test."""
    mod._store = None
    yield
    mod._store = None


class TestInitMemory:
    def test_creates_store(self, tmp_path: Path) -> None:
        store = mod.init_memory(base_dir=str(tmp_path / "mem"))
        assert isinstance(store, MemoryStore)
        assert mod.get_store() is store

    def test_get_store_none_before_init(self) -> None:
        assert mod.get_store() is None


class TestRecordTaskOutcome:
    def test_writes_episodic_memory(self, tmp_path: Path) -> None:
        mod.init_memory(base_dir=str(tmp_path / "mem"))
        mod.record_task_outcome(
            task_id="t-001",
            agent_id="lead-backend",
            instruction="Deploy the API",
            status="completed",
            result_summary="Deployed to staging",
            tools_used=["execute", "write"],
        )
        store = mod.get_store()
        assert store is not None
        results = store.recall("episodic", query="Deploy the API")
        assert len(results) == 1
        assert "t-001" in results[0].content
        assert "completed" in results[0].tags
        assert "lead-backend" in results[0].tags
        assert "execute" in results[0].tags
        assert results[0].agent_id == "lead-backend"
        assert results[0].metadata["task_id"] == "t-001"

    def test_writes_without_tools_used(self, tmp_path: Path) -> None:
        mod.init_memory(base_dir=str(tmp_path / "mem"))
        mod.record_task_outcome(
            task_id="t-002",
            agent_id="ceo",
            instruction="Review strategy",
            status="failed",
            result_summary="Timed out",
        )
        store = mod.get_store()
        results = store.recall("episodic", agent_id="ceo")
        assert len(results) == 1
        assert "failed" in results[0].tags
        assert "execute" not in results[0].tags

    def test_noop_when_store_none(self) -> None:
        # Should not raise
        mod.record_task_outcome(
            task_id="t-999", agent_id="x", instruction="y", status="z", result_summary="w"
        )


class TestRecordKnowledge:
    def test_writes_semantic_memory(self, tmp_path: Path) -> None:
        mod.init_memory(base_dir=str(tmp_path / "mem"))
        mod.record_knowledge(
            agent_id="analyst",
            topic="market",
            content="Q3 revenue grew 12%",
            tags=["finance", "quarterly"],
        )
        store = mod.get_store()
        results = store.recall("semantic", query="Q3 revenue")
        assert len(results) == 1
        assert "finance" in results[0].tags
        assert results[0].agent_id == "analyst"

    def test_noop_when_store_none(self) -> None:
        mod.record_knowledge(agent_id="x", topic="t", content="c")


class TestRecordProcedure:
    def test_writes_procedural_memory(self, tmp_path: Path) -> None:
        mod.init_memory(base_dir=str(tmp_path / "mem"))
        mod.record_procedure(
            agent_id="devops",
            procedure="Run ansible-playbook deploy.yml to deploy",
            context="AWS EC2",
        )
        store = mod.get_store()
        results = store.recall("procedural", query="ansible")
        assert len(results) == 1
        assert results[0].agent_id == "devops"

    def test_noop_when_store_none(self) -> None:
        mod.record_procedure(agent_id="x", procedure="p", context="c")


class TestRecallContext:
    def test_returns_across_types(self, tmp_path: Path) -> None:
        mod.init_memory(base_dir=str(tmp_path / "mem"))
        mod.record_task_outcome(
            task_id="t-10", agent_id="a", instruction="Deploy", status="ok", result_summary="Done"
        )
        mod.record_knowledge(agent_id="a", topic="deploy", content="Deploy guide v2")
        mod.record_procedure(agent_id="a", procedure="Deploy steps", context="CI/CD")

        results = mod.recall_context("Deploy")
        assert len(results) == 3
        types = {r["type"] for r in results}
        assert types == {"episodic", "semantic", "procedural"}

    def test_respects_limit(self, tmp_path: Path) -> None:
        mod.init_memory(base_dir=str(tmp_path / "mem"))
        for i in range(10):
            mod.record_task_outcome(
                task_id=f"t-{i}", agent_id="a", instruction="X", status="ok", result_summary="Y"
            )
        results = mod.recall_context("X", limit=3)
        assert len(results) == 3

    def test_noop_when_store_none(self) -> None:
        results = mod.recall_context("anything")
        assert results == []
