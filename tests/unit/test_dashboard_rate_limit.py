"""Tests for dashboard rate limiting (Sprint 4 P2 — item 10.3).

Covers the custom :class:`~ai_company.dashboard.app._RateLimiter` directly and
through the HTTP middleware:

- Requests exceeding the rate limit return ``429``.
- The limiter resets after the window elapses.
- The CORS middleware rejects disallowed origins.
- Authenticated requests compose correctly with the rate limiter: the
  ``X-API-Key`` guard authorises writes, but there is no authenticated bypass
  of the limiter — every request consumes budget (matches current behaviour).

All file I/O is anchored at ``tmp_path`` via ``DASHBOARD_DATA_DIR`` so no real
project data is touched.
"""

from __future__ import annotations

import time
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.app import _RateLimiter

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _setup_minimal_data(tmp_path: Path) -> None:
    """Create the minimal workspace files the dashboard API expects."""
    (tmp_path / "company").mkdir(exist_ok=True)
    (tmp_path / "company" / "agent-registry.json").write_text("[]", encoding="utf-8")
    (tmp_path / "company" / "departments.yaml").write_text("departments: []", encoding="utf-8")
    (tmp_path / ".opencode").mkdir(exist_ok=True)
    (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
    (tmp_path / "orchestrator").mkdir(exist_ok=True)
    (tmp_path / "orchestrator" / "approvals.yaml").write_text("requests: []", encoding="utf-8")
    (tmp_path / "orchestrator" / "escalation.yaml").write_text(
        "rules: []\nevents: []", encoding="utf-8"
    )
    (tmp_path / "orchestrator" / "scheduler.yaml").write_text("tasks: []", encoding="utf-8")


def _make_app(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    *,
    rate_limit: str = "10",
    api_key: str = "",
    origins: str | None = None,
) -> "object":
    """Build a fresh dashboard app bound to *tmp_path* with the given env.

    ``DASHBOARD_DATA_DIR`` is always pointed at ``tmp_path`` so the state
    store, MessageBus, and SQLite database never touch the real project.
    """
    monkeypatch.setenv("DASHBOARD_RATE_LIMIT", rate_limit)
    if api_key:
        monkeypatch.setenv("DASHBOARD_API_KEY", api_key)
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")
        # The role-key env surface may already be populated by a loaded .env
        # (e.g. llm.client runs load_dotenv at import), which would shadow the
        # DASHBOARD_API_KEY under test via rbac._configured_keys. Clear it so
        # this helper's key is authoritative and tests are order-independent.
        monkeypatch.delenv("DASHBOARD_ADMIN_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_APPROVE_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_RUN_KEY", raising=False)
    else:
        monkeypatch.delenv("DASHBOARD_API_KEY", raising=False)
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "open")
    if origins is None:
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
    else:
        monkeypatch.setenv("DASHBOARD_CORS_ORIGINS", origins)
    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    _setup_minimal_data(tmp_path)

    from ai_company.dashboard.app import create_app

    return create_app()


@pytest.fixture()
def rate_app(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """A dashboard app with a tiny, configurable rate limit (3 req/min)."""
    return _make_app(monkeypatch, tmp_path, rate_limit="3")


# ---------------------------------------------------------------------------
# Unit tests: _RateLimiter
# ---------------------------------------------------------------------------


class TestRateLimiterUnit:
    """Direct coverage of the sliding-window limiter."""

    def test_requests_exceeding_limit_blocked(self) -> None:
        limiter = _RateLimiter(max_requests=2, window_seconds=60)
        assert limiter.is_allowed("ip-1") == (True, 1)
        assert limiter.is_allowed("ip-1") == (True, 0)
        assert limiter.is_allowed("ip-1") == (False, 0)

    def test_different_keys_have_separate_budgets(self) -> None:
        limiter = _RateLimiter(max_requests=1, window_seconds=60)
        assert limiter.is_allowed("ip-a") == (True, 0)
        assert limiter.is_allowed("ip-a") == (False, 0)
        assert limiter.is_allowed("ip-b") == (True, 0)

    def test_resets_after_window_elapses(self) -> None:
        """Hits recorded before the window are pruned and budget is restored."""
        limiter = _RateLimiter(max_requests=2, window_seconds=60)
        limiter.is_allowed("ip-1")
        limiter.is_allowed("ip-1")
        assert limiter.is_allowed("ip-1") == (False, 0)

        # Backdate the recorded hits so they fall outside the window.
        limiter._hits["ip-1"] = [time.time() - 61.0]
        allowed, remaining = limiter.is_allowed("ip-1")
        assert allowed is True
        assert remaining == 1

    def test_resets_after_window_with_mocked_clock(self) -> None:
        """Advancing the clock past the window restores the budget."""
        clock = [1_000_000.0]
        with patch("ai_company.dashboard.app.time.time", side_effect=lambda: clock[0]):
            limiter = _RateLimiter(max_requests=1, window_seconds=10)
            assert limiter.is_allowed("ip-1") == (True, 0)
            assert limiter.is_allowed("ip-1") == (False, 0)

            clock[0] += 11.0
            assert limiter.is_allowed("ip-1") == (True, 0)


# ---------------------------------------------------------------------------
# HTTP tests: 429 behaviour + headers
# ---------------------------------------------------------------------------


class TestRateLimitHttp:
    """Middleware-level behaviour through the FastAPI TestClient."""

    def test_requests_exceeding_limit_return_429(self, rate_app) -> None:
        client = TestClient(rate_app)
        for _ in range(3):
            assert client.get("/health").status_code == 200
        resp = client.get("/health")
        assert resp.status_code == 429
        assert resp.json()["detail"] == "Rate limit exceeded"

    def test_rate_limit_headers_on_allowed_request(self, rate_app) -> None:
        client = TestClient(rate_app)
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.headers["x-ratelimit-limit"] == "3"
        assert resp.headers["x-ratelimit-remaining"] == "2"

    def test_429_response_includes_rate_limit_headers(self, rate_app) -> None:
        client = TestClient(rate_app)
        for _ in range(3):
            client.get("/health")
        resp = client.get("/health")
        assert resp.status_code == 429
        assert resp.headers["x-ratelimit-limit"] == "3"
        assert resp.headers["x-ratelimit-remaining"] == "0"

    def test_rate_limit_resets_after_window(self, rate_app) -> None:
        client = TestClient(rate_app)
        for _ in range(3):
            assert client.get("/health").status_code == 200
        assert client.get("/health").status_code == 429

        # Simulate the window elapsing: the middleware reads the same limiter
        # stored on app.state, so backdating its hits frees the budget. The
        # per-request bucket key is implementation-dependent (older Starlette
        # TestClients pass scope["client"]=None, so the middleware falls back
        # to "unknown"), so backdate every bucket the limiter actually holds.
        for key in rate_app.state.limiter._hits:
            rate_app.state.limiter._hits[key] = [time.time() - 61.0]
        assert client.get("/health").status_code == 200


# ---------------------------------------------------------------------------
# HTTP tests: CORS
# ---------------------------------------------------------------------------


class TestCorsRejectsDisallowedOrigins:
    """The CORS allowlist must never reflect an unknown origin."""

    def test_allowed_origin_reflected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        app = _make_app(monkeypatch, tmp_path, origins="https://app.example.com")
        client = TestClient(app)
        resp = client.options(
            "/api/v1/dashboard",
            headers={
                "Origin": "https://app.example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert resp.headers.get("access-control-allow-origin") == "https://app.example.com"

    def test_disallowed_origin_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        # Default allowlist is localhost-only.
        app = _make_app(monkeypatch, tmp_path)
        client = TestClient(app)
        resp = client.options(
            "/api/v1/dashboard",
            headers={
                "Origin": "https://evil.example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        acao = resp.headers.get("access-control-allow-origin", "")
        assert acao != "https://evil.example.com"
        assert acao == ""


# ---------------------------------------------------------------------------
# HTTP tests: authentication + rate limit composition
# ---------------------------------------------------------------------------


class TestAuthenticatedRequests:
    """Write endpoints require an API key; the limiter applies to all requests."""

    def test_authenticated_write_within_limit_succeeds(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        app = _make_app(monkeypatch, tmp_path, rate_limit="10", api_key="secret-key-123")
        client = TestClient(app)
        resp = client.post(
            "/api/v1/tasks",
            json={
                "receiver_id": "test-agent",
                "instruction": "Build a widget for the dashboard",
            },
            headers={"X-API-Key": "secret-key-123"},
        )
        assert resp.status_code == 201

    def test_authenticated_write_missing_key_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        app = _make_app(monkeypatch, tmp_path, rate_limit="10", api_key="secret-key-123")
        client = TestClient(app)
        resp = client.post(
            "/api/v1/tasks",
            json={
                "receiver_id": "test-agent",
                "instruction": "Build a widget for the dashboard",
            },
        )
        assert resp.status_code == 401
        assert "API key" in resp.json()["detail"]

    def test_authenticated_requests_still_rate_limited(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Document current behaviour: auth does not bypass the rate limiter.

        Every request (authenticated or not) consumes the per-IP budget, so an
        authenticated client is still limited once the budget is exhausted.
        """
        app = _make_app(monkeypatch, tmp_path, rate_limit="2", api_key="secret-key-123")
        client = TestClient(app)
        headers = {"X-API-Key": "secret-key-123"}
        payload = {
            "receiver_id": "test-agent",
            "instruction": "Build a widget for the dashboard",
        }
        assert client.post("/api/v1/tasks", json=payload, headers=headers).status_code == 201
        assert client.post("/api/v1/tasks", json=payload, headers=headers).status_code == 201
        resp = client.post("/api/v1/tasks", json=payload, headers=headers)
        assert resp.status_code == 429
