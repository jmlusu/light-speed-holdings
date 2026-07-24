"""Tests for PRE-11: Token Counting Integration.

Verifies pre-flight token estimation and budget checking before LLM calls
in both AgentLoop and LLMClient.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from ai_company.executor.agent_loop import AgentLoop, LoopConfig
from ai_company.llm.client import LLMClient, estimate_call_cost
from ai_company.llm.cost_tracker import CostTracker
from ai_company.llm.providers.base import LLMProviderError


class TestEstimateCallCost:
    """PRE-11: Verify the estimate_call_cost function."""

    def test_estimate_with_empty_prompts(self) -> None:
        """Empty prompts should still produce a non-zero cost estimate."""
        cost = estimate_call_cost("", "")
        assert cost > 0.0

    def test_estimate_scales_with_prompt_length(self) -> None:
        """Longer prompts should produce higher cost estimates."""
        short_cost = estimate_call_cost("sys", "Do something")
        long_cost = estimate_call_cost("sys", "x " * 10000)
        assert long_cost > short_cost

    def test_estimate_uses_model_costs(self) -> None:
        """Estimate should use the cost table for the given model."""
        # Unknown model falls back to _default
        cost = estimate_call_cost("system", "user", model="unknown-model")
        assert cost > 0.0

    def test_estimate_with_known_model(self) -> None:
        """Estimate should use the cost table for a known model."""
        cost = estimate_call_cost("sys", "prompt", model="gpt-4o-mini")
        assert cost > 0.0

    def test_estimate_tokens_heuristic(self) -> None:
        """_estimate_tokens should produce reasonable estimates."""
        from ai_company.executor.agent_loop import AgentLoop

        # A short string should be ~5 tokens
        tokens = AgentLoop._estimate_tokens("hello world")
        assert 2 <= tokens <= 20

        # A longer string should have more tokens
        long_tokens = AgentLoop._estimate_tokens("hello world " * 100)
        assert long_tokens > tokens


class TestAgentLoopBudgetCheck:
    """PRE-11: Verify pre-flight budget check in AgentLoop."""

    def test_budget_check_uses_estimated_cost(self) -> None:
        """AgentLoop should estimate cost before calling check_budget."""
        mock_cost_tracker = MagicMock(spec=CostTracker)
        mock_cost_tracker.check_budget.return_value = (True, "within budget")

        llm = MagicMock()
        runner = MagicMock()
        loop = AgentLoop(
            llm=llm,
            runner=runner,
            cost_tracker=mock_cost_tracker,
            config=LoopConfig(max_iterations=1, max_tokens=100),
        )

        # Mock the LLM call to return a successful response
        mock_response = MagicMock()
        mock_response.content = '{"result": "done", "done": true}'
        mock_response.usage = {"prompt_tokens": 10, "completion_tokens": 5}
        mock_response.model = "test-model"
        mock_response.provider = "test"
        loop._call_llm = MagicMock(return_value=mock_response)

        from ai_company.executor.context import AgentContext

        agent = AgentContext(
            name="test", role="Test Agent", type="Specialist", department="Test",
            mission="", responsibilities=[], tools=[], permission="Execute",
        )

        loop.run(agent, "Do something", task_id="task-1")

        # check_budget should be called with a non-zero proposed_cost
        mock_cost_tracker.check_budget.assert_called()
        call_args = mock_cost_tracker.check_budget.call_args
        assert call_args[0][0] == "task-1"  # task_id
        # proposed_cost should be > 0 (estimated)
        proposed = call_args[1].get("proposed_cost", call_args[0][1] if len(call_args[0]) > 1 else 0)
        assert proposed > 0.0

    def test_budget_exceeded_stops_loop(self) -> None:
        """When budget is exceeded, AgentLoop should stop immediately."""
        mock_cost_tracker = MagicMock(spec=CostTracker)
        mock_cost_tracker.check_budget.return_value = (
            False, "Daily budget exceeded: $10.00 > $5.00"
        )

        llm = MagicMock()
        runner = MagicMock()
        loop = AgentLoop(
            llm=llm,
            runner=runner,
            cost_tracker=mock_cost_tracker,
            config=LoopConfig(max_iterations=5),
        )

        from ai_company.executor.context import AgentContext

        agent = AgentContext(
            name="test", role="Test Agent", type="Specialist", department="Test",
            mission="", responsibilities=[], tools=[], permission="Execute",
        )

        with patch.object(loop, "_call_llm") as mock_call:
            result = loop.run(agent, "Do something", task_id="task-1")

        # Loop should have stopped early
        assert result.iterations == 0
        assert "Budget exceeded" in result.error
        # LLM should never have been called
        mock_call.assert_not_called()


class TestLLMClientBudgetCheck:
    """PRE-11: Verify pre-flight budget check in LLMClient."""

    def test_budget_check_before_llm_call(self) -> None:
        """LLMClient.execute_task should check budget before calling LLM."""
        mock_tracker = MagicMock(spec=CostTracker)
        mock_tracker.check_budget.return_value = (False, "Over budget")

        client = LLMClient.__new__(LLMClient)
        client.router = MagicMock()
        client.router.resolve.return_value = MagicMock(
            provider="test", model="test-model", tier="fast"
        )
        client.router.get_tier.return_value = MagicMock(
            providers=[MagicMock(provider="test", model="test-model")]
        )
        client._providers = {"test": MagicMock()}
        client._providers["test"].is_available.return_value = True
        client._circuit_breakers = {"test": MagicMock()}
        client._circuit_breakers["test"].is_available = True
        client._cost_tracker = mock_tracker

        with pytest.raises(LLMProviderError, match="budget check failed"):
            client.execute_task(
                agent_name="test",
                task_instruction="Do something",
                task_id="task-1",
            )

        # Budget check should have been called with estimated cost > 0
        mock_tracker.check_budget.assert_called_once()
        call_args = mock_tracker.check_budget.call_args
        proposed = call_args[1].get("proposed_cost", 0)
        assert proposed > 0.0
