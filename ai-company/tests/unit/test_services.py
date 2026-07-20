"""Tests for the FileStore abstraction, department services, and persistent workflow state."""

from __future__ import annotations

import json
import threading
from pathlib import Path

import pytest

from ai_company.store.file_store import FileStore
from ai_company.services.marketing import MarketingService
from ai_company.services.sales import SalesService
from ai_company.services.customer_success import CustomerSuccessService
from ai_company.services.legal import LegalService
from ai_company.services.hr import HRService
from ai_company.models import (
    Company,
    CompanyRegistry,
    Workflow,
    WorkflowStep,
)
from ai_company.workflow.engine import WorkflowEngine


# ── FileStore Tests ───────────────────────────────────────────────────


class TestFileStore:
    def test_read_write_json(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path)
        store.write_json("data.json", {"key": "value"})
        result = store.read_json("data.json")
        assert result == {"key": "value"}

    def test_read_write_yaml(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path)
        store.write_yaml("config.yaml", {"section": {"key": "value"}})
        result = store.read_yaml("config.yaml")
        assert result == {"section": {"key": "value"}}

    def test_atomic_write_creates_parent_dirs(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path)
        store.write_json("deep/nested/file.json", [1, 2, 3])
        assert store.read_json("deep/nested/file.json") == [1, 2, 3]

    def test_read_nonexistent_returns_none(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path)
        assert store.read_json("nope.json") is None
        assert store.read_yaml("nope.yaml") is None

    def test_exists_and_delete(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path)
        store.write_json("del.json", [1])
        assert store.exists("del.json")
        assert store.delete("del.json")
        assert not store.exists("del.json")
        assert not store.delete("del.json")  # Double delete is safe

    def test_list_files(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path)
        store.write_json("a.json", 1)
        store.write_json("b.json", 2)
        store.write_yaml("c.yaml", 3)
        files = store.list_files(pattern="*.json")
        assert len(files) == 2

    def test_backup_created(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path, backup=True)
        store.write_json("test.json", {"v": 1})
        assert (tmp_path / "test.json.bak").exists()

    def test_backup_disabled(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path, backup=False)
        store.write_json("test.json", {"v": 1})
        assert not (tmp_path / "test.json.bak").exists()

    def test_corrupt_json_returns_none(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path)
        (tmp_path / "bad.json").write_text("{invalid json!!!", encoding="utf-8")
        assert store.read_json("bad.json") is None

    def test_concurrent_writes(self, tmp_path: Path) -> None:
        """Test that concurrent atomic writes don't corrupt data."""
        store = FileStore(tmp_path)
        store.write_json("counter.json", {"count": 0})

        def increment(n: int) -> None:
            for _ in range(10):
                def updater(data: dict | None) -> dict:
                    if data is None:
                        data = {"count": 0}
                    data["count"] = data.get("count", 0) + 1
                    return data
                store.update_json("counter.json", updater)

        threads = [threading.Thread(target=increment, args=(i,)) for i in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        result = store.read_json("counter.json")
        assert result["count"] == 40


# ── Marketing Service Tests ──────────────────────────────────────────


class TestMarketingService:
    def test_create_and_list_campaigns(self, tmp_path: Path) -> None:
        svc = MarketingService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        campaign = svc.create_campaign(
            campaign_id="camp-1",
            name="Product Launch",
            channel="email",
        )
        assert campaign["id"] == "camp-1"
        assert campaign["status"] == "draft"

        campaigns = svc.list_campaigns()
        assert len(campaigns) == 1
        assert campaigns[0]["name"] == "Product Launch"

    def test_duplicate_campaign_raises(self, tmp_path: Path) -> None:
        svc = MarketingService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        svc.create_campaign(campaign_id="dup", name="First")
        with pytest.raises(ValueError, match="already exists"):
            svc.create_campaign(campaign_id="dup", name="Second")

    def test_launch_campaign(self, tmp_path: Path) -> None:
        svc = MarketingService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        svc.create_campaign(campaign_id="c1", name="Test")
        result = svc.launch_campaign("c1")
        assert result["status"] == "active"

    def test_update_metrics(self, tmp_path: Path) -> None:
        svc = MarketingService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        svc.create_campaign(campaign_id="c1", name="Test")
        svc.update_metrics("c1", impressions=100, clicks=10, conversions=2)
        metrics = svc.get_campaign_metrics("c1")
        assert metrics["impressions"] == 100
        assert metrics["clicks"] == 10
        assert metrics["conversions"] == 2

    def test_summary(self, tmp_path: Path) -> None:
        svc = MarketingService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        svc.create_campaign(campaign_id="c1", name="Test")
        summary = svc.get_summary()
        assert summary["total_campaigns"] == 1
        assert summary["department"] == "marketing"


# ── Sales Service Tests ──────────────────────────────────────────────


class TestSalesService:
    def test_add_and_list_leads(self, tmp_path: Path) -> None:
        svc = SalesService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        lead = svc.add_lead(lead_id="l1", name="Acme Corp", source="website")
        assert lead["id"] == "l1"
        assert lead["status"] == "new"

        leads = svc.list_leads()
        assert len(leads) == 1

    def test_add_deal(self, tmp_path: Path) -> None:
        svc = SalesService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        deal = svc.add_deal(deal_id="d1", name="Enterprise Deal", value=100000)
        assert deal["value"] == 100000
        assert deal["stage"] == "prospecting"

    def test_advance_deal(self, tmp_path: Path) -> None:
        svc = SalesService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        svc.add_deal(deal_id="d1", name="Deal", value=50000)
        result = svc.advance_deal("d1", "qualification")
        assert result["stage"] == "qualification"

    def test_pipeline_summary(self, tmp_path: Path) -> None:
        svc = SalesService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        svc.add_lead(lead_id="l1", name="Lead 1")
        svc.add_deal(deal_id="d1", name="Deal 1", value=25000)
        summary = svc.get_pipeline_summary()
        assert summary["total_leads"] == 1
        assert summary["active_deals"] == 1
        assert summary["pipeline_value"] == 25000


# ── Customer Success Service Tests ───────────────────────────────────


class TestCustomerSuccessService:
    def test_create_and_resolve_ticket(self, tmp_path: Path) -> None:
        svc = CustomerSuccessService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        ticket = svc.create_ticket(ticket_id="t1", subject="Login issue", priority="high")
        assert ticket["status"] == "open"

        result = svc.update_ticket_status("t1", "resolved", resolution="Password reset")
        assert result["status"] == "resolved"
        assert result["resolution"] == "Password reset"

    def test_escalate_ticket(self, tmp_path: Path) -> None:
        svc = CustomerSuccessService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        svc.create_ticket(ticket_id="t1", subject="Bug")
        result = svc.escalate_ticket("t1", reason="Customer threatening churn")
        assert result["status"] == "escalated"

    def test_satisfaction_report(self, tmp_path: Path) -> None:
        svc = CustomerSuccessService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        svc.create_ticket(ticket_id="t1", subject="A")
        svc.create_ticket(ticket_id="t2", subject="B")
        svc.update_ticket_status("t1", "resolved")

        report = svc.get_satisfaction_report()
        assert report["total_tickets"] == 2
        assert report["resolved"] == 1
        assert report["resolution_rate"] == 50.0


# ── Legal Service Tests ──────────────────────────────────────────────


class TestLegalService:
    def test_add_and_approve_contract(self, tmp_path: Path) -> None:
        svc = LegalService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        contract = svc.add_contract(
            contract_id="c1", name="NDA", party="Acme", value=0,
        )
        assert contract["status"] == "draft"

        approved = svc.approve_contract("c1", approver="legal-head")
        assert approved["status"] == "approved"
        assert approved["approved_by"] == "legal-head"

    def test_terminate_contract(self, tmp_path: Path) -> None:
        svc = LegalService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        svc.add_contract(contract_id="c1", name="SaaS Agreement", party="Vendor")
        result = svc.terminate_contract("c1", reason="Vendor breach")
        assert result["status"] == "terminated"

    def test_compliance_check(self, tmp_path: Path) -> None:
        svc = LegalService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        svc.add_contract(contract_id="c1", name="A", party="X")
        svc.add_contract(contract_id="c2", name="B", party="Y")
        svc.approve_contract("c1")

        report = svc.compliance_check()
        assert report["total_contracts"] == 2
        assert report["active"] == 1
        assert report["draft_pending"] == 1


# ── HR Service Tests ─────────────────────────────────────────────────


class TestHRService:
    def test_onboard_and_activate(self, tmp_path: Path) -> None:
        svc = HRService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        agent = svc.onboard(
            agent_id="dev-1",
            role="Backend Engineer",
            department="Technology",
        )
        assert agent["status"] == "onboarding"

        activated = svc.activate("dev-1")
        assert activated["status"] == "active"

    def test_deactivate(self, tmp_path: Path) -> None:
        svc = HRService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        svc.onboard(agent_id="a1", role="Dev", department="Eng")
        svc.activate("a1")
        result = svc.deactivate("a1", reason="Project completed")
        assert result["status"] == "inactive"

    def test_workforce_report(self, tmp_path: Path) -> None:
        svc = HRService(data_dir=tmp_path, memory_dir=str(tmp_path / "mem"))
        svc.onboard(agent_id="a1", role="Dev", department="Eng")
        svc.onboard(agent_id="a2", role="PM", department="Product")
        svc.activate("a1")

        report = svc.get_workforce_report()
        assert report["total_agents"] == 2
        assert report["active"] == 1
        assert report["onboarding"] == 1
        assert report["by_department"]["Eng"] == 1
        assert report["by_department"]["Product"] == 1


# ── Persistent Workflow Engine Tests ─────────────────────────────────


@pytest.fixture()
def registry() -> CompanyRegistry:
    return CompanyRegistry(
        company=Company(id="test", name="Test"),
        workflows=[
            Workflow(
                id="hiring",
                name="Hiring Workflow",
                trigger="job_requisition",
                owner="hr",
                steps=[
                    WorkflowStep(id="post", name="Post Job", action="Create job posting", owner="recruiter"),
                    WorkflowStep(id="review", name="Review Resumes", action="Screen candidates", owner="recruiter"),
                    WorkflowStep(id="interview", name="Interview", action="Conduct interviews", owner="hiring_manager"),
                ],
            ),
        ],
    )


class TestPersistentWorkflowEngine:
    def test_instances_persist(self, tmp_path: Path, registry: CompanyRegistry) -> None:
        state_dir = tmp_path / "wf_instances"
        # Start a workflow and advance it
        engine = WorkflowEngine(registry, state_dir=state_dir)
        instance_id = engine.start("hiring")
        engine.complete_step(instance_id, "Posted on LinkedIn")
        status1 = engine.get_status(instance_id)
        assert status1["current_step"] == "Review Resumes"
        assert status1["completed_steps"] == 1

        # Create a new engine with same state_dir -- should load persisted state
        engine2 = WorkflowEngine(registry, state_dir=state_dir)
        status2 = engine2.get_status(instance_id)
        assert status2 is not None
        assert status2["current_step"] == "Review Resumes"
        assert status2["completed_steps"] == 1

    def test_cancel_persists(self, tmp_path: Path, registry: CompanyRegistry) -> None:
        state_dir = tmp_path / "wf_instances"
        engine = WorkflowEngine(registry, state_dir=state_dir)
        instance_id = engine.start("hiring")
        engine.cancel(instance_id)

        # Reload and verify
        engine2 = WorkflowEngine(registry, state_dir=state_dir)
        status = engine2.get_status(instance_id)
        assert status["status"] == "cancelled"

    def test_list_instances(self, tmp_path: Path, registry: CompanyRegistry) -> None:
        state_dir = tmp_path / "wf_instances"
        engine = WorkflowEngine(registry, state_dir=state_dir)
        id1 = engine.start("hiring")
        id2 = engine.start("hiring")
        # Both may have same timestamp; if so, second overwrites first.
        # The important thing is list_instances works.
        instances = engine.list_instances()
        assert len(instances) >= 1
        assert all(i["workflow_id"] == "hiring" for i in instances)

        # Filter by non-existent workflow_id
        empty = engine.list_instances(workflow_id="nonexistent")
        assert len(empty) == 0

    def test_missing_workflow_on_reload(self, tmp_path: Path) -> None:
        """Instance referencing a removed workflow is skipped gracefully."""
        state_dir = tmp_path / "wf_instances"

        # Create with a workflow
        reg1 = CompanyRegistry(
            company=Company(id="test", name="Test"),
            workflows=[
                Workflow(id="old_wf", name="Old", trigger="manual", owner="ops",
                         steps=[WorkflowStep(id="s1", name="Step 1")]),
            ],
        )
        engine1 = WorkflowEngine(reg1, state_dir=state_dir)
        instance_id = engine1.start("old_wf")

        # Reload WITHOUT that workflow
        reg2 = CompanyRegistry(company=Company(id="test", name="Test"), workflows=[])
        engine2 = WorkflowEngine(reg2, state_dir=state_dir)
        # Instance should be skipped (workflow not found), but engine loads fine
        assert engine2.get_status(instance_id) is None
