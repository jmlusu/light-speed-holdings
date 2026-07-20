"""Tests for the CEO dashboard API endpoints."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from ai_company.dashboard.app import app

client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture()
def setup_dashboard_data(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Create fixture data files and patch paths used by the API."""

    # Patch working directory to tmp_path
    monkeypatch.chdir(tmp_path)

    # Rebind the dashboard StateStore singleton to the isolated workspace so
    # all state I/O is rooted at tmp_path (independent of cwd / import-time
    # singleton). Fixes pre-existing fixture isolation for the module-level
    # ``client`` created at import time.
    from ai_company.dashboard.repository import get_state_store, reset_state_store

    reset_state_store()
    get_state_store(tmp_path)

    # Create company directory and registry
    (tmp_path / "company").mkdir()
    registry = [
        {
            "name": "chief-of-staff",
            "role": "Chief of Staff",
            "type": "executive",
            "department": "Executive",
            "reportsTo": "human-ceo",
            "directReports": ["lead-engineering", "lead-marketing"],
            "description": "Coordinates all departments",
        },
        {
            "name": "lead-engineering",
            "role": "Lead Engineer",
            "type": "specialist",
            "department": "Engineering",
            "reportsTo": "chief-of-staff",
            "directReports": [],
            "description": "Leads engineering efforts",
        },
        {
            "name": "lead-marketing",
            "role": "Marketing Lead",
            "type": "specialist",
            "department": "Marketing",
            "reportsTo": "chief-of-staff",
            "directReports": [],
            "description": "Leads marketing efforts",
        },
    ]
    (tmp_path / "company" / "agent-registry.json").write_text(
        json.dumps(registry), encoding="utf-8"
    )

    # Create departments yaml
    departments = {
        "departments": [
            {
                "name": "Executive",
                "executive": "chief-of-staff",
                "agents": ["chief-of-staff"],
                "total_agents": 1,
            },
            {
                "name": "Engineering",
                "executive": "lead-engineering",
                "agents": ["lead-engineering"],
                "total_agents": 1,
            },
        ]
    }
    (tmp_path / "company" / "departments.yaml").write_text(
        yaml.dump(departments), encoding="utf-8"
    )

    # Create orchestrator directories
    (tmp_path / "orchestrator").mkdir(exist_ok=True)
    (tmp_path / ".opencode").mkdir(exist_ok=True)

    # Empty inbox
    (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")

    # Empty approvals
    (tmp_path / "orchestrator" / "approvals.yaml").write_text(
        yaml.dump({"requests": []}), encoding="utf-8"
    )

    # Empty escalation
    (tmp_path / "orchestrator" / "escalation.yaml").write_text(
        yaml.dump({"rules": [], "events": []}), encoding="utf-8"
    )

    # Copy models.yaml into tmp_path/company so ModelRouter can find it
    import shutil

    real_models = Path(__file__).resolve().parents[2] / "company" / "models.yaml"
    if real_models.exists():
        shutil.copy2(str(real_models), str(tmp_path / "company" / "models.yaml"))

    # Copy kpis.yaml into tmp_path/company/config/ for KPI endpoints
    real_kpis = Path(__file__).resolve().parents[2] / "company" / "config" / "kpis.yaml"
    if real_kpis.exists():
        config_dir = tmp_path / "company" / "config"
        config_dir.mkdir(exist_ok=True)
        shutil.copy2(str(real_kpis), str(config_dir / "kpis.yaml"))

    # Empty scheduler
    (tmp_path / "orchestrator" / "scheduler.yaml").write_text(
        yaml.dump({"tasks": []}), encoding="utf-8"
    )


class TestDashboardKPIs:
    def test_get_dashboard_returns_kpis(self, setup_dashboard_data: None) -> None:
        resp = client.get("/api/dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert "pending_tasks" in data
        assert "total_agents" in data
        assert data["total_agents"] == 3
        assert "uptime_seconds" in data

    def test_dashboard_tasks_count(self, setup_dashboard_data: None) -> None:
        # Add tasks with different statuses
        inbox_path = Path(".opencode/inbox.json")
        tasks = [
            {"id": "t1", "sender_id": "a", "receiver_id": "b", "instruction": "do x", "status": "pending"},
            {"id": "t2", "sender_id": "a", "receiver_id": "b", "instruction": "do y", "status": "completed"},
            {"id": "t3", "sender_id": "a", "receiver_id": "b", "instruction": "do z", "status": "in_progress"},
        ]
        inbox_path.write_text(json.dumps(tasks), encoding="utf-8")

        resp = client.get("/api/dashboard")
        data = resp.json()
        assert data["pending_tasks"] == 1
        assert data["completed_tasks"] == 1
        assert data["in_progress_tasks"] == 1


class TestAgents:
    def test_list_agents(self, setup_dashboard_data: None) -> None:
        resp = client.get("/api/agents")
        assert resp.status_code == 200
        agents = resp.json()
        assert len(agents) == 3
        names = {a["name"] for a in agents}
        assert "chief-of-staff" in names

    def test_get_agent_by_name(self, setup_dashboard_data: None) -> None:
        resp = client.get("/api/agents/chief-of-staff")
        assert resp.status_code == 200
        assert resp.json()["role"] == "Chief of Staff"

    def test_get_agent_not_found(self, setup_dashboard_data: None) -> None:
        resp = client.get("/api/agents/nonexistent")
        assert resp.status_code == 404


class TestOrgChart:
    def test_org_chart_structure(self, setup_dashboard_data: None) -> None:
        resp = client.get("/api/org-chart")
        assert resp.status_code == 200
        chart = resp.json()
        assert len(chart) >= 1
        root = chart[0]
        assert root["name"] == "chief-of-staff"
        assert len(root["children"]) == 2


class TestTasks:
    def test_list_tasks_empty(self, setup_dashboard_data: None) -> None:
        resp = client.get("/api/tasks")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_create_task(self, setup_dashboard_data: None) -> None:
        resp = client.post(
            "/api/tasks",
            json={"receiver_id": "lead-engineering", "instruction": "Build API"},
        )
        assert resp.status_code == 201
        task = resp.json()
        assert task["receiver_id"] == "lead-engineering"
        assert task["status"] == "pending"
        assert task["priority"] == "medium"

    def test_list_tasks_after_create(self, setup_dashboard_data: None) -> None:
        client.post(
            "/api/tasks",
            json={"receiver_id": "lead-engineering", "instruction": "Build API"},
        )
        resp = client.get("/api/tasks")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_list_tasks_filter_status(self, setup_dashboard_data: None) -> None:
        client.post(
            "/api/tasks",
            json={"receiver_id": "lead-engineering", "instruction": "Build API"},
        )
        resp = client.get("/api/tasks?status=completed")
        assert resp.status_code == 200
        assert resp.json() == []


class TestApprovals:
    def test_approve_request(self, setup_dashboard_data: None) -> None:
        approvals_path = Path("orchestrator/approvals.yaml")
        data = {
            "requests": [
                {
                    "id": "req-1",
                    "task_id": "t-1",
                    "agent_id": "lead-engineering",
                    "action": "deploy",
                    "description": "Deploy to prod",
                    "status": "pending",
                }
            ]
        }
        approvals_path.write_text(yaml.dump(data), encoding="utf-8")

        resp = client.post("/api/approvals/req-1/approve")
        assert resp.status_code == 200
        assert resp.json()["ok"] is True

        # Verify it's no longer pending
        resp = client.get("/api/approvals")
        assert resp.status_code == 200
        assert len(resp.json()) == 0

    def test_reject_request(self, setup_dashboard_data: None) -> None:
        approvals_path = Path("orchestrator/approvals.yaml")
        data = {
            "requests": [
                {
                    "id": "req-2",
                    "task_id": "t-2",
                    "agent_id": "lead-marketing",
                    "action": "campaign",
                    "description": "Launch campaign",
                    "status": "pending",
                }
            ]
        }
        approvals_path.write_text(yaml.dump(data), encoding="utf-8")

        resp = client.post("/api/approvals/req-2/reject")
        assert resp.status_code == 200
        assert resp.json()["ok"] is True

    def test_approve_nonexistent(self, setup_dashboard_data: None) -> None:
        resp = client.post("/api/approvals/nonexistent/approve")
        assert resp.status_code == 404


class TestEscalations:
    def test_resolve_escalation(self, setup_dashboard_data: None) -> None:
        esc_path = Path("orchestrator/escalation.yaml")
        data = {
            "events": [
                {
                    "task_id": "esc-1",
                    "rule_id": "timeout",
                    "from_agent": "a",
                    "to_agent": "b",
                    "reason": "took too long",
                    "resolved": False,
                }
            ]
        }
        esc_path.write_text(yaml.dump(data), encoding="utf-8")

        resp = client.post("/api/escalations/esc-1/resolve")
        assert resp.status_code == 200
        assert resp.json()["ok"] is True

    def test_resolve_nonexistent(self, setup_dashboard_data: None) -> None:
        resp = client.post("/api/escalations/nonexistent/resolve")
        assert resp.status_code == 404


class TestDepartments:
    def test_list_departments(self, setup_dashboard_data: None) -> None:
        resp = client.get("/api/departments")
        assert resp.status_code == 200
        depts = resp.json()
        assert len(depts) == 2


class TestModels:
    def test_list_model_routes(self, setup_dashboard_data: None) -> None:
        resp = client.get("/api/models")
        assert resp.status_code == 200
        routes = resp.json()
        assert len(routes) >= 1
        assert all("agent" in r for r in routes)

    def test_list_model_tiers(self, setup_dashboard_data: None) -> None:
        resp = client.get("/api/models/tiers")
        assert resp.status_code == 200
        tiers = resp.json()
        assert len(tiers) == 3
        tier_ids = {t["id"] for t in tiers}
        assert "fast" in tier_ids
        assert "standard" in tier_ids
        assert "premium" in tier_ids


class TestScheduler:
    def test_list_scheduled(self, setup_dashboard_data: None) -> None:
        resp = client.get("/api/scheduler")
        assert resp.status_code == 200
        assert resp.json() == []


class TestKpiEndpoints:
    """Contract tests for the department KPI API endpoints."""

    def test_get_department_kpis(self, setup_dashboard_data: None) -> None:
        """GET /api/departments/{name}/kpis returns KPI definitions."""
        resp = client.get("/api/departments/engineering/kpis")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Engineering"
        assert "kpis" in data
        assert len(data["kpis"]) > 0
        # Each KPI must have required fields
        for kpi in data["kpis"]:
            assert "id" in kpi
            assert "name" in kpi
            assert "target" in kpi
            assert "unit" in kpi
            assert "frequency" in kpi

    def test_get_department_kpis_not_found(self, setup_dashboard_data: None) -> None:
        resp = client.get("/api/departments/nonexistent/kpis")
        assert resp.status_code == 404

    def test_list_all_kpis(self, setup_dashboard_data: None) -> None:
        resp = client.get("/api/kpis")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, dict)
        assert "engineering" in data
        assert len(data["engineering"]["kpis"]) > 0

    def test_kpi_summary(self, setup_dashboard_data: None) -> None:
        resp = client.get("/api/kpis/summary")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # Each summary item must have required fields
        for item in data:
            assert "department" in item
            assert "kpi_id" in item
            assert "name" in item
            assert "target" in item
            assert "unit" in item
            assert "frequency" in item
