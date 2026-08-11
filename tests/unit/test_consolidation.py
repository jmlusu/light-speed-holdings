"""Unit tests for memory consolidation cadence (GAP-005).

The executor drives ``ConsolidationScheduler.on_tick()`` once per ``tick()``
(``executor/loop.py``).  These tests verify the scheduler self-throttles: a
heavy prune/dedup pass only runs when the configured cadence
(``tick_interval``) or the entry threshold is reached — never on every tick —
so the executor hot path is never blocked.
"""

from __future__ import annotations

from pathlib import Path

from ai_company.memory.consolidation import ConsolidationConfig, ConsolidationScheduler
from ai_company.memory.engine import MemoryStore


class _FakeStore:
    """MemoryStore stand-in that records prune/consolidate calls."""

    def __init__(self, stats: dict[str, int] | None = None) -> None:
        self._stats = dict(stats or {})
        self.prune_calls = 0
        self.consolidate_calls = 0

    def stats(self) -> dict[str, int]:
        return dict(self._stats)

    def prune(
        self,
        max_age_days: int | None = None,
        max_entries_per_type: int | None = None,
    ) -> int:
        self.prune_calls += 1
        return 0

    def consolidate_all(self) -> dict[str, int]:
        self.consolidate_calls += 1
        return {
            "semantic_duplicates_removed": 0,
            "aggregates_created": 0,
            "types_processed": 0,
        }


class TestConsolidationCadence:
    """Consolidation runs on the configured cadence and throttles in between."""

    def test_on_tick_increments_counter_without_running(self) -> None:
        """Default tick_interval=50: on_tick() never runs on the first tick."""
        scheduler = ConsolidationScheduler(store=_FakeStore())

        assert scheduler.tick_count == 0
        result = scheduler.on_tick()

        assert result is None  # throttled — cadence not reached
        assert scheduler.tick_count == 1
        assert scheduler.last_consolidated is None

    def test_on_tick_runs_exactly_when_interval_reached(self) -> None:
        """Consolidation runs on the tick whose count matches the interval."""
        store = _FakeStore()
        scheduler = ConsolidationScheduler(
            store=store,
            config=ConsolidationConfig(tick_interval=3),
        )

        assert scheduler.on_tick() is None  # tick 1
        assert scheduler.on_tick() is None  # tick 2
        summary = scheduler.on_tick()  # tick 3 -> runs

        assert summary is not None
        assert "entries_pruned" in summary
        assert "semantic_duplicates_removed" in summary
        assert store.prune_calls == 1
        assert store.consolidate_calls == 1
        assert scheduler.last_consolidated is not None

    def test_on_tick_throttles_immediately_after_a_run(self) -> None:
        """Consolidation never runs on consecutive ticks (no hot-path op)."""
        store = _FakeStore()
        scheduler = ConsolidationScheduler(
            store=store,
            config=ConsolidationConfig(tick_interval=2),
        )

        assert scheduler.on_tick() is None  # tick 1
        assert scheduler.on_tick() is not None  # tick 2 -> runs
        assert scheduler.on_tick() is None  # tick 3 -> throttled
        assert store.consolidate_calls == 1

    def test_entry_threshold_triggers_when_interval_disabled(self) -> None:
        """Memory growth alone triggers consolidation when tick cadence is off."""
        store = _FakeStore(stats={"episodic": 10})
        scheduler = ConsolidationScheduler(
            store=store,
            config=ConsolidationConfig(tick_interval=0, entry_threshold=5),
        )

        summary = scheduler.on_tick()

        assert summary is not None
        assert store.consolidate_calls == 1

    def test_stays_idle_below_threshold_with_interval_disabled(self) -> None:
        """tick_interval=0 with a small store stays idle."""
        scheduler = ConsolidationScheduler(
            store=_FakeStore(stats={"episodic": 3}),
            config=ConsolidationConfig(tick_interval=0, entry_threshold=500),
        )

        assert scheduler.on_tick() is None
        assert scheduler.last_consolidated is None

    def test_on_tick_without_store_returns_error(self) -> None:
        """A due consolidation pass without a store degrades gracefully."""
        scheduler = ConsolidationScheduler(
            store=None,
            config=ConsolidationConfig(tick_interval=1),
        )

        assert scheduler.on_tick() == {"error": "no_store"}
        assert scheduler.last_consolidated is None


class TestConsolidationWithRealStore:
    """Cadence against a real MemoryStore — no LLM required."""

    def test_consolidation_dedupes_and_prunes_real_store(self, tmp_path: Path) -> None:
        store = MemoryStore(base_dir=tmp_path / "memory")
        store.store("episodic", "Task 1 completed", agent_id="a1", tags=["ok"])
        store.store("semantic", "Python is a language", agent_id="a1", tags=["learn"])
        store.store("semantic", "python is a language", agent_id="a1", tags=["learn"])

        scheduler = ConsolidationScheduler(
            store=store,
            config=ConsolidationConfig(tick_interval=1),
        )
        summary = scheduler.on_tick()

        assert summary is not None
        assert summary["entries_pruned"] == 0
        assert summary["semantic_duplicates_removed"] == 1
        assert scheduler.last_consolidated is not None
