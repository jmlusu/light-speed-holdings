"""Tests for tamper-evident audit trail chaining (C1)."""

from __future__ import annotations

import json
from pathlib import Path

from ai_company.audit.events import AuditEvent, AuditEventType
from ai_company.audit.integrity import verify_audit_chain
from ai_company.audit.writer import _ZERO_HASH, AuditWriter


def _event(agent: str = "test-agent", **overrides: object) -> AuditEvent:
    defaults: dict[str, object] = {
        "event_type": AuditEventType.TOOL_CALL,
        "agent_id": agent,
        "task_id": "task-001",
        "tool": "bash",
        "args": {"cmd": "ls"},
    }
    defaults.update(overrides)
    return AuditEvent(**defaults)  # type: ignore[arg-type]


class TestAuditChainWrites:
    """Verify writer injects chain fields and chains lines."""

    def test_lines_carry_seq_and_prev_hash(self, tmp_path: Path) -> None:
        log_file = tmp_path / "audit.jsonl"
        writer = AuditWriter(path=log_file)
        writer.write_batch([_event(task_id="a"), _event(task_id="b"), _event(task_id="c")])

        with open(log_file, encoding="utf-8") as fh:
            lines = fh.readlines()  # keeps trailing newlines, matching the chain hash
        assert len(lines) == 3
        line_data = [json.loads(line) for line in lines]
        assert [d["__seq"] for d in line_data] == [1, 2, 3]
        assert line_data[0]["__prev_hash"] == _ZERO_HASH
        # Each subsequent line references the hash of the previous raw line.
        from hashlib import sha256

        assert line_data[1]["__prev_hash"] == sha256(lines[0].encode("utf-8")).hexdigest()
        assert line_data[2]["__prev_hash"] == sha256(lines[1].encode("utf-8")).hexdigest()

    def test_reader_ignores_chain_fields(self, tmp_path: Path) -> None:
        """Chain fields must not leak into parsed AuditEvent objects."""
        log_file = tmp_path / "audit.jsonl"
        AuditWriter(path=log_file).write(_event())
        from ai_company.audit.reader import AuditReader

        events = AuditReader(path=log_file).read_all()
        assert len(events) == 1
        assert not hasattr(events[0], "__seq")
        assert not hasattr(events[0], "__prev_hash")

    def test_append_from_new_writer_continues_chain(self, tmp_path: Path) -> None:
        """A second writer instance must chain off the on-disk tail."""
        log_file = tmp_path / "audit.jsonl"
        AuditWriter(path=log_file).write(_event(task_id="first"))
        AuditWriter(path=log_file).write(_event(task_id="second"))

        from ai_company.audit.reader import AuditReader

        assert len(AuditReader(path=log_file).read_all()) == 2
        result = verify_audit_chain(log_file)
        assert result["ok"], result["errors"]


class TestAuditChainVerify:
    """Verify chain detection of tampering."""

    def test_intact_chain_passes(self, tmp_path: Path) -> None:
        log_file = tmp_path / "audit.jsonl"
        AuditWriter(path=log_file).write_batch([_event(task_id=f"t-{i}") for i in range(10)])
        result = verify_audit_chain(log_file)
        assert result["ok"] is True
        assert result["events"] == 10
        assert result["errors"] == []

    def test_modified_field_detected(self, tmp_path: Path) -> None:
        log_file = tmp_path / "audit.jsonl"
        AuditWriter(path=log_file).write_batch(
            [_event(task_id="t-1"), _event(task_id="t-2"), _event(task_id="t-3")]
        )
        # Tamper: change a field in the middle line without updating the chain.
        lines = log_file.read_text(encoding="utf-8").splitlines()
        data = json.loads(lines[1])
        data["task_id"] = "t-999"
        lines[1] = json.dumps(data, ensure_ascii=False)
        log_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

        result = verify_audit_chain(log_file)
        assert result["ok"] is False
        assert any("chain break" in e for e in result["errors"]), result["errors"]

    def test_removed_line_detected(self, tmp_path: Path) -> None:
        log_file = tmp_path / "audit.jsonl"
        AuditWriter(path=log_file).write_batch(
            [_event(task_id="t-1"), _event(task_id="t-2"), _event(task_id="t-3")]
        )
        # Delete the line with __seq == 2.
        lines = log_file.read_text(encoding="utf-8").splitlines()
        kept = [ln for ln in lines if json.loads(ln)["__seq"] != 2]
        log_file.write_text("\n".join(kept) + "\n", encoding="utf-8")

        result = verify_audit_chain(log_file)
        assert result["ok"] is False
        assert any("seq mismatch" in e or "chain break" in e for e in result["errors"])

    def test_empty_and_missing_trails_pass(self, tmp_path: Path) -> None:
        assert verify_audit_chain(tmp_path / "nope.jsonl")["ok"] is True
        empty = tmp_path / "empty.jsonl"
        empty.touch()
        assert verify_audit_chain(empty)["ok"] is True
        assert verify_audit_chain(empty)["events"] == 0


class TestAuditChainRotation:
    """Verify the chain stays verifiable across rotation."""

    def test_chain_valid_across_rotation(self, tmp_path: Path) -> None:
        log_file = tmp_path / "audit.jsonl"
        writer = AuditWriter(path=log_file, max_bytes=200, keep_files=3)
        for i in range(40):
            writer.write(_event(task_id=f"rot-{i}"))

        # Multiple rotations should have occurred.
        assert len(writer.list_rotated_files()) >= 1
        result = verify_audit_chain(log_file)
        assert result["ok"] is True, result["errors"]
        # Every retained event should be counted.
        assert result["events"] >= 3
        assert len(result["files"]) >= 2

    def test_rotated_away_head_is_tolerated(self, tmp_path: Path) -> None:
        """The oldest retained line (seq > 1) must not produce a false break."""
        log_file = tmp_path / "audit.jsonl"
        writer = AuditWriter(path=log_file, max_bytes=150, keep_files=1)
        for i in range(12):
            writer.write(_event(task_id=f"t-{i}"))

        result = verify_audit_chain(log_file)
        assert result["ok"] is True, result["errors"]
        # The oldest retained file should no longer start at seq 1.
        first_events = json.loads(result["files"][0] and _first_line(Path(result["files"][0])))
        assert first_events["__seq"] > 1 or result["events"] < 12


def _first_line(path: Path) -> str:
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                return line
    raise AssertionError("empty file")
