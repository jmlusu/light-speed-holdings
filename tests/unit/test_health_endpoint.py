"""Tests for the dashboard /health endpoint.

Covers the deep health check response shape plus the ticket #61 / GAP-011
regressions: /health must read live state through the StateStore (never a
CWD-relative path) and report task counts from the live inbox.
"""

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from ai_company.dashboard.app import app
from ai_company.version import get_version


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


def test_health_reports_derived_api_version() -> None:
    """/health version must come from the single version source (ticket #64)."""
    client = TestClient(app)
    payload = client.get("/health").json()
    assert payload["version"] == get_version()
    assert payload["version"] != "0.2.0"


def test_health_is_cwd_independent(tmp_path: Path, monkeypatch) -> None:
    """/health must read state anchored at the StateStore, not the CWD.

    Regression for ticket #61: the old implementation checked
    ``Path(".opencode/inbox.json")`` relative to the process CWD, so health
    reported missing state when the dashboard ran from another directory.
    """
    # Seed a data root with the state files health checks.
    (tmp_path / ".opencode").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
    (tmp_path / ".opencode" / "agents").mkdir(exist_ok=True)
    (tmp_path / ".opencode" / "agents" / "test-agent.md").write_text("# a", encoding="utf-8")
    (tmp_path / ".opencode" / "audit").write_text("", encoding="utf-8")
    (tmp_path / "company").mkdir(exist_ok=True)
    (tmp_path / "company" / "agent-registry.json").write_text("[]", encoding="utf-8")
    (tmp_path / "company" / "models.yaml").write_text("models: []", encoding="utf-8")

    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))
    # Run from a directory that contains none of the state files.
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir(exist_ok=True)
    monkeypatch.chdir(elsewhere)

    from ai_company.dashboard.app import create_app

    client = TestClient(create_app())
    payload = client.get("/health").json()
    assert payload["checks"]["inbox"] == "ok"
    assert payload["checks"]["registry"] == "ok"
    assert payload["checks"]["agents"].startswith("ok")
    assert payload["checks"]["config"] == "ok"
    assert payload["checks"]["audit_log"].startswith("ok")


def test_health_reads_live_task_counts_from_inbox(tmp_path: Path, monkeypatch) -> None:
    """metrics_summary counts must reflect the live inbox (ticket #61)."""
    # Order-independence: the dashboard MessageBus and StateStore are
    # process-wide singletons that root at first use. Reset them so this test
    # always reads its own temp inbox rather than a stale/global root.
    import ai_company.dashboard.api as dash_api
    from ai_company.dashboard.repository import reset_state_store

    dash_api._bus = None
    reset_state_store()

    (tmp_path / ".opencode").mkdir(parents=True, exist_ok=True)
    tasks = [
        {"id": "t1", "status": "completed"},
        {"id": "t2", "status": "completed"},
        {"id": "t3", "status": "failed"},
        {"id": "t4", "status": "pending"},
    ]
    (tmp_path / ".opencode" / "inbox.json").write_text(json.dumps(tasks), encoding="utf-8")
    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))

    from ai_company.dashboard.app import create_app

    client = TestClient(create_app())
    summary = client.get("/health").json()["metrics_summary"]
    assert summary["tasks_total"] == 4
    assert summary["tasks_completed"] == 2
    assert summary["tasks_failed"] == 1
    assert summary["success_rate_pct"] == 50.0
