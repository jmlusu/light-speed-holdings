"""Unit tests for the CEO Alert Center durable store.

Covers :class:`ai_company.dashboard.alert_store.AlertStore`: add/dedupe,
acknowledge/snooze/clear lifecycle, retention pruning, and expired-snooze
re-activation.  Uses an explicit temp base dir so tests never touch the real
project state.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from ai_company.dashboard.alert_store import AlertStore
from ai_company.dashboard.analytics import Alert


def _alert(**over: object) -> Alert:
    base: dict[str, object] = {
        "rule_name": "High failure rate",
        "department": "engineering",
        "kpi_key": "failure_rate",
        "current_value": 12.0,
        "threshold": 10.0,
        "operator": "gt",
        "severity": "critical",
        "fired_at": datetime.now(timezone.utc).isoformat(),
        "message": "[CRITICAL] High failure rate: engineering.failure_rate = 12.0",
    }
    base.update(over)
    return Alert(**base)  # type: ignore[arg-type]


def test_add_persists_and_assigns_id(tmp_path: Path) -> None:
    store = AlertStore(base_dir=tmp_path)
    ids = store.add([_alert()])
    assert len(ids) == 1
    rows = store.list_alerts()
    assert len(rows) == 1
    assert rows[0]["id"] == ids[0]
    assert rows[0]["status"] == "active"
    # Persisted to disk — survives a fresh store instance over the same dir.
    rows2 = AlertStore(base_dir=tmp_path).list_alerts()
    assert len(rows2) == 1


def test_dedupe_identical_active(tmp_path: Path) -> None:
    store = AlertStore(base_dir=tmp_path)
    store.add([_alert()])
    added = store.add([_alert()])
    assert added == []
    assert len(store.list_alerts()) == 1


def test_dedupe_respected_after_clear(tmp_path: Path) -> None:
    store = AlertStore(base_dir=tmp_path)
    ids = store.add([_alert()])
    store.clear(ids[0])
    # After clearing, a new identical fire is allowed.
    added = store.add([_alert()])
    assert len(added) == 1
    assert len(store.list_alerts()) == 2


def test_acknowledge_lifecycle(tmp_path: Path) -> None:
    store = AlertStore(base_dir=tmp_path)
    aid = store.add([_alert()])[0]
    store.acknowledge(aid)
    assert store.list_alerts(status="acknowledged")[0]["id"] == aid
    # Idempotent acknowledge returns None (already acknowledged).
    assert store.acknowledge(aid) is None


def test_snooze_sets_until_and_suppresses(tmp_path: Path) -> None:
    store = AlertStore(base_dir=tmp_path)
    aid = store.add([_alert()])[0]
    store.snooze(aid, until_hours=4)
    row = store.list_alerts(status="snoozed")[0]
    assert row["snoozed_until"]
    # While snoozed (future until), a new identical fire is suppressed.
    assert store.add([_alert()]) == []


def test_expired_snooze_reactivates_on_active_read(tmp_path: Path) -> None:
    store = AlertStore(base_dir=tmp_path)
    a = _alert()
    a.fired_at = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    aid = store.add([a])[0]
    past = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    store.snooze(aid, until_hours=0)
    # Force an already-expired snoozed_until by editing directly.
    rows = store.list_alerts()
    rows[0]["snoozed_until"] = past
    store._write_pruned(rows)
    active = store.list_alerts(status="active")
    assert active and active[0]["id"] == aid


def test_clear_and_clear_all(tmp_path: Path) -> None:
    store = AlertStore(base_dir=tmp_path)
    store.add([_alert(rule_name="r1")])
    store.add([_alert(rule_name="r2")])
    assert store.clear_all() == 2
    assert all(a["status"] == "cleared" for a in store.list_alerts())


def test_retention_prunes_old_cleared(tmp_path: Path) -> None:
    store = AlertStore(base_dir=tmp_path)
    old = _alert(rule_name="old")
    old.fired_at = (datetime.now(timezone.utc) - timedelta(days=60)).isoformat()
    aid = store.add([old])[0]
    store.add([_alert(rule_name="fresh")])
    # Clearing triggers a write, which prunes terminal rows older than retention.
    store.clear(aid)
    rows = store.list_alerts()
    names = {r["rule_name"] for r in rows}
    assert "old" not in names
    assert "fresh" in names


def test_unknown_id_returns_none(tmp_path: Path) -> None:
    store = AlertStore(base_dir=tmp_path)
    assert store.clear("nope") is None
    assert store.acknowledge("nope") is None
    assert store.snooze("nope") is None
