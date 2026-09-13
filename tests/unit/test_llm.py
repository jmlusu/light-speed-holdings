"""Tests for the LLM abstraction layer."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_company.llm.providers.base import (
    ChatResponse,
    LLMProvider,
    LLMProviderError,
    LLMResponseError,
)
from ai_company.llm.providers.ollama import OllamaProvider
from ai_company.llm.providers.openai_compatible import OpenAICompatibleProvider


@pytest.fixture(autouse=True)
def _no_omniroute_ping(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make LLMClient construction skip the real OmniRoute health ping.

    With ``OMNIROUTE_API_KEY`` set in the environment, ``LLMClient.__init__``
    calls ``httpx.get`` against the gateway on every construction (~4s TCP
    timeout). Failing fast keeps tests hermetic.
    """
    from tests.unit.conftest import patch_local_only_httpx

    patch_local_only_httpx(monkeypatch)


# ── Base types ──────────────────────────────────────────────────────


def test_chat_response_fields():
    resp = ChatResponse(content="hello", model="test", provider="test", usage={"prompt_tokens": 10})
    assert resp.content == "hello"
    assert resp.model == "test"
    assert resp.usage["prompt_tokens"] == 10


def test_provider_error_message():
    err = LLMProviderError("opencode", "timeout", status_code=504)
    assert "[opencode]" in str(err)
    assert err.status_code == 504


def test_provider_error_category_classification():
    from ai_company.llm.providers.base import ProviderErrorCategory

    assert LLMProviderError("p", "x", 429).category == ProviderErrorCategory.RATE_LIMIT
    assert LLMProviderError("p", "x", 401).category == ProviderErrorCategory.AUTH
    assert LLMProviderError("p", "x", 403).category == ProviderErrorCategory.AUTH
    assert LLMProviderError("p", "x", 408).category == ProviderErrorCategory.TIMEOUT
    assert LLMProviderError("p", "x", 503).category == ProviderErrorCategory.SERVER
    assert LLMProviderError("p", "x", 400).category == ProviderErrorCategory.CLIENT
    assert LLMProviderError("p", "x").category == ProviderErrorCategory.UNKNOWN


def test_provider_error_category_message_fallback():
    from ai_company.llm.providers.base import ProviderErrorCategory

    assert LLMProviderError("p", "request timed out").category == ProviderErrorCategory.TIMEOUT
    assert (
        LLMProviderError("p", "Cannot connect to host").category == ProviderErrorCategory.CONNECTION
    )
    assert LLMProviderError("p", "arbitrary message").category == ProviderErrorCategory.UNKNOWN


def test_response_error_tracks_attempts():
    err = LLMResponseError("bad json", attempts=5, last_raw="{bad")
    assert err.attempts == 5
    assert err.last_raw == "{bad"


# ── OpenAI Compatible Provider ─────────────────────────────────────


def test_openai_compatible_no_api_key():
    provider = OpenAICompatibleProvider(
        name="test",
        api_base="http://localhost:9999",
        default_model="test-model",
        api_key_env="NONEXISTENT_KEY_12345",
    )
    assert not provider.is_available()


def test_openai_compatible_requires_api_key():
    provider = OpenAICompatibleProvider(
        name="test",
        api_base="http://localhost:9999",
        default_model="test-model",
    )
    with pytest.raises(LLMProviderError, match="No API key"):
        provider.chat("system", "user")


# ── Ollama Provider ────────────────────────────────────────────────


def test_ollama_not_available_when_offline(monkeypatch: pytest.MonkeyPatch):
    import httpx

    provider = OllamaProvider(api_base="http://localhost:19999")

    def _refuse(*args: object, **kwargs: object) -> None:
        raise httpx.ConnectError("Connection refused")

    monkeypatch.setattr(provider._client, "get", _refuse)
    assert not provider.is_available()


def test_ollama_requires_running_server(monkeypatch: pytest.MonkeyPatch):
    import httpx

    provider = OllamaProvider(api_base="http://localhost:19999")

    def _refuse(*args: object, **kwargs: object) -> None:
        raise httpx.ConnectError("Connection refused")

    monkeypatch.setattr(provider._client, "post", _refuse)
    with pytest.raises(LLMProviderError, match="Cannot connect"):
        provider.chat("system", "user")


# ── LLM Client ─────────────────────────────────────────────────────


class TestLLMClient:
    def test_init_loads_providers(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.chdir(tmp_path)
        _setup_model_files(tmp_path)

        from ai_company.llm.client import LLMClient

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )
        assert "opencode" in client._providers
        assert "deepseek" in client._providers
        assert "ollama" in client._providers

    def test_parse_valid_json(self):
        from ai_company.llm.json_parser import parse_llm_json

        result = parse_llm_json('{"plan": [], "result": "ok", "artifacts": []}')
        assert result is not None
        assert result["result"] == "ok"

    def test_parse_json_in_code_block(self):
        from ai_company.llm.json_parser import parse_llm_json

        raw = 'Here is the plan:\n```json\n{"plan": [{"tool": "read", "args": {"path": "x.py"}}], "result": "done", "artifacts": []}\n```'
        result = parse_llm_json(raw)
        assert result is not None
        assert len(result["plan"]) == 1

    def test_parse_json_embedded_in_text(self):
        from ai_company.llm.json_parser import parse_llm_json

        raw = 'Sure! {"plan": [], "result": "all done", "artifacts": []} hope that helps!'
        result = parse_llm_json(raw)
        assert result is not None
        assert result["result"] == "all done"

    def test_parse_invalid_returns_none(self):
        from ai_company.llm.json_parser import parse_llm_json

        assert parse_llm_json("I'm not sure what to do here.") is None
        assert parse_llm_json("```some code```") is None

    def test_execute_task_retries_on_bad_json(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.chdir(tmp_path)
        _setup_model_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        from ai_company.llm.client import LLMClient

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        # Mock all providers to return invalid JSON
        mock_provider = MagicMock(spec=LLMProvider)
        mock_provider.is_available.return_value = True
        mock_provider.chat.return_value = ChatResponse(
            content="not json at all", model="test", provider="mock"
        )
        client._providers = {
            "opencode": mock_provider,
            "deepseek": mock_provider,
            "ollama": mock_provider,
        }

        with pytest.raises(LLMResponseError, match="5 attempts"):
            client.execute_task("test-agent", "do something", max_retries=5)

        # Should have been called 5 times (once per retry)
        assert mock_provider.chat.call_count == 5

    def test_execute_task_success_on_retry(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.chdir(tmp_path)
        _setup_model_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        from ai_company.llm.client import LLMClient

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        good_response = json.dumps({"plan": [], "result": "success", "artifacts": []})
        mock_provider = MagicMock(spec=LLMProvider)
        mock_provider.is_available.return_value = True
        # Fail first 2 times, succeed on 3rd
        mock_provider.chat.side_effect = [
            ChatResponse(content="bad", model="test", provider="mock"),
            ChatResponse(content="also bad", model="test", provider="mock"),
            ChatResponse(content=good_response, model="test", provider="mock"),
        ]
        client._providers = {
            "opencode": mock_provider,
            "deepseek": mock_provider,
            "ollama": mock_provider,
        }

        result = client.execute_task("test-agent", "do something", max_retries=5)
        assert result["result"] == "success"
        assert mock_provider.chat.call_count == 3

    def test_execute_task_retries_cycle_providers(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """GAP-019: a retry after invalid JSON moves to the next provider, not provider 0 again."""
        from types import SimpleNamespace

        monkeypatch.chdir(tmp_path)
        _setup_model_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        from ai_company.llm.client import LLMClient

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        good_response = json.dumps({"plan": [], "result": "success", "artifacts": []})
        bad_provider = MagicMock(spec=LLMProvider)
        bad_provider.is_available.return_value = True
        bad_provider.chat.return_value = ChatResponse(
            content="not json", model="big-pickle", provider="opencode"
        )
        good_provider = MagicMock(spec=LLMProvider)
        good_provider.is_available.return_value = True
        good_provider.chat.return_value = ChatResponse(
            content=good_response, model="deepseek-chat", provider="deepseek"
        )
        client._providers = {
            "opencode": bad_provider,
            "deepseek": good_provider,
            "ollama": bad_provider,
        }

        client.router.resolve = MagicMock(
            return_value=SimpleNamespace(
                tier="standard", provider="deepseek", model="deepseek-chat"
            )
        )
        client.router.get_tier = MagicMock(
            return_value=SimpleNamespace(
                providers=[
                    SimpleNamespace(provider="opencode", model="big-pickle"),
                    SimpleNamespace(provider="deepseek", model="deepseek-chat"),
                    SimpleNamespace(provider="ollama", model="llama3.1-8b-32k"),
                ]
            )
        )

        result = client.execute_task("test-agent", "do something", max_retries=5)

        assert result["result"] == "success"
        # Attempt 0 hit provider 0 (opencode); the retry cycled to provider 1 (deepseek)
        assert bad_provider.chat.call_count == 1
        assert good_provider.chat.call_count == 1

    def test_execute_task_round_robin_distribution(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """GAP-019: across N retries, calls are distributed evenly across the chain."""
        from types import SimpleNamespace

        monkeypatch.chdir(tmp_path)
        _setup_model_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        from ai_company.llm.client import LLMClient

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        mocks = {pid: MagicMock(spec=LLMProvider) for pid in ("opencode", "deepseek", "ollama")}
        for provider in mocks.values():
            provider.is_available.return_value = True
            provider.chat.return_value = ChatResponse(
                content="not json", model="test", provider="mock"
            )
        client._providers = mocks

        client.router.resolve = MagicMock(
            return_value=SimpleNamespace(
                tier="standard", provider="deepseek", model="deepseek-chat"
            )
        )
        client.router.get_tier = MagicMock(
            return_value=SimpleNamespace(
                providers=[
                    SimpleNamespace(provider="opencode", model="big-pickle"),
                    SimpleNamespace(provider="deepseek", model="deepseek-chat"),
                    SimpleNamespace(provider="ollama", model="llama3.1-8b-32k"),
                ]
            )
        )

        with pytest.raises(LLMResponseError, match="6 attempts"):
            client.execute_task("test-agent", "do something", max_retries=6)

        # 6 attempts over a 3-provider chain == 2 calls per provider (round-robin)
        for provider in mocks.values():
            assert provider.chat.call_count == 2

    def test_execute_task_breaker_skips_open_provider(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """Once the circuit opens, the provider is skipped on later attempts."""
        from types import SimpleNamespace

        monkeypatch.chdir(tmp_path)
        _setup_model_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        from ai_company.llm.client import LLMClient

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        failing = MagicMock(spec=LLMProvider)
        failing.is_available.return_value = True
        failing.chat.side_effect = LLMProviderError("opencode", "rate limited", status_code=429)
        client._providers = {
            "opencode": failing,
            "deepseek": failing,
            "ollama": failing,
        }

        from ai_company.llm.circuit_breaker import CircuitBreaker

        # Trip each provider's breaker after a single failure so the skip
        # behaviour is observable within a 5-attempt run.
        client._circuit_breakers = {
            pid: CircuitBreaker(failure_threshold=1) for pid in client._providers
        }

        client.router.resolve = MagicMock(
            return_value=SimpleNamespace(
                tier="standard", provider="deepseek", model="deepseek-chat"
            )
        )
        client.router.get_tier = MagicMock(
            return_value=SimpleNamespace(
                providers=[
                    SimpleNamespace(provider="opencode", model="big-pickle"),
                    SimpleNamespace(provider="deepseek", model="deepseek-chat"),
                    SimpleNamespace(provider="ollama", model="llama3.1-8b-32k"),
                ]
            )
        )

        with pytest.raises(LLMResponseError):
            client.execute_task("test-agent", "do something", max_retries=5)

        # One failure per provider opens each breaker; the remaining two
        # attempts skip the providers entirely.
        assert failing.chat.call_count == 3
        for pid in client._circuit_breakers:
            assert not client._circuit_breakers[pid].is_available

    def test_execute_task_auth_failure_does_not_open_breaker(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """Auth failures don't count toward the breaker threshold."""
        from types import SimpleNamespace

        monkeypatch.chdir(tmp_path)
        _setup_model_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        from ai_company.llm.client import LLMClient

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        failing = MagicMock(spec=LLMProvider)
        failing.is_available.return_value = True
        failing.chat.side_effect = LLMProviderError("opencode", "bad key", status_code=401)
        client._providers = {
            "opencode": failing,
            "deepseek": failing,
            "ollama": failing,
        }

        from ai_company.llm.circuit_breaker import CircuitBreaker

        # Threshold of 1 — even a single counted failure would open the
        # breaker, so the auth-exemption path is what keeps it closed.
        client._circuit_breakers = {
            pid: CircuitBreaker(failure_threshold=1) for pid in client._providers
        }

        client.router.resolve = MagicMock(
            return_value=SimpleNamespace(
                tier="standard", provider="deepseek", model="deepseek-chat"
            )
        )
        client.router.get_tier = MagicMock(
            return_value=SimpleNamespace(
                providers=[
                    SimpleNamespace(provider="opencode", model="big-pickle"),
                    SimpleNamespace(provider="deepseek", model="deepseek-chat"),
                    SimpleNamespace(provider="ollama", model="llama3.1-8b-32k"),
                ]
            )
        )

        with pytest.raises(LLMResponseError):
            client.execute_task("test-agent", "do something", max_retries=5)

        # Every attempt still reaches the provider; breaker stays closed.
        assert failing.chat.call_count == 5
        for pid in client._circuit_breakers:
            assert client._circuit_breakers[pid].is_available

    def test_execute_task_limiter_skips_limited_provider(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """A token-bucket-limited provider is skipped when the bucket is empty."""
        from types import SimpleNamespace

        monkeypatch.chdir(tmp_path)
        _setup_model_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        from ai_company.llm.client import LLMClient
        from ai_company.llm.token_bucket import TokenBucket

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
            limiter_timeout=0.0,
        )

        good_response = json.dumps({"plan": [], "result": "success", "artifacts": []})
        limited = MagicMock(spec=LLMProvider)
        limited.is_available.return_value = True
        limited.chat.return_value = ChatResponse(
            content="should not be called", model="big-pickle", provider="opencode"
        )
        good = MagicMock(spec=LLMProvider)
        good.is_available.return_value = True
        good.chat.return_value = ChatResponse(
            content=good_response, model="deepseek-chat", provider="deepseek"
        )
        client._providers = {
            "opencode": limited,
            "deepseek": good,
            "ollama": good,
        }
        client._limiters = {
            "opencode": TokenBucket(rate=0.0, capacity=0),
        }

        client.router.resolve = MagicMock(
            return_value=SimpleNamespace(
                tier="standard", provider="deepseek", model="deepseek-chat"
            )
        )
        client.router.get_tier = MagicMock(
            return_value=SimpleNamespace(
                providers=[
                    SimpleNamespace(provider="opencode", model="big-pickle"),
                    SimpleNamespace(provider="deepseek", model="deepseek-chat"),
                ]
            )
        )

        result = client.execute_task("test-agent", "do something", max_retries=3)

        # Empty bucket -> opencode never called; deepseek satisfies the task.
        assert result["result"] == "success"
        assert limited.chat.call_count == 0
        assert good.chat.call_count == 1

    def test_execute_task_limiter_refills_between_attempts(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """A provider is reachable again after the bucket refills."""
        from types import SimpleNamespace

        monkeypatch.chdir(tmp_path)
        _setup_model_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        from ai_company.llm.client import LLMClient
        from ai_company.llm.token_bucket import TokenBucket

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
            limiter_timeout=5.0,
        )

        good_response = json.dumps({"plan": [], "result": "success", "artifacts": []})
        provider = MagicMock(spec=LLMProvider)
        provider.is_available.return_value = True
        provider.chat.return_value = ChatResponse(
            content=good_response, model="big-pickle", provider="opencode"
        )
        client._providers = {"opencode": provider}
        client._limiters = {"opencode": TokenBucket(rate=100.0, capacity=1)}

        client.router.resolve = MagicMock(
            return_value=SimpleNamespace(tier="standard", provider="opencode", model="big-pickle")
        )
        client.router.get_tier = MagicMock(
            return_value=SimpleNamespace(
                providers=[SimpleNamespace(provider="opencode", model="big-pickle")]
            )
        )

        assert (
            client.execute_task("test-agent", "do something", max_retries=3)["result"] == "success"
        )
        # Bucket refilled between the acquire and the call, so it succeeds.
        assert provider.chat.call_count == 1


# ── Helpers ─────────────────────────────────────────────────────────


def _setup_model_files(tmp_path: Path) -> None:
    """Create minimal models.yaml and registry for testing."""
    (tmp_path / "company").mkdir(exist_ok=True)

    models = {
        "providers": {
            "opencode": {
                "backend": "openai_compatible",
                "default_model": "big-pickle",
                "api_base": "https://opencode.ai/api/v1",
            },
            "deepseek": {
                "backend": "openai_compatible",
                "default_model": "deepseek-chat",
                "api_base": "https://api.deepseek.com/v1",
            },
            "ollama": {
                "backend": "ollama",
                "default_model": "llama3.1-8b-32k",
                "api_base": "http://localhost:11434",
            },
        },
        "tiers": {
            "fast": {
                "description": "Fast",
                "providers": [{"provider": "opencode", "model": "big-pickle"}],
            },
            "standard": {
                "description": "Standard",
                "providers": [{"provider": "deepseek", "model": "deepseek-chat"}],
            },
            "premium": {
                "description": "Premium",
                "providers": [{"provider": "deepseek", "model": "deepseek-coder"}],
            },
        },
        "routing": [
            {"agent_type": "Board", "tier": "fast"},
            {"agent_type": "Executive", "tier": "standard"},
            {"agent_type": "Specialist", "tier": "standard"},
        ],
    }
    (tmp_path / "company" / "models.yaml").write_text(json.dumps(models), encoding="utf-8")

    registry = [
        {
            "name": "test-agent",
            "role": "Test Agent",
            "type": "Specialist",
            "department": "Test",
            "reportsTo": "ceo",
            "directReports": [],
            "description": "A test agent",
            "tools": ["read", "write"],
            "permission": "Execute",
        },
    ]
    (tmp_path / "company" / "agent-registry.json").write_text(
        json.dumps(registry), encoding="utf-8"
    )


def _create_agent_spec(tmp_path: Path, agent_name: str) -> None:
    """Create a minimal agent spec card."""
    agents_dir = tmp_path / ".opencode" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    spec = f"""---
name: {agent_name}
description: A test agent for unit tests
tools: ["read", "write", "execute"]
mode: subagent
permission:
  read: allow
  write: allow
  bash: allow
---

# {agent_name.replace("-", " ").title()}

## Identity

Type: Specialist

Department: Test

Reports To: ceo

---

## Mission

Test things thoroughly.

---

## Responsibilities

- Write tests
- Review code
- Fix bugs

---

## Operating Guidelines

Be thorough. Test everything.

---

## Operating Principles

- Evidence over opinion
- Automate repetitive work
"""
    (agents_dir / f"{agent_name}.md").write_text(spec, encoding="utf-8")
