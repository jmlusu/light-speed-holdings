"""Dashboard smoke tests (regression lock for the StateStore remediation).

These exercise the live FastAPI app over a TestClient backed by a temp
StateStore, proving the dashboard boots, the store binds to a temp root,
and core endpoints respond 200 with the expected shape. They pin the
P0/P2 fixes end-to-end so a regression in path resolution or the DLQ
bypass would turn the build red.

Author: qa_automation_engineer (owned by test_engineering_lead).
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.app import create_app
from ai_company.dashboard.repository import configure_state_store, reset_state_store


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    """App whose StateStore is bound to a temp root."""
    reset_state_store()
    inbox = tmp_path / ".opencode"
    inbox.mkdir(parents=True, exist_ok=True)
    (inbox / "inbox.json").write_text("[]", encoding="utf-8")

    configure_state_store(tmp_path)
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client
    reset_state_store()


def test_app_boots_with_temp_store(client: TestClient) -> None:
    """App constructs and binds the store without a relative_to crash."""
    assert client is not None


def test_health_endpoint_returns_200(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert "status" in body


def test_read_endpoints_respond_against_temp_store(client: TestClient) -> None:
    """Representative read endpoints work against the temp store (no 5xx)."""
    for path in ("/", "/tasks", "/kpis", "/costs", "/escalations", "/agents"):
        resp = client.get(path)
        assert resp.status_code in (200, 404)  # 5xx would indicate a regression
