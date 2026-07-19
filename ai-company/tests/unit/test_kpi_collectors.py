"""Tests for the per-department KPI collectors."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from ai_company.dashboard.kpis import ALL_COLLECTORS, collect_all_kpis
from ai_company.dashboard.kpis.base import KPICollector
from ai_company.dashboard.kpis.customer_success import CustomerSuccessKPICollector
from ai_company.dashboard.kpis.engineering import EngineeringKPICollector
from ai_company.dashboard.kpis.finance import FinanceKPICollector
from ai_company.dashboard.kpis.hr import HRKPICollector
from ai_company.dashboard.kpis.legal import LegalKPICollector
from ai_company.dashboard.kpis.marketing import MarketingKPICollector
from ai_company.dashboard.kpis.sales import SalesKPICollector


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def project(tmp_path: Path) -> Path:
    """Create a minimal project tree for collectors to read from."""
    # .opencode/inbox.json with a mix of statuses
    (tmp_path / ".opencode").mkdir()
    tasks = [
        {"id": "t1", "sender_id": "a", "receiver_id": "b", "instruction": "x", "status": "pending"},
        {"id": "t2", "sender_id": "a", "receiver_id": "b", "instruction": "y", "status": "completed"},
        {"id": "t3", "sender_id": "a", "receiver_id": "b", "instruction": "z", "status": "completed"},
        {"id": "t4", "sender_id": "a", "receiver_id": "b", "instruction": "w", "status": "failed"},
        {"id": "t5", "sender_id": "a", "receiver_id": "b", "instruction": "v", "status": "in_progress"},
    ]
    (tmp_path / ".opencode" / "inbox.json").write_text(json.dumps(tasks), encoding="utf-8")

    # orchestrator/escalation.yaml
    (tmp_path / "orchestrator").mkdir()
    escalation = {
        "rules": [],
        "events": [
            {"task_id": "e1", "rule_id": "r1", "from_agent": "a", "to_agent": "b",
             "reason": "timeout", "resolved": False},
            {"task_id": "e2", "rule_id": "r1", "from_agent": "a", "to_agent": "b",
             "reason": "timeout", "resolved": True},
        ],
    }
    (tmp_path / "orchestrator" / "escalation.yaml").write_text(
        yaml.dump(escalation), encoding="utf-8"
    )

    # orchestrator/scheduler.yaml
    (tmp_path / "orchestrator" / "scheduler.yaml").write_text(
        yaml.dump({"tasks": [{"name": "daily-sync"}]}), encoding="utf-8"
    )

    # company/agent-registry.json
    (tmp_path / "company").mkdir()
    registry = [
        {"name": "cto", "role": "CTO", "type": "executive", "department": "Technology",
         "reportsTo": "ceo", "directReports": [], "description": "CTO"},
        {"name": "lead_backend", "role": "Backend Lead", "type": "specialist",
         "department": "Technology", "reportsTo": "cto", "directReports": [],
         "description": "Backend"},
        {"name": "cmo", "role": "CMO", "type": "executive", "department": "Marketing",
         "reportsTo": "ceo", "directReports": [], "description": "CMO"},
    ]
    (tmp_path / "company" / "agent-registry.json").write_text(
        json.dumps(registry), encoding="utf-8"
    )

    # company/departments.yaml
    departments = {
        "departments": [
            {"name": "Technology", "executive": "cto", "agents": ["lead_backend"],
             "totalAgents": 8},
            {"name": "Marketing", "executive": "cmo", "agents": [],
             "totalAgents": 1},
            {"name": "Finance", "executive": "cfo", "agents": [],
             "totalAgents": 0},
        ]
    }
    (tmp_path / "company" / "departments.yaml").write_text(
        yaml.dump(departments), encoding="utf-8"
    )

    # company/config/kpis.yaml (minimal)
    (tmp_path / "company" / "config").mkdir(parents=True)
    kpis = {
        "departments": {
            "finance": {
                "name": "Finance",
                "kpis": [
                    {"id": "budget_utilization", "name": "Budget Utilization",
                     "unit": "%", "target": 90, "frequency": "monthly"},
                ],
            }
        }
    }
    (tmp_path / "company" / "config" / "kpis.yaml").write_text(
        yaml.dump(kpis), encoding="utf-8"
    )

    return tmp_path


@pytest.fixture()
def empty_project(tmp_path: Path) -> Path:
    """An empty project tree — all collectors should handle missing files."""
    return tmp_path


# ---------------------------------------------------------------------------
# Engineering
# ---------------------------------------------------------------------------

class TestEngineeringCollector:
    def test_collects_task_counts(self, project: Path) -> None:
        result = EngineeringKPICollector(project).collect()
        assert result["department"] == "engineering"
        kpis = result["kpis"]

        assert kpis["total_tasks"]["current"] == 5
        assert kpis["pending_tasks"]["current"] == 1
        assert kpis["in_progress_tasks"]["current"] == 1
        assert kpis["completed_tasks"]["current"] == 2
        assert kpis["failed_tasks"]["current"] == 1

    def test_completion_rate(self, project: Path) -> None:
        result = EngineeringKPICollector(project).collect()
        rate = result["kpis"]["task_completion_rate"]["current"]
        # 2 completed / 5 total = 40%
        assert rate == 40.0

    def test_escalation_counts(self, project: Path) -> None:
        result = EngineeringKPICollector(project).collect()
        assert result["kpis"]["open_escalations"]["current"] == 1
        assert result["kpis"]["escalation_rate"]["current"] == 40.0  # 2 events / 5 tasks

    def test_scheduled_tasks(self, project: Path) -> None:
        result = EngineeringKPICollector(project).collect()
        assert result["kpis"]["scheduled_tasks"]["current"] == 1

    def test_missing_files(self, empty_project: Path) -> None:
        result = EngineeringKPICollector(empty_project).collect()
        assert result["department"] == "engineering"
        assert result["kpis"]["total_tasks"]["current"] == 0
        assert result["kpis"]["open_escalations"]["current"] == 0


# ---------------------------------------------------------------------------
# HR
# ---------------------------------------------------------------------------

class TestHRCollector:
    def test_total_agents(self, project: Path) -> None:
        result = HRKPICollector(project).collect()
        assert result["kpis"]["total_agents"]["current"] == 3

    def test_agents_by_department(self, project: Path) -> None:
        result = HRKPICollector(project).collect()
        breakdown = result["kpis"]["agents_by_department"]["current"]
        assert breakdown["Technology"] == 2
        assert breakdown["Marketing"] == 1

    def test_department_coverage(self, project: Path) -> None:
        result = HRKPICollector(project).collect()
        # 2 of 3 declared departments have agents (Technology=8, Marketing=1, Finance=0)
        assert result["kpis"]["department_coverage"]["current"] == pytest.approx(66.7, abs=0.1)

    def test_missing_files(self, empty_project: Path) -> None:
        result = HRKPICollector(empty_project).collect()
        assert result["kpis"]["total_agents"]["current"] == 0
        assert result["kpis"]["department_coverage"]["current"] == 0.0


# ---------------------------------------------------------------------------
# Finance
# ---------------------------------------------------------------------------

class TestFinanceCollector:
    def test_budget_utilization_no_tracker(self, project: Path) -> None:
        result = FinanceKPICollector(project).collect()
        assert result["department"] == "finance"
        assert result["kpis"]["budget_utilization"]["current"] == 0.0

    def test_missing_files(self, empty_project: Path) -> None:
        result = FinanceKPICollector(empty_project).collect()
        assert result["kpis"]["active_agents"]["current"] == 0


# ---------------------------------------------------------------------------
# Marketing
# ---------------------------------------------------------------------------

class TestMarketingCollector:
    def test_empty_project(self, empty_project: Path) -> None:
        result = MarketingKPICollector(empty_project).collect()
        assert result["department"] == "marketing"
        assert result["kpis"]["campaign_generation_rate"]["current"] == 0
        assert result["kpis"]["content_quality_score"]["current"] == 0.0

    def test_project_with_data(self, project: Path) -> None:
        result = MarketingKPICollector(project).collect()
        assert result["department"] == "marketing"
        # No marketing-specific task receivers in our fixture tasks
        assert result["kpis"]["total_marketing_tasks"]["current"] == 0


# ---------------------------------------------------------------------------
# Sales
# ---------------------------------------------------------------------------

class TestSalesCollector:
    def test_empty_project(self, empty_project: Path) -> None:
        result = SalesKPICollector(empty_project).collect()
        assert result["department"] == "sales"
        assert result["kpis"]["pipeline_value"]["current"] == 0
        assert result["kpis"]["total_deals"]["current"] == 0

    def test_project_with_data(self, project: Path) -> None:
        result = SalesKPICollector(project).collect()
        assert result["department"] == "sales"
        assert result["kpis"]["total_sales_tasks"]["current"] == 0


# ---------------------------------------------------------------------------
# Customer Success
# ---------------------------------------------------------------------------

class TestCustomerSuccessCollector:
    def test_empty_project(self, empty_project: Path) -> None:
        result = CustomerSuccessKPICollector(empty_project).collect()
        assert result["department"] == "customer_success"
        assert result["kpis"]["total_tickets"]["current"] == 0
        assert result["kpis"]["customer_satisfaction"]["current"] == 0.0

    def test_project_with_data(self, project: Path) -> None:
        result = CustomerSuccessKPICollector(project).collect()
        assert result["department"] == "customer_success"
        assert result["kpis"]["total_cs_tasks"]["current"] == 0


# ---------------------------------------------------------------------------
# Legal
# ---------------------------------------------------------------------------

class TestLegalCollector:
    def test_empty_project(self, empty_project: Path) -> None:
        result = LegalKPICollector(empty_project).collect()
        assert result["department"] == "legal"
        assert result["kpis"]["total_contracts"]["current"] == 0
        assert result["kpis"]["compliance_score"]["current"] == 0.0

    def test_project_with_data(self, project: Path) -> None:
        result = LegalKPICollector(project).collect()
        assert result["department"] == "legal"
        assert result["kpis"]["total_legal_tasks"]["current"] == 0


# ---------------------------------------------------------------------------
# All departments return results
# ---------------------------------------------------------------------------

class TestAllCollectors:
    def test_all_departments_return_results(self, project: Path) -> None:
        """Every registered collector produces a valid result dict."""
        for collector_cls in ALL_COLLECTORS:
            result = collector_cls(project).collect()
            assert "department" in result, f"{collector_cls} missing 'department'"
            assert "kpis" in result, f"{collector_cls} missing 'kpis'"
            assert result["department"], f"{collector_cls} has empty department"

    def test_missing_files_handled_gracefully(self, empty_project: Path) -> None:
        """All collectors must not crash when no operational files exist."""
        for collector_cls in ALL_COLLECTORS:
            result = collector_cls(empty_project).collect()
            assert "department" in result
            assert "kpis" in result
            assert isinstance(result["kpis"], dict)

    def test_collect_all_kpis_aggregates(self, project: Path) -> None:
        """collect_all_kpis() returns all departments under a timestamp."""
        snapshot = collect_all_kpis(project)
        assert "collected_at" in snapshot
        assert "departments" in snapshot
        depts = snapshot["departments"]
        assert len(depts) == len(ALL_COLLECTORS)
        assert "engineering" in depts
        assert "hr" in depts
        assert "finance" in depts
        assert "marketing" in depts
        assert "sales" in depts
        assert "customer_success" in depts
        assert "legal" in depts

    def test_collect_all_kpis_empty_project(self, empty_project: Path) -> None:
        """Aggregation works even when no data files exist."""
        snapshot = collect_all_kpis(empty_project)
        assert "departments" in snapshot
        for dept, data in snapshot["departments"].items():
            assert "kpis" in data, f"Department {dept} missing kpis"
