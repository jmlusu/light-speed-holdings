"""Sprint 5 T009 — OAuth2 client-credentials auth tests.

Covers the ``OAuth2TokenManager`` (token fetch, cache, TTL, fail-closed)
and its integration into ``OpenAICompatibleProvider`` (per-request bearer
token, availability, API-key fallback).
"""

from __future__ import annotations

import time
from pathlib import Path
from unittest.mock import MagicMock

import httpx
import pytest

from ai_company.llm.oauth2 import OAuth2Config, OAuth2Error, OAuth2TokenManager
from ai_company.llm.providers.base import ChatResponse, LLMProviderError
from ai_company.llm.providers.openai_compatible import OpenAICompatibleProvider

_TOKEN_URL = "https://idp.example.com/oauth/token"


def _token_transport(
    access_token: str = "test-token-abc",
    expires_in: int = 3600,
    status_code: int = 200,
) -> httpx.MockTransport:
    """Mock transport that answers the token endpoint."""
    handler = MagicMock(
        side_effect=lambda request: httpx.Response(
            status_code,
            json={
                "access_token": access_token,
                "token_type": "Bearer",
                "expires_in": expires_in,
            },
        )
    )
    return httpx.MockTransport(handler)


def _config(**overrides: object) -> OAuth2Config:
    defaults: dict[str, object] = {
        "token_url": _TOKEN_URL,
        "client_id": "my-client",
        "client_secret": "s3cret",
        "scope": "llm:inference",
    }
    defaults.update(overrides)
    return OAuth2Config(**defaults)  # type: ignore[arg-type]


# ── OAuth2TokenManager ──────────────────────────────────────────────


def test_fetches_token_and_caches_it() -> None:
    transport = _token_transport()
    manager = OAuth2TokenManager(_config(), http_client=httpx.Client(transport=transport))

    assert manager.get_access_token() == "test-token-abc"
    # Second call within TTL must reuse the cache (only one fetch).
    assert manager.get_access_token() == "test-token-abc"
    assert transport.handler.call_count == 1  # type: ignore[attr-defined]
    manager._client.close()  # type: ignore[union-attr]


def test_missing_credentials_fail_closed() -> None:
    manager = OAuth2TokenManager(
        _config(client_id="", client_secret=""),
        http_client=httpx.Client(transport=_token_transport()),
    )
    assert not manager.is_configured
    with pytest.raises(OAuth2Error, match="credentials missing"):
        manager.get_access_token()
    manager._client.close()  # type: ignore[union-attr]


def test_token_endpoint_non_200_fails_closed() -> None:
    manager = OAuth2TokenManager(
        _config(),
        http_client=httpx.Client(transport=_token_transport(status_code=500)),
    )
    with pytest.raises(OAuth2Error, match="500"):
        manager.get_access_token()
    manager._client.close()  # type: ignore[union-attr]


def test_token_endpoint_missing_access_token_fails_closed() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json={"token_type": "Bearer"})
    )
    manager = OAuth2TokenManager(_config(), http_client=httpx.Client(transport=transport))
    with pytest.raises(OAuth2Error, match="missing access_token"):
        manager.get_access_token()
    manager._client.close()  # type: ignore[union-attr]


def test_expired_token_is_refreshed() -> None:
    transport = _token_transport(expires_in=1)
    manager = OAuth2TokenManager(_config(), http_client=httpx.Client(transport=transport))
    assert manager.get_access_token() == "test-token-abc"

    # Simulate elapsed time past the TTL + safety margin.
    manager._expires_at = time.time() - 10.0  # type: ignore[attr-defined]
    assert manager.get_access_token() == "test-token-abc"
    assert transport.handler.call_count == 2  # type: ignore[attr-defined]
    manager._client.close()  # type: ignore[union-attr]


def test_sends_grant_type_and_credentials() -> None:
    captured: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = request.content.decode("utf-8")
        return httpx.Response(200, json={"access_token": "tok", "expires_in": 3600})

    manager = OAuth2TokenManager(
        _config(scope="llm:inference"),
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    manager.get_access_token()
    manager._client.close()  # type: ignore[union-attr]

    assert "grant_type=client_credentials" in captured["body"]
    assert "client_id=my-client" in captured["body"]
    assert "client_secret=s3cret" in captured["body"]
    assert "scope=llm%3Ainference" in captured["body"]


def test_env_var_credentials_resolved(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OAUTH2_TEST_CLIENT_ID", "env-client")
    monkeypatch.setenv("OAUTH2_TEST_CLIENT_SECRET", "env-secret")
    manager = OAuth2TokenManager(
        _config(
            client_id="",
            client_secret="",
            client_id_env="OAUTH2_TEST_CLIENT_ID",
            client_secret_env="OAUTH2_TEST_CLIENT_SECRET",
        ),
        http_client=httpx.Client(transport=_token_transport()),
    )
    assert manager.is_configured
    assert manager.get_access_token() == "test-token-abc"
    manager._client.close()  # type: ignore[union-attr]


# ── OpenAICompatibleProvider integration ────────────────────────────


def _mock_chat_response() -> ChatResponse:
    return ChatResponse(content="hello", model="test-model", provider="oauth-test")


def test_provider_uses_oauth2_bearer_header() -> None:
    manager = OAuth2TokenManager(
        _config(),
        http_client=httpx.Client(transport=_token_transport()),
    )
    provider = OpenAICompatibleProvider(
        name="oauth-test",
        api_base="https://llm.example.com/v1",
        default_model="test-model",
        oauth2=manager,
    )
    assert provider.is_available()

    mock_client = MagicMock(spec=httpx.Client)
    mock_client.post.return_value.status_code = 200
    mock_client.post.return_value.json.return_value = {
        "choices": [{"message": {"content": "hello"}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5},
    }
    provider._client = mock_client

    provider.chat("sys", "usr")
    _, kwargs = mock_client.post.call_args
    assert kwargs["headers"]["Authorization"] == "Bearer test-token-abc"
    manager._client.close()  # type: ignore[union-attr]


def test_provider_fail_closed_when_oauth2_unconfigured() -> None:
    manager = OAuth2TokenManager(
        _config(client_id="", client_secret=""),
        http_client=httpx.Client(transport=_token_transport()),
    )
    provider = OpenAICompatibleProvider(
        name="oauth-test",
        api_base="https://llm.example.com/v1",
        default_model="test-model",
        oauth2=manager,
    )
    assert not provider.is_available()
    with pytest.raises(LLMProviderError):
        provider.chat("sys", "usr")
    manager._client.close()  # type: ignore[union-attr]


def test_provider_falls_back_to_api_key_when_no_oauth2(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # No OAuth2 manager, no API key -> unavailable (fail-closed).
    provider = OpenAICompatibleProvider(
        name="oauth-test",
        api_base="https://llm.example.com/v1",
        default_model="test-model",
        api_key_env="NONEXISTENT_KEY_XYZ",
        auth_style="x-api-key",
    )
    assert not provider.is_available()

    # With a static API key the provider works without any OAuth2 config.
    monkeypatch.setenv("OAUTH2_TEST_API_KEY", "static-key")
    provider = OpenAICompatibleProvider(
        name="oauth-test",
        api_base="https://llm.example.com/v1",
        default_model="test-model",
        api_key_env="OAUTH2_TEST_API_KEY",
        auth_style="x-api-key",
    )
    assert provider.is_available()
    assert provider._oauth2 is None  # type: ignore[attr-defined]
    provider._client = None
    with pytest.raises(LLMProviderError, match="No API key or OAuth2"):
        provider.chat("sys", "usr")


def test_client_wires_oauth2_from_models_yaml(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """LLMClient builds an OAuth2-managed provider when models.yaml says so."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("OAUTH2_TEST_CLIENT_ID", "env-client")
    monkeypatch.setenv("OAUTH2_TEST_CLIENT_SECRET", "env-secret")
    (tmp_path / "company").mkdir(exist_ok=True)
    models = {
        "providers": {
            "enterprise": {
                "backend": "openai_compatible",
                "default_model": "enterprise-model",
                "api_base": "https://llm.example.com/v1",
                "oauth2": {
                    "token_url": _TOKEN_URL,
                    "client_id_env": "OAUTH2_TEST_CLIENT_ID",
                    "client_secret_env": "OAUTH2_TEST_CLIENT_SECRET",
                    "scope": "llm:inference",
                    "cache_ttl_seconds": 300,
                },
            }
        },
        "tiers": {
            "standard": {
                "description": "Standard",
                "providers": [{"provider": "enterprise", "model": "enterprise-model"}],
            }
        },
        "routing": [{"agent_type": "Specialist", "tier": "standard"}],
    }
    import json

    (tmp_path / "company" / "models.yaml").write_text(json.dumps(models), encoding="utf-8")
    (tmp_path / "company" / "agent-registry.json").write_text("[]", encoding="utf-8")

    from ai_company.llm.client import LLMClient

    client = LLMClient(
        config_path=str(tmp_path / "company" / "models.yaml"),
        registry_path=str(tmp_path / "company" / "agent-registry.json"),
    )
    provider = client._providers["enterprise"]
    assert provider is not None
    assert provider._oauth2 is not None  # type: ignore[attr-defined]
    assert provider._oauth2.is_configured  # type: ignore[attr-defined]
