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
from ai_company.llm.prompt_compressor import PromptCompressor
from ai_company.llm.providers.base import (
    ChatResponse,
    LLMProvider,
    LLMProviderError,
    LLMResponseError,
    StreamChunk,
)
from ai_company.llm.providers.llamacpp import LlamaCppConfig, LlamaCppProvider
from ai_company.llm.providers.ollama import OllamaProvider
from ai_company.llm.providers.openai_compatible import OpenAICompatibleProvider
from ai_company.llm.response_cache import ResponseCache
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
        response_cache: ResponseCache | None = None,
        prompt_compressor: PromptCompressor | None = None,
    ) -> None:
        self.router = ModelRouter(config_path=config_path, registry_path=registry_path)
        self._providers: dict[str, LLMProvider] = {}
        self._circuit_breakers: dict[str, CircuitBreaker] = {}
        self._limiters: dict[str, TokenBucket] = {}
        self._cost_tracker = cost_tracker
        self._limiter_timeout = limiter_timeout
        self._response_cache = response_cache
        self._prompt_compressor = prompt_compressor
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
            elif pcfg.id == "llamacpp":
                # Get model-specific config from models.yaml
                model_dir = getattr(pcfg, "model_dir", "./models")
                model_name = pcfg.default_model
                models_config = getattr(pcfg, "models", {})
                model_config = models_config.get(model_name, {})
                model_path = model_config.get("path", f"{model_dir}/{model_name}.gguf")

                # Hardware config (model-specific overrides provider defaults)
                hw_config = getattr(pcfg, "hardware", {})
                model_hw = model_config.get("hardware", {})
                hw_config = {**hw_config, **model_hw}

                # Inference config
                inf_config = getattr(pcfg, "inference", {})

                llama_config = LlamaCppConfig(
                    model_path=model_path,
                    n_ctx=hw_config.get("n_ctx", 32768),
                    n_batch=hw_config.get("n_batch", 512),
                    n_threads=hw_config.get("n_threads", 8),
                    n_threads_batch=hw_config.get("n_threads_batch", 8),
                    n_gpu_layers=hw_config.get("n_gpu_layers", 0),
                    use_mlock=hw_config.get("use_mlock", True),
                    use_mmap=hw_config.get("use_mmap", True),
                    temperature=inf_config.get("temperature", 0.3),
                    top_p=inf_config.get("top_p", 0.9),
                    top_k=inf_config.get("top_k", 40),
                    repeat_penalty=inf_config.get("repeat_penalty", 1.1),
                )

                # Get server config from provider config
                server_config = getattr(pcfg, "server", {}) or {}
                server_port = server_config.get("port", 8088)
                server_host = server_config.get("host", "127.0.0.1")
                api_key = server_config.get("api_key", "local")
                model_ports = server_config.get("ports", {})

                self._providers[pcfg.id] = LlamaCppProvider(
                    name=pcfg.id,
                    model_path=model_path,
                    config=llama_config,
                    server_port=server_port,
                    server_host=server_host,
                    use_server=True,
                    api_key=api_key,
                    model_ports=model_ports,
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

        self._log_omniroute_status()

    @staticmethod
    def _log_omniroute_status(_unused: Any | None = None) -> None:
        """Log OmniRoute gateway connectivity at startup."""
        import os

        omniroute_key = os.environ.get("OMNIROUTE_API_KEY", "")
        omniroute_url = os.environ.get("OMNIROUTE_API_BASE", "http://localhost:20128")

        if not omniroute_key:
            logger.info("OmniRoute: not configured (OMNIROUTE_API_KEY not set)")
            return

        try:
            import httpx

            resp = httpx.get(f"{omniroute_url}/health", timeout=3.0)
            if resp.status_code == 200:
                logger.info("OmniRoute: reachable at %s", omniroute_url)
            else:
                logger.warning("OmniRoute: HTTP %d at %s", resp.status_code, omniroute_url)
        except Exception as exc:  # noqa: BLE001
            logger.warning("OmniRoute: unreachable at %s (%s)", omniroute_url, exc)

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

        # Optional prompt compression to reduce token count.
        if self._prompt_compressor is not None:
            system_prompt, task_instruction, compression = self._prompt_compressor.compress(
                system_prompt, task_instruction
            )
            logger.debug(
                "Prompt compressed: %d → %d tokens (%.0f%% reduction)",
                compression.original_tokens_est,
                compression.compressed_tokens_est,
                compression.reduction_ratio * 100,
            )

        # Assemble the exact prompt text once so heuristic fallback counts
        # match what was actually sent to the provider.
        prompt_text = join_prompt(system_prompt, task_instruction)

        # Optional response cache check — only for deterministic queries
        # (temperature=0). Creative/non-deterministic outputs must not be cached.
        if self._response_cache is not None:
            cached = self._response_cache.get(
                system_prompt=system_prompt,
                user_prompt=task_instruction,
                model=route.model,
                temperature=0.0,
            )
            if cached is not None:
                logger.info(
                    "Cache hit: agent=%s model=%s tokens_saved=%d cost_saved=$%.6f",
                    agent_name,
                    route.model,
                    cached.tokens_saved,
                    cached.cost_saved,
                )
                parsed = self._parse_response(cached.content)
                if parsed is not None:
                    return parsed

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
                    # Cache successful responses for deterministic queries.
                    if self._response_cache is not None:
                        self._response_cache.set(
                            system_prompt=system_prompt,
                            user_prompt=task_instruction,
                            model=model,
                            temperature=0.0,
                            response_content=response.content,
                            tokens_used=usage.total_tokens,
                            cost_usd=getattr(
                                self._cost_tracker,
                                "_calculate_cost",
                                lambda m, p, c: 0.0,
                            )(model, usage.prompt_tokens, usage.completion_tokens),
                        )
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

                # Check for token-limit error and try to rotate
                if self._is_token_limit_error(str(exc)):
                    logger.info(
                        "Token limit detected, attempting rotation from %s/%s",
                        provider_id,
                        model,
                    )
                    # Try to rotate to a different model (sync version)
                    rotated_route = self.router.rotate_on_token_limit_sync(model, task_instruction)
                    if rotated_route and rotated_route.model != model:
                        # Use the rotated model for the next attempt
                        provider_chain.append((rotated_route.provider, rotated_route.model))
                        logger.info(
                            "Rotated to %s/%s (tier: %s)",
                            rotated_route.provider,
                            rotated_route.model,
                            rotated_route.tier,
                        )

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

        # Optional prompt compression to reduce token count.
        if self._prompt_compressor is not None:
            system_prompt, task_instruction, compression = self._prompt_compressor.compress(
                system_prompt, task_instruction
            )
            logger.debug(
                "Prompt compressed: %d → %d tokens (%.0f%% reduction)",
                compression.original_tokens_est,
                compression.compressed_tokens_est,
                compression.reduction_ratio * 100,
            )

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

    def _is_token_limit_error(self, error_msg: str) -> bool:
        """Check if an error message indicates a token/context limit exceeded.

        Returns True if the error message contains patterns suggesting
        the context window was exceeded, triggering rotation logic.
        """
        from ai_company.model_router import ModelRouter

        lowered = error_msg.lower()
        return any(pattern in lowered for pattern in ModelRouter.TOKEN_LIMIT_PATTERNS)

    def get_provider(self, provider_id: str) -> LLMProvider | None:
        return self._providers.get(provider_id)

    def get_breaker(self, provider_id: str) -> CircuitBreaker | None:
        """Return the circuit breaker for a provider, if one is configured."""
        return self._circuit_breakers.get(provider_id)
