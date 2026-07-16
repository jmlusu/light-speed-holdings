"""Tests for the LLM abstraction layer."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ai_company.llm.providers.base import (
    ChatResponse,
    LLMProvider,
    LLMProviderError,
    LLMResponseError,
)
from ai_company.llm.providers.openai_compatible import OpenAICompatibleProvider
from ai_company.llm.providers.ollama import OllamaProvider


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


def test_response_error_tracks_attempts():
    err = LLMResponseError("bad json", attempts=5, last_raw="{bad")
    assert err.attempts == 5
    assert err.last_raw == "{bad"


# ── OpenAI Compatible Provider ─────────────────────────────────────


def test_openai_compatible_no_api_key():
    provider = OpenAICompatibleProvider(
        name="test", api_base="http://localhost:9999", default_model="test-model",
        api_key_env="NONEXISTENT_KEY_12345",
    )
    assert not provider.is_available()


def test_openai_compatible_requires_api_key():
    provider = OpenAICompatibleProvider(
        name="test", api_base="http://localhost:9999", default_model="test-model",
    )
    with pytest.raises(LLMProviderError, match="No API key"):
        provider.chat("system", "user")


# ── Ollama Provider ────────────────────────────────────────────────


def test_ollama_not_available_when_offline():
    provider = OllamaProvider(api_base="http://localhost:19999")
    assert not provider.is_available()


def test_ollama_requires_running_server():
    provider = OllamaProvider(api_base="http://localhost:19999")
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

    def test_parse_valid_json(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.chdir(tmp_path)
        _setup_model_files(tmp_path)

        from ai_company.llm.client import LLMClient

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        result = client._parse_response('{"plan": [], "result": "ok", "artifacts": []}')
        assert result is not None
        assert result["result"] == "ok"

    def test_parse_json_in_code_block(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.chdir(tmp_path)
        _setup_model_files(tmp_path)

        from ai_company.llm.client import LLMClient

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        raw = 'Here is the plan:\n```json\n{"plan": [{"tool": "read", "args": {"path": "x.py"}}], "result": "done", "artifacts": []}\n```'
        result = client._parse_response(raw)
        assert result is not None
        assert len(result["plan"]) == 1

    def test_parse_json_embedded_in_text(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.chdir(tmp_path)
        _setup_model_files(tmp_path)

        from ai_company.llm.client import LLMClient

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        raw = 'Sure! {"plan": [], "result": "all done", "artifacts": []} hope that helps!'
        result = client._parse_response(raw)
        assert result is not None
        assert result["result"] == "all done"

    def test_parse_invalid_returns_none(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.chdir(tmp_path)
        _setup_model_files(tmp_path)

        from ai_company.llm.client import LLMClient

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        assert client._parse_response("I'm not sure what to do here.") is None
        assert client._parse_response("```some code```") is None

    def test_execute_task_retries_on_bad_json(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
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
        client._providers = {"opencode": mock_provider, "deepseek": mock_provider, "ollama": mock_provider}

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
        client._providers = {"opencode": mock_provider, "deepseek": mock_provider, "ollama": mock_provider}

        result = client.execute_task("test-agent", "do something", max_retries=5)
        assert result["result"] == "success"
        assert mock_provider.chat.call_count == 3


# ── Helpers ─────────────────────────────────────────────────────────


def _setup_model_files(tmp_path: Path) -> None:
    """Create minimal models.yaml and registry for testing."""
    (tmp_path / "company").mkdir(exist_ok=True)

    models = {
        "providers": {
            "opencode": {"backend": "openai_compatible", "default_model": "big-pickle", "api_base": "https://opencode.ai/api/v1"},
            "deepseek": {"backend": "openai_compatible", "default_model": "deepseek-chat", "api_base": "https://api.deepseek.com/v1"},
            "ollama": {"backend": "ollama", "default_model": "llama3.1:8b", "api_base": "http://localhost:11434"},
        },
        "tiers": {
            "fast": {"description": "Fast", "providers": [{"provider": "opencode", "model": "big-pickle"}]},
            "standard": {"description": "Standard", "providers": [{"provider": "deepseek", "model": "deepseek-chat"}]},
            "premium": {"description": "Premium", "providers": [{"provider": "deepseek", "model": "deepseek-coder"}]},
        },
        "routing": [
            {"agent_type": "Board", "tier": "fast"},
            {"agent_type": "Executive", "tier": "standard"},
            {"agent_type": "Specialist", "tier": "standard"},
        ],
    }
    (tmp_path / "company" / "models.yaml").write_text(
        json.dumps(models), encoding="utf-8"
    )

    registry = [
        {"name": "test-agent", "role": "Test Agent", "type": "Specialist", "department": "Test",
         "reportsTo": "ceo", "directReports": [], "description": "A test agent",
         "tools": ["read", "write"], "permission": "Execute"},
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

# {agent_name.replace('-', ' ').title()}

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
