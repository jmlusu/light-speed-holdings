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
        """Default auth mode blocks GET/HEAD/OPTIONS when no key is set."""
        monkeypatch.delenv("DASHBOARD_API_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.delenv("DASHBOARD_AUTH_MODE", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.get("/health")
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
