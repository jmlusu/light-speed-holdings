"""Tests for the dashboard /health endpoint."""

from fastapi.testclient import TestClient

from ai_company.dashboard.app import app


def test_health_endpoint_returns_200() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200


def test_health_endpoint_contains_expected_keys() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    # The deep health check exposes status plus nested checks and metrics.
    assert "status" in payload
    assert "checks" in payload
    assert "metrics_summary" in payload
    for key in ("disk_space", "process_memory", "memory_store"):
        assert key in payload["checks"]
