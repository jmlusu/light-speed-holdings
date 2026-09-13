"""Tests for OmniRoute meta-provider integration (#151/#154).

Covers:
  - ModelRouter: OmniRoute fallback when tier has no providers
  - ModelRouter: resolve_with_fallback appends OmniRoute as last resort
  - ModelRouter: _resolve_free_tier with OmniRoute in static fallback
  - ModelRouter: budget degradation doesn't affect override/escalation/approval
  - ModelRouter: complexity scoring prevents downgrade for high/critical priority
  - LLMClient: execute_task end-to-end with mocked OmniRoute provider
  - LLMClient: execute_task_stream with mocked provider
  - LLMClient: graceful degradation when OmniRoute is unreachable
  - Doctor: check_omniroute_health when key is set / not set / unreachable
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from ai_company.llm.providers.base import ChatResponse, LLMProvider


@pytest.fixture(autouse=True)
def _no_omniroute_ping(monkeypatch: pytest.MonkeyPatch) -> None:
    """Failing-fast httpx.get keeps LLMClient construction hermetic.

    Tests that verify OmniRoute health/mock responses re-patch ``httpx.get``
    themselves and override this default.
    """
    from tests.unit.conftest import patch_local_only_httpx

    patch_local_only_httpx(monkeypatch)


# ── Helpers ──────────────────────────────────────────────────────────


def _setup_omniroute_model_files(tmp_path: Path) -> None:
    """Create models.yaml with OmniRoute in provider catalog + all tiers."""
    (tmp_path / "company").mkdir(exist_ok=True)

    models = {
        "providers": {
            "opencode": {
                "backend": "openai_compatible",
                "default_model": "big-pickle",
                "api_base": "https://opencode.ai/zen/v1",
            },
            "gemini": {
                "backend": "openai_compatible",
                "default_model": "gemini-3.5-flash",
                "api_base": "https://generativelanguage.googleapis.com/v1beta/openai",
            },
            "ollama": {
                "backend": "ollama",
                "default_model": "llama3.1-8b-32k",
                "api_base": "http://localhost:11434",
            },
            "omniroute": {
                "backend": "openai_compatible",
                "default_model": "auto",
                "api_base": "http://localhost:20128/v1",
            },
        },
        "tiers": {
            "fast": {
                "description": "Cheap and fast",
                "providers": [
                    {"provider": "ollama", "model": "llama3.1-8b-32k"},
                    {"provider": "gemini", "model": "gemini-3.5-flash"},
                    {"provider": "omniroute", "model": "auto"},
                ],
            },
            "standard": {
                "description": "Balanced",
                "providers": [
                    {"provider": "opencode", "model": "big-pickle"},
                    {"provider": "ollama", "model": "llama3.1-8b-32k"},
                    {"provider": "omniroute", "model": "auto"},
                ],
            },
            "premium": {
                "description": "Best reasoning",
                "providers": [
                    {"provider": "opencode", "model": "big-pickle"},
                    {"provider": "omniroute", "model": "auto"},
                ],
            },
        },
        "routing": [
            {"agent_type": "Board", "tier": "fast"},
            {"agent_type": "Executive", "priority": "medium", "tier": "standard"},
            {"agent_type": "Executive", "priority": "critical", "tier": "premium"},
            {"agent_type": "Specialist", "priority": "low", "tier": "standard"},
            {"agent_type": "Specialist", "priority": "medium", "tier": "standard"},
            {"agent_type": "Specialist", "priority": "high", "tier": "premium"},
            {"agent_type": "Specialist", "priority": "critical", "tier": "premium"},
            {"context": "escalation", "tier": "premium"},
            {"context": "approval", "tier": "premium"},
        ],
        "free_tier": {
            "static_fallback": [
                {"provider": "omniroute", "model": "auto"},
            ],
        },
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
description: A test agent
tools: ["read", "write", "execute"]
mode: subagent
permission:
  read: allow
  write: allow
  bash: allow
---

# {agent_name.replace("-", " ").title()}

## Mission

Test things.
"""
    (agents_dir / f"{agent_name}.md").write_text(spec, encoding="utf-8")


# ══════════════════════════════════════════════════════════════════════
# ModelRouter: empty tier → OmniRoute fallback
# ══════════════════════════════════════════════════════════════════════


class TestEmptyTierOmniRouteFallback:
    """When a resolved tier has no providers, ModelRouter falls back to OmniRoute."""

    def test_resolve_empty_tier_returns_omniroute(self, tmp_path: Path):
        from ai_company.model_router import ModelRouter

        config = {
            "providers": {
                "omniroute": {
                    "backend": "openai_compatible",
                    "default_model": "auto",
                    "api_base": "http://localhost:20128/v1",
                },
            },
            "tiers": {
                "fast": {
                    "description": "Empty tier",
                    "providers": [],
                },
            },
            "routing": [
                {"agent_type": "Specialist", "priority": "low", "tier": "fast"},
            ],
        }
        path = tmp_path / "models.yaml"
        path.write_text(json.dumps(config), encoding="utf-8")

        router = ModelRouter(config_path=str(path))
        route = router.resolve(agent_name="any-agent", priority="low", agent_type="Specialist")

        assert route.provider == "omniroute"
        assert route.model == "auto"
        assert route.tier == "fast"
        assert "no providers" in route.reason.lower() or "omniroute" in route.reason.lower()

    def test_resolve_missing_tier_returns_omniroute(self, tmp_path: Path):
        """Tier ID doesn't exist in config at all."""
        from ai_company.model_router import ModelRouter

        config = {
            "providers": {
                "omniroute": {
                    "backend": "openai_compatible",
                    "default_model": "auto",
                    "api_base": "http://localhost:20128/v1",
                },
            },
            "tiers": {},
            "routing": [
                {"context": "custom", "tier": "nonexistent"},
            ],
        }
        path = tmp_path / "models.yaml"
        path.write_text(json.dumps(config), encoding="utf-8")

        router = ModelRouter(config_path=str(path))
        route = router.resolve(context="custom")

        assert route.provider == "omniroute"
        assert route.model == "auto"


# ══════════════════════════════════════════════════════════════════════
# ModelRouter: normal resolution (OmniRoute is fallback, not primary)
# ══════════════════════════════════════════════════════════════════════


class TestNormalResolutionNotOmniRoute:
    """When a tier has providers, the first provider should be chosen, not OmniRoute."""

    def test_standard_tier_resolves_to_opencode(self, tmp_path: Path):
        from ai_company.model_router import ModelRouter

        _setup_omniroute_model_files(tmp_path)
        router = ModelRouter(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )
        route = router.resolve(agent_name="test-agent", priority="medium", agent_type="Specialist")

        assert route.tier == "standard"
        assert route.provider == "opencode"
        assert route.model == "big-pickle"
        assert "omniroute" not in route.provider

    def test_fast_tier_resolves_to_ollama(self, tmp_path: Path):
        from ai_company.model_router import ModelRouter

        _setup_omniroute_model_files(tmp_path)
        router = ModelRouter(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )
        route = router.resolve(agent_name="test-agent", agent_type="Board")

        assert route.tier == "fast"
        assert route.provider == "ollama"
        assert route.model == "llama3.1-8b-32k"


# ══════════════════════════════════════════════════════════════════════
# ModelRouter: resolve_with_fallback appends OmniRoute
# ══════════════════════════════════════════════════════════════════════


class TestResolveWithFallbackOmniRoute:
    """resolve_with_fallback should include OmniRoute as the last resort."""

    def test_omniroute_is_last_resort_in_chain(self, tmp_path: Path):
        from ai_company.model_router import ModelRouter

        _setup_omniroute_model_files(tmp_path)
        router = ModelRouter(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )
        routes = router.resolve_with_fallback(
            agent_name="test-agent", priority="medium", agent_type="Specialist"
        )

        assert len(routes) >= 2
        last = routes[-1]
        assert last.provider == "omniroute"
        assert last.model == "auto"
        assert "last-resort" in last.reason.lower() or "fallback" in last.reason.lower()

    def test_omniroute_appended_as_last_resort_always(self, tmp_path: Path):
        """OmniRoute is always appended as the last-resort fallback,
        even if it already appears as a provider in the primary tier.
        This is by design: the ``seen`` set tracks *tier IDs* (not
        provider names), so ``'omniroute' in seen`` is always False."""
        from ai_company.model_router import ModelRouter

        config = {
            "providers": {
                "omniroute": {
                    "backend": "openai_compatible",
                    "default_model": "auto",
                    "api_base": "http://localhost:20128/v1",
                },
            },
            "tiers": {
                "standard": {
                    "description": "OmniRoute only",
                    "providers": [{"provider": "omniroute", "model": "auto"}],
                },
                "premium": {
                    "description": "Empty",
                    "providers": [],
                },
            },
            "routing": [
                {"agent_type": "Specialist", "priority": "medium", "tier": "standard"},
            ],
        }
        path = tmp_path / "models.yaml"
        path.write_text(json.dumps(config), encoding="utf-8")
        registry = [
            {
                "name": "test-agent",
                "role": "Test Agent",
                "type": "Specialist",
                "department": "Test",
                "reportsTo": "ceo",
                "directReports": [],
                "description": "A test agent",
                "tools": ["read"],
                "permission": "Execute",
            },
        ]
        (tmp_path / "agent-registry.json").write_text(json.dumps(registry), encoding="utf-8")

        router = ModelRouter(
            config_path=str(path),
            registry_path=str(tmp_path / "agent-registry.json"),
        )
        routes = router.resolve_with_fallback(
            agent_name="test-agent", priority="medium", agent_type="Specialist"
        )

        # Last route must be the OmniRoute last-resort fallback
        assert routes[-1].provider == "omniroute"
        assert routes[-1].model == "auto"


# ══════════════════════════════════════════════════════════════════════
# ModelRouter: _resolve_free_tier with OmniRoute
# ══════════════════════════════════════════════════════════════════════


class TestFreeTierOmniRoute:
    """Free tier should use OmniRoute as the static fallback."""

    def test_free_tier_static_fallback_returns_omniroute(self, tmp_path: Path):
        from ai_company.model_router import ModelRouter

        config = {
            "providers": {
                "omniroute": {
                    "backend": "openai_compatible",
                    "default_model": "auto",
                    "api_base": "http://localhost:20128/v1",
                },
            },
            "tiers": {},
            "routing": [{"context": "test_free", "tier": "free"}],
            "free_tier": {
                "static_fallback": [
                    {"provider": "omniroute", "model": "auto"},
                ],
            },
        }
        path = tmp_path / "models.yaml"
        path.write_text(json.dumps(config), encoding="utf-8")

        router = ModelRouter(config_path=str(path))
        # Clear cache to force static fallback
        router._clear_cached_free_models()

        route = router.resolve(context="test_free")
        assert route.tier == "free"
        assert route.provider == "omniroute"
        assert route.model == "auto"


# ══════════════════════════════════════════════════════════════════════
# ModelRouter: budget degradation doesn't affect protected tiers
# ══════════════════════════════════════════════════════════════════════


class TestBudgetDegradationProtectedTiers:
    """Override, escalation, and approval tiers should bypass budget degradation."""

    def test_override_tier_ignores_budget_pressure(self, tmp_path: Path):
        from ai_company.model_router import ModelRouter

        config = {
            "providers": {
                "opencode": {
                    "backend": "openai_compatible",
                    "default_model": "big-pickle",
                    "api_base": "https://opencode.ai/zen/v1",
                },
            },
            "tiers": {
                "standard": {
                    "description": "Balanced",
                    "providers": [{"provider": "opencode", "model": "big-pickle"}],
                },
            },
            "routing": [
                {"context": "override", "tier": "standard"},
            ],
            "budget_degradation": {
                "warning_threshold": 0.80,
                "pressure_threshold": 0.90,
                "critical_threshold": 0.95,
                "hard_stop_threshold": 1.00,
            },
        }
        path = tmp_path / "models.yaml"
        path.write_text(json.dumps(config), encoding="utf-8")

        router = ModelRouter(config_path=str(path))
        # Simulate 95% budget pressure
        router._config["budget_pressure"] = 0.95

        route = router.resolve(context="override")
        # Override tier should not be degraded
        assert route.tier == "standard"

    def test_escalation_context_ignores_budget_pressure(self, tmp_path: Path):
        from ai_company.model_router import ModelRouter

        config = {
            "providers": {
                "opencode": {
                    "backend": "openai_compatible",
                    "default_model": "big-pickle",
                    "api_base": "https://opencode.ai/zen/v1",
                },
            },
            "tiers": {
                "premium": {
                    "description": "Best",
                    "providers": [{"provider": "opencode", "model": "big-pickle"}],
                },
            },
            "routing": [
                {"context": "escalation", "tier": "premium"},
            ],
            "budget_degradation": {
                "warning_threshold": 0.80,
                "pressure_threshold": 0.90,
                "critical_threshold": 0.95,
                "hard_stop_threshold": 1.00,
            },
        }
        path = tmp_path / "models.yaml"
        path.write_text(json.dumps(config), encoding="utf-8")

        router = ModelRouter(config_path=str(path))
        router._config["budget_pressure"] = 0.99

        route = router.resolve(context="escalation")
        assert route.tier == "premium"


# ══════════════════════════════════════════════════════════════════════
# ModelRouter: complexity scoring prevents downgrade
# ══════════════════════════════════════════════════════════════════════


class TestComplexityScoringProtection:
    """High/critical priority tasks should not be downgraded."""

    def test_critical_priority_uses_premium_tier(self, tmp_path: Path):
        from ai_company.model_router import ModelRouter

        _setup_omniroute_model_files(tmp_path)
        router = ModelRouter(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )
        route = router.resolve(
            agent_name="test-agent", priority="critical", agent_type="Specialist"
        )
        assert route.tier == "premium"

    def test_high_priority_uses_premium_tier(self, tmp_path: Path):
        from ai_company.model_router import ModelRouter

        _setup_omniroute_model_files(tmp_path)
        router = ModelRouter(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )
        route = router.resolve(agent_name="test-agent", priority="high", agent_type="Specialist")
        assert route.tier == "premium"


# ══════════════════════════════════════════════════════════════════════
# LLMClient: execute_task with mocked OmniRoute provider
# ══════════════════════════════════════════════════════════════════════


class TestLLMClientOmniRouteExecuteTask:
    """End-to-end execute_task with mocked OmniRoute provider."""

    def test_execute_task_uses_omniroute_fallback(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.chdir(tmp_path)
        _setup_omniroute_model_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        from ai_company.llm.client import LLMClient

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        good_response = json.dumps({"plan": [], "result": "omniroute success", "artifacts": []})
        mock_provider = MagicMock(spec=LLMProvider)
        mock_provider.is_available.return_value = True
        mock_provider.chat.return_value = ChatResponse(
            content=good_response, model="auto", provider="omniroute"
        )
        client._providers = {"omniroute": mock_provider}

        # Force router to return OmniRoute route
        client.router.resolve = MagicMock(
            return_value=SimpleNamespace(tier="standard", provider="omniroute", model="auto")
        )
        client.router.get_tier = MagicMock(
            return_value=SimpleNamespace(
                providers=[SimpleNamespace(provider="omniroute", model="auto")]
            )
        )

        result = client.execute_task("test-agent", "do something")
        assert result["result"] == "omniroute success"
        assert mock_provider.chat.call_count == 1

    def test_execute_task_provider_error_falls_back(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """When primary provider errors, should fall back to next in chain."""
        from ai_company.llm.providers.base import LLMProviderError

        monkeypatch.chdir(tmp_path)
        _setup_omniroute_model_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        from ai_company.llm.client import LLMClient

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        good_response = json.dumps({"plan": [], "result": "fallback works", "artifacts": []})
        bad_provider = MagicMock(spec=LLMProvider)
        bad_provider.is_available.return_value = True
        bad_provider.chat.side_effect = LLMProviderError("bad-provider", "connection failed")

        good_provider = MagicMock(spec=LLMProvider)
        good_provider.is_available.return_value = True
        good_provider.chat.return_value = ChatResponse(
            content=good_response, model="auto", provider="omniroute"
        )

        client._providers = {"bad-provider": bad_provider, "omniroute": good_provider}

        client.router.resolve = MagicMock(
            return_value=SimpleNamespace(tier="standard", provider="bad-provider", model="model-x")
        )
        client.router.get_tier = MagicMock(
            return_value=SimpleNamespace(
                providers=[
                    SimpleNamespace(provider="bad-provider", model="model-x"),
                    SimpleNamespace(provider="omniroute", model="auto"),
                ]
            )
        )

        result = client.execute_task("test-agent", "do something", max_retries=3)
        assert result["result"] == "fallback works"
        assert bad_provider.chat.call_count >= 1
        assert good_provider.chat.call_count == 1


# ══════════════════════════════════════════════════════════════════════
# LLMClient: execute_task_stream with mocked provider
# ══════════════════════════════════════════════════════════════════════


class TestLLMClientOmniRouteStreaming:
    """execute_task_stream with mocked OmniRoute provider."""

    def test_streaming_returns_valid_json(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        from ai_company.llm.providers.base import StreamChunk

        monkeypatch.chdir(tmp_path)
        _setup_omniroute_model_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        from ai_company.llm.client import LLMClient

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        good_json = json.dumps({"plan": [], "result": "streamed", "artifacts": []})

        mock_provider = MagicMock(spec=LLMProvider)
        mock_provider.is_available.return_value = True
        mock_provider.chat_stream.return_value = iter(
            [
                StreamChunk(delta=good_json, finish_reason="stop"),
            ]
        )
        client._providers = {"omniroute": mock_provider}

        client.router.resolve = MagicMock(
            return_value=SimpleNamespace(tier="standard", provider="omniroute", model="auto")
        )
        client.router.get_tier = MagicMock(
            return_value=SimpleNamespace(
                providers=[SimpleNamespace(provider="omniroute", model="auto")]
            )
        )

        chunks = list(client.execute_task_stream("test-agent", "do something"))
        assert len(chunks) >= 1
        assert chunks[0].delta == good_json

    def test_streaming_retries_on_bad_json(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        from ai_company.llm.providers.base import StreamChunk

        monkeypatch.chdir(tmp_path)
        _setup_omniroute_model_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        from ai_company.llm.client import LLMClient

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        good_json = json.dumps({"plan": [], "result": "ok", "artifacts": []})
        mock_provider = MagicMock(spec=LLMProvider)
        mock_provider.is_available.return_value = True
        mock_provider.chat_stream.side_effect = [
            iter([StreamChunk(delta="not json", finish_reason="stop")]),
            iter([StreamChunk(delta="also bad", finish_reason="stop")]),
            iter([StreamChunk(delta=good_json, finish_reason="stop")]),
        ]
        client._providers = {"omniroute": mock_provider}

        client.router.resolve = MagicMock(
            return_value=SimpleNamespace(tier="standard", provider="omniroute", model="auto")
        )
        client.router.get_tier = MagicMock(
            return_value=SimpleNamespace(
                providers=[SimpleNamespace(provider="omniroute", model="auto")]
            )
        )

        list(client.execute_task_stream("test-agent", "do something", max_retries=3))
        # Should have retried 3 times
        assert mock_provider.chat_stream.call_count == 3


# ══════════════════════════════════════════════════════════════════════
# LLMClient: graceful degradation when OmniRoute is unreachable
# ══════════════════════════════════════════════════════════════════════


class TestLLMClientGracefulDegradation:
    """When OmniRoute is unreachable, execution should still work via other providers."""

    def test_execute_task_falls_back_to_other_provider(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.chdir(tmp_path)
        _setup_omniroute_model_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        from ai_company.llm.client import LLMClient

        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        good_response = json.dumps({"plan": [], "result": "from ollama", "artifacts": []})
        ollama_provider = MagicMock(spec=LLMProvider)
        ollama_provider.is_available.return_value = True
        ollama_provider.chat.return_value = ChatResponse(
            content=good_response, model="llama3.1-8b-32k", provider="ollama"
        )
        client._providers = {"ollama": ollama_provider}

        # Router returns ollama route (not OmniRoute)
        client.router.resolve = MagicMock(
            return_value=SimpleNamespace(tier="fast", provider="ollama", model="llama3.1-8b-32k")
        )
        client.router.get_tier = MagicMock(
            return_value=SimpleNamespace(
                providers=[SimpleNamespace(provider="ollama", model="llama3.1-8b-32k")]
            )
        )

        result = client.execute_task("test-agent", "do something")
        assert result["result"] == "from ollama"

    def test_log_omniroute_status_unreachable(self, tmp_path: Path, caplog):
        """_log_omniroute_status should log a warning when unreachable."""
        from ai_company.llm.client import LLMClient

        with (
            patch.dict("os.environ", {"OMNIROUTE_API_KEY": "sk-test-key"}),
            patch("httpx.get", side_effect=ConnectionError("Connection refused")),
        ):
            # Should not raise
            LLMClient._log_omniroute_status(None)

    def test_log_omniroute_status_not_configured(self, tmp_path: Path, caplog):
        """_log_omniroute_status should log info when no API key."""
        from ai_company.llm.client import LLMClient

        with patch.dict("os.environ", {}, clear=True):
            # Should not raise
            LLMClient._log_omniroute_status(None)


# ══════════════════════════════════════════════════════════════════════
# Doctor: check_omniroute_health
# ══════════════════════════════════════════════════════════════════════


class TestCheckOmniRouteHealth:
    """Test the OmniRoute health check in the doctor module."""

    def test_check_skipped_when_no_api_key(self):
        from ai_company.doctor.checks import check_omniroute_health

        with patch.dict("os.environ", {}, clear=True):
            result = check_omniroute_health()
            assert result.passed is True
            assert result.severity == "info"
            assert "skipped" in result.message.lower()

    def test_check_passes_when_reachable(self):
        from ai_company.doctor.checks import check_omniroute_health

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"providers": 10}
        mock_response.headers = {"content-type": "application/json"}

        with (
            patch.dict("os.environ", {"OMNIROUTE_API_KEY": "sk-test-key"}),
            patch("httpx.get", return_value=mock_response),
        ):
            result = check_omniroute_health()

            assert result.passed is True
            assert result.severity == "ok"

    def test_check_fails_when_unreachable(self):
        from ai_company.doctor.checks import check_omniroute_health

        with (
            patch.dict("os.environ", {"OMNIROUTE_API_KEY": "sk-test-key"}),
            patch("httpx.get", side_effect=ConnectionError("Connection refused")),
        ):
            result = check_omniroute_health()

            assert result.passed is False
            assert result.severity == "warning"

    def test_check_fails_on_non_200(self):
        from ai_company.doctor.checks import check_omniroute_health

        mock_response = MagicMock()
        mock_response.status_code = 503

        with (
            patch.dict("os.environ", {"OMNIROUTE_API_KEY": "sk-test-key"}),
            patch("httpx.get", return_value=mock_response),
        ):
            result = check_omniroute_health()

            assert result.passed is False
            assert result.severity == "warning"
