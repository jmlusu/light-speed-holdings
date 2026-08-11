"""OpenAI-compatible LLM provider.

Handles both OpenCode (Big Pickle) and Deepseek since both expose
an OpenAI-compatible /v1/chat/completions endpoint.
"""

from __future__ import annotations

import json
import logging
import os
import time
from collections.abc import Generator
from typing import TYPE_CHECKING, Any

import httpx

from ai_company.llm.providers.base import (
    ChatResponse,
    LLMProvider,
    LLMProviderError,
    StreamChunk,
)

if TYPE_CHECKING:
    from ai_company.llm.oauth2 import OAuth2TokenManager

logger = logging.getLogger(__name__)


class OpenAICompatibleProvider(LLMProvider):
    """Provider for any OpenAI-compatible API (OpenCode, Deepseek, etc.).

    Auth is resolved per request: either a static API key (``api_key_env``)
    or an OAuth2 client-credentials token (``oauth2``). When no auth is
    configured the provider is unavailable (fail-closed).
    """

    def __init__(
        self,
        name: str,
        api_base: str,
        default_model: str,
        api_key_env: str = "",
        timeout: float = 120.0,
        auth_style: str = "bearer",  # "bearer" for OpenAI-family, "x-api-key" for Anthropic
        oauth2: OAuth2TokenManager | None = None,
    ) -> None:
        self.name = name
        self.api_base = api_base.rstrip("/")
        self.default_model = default_model
        self.timeout = timeout
        self.auth_style = auth_style
        self._oauth2 = oauth2

        # Resolve API key from env var
        api_key = ""
        if api_key_env:
            api_key = os.environ.get(api_key_env, "")
        if not api_key:
            api_key = os.environ.get(f"{name.upper()}_API_KEY", "")

        self._api_key = api_key
        self._client: httpx.Client | None = None
        if api_key or (oauth2 is not None and oauth2.is_configured):
            headers = {"Content-Type": "application/json"}
            if auth_style == "x-api-key":
                headers["anthropic-version"] = "2023-06-01"
            self._client = httpx.Client(
                base_url=self.api_base,
                headers=headers,
                timeout=self.timeout,
            )

    def _auth_headers(self) -> dict[str, str]:
        """Build per-request auth headers from OAuth2 or a static API key.

        Raises:
            LLMProviderError: If OAuth2 is configured but a token cannot be
                obtained, or no auth is available at all.
        """
        if self._oauth2 is not None:
            token = self._oauth2.get_access_token()
            return {"Authorization": f"Bearer {token}"}
        if self.auth_style == "x-api-key":
            return {
                "x-api-key": self._api_key,
                "anthropic-version": "2023-06-01",
            }
        return {"Authorization": f"Bearer {self._api_key}"}

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
    ) -> ChatResponse:
        if not self._client:
            raise LLMProviderError(self.name, "No API key or OAuth2 credentials configured")

        model = model or self.default_model

        if self.auth_style == "x-api-key":
            # Anthropic API format
            endpoint = "/v1/messages"
            payload: dict[str, Any] = {
                "model": model,
                "max_tokens": 4096,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_prompt}],
            }
        else:
            # OpenAI-compatible format
            endpoint = "/chat/completions"
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.3,
                "max_tokens": 4096,
            }

        start = time.perf_counter()
        try:
            resp = self._client.post(
                endpoint,
                json=payload,
                headers=self._auth_headers(),
            )
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
        logger.info(
            "LLM chat completed in %.1f ms (provider=%s, model=%s)",
            (time.perf_counter() - start) * 1000,
            self.name,
            model,
        )

        if self.auth_style == "x-api-key":
            # Anthropic response format
            content = data.get("content", [{}])[0].get("text", "")
            usage = data.get("usage", {})
            prompt_tok = usage.get("input_tokens", 0)
            comp_tok = usage.get("output_tokens", 0)
            return ChatResponse(
                content=content,
                model=model,
                provider=self.name,
                prompt_tokens=prompt_tok,
                completion_tokens=comp_tok,
                total_tokens=prompt_tok + comp_tok,
            )
        else:
            # OpenAI response format
            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            prompt_tok = usage.get("prompt_tokens", 0)
            comp_tok = usage.get("completion_tokens", 0)
            return ChatResponse(
                content=content,
                model=model,
                provider=self.name,
                prompt_tokens=prompt_tok,
                completion_tokens=comp_tok,
                total_tokens=prompt_tok + comp_tok,
            )

    def chat_stream(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
    ) -> Generator[StreamChunk, None, None]:
        if not self._client:
            raise LLMProviderError(self.name, "No API key or OAuth2 credentials configured")

        model = model or self.default_model

        if self.auth_style == "x-api-key":
            endpoint = "/v1/messages"
            payload: dict[str, Any] = {
                "model": model,
                "max_tokens": 4096,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_prompt}],
                "stream": True,
            }
        else:
            endpoint = "/chat/completions"
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.3,
                "max_tokens": 4096,
                "stream": True,
            }

        start = time.perf_counter()
        try:
            with self._client.stream(
                "POST",
                endpoint,
                json=payload,
                headers=self._auth_headers(),
            ) as resp:
                if resp.status_code != 200:
                    raise LLMProviderError(
                        self.name,
                        f"API returned {resp.status_code}: "
                        f"{resp.read()[:200].decode('utf-8', errors='replace')}",
                        status_code=resp.status_code,
                    )

                if self.auth_style == "x-api-key":
                    yield from self._parse_anthropic_sse(resp)
                else:
                    yield from self._parse_openai_sse(resp)
        except httpx.TimeoutException as exc:
            raise LLMProviderError(self.name, f"Request timed out: {exc}") from exc
        except httpx.HTTPError as exc:
            raise LLMProviderError(self.name, f"HTTP error: {exc}") from exc
        logger.info(
            "LLM stream completed in %.1f ms (provider=%s, model=%s)",
            (time.perf_counter() - start) * 1000,
            self.name,
            model,
        )

    def _parse_openai_sse(self, resp: httpx.Response) -> Generator[StreamChunk, None, None]:
        """Parse OpenAI-format SSE stream."""
        for line in resp.iter_lines():
            if not line:
                continue
            if not line.startswith("data: "):
                continue
            payload = line[6:]
            if payload.strip() == "[DONE]":
                yield StreamChunk(delta="", finish_reason="stop")
                return
            try:
                chunk = json.loads(payload)
            except json.JSONDecodeError:
                continue
            choice = chunk.get("choices", [{}])[0]
            delta_obj = choice.get("delta", {})
            content = delta_obj.get("content", "")
            finish = choice.get("finish_reason")
            usage_data = chunk.get("usage")
            usage = None
            if usage_data:
                usage = {
                    "prompt_tokens": usage_data.get("prompt_tokens", 0),
                    "completion_tokens": usage_data.get("completion_tokens", 0),
                }
            if content or finish:
                yield StreamChunk(
                    delta=content or "",
                    finish_reason=finish,
                    usage=usage,
                )

    def _parse_anthropic_sse(self, resp: httpx.Response) -> Generator[StreamChunk, None, None]:
        """Parse Anthropic-format SSE stream."""
        event_type = ""
        for line in resp.iter_lines():
            if not line:
                event_type = ""
                continue
            if line.startswith("event: "):
                event_type = line[7:]
                continue
            if not line.startswith("data: "):
                continue
            try:
                data = json.loads(line[6:])
            except json.JSONDecodeError:
                continue
            if event_type == "content_block_delta":
                delta_obj = data.get("delta", {})
                text = delta_obj.get("text", "")
                if text:
                    yield StreamChunk(delta=text)
            elif event_type == "message_stop":
                yield StreamChunk(delta="", finish_reason="stop")
                return
            elif event_type == "message_delta":
                usage_data = data.get("usage")
                if usage_data:
                    yield StreamChunk(
                        delta="",
                        finish_reason=data.get("delta", {}).get("stop_reason", "stop"),
                        usage={
                            "prompt_tokens": 0,
                            "completion_tokens": usage_data.get("output_tokens", 0),
                        },
                    )

    def is_available(self) -> bool:
        if self._client is None:
            return False
        if self._oauth2 is not None:
            return self._oauth2.is_configured
        return True
