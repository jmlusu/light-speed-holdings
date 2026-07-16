"""Unified LLM client — routes tasks to the right provider with retry logic."""

from __future__ import annotations

import json
import re
from typing import Any

from dotenv import load_dotenv

load_dotenv()


from ai_company.llm.providers.base import (
    LLMProvider,
    LLMProviderError,
    LLMResponseError,
)
from ai_company.llm.providers.openai_compatible import OpenAICompatibleProvider
from ai_company.llm.providers.ollama import OllamaProvider
from ai_company.model_router import ModelRouter


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
        self._init_providers()

    def _init_providers(self) -> None:
        """Create provider instances from models.yaml config."""
        for pcfg in self.router.list_providers():
            if pcfg.id == "ollama":
                self._providers[pcfg.id] = OllamaProvider(
                    name=pcfg.id,
                    api_base=pcfg.api_base or "http://localhost:11434",
                    default_model=pcfg.default_model,
                )
            else:
                # OpenAI-compatible: opencode, deepseek, openai, anthropic
                api_key_env = f"{pcfg.id.upper()}_API_KEY"
                self._providers[pcfg.id] = OpenAICompatibleProvider(
                    name=pcfg.id,
                    api_base=pcfg.api_base,
                    default_model=pcfg.default_model,
                    api_key_env=api_key_env,
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
            agent_name=agent_name, priority=priority, context=context
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

        for attempt in range(1, max_retries + 1):
            for provider_id, model in provider_chain:
                provider = self._providers.get(provider_id)
                if not provider or not provider.is_available():
                    continue

                try:
                    response = provider.chat(
                        system_prompt=system_prompt,
                        user_prompt=task_instruction,
                        model=model,
                    )
                    parsed = self._parse_response(response.content)
                    if parsed is not None:
                        return parsed
                    last_raw = response.content
                    last_error = f"Attempt {attempt}: Invalid JSON from {provider_id}/{model}"
                    break  # Move to next attempt (retry with same provider chain)
                except LLMProviderError as exc:
                    last_error = f"Attempt {attempt}: {exc}"
                    continue  # Try next provider in tier

        raise LLMResponseError(
            f"Failed to get valid JSON after {max_retries} attempts. Last error: {last_error}",
            attempts=max_retries,
            last_raw=last_raw,
        )

    def _parse_response(self, content: str) -> dict[str, Any] | None:
        """Try to parse the LLM response as JSON.

        Attempts:
        1. Direct JSON parse
        2. Extract from markdown code block (```json ... ```)
        3. Extract first { ... } block from text
        """
        # Attempt 1: direct parse
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                return data
        except (json.JSONDecodeError, TypeError):
            pass

        # Attempt 2: extract from markdown code block
        match = re.search(r"```(?:json)?\s*\n(.*?)\n```", content, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
                if isinstance(data, dict):
                    return data
            except (json.JSONDecodeError, TypeError):
                pass

        # Attempt 3: find first { ... } block
        depth = 0
        start = -1
        for i, ch in enumerate(content):
            if ch == "{":
                if depth == 0:
                    start = i
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0 and start >= 0:
                    try:
                        data = json.loads(content[start : i + 1])
                        if isinstance(data, dict):
                            return data
                    except (json.JSONDecodeError, TypeError):
                        start = -1

        return None

    def get_provider(self, provider_id: str) -> LLMProvider | None:
        return self._providers.get(provider_id)

    def list_available_providers(self) -> list[str]:
        return [pid for pid, p in self._providers.items() if p.is_available()]
