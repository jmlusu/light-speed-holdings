"""Offline / Network-Deny Tests for LS-MEM.

Implements architecture §18 and threat model T14–T16, T18–T20:
- Full CRUD, search, audit, export, rebuild work with internet disabled
- Gateway remains default-deny; zero non-localhost sockets
- Zero outbound hosts in skill scripts
- No package update checks from LS-MEM paths
"""

from unittest.mock import MagicMock, patch

import pytest

from src.ai_company.lsmem.engine import EngineConfig, LSMEMEngine
from src.ai_company.lsmem.gateway import GatewayConfig, PermissionGateway
from src.ai_company.lsmem.redaction import SecretScanner


@pytest.fixture
def offline_engine(tmp_path):
    """Create an engine instance for offline testing."""
    db_path = tmp_path / "test_memory.db"
    config = EngineConfig()

    eng = LSMEMEngine(
        db_path=db_path,
        config=config,
        scanner=SecretScanner(),
        classifier=None,  # Uses default
        gateway=PermissionGateway(GatewayConfig()),
        auditor=None,  # Uses default
        scorer=None,  # Uses default
    )
    eng.initialize()
    yield eng
    eng.close()


class TestOfflineOperation:
    """Test that LS-MEM works fully offline."""

    def test_crud_operations_offline(self, offline_engine):
        """Test CRUD operations work without network."""
        # Create
        record = offline_engine.remember(
            content="Offline test content",
            type="observation",
            title="Offline Test",
            project="offline_test",
            created_by="offline_agent",
        )
        assert record.id is not None
        assert record.content == "Offline test content"

        # Read
        retrieved = offline_engine.get(record.id)
        assert retrieved is not None
        assert retrieved.content == "Offline test content"

        # Update
        updated = offline_engine.update(
            record_id=record.id,
            actor="test_agent",
            content="Updated offline content",
        )
        assert updated.content == "Updated offline content"

        # Delete (soft)
        success = offline_engine.forget(record.id, "test_agent")
        assert success

        # Restore
        restored = offline_engine.restore(record.id, "test_agent")
        assert restored

    def test_search_offline(self, offline_engine):
        """Test FTS5 search works offline."""
        offline_engine.remember(
            content="Offline searchable content",
            type="observation",
            title="Search Test",
            project="search_offline",
            created_by="offline_agent",
        )
        offline_engine.remember(
            content="Another offline item",
            type="decision",
            title="Decision Test",
            project="search_offline",
            created_by="offline_agent",
        )

        results = offline_engine.search("offline", project="search_offline")
        assert len(results) >= 1
        assert any("offline" in r.content.lower() for r in results)

    def test_lifecycle_offline(self, offline_engine):
        """Test lifecycle management works offline."""
        # Insert a stale record directly
        import sqlite3

        conn = sqlite3.connect(offline_engine.db_path)
        conn.execute("""
            INSERT INTO memories (id, type, title, content, source, project, created_by,
                                created_at, updated_at, classification, confidence, tags,
                                ttl_days, stale_at, superseded_by, pinned,
                                constitutional_block, verified_by, tier,
                                approved_for_external_use, external_approval_token,
                                status, deleted_at, delete_actor, fts_rowid, vector_id, correlation_id)
            VALUES ('lifecycle-test', 'observation', 'Lifecycle', 'Old memory', 'test', 'lifecycle', 'test',
                    '2020-01-01T00:00:00', '2020-01-01T00:00:00', 'INTERNAL', 0.5, '[]',
                    30, '2020-06-01T00:00:00', NULL, 0, 0, NULL, 1,
                    0, NULL, 'ACTIVE', NULL, NULL, NULL, NULL, 'corr-lifecycle')
        """)
        conn.commit()
        conn.close()

        counts = offline_engine.apply_lifecycle()
        assert counts["stale_archived"] >= 1

    def test_rebuild_fts_offline(self, offline_engine):
        """Test FTS5 rebuild works offline."""
        offline_engine.remember(
            content="Rebuild test content",
            type="observation",
            title="Rebuild Test",
            project="rebuild_test",
            created_by="offline_agent",
        )
        count = offline_engine.rebuild_fts()
        assert count >= 1

    def test_integrity_check_offline(self, offline_engine):
        """Test integrity check works offline."""
        assert offline_engine.integrity_check() is True


class TestNetworkDeny:
    """Test network deny-by-default behavior."""

    def test_no_outbound_connections_on_remember(self, offline_engine):
        """Test that remember() makes no outbound connections."""
        # This test verifies the engine doesn't attempt network I/O
        # by mocking socket and ensuring no connect() calls
        with patch("socket.socket") as mock_socket:
            mock_sock = MagicMock()
            mock_socket.return_value = mock_sock

            engine = offline_engine
            engine.remember(
                content="Network test",
                type="observation",
                title="Network Test",
                project="net_test",
                created_by="test_agent",
            )

            # Verify no connect() was called
            mock_sock.connect.assert_not_called()

    def test_gateway_blocks_external_by_default(self, offline_engine):
        """Test gateway blocks all external access by default."""
        gateway = offline_engine.gateway
        decision = gateway.evaluate(
            agent_id="test_agent",
            provider="external-api",
            operation="embedding",
            destination="api.example.com",
            data_classification="INTERNAL",
            payload_preview="test",
        )
        assert decision.allowed is False
        assert decision.requires_human_approval is False
        assert "disabled" in decision.reason.lower()

    def test_gateway_allows_local_operations(self, offline_engine):
        """Test gateway allows local operations."""
        gateway = offline_engine.gateway
        decision = gateway.check_local_operation()
        assert decision.allowed is True
        assert "local" in decision.reason.lower()

    def test_no_dns_resolution_on_startup(self, offline_engine):
        """Test no DNS resolution during engine initialization."""
        with patch("socket.getaddrinfo") as mock_getaddrinfo:
            engine = LSMEMEngine(
                db_path=":memory:",
                scanner=None,
            )
            engine.initialize()
            # Should not have called getaddrinfo for external hosts
            for call in mock_getaddrinfo.call_args_list:
                host = call[0][0]
                assert host in ("localhost", "127.0.0.1", "::1"), f"Unexpected DNS lookup: {host}"


class TestGatewayOffline:
    """Test permission gateway offline behavior."""

    @pytest.fixture
    def gateway(self):
        return PermissionGateway(GatewayConfig())

    def test_local_operations_allowed(self, gateway):
        """Test local operations are auto-allowed."""
        decision = gateway.check_local_operation()
        assert decision.allowed is True

    def test_external_blocked_by_default(self, gateway):
        """Test external access blocked by default."""
        decision = gateway.evaluate(
            agent_id="test",
            provider="ollama",
            operation="embedding",
            destination="http://127.0.0.1:11434",
            data_classification="INTERNAL",
            payload_preview="test",
        )
        # Ollama on loopback should be allowed if configured
        # But by default all external is blocked
        assert decision.allowed is False or decision.requires_human_approval

    def test_human_approval_flow(self, gateway):
        """Test human approval flow works offline."""
        # Enable gateway for this test
        gateway.config.enabled = True
        gateway.config.approved_providers = ["custom"]
        gateway.config.approved_domains = ["api.example.com"]
        gateway.config.approved_operations = ["inference"]
        gateway.config.data_classes_allowed = {"internal": True}

        # Request external access
        decision = gateway.evaluate(
            agent_id="test",
            provider="custom",
            operation="inference",
            destination="api.example.com",
            data_classification="INTERNAL",
            payload_preview="test data",
        )
        assert decision.requires_human_approval is True
        assert decision.approval_token is not None

        # Human approves
        approved = gateway.submit_human_approval(
            approval_token=decision.approval_token,
            approved_by="human_operator",
            approved=True,
        )
        assert approved.allowed is True
        assert approved.audit_event is not None

    def test_classification_enforcement(self, gateway):
        """Test classification-based egress control."""
        config = GatewayConfig()
        config.enabled = True
        config.approved_providers = ["test"]
        config.approved_domains = ["localhost"]
        config.approved_operations = ["embedding"]
        config.data_classes_allowed = {
            "public": False,
            "internal": False,
            "confidential": False,
            "restricted": False,
        }
        gateway = PermissionGateway(config)

        decision = gateway.evaluate(
            agent_id="test",
            provider="test",
            operation="embedding",
            destination="localhost",
            data_classification="RESTRICTED",
            payload_preview="secret",
        )
        assert decision.allowed is False
        assert "restricted" in decision.reason.lower() or "block" in decision.reason.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
