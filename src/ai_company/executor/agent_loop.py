"""Multi-turn agentic loop — ReAct pattern for LLM + tool interaction.

The core loop:

  1. Send system prompt + user prompt to LLM.
  2. Parse the JSON response → ``{thought, plan, result, done}``.
  3. If ``plan`` has tool steps, execute them via ``ToolRunner``.
  4. Feed tool results back to the LLM as observations.
  5. Repeat until ``done`` is true, the plan is empty, or max iterations hit.
"""

from __future__ import annotations

import contextlib
import logging
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from ai_company.executor.ab_testing import (
    ExperimentMetrics,
    record_experiment_metrics,
    should_use_complexity_routing,
    should_use_history_summarization,
    should_use_optimized_prompts,
    should_use_tool_summarization,
)
from ai_company.executor.context import AgentContext
from ai_company.executor.history_manager import create_history_manager
from ai_company.executor.hitl_gate import HITLGate
from ai_company.executor.optimized_prompts import (
    build_optimized_system_prompt,
    build_optimized_user_prompt,
)
from ai_company.executor.prompts import (
    build_iteration_feedback,
    build_system_prompt_typed,
    build_user_prompt_typed,
)
from ai_company.executor.tool_runner import ToolRunner
from ai_company.executor.tool_summarizer import build_summarized_feedback
from ai_company.llm.client import LLMClient
from ai_company.llm.cost_tracker import CostTracker
from ai_company.llm.json_parser import parse_llm_json
from ai_company.llm.providers.base import ChatResponse, LLMProviderError, LLMResponseError
from ai_company.llm.token_counter import count_prompt_tokens, count_tokens
from ai_company.model_router import TIER_ORDER
from ai_company.orchestrator.suspend_store import SuspendedState
from ai_company.utils.logging import get_correlation_id

logger = logging.getLogger(__name__)

try:
    from ai_company.telemetry import start_span as _start_span
except ImportError:  # pragma: no cover — OTel optional

    @contextlib.contextmanager
    def _start_span(_name: str, **_kwargs: object) -> Iterator[None]:  # type: ignore
        yield


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
    # Token budget per iteration (for per-iteration enforcement)
    max_tokens_per_iteration: int = 8000
    # Estimated completion tokens for cost estimation
    estimated_completion_tokens: int = 1000
    # Use optimized prompts for specialists (token-efficient)
    use_optimized_prompts: bool = True
    # Token budget for system prompt
    system_prompt_token_budget: int = 6000
    # Conversation history management
    enable_history_summarization: bool = True
    max_full_turns: int = 3
    max_summary_tokens: int = 1000
    max_history_tokens: int = 6000
    # Tool result summarization
    enable_tool_summarization: bool = True
    max_tokens_per_tool_summary: int = 500
    # Detailed token logging for validation
    enable_detailed_token_logging: bool = False


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
    # O7: True when the loop stopped because max_iterations was exhausted
    # without the agent signalling completion (distinct from a failure).
    timed_out: bool = False

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
        *,
        non_blocking_hitl: bool = False,
    ) -> None:
        self.llm = llm
        self.runner = runner or ToolRunner()
        self.cost_tracker = cost_tracker
        self.hitl_gate = hitl_gate
        self.config = config or LoopConfig()
        # GAP-004: when True, HITL-gated steps raise HITLParked instead of
        # blocking the executor thread.
        self.non_blocking_hitl = non_blocking_hitl
        self._current_priority: str = "medium"
        self._current_task_prompt: str = ""
        self._current_agent_name: str = ""
        # Snapshot of loop state at the point of HITLParked, so the executor
        # can persist it to disk for async resume (issue #42).
        self._park_state: SuspendedState | None = None

    def run(
        self,
        agent: AgentContext,
        user_prompt: str,
        agent_name: str = "",
        task_id: str = "",
        priority: str = "medium",
        *,
        preapproved: bool = False,
        resumed_state: Any | None = None,
    ) -> LoopResult:
        """Execute the full agentic loop for a single task.

        Args:
            agent: Parsed agent context (from spec card).
            user_prompt: The task instruction / user message.
            agent_name: Override agent name (defaults to ``agent.name``).
            task_id: Task ID for cost tracking and HITL.
            priority: Task priority for model routing.
            preapproved: When True, HITL-gated steps execute directly.
            resumed_state: Optional ``SuspendedState`` from a previous park.
                When provided the loop restores conversation history and
                continues from the parked iteration instead of starting over.

        Returns:
            ``LoopResult`` with the final response, iteration count, and stats.
        """
        resolved_name = agent_name or agent.name
        self._current_priority = priority
        self._current_task_prompt = user_prompt
        self._current_agent_name = resolved_name

        # A/B Testing: Check which optimizations to enable for this task
        agent_type = agent.type.strip().lower()
        use_optimized = (
            self.config.use_optimized_prompts
            and agent_type == "specialist"
            and should_use_optimized_prompts(resolved_name, task_id)
        )
        use_history_sum = (
            self.config.enable_history_summarization
            and should_use_history_summarization(resolved_name, task_id)
        )
        use_tool_sum = self.config.enable_tool_summarization and should_use_tool_summarization(
            resolved_name, task_id
        )
        use_complexity = should_use_complexity_routing(resolved_name, task_id)

        # Use optimized prompts for specialists (token-efficient)
        if use_optimized:
            system_prompt = build_optimized_system_prompt(
                agent=agent,
                user_prompt=user_prompt,
                token_budget=self.config.system_prompt_token_budget,
            )
            initial_user = build_optimized_user_prompt(user_prompt, priority)
        else:
            system_prompt = build_system_prompt_typed(agent)
            initial_user = build_user_prompt_typed(user_prompt, priority)

        logger.info(
            "Agent loop started: agent=%s task_id=%s correlation_id=%s resumed=%s "
            "optimized_prompts=%s history_summarization=%s tool_summarization=%s complexity_routing=%s",
            resolved_name,
            task_id,
            get_correlation_id(),
            resumed_state is not None,
            use_optimized,
            use_history_sum,
            use_tool_sum,
            use_complexity,
        )

        # Initialize conversation history manager
        history_manager = None
        if use_history_sum:
            history_manager = create_history_manager(
                llm=self.llm,
                config={
                    "max_full_turns": self.config.max_full_turns,
                    "max_summary_tokens": self.config.max_summary_tokens,
                    "max_total_tokens": self.config.max_history_tokens,
                },
            )
            history_manager.add_turn(initial_user)

        # Store experiment variants for metrics recording
        self._current_experiment_variants = {
            "optimized_prompts": "treatment" if use_optimized else "control",
            "history_summarization": "treatment" if use_history_sum else "control",
            "tool_summarization": "treatment" if use_tool_sum else "control",
            "complexity_routing": "treatment" if use_complexity else "control",
        }

        # OTel span wraps the agentic loop body (T7 / issue #40).
        with _start_span(
            "agent.loop",
            attributes={
                "agent.name": resolved_name,
                "task_id": task_id,
                "priority": priority,
            },
        ):
            # Accumulators — restore from suspended state when resuming.
            all_tool_records: list[ToolCallRecord] = []
            total_prompt_tokens = 0
            total_completion_tokens = 0
            total_cost_usd = 0.0
            done = False
            final_result_text = ""
            last_error = ""
            iterations_completed = 0
            timed_out = False
            start_iteration = 1

            if resumed_state is not None:
                # Restore history manager state if available
                if history_manager and resumed_state.conversation_history:
                    # Replay history into manager
                    for entry in resumed_state.conversation_history:
                        if entry.startswith("PRIORITY:") or entry.startswith("TASK:"):
                            history_manager.add_turn(entry)
                        else:
                            history_manager.add_tool_feedback(entry)

                iterations_completed = resumed_state.iterations_completed
                start_iteration = iterations_completed + 1
                all_tool_records = [
                    ToolCallRecord(**r) if isinstance(r, dict) else r
                    for r in resumed_state.tool_results
                ]
                total_prompt_tokens = resumed_state.total_prompt_tokens
                total_completion_tokens = resumed_state.total_completion_tokens
                total_cost_usd = resumed_state.total_cost_usd
                logger.info(
                    "Restored suspended state: %d iterations, %d history entries",
                    iterations_completed,
                    len(resumed_state.conversation_history),
                )

            # Track conversation history for non-manager case
            conversation_history_list: list[str] = [initial_user]

            for iteration in range(start_iteration, self.config.max_iterations + 1):
                # ── Get conversation context ────────────────────────────────
                if history_manager:
                    full_user_prompt = history_manager.get_context()
                else:
                    full_user_prompt = "\n\n".join(conversation_history_list)

                # ── Budget check (per-iteration enforcement) ────────────────
                if self.cost_tracker and task_id:
                    # Estimate prompt tokens for this iteration
                    estimated_prompt_tokens = count_prompt_tokens(system_prompt, full_user_prompt)
                    # Get the model that will be used (from router, with budget degradation)
                    route = self.llm.router.resolve(
                        agent_name=self._current_agent_name,
                        priority=self._current_priority,
                        task_prompt=self._current_task_prompt,
                        cost_tracker=self.cost_tracker,
                    )
                    estimated_cost = self.cost_tracker.estimate_call_cost(
                        model=route.model,
                        prompt_tokens=estimated_prompt_tokens,
                        estimated_completion_tokens=self.config.estimated_completion_tokens,
                    )
                    allowed, reason = self.cost_tracker.check_budget(task_id, estimated_cost)
                    if not allowed:
                        last_error = f"Budget exceeded (iteration {iteration}): {reason}"
                        logger.warning("Budget check failed at iteration %d: %s", iteration, reason)
                        break

                # Check token budget per iteration
                if self.config.max_tokens_per_iteration:
                    estimated_prompt_tokens = count_prompt_tokens(system_prompt, full_user_prompt)
                    if estimated_prompt_tokens > self.config.max_tokens_per_iteration:
                        last_error = f"Token budget exceeded at iteration {iteration}: {estimated_prompt_tokens} > {self.config.max_tokens_per_iteration}"
                        logger.warning(
                            "Token budget check failed at iteration %d: %d tokens",
                            iteration,
                            estimated_prompt_tokens,
                        )
                        break

                # ── Budget check (legacy, between iterations) ────────────────
                if self.cost_tracker and task_id:
                    allowed, reason = self.cost_tracker.check_budget(task_id)
                    if not allowed:
                        last_error = f"Budget exceeded: {reason}"
                        break

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

                # ── Detailed token logging for validation ─────────────────────────────
                if self.config.enable_detailed_token_logging:
                    system_prompt_tokens = count_tokens(system_prompt)
                    history_tokens = count_tokens(full_user_prompt) - system_prompt_tokens

                    logger.debug(
                        "Token breakdown iter=%d: system=%d history=%d total_prompt=%d estimated=%d",
                        iteration,
                        system_prompt_tokens,
                        max(0, history_tokens),
                        prompt_tok,
                        estimated_prompt_tokens,
                    )

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
                risk_level = (
                    priority if priority in ("low", "medium", "high", "critical") else "medium"
                )

                # Snapshot loop state for suspension (issue #42): if
                # runner.run_plan() raises HITLParked the executor needs
                # this state to persist it to disk for async resume.
                if history_manager:
                    suspended_history = [history_manager.get_context()]
                else:
                    suspended_history = list(conversation_history_list)
                self._park_state = SuspendedState(
                    task_id=task_id,
                    conversation_history=suspended_history,
                    iterations_completed=iterations_completed,
                    tool_results=[{k: v for k, v in r.__dict__.items()} for r in all_tool_records],
                    total_prompt_tokens=total_prompt_tokens,
                    total_completion_tokens=total_completion_tokens,
                    total_cost_usd=total_cost_usd,
                    agent_name=resolved_name,
                    priority=priority,
                )

                step_results = self.runner.run_plan(
                    plan=plan,
                    hitl_gate=self.hitl_gate,
                    task_id=task_id,
                    agent_id=resolved_name,
                    seniority=seniority,
                    risk_level=risk_level,
                    non_blocking=self.non_blocking_hitl,
                    preapproved=preapproved,
                )

                for i, step_result in enumerate(step_results):
                    # GAP-019: belt-and-braces — never crash the loop if a step
                    # result is not a dict (e.g. a plan that degenerated into
                    # free text mid-run).  Coerce it into an error record so the
                    # model sees feedback and can self-correct.
                    if not isinstance(step_result, dict):
                        step_result = {
                            "step": i,
                            "tool": "unknown",
                            "status": "error",
                            "error": (
                                f"Malformed tool result: expected a dict, "
                                f"got {type(step_result).__name__}"
                            ),
                        }
                    record = ToolCallRecord(
                        step=step_result.get("step", i),
                        tool=step_result.get("tool", "unknown"),
                        status=step_result.get("status", "unknown"),
                        result=step_result,
                        iteration=iteration,
                    )
                    all_tool_records.append(record)

                # ── Feed results back to LLM ──────────────────────────
                if use_tool_sum:
                    feedback = build_summarized_feedback(
                        step_results=step_results,
                        iteration=iteration,
                        max_iterations=self.config.max_iterations,
                        max_tokens_per_tool=self.config.max_tokens_per_tool_summary,
                        llm=self.llm,
                    )
                else:
                    feedback = build_iteration_feedback(
                        step_results=step_results,
                        iteration=iteration,
                        max_iterations=self.config.max_iterations,
                    )
                if history_manager:
                    history_manager.add_tool_feedback(feedback)
                else:
                    conversation_history_list.append(feedback)

                # Check if agent explicitly signaled done
                if is_done:
                    final_result_text = result_text or "Task completed."
                    done = True
                    break

            # ── Handle max-iterations exhaustion ──────────────────────
            if not done and not last_error:
                # O7: mark this as a timeout (not a generic failure) so the
                # executor can persist TaskStatus.TIMEOUT and operators can
                # distinguish a hit iteration cap from a hard error.
                timed_out = True
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

        # Record experiment metrics for A/B testing
        if task_id and hasattr(self, "_current_experiment_variants"):
            try:
                metrics = ExperimentMetrics(
                    experiment_name="optimized_prompts",
                    variant=self._current_experiment_variants.get("optimized_prompts", "control"),
                    task_id=task_id,
                    agent_name=resolved_name,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    prompt_tokens=total_prompt_tokens,
                    completion_tokens=total_completion_tokens,
                    total_tokens=total_prompt_tokens + total_completion_tokens,
                    cost_usd=total_cost_usd,
                    iterations=iterations_completed,
                    success=done and not last_error,
                    error=last_error,
                    task_completed=done,
                )
                record_experiment_metrics(metrics)
            except (OSError, ValueError) as e:
                logger.debug("Failed to record experiment metrics: %s", e)

        return LoopResult(
            final_response=final_result_text,
            iterations=iterations_completed,
            tool_results=all_tool_records,
            total_prompt_tokens=total_prompt_tokens,
            total_completion_tokens=total_completion_tokens,
            total_cost_usd=round(total_cost_usd, 8),
            done=done,
            error=last_error,
            timed_out=timed_out,
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

        Uses complexity-aware routing via ``task_prompt`` and implements
        quality-based fallback: if all providers in the current tier fail,
        promotes to the next higher tier (fast → standard → premium).
        """
        # Get complexity-aware route (pass cost_tracker for budget degradation)
        route = self.llm.router.resolve_with_complexity(
            agent_name=self._current_agent_name or None,
            priority=self._current_priority,
            task_prompt=self._current_task_prompt,
            cost_tracker=self.cost_tracker,
        )

        # Build fallback chain: current tier providers + higher tiers
        fallback_routes = self.llm.router.resolve_with_fallback(
            agent_name=self._current_agent_name or None,
            priority=self._current_priority,
            task_prompt=self._current_task_prompt,
            cost_tracker=self.cost_tracker,
        )
        provider_chain: list[tuple[str, str]] = []

        # Use complexity-adjusted tier as primary
        primary_tier = route.tier
        for fb_route in fallback_routes:
            # Start from the complexity-adjusted tier
            if fb_route.tier == primary_tier or TIER_ORDER.index(fb_route.tier) >= TIER_ORDER.index(
                primary_tier
            ):
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
            breaker = self.llm.get_breaker(provider_id)
            if breaker and not breaker.is_available:
                continue

            use_model = model or resolved_model

            try:
                with _start_span(
                    "llm.execute",
                    attributes={
                        "provider": provider_id,
                        "model": use_model,
                        "task_id": self._current_task_prompt[:32]
                        if self._current_task_prompt
                        else "",
                    },
                ):
                    response = provider.chat(
                        system_prompt=system_prompt,
                        user_prompt=user_prompt,
                        model=use_model,
                    )
                if breaker:
                    breaker.record_success()
                return response
            except LLMProviderError as exc:
                if breaker:
                    breaker.record_failure(exc.category.value)
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
