"""OpenAI-compatible LLM provider.

Handles both OpenCode (Big Pickle) and Deepseek since both expose
an OpenAI-compatible /v1/chat/completions endpoint.
"""

from __future__ import annotations

import os
from typing import Any

import httpx

from ai_company.llm.providers.base import (
    ChatResponse,
    LLMProvider,
    LLMProviderError,
)


class OpenAICompatibleProvider(LLMProvider):
    """Provider for any OpenAI-compatible API (OpenCode, Deepseek, etc.)."""

    def __init__(
        self,
        name: str,
        api_base: str,
        default_model: str,
        api_key_env: str = "",
        timeout: float = 120.0,
    ) -> None:
        self.name = name
        self.api_base = api_base.rstrip("/")
        self.default_model = default_model
        self.timeout = timeout

        # Resolve API key from env var
        api_key = ""
        if api_key_env:
            api_key = os.environ.get(api_key_env, "")
        if not api_key:
            api_key = os.environ.get(f"{name.upper()}_API_KEY", "")

        self._api_key = api_key
        self._client: httpx.Client | None = None
        if api_key:
            self._client = httpx.Client(
                base_url=self.api_base,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                timeout=self.timeout,
            )

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
    ) -> ChatResponse:
        if not self._client:
            raise LLMProviderError(self.name, "No API key configured")

        model = model or self.default_model

        payload: dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 4096,
        }

        try:
            resp = self._client.post("/chat/completions", json=payload)
        except httpx.TimeoutException as exc:
            raise LLMProviderError(self.name, f"Request timed out: {exc}") from exc
        except httpx.HTTPError as exc:
            raise LLMProviderError(self.name, f"HTTP error: {exc}") from exc

        if resp.status_code != 200:
            raise LLMProviderError(
                self.name,
                f"API returned {resp.status_code}: {resp.text[:200]}",
                status_code=resp.status_code,
            )

        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})

        return ChatResponse(
            content=content,
            model=model,
            provider=self.name,
            usage={
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
            },
        )

    def is_available(self) -> bool:
        return self._client is not None
