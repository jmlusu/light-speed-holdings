"""Unified LLM client — routes tasks to the right provider with retry logic."""

from __future__ import annotations

import logging
from collections.abc import Generator
from typing import Any

from dotenv import load_dotenv

from ai_company.dashboard.monitoring import inc_metric, record_llm_cost
from ai_company.llm.circuit_breaker import CircuitBreaker
from ai_company.llm.cost_tracker import CostTracker, _cost_per_token
from ai_company.llm.json_parser import parse_llm_json
from ai_company.llm.oauth2 import OAuth2Config, OAuth2TokenManager
from ai_company.llm.providers.base import (
    ChatResponse,
    LLMProvider,
    LLMProviderError,
    LLMResponseError,
    StreamChunk,
)
from ai_company.llm.providers.ollama import OllamaProvider
from ai_company.llm.providers.openai_compatible import OpenAICompatibleProvider
from ai_company.llm.token_bucket import TokenBucket
from ai_company.llm.token_counter import (
    TokenUsage,
    count_prompt_tokens,
    count_tokens,
    join_prompt,
    usage_from_response,
)
from ai_company.model_router import ModelRouter, ProviderConfig
from ai_company.utils.logging import get_correlation_id

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
        limiter_timeout: Seconds to wait for a token-bucket slot before an
            attempt is skipped as rate-limited. Providers without a
            ``rate_limit`` block in models.yaml are not limited.
    """

    # Class-level default so instances built via ``__new__`` (streaming tests)
    # remain safe: limiter lookups degrade to "not limited".
    _limiters: dict[str, TokenBucket] = {}

    def __init__(
        self,
        config_path: str = "company/models.yaml",
        registry_path: str = "company/agent-registry.json",
        cost_tracker: CostTracker | None = None,
        limiter_timeout: float = 30.0,
    ) -> None:
        self.router = ModelRouter(config_path=config_path, registry_path=registry_path)
        self._providers: dict[str, LLMProvider] = {}
        self._circuit_breakers: dict[str, CircuitBreaker] = {}
        self._limiters: dict[str, TokenBucket] = {}
        self._cost_tracker = cost_tracker
        self._limiter_timeout = limiter_timeout
        self._init_providers()

    def _init_providers(self) -> None:
        """Create provider instances from models.yaml config."""
        for pcfg in self.router.list_providers():
            self._circuit_breakers[pcfg.id] = CircuitBreaker()

            rl = getattr(pcfg, "rate_limit", None) or {}
            if rl.get("rate") is not None and rl.get("capacity") is not None:
                self._limiters[pcfg.id] = TokenBucket(
                    rate=float(rl["rate"]),
                    capacity=float(rl["capacity"]),
                )

            oauth2 = self._build_oauth2_manager(pcfg)

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
                    oauth2=oauth2,
                )

    @staticmethod
    def _build_oauth2_manager(
        pcfg: ProviderConfig,
    ) -> OAuth2TokenManager | None:
        """Build an OAuth2 token manager from a provider config, if configured.

        Returns None when the provider has no ``oauth2`` block (API-key auth
        is used instead). Missing required fields (``token_url``) are treated
        as an unconfigured provider rather than a crash.
        """
        oauth2_cfg = getattr(pcfg, "oauth2", None) or {}
        token_url = oauth2_cfg.get("token_url")
        if not token_url:
            return None
        try:
            config = OAuth2Config(
                token_url=token_url,
                client_id=oauth2_cfg.get("client_id", ""),
                client_secret=oauth2_cfg.get("client_secret", ""),
                client_id_env=oauth2_cfg.get("client_id_env", ""),
                client_secret_env=oauth2_cfg.get("client_secret_env", ""),
                scope=oauth2_cfg.get("scope"),
                audience=oauth2_cfg.get("audience"),
                cache_ttl_seconds=oauth2_cfg.get("cache_ttl_seconds", 3600),
            )
            return OAuth2TokenManager.from_config(config)
        except (TypeError, ValueError):
            logger.warning("Invalid OAuth2 config for provider %s", pcfg.id)
            return None

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
            agent_name=agent_name,
            priority=priority,
            context=context,
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

        last_error: str = ""
        last_raw: str = ""

        # Assemble the exact prompt text once so heuristic fallback counts
        # match what was actually sent to the provider.
        prompt_text = join_prompt(system_prompt, task_instruction)

        for attempt in range(max_retries):
            provider_idx = attempt % len(provider_chain)
            provider_id, model = provider_chain[provider_idx]

            provider = self._providers.get(provider_id)
            breaker = self._circuit_breakers.get(provider_id)
            if not provider or not provider.is_available():
                continue
            if breaker and not breaker.is_available:
                continue
            limiter = self._limiters.get(provider_id)
            if limiter and not limiter.acquire(timeout=self._limiter_timeout):
                last_error = f"Attempt {attempt + 1}: {provider_id} rate limit (limiter timeout)"
                logger.debug(
                    "LLM attempt skipped",
                    extra={
                        "attempt": attempt + 1,
                        "model": model,
                        "error": last_error,
                    },
                )
                inc_metric("llm_errors_total")
                continue

            # Count prompt tokens before the call (heuristic estimate).
            logger.debug(
                "LLM prompt token estimate: agent=%s model=%s prompt_tokens=%d",
                agent_name,
                model,
                count_prompt_tokens(system_prompt, task_instruction, model),
            )

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
                    usage = usage_from_response(
                        response,
                        prompt_text,
                        response.model or model,
                    )
                    self._record_usage(response, agent_name, task_id, attempt + 1, usage)
                    inc_metric("llm_requests_total")
                    return parsed
                last_raw = response.content
                last_error = f"Attempt {attempt + 1}: Invalid JSON from {provider_id}/{model}"
                logger.debug(
                    "LLM attempt failed",
                    extra={
                        "attempt": attempt + 1,
                        "model": model,
                        "error": last_error,
                    },
                )
            except LLMProviderError as exc:
                if breaker:
                    breaker.record_failure(exc.category.value)
                last_error = f"Attempt {attempt + 1}: {exc}"
                logger.debug(
                    "LLM attempt failed",
                    extra={
                        "attempt": attempt + 1,
                        "model": model,
                        "error": str(exc),
                    },
                )
                inc_metric("llm_errors_total")

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
        task_id: str = "",
    ) -> Generator[StreamChunk, None, None]:
        """Execute a task via streaming, yielding chunks as they arrive.

        Collects the full response text and attempts JSON parsing once the
        stream finishes. Yields all intermediate chunks for real-time output.

        When ``task_id`` is provided, token usage is recorded heuristically
        (streaming responses do not surface aggregated usage metadata
        reliably), matching the counts used elsewhere in cost tracking.

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
            agent_name=agent_name,
            priority=priority,
            context=context,
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
            limiter = self._limiters.get(provider_id)
            if limiter and not limiter.acquire(timeout=self._limiter_timeout):
                last_error = f"Attempt {attempt + 1}: {provider_id} rate limit (limiter timeout)"
                logger.debug(
                    "LLM attempt skipped",
                    extra={
                        "attempt": attempt + 1,
                        "model": model,
                        "error": last_error,
                    },
                )
                inc_metric("llm_errors_total")
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
                    if task_id:
                        # Streaming responses don't surface aggregated usage
                        # metadata reliably, so count tokens heuristically.
                        self._record_usage(
                            ChatResponse(
                                content=full_text,
                                model=model,
                                provider=provider_id,
                            ),
                            agent_name,
                            task_id,
                            attempt + 1,
                            usage=TokenUsage(
                                prompt_tokens=count_prompt_tokens(
                                    system_prompt, task_instruction, model
                                ),
                                completion_tokens=count_tokens(full_text, model),
                            ),
                        )
                    inc_metric("llm_requests_total")
                    return
                last_raw = full_text
                last_error = f"Attempt {attempt + 1}: Invalid JSON from {provider_id}/{model}"
                logger.debug(
                    "LLM attempt failed",
                    extra={
                        "attempt": attempt + 1,
                        "model": model,
                        "error": last_error,
                    },
                )
            except LLMProviderError as exc:
                if breaker:
                    breaker.record_failure(exc.category.value)
                last_error = f"Attempt {attempt + 1}: {exc}"
                logger.debug(
                    "LLM attempt failed",
                    extra={
                        "attempt": attempt + 1,
                        "model": model,
                        "error": str(exc),
                    },
                )
                inc_metric("llm_errors_total")

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
        usage: TokenUsage | None = None,
    ) -> None:
        """Record token usage to JSONL (CostTracker), SQLite (CostAnalytics),
        and the dashboard Prometheus counters.

        Prefers provider-reported usage metadata and falls back to heuristic
        token counts (see ``ai_company.llm.token_counter``). The existing
        JSONL logging via CostTracker is preserved as-is. When the SQLite
        database singleton is available, usage is also written to the
        ``cost_records`` table for dashboard analytics — unless a CostTracker
        is attached, in which case the tracker's own SQLite mirror is the
        single write path (OB5, no double-write).

        Args:
            response: The ChatResponse from the provider.
            agent_name: Name of the agent that made the call.
            task_id: Task ID for cost tracking.
            iteration: Current iteration number.
            usage: TokenUsage for the call. When omitted, falls back to the
                response's own token fields.
        """
        if not task_id:
            return

        if usage is None:
            usage = TokenUsage(
                prompt_tokens=int(getattr(response, "prompt_tokens", 0) or 0),
                completion_tokens=int(getattr(response, "completion_tokens", 0) or 0),
            )

        cost_usd = 0.0

        # ── 1. JSONL logging (existing CostTracker) ────────────────
        cost_tracker = getattr(self, "_cost_tracker", None)
        if cost_tracker is not None:
            try:
                record = cost_tracker.record_usage(
                    model=response.model,
                    provider=response.provider,
                    agent_name=agent_name,
                    task_id=task_id,
                    prompt_tokens=usage.prompt_tokens,
                    completion_tokens=usage.completion_tokens,
                    iteration=iteration,
                )
                cost_usd = record.cost_usd
            except Exception:  # noqa: BLE001 - cost tracking is best-effort
                logger.debug(
                    "JSONL cost tracking failed for task %s",
                    task_id,
                    exc_info=True,
                )

        # Compute cost if the tracker didn't (or wasn't configured)
        if cost_usd == 0.0:
            cost_usd = round(
                usage.prompt_tokens * _cost_per_token(response.model, "input")
                + usage.completion_tokens * _cost_per_token(response.model, "output"),
                8,
            )

        # Feed the Prometheus cost counters (OB1).
        record_llm_cost(provider=response.provider, cost_usd=cost_usd)

        # ── 2. SQLite recording (CostAnalytics) ───────────────────
        # OB5: when a CostTracker is attached it already mirrors every
        # usage record to SQLite (see CostTracker.record_usage), so writing
        # here too would double-count cost rows. Only fall back to the
        # direct SQLite write when no tracker is configured.
        if cost_tracker is None:
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
                        prompt_tokens=usage.prompt_tokens,
                        completion_tokens=usage.completion_tokens,
                        cost_usd=cost_usd,
                        iteration=iteration,
                    )
            except Exception:  # noqa: BLE001 - cost analytics is best-effort
                logger.debug(
                    "SQLite cost tracking failed for task %s",
                    task_id,
                    exc_info=True,
                )

    def _parse_response(self, content: str) -> dict[str, Any] | None:
        """Try to parse the LLM response as JSON."""
        return parse_llm_json(content)

    def get_provider(self, provider_id: str) -> LLMProvider | None:
        return self._providers.get(provider_id)

    def get_breaker(self, provider_id: str) -> CircuitBreaker | None:
        """Return the circuit breaker for a provider, if one is configured."""
        return self._circuit_breakers.get(provider_id)
