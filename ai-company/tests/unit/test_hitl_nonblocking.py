"""Unit tests for GAP-004 — non-blocking HITL in the executor.

Verifies:
- ``HITLGate.request_and_park`` returns immediately (non-blocking) and
  registers a request with the SAME shared ``ApprovalGate`` hook used by
  ciso's tier enforcement (GAP-003).
- ``HITLGate.resume_approved`` reports the human decision without blocking.
- ``ToolRunner.run_plan(non_blocking=True)`` raises ``HITLParked`` instead
  of blocking; with ``preapproved=True`` it executes the gated step.
- ``Executor`` does NOT block: on hitting the HITL gate the task is parked
  in ``WAITING_APPROVAL`` and the loop moves on; a later tick with an
  approved decision resumes and completes the task.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_company.executor.tool_runner import HITLParked, ToolRunner
from ai_company.executor.hitl_gate import HITLGate
from ai_company.models.models import TaskStatus
from ai_company.orchestrator.approval import ApprovalGate


# ── HITLGate park/resume ─────────────────────────────────────────


def _make_gate(tmp_path: Path) -> HITLGate:
    gate = ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))
    return HITLGate(approval_gate=gate, poll_interval=0.05, timeout_minutes=0.05)


def test_request_and_park_is_non_blocking(tmp_path: Path) -> None:
    hitl = _make_gate(tmp_path)
    # Returns immediately (no human interaction yet).
    request_id = hitl.request_and_park(
        task_id="t-park", agent_id="agent-1", tool="write",
        args={"path": "secrets.yaml", "content": "x"},
    )
    assert request_id.startswith("hitl-")
    # Still pending -> resume_approved reports None (not blocking).
    assert hitl.resume_approved(request_id) is None
    # The SAME shared ApprovalGate hook recorded the request.
    pending = hitl.gate.get_pending_requests()
    assert any(r.id == request_id for r in pending)


def test_resume_approved_detects_decision(tmp_path: Path) -> None:
    hitl = _make_gate(tmp_path)
    request_id = hitl.request_and_park(
        task_id="t-park", agent_id="agent-1", tool="execute",
        args={"command": "rm -rf /"},
    )
    # Human rejects.
    hitl.gate.reject(request_id, "human-ceo")
    assert hitl.resume_approved(request_id) is False


# ── ToolRunner non-blocking / preapproved ─────────────────────────


def test_run_plan_non_blocking_raises_parked(tmp_path: Path) -> None:
    gate = ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))
    hitl = HITLGate(approval_gate=gate, poll_interval=0.05, timeout_minutes=0.05)
    runner = ToolRunner(project_root=tmp_path)

    with pytest.raises(HITLParked) as exc_info:
        runner.run_plan(
            [{"tool": "write", "args": {"path": "config/secrets.yaml", "content": "x"}}],
            hitl_gate=hitl,
            task_id="t-1",
            agent_id="junior_dev",
            seniority="mid",
            risk_level="high",
            non_blocking=True,
        )
    # Parked carries the request id and reuses the shared gate hook.
    assert exc_info.value.request_id.startswith("hitl-")
    assert any(r.id == exc_info.value.request_id for r in gate.get_pending_requests())


def test_run_plan_preapproved_executes(tmp_path: Path) -> None:
    gate = ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))
    hitl = HITLGate(approval_gate=gate, poll_interval=0.05, timeout_minutes=0.05)
    runner = ToolRunner(project_root=tmp_path)

    results = runner.run_plan(
        [{"tool": "write", "args": {"path": "out.py", "content": "y = 1"}}],
        hitl_gate=hitl,
        task_id="t-2",
        agent_id="junior_dev",
        seniority="mid",
        risk_level="high",
        preapproved=True,
    )
    assert results[0]["status"] == "ok"
    assert (tmp_path / "out.py").read_text() == "y = 1"


# ── Executor park + resume (non-blocking) ────────────────────────


def _setup_executor_files(tmp_path: Path) -> None:
    company = tmp_path / "company"
    company.mkdir()
    models = {
        "providers": {"opencode": {"backend": "openai_compatible",
                                    "default_model": "big-pickle",
                                    "api_base": "https://opencode.ai/api/v1"}},
        "tiers": {"standard": {"description": "std",
                                "providers": [{"provider": "opencode",
                                               "model": "big-pickle"}]}},
        "routing": [{"agent_type": "Specialist", "tier": "standard"}],
    }
    (company / "models.yaml").write_text(json.dumps(models), encoding="utf-8")
    registry = [{"name": "test-agent", "role": "Test", "type": "Specialist",
                 "department": "Test", "reportsTo": "ceo", "directReports": [],
                 "description": "test", "tools": ["read", "write"],
                 "permission": "Execute"}]
    (company / "agent-registry.json").write_text(json.dumps(registry), encoding="utf-8")
    op = tmp_path / ".opencode"
    op.mkdir()
    (op / "inbox.json").write_text("[]", encoding="utf-8")
    (tmp_path / "orchestrator").mkdir(exist_ok=True)
    (tmp_path / "orchestrator" / "approvals.yaml").write_text("requests: []", encoding="utf-8")
    agents = op / "agents"
    agents.mkdir()
    (agents / "test-agent.md").write_text(
        "---\nname: test-agent\ndescription: t\ntools: [\"read\", \"write\"]\n"
        "mode: subagent\npermission:\n  read: allow\n  write: allow\n---\n\n"
        "# Test Agent\n\nType: Specialist\nDepartment: Test\nReports To: ceo\n\n"
        "## Mission\nExecute tasks.\n",
        encoding="utf-8",
    )


def test_executor_parks_and_resumes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Executor must not block on HITL: park the task, continue, then resume."""
    monkeypatch.chdir(tmp_path)
    _setup_executor_files(tmp_path)

    # A gated task: writing to a secrets path requires HITL (tier 4).
    inbox = tmp_path / ".opencode" / "inbox.json"
    task = {
        "id": "task-hitl-1",
        "sender_id": "human-ceo",
        "receiver_id": "test-agent",
        "instruction": "Write the secret file",
        "status": "pending",
        "priority": "high",
    }
    inbox.write_text(json.dumps([task]), encoding="utf-8")

    from ai_company.executor.loop import Executor

    executor = Executor(
        config_path=str(tmp_path / "company" / "models.yaml"),
        registry_path=str(tmp_path / "company" / "agent-registry.json"),
        agents_dir=str(tmp_path / ".opencode" / "agents"),
        results_dir=str(tmp_path / "results"),
    )

    call = {"n": 0}

    def fake_run(*args: object, **kwargs: object) -> object:
        call["n"] += 1
        from ai_company.executor.agent_loop import LoopResult
        from ai_company.executor.tool_runner import HITLParked

        gated = kwargs["preapproved"] is False and call["n"] == 1
        if gated:
            # Mimic what ToolRunner does in non-blocking mode: register the
            # request with the SAME shared ApprovalGate hook, then park.
            rid = executor.hitl.request_and_park(
                task_id=kwargs["task_id"], agent_id=kwargs["agent_name"],
                tool="write", args={"path": "secrets.yaml"},
            )
            raise HITLParked(
                task_id=kwargs["task_id"], agent_id=kwargs["agent_name"],
                tool="write", request_id=rid, tier=4,
            )
        return LoopResult(
            final_response="Secret written.", iterations=1, tool_results=[],
            total_prompt_tokens=10, total_completion_tokens=5,
            total_cost_usd=0.0, done=True, error="",
        )

    executor.agent_loop.run = MagicMock(side_effect=fake_run)

    # First tick: must PARK and NOT block; task left in WAITING_APPROVAL.
    count = executor.tick()
    assert count == 1
    parked = json.loads(inbox.read_text(encoding="utf-8"))
    assert parked[0]["status"] == TaskStatus.WAITING_APPROVAL.value
    assert "task-hitl-1" in executor._pending_approvals

    # Resume: approve the parked request and tick again.
    request_id = executor._pending_approvals["task-hitl-1"]
    executor.hitl.gate.approve(request_id, "human-ceo")

    executor.tick()

    updated = json.loads(inbox.read_text(encoding="utf-8"))
    assert updated[0]["status"] == TaskStatus.COMPLETED.value
    assert "task-hitl-1" not in executor._pending_approvals


def test_executor_continues_past_parked_task(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A parked task must not prevent other pending tasks from running."""
    monkeypatch.chdir(tmp_path)
    _setup_executor_files(tmp_path)

    inbox = tmp_path / ".opencode" / "inbox.json"
    tasks = [
        {"id": "t-park", "sender_id": "h", "receiver_id": "test-agent",
         "instruction": "gated", "status": "pending", "priority": "high"},
        {"id": "t-normal", "sender_id": "h", "receiver_id": "test-agent",
         "instruction": "normal", "status": "pending", "priority": "medium"},
    ]
    inbox.write_text(json.dumps(tasks), encoding="utf-8")

    from ai_company.executor.loop import Executor

    executor = Executor(
        config_path=str(tmp_path / "company" / "models.yaml"),
        registry_path=str(tmp_path / "company" / "agent-registry.json"),
        agents_dir=str(tmp_path / ".opencode" / "agents"),
        results_dir=str(tmp_path / "results"),
    )

    def fake_run(*args: object, **kwargs: object) -> object:
        from ai_company.executor.agent_loop import LoopResult
        from ai_company.executor.tool_runner import HITLParked

        if kwargs["task_id"] == "t-park":
            rid = executor.hitl.request_and_park(
                task_id="t-park", agent_id=kwargs["agent_name"],
                tool="write", args={"path": "secrets.yaml"},
            )
            raise HITLParked(
                task_id="t-park", agent_id=kwargs["agent_name"], tool="write",
                request_id=rid, tier=4,
            )
        return LoopResult(
            final_response="done", iterations=1, tool_results=[],
            total_prompt_tokens=10, total_completion_tokens=5,
            total_cost_usd=0.0, done=True, error="",
        )

    executor.agent_loop.run = MagicMock(side_effect=fake_run)

    count = executor.tick()
    assert count == 2  # both pending tasks processed in this single pass
    updated = {t["id"]: t["status"] for t in json.loads(inbox.read_text(encoding="utf-8"))}
    assert updated["t-park"] == TaskStatus.WAITING_APPROVAL.value
    assert updated["t-normal"] == TaskStatus.COMPLETED.value
