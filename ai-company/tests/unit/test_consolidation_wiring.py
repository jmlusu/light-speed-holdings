"""Tests for PRE-06: Wire GAP-005 Memory Consolidation lifecycle.

Verifies that the ConsolidationScheduler's start() and stop() are called
during Executor.start() and Executor.stop() respectively.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest


class TestConsolidationWiring:
    """PRE-06: Verify ConsolidationScheduler lifecycle in Executor."""

    def _make_executor(self, monkeypatch: pytest.MonkeyPatch) -> Any:
        """Create a minimal Executor with mocked dependencies."""
        import tempfile

        tmp_path = Path(tempfile.mkdtemp(prefix="test_executor_"))
        monkeypatch.chdir(tmp_path)

        # Set up minimal files
        company_dir = tmp_path / "company"
        company_dir.mkdir(exist_ok=True)
        (company_dir / "models.yaml").write_text(
            json.dumps({
                "providers": {"opencode": {"backend": "openai_compatible", "default_model": "big-pickle", "api_base": "http://localhost"}},
                "tiers": {"fast": {"description": "Fast", "providers": [{"provider": "opencode", "model": "big-pickle"}]}},
                "routing": [{"agent_type": "Specialist", "tier": "fast"}],
            }),
            encoding="utf-8",
        )
        (company_dir / "agent-registry.json").write_text(
            json.dumps([{"name": "test", "role": "Test", "type": "Specialist", "department": "Test"}]),
            encoding="utf-8",
        )
        (tmp_path / ".opencode").mkdir(exist_ok=True)
        (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
        (tmp_path / "orchestrator").mkdir(exist_ok=True)
        (tmp_path / "orchestrator" / "approvals.yaml").write_text("requests: []", encoding="utf-8")

        with patch("ai_company.executor.loop.MessageBus"):
            from ai_company.executor.loop import Executor
            executor = Executor(
                config_path=str(company_dir / "models.yaml"),
                registry_path=str(company_dir / "agent-registry.json"),
                agents_dir=str(tmp_path / ".opencode" / "agents"),
                results_dir=str(tmp_path / "results"),
            )
        return executor

    def test_consolidation_scheduler_initialized(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Executor should have a ConsolidationScheduler with correct config."""
        executor = self._make_executor(monkeypatch)

        from ai_company.memory.consolidation import ConsolidationScheduler
        assert isinstance(executor._consolidation_scheduler, ConsolidationScheduler)
        assert executor._consolidation_config.tick_interval == 50

    def test_tick_calls_on_tick(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Executor.tick() should call consolidation_scheduler.on_tick()."""
        executor = self._make_executor(monkeypatch)
        executor._consolidation_scheduler.on_tick = MagicMock(return_value=None)

        executor.tick()

        executor._consolidation_scheduler.on_tick.assert_called_once()

    def test_stop_calls_consolidation_stop(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Executor.stop() should call consolidation_scheduler.stop()."""
        executor = self._make_executor(monkeypatch)
        executor._consolidation_scheduler.stop = MagicMock()

        executor.stop()

        executor._consolidation_scheduler.stop.assert_called_once()

    def test_start_wires_consolidation(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Executor.start() should call consolidation_scheduler.start().

        We test this by checking the method exists and is called via
        the start() flow. We mock time.sleep to prevent blocking.
        """
        executor = self._make_executor(monkeypatch)
        executor._consolidation_scheduler.start = MagicMock()
        executor._consolidation_scheduler.stop = MagicMock()

        # tick returns 0 immediately; after one iteration set running=False
        call_count = 0

        def fake_tick() -> int:
            nonlocal call_count
            call_count += 1
            executor.running = False
            return 0

        executor.tick = fake_tick
        executor.start()

        executor._consolidation_scheduler.start.assert_called_once()

    def test_stop_is_idempotent(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Calling stop() multiple times should not raise."""
        executor = self._make_executor(monkeypatch)
        executor.stop()
        executor.stop()  # Should not raise
