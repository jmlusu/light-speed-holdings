"""Validate company/narrative_outcomes.yaml — the clinic/NGO/Offer E instrumentation.

Run from repo root:
    uv run pytest tests/unit/test_narrative_outcomes.py
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from ai_company.services.client_intake import ClientIntakeService

BLOCKED_OFFERS = ClientIntakeService.BLOCKED_OFFERS

REPO_ROOT = Path(__file__).resolve().parents[2]
TRACKER_PATH = REPO_ROOT / "company" / "narrative_outcomes.yaml"

VALID_STATUSES = {"not_started", "pilot", "blocked", "shipped"}
EXPECTED_OUTCOMES = {"clinic_whatsapp", "ngo_donor_reporting", "offer_e_licensing"}


@pytest.fixture(scope="module")
def tracker() -> dict[str, Any]:
    """Load the narrative outcomes tracker YAML."""
    with open(TRACKER_PATH, encoding="utf-8") as f:
        data: dict[str, Any] = yaml.safe_load(f)
        return data


@pytest.fixture(scope="module")
def outcomes(tracker: dict[str, Any]) -> dict[str, Any]:
    """Return the outcomes mapping."""
    result: dict[str, Any] = tracker["outcomes"]
    return result


def test_top_level_structure(tracker: dict[str, Any]) -> None:
    """Tracker carries the instrumentation start date, rules, and outcomes."""
    assert tracker["instrumentation_start"]
    assert isinstance(tracker["rules"], list) and tracker["rules"]
    assert isinstance(tracker["outcomes"], dict)


def test_expected_pillars_present(outcomes: dict[str, Any]) -> None:
    """Exactly the three claimed outcome pillars are instrumented."""
    assert set(outcomes) == EXPECTED_OUTCOMES


def test_statuses_valid(outcomes: dict[str, Any]) -> None:
    """Every pillar uses the declared status enum."""
    for key, outcome in outcomes.items():
        assert outcome["status"] in VALID_STATUSES, f"{key}: {outcome['status']!r}"


def test_claim_sources_exist(outcomes: dict[str, Any]) -> None:
    """Each claim cites an existing repo file (path[:line] form)."""
    for key, outcome in outcomes.items():
        source = str(outcome["claim_source"])
        path_str = source.rsplit(":", 1)[0] if ":" in source else source
        path = REPO_ROOT / path_str
        assert path.exists(), f"{key}: claim_source not found: {path_str}"


def test_governance_refs_exist(outcomes: dict[str, Any]) -> None:
    """Every governance reference points at a real artifact."""
    for key, outcome in outcomes.items():
        for ref in outcome["governance_refs"]:
            assert (REPO_ROOT / ref).exists(), f"{key}: missing governance ref: {ref}"


def test_metrics_are_instrumented_without_fabricated_values(
    outcomes: dict[str, Any],
) -> None:
    """Each metric declares unit/source/formula and starts with current: null."""
    seen_ids: set[str] = set()
    for key, outcome in outcomes.items():
        metrics = outcome["metrics"]
        assert metrics, f"{key}: no metrics defined"
        for metric in metrics:
            assert metric["id"] not in seen_ids, f"duplicate metric id {metric['id']}"
            seen_ids.add(metric["id"])
            assert metric["name"]
            assert metric["unit"]
            assert metric["source"], f"{key}/{metric['id']}: missing source"
            assert metric["formula"], f"{key}/{metric['id']}: missing formula"
            assert metric["current"] is None, (
                f"{key}/{metric['id']}: current must stay null until a real source exists"
            )


def test_claim_gates_defined(outcomes: dict[str, Any]) -> None:
    """No pillar may be restated as fact until its claim_gate conditions exist."""
    for key, outcome in outcomes.items():
        gate = outcome["claim_gate"]
        assert gate, f"{key}: claim_gate empty"
        assert all(isinstance(item, str) and item.strip() for item in gate)


def test_status_consistent_with_runtime_offer_gates(outcomes: dict[str, Any]) -> None:
    """Blocked pillars match client_intake.BLOCKED_OFFERS; Offer E is not blocked."""
    assert (outcomes["clinic_whatsapp"]["status"] == "blocked") == ("offer_b" in BLOCKED_OFFERS), (
        "clinic_whatsapp status must mirror offer_b runtime gate"
    )
    assert (outcomes["ngo_donor_reporting"]["status"] == "blocked") == (
        "offer_c" in BLOCKED_OFFERS
    ), "ngo_donor_reporting status must mirror offer_c runtime gate"
    assert "offer_e" not in BLOCKED_OFFERS
    assert outcomes["offer_e_licensing"]["status"] != "blocked"
