"""Local Ollama LLM provider."""

from __future__ import annotations

import httpx

from ai_company.llm.providers.base import (
    ChatResponse,
    LLMProvider,
    LLMProviderError,
)


class OllamaProvider(LLMProvider):
    """Provider for local Ollama instances."""

    def __init__(
        self,
        name: str = "ollama",
        api_base: str = "http://localhost:11434",
        default_model: str = "llama3.1:8b",
        timeout: float = 300.0,
    ) -> None:
        self.name = name
        self.api_base = api_base.rstrip("/")
        self.default_model = default_model
        self._client = httpx.Client(
            base_url=self.api_base,
            timeout=timeout,
        )

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
    ) -> ChatResponse:
        model = model or self.default_model

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 4096,
            },
        }

        try:
            resp = self._client.post("/api/chat", json=payload)
        except httpx.ConnectError:
            raise LLMProviderError(
                self.name,
                f"Cannot connect to Ollama at {self.api_base}. Is Ollama running?",
            )
        except httpx.TimeoutException as exc:
            raise LLMProviderError(self.name, f"Request timed out: {exc}") from exc
        except httpx.HTTPError as exc:
            raise LLMProviderError(self.name, f"HTTP error: {exc}") from exc

        if resp.status_code != 200:
            raise LLMProviderError(
                self.name,
                f"Ollama returned {resp.status_code}: {resp.text[:200]}",
                status_code=resp.status_code,
            )

        data = resp.json()
        content = data["message"]["content"]
        eval_count = data.get("eval_count", 0)
        prompt_eval_count = data.get("prompt_eval_count", 0)

        return ChatResponse(
            content=content,
            model=model,
            provider=self.name,
            usage={
                "prompt_tokens": prompt_eval_count,
                "completion_tokens": eval_count,
            },
        )

    def is_available(self) -> bool:
        try:
            resp = self._client.get("/api/tags", timeout=3.0)
            return resp.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException):
            return False
