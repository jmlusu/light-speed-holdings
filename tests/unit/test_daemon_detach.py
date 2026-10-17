"""Detached daemon subprocess tests (GitHub #56).

Covers the CLI/daemon wiring that makes ``ai-company executor start --daemon``
spawn a *real* detached OS process that survives its parent shell: command
construction, ``subprocess.Popen`` detach flags, PID/status file handoff,
module entry point wiring, and stop/status semantics. All tests use fake
processes or a fast non-LLM child command — no executor work is spawned and
nothing is spent.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest
from typer.testing import CliRunner

from ai_company.cli.main import app
from ai_company.executor import daemon as daemon_mod
from ai_company.executor.daemon import (
    DaemonHealthStatus,
    ExecutorDaemon,
    build_daemon_command,
    launch_detached_daemon,
)
from ai_company.executor.daemon import (
    main as daemon_main,
)

runner = CliRunner()

POLL = 0.1


def _start_args(tmp_path: Path) -> list[str]:
    return [
        "executor",
        "start",
        "--daemon",
        "--pid-dir",
        str(tmp_path),
        "--log-dir",
        str(tmp_path),
        "--kpi-snapshot-interval",
        "0",
        "--governance-interval",
        "0",
    ]


# ── Command construction ───────────────────────────────────────────────


class TestBuildDaemonCommand:
    def test_build_daemon_command_defaults(self) -> None:
        cmd = build_daemon_command(
            poll_interval=5.0,
            config="company/models.yaml",
            registry="company/agent-registry.json",
            pid_dir="logs",
            log_dir="logs",
            kpi_snapshot_interval=300.0,
            governance_interval=86400.0,
            db_path=None,
            daily_budget_usd=None,
            task_budget_usd=None,
            auto_suspend=False,
        )
        # Fresh interpreter via the daemon module entry point.
        assert cmd[0] == sys.executable
        assert cmd[1] == "-m"
        assert cmd[2] == "ai_company.executor.daemon"
        # Core options are always forwarded.
        assert "--poll-interval" in cmd
        assert "5.0" in cmd
        assert "--config" in cmd
        assert "--pid-dir" in cmd
        assert "--log-dir" in cmd
        assert "--kpi-snapshot-interval" in cmd
        assert "--governance-interval" in cmd
        # Optional flags are omitted when unset.
        assert "--db-path" not in cmd
        assert "--daily-budget-usd" not in cmd
        assert "--auto-suspend" not in cmd

    def test_build_daemon_command_includes_optional_flags(self) -> None:
        cmd = build_daemon_command(
            poll_interval=2.0,
            config="c.yaml",
            registry="r.json",
            pid_dir="logs",
            log_dir="logs",
            kpi_snapshot_interval=0.0,
            governance_interval=0.0,
            db_path="data/x.db",
            daily_budget_usd=12.5,
            task_budget_usd=3.25,
            auto_suspend=True,
        )
        assert cmd[cmd.index("--db-path") + 1] == "data/x.db"
        assert cmd[cmd.index("--daily-budget-usd") + 1] == "12.5"
        assert cmd[cmd.index("--task-budget-usd") + 1] == "3.25"
        assert cmd[-1] == "--auto-suspend"


# ── Detached launch wiring ─────────────────────────────────────────────


class _FakeProc:
    """Minimal stand-in for ``subprocess.Popen``."""

    def __init__(self, exit_code: int | None = None) -> None:
        self.exit_code = exit_code

    def poll(self) -> int | None:
        return self.exit_code


def _install_fake_popen(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    *,
    exit_code: int | None = None,
    write_state: bool = True,
    write_on_poll: bool = False,
) -> list[tuple[list[str], dict[str, Any]]]:
    """Patch ``subprocess.Popen`` with a fake that simulates the child.

    By default the fake writes PID/status files immediately (as the daemon
    child does during startup); with ``write_on_poll`` it writes the PID on
    the first ``poll()`` call to exercise the parent's wait loop.
    """
    calls: list[tuple[list[str], dict[str, Any]]] = []

    def _fake_popen(cmd: list[str], **kwargs: Any) -> _FakeProc:
        calls.append((cmd, kwargs))
        proc = _FakeProc(exit_code=exit_code)
        if write_on_poll:
            original_poll = proc.poll

            def _poll_and_write() -> int | None:
                (tmp_path / "executor-daemon.pid").write_text("7777", encoding="utf-8")
                return original_poll()

            proc.poll = _poll_and_write  # type: ignore[method-assign]
        elif write_state:
            (tmp_path / "executor-daemon.pid").write_text("4242", encoding="utf-8")
            DaemonHealthStatus(tmp_path / "executor-daemon.json").write(
                pid=4242, state="running", started_at="2026-01-01T00:00:00+00:00"
            )
        return proc

    monkeypatch.setattr(daemon_mod.subprocess, "Popen", _fake_popen)
    return calls


def _launch_kwargs(tmp_path: Path, *, wait_timeout: float = 2.0) -> dict[str, Any]:
    return {
        "poll_interval": POLL,
        "config": "company/models.yaml",
        "registry": "company/agent-registry.json",
        "pid_dir": str(tmp_path),
        "log_dir": str(tmp_path),
        "kpi_snapshot_interval": 0.0,
        "governance_interval": 0.0,
        "db_path": None,
        "daily_budget_usd": None,
        "task_budget_usd": None,
        "auto_suspend": False,
        "wait_timeout": wait_timeout,
    }


class TestLaunchDetachedDaemon:
    def test_spawns_detached_subprocess_and_returns_pid(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        calls = _install_fake_popen(monkeypatch, tmp_path)

        pid = launch_detached_daemon(**_launch_kwargs(tmp_path))

        assert pid == 4242
        assert len(calls) == 1
        cmd, kwargs = calls[0]
        assert cmd[0] == sys.executable
        assert cmd[1] == "-m"
        assert cmd[2] == "ai_company.executor.daemon"

        # Detach mechanics: no inherited console/stdin, output to the log.
        assert kwargs["stdin"] == subprocess.DEVNULL
        assert kwargs["stdout"].name.endswith("executor-daemon.log")
        assert kwargs["stderr"] is kwargs["stdout"]
        assert kwargs["start_new_session"] is True
        if os.name == "nt":
            flags = kwargs["creationflags"]
            assert flags & getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            assert flags & getattr(subprocess, "DETACHED_PROCESS", 0)
        else:
            assert kwargs["creationflags"] == 0

        # The child's own PID/status files were recorded and are readable.
        assert (tmp_path / "executor-daemon.pid").read_text(encoding="utf-8") == "4242"
        status = DaemonHealthStatus(tmp_path / "executor-daemon.json").read()
        assert status is not None
        assert status["state"] == "running"
        assert status["pid"] == 4242

    def test_waits_for_child_pid_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _install_fake_popen(monkeypatch, tmp_path, write_state=False, write_on_poll=True)

        pid = launch_detached_daemon(**_launch_kwargs(tmp_path))

        assert pid == 7777

    def test_raises_when_child_exits_during_startup(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _install_fake_popen(monkeypatch, tmp_path, exit_code=1, write_state=False)

        with pytest.raises(RuntimeError, match="exited during startup"):
            launch_detached_daemon(**_launch_kwargs(tmp_path))

    def test_refuses_when_already_running(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        (tmp_path / "executor-daemon.pid").write_text("4242", encoding="utf-8")
        monkeypatch.setattr(daemon_mod, "_is_process_alive", lambda pid: True)

        def _boom(*args: Any, **kwargs: Any) -> None:
            raise AssertionError("Popen must not be called when a daemon is already running")

        monkeypatch.setattr(daemon_mod.subprocess, "Popen", _boom)

        with pytest.raises(RuntimeError, match="already running"):
            launch_detached_daemon(**_launch_kwargs(tmp_path))

    def test_real_detach_smoke_non_spending(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Spawn a real detached child (no LLM work) and verify lifecycle.

        The child is a tiny stdlib script that writes its PID file, then
        waits for a stop sentinel — it exercises the actual
        ``subprocess.Popen`` + detach flags path without touching the
        executor or spending anything.
        """
        stop_file = tmp_path / "executor-daemon.stop"
        script = (
            "import os, pathlib, sys, time\n"
            f"pid_file = pathlib.Path({str(tmp_path)!r}) / 'executor-daemon.pid'\n"
            f"stop_file = pathlib.Path({str(tmp_path)!r}) / 'executor-daemon.stop'\n"
            "pid_file.write_text(str(os.getpid()), encoding='utf-8')\n"
            "deadline = time.monotonic() + 60\n"
            "while time.monotonic() < deadline and not stop_file.exists():\n"
            "    time.sleep(0.05)\n"
            "sys.exit(0)\n"
        )
        monkeypatch.setattr(
            daemon_mod, "build_daemon_command", lambda **kwargs: [sys.executable, "-c", script]
        )

        # Generous timeout: the child spawn can be slow on a loaded machine.
        pid = launch_detached_daemon(**_launch_kwargs(tmp_path, wait_timeout=15.0))
        try:
            assert daemon_mod._is_process_alive(pid) is True
            assert int((tmp_path / "executor-daemon.pid").read_text(encoding="utf-8")) == pid
        finally:
            # Never leak the child: ask it to exit, force-kill as a backstop.
            stop_file.write_text("stop", encoding="utf-8")
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline and daemon_mod._is_process_alive(pid):
                time.sleep(0.05)
            if daemon_mod._is_process_alive(pid):
                import psutil

                proc = psutil.Process(pid)
                proc.kill()
                proc.wait(timeout=5.0)
        assert daemon_mod._is_process_alive(pid) is False


# ── Module entry point (the detached child) ────────────────────────────


class _FakeDaemon:
    """Records construction args and simulates the child's startup writes."""

    instances: list[dict[str, Any]] = []

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs
        _FakeDaemon.instances.append(kwargs)

    def start(self) -> None:
        pid_path = Path(self.kwargs["pid_path"])
        status_path = Path(self.kwargs["status_path"])
        pid_path.parent.mkdir(parents=True, exist_ok=True)
        pid_path.write_text(str(os.getpid()), encoding="utf-8")
        DaemonHealthStatus(status_path).write(
            pid=os.getpid(), state="running", started_at="2026-01-01T00:00:00+00:00"
        )


class TestDaemonEntryPoint:
    def test_main_constructs_daemon_and_starts(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _FakeDaemon.instances = []
        monkeypatch.setattr(daemon_mod, "ExecutorDaemon", _FakeDaemon)

        rc = daemon_main(
            [
                "--poll-interval",
                "0.5",
                "--config",
                "company/models.yaml",
                "--registry",
                "company/agent-registry.json",
                "--pid-dir",
                str(tmp_path),
                "--log-dir",
                str(tmp_path),
                "--kpi-snapshot-interval",
                "0",
                "--governance-interval",
                "0",
                "--db-path",
                str(tmp_path / "x.db"),
                "--daily-budget-usd",
                "12.5",
                "--auto-suspend",
            ]
        )

        assert rc == 0
        assert len(_FakeDaemon.instances) == 1
        kwargs = _FakeDaemon.instances[0]
        assert kwargs["pid_path"] == tmp_path / "executor-daemon.pid"
        assert kwargs["log_path"] == tmp_path / "executor-daemon.log"
        assert kwargs["status_path"] == tmp_path / "executor-daemon.json"
        assert kwargs["poll_interval"] == 0.5
        assert kwargs["kpi_snapshot_interval"] == 0
        assert kwargs["governance_interval"] == 0
        assert callable(kwargs["executor_factory"])
        # The child's startup flow wrote PID + status files.
        assert (tmp_path / "executor-daemon.pid").exists()
        status = DaemonHealthStatus(tmp_path / "executor-daemon.json").read()
        assert status is not None
        assert status["state"] == "running"

    def test_main_returns_1_on_runtime_error(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        class _FailingDaemon:
            def __init__(self, **kwargs: Any) -> None:
                pass

            def start(self) -> None:
                raise RuntimeError("Daemon already running with PID 999. Stop it first.")

        monkeypatch.setattr(daemon_mod, "ExecutorDaemon", _FailingDaemon)

        rc = daemon_main(["--pid-dir", str(tmp_path), "--log-dir", str(tmp_path)])

        assert rc == 1


# ── CLI start / stop / status ──────────────────────────────────────────


class TestCliDaemonLifecycle:
    def test_start_writes_pid_and_status_files(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _install_fake_popen(monkeypatch, tmp_path)

        result = runner.invoke(app, _start_args(tmp_path))

        assert result.exit_code == 0, result.output
        assert "Started executor daemon" in result.output
        assert (tmp_path / "executor-daemon.pid").exists()
        status = json.loads((tmp_path / "executor-daemon.json").read_text(encoding="utf-8"))
        assert status["state"] == "running"

    def test_start_refuses_when_daemon_already_running(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        (tmp_path / "executor-daemon.pid").write_text(str(os.getpid()), encoding="utf-8")
        monkeypatch.setattr(daemon_mod, "_is_process_alive", lambda pid: True)

        def _boom(*args: Any, **kwargs: Any) -> None:
            raise AssertionError("Popen must not be called when a daemon is already running")

        monkeypatch.setattr(daemon_mod.subprocess, "Popen", _boom)

        result = runner.invoke(app, _start_args(tmp_path))

        assert result.exit_code == 1
        assert "already running" in result.output

    def test_status_reflects_running(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        status_path = tmp_path / "executor-daemon.json"
        DaemonHealthStatus(status_path).write(
            pid=4242, state="running", started_at="2026-01-01T00:00:00+00:00"
        )
        monkeypatch.setattr(daemon_mod, "_is_process_alive", lambda pid: True)

        result = runner.invoke(app, ["executor", "status", "--log-dir", str(tmp_path)])

        assert result.exit_code == 0
        assert "State: running" in result.output
        assert "PID: 4242" in result.output

    def test_status_reports_stale_running_status_when_pid_dead(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        status_path = tmp_path / "executor-daemon.json"
        DaemonHealthStatus(status_path).write(
            pid=999999, state="running", started_at="2026-01-01T00:00:00+00:00"
        )
        monkeypatch.setattr(daemon_mod, "_is_process_alive", lambda pid: False)

        result = runner.invoke(app, ["executor", "status", "--log-dir", str(tmp_path)])

        assert result.exit_code == 0
        assert "not running (stale)" in result.output

    def test_stop_kills_pid_and_clears_state(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Stop force-terminates the detached PID and clears PID/status state.

        Uses a fake monotonic clock so the graceful-wait timeout path runs in
        microseconds instead of real seconds.
        """
        pid_path = tmp_path / "executor-daemon.pid"
        status_path = tmp_path / "executor-daemon.json"
        pid_path.write_text("4242", encoding="utf-8")
        DaemonHealthStatus(status_path).write(
            pid=4242, state="running", started_at="2026-01-01T00:00:00+00:00"
        )

        counter = {"now": 1000.0}

        def _fake_time() -> float:
            counter["now"] += 1.0
            return counter["now"]

        monkeypatch.setattr(daemon_mod.time, "time", _fake_time)
        monkeypatch.setattr(daemon_mod.time, "sleep", lambda seconds: None)
        monkeypatch.setattr(daemon_mod, "_is_process_alive", lambda pid: True)
        monkeypatch.setattr(ExecutorDaemon, "_force_terminate", lambda self, pid: True)

        result = runner.invoke(
            app, ["executor", "stop", "--pid-dir", str(tmp_path), "--log-dir", str(tmp_path)]
        )

        assert result.exit_code == 0, result.output
        assert "stop signal sent" in result.output.lower()
        # The PID file is gone and status reflects a stopped daemon: no orphan.
        assert not pid_path.exists()
        status = json.loads(status_path.read_text(encoding="utf-8"))
        assert status["state"] == "stopped"
