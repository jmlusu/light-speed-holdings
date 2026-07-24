"""Unit tests for API versioning (PRE-12).

Validates the versioning strategy:
- ``/api/v1/*`` endpoints respond correctly
- Legacy ``/api/*`` paths redirect (308) to ``/api/v1/*``
- ``API-Version`` header is present on versioned responses
- Deprecation headers on legacy redirects
- ``/api/version`` endpoint returns version metadata
- Mobile API versioned paths
- Monitoring endpoints are NOT versioned

Run:
    pytest tests/unit/test_api_versioning.py -v
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.app import app
from tests.fixtures.dashboard_data import patch_rate_limiter


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Isolated TestClient with fixture data."""
    monkeypatch.chdir(tmp_path)
    # PRE-03: set API key so POST/DELETE mutations are allowed in tests
    monkeypatch.setenv("DASHBOARD_API_KEY", "test-key-123")
    from ai_company.dashboard import api as dash_api
    from ai_company.dashboard.repository import get_state_store, reset_state_store

    reset_state_store()
    get_state_store(tmp_path)
    dash_api._bus = None

    from tests.fixtures.dashboard_data import seed_dashboard_workspace

    seed_dashboard_workspace(tmp_path, task_count=5, agent_count=3)

    with patch_rate_limiter():
        # follow_redirects=False so we can inspect redirect responses directly
        yield TestClient(app, raise_server_exceptions=False, follow_redirects=False)

    reset_state_store()
    dash_api._bus = None


# ---------------------------------------------------------------------------
# Versioned endpoint responses
# ---------------------------------------------------------------------------


class TestVersionedEndpoints:
    """Verify /api/v1/* endpoints respond with correct data and headers."""

    def test_versioned_dashboard_returns_200(self, client: TestClient) -> None:
        resp = client.get("/api/v1/dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert "pending_tasks" in data
        assert "uptime_seconds" in data

    def test_versioned_agents_returns_200(self, client: TestClient) -> None:
        resp = client.get("/api/v1/agents")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_versioned_tasks_returns_200(self, client: TestClient) -> None:
        resp = client.get("/api/v1/tasks")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_versioned_approvals_returns_200(self, client: TestClient) -> None:
        resp = client.get("/api/v1/approvals")
        assert resp.status_code == 200

    def test_versioned_departments_returns_200(self, client: TestClient) -> None:
        resp = client.get("/api/v1/departments")
        assert resp.status_code == 200

    def test_versioned_models_returns_200(self, client: TestClient) -> None:
        resp = client.get("/api/v1/models")
        assert resp.status_code == 200

    def test_versioned_kpis_returns_200(self, client: TestClient) -> None:
        resp = client.get("/api/v1/kpis")
        assert resp.status_code == 200

    def test_versioned_scheduler_returns_200(self, client: TestClient) -> None:
        resp = client.get("/api/v1/scheduler")
        assert resp.status_code == 200

    def test_versioned_org_chart_returns_200(self, client: TestClient) -> None:
        resp = client.get("/api/v1/org-chart")
        assert resp.status_code == 200

    def test_versioned_metrics_returns_200(self, client: TestClient) -> None:
        resp = client.get("/api/v1/metrics")
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# API-Version header
# ---------------------------------------------------------------------------


class TestAPIVersionHeader:
    """Verify API-Version header is present on versioned responses."""

    def test_version_header_on_dashboard(self, client: TestClient) -> None:
        resp = client.get("/api/v1/dashboard")
        assert resp.status_code == 200
        assert "API-Version" in resp.headers
        assert resp.headers["API-Version"] == "v1"

    def test_version_header_on_agents(self, client: TestClient) -> None:
        resp = client.get("/api/v1/agents")
        assert resp.headers.get("API-Version") == "v1"

    def test_version_header_on_tasks(self, client: TestClient) -> None:
        resp = client.get("/api/v1/tasks")
        assert resp.headers.get("API-Version") == "v1"

    def test_version_header_on_post_task(self, client: TestClient) -> None:
        resp = client.post(
            "/api/v1/tasks",
            json={
                "receiver_id": "chief-of-staff",
                "instruction": "Create versioned task",
            },
            headers={"X-API-Key": "test-key-123"},
        )
        assert resp.status_code == 201
        assert resp.headers.get("API-Version") == "v1"

    def test_no_version_header_on_health(self, client: TestClient) -> None:
        """Health check is not under /api/v1/ so should not have the header."""
        resp = client.get("/health")
        assert resp.status_code == 200
        assert "API-Version" not in resp.headers


# ---------------------------------------------------------------------------
# Legacy redirect behavior
# ---------------------------------------------------------------------------


class TestLegacyRedirects:
    """Verify /api/* redirects to /api/v1/* with deprecation headers."""

    def test_legacy_dashboard_redirects_to_v1(self, client: TestClient) -> None:
        resp = client.get("/api/dashboard")
        assert resp.status_code == 308
        assert "/api/v1/dashboard" in resp.headers["Location"]

    def test_legacy_agents_redirects_to_v1(self, client: TestClient) -> None:
        resp = client.get("/api/agents")
        assert resp.status_code == 308
        assert "/api/v1/agents" in resp.headers["Location"]

    def test_legacy_tasks_redirects_to_v1(self, client: TestClient) -> None:
        resp = client.get("/api/tasks")
        assert resp.status_code == 308
        assert "/api/v1/tasks" in resp.headers["Location"]

    def test_legacy_approvals_redirects_to_v1(self, client: TestClient) -> None:
        resp = client.get("/api/approvals")
        assert resp.status_code == 308
        assert "/api/v1/approvals" in resp.headers["Location"]

    def test_redirect_has_deprecation_header(self, client: TestClient) -> None:
        resp = client.get("/api/dashboard")
        assert resp.headers.get("Deprecation") == "true"

    def test_redirect_has_sunset_header(self, client: TestClient) -> None:
        resp = client.get("/api/dashboard")
        assert "Sunset" in resp.headers
        # Sunset should be a valid HTTP-date
        sunset = resp.headers["Sunset"]
        assert "2027" in sunset

    def test_redirect_has_api_version_header(self, client: TestClient) -> None:
        resp = client.get("/api/dashboard")
        assert resp.headers.get("API-Version") == "v1"

    def test_redirect_preserves_query_string(self, client: TestClient) -> None:
        resp = client.get("/api/tasks?status=pending")
        assert resp.status_code == 308
        location = resp.headers["Location"]
        assert "/api/v1/tasks" in location
        assert "status=pending" in location

    def test_legacy_post_task_redirects(self, client: TestClient) -> None:
        """308 preserves the HTTP method, so POST should redirect correctly."""
        resp = client.post(
            "/api/tasks",
            json={
                "receiver_id": "chief-of-staff",
                "instruction": "Test legacy redirect for POST",
            },
        )
        assert resp.status_code == 308
        assert "/api/v1/tasks" in resp.headers["Location"]

    def test_legacy_mobile_redirects_to_v1(self, client: TestClient) -> None:
        resp = client.get("/api/mobile/dashboard")
        assert resp.status_code == 308
        assert "/api/v1/mobile/dashboard" in resp.headers["Location"]


# ---------------------------------------------------------------------------
# Redirect follows work (TestClient follows by default)
# ---------------------------------------------------------------------------


class TestRedirectFollows:
    """Verify that following redirects reaches the actual endpoint."""

    @pytest.fixture()
    def follow_client(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
        """TestClient that follows redirects (default behavior)."""
        monkeypatch.chdir(tmp_path)
        # PRE-03: set API key so POST/DELETE mutations are allowed in tests
        monkeypatch.setenv("DASHBOARD_API_KEY", "test-key-123")
        from ai_company.dashboard import api as dash_api
        from ai_company.dashboard.repository import get_state_store, reset_state_store

        reset_state_store()
        get_state_store(tmp_path)
        dash_api._bus = None

        from tests.fixtures.dashboard_data import seed_dashboard_workspace

        seed_dashboard_workspace(tmp_path, task_count=3, agent_count=3)

        with patch_rate_limiter():
            yield TestClient(app, raise_server_exceptions=False, follow_redirects=True)

        reset_state_store()
        dash_api._bus = None

    def test_follow_legacy_dashboard_returns_data(self, follow_client: TestClient) -> None:
        """Following the redirect from /api/dashboard should return KPI data."""
        resp = follow_client.get("/api/dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert "pending_tasks" in data

    def test_follow_legacy_agents_returns_list(self, follow_client: TestClient) -> None:
        resp = follow_client.get("/api/agents")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_follow_legacy_post_creates_task(self, follow_client: TestClient) -> None:
        resp = follow_client.post(
            "/api/tasks",
            json={
                "receiver_id": "chief-of-staff",
                "instruction": "Review the quarterly budget forecast",
            },
            headers={"X-API-Key": "test-key-123"},
        )
        assert resp.status_code == 201
        task = resp.json()
        assert task["status"] == "pending"


# ---------------------------------------------------------------------------
# Version info endpoint
# ---------------------------------------------------------------------------


class TestVersionInfoEndpoint:
    """Verify the /api/version discovery endpoint."""

    def test_version_info_returns_200(self, client: TestClient) -> None:
        resp = client.get("/api/version")
        assert resp.status_code == 200

    def test_version_info_shape(self, client: TestClient) -> None:
        resp = client.get("/api/version")
        data = resp.json()
        assert data["current_version"] == "v1"
        assert data["latest_version"] == "v1"
        assert isinstance(data["deprecated_versions"], list)
        assert "sunset_date" in data

    def test_version_info_not_versioned(self, client: TestClient) -> None:
        """/api/version is not under /api/v1/, so no API-Version header."""
        resp = client.get("/api/version")
        assert "API-Version" not in resp.headers


# ---------------------------------------------------------------------------
# Mobile API versioning
# ---------------------------------------------------------------------------


class TestMobileAPIVersioning:
    """Verify mobile API endpoints are under /api/v1/mobile/."""

    def test_mobile_dashboard_versioned(self, client: TestClient) -> None:
        resp = client.get("/api/v1/mobile/dashboard")
        assert resp.status_code == 200
        assert resp.headers.get("API-Version") == "v1"

    def test_mobile_tasks_versioned(self, client: TestClient) -> None:
        resp = client.get("/api/v1/mobile/tasks")
        assert resp.status_code == 200
        assert resp.headers.get("API-Version") == "v1"

    def test_mobile_kpis_compact_versioned(self, client: TestClient) -> None:
        resp = client.get("/api/v1/mobile/kpis/compact")
        assert resp.status_code == 200
        assert resp.headers.get("API-Version") == "v1"

    def test_legacy_mobile_redirects(self, client: TestClient) -> None:
        resp = client.get("/api/mobile/dashboard")
        assert resp.status_code == 308
        assert "/api/v1/mobile/dashboard" in resp.headers["Location"]


# ---------------------------------------------------------------------------
# Non-versioned endpoints
# ---------------------------------------------------------------------------


class TestNonVersionedEndpoints:
    """Verify monitoring/ops endpoints are NOT under /api/v1/."""

    def test_health_not_versioned(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert "API-Version" not in resp.headers

    def test_metrics_not_versioned(self, client: TestClient) -> None:
        """The monitoring router's /metrics is at root level, not /api/v1/."""
        resp = client.get("/metrics")
        # May be 200 or 404 depending on monitoring router availability
        assert resp.status_code in (200, 404)
        # Even if it exists, it should NOT have the version header
        if resp.status_code == 200:
            assert "API-Version" not in resp.headers

    def test_root_page_not_versioned(self, client: TestClient) -> None:
        resp = client.get("/")
        assert resp.status_code == 200
        assert "API-Version" not in resp.headers
