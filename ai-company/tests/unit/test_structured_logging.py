"""Tests for PRE-08: Structured Logging — no print() in non-CLI modules.

Verifies that non-CLI modules under ai_company use logger instead of print(),
and that the structured logging infrastructure (JSON formatter, correlation IDs)
is properly configured.
"""

from __future__ import annotations

import logging



class TestStructuredLogging:
    """PRE-08: Verify structured logging infrastructure and print() removal."""

    def test_no_print_in_executor_loop(self) -> None:
        """executor/loop.py should not contain bare print() calls."""
        from pathlib import Path

        loop_file = Path(__file__).parents[2] / "src" / "ai_company" / "executor" / "loop.py"
        content = loop_file.read_text(encoding="utf-8")

        # Strip comments and strings to find bare print() calls
        lines = content.split("\n")
        bare_prints = []
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # Skip comments
            if stripped.startswith("#"):
                continue
            # Skip lines inside strings (approximate check)
            if '"""' in stripped or "'''" in stripped:
                continue
            if stripped.startswith("print("):
                bare_prints.append(i)

        assert bare_prints == [], f"Found print() calls on lines: {bare_prints}"

    def test_executor_loop_uses_logger(self) -> None:
        """executor/loop.py should import and use logger."""
        from pathlib import Path

        loop_file = Path(__file__).parents[2] / "src" / "ai_company" / "executor" / "loop.py"
        content = loop_file.read_text(encoding="utf-8")

        assert "import logging" in content
        assert 'logger = logging.getLogger(__name__)' in content
        assert "logger.info(" in content

    def test_logging_config_provides_json_formatter(self) -> None:
        """logging_config.JSONFormatter should produce valid JSON log lines."""
        from ai_company.logging_config import JSONFormatter

        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="test.py",
            lineno=1, msg="Test message %s", args=("arg1",),
            exc_info=None,
        )
        output = formatter.format(record)

        import json
        parsed = json.loads(output)
        assert parsed["level"] == "INFO"
        assert parsed["message"] == "Test message arg1"
        assert "ts" in parsed
        assert "correlation_id" in parsed

    def test_correlation_id_auto_generates(self) -> None:
        """get_correlation_id() should auto-generate an ID if none is set."""
        from ai_company.utils.logging import get_correlation_id, set_correlation_id

        # Reset to empty
        set_correlation_id("")
        cid = get_correlation_id()
        assert len(cid) == 12  # hex[:12]
        # Second call returns the same ID
        assert get_correlation_id() == cid

    def test_new_correlation_id_changes(self) -> None:
        """new_correlation_id() should generate a different ID."""
        from ai_company.utils.logging import get_correlation_id, new_correlation_id

        old = get_correlation_id()
        new = new_correlation_id()
        assert new != old
        assert get_correlation_id() == new

    def test_human_formatter_produces_output(self) -> None:
        """HumanFormatter should produce readable output."""
        from ai_company.logging_config import HumanFormatter

        formatter = HumanFormatter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="test.py",
            lineno=1, msg="Hello world", args=(),
            exc_info=None,
        )
        output = formatter.format(record)
        assert "INFO" in output
        assert "Hello world" in output
