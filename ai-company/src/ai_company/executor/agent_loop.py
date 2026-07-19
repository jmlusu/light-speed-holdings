"""Multi-turn agentic loop — ReAct pattern for LLM + tool interaction.

The core loop:

  1. Send system prompt + user prompt to LLM.
  2. Parse the JSON response → ``{thought, plan, result, done}``.
  3. If ``plan`` has tool steps, execute them via ``ToolRunner``.
  4. Feed tool results back to the LLM as observations.
  5. Repeat until ``done`` is true, the plan is empty, or max iterations hit.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ai_company.executor.context import AgentContext
from ai_company.executor.hitl_gate import HITLGate
from ai_company.executor.prompts import (
    build_iteration_feedback,
    build_system_prompt_typed,
    build_user_prompt_typed,
)
from ai_company.executor.tool_runner import ToolRunner
from ai_company.llm.client import LLMClient
from ai_company.llm.cost_tracker import CostTracker
from ai_company.llm.json_parser import parse_llm_json
from ai_company.llm.providers.base import ChatResponse, LLMProviderError, LLMResponseError


# ---------------------------------------------------------------------------
# Configuration & result dataclasses
# ---------------------------------------------------------------------------


@dataclass
class LoopConfig:
    """Configuration for the agentic loop."""

    max_iterations: int = 10
    max_tokens: int = 4096
    temperature: float = 0.3
    # Budget guards — None means unlimited
    daily_budget_usd: float | None = None
    task_budget_usd: float | None = None


@dataclass
class ToolCallRecord:
    """Record of a single tool invocation within the loop."""

    step: int
    tool: str
    status: str
    result: dict[str, Any]
    iteration: int


@dataclass
class LoopResult:
    """Outcome of running the agentic loop to completion."""

    final_response: str
    iterations: int
    tool_results: list[ToolCallRecord]
    total_prompt_tokens: int
    total_completion_tokens: int
    total_cost_usd: float
    done: bool
    error: str = ""

    @property
    def total_tokens(self) -> int:
        return self.total_prompt_tokens + self.total_completion_tokens


# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------


class AgentLoop:
    """Multi-turn agentic loop implementing the ReAct pattern.

    Takes an ``AgentContext`` (parsed agent spec), builds typed prompts,
    and runs iterative LLM ↔ tool interaction until the agent signals
    completion or a stopping condition is met.

    Args:
        llm: The unified LLM client.
        runner: Tool runner for executing tool plans.
        cost_tracker: Optional cost tracker for recording usage.
        hitl_gate: Human-in-the-loop gate for approval tiers.
        config: Loop configuration (max iterations, budgets, etc.).
    """

    def __init__(
        self,
        llm: LLMClient,
        runner: ToolRunner | None = None,
        cost_tracker: CostTracker | None = None,
        hitl_gate: HITLGate | None = None,
        config: LoopConfig | None = None,
    ) -> None:
        self.llm = llm
        self.runner = runner or ToolRunner()
        self.cost_tracker = cost_tracker
        self.hitl_gate = hitl_gate
        self.config = config or LoopConfig()
        self._current_priority: str = "medium"
        self._current_task_prompt: str = ""

    def run(
        self,
        agent: AgentContext,
        user_prompt: str,
        agent_name: str = "",
        task_id: str = "",
        priority: str = "medium",
    ) -> LoopResult:
        """Execute the full agentic loop for a single task.

        Args:
            agent: Parsed agent context (from spec card).
            user_prompt: The task instruction / user message.
            agent_name: Override agent name (defaults to ``agent.name``).
            task_id: Task ID for cost tracking and HITL.
            priority: Task priority for model routing.

        Returns:
            ``LoopResult`` with the final response, iteration count, and stats.
        """
        resolved_name = agent_name or agent.name
        self._current_priority = priority
        self._current_task_prompt = user_prompt
        system_prompt = build_system_prompt_typed(agent)
        initial_user = build_user_prompt_typed(user_prompt, priority)

        # Accumulators
        all_tool_records: list[ToolCallRecord] = []
        total_prompt_tokens = 0
        total_completion_tokens = 0
        total_cost_usd = 0.0
        conversation_history: list[str] = [initial_user]
        done = False
        final_result_text = ""
        last_error = ""
        iterations_completed = 0

        for iteration in range(1, self.config.max_iterations + 1):
            # ── Budget check ──────────────────────────────────────
            if self.cost_tracker and task_id:
                allowed, reason = self.cost_tracker.check_budget(task_id)
                if not allowed:
                    last_error = f"Budget exceeded: {reason}"
                    break

            # ── Assemble the full user prompt with history ────────
            full_user_prompt = "\n\n".join(conversation_history)

            # ── Call LLM ──────────────────────────────────────────
            try:
                response = self._call_llm(
                    system_prompt=system_prompt,
                    user_prompt=full_user_prompt,
                    model=None,  # Let router decide
                )
            except (LLMProviderError, LLMResponseError) as exc:
                last_error = f"LLM error at iteration {iteration}: {exc}"
                break

            # ── Track usage ───────────────────────────────────────
            prompt_tok = response.usage.get("prompt_tokens", 0)
            comp_tok = response.usage.get("completion_tokens", 0)
            total_prompt_tokens += prompt_tok
            total_completion_tokens += comp_tok

            if self.cost_tracker and task_id:
                rec = self.cost_tracker.record_usage(
                    model=response.model,
                    provider=response.provider,
                    agent_name=resolved_name,
                    task_id=task_id,
                    prompt_tokens=prompt_tok,
                    completion_tokens=comp_tok,
                    iteration=iteration,
                )
                total_cost_usd += rec.cost_usd

            iterations_completed += 1

            # ── Parse the response ────────────────────────────────
            parsed = self._parse_agent_response(response.content)

            if parsed is None:
                # LLM didn't return valid JSON — treat the raw text as final answer
                final_result_text = response.content.strip()
                done = True
                break

            plan = parsed.get("plan", [])
            result_text = parsed.get("result", "")
            is_done = parsed.get("done", False)

            # ── No tools in plan → complete ───────────────────────
            if not plan:
                final_result_text = result_text or response.content.strip()
                done = True
                break

            # ── Execute tools ─────────────────────────────────────
            seniority = _derive_seniority(agent.type)
            risk_level = priority if priority in ("low", "medium", "high", "critical") else "medium"

            step_results = self.runner.run_plan(
                plan=plan,
                hitl_gate=self.hitl_gate,
                task_id=task_id,
                agent_id=resolved_name,
                seniority=seniority,
                risk_level=risk_level,
            )

            for i, step_result in enumerate(step_results):
                record = ToolCallRecord(
                    step=step_result.get("step", i),
                    tool=step_result.get("tool", "unknown"),
                    status=step_result.get("status", "unknown"),
                    result=step_result,
                    iteration=iteration,
                )
                all_tool_records.append(record)

            # ── Feed results back to LLM ──────────────────────────
            feedback = build_iteration_feedback(
                step_results=step_results,
                iteration=iteration,
                max_iterations=self.config.max_iterations,
            )
            conversation_history.append(feedback)

            # Check if agent explicitly signaled done
            if is_done:
                final_result_text = result_text or "Task completed."
                done = True
                break

        # ── Handle max-iterations exhaustion ──────────────────────
        if not done and not last_error:
            last_error = (
                f"Max iterations ({self.config.max_iterations}) reached "
                "without agent signaling completion."
            )
            # Use whatever result text we have from the last iteration
            if not final_result_text:
                final_result_text = (
                    f"Loop terminated after {self.config.max_iterations} iterations. "
                    f"Last LLM result: {parsed.get('result', '') if parsed else 'N/A'}"
                )

        return LoopResult(
            final_response=final_result_text,
            iterations=iterations_completed,
            tool_results=all_tool_records,
            total_prompt_tokens=total_prompt_tokens,
            total_completion_tokens=total_completion_tokens,
            total_cost_usd=round(total_cost_usd, 8),
            done=done,
            error=last_error,
        )

    # ── Internal helpers ───────────────────────────────────────────

    def _call_llm(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
    ) -> ChatResponse:
        """Make a raw LLM call via the unified client's provider chain.

        Bypasses ``LLMClient.execute_task()`` (which does single-pass
        JSON parsing) and calls the provider's ``chat()`` directly,
        returning the raw ``ChatResponse`` with usage stats.

        Uses domain-aware routing via ``task_prompt`` and implements
        quality-based fallback: if all providers in the current tier fail,
        promotes to the next higher tier (fast → standard → premium).
        """
        # Resolve which provider/model to use via the router (with domain detection)
        self.llm.router.resolve(
            priority=self._current_priority,
            task_prompt=self._current_task_prompt,
        )

        # Build fallback chain: current tier providers + higher tiers
        fallback_routes = self.llm.router.resolve_with_fallback(
            priority=self._current_priority,
            task_prompt=self._current_task_prompt,
        )
        provider_chain: list[tuple[str, str]] = []
        for fb_route in fallback_routes:
            tier = self.llm.router.get_tier(fb_route.tier)
            if tier and tier.providers:
                for p in tier.providers:
                    provider_chain.append((p.provider, p.model))
            else:
                provider_chain.append((fb_route.provider, fb_route.model))

        last_error: Exception | None = None

        for provider_id, resolved_model in provider_chain:
            provider = self.llm.get_provider(provider_id)
            if not provider or not provider.is_available():
                continue

            use_model = model or resolved_model

            try:
                response = provider.chat(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    model=use_model,
                )
                return response
            except LLMProviderError as exc:
                last_error = exc
                continue

        raise LLMProviderError(
            "agent_loop",
            f"No provider available. Last error: {last_error}",
        )

    @staticmethod
    def _parse_agent_response(content: str) -> dict[str, Any] | None:
        """Parse the LLM response as a ReAct-style JSON dict."""
        return parse_llm_json(content)


def _derive_seniority(agent_type: str) -> str:
    """Map an agent type string to a seniority level for tier classification.

    Board → executive, Executive → executive, Specialist → mid.
    """
    t = agent_type.lower()
    if t in ("board", "executive"):
        return "executive"
    if t in ("lead", "senior specialist"):
        return "lead"
    return "mid"
