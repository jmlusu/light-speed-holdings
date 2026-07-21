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
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        # Process exists but we don't have permission to signal it.
        return True


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
        self.status_path.write_text(
            json.dumps(data, indent=2, default=str), encoding="utf-8"
        )
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
    """

    def __init__(
        self,
        executor_factory: Callable[..., Any],
        poll_interval: float = 5.0,
        pid_path: Path | None = None,
        log_path: Path | None = None,
        status_path: Path | None = None,
        *,
        _clock: Callable[[], float] | None = None,
        _sleep: Callable[[float], None] | None = None,
    ) -> None:
        self.executor_factory = executor_factory
        self.poll_interval = poll_interval

        self.pid_file = DaemonPIDFile(
            pid_path or (DEFAULT_PID_DIR / "executor-daemon.pid")
        )
        self.status_file = DaemonHealthStatus(
            status_path or DEFAULT_HEALTH_FILE
        )
        self.log_path = log_path or (DEFAULT_LOG_DIR / "executor-daemon.log")

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

        # Write PID file
        pid = os.getpid()
        self.pid_file.write(pid)
        logger.info("Executor daemon starting (PID=%d)", pid)

        # Write initial status
        self._started_at = datetime.now(timezone.utc).isoformat()
        self.status_file.write(
            pid=pid,
            state="running",
            started_at=self._started_at,
        )

        # Install signal handlers
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

    def stop_daemon(self) -> bool:
        """Send SIGTERM to the daemon process recorded in the PID file.

        Returns:
            True if the signal was sent successfully, False otherwise.
        """
        pid = self.pid_file.read()
        if pid is None:
            return False

        if not _is_process_alive(pid):
            # Stale PID file — clean up
            self.pid_file.remove()
            self.status_file.write(pid=pid, state="stopped")
            return False

        try:
            os.kill(pid, signal.SIGTERM)
            logger.info("Sent SIGTERM to daemon PID %d", pid)
            return True
        except PermissionError:
            logger.error("No permission to signal PID %d", pid)
            return False
        except ProcessLookupError:
            self.pid_file.remove()
            return False

    @staticmethod
    def is_daemon_running(pid_path: Path | None = None) -> bool:
        """Check if a daemon instance is currently running."""
        pid_file = DaemonPIDFile(
            pid_path or (DEFAULT_PID_DIR / "executor-daemon.pid")
        )
        return pid_file.is_running()

    @staticmethod
    def get_daemon_status(
        status_path: Path | None = None,
    ) -> dict[str, Any] | None:
        """Read the daemon status file. Returns None if no daemon status exists."""
        sf = DaemonHealthStatus(
            status_path or DEFAULT_HEALTH_FILE
        )
        return sf.read()

    # ── Internal ─────────────────────────────────────────────────────

    def _run_loop(self) -> None:
        """Main polling loop — creates executor and calls tick() periodically."""
        executor = self.executor_factory()
        logger.info("Executor created; entering poll loop (interval=%.1fs)", self.poll_interval)

        while not self._shutdown_event:
            try:
                count = executor.tick()
                self._ticks_completed += 1
                logger.info(
                    "Tick #%d completed — processed %d task(s)",
                    self._ticks_completed, count,
                )
                self._update_status("running")
            except Exception:
                logger.exception("Error during tick")

            # Sleep in small increments so we can respond to signals quickly
            self._interruptible_sleep(self.poll_interval)

    def _interruptible_sleep(self, duration: float) -> None:
        """Sleep for *duration* seconds, checking the shutdown flag frequently."""
        end = self._clock() + duration
        while not self._shutdown_event and self._clock() < end:
            remaining = end - self._clock()
            chunk = min(remaining, 1.0)
            if chunk > 0:
                self._sleep(chunk)

    def _setup_logging(self) -> None:
        """Configure file + console logging for daemon mode."""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        # File handler
        fh = logging.FileHandler(str(self.log_path), encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fmt = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fh.setFormatter(fmt)
        root_logger.addHandler(fh)

        # Console handler (stderr)
        ch = logging.StreamHandler(sys.stderr)
        ch.setLevel(logging.INFO)
        ch.setFormatter(fmt)
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
        logger.info("Cleanup complete")
