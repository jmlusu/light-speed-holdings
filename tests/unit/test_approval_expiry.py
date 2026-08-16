"""Tests for the approval expiry sweep (Sprint 7).

Covers ``ApprovalGate.sweep_expired()``: expired pending requests transition
to ``EXPIRED`` and are persisted, live requests are untouched, empty gates
are safe, and the sweep is idempotent.  Also covers the single-request
:meth:`ApprovalGate.expire` helper.

All file I/O uses the ``tmp_path`` fixture for complete isolation.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from ai_company.orchestrator.approval import ApprovalGate, ApprovalStatus


@pytest.fixture()
def gate(tmp_path: Path) -> ApprovalGate:
    """ApprovalGate backed by an isolated tmp directory."""
    return ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))


def _backdate_expiry(gate: ApprovalGate, request_id: str, minutes: int = 5) -> None:
    """Force a request's expires_at into the past (no persistence)."""
    request = gate.get_request(request_id)
    assert request is not None
    request.expires_at = datetime.now(timezone.utc) - timedelta(minutes=minutes)  # use UTC per ticket #58 convention


# ═══════════════════════════════════════════════════════════════════════════════
# sweep_expired
# ═══════════════════════════════════════════════════════════════════════════════


class TestSweepExpired:
    def test_expired_pending_request_becomes_expired_and_persisted(self, tmp_path: Path) -> None:
        gate = ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))
        gate.request_approval("req-1", "task-1", "agent-a", "deploy", "Deploy")
        _backdate_expiry(gate, "req-1")

        count = gate.sweep_expired()

        assert count == 1
        req = gate.get_request("req-1")
        assert req is not None
        assert req.status == ApprovalStatus.EXPIRED
        assert req.responded_at is not None
        assert gate.get_pending_requests() == []

        # Persisted: a fresh gate over the same file sees EXPIRED.
        reloaded = ApprovalGate(config_path=str(tmp_path / "approvals.yaml"))
        req = reloaded.get_request("req-1")
        assert req is not None
        assert req.status == ApprovalStatus.EXPIRED

    def test_not_yet_expired_request_untouched(self, gate: ApprovalGate) -> None:
        gate.request_approval("req-1", "task-1", "agent-a", "deploy", "Deploy")

        assert gate.sweep_expired() == 0

        req = gate.get_request("req-1")
        assert req is not None
        assert req.status == ApprovalStatus.PENDING
        assert len(gate.get_pending_requests()) == 1

    def test_request_without_deadline_untouched(self, gate: ApprovalGate) -> None:
        gate.request_approval("req-1", "task-1", "agent-a", "deploy", "Deploy")
        gate.requests[0].expires_at = None

        assert gate.sweep_expired() == 0
        assert gate.get_request("req-1").status == ApprovalStatus.PENDING

    def test_no_requests_returns_zero(self, gate: ApprovalGate) -> None:
        assert gate.sweep_expired() == 0

    def test_already_decided_requests_untouched(self, gate: ApprovalGate) -> None:
        gate.request_approval("req-a", "t1", "a1", "deploy", "approved one")
        gate.approve("req-a", "human-1")
        gate.request_approval("req-r", "t2", "a2", "deploy", "rejected one")
        gate.reject("req-r", "human-2")
        # Backdate an approved request's expires_at — sweep must not touch it.
        approved = gate.get_request("req-a")
        assert approved is not None
        approved.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)

        assert gate.sweep_expired() == 0
        assert gate.get_request("req-a").status == ApprovalStatus.APPROVED
        assert gate.get_request("req-r").status == ApprovalStatus.REJECTED

    def test_sweep_is_idempotent(self, gate: ApprovalGate) -> None:
        gate.request_approval("req-1", "task-1", "agent-a", "deploy", "Deploy")
        _backdate_expiry(gate, "req-1")

        assert gate.sweep_expired() == 1
        # Second sweep finds nothing left to expire.
        assert gate.sweep_expired() == 0
        assert gate.get_request("req-1").status == ApprovalStatus.EXPIRED

    def test_sweep_expires_only_expired_of_mixed_batch(self, gate: ApprovalGate) -> None:
        gate.request_approval("r-old", "t1", "a1", "deploy", "old")
        gate.request_approval("r-new", "t2", "a2", "deploy", "new")
        _backdate_expiry(gate, "r-old")

        assert gate.sweep_expired() == 1
        assert gate.get_request("r-old").status == ApprovalStatus.EXPIRED
        assert gate.get_request("r-new").status == ApprovalStatus.PENDING

    def test_multiple_expired_requests_all_swept(self, gate: ApprovalGate) -> None:
        gate.request_approval("r1", "t1", "a1", "deploy", "one")
        gate.request_approval("r2", "t2", "a2", "deploy", "two")
        _backdate_expiry(gate, "r1")
        _backdate_expiry(gate, "r2")

        assert gate.sweep_expired() == 2
        assert gate.get_request("r1").status == ApprovalStatus.EXPIRED
        assert gate.get_request("r2").status == ApprovalStatus.EXPIRED


# ═══════════════════════════════════════════════════════════════════════════════
# expire (single-request helper)
# ═══════════════════════════════════════════════════════════════════════════════


class TestExpireHelper:
    def test_expire_single_request(self, gate: ApprovalGate) -> None:
        gate.request_approval("req-1", "task-1", "agent-a", "deploy", "Deploy")
        _backdate_expiry(gate, "req-1")

        assert gate.expire("req-1") is True
        assert gate.get_request("req-1").status == ApprovalStatus.EXPIRED

    def test_expire_not_yet_expired_returns_false(self, gate: ApprovalGate) -> None:
        gate.request_approval("req-1", "task-1", "agent-a", "deploy", "Deploy")

        assert gate.expire("req-1") is False
        assert gate.get_request("req-1").status == ApprovalStatus.PENDING

    def test_expire_unknown_request_returns_false(self, gate: ApprovalGate) -> None:
        assert gate.expire("unknown") is False

    def test_expire_approved_request_returns_false(self, gate: ApprovalGate) -> None:
        gate.request_approval("req-1", "task-1", "agent-a", "deploy", "Deploy")
        gate.approve("req-1", "human-1")

        assert gate.expire("req-1") is False
        assert gate.get_request("req-1").status == ApprovalStatus.APPROVED

    def test_expire_request_without_deadline_returns_false(self, gate: ApprovalGate) -> None:
        gate.request_approval("req-1", "task-1", "agent-a", "deploy", "Deploy")
        gate.requests[0].expires_at = None

        assert gate.expire("req-1") is False
        assert gate.get_request("req-1").status == ApprovalStatus.PENDING
