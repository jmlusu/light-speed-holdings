"""Sprint 4 T016 — dashboard HTTP rate limiting: 429s, headers, per-IP isolation, CORS.

Covers the GAP-010 rate limiter at the HTTP layer (which the unit suite does
not): requests beyond ``DASHBOARD_RATE_LIMIT`` receive 429, the
``X-RateLimit-*`` headers decrement correctly, per-IP state is independent,
and disallowed origins are not reflected by CORS preflight.
"""

from __future__ import annotations

import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.app import _RateLimiter, create_app


@pytest.fixture()
def isolated(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Give every test a fresh app context: no API key, tmp data root + cwd."""
    monkeypatch.delenv("DASHBOARD_API_KEY", raising=False)
    monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))
    monkeypatch.chdir(tmp_path)


# ── HTTP-level rate limiting ───────────────────────────────────────────


class TestHTTPRateLimiting:
    def test_requests_within_limit_succeed(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "5")
        app = create_app()
        client = TestClient(app)
        for _ in range(5):
            resp = client.get("/api/v1/agents")
            assert resp.status_code == 200

    def test_request_after_limit_returns_429(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "3")
        app = create_app()
        client = TestClient(app)
        for _ in range(3):
            assert client.get("/api/v1/agents").status_code == 200
        resp = client.get("/api/v1/agents")
        assert resp.status_code == 429
        assert resp.json() == {"detail": "Rate limit exceeded"}

    def test_rate_limit_headers_decrement_and_reset(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "3")
        app = create_app()
        client = TestClient(app)

        first = client.get("/api/v1/agents")
        assert first.status_code == 200
        assert first.headers["X-RateLimit-Limit"] == "3"
        assert first.headers["X-RateLimit-Remaining"] == "2"

        second = client.get("/api/v1/agents")
        assert second.headers["X-RateLimit-Remaining"] == "1"

        third = client.get("/api/v1/agents")
        assert third.headers["X-RateLimit-Remaining"] == "0"

        blocked = client.get("/api/v1/agents")
        assert blocked.status_code == 429
        assert blocked.headers["X-RateLimit-Limit"] == "3"
        assert blocked.headers["X-RateLimit-Remaining"] == "0"

    def test_rate_limit_state_is_per_app_instance(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A fresh create_app() must have a fresh limiter (no global leak)."""
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "1")
        first_app = create_app()
        client_a = TestClient(first_app)
        assert client_a.get("/api/v1/agents").status_code == 200
        assert client_a.get("/api/v1/agents").status_code == 429

        second_app = create_app()
        client_b = TestClient(second_app)
        assert client_b.get("/api/v1/agents").status_code == 200


# ── Limiter-level isolation and window semantics ───────────────────────


class TestLimiterIsolation:
    def test_per_ip_limits_are_independent(self) -> None:
        limiter = _RateLimiter(max_requests=2, window_seconds=60)
        assert limiter.is_allowed("ip-a") == (True, 1)
        assert limiter.is_allowed("ip-a") == (True, 0)
        assert limiter.is_allowed("ip-a") == (False, 0)
        # A different client is not affected by ip-a's exhaustion.
        assert limiter.is_allowed("ip-b") == (True, 1)

    def test_window_slides_and_recovers(self) -> None:
        limiter = _RateLimiter(max_requests=1, window_seconds=60)
        assert limiter.is_allowed("ip-a") == (True, 0)
        assert limiter.is_allowed("ip-a") == (False, 0)
        # Backdate the hit beyond the window -> pruned on next check.
        limiter._hits["ip-a"] = [time.time() - 61]
        assert limiter.is_allowed("ip-a") == (True, 0)

    def test_old_hits_are_pruned_before_limit_check(self) -> None:
        limiter = _RateLimiter(max_requests=2, window_seconds=60)
        limiter._hits["ip-a"] = [time.time() - 61, time.time() - 61]
        # Both hits are stale, so the request is allowed.
        assert limiter.is_allowed("ip-a") == (True, 1)


# ── CORS preflight rejection (rate-limit adjacency) ────────────────────


class TestCORSPreflight:
    def test_allowed_origin_is_reflected(self, isolated: None) -> None:
        app = create_app()
        client = TestClient(app)
        resp = client.options(
            "/api/v1/dashboard",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert resp.headers.get("access-control-allow-origin") == "http://localhost:3000"

    def test_unknown_origin_is_rejected(self, isolated: None) -> None:
        app = create_app()
        client = TestClient(app)
        resp = client.options(
            "/api/v1/dashboard",
            headers={
                "Origin": "https://evil.example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert resp.headers.get("access-control-allow-origin", "") == ""

    def test_custom_origin_env_is_honoured(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_CORS_ORIGINS", "https://app.example.com")
        app = create_app()
        client = TestClient(app)

        allowed = client.options(
            "/api/v1/dashboard",
            headers={
                "Origin": "https://app.example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert allowed.headers.get("access-control-allow-origin") == "https://app.example.com"

        rejected = client.options(
            "/api/v1/dashboard",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert rejected.headers.get("access-control-allow-origin", "") == ""

    def test_wildcard_env_is_never_reflected(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_CORS_ORIGINS", "*")
        app = create_app()
        client = TestClient(app)
        resp = client.options(
            "/api/v1/dashboard",
            headers={
                "Origin": "https://any-origin.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert resp.headers.get("access-control-allow-origin", "") != "*"
