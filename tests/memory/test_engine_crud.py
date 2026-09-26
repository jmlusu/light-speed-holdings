"""Integration tests for LS-MEM Engine CRUD operations."""

import shutil
import tempfile
from pathlib import Path

import pytest

from src.ai_company.lsmem.audit import AuditLogger
from src.ai_company.lsmem.classification import ClassificationLayer
from src.ai_company.lsmem.engine import EngineConfig, LSMEMEngine
from src.ai_company.lsmem.gateway import GatewayConfig, PermissionGateway
from src.ai_company.lsmem.redaction import SecretScanner

# Split so raw file content never matches GitHub Push Protection patterns.
FAKE_STRIPE_KEY = "sk_live_" + "abcdefghijklmnopqrstuvwxyz123456"


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test database."""
    d = Path(tempfile.mkdtemp())
    yield d
    shutil.rmtree(d, ignore_errors=True)


@pytest.fixture
def engine(temp_dir):
    """Create a test engine instance."""
    db_path = temp_dir / "test_memory.db"
    config = EngineConfig()
    scanner = SecretScanner()
    classifier = ClassificationLayer()
    gateway = PermissionGateway(GatewayConfig())

    audit_db = temp_dir / "audit" / "audit.db"
    auditor = AuditLogger(audit_db, retention_days_crud=1, retention_days_gateway=1)

    eng = LSMEMEngine(
        db_path=db_path,
        config=config,
        scanner=scanner,
        classifier=classifier,
        gateway=gateway,
        auditor=auditor,
    )
    eng.initialize()
    yield eng
    eng.close()


class TestEngineCRUD:
    """Test basic CRUD operations."""

    def test_remember_basic(self, engine):
        """Test basic memory storage."""
        record = engine.remember(
            content="This is a test observation",
            type="observation",
            title="Test Observation",
            project="test_project",
            created_by="test_agent",
            classification="INTERNAL",
            confidence=0.8,
            tags=["test", "observation"],
        )

        assert record.id is not None
        assert record.type == "observation"
        assert record.title == "Test Observation"
        assert record.content == "This is a test observation"
        assert record.classification == "INTERNAL"
        assert record.tier >= 1
        assert record.status == "ACTIVE"

    def test_remember_with_secret(self, engine):
        """Test that secrets are redacted on store."""
        record = engine.remember(
            content=f"My API key is {FAKE_STRIPE_KEY}",
            type="observation",
            title="Secret Test",
            project="test_project",
            created_by="test_agent",
            classification="INTERNAL",
            confidence=0.9,
        )

        assert "[REDACTED_SECRET]" in record.content
        assert FAKE_STRIPE_KEY not in record.content
        assert record.classification == "RESTRICTED"

    def test_get_memory(self, engine):
        """Test retrieving a memory by ID."""
        record = engine.remember(
            content="Test content for retrieval",
            type="decision",
            title="Decision Test",
            project="test_project",
            created_by="test_agent",
        )

        retrieved = engine.get(record.id)
        assert retrieved is not None
        assert retrieved.id == record.id
        assert retrieved.content == "Test content for retrieval"

    def test_get_nonexistent(self, engine):
        """Test getting non-existent memory returns None."""
        result = engine.get("non-existent-id")
        assert result is None

    def test_search_basic(self, engine):
        """Test FTS5 search."""
        engine.remember(
            content="The quick brown fox jumps over the lazy dog",
            type="observation",
            title="Fox Observation",
            project="search_test",
            created_by="test_agent",
        )
        engine.remember(
            content="A slow red turtle walks on the beach",
            type="observation",
            title="Turtle Observation",
            project="search_test",
            created_by="test_agent",
        )

        results = engine.search("fox", project="search_test")
        assert len(results) >= 1
        assert any("fox" in r.content.lower() for r in results)

        results = engine.search("turtle", project="search_test")
        assert len(results) >= 1

    def test_search_filter_by_classification(self, engine):
        """Test search excludes RESTRICTED by default."""
        engine.remember(
            content="Public info",
            type="observation",
            title="Public",
            project="class_test",
            created_by="test_agent",
            classification="PUBLIC",
        )
        engine.remember(
            content=f"Secret info {FAKE_STRIPE_KEY}",
            type="observation",
            title="Restricted",
            project="class_test",
            created_by="test_agent",
            classification="INTERNAL",  # Will be upgraded to RESTRICTED
        )

        results = engine.search("info", project="class_test")
        # RESTRICTED should be excluded from search results
        assert all(r.classification != "RESTRICTED" for r in results)

    def test_update_memory(self, engine):
        """Test updating a memory."""
        import time

        record = engine.remember(
            content="Original content",
            type="observation",
            title="Update Test",
            project="update_test",
            created_by="test_agent",
        )
        time.sleep(0.02)  # Windows clock granularity (~15ms) can alias create/update timestamps

        updated = engine.update(
            record_id=record.id,
            actor="test_agent",
            content="Updated content",
            title="Updated Title",
        )

        assert updated is not None
        assert updated.content == "Updated content"
        assert updated.title == "Updated Title"
        assert updated.updated_at != record.updated_at

    def test_supersede(self, engine):
        """Test superseding a memory with newer version."""
        original = engine.remember(
            content="Version 1",
            type="decision",
            title="Decision v1",
            project="supersede_test",
            created_by="test_agent",
        )

        new_record = engine.remember(
            content="Version 2 - improved",
            type="decision",
            title="Decision v2",
            project="supersede_test",
            created_by="test_agent",
        )

        # Supersede old with new
        success = engine.supersede(original.id, "test_agent", new_record.id)
        assert success

        original_updated = engine.get(original.id)
        assert original_updated.status == "SUPERSEDED"
        assert original_updated.superseded_by == new_record.id

    def test_pin_unpin(self, engine):
        """Test pinning and unpinning memories."""
        record = engine.remember(
            content="Important memory",
            type="architecture",
            title="Architecture Decision",
            project="pin_test",
            created_by="test_agent",
        )

        # Pin
        success = engine.pin(record.id, "test_agent", pinned=True)
        assert success
        pinned = engine.get(record.id)
        assert pinned.pinned is True

        # Unpin
        success = engine.pin(record.id, "test_agent", pinned=False)
        assert success
        unpinned = engine.get(record.id)
        assert unpinned.pinned is False

    def test_verify_tier3(self, engine):
        """Test promoting to Tier 3 (human verified)."""
        record = engine.remember(
            content="Human verified fact",
            type="lesson",
            title="Verified Lesson",
            project="verify_test",
            created_by="test_agent",
        )

        success = engine.verify(record.id, "human_reviewer", verified=True)
        assert success
        verified = engine.get(record.id)
        assert verified.tier == 3
        assert verified.verified_by is not None
        assert "human_reviewer" in verified.verified_by


class TestEngineDeletion:
    """Test deletion operations."""

    def test_forget_soft_delete(self, engine):
        """Test soft delete (forget)."""
        record = engine.remember(
            content="To be forgotten",
            type="task",
            title="Forget Test",
            project="delete_test",
            created_by="test_agent",
        )

        success = engine.forget(record.id, "test_agent")
        assert success

        forgotten = engine.get(record.id)
        assert forgotten.status == "ARCHIVED"
        assert forgotten.deleted_at is not None
        assert forgotten.delete_actor == "test_agent"

    def test_purge_hard_delete(self, engine):
        """Test hard delete (purge)."""
        record = engine.remember(
            content="To be purged",
            type="task",
            title="Purge Test",
            project="purge_test",
            created_by="test_agent",
        )

        success = engine.purge(record.id, "test_agent", confirm=True)
        assert success

        purged = engine.get(record.id)
        assert purged.status == "PURGED"

    def test_purge_requires_confirm(self, engine):
        """Test purge requires explicit confirmation."""
        record = engine.remember(
            content="Test",
            type="task",
            title="Purge Confirm Test",
            project="purge_confirm",
            created_by="test_agent",
        )

        with pytest.raises(ValueError, match="confirm"):
            engine.purge(record.id, "test_agent", confirm=False)

    def test_restore(self, engine):
        """Test restoring soft-deleted memory."""
        record = engine.remember(
            content="To be restored",
            type="task",
            title="Restore Test",
            project="restore_test",
            created_by="test_agent",
        )

        engine.forget(record.id, "test_agent")
        restored = engine.restore(record.id, "test_agent")
        assert restored

        restored_record = engine.get(record.id)
        assert restored_record.status == "ACTIVE"
        assert restored_record.deleted_at is None


class TestEngineLifecycle:
    """Test lifecycle management."""

    def test_apply_lifecycle(self, engine):
        """Test lifecycle rules (stale, expired)."""
        # Create a memory with past stale_at
        import sqlite3

        conn = sqlite3.connect(engine.db_path)
        conn.execute("""
            INSERT INTO memories (id, type, title, content, source, project, created_by,
                                created_at, updated_at, classification, confidence, tags,
                                ttl_days, stale_at, superseded_by, pinned,
                                constitutional_block, verified_by, tier,
                                approved_for_external_use, external_approval_token,
                                status, deleted_at, delete_actor, correlation_id)
            VALUES ('stale-test', 'observation', 'Stale', 'Old memory', 'test', 'lifecycle', 'test',
                    '2020-01-01T00:00:00', '2020-01-01T00:00:00', 'INTERNAL', 0.5, '[]',
                    30, '2020-06-01T00:00:00', NULL, 0, 0, NULL, 1,
                    0, NULL, 'ACTIVE', NULL, NULL, 'corr-1')
        """)
        conn.commit()
        conn.close()

        counts = engine.apply_lifecycle()
        assert counts["stale_archived"] >= 1

        stale = engine.get("stale-test")
        assert stale.status == "ARCHIVED"


class TestEngineSearch:
    """Test search functionality."""

    def test_search_by_correlation(self, engine):
        """Test searching by correlation ID."""
        # Create multiple memories with same correlation_id
        corr_id = "test-correlation-123"
        for i in range(3):
            engine.remember(
                content=f"Memory {i}",
                type="observation",
                title=f"Corr Test {i}",
                project="corr_test",
                created_by="test_agent",
                correlation_id=corr_id,
            )

        results = engine.search_by_correlation(corr_id)
        assert len(results) == 3


class TestEngineStatus:
    """Test engine status reporting."""

    def test_status(self, engine):
        """Test engine status reporting."""
        engine.remember(
            content="Test 1", type="observation", title="T1", project="status_test", created_by="a"
        )
        engine.remember(
            content="Test 2", type="decision", title="T2", project="status_test", created_by="b"
        )
        engine.remember(
            content="Test 3", type="task", title="T3", project="status_test", created_by="c"
        )

        status = engine.status()
        assert status["total"] >= 3
        assert status["active"] >= 3
        assert "by_type" in status
        assert "by_classification" in status
        assert "by_tier" in status
        assert status["integrity_ok"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
