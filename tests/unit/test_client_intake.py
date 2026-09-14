"""Tests for the client intake governance gate flow.

Regression lock for issue #81: ``_check_gate_status`` must read the same bare
gate keys that ``set_gate`` writes (``contract``/``dpa``/``compliance``/
``security``).  The old implementation read suffixed keys
(``contract_signed``/``dpa_executed``/``compliance_review``/
``security_review``) that nothing wrote, so gates never appeared to pass and
engagement creation was blocked forever.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_company.services.client_intake import ClientIntakeService


@pytest.fixture(autouse=True)
def _anchor_data_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Anchor the shared data root so the default MessageBus and AuditWriter
    stay inside the per-test tmp dir instead of the real project directory."""
    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))


def _make_service(tmp_path: Path) -> ClientIntakeService:
    return ClientIntakeService(
        data_dir=str(tmp_path / "data"),
        memory_dir=str(tmp_path / "memory"),
    )


def test_set_gate_round_trip_is_detected_by_gate_status(tmp_path: Path) -> None:
    """Gates set through the public API must be visible to the gate status
    reader (single key vocabulary: bare gate names)."""
    svc = _make_service(tmp_path)
    for gate in svc.REQUIRED_GATES:
        result = svc.set_gate("client-1", gate, True, reviewer="test-reviewer")
        assert result.success, result.errors

    status = svc._check_gate_status("client-1")
    assert status == {"contract": True, "dpa": True, "compliance": True, "security": True}


def test_check_governance_gates_passes_once_all_gates_set(tmp_path: Path) -> None:
    """Once every required gate passes, governance clearance succeeds."""
    svc = _make_service(tmp_path)
    for gate in svc.REQUIRED_GATES:
        svc.set_gate("client-1", gate, True)

    result = svc.check_governance_gates("client-1")
    assert result.success, result.errors
    assert result.data is not None
    assert result.data["all_passed"] is True


def test_legacy_suffixed_gate_keys_are_ignored(tmp_path: Path) -> None:
    """Gate status must not consider the old suffixed key names."""
    svc = _make_service(tmp_path)
    svc._save_data(
        "governance_gates.yaml",
        {
            "gates": {
                "client-1": {
                    "contract_signed": True,
                    "dpa_executed": True,
                    "compliance_review": True,
                    "security_review": True,
                    "contract": False,
                    "dpa": False,
                    "compliance": False,
                    "security": False,
                }
            }
        },
    )

    status = svc._check_gate_status("client-1")
    assert status == {"contract": False, "dpa": False, "compliance": False, "security": False}


def test_missing_client_has_no_passed_gates(tmp_path: Path) -> None:
    """A client with no recorded gates reports all gates as failed."""
    svc = _make_service(tmp_path)
    status = svc._check_gate_status("unknown-client")
    assert status == {"contract": False, "dpa": False, "compliance": False, "security": False}
