"""Structured logging with correlation IDs for AI Company Builder.

Provides a ``CorrelationFilter`` that injects a thread-safe correlation ID
into every log record, plus convenience helpers for setup and propagation.

Usage::

    from ai_company.utils.logging import (
        setup_correlated_logging,
        get_correlation_id,
        set_correlation_id,
        new_correlation_id,
    )

    setup_correlated_logging()
    logger = logging.getLogger("ai_company.executor.loop")
    logger.info("Processing task")  # record will include correlation_id
"""

from __future__ import annotations

import logging
import uuid
from contextvars import ContextVar

# ---------------------------------------------------------------------------
# Correlation ID — context-local, thread-safe, async-safe
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
# CorrelationFilter — injects correlation_id into every LogRecord
# ---------------------------------------------------------------------------


class CorrelationFilter(logging.Filter):
    """Logging filter that attaches ``correlation_id`` to every log record.

    The correlation ID is read from a ``ContextVar``, making it thread-safe
    and async-safe.  If no ID has been set yet, one is auto-generated.

    Install this filter on the root ``ai_company`` logger (or any logger)
    so that *all* downstream loggers inherit it::

        logger = logging.getLogger("ai_company")
        logger.addFilter(CorrelationFilter())
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Add correlation_id attribute to *record*.

        Always returns ``True`` — this filter enriches records but never
        suppresses them.
        """
        record.correlation_id = get_correlation_id()  # type: ignore[attr-defined]
        return True


# ---------------------------------------------------------------------------
# Setup helper
# ---------------------------------------------------------------------------


def setup_correlated_logging(
    level: int = logging.INFO,
    json_mode: bool | None = None,
    log_file: str | None = None,
) -> None:
    """Configure structured logging with correlation IDs for ``ai_company``.

    This is a convenience wrapper that installs a ``CorrelationFilter`` on the
    ``ai_company`` logger and configures appropriate formatters.

    Args:
        level: Minimum log level.
        json_mode: True for JSON lines, False for human-readable, None for auto.
        log_file: Optional file path for a second JSON log stream.
    """
    from ai_company.logging_config import setup_logging

    # Delegate to the existing setup which handles formatters and handlers
    setup_logging(level=level, json_mode=json_mode, log_file=log_file)

    # Install the CorrelationFilter on the ai_company root logger
    root = logging.getLogger("ai_company")
    if not any(isinstance(f, CorrelationFilter) for f in root.filters):
        root.addFilter(CorrelationFilter())
