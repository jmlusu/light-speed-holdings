"""Tests for the orchestrator tick cycle."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from ai_company.orchestrator.approval import ApprovalGate
from ai_company.orchestrator.escalation import (
    EscalationManager,
    Postmortem,
    PostmortemStore,
    TimelineEntry,
    ActionItem,
    ImpactAssessment,
)
from ai_company.orchestrator.scheduler import Scheduler


@pytest.fixture()
def scheduler(tmp_path: Path) -> Scheduler:
    return Scheduler(config_path=str(tmp_path / "scheduler.yaml"))


@pytest.fixture()
def escalation(tmp_path: Path) -> EscalationManager:
    return EscalationManager(config_path=str(tmp_path / "escalation.yaml"))


@pytest.fixture()
def gate(tmp_path: Path) -> ApprovalGate:
    return ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))


@pytest.fixture()
def pm_store(tmp_path: Path) -> PostmortemStore:
    return PostmortemStore(storage_dir=str(tmp_path / "postmortems"))


def test_scheduler_pending_empty(scheduler: Scheduler) -> None:
    assert scheduler.get_pending_tasks() == []


def test_scheduler_pending_after_add(scheduler: Scheduler) -> None:
    scheduler.add_task("t1", "Test Task", interval_minutes=60)
    # Force next_run into the past so it's "due"
    scheduler.tasks[0].next_run = datetime.now() - timedelta(minutes=1)
    pending = scheduler.get_pending_tasks()
    assert len(pending) == 1
    assert pending[0].id == "t1"


def test_scheduler_mark_completed_reschedules(scheduler: Scheduler) -> None:
    scheduler.add_task("t1", "Test Task", interval_minutes=60)
    scheduler.tasks[0].next_run = datetime.now() - timedelta(minutes=1)
    scheduler.mark_completed("t1")
    task = scheduler.tasks[0]
    assert task.last_run is not None
    assert task.next_run > datetime.now()


def test_escalation_pending_empty(escalation: EscalationManager) -> None:
    assert escalation.get_pending_escalations() == []


def test_escalation_trigger_and_pending(escalation: EscalationManager) -> None:
    escalation.add_rule("r1", "Timeout", "task_timeout", "chief-of-staff")
    evt = escalation.trigger_escalation("task-1", "r1", "cto", "timed out")
    assert evt is not None
    assert evt.to_agent == "chief-of-staff"
    pending = escalation.get_pending_escalations()
    assert len(pending) == 1


def test_escalation_resolve(escalation: EscalationManager) -> None:
    escalation.add_rule("r1", "Timeout", "task_timeout", "chief-of-staff")
    escalation.trigger_escalation("task-1", "r1", "cto", "timed out")
    escalation.resolve_escalation("task-1")
    assert escalation.get_pending_escalations() == []


def test_approval_pending_empty(gate: ApprovalGate) -> None:
    assert gate.get_pending_requests() == []


def test_approval_request_and_approve(gate: ApprovalGate) -> None:
    req = gate.request_approval("a1", "task-1", "cto", "deploy", "Deploy to prod")
    assert req.status.value == "pending"
    result = gate.approve("a1", "human-operator")
    assert result is True
    assert gate.get_pending_requests() == []


def test_approval_request_and_reject(gate: ApprovalGate) -> None:
    gate.request_approval("a1", "task-1", "cto", "deploy", "Deploy to prod")
    result = gate.reject("a1", "human-operator", notes="Not ready")
    assert result is True
    assert gate.get_pending_requests() == []


def test_approval_expired_not_pending(gate: ApprovalGate) -> None:
    gate.request_approval("a1", "task-1", "cto", "deploy", "Deploy to prod")
    gate.requests[0].expires_at = datetime.now() - timedelta(minutes=1)
    assert gate.get_pending_requests() == []


# ─── Postmortem tests ────────────────────────────────────────────────


def test_postmortem_store_save_and_load(pm_store: PostmortemStore) -> None:
    pm = Postmortem(incident_id="INC-001", title="Test incident", severity="high")
    path = pm_store.save(pm)
    assert path.exists()

    loaded = pm_store.load("INC-001")
    assert loaded is not None
    assert loaded.incident_id == "INC-001"
    assert loaded.title == "Test incident"
    assert loaded.severity == "high"
    assert loaded.status == "draft"


def test_postmortem_store_load_nonexistent(pm_store: PostmortemStore) -> None:
    assert pm_store.load("INC-NONE") is None


def test_postmortem_store_list_all(pm_store: PostmortemStore) -> None:
    pm_store.save(Postmortem(incident_id="INC-001", title="First"))
    pm_store.save(Postmortem(incident_id="INC-002", title="Second"))
    all_pm = pm_store.list_all()
    assert len(all_pm) == 2
    ids = [pm.incident_id for pm in all_pm]
    assert "INC-001" in ids
    assert "INC-002" in ids


def test_postmortem_store_create_from_escalation(pm_store: PostmortemStore) -> None:
    from ai_company.orchestrator.escalation import EscalationEvent

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
    assert len(pm.timeline) == 2

    loaded = pm_store.load("INC-task-42")
    assert loaded is not None


def test_postmortem_model_defaults() -> None:
    pm = Postmortem(incident_id="INC-999", title="Defaults test")
    assert pm.severity == "medium"
    assert pm.status == "draft"
    assert pm.timeline == []
    assert pm.resolution_steps == []
    assert pm.action_items == []
    assert pm.impact.tasks_before == 0
    assert pm.impact.downtime_minutes == 0


def test_postmortem_model_with_full_data() -> None:
    pm = Postmortem(
        incident_id="INC-100",
        title="Full test",
        severity="critical",
        affected_agent="cto",
        department="engineering",
        escalation_rule="timeout",
        duration="2h 15m",
        status="resolved",
        root_cause="Memory leak in worker process.",
        impact=ImpactAssessment(
            tasks_before=50,
            tasks_during=12,
            tasks_after=48,
            agents_before=5,
            agents_during=2,
            agents_after=5,
            downtime_minutes=135,
        ),
        timeline=[
            TimelineEntry(time="10:00", description="Worker crashed"),
            TimelineEntry(time="10:05", description="Escalation triggered"),
            TimelineEntry(time="12:15", description="Restarted with fix"),
        ],
        resolution_steps=["Identified crash", "Applied patch", "Restarted workers"],
        action_items=[
            ActionItem(id="AI-1", action="Add memory limits", owner="devops", due_date="2026-07-24", status="open"),
        ],
        lessons_learned=["Need memory monitoring"],
        prevention_measures=["Add heap dump collection"],
        prepared_by="chief-of-staff",
        reviewed_by="human-operator",
    )
    assert pm.impact.tasks_during == 12
    assert len(pm.timeline) == 3
    assert len(pm.action_items) == 1
    assert pm.action_items[0].status == "open"


def test_postmortem_store_overwrite(pm_store: PostmortemStore) -> None:
    pm_store.save(Postmortem(incident_id="INC-OV", title="Original"))
    pm_store.save(Postmortem(incident_id="INC-OV", title="Updated"))
    loaded = pm_store.load("INC-OV")
    assert loaded is not None
    assert loaded.title == "Updated"


def test_postmortem_list_all_empty(pm_store: PostmortemStore) -> None:
    assert pm_store.list_all() == []
