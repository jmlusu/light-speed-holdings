"""Sprint 4 T015 — CLI command behaviour tests (side-effect free).

IMPORTANT: this project's Typer version runs ``CliRunner`` commands in the
real working directory (no automatic filesystem isolation), so every test
either passes explicit ``tmp_path`` paths, redirects the cwd with
``monkeypatch.chdir``, or mocks the side-effecting internal so no real
repository state is ever written.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from ai_company.cli.main import app

runner = CliRunner()

VALID_AGENT_SPEC = """\
---
description: QA Engineer agent
permission:
  read: allow
  edit: allow
  bash: allow
  grep: allow
  list: allow
---

## Mission
Ensures software quality through testing strategies, automation, and quality gates.

## Responsibilities
- Design and implement test strategies.
- Build and maintain automated test suites.

## Operating Guidelines
Quality is everyone's job, but QA owns the process.

## Success Metrics
- Technical quality of deliverables

## Operating Principles
- Evidence over opinion
"""

INVALID_AGENT_SPEC = """\
---
description: Broken agent
---

## Responsibilities
- Do stuff
"""


def _write_agents_dir(tmp_path: Path, files: dict[str, str]) -> Path:
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir(exist_ok=True)
    for name, content in files.items():
        (agents_dir / name).write_text(content, encoding="utf-8")
    return agents_dir


# ── Root / generic commands ────────────────────────────────────────────


def test_status_prints_company_info() -> None:
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "Light Speed Holdings" in result.stdout


def test_unknown_command_exits_2() -> None:
    result = runner.invoke(app, ["not-a-command"])
    assert result.exit_code == 2


def test_sop_without_id_exits_0() -> None:
    """``sop`` with no args exits cleanly regardless of docs/ availability."""
    result = runner.invoke(app, ["sop"])
    assert result.exit_code == 0


def test_sop_unknown_id_exits_1() -> None:
    result = runner.invoke(app, ["sop", "SOP-NOT-REAL-000"])
    assert result.exit_code == 1
    assert "not found" in result.stdout.lower()


def test_raci_unknown_id_exits_1() -> None:
    result = runner.invoke(app, ["raci", "RACI-NOT-REAL-000"])
    assert result.exit_code == 1
    assert "not found" in result.stdout.lower()


# ── sync-registry / generate ───────────────────────────────────────────


def test_sync_registry_missing_yaml_exits_1(tmp_path: Path) -> None:
    result = runner.invoke(app, ["sync-registry", "--yaml-path", str(tmp_path / "nope.yaml")])
    assert result.exit_code == 1


def test_sync_registry_success_mocked(tmp_path: Path) -> None:
    registry = tmp_path / "company-registry.yaml"
    registry.write_text("company:\n  agents: []\n", encoding="utf-8")
    with patch("ai_company.registry.sync.sync_registry", return_value=2):
        result = runner.invoke(
            app,
            [
                "sync-registry",
                "--yaml-path",
                str(registry),
                "--json-path",
                str(tmp_path / "out.json"),
            ],
        )
    assert result.exit_code == 0
    assert "Synced 2 agents" in result.stdout


def test_generate_success_mocked(tmp_path: Path) -> None:
    registry = tmp_path / "company-registry.yaml"
    registry.write_text("company:\n  agents: []\n", encoding="utf-8")
    gen = MagicMock()
    gen.generate_all.return_value = ["qa_engineer.md"]
    with (
        patch("ai_company.registry.sync.sync_registry", return_value=0),
        patch("ai_company.generator.AgentGenerator", return_value=gen),
    ):
        result = runner.invoke(app, ["generate", "--registry", str(registry)])
    assert result.exit_code == 0
    assert "Done: 1 agent files generated." in result.stdout


# ── executor ───────────────────────────────────────────────────────────


def test_executor_status_exits_0() -> None:
    """Status is read-only; exit 0 regardless of daemon/inbox state."""
    result = runner.invoke(app, ["executor", "status"])
    assert result.exit_code == 0


def test_executor_stop_without_daemon_exits_1(tmp_path: Path) -> None:
    # Default paths would target the repo's real logs/ dir; use tmp_path so
    # no live daemon is ever touched (CliRunner runs with no isolation).
    result = runner.invoke(
        app,
        ["executor", "stop", "--pid-dir", str(tmp_path), "--log-dir", str(tmp_path)],
    )
    assert result.exit_code == 1
    assert "No running daemon" in result.stdout


def test_executor_tick_mocked() -> None:
    executor = MagicMock()
    executor.tick.return_value = 2
    executor.stats.to_dict.return_value = {"executed": 2}
    with patch("ai_company.executor.loop.Executor", return_value=executor):
        result = runner.invoke(app, ["executor", "tick"])
    assert result.exit_code == 0
    assert "Processed 2 task(s)." in result.stdout


def test_executor_dlq_clear_mocked() -> None:
    dlq = MagicMock()
    dlq.clear.return_value = 3
    with patch("ai_company.executor.dead_letter.DeadLetterQueue", return_value=dlq):
        result = runner.invoke(app, ["executor", "dlq-clear"])
    assert result.exit_code == 0
    assert "Cleared 3 entry(ies)" in result.stdout


# ── orchestrator ───────────────────────────────────────────────────────


def test_orchestrator_tick_empty_mocked() -> None:
    """Tick must never write real orchestrator state, so internals are mocked."""
    scheduler = MagicMock()
    scheduler.get_pending_tasks.return_value = []
    escalation = MagicMock()
    escalation.get_pending_escalations.return_value = []
    gate = MagicMock()
    gate.get_pending_requests.return_value = []
    with (
        patch("ai_company.orchestrator.scheduler.Scheduler", return_value=scheduler),
        patch("ai_company.orchestrator.escalation.EscalationManager", return_value=escalation),
        patch("ai_company.orchestrator.approval.ApprovalGate", return_value=gate),
    ):
        result = runner.invoke(app, ["orchestrator", "tick"])
    assert result.exit_code == 0
    assert "Total items needing attention: 0" in result.stdout


# ── doctor ─────────────────────────────────────────────────────────────


def test_doctor_run_prints_health_table() -> None:
    with patch("ai_company.cli.doctor.run_all_checks", return_value=[]):
        result = runner.invoke(app, ["doctor", "run"])
    assert result.exit_code == 0
    assert "System Health" in result.stdout


# ── security ───────────────────────────────────────────────────────────


def test_security_key_status(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Real key manager, but isolated in tmp cwd so no repo files are written."""
    monkeypatch.setenv("MEMORY_ENCRYPTION_KEY", "test-secret-key")
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["security", "key-status"])
    assert result.exit_code == 0
    assert "Current key ID:" in result.stdout
    assert (tmp_path / "security" / "memory_keys.json").exists()


# ── validate ───────────────────────────────────────────────────────────


def test_validate_naming_success_mocked() -> None:
    gen = MagicMock()
    gen.load_registry.return_value = []
    with patch("ai_company.generator.AgentGenerator", return_value=gen):
        result = runner.invoke(app, ["validate", "naming"])
    assert result.exit_code == 0
    assert "All naming conventions are correct." in result.stdout


def test_validate_references_missing_config_dir_exits_1(tmp_path: Path) -> None:
    result = runner.invoke(app, ["validate", "references", "--config-dir", str(tmp_path / "nope")])
    assert result.exit_code == 1


def test_validate_config_empty_project_exits_1(tmp_path: Path) -> None:
    result = runner.invoke(app, ["validate", "config", "--project-root", str(tmp_path)])
    assert result.exit_code == 1
    assert "Summary:" in result.stdout


# ── agents validate ────────────────────────────────────────────────────


def test_agents_validate_default_validates_all(tmp_path: Path) -> None:
    agents_dir = _write_agents_dir(tmp_path, {"qa_engineer.md": VALID_AGENT_SPEC})
    result = runner.invoke(app, ["agents", "validate", "--agents-dir", str(agents_dir)])
    assert result.exit_code == 0
    assert "Validated: 1" in result.stdout


def test_agents_validate_missing_dir_exits_1(tmp_path: Path) -> None:
    result = runner.invoke(app, ["agents", "validate", "--agents-dir", str(tmp_path / "nope")])
    assert result.exit_code == 1
    assert "Agents directory not found" in result.stdout


def test_agents_validate_missing_agent_exits_1(tmp_path: Path) -> None:
    agents_dir = _write_agents_dir(tmp_path, {})
    result = runner.invoke(
        app, ["agents", "validate", "--agent", "ghost-agent", "--agents-dir", str(agents_dir)]
    )
    assert result.exit_code == 1
    assert "not found" in result.stdout


def test_agents_validate_valid_spec_exits_0(tmp_path: Path) -> None:
    agents_dir = _write_agents_dir(tmp_path, {"qa_engineer.md": VALID_AGENT_SPEC})
    result = runner.invoke(
        app, ["agents", "validate", "--agent", "qa_engineer", "--agents-dir", str(agents_dir)]
    )
    assert result.exit_code == 0
    assert "OK" in result.stdout


def test_agents_validate_invalid_spec_exits_1(tmp_path: Path) -> None:
    agents_dir = _write_agents_dir(tmp_path, {"broken_agent.md": INVALID_AGENT_SPEC})
    result = runner.invoke(
        app, ["agents", "validate", "--agent", "broken_agent", "--agents-dir", str(agents_dir)]
    )
    assert result.exit_code == 1
    assert "FAILED" in result.stdout
    assert "Missing required field: mission" in result.stdout


def test_agents_validate_all_reports_summary(tmp_path: Path) -> None:
    agents_dir = _write_agents_dir(
        tmp_path,
        {"qa_engineer.md": VALID_AGENT_SPEC, "broken_agent.md": INVALID_AGENT_SPEC},
    )
    result = runner.invoke(app, ["agents", "validate", "--agents-dir", str(agents_dir)])
    assert result.exit_code == 1  # one valid + one broken -> overall failure
    assert "Validated: 2 | Valid: 1 | Invalid: 1" in result.stdout
