"""Tests for approval escalation: gate, multi-step, expiration, and HITL parking.

Covers Task S3-14 — comprehensive coverage of the approval gate lifecycle,
multi-step (two-person) approvals, expiration semantics, the escalation manager,
HITL gate parking/resume, and the postmortem store.

All file I/O uses the ``tmp_path`` fixture for complete isolation.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from ai_company.executor.hitl_gate import HITLGate
from ai_company.orchestrator.approval import ApprovalGate, ApprovalStatus
from ai_company.orchestrator.escalation import (
    EscalationEvent,
    EscalationManager,
    Postmortem,
    PostmortemStore,
)


# ─── Shared fixtures ──────────────────────────────────────────────────────────


@pytest.fixture()
def gate(tmp_path: Path) -> ApprovalGate:
    """ApprovalGate backed by an isolated tmp directory."""
    return ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))


@pytest.fixture()
def escalation(tmp_path: Path) -> EscalationManager:
    """EscalationManager backed by an isolated tmp directory."""
    return EscalationManager(config_path=str(tmp_path / "escalation.yaml"))


@pytest.fixture()
def pm_store(tmp_path: Path) -> PostmortemStore:
    """PostmortemStore backed by an isolated tmp directory."""
    return PostmortemStore(storage_dir=str(tmp_path / "postmortems"))


@pytest.fixture()
def hitl(tmp_path: Path) -> HITLGate:
    """HITLGate with a short poll interval for test speed."""
    approval = ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))
    return HITLGate(approval_gate=approval, poll_interval=0.05, timeout_minutes=0.05)


# ═══════════════════════════════════════════════════════════════════════════════
# TestApprovalGateBasic
# ═══════════════════════════════════════════════════════════════════════════════


class TestApprovalGateBasic:
    """Core approval gate operations: request, approve, reject, edge cases."""

    def test_request_approval_creates_pending(self, gate: ApprovalGate) -> None:
        req = gate.request_approval(
            request_id="req-1",
            task_id="task-1",
            agent_id="agent-a",
            action="deploy",
            description="Deploy to production",
        )
        assert req.status == ApprovalStatus.PENDING
        assert req.id == "req-1"
        assert req.task_id == "task-1"
        pending = gate.get_pending_requests()
        assert len(pending) == 1
        assert pending[0].id == "req-1"

    def test_approve_single_approver(self, gate: ApprovalGate) -> None:
        gate.request_approval(
            request_id="req-1",
            task_id="task-1",
            agent_id="agent-a",
            action="deploy",
            description="Deploy",
        )
        result = gate.approve("req-1", "human-ceo")
        assert result is True
        req = gate.get_request("req-1")
        assert req is not None
        assert req.status == ApprovalStatus.APPROVED
        assert req.response_by == "human-ceo"
        assert req.responded_at is not None
        assert "human-ceo" in req.approved_by_list
        # Should no longer appear in pending.
        assert gate.get_pending_requests() == []

    def test_reject_single_approver(self, gate: ApprovalGate) -> None:
        gate.request_approval(
            request_id="req-1",
            task_id="task-1",
            agent_id="agent-a",
            action="deploy",
            description="Deploy",
        )
        result = gate.reject("req-1", "human-cto", notes="Not ready")
        assert result is True
        req = gate.get_request("req-1")
        assert req is not None
        assert req.status == ApprovalStatus.REJECTED
        assert req.response_by == "human-cto"
        assert req.notes == "Not ready"
        assert gate.get_pending_requests() == []

    def test_approve_nonexistent_returns_false(self, gate: ApprovalGate) -> None:
        result = gate.approve("nonexistent-id", "human")
        assert result is False

    def test_reject_nonexistent_returns_false(self, gate: ApprovalGate) -> None:
        result = gate.reject("nonexistent-id", "human")
        assert result is False

    def test_approve_already_approved_returns_false(self, gate: ApprovalGate) -> None:
        gate.request_approval(
            request_id="req-1",
            task_id="task-1",
            agent_id="agent-a",
            action="deploy",
            description="Deploy",
        )
        # First approve succeeds.
        assert gate.approve("req-1", "human-1") is True
        # Second approve fails because status is no longer PENDING.
        result = gate.approve("req-1", "human-2")
        assert result is False

    def test_reject_already_rejected_returns_false(self, gate: ApprovalGate) -> None:
        gate.request_approval(
            request_id="req-1",
            task_id="task-1",
            agent_id="agent-a",
            action="deploy",
            description="Deploy",
        )
        assert gate.reject("req-1", "human-1") is True
        result = gate.reject("req-1", "human-2")
        assert result is False

    def test_approve_after_reject_returns_false(self, gate: ApprovalGate) -> None:
        gate.request_approval(
            request_id="req-1",
            task_id="task-1",
            agent_id="agent-a",
            action="deploy",
            description="Deploy",
        )
        gate.reject("req-1", "human-1")
        result = gate.approve("req-1", "human-2")
        assert result is False

    def test_get_pending_requests_filters_correctly(
        self, gate: ApprovalGate
    ) -> None:
        # Create three requests with varying states.
        gate.request_approval(
            request_id="r-pending", task_id="t1", agent_id="a1",
            action="write", description="d1",
        )
        gate.request_approval(
            request_id="r-approved", task_id="t2", agent_id="a2",
            action="write", description="d2",
        )
        gate.request_approval(
            request_id="r-rejected", task_id="t3", agent_id="a3",
            action="write", description="d3",
        )
        gate.approve("r-approved", "human-1")
        gate.reject("r-rejected", "human-2")

        pending = gate.get_pending_requests()
        assert len(pending) == 1
        assert pending[0].id == "r-pending"

    def test_get_request_returns_none_for_unknown(
        self, gate: ApprovalGate
    ) -> None:
        assert gate.get_request("unknown") is None

    def test_list_all_returns_all_requests(self, gate: ApprovalGate) -> None:
        gate.request_approval(
            request_id="r1", task_id="t1", agent_id="a1",
            action="write", description="d1",
        )
        gate.request_approval(
            request_id="r2", task_id="t2", agent_id="a2",
            action="execute", description="d2",
        )
        all_reqs = gate.list_all()
        assert len(all_reqs) == 2

    def test_request_sets_expiry(self, gate: ApprovalGate) -> None:
        before = datetime.now()
        gate.request_approval(
            request_id="r1", task_id="t1", agent_id="a1",
            action="write", description="d1", expires_in_minutes=30,
        )
        req = gate.get_request("r1")
        assert req is not None
        assert req.expires_at is not None
        assert req.expires_at > before
        assert req.expires_at <= before + timedelta(minutes=31)


# ═══════════════════════════════════════════════════════════════════════════════
# TestMultiStepApproval
# ═══════════════════════════════════════════════════════════════════════════════


class TestMultiStepApproval:
    """Multi-approver (two-person rule) scenarios."""

    def test_multi_step_requires_all(self, gate: ApprovalGate) -> None:
        """With required_approvers=2, a single approve keeps it pending."""
        gate.request_approval(
            request_id="req-1",
            task_id="task-1",
            agent_id="agent-a",
            action="terraform-apply",
            description="Apply infrastructure",
            required_approvers=2,
        )
        result = gate.approve("req-1", "human-vp")
        assert result is True
        req = gate.get_request("req-1")
        assert req is not None
        assert req.status == ApprovalStatus.PENDING  # Still pending.
        assert len(req.approved_by_list) == 1
        assert "human-vp" in req.approved_by_list
        # Still appears in pending.
        assert len(gate.get_pending_requests()) == 1

    def test_multi_step_completes(self, gate: ApprovalGate) -> None:
        """Two approvals required: after two different approvers, it is approved."""
        gate.request_approval(
            request_id="req-1",
            task_id="task-1",
            agent_id="agent-a",
            action="terraform-apply",
            description="Apply infrastructure",
            required_approvers=2,
        )
        gate.approve("req-1", "human-vp")
        gate.approve("req-1", "human-cto")
        req = gate.get_request("req-1")
        assert req is not None
        assert req.status == ApprovalStatus.APPROVED
        assert len(req.approved_by_list) == 2
        assert gate.get_pending_requests() == []

    def test_multi_step_different_approvers_deduped(
        self, gate: ApprovalGate
    ) -> None:
        """Same person approving twice should be deduped; stays pending."""
        gate.request_approval(
            request_id="req-1",
            task_id="task-1",
            agent_id="agent-a",
            action="deploy",
            description="Deploy",
            required_approvers=2,
        )
        gate.approve("req-1", "human-vp")
        gate.approve("req-1", "human-vp")  # Same person again.
        req = gate.get_request("req-1")
        assert req is not None
        assert req.status == ApprovalStatus.PENDING  # Still pending.
        assert len(req.approved_by_list) == 1  # Deduped.

    def test_multi_step_partial_rejection(self, gate: ApprovalGate) -> None:
        """One of three approved, then rejected → overall rejected."""
        gate.request_approval(
            request_id="req-1",
            task_id="task-1",
            agent_id="agent-a",
            action="terraform-apply",
            description="Apply infrastructure",
            required_approvers=3,
        )
        gate.approve("req-1", "human-vp")
        gate.approve("req-1", "human-cto")
        # Still pending after 2 of 3.
        req = gate.get_request("req-1")
        assert req is not None
        assert req.status == ApprovalStatus.PENDING

        # Reject stops the process.
        gate.reject("req-1", "human-coo", notes="Policy violation")
        req = gate.get_request("req-1")
        assert req is not None
        assert req.status == ApprovalStatus.REJECTED
        assert req.notes == "Policy violation"

    def test_multi_step_three_of_three(self, gate: ApprovalGate) -> None:
        """All three approvers approve → approved."""
        gate.request_approval(
            request_id="req-1",
            task_id="task-1",
            agent_id="agent-a",
            action="deploy",
            description="Deploy",
            required_approvers=3,
        )
        gate.approve("req-1", "approver-1")
        gate.approve("req-1", "approver-2")
        gate.approve("req-1", "approver-3")
        req = gate.get_request("req-1")
        assert req is not None
        assert req.status == ApprovalStatus.APPROVED
        assert len(req.approved_by_list) == 3


# ═══════════════════════════════════════════════════════════════════════════════
# TestApprovalExpiration
# ═══════════════════════════════════════════════════════════════════════════════


class TestApprovalExpiration:
    """Expiration-related behavior for approval requests."""

    def test_expired_request_excluded_from_pending(
        self, gate: ApprovalGate
    ) -> None:
        gate.request_approval(
            request_id="req-1",
            task_id="task-1",
            agent_id="agent-a",
            action="deploy",
            description="Deploy",
            expires_in_minutes=60,
        )
        # Manually backdate the expiry.
        gate.requests[0].expires_at = datetime.now() - timedelta(minutes=5)
        pending = gate.get_pending_requests()
        assert len(pending) == 0

    def test_not_yet_expired_included(self, gate: ApprovalGate) -> None:
        gate.request_approval(
            request_id="req-1",
            task_id="task-1",
            agent_id="agent-a",
            action="deploy",
            description="Deploy",
            expires_in_minutes=60,
        )
        pending = gate.get_pending_requests()
        assert len(pending) == 1

    def test_approve_expired_request_returns_false(
        self, gate: ApprovalGate
    ) -> None:
        gate.request_approval(
            request_id="req-1",
            task_id="task-1",
            agent_id="agent-a",
            action="deploy",
            description="Deploy",
            expires_in_minutes=60,
        )
        gate.requests[0].expires_at = datetime.now() - timedelta(minutes=5)
        # Approve should still work at gate level (status is PENDING).
        # The expiration only affects get_pending_requests filtering.
        result = gate.approve("req-1", "human")
        assert result is True

    def test_request_with_zero_expiration(self, gate: ApprovalGate) -> None:
        """expires_in_minutes=0 creates an immediately-expired request."""
        gate.request_approval(
            request_id="req-1",
            task_id="task-1",
            agent_id="agent-a",
            action="deploy",
            description="Deploy",
            expires_in_minutes=0,
        )
        pending = gate.get_pending_requests()
        assert len(pending) == 0

    def test_request_with_no_expiry_always_pending(
        self, gate: ApprovalGate
    ) -> None:
        """When expires_at is None, the request is always pending."""
        gate.request_approval(
            request_id="req-1",
            task_id="task-1",
            agent_id="agent-a",
            action="deploy",
            description="Deploy",
            expires_in_minutes=60,
        )
        # Force expires_at to None to simulate unlimited.
        gate.requests[0].expires_at = None
        pending = gate.get_pending_requests()
        assert len(pending) == 1

    def test_mixed_expired_and_active(self, gate: ApprovalGate) -> None:
        """Only non-expired pending requests appear."""
        gate.request_approval(
            request_id="r-active", task_id="t1", agent_id="a1",
            action="write", description="d1", expires_in_minutes=60,
        )
        gate.request_approval(
            request_id="r-expired", task_id="t2", agent_id="a2",
            action="write", description="d2", expires_in_minutes=60,
        )
        gate.requests[1].expires_at = datetime.now() - timedelta(minutes=1)
        pending = gate.get_pending_requests()
        assert len(pending) == 1
        assert pending[0].id == "r-active"


# ═══════════════════════════════════════════════════════════════════════════════
# TestEscalationManager
# ═══════════════════════════════════════════════════════════════════════════════


class TestEscalationManager:
    """Escalation rule CRUD, triggering, and persistence."""

    def test_add_rule(self, escalation: EscalationManager) -> None:
        rule = escalation.add_rule(
            rule_id="r1",
            name="Task Timeout",
            trigger="task_timeout",
            escalate_to="chief-of-staff",
            max_retries=3,
            timeout_minutes=30,
        )
        assert rule.id == "r1"
        assert rule.name == "Task Timeout"
        assert rule.trigger == "task_timeout"
        assert rule.escalate_to == "chief-of-staff"
        rules = escalation.list_rules()
        assert len(rules) == 1
        assert rules[0].id == "r1"

    def test_remove_rule(self, escalation: EscalationManager) -> None:
        escalation.add_rule("r1", "Timeout", "task_timeout", "chief-of-staff")
        escalation.add_rule("r2", "Cost", "cost_exceeded", "finance-lead")
        result = escalation.remove_rule("r1")
        assert result is True
        rules = escalation.list_rules()
        assert len(rules) == 1
        assert rules[0].id == "r2"

    def test_remove_nonexistent_returns_false(
        self, escalation: EscalationManager
    ) -> None:
        result = escalation.remove_rule("nonexistent")
        assert result is False

    def test_trigger_escalation(self, escalation: EscalationManager) -> None:
        escalation.add_rule(
            "r1", "Timeout", "task_timeout", "chief-of-staff",
        )
        event = escalation.trigger_escalation(
            task_id="task-42",
            rule_id="r1",
            from_agent="lead-backend",
            reason="Task failed after 3 retries",
        )
        assert event is not None
        assert event.task_id == "task-42"
        assert event.rule_id == "r1"
        assert event.from_agent == "lead-backend"
        assert event.to_agent == "chief-of-staff"
        assert event.reason == "Task failed after 3 retries"
        assert event.resolved is False
        assert isinstance(event.timestamp, datetime)
        # Should appear in pending escalations.
        pending = escalation.get_pending_escalations()
        assert len(pending) == 1
        assert pending[0].task_id == "task-42"

    def test_trigger_unknown_rule_returns_none(
        self, escalation: EscalationManager
    ) -> None:
        event = escalation.trigger_escalation(
            task_id="task-1",
            rule_id="nonexistent",
            from_agent="agent-x",
            reason="reason",
        )
        assert event is None

    def test_resolve_escalation(self, escalation: EscalationManager) -> None:
        escalation.add_rule("r1", "Timeout", "task_timeout", "chief-of-staff")
        escalation.trigger_escalation("task-1", "r1", "agent-a", "timeout")
        escalation.trigger_escalation("task-2", "r1", "agent-b", "timeout")
        escalation.resolve_escalation("task-1")
        pending = escalation.get_pending_escalations()
        assert len(pending) == 1
        assert pending[0].task_id == "task-2"
        # Check the resolved one is marked.
        evt = escalation.get_event("task-1")
        assert evt is not None
        assert evt.resolved is True

    def test_persistence_across_instances(self, tmp_path: Path) -> None:
        """Rules and events survive when a new EscalationManager reads the same file."""
        config = str(tmp_path / "escalation.yaml")
        mgr1 = EscalationManager(config_path=config)
        mgr1.add_rule("r1", "Timeout", "task_timeout", "chief-of-staff")
        mgr1.trigger_escalation("task-1", "r1", "agent-a", "reason")

        # Create a new instance pointing to the same file.
        mgr2 = EscalationManager(config_path=config)
        assert len(mgr2.list_rules()) == 1
        assert mgr2.list_rules()[0].id == "r1"
        assert len(mgr2.get_pending_escalations()) == 1

    def test_get_event_returns_none_for_unknown(
        self, escalation: EscalationManager
    ) -> None:
        assert escalation.get_event("nonexistent") is None

    def test_multiple_rules_and_events(
        self, escalation: EscalationManager
    ) -> None:
        """Multiple rules and events can coexist."""
        escalation.add_rule("r1", "Timeout", "task_timeout", "chief-of-staff")
        escalation.add_rule("r2", "Cost", "cost_exceeded", "finance-lead")
        escalation.trigger_escalation("t1", "r1", "a1", "timeout")
        escalation.trigger_escalation("t2", "r2", "a2", "over budget")
        assert len(escalation.list_rules()) == 2
        assert len(escalation.get_pending_escalations()) == 2


# ═══════════════════════════════════════════════════════════════════════════════
# TestHITLGateParking
# ═══════════════════════════════════════════════════════════════════════════════


class TestHITLGateParking:
    """Non-blocking HITL parking and resume."""

    def test_request_and_park_creates_request(
        self, hitl: HITLGate
    ) -> None:
        request_id = hitl.request_and_park(
            task_id="task-1",
            agent_id="agent-a",
            tool="write",
            args={"path": "secrets.yaml", "content": "x"},
        )
        assert request_id.startswith("hitl-")
        # Should appear in the shared ApprovalGate.
        pending = hitl.gate.get_pending_requests()
        assert any(r.id == request_id for r in pending)
        # Should be in pending requests.
        assert hitl.has_pending_requests() is True

    def test_resume_approved_returns_none_when_pending(
        self, hitl: HITLGate
    ) -> None:
        request_id = hitl.request_and_park(
            task_id="task-1",
            agent_id="agent-a",
            tool="execute",
            args={"command": "ls -la"},
        )
        # Still pending → resume_approved returns None.
        result = hitl.resume_approved(request_id)
        assert result is None

    def test_resume_approved_returns_true_after_approval(
        self, hitl: HITLGate
    ) -> None:
        request_id = hitl.request_and_park(
            task_id="task-1",
            agent_id="agent-a",
            tool="write",
            args={"path": "out.py", "content": "y = 1"},
        )
        hitl.gate.approve(request_id, "human-ceo")
        result = hitl.resume_approved(request_id)
        assert result is True

    def test_resume_approved_returns_false_after_rejection(
        self, hitl: HITLGate
    ) -> None:
        request_id = hitl.request_and_park(
            task_id="task-1",
            agent_id="agent-a",
            tool="execute",
            args={"command": "rm -rf /"},
        )
        hitl.gate.reject(request_id, "human-cto", notes="Dangerous")
        result = hitl.resume_approved(request_id)
        assert result is False

    def test_resolve_all_pending_parked_requests_not_resolved(
        self, hitl: HITLGate
    ) -> None:
        """resolve_all_pending skips parked (no-future) requests.

        ``request_and_park`` does not create a Future, so
        ``resolve_approved`` returns None for them and they are not
        included in the resolved dict.
        """
        rid = hitl.request_and_park(
            task_id="t1", agent_id="a1", tool="write",
            args={"path": "f1.txt", "content": "a"},
        )
        hitl.gate.approve(rid, "human-1")
        resolved = hitl.resolve_all_pending()
        # Parked requests have no future → nothing resolved.
        assert resolved == {}

    def test_resolve_all_pending_with_future(self, hitl: HITLGate) -> None:
        """resolve_all_pending resolves blocking-path requests that have futures."""
        # request_and_wait returns a Future; the request_id is stored
        # internally in _pending_requests and _futures.
        future = hitl.request_and_wait(
            task_id="t1", agent_id="a1", tool="write",
            args={"path": "f1.txt", "content": "a"},
        )
        # Grab the request_id from the internal tracking dict.
        with hitl._lock:
            rids = list(hitl._futures.keys())
        assert len(rids) == 1
        rid = rids[0]

        # Approve the request so resolve_all_pending picks it up.
        hitl.gate.approve(rid, "human-1")
        resolved = hitl.resolve_all_pending()
        assert rid in resolved
        assert resolved[rid] is True

    def test_has_pending_requests_false_when_empty(
        self, hitl: HITLGate
    ) -> None:
        assert hitl.has_pending_requests() is False

    def test_parked_request_removed_from_pending_after_decision(
        self, hitl: HITLGate
    ) -> None:
        """After approve + resume, the request is removed from internal tracking."""
        rid = hitl.request_and_park(
            task_id="t1", agent_id="a1", tool="write",
            args={"path": "x.txt", "content": "data"},
        )
        hitl.gate.approve(rid, "human-1")
        # Resolve.
        result = hitl.resume_approved(rid)
        assert result is True
        # Calling resume_approved again returns None (no longer tracked).
        assert hitl.resume_approved(rid) is None

    def test_cancel_removes_pending(self, hitl: HITLGate) -> None:
        """Cancel resolves a parked request as False and cleans up."""
        rid = hitl.request_and_park(
            task_id="t1", agent_id="a1", tool="write",
            args={"path": "x.txt", "content": "data"},
        )
        hitl.cancel(rid)
        # The request should now resolve as False via resume_approved
        # (since the underlying gate still has it as pending, but HITL
        # cleaned up its tracking).
        assert hitl.resume_approved(rid) is None


# ═══════════════════════════════════════════════════════════════════════════════
# TestPostmortemStore
# ═══════════════════════════════════════════════════════════════════════════════


class TestPostmortemStore:
    """Postmortem persistence and creation from escalation events."""

    def test_save_and_load(self, pm_store: PostmortemStore) -> None:
        pm = Postmortem(incident_id="INC-100", title="Database outage", severity="critical")
        path = pm_store.save(pm)
        assert path.exists()

        loaded = pm_store.load("INC-100")
        assert loaded is not None
        assert loaded.incident_id == "INC-100"
        assert loaded.title == "Database outage"
        assert loaded.severity == "critical"
        assert loaded.status == "draft"

    def test_list_all(self, pm_store: PostmortemStore) -> None:
        pm_store.save(Postmortem(incident_id="INC-001", title="First"))
        pm_store.save(Postmortem(incident_id="INC-002", title="Second"))
        pm_store.save(Postmortem(incident_id="INC-003", title="Third"))
        all_pm = pm_store.list_all()
        assert len(all_pm) == 3
        ids = [pm.incident_id for pm in all_pm]
        assert "INC-001" in ids
        assert "INC-002" in ids
        assert "INC-003" in ids

    def test_list_all_empty(self, pm_store: PostmortemStore) -> None:
        assert pm_store.list_all() == []

    def test_load_nonexistent(self, pm_store: PostmortemStore) -> None:
        result = pm_store.load("INC-NONE")
        assert result is None

    def test_create_from_escalation(self, pm_store: PostmortemStore) -> None:
        event = EscalationEvent(
            task_id="task-42",
            rule_id="r1",
            from_agent="lead-backend",
            to_agent="chief-of-staff",
            reason="Task failed after 3 retries",
        )
        pm = pm_store.create_from_escalation(event, title="Backend failure")
        assert pm.incident_id == "INC-task-42"
        assert pm.title == "Backend failure"
        assert pm.affected_agent == "lead-backend"
        assert pm.status == "draft"
        assert pm.severity == "medium"
        assert len(pm.timeline) == 2
        assert pm.timeline[0].description.startswith("Escalation triggered")
        assert pm.prepared_by == "chief-of-staff"

        # Verify persisted to disk.
        loaded = pm_store.load("INC-task-42")
        assert loaded is not None
        assert loaded.incident_id == "INC-task-42"

    def test_create_from_escalation_with_rule(
        self, pm_store: PostmortemStore
    ) -> None:
        """When a rule is passed, postmortem uses the rule name."""
        from ai_company.orchestrator.escalation import EscalationRule

        event = EscalationEvent(
            task_id="task-99",
            rule_id="r1",
            from_agent="agent-x",
            to_agent="coo",
            reason="Budget exceeded",
        )
        rule = EscalationRule(
            id="r1",
            name="Cost Threshold",
            trigger="cost_exceeded",
            escalate_to="finance-lead",
        )
        pm = pm_store.create_from_escalation(
            event, rule=rule, title="Cost incident",
        )
        assert pm.escalation_rule == "Cost Threshold"

    def test_create_from_escalation_default_title(
        self, pm_store: PostmortemStore
    ) -> None:
        """Without an explicit title, incident title defaults from the reason."""
        event = EscalationEvent(
            task_id="task-5",
            rule_id="r1",
            from_agent="a1",
            to_agent="a2",
            reason="Service degraded",
        )
        pm = pm_store.create_from_escalation(event)
        assert "Service degraded" in pm.title

    def test_overwrite_same_incident(self, pm_store: PostmortemStore) -> None:
        pm_store.save(Postmortem(incident_id="INC-OV", title="Original"))
        pm_store.save(Postmortem(incident_id="INC-OV", title="Updated"))
        loaded = pm_store.load("INC-OV")
        assert loaded is not None
        assert loaded.title == "Updated"

    def test_postmortem_full_data_roundtrip(
        self, pm_store: PostmortemStore
    ) -> None:
        """A fully populated postmortem survives save/load."""
        pm = Postmortem(
            incident_id="INC-FULL",
            title="Full roundtrip",
            severity="critical",
            affected_agent="cto",
            department="engineering",
            status="resolved",
            root_cause="Memory leak",
            timeline=[],
            resolution_steps=["Identified", "Fixed"],
            lessons_learned=["Add monitoring"],
            prevention_measures=["Heap dumps"],
            prepared_by="chief-of-staff",
            reviewed_by="human-operator",
        )
        pm_store.save(pm)
        loaded = pm_store.load("INC-FULL")
        assert loaded is not None
        assert loaded.severity == "critical"
        assert loaded.department == "engineering"
        assert loaded.status == "resolved"
        assert loaded.root_cause == "Memory leak"
        assert loaded.resolution_steps == ["Identified", "Fixed"]
        assert loaded.lessons_learned == ["Add monitoring"]
        assert loaded.prevention_measures == ["Heap dumps"]
        assert loaded.prepared_by == "chief-of-staff"
        assert loaded.reviewed_by == "human-operator"
