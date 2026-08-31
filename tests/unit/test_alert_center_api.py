"""Contract tests for the CEO Alert Center API endpoints.

Covers ``GET /api/v1/alerts`` and the lifecycle write endpoints
(ack / snooze / clear / clear-all) using the isolated dashboard TestClient
(bound to a temp state root so ``AlertStore()`` resolves to ``tmp_path``).
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.alert_store import AlertStore
from ai_company.dashboard.analytics import Alert
from ai_company.dashboard.app import app


def _alert(rule_name: str = "High failure rate") -> Alert:
    return Alert(
        rule_name=rule_name,
        department="engineering",
        kpi_key="failure_rate",
        current_value=12.0,
        threshold=10.0,
        operator="gt",
        severity="critical",
        fired_at="2026-08-31T12:00:00+00:00",
        message=f"[CRITICAL] {rule_name}: engineering.failure_rate = 12.0",
    )


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.chdir(tmp_path)
    from ai_company.dashboard import api as dash_api
    from ai_company.dashboard.repository import get_state_store, reset_state_store
    from tests.fixtures.dashboard_data import patch_rate_limiter

    reset_state_store()
    get_state_store(tmp_path)
    dash_api._bus = None

    with patch_rate_limiter():
        yield TestClient(app, raise_server_exceptions=False)

    reset_state_store()
    dash_api._bus = None


class TestListAlerts:
    def test_list_empty(self, client: TestClient) -> None:
        resp = client.get("/api/v1/alerts")
        assert resp.status_code == 200
        body = resp.json()
        assert body["count"] == 0
        assert body["alerts"] == []

    def test_list_returns_persisted(self, client: TestClient, tmp_path: Path) -> None:
        AlertStore(base_dir=tmp_path / "dashboard").add([_alert()])
        resp = client.get("/api/v1/alerts")
        assert resp.status_code == 200
        body = resp.json()
        assert body["count"] == 1
        alert = body["alerts"][0]
        assert alert["rule_name"] == "High failure rate"
        assert alert["status"] == "active"
        assert "id" in alert

    def test_list_filters_by_status(self, client: TestClient, tmp_path: Path) -> None:
        store = AlertStore(base_dir=tmp_path / "dashboard")
        aid = store.add([_alert()])[0]
        store.acknowledge(aid)
        resp = client.get("/api/v1/alerts", params={"status": "acknowledged"})
        assert resp.status_code == 200
        assert resp.json()["count"] == 1
        resp = client.get("/api/v1/alerts", params={"status": "active"})
        assert resp.json()["count"] == 0


class TestLifecycle:
    def test_ack(self, client: TestClient, tmp_path: Path) -> None:
        store = AlertStore(base_dir=tmp_path / "dashboard")
        aid = store.add([_alert()])[0]
        resp = client.post(f"/api/v1/alerts/{aid}/ack")
        assert resp.status_code == 200
        assert resp.json()["status"] == "acknowledged"

    def test_snooze(self, client: TestClient, tmp_path: Path) -> None:
        store = AlertStore(base_dir=tmp_path / "dashboard")
        aid = store.add([_alert()])[0]
        resp = client.post(f"/api/v1/alerts/{aid}/snooze?until_hours=4")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "snoozed"
        assert body["snoozed_until"]

    def test_clear(self, client: TestClient, tmp_path: Path) -> None:
        store = AlertStore(base_dir=tmp_path / "dashboard")
        aid = store.add([_alert()])[0]
        resp = client.post(f"/api/v1/alerts/{aid}/clear")
        assert resp.status_code == 200
        assert resp.json()["status"] == "cleared"

    def test_clear_all(self, client: TestClient, tmp_path: Path) -> None:
        store = AlertStore(base_dir=tmp_path / "dashboard")
        store.add([_alert("r1")])
        store.add([_alert("r2")])
        resp = client.post("/api/v1/alerts/clear-all")
        assert resp.status_code == 200
        assert resp.json()["cleared"] == 2

    def test_unknown_id_404(self, client: TestClient) -> None:
        resp = client.post("/api/v1/alerts/missing/ack")
        assert resp.status_code == 404
