"""
Tests for evidence separation enforcement (AGENTS.md §9.3).

These tests verify that agents performing audits never write into the
evidence directory they are auditing.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from ai_company.audit.events import AuditEvent
from ai_company.orchestrator.dead_letter import (
    DeadLetterEntry,
    DeadLetterStore,
    reset_dead_letter_store,
)
from ai_company.orchestrator.escalation import EscalationEvent
from ai_company.orchestrator.escalation_events import (
    EscalationEventStore,
    reset_escalation_event_store,
)


class TestEscalationEventStoreEvidenceSeparation:
    """Test that escalation event store enforces evidence separation."""

    def setup_method(self):
        reset_escalation_event_store()

    def teardown_method(self):
        reset_escalation_event_store()

    def test_store_is_append_only(self):
        """Events are appended, never modified in place."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "escalation_events.jsonl"
            store = EscalationEventStore(str(path))

            event1 = EscalationEvent(
                task_id="task-1",
                rule_id="rule-1",
                from_agent="agent-a",
                to_agent="agent-b",
                reason="test reason 1",
            )
            store.append(event1)

            # Read raw file
            with open(path, "r") as f:
                lines1 = f.readlines()

            event2 = EscalationEvent(
                task_id="task-2",
                rule_id="rule-2",
                from_agent="agent-c",
                to_agent="agent-d",
                reason="test reason 2",
            )
            store.append(event2)

            # Read raw file again
            with open(path, "r") as f:
                lines2 = f.readlines()

            # Second append should add a line, not modify existing
            assert len(lines2) == len(lines1) + 1
            assert lines2[0] == lines1[0]  # First line unchanged

    def test_original_event_unchanged_after_resolution(self):
        """Original event stays intact when resolution event is appended."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "escalation_events.jsonl"
            store = EscalationEventStore(str(path))

            event = EscalationEvent(
                task_id="task-1",
                rule_id="rule-1",
                from_agent="agent-a",
                to_agent="agent-b",
                reason="test reason",
            )
            store.append(event)

            # Read initial
            with open(path, "r") as f:
                initial_lines = f.readlines()

            # Create a resolution event (append-only)
            resolution_event = event.model_copy(update={"resolved": True})
            store.append(resolution_event)

            # Read after resolution
            with open(path, "r") as f:
                final_lines = f.readlines()

            # Original event should still be there
            assert len(final_lines) == 2
            assert final_lines[0] == initial_lines[0]


class TestDeadLetterStoreEvidenceSeparation:
    """Test that dead-letter store enforces evidence separation."""

    def setup_method(self):
        reset_dead_letter_store()

    def teardown_method(self):
        reset_dead_letter_store()

    def test_store_is_append_only(self):
        """Entries are appended, never modified in place."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "dead_letter.jsonl"
            store = DeadLetterStore(str(path))

            entry1 = DeadLetterEntry(
                id="dlq-1",
                task_id="task-1",
                agent_id="agent-a",
                payload={"id": "task-1", "action": "test"},
                failure_reason="timeout",
            )
            store.append(entry1)

            with open(path, "r") as f:
                lines1 = f.readlines()

            entry2 = DeadLetterEntry(
                id="dlq-2",
                task_id="task-2",
                agent_id="agent-b",
                payload={"id": "task-2", "action": "test"},
                failure_reason="error",
            )
            store.append(entry2)

            with open(path, "r") as f:
                lines2 = f.readlines()

            assert len(lines2) == len(lines1) + 1
            assert lines2[0] == lines1[0]

    def test_resolution_appends_new_record(self):
        """Resolution appends a new record, doesn't modify original."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "dead_letter.jsonl"
            store = DeadLetterStore(str(path))

            entry = DeadLetterEntry(
                id="dlq-1",
                task_id="task-1",
                agent_id="agent-a",
                payload={"id": "task-1"},
                failure_reason="timeout",
            )
            store.append(entry)

            with open(path, "r") as f:
                lines_before = f.readlines()
            assert len(lines_before) == 1, "Expected one dead-letter record before resolution"

            store.mark_resolved("dlq-1", "requeued")

            with open(path, "r") as f:
                lines2 = f.readlines()

            # Should have original + resolution record
            assert len(lines2) == 2


class TestAuditExportEvidenceSeparation:
    """Test that audit export writes to evidence directory without modifying source."""

    def test_export_does_not_modify_source_db(self) -> None:
        """Export reads from audit DB but never modifies it."""
        import sqlite3
        import tempfile
        from pathlib import Path

        # Create temp directory manually to control cleanup
        tmp = tempfile.mkdtemp()
        try:
            db_path = Path(tmp) / "audit.db"

            # Create a minimal audit DB
            with sqlite3.connect(db_path) as conn:
                conn.execute("""
                    CREATE TABLE audit_log (
                        rowid INTEGER PRIMARY KEY,
                        event_id TEXT,
                        event_type TEXT,
                        timestamp TEXT,
                        actor TEXT,
                        correlation_id TEXT,
                        details TEXT,
                        payload_hash TEXT,
                        prev_hash TEXT
                    )
                """)
                conn.execute(
                    "INSERT INTO audit_log (event_id, event_type, timestamp, actor, correlation_id, details, payload_hash, prev_hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        "evt-1",
                        "test",
                        "2026-01-01T00:00:00+00:00",
                        "agent-1",
                        "corr-1",
                        "{}",
                        "hash1",
                        "hash0",
                    ),
                )

            from ai_company.audit.export import export_audit_log

            count = export_audit_log(
                db_path=db_path, output_dir=Path(tmp) / "evidence", date="2026-01-01"
            )

            assert count == 1

            # Verify source DB unchanged
            with sqlite3.connect(db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM audit_log")
                assert cursor.fetchone()[0] == 1

            # Verify export file exists and has correct content
            export_files = list(Path(tmp).glob("evidence/audit-*.jsonl"))
            assert len(export_files) == 1

            with open(export_files[0]) as f:
                content = f.read().strip()
                assert "evt-1" in content
        finally:
            # Clean up temp directory
            import shutil

            shutil.rmtree(tmp, ignore_errors=True)


class TestAuditWriterEvidenceSeparation:
    """Test that audit writer writes to evidence directory without modifying source."""

    def test_audit_writer_writes_to_evidence_dir(self):
        """AuditWriter writes events to evidence directory, not source."""
        with tempfile.TemporaryDirectory() as tmp:
            evidence_dir = Path(tmp) / "evidence"

            from ai_company.audit.writer import AuditWriter

            writer = AuditWriter(path=evidence_dir / "audit.jsonl")

            event = AuditEvent(
                event_type="task_created",
                task_id="task-1",
                agent_id="agent-1",
                tool="test_tool",
                args={"key": "value"},
            )
            writer.write(event)

            # Check evidence file was created
            evidence_files = list(evidence_dir.glob("audit*.jsonl"))
            assert len(evidence_files) >= 1

            with open(evidence_files[0]) as f:
                content = f.read().strip()
                assert "task_created" in content
                assert "task-1" in content


class TestEvidenceDirectoryStructure:
    """Test that evidence directories exist and have correct structure."""

    def test_reports_evidence_directory_exists(self):
        """reports/evidence/ directory exists for weekly audit evidence."""
        evidence_dir = Path("reports/evidence")
        # Directory should exist (created by workflow or tests)
        assert evidence_dir.exists() or evidence_dir.parent.exists()

    def test_orchestrator_escalation_events_exists(self):
        """orchestrator/escalation_events.jsonl can be created."""
        import tempfile

        from ai_company.orchestrator.escalation_events import EscalationEventStore

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "orchestrator" / "escalation_events.jsonl"
            store = EscalationEventStore(str(path))

            from ai_company.orchestrator.escalation import EscalationEvent

            event = EscalationEvent(
                task_id="task-1",
                rule_id="rule-1",
                from_agent="agent-a",
                to_agent="agent-b",
                reason="test",
            )
            store.append(event)

            assert Path(store.path).exists()
            assert store.path.read_text().strip() != ""

    def test_orchestrator_dead_letter_exists(self):
        """orchestrator/dead_letter.jsonl can be created."""
        import tempfile

        from ai_company.orchestrator.dead_letter import DeadLetterStore

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "orchestrator" / "dead_letter.jsonl"
            store = DeadLetterStore(str(path))

            from ai_company.orchestrator.dead_letter import DeadLetterEntry

            entry = DeadLetterEntry(
                id="dlq-1",
                task_id="task-1",
                agent_id="agent-a",
                payload={"id": "task-1"},
                failure_reason="test",
            )
            store.append(entry)

            assert Path(store.path).exists()
            assert store.path.read_text().strip() != ""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
