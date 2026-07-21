"""Integration tests for approval escalation (Phase 3C).

Covers the HITL gate parking/unparking flow, escalation rule loading,
approval timeout, and preapproved bypass — all wired through the real
Executor + MessageBus + ApprovalGate with a mocked LLM layer.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from ai_company.executor.hitl_gate import HITLGate
from ai_company.executor.tool_runner import HITLParked
from ai_company.models import TaskStatus
from ai_company.orchestrator.approval import ApprovalStatus
from ai_company.orchestrator.escalation import EscalationManager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _loop_result(
    result: str = "Task completed.",
    *,
    done: bool = True,
    error: str = "",
) -> Any:
    """Build a ``LoopResult``-compatible object for the executor to consume.

    ``agent_loop.run()`` returns a ``LoopResult`` (not a ``ChatResponse``),
    so tests that mock the agent loop's return value must provide an object
    with ``tool_results``, ``final_response``, ``done``, etc.
    """
    from tests.integration.conftest import FakeLoopResult

    return FakeLoopResult(
        final_response=result,
        done=done,
        error=error,
    )


def _inbox_tasks(workspace: Path) -> list[dict]:
    raw = (workspace / ".opencode" / "inbox.json").read_text(encoding="utf-8")
    return json.loads(raw)


def _submit_task(
    workspace: Path,
    task_id: str = "task-hitl-001",
    instruction: str = "Write to src/important.py",
    *,
    priority: str = "high",
) -> None:
    """Write a single pending task directly into the inbox."""
    inbox = workspace / ".opencode" / "inbox.json"
    inbox.write_text(
        json.dumps([
            {
                "id": task_id,
                "sender_id": "human-ceo",
                "receiver_id": "test-agent",
                "instruction": instruction,
                "status": "pending",
                "priority": priority,
            }
        ]),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestHitlGateParksTask:
    """1. Task with HITL-gated tool raises HITLParked → stays WAITING_APPROVAL."""

    def test_hitl_gate_parks_task(self, executor, workspace: Path) -> None:
        _submit_task(workspace)

        # Simulate agent loop raising HITLParked on the first call.
        # The HITLParked needs a valid request_id, so we first let the
        # real HITL gate create one, then raise.
        hitl_gate = executor.hitl

        def _raising_run(*args: Any, **kwargs: Any) -> Any:
            request_id = hitl_gate.request_and_park(
                task_id="task-hitl-001",
                agent_id="test-agent",
                tool="write",
                args={"path": "src/important.py", "content": "data"},
            )
            raise HITLParked(
                task_id="task-hitl-001",
                agent_id="test-agent",
                tool="write",
                request_id=request_id,
                tier=2,
            )

        executor.agent_loop.run = _raising_run  # type: ignore[assignment]

        count = executor.tick()
        assert count == 1

        # Task should be parked in WAITING_APPROVAL, not completed/failed.
        tasks = _inbox_tasks(workspace)
        assert len(tasks) == 1
        assert tasks[0]["status"] == TaskStatus.WAITING_APPROVAL.value

        # The executor should have recorded the pending approval mapping.
        assert "task-hitl-001" in executor._pending_approvals


class TestApprovalUnblocksTask:
    """2. After parking, approving via HITLGate resumes execution."""

    def test_approval_unblocks_task(self, executor, workspace: Path) -> None:
        _submit_task(workspace)

        hitl_gate = executor.hitl
        call_count = 0

        def _run_side_effect(*args: Any, **kwargs: Any) -> Any:
            nonlocal call_count
            call_count += 1

            if call_count == 1:
                # First call: park the task.
                request_id = hitl_gate.request_and_park(
                    task_id="task-hitl-001",
                    agent_id="test-agent",
                    tool="write",
                    args={"path": "src/important.py", "content": "data"},
                )
                raise HITLParked(
                    task_id="task-hitl-001",
                    agent_id="test-agent",
                    tool="write",
                    request_id=request_id,
                    tier=2,
                )

            # Second call (after approval): succeed normally with a LoopResult.
            return _loop_result(result="Write completed.", done=True)

        executor.agent_loop.run = _run_side_effect  # type: ignore[assignment]

        # Tick 1 — parks the task.
        executor.tick()
        tasks = _inbox_tasks(workspace)
        assert tasks[0]["status"] == TaskStatus.WAITING_APPROVAL.value

        # Approve the request via the ApprovalGate.
        pending = hitl_gate.gate.get_pending_requests()
        assert len(pending) >= 1, "Expected at least one pending approval request"
        request_id = pending[0].id
        hitl_gate.gate.approve(request_id, approved_by="human-ceo")

        # Tick 2 — _resume_parked_tasks detects approval and re-processes.
        executor.tick()

        tasks = _inbox_tasks(workspace)
        assert tasks[0]["status"] == TaskStatus.COMPLETED.value
        assert "Write completed" in tasks[0]["result"]
        assert call_count == 2, "agent_loop.run should have been called twice"


class TestEscalationRulesLoad:
    """3. Verify escalation.yaml rules are loaded correctly."""

    def test_escalation_rules_load(self, workspace: Path) -> None:
        escalation_yaml = workspace / "orchestrator" / "escalation.yaml"
        escalation_yaml.write_text(
            "rules:\n"
            "- id: hitl-timeout\n"
            "  name: HITL Timeout Escalation\n"
            "  trigger: hitl_timeout\n"
            "  escalate_to: chief-of-staff\n"
            "  max_retries: 3\n"
            "  timeout_minutes: 30\n"
            "  enabled: true\n"
            "- id: critical-failure\n"
            "  name: Critical Failure Escalation\n"
            "  trigger: critical_failure\n"
            "  escalate_to: human-ceo\n"
            "  max_retries: 1\n"
            "  timeout_minutes: 10\n"
            "  enabled: true\n",
            encoding="utf-8",
        )

        manager = EscalationManager(config_path=str(escalation_yaml))
        rules = manager.list_rules()

        assert len(rules) == 2

        r1 = next(r for r in rules if r.id == "hitl-timeout")
        assert r1.name == "HITL Timeout Escalation"
        assert r1.trigger == "hitl_timeout"
        assert r1.escalate_to == "chief-of-staff"
        assert r1.max_retries == 3
        assert r1.timeout_minutes == 30
        assert r1.enabled is True

        r2 = next(r for r in rules if r.id == "critical-failure")
        assert r2.name == "Critical Failure Escalation"
        assert r2.trigger == "critical_failure"
        assert r2.escalate_to == "human-ceo"
        assert r2.max_retries == 1
        assert r2.timeout_minutes == 10
        assert r2.enabled is True

    def test_escalation_rules_load_empty(self, workspace: Path) -> None:
        """Loading an escalation file with no rules produces an empty list."""
        escalation_yaml = workspace / "orchestrator" / "escalation.yaml"
        escalation_yaml.write_text("rules: []\n", encoding="utf-8")

        manager = EscalationManager(config_path=str(escalation_yaml))
        assert manager.list_rules() == []

    def test_escalation_trigger_creates_event(self, workspace: Path) -> None:
        """Triggering an escalation rule produces an EscalationEvent."""
        escalation_yaml = workspace / "orchestrator" / "escalation.yaml"
        escalation_yaml.write_text(
            "rules:\n"
            "- id: timeout-rule\n"
            "  name: Timeout\n"
            "  trigger: hitl_timeout\n"
            "  escalate_to: chief-of-staff\n"
            "  timeout_minutes: 15\n",
            encoding="utf-8",
        )

        manager = EscalationManager(config_path=str(escalation_yaml))
        event = manager.trigger_escalation(
            task_id="task-escalate-001",
            rule_id="timeout-rule",
            from_agent="test-agent",
            reason="HITL request expired",
        )

        assert event is not None
        assert event.task_id == "task-escalate-001"
        assert event.to_agent == "chief-of-staff"
        assert event.reason == "HITL request expired"
        assert event.resolved is False

        pending = manager.get_pending_escalations()
        assert len(pending) == 1
        assert pending[0].task_id == "task-escalate-001"


class TestApprovalTimeout:
    """4. Task parked too long without approval is escalated or failed."""

    def test_approval_timeout_fails_task(self, executor, workspace: Path) -> None:
        """When the HITL request expires, resume_approved returns False and
        the task is transitioned to FAILED."""
        _submit_task(workspace)

        hitl_gate = executor.hitl

        # Use a very short timeout so the request expires quickly.
        original_timeout = hitl_gate.timeout_minutes
        hitl_gate.timeout_minutes = 0  # expires immediately

        def _raising_run(*args: Any, **kwargs: Any) -> Any:
            request_id = hitl_gate.request_and_park(
                task_id="task-hitl-001",
                agent_id="test-agent",
                tool="write",
                args={"path": "src/important.py", "content": "data"},
            )
            raise HITLParked(
                task_id="task-hitl-001",
                agent_id="test-agent",
                tool="write",
                request_id=request_id,
                tier=2,
            )

        executor.agent_loop.run = _raising_run  # type: ignore[assignment]

        # Tick 1 — parks the task.
        executor.tick()
        tasks = _inbox_tasks(workspace)
        assert tasks[0]["status"] == TaskStatus.WAITING_APPROVAL.value

        # Backdate the approval request so it's already expired.
        for req in hitl_gate.gate.requests:
            if req.status == ApprovalStatus.PENDING:
                req.expires_at = datetime.now() - timedelta(minutes=1)
        hitl_gate.gate._save_config()

        # Tick 2 — resume_approved sees the expired request → fails the task.
        executor.tick()

        tasks = _inbox_tasks(workspace)
        assert tasks[0]["status"] == TaskStatus.FAILED.value
        assert "denied" in tasks[0]["result"].lower() or "approval" in tasks[0]["result"].lower()

        # Restore original timeout.
        hitl_gate.timeout_minutes = original_timeout

    def test_approval_rejection_fails_task(self, executor, workspace: Path) -> None:
        """Explicit rejection also transitions the task to FAILED."""
        _submit_task(workspace)

        hitl_gate = executor.hitl

        def _raising_run(*args: Any, **kwargs: Any) -> Any:
            request_id = hitl_gate.request_and_park(
                task_id="task-hitl-001",
                agent_id="test-agent",
                tool="execute",
                args={"command": "rm -rf /tmp/test"},
            )
            raise HITLParked(
                task_id="task-hitl-001",
                agent_id="test-agent",
                tool="execute",
                request_id=request_id,
                tier=3,
            )

        executor.agent_loop.run = _raising_run  # type: ignore[assignment]

        # Tick 1 — parks.
        executor.tick()
        tasks = _inbox_tasks(workspace)
        assert tasks[0]["status"] == TaskStatus.WAITING_APPROVAL.value

        # Reject the approval request.
        pending = hitl_gate.gate.get_pending_requests()
        assert len(pending) >= 1
        hitl_gate.gate.reject(pending[0].id, rejected_by="human-ceo", notes="Too risky")

        # Tick 2 — resume detects rejection → fail.
        executor.tick()

        tasks = _inbox_tasks(workspace)
        assert tasks[0]["status"] == TaskStatus.FAILED.value
        assert "denied" in tasks[0]["result"].lower()


class TestPreapprovedBypassesHitl:
    """5. ``preapproved=True`` skips HITL gate entirely."""

    def test_preapproved_bypasses_hitl(self, executor, workspace: Path) -> None:
        """When the executor resumes a parked task with preapproved=True,
        the agent_loop.run call passes preapproved=True so the HITL-gated
        step executes directly without re-raising HITLParked."""
        _submit_task(workspace)

        hitl_gate = executor.hitl
        call_count = 0

        def _run_with_park(*args: Any, **kwargs: Any) -> Any:
            nonlocal call_count
            call_count += 1

            if call_count == 1:
                # First call — park.
                request_id = hitl_gate.request_and_park(
                    task_id="task-hitl-001",
                    agent_id="test-agent",
                    tool="write",
                    args={"path": "src/important.py", "content": "data"},
                )
                raise HITLParked(
                    task_id="task-hitl-001",
                    agent_id="test-agent",
                    tool="write",
                    request_id=request_id,
                    tier=2,
                )

            # Subsequent calls — verify preapproved was passed.
            assert kwargs.get("preapproved") is True, (
                "Expected preapproved=True on resume call"
            )
            return _loop_result(result="Preapproved write done.", done=True)

        executor.agent_loop.run = _run_with_park  # type: ignore[assignment]

        # Tick 1 — parks.
        executor.tick()
        tasks = _inbox_tasks(workspace)
        assert tasks[0]["status"] == TaskStatus.WAITING_APPROVAL.value

        # Approve the request.
        pending = hitl_gate.gate.get_pending_requests()
        assert len(pending) >= 1
        hitl_gate.gate.approve(pending[0].id, approved_by="human-ceo")

        # Tick 2 — resumes with preapproved=True.
        executor.tick()

        tasks = _inbox_tasks(workspace)
        assert tasks[0]["status"] == TaskStatus.COMPLETED.value
        assert "Preapproved write done" in tasks[0]["result"]
        assert call_count == 2

    def test_preapproved_flag_reaches_agent_loop(
        self, executor, workspace: Path
    ) -> None:
        """Verify the preapproved flag propagates from _resume_parked_tasks
        through _process_task into agent_loop.run kwargs."""
        _submit_task(workspace)

        hitl_gate = executor.hitl
        captured_kwargs: list[dict[str, Any]] = []

        def _capturing_run(*args: Any, **kwargs: Any) -> Any:
            captured_kwargs.append(dict(kwargs))
            if len(captured_kwargs) == 1:
                request_id = hitl_gate.request_and_park(
                    task_id="task-hitl-001",
                    agent_id="test-agent",
                    tool="write",
                    args={"path": "src/important.py", "content": "x"},
                )
                raise HITLParked(
                    task_id="task-hitl-001",
                    agent_id="test-agent",
                    tool="write",
                    request_id=request_id,
                    tier=2,
                )
            return _loop_result(result="Done.", done=True)

        executor.agent_loop.run = _capturing_run  # type: ignore[assignment]

        # Tick 1 — park.
        executor.tick()

        # Approve.
        pending = hitl_gate.gate.get_pending_requests()
        hitl_gate.gate.approve(pending[0].id, approved_by="human-ceo")

        # Tick 2 — resume.
        executor.tick()

        assert len(captured_kwargs) == 2
        # First call: preapproved not passed (defaults to False).
        assert captured_kwargs[0].get("preapproved", False) is False
        # Second call: preapproved=True because resume path passes it.
        assert captured_kwargs[1]["preapproved"] is True


class TestHitlGateUnit:
    """Supplementary unit-level checks on HITLGate directly."""

    def test_request_and_park_creates_pending(self) -> None:
        """request_and_park creates a PENDING approval and tracks it."""
        gate = HITLGate(poll_interval=1, timeout_minutes=60)
        request_id = gate.request_and_park(
            task_id="task-001",
            agent_id="agent-a",
            tool="execute",
            args={"command": "pytest"},
        )
        assert request_id.startswith("hitl-")
        assert gate.has_pending_requests()

        req = gate.gate.get_request(request_id)
        assert req is not None
        assert req.status == ApprovalStatus.PENDING

    def test_resume_approved_returns_none_while_pending(self) -> None:
        gate = HITLGate(poll_interval=1, timeout_minutes=60)
        request_id = gate.request_and_park(
            task_id="task-002",
            agent_id="agent-b",
            tool="write",
            args={"path": "src/foo.py", "content": "x"},
        )
        result = gate.resume_approved(request_id)
        assert result is None

    def test_resume_approved_returns_true_after_approval(self) -> None:
        gate = HITLGate(poll_interval=1, timeout_minutes=60)
        request_id = gate.request_and_park(
            task_id="task-003",
            agent_id="agent-c",
            tool="write",
            args={"path": "src/bar.py", "content": "y"},
        )
        gate.gate.approve(request_id, approved_by="human-ceo")
        result = gate.resume_approved(request_id)
        assert result is True
        assert not gate.has_pending_requests()

    def test_resume_approved_returns_false_after_rejection(self) -> None:
        gate = HITLGate(poll_interval=1, timeout_minutes=60)
        request_id = gate.request_and_park(
            task_id="task-004",
            agent_id="agent-d",
            tool="execute",
            args={"command": "rm -rf /"},
        )
        gate.gate.reject(request_id, rejected_by="human-ceo")
        result = gate.resume_approved(request_id)
        assert result is False

    def test_resume_all_parked_requests(self) -> None:
        """Multiple parked requests can each be polled via resume_approved."""
        gate = HITLGate(poll_interval=1, timeout_minutes=60)
        r1 = gate.request_and_park("t1", "a", "write", {"path": "a.py", "content": ""})
        r2 = gate.request_and_park("t2", "b", "write", {"path": "b.py", "content": ""})
        r3 = gate.request_and_park("t3", "c", "write", {"path": "c.py", "content": ""})

        gate.gate.approve(r1, approved_by="ceo")
        gate.gate.reject(r3, rejected_by="ceo")

        # Use resume_approved() per-request — the actual method the executor
        # uses for non-blocking HITL (resolve_all_pending only works with
        # futures from request_and_wait, not request_and_park).
        assert gate.resume_approved(r1) is True
        assert gate.resume_approved(r2) is None  # still pending
        assert gate.resume_approved(r3) is False

    def test_cancel_removes_pending_request(self) -> None:
        gate = HITLGate(poll_interval=1, timeout_minutes=60)
        request_id = gate.request_and_park(
            task_id="task-005",
            agent_id="agent-e",
            tool="write",
            args={"path": "x.py", "content": ""},
        )
        # request_and_park doesn't create a future, but cancel should
        # remove it from pending.
        gate.cancel(request_id)
        assert not gate.has_pending_requests()
        # resume_approved returns None because request is gone from _pending_requests.
        assert gate.resume_approved(request_id) is None

    def test_resume_approved_expired_request(self) -> None:
        """resume_approved returns False for an expired request."""
        gate = HITLGate(poll_interval=1, timeout_minutes=0)
        request_id = gate.request_and_park(
            task_id="task-006",
            agent_id="agent-f",
            tool="write",
            args={"path": "y.py", "content": ""},
        )
        # Backdate the expiry so it's already expired.
        req = gate.gate.get_request(request_id)
        assert req is not None
        req.expires_at = datetime.now() - timedelta(minutes=1)
        gate.gate._save_config()

        result = gate.resume_approved(request_id)
        assert result is False
