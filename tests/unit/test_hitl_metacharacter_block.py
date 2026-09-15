"""Tests for ticket #70 — HITL must never approve a command the executor
can never run (GAP-016 shell-metacharacter rejection).

Verifies the approval-time validation design:
- A metacharacter command is rejected by ToolRunner WITHOUT approval and
  STILL rejected WITH ``preapproved=True`` (execution stays fail-closed).
- ``HITLGate`` flags the persisted request (``metacharacter_blocked=True``)
  and warns the human in the request description at creation time.
- The executor's resume path fails a flagged-approved task FAST with an
  explicit message instead of re-running the loop and silently retrying
  the un-runnable command until max iterations.
- Clean commands are NOT flagged and still resume normally.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_company.executor.hitl_gate import HITLGate
from ai_company.executor.tool_runner import HITLParked, ToolRunner
from ai_company.models.models import TaskStatus
from ai_company.orchestrator.approval import ApprovalGate

PIPE_COMMAND = "grep 'error' .opencode/audit.jsonl | grep -oP 'foo'"


@pytest.fixture(autouse=True)
def _anchor_data_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Anchor DASHBOARD_DATA_DIR so default-constructed MessageBus / AuditWriter
    stay inside the per-test tmp dir instead of the real project directory."""
    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))
    from tests.unit.conftest import patch_local_only_httpx

    patch_local_only_httpx(monkeypatch)
    from ai_company.executor import loop as loop_mod
    from ai_company.memory.engine import MemoryStore

    isolated = MemoryStore(base_dir=str(tmp_path / "memory"))
    monkeypatch.setattr(loop_mod, "init_memory", lambda *a, **kw: isolated)


def _make_gate(tmp_path: Path) -> HITLGate:
    gate = ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))
    return HITLGate(approval_gate=gate, poll_interval=0.05, timeout_minutes=0.05)


# ── Execution stays fail-closed (with or without approval) ───────────


class TestExecutionFailClosed:
    def test_pipe_command_rejected_without_approval(self, tmp_path: Path) -> None:
        """Regression guard: a pipe command is still rejected with no gate."""
        runner = ToolRunner(project_root=tmp_path)
        results = runner.run_plan([{"tool": "execute", "args": {"command": PIPE_COMMAND}}])
        assert results[0]["status"] == "error"
        assert "metacharacter" in results[0]["error"].lower()

    def test_pipe_command_still_rejected_with_preapproved(self, tmp_path: Path) -> None:
        """HITL approval (preapproved=True) must NEVER bypass the metacharacter
        filter — 'honoring' an approved pipe would either silently do the
        wrong thing (tokenized, no pipe semantics) or require shell=True."""
        runner = ToolRunner(project_root=tmp_path)
        results = runner.run_plan(
            [{"tool": "execute", "args": {"command": PIPE_COMMAND}}],
            preapproved=True,
        )
        assert results[0]["status"] == "error"
        assert "metacharacter" in results[0]["error"].lower()


# ── HITLGate flags + warns at request creation ───────────────────────


class TestHITLGateFlags:
    def test_request_and_park_flags_metacharacter_command(self, tmp_path: Path) -> None:
        hitl = _make_gate(tmp_path)
        request_id = hitl.request_and_park(
            task_id="t-pipe",
            agent_id="agent-1",
            tool="execute",
            args={"command": PIPE_COMMAND},
        )
        req = hitl.gate.get_request(request_id)
        assert req is not None
        # Flag persisted on the request so the resume path can read it.
        assert req.metacharacter_blocked is True
        assert hitl.is_metacharacter_blocked(request_id) is True
        # The human sees the warning in the request description (dashboard +
        # CLI both surface ``description``).
        assert "[BLOCKED]" in req.description
        assert "|" in req.description

    def test_request_and_park_clean_command_not_flagged(self, tmp_path: Path) -> None:
        hitl = _make_gate(tmp_path)
        request_id = hitl.request_and_park(
            task_id="t-clean",
            agent_id="agent-1",
            tool="bash",
            args={"command": "grep 'error' .opencode/audit.jsonl"},
        )
        req = hitl.gate.get_request(request_id)
        assert req is not None
        assert req.metacharacter_blocked is False
        assert hitl.is_metacharacter_blocked(request_id) is False
        assert "[BLOCKED]" not in req.description

    def test_non_command_tool_not_flagged(self, tmp_path: Path) -> None:
        hitl = _make_gate(tmp_path)
        request_id = hitl.request_and_park(
            task_id="t-write",
            agent_id="agent-1",
            tool="write",
            args={"path": "src/app.py", "content": "x"},
        )
        assert hitl.is_metacharacter_blocked(request_id) is False

    def test_request_and_wait_flags_metacharacter_command(self, tmp_path: Path) -> None:
        """The blocking wait path (request_and_wait_sync) flags too."""
        hitl = _make_gate(tmp_path)
        future = hitl.request_and_wait(
            task_id="t-pipe-wait",
            agent_id="agent-1",
            tool="execute",
            args={"command": PIPE_COMMAND},
        )
        request_id = next(iter(hitl._pending_requests))
        assert hitl.is_metacharacter_blocked(request_id) is True
        # Avoid a lingering poll thread — cancel and clean up.
        hitl.cancel(request_id)
        future.cancel()

    def test_legacy_request_without_flag_not_blocked(self, tmp_path: Path) -> None:
        """A persisted request from before the flag exists (no key in YAML)
        must load as False and resume as before."""
        gate = ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))
        gate.request_approval("legacy-1", "t-1", "a-1", "tool:bash", "Execute: echo hi")
        hitl = HITLGate(approval_gate=gate)
        assert hitl.is_metacharacter_blocked("legacy-1") is False


# ── Executor resume path: fail fast, do not retry ────────────────────


def _setup_executor_files(tmp_path: Path) -> None:
    company = tmp_path / "company"
    company.mkdir()
    models = {
        "providers": {
            "opencode": {
                "backend": "openai_compatible",
                "default_model": "big-pickle",
                "api_base": "https://opencode.ai/api/v1",
            }
        },
        "tiers": {
            "standard": {
                "description": "std",
                "providers": [{"provider": "opencode", "model": "big-pickle"}],
            }
        },
        "routing": [{"agent_type": "Specialist", "tier": "standard"}],
    }
    (company / "models.yaml").write_text(json.dumps(models), encoding="utf-8")
    registry = [
        {
            "name": "test-agent",
            "role": "Test",
            "type": "Specialist",
            "department": "Test",
            "reportsTo": "ceo",
            "directReports": [],
            "description": "test",
            "tools": ["read", "write", "execute"],
            "permission": "Execute",
        }
    ]
    (company / "agent-registry.json").write_text(json.dumps(registry), encoding="utf-8")
    op = tmp_path / ".opencode"
    op.mkdir()
    (op / "inbox.json").write_text("[]", encoding="utf-8")
    (tmp_path / "orchestrator").mkdir(exist_ok=True)
    (tmp_path / "orchestrator" / "approvals.yaml").write_text("requests: []", encoding="utf-8")
    agents = op / "agents"
    agents.mkdir()
    (agents / "test-agent.md").write_text(
        '---\nname: test-agent\ndescription: t\ntools: ["read", "write", "execute"]\n'
        "mode: subagent\npermission:\n  read: allow\n  write: allow\n  bash: allow\n---\n\n"
        "# Test Agent\n\nType: Specialist\nDepartment: Test\nReports To: ceo\n\n"
        "## Mission\nExecute tasks.\n",
        encoding="utf-8",
    )


class TestExecutorResume:
    def test_approved_blocked_request_fails_fast(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Ticket #70 core regression: approving a pipe command must NOT
        re-run the loop and retry an un-runnable command until max iterations.
        It fails fast with an explicit message instead."""
        monkeypatch.chdir(tmp_path)
        _setup_executor_files(tmp_path)

        inbox = tmp_path / ".opencode" / "inbox.json"
        inbox.write_text(
            json.dumps(
                [
                    {
                        "id": "task-pipe-1",
                        "sender_id": "human-ceo",
                        "receiver_id": "test-agent",
                        "instruction": "Find errors in audit log",
                        "status": "pending",
                        "priority": "high",
                    }
                ]
            ),
            encoding="utf-8",
        )

        from ai_company.executor.agent_loop import LoopResult
        from ai_company.executor.loop import Executor

        executor = Executor(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
            agents_dir=str(tmp_path / ".opencode" / "agents"),
            results_dir=str(tmp_path / "results"),
        )

        calls = {"n": 0}

        def fake_run(*args: object, **kwargs: object) -> object:
            calls["n"] += 1
            if kwargs["preapproved"] is False:
                # Mimic ToolRunner non-blocking parking for the gated step:
                # the command contains a pipe, so the request must be flagged.
                rid = executor.hitl.request_and_park(
                    task_id=kwargs["task_id"],
                    agent_id=kwargs["agent_name"],
                    tool="execute",
                    args={"command": PIPE_COMMAND},
                )
                raise HITLParked(
                    task_id=kwargs["task_id"],
                    agent_id=kwargs["agent_name"],
                    tool="execute",
                    request_id=rid,
                    tier=2,
                )
            return LoopResult(
                final_response="should never run",
                iterations=1,
                tool_results=[],
                total_prompt_tokens=10,
                total_completion_tokens=5,
                total_cost_usd=0.0,
                done=True,
                error="",
            )

        executor.agent_loop.run = MagicMock(side_effect=fake_run)

        # First tick: park the task (request flagged at creation time).
        assert executor.tick() == 1
        parked = json.loads(inbox.read_text(encoding="utf-8"))
        assert parked[0]["status"] == TaskStatus.WAITING_APPROVAL.value
        request_id = executor._pending_approvals["task-pipe-1"]
        assert executor.hitl.is_metacharacter_blocked(request_id) is True

        # Human approves anyway (despite the [BLOCKED] warning).
        executor.hitl.gate.approve(request_id, "human-ceo")
        executor.tick()

        # Fail fast: no second run of the loop, task FAILED with a clear reason.
        updated = json.loads(inbox.read_text(encoding="utf-8"))
        assert updated[0]["status"] == TaskStatus.FAILED.value
        assert "metacharacters" in updated[0]["result"]
        assert "task-pipe-1" not in executor._pending_approvals
        assert calls["n"] == 1  # the loop was NOT re-run to retry

    def test_approved_clean_command_still_resumes(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Regression guard: an approved clean (non-flagged) command keeps the
        existing resume behaviour — the loop re-runs with preapproved=True."""
        monkeypatch.chdir(tmp_path)
        _setup_executor_files(tmp_path)

        inbox = tmp_path / ".opencode" / "inbox.json"
        inbox.write_text(
            json.dumps(
                [
                    {
                        "id": "task-clean-1",
                        "sender_id": "human-ceo",
                        "receiver_id": "test-agent",
                        "instruction": "Grep audit log",
                        "status": "pending",
                        "priority": "high",
                    }
                ]
            ),
            encoding="utf-8",
        )

        from ai_company.executor.agent_loop import LoopResult
        from ai_company.executor.loop import Executor

        executor = Executor(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
            agents_dir=str(tmp_path / ".opencode" / "agents"),
            results_dir=str(tmp_path / "results"),
        )

        calls = {"n": 0}

        def fake_run(*args: object, **kwargs: object) -> object:
            calls["n"] += 1
            if kwargs["preapproved"] is False:
                rid = executor.hitl.request_and_park(
                    task_id=kwargs["task_id"],
                    agent_id=kwargs["agent_name"],
                    tool="execute",
                    args={"command": "grep 'error' .opencode/audit.jsonl"},
                )
                raise HITLParked(
                    task_id=kwargs["task_id"],
                    agent_id=kwargs["agent_name"],
                    tool="execute",
                    request_id=rid,
                    tier=2,
                )
            return LoopResult(
                final_response="Found 3 errors.",
                iterations=1,
                tool_results=[],
                total_prompt_tokens=10,
                total_completion_tokens=5,
                total_cost_usd=0.0,
                done=True,
                error="",
            )

        executor.agent_loop.run = MagicMock(side_effect=fake_run)

        assert executor.tick() == 1
        request_id = executor._pending_approvals["task-clean-1"]
        assert executor.hitl.is_metacharacter_blocked(request_id) is False

        executor.hitl.gate.approve(request_id, "human-ceo")
        executor.tick()

        updated = json.loads(inbox.read_text(encoding="utf-8"))
        assert updated[0]["status"] == TaskStatus.COMPLETED.value
        assert "Found 3 errors." in updated[0]["result"]
        assert calls["n"] == 2  # parked run + resumed preapproved run
