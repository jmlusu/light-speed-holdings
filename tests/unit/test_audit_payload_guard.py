"""Unit tests for audit payload bounds and the writer event counter.

Regression tests for ticket #71: a tool_call event that greps a binary file
previously stored a ~300 KB mojibake blob in the canonical trail. Every
string and collection in an event payload must be bounded before it is
serialized, and the writer must expose an event counter so the executor can
smoke-check trail growth.
"""

from __future__ import annotations

import json

from ai_company.audit.events import AuditEvent
from ai_company.audit.writer import (
    _TRUNCATION_MARKER,
    DEFAULT_MAX_COLLECTION_ITEMS,
    DEFAULT_MAX_STRING_CHARS,
    AuditWriter,
    _sanitize_for_audit,
)


class TestSanitizeForAudit:
    def test_short_strings_pass_through(self) -> None:
        assert _sanitize_for_audit("hello") == "hello"

    def test_long_strings_are_truncated(self) -> None:
        raw = "x" * (DEFAULT_MAX_STRING_CHARS + 500)
        sanitized = _sanitize_for_audit(raw)
        assert isinstance(sanitized, str)
        assert len(sanitized) == DEFAULT_MAX_STRING_CHARS + len(_TRUNCATION_MARKER)
        assert sanitized.endswith(_TRUNCATION_MARKER)
        assert sanitized.startswith("x" * DEFAULT_MAX_STRING_CHARS)

    def test_bytes_are_replaced_with_size_placeholder(self) -> None:
        assert _sanitize_for_audit(b"\x00\x01\x02") == "<audit:bytes len=3>"

    def test_oversized_dict_is_capped(self) -> None:
        raw = {f"k{i}": i for i in range(DEFAULT_MAX_COLLECTION_ITEMS + 10)}
        sanitized = _sanitize_for_audit(raw)
        assert isinstance(sanitized, dict)
        assert len(sanitized) == DEFAULT_MAX_COLLECTION_ITEMS + 1  # + truncation key
        assert "..." in sanitized
        assert "10 more items" in sanitized["..."]

    def test_oversized_list_is_capped(self) -> None:
        raw = list(range(DEFAULT_MAX_COLLECTION_ITEMS + 25))
        sanitized = _sanitize_for_audit(raw)
        assert isinstance(sanitized, list)
        assert len(sanitized) == DEFAULT_MAX_COLLECTION_ITEMS + 1  # + truncation marker
        assert "25 more items" in sanitized[-1]

    def test_nested_payload_is_bounded_recursively(self) -> None:
        raw = {
            "matches": [{"line": "y" * 50_000, "meta": {"blob": b"z" * 123}}],
            "ok": True,
        }
        sanitized = _sanitize_for_audit(raw)
        match = sanitized["matches"][0]
        assert len(match["line"]) == DEFAULT_MAX_STRING_CHARS + len(_TRUNCATION_MARKER)
        assert match["meta"]["blob"] == "<audit:bytes len=123>"
        assert sanitized["ok"] is True

    def test_unknown_objects_fall_back_to_bounded_repr(self) -> None:
        class _Weird:
            pass

        sanitized = _sanitize_for_audit(_Weird())
        assert isinstance(sanitized, str)
        assert len(sanitized) <= DEFAULT_MAX_STRING_CHARS + len(_TRUNCATION_MARKER)


class TestAuditWriterPayloadBounds:
    def test_write_batch_bounds_oversized_tool_result(self, tmp_path) -> None:
        writer = AuditWriter(tmp_path / "audit")
        writer.write_batch(
            [
                AuditEvent(
                    event_type="tool_call",
                    agent_id="test-agent",
                    task_id="task-big",
                    tool="grep",
                    args={"pattern": "error", "path": "data/ai_company.db"},
                    result={"matches": [{"line": "y" * 200_000, "blob": b"z" * 4096}]},
                )
            ]
        )

        raw = (tmp_path / "audit").read_text(encoding="utf-8")
        line = raw.strip().splitlines()[-1]
        parsed = json.loads(line)
        assert parsed["event_type"] == "tool_call"
        match = parsed["result"]["matches"][0]
        assert len(match["line"]) == DEFAULT_MAX_STRING_CHARS + len(_TRUNCATION_MARKER)
        assert match["blob"] == "<audit:bytes len=4096>"
        # The whole line must stay small even though the raw payload was ~204 KB.
        assert len(line) < 16 * 1024

    def test_write_batch_increments_events_written(self, tmp_path) -> None:
        writer = AuditWriter(tmp_path / "audit")
        assert writer.events_written == 0
        writer.write_batch([AuditEvent(event_type="tool_call", agent_id="a")])
        writer.write_batch(
            [
                AuditEvent(event_type="task_created", agent_id="a"),
                AuditEvent(event_type="task_completed", agent_id="a"),
            ]
        )
        assert writer.events_written == 3

    def test_empty_batch_does_not_increment_counter(self, tmp_path) -> None:
        writer = AuditWriter(tmp_path / "audit")
        writer.write_batch([])
        assert writer.events_written == 0
