"""Unit tests for structured logging with correlation IDs (GAP-018).

These tests verify the JSON/Human formatters, the shared correlation-ID
context, and that ``utils.logging`` and ``logging_config`` operate on the
same ``ContextVar`` so a correlation ID set during task execution is
emitted in every structured log record.
"""

from __future__ import annotations

import json
import logging

import pytest

from ai_company.logging_config import (
    HumanFormatter,
    JSONFormatter,
    get_correlation_id,
    get_logger,
    set_correlation_id,
    setup_logging,
)
from ai_company.utils.logging import (
    CorrelationFilter,
    new_correlation_id,
    setup_correlated_logging,
)


@pytest.fixture(autouse=True)
def _reset_correlation_id():
    """Reset the shared correlation-ID context before/after each test."""
    set_correlation_id("")
    yield
    set_correlation_id("")


def _make_record(
    msg: str = "hello",
    name: str = "ai_company.test.module",
    level: int = logging.INFO,
) -> logging.LogRecord:
    return logging.LogRecord(
        name=name,
        level=level,
        pathname=__file__,
        lineno=10,
        msg=msg,
        args=(),
        exc_info=None,
    )


class TestJSONFormatter:
    """JSON lines carry consistent structured fields."""

    def test_emits_structured_fields(self) -> None:
        out = json.loads(JSONFormatter().format(_make_record()))
        assert out["ts"]
        assert out["level"] == "INFO"
        assert out["logger"] == "ai_company.test.module"
        assert out["message"] == "hello"
        assert "correlation_id" in out

    def test_includes_correlation_id_from_context(self) -> None:
        set_correlation_id("task-abc-123")
        out = json.loads(JSONFormatter().format(_make_record()))
        assert out["correlation_id"] == "task-abc-123"

    def test_auto_generates_correlation_id_when_empty(self) -> None:
        out = json.loads(JSONFormatter().format(_make_record()))
        assert len(out["correlation_id"]) == 12

    def test_merges_extra_fields(self) -> None:
        record = _make_record()
        record.task_id = "task-42"  # type: ignore[attr-defined]
        out = json.loads(JSONFormatter().format(record))
        assert out["task_id"] == "task-42"

    def test_always_single_json_line(self) -> None:
        raw = JSONFormatter().format(_make_record())
        assert "\n" not in raw


class TestHumanFormatter:
    """Terminal formatter includes level, time, and correlation prefix."""

    def test_includes_level_and_correlation_prefix(self) -> None:
        set_correlation_id("abc12345def0")
        out = HumanFormatter().format(_make_record(msg="ready"))
        assert "INFO" in out
        assert "abc12345" in out
        assert "ready" in out


class TestCorrelationContext:
    """utils.logging and logging_config share one ContextVar (GAP-018)."""

    def test_set_via_utils_read_via_logging_config(self) -> None:
        from ai_company.utils.logging import set_correlation_id as utils_set

        utils_set("shared-cid")
        assert get_correlation_id() == "shared-cid"

    def test_new_correlation_id_generates_hex_and_sticks(self) -> None:
        cid = new_correlation_id()
        assert len(cid) == 12
        assert int(cid, 16) >= 0  # valid 12-char hex prefix
        assert get_correlation_id() == cid

    def test_get_auto_generates_once_per_context(self) -> None:
        first = get_correlation_id()
        assert first
        assert get_correlation_id() == first

    def test_correlation_filter_attaches_id(self) -> None:
        set_correlation_id("filter-cid")
        record = _make_record()
        assert CorrelationFilter().filter(record) is True
        assert record.correlation_id == "filter-cid"  # type: ignore[attr-defined]


class TestSetup:
    """setup_logging installs the expected handler/formatter."""

    def test_json_mode_installs_json_handler(self) -> None:
        setup_logging(level=logging.DEBUG, json_mode=True)
        handlers = logging.getLogger("ai_company").handlers
        assert any(isinstance(h.formatter, JSONFormatter) for h in handlers)
        logging.getLogger("ai_company").handlers.clear()

    def test_human_mode_installs_human_handler(self) -> None:
        setup_logging(level=logging.DEBUG, json_mode=False)
        handlers = logging.getLogger("ai_company").handlers
        assert any(isinstance(h.formatter, HumanFormatter) for h in handlers)
        logging.getLogger("ai_company").handlers.clear()

    def test_setup_correlated_logging_installs_filter(self) -> None:
        setup_correlated_logging(json_mode=True)
        root = logging.getLogger("ai_company")
        assert any(isinstance(f, CorrelationFilter) for f in root.filters)
        logging.getLogger("ai_company").handlers.clear()


class TestGetLogger:
    """get_logger returns children of the ai_company namespace."""

    def test_namespace_prefixed(self) -> None:
        assert get_logger("executor.loop").name == "ai_company.executor.loop"

    def test_no_double_prefix(self) -> None:
        assert get_logger("ai_company.executor.loop").name == "ai_company.executor.loop"
