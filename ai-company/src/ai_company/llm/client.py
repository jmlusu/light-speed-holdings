"""Unified LLM client — routes tasks to the right provider with retry logic."""

from __future__ import annotations

from collections.abc import Generator
from typing import Any

from ai_company.llm.circuit_breaker import CircuitBreaker
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

from dotenv import load_dotenv

load_dotenv()


_MAX_RETRIES = 5


class LLMClient:
    """Unified client that resolves provider via ModelRouter and executes tasks.

    Retry policy: up to 5 attempts if the LLM response is not valid JSON.
    Falls back through the tier's provider chain on provider errors.
    """

    def __init__(
        self,
        config_path: str = "company/models.yaml",
        registry_path: str = "company/agent-registry.json",
    ) -> None:
        self.router = ModelRouter(config_path=config_path, registry_path=registry_path)
        self._providers: dict[str, LLMProvider] = {}
        self._circuit_breakers: dict[str, CircuitBreaker] = {}
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
    ) -> dict[str, Any]:
        """Execute a task by calling the LLM and parsing the structured response.

        Returns parsed JSON dict with keys: plan, result, artifacts.
        Retries up to max_retries times if response is not valid JSON.
        Falls back to next provider in tier on provider errors.

        Raises:
            LLMResponseError: If all retries exhausted without valid JSON.
            LLMProviderError: If no provider is available.
        """
        route = self.router.resolve(
            agent_name=agent_name, priority=priority, context=context,
            task_prompt=task_instruction,
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

        for attempt in range(1, max_retries + 1):
            for provider_id, model in provider_chain:
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
                    last_error = (
                        f"Attempt {attempt}: Invalid JSON from {provider_id}/{model}"
                    )
                    break
                except LLMProviderError as exc:
                    if breaker:
                        breaker.record_failure()
                    last_error = f"Attempt {attempt}: {exc}"
                    continue

        raise LLMResponseError(
            f"Failed to get valid JSON after {max_retries} attempts. Last error: {last_error}",
            attempts=max_retries,
            last_raw=full_text if "full_text" in dir() else "",
        )

    def _parse_response(self, content: str) -> dict[str, Any] | None:
        """Try to parse the LLM response as JSON."""
        return parse_llm_json(content)

    def get_provider(self, provider_id: str) -> LLMProvider | None:
        return self._providers.get(provider_id)

    def list_available_providers(self) -> list[str]:
        return [pid for pid, p in self._providers.items() if p.is_available()]
