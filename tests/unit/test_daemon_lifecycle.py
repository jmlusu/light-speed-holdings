"""End-to-end lifecycle tests for ExecutorDaemon (S3-06).

Covers PID file management, status reporting, stop/start semantics on both
Unix and Windows (sentinel-file graceful shutdown), stale PID cleanup,
double-start protection, signal-driven graceful shutdown, and scheduler
enable/disable wiring.
"""

from __future__ import annotations

import os
import signal
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable

import pytest

from ai_company.executor.daemon import (
    DaemonHealthStatus,
    ExecutorDaemon,
)

POLL = 0.2


class _FakeExecutor:
    """Minimal Executor stand-in that records tick calls."""

    def __init__(self) -> None:
        self.ticks = 0

    def tick(self) -> int:
        self.ticks += 1
        return 0


class _FakeClock:
    """Deterministic clock for the daemon's interruptible sleep."""

    def __init__(self, start: float = 1000.0) -> None:
        self.now = start

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


def _make_sleep(
    clock: _FakeClock,
    daemon: ExecutorDaemon,
    stop_after_calls: int | None = None,
) -> Callable[[float], None]:
    """Build a sleep that advances the fake clock and optionally requests
    shutdown after a given number of calls."""
    calls = {"n": 0}

    def _sleep(seconds: float) -> None:
        calls["n"] += 1
        clock.advance(seconds)
        if stop_after_calls is not None and calls["n"] >= stop_after_calls:
            daemon._shutdown_event = True

    return _sleep


def _make_daemon(
    tmp_path: Path,
    *,
    executor_factory: Callable[[], Any] | None = None,
    clock: _FakeClock | None = None,
    kpi_snapshot_interval: float = 0.0,
    governance_interval: float = 0.0,
) -> ExecutorDaemon:
    return ExecutorDaemon(
        executor_factory=executor_factory or _FakeExecutor,
        poll_interval=POLL,
        pid_path=tmp_path / "executor-daemon.pid",
        log_path=tmp_path / "executor-daemon.log",
        status_path=tmp_path / "executor-daemon.json",
        kpi_snapshot_interval=kpi_snapshot_interval,
        governance_interval=governance_interval,
        _clock=clock or _FakeClock(),
    )


def _disable_side_effects(daemon: ExecutorDaemon, monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep tests isolated: no root-logger handlers, no real signal install."""
    monkeypatch.setattr(daemon, "_setup_logging", lambda: None)
    monkeypatch.setattr(daemon, "_install_signal_handlers", lambda: None)


# ── PID file lifecycle ─────────────────────────────────────────────────


class TestPidFileLifecycle:
    def test_pid_file_written_on_start_removed_on_cleanup(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        pid_path = tmp_path / "executor-daemon.pid"
        status_path = tmp_path / "executor-daemon.json"
        executor = _FakeExecutor()
        clock = _FakeClock()
        daemon = _make_daemon(tmp_path, executor_factory=lambda: executor, clock=clock)
        _disable_side_effects(daemon, monkeypatch)
        daemon._sleep = _make_sleep(clock, daemon, stop_after_calls=1)

        observed: dict[str, bool] = {}
        original_tick = executor.tick

        def _observe_tick() -> int:
            observed["pid_exists"] = pid_path.exists()
            observed["status_exists"] = status_path.exists()
            return original_tick()

        executor.tick = _observe_tick  # type: ignore[method-assign]
        daemon.start()

        # While the loop was running both files existed; cleanup removed the
        # PID file and left a stopped status behind.
        assert observed["pid_exists"] is True
        assert observed["status_exists"] is True
        assert not pid_path.exists()
        assert status_path.exists()
        status = daemon.status_file.read()
        assert status is not None
        assert status["state"] == "stopped"
        assert status["pid"] == os.getpid()

    def test_stale_stop_sentinel_cleared_on_start(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # A previous hard-killed run left a stop sentinel behind; a fresh
        # start must clear it or the loop would exit immediately.
        daemon = _make_daemon(tmp_path)
        daemon._request_stop()
        assert daemon.stop_path.exists()

        clock = _FakeClock()
        executor = _FakeExecutor()
        daemon = _make_daemon(tmp_path, executor_factory=lambda: executor, clock=clock)
        _disable_side_effects(daemon, monkeypatch)
        daemon._sleep = _make_sleep(clock, daemon, stop_after_calls=1)

        daemon.start()

        assert not daemon.stop_path.exists()
        assert executor.ticks == 1


# ── Status / running state ─────────────────────────────────────────────


class TestStatusReporting:
    def test_is_daemon_running_and_get_status(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        pid_path = tmp_path / "executor-daemon.pid"
        status_path = tmp_path / "executor-daemon.json"
        status_file = DaemonHealthStatus(status_path)
        status_file.write(pid=4242, state="running", ticks_completed=7)
        pid_path.write_text("4242", encoding="utf-8")

        monkeypatch.setattr("ai_company.executor.daemon._is_process_alive", lambda pid: pid == 4242)
        assert ExecutorDaemon.is_daemon_running(pid_path) is True

        pid_path.write_text("999999", encoding="utf-8")
        assert ExecutorDaemon.is_daemon_running(pid_path) is False

        status = ExecutorDaemon.get_daemon_status(status_path)
        assert status is not None
        assert status["state"] == "running"
        assert status["ticks_completed"] == 7

        assert ExecutorDaemon.get_daemon_status(tmp_path / "missing.json") is None

    def test_status_file_reflects_ticks_completed(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        executor = _FakeExecutor()
        clock = _FakeClock()
        daemon = _make_daemon(tmp_path, executor_factory=lambda: executor, clock=clock)
        _disable_side_effects(daemon, monkeypatch)
        daemon._sleep = _make_sleep(clock, daemon, stop_after_calls=3)

        daemon.start()

        assert executor.ticks == 3
        status = daemon.status_file.read()
        assert status is not None
        assert status["ticks_completed"] == 3
        assert status["state"] == "stopped"


# ── stop_daemon ────────────────────────────────────────────────────────


class TestStopDaemon:
    def test_stop_daemon_writes_sentinel_and_waits_for_clean_exit(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Windows path: no SIGTERM available, so the sentinel file is the
        stop mechanism; returns True once the process exits."""
        pid_path = tmp_path / "executor-daemon.pid"
        pid_path.write_text("4242", encoding="utf-8")
        clock = _FakeClock()
        daemon = _make_daemon(tmp_path, clock=clock)
        daemon._sleep = lambda seconds: clock.advance(seconds)

        calls = {"n": 0}
        monkeypatch.setattr(
            "ai_company.executor.daemon._is_process_alive",
            lambda pid: calls.__setitem__("n", calls["n"] + 1) or calls["n"] == 1,
        )
        # Force the Windows code path so the real SIGTERM is never sent to a
        # non-existent PID (which raises ProcessLookupError on Linux CI).
        monkeypatch.setattr("ai_company.executor.daemon.os.name", "nt")

        result = daemon.stop_daemon(timeout=5.0)

        assert result is True
        # Sentinel written so the daemon's loop can shut down gracefully.
        assert daemon.stop_path.exists()
        assert daemon.stop_path.read_text(encoding="utf-8") == "stop"
        # PID file remains until the daemon's own cleanup runs — the caller
        # does not delete it for a gracefully-exiting daemon.
        assert pid_path.exists()

    def test_stop_daemon_sends_sigterm_on_posix(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Unix path: SIGTERM is delivered to the recorded PID."""
        pid_path = tmp_path / "executor-daemon.pid"
        pid_path.write_text("4242", encoding="utf-8")
        clock = _FakeClock()
        daemon = _make_daemon(tmp_path, clock=clock)
        daemon._sleep = lambda seconds: clock.advance(seconds)

        sent: list[tuple[int, int]] = []
        monkeypatch.setattr("ai_company.executor.daemon.os.name", "posix")
        monkeypatch.setattr(
            "ai_company.executor.daemon.os.kill",
            lambda pid, sig: sent.append((pid, sig)),
        )
        calls = {"n": 0}
        monkeypatch.setattr(
            "ai_company.executor.daemon._is_process_alive",
            lambda pid: calls.__setitem__("n", calls["n"] + 1) or calls["n"] == 1,
        )

        result = daemon.stop_daemon(timeout=5.0)

        assert result is True
        assert sent == [(4242, signal.SIGTERM)]
        assert daemon.stop_path.exists()

    def test_stop_daemon_cleans_stale_pid_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A PID file pointing at a dead process is cleaned up and reports
        stopped, and stop_daemon returns False (nothing was running)."""
        pid_path = tmp_path / "executor-daemon.pid"
        status_path = tmp_path / "executor-daemon.json"
        pid_path.write_text("999999", encoding="utf-8")
        daemon = _make_daemon(tmp_path)
        monkeypatch.setattr("ai_company.executor.daemon._is_process_alive", lambda pid: False)

        result = daemon.stop_daemon(timeout=5.0)

        assert result is False
        assert not pid_path.exists()
        status = DaemonHealthStatus(status_path).read()
        assert status is not None
        assert status["state"] == "stopped"

    def test_stop_daemon_force_terminates_after_timeout(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """If the daemon ignores the graceful stop, stop_daemon force-
        terminates and cleans up stale state from the caller side."""
        pid_path = tmp_path / "executor-daemon.pid"
        status_path = tmp_path / "executor-daemon.json"
        pid_path.write_text("4242", encoding="utf-8")
        status_file = DaemonHealthStatus(status_path)
        status_file.write(pid=4242, state="running", started_at="2026-01-01T00:00:00+00:00")
        clock = _FakeClock()
        daemon = _make_daemon(tmp_path, clock=clock)
        daemon._sleep = lambda seconds: clock.advance(seconds)

        # Process stays alive forever (simulating a blocked tick).
        monkeypatch.setattr("ai_company.executor.daemon._is_process_alive", lambda pid: True)
        # SIGTERM delivery is a no-op (process ignores the graceful stop), so
        # the timeout path is reached on both Windows and Linux CI.
        monkeypatch.setattr("ai_company.executor.daemon.os.kill", lambda pid, sig: None)
        monkeypatch.setattr(daemon, "_force_terminate", lambda pid: True)

        result = daemon.stop_daemon(timeout=0.5)

        assert result is True
        assert not pid_path.exists()
        assert not daemon.stop_path.exists()
        status = daemon.status_file.read()
        assert status is not None
        assert status["state"] == "stopped"
        # Existing history preserved for `executor status` after forced stop.
        assert status["started_at"] == "2026-01-01T00:00:00+00:00"


# ── Double start protection ────────────────────────────────────────────


class TestDoubleStart:
    def test_start_refuses_when_pid_file_points_to_live_process(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        pid_path = tmp_path / "executor-daemon.pid"
        pid_path.write_text(str(os.getpid()), encoding="utf-8")  # this test process
        daemon = _make_daemon(tmp_path)
        _disable_side_effects(daemon, monkeypatch)

        with pytest.raises(RuntimeError, match="already running"):
            daemon.start()

        # PID file must not have been overwritten.
        assert pid_path.read_text(encoding="utf-8") == str(os.getpid())


# ── Graceful shutdown via signal ───────────────────────────────────────


class TestSignalShutdown:
    def test_signal_handler_sets_shutdown_event_and_loop_exits(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        handlers: dict[int, Any] = {}
        monkeypatch.setattr(
            "ai_company.executor.daemon.signal.signal",
            lambda signum, handler: handlers.__setitem__(signum, handler),
        )
        executor = _FakeExecutor()
        clock = _FakeClock()
        daemon = _make_daemon(tmp_path, executor_factory=lambda: executor, clock=clock)
        monkeypatch.setattr(daemon, "_setup_logging", lambda: None)

        def _sleep_then_signal(seconds: float) -> None:
            clock.advance(seconds)
            handlers[signal.SIGTERM](signal.SIGTERM, None)  # simulate SIGTERM delivery

        daemon._sleep = _sleep_then_signal

        daemon.start()

        # Handler fired after the first tick: loop exits, cleanup runs.
        assert executor.ticks == 1
        assert daemon._shutdown_event is True
        assert not (tmp_path / "executor-daemon.pid").exists()
        status = daemon.status_file.read()
        assert status is not None
        assert status["state"] == "stopped"


# ── Scheduler wiring ───────────────────────────────────────────────────


class TestSchedulerWiring:
    def test_disabled_intervals_return_no_schedulers(self, tmp_path: Path) -> None:
        daemon = _make_daemon(tmp_path, kpi_snapshot_interval=0, governance_interval=0)
        executor = SimpleNamespace(database=None)

        assert daemon._make_snapshot_scheduler(executor) is None
        assert daemon._make_governance_scheduler(executor) is None

    def test_negative_intervals_also_disable_schedulers(self, tmp_path: Path) -> None:
        daemon = _make_daemon(tmp_path, kpi_snapshot_interval=-1, governance_interval=-5)
        executor = SimpleNamespace(database=None)

        assert daemon._make_snapshot_scheduler(executor) is None
        assert daemon._make_governance_scheduler(executor) is None

    def test_positive_intervals_build_schedulers(self, tmp_path: Path) -> None:
        from ai_company.dashboard.kpis.scheduler import KPISnapshotScheduler
        from ai_company.data import GovernanceScheduler

        daemon = _make_daemon(tmp_path, kpi_snapshot_interval=30, governance_interval=60)
        executor = SimpleNamespace(database=None)

        snapshot = daemon._make_snapshot_scheduler(executor)
        governance = daemon._make_governance_scheduler(executor)
        assert isinstance(snapshot, KPISnapshotScheduler)
        assert isinstance(governance, GovernanceScheduler)
