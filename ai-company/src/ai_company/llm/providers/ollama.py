"""Local Ollama LLM provider."""

from __future__ import annotations

import json
from collections.abc import Generator

import httpx

from ai_company.llm.providers.base import (
    ChatResponse,
    LLMProvider,
    LLMProviderError,
    StreamChunk,
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
            prompt_tokens=prompt_eval_count,
            completion_tokens=eval_count,
            total_tokens=prompt_eval_count + eval_count,
        )

    def chat_stream(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
    ) -> Generator[StreamChunk, None, None]:
        model = model or self.default_model

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": True,
            "options": {
                "temperature": 0.3,
                "num_predict": 4096,
            },
        }

        try:
            with self._client.stream("POST", "/api/chat", json=payload) as resp:
                if resp.status_code != 200:
                    raise LLMProviderError(
                        self.name,
                        f"Ollama returned {resp.status_code}: "
                        f"{resp.read()[:200].decode('utf-8', errors='replace')}",
                        status_code=resp.status_code,
                    )

                for line in resp.iter_lines():
                    if not line:
                        continue
                    try:
                        chunk = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    message = chunk.get("message", {})
                    content = message.get("content", "")
                    done = chunk.get("done", False)
                    if done:
                        yield StreamChunk(
                            delta="",
                            finish_reason="stop",
                            usage={
                                "prompt_tokens": chunk.get("prompt_eval_count", 0),
                                "completion_tokens": chunk.get("eval_count", 0),
                            },
                        )
                        return
                    if content:
                        yield StreamChunk(delta=content)
        except httpx.ConnectError:
            raise LLMProviderError(
                self.name,
                f"Cannot connect to Ollama at {self.api_base}. Is Ollama running?",
            )
        except httpx.TimeoutException as exc:
            raise LLMProviderError(self.name, f"Request timed out: {exc}") from exc
        except httpx.HTTPError as exc:
            raise LLMProviderError(self.name, f"HTTP error: {exc}") from exc

    def is_available(self) -> bool:
        try:
            resp = self._client.get("/api/tags", timeout=3.0)
            return resp.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException):
            return False
