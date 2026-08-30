"""Tests for GAP-010 — dashboard CORS, API key, and rate-limiting security."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def _anchor_data_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Anchor DASHBOARD_DATA_DIR so create_app() writes to the per-test tmp
    dir instead of the real project ``.opencode`` directory."""
    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))


# ── CORS configuration tests ──────────────────────────────────────────


class TestCORSConfiguration:
    """Verify CORS origins are configurable and never wildcard (GAP-010)."""

    def test_default_cors_allows_localhost(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Default config should allow http://localhost:3000."""
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.options(
            "/api/v1/dashboard",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        acao = resp.headers.get("access-control-allow-origin", "")
        assert acao == "http://localhost:3000"

    def test_default_cors_is_not_wildcard(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Default CORS must never reflect '*'."""
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.options(
            "/api/v1/dashboard",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert resp.headers.get("access-control-allow-origin", "") != "*"

    def test_cors_custom_origins(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Custom origins should be honoured."""
        monkeypatch.setenv("DASHBOARD_CORS_ORIGINS", "https://app.example.com")
        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.options(
            "/api/v1/dashboard",
            headers={
                "Origin": "https://app.example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert resp.headers.get("access-control-allow-origin", "") == "https://app.example.com"

    def test_cors_unknown_origin_rejected(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """An origin not in the allowlist must not be reflected."""
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        from ai_company.dashboard.app import create_app

        app = create_app()
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

    def test_cors_wildcard_in_env_is_rejected(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A '*' entry in DASHBOARD_CORS_ORIGINS must not open CORS."""
        monkeypatch.setenv("DASHBOARD_CORS_ORIGINS", "*")
        from ai_company.dashboard.app import create_app

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


# ── API key authentication tests ──────────────────────────────────────


class TestAPIKeyAuth:
    """Verify that ALL endpoints require an API key in api_key mode (fail-closed)."""

    def test_read_without_api_key_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """GET requests require API key in api_key mode (fail-closed)."""
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard")
        assert resp.status_code == 401
        assert "API key" in resp.json()["detail"]

    def test_write_without_api_key_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """POST requests without API key should be rejected when key is set."""
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.post(
            "/api/v1/tasks",
            json={"receiver_id": "agent", "instruction": "do something"},
        )
        assert resp.status_code == 401
        assert "API key" in resp.json()["detail"]

    def test_write_with_valid_api_key_accepted(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """POST requests with correct API key should succeed."""
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_ADMIN_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_APPROVE_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_RUN_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.post(
            "/api/v1/tasks",
            json={"receiver_id": "agent", "instruction": "do something"},
            headers={"X-API-Key": "secret-key-123"},
        )
        assert resp.status_code == 201

    def test_read_with_valid_api_key_accepted(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """GET requests with correct API key should succeed."""
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_ADMIN_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_APPROVE_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_RUN_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.get(
            "/api/v1/dashboard",
            headers={"X-API-Key": "secret-key-123"},
        )
        assert resp.status_code == 200

    def test_write_with_wrong_api_key_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """POST requests with wrong API key should be rejected."""
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.post(
            "/api/v1/tasks",
            json={"receiver_id": "agent", "instruction": "do something"},
            headers={"X-API-Key": "wrong-key"},
        )
        assert resp.status_code == 401

    def test_open_mode_allows_all(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """DASHBOARD_AUTH_MODE=open explicitly disables auth (localhost dev)."""
        monkeypatch.delenv("DASHBOARD_API_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "open")
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.post(
            "/api/v1/tasks",
            json={"receiver_id": "agent", "instruction": "do something"},
        )
        assert resp.status_code == 201

    def test_default_mode_is_fail_closed_without_key(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Default auth mode rejects ALL requests when no key is set."""
        monkeypatch.delenv("DASHBOARD_API_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.delenv("DASHBOARD_AUTH_MODE", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.post(
            "/api/v1/tasks",
            json={"receiver_id": "agent", "instruction": "do something"},
        )
        assert resp.status_code == 401

    def test_default_mode_rejects_safe_methods_without_key(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Default auth mode blocks GET/HEAD/OPTIONS on API endpoints when no key is set."""
        monkeypatch.delenv("DASHBOARD_API_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.delenv("DASHBOARD_AUTH_MODE", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        # /health is exempted from auth (CI liveness probe); /metrics is not
        resp = client.get("/metrics")
        assert resp.status_code == 401

    @staticmethod
    def _setup_minimal_data(tmp_path: Path) -> None:
        (tmp_path / "company").mkdir(exist_ok=True)
        (tmp_path / "company" / "agent-registry.json").write_text("[]", encoding="utf-8")
        (tmp_path / ".opencode").mkdir(exist_ok=True)
        (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
        (tmp_path / "orchestrator").mkdir(exist_ok=True)
        (tmp_path / "orchestrator" / "approvals.yaml").write_text("requests: []", encoding="utf-8")
        (tmp_path / "orchestrator" / "escalation.yaml").write_text(
            "rules: []\nevents: []", encoding="utf-8"
        )
        (tmp_path / "orchestrator" / "scheduler.yaml").write_text("tasks: []", encoding="utf-8")
        (tmp_path / "company" / "departments.yaml").write_text("departments: []", encoding="utf-8")

        import shutil

        real_models = Path(__file__).resolve().parents[2] / "company" / "models.yaml"
        if real_models.exists():
            shutil.copy2(str(real_models), str(tmp_path / "company" / "models.yaml"))


# ── ADR-013: middleware carve-out + bootstrap token tests ─────────────


class TestADRCarveOuts:
    """ADR-013: page routes, static assets, and bootstrap endpoint bypass the API-key guard."""

    def test_page_routes_accessible_without_key(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Page routes (/, /agents, /tasks, etc.) must load without an API key."""
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        for path in (
            "/",
            "/agents",
            "/tasks",
            "/kpis",
            "/costs",
            "/escalations",
            "/command-center",
        ):
            resp = client.get(path)
            assert resp.status_code == 200, f"Expected 200 for {path}, got {resp.status_code}"

    def test_bootstrap_endpoint_accessible_without_key(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """GET /api/v1/bootstrap-token must be callable without an API key."""
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/bootstrap-token")
        assert resp.status_code == 200
        data = resp.json()
        assert "token" in data
        assert len(data["token"]) > 10

    def test_api_endpoints_still_require_key(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """API endpoints (/api/v1/*) must still require an API key."""
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard")
        assert resp.status_code == 401

    def test_ops_endpoints_still_require_key(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Ops endpoints (/metrics) must still require an API key (/health is exempted for CI liveness)."""
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.get("/metrics")
        assert resp.status_code == 401

    @staticmethod
    def _setup_minimal_data(tmp_path: Path) -> None:
        (tmp_path / "company").mkdir(exist_ok=True)
        (tmp_path / "company" / "agent-registry.json").write_text("[]", encoding="utf-8")
        (tmp_path / ".opencode").mkdir(exist_ok=True)
        (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
        (tmp_path / "orchestrator").mkdir(exist_ok=True)
        (tmp_path / "orchestrator" / "approvals.yaml").write_text("requests: []", encoding="utf-8")
        (tmp_path / "orchestrator" / "escalation.yaml").write_text(
            "rules: []\nevents: []", encoding="utf-8"
        )
        (tmp_path / "orchestrator" / "scheduler.yaml").write_text("tasks: []", encoding="utf-8")
        (tmp_path / "company" / "departments.yaml").write_text("departments: []", encoding="utf-8")

        import shutil

        real_models = Path(__file__).resolve().parents[2] / "company" / "models.yaml"
        if real_models.exists():
            shutil.copy2(str(real_models), str(tmp_path / "company" / "models.yaml"))


class TestSessionTokenAuth:
    """ADR-013: browser session tokens authenticate via X-API-Key."""

    def test_session_token_authenticates_api_request(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A valid session token should authenticate an API request."""
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        # Mint a token from the bootstrap endpoint
        resp = client.get("/api/v1/bootstrap-token")
        token = resp.json()["token"]
        # Use the token as X-API-Key on an API request
        resp = client.get("/api/v1/dashboard", headers={"X-API-Key": token})
        assert resp.status_code == 200

    def test_session_token_authenticates_websocket(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A valid session token should authenticate a WebSocket handshake."""
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/bootstrap-token")
        token = resp.json()["token"]
        with client.websocket_connect(f"/ws/v1/dashboard?api_key={token}") as ws:
            hello = ws.receive_json()
            assert hello["type"] == "connected"

    def test_invalid_session_token_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """An invalid session token must be rejected."""
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard", headers={"X-API-Key": "not-a-real-token"})
        assert resp.status_code == 401

    def test_session_token_ip_bound(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """A session token from a different IP must be rejected."""
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.sessions import mint_bootstrap_token, resolve_session_token
        from ai_company.security.rbac import Role

        # Mint a token bound to one IP
        token = mint_bootstrap_token("192.168.1.100")
        # Should resolve from the same IP
        assert resolve_session_token(token, "192.168.1.100") == Role.APPROVE
        # Should fail from a different IP
        assert resolve_session_token(token, "10.0.0.1") is None

    @staticmethod
    def _setup_minimal_data(tmp_path: Path) -> None:
        (tmp_path / "company").mkdir(exist_ok=True)
        (tmp_path / "company" / "agent-registry.json").write_text("[]", encoding="utf-8")
        (tmp_path / ".opencode").mkdir(exist_ok=True)
        (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
        (tmp_path / "orchestrator").mkdir(exist_ok=True)
        (tmp_path / "orchestrator" / "approvals.yaml").write_text("requests: []", encoding="utf-8")
        (tmp_path / "orchestrator" / "escalation.yaml").write_text(
            "rules: []\nevents: []", encoding="utf-8"
        )
        (tmp_path / "orchestrator" / "scheduler.yaml").write_text("tasks: []", encoding="utf-8")
        (tmp_path / "company" / "departments.yaml").write_text("departments: []", encoding="utf-8")

        import shutil

        real_models = Path(__file__).resolve().parents[2] / "company" / "models.yaml"
        if real_models.exists():
            shutil.copy2(str(real_models), str(tmp_path / "company" / "models.yaml"))


# ── Rate limiting tests ──────────────────────────────────────────────


class TestRateLimiting:
    def test_rate_limit_allows_normal_traffic(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A few requests should all pass."""
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "5")
        monkeypatch.delenv("DASHBOARD_API_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)

        from ai_company.dashboard.app import _RateLimiter

        limiter = _RateLimiter(max_requests=5, window_seconds=60)
        for _ in range(5):
            allowed, _ = limiter.is_allowed("test-ip")
            assert allowed is True

    def test_rate_limit_blocks_excess(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Requests beyond the limit should be blocked."""
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "3")
        monkeypatch.delenv("DASHBOARD_API_KEY", raising=False)

        from ai_company.dashboard.app import _RateLimiter

        limiter = _RateLimiter(max_requests=3, window_seconds=60)
        allowed, _ = limiter.is_allowed("test-ip")
        assert allowed is True
        allowed, _ = limiter.is_allowed("test-ip")
        assert allowed is True
        allowed, _ = limiter.is_allowed("test-ip")
        assert allowed is True
        allowed, _ = limiter.is_allowed("test-ip")
        assert allowed is False

    def test_different_ips_have_separate_limits(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Different client IPs should be tracked independently."""
        monkeypatch.delenv("DASHBOARD_API_KEY", raising=False)

        from ai_company.dashboard.app import _RateLimiter

        limiter = _RateLimiter(max_requests=2, window_seconds=60)
        allowed, _ = limiter.is_allowed("ip-a")
        assert allowed is True
        allowed, _ = limiter.is_allowed("ip-a")
        assert allowed is True
        allowed, _ = limiter.is_allowed("ip-a")
        assert allowed is False
        # Different IP should still be allowed
        allowed, _ = limiter.is_allowed("ip-b")
        assert allowed is True


# ── Security headers tests (T018 / ticket #11) ──────────────────────


class TestSecurityHeaders:
    """CSP, HSTS, and framing/type-confusion guards on every response."""

    def test_default_headers_present_on_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A normal 200 response carries the full security header set."""
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.get("/health")
        assert resp.status_code == 200
        assert "content-security-policy" in resp.headers
        assert resp.headers["content-security-policy"].startswith("default-src 'self'")
        assert "X-Frame-Options" in resp.headers
        assert resp.headers["X-Frame-Options"] == "DENY"
        assert resp.headers["X-Content-Type-Options"] == "nosniff"
        assert resp.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
        assert "Permissions-Policy" in resp.headers
        assert "Strict-Transport-Security" in resp.headers
        assert "max-age=31536000" in resp.headers["Strict-Transport-Security"]

    def test_headers_present_on_auth_rejection(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Even a 401 short-circuit response must carry the security headers."""
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.post(
            "/api/v1/tasks",
            json={"receiver_id": "agent", "instruction": "do something"},
        )
        assert resp.status_code == 401
        assert "content-security-policy" in resp.headers
        assert resp.headers["X-Content-Type-Options"] == "nosniff"
        assert resp.headers["X-Frame-Options"] == "DENY"
        assert "Strict-Transport-Security" in resp.headers

    def test_csp_overrideable_via_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """DASHBOARD_CSP replaces the default policy."""
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.setenv(
            "DASHBOARD_CSP",
            "default-src 'none'; frame-ancestors 'none'; base-uri 'self'",
        )
        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.get("/health")
        assert resp.headers["content-security-policy"] == (
            "default-src 'none'; frame-ancestors 'none'; base-uri 'self'"
        )

    def test_hsts_disabled_when_max_age_zero(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """DASHBOARD_HSTS_MAX_AGE=0 suppresses the HSTS header."""
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.setenv("DASHBOARD_HSTS_MAX_AGE", "0")
        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.get("/health")
        assert "Strict-Transport-Security" not in resp.headers

    @staticmethod
    def _setup_minimal_data(tmp_path: Path) -> None:
        (tmp_path / "company").mkdir(exist_ok=True)
        (tmp_path / "company" / "agent-registry.json").write_text("[]", encoding="utf-8")
        (tmp_path / ".opencode").mkdir(exist_ok=True)
        (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
        (tmp_path / "orchestrator").mkdir(exist_ok=True)
        (tmp_path / "orchestrator" / "approvals.yaml").write_text("requests: []", encoding="utf-8")
        (tmp_path / "orchestrator" / "escalation.yaml").write_text(
            "rules: []\nevents: []", encoding="utf-8"
        )
        (tmp_path / "orchestrator" / "scheduler.yaml").write_text("tasks: []", encoding="utf-8")
        (tmp_path / "company" / "departments.yaml").write_text("departments: []", encoding="utf-8")

        import shutil

        real_models = Path(__file__).resolve().parents[2] / "company" / "models.yaml"
        if real_models.exists():
            shutil.copy2(str(real_models), str(tmp_path / "company" / "models.yaml"))


# ── WebSocket origin validation tests (T018 / ticket #11) ────────────


class TestWebSocketOrigin:
    """Cross-site WebSocket hijacking is blocked at the handshake."""

    def test_ws_rejects_cross_site_origin(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """An Origin not matching the host or allowlist must be refused."""
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        from starlette.websockets import WebSocketDisconnect

        with (
            pytest.raises(WebSocketDisconnect),
            client.websocket_connect(
                "/ws/v1/dashboard", headers={"origin": "https://evil.example.com"}
            ),
        ):
            pass

    def test_ws_accepts_same_origin(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A same-host Origin (or no Origin) must be accepted."""
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "open")
        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        with client.websocket_connect(
            "/ws/v1/dashboard", headers={"origin": "http://testserver"}
        ) as ws:
            hello = ws.receive_json()
            assert hello["type"] == "connected"

    def test_ws_accepts_allowlisted_origin(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """An Origin in the CORS allowlist must be accepted."""
        monkeypatch.setenv("DASHBOARD_CORS_ORIGINS", "https://dashboard.example.com")
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "open")
        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        with client.websocket_connect(
            "/ws/v1/dashboard",
            headers={"origin": "https://dashboard.example.com"},
        ) as ws:
            hello = ws.receive_json()
            assert hello["type"] == "connected"


# ── WebSocket role-gate tests (ADR-012) ──────────────────────────────


class TestWebSocketRoleGate:
    """api_key mode requires a valid ?api_key= (at least ``run``) to connect."""

    RUN_KEY = "test-run-key"
    ADMIN_KEY = "test-admin-key"

    @pytest.fixture(autouse=True)
    def _role_keys(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DASHBOARD_RUN_KEY", self.RUN_KEY)
        monkeypatch.setenv("DASHBOARD_ADMIN_KEY", self.ADMIN_KEY)
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")

    def _connect(self, url: str = "/ws/v1/dashboard") -> None:
        from starlette.websockets import WebSocketDisconnect

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        with (
            pytest.raises(WebSocketDisconnect),
            client.websocket_connect(url),
        ):
            pass

    def test_ws_rejects_missing_key_in_api_key_mode(self) -> None:
        """A handshake without ?api_key= must be refused with 1008."""
        self._connect()

    def test_ws_rejects_unknown_key_in_api_key_mode(self) -> None:
        """An unknown ?api_key= must be refused with 1008."""
        self._connect("/ws/v1/dashboard?api_key=not-a-real-key")

    def test_ws_accepts_run_key(self) -> None:
        """A valid run key must connect and receive the hello message."""
        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        with client.websocket_connect(f"/ws/v1/dashboard?api_key={self.RUN_KEY}") as ws:
            hello = ws.receive_json()
            assert hello["type"] == "connected"

    def test_ws_accepts_open_mode_without_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """open mode (loopback dev) connects with no key — admin role."""
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "open")
        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        with client.websocket_connect("/ws/v1/dashboard") as ws:
            hello = ws.receive_json()
            assert hello["type"] == "connected"


# ── WebSocket hardening tests ──────────────────────────────────────────


class TestWebSocketHardening:
    """Verify WS connection cap, topic allowlist, message-size and rate limits."""

    def _client(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "open")
        monkeypatch.delenv("DASHBOARD_API_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        (tmp_path / "company").mkdir(exist_ok=True)
        (tmp_path / "company" / "agent-registry.json").write_text("[]", encoding="utf-8")
        (tmp_path / ".opencode").mkdir(exist_ok=True)
        (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
        (tmp_path / "orchestrator").mkdir(exist_ok=True)
        (tmp_path / "orchestrator" / "approvals.yaml").write_text("requests: []", encoding="utf-8")
        (tmp_path / "orchestrator" / "escalation.yaml").write_text(
            "rules: []\nevents: []", encoding="utf-8"
        )
        from ai_company.dashboard.app import create_app

        return TestClient(create_app())

    def test_subscribe_rejects_unknown_topic(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Unknown topics are filtered out of the subscribe response."""
        client = self._client(monkeypatch, tmp_path)
        with client.websocket_connect("/ws/v1/dashboard") as ws:
            hello = ws.receive_json()
            assert hello["type"] == "connected"
            ws.send_json({"type": "subscribe", "topics": ["kpis", "secret-channel"]})
            resp = ws.receive_json()
            assert resp["type"] == "subscribed"
            assert resp["topics"] == ["kpis"]
            assert "secret-channel" in resp["invalid"]

    def test_subscribe_non_list_topics_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A non-list topics field must return an error, not crash."""
        client = self._client(monkeypatch, tmp_path)
        with client.websocket_connect("/ws/v1/dashboard") as ws:
            ws.receive_json()
            ws.send_json({"type": "subscribe", "topics": "kpis"})
            resp = ws.receive_json()
            assert resp["type"] == "error"

    def test_oversized_message_closes_connection(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Messages over the byte cap must close the connection with 1009."""
        monkeypatch.setenv("DASHBOARD_WS_MAX_MESSAGE_BYTES", "64")
        client = self._client(monkeypatch, tmp_path)
        with client.websocket_connect("/ws/v1/dashboard") as ws:
            ws.receive_json()
            ws.send_json({"type": "ping", "padding": "x" * 200})
            err = ws.receive_json()
            assert err["type"] == "error"

    def test_rate_limit_closes_connection(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Exceeding the inbound rate limit must close with 1008."""
        monkeypatch.setenv("DASHBOARD_WS_RATE_LIMIT_MESSAGES", "2")
        monkeypatch.setenv("DASHBOARD_WS_RATE_LIMIT_WINDOW_S", "10")
        from starlette.websockets import WebSocketDisconnect

        client = self._client(monkeypatch, tmp_path)
        with client.websocket_connect("/ws/v1/dashboard") as ws:
            ws.receive_json()
            ws.send_json({"type": "ping"})
            assert ws.receive_json()["type"] == "pong"
            ws.send_json({"type": "ping"})
            assert ws.receive_json()["type"] == "pong"
            # Third message within the window trips the 2-msg limit.
            ws.send_json({"type": "ping"})
            err = ws.receive_json()
            assert err["type"] == "error"
            with pytest.raises(WebSocketDisconnect):
                ws.receive_json()

    def test_pong_heartbeat_reply_acknowledged_silently(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A client pong (reply to a server heartbeat probe) gets no error frame."""
        client = self._client(monkeypatch, tmp_path)
        with client.websocket_connect("/ws/v1/dashboard") as ws:
            ws.receive_json()  # connected hello
            ws.send_json({"type": "pong"})
            # The next legitimate exchange must not be shadowed by an error
            # reply to the pong.
            ws.send_json({"type": "ping"})
            assert ws.receive_json()["type"] == "pong"

    def test_connection_cap_rejects_excess(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A connection beyond the cap must be refused with 1013."""
        monkeypatch.setenv("DASHBOARD_MAX_WS_CLIENTS", "1")
        from starlette.websockets import WebSocketDisconnect

        client = self._client(monkeypatch, tmp_path)
        with (
            client.websocket_connect("/ws/v1/dashboard") as ws,
            pytest.raises(WebSocketDisconnect) as exc_info,
        ):
            ws.receive_json()
            with client.websocket_connect("/ws/v1/dashboard"):
                pass
        assert exc_info.value.code == 1013


# ── WebSocket liveness sweep tests (C2) ───────────────────────────────


class _FakeWS:
    """Minimal WebSocket double for exercising the ConnectionManager."""

    def __init__(self) -> None:
        self.accepted = False
        self.closed_code: int | None = None
        self.closed_reason: str | None = None
        self.sent_text: list[str] = []

    async def accept(self) -> None:
        self.accepted = True

    async def close(self, code: int = 1000, reason: str | None = None) -> None:
        self.closed_code = code
        self.closed_reason = reason

    async def send_text(self, payload: str) -> None:
        self.sent_text.append(payload)

    async def send_json(self, payload: dict) -> None:
        pass


class _FailingSendWS(_FakeWS):
    """WebSocket double whose probe sends always fail (dead client)."""

    async def send_text(self, payload: str) -> None:
        raise RuntimeError("Simulated send failure")


class TestWebSocketLiveness:
    """Verify idle connections are reaped and health is observable (C2)."""

    async def test_idle_connections_are_reaped(self) -> None:
        import time as _time

        from ai_company.dashboard.ws import ConnectionManager

        manager = ConnectionManager()
        try:
            ws = _FakeWS()
            assert await manager.connect(ws) is True
            # Simulate a connection that has been silent far beyond the limit.
            manager._last_seen[id(ws)] = _time.monotonic() - 3600
            assert manager.active_count == 1

            reaped = await manager._idle_sweep_once()
            assert reaped == [ws]
            assert ws.closed_code == 1008
            assert ws.closed_reason == "Idle timeout"
            assert manager.active_count == 0
        finally:
            manager._stop_sweeper()

    async def test_recent_activity_prevents_reap(self) -> None:
        from ai_company.dashboard.ws import ConnectionManager

        manager = ConnectionManager()
        try:
            ws = _FakeWS()
            assert await manager.connect(ws) is True
            reaped = await manager._idle_sweep_once()
            assert reaped == []
            assert manager.active_count == 1
            assert ws.closed_code is None
        finally:
            await manager.disconnect(ws)
            manager._stop_sweeper()

    async def test_inbound_message_touches_last_seen(self) -> None:
        import time as _time

        from ai_company.dashboard.ws import ConnectionManager

        manager = ConnectionManager()
        try:
            ws = _FakeWS()
            assert await manager.connect(ws) is True
            manager._last_seen[id(ws)] = _time.monotonic() - 3600
            assert manager._check_rate_limit(id(ws)) is True  # any inbound message
            reaped = await manager._idle_sweep_once()
            assert reaped == []
            assert manager.active_count == 1
        finally:
            await manager.disconnect(ws)
            manager._stop_sweeper()

    async def test_zero_timeout_disables_sweep(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import time as _time

        monkeypatch.setenv("DASHBOARD_WS_IDLE_TIMEOUT_S", "0")
        from ai_company.dashboard.ws import ConnectionManager

        manager = ConnectionManager()
        try:
            ws = _FakeWS()
            assert await manager.connect(ws) is True
            manager._last_seen[id(ws)] = _time.monotonic() - 3600
            reaped = await manager._idle_sweep_once()
            assert reaped == []
            assert manager.active_count == 1
            assert ws.closed_code is None
        finally:
            await manager.disconnect(ws)
            manager._stop_sweeper()

    async def test_stats_reports_connection_health(self) -> None:
        from ai_company.dashboard.ws import ConnectionManager

        manager = ConnectionManager()
        try:
            ws1, ws2 = _FakeWS(), _FakeWS()
            assert await manager.connect(ws1)
            assert await manager.connect(ws2)
            await manager.subscribe(ws1, ["kpis", "alerts"])
            await manager.subscribe(ws2, ["kpis"])

            stats = manager.stats()
            assert stats["active_clients"] == 2
            assert stats["connection_cap"] >= 2
            assert stats["idle_timeout_s"] == 600
            assert stats["subscribed_topics"] == {"kpis": 2, "alerts": 1}
            assert stats["sweeps_run"] >= 0
        finally:
            await manager.disconnect(ws1)
            await manager.disconnect(ws2)
            manager._stop_sweeper()


# ── WebSocket server heartbeat probe tests (C2) ─────────────────────────


class TestWebSocketHeartbeat:
    """Verify the server-initiated heartbeat probe and its reap deadline."""

    async def test_probe_sent_after_silence(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import json
        import time as _time

        monkeypatch.setenv("DASHBOARD_WS_HEARTBEAT_INTERVAL_S", "30")
        monkeypatch.setenv("DASHBOARD_WS_PONG_TIMEOUT_S", "30")
        from ai_company.dashboard.ws import ConnectionManager

        manager = ConnectionManager()
        try:
            ws = _FakeWS()
            assert await manager.connect(ws) is True
            now = _time.monotonic()
            manager._last_seen[id(ws)] = now - 31

            reaped = await manager._idle_sweep_once(now=now)

            assert reaped == []
            assert manager.active_count == 1
            assert ws.closed_code is None
            assert len(ws.sent_text) == 1
            probe = json.loads(ws.sent_text[0])
            assert probe["type"] == "ping"
            assert probe["source"] == "server"
            assert id(ws) in manager._probe_sent_at
            assert manager._probes_sent == 1
        finally:
            await manager.disconnect(ws)
            manager._stop_sweeper()

    async def test_missed_pong_reaps(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import time as _time

        monkeypatch.setenv("DASHBOARD_WS_HEARTBEAT_INTERVAL_S", "30")
        monkeypatch.setenv("DASHBOARD_WS_PONG_TIMEOUT_S", "30")
        from ai_company.dashboard.ws import ConnectionManager

        manager = ConnectionManager()
        try:
            ws = _FakeWS()
            assert await manager.connect(ws) is True
            now = _time.monotonic()
            manager._last_seen[id(ws)] = now - 31
            # First pass probes; second pass (past the pong deadline) reaps.
            await manager._idle_sweep_once(now=now)
            assert manager.active_count == 1

            reaped = await manager._idle_sweep_once(now=now + 31)

            assert reaped == [ws]
            assert ws.closed_code == 1008
            assert ws.closed_reason == "No heartbeat response"
            assert manager.active_count == 0
        finally:
            manager._stop_sweeper()

    async def test_inbound_activity_clears_probe(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import time as _time

        monkeypatch.setenv("DASHBOARD_WS_HEARTBEAT_INTERVAL_S", "30")
        monkeypatch.setenv("DASHBOARD_WS_PONG_TIMEOUT_S", "30")
        from ai_company.dashboard.ws import ConnectionManager

        manager = ConnectionManager()
        try:
            ws = _FakeWS()
            assert await manager.connect(ws) is True
            now = _time.monotonic()
            manager._last_seen[id(ws)] = now - 31
            await manager._idle_sweep_once(now=now)
            assert id(ws) in manager._probe_sent_at

            # Any inbound message (a pong reply) clears the pending probe.
            assert manager._check_rate_limit(id(ws)) is True
            assert id(ws) not in manager._probe_sent_at

            reaped = await manager._idle_sweep_once(now=now + 31)
            assert reaped == []
            assert ws.closed_code is None
            assert manager.active_count == 1
        finally:
            await manager.disconnect(ws)
            manager._stop_sweeper()

    async def test_probe_disabled_when_interval_zero(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import time as _time

        monkeypatch.setenv("DASHBOARD_WS_HEARTBEAT_INTERVAL_S", "0")
        from ai_company.dashboard.ws import ConnectionManager

        manager = ConnectionManager()
        try:
            ws = _FakeWS()
            assert await manager.connect(ws) is True
            now = _time.monotonic()
            manager._last_seen[id(ws)] = now - 31

            reaped = await manager._idle_sweep_once(now=now)

            assert reaped == []
            assert len(ws.sent_text) == 0
            assert ws.closed_code is None
            assert manager.active_count == 1
        finally:
            await manager.disconnect(ws)
            manager._stop_sweeper()

    async def test_probe_send_failure_prunes_immediately(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import time as _time

        monkeypatch.setenv("DASHBOARD_WS_HEARTBEAT_INTERVAL_S", "30")
        from ai_company.dashboard.ws import ConnectionManager

        manager = ConnectionManager()
        try:
            ws = _FailingSendWS()
            assert await manager.connect(ws) is True
            now = _time.monotonic()
            manager._last_seen[id(ws)] = now - 31

            reaped = await manager._idle_sweep_once(now=now)

            assert reaped == [ws]
            assert ws.closed_code == 1008
            assert ws.closed_reason == "Heartbeat send failed"
            assert manager.active_count == 0
        finally:
            manager._stop_sweeper()

    async def test_stats_include_heartbeat(self) -> None:
        from ai_company.dashboard.ws import ConnectionManager

        manager = ConnectionManager()
        try:
            ws = _FakeWS()
            assert await manager.connect(ws) is True
            stats = manager.stats()
            assert stats["heartbeat_interval_s"] == 300
            assert stats["pong_timeout_s"] == 120
            assert stats["probes_sent"] == 0
            assert stats["probes_outstanding"] == 0
        finally:
            await manager.disconnect(ws)
            manager._stop_sweeper()
