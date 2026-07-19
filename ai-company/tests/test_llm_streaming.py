"""Tests for LLM streaming support."""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest

from ai_company.llm.providers.base import (
    ChatResponse,
    LLMProvider,
    LLMProviderError,
    StreamChunk,
)
from ai_company.llm.providers.ollama import OllamaProvider
from ai_company.llm.providers.openai_compatible import OpenAICompatibleProvider


# ---------------------------------------------------------------------------
# Default fallback: chat_stream() delegates to chat()
# ---------------------------------------------------------------------------


class StubProvider(LLMProvider):
    """Minimal provider that only implements chat() for fallback testing."""

    name = "stub"

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
    ) -> ChatResponse:
        return ChatResponse(
            content='{"result": "ok"}',
            model="stub-v1",
            provider="stub",
            usage={"prompt_tokens": 10, "completion_tokens": 5},
        )

    def is_available(self) -> bool:
        return True


def test_chat_stream_fallback():
    provider = StubProvider()
    chunks = list(provider.chat_stream("sys", "usr"))
    assert len(chunks) == 1
    assert chunks[0].delta == '{"result": "ok"}'
    assert chunks[0].finish_reason == "stop"
    assert chunks[0].usage == {"prompt_tokens": 10, "completion_tokens": 5}


def test_stream_chunk_immutability():
    chunk = StreamChunk(delta="hello", finish_reason="stop")
    assert chunk.delta == "hello"
    assert chunk.finish_reason == "stop"
    assert chunk.usage is None


# ---------------------------------------------------------------------------
# OpenAI-compatible streaming
# ---------------------------------------------------------------------------


def _make_openai_sse_chunks(*texts: str) -> list[str]:
    """Build raw SSE lines for OpenAI format."""
    lines: list[str] = []
    for text in texts:
        chunk = {
            "choices": [{"delta": {"content": text}, "finish_reason": None}],
        }
        lines.append(f"data: {json.dumps(chunk)}\n")
    # Final chunk
    lines.append("data: {\"choices\": [{\"delta\": {}, \"finish_reason\": \"stop\"}]}\n")
    lines.append("data: [DONE]\n")
    return lines


def _mock_openai_response(status_code: int = 200, body_lines: list[str] | None = None) -> MagicMock:
    """Create a mock httpx.Response for OpenAI SSE."""
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    if body_lines is None:
        body_lines = _make_openai_sse_chunks("Hello", " world")
    resp.iter_lines.return_value = [line.rstrip("\n") for line in body_lines]
    resp.read.return_value = b"error body"
    return resp


def test_openai_streaming_yields_chunks():
    provider = OpenAICompatibleProvider(
        name="test-openai",
        api_base="https://api.example.com/v1",
        default_model="gpt-4o",
        api_key_env="TEST_OPENAI_KEY",
    )
    mock_client = MagicMock(spec=httpx.Client)
    provider._client = mock_client

    mock_resp = _mock_openai_response()
    mock_client.stream.return_value.__enter__ = MagicMock(return_value=mock_resp)
    mock_client.stream.return_value.__exit__ = MagicMock(return_value=False)

    chunks = list(provider.chat_stream("sys", "usr"))
    deltas = [c.delta for c in chunks]
    assert "Hello" in deltas
    assert " world" in deltas
    assert any(c.finish_reason == "stop" for c in chunks)


def test_openai_streaming_no_api_key():
    provider = OpenAICompatibleProvider(
        name="test-openai",
        api_base="https://api.example.com/v1",
        default_model="gpt-4o",
    )
    provider._client = None
    with pytest.raises(LLMProviderError, match="No API key"):
        list(provider.chat_stream("sys", "usr"))


def test_openai_streaming_http_error():
    provider = OpenAICompatibleProvider(
        name="test-openai",
        api_base="https://api.example.com/v1",
        default_model="gpt-4o",
        api_key_env="TEST_OPENAI_KEY",
    )
    mock_client = MagicMock(spec=httpx.Client)
    provider._client = mock_client

    resp = MagicMock(spec=httpx.Response)
    resp.status_code = 500
    resp.read.return_value = b"internal error"
    mock_client.stream.return_value.__enter__ = MagicMock(return_value=resp)
    mock_client.stream.return_value.__exit__ = MagicMock(return_value=False)

    with pytest.raises(LLMProviderError, match="500"):
        list(provider.chat_stream("sys", "usr"))


# ---------------------------------------------------------------------------
# OpenAI SSE edge cases
# ---------------------------------------------------------------------------


def test_openai_streaming_empty_content_delta():
    provider = OpenAICompatibleProvider(
        name="test-openai",
        api_base="https://api.example.com/v1",
        default_model="gpt-4o",
        api_key_env="TEST_OPENAI_KEY",
    )
    mock_client = MagicMock(spec=httpx.Client)
    provider._client = mock_client

    lines = [
        'data: {"choices": [{"delta": {"role": "assistant"}, "finish_reason": null}]}\n',
        'data: {"choices": [{"delta": {"content": "hi"}, "finish_reason": null}]}\n',
        'data: {"choices": [{"delta": {}, "finish_reason": "stop"}]}\n',
        "data: [DONE]\n",
    ]
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = 200
    resp.iter_lines.return_value = [line.rstrip("\n") for line in lines]
    mock_client.stream.return_value.__enter__ = MagicMock(return_value=resp)
    mock_client.stream.return_value.__exit__ = MagicMock(return_value=False)

    chunks = list(provider.chat_stream("sys", "usr"))
    # role-only delta (no content) is skipped, so first real chunk is "hi"
    assert chunks[0].delta == "hi"
    assert chunks[0].finish_reason is None
    deltas = [c.delta for c in chunks if c.delta]
    assert deltas == ["hi"]


# ---------------------------------------------------------------------------
# Anthropic streaming
# ---------------------------------------------------------------------------


def _mock_anthropic_response(status_code: int = 200, body_lines: list[str] | None = None) -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    if body_lines is None:
        body_lines = [
            "event: content_block_delta",
            'data: {"delta": {"type": "text_delta", "text": "Hey"}}',
            "",
            "event: content_block_delta",
            'data: {"delta": {"type": "text_delta", "text": " there"}}',
            "",
            "event: message_delta",
            'data: {"delta": {"stop_reason": "end_turn"}, "usage": {"output_tokens": 12}}',
            "",
            "event: message_stop",
            "data: {}",
        ]
    resp.iter_lines.return_value = body_lines
    resp.read.return_value = b"error body"
    return resp


def test_anthropic_streaming_yields_chunks():
    provider = OpenAICompatibleProvider(
        name="anthropic",
        api_base="https://api.anthropic.com",
        default_model="claude-sonnet-4-20250514",
        api_key_env="ANTHROPIC_API_KEY",
        auth_style="x-api-key",
    )
    mock_client = MagicMock(spec=httpx.Client)
    provider._client = mock_client

    mock_resp = _mock_anthropic_response()
    mock_client.stream.return_value.__enter__ = MagicMock(return_value=mock_resp)
    mock_client.stream.return_value.__exit__ = MagicMock(return_value=False)

    chunks = list(provider.chat_stream("sys", "usr"))
    deltas = [c.delta for c in chunks]
    assert "Hey" in deltas
    assert " there" in deltas
    assert any(c.finish_reason == "stop" for c in chunks)


# ---------------------------------------------------------------------------
# Ollama streaming
# ---------------------------------------------------------------------------


def _make_ollama_ndjson_chunks(*texts: str) -> list[str]:
    lines: list[str] = []
    for text in texts:
        chunk = {"message": {"content": text}, "done": False}
        lines.append(json.dumps(chunk))
    done_chunk: dict[str, Any] = {
        "message": {"content": ""},
        "done": True,
        "eval_count": 20,
        "prompt_eval_count": 10,
    }
    lines.append(json.dumps(done_chunk))
    return lines


def test_ollama_streaming_yields_chunks():
    provider = OllamaProvider(
        name="ollama",
        api_base="http://localhost:11434",
        default_model="llama3.1:8b",
    )
    mock_client = MagicMock(spec=httpx.Client)
    provider._client = mock_client

    body_lines = _make_ollama_ndjson_chunks("Hi", " there")
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = 200
    resp.iter_lines.return_value = body_lines
    resp.read.return_value = b"error"
    mock_client.stream.return_value.__enter__ = MagicMock(return_value=resp)
    mock_client.stream.return_value.__exit__ = MagicMock(return_value=False)

    chunks = list(provider.chat_stream("sys", "usr"))
    deltas = [c.delta for c in chunks]
    assert "Hi" in deltas
    assert " there" in deltas

    final = chunks[-1]
    assert final.finish_reason == "stop"
    assert final.usage == {"prompt_tokens": 10, "completion_tokens": 20}


def test_ollama_streaming_connection_error():
    provider = OllamaProvider(
        name="ollama",
        api_base="http://localhost:11434",
        default_model="llama3.1:8b",
    )
    mock_client = MagicMock(spec=httpx.Client)
    provider._client = mock_client
    mock_client.stream.side_effect = httpx.ConnectError("refused")

    with pytest.raises(LLMProviderError, match="Cannot connect"):
        list(provider.chat_stream("sys", "usr"))


# ---------------------------------------------------------------------------
# LLMClient.execute_task_stream
# ---------------------------------------------------------------------------


def _mock_openai_provider(model: str = "gpt-4o") -> OpenAICompatibleProvider:
    """Create a mock OpenAI provider with a fake HTTP client."""
    provider = OpenAICompatibleProvider(
        name="test-provider",
        api_base="https://api.example.com/v1",
        default_model=model,
        api_key_env="TEST_STREAMING_KEY",
    )
    mock_client = MagicMock(spec=httpx.Client)
    provider._client = mock_client
    return provider


def test_execute_task_stream_yields_chunks_and_parses():
    """execute_task_stream should yield chunks and return parsed JSON."""
    provider = _mock_openai_provider()

    body_lines = [
        'data: {"choices": [{"delta": {"content": "{\\"plan\\": [], \\"result\\": \\"done\\", \\"artifacts\\": []}"}, "finish_reason": null}]}\n',
        'data: {"choices": [{"delta": {}, "finish_reason": "stop"}]}\n',
        "data: [DONE]\n",
    ]
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = 200
    resp.iter_lines.return_value = body_lines
    resp.read.return_value = b"err"
    provider._client.stream.return_value.__enter__ = MagicMock(return_value=resp)
    provider._client.stream.return_value.__exit__ = MagicMock(return_value=False)

    with patch("ai_company.llm.client.ModelRouter") as MockRouter:
        mock_router = MockRouter.return_value
        mock_route = MagicMock()
        mock_route.provider = "test-provider"
        mock_route.model = "gpt-4o"
        mock_route.tier = "standard"
        mock_router.resolve.return_value = mock_route

        mock_tier = MagicMock()
        mock_tier.providers = [MagicMock(provider="test-provider", model="gpt-4o")]
        mock_router.get_tier.return_value = mock_tier

        from ai_company.llm.client import LLMClient

        client = LLMClient.__new__(LLMClient)
        client.router = mock_router
        client._providers = {"test-provider": provider}
        client._circuit_breakers = {}

        chunks = list(client.execute_task_stream("agent1", "do something"))
        assert len(chunks) >= 1
        assert any(c.delta for c in chunks)


def test_execute_task_stream_empty_response_raises():
    """execute_task_stream raises LLMResponseError when JSON parse fails."""
    provider = _mock_openai_provider()

    body_lines = [
        'data: {"choices": [{"delta": {"content": "not json at all"}, "finish_reason": null}]}\n',
        'data: {"choices": [{"delta": {}, "finish_reason": "stop"}]}\n',
        "data: [DONE]\n",
    ]
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = 200
    resp.iter_lines.return_value = body_lines
    resp.read.return_value = b"err"
    provider._client.stream.return_value.__enter__ = MagicMock(return_value=resp)
    provider._client.stream.return_value.__exit__ = MagicMock(return_value=False)

    with patch("ai_company.llm.client.ModelRouter") as MockRouter:
        mock_router = MockRouter.return_value
        mock_route = MagicMock()
        mock_route.provider = "test-provider"
        mock_route.model = "gpt-4o"
        mock_route.tier = "standard"
        mock_router.resolve.return_value = mock_route

        mock_tier = MagicMock()
        mock_tier.providers = [MagicMock(provider="test-provider", model="gpt-4o")]
        mock_router.get_tier.return_value = mock_tier

        from ai_company.llm.client import LLMClient

        client = LLMClient.__new__(LLMClient)
        client.router = mock_router
        client._providers = {"test-provider": provider}
        client._circuit_breakers = {}

        from ai_company.llm.providers.base import LLMResponseError

        with pytest.raises(LLMResponseError):
            list(client.execute_task_stream("agent1", "do something", max_retries=1))
