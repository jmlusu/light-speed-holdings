"""Unit tests for ClientIntakeService."""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_company.models.task import TaskPriority
from ai_company.orchestrator.message_bus import MessageBus
from ai_company.services.client_intake import ClientIntakeService, GovernanceGateError


@pytest.fixture()
def custom_bus(tmp_path: Path) -> MessageBus:
    inbox = tmp_path / "inbox.json"
    return MessageBus(storage_path=str(inbox))


@pytest.fixture()
def intake_service(tmp_path: Path, custom_bus: MessageBus) -> ClientIntakeService:
    service = ClientIntakeService(data_dir=tmp_path / "data", bus=custom_bus)
    return service


class TestClientIntakeService:
    def test_create_client_success(self, intake_service: ClientIntakeService) -> None:
        result = intake_service.create_client(
            client_id="ngo_hope",
            client_name="Project Hope",
            client_type="ngo",
            contact_email="director@hope.org",
            currency="USD",
        )
        assert result.success is True
        assert result.data["id"] == "ngo_hope"
        assert result.data["governance_gates_passed"] is False

        # Duplicate ID should fail
        dup = intake_service.create_client(
            client_id="ngo_hope",
            client_name="Duplicate Hope",
        )
        assert dup.success is False
        assert any("already exists" in e for e in dup.errors)

    def test_list_clients_and_filtering(self, intake_service: ClientIntakeService) -> None:
        intake_service.create_client("c1", "Client One", client_type="ngo")
        intake_service.create_client("c2", "Client Two", client_type="sme")

        all_clients = intake_service.list_clients()
        assert len(all_clients.data) == 2

        ngos = intake_service.list_clients(client_type="ngo")
        assert len(ngos.data) == 1
        assert ngos.data[0]["id"] == "c1"

    def test_set_and_check_governance_gates(self, intake_service: ClientIntakeService) -> None:
        intake_service.create_client("c1", "Client One")

        # Invalid gate
        invalid = intake_service.set_gate("c1", "invalid_gate", True)
        assert invalid.success is False

        # Check gates before setting
        status = intake_service.check_governance_gates("c1")
        assert status.success is False
        assert len(status.metadata["missing"]) == 4

        # Set all 4 gates
        for gate in ("contract", "dpa", "compliance", "security"):
            res = intake_service.set_gate("c1", gate, True, reviewer="auditor")
            assert res.success is True

        passed_status = intake_service.check_governance_gates("c1")
        assert passed_status.success is True
        assert passed_status.data["all_passed"] is True

    def test_create_engagement_blocked_offer(self, intake_service: ClientIntakeService) -> None:
        intake_service.create_client("c1", "Client One")
        with pytest.raises(GovernanceGateError, match="is BLOCKED"):
            intake_service.create_engagement(
                client_id="c1",
                offer_code="offer_b",
                description="Blocked engagement test",
            )

    def test_create_engagement_missing_gates(self, intake_service: ClientIntakeService) -> None:
        intake_service.create_client("c1", "Client One")
        with pytest.raises(GovernanceGateError, match="Governance gates not satisfied"):
            intake_service.create_engagement(
                client_id="c1",
                offer_code="offer_a",
                description="Unsatisfied gates",
            )

    def test_create_engagement_success_and_list(self, intake_service: ClientIntakeService) -> None:
        intake_service.create_client("c1", "Client One")
        for gate in ("contract", "dpa", "compliance", "security"):
            intake_service.set_gate("c1", gate, True, reviewer="lead")

        eng_res = intake_service.create_engagement(
            client_id="c1",
            offer_code="offer_a",
            description="Active digital strategy delivery",
            lead_agent="strategist",
            priority=TaskPriority.HIGH,
            contract="CTR-2026-001",
        )
        assert eng_res.success is True
        task = eng_res.data
        assert task.receiver_id == "strategist"
        assert "client_work" in task.tags

        engagements = intake_service.list_engagements()
        assert len(engagements.data) == 1
        assert engagements.data[0]["client"] == "c1"
        assert engagements.data[0]["offer"] == "offer_a"

    def test_get_summary(self, intake_service: ClientIntakeService) -> None:
        summary = intake_service.get_summary()
        assert "blocked_offers" in summary
        assert "offer_b" in summary["blocked_offers"]
