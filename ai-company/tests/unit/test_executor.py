"""Tests for the executor modules — context, tool runner, HITL gate, loop."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_company.executor.context import (
    build_system_prompt,
    build_user_prompt,
    parse_agent_spec,
)
from ai_company.executor.tool_runner import ToolRunner
from ai_company.executor.hitl_gate import HITLGate
from ai_company.orchestrator.approval import ApprovalGate


# ── Context / Spec Parser ──────────────────────────────────────────


class TestSpecParser:
    def test_parse_existing_agent(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / ".opencode" / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "chief-of-staff.md").write_text(
            _AGENT_SPEC_SAMPLE, encoding="utf-8"
        )

        ctx = parse_agent_spec("chief-of-staff", str(agents_dir))
        assert ctx.name == "chief-of-staff"
        assert ctx.type == "Executive"
        assert ctx.department == "Office of the CEO"
        assert "read" in ctx.tools
        assert "write" in ctx.tools
        assert len(ctx.responsibilities) >= 2
        assert "orchestrate" in ctx.mission.lower() or "orchestrator" in ctx.mission.lower()

    def test_parse_missing_agent_returns_defaults(self, tmp_path: Path) -> None:
        ctx = parse_agent_spec("nonexistent", str(tmp_path / "nope"))
        assert ctx.name == "nonexistent"
        assert ctx.type == "Unknown"

    def test_parse_specialist_agent(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / ".opencode" / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "lead-backend.md").write_text(
            _SPECIALIST_SPEC_SAMPLE, encoding="utf-8"
        )

        ctx = parse_agent_spec("lead-backend", str(agents_dir))
        assert ctx.name == "lead-backend"
        assert ctx.type == "Specialist"
        assert ctx.department == "Technology"
        assert "code_interpreter" in ctx.tools

    def test_build_system_prompt_includes_key_sections(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / ".opencode" / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "agent.md").write_text(_AGENT_SPEC_SAMPLE, encoding="utf-8")

        ctx = parse_agent_spec("agent", str(agents_dir))
        prompt = build_system_prompt(ctx)

        assert "Light Speed Holdings" in prompt
        assert "RESPONSIBILITIES:" in prompt
        assert "ALLOWED TOOLS:" in prompt
        assert '"plan"' in prompt
        assert '"result"' in prompt
        assert '"artifacts"' in prompt

    def test_build_user_prompt(self) -> None:
        prompt = build_user_prompt("Build a REST API", "high")
        assert "PRIORITY: HIGH" in prompt
        assert "Build a REST API" in prompt


# ── Tool Runner ─────────────────────────────────────────────────────


class TestToolRunner:
    def test_read_file(self, tmp_path: Path) -> None:
        (tmp_path / "test.py").write_text("print('hello')", encoding="utf-8")
        runner = ToolRunner(project_root=tmp_path)

        results = runner.run_plan([{"tool": "read", "args": {"path": "test.py"}}])
        assert results[0]["status"] == "ok"
        assert "hello" in results[0]["content"]

    def test_read_nonexistent_file(self, tmp_path: Path) -> None:
        runner = ToolRunner(project_root=tmp_path)
        results = runner.run_plan([{"tool": "read", "args": {"path": "nope.py"}}])
        assert results[0]["status"] == "error"
        assert "not found" in results[0]["error"].lower()

    def test_write_file(self, tmp_path: Path) -> None:
        runner = ToolRunner(project_root=tmp_path)
        results = runner.run_plan(
            [{"tool": "write", "args": {"path": "out.py", "content": "x = 1"}}],
            hitl_gate=None,  # No HITL gate → auto-approve
        )
        assert results[0]["status"] == "ok"
        assert (tmp_path / "out.py").read_text() == "x = 1"

    def test_write_creates_parent_dirs(self, tmp_path: Path) -> None:
        runner = ToolRunner(project_root=tmp_path)
        runner.run_plan(
            [{"tool": "write", "args": {"path": "src/deep/file.py", "content": "ok"}}],
            hitl_gate=None,
        )
        assert (tmp_path / "src" / "deep" / "file.py").exists()

    def test_grep_finds_pattern(self, tmp_path: Path) -> None:
        (tmp_path / "main.py").write_text("def foo():\n    pass\ndef bar():\n    pass", encoding="utf-8")
        runner = ToolRunner(project_root=tmp_path)
        results = runner.run_plan([{"tool": "grep", "args": {"pattern": "def foo"}}])
        assert results[0]["status"] == "ok"
        assert len(results[0]["matches"]) >= 1

    def test_list_directory(self, tmp_path: Path) -> None:
        (tmp_path / "a.txt").touch()
        (tmp_path / "b.py").touch()
        runner = ToolRunner(project_root=tmp_path)
        results = runner.run_plan([{"tool": "list", "args": {"path": "."}}])
        assert results[0]["status"] == "ok"
        assert len(results[0]["entries"]) == 2

    def test_execute_command(self, tmp_path: Path) -> None:
        runner = ToolRunner(project_root=tmp_path)
        results = runner.run_plan(
            [{"tool": "execute", "args": {"command": "echo hello"}}],
            hitl_gate=None,
        )
        assert results[0]["status"] == "ok"
        assert "hello" in results[0]["stdout"]

    def test_execute_failing_command(self, tmp_path: Path) -> None:
        runner = ToolRunner(project_root=tmp_path)
        results = runner.run_plan(
            [{"tool": "execute", "args": {"command": "python -c \"exit(1)\""}}],
            hitl_gate=None,
        )
        assert results[0]["status"] == "ok"
        assert results[0]["returncode"] == 1

    def test_path_escape_blocked(self, tmp_path: Path) -> None:
        runner = ToolRunner(project_root=tmp_path)
        results = runner.run_plan([{"tool": "read", "args": {"path": "../../etc/passwd"}}])
        assert results[0]["status"] == "error"
        assert "escapes project root" in results[0]["error"]

    def test_unknown_tool(self, tmp_path: Path) -> None:
        runner = ToolRunner(project_root=tmp_path)
        results = runner.run_plan([{"tool": "unknown_tool", "args": {}}])
        assert results[0]["status"] == "error"
        assert "unknown" in results[0]["error"].lower()

    def test_multiple_steps(self, tmp_path: Path) -> None:
        (tmp_path / "input.py").write_text("data", encoding="utf-8")
        runner = ToolRunner(project_root=tmp_path)
        results = runner.run_plan([
            {"tool": "read", "args": {"path": "input.py"}},
            {"tool": "write", "args": {"path": "output.py", "content": "transformed"}},
            {"tool": "list", "args": {"path": "."}},
        ], hitl_gate=None)
        assert len(results) == 3
        assert all(r["status"] == "ok" for r in results)

    def test_delegate_returns_action(self, tmp_path: Path) -> None:
        runner = ToolRunner(project_root=tmp_path)
        results = runner.run_plan([
            {"tool": "delegate", "args": {"receiver": "lead-backend", "instruction": "Build API"}}
        ])
        assert results[0]["status"] == "ok"
        assert results[0]["action"] == "delegate"


# ── HITL Gate ───────────────────────────────────────────────────────


class TestHITLGate:
    def test_approval_creates_request(self, tmp_path: Path) -> None:
        gate = ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))
        hitl = HITLGate(approval_gate=gate, poll_interval=0.1, timeout_minutes=0.05)

        # Simulate approval in background
        import threading

        def approve_after_delay():
            import time
            time.sleep(0.3)
            requests = gate.get_pending_requests()
            if requests:
                gate.approve(requests[0].id, "human-ceo")

        t = threading.Thread(target=approve_after_delay)
        t.start()

        # request_and_wait_sync blocks until approval/rejection/timeout
        result = hitl.request_and_wait_sync(
            task_id="t-1", agent_id="agent-1", tool="write",
            args={"path": "test.py", "content": "x = 1"},
        )
        t.join()

        assert result is True

    def test_rejection_returns_false(self, tmp_path: Path) -> None:
        gate = ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))
        hitl = HITLGate(approval_gate=gate, poll_interval=0.1, timeout_minutes=0.05)

        import threading

        def reject_after_delay():
            import time
            time.sleep(0.3)
            requests = gate.get_pending_requests()
            if requests:
                gate.reject(requests[0].id, "human-ceo")

        t = threading.Thread(target=reject_after_delay)
        t.start()

        result = hitl.request_and_wait_sync(
            task_id="t-2", agent_id="agent-2", tool="execute",
            args={"command": "rm -rf /"},
        )
        t.join()

        assert result is False

    def test_future_api(self, tmp_path: Path) -> None:
        """Test the non-blocking Future-based API."""
        gate = ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))
        hitl = HITLGate(approval_gate=gate, poll_interval=0.1, timeout_minutes=0.05)

        import threading

        def approve_after_delay():
            import time
            time.sleep(0.3)
            requests = gate.get_pending_requests()
            if requests:
                gate.approve(requests[0].id, "human-ceo")

        t = threading.Thread(target=approve_after_delay)
        t.start()

        # request_and_wait returns a Future
        future = hitl.request_and_wait(
            task_id="t-3", agent_id="agent-3", tool="read",
            args={"path": "test.py"},
        )
        import concurrent.futures
        assert isinstance(future, concurrent.futures.Future)

        # Block on the future
        result = future.result(timeout=5)
        t.join()
        assert result is True


# ── Executor Loop ───────────────────────────────────────────────────


@dataclass
class _FakeToolCallRecord:
    """Minimal stand-in for agent_loop.ToolCallRecord used in tests."""

    step: int = 0
    tool: str = ""
    status: str = "ok"
    result: dict = field(default_factory=dict)
    iteration: int = 1


@dataclass
class _FakeLoopResult:
    """Minimal stand-in for agent_loop.LoopResult used in tests."""

    final_response: str = "Task completed."
    iterations: int = 1
    tool_results: list = field(default_factory=list)
    total_prompt_tokens: int = 100
    total_completion_tokens: int = 50
    total_cost_usd: float = 0.001
    done: bool = True
    error: str = ""

    @property
    def total_tokens(self) -> int:
        return self.total_prompt_tokens + self.total_completion_tokens


class TestExecutorLoop:
    def test_tick_with_no_tasks(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        _setup_executor_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        from ai_company.executor.loop import Executor

        executor = Executor(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
            agents_dir=str(tmp_path / ".opencode" / "agents"),
            results_dir=str(tmp_path / "results"),
        )
        count = executor.tick()
        assert count == 0

    def test_tick_processes_pending_task(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        _setup_executor_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        # Create a pending task
        inbox = tmp_path / ".opencode" / "inbox.json"
        task = {
            "id": "task-001",
            "sender_id": "human-ceo",
            "receiver_id": "test-agent",
            "instruction": "Read the test.py file and report its contents",
            "status": "pending",
            "priority": "medium",
        }
        inbox.write_text(json.dumps([task]), encoding="utf-8")

        # Create the file to read
        (tmp_path / "test.py").write_text("x = 42", encoding="utf-8")

        from ai_company.executor.loop import Executor

        executor = Executor(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
            agents_dir=str(tmp_path / ".opencode" / "agents"),
            results_dir=str(tmp_path / "results"),
        )

        # Mock agent_loop.run to return a successful result
        mock_result = _FakeLoopResult(
            final_response="File contains x = 42",
            iterations=1,
            tool_results=[],
            done=True,
            error="",
        )
        executor.agent_loop.run = MagicMock(return_value=mock_result)

        count = executor.tick()
        assert count == 1

        # Verify agent_loop.run was called
        executor.agent_loop.run.assert_called_once()

        # Verify task was completed
        updated = json.loads(inbox.read_text(encoding="utf-8"))
        assert updated[0]["status"] == "completed"
        assert "42" in updated[0]["result"]

        # Verify results were saved
        log_path = tmp_path / "results" / "task-001" / "loop_result.json"
        assert log_path.exists()
        log = json.loads(log_path.read_text(encoding="utf-8"))
        assert log["task_id"] == "task-001"
        assert log["agent"] == "test-agent"

    def test_tick_handles_loop_failure(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        _setup_executor_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        inbox = tmp_path / ".opencode" / "inbox.json"
        task = {
            "id": "task-002",
            "sender_id": "human-ceo",
            "receiver_id": "test-agent",
            "instruction": "Do something",
            "status": "pending",
            "priority": "medium",
        }
        inbox.write_text(json.dumps([task]), encoding="utf-8")

        from ai_company.executor.loop import Executor

        executor = Executor(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
            agents_dir=str(tmp_path / ".opencode" / "agents"),
            results_dir=str(tmp_path / "results"),
        )

        # Mock agent_loop.run to raise an exception
        executor.agent_loop.run = MagicMock(side_effect=RuntimeError("LLM API down"))

        count = executor.tick()
        assert count == 1

        updated = json.loads(inbox.read_text(encoding="utf-8"))
        assert updated[0]["status"] == "failed"
        assert "LLM API down" in updated[0]["result"]

    def test_process_task_uses_agent_loop(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verify _process_task delegates to AgentLoop.run()."""
        monkeypatch.chdir(tmp_path)
        _setup_executor_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        inbox = tmp_path / ".opencode" / "inbox.json"
        task = {
            "id": "task-loop-001",
            "sender_id": "human-ceo",
            "receiver_id": "test-agent",
            "instruction": "Analyze codebase",
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

        mock_result = _FakeLoopResult(
            final_response="Analysis complete.",
            iterations=3,
            done=True,
        )
        executor.agent_loop.run = MagicMock(return_value=mock_result)

        executor.tick()

        # Verify agent_loop.run was called with correct args
        call_kwargs = executor.agent_loop.run.call_args
        assert call_kwargs.kwargs["agent_name"] == "test-agent"
        assert call_kwargs.kwargs["task_id"] == "task-loop-001"
        assert call_kwargs.kwargs["priority"] == "high"
        assert "Analyze codebase" in call_kwargs.kwargs["user_prompt"]

    def test_process_task_handles_loop_failure(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verify error handling when AgentLoop.run() raises."""
        monkeypatch.chdir(tmp_path)
        _setup_executor_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        inbox = tmp_path / ".opencode" / "inbox.json"
        task = {
            "id": "task-fail-001",
            "sender_id": "human-ceo",
            "receiver_id": "test-agent",
            "instruction": "Failing task",
            "status": "pending",
            "priority": "medium",
        }
        inbox.write_text(json.dumps([task]), encoding="utf-8")

        from ai_company.executor.loop import Executor

        executor = Executor(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
            agents_dir=str(tmp_path / ".opencode" / "agents"),
            results_dir=str(tmp_path / "results"),
        )

        executor.agent_loop.run = MagicMock(side_effect=ConnectionError("Network unreachable"))

        executor.tick()

        assert executor.stats.tasks_failed == 1
        assert executor.stats.tasks_succeeded == 0

        updated = json.loads(inbox.read_text(encoding="utf-8"))
        assert updated[0]["status"] == "failed"
        assert "Network unreachable" in updated[0]["result"]

    def test_process_task_creates_subtasks_from_records(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verify delegation from ToolCallRecord creates subtasks."""
        monkeypatch.chdir(tmp_path)
        _setup_executor_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")
        _create_agent_spec(tmp_path, "lead-backend")

        inbox = tmp_path / ".opencode" / "inbox.json"
        task = {
            "id": "task-deleg-001",
            "sender_id": "human-ceo",
            "receiver_id": "test-agent",
            "instruction": "Build API and frontend",
            "status": "pending",
            "priority": "medium",
        }
        inbox.write_text(json.dumps([task]), encoding="utf-8")

        from ai_company.executor.loop import Executor

        executor = Executor(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
            agents_dir=str(tmp_path / ".opencode" / "agents"),
            results_dir=str(tmp_path / "results"),
        )

        # Create a mock result with a delegate tool record
        delegate_record = _FakeToolCallRecord(
            step=1,
            tool="delegate",
            status="ok",
            result={"receiver": "lead-backend", "instruction": "Build REST API"},
            iteration=1,
        )
        mock_result = _FakeLoopResult(
            final_response="Delegated to lead-backend.",
            iterations=1,
            tool_results=[delegate_record],
            done=True,
        )
        executor.agent_loop.run = MagicMock(return_value=mock_result)

        executor.tick()

        # Verify a subtask was created in the inbox
        updated = json.loads(inbox.read_text(encoding="utf-8"))
        # Original task + 1 subtask
        assert len(updated) == 2

        subtask = [t for t in updated if t["id"] != "task-deleg-001"][0]
        assert subtask["sender_id"] == "test-agent"
        assert subtask["receiver_id"] == "lead-backend"
        assert subtask["instruction"] == "Build REST API"
        assert subtask["status"] == "pending"

    def test_stats_tracking(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        _setup_executor_files(tmp_path)

        from ai_company.executor.loop import Executor

        executor = Executor(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        assert executor.stats.tasks_processed == 0
        assert executor.stats.uptime_seconds == 0

        d = executor.stats.to_dict()
        assert d["tasks_processed"] == 0
        assert d["running"] is False


# ── Helpers ─────────────────────────────────────────────────────────


_AGENT_SPEC_SAMPLE = """\
---
name: chief-of-staff
description: The primary orchestrator and strategic alignment agent.
tools: ["read", "write", "execute", "delegate"]
mode: subagent
permission:
  read: allow
  write: allow
  bash: allow
  task: allow
---

# Chief of Staff

## Identity

Type: Executive

Department: Office of the CEO

Reports To: human-ceo

---

## Mission

The primary orchestrator and strategic alignment agent for the entire company.

---

## Responsibilities

- Align company goals across all departments
- Orchestrate agent communication and task delegation
- Resolve cross-department conflicts
- Ensure strategic initiatives reach completion

---

## Operating Guidelines

Maintain high-level strategic oversight. Never execute low-level tasks directly. Delegate everything.

---

## Operating Principles

- Evidence over opinion
- Customer first
- Automate repetitive work
- Escalate uncertainty
"""

_SPECIALIST_SPEC_SAMPLE = """\
---
name: lead-backend
description: Manages backend systems, APIs, and server-side agent logic.
tools: ["read", "write", "execute", "code_interpreter"]
mode: subagent
permission:
  read: allow
  write: allow
  bash: allow
---

# Lead Backend Engineer

## Identity

Type: Specialist

Department: Technology

Reports To: cto

---

## Mission

Manages backend systems, APIs, and server-side agent logic.

---

## Responsibilities

- Develop and maintain REST APIs
- Lead backend code reviews
- Manage database schemas
- Optimize backend performance

---

## Operating Guidelines

Write modular, well-documented code. API-first design.
"""


def _setup_model_files(tmp_path: Path) -> None:
    (tmp_path / "company").mkdir(exist_ok=True)
    models = {
        "providers": {
            "opencode": {"backend": "openai_compatible", "default_model": "big-pickle", "api_base": "https://opencode.ai/api/v1"},
            "deepseek": {"backend": "openai_compatible", "default_model": "deepseek-chat", "api_base": "https://api.deepseek.com/v1"},
            "ollama": {"backend": "ollama", "default_model": "llama3.1:8b", "api_base": "http://localhost:11434"},
        },
        "tiers": {
            "fast": {"description": "Fast", "providers": [{"provider": "opencode", "model": "big-pickle"}]},
            "standard": {"description": "Standard", "providers": [{"provider": "deepseek", "model": "deepseek-chat"}]},
            "premium": {"description": "Premium", "providers": [{"provider": "deepseek", "model": "deepseek-coder"}]},
        },
        "routing": [
            {"agent_type": "Board", "tier": "fast"},
            {"agent_type": "Executive", "tier": "standard"},
            {"agent_type": "Specialist", "tier": "standard"},
        ],
    }
    (tmp_path / "company" / "models.yaml").write_text(json.dumps(models), encoding="utf-8")

    registry = [
        {"name": "test-agent", "role": "Test Agent", "type": "Specialist", "department": "Test",
         "reportsTo": "ceo", "directReports": [], "description": "A test agent",
         "tools": ["read", "write"], "permission": "Execute"},
    ]
    (tmp_path / "company" / "agent-registry.json").write_text(json.dumps(registry), encoding="utf-8")


def _setup_executor_files(tmp_path: Path) -> None:
    _setup_model_files(tmp_path)
    (tmp_path / ".opencode").mkdir(exist_ok=True)
    (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
    (tmp_path / "orchestrator").mkdir(exist_ok=True)
    (tmp_path / "orchestrator" / "approvals.yaml").write_text("requests: []", encoding="utf-8")


def _create_agent_spec(tmp_path: Path, agent_name: str) -> None:
    agents_dir = tmp_path / ".opencode" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    spec = f"""\
---
name: {agent_name}
description: A test agent
tools: ["read", "write", "execute"]
mode: subagent
permission:
  read: allow
  write: allow
---

# Test Agent

## Identity

Type: Specialist

Department: Test

Reports To: ceo

---

## Mission

Execute test tasks.

---

## Responsibilities

- Read files
- Write files
- Execute commands

---

## Operating Guidelines

Be thorough.
"""
    (agents_dir / f"{agent_name}.md").write_text(spec, encoding="utf-8")
