"""Tests for cost tracker integration with LLMClient and providers."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ai_company.llm.providers.base import ChatResponse
from ai_company.llm.cost_tracker import CostTracker, UsageRecord


# ---------------------------------------------------------------------------
# ChatResponse token fields
# ---------------------------------------------------------------------------


class TestChatResponseTokenFields:
    """Verify ChatResponse exposes dedicated token count fields."""

    def test_explicit_token_counts(self) -> None:
        resp = ChatResponse(
            content="hello",
            model="gpt-4o",
            provider="openai",
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
        )
        assert resp.prompt_tokens == 100
        assert resp.completion_tokens == 50
        assert resp.total_tokens == 150

    def test_auto_derived_total_tokens(self) -> None:
        resp = ChatResponse(
            content="hello",
            model="gpt-4o",
            provider="openai",
            prompt_tokens=100,
            completion_tokens=50,
        )
        assert resp.total_tokens == 150

    def test_usage_dict_populated_from_fields(self) -> None:
        resp = ChatResponse(
            content="hello",
            model="gpt-4o",
            provider="openai",
            prompt_tokens=100,
            completion_tokens=50,
        )
        assert resp.usage["prompt_tokens"] == 100
        assert resp.usage["completion_tokens"] == 50

    def test_zero_tokens(self) -> None:
        resp = ChatResponse(
            content="hello",
            model="gpt-4o",
            provider="openai",
        )
        assert resp.prompt_tokens == 0
        assert resp.completion_tokens == 0
        assert resp.total_tokens == 0


# ---------------------------------------------------------------------------
# CostTracker.record_usage
# ---------------------------------------------------------------------------


class TestCostTrackerRecordUsage:
    """Verify CostTracker records and persists usage correctly."""

    def test_record_usage_returns_usage_record(self, tmp_path: Path) -> None:
        tracker = CostTracker(results_dir=tmp_path)
        record = tracker.record_usage(
            model="gpt-4o",
            provider="openai",
            agent_name="test-agent",
            task_id="task-001",
            prompt_tokens=100,
            completion_tokens=50,
        )
        assert isinstance(record, UsageRecord)
        assert record.prompt_tokens == 100
        assert record.completion_tokens == 50
        assert record.cost_usd > 0

    def test_record_usage_persists_to_jsonl(self, tmp_path: Path) -> None:
        tracker = CostTracker(results_dir=tmp_path)
        tracker.record_usage(
            model="gpt-4o",
            provider="openai",
            agent_name="test-agent",
            task_id="task-001",
            prompt_tokens=100,
            completion_tokens=50,
        )
        log_path = tmp_path / "cost_log.jsonl"
        assert log_path.exists()
        lines = log_path.read_text().strip().split("\n")
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert data["model"] == "gpt-4o"
        assert data["prompt_tokens"] == 100
        assert data["completion_tokens"] == 50

    def test_daily_summary(self, tmp_path: Path) -> None:
        tracker = CostTracker(results_dir=tmp_path)
        tracker.record_usage(
            model="gpt-4o", provider="openai", agent_name="a",
            task_id="t1", prompt_tokens=100, completion_tokens=50,
        )
        tracker.record_usage(
            model="gpt-4o", provider="openai", agent_name="a",
            task_id="t2", prompt_tokens=200, completion_tokens=100,
        )
        summary = tracker.get_daily_summary()
        assert summary["call_count"] == 2
        assert summary["total_prompt_tokens"] == 300
        assert summary["total_completion_tokens"] == 150

    def test_task_summary(self, tmp_path: Path) -> None:
        tracker = CostTracker(results_dir=tmp_path)
        tracker.record_usage(
            model="gpt-4o", provider="openai", agent_name="a",
            task_id="t1", prompt_tokens=100, completion_tokens=50,
        )
        tracker.record_usage(
            model="gpt-4o", provider="openai", agent_name="a",
            task_id="t1", prompt_tokens=200, completion_tokens=100,
        )
        tracker.record_usage(
            model="gpt-4o", provider="openai", agent_name="a",
            task_id="t2", prompt_tokens=50, completion_tokens=25,
        )
        summary = tracker.get_task_summary("t1")
        assert summary["call_count"] == 2
        assert summary["total_prompt_tokens"] == 300


# ---------------------------------------------------------------------------
# CostTracker budget enforcement
# ---------------------------------------------------------------------------


class TestCostTrackerBudget:
    """Verify budget checks work correctly."""

    def test_daily_budget_check(self, tmp_path: Path) -> None:
        tracker = CostTracker(results_dir=tmp_path, daily_budget_usd=0.01)
        allowed, reason = tracker.check_budget("t1", proposed_cost=0.005)
        assert allowed is True
        tracker.record_usage(
            model="gpt-4o", provider="openai", agent_name="a",
            task_id="t1", prompt_tokens=10000, completion_tokens=10000,
        )
        allowed, reason = tracker.check_budget("t1", proposed_cost=0.01)
        assert allowed is False
        assert "Daily budget exceeded" in reason

    def test_task_budget_check(self, tmp_path: Path) -> None:
        tracker = CostTracker(results_dir=tmp_path, task_budget_usd=0.01)
        allowed, _ = tracker.check_budget("t1", proposed_cost=0.005)
        assert allowed is True
        tracker.record_usage(
            model="gpt-4o", provider="openai", agent_name="a",
            task_id="t1", prompt_tokens=10000, completion_tokens=10000,
        )
        allowed, reason = tracker.check_budget("t1", proposed_cost=0.01)
        assert allowed is False
        assert "Task budget exceeded" in reason


# ---------------------------------------------------------------------------
# LLMClient cost tracker integration
# ---------------------------------------------------------------------------


class TestLLMClientCostIntegration:
    """Verify LLMClient records token usage when a CostTracker is set."""

    @patch("ai_company.llm.client.ModelRouter")
    def test_execute_task_records_usage(self, mock_router_cls: MagicMock, tmp_path: Path) -> None:
        from ai_company.llm.client import LLMClient

        # Set up mock router
        mock_router = mock_router_cls.return_value
        mock_route = MagicMock()
        mock_route.tier = "fast"
        mock_route.provider = "ollama"
        mock_route.model = "llama3.1:8b"
        mock_router.resolve.return_value = mock_route
        mock_tier = MagicMock()
        mock_tier.providers = []
        mock_router.get_tier.return_value = mock_tier
        mock_router.list_providers.return_value = []

        # Set up cost tracker
        tracker = CostTracker(results_dir=tmp_path)

        client = LLMClient(cost_tracker=tracker)

        # Mock the provider
        mock_provider = MagicMock()
        mock_provider.is_available.return_value = True
        mock_provider.chat.return_value = ChatResponse(
            content='{"result": "done", "done": true}',
            model="llama3.1:8b",
            provider="ollama",
            prompt_tokens=100,
            completion_tokens=50,
        )
        client._providers = {"ollama": mock_provider}

        result = client.execute_task(
            agent_name="test-agent",
            task_instruction="do something",
            task_id="task-test-001",
        )

        assert result is not None
        # Verify cost tracker recorded usage
        summary = tracker.get_task_summary("task-test-001")
        assert summary["call_count"] == 1
        assert summary["total_prompt_tokens"] == 100
        assert summary["total_completion_tokens"] == 50

    @patch("ai_company.llm.client.ModelRouter")
    def test_execute_task_no_tracking_without_task_id(self, mock_router_cls: MagicMock, tmp_path: Path) -> None:
        from ai_company.llm.client import LLMClient

        mock_router = mock_router_cls.return_value
        mock_route = MagicMock()
        mock_route.tier = "fast"
        mock_route.provider = "ollama"
        mock_route.model = "llama3.1:8b"
        mock_router.resolve.return_value = mock_route
        mock_tier = MagicMock()
        mock_tier.providers = []
        mock_router.get_tier.return_value = mock_tier
        mock_router.list_providers.return_value = []

        tracker = CostTracker(results_dir=tmp_path)
        client = LLMClient(cost_tracker=tracker)

        mock_provider = MagicMock()
        mock_provider.is_available.return_value = True
        mock_provider.chat.return_value = ChatResponse(
            content='{"result": "done", "done": true}',
            model="llama3.1:8b",
            provider="ollama",
            prompt_tokens=100,
            completion_tokens=50,
        )
        client._providers = {"ollama": mock_provider}

        # No task_id provided — should not record
        client.execute_task(
            agent_name="test-agent",
            task_instruction="do something",
        )

        summary = tracker.get_task_summary("nonexistent")
        assert summary["call_count"] == 0

    @patch("ai_company.llm.client.ModelRouter")
    def test_execute_task_no_tracker(self, mock_router_cls: MagicMock) -> None:
        from ai_company.llm.client import LLMClient

        mock_router = mock_router_cls.return_value
        mock_route = MagicMock()
        mock_route.tier = "fast"
        mock_route.provider = "ollama"
        mock_route.model = "llama3.1:8b"
        mock_router.resolve.return_value = mock_route
        mock_tier = MagicMock()
        mock_tier.providers = []
        mock_router.get_tier.return_value = mock_tier
        mock_router.list_providers.return_value = []

        # No cost tracker
        client = LLMClient()

        mock_provider = MagicMock()
        mock_provider.is_available.return_value = True
        mock_provider.chat.return_value = ChatResponse(
            content='{"result": "done", "done": true}',
            model="llama3.1:8b",
            provider="ollama",
            prompt_tokens=100,
            completion_tokens=50,
        )
        client._providers = {"ollama": mock_provider}

        # Should work without error
        result = client.execute_task(
            agent_name="test-agent",
            task_instruction="do something",
            task_id="task-001",
        )
        assert result is not None
