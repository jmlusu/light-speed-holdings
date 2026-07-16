"""Tests for the orchestrator tick cycle."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from ai_company.orchestrator.approval import ApprovalGate
from ai_company.orchestrator.escalation import EscalationManager
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
