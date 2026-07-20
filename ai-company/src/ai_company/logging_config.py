"""Structured logging configuration with correlation IDs and JSON output.

Usage:
    from ai_company.logging_config import setup_logging, get_logger, get_correlation_id

    setup_logging()
    logger = get_logger(__name__)
    logger.info("Task started", task_id="abc-123")
"""

from __future__ import annotations

import json
import logging
import os
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any

# ---------------------------------------------------------------------------
# Correlation ID — context-local, propagated across async boundaries
# ---------------------------------------------------------------------------

_correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")


def get_correlation_id() -> str:
    """Return the current correlation ID (auto-generates if empty)."""
    cid = _correlation_id.get()
    if not cid:
        cid = uuid.uuid4().hex[:12]
        _correlation_id.set(cid)
    return cid


def set_correlation_id(cid: str) -> None:
    """Set the correlation ID for the current context."""
    _correlation_id.set(cid)


def new_correlation_id() -> str:
    """Generate and set a new correlation ID. Returns the new ID."""
    cid = uuid.uuid4().hex[:12]
    _correlation_id.set(cid)
    return cid


# ---------------------------------------------------------------------------
# JSON Formatter
# ---------------------------------------------------------------------------


class JSONFormatter(logging.Formatter):
    """Emits each log record as a single JSON line with structured fields."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": get_correlation_id(),
        }

        # Include exception info if present
        if record.exc_info and record.exc_info[1] is not None:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Merge any extra structured fields attached via `extra=`
        standard_attrs = {
            "name", "msg", "args", "created", "filename", "funcName",
            "lineno", "levelname", "levelno", "pathname", "module",
            "exc_info", "exc_text", "stack_info", "thread", "threadName",
            "processName", "process", "msecs", "relativeCreated",
            "message", "taskName",
        }
        for key, value in record.__dict__.items():
            if key.startswith("_") or key in standard_attrs:
                continue
            if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                continue
            log_entry[key] = value

        return json.dumps(log_entry, default=str, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Human-Readable Formatter (for terminal / dev mode)
# ---------------------------------------------------------------------------


class HumanFormatter(logging.Formatter):
    """Compact colored format for terminal output."""

    COLORS = {
        "DEBUG": "\033[36m",     # cyan
        "INFO": "\033[32m",      # green
        "WARNING": "\033[33m",   # yellow
        "ERROR": "\033[31m",     # red
        "CRITICAL": "\033[1;31m",  # bold red
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, "")
        ts = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        cid = get_correlation_id()[:8]
        prefix = f"{color}{record.levelname:<8}{self.RESET} {ts} [{cid}] {record.name}"
        return f"{prefix}: {record.getMessage()}"


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------


def setup_logging(
    level: str | int = "INFO",
    json_mode: bool | None = None,
    log_file: str | None = None,
) -> None:
    """Configure the root logger for the ai_company package.

    Args:
        level: Minimum log level (name or int). Defaults to INFO.
        json_mode: True = JSON lines, False = human-readable, None = auto-detect
                   (JSON when AI_COMPANY_LOG_JSON=1 or stdout is not a TTY).
        log_file: Optional file path for a second JSON log stream.
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    # Auto-detect JSON mode
    if json_mode is None:
        env_json = os.environ.get("AI_COMPANY_LOG_JSON", "")
        if env_json in ("1", "true", "yes"):
            json_mode = True
        elif env_json in ("0", "false", "no"):
            json_mode = False
        else:
            # Default to JSON in non-TTY (Docker, CI), human in terminal
            json_mode = not _is_terminal()

    root = logging.getLogger("ai_company")
    root.setLevel(level)

    # Remove existing handlers to avoid duplicates on re-config
    root.handlers.clear()

    # Primary handler (stdout)
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(level)
    if json_mode:
        stdout_handler.setFormatter(JSONFormatter())
    else:
        stdout_handler.setFormatter(HumanFormatter())
    root.addHandler(stdout_handler)

    # Optional file handler (always JSON)
    if log_file:
        from pathlib import Path

        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(JSONFormatter())
        root.addHandler(file_handler)

    # Set the ai_company package logger to the same level
    logging.getLogger("ai_company").setLevel(level)


def _is_terminal() -> bool:
    """Check if stdout is a terminal (for formatter auto-detection)."""
    import sys
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


# ---------------------------------------------------------------------------
# Convenience
# ---------------------------------------------------------------------------


def get_logger(name: str) -> logging.Logger:
    """Get a child logger under the ai_company namespace."""
    return logging.getLogger(f"ai_company.{name}" if not name.startswith("ai_company") else name)
