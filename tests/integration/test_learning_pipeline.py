"""End-to-end tests for the continuous learning pipeline.

Tests the full lifecycle: recall → inject into prompt → task completion →
extract knowledge → store → recall again.  Verifies metrics recording,
consolidation digest, and dynamic few-shot selection.

All tests use temporary directories and mocked LLM — no network calls.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_company.executor.optimized_prompts import (
    _build_dynamic_few_shot,
    build_optimized_system_prompt,
)
from ai_company.executor.prompts import (
    _inject_memory_context,
    build_system_prompt_typed,
)
from ai_company.memory.consolidation import ConsolidationConfig, ConsolidationScheduler
from ai_company.memory.engine import MemoryStore
from ai_company.memory.integration import (
    extract_post_task_knowledge,
    recall_context,
    record_knowledge,
    record_procedure,
    record_task_outcome,
)
from ai_company.memory.metrics import LearningMetricsCollector, TaskMetrics


@pytest.fixture()
def memory_store(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> MemoryStore:
    """Create a fresh MemoryStore in a temp directory and patch the global _store."""
    import ai_company.memory.integration as mi

    store = MemoryStore(base_dir=tmp_path)
    monkeypatch.setattr(mi, "_store", store)
    return store


@pytest.fixture()
def metrics_collector(tmp_path: Path) -> LearningMetricsCollector:
    """Create a fresh metrics collector in a temp directory."""
    return LearningMetricsCollector(base_dir=tmp_path)


class TestFullLifecycle:
    """Test: record episodic → extract semantic → recall semantic → inject into prompt."""

    def test_record_then_recall_episodic(self, memory_store: MemoryStore) -> None:
        """Episodic memory recorded by record_task_outcome is recallable."""
        record_task_outcome(
            task_id="task-1",
            agent_id="backend-engineer",
            instruction="Fix the login bug in auth module",
            status="completed",
            result_summary="Fixed auth bug by adding null check in login.py:42",
            tools_used=["read", "edit", "bash"],
        )
        results = recall_context("login bug auth", limit=5)
        assert len(results) >= 1
        assert any("task-1" in r["content"] for r in results)

    def test_record_then_recall_semantic(self, memory_store: MemoryStore) -> None:
        """Semantic knowledge recorded by record_knowledge is recallable."""
        record_knowledge(
            agent_id="backend-engineer",
            topic="auth-pattern",
            content="Pattern: auth bugs are usually caused by missing null checks in middleware. Always add defensive guards before accessing user session objects.",
            tags=["auth", "backend-engineer"],
        )
        results = recall_context("auth middleware null check", limit=5)
        assert len(results) >= 1
        assert any("semantic" in r["type"] for r in results)

    def test_record_then_recall_procedural(self, memory_store: MemoryStore) -> None:
        """Procedural memory recorded by record_procedure is recallable."""
        record_procedure(
            agent_id="backend-engineer",
            procedure="When bash pytest fails with ImportError: check if PYTHONPATH includes the src/ directory. Fix: export PYTHONPATH=src:$PYTHONPATH before running.",
            context="error-recovery:bash",
            tags=["error-recovery", "bash", "backend-engineer"],
        )
        results = recall_context("pytest ImportError PYTHONPATH", limit=5)
        assert len(results) >= 1
        assert any("procedural" in r["type"] for r in results)

    def test_extraction_creates_semantic_and_procedural(self, memory_store: MemoryStore) -> None:
        """extract_post_task_knowledge creates semantic + procedural from tool traces."""
        from ai_company.executor.agent_loop import LoopResult

        mock_result = MagicMock(spec=LoopResult)
        mock_result.done = True
        mock_result.final_response = "Fixed the bug by editing auth.py"
        mock_result.tool_results = [
            MagicMock(
                tool="read", status="ok", output="file contents", error=None, iteration=1, step=1
            ),
            MagicMock(tool="edit", status="ok", output="edited", error=None, iteration=2, step=2),
        ]

        # Store episodic first (simulates what executor does)
        record_task_outcome(
            task_id="task-extract-1",
            agent_id="backend-engineer",
            instruction="Fix auth bug",
            status="completed",
            result_summary="Fixed the bug by editing auth.py",
            tools_used=["read", "edit"],
        )

        # Now extract
        extract_post_task_knowledge(
            task_id="task-extract-1",
            agent_id="backend-engineer",
            instruction="Fix auth bug",
            status="completed",
            result_summary="Fixed the bug by editing auth.py",
            tool_results=mock_result.tool_results,
        )

        # Verify semantic knowledge was created
        semantic_results = recall_context("backend-engineer task-pattern", limit=10)
        assert any("solved" in r.get("content", "") for r in semantic_results)

    def test_extraction_creates_procedure_on_failure(self, memory_store: MemoryStore) -> None:
        """Failed tool results create procedural memory entries."""
        failed_tool = MagicMock(
            tool="bash",
            status="error",
            output="",
            error="Command failed: pytest not found",
            iteration=1,
            step=1,
        )

        extract_post_task_knowledge(
            task_id="task-fail-1",
            agent_id="backend-engineer",
            instruction="Run tests",
            status="failed",
            result_summary="pytest command not found",
            tool_results=[failed_tool],
        )

        # Verify procedural entry was created
        results = recall_context("backend-engineer error-recovery bash", limit=10)
        assert any("procedural" in r["type"] for r in results)

    def test_extraction_creates_timeout_procedure(self, memory_store: MemoryStore) -> None:
        """Timeout status creates a timeout-prevention procedural entry."""
        tools = [
            MagicMock(tool="read", status="ok", output="", error=None, iteration=1, step=1),
            MagicMock(tool="edit", status="ok", output="", error=None, iteration=2, step=2),
            MagicMock(tool="bash", status="ok", output="", error=None, iteration=3, step=3),
        ]

        extract_post_task_knowledge(
            task_id="task-timeout-1",
            agent_id="backend-engineer",
            instruction="Complex refactor of auth module",
            status="timeout",
            result_summary="Loop did not complete",
            tool_results=tools,
        )

        results = recall_context("backend-engineer timeout", limit=10)
        assert any("timeout" in " ".join(r.get("tags", [])) for r in results)


class TestPromptInjection:
    """Test that recalled memories are injected into prompts correctly."""

    def test_memory_injection_adds_section(self) -> None:
        """Memories are formatted and added as a Relevant Past Work section."""
        parts = ["# Agent", "## Mission", "Do stuff"]
        memories = [
            {
                "type": "semantic",
                "content": "Pattern: auth bugs need null checks",
                "agent_id": "backend-engineer",
                "tags": ["auth"],
                "similarity": 0.85,
            }
        ]
        _inject_memory_context(parts, memories)
        joined = "\n".join(parts)
        assert "## Relevant Past Work" in joined
        assert "auth bugs need null checks" in joined

    def test_memory_injection_caps_at_max(self) -> None:
        """Only up to max_memories entries are included."""
        parts = ["# Agent"]
        memories = [
            {
                "type": "semantic",
                "content": f"Memory {i}",
                "agent_id": "a",
                "tags": [],
                "similarity": 0.5 + i * 0.1,
            }
            for i in range(10)
        ]
        _inject_memory_context(parts, memories, max_memories=2)
        joined = "\n".join(parts)
        # Should have exactly 2 entries
        assert joined.count("### Previous") == 2

    def test_memory_injection_empty_memories_no_section(self) -> None:
        """Empty memories list adds nothing."""
        parts = ["# Agent", "## Mission"]
        _inject_memory_context(parts, [])
        assert len(parts) == 2

    def test_build_system_prompt_includes_memories(self) -> None:
        """build_system_prompt_typed includes memories when provided."""
        from ai_company.executor.context import AgentContext

        agent = AgentContext(
            name="test-agent",
            role="specialist",
            type="specialist",
            mission="Test things",
        )
        memories = [
            {
                "type": "semantic",
                "content": "Previously: auth bugs always need null checks in middleware",
                "agent_id": "backend-engineer",
                "tags": ["auth"],
                "similarity": 0.9,
            }
        ]
        prompt = build_system_prompt_typed(agent, memories=memories)
        assert "Relevant Past Work" in prompt
        assert "auth bugs always need null checks" in prompt

    def test_dynamic_few_shot_from_memories(self) -> None:
        """_build_dynamic_few_shot returns formatted examples from high-similarity memories."""
        memories = [
            {
                "type": "semantic",
                "content": "Agent solved: fix auth bug using read, edit, bash. Outcome: fixed.",
                "agent_id": "backend-engineer",
                "tags": ["completed", "backend-engineer"],
                "similarity": 0.85,
            },
            {
                "type": "semantic",
                "content": "Agent solved: add tests using read, edit, pytest. Outcome: tests pass.",
                "agent_id": "qa-engineer",
                "tags": ["completed", "qa-engineer"],
                "similarity": 0.75,
            },
        ]
        result = _build_dynamic_few_shot(memories, max_examples=2)
        assert result is not None
        assert "Dynamic Examples" in result
        assert "similarity" in result

    def test_dynamic_few_shot_no_completed_returns_none(self) -> None:
        """Dynamic few-shot returns None when no completed memories exist."""
        memories = [
            {
                "type": "semantic",
                "content": "Some knowledge",
                "agent_id": "a",
                "tags": ["failed"],
                "similarity": 0.9,
            }
        ]
        assert _build_dynamic_few_shot(memories) is None

    def test_dynamic_few_shot_low_similarity_returns_none(self) -> None:
        """Dynamic few-shot returns None when similarity is below threshold."""
        memories = [
            {
                "type": "semantic",
                "content": "Agent solved: fix bug",
                "agent_id": "a",
                "tags": ["completed", "a"],
                "similarity": 0.3,
            }
        ]
        assert _build_dynamic_few_shot(memories) is None

    def test_optimized_prompt_prefers_dynamic_few_shot(self) -> None:
        """build_optimized_system_prompt uses dynamic examples when memories available."""
        from ai_company.executor.context import AgentContext

        agent = AgentContext(
            name="test-agent",
            role="specialist",
            type="specialist",
            mission="Test things",
        )
        memories = [
            {
                "type": "semantic",
                "content": "Agent solved: fix auth bug by reading auth.py, editing the null check, running tests",
                "agent_id": "backend-engineer",
                "tags": ["completed", "backend-engineer"],
                "similarity": 0.85,
            }
        ]
        prompt = build_optimized_system_prompt(
            agent=agent,
            user_prompt="debug the login error",
            memories=memories,
        )
        assert "Dynamic Examples" in prompt


class TestConsolidationDigest:
    """Test that the consolidation scheduler digests old episodic memories."""

    def test_digest_old_episodic(self, memory_store: MemoryStore) -> None:
        """Old episodic entries are digested into semantic/procedural."""
        # Seed many old episodic entries
        for i in range(5):
            entry = memory_store.store(
                "episodic",
                content=f"Task {i}: old task with tool read, edit. Status: completed.",
                agent_id="backend-engineer",
                tags=["completed", "backend-engineer", "read", "edit"],
            )
            # Backdate the created_at
            from datetime import datetime, timedelta, timezone

            entry.created_at = (datetime.now(timezone.utc) - timedelta(days=60)).isoformat()
            memory_store._save("episodic")

        initial_count = len(memory_store._stores.get("episodic", []))
        assert initial_count == 5

        # Run digest
        digested = memory_store._digest_episodic(max_age_days=30)
        assert digested == 5

        # Old entries should be removed
        remaining = len(memory_store._stores.get("episodic", []))
        assert remaining == 0

        # Semantic knowledge should have been created
        semantic = memory_store._stores.get("semantic", [])
        assert len(semantic) >= 1
        assert any("auto-digested" in e.tags for e in semantic)


class TestMetrics:
    """Test metrics collection and snapshot computation."""

    def test_record_task_metrics(self, metrics_collector: LearningMetricsCollector) -> None:
        """Task metrics are recorded and persisted."""
        metrics = TaskMetrics(
            task_id="task-1",
            agent_id="backend-engineer",
            status="completed",
            iterations=3,
            total_tokens=1500,
            total_cost_usd=0.02,
            memory_recall_count=2,
            memory_avg_similarity=0.75,
        )
        metrics_collector.record_task(metrics)
        recent = metrics_collector.get_recent_tasks(1)
        assert len(recent) == 1
        assert recent[0]["task_id"] == "task-1"

    def test_compute_snapshot(self, metrics_collector: LearningMetricsCollector) -> None:
        """Snapshot computation returns correct aggregates."""
        for i in range(5):
            metrics_collector.record_task(
                TaskMetrics(
                    task_id=f"task-{i}",
                    agent_id="a",
                    status="completed",
                    iterations=2 + i,
                    total_tokens=1000 + i * 200,
                )
            )
        snap = metrics_collector.compute_snapshot()
        assert snap.total_tasks_recorded == 5
        assert snap.avg_tokens_per_task > 0
        assert snap.avg_iterations_per_task > 0
        assert snap.error_rate == 0.0

    def test_error_rate_in_snapshot(self, metrics_collector: LearningMetricsCollector) -> None:
        """Error rate is computed correctly."""
        for i in range(4):
            metrics_collector.record_task(
                TaskMetrics(task_id=f"t{i}", agent_id="a", status="completed", iterations=1)
            )
        metrics_collector.record_task(
            TaskMetrics(task_id="t-fail", agent_id="a", status="failed", iterations=5)
        )
        snap = metrics_collector.compute_snapshot()
        assert snap.error_rate == pytest.approx(0.2, abs=0.01)

    def test_trend_detection(self, metrics_collector: LearningMetricsCollector) -> None:
        """Trend detection flags improvement when recent tasks use fewer tokens."""
        # First 10 tasks: 3000 tokens each
        for i in range(10):
            metrics_collector.record_task(
                TaskMetrics(task_id=f"old-{i}", agent_id="a", status="completed", total_tokens=3000)
            )
        # Next 10 tasks: 1000 tokens each (improvement)
        for i in range(10):
            metrics_collector.record_task(
                TaskMetrics(task_id=f"new-{i}", agent_id="a", status="completed", total_tokens=1000)
            )
        snap = metrics_collector.compute_snapshot()
        assert snap.token_trend == "improving"

    def test_consolidation_stats_recorded(
        self, metrics_collector: LearningMetricsCollector
    ) -> None:
        """Consolidation stats are accumulated in the snapshot."""
        # Seed a snapshot first
        metrics_collector.compute_snapshot()
        metrics_collector.record_consolidation(entries_pruned=10, episodic_digested=5)
        metrics_collector.record_consolidation(entries_pruned=5, episodic_digested=3)
        snap = metrics_collector.compute_snapshot()
        assert snap.entries_pruned_total == 15
        assert snap.episodic_digested_total == 8

    def test_persistence(self, tmp_path: Path) -> None:
        """Metrics survive restart (loaded from disk)."""
        c1 = LearningMetricsCollector(base_dir=tmp_path)
        c1.record_task(
            TaskMetrics(task_id="persist-1", agent_id="a", status="completed", iterations=2)
        )
        # Create new collector pointing to same dir
        c2 = LearningMetricsCollector(base_dir=tmp_path)
        tasks = c2.get_recent_tasks(10)
        assert len(tasks) == 1
        assert tasks[0]["task_id"] == "persist-1"


class TestConsolidationScheduler:
    """Test the ConsolidationScheduler integration with MemoryStore."""

    def test_scheduler_runs_consolidation(self, memory_store: MemoryStore) -> None:
        """Scheduler triggers consolidation after tick_interval ticks."""
        config = ConsolidationConfig(tick_interval=3, entry_threshold=100)
        scheduler = ConsolidationScheduler(store=memory_store, config=config)

        # First 2 ticks: no consolidation
        assert scheduler.on_tick() is None
        assert scheduler.on_tick() is None

        # Third tick: consolidation runs
        result = scheduler.on_tick()
        assert result is not None

    def test_scheduler_threshold_trigger(self, memory_store: MemoryStore) -> None:
        """Scheduler triggers when entry threshold is exceeded."""
        config = ConsolidationConfig(tick_interval=1000, entry_threshold=3)
        scheduler = ConsolidationScheduler(store=memory_store, config=config)

        # Add entries to exceed threshold
        for i in range(5):
            memory_store.store("episodic", content=f"entry {i}", agent_id="a", tags=[])

        result = scheduler.on_tick()
        assert result is not None
