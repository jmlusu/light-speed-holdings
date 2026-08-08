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

import json
import logging
import os
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from ai_company.logging_config import HumanFormatter, JSONFormatter
from ai_company.utils.logging import CorrelationFilter

logger = logging.getLogger(__name__)

# Default paths
DEFAULT_PID_DIR = Path("logs")
DEFAULT_LOG_DIR = Path("logs")
DEFAULT_HEALTH_FILE = Path("logs") / "executor-daemon.json"


class DaemonPIDFile:
    """Manages a PID file for daemon lifecycle tracking.

    The PID file contains the process ID of the running daemon and is used
    to prevent multiple daemon instances and to enable stop/status commands.
    """

    def __init__(self, pid_path: Path) -> None:
        self.pid_path = pid_path

    def write(self, pid: int | None = None) -> None:
        """Write the current (or given) PID to the file.

        Creates parent directories if they don't exist.
        """
        if pid is None:
            pid = os.getpid()
        self.pid_path.parent.mkdir(parents=True, exist_ok=True)
        self.pid_path.write_text(str(pid), encoding="utf-8")
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

        return psutil.pid_exists(pid)
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
        self.status_path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
        logger.debug("Health status written: %s", self.status_path)

    def read(self) -> dict[str, Any] | None:
        """Read daemon status from the JSON file. Returns None if missing."""
        if not self.status_path.exists():
            return None
        try:
            return json.loads(self.status_path.read_text(encoding="utf-8"))
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
                self._mark_stopped(pid)
                return False
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
        fh = logging.FileHandler(str(self.log_path), encoding="utf-8")
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
