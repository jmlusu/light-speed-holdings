"""Durable storage for CEO Alert Center alerts.

The :class:`AlertEngine` (in :mod:`ai_company.dashboard.analytics`) evaluates
threshold rules against a KPI snapshot but is intentionally stateless — it
returns fired alerts and forgets them.  :class:`AlertStore` adds the durable,
queried, lifecycle-managed layer so the dashboard can show a persistent Alert
Center with acknowledge / snooze / clear semantics.

Alerts are stored as a JSON list via :class:`ai_company.store.file_store.FileStore`
under the dashboard data root (``<state base>/dashboard/alerts.json``), matching
the existing KPI-history storage convention (SQLite-first mirror is retired).

Lifecycle states::

    active -> acknowledged | snoozed -> cleared

A ``snoozed`` alert carries a ``snoozed_until`` timestamp and is treated as
suppressed (dedupe ignores it from new fires) until that time.  Cleared and
acknowledged entries older than :data:`RETENTION_DAYS` are pruned on each write.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from ai_company.dashboard.analytics import Alert, AlertRule
from ai_company.dashboard.repository import get_state_store
from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)

RETENTION_DAYS = 30
STATUS_ACTIVE = "active"
STATUS_ACKNOWLEDGED = "acknowledged"
STATUS_SNOOZED = "snoozed"
STATUS_CLEARED = "cleared"
_VALID_STATUSES = frozenset({STATUS_ACTIVE, STATUS_ACKNOWLEDGED, STATUS_SNOOZED, STATUS_CLEARED})

_ALERTS_REL = Path("alerts.json")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class AlertStore:
    """Persist and manage fired alerts with a simple lifecycle.

    Parameters
    ----------
    base_dir:
        Root directory for the alert data file.  Defaults to the configured
        :class:`StateStore` base (so tests anchored at a temp root never write
        into the real project), mirroring ``KPIHistoryStore``.
    """

    def __init__(self, base_dir: Path | None = None) -> None:
        if base_dir is None:
            base_dir = Path(get_state_store().base_dir) / "dashboard"
        self._dir = base_dir
        self._dir.mkdir(parents=True, exist_ok=True)
        self._store = FileStore(self._dir, backup=False)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add(self, alerts: list[Alert] | list[dict[str, Any]]) -> list[str]:
        """Persist fired alerts, skipping duplicates that are active/snoozed.

        A new alert is skipped when an identical
        ``(rule_name, department, kpi_key, severity)`` row is already
        ``active`` or is ``snoozed`` with a ``snoozed_until`` in the future
        (time-boxed re-fire suppression).

        Returns the ``id``s of alerts actually added.
        """
        if not alerts:
            return []
        existing = self._read()
        by_key = {
            self._identity(a): a
            for a in existing
            if a.get("status") in (STATUS_ACTIVE, STATUS_SNOOZED)
        }
        now = datetime.now(timezone.utc)
        added: list[str] = []
        for raw in alerts:
            a = self._to_dict(raw)
            ident = self._identity(a)
            prior = by_key.get(ident)
            if prior is not None:
                # Suppress while an identical active/snoozed row exists.
                if prior.get("status") == STATUS_ACTIVE:
                    continue
                until = self._parse_ts(prior.get("snoozed_until"))
                if until is not None and until > now:
                    continue
            # Otherwise upsert: clear/snooze-expire the prior row and add a new one.
            if prior is not None:
                prior["status"] = STATUS_CLEARED
                prior["updated_at"] = _now_iso()
            a["id"] = str(uuid.uuid4())
            a["fired_at"] = a.get("fired_at") or _now_iso()
            a["status"] = STATUS_ACTIVE
            a["updated_at"] = _now_iso()
            existing.append(a)
            by_key[ident] = a
            added.append(a["id"])
        self._write_pruned(existing)
        return added

    def list_alerts(
        self,
        status: str | None = None,
        severity: str | None = None,
        limit: int = 200,
    ) -> list[dict[str, Any]]:
        """Return alerts newest-first, optionally filtered.

        ``snoozed`` alerts whose ``snoozed_until`` has passed are surfaced as
        ``active`` again (a lazy, write-free re-activation for read paths).
        """
        rows = self._read()
        if severity:
            rows = [a for a in rows if a.get("severity") == severity]
        if status:
            rows = [a for a in rows if self._matches_status(a, status)]
        rows.sort(key=lambda a: a.get("fired_at", ""), reverse=True)
        return rows[:limit]

    def acknowledge(self, alert_id: str) -> dict[str, Any] | None:
        """Mark an alert acknowledged. Returns the updated row, or ``None``."""
        return self._transition(alert_id, STATUS_ACKNOWLEDGED)

    def snooze(self, alert_id: str, until_hours: int = 4) -> dict[str, Any] | None:
        """Snooze an alert for ``until_hours``. Returns the updated row."""
        rows = self._read()
        for row in rows:
            if row.get("id") != alert_id:
                continue
            row["status"] = STATUS_SNOOZED
            row["snoozed_until"] = (
                datetime.now(timezone.utc) + timedelta(hours=until_hours)
            ).isoformat()
            row["updated_at"] = _now_iso()
            self._write_pruned(rows)
            return row
        return None

    def clear(self, alert_id: str) -> dict[str, Any] | None:
        """Clear an alert. Returns the updated row, or ``None``."""
        return self._transition(alert_id, STATUS_CLEARED)

    def clear_all(self, severity: str | None = None) -> int:
        """Clear all alerts (optionally only a given severity). Returns count."""
        rows = self._read()
        changed = 0
        for a in rows:
            if severity and a.get("severity") != severity:
                continue
            if a.get("status") != STATUS_CLEARED:
                a["status"] = STATUS_CLEARED
                a["updated_at"] = _now_iso()
                changed += 1
        if changed:
            self._write_pruned(rows)
        return changed

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _read(self) -> list[dict[str, Any]]:
        try:
            return [dict(a) for a in self._store.read_json_list(_ALERTS_REL)]
        except FileNotFoundError:
            return []

    def _write_pruned(self, rows: list[dict[str, Any]]) -> None:
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=RETENTION_DAYS)
        kept: list[dict[str, Any]] = []
        for a in rows:
            ts = self._parse_ts(a.get("fired_at"))
            if ts is None:
                kept.append(a)
                continue
            # Retain active/snoozed regardless of age; prune terminal rows older
            # than the retention window.
            if a.get("status") in (STATUS_ACTIVE, STATUS_SNOOZED) or ts >= cutoff:
                kept.append(a)
        self._store.write_json(_ALERTS_REL, kept)

    def _transition(self, alert_id: str, new_status: str) -> dict[str, Any] | None:
        rows = self._read()
        for row in rows:
            if row.get("id") != alert_id:
                continue
            if row.get("status") == new_status:
                return None
            row["status"] = new_status
            row["updated_at"] = _now_iso()
            self._write_pruned(rows)
            return row
        return None

    @staticmethod
    def _identity(a: dict[str, Any]) -> tuple[str, str, str, str]:
        return (
            str(a.get("rule_name", "")),
            str(a.get("department", "")),
            str(a.get("kpi_key", "")),
            str(a.get("severity", "")),
        )

    @staticmethod
    def _resolve_status(a: dict[str, Any]) -> dict[str, Any]:
        if a.get("status") == STATUS_SNOOZED:
            until = AlertStore._parse_ts(a.get("snoozed_until"))
            if until is not None and until <= datetime.now(timezone.utc):
                a["status"] = STATUS_ACTIVE
                a["snoozed_until"] = None
        return a

    @classmethod
    def _matches_status(cls, a: dict[str, Any], status: str) -> bool:
        resolved = cls._resolve_status(dict(a))
        return resolved.get("status") == status

    @staticmethod
    def _parse_ts(value: Any) -> datetime | None:
        if not value:
            return None
        try:
            parsed = datetime.fromisoformat(str(value))
        except (TypeError, ValueError):
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed

    @classmethod
    def _to_dict(cls, raw: Alert | dict[str, Any]) -> dict[str, Any]:
        if isinstance(raw, Alert):
            return {
                "rule_name": raw.rule_name,
                "department": raw.department,
                "kpi_key": raw.kpi_key,
                "current_value": raw.current_value,
                "threshold": raw.threshold,
                "operator": raw.operator,
                "severity": raw.severity,
                "fired_at": raw.fired_at,
                "message": raw.message,
                "status": STATUS_ACTIVE,
                "snoozed_until": None,
            }
        return dict(raw)


def default_alert_rules() -> list[AlertRule]:
    """Return the canonical 7 default alert rules.

    Centralised here (moved out of ``api.py``) so both the direct evaluator
    and the background scheduler share one source of truth.
    """
    return [
        AlertRule(
            name="High failure rate",
            department="*",
            kpi_key="failure_rate",
            operator="gt",
            threshold=10.0,
            severity="critical",
        ),
        AlertRule(
            name="High failure rate warning",
            department="*",
            kpi_key="failure_rate",
            operator="gt",
            threshold=5.0,
            severity="warning",
        ),
        AlertRule(
            name="Low task completion",
            department="*",
            kpi_key="task_completion_rate",
            operator="lt",
            threshold=80.0,
            severity="warning",
        ),
        AlertRule(
            name="Open escalations",
            department="*",
            kpi_key="open_escalations",
            operator="gt",
            threshold=3,
            severity="warning",
        ),
        AlertRule(
            name="Budget overage",
            department="finance",
            kpi_key="budget_utilization",
            operator="gt",
            threshold=95.0,
            severity="critical",
        ),
        AlertRule(
            name="Low customer satisfaction",
            department="customer_success",
            kpi_key="customer_satisfaction",
            operator="lt",
            threshold=7.0,
            severity="warning",
        ),
        AlertRule(
            name="Low compliance score",
            department="legal",
            kpi_key="compliance_score",
            operator="lt",
            threshold=90.0,
            severity="critical",
        ),
    ]
