"""LS-MEM audit chain-head tests: persisted head makes tail tampering detectable."""

import json
import shutil
import sqlite3
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from src.ai_company.lsmem.audit import AuditLogger


@pytest.fixture
def temp_dir():
    d = Path(tempfile.mkdtemp())
    yield d
    shutil.rmtree(d, ignore_errors=True)


class TestAuditChainHead:
    """Persisted chain head (architecture §10.1): verify_chain covers the final event."""

    @pytest.fixture
    def auditor(self, temp_dir):
        a = AuditLogger(temp_dir / "audit" / "audit.db")
        a.initialize()
        yield a
        a.close()

    def _log_n(self, auditor, n=3):
        for i in range(n):
            auditor.log(
                "memory_create",
                "test-agent",
                f"corr-{i}",
                {"step": i, "memory_id": f"mem-{i}"},
            )
            time.sleep(0.01)

    def _rows(self, auditor, sql, params=()):
        conn = sqlite3.connect(auditor.db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return rows

    def _row(self, auditor, sql, params=()):
        rows = self._rows(auditor, sql, params)
        return rows[0] if rows else None

    def _exec(self, auditor, sql, params=()):
        conn = sqlite3.connect(auditor.db_path)
        conn.execute(sql, params)
        conn.commit()
        conn.close()

    def test_valid_chain_passes(self, auditor):
        self._log_n(auditor, 3)
        assert auditor.verify_chain() is True

    def test_tail_tamper_details_detected(self, auditor):
        self._log_n(auditor, 3)
        last = self._row(auditor, "SELECT event_id FROM audit_log ORDER BY rowid DESC LIMIT 1")
        self._exec(
            auditor,
            "UPDATE audit_log SET details = ? WHERE event_id = ?",
            (json.dumps({"step": 99, "memory_id": "forged"}), last["event_id"]),
        )
        assert auditor.verify_chain() is False

    def test_tail_tamper_payload_hash_detected(self, auditor):
        self._log_n(auditor, 3)
        last = self._row(auditor, "SELECT event_id FROM audit_log ORDER BY rowid DESC LIMIT 1")
        self._exec(
            auditor,
            "UPDATE audit_log SET payload_hash = ? WHERE event_id = ?",
            ("sha256:" + "a" * 64, last["event_id"]),
        )
        assert auditor.verify_chain() is False

    def test_mid_chain_tamper_still_detected(self, auditor):
        self._log_n(auditor, 3)
        ids = [
            row["event_id"]
            for row in self._rows(auditor, "SELECT event_id FROM audit_log ORDER BY rowid ASC")
        ]
        self._exec(
            auditor,
            "UPDATE audit_log SET details = ? WHERE event_id = ?",
            (json.dumps({"step": 42, "memory_id": "forged-middle"}), ids[1]),
        )
        assert auditor.verify_chain() is False

    def test_legacy_db_without_meta_recovers(self, temp_dir):
        db = temp_dir / "audit" / "audit.db"
        first = AuditLogger(db)
        first.initialize()
        for i in range(2):
            first.log("memory_create", "test-agent", f"corr-{i}", {"step": i})
            time.sleep(0.01)
        first.close()

        conn = sqlite3.connect(db)
        conn.execute("DELETE FROM audit_meta")
        conn.commit()
        conn.close()

        second = AuditLogger(db)
        second.initialize()
        assert second.verify_chain() is True
        head = self._row(second, "SELECT value FROM audit_meta WHERE key = 'chain_head'")
        assert head is not None
        assert head["value"]
        second.close()

        third = AuditLogger(db)
        third.initialize()
        assert third.verify_chain() is True
        third.close()

    def test_head_persisted_after_log(self, auditor):
        self._log_n(auditor, 3)
        head = self._row(auditor, "SELECT value FROM audit_meta WHERE key = 'chain_head'")
        last = self._row(auditor, "SELECT * FROM audit_log ORDER BY rowid DESC LIMIT 1")
        assert head is not None
        assert head["value"]
        assert head["value"] == auditor._compute_event_hash(auditor._row_to_event(last))

    def test_prune_updates_head(self, temp_dir):
        auditor = AuditLogger(
            temp_dir / "audit" / "audit.db", retention_days_crud=1, retention_days_gateway=1
        )
        auditor.initialize()
        self._log_n(auditor, 3)

        changed = auditor.prune()
        assert isinstance(changed, int)
        assert auditor.verify_chain() is True

        head = self._row(auditor, "SELECT value FROM audit_meta WHERE key = 'chain_head'")
        last = self._row(auditor, "SELECT * FROM audit_log ORDER BY rowid DESC LIMIT 1")
        assert last is not None
        assert head is not None
        assert head["value"] == auditor._compute_event_hash(auditor._row_to_event(last))
        auditor.close()

    def test_prune_reanchors_after_leading_rows_deleted(self, temp_dir):
        auditor = AuditLogger(
            temp_dir / "audit" / "audit.db", retention_days_crud=1, retention_days_gateway=1
        )
        auditor.initialize()
        self._log_n(auditor, 3)
        ids = [
            row["event_id"]
            for row in self._rows(auditor, "SELECT event_id FROM audit_log ORDER BY rowid ASC")
        ]
        stale = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()
        for event_id in ids[1:]:
            self._exec(
                auditor, "UPDATE audit_log SET timestamp = ? WHERE event_id = ?", (stale, event_id)
            )

        auditor.prune()
        assert auditor.verify_chain() is True

        head = self._row(auditor, "SELECT value FROM audit_meta WHERE key = 'chain_head'")
        last = self._row(auditor, "SELECT * FROM audit_log ORDER BY rowid DESC LIMIT 1")
        assert last is not None
        assert last["event_id"] == ids[0]
        assert head is not None
        assert head["value"] == auditor._compute_event_hash(auditor._row_to_event(last))
        auditor.close()

    def test_prune_clears_head_when_no_rows_remain(self, temp_dir):
        auditor = AuditLogger(
            temp_dir / "audit" / "audit.db", retention_days_crud=0, retention_days_gateway=0
        )
        auditor.initialize()
        self._log_n(auditor, 2)

        auditor.prune()
        count = self._row(auditor, "SELECT COUNT(*) AS n FROM audit_log")
        head = self._row(auditor, "SELECT value FROM audit_meta WHERE key = 'chain_head'")
        assert count["n"] == 0
        assert head is None
        assert auditor.verify_chain() is True

        auditor.log("memory_create", "test-agent", "corr-after-prune", {"step": "fresh"})
        assert auditor.verify_chain() is True
        auditor.close()
