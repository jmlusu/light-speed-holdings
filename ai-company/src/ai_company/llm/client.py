"""Unified LLM client — routes tasks to the right provider with retry logic."""

from __future__ import annotations

import logging
from collections.abc import Generator
from typing import Any

from ai_company.llm.circuit_breaker import CircuitBreaker
from ai_company.llm.cost_tracker import CostTracker, _cost_per_token
from ai_company.llm.json_parser import parse_llm_json
from ai_company.llm.providers.base import (
    LLMProvider,
    LLMProviderError,
    LLMResponseError,
    StreamChunk,
)
from ai_company.llm.providers.openai_compatible import OpenAICompatibleProvider
from ai_company.llm.providers.ollama import OllamaProvider
from ai_company.model_router import ModelRouter
from ai_company.utils.logging import get_correlation_id

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


_MAX_RETRIES = 5


class LLMClient:
    """Unified client that resolves provider via ModelRouter and executes tasks.

    Retry policy: up to 5 attempts if the LLM response is not valid JSON.
    Falls back through the tier's provider chain on provider errors.

    Args:
        config_path: Path to the models routing config.
        registry_path: Path to the agent registry for per-agent routing.
        cost_tracker: Optional cost tracker for recording token usage.
    """

    def __init__(
        self,
        config_path: str = "company/models.yaml",
        registry_path: str = "company/agent-registry.json",
        cost_tracker: CostTracker | None = None,
    ) -> None:
        self.router = ModelRouter(config_path=config_path, registry_path=registry_path)
        self._providers: dict[str, LLMProvider] = {}
        self._circuit_breakers: dict[str, CircuitBreaker] = {}
        self._cost_tracker = cost_tracker
        self._init_providers()

    def _init_providers(self) -> None:
        """Create provider instances from models.yaml config."""
        for pcfg in self.router.list_providers():
            self._circuit_breakers[pcfg.id] = CircuitBreaker()

            if pcfg.id == "ollama":
                self._providers[pcfg.id] = OllamaProvider(
                    name=pcfg.id,
                    api_base=pcfg.api_base or "http://localhost:11434",
                    default_model=pcfg.default_model,
                )
            else:
                # Determine auth style based on backend or provider id
                auth_style = "x-api-key" if pcfg.id == "anthropic" else "bearer"
                api_key_env = f"{pcfg.id.upper()}_API_KEY"
                self._providers[pcfg.id] = OpenAICompatibleProvider(
                    name=pcfg.id,
                    api_base=pcfg.api_base,
                    default_model=pcfg.default_model,
                    api_key_env=api_key_env,
                    auth_style=auth_style,
                )

    def execute_task(
        self,
        agent_name: str,
        task_instruction: str,
        priority: str = "medium",
        context: str | None = None,
        system_prompt: str = "",
        max_retries: int = _MAX_RETRIES,
        task_id: str = "",
    ) -> dict[str, Any]:
        """Execute a task by calling the LLM and parsing the structured response.

        Returns parsed JSON dict with keys: plan, result, artifacts.
        Retries up to max_retries times if response is not valid JSON.
        Falls back to next provider in tier on provider errors.

        Args:
            agent_name: Name of the agent executing the task.
            task_instruction: The task instruction / user message.
            priority: Task priority for model routing.
            context: Optional context override for routing.
            system_prompt: System-level instructions for the model.
            max_retries: Maximum number of retry attempts.
            task_id: Task ID for cost tracking. If empty, cost is not recorded.

        Raises:
            LLMResponseError: If all retries exhausted without valid JSON.
            LLMProviderError: If no provider is available.
        """
        route = self.router.resolve(
            agent_name=agent_name, priority=priority, context=context,
            task_prompt=task_instruction,
        )

        logger.debug(
            "LLM execute_task: agent=%s provider=%s model=%s correlation_id=%s",
            agent_name,
            route.provider,
            route.model,
            get_correlation_id(),
        )

        # Get the tier's provider chain for fallback
        tier = self.router.get_tier(route.tier)
        provider_chain: list[tuple[str, str]] = []
        if tier and tier.providers:
            provider_chain = [(p.provider, p.model) for p in tier.providers]
        else:
            provider_chain = [(route.provider, route.model)]

        # PRE-11: Pre-flight budget check before calling the LLM
        if self._cost_tracker and task_id:
            estimated_cost = estimate_call_cost(
                system_prompt, task_instruction, model=route.model,
            )
            allowed, reason = self._cost_tracker.check_budget(
                task_id, proposed_cost=estimated_cost,
            )
            if not allowed:
                raise LLMProviderError(
                    provider="budget",
                    message=f"budget check failed for task {task_id}: {reason}",
                )

        last_error: str = ""
        last_raw: str = ""

        for attempt in range(max_retries):
            provider_idx = attempt % len(provider_chain)
            provider_id, model = provider_chain[provider_idx]

            provider = self._providers.get(provider_id)
            breaker = self._circuit_breakers.get(provider_id)
            if not provider or not provider.is_available():
                continue
            if breaker and not breaker.is_available:
                continue

            try:
                response = provider.chat(
                    system_prompt=system_prompt,
                    user_prompt=task_instruction,
                    model=model,
                )
                if breaker:
                    breaker.record_success()
                parsed = self._parse_response(response.content)
                if parsed is not None:
                    self._record_usage(response, agent_name, task_id, attempt + 1)
                    return parsed
                last_raw = response.content
                last_error = f"Attempt {attempt + 1}: Invalid JSON from {provider_id}/{model}"
            except LLMProviderError as exc:
                if breaker:
                    breaker.record_failure()
                last_error = f"Attempt {attempt + 1}: {exc}"

        raise LLMResponseError(
            f"Failed to get valid JSON after {max_retries} attempts. Last error: {last_error}",
            attempts=max_retries,
            last_raw=last_raw,
        )

    def execute_task_stream(
        self,
        agent_name: str,
        task_instruction: str,
        priority: str = "medium",
        context: str | None = None,
        system_prompt: str = "",
        max_retries: int = _MAX_RETRIES,
    ) -> Generator[StreamChunk, None, None]:
        """Execute a task via streaming, yielding chunks as they arrive.

        Collects the full response text and attempts JSON parsing once the
        stream finishes. Yields all intermediate chunks for real-time output.

        Raises:
            LLMResponseError: If all retries exhausted without valid JSON.
            LLMProviderError: If no provider is available.
        """
        route = self.router.resolve(
            agent_name=agent_name, priority=priority, context=context,
            task_prompt=task_instruction,
        )

        tier = self.router.get_tier(route.tier)
        provider_chain: list[tuple[str, str]] = []
        if tier and tier.providers:
            provider_chain = [(p.provider, p.model) for p in tier.providers]
        else:
            provider_chain = [(route.provider, route.model)]

        last_error: str = ""
        last_raw: str = ""

        for attempt in range(max_retries):
            provider_idx = attempt % len(provider_chain)
            provider_id, model = provider_chain[provider_idx]

            provider = self._providers.get(provider_id)
            breaker = self._circuit_breakers.get(provider_id)
            if not provider or not provider.is_available():
                continue
            if breaker and not breaker.is_available:
                continue

            full_text = ""
            try:
                for chunk in provider.chat_stream(
                    system_prompt=system_prompt,
                    user_prompt=task_instruction,
                    model=model,
                ):
                    full_text += chunk.delta
                    yield chunk

                if breaker:
                    breaker.record_success()

                parsed = self._parse_response(full_text)
                if parsed is not None:
                    return
                last_raw = full_text
                last_error = (
                    f"Attempt {attempt + 1}: Invalid JSON from {provider_id}/{model}"
                )
            except LLMProviderError as exc:
                if breaker:
                    breaker.record_failure()
                last_error = f"Attempt {attempt + 1}: {exc}"

        raise LLMResponseError(
            f"Failed to get valid JSON after {max_retries} attempts. Last error: {last_error}",
            attempts=max_retries,
            last_raw=last_raw,
        )

    def _record_usage(
        self,
        response: Any,
        agent_name: str,
        task_id: str,
        iteration: int,
    ) -> None:
        """Record token usage to JSONL (CostTracker) and SQLite (CostAnalytics).

        The existing JSONL logging via CostTracker is preserved as-is.
        When the SQLite database singleton is available, usage is also
        written to the ``cost_records`` table for dashboard analytics.

        Args:
            response: The ChatResponse from the provider.
            agent_name: Name of the agent that made the call.
            task_id: Task ID for cost tracking.
            iteration: Current iteration number.
        """
        if not task_id:
            return

        cost_usd = 0.0

        # ── 1. JSONL logging (existing CostTracker) ────────────────
        if self._cost_tracker is not None:
            try:
                record = self._cost_tracker.record_usage(
                    model=response.model,
                    provider=response.provider,
                    agent_name=agent_name,
                    task_id=task_id,
                    prompt_tokens=response.prompt_tokens,
                    completion_tokens=response.completion_tokens,
                    iteration=iteration,
                )
                cost_usd = record.cost_usd
            except Exception:
                logger.debug(
                    "JSONL cost tracking failed for task %s", task_id, exc_info=True,
                )

        # Compute cost if the tracker didn't (or wasn't configured)
        if cost_usd == 0.0:
            cost_usd = round(
                response.prompt_tokens * _cost_per_token(response.model, "input")
                + response.completion_tokens * _cost_per_token(response.model, "output"),
                8,
            )

        # ── 2. SQLite recording (CostAnalytics) ───────────────────
        try:
            from ai_company.data import CostAnalytics, get_database

            db = get_database()
            if db is not None:
                analytics = CostAnalytics(db)
                analytics.record_usage(
                    model=response.model,
                    provider=response.provider,
                    agent_name=agent_name,
                    task_id=task_id,
                    prompt_tokens=response.prompt_tokens,
                    completion_tokens=response.completion_tokens,
                    cost_usd=cost_usd,
                    iteration=iteration,
                )
        except Exception:
            logger.debug(
                "SQLite cost tracking failed for task %s", task_id, exc_info=True,
            )

    def _parse_response(self, content: str) -> dict[str, Any] | None:
        """Try to parse the LLM response as JSON."""
        return parse_llm_json(content)

    def get_provider(self, provider_id: str) -> LLMProvider | None:
        return self._providers.get(provider_id)

    def list_available_providers(self) -> list[str]:
        return [pid for pid, p in self._providers.items() if p.is_available()]


# ---------------------------------------------------------------------------
# Token estimation helpers
# ---------------------------------------------------------------------------


def _estimate_tokens(text: str) -> int:
    """Rough heuristic: ~4 characters per token for English text.

    This is intentionally simple — it does not require a real tokenizer
    and is used only for pre-flight cost estimates and budget checks.
    """
    if not text:
        return 1  # Minimum 1 token even for empty input
    return max(1, len(text) // 4)


def estimate_call_cost(
    system_prompt: str,
    user_prompt: str,
    model: str | None = None,
) -> float:
    """Estimate the cost in USD of a hypothetical LLM call.

    Uses a simple character-count heuristic to estimate token counts,
    then looks up per-token pricing in :data:`MODEL_COSTS`.

    Args:
        system_prompt: The system-level prompt.
        user_prompt: The user-level prompt / task instruction.
        model: Model identifier.  Falls back to ``_default`` when unknown.

    Returns:
        Estimated cost in USD (float).
    """
    prompt_tokens = _estimate_tokens(system_prompt) + _estimate_tokens(user_prompt)
    resolved_model = model or "_default"
    input_cost = prompt_tokens * _cost_per_token(resolved_model, "input")
    # Assume ~25% completion ratio for estimation purposes
    completion_tokens = max(1, prompt_tokens // 4)
    output_cost = completion_tokens * _cost_per_token(resolved_model, "output")
    return round(input_cost + output_cost, 8)
