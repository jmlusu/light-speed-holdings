"""Regression tests for approval matrix integrity.

A rework of ``config/decision/approval_matrix.yaml`` dropped roughly twenty
action gates (agent lifecycle, data operations, security, board, compliance,
financial) and duplicated the spend/data-access/security entries three times
each. These tests fail loudly if gates disappear or duplicates return.
"""

from __future__ import annotations

from pathlib import Path

import yaml

MATRIX_PATH = Path(__file__).parents[2] / "config" / "decision" / "approval_matrix.yaml"
REQUIRED_KEYS = {"action", "risk_level", "required_approvals", "sla_hours", "auto_approve"}
CRITICAL_GATES = {
    "deploy_to_production",
    "hire_executive",
    "security_exception",
    "agent_creation",
    "agent_deletion",
    "agent_modification",
    "model_provider_change",
    "data_export",
    "data_deletion",
    "pii_access",
    "backup_restore",
    "vulnerability_disclosure",
    "incident_response_activation",
    "board_vote",
    "gdpr_request",
    "budget_reallocation",
    "contract_signing",
    "vendor_payment_over_threshold",
    "client_onboarding_offer_b",
    "client_onboarding_offer_c",
    "client_data_processing",
    "donor_data_handling",
    "local_model_deletion",
}


def _entries() -> list[dict]:
    with MATRIX_PATH.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return data["approval_matrix"]


def test_every_entry_has_required_keys() -> None:
    for entry in _entries():
        missing = REQUIRED_KEYS - set(entry)
        assert not missing, f"{entry.get('action')} missing keys: {sorted(missing)}"


def test_action_names_are_unique() -> None:
    actions = [entry["action"] for entry in _entries()]
    duplicates = sorted({a for a in actions if actions.count(a) > 1})
    assert not duplicates, f"duplicate approval actions: {duplicates}"


def test_critical_gates_are_present() -> None:
    actions = {entry["action"] for entry in _entries()}
    missing = CRITICAL_GATES - actions
    assert not missing, f"dropped approval gates: {sorted(missing)}"


def test_blocked_offers_stay_blocked_until_ratified() -> None:
    by_action = {entry["action"]: entry for entry in _entries()}
    assert by_action["client_onboarding_offer_b"]["blocked_until"] == "board_ratified_governance"
    assert by_action["client_onboarding_offer_c"]["blocked_until"] == "board_ratified_governance"


def test_no_auto_approve_for_critical_actions() -> None:
    # Incident response must activate immediately; every other critical
    # action requires human sign-off.
    exceptions = {"incident_response_activation"}
    for entry in _entries():
        if entry["risk_level"] == "critical" and entry["action"] not in exceptions:
            assert entry["auto_approve"] is False, (
                f"{entry['action']} auto-approves a critical action"
            )


def test_risk_levels_are_valid() -> None:
    valid = {"low", "medium", "high", "critical"}
    for entry in _entries():
        assert entry["risk_level"] in valid, f"{entry['action']} has invalid risk level"


def test_required_approvals_reference_known_roles() -> None:
    known = {
        "human-ceo",
        "board-chair",
        "cto",
        "ciso",
        "cfo",
        "coo",
        "clo",
        "cmo",
        "cpo",
        "cdo",
        "data-privacy-officer",
        "peer_review",
    }
    for entry in _entries():
        unknown = set(entry["required_approvals"]) - known
        assert not unknown, f"{entry['action']} references unknown approvers: {sorted(unknown)}"
