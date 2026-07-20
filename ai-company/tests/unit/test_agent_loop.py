"""Tests for the multi-turn agentic loop (ReAct pattern)."""

from __future__ import annotations

import json
from pathlib import Path
import concurrent.futures
from unittest.mock import MagicMock

from ai_company.executor.agent_loop import (
    AgentLoop,
    LoopConfig,
    LoopResult,
)
from ai_company.executor.context import AgentContext
from ai_company.executor.tool_runner import ToolRunner
from ai_company.llm.providers.base import ChatResponse, LLMProviderError


# ── Auto-approving HITL gate ──────────────────────────────────────────
#
# The tier-aware ToolRunner classifies some tool actions (e.g. ``write``)
# as Tier 2 (Single Approver), which requires HITL approval.  To keep the
# multi-turn loop tests independent of the production ApprovalGate (and of
# whether ``tool_runner`` falls back to a no-gate warning path), we inject a
# self-contained auto-approving gate.  It satisfies BOTH the synchronous
# path (``request_and_wait_sync``) and the non-blocking path
# (``request_and_wait`` returning a resolved Future), so the test passes
# regardless of which branch ToolRunner uses.


class _AutoApprovingGate:
    """A stand-in HITLGate that always approves."""

    def request_and_wait_sync(
        self,
        task_id: str = "",
        agent_id: str = "",
        tool: str = "",
        args: dict | None = None,
    ) -> bool:
        return True

    def request_and_wait(
        self,
        task_id: str = "",
        agent_id: str = "",
        tool: str = "",
        args: dict | None = None,
    ) -> concurrent.futures.Future[bool]:
        future: concurrent.futures.Future[bool] = concurrent.futures.Future()
        future.set_result(True)
        return future


# ── Helpers ─────────────────────────────────────────────────────────


def _make_agent(
    name: str = "test-agent",
    agent_type: str = "Specialist",
    tools: list[str] | None = None,
) -> AgentContext:
    """Create a minimal AgentContext for testing."""
    return AgentContext(
        name=name,
        role=f"{name} agent",
        type=agent_type,
        department="Engineering",
        mission="Complete assigned tasks.",
        responsibilities=["Execute tasks", "Report results"],
        tools=tools or ["read", "write", "execute", "grep", "list"],
    )


def _make_chat_response(
    content: str,
    model: str = "test-model",
    provider: str = "mock",
    prompt_tokens: int = 100,
    completion_tokens: int = 50,
) -> ChatResponse:
    """Create a ChatResponse with the given JSON content."""
    return ChatResponse(
        content=content,
        model=model,
        provider=provider,
        usage={
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
        },
    )


def _json_response(
    thought: str = "Thinking...",
    plan: list[dict] | None = None,
    result: str = "Done.",
    done: bool = True,
) -> str:
    """Build a valid JSON agent response string."""
    return json.dumps({
        "thought": thought,
        "plan": plan or [],
        "result": result,
        "done": done,
    })


def _setup_llm_client(tmp_path: Path) -> MagicMock:
    """Create a mock LLMClient with the router and provider stubs."""
    models = {
        "providers": {
            "mock_provider": {
                "backend": "openai_compatible",
                "default_model": "test-model",
                "api_base": "http://localhost:9999",
            },
        },
        "tiers": {
            "standard": {
                "description": "Test tier",
                "providers": [{"provider": "mock_provider", "model": "test-model"}],
            },
        },
        "routing": [
            {"agent_type": "Specialist", "tier": "standard"},
            {"agent_type": "Executive", "tier": "standard"},
        ],
    }
    (tmp_path / "company").mkdir(exist_ok=True)
    (tmp_path / "company" / "models.yaml").write_text(
        json.dumps(models), encoding="utf-8"
    )
    (tmp_path / "company" / "agent-registry.json").write_text(
        json.dumps([]), encoding="utf-8"
    )

    mock_provider = MagicMock()
    mock_provider.is_available.return_value = True
    mock_provider.chat.return_value = _make_chat_response(_json_response())

    mock_route = MagicMock(provider="mock_provider", model="test-model", tier="standard")
    mock_tier = MagicMock(providers=[MagicMock(provider="mock_provider", model="test-model")])

    client = MagicMock()
    client.router.resolve.return_value = mock_route
    client.router.get_tier.return_value = mock_tier
    client.router.resolve_with_fallback.return_value = [mock_route]
    client.get_provider.return_value = mock_provider

    return client, mock_provider


# ── Test: single-turn completion (no tools needed) ──────────────────


class TestSingleTurnCompletion:
    """When the LLM returns done=True with an empty plan on the first call."""

    def test_completes_immediately(self, tmp_path: Path) -> None:
        client, mock_provider = _setup_llm_client(tmp_path)
        runner = ToolRunner(project_root=tmp_path)
        config = LoopConfig(max_iterations=10)

        loop = AgentLoop(llm=client, runner=runner, config=config)
        agent = _make_agent()
        response_json = _json_response(
            thought="This is straightforward, no tools needed.",
            plan=[],
            result="Task completed successfully.",
            done=True,
        )
        mock_provider.chat.return_value = _make_chat_response(response_json)

        result = loop.run(
            agent=agent,
            user_prompt="What is 2+2?",
            task_id="task-001",
        )

        assert result.done is True
        assert result.iterations == 1
        assert "4" in result.final_response or "completed" in result.final_response.lower()
        assert len(result.tool_results) == 0
        assert mock_provider.chat.call_count == 1

    def test_result_text_used(self, tmp_path: Path) -> None:
        client, mock_provider = _setup_llm_client(tmp_path)
        runner = ToolRunner(project_root=tmp_path)
        loop = AgentLoop(llm=client, runner=runner, config=LoopConfig())

        mock_provider.chat.return_value = _make_chat_response(
            _json_response(result="The answer is 4.", done=True)
        )

        result = loop.run(agent=_make_agent(), user_prompt="What is 2+2?")
        assert result.final_response == "The answer is 4."


# ── Test: multi-turn tool loop ──────────────────────────────────────


class TestMultiTurnToolLoop:
    """Simulate 3 iterations: read → write → done."""

    def test_three_iteration_loop(self, tmp_path: Path) -> None:
        client, mock_provider = _setup_llm_client(tmp_path)

        # Create a file for the read tool
        (tmp_path / "input.py").write_text("x = 1", encoding="utf-8")

        runner = ToolRunner(project_root=tmp_path)
        config = LoopConfig(max_iterations=10)
        # Inject a self-contained auto-approving HITL gate so the Tier2
        # ``write`` step is approved regardless of ToolRunner's gate path.
        loop = AgentLoop(llm=client, runner=runner, hitl_gate=_AutoApprovingGate(), config=config)
        agent = _make_agent()

        # LLM responses for each iteration:
        # 1) Read the file → plan has a read tool
        # 2) Write a transformed file → plan has a write tool
        # 3) Done → no plan, just result
        resp1 = _make_chat_response(_json_response(
            thought="I need to read the input file first.",
            plan=[{"tool": "read", "args": {"path": "input.py"}}],
            done=False,
        ))
        resp2 = _make_chat_response(_json_response(
            thought="I've read the file. Now I'll write the output.",
            plan=[{"tool": "write", "args": {"path": "output.py", "content": "x = 2"}}],
            done=False,
        ))
        resp3 = _make_chat_response(_json_response(
            thought="File written successfully.",
            result="Transformed input.py → output.py",
            done=True,
        ))

        mock_provider.chat.side_effect = [resp1, resp2, resp3]

        result = loop.run(
            agent=agent,
            user_prompt="Read input.py and write a transformed output.py",
            task_id="task-002",
        )

        assert result.done is True
        assert result.iterations == 3
        assert len(result.tool_results) == 2
        assert result.tool_results[0].tool == "read"
        assert result.tool_results[1].tool == "write"
        assert "output.py" in result.final_response

        # Verify files were actually written
        assert (tmp_path / "output.py").read_text(encoding="utf-8") == "x = 2"

    def test_iteration_feedback_formatted(self, tmp_path: Path) -> None:
        """Verify the feedback text includes tool results."""
        client, mock_provider = _setup_llm_client(tmp_path)
        (tmp_path / "data.txt").write_text("hello", encoding="utf-8")

        runner = ToolRunner(project_root=tmp_path)
        loop = AgentLoop(llm=client, runner=runner, config=LoopConfig(max_iterations=3))

        # Iteration 1: read the file
        resp1 = _make_chat_response(_json_response(
            plan=[{"tool": "read", "args": {"path": "data.txt"}}],
            done=False,
        ))
        # Iteration 2: done
        resp2 = _make_chat_response(_json_response(
            result="Read the file.",
            done=True,
        ))

        mock_provider.chat.side_effect = [resp1, resp2]

        result = loop.run(agent=_make_agent(), user_prompt="Read data.txt")

        assert result.iterations == 2

        # The second call's user_prompt should contain tool results
        second_call_args = mock_provider.chat.call_args_list[1]
        user_prompt = second_call_args[1]["user_prompt"] if "user_prompt" in second_call_args[1] else second_call_args[0][1]
        assert "Tool Execution Results" in user_prompt
        assert "data.txt" in user_prompt


# ── Test: max iterations stops the loop ──────────────────────────────


class TestMaxIterations:
    """The loop must stop at the configured cap."""

    def test_stops_at_max_iterations(self, tmp_path: Path) -> None:
        client, mock_provider = _setup_llm_client(tmp_path)
        runner = ToolRunner(project_root=tmp_path)
        config = LoopConfig(max_iterations=3)
        loop = AgentLoop(llm=client, runner=runner, config=config)

        # LLM always wants to do more tools — never sets done=True
        infinite_plan_response = _make_chat_response(_json_response(
            thought="Let me keep going...",
            plan=[{"tool": "list", "args": {"path": "."}}],
            done=False,
        ))
        mock_provider.chat.return_value = infinite_plan_response

        result = loop.run(agent=_make_agent(), user_prompt="Do something")

        assert result.iterations == 3
        assert result.done is False
        assert "Max iterations" in result.error
        assert len(result.tool_results) == 3

    def test_max_iterations_one(self, tmp_path: Path) -> None:
        client, mock_provider = _setup_llm_client(tmp_path)
        runner = ToolRunner(project_root=tmp_path)
        config = LoopConfig(max_iterations=1)
        loop = AgentLoop(llm=client, runner=runner, config=config)

        mock_provider.chat.return_value = _make_chat_response(_json_response(
            plan=[{"tool": "list", "args": {"path": "."}}],
            done=False,
        ))

        result = loop.run(agent=_make_agent(), user_prompt="Do something")

        assert result.iterations == 1
        assert "Max iterations" in result.error


# ── Test: tool errors are fed back to the LLM ───────────────────────


class TestToolErrorFeedback:
    """When a tool fails, the error should appear in the feedback to the LLM."""

    def test_error_in_result_fed_back(self, tmp_path: Path) -> None:
        client, mock_provider = _setup_llm_client(tmp_path)
        runner = ToolRunner(project_root=tmp_path)
        loop = AgentLoop(llm=client, runner=runner, config=LoopConfig(max_iterations=3))

        # Iteration 1: try to read a file that doesn't exist
        resp1 = _make_chat_response(_json_response(
            thought="Let me read the file.",
            plan=[{"tool": "read", "args": {"path": "nonexistent.py"}}],
            done=False,
        ))
        # Iteration 2: acknowledge the error and complete
        resp2 = _make_chat_response(_json_response(
            thought="The file doesn't exist.",
            result="File was not found, task complete.",
            done=True,
        ))

        mock_provider.chat.side_effect = [resp1, resp2]

        result = loop.run(agent=_make_agent(), user_prompt="Read nonexistent.py")

        assert result.done is True
        assert result.iterations == 2

        # Verify error was in the tool results
        assert result.tool_results[0].status == "error"
        assert "not found" in result.tool_results[0].result.get("error", "").lower()

        # Verify the second LLM call received the error
        second_call = mock_provider.chat.call_args_list[1]
        user_prompt = second_call[1]["user_prompt"] if "user_prompt" in second_call[1] else second_call[0][1]
        assert "Error" in user_prompt
        assert "not found" in user_prompt.lower()

    def test_denied_tool_fed_back(self, tmp_path: Path) -> None:
        """A denied tool (HITL rejection) should also appear in feedback."""
        client, mock_provider = _setup_llm_client(tmp_path)

        # Mock tool runner to return a denied step
        runner = MagicMock()
        runner.run_plan.return_value = [
            {"step": 0, "tool": "write", "status": "denied", "error": "Human approval denied"}
        ]

        loop = AgentLoop(llm=client, runner=runner, config=LoopConfig(max_iterations=3))

        resp1 = _make_chat_response(_json_response(
            plan=[{"tool": "write", "args": {"path": "x.py", "content": "y"}}],
            done=False,
        ))
        resp2 = _make_chat_response(_json_response(
            result="Write was denied, noting that.",
            done=True,
        ))

        mock_provider.chat.side_effect = [resp1, resp2]

        result = loop.run(agent=_make_agent(), user_prompt="Write x.py")

        assert result.done is True
        assert result.tool_results[0].status == "denied"

        # The feedback should mention the denial
        second_call = mock_provider.chat.call_args_list[1]
        user_prompt = second_call[1]["user_prompt"] if "user_prompt" in second_call[1] else second_call[0][1]
        assert "denied" in user_prompt.lower()


# ── Test: empty plan completes immediately ───────────────────────────


class TestEmptyPlan:
    """An empty plan array means the agent is done."""

    def test_empty_plan_completes(self, tmp_path: Path) -> None:
        client, mock_provider = _setup_llm_client(tmp_path)
        runner = ToolRunner(project_root=tmp_path)
        loop = AgentLoop(llm=client, runner=runner, config=LoopConfig())

        mock_provider.chat.return_value = _make_chat_response(_json_response(
            thought="No tools needed.",
            plan=[],
            result="Task is complete without any tool calls.",
            done=False,  # Even with done=False, empty plan should stop
        ))

        result = loop.run(agent=_make_agent(), user_prompt="What time is it?")

        assert result.done is True
        assert result.iterations == 1
        assert len(result.tool_results) == 0
        assert "complete" in result.final_response.lower()
        assert mock_provider.chat.call_count == 1

    def test_done_true_with_plan_completes_after_execution(self, tmp_path: Path) -> None:
        """done=True with a plan still executes the plan, then stops."""
        client, mock_provider = _setup_llm_client(tmp_path)
        runner = ToolRunner(project_root=tmp_path)
        loop = AgentLoop(llm=client, runner=runner, config=LoopConfig())

        mock_provider.chat.return_value = _make_chat_response(_json_response(
            thought="One last read.",
            plan=[{"tool": "list", "args": {"path": "."}}],
            result="Listed directory.",
            done=True,
        ))

        result = loop.run(agent=_make_agent(), user_prompt="List files")

        assert result.done is True
        assert result.iterations == 1
        assert len(result.tool_results) == 1


# ── Test: LLM error handling ────────────────────────────────────────


class TestLLMErrorHandling:
    """The loop should gracefully handle LLM provider errors."""

    def test_provider_error_stops_loop(self, tmp_path: Path) -> None:
        client, mock_provider = _setup_llm_client(tmp_path)
        runner = ToolRunner(project_root=tmp_path)
        loop = AgentLoop(llm=client, runner=runner, config=LoopConfig())

        mock_provider.chat.side_effect = LLMProviderError("mock", "Service unavailable")

        result = loop.run(agent=_make_agent(), user_prompt="Do something")

        assert result.done is False
        assert "LLM error" in result.error
        # LLM failed before producing output — no completed iterations
        assert result.iterations == 0

    def test_invalid_json_treated_as_final_response(self, tmp_path: Path) -> None:
        """If LLM returns non-JSON, treat raw text as the final answer."""
        client, mock_provider = _setup_llm_client(tmp_path)
        runner = ToolRunner(project_root=tmp_path)
        loop = AgentLoop(llm=client, runner=runner, config=LoopConfig())

        mock_provider.chat.return_value = _make_chat_response(
            "I'm not sure how to respond with JSON. Here's my answer: 42."
        )

        result = loop.run(agent=_make_agent(), user_prompt="What is 2+2?")

        assert result.done is True
        assert "42" in result.final_response
        assert result.iterations == 1


# ── Test: cost tracking integration ──────────────────────────────────


class TestCostTrackingIntegration:
    """Verify the loop integrates with CostTracker."""

    def test_cost_tracker_records_usage(self, tmp_path: Path) -> None:
        from ai_company.llm.cost_tracker import CostTracker

        client, mock_provider = _setup_llm_client(tmp_path)
        runner = ToolRunner(project_root=tmp_path)
        cost_tracker = CostTracker(results_dir=str(tmp_path / "results"))
        config = LoopConfig(max_iterations=3)
        loop = AgentLoop(
            llm=client, runner=runner, cost_tracker=cost_tracker, config=config,
        )

        # 2 turns: read → done
        resp1 = _make_chat_response(
            _json_response(
                plan=[{"tool": "list", "args": {"path": "."}}],
                done=False,
            ),
            prompt_tokens=200,
            completion_tokens=80,
        )
        resp2 = _make_chat_response(
            _json_response(result="Done.", done=True),
            prompt_tokens=300,
            completion_tokens=60,
        )
        mock_provider.chat.side_effect = [resp1, resp2]

        result = loop.run(agent=_make_agent(), user_prompt="List files", task_id="task-cost-1")

        assert result.total_prompt_tokens == 500
        assert result.total_completion_tokens == 140
        assert result.total_cost_usd > 0

        # Verify the log file was written
        log_path = tmp_path / "results" / "cost_log.jsonl"
        assert log_path.exists()
        lines = log_path.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 2

    def test_daily_budget_stops_loop(self, tmp_path: Path) -> None:
        from ai_company.llm.cost_tracker import CostTracker

        client, mock_provider = _setup_llm_client(tmp_path)
        runner = ToolRunner(project_root=tmp_path)
        cost_tracker = CostTracker(
            results_dir=str(tmp_path / "results"),
            daily_budget_usd=0.0001,  # Extremely low budget
        )
        loop = AgentLoop(
            llm=client, runner=runner, cost_tracker=cost_tracker,
            config=LoopConfig(max_iterations=10),
        )

        # First call returns a tool plan, second would be the feedback
        resp1 = _make_chat_response(
            _json_response(
                plan=[{"tool": "list", "args": {"path": "."}}],
                done=False,
            ),
            prompt_tokens=10000,  # High token count to blow the budget
            completion_tokens=5000,
        )
        mock_provider.chat.return_value = resp1

        result = loop.run(agent=_make_agent(), user_prompt="Do stuff", task_id="task-budget-1")

        # Should have stopped early due to budget
        assert result.done is False
        assert "Budget" in result.error or "budget" in result.error.lower()


# ── Test: LoopConfig defaults ────────────────────────────────────────


class TestLoopConfig:
    def test_defaults(self) -> None:
        config = LoopConfig()
        assert config.max_iterations == 10
        assert config.max_tokens == 4096
        assert config.temperature == 0.3
        assert config.daily_budget_usd is None
        assert config.task_budget_usd is None

    def test_custom_config(self) -> None:
        config = LoopConfig(max_iterations=5, temperature=0.7, task_budget_usd=1.0)
        assert config.max_iterations == 5
        assert config.temperature == 0.7
        assert config.task_budget_usd == 1.0


# ── Test: LoopResult properties ──────────────────────────────────────


class TestLoopResult:
    def test_total_tokens(self) -> None:
        result = LoopResult(
            final_response="done",
            iterations=2,
            tool_results=[],
            total_prompt_tokens=500,
            total_completion_tokens=200,
            total_cost_usd=0.01,
            done=True,
        )
        assert result.total_tokens == 700

    def test_error_default_empty(self) -> None:
        result = LoopResult(
            final_response="done",
            iterations=1,
            tool_results=[],
            total_prompt_tokens=0,
            total_completion_tokens=0,
            total_cost_usd=0.0,
            done=True,
        )
        assert result.error == ""


# ── Test: parse_agent_response edge cases ────────────────────────────


class TestParseAgentResponse:
    def test_valid_json(self) -> None:
        raw = '{"thought": "hmm", "plan": [], "result": "ok", "done": true}'
        result = AgentLoop._parse_agent_response(raw)
        assert result is not None
        assert result["done"] is True

    def test_json_in_code_block(self) -> None:
        raw = '```json\n{"thought": "hmm", "plan": [], "result": "ok", "done": true}\n```'
        result = AgentLoop._parse_agent_response(raw)
        assert result is not None
        assert result["result"] == "ok"

    def test_json_embedded_in_text(self) -> None:
        raw = 'Here is my response: {"thought": "hmm", "plan": [], "result": "ok", "done": true} Hope that helps!'
        result = AgentLoop._parse_agent_response(raw)
        assert result is not None

    def test_invalid_json_returns_none(self) -> None:
        assert AgentLoop._parse_agent_response("I have no idea what to say.") is None
        assert AgentLoop._parse_agent_response("```no json here```") is None

    def test_non_dict_json_returns_none(self) -> None:
        assert AgentLoop._parse_agent_response('"just a string"') is None
        assert AgentLoop._parse_agent_response('[1, 2, 3]') is None
