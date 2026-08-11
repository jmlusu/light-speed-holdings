"""Sprint 4 T017 — approval escalation lifecycle: request, approve/reject, expiry,
timeout, manual override, escalation ladder, and postmortem creation.

All state is anchored under ``tmp_path`` config files so no real repository
``orchestrator/*.yaml`` files are read or written.
"""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from ai_company.executor.hitl_gate import HITLGate
from ai_company.orchestrator.approval import ApprovalGate, ApprovalStatus
from ai_company.orchestrator.escalation import (
    EscalationManager,
    Postmortem,
    PostmortemStore,
)


@pytest.fixture()
def gate(tmp_path: Path) -> ApprovalGate:
    return ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))


@pytest.fixture()
def escalation(tmp_path: Path) -> EscalationManager:
    return EscalationManager(config_path=str(tmp_path / "escalation.yaml"))


# ── Approval lifecycle ─────────────────────────────────────────────────


class TestApprovalLifecycle:
    def test_request_creates_pending_request(self, gate: ApprovalGate) -> None:
        req = gate.request_approval(
            request_id="REQ-1",
            task_id="TASK-1",
            agent_id="qa_engineer",
            action="deploy",
            description="Deploy to production",
        )
        assert req.status == ApprovalStatus.PENDING
        assert gate.get_request("REQ-1") is req
        assert [r.id for r in gate.get_pending_requests()] == ["REQ-1"]

    def test_approve_resolves_request(self, gate: ApprovalGate) -> None:
        gate.request_approval("REQ-1", "TASK-1", "qa_engineer", "deploy", "Deploy")
        assert gate.approve("REQ-1", "human-operator") is True
        req = gate.get_request("REQ-1")
        assert req is not None
        assert req.status == ApprovalStatus.APPROVED
        assert req.response_by == "human-operator"
        assert req.responded_at is not None
        assert gate.get_pending_requests() == []

    def test_reject_denies_request(self, gate: ApprovalGate) -> None:
        gate.request_approval("REQ-1", "TASK-1", "qa_engineer", "deploy", "Deploy")
        assert gate.reject("REQ-1", "human-operator") is True
        req = gate.get_request("REQ-1")
        assert req is not None
        assert req.status == ApprovalStatus.REJECTED
        assert gate.get_pending_requests() == []

    def test_second_action_on_processed_request_fails(self, gate: ApprovalGate) -> None:
        gate.request_approval("REQ-1", "TASK-1", "qa_engineer", "deploy", "Deploy")
        assert gate.reject("REQ-1", "human-operator") is True
        assert gate.approve("REQ-1", "human-operator") is False
        assert gate.reject("REQ-1", "human-operator") is False
        assert gate.get_request("REQ-1").status == ApprovalStatus.REJECTED

    def test_action_on_unknown_request_fails(self, gate: ApprovalGate) -> None:
        assert gate.approve("REQ-UNKNOWN", "human-operator") is False
        assert gate.reject("REQ-UNKNOWN", "human-operator") is False

    def test_multi_approver_requires_all_approvers(self, gate: ApprovalGate) -> None:
        gate.request_approval(
            "REQ-1",
            "TASK-1",
            "qa_engineer",
            "deploy",
            "Deploy",
            required_approvers=2,
        )
        assert gate.approve("REQ-1", "approver-a") is True
        assert gate.get_request("REQ-1").status == ApprovalStatus.PENDING
        assert gate.approve("REQ-1", "approver-b") is True
        req = gate.get_request("REQ-1")
        assert req.status == ApprovalStatus.APPROVED
        assert req.approved_by_list == ["approver-a", "approver-b"]

    def test_requests_persist_across_gate_instances(self, tmp_path: Path) -> None:
        config_path = tmp_path / "approvals.yaml"
        gate1 = ApprovalGate(config_path=str(config_path))
        gate1.request_approval("REQ-1", "TASK-1", "qa_engineer", "deploy", "Deploy")
        gate2 = ApprovalGate(config_path=str(config_path))
        req = gate2.get_request("REQ-1")
        assert req is not None
        assert req.id == "REQ-1"
        assert req.status == ApprovalStatus.PENDING


# ── Expiry, timeout, and manual override ───────────────────────────────


class TestExpiryAndTimeout:
    def test_expired_request_is_not_pending(self, gate: ApprovalGate) -> None:
        gate.request_approval(
            "REQ-1",
            "TASK-1",
            "qa_engineer",
            "deploy",
            "Deploy",
            expires_in_minutes=-1,
        )
        req = gate.get_request("REQ-1")
        assert req is not None
        assert req.expires_at is not None
        assert gate.get_pending_requests() == []

    def test_manual_override_can_approve_pending_request_after_expiry(
        self, gate: ApprovalGate
    ) -> None:
        """Current contract: approve() gates on status, not expiry, so a human
        can still force an approval for an expired-but-pending request."""
        gate.request_approval(
            "REQ-1",
            "TASK-1",
            "qa_engineer",
            "deploy",
            "Deploy",
            expires_in_minutes=-1,
        )
        assert gate.get_request("REQ-1").status == ApprovalStatus.PENDING
        assert gate.approve("REQ-1", "human-operator") is True
        assert gate.get_request("REQ-1").status == ApprovalStatus.APPROVED

    def test_hitl_gate_denies_expired_request(self, tmp_path: Path) -> None:
        gate = ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))
        hitl = HITLGate(approval_gate=gate, timeout_minutes=0)
        request_id = hitl.request_and_park(
            "TASK-1", "qa_engineer", "write", {"path": "x.txt", "content": "y"}
        )
        time.sleep(0.01)  # ensure expires_at has fallen into the past
        assert hitl.resume_approved(request_id) is False

    def test_hitl_gate_approval_resumes_true(self, tmp_path: Path) -> None:
        gate = ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))
        hitl = HITLGate(approval_gate=gate, timeout_minutes=30)
        request_id = hitl.request_and_park(
            "TASK-1", "qa_engineer", "write", {"path": "x.txt", "content": "y"}
        )
        assert hitl.resume_approved(request_id) is None  # still pending
        assert gate.approve(request_id, "human-operator") is True
        assert hitl.resume_approved(request_id) is True

    def test_hitl_gate_rejection_resumes_false(self, tmp_path: Path) -> None:
        gate = ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))
        hitl = HITLGate(approval_gate=gate, timeout_minutes=30)
        request_id = hitl.request_and_park(
            "TASK-1", "qa_engineer", "execute", {"command": "rm -rf /tmp/x"}
        )
        assert gate.reject(request_id, "human-operator") is True
        assert hitl.resume_approved(request_id) is False

    def test_unknown_parked_request_resumes_none(self, tmp_path: Path) -> None:
        gate = ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))
        hitl = HITLGate(approval_gate=gate, timeout_minutes=30)
        assert hitl.resume_approved("hitl-never-parked") is None


# ── Escalation flow ────────────────────────────────────────────────────


class TestEscalationFlow:
    def test_escalation_ladder_manager_to_director_to_vp(
        self, escalation: EscalationManager
    ) -> None:
        escalation.add_rule("tier-1", "First escalation", "no response", "manager")
        escalation.add_rule("tier-2", "Second escalation", "manager no response", "director")
        escalation.add_rule("tier-3", "Third escalation", "director no response", "vp")
        escalation.add_rule("tier-4", "Final escalation", "vp no response", "c-level")

        evt1 = escalation.trigger_escalation("TASK-1", "tier-1", "staff_agent", "no reply")
        assert evt1 is not None and evt1.to_agent == "manager"
        evt2 = escalation.trigger_escalation("TASK-1", "tier-2", "manager", "no reply")
        assert evt2 is not None and evt2.to_agent == "director"
        evt3 = escalation.trigger_escalation("TASK-1", "tier-3", "director", "no reply")
        assert evt3 is not None and evt3.to_agent == "vp"
        evt4 = escalation.trigger_escalation("TASK-1", "tier-4", "vp", "no reply")
        assert evt4 is not None and evt4.to_agent == "c-level"

    def test_trigger_unknown_rule_returns_none(self, escalation: EscalationManager) -> None:
        assert escalation.trigger_escalation("TASK-1", "tier-nope", "staff_agent", "r") is None

    def test_pending_until_resolved(self, escalation: EscalationManager) -> None:
        escalation.add_rule("tier-1", "First escalation", "no response", "manager")
        escalation.trigger_escalation("TASK-1", "tier-1", "staff_agent", "no reply")
        pending = escalation.get_pending_escalations()
        assert len(pending) == 1
        assert pending[0].rule_id == "tier-1"
        assert pending[0].resolved is False
        assert pending[0].from_agent == "staff_agent"

        escalation.resolve_escalation("TASK-1")
        assert escalation.get_pending_escalations() == []

    def test_events_persist_across_manager_instances(self, tmp_path: Path) -> None:
        config_path = tmp_path / "escalation.yaml"
        manager1 = EscalationManager(config_path=str(config_path))
        manager1.add_rule("tier-1", "First escalation", "no response", "manager")
        manager1.trigger_escalation("TASK-1", "tier-1", "staff_agent", "no reply")

        manager2 = EscalationManager(config_path=str(config_path))
        assert [r.id for r in manager2.list_rules()] == ["tier-1"]
        event = manager2.get_event("TASK-1")
        assert event is not None
        assert event.resolved is False
        assert event.to_agent == "manager"

    def test_add_and_remove_rule(self, escalation: EscalationManager) -> None:
        escalation.add_rule(
            "r1",
            "Rule 1",
            "timeout",
            "manager",
            max_retries=2,
            timeout_minutes=15,
        )
        rule = escalation.list_rules()[0]
        assert rule.max_retries == 2
        assert rule.timeout_minutes == 15
        assert rule.enabled is True

        assert escalation.remove_rule("r1") is True
        assert escalation.remove_rule("r1") is False
        assert escalation.list_rules() == []

    def test_rule_timeout_field_is_persisted(self, tmp_path: Path) -> None:
        config_path = tmp_path / "escalation.yaml"
        manager1 = EscalationManager(config_path=str(config_path))
        manager1.add_rule("r1", "Rule 1", "timeout", "vp", timeout_minutes=45)
        manager2 = EscalationManager(config_path=str(config_path))
        assert manager2.list_rules()[0].timeout_minutes == 45


# ── Postmortem from escalation ─────────────────────────────────────────


class TestPostmortemFromEscalation:
    def test_create_from_escalation(self, tmp_path: Path) -> None:
        config_path = tmp_path / "escalation.yaml"
        store = PostmortemStore(storage_dir=str(tmp_path / "postmortems"))
        manager = EscalationManager(config_path=str(config_path))
        manager.add_rule("tier-1", "First escalation", "no response", "manager")
        event = manager.trigger_escalation("TASK-9", "tier-1", "staff_agent", "no reply")
        assert event is not None

        pm = store.create_from_escalation(event, title="Task 9 incident")
        assert pm.incident_id == "INC-TASK-9"
        assert pm.affected_agent == "staff_agent"
        assert pm.prepared_by == "manager"
        assert pm.status == "draft"
        assert "Escalation triggered" in pm.timeline[0].description

        loaded = store.load("INC-TASK-9")
        assert loaded is not None
        assert loaded.title == "Task 9 incident"

    def test_postmortem_save_and_list(self, tmp_path: Path) -> None:
        store = PostmortemStore(storage_dir=str(tmp_path / "postmortems"))
        pm = Postmortem(incident_id="INC-1", title="Incident one")
        saved = store.save(pm)
        assert saved.name == "INC-1.json"
        assert [p.incident_id for p in store.list_all()] == ["INC-1"]

    def test_postmortem_load_missing_returns_none(self, tmp_path: Path) -> None:
        store = PostmortemStore(storage_dir=str(tmp_path / "postmortems"))
        assert store.load("INC-MISSING") is None
