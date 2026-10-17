"""Unit tests for new read-only command center API endpoints.

Covers:
    - /health (monitoring.py) — deep health check
    - /api/v1/briefing (api.py) — executive briefing aggregation
    - /api/v1/models/telemetry (api.py) — per-model telemetry summary
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.app import app


@pytest.fixture()
def client(workspace: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """TestClient wired to the isolated workspace."""
    from ai_company.dashboard import api as dash_api
    from ai_company.dashboard.repository import get_state_store, reset_state_store

    dash_api._bus = None
    reset_state_store()
    get_state_store(workspace)
    return TestClient(app, raise_server_exceptions=False)


# ---------------------------------------------------------------------------
# /health endpoint
# ---------------------------------------------------------------------------


class TestHealthEndpoint:
    """GET /health — deep health check."""

    def test_health_returns_200(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_health_body_is_json(self, client: TestClient) -> None:
        resp = client.get("/health")
        data = resp.json()
        assert isinstance(data, dict)

    def test_health_contains_status(self, client: TestClient) -> None:
        resp = client.get("/health")
        data = resp.json()
        # Should have a top-level status indicator
        assert "status" in data or "ok" in data or "healthy" in str(data).lower()

    def test_health_checks_inbox(self, client: TestClient) -> None:
        resp = client.get("/health")
        data = resp.json()
        # The health endpoint checks inbox.json
        checks = data.get("checks", data)
        if isinstance(checks, dict) and "inbox" in checks:
            assert "ok" in checks["inbox"] or "missing" in checks["inbox"]


# ---------------------------------------------------------------------------
# /api/v1/briefing endpoint
# ---------------------------------------------------------------------------


class TestBriefingEndpoint:
    """GET /api/v1/briefing — executive briefing aggregation."""

    def test_briefing_returns_200(self, client: TestClient) -> None:
        resp = client.get("/api/v1/briefing")
        assert resp.status_code == 200

    def test_briefing_body_is_dict(self, client: TestClient) -> None:
        resp = client.get("/api/v1/briefing")
        data = resp.json()
        assert isinstance(data, dict)

    def test_briefing_has_items(self, client: TestClient) -> None:
        resp = client.get("/api/v1/briefing")
        data = resp.json()
        # Should have an items list (may be empty in isolated workspace)
        assert "items" in data
        assert isinstance(data["items"], list)

    def test_briefing_items_have_required_fields(self, client: TestClient) -> None:
        resp = client.get("/api/v1/briefing")
        data = resp.json()
        for item in data.get("items", []):
            assert "id" in item
            assert "title" in item
            assert "priority" in item
            assert item["priority"] in ("high", "medium", "low")


# ---------------------------------------------------------------------------
# /api/v1/models/telemetry endpoint
# ---------------------------------------------------------------------------


class TestModelTelemetryEndpoint:
    """GET /api/v1/models/telemetry — per-model telemetry summary."""

    def test_telemetry_returns_200(self, client: TestClient) -> None:
        resp = client.get("/api/v1/models/telemetry")
        assert resp.status_code == 200

    def test_telemetry_body_is_list(self, client: TestClient) -> None:
        resp = client.get("/api/v1/models/telemetry")
        data = resp.json()
        assert isinstance(data, list)

    def test_telemetry_empty_when_no_audit_data(self, client: TestClient) -> None:
        """Without audit log entries, telemetry should return an empty list."""
        resp = client.get("/api/v1/models/telemetry")
        data = resp.json()
        # In isolated workspace there's no audit data, so should be empty
        assert len(data) == 0

    def test_telemetry_item_shape(self, client: TestClient, workspace: Path) -> None:
        """When audit data exists, items should have the correct shape."""
        # Seed a minimal audit entry — the JSONL trail is a single file at
        # .opencode/audit (not a directory).
        audit_dir = workspace / ".opencode"
        audit_dir.mkdir(parents=True, exist_ok=True)
        event = {
            "event_type": "tool_result",
            "timestamp": "2026-08-19T00:00:00Z",
            "metadata": {
                "model": "big-pickle",
                "cost": 0.001,
                "latency_ms": 150.0,
            },
        }
        (audit_dir / "audit").write_text(json.dumps(event) + "\n", encoding="utf-8")

        # Re-point the StateStore to the test workspace
        from ai_company.dashboard.repository import configure_state_store

        configure_state_store(str(workspace))

        resp = client.get("/api/v1/models/telemetry")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1

        item = data[0]
        assert "model_id" in item
        assert "request_count" in item
        assert "success_rate" in item
        assert "avg_latency_ms" in item
        assert "total_cost_usd" in item
        assert item["model_id"] == "big-pickle"
        assert item["request_count"] == 1
