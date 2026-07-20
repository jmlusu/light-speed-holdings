"""Shared fixtures for integration tests.

These fixtures isolate every integration test from the real project state:

- ``tmp_path``-based workspace (chdir) so no writes hit the real ``.opencode``,
  ``company/``, or ``orchestrator/`` directories.
- A mocked LLM client so no network call is ever made.
- Reset of module-level global state (audit writer, memory store, dashboard
  bus) between tests so suites do not leak into one another.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_company.orchestrator.message_bus import MessageBus


# ---------------------------------------------------------------------------
# Workspace isolation
# ---------------------------------------------------------------------------


def _write_agent_registry(tmp_path: Path) -> None:
    """Write a minimal agent-registry.json consumed by the dashboard API."""
    registry = [
        {
            "name": "chief-of-staff",
            "role": "Chief of Staff",
            "type": "Executive",
            "department": "Executive",
            "reportsTo": "human-ceo",
            "directReports": ["test-agent"],
            "description": "Coordinates all departments",
            "tools": ["read", "write", "delegate"],
            "permission": "Execute",
        },
        {
            "name": "test-agent",
            "role": "Test Agent",
            "type": "Specialist",
            "department": "Test",
            "reportsTo": "chief-of-staff",
            "directReports": [],
            "description": "A test agent",
            "tools": ["read", "write", "execute"],
            "permission": "Execute",
        },
        {
            "name": "lead-backend",
            "role": "Lead Backend",
            "type": "Specialist",
            "department": "Technology",
            "reportsTo": "cto",
            "directReports": [],
            "description": "Backend lead",
            "tools": ["read", "write"],
            "permission": "Execute",
        },
    ]
    (tmp_path / "company").mkdir(parents=True, exist_ok=True)
    (tmp_path / "company" / "agent-registry.json").write_text(
        json.dumps(registry), encoding="utf-8"
    )


def _write_models_yaml(tmp_path: Path) -> None:
    """Write a minimal models.yaml so ModelRouter can initialise offline."""
    import yaml

    (tmp_path / "company").mkdir(parents=True, exist_ok=True)
    models = {
        "providers": {
            "opencode": {
                "backend": "openai_compatible",
                "default_model": "big-pickle",
                "api_base": "https://opencode.ai/api/v1",
            },
        },
        "tiers": {
            "fast": {"description": "Fast", "providers": [{"provider": "opencode", "model": "big-pickle"}]},
            "standard": {"description": "Standard", "providers": [{"provider": "opencode", "model": "big-pickle"}]},
            "premium": {"description": "Premium", "providers": [{"provider": "opencode", "model": "big-pickle"}]},
        },
        "routing": [
            {"agent_type": "Board", "tier": "fast"},
            {"agent_type": "Executive", "tier": "standard"},
            {"agent_type": "Specialist", "tier": "standard"},
        ],
    }
    (tmp_path / "company" / "models.yaml").write_text(yaml.dump(models), encoding="utf-8")


def _write_agent_spec(tmp_path: Path, agent_name: str) -> None:
    """Write a minimal agent spec card under `.opencode/agents`."""
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


@pytest.fixture()
def workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Isolated workspace: chdir + seeded config/agent files.

    Returns the tmp_path so tests can address files by relative path.
    """
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".opencode").mkdir(exist_ok=True)
    (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
    (tmp_path / "orchestrator").mkdir(exist_ok=True)
    (tmp_path / "orchestrator" / "approvals.yaml").write_text("requests: []", encoding="utf-8")
    (tmp_path / "orchestrator" / "escalation.yaml").write_text("{'rules': [], 'events': []}", encoding="utf-8")
    (tmp_path / "orchestrator" / "scheduler.yaml").write_text("tasks: []", encoding="utf-8")
    _write_models_yaml(tmp_path)
    _write_agent_registry(tmp_path)
    _write_agent_spec(tmp_path, "test-agent")
    _write_agent_spec(tmp_path, "lead-backend")
    return tmp_path


# ---------------------------------------------------------------------------
# Mocked LLM client
# ---------------------------------------------------------------------------


class FakeLoopResult:
    """Minimal stand-in for ``agent_loop.LoopResult``."""

    def __init__(
        self,
        final_response: str = "Task completed.",
        iterations: int = 1,
        tool_results: list | None = None,
        total_prompt_tokens: int = 100,
        total_completion_tokens: int = 50,
        total_cost_usd: float = 0.001,
        done: bool = True,
        error: str = "",
    ) -> None:
        self.final_response = final_response
        self.iterations = iterations
        self.tool_results = tool_results or []
        self.total_prompt_tokens = total_prompt_tokens
        self.total_completion_tokens = total_completion_tokens
        self.total_cost_usd = total_cost_usd
        self.done = done
        self.error = error

    @property
    def total_tokens(self) -> int:
        return self.total_prompt_tokens + self.total_completion_tokens


@pytest.fixture()
def mock_llm(workspace: Path, monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Patch ``LLMClient`` so no real network call occurs.

    The executor constructs its own ``LLMClient``; we patch the class in the
    executor module so the constructed instance is a MagicMock. We then drive
    the agent loop through ``agent_loop.run`` which is what actually calls the
    LLM layer.
    """
    fake = MagicMock()
    fake.execute_task.return_value = {"plan": [], "result": "ok", "artifacts": []}
    fake.execute_task_stream.return_value = iter([])
    # The Executor builds an AgentLoop with self.llm; patch the class used.
    monkeypatch.setattr(
        "ai_company.executor.loop.LLMClient", lambda *a, **k: fake
    )
    return fake


@pytest.fixture()
def executor(workspace: Path, mock_llm: MagicMock):
    """Construct an Executor wired to the isolated workspace + mocked LLM."""
    from ai_company.audit.integration import init_audit
    from ai_company.executor.loop import Executor
    from ai_company.memory.integration import init_memory

    ex = Executor(
        config_path=str(workspace / "company" / "models.yaml"),
        registry_path=str(workspace / "company" / "agent-registry.json"),
        agents_dir=str(workspace / ".opencode" / "agents"),
        results_dir=str(workspace / "results"),
    )
    # Re-init audit + memory to the isolated workspace dirs.
    # init_audit() is idempotent, so reset the global writer first.
    import ai_company.audit.integration as audit_mod
    import ai_company.memory.integration as mem_mod

    audit_mod._writer = None
    mem_mod._store = None
    mem_mod._vector_store = None
    init_audit(audit_dir=str(workspace / ".opencode" / "audit"))
    init_memory(base_dir=str(workspace / "memory"))
    return ex


@pytest.fixture()
def bus(workspace: Path) -> MessageBus:
    """A MessageBus pointed at the isolated inbox.json."""
    return MessageBus(storage_path=str(workspace / ".opencode" / "inbox.json"))


@pytest.fixture(autouse=True)
def _reset_global_state():
    """Reset module-level globals so integration suites don't leak."""
    yield
    import ai_company.audit.integration as audit_mod
    import ai_company.dashboard.api as dash_api
    import ai_company.memory.integration as mem_mod

    audit_mod._writer = None
    mem_mod._store = None
    mem_mod._vector_store = None
    dash_api._bus = None
