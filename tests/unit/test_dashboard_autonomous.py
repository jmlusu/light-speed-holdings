"""Tests for the ``ai-company dashboard autonomous`` CLI shortcut (US-A09)."""

from __future__ import annotations

import contextlib
import re
from typing import Any

import pytest
import uvicorn
from typer.testing import CliRunner

import ai_company.cli.executor as executor_cli
from ai_company.cli import dashboard as dashboard_cli
from ai_company.cli.dashboard import app
from ai_company.executor.daemon import ExecutorDaemon

runner = CliRunner()

_ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences.

    Rich forces color output when running under CI (``GITHUB_ACTIONS``),
    splitting option text like ``--no-executor`` across styled spans, so
    assertions must match against the plain-text rendering.
    """
    return _ANSI_ESCAPE.sub("", text)


def _combined(result: Any) -> str:
    """Return stdout plus stderr, across click runner versions.

    Args:
        result: CliRunner result whose messages should be surfaced.

    Returns:
        Concatenated output text for assertion messages.
    """
    text = result.output
    with contextlib.suppress(ValueError):
        text += result.stderr or ""
    return text


class TestAutonomousHelp:
    """``dashboard autonomous --help`` renders its options."""

    def test_autonomous_help_renders(self) -> None:
        result = runner.invoke(app, ["autonomous", "--help"])
        assert result.exit_code == 0, _combined(result)
        output = _strip_ansi(result.output)
        assert "--no-executor" in output
        assert "--port" in output
        assert "--host" in output
        assert "--no-open" in output

    def test_dashboard_help_lists_autonomous(self) -> None:
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0, _combined(result)
        assert "autonomous" in _strip_ansi(result.output)


class TestAutonomousLaunchGuards:
    """Guards fire before any daemon start or server launch."""

    @pytest.mark.parametrize("port", [1440, 1441])
    def test_refuses_vite_port(self, monkeypatch: pytest.MonkeyPatch, port: int) -> None:
        daemon_calls: list[str] = []
        monkeypatch.setattr(
            dashboard_cli,
            "_ensure_executor_daemon",
            lambda: daemon_calls.append("daemon"),
        )
        monkeypatch.setattr(uvicorn, "run", lambda *a, **k: pytest.fail("uvicorn must not run"))
        result = runner.invoke(app, ["autonomous", "--port", str(port), "--no-open"])
        assert result.exit_code == 1, _combined(result)
        assert "Marketing Site" in _combined(result)
        assert daemon_calls == []

    def test_refuses_non_loopback_with_open_auth(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "open")
        daemon_calls: list[str] = []
        monkeypatch.setattr(
            dashboard_cli,
            "_ensure_executor_daemon",
            lambda: daemon_calls.append("daemon"),
        )
        monkeypatch.setattr(uvicorn, "run", lambda *a, **k: pytest.fail("uvicorn must not run"))
        result = runner.invoke(app, ["autonomous", "--host", "0.0.0.0", "--no-open"])
        assert result.exit_code == 1, _combined(result)
        assert "loopback" in _combined(result)
        assert daemon_calls == []


class TestAutonomousFlow:
    """Command flow: validate -> ensure daemon -> serve."""

    def test_starts_daemon_before_serving(self, monkeypatch: pytest.MonkeyPatch) -> None:
        order: list[str] = []
        monkeypatch.setattr(
            dashboard_cli,
            "_ensure_executor_daemon",
            lambda: order.append("daemon"),
        )

        def fake_run(*args: Any, **kwargs: Any) -> None:
            order.append("serve")

        monkeypatch.setattr(uvicorn, "run", fake_run)
        result = runner.invoke(app, ["autonomous", "--no-open"])
        assert result.exit_code == 0, f"{_combined(result)} {result.exception!r}"
        assert order == ["daemon", "serve"]

    def test_no_executor_flag_skips_daemon(self, monkeypatch: pytest.MonkeyPatch) -> None:
        order: list[str] = []
        monkeypatch.setattr(
            dashboard_cli,
            "_ensure_executor_daemon",
            lambda: order.append("daemon"),
        )

        def fake_run(*args: Any, **kwargs: Any) -> None:
            order.append("serve")

        monkeypatch.setattr(uvicorn, "run", fake_run)
        result = runner.invoke(app, ["autonomous", "--no-open", "--no-executor"])
        assert result.exit_code == 0, f"{_combined(result)} {result.exception!r}"
        assert order == ["serve"]

    def test_default_port_and_host_passed_to_uvicorn(self, monkeypatch: pytest.MonkeyPatch) -> None:
        captured: dict[str, Any] = {}
        monkeypatch.setattr(dashboard_cli, "_ensure_executor_daemon", lambda: None)

        def fake_run(target: str, **kwargs: Any) -> None:
            captured["target"] = target
            captured.update(kwargs)

        monkeypatch.setattr(uvicorn, "run", fake_run)
        result = runner.invoke(app, ["autonomous", "--no-open"])
        assert result.exit_code == 0, f"{_combined(result)} {result.exception!r}"
        assert captured["target"] == "ai_company.dashboard.app:app"
        assert captured["port"] == 8420
        assert captured["host"] == "127.0.0.1"
        assert captured["log_level"] == "info"


class TestEnsureExecutorDaemon:
    """``_ensure_executor_daemon`` reuses the ``executor start`` daemon path."""

    def test_skips_when_already_running(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        monkeypatch.setattr(ExecutorDaemon, "is_daemon_running", lambda pid_path=None: True)
        resolve_calls: list[tuple[Any, ...]] = []
        start_calls: list[dict[str, Any]] = []
        monkeypatch.setattr(
            executor_cli,
            "_resolve_budgets",
            lambda *a: resolve_calls.append(a) or (1.0, 1.0, False),
        )
        monkeypatch.setattr(executor_cli, "_start_daemon", lambda **k: start_calls.append(k))

        dashboard_cli._ensure_executor_daemon()

        assert resolve_calls == []
        assert start_calls == []
        assert "already running" in capsys.readouterr().out

    def test_starts_daemon_with_executor_defaults(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(ExecutorDaemon, "is_daemon_running", lambda pid_path=None: False)
        resolved: dict[str, Any] = {}

        def fake_resolve(
            daily: Any, task: Any, suspend: Any, guardrails: Any
        ) -> tuple[float, float, bool]:
            resolved["args"] = (daily, task, suspend, guardrails)
            return 1.5, 0.25, True

        started: dict[str, Any] = {}
        monkeypatch.setattr(executor_cli, "_resolve_budgets", fake_resolve)
        monkeypatch.setattr(executor_cli, "_start_daemon", lambda **k: started.update(k))

        dashboard_cli._ensure_executor_daemon()

        assert resolved["args"] == (
            None,
            None,
            False,
            "config/company/guardrails.yaml",
        )
        assert started["poll_interval"] == 5.0
        assert started["config"] == "company/models.yaml"
        assert started["registry"] == "company/agent-registry.json"
        assert started["pid_dir"] == "logs"
        assert started["log_dir"] == "logs"
        assert started["kpi_snapshot_interval"] == 3600.0
        assert started["governance_interval"] == 86400.0
        assert started["routine_interval"] == 900.0
        assert started["db_path"] is None
        assert started["daily_budget_usd"] == 1.5
        assert started["task_budget_usd"] == 0.25
        assert started["auto_suspend"] is True
