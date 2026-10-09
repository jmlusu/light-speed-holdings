"""Tests for the Studio Scorecard v1 collector (T2 #418).

Honesty-first: empty stores and unratified figures must yield ``no_data``,
never fabricated values. The collector must never raise.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import yaml

from ai_company.dashboard.kpis import ALL_COLLECTORS, collect_all_kpis
from ai_company.dashboard.kpis.studio import StudioScorecardCollector
from ai_company.models import Task


@pytest.fixture(autouse=True)
def _state_store_at_project_root(tmp_path: Path) -> None:
    import ai_company.dashboard.api as dash_api
    from ai_company.dashboard.repository import configure_state_store, reset_state_store

    reset_state_store()
    configure_state_store(tmp_path)
    dash_api._bus = None
    yield
    dash_api._bus = None
    reset_state_store()


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    (tmp_path / ".opencode").mkdir()
    (tmp_path / "orchestrator").mkdir()
    (tmp_path / "orchestrator" / "escalation.yaml").write_text(
        yaml.dump({"events": []}), encoding="utf-8"
    )
    (tmp_path / "orchestrator" / "cost_tracker.json").write_text(
        json.dumps({"total_budget": 100.0, "total_spent": 10.0, "llm_spend": 10.0}),
        encoding="utf-8",
    )
    (tmp_path / "orchestrator" / "approvals.yaml").write_text(
        yaml.dump({"requests": []}), encoding="utf-8"
    )
    (tmp_path / "company").mkdir()
    return tmp_path


def _write_inbox(root: Path, tasks: list[dict[str, Any]]) -> None:
    (root / ".opencode" / "inbox.json").write_text(json.dumps(tasks), encoding="utf-8")


def _write_tracker(root: Path, tracker: dict[str, Any]) -> None:
    (root / "company" / "studio_tracker.yaml").write_text(
        yaml.dump(tracker), encoding="utf-8"
    )


def _base_tracker() -> dict[str, Any]:
    return {
        "instrumentation_start": "2026-10-07",
        "baseline_days": 30,
        "ventures": {},
        "cfo": {"ratified": False},
    }


def _stub_audit(monkeypatch: pytest.MonkeyPatch, events: list[Any]) -> None:
    import ai_company.audit.reader as reader_mod

    class _StubReader:
        def read_all(self) -> list[Any]:
            return list(events)

    monkeypatch.setattr(reader_mod, "AuditReader", _StubReader)


def _audit_event(event_type: str, timestamp: str, decision: str = "") -> Any:
    from ai_company.audit.events import AuditEvent, AuditEventType

    meta = {"decision": decision} if decision else {}
    return AuditEvent(
        event_type=AuditEventType(event_type),
        agent_id="a",
        task_id="t",
        timestamp=timestamp,
        metadata=meta,
    )


# ---------------------------------------------------------------------------
# Empty / honesty states
# ---------------------------------------------------------------------------


def test_empty_store_yields_no_data_not_zeros(
    project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _write_tracker(project, _base_tracker())
    _stub_audit(monkeypatch, [])
    snap = StudioScorecardCollector(project_root=project).collect()

    assert snap["department"] == "studio"
    assert snap["kpis"]["atc_rate"]["current"] is None
    assert snap["kpis"]["atc_rate"]["status"] == "no_data"
    assert snap["kpis"]["capital_efficiency"]["current"] is None
    assert "unratified" in (snap["kpis"]["capital_efficiency"]["error"] or "")
    assert snap["baseline"]["active"] is True
    for venture in snap["ventures"].values():
        assert venture["velocity_days"]["status"] == "no_data"


def test_collector_never_raises_on_missing_files(tmp_path: Path) -> None:
    snap = StudioScorecardCollector(project_root=tmp_path).collect()
    assert snap["department"] == "studio"
    assert snap["kpis"]["atc_rate"]["status"] == "no_data"


# ---------------------------------------------------------------------------
# ATC math + denominator rule
# ---------------------------------------------------------------------------


def test_atc_denominator_rule(
    project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _write_tracker(project, _base_tracker())
    _stub_audit(monkeypatch, [])
    _write_inbox(
        project,
        [
            {"id": "c1", "status": "completed", "venture_id": "venture-a"},
            {"id": "c2", "status": "completed", "venture_id": "venture-a",
             "manual_intervention": True},  # forced completion = failure
            {"id": "f1", "status": "failed", "venture_id": "venture-a"},
            {"id": "p1", "status": "pending", "venture_id": "venture-a"},
        ],
    )
    snap = StudioScorecardCollector(project_root=project).collect()

    atc = snap["kpis"]["atc_rate"]
    assert atc["current"] == pytest.approx(100.0 / 3, abs=0.05)  # pending excluded
    assert atc["band"] == "block_scale"
    assert snap["ventures"]["venture-a"]["atc"] == atc["current"]
    assert snap["ventures"]["venture-a"]["task_count"] == 3


# ---------------------------------------------------------------------------
# Velocity
# ---------------------------------------------------------------------------


def test_velocity_requires_gate_review(
    project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tracker = _base_tracker()
    tracker["ventures"] = {
        "venture-a": {
            "name": "Enterprise Agent",
            "thesis_approved": "2026-08-01",
            "deploy": "2026-09-24",
            "gate_reviewed_by": "",
            "gate_reviewed_at": "",
            "pauses": [],
        }
    }
    _write_tracker(project, tracker)
    _stub_audit(monkeypatch, [])
    snap = StudioScorecardCollector(project_root=project).collect()
    assert snap["ventures"]["venture-a"]["velocity_days"]["status"] == "no_data"


def test_velocity_net_of_pauses(
    project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tracker = _base_tracker()
    tracker["ventures"] = {
        "venture-a": {
            "name": "Enterprise Agent",
            "thesis_approved": "2026-08-01",
            "deploy": "2026-09-24",  # 54 gross days
            "gate_reviewed_by": "coo",
            "gate_reviewed_at": "2026-09-25",
            "pauses": [{"reason": "customer wait", "from": "2026-08-10", "to": "2026-08-20"}],
        }
    }
    _write_tracker(project, tracker)
    _stub_audit(monkeypatch, [])
    snap = StudioScorecardCollector(project_root=project).collect()
    vel = snap["ventures"]["venture-a"]["velocity_days"]
    assert vel["current"] == 44
    assert vel["status"] == "on_track"


# ---------------------------------------------------------------------------
# Correction ratio (stubbed audit trail)
# ---------------------------------------------------------------------------


def test_correction_ratio_measurement_only(
    project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _write_tracker(project, _base_tracker())
    now = "2026-10-07T12:00:00+00:00"
    events = [_audit_event("tool_call", now) for _ in range(10)]
    events.append(_audit_event("hitl_denied", now))
    _stub_audit(monkeypatch, events)
    snap = StudioScorecardCollector(project_root=project).collect()

    corr = snap["kpis"]["correction_per_1k"]
    assert corr["current"] == pytest.approx(100.0)
    assert corr["status"] == "info"
    assert corr["baseline"] == "measurement_only"


# ---------------------------------------------------------------------------
# Capital efficiency (ratified only)
# ---------------------------------------------------------------------------


def test_capital_withheld_until_ratified(
    project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tracker = _base_tracker()
    tracker["cfo"] = {"ratified": False, "contracted_arr_usd": 50000.0}
    tracker["ventures"] = {"venture-a": {"capital_consumed_usd": 10000.0}}
    _write_tracker(project, tracker)
    _stub_audit(monkeypatch, [])
    snap = StudioScorecardCollector(project_root=project).collect()
    assert snap["kpis"]["capital_efficiency"]["current"] is None


def test_capital_ratio_when_ratified(
    project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tracker = _base_tracker()
    tracker["cfo"] = {
        "ratified": True,
        "contracted_arr_usd": 30000.0,
        "verified_cost_avoidance_usd": 4000.0,
    }
    tracker["ventures"] = {"venture-a": {"capital_consumed_usd": 10000.0}}
    _write_tracker(project, tracker)
    _stub_audit(monkeypatch, [])
    snap = StudioScorecardCollector(project_root=project).collect()
    assert snap["kpis"]["capital_efficiency"]["current"] == pytest.approx(3.4)


# ---------------------------------------------------------------------------
# Model / registration additive checks
# ---------------------------------------------------------------------------


def test_task_model_backward_compatible() -> None:
    legacy = {"id": "x", "status": "pending"}
    t = Task(**legacy)
    assert t.venture_id == "studio-core"
    assert t.manual_intervention is False
    assert t.cost_usd == 0.0
    stamped = Task(id="y", status="completed", venture_id="venture-b",
                   model_id="m", cost_usd=0.5, manual_intervention=True)
    assert stamped.model_dump()["venture_id"] == "venture-b"


def test_studio_collector_registered(project: Path) -> None:
    assert StudioScorecardCollector in ALL_COLLECTORS
    _write_tracker(project, _base_tracker())
    snap = collect_all_kpis(project_root=project)
    assert "studio" in snap["departments"]
