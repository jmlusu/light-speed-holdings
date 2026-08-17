"""Daemon mode for the executor.

Provides background autonomous operation with:
- PID file management (write/check/remove)
- Signal handling (SIGTERM, SIGINT) for graceful shutdown
- File logging when in daemon mode
- Periodic task execution loop
- Health check / status file

Usage:
    # Via CLI (preferred):
    ai-company executor start --daemon
    ai-company executor stop
    ai-company executor status

    # Programmatically:
    daemon = ExecutorDaemon(executor_factory=my_factory)
    daemon.start()  # forks or runs in-process
"""

from __future__ import annotations

import argparse
import json
import logging
import logging.handlers
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, cast

from ai_company.logging_config import HumanFormatter, JSONFormatter
from ai_company.utils.file_lock import atomic_write
from ai_company.utils.logging import CorrelationFilter

logger = logging.getLogger(__name__)

# Default paths
DEFAULT_PID_DIR = Path("logs")
DEFAULT_LOG_DIR = Path("logs")
DEFAULT_HEALTH_FILE = Path("logs") / "executor-daemon.json"


def _sweep_expired_approvals(executor: Any) -> int:
    """Expire stale pending approval requests (Sprint 7).

    Prefers the executor's live ``ApprovalGate`` so in-memory state stays
    consistent with the sweep; falls back to the singleton gate over the shared
    approvals file when the executor has no HITL gate.
    """
    from ai_company.orchestrator.approval import ApprovalGate

    gate = getattr(getattr(executor, "hitl", None), "gate", None)
    if not isinstance(gate, ApprovalGate):
        gate = ApprovalGate.get_instance()
    return gate.sweep_expired()


def _archive_resolved_approvals(executor: Any) -> int:
    """Archive resolved approval requests past the retention window (ticket #58).

    The approvals store is a working store, not the ledger: resolved
    (approved/rejected/expired) requests older than the gate's retention
    window are dropped from the YAML on the governance cadence, while the
    append-only audit trail keeps the full history.

    Requests still referenced by the executor's live resume index
    (``_pending_approvals``, i.e. tasks currently parked in
    ``WAITING_APPROVAL``) are passed as protected so a parked task can never
    lose the request that decides its resume.
    """
    from ai_company.orchestrator.approval import ApprovalGate

    gate = getattr(getattr(executor, "hitl", None), "gate", None)
    if not isinstance(gate, ApprovalGate):
        gate = ApprovalGate.get_instance()
    pending_index = getattr(executor, "_pending_approvals", None)
    protected: set[str] = set()
    if pending_index:
        protected = {str(request_id) for request_id in pending_index.values()}
    return gate.archive_resolved(protected_request_ids=protected)


def _sweep_suspended_states(executor: Any) -> int:
    """Remove suspended state files older than the retention window (issue #42).

    Called on the daemon's governance cadence alongside approval expiry and
    archival.  Uses the executor's ``SuspendStore`` when available; falls
    back to a fresh store over the default directory.
    """
    store = getattr(executor, "_suspend_store", None)
    if store is None:
        from ai_company.orchestrator.suspend_store import SuspendStore

        store = SuspendStore()
    return store.sweep_expired()


def resolve_database(db_path: str | None) -> Any:
    """Initialise and return the SQLite database for write-through.

    ``None`` keeps the legacy file-only behaviour; a real database is
    returned so MessageBus/CostTracker/audit mirror mutations into it.
    """
    if db_path is None:
        return None
    from ai_company.data.database import init_database

    return init_database(db_path)


def build_executor_factory(
    *,
    poll_interval: float,
    config: str,
    registry: str,
    db_path: str | None,
    daily_budget_usd: float | None = None,
    task_budget_usd: float | None = None,
    auto_suspend: bool = False,
) -> Callable[..., Any]:
    """Return a factory that builds the executor loop instance.

    Deferred construction keeps daemon startup light: the heavy LLM/embedding
    imports happen only once the poll loop actually begins, not when the
    detached subprocess boots.
    """

    def factory() -> Any:
        from ai_company.executor.loop import Executor

        return Executor(
            poll_interval=poll_interval,
            config_path=config,
            registry_path=registry,
            database=resolve_database(db_path),
            daily_budget_usd=daily_budget_usd,
            task_budget_usd=task_budget_usd,
            auto_suspend_on_overspend=auto_suspend,
        )

    return factory


def build_daemon_command(
    *,
    poll_interval: float,
    config: str,
    registry: str,
    pid_dir: str,
    log_dir: str,
    kpi_snapshot_interval: float,
    governance_interval: float,
    db_path: str | None,
    daily_budget_usd: float | None = None,
    task_budget_usd: float | None = None,
    auto_suspend: bool = False,
) -> list[str]:
    """Build the argv used to spawn the detached daemon subprocess.

    The child runs the daemon module entry point in a *fresh interpreter*
    (``python -m ai_company.executor.daemon``) so the daemon is a real OS
    process that survives the shell that launched it (GitHub #56).
    """
    cmd = [
        sys.executable,
        "-m",
        "ai_company.executor.daemon",
        "--poll-interval",
        str(poll_interval),
        "--config",
        config,
        "--registry",
        registry,
        "--pid-dir",
        pid_dir,
        "--log-dir",
        log_dir,
        "--kpi-snapshot-interval",
        str(kpi_snapshot_interval),
        "--governance-interval",
        str(governance_interval),
    ]
    if db_path is not None:
        cmd += ["--db-path", db_path]
    if daily_budget_usd is not None:
        cmd += ["--daily-budget-usd", str(daily_budget_usd)]
    if task_budget_usd is not None:
        cmd += ["--task-budget-usd", str(task_budget_usd)]
    if auto_suspend:
        cmd.append("--auto-suspend")
    return cmd


def _windows_detach_flags() -> int:
    """Windows creation flags that detach a child from the parent console.

    ``DETACHED_PROCESS`` gives the child no inherited console, and
    ``CREATE_NEW_PROCESS_GROUP`` makes it a new process group so it can never
    receive Ctrl+C sent to the parent's console. Returns 0 on non-Windows
    platforms, where :func:`launch_detached_daemon` detaches via
    ``start_new_session`` instead. ``getattr`` keeps the module importable on
    platforms whose ``subprocess`` lacks the constants.
    """
    if os.name != "nt":
        return 0
    return getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | getattr(
        subprocess, "DETACHED_PROCESS", 0
    )


def _daemon_start_failure_message(log_path: Path, proc: subprocess.Popen[Any]) -> str:
    """Compose a diagnosable error when the daemon child dies during startup."""
    exit_code = proc.poll()
    tail = ""
    if log_path.exists():
        try:
            lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
            tail = "\n".join(lines[-10:])
        except OSError:
            tail = ""
    return (
        f"Daemon process exited during startup (exit code {exit_code}).\n"
        f"Recent log output:\n{tail or '(no log output yet)'}"
    )


def launch_detached_daemon(
    *,
    poll_interval: float,
    config: str,
    registry: str,
    pid_dir: str,
    log_dir: str,
    kpi_snapshot_interval: float,
    governance_interval: float,
    db_path: str | None,
    daily_budget_usd: float | None = None,
    task_budget_usd: float | None = None,
    auto_suspend: bool = False,
    wait_timeout: float = 10.0,
) -> int:
    """Spawn the daemon loop as a detached OS process and return its PID.

    The child writes its own PID/status files (its ``start()`` flow); the
    parent only waits for the PID file to appear (up to *wait_timeout*
    seconds) so ``executor stop`` / ``executor status`` work immediately
    after ``start`` returns.

    On Windows the child is spawned with ``CREATE_NEW_PROCESS_GROUP |
    DETACHED_PROCESS``; on POSIX with ``start_new_session``. stdout/stderr
    are redirected to the daemon log file so the detached process has a
    valid output target and no console dependency.

    Raises:
        RuntimeError: If a daemon is already running, the child cannot be
            spawned, or the child exits before recording its PID.
    """
    pid_path = Path(pid_dir) / "executor-daemon.pid"
    log_path = Path(log_dir) / "executor-daemon.log"

    if ExecutorDaemon.is_daemon_running(pid_path):
        existing_pid = pid_path.read_text(encoding="utf-8").strip()
        raise RuntimeError(
            f"Daemon already running with PID {existing_pid}. Use 'executor stop' to stop it first."
        )

    cmd = build_daemon_command(
        poll_interval=poll_interval,
        config=config,
        registry=registry,
        pid_dir=pid_dir,
        log_dir=log_dir,
        kpi_snapshot_interval=kpi_snapshot_interval,
        governance_interval=governance_interval,
        db_path=db_path,
        daily_budget_usd=daily_budget_usd,
        task_budget_usd=task_budget_usd,
        auto_suspend=auto_suspend,
    )

    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as log_handle:
        try:
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.DEVNULL,
                stdout=log_handle,
                stderr=log_handle,
                creationflags=_windows_detach_flags(),
                start_new_session=True,  # POSIX: setsid(); ignored on Windows
            )
        except OSError as exc:
            raise RuntimeError(f"Failed to spawn daemon process: {exc}") from exc

    # Wait for the child to record its PID. If it exits before doing so,
    # surface the tail of the log so the failure is diagnosable.
    deadline = time.monotonic() + wait_timeout
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            break
        try:
            pid = int(pid_path.read_text(encoding="utf-8").strip())
        except (OSError, ValueError):
            pid = None
        if pid is not None:
            return pid
        time.sleep(0.1)

    raise RuntimeError(_daemon_start_failure_message(log_path, proc))


def main(argv: list[str] | None = None) -> int:
    """Daemon loop entry point for the detached subprocess.

    Invoked by ``python -m ai_company.executor.daemon`` (see
    :func:`launch_detached_daemon`). Runs the executor poll loop in-process
    with PID/status file management until a stop is requested.
    """
    parser = argparse.ArgumentParser(
        prog="python -m ai_company.executor.daemon",
        description="AI Company executor daemon loop (detached subprocess).",
    )
    parser.add_argument("--poll-interval", type=float, default=5.0)
    parser.add_argument("--config", default="company/models.yaml")
    parser.add_argument("--registry", default="company/agent-registry.json")
    parser.add_argument("--pid-dir", default="logs")
    parser.add_argument("--log-dir", default="logs")
    parser.add_argument("--kpi-snapshot-interval", type=float, default=300.0)
    parser.add_argument("--governance-interval", type=float, default=86400.0)
    parser.add_argument("--db-path", default=None)
    parser.add_argument("--daily-budget-usd", type=float, default=None)
    parser.add_argument("--task-budget-usd", type=float, default=None)
    parser.add_argument("--auto-suspend", action="store_true")
    args = parser.parse_args(argv)

    daemon = ExecutorDaemon(
        executor_factory=build_executor_factory(
            poll_interval=args.poll_interval,
            config=args.config,
            registry=args.registry,
            db_path=args.db_path,
            daily_budget_usd=args.daily_budget_usd,
            task_budget_usd=args.task_budget_usd,
            auto_suspend=args.auto_suspend,
        ),
        poll_interval=args.poll_interval,
        pid_path=Path(args.pid_dir) / "executor-daemon.pid",
        log_path=Path(args.log_dir) / "executor-daemon.log",
        status_path=Path(args.log_dir) / "executor-daemon.json",
        kpi_snapshot_interval=args.kpi_snapshot_interval,
        governance_interval=args.governance_interval,
    )
    try:
        daemon.start()
    except RuntimeError as exc:
        print(f"Daemon error: {exc}", file=sys.stderr)
        return 1
    return 0


class DaemonPIDFile:
    """Manages a PID file for daemon lifecycle tracking.

    The PID file contains the process ID of the running daemon and is used
    to prevent multiple daemon instances and to enable stop/status commands.
    """

    def __init__(self, pid_path: Path) -> None:
        self.pid_path = pid_path

    def write(self, pid: int | None = None) -> None:
        """Write the current (or given) PID to the file atomically.

        Creates parent directories if they don't exist.  The write is atomic
        (temp-file-then-rename) so a crash mid-write can never leave a
        truncated PID file that :meth:`read` misparses.
        """
        if pid is None:
            pid = os.getpid()
        self.pid_path.parent.mkdir(parents=True, exist_ok=True)
        with atomic_write(self.pid_path) as f:
            f.write(str(pid))
        logger.debug("PID file written: %s (pid=%d)", self.pid_path, pid)

    def read(self) -> int | None:
        """Read the PID from the file. Returns None if file is missing or invalid."""
        if not self.pid_path.exists():
            return None
        try:
            content = self.pid_path.read_text(encoding="utf-8").strip()
            return int(content)
        except (ValueError, OSError):
            return None

    def is_running(self) -> bool:
        """Check if the process recorded in the PID file is actually running."""
        pid = self.read()
        if pid is None:
            return False
        return _is_process_alive(pid)

    def remove(self) -> bool:
        """Remove the PID file. Returns True if it existed."""
        if self.pid_path.exists():
            self.pid_path.unlink()
            logger.debug("PID file removed: %s", self.pid_path)
            return True
        return False


def _is_process_alive(pid: int) -> bool:
    """Check whether a process with the given PID is running."""
    # Windows: os.kill(pid, 0) is not supported. Use psutil or OpenProcess.
    try:
        import psutil

        return bool(psutil.pid_exists(pid))
    except ImportError:
        pass

    # Fallback for Unix-like systems
    if hasattr(os, "kill"):
        try:
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            return False
        except PermissionError:
            # Process exists but we don't have permission to signal it.
            return True
        except OSError:
            # On Windows, os.kill with signal 0 raises OSError.
            # Try to use ctypes to check.
            try:
                import ctypes

                kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]  # Windows-only module
                handle = kernel32.OpenProcess(
                    0x0400 | 0x0010, False, pid
                )  # PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE
                if handle:
                    kernel32.CloseHandle(handle)
                    return True
                return False
            except Exception:  # noqa: BLE001 - process probe may fail; fall back to False
                return False

    return False


class DaemonHealthStatus:
    """Writes and reads a JSON health/status file for the daemon.

    The status file contains:
    - pid: current daemon PID
    - state: running | stopping | stopped
    - started_at: ISO timestamp of when the daemon started
    - last_tick_at: ISO timestamp of last tick completion
    - ticks_completed: total tick count
    - uptime_seconds: seconds since start
    """

    def __init__(self, status_path: Path) -> None:
        self.status_path = status_path

    def write(
        self,
        *,
        pid: int,
        state: str,
        started_at: str | None = None,
        last_tick_at: str | None = None,
        ticks_completed: int = 0,
    ) -> None:
        """Write daemon status to the JSON file."""
        now_iso = datetime.now(timezone.utc).isoformat()
        uptime = 0.0
        if started_at:
            try:
                start_dt = datetime.fromisoformat(started_at)
                uptime = (datetime.now(timezone.utc) - start_dt).total_seconds()
            except ValueError:
                uptime = 0.0

        data = {
            "pid": pid,
            "state": state,
            "started_at": started_at or now_iso,
            "last_tick_at": last_tick_at,
            "ticks_completed": ticks_completed,
            "uptime_seconds": round(uptime, 1),
            "updated_at": now_iso,
        }
        self.status_path.parent.mkdir(parents=True, exist_ok=True)
        with atomic_write(self.status_path) as f:
            f.write(json.dumps(data, indent=2, default=str))
        logger.debug("Health status written: %s", self.status_path)

    def read(self) -> dict[str, Any] | None:
        """Read daemon status from the JSON file. Returns None if missing."""
        if not self.status_path.exists():
            return None
        try:
            return cast(
                dict[str, Any],
                json.loads(self.status_path.read_text(encoding="utf-8")),
            )
        except (json.JSONDecodeError, OSError):
            return None

    def remove(self) -> bool:
        """Remove the status file."""
        if self.status_path.exists():
            self.status_path.unlink()
            return True
        return False


class ExecutorDaemon:
    """Runs the Executor in daemon mode with PID management, signal handling,
    file logging, and periodic health status updates.

    The daemon wraps an existing Executor instance and its tick() loop,
    adding lifecycle management appropriate for long-running background
    processes.

    Args:
        executor_factory: Callable that returns an Executor instance. Deferred
            creation so the daemon can set up logging/signals before importing
            heavy modules.
        poll_interval: Seconds between polling cycles.
        pid_path: Path to the PID file.
        log_path: Path to the log file (None = no file logging).
        status_path: Path to the health/status JSON file.
        stop_path: Path to the stop-request sentinel file. When this file
            exists the daemon's poll loop exits gracefully. Windows cannot
            run Python signal handlers via ``TerminateProcess``, so this
            sentinel is the reliable cross-platform stop mechanism.
        kpi_snapshot_interval: Seconds between periodic KPI snapshot
            collections (Sprint 2, Item 3). ``<= 0`` disables collection.
        governance_interval: Seconds between periodic retention enforcement
            (Sprint 3, item 3). <= 0 disables.
    """

    def __init__(
        self,
        executor_factory: Callable[..., Any],
        poll_interval: float = 5.0,
        pid_path: Path | None = None,
        log_path: Path | None = None,
        status_path: Path | None = None,
        stop_path: Path | None = None,
        kpi_snapshot_interval: float = 300.0,
        governance_interval: float = 86400.0,
        *,
        _clock: Callable[[], float] | None = None,
        _sleep: Callable[[float], None] | None = None,
    ) -> None:
        self.executor_factory = executor_factory
        self.poll_interval = poll_interval
        self.kpi_snapshot_interval = kpi_snapshot_interval
        self.governance_interval = governance_interval

        self.pid_file = DaemonPIDFile(pid_path or (DEFAULT_PID_DIR / "executor-daemon.pid"))
        self.status_file = DaemonHealthStatus(status_path or DEFAULT_HEALTH_FILE)
        self.log_path = log_path or (DEFAULT_LOG_DIR / "executor-daemon.log")
        self.stop_path = stop_path or self.pid_file.pid_path.with_suffix(".stop")

        self._shutdown_event = False
        self._started_at: str | None = None
        self._ticks_completed: int = 0

        # Injectable for testing
        self._clock = _clock or time.time
        self._sleep = _sleep or time.sleep

    # ── Public API ───────────────────────────────────────────────────

    def start(self) -> None:
        """Start the daemon. Sets up PID file, signals, logging, then
        enters the polling loop.

        Raises:
            RuntimeError: If another daemon instance is already running.
        """
        # Guard against double-start
        if self.pid_file.is_running():
            existing_pid = self.pid_file.read()
            raise RuntimeError(
                f"Daemon already running with PID {existing_pid}. "
                "Use 'executor stop' to stop it first."
            )

        # Set up file logging
        self._setup_logging()

        # Clear any stale stop-request file left by a previous (hard-killed)
        # run so the new daemon does not immediately shut itself down.
        self._clear_stop_request()

        # Write PID file
        pid = os.getpid()
        self.pid_file.write(pid)
        logger.info("Executor daemon starting (PID=%d)", pid)

        # Record start time and install signal handlers
        self._started_at = datetime.now(timezone.utc).isoformat()
        self._install_signal_handlers()

        # Write initial status
        self._update_status("running")

        # Enter main loop
        try:
            self._run_loop()
        except Exception:
            logger.exception("Executor daemon encountered an unhandled exception")
            raise
        finally:
            self._cleanup()

    def stop_daemon(self, timeout: float = 15.0) -> bool:
        """Stop the daemon process recorded in the PID file.

        Works reliably on both Unix and Windows:

        1. Writes a stop-request sentinel file. The daemon's poll loop
           watches for it and performs a graceful shutdown (pending tasks
           in the in-flight tick are flushed, PID file removed, status set
           to ``stopped``). On Windows this is the ONLY reliable stop
           mechanism: ``os.kill(pid, SIGTERM)`` and ``psutil.terminate()``
           map to ``TerminateProcess``, which kills the process without
           running Python signal handlers or ``finally`` cleanup.
        2. On Unix, also sends ``SIGTERM`` so the in-process handler fires
           immediately.
        3. Waits up to *timeout* seconds for the daemon to exit cleanly.
        4. If it does not exit in time (e.g. blocked in a long tick),
           force-terminates the process and removes stale PID/status files
           from the caller side.

        Returns:
            True if the daemon was stopped (or a stop was requested for a
            live process), False if no running daemon was found.
        """
        pid = self.pid_file.read()
        if pid is None:
            return False

        if not _is_process_alive(pid):
            # Stale PID file — clean up
            self._mark_stopped(pid)
            logger.info("Stale PID file cleaned up (pid=%d)", pid)
            return False

        # 1. Stop-request sentinel (cross-platform graceful shutdown).
        self._request_stop()

        # 2. Unix fast path: SIGTERM triggers the in-process handler.
        if os.name != "nt":
            try:
                os.kill(pid, signal.SIGTERM)
                logger.info("Sent SIGTERM to daemon PID %d", pid)
            except ProcessLookupError:
                # The daemon already exited between the alive-check and the
                # signal — the stop has effectively succeeded, so clean up
                # the stale PID/status files and report success.
                self._mark_stopped(pid)
                logger.info("Daemon PID %d already gone at SIGTERM; stop successful", pid)
                return True
            except PermissionError:
                logger.error("No permission to signal PID %d", pid)
                return False

        # 3. Wait for the daemon to exit gracefully (it removes its own
        #    PID file in _cleanup()).
        deadline = self._clock() + timeout
        while self._clock() < deadline and _is_process_alive(pid):
            self._sleep(0.2)

        if not _is_process_alive(pid):
            logger.info("Daemon PID %d exited cleanly", pid)
            return True

        # 4. Timeout fallback: force terminate + caller-side cleanup.
        logger.warning("Daemon PID %d did not exit within %.1fs; forcing terminate", pid, timeout)
        if not self._force_terminate(pid):
            return False
        self._mark_stopped(pid)
        return True

    @staticmethod
    def is_daemon_running(pid_path: Path | None = None) -> bool:
        """Check if a daemon instance is currently running."""
        pid_file = DaemonPIDFile(pid_path or (DEFAULT_PID_DIR / "executor-daemon.pid"))
        return pid_file.is_running()

    @staticmethod
    def is_pid_alive(pid: int) -> bool:
        """Return True if the process with the given PID is still alive."""
        return _is_process_alive(pid)

    @staticmethod
    def get_daemon_status(
        status_path: Path | None = None,
    ) -> dict[str, Any] | None:
        """Read the daemon status file. Returns None if no daemon status exists."""
        sf = DaemonHealthStatus(status_path or DEFAULT_HEALTH_FILE)
        return sf.read()

    # ── Internal ─────────────────────────────────────────────────────

    def _run_loop(self) -> None:
        """Main polling loop — creates executor and calls tick() periodically."""
        executor = self.executor_factory()
        logger.info("Executor created; entering poll loop (interval=%.1fs)", self.poll_interval)

        snapshot_scheduler = self._make_snapshot_scheduler(executor)
        governance_scheduler = self._make_governance_scheduler(executor)

        while not self._shutdown_event:
            # Graceful stop requested via sentinel file (Windows relies on
            # this because TerminateProcess cannot run Python handlers).
            if self._stop_requested():
                logger.info("Stop requested via sentinel file — shutting down")
                self._shutdown_event = True
                break
            try:
                count = executor.tick()
                self._ticks_completed += 1
                logger.info(
                    "Tick #%d completed — processed %d task(s)",
                    self._ticks_completed,
                    count,
                )
                self._update_status("running")
            except Exception:
                logger.exception("Error during tick")

            if snapshot_scheduler is not None:
                try:
                    stored = snapshot_scheduler.run_due()
                    if stored:
                        logger.info("KPI snapshot stored %d entries", stored)
                except Exception:
                    logger.exception("Error during KPI snapshot collection")

            if governance_scheduler is not None:
                try:
                    processed = governance_scheduler.run_due()
                    if processed:
                        logger.info("Retention enforcement processed %d table(s)", len(processed))
                except Exception:
                    logger.exception("Error during retention enforcement")

                # Sprint 7: expire stale pending approval requests on the same
                # governance cadence (no new threads/timers).
                try:
                    expired = _sweep_expired_approvals(executor)
                    if expired:
                        logger.info("Expired %d stale approval request(s)", expired)
                except Exception:
                    logger.exception("Error during approval expiry sweep")

                # Ticket #58: archive resolved approvals past the retention
                # window on the same cadence so the working store stays
                # bounded; the audit trail remains the durable ledger.
                try:
                    archived = _archive_resolved_approvals(executor)
                    if archived:
                        logger.info("Archived %d resolved approval request(s)", archived)
                except Exception:
                    logger.exception("Error during approval archival")

                # Issue #42: sweep expired suspended state files on the same
                # governance cadence so disk usage stays bounded.
                try:
                    swept = _sweep_suspended_states(executor)
                    if swept:
                        logger.info("Swept %d expired suspended state file(s)", swept)
                except Exception:
                    logger.exception("Error during suspended state sweep")

            # Sleep in small increments so we can respond to signals quickly
            self._interruptible_sleep(self.poll_interval)

    def _make_snapshot_scheduler(self, executor: Any) -> Any:
        """Build the periodic KPI snapshot scheduler, or ``None`` if disabled."""
        if self.kpi_snapshot_interval <= 0:
            return None
        from ai_company.dashboard.kpis.scheduler import KPISnapshotScheduler

        return KPISnapshotScheduler(
            interval_seconds=self.kpi_snapshot_interval,
            database=getattr(executor, "database", None),
        )

    def _make_governance_scheduler(self, executor: Any) -> Any:
        """Build the periodic retention scheduler, or None if disabled."""
        if self.governance_interval <= 0:
            return None
        from ai_company.data import GovernanceScheduler

        return GovernanceScheduler(
            interval_seconds=self.governance_interval,
            database=getattr(executor, "database", None),
        )

    def _interruptible_sleep(self, duration: float) -> None:
        """Sleep for *duration* seconds, checking the shutdown flag frequently."""
        end = self._clock() + duration
        while not self._shutdown_event and self._clock() < end:
            if self._stop_requested():
                self._shutdown_event = True
                break
            remaining = end - self._clock()
            chunk = min(remaining, 1.0)
            if chunk > 0:
                self._sleep(chunk)

    def _setup_logging(self) -> None:
        """Configure structured logging for daemon mode (GAP-018).

        File handler writes structured JSON lines; console handler writes
        human-readable output; a CorrelationFilter injects the correlation
        ID into every record so daemon logs are traceable per task.
        """
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        if not any(isinstance(f, CorrelationFilter) for f in root_logger.filters):
            root_logger.addFilter(CorrelationFilter())

        # File handler — always structured JSON
        fh = logging.handlers.RotatingFileHandler(
            str(self.log_path),
            maxBytes=10_000_000,
            backupCount=5,
            encoding="utf-8",
        )
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(JSONFormatter())
        root_logger.addHandler(fh)

        # Console handler (stderr) — human-readable
        ch = logging.StreamHandler(sys.stderr)
        ch.setLevel(logging.INFO)
        ch.setFormatter(HumanFormatter())
        root_logger.addHandler(ch)

        logger.info("Daemon logging initialized → %s", self.log_path)

    def _install_signal_handlers(self) -> None:
        """Install SIGTERM and SIGINT handlers for graceful shutdown."""

        def _handle_sigterm(signum: int, frame: Any) -> None:
            logger.info("Received SIGTERM — initiating graceful shutdown")
            self._shutdown_event = True
            self._update_status("stopping")

        def _handle_sigint(signum: int, frame: Any) -> None:
            logger.info("Received SIGINT — initiating graceful shutdown")
            self._shutdown_event = True
            self._update_status("stopping")

        signal.signal(signal.SIGTERM, _handle_sigterm)
        signal.signal(signal.SIGINT, _handle_sigint)
        logger.debug("Signal handlers installed (SIGTERM, SIGINT)")

    def _update_status(self, state: str) -> None:
        """Write current status to the health file."""
        self.status_file.write(
            pid=os.getpid(),
            state=state,
            started_at=self._started_at,
            ticks_completed=self._ticks_completed,
        )

    def _stop_requested(self) -> bool:
        """Return True if a stop-request sentinel file is present."""
        try:
            return self.stop_path.exists()
        except OSError:
            return False

    def _request_stop(self) -> None:
        """Write the stop-request sentinel file the daemon's loop watches."""
        self.stop_path.parent.mkdir(parents=True, exist_ok=True)
        self.stop_path.write_text("stop", encoding="utf-8")
        logger.info("Stop request sentinel written: %s", self.stop_path)

    def _clear_stop_request(self) -> None:
        """Remove the stop-request sentinel file if present."""
        if self.stop_path.exists():
            try:
                self.stop_path.unlink()
            except OSError:
                logger.debug("Failed to remove stop sentinel %s", self.stop_path)

    def _mark_stopped(self, pid: int) -> None:
        """Remove PID file and write a 'stopped' status (stale/forced stop).

        Used when the daemon process cannot clean up after itself: stale PID
        files, or after a force-terminate on Windows where the daemon never
        ran its ``finally`` cleanup. Preserves any existing status history
        (started_at, ticks_completed) so ``executor status`` still reports
        meaningful data after a forced stop.
        """
        existing = self.status_file.read() or {}
        self._clear_stop_request()
        self.pid_file.remove()
        self.status_file.write(
            pid=pid,
            state="stopped",
            started_at=existing.get("started_at") or self._started_at,
            ticks_completed=existing.get("ticks_completed") or self._ticks_completed,
        )
        logger.info("Marked daemon PID %d as stopped", pid)

    def _force_terminate(self, pid: int) -> bool:
        """Force-terminate a process that ignored the graceful stop request.

        Uses psutil when available (TerminateProcess on Windows, SIGTERM +
        SIGKILL fallback on Unix); falls back to ``os.kill`` for
        minimal-environment cases.
        """
        try:
            import psutil
        except ImportError:  # pragma: no cover - psutil is a hard dependency
            try:
                os.kill(pid, signal.SIGTERM)
                return True
            except OSError:
                logger.error("Failed to terminate PID %d via os.kill", pid)
                return False

        try:
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait(timeout=5.0)
            return True
        except psutil.NoSuchProcess:
            # Already gone — nothing to do.
            return True
        except psutil.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5.0)
            return True
        except psutil.AccessDenied:
            logger.error("No permission to terminate PID %d", pid)
            return False
        except Exception:  # noqa: BLE001 - best-effort terminate
            logger.exception("Failed to force-terminate PID %d", pid)
            return False

    def _cleanup(self) -> None:
        """Remove PID file and update status on shutdown."""
        logger.info(
            "Executor daemon shutting down after %d tick(s)",
            self._ticks_completed,
        )
        self.status_file.write(
            pid=os.getpid(),
            state="stopped",
            started_at=self._started_at,
            ticks_completed=self._ticks_completed,
        )
        self.pid_file.remove()
        self._clear_stop_request()
        logger.info("Cleanup complete")


if __name__ == "__main__":
    raise SystemExit(main())
