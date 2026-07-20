"""Tests for GAP-010 — dashboard CORS, API key, and rate-limiting security."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient


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
            "/api/dashboard",
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
            "/api/dashboard",
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
            "/api/dashboard",
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
            "/api/dashboard",
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
            "/api/dashboard",
            headers={
                "Origin": "https://any-origin.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert resp.headers.get("access-control-allow-origin", "") != "*"


# ── API key authentication tests ──────────────────────────────────────


class TestAPIKeyAuth:
    """Verify that write endpoints require an API key when configured."""

    def test_read_without_api_key_works(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """GET requests should always work without an API key."""
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/dashboard")
        assert resp.status_code == 200

    def test_write_without_api_key_rejected(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """POST requests without API key should be rejected when key is set."""
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.post(
            "/api/tasks",
            json={"receiver_id": "agent", "instruction": "do something"},
        )
        assert resp.status_code == 401
        assert "API key" in resp.json()["detail"]

    def test_write_with_valid_api_key_accepted(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """POST requests with correct API key should succeed."""
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.post(
            "/api/tasks",
            json={"receiver_id": "agent", "instruction": "do something"},
            headers={"X-API-Key": "secret-key-123"},
        )
        assert resp.status_code == 201

    def test_write_with_wrong_api_key_rejected(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """POST requests with wrong API key should be rejected."""
        monkeypatch.setenv("DASHBOARD_API_KEY", "secret-key-123")
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.post(
            "/api/tasks",
            json={"receiver_id": "agent", "instruction": "do something"},
            headers={"X-API-Key": "wrong-key"},
        )
        assert resp.status_code == 401

    def test_no_api_key_configured_allows_all(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """When DASHBOARD_API_KEY is not set, all requests pass (open mode)."""
        monkeypatch.delenv("DASHBOARD_API_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
        monkeypatch.chdir(tmp_path)
        self._setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        app = create_app()
        client = TestClient(app)
        resp = client.post(
            "/api/tasks",
            json={"receiver_id": "agent", "instruction": "do something"},
        )
        assert resp.status_code == 201

    @staticmethod
    def _setup_minimal_data(tmp_path: Path) -> None:
        (tmp_path / "company").mkdir(exist_ok=True)
        (tmp_path / "company" / "agent-registry.json").write_text("[]", encoding="utf-8")
        (tmp_path / ".opencode").mkdir(exist_ok=True)
        (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
        (tmp_path / "orchestrator").mkdir(exist_ok=True)
        (tmp_path / "orchestrator" / "approvals.yaml").write_text("requests: []", encoding="utf-8")
        (tmp_path / "orchestrator" / "escalation.yaml").write_text("rules: []\nevents: []", encoding="utf-8")
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
            assert limiter.is_allowed("test-ip")

    def test_rate_limit_blocks_excess(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Requests beyond the limit should be blocked."""
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "3")
        monkeypatch.delenv("DASHBOARD_API_KEY", raising=False)

        from ai_company.dashboard.app import _RateLimiter

        limiter = _RateLimiter(max_requests=3, window_seconds=60)
        assert limiter.is_allowed("test-ip") is True
        assert limiter.is_allowed("test-ip") is True
        assert limiter.is_allowed("test-ip") is True
        assert limiter.is_allowed("test-ip") is False

    def test_different_ips_have_separate_limits(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Different client IPs should be tracked independently."""
        monkeypatch.delenv("DASHBOARD_API_KEY", raising=False)

        from ai_company.dashboard.app import _RateLimiter

        limiter = _RateLimiter(max_requests=2, window_seconds=60)
        assert limiter.is_allowed("ip-a") is True
        assert limiter.is_allowed("ip-a") is True
        assert limiter.is_allowed("ip-a") is False
        # Different IP should still be allowed
        assert limiter.is_allowed("ip-b") is True
