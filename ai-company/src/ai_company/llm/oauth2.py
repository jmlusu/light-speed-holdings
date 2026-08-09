"""OAuth2 client-credentials token manager for LLM providers.

Provides an in-memory, TTL-bounded access-token cache for the OAuth2
``client_credentials`` grant. Designed to be fail-closed:

- Missing client id/secret makes the provider unavailable.
- A failed token fetch raises :class:`OAuth2Error` (a subclass of
  :class:`~ai_company.llm.providers.base.LLMProviderError`) so the
  router can fall through to the next provider.

Tokens are cached in memory only and never persisted. Secrets are read
from the environment and are never logged.
"""

from __future__ import annotations

import logging
import os
import threading
import time
from dataclasses import dataclass
from typing import Any

import httpx

from ai_company.llm.providers.base import LLMProviderError

logger = logging.getLogger(__name__)

_GRANT_TYPE = "client_credentials"


class OAuth2Error(LLMProviderError):
    """Raised when OAuth2 client-credentials auth cannot obtain a token."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__("oauth2", message, status_code=status_code)


@dataclass(frozen=True)
class OAuth2Config:
    """OAuth2 client-credentials configuration for a provider.

    Attributes:
        token_url: Token endpoint that issues access tokens.
        client_id: Client identifier. When empty, read from ``client_id_env``.
        client_secret: Client secret. When empty, read from ``client_secret_env``.
        client_id_env: Env var holding the client id (fallback).
        client_secret_env: Env var holding the client secret (fallback).
        scope: Optional OAuth2 scope string.
        audience: Optional audience claim for the token request.
        cache_ttl_seconds: Hard cap on how long a cached token is reused.
            The token's own ``expires_in`` is used when smaller.
    """

    token_url: str
    client_id: str = ""
    client_secret: str = ""
    client_id_env: str = ""
    client_secret_env: str = ""
    scope: str | None = None
    audience: str | None = None
    cache_ttl_seconds: int = 3600


class OAuth2TokenManager:
    """Fetches and caches OAuth2 client-credentials access tokens.

    The cache is in-memory and thread-safe. A token is reused until it is
    within a safety margin of expiry or the configured TTL elapses, then a
    single refresh is performed (concurrent callers share one refresh).
    """

    _SAFETY_MARGIN_SECONDS = 60.0

    def __init__(
        self,
        config: OAuth2Config,
        timeout: float = 30.0,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._config = config
        self._timeout = timeout
        self._lock = threading.Lock()
        self._access_token: str | None = None
        self._expires_at: float = 0.0
        self._client = http_client

    @classmethod
    def from_config(
        cls,
        config: OAuth2Config,
        timeout: float = 30.0,
    ) -> OAuth2TokenManager:
        """Build a manager from a config, resolving env-var credentials."""
        return cls(config=config, timeout=timeout)

    # ── Public API ───────────────────────────────────────────────────

    @property
    def is_configured(self) -> bool:
        """True when both a client id and secret are available (fail-closed)."""
        return bool(self._resolve_client_id() and self._resolve_client_secret())

    def get_access_token(self) -> str:
        """Return a valid access token, fetching/refreshing as needed.

        Returns:
            The bearer token value.

        Raises:
            OAuth2Error: If credentials are missing or the token endpoint
                fails (non-2xx or transport error).
        """
        with self._lock:
            if self._is_cache_valid():
                return self._access_token or ""
            token = self._fetch_token()
            self._access_token = token["access_token"]
            expires_in = self._safe_expires_in(token)
            self._expires_at = time.time() + expires_in
            logger.debug(
                "OAuth2 token acquired for %s (expires_in=%ss)",
                self._config.token_url,
                int(expires_in),
            )
            return self._access_token

    def invalidate(self) -> None:
        """Drop the cached token so the next call refreshes."""
        with self._lock:
            self._access_token = None
            self._expires_at = 0.0

    # ── Internals ────────────────────────────────────────────────────

    def _resolve_client_id(self) -> str:
        if self._config.client_id:
            return self._config.client_id
        if self._config.client_id_env:
            return os.environ.get(self._config.client_id_env, "")
        return ""

    def _resolve_client_secret(self) -> str:
        if self._config.client_secret:
            return self._config.client_secret
        if self._config.client_secret_env:
            return os.environ.get(self._config.client_secret_env, "")
        return ""

    def _is_cache_valid(self) -> bool:
        if not self._access_token:
            return False
        safety_margin = self._SAFETY_MARGIN_SECONDS
        return time.time() < self._expires_at - safety_margin

    def _safe_expires_in(self, token: dict[str, Any]) -> float:
        raw = token.get("expires_in")
        try:
            expires_in = float(raw or 0)
        except (TypeError, ValueError):
            expires_in = 0.0
        if expires_in <= 0:
            expires_in = float(self._config.cache_ttl_seconds or 3600)
        return min(expires_in, float(self._config.cache_ttl_seconds or 3600))

    def _token_endpoint_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/x-www-form-urlencoded"}

    def _token_payload(self) -> dict[str, str]:
        payload: dict[str, str] = {
            "grant_type": _GRANT_TYPE,
            "client_id": self._resolve_client_id(),
            "client_secret": self._resolve_client_secret(),
        }
        if self._config.scope:
            payload["scope"] = self._config.scope
        if self._config.audience:
            payload["audience"] = self._config.audience
        return payload

    def _fetch_token(self) -> dict[str, Any]:
        client_id = self._resolve_client_id()
        client_secret = self._resolve_client_secret()
        if not client_id or not client_secret:
            raise OAuth2Error(
                "OAuth2 client credentials missing (set client id/secret or their env vars)"
            )

        client = self._client or httpx.Client(timeout=self._timeout)
        try:
            resp = client.post(
                self._config.token_url,
                data=self._token_payload(),
                headers=self._token_endpoint_headers(),
            )
        except httpx.HTTPError as exc:
            raise OAuth2Error(f"Token endpoint request failed: {exc}") from exc
        finally:
            if self._client is None:
                client.close()

        if resp.status_code != 200:
            raise OAuth2Error(
                f"Token endpoint returned {resp.status_code}: {resp.text[:200]}",
                status_code=resp.status_code,
            )

        data = resp.json()
        token = data.get("access_token")
        if not token:
            raise OAuth2Error("Token endpoint response missing access_token")
        return data
