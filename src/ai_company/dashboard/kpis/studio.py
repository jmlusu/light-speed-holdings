"""Studio Scorecard v1 KPI collector (T2 #418, Wayfinder map #416).

Computes the blueprint four from live internal telemetry only:
ATC rate, velocity to MVP, manual correction ratio, capital efficiency —
plus per-venture portfolio cards and a risk strip.

Honesty contract (ADR-020/033, T1 scoreboard-v1):
- Every metric is evidenced, qualified, or ``no_data``. Nothing is fabricated:
  missing gate timestamps, unratified CFO figures, or an empty trail yield
  ``no_data`` with an explanatory error, never a zero dressed as a value.
- First 30 days after ``instrumentation_start`` are measurement-only: the
  correction ratio and capital efficiency report ``status: info`` with no
  target while the baseline accumulates.
- ATC denominator rule (T1 decision 1): ``tasks_entered`` = tasks in a
  terminal state (completed/failed/timeout/cancelled/escalated). Forced human
  completion (``manual_intervention=True``) counts as failure. Scheduled
  Tier-gate HITL approvals are governance, not failure, and never set the flag.
- Correction numerator = ``hitl_denied`` tool denials + ``approval_resolved``
  rejections + tasks flagged ``manual_intervention``, per 1,000 ``tool_call``
  audit events (trailing 30d). Per-archetype correction splits are deferred
  until audit events carry venture context (documented follow-up).
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ai_company.dashboard.kpis.base import KPICollector
from ai_company.data.database import Database
from ai_company.data.task_store import TERMINAL_STATUSES

logger = logging.getLogger(__name__)

# Re-exported from the shared single source of truth (data.task_store) so
# ATC and unit cost can never drift onto different denominators.
__all__ = ["StudioScorecardCollector", "TERMINAL_STATUSES"]

_KNOWN_VENTURES = ("venture-a", "venture-b", "venture-c", "studio-core")


class StudioScorecardCollector(KPICollector):
    """Collects the Studio Scorecard v1 snapshot as a virtual KPI department."""

    department = "studio"

    def __init__(
        self,
        project_root: Path | None = None,
        database: Database | None = None,
    ) -> None:
        super().__init__(project_root=project_root, database=database)

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def collect(self) -> dict[str, Any]:
        """Compute the scorecard snapshot. Never raises."""
        try:
            return self._collect_inner()
        except Exception:  # noqa: BLE001 - collectors must never raise
            logger.warning("Studio scorecard collection failed", exc_info=True)
            return {
                "department": self.department,
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "data_quality": "error",
                "error": "Studio scorecard collection failed; see logs",
                "kpis": {},
                "ventures": {},
                "risk": {},
            }

    def _collect_inner(self) -> dict[str, Any]:
        tracker = self._load_yaml("company/studio_tracker.yaml")
        ventures_cfg: dict[str, Any] = tracker.get("ventures", {})
        cfo: dict[str, Any] = tracker.get("cfo", {})
        baseline_days = int(tracker.get("baseline_days", 30) or 30)
        baseline_start = str(tracker.get("instrumentation_start", "") or "")

        tasks = self._tasks_from_sqlite()
        tasks_source = "sqlite" if tasks is not None else None
        if tasks is None:
            tasks = self._tasks_from_bus()
            tasks_source = "message_bus" if tasks else None
        tasks = tasks or []
        if tasks_source == "sqlite":
            tasks_quality, tasks_error = "real", None
        elif tasks_source == "message_bus":
            tasks_quality, tasks_error = (
                "fallback",
                "Using MessageBus (SQLite unavailable)",
            )
        else:
            tasks_quality, tasks_error = (
                "error",
                "No task data available (SQLite and MessageBus both unavailable)",
            )

        terminal = [t for t in tasks if str(t.get("status", "")) in TERMINAL_STATUSES]

        atc_overall = self._atc(terminal, None)
        atc_quality = tasks_quality if terminal else "error"
        atc_error = (
            tasks_error
            if tasks_error
            else (None if terminal else "No terminal tasks yet — ATC has no denominator")
        )

        ventures: dict[str, Any] = {}
        for vid in _KNOWN_VENTURES:
            cfg = ventures_cfg.get(vid, {})
            v_tasks = [
                t
                for t in terminal
                if str(t.get("venture_id", "studio-core") or "studio-core") == vid
            ]
            ventures[vid] = {
                "name": str(cfg.get("name", vid)),
                "archetype": str(cfg.get("archetype", "")),
                "stage": str(cfg.get("stage", "")),
                "atc": self._atc(v_tasks, vid),
                "task_count": len(v_tasks),
                "velocity_days": self._velocity(cfg),
            }

        correction, correction_quality, correction_error = self._correction_ratio()
        capital, capital_quality, capital_error = self._capital(cfo, ventures_cfg)
        risk = self._risk_strip()

        baseline_active, baseline_info = self._baseline_state(baseline_start, baseline_days)

        kpis: dict[str, Any] = {
            "atc_rate": self._banded_kpi(
                atc_overall,
                90.0,
                "%",
                higher_is_better=True,
                bands=[(90.0, "green"), (80.0, "watch")],
                below_band="block_scale",
                data_quality=atc_quality,
                error=atc_error,
            ),
            "correction_per_1k": self._baseline_kpi(
                correction,
                "count/1k",
                correction_quality,
                correction_error,
                baseline_active,
            ),
            "capital_efficiency": self._baseline_kpi(
                capital,
                "multiple",
                capital_quality,
                capital_error,
                baseline_active,
            ),
        }

        return {
            "department": self.department,
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "data_quality": tasks_quality,
            "baseline": baseline_info,
            "kpis": kpis,
            "ventures": ventures,
            "risk": risk,
        }

    # ------------------------------------------------------------------
    # ATC
    # ------------------------------------------------------------------

    def _atc(self, terminal: list[dict[str, Any]], _venture: str | None) -> float | None:
        """ATC = completed-without-manual / terminal-entered * 100."""
        if not terminal:
            return None
        clean = sum(
            1
            for t in terminal
            if str(t.get("status", "")) == "completed" and not t.get("manual_intervention", False)
        )
        return round(clean / len(terminal) * 100, 1)

    # ------------------------------------------------------------------
    # Velocity
    # ------------------------------------------------------------------

    def _velocity(self, cfg: dict[str, Any]) -> dict[str, Any]:
        """Velocity days for one venture, or a qualified no_data state."""
        thesis = str(cfg.get("thesis_approved", "") or "")
        deploy = str(cfg.get("deploy", "") or "")
        if not thesis or not deploy:
            return {
                "current": None,
                "status": "no_data",
                "error": "Gate timestamps missing (thesis_approved/deploy)",
            }
        if not cfg.get("gate_reviewed_at") or not cfg.get("gate_reviewed_by"):
            return {
                "current": None,
                "status": "no_data",
                "error": "No recorded gate review — phase advance unreviewed",
            }
        try:
            start = datetime.fromisoformat(thesis.replace("Z", "+00:00"))
            end = datetime.fromisoformat(deploy.replace("Z", "+00:00"))
        except ValueError:
            return {"current": None, "status": "no_data", "error": "Unparseable gate timestamps"}
        days = (end - start).days
        if days < 0:
            return {
                "current": None,
                "status": "no_data",
                "error": "Deploy predates thesis approval — tracker data invalid",
            }
        paused = 0
        pauses = cfg.get("pauses", []) or []
        for p in pauses:
            if not isinstance(p, dict):
                continue
            try:
                pf = datetime.fromisoformat(str(p.get("from", "")).replace("Z", "+00:00"))
                pt = datetime.fromisoformat(str(p.get("to", "")).replace("Z", "+00:00"))
            except ValueError:
                continue
            if pt >= pf and pf >= start and pt <= end:
                paused += (pt - pf).days
        net = max(0, days - paused)
        if net < 60:
            status = "on_track"
        elif net <= 90:
            status = "attention"
        else:
            status = "critical"
        return {
            "current": net,
            "unit": "days",
            "status": status,
            "gross_days": days,
            "paused_days": paused,
        }

    # ------------------------------------------------------------------
    # Correction ratio (audit trail, trailing 30d)
    # ------------------------------------------------------------------

    def _correction_ratio(self) -> tuple[float | None, str, str | None]:
        """(denials + rejections + manual tasks) per 1,000 tool calls."""
        try:
            from ai_company.audit.reader import AuditReader
        except ImportError as exc:
            return None, "error", f"Audit reader unavailable: {exc}"
        try:
            reader = AuditReader()
            cutoff = self._iso_days_ago(30)
            tool_calls = 0
            denials = 0
            rejections = 0
            for e in reader.read_all():
                ts = str(getattr(e, "timestamp", "") or "")
                if ts < cutoff:
                    continue
                et = str(getattr(e.event_type, "value", e.event_type))
                if et == "tool_call":
                    tool_calls += 1
                elif et == "hitl_denied":
                    denials += 1
                elif et == "approval_resolved":
                    meta = getattr(e, "metadata", {}) or {}
                    if isinstance(meta, dict) and meta.get("decision") == "rejected":
                        rejections += 1
        except Exception as exc:  # noqa: BLE001 - collectors must never raise
            logger.warning("Studio correction read failed", exc_info=True)
            return None, "error", f"Audit trail unreadable: {exc}"

        manual = sum(1 for t in self._terminal_cache() if t.get("manual_intervention", False))
        numerator = denials + rejections + manual
        if tool_calls == 0:
            return None, "error", "No tool_call events in trailing 30d — no action volume"
        return (
            round(numerator / tool_calls * 1000, 2),
            "real",
            None,
        )

    def _terminal_cache(self) -> list[dict[str, Any]]:
        tasks = self._tasks_from_sqlite()
        if tasks is None:
            tasks = self._tasks_from_bus()
        tasks = tasks or []
        return [t for t in tasks if str(t.get("status", "")) in TERMINAL_STATUSES]

    # ------------------------------------------------------------------
    # Capital efficiency (CFO inputs, ratified only)
    # ------------------------------------------------------------------

    def _capital(
        self, cfo: dict[str, Any], ventures_cfg: dict[str, Any]
    ) -> tuple[float | None, str, str | None]:
        """realized_value / capital_consumed — ratified figures only."""
        if not isinstance(cfo, dict) or not cfo.get("ratified", False):
            return None, "error", "CFO figures unratified — capital efficiency withheld (ADR-033)"
        realized = float(cfo.get("contracted_arr_usd", 0.0) or 0.0) + float(
            cfo.get("verified_cost_avoidance_usd", 0.0) or 0.0
        )
        consumed = 0.0
        for _vid, cfg in (ventures_cfg or {}).items():
            if isinstance(cfg, dict):
                try:
                    consumed += float(cfg.get("capital_consumed_usd", 0.0) or 0.0)
                except (TypeError, ValueError):
                    continue
        if consumed <= 0:
            return None, "error", "No capital consumed recorded yet"
        return round(realized / consumed, 2), "real", None

    # ------------------------------------------------------------------
    # Risk strip
    # ------------------------------------------------------------------

    def _risk_strip(self) -> dict[str, Any]:
        approvals = self._load_yaml("orchestrator/approvals.yaml")
        requests = approvals.get("requests", []) if isinstance(approvals, dict) else []
        expired = sum(1 for r in requests if isinstance(r, dict) and r.get("status") == "expired")
        pending_approvals = sum(
            1 for r in requests if isinstance(r, dict) and r.get("status") == "pending"
        )
        events = self._escalations_from_sqlite()
        if events is None:
            events = self._load_yaml("orchestrator/escalation.yaml").get("events", [])
        open_escalations = sum(1 for e in events or [] if not (e or {}).get("resolved", False))
        cost: dict[str, Any] = self._load_json("orchestrator/cost_tracker.json")
        spent = 0.0
        budget = 0.0
        if isinstance(cost, dict):
            try:
                spent = float(cost.get("total_spent", 0.0) or 0.0)
                budget = float(cost.get("total_budget", 0.0) or 0.0)
            except (TypeError, ValueError):
                spent, budget = 0.0, 0.0
        return {
            "expired_approvals": expired,
            "pending_approvals": pending_approvals,
            "open_escalations": open_escalations,
            "cost_overrun": bool(budget > 0 and spent > budget),
            "total_spent": spent,
            "total_budget": budget,
        }

    # ------------------------------------------------------------------
    # Baseline + KPI shaping helpers
    # ------------------------------------------------------------------

    def _baseline_state(self, start: str, window_days: int) -> tuple[bool, dict[str, Any]]:
        """Measurement-only window anchored at instrumentation_start."""
        info: dict[str, Any] = {
            "window_days": window_days,
            "started_at": start or None,
            "active": False,
            "days_elapsed": None,
        }
        if not start:
            info["note"] = "instrumentation_start unset — treating baseline as active"
            return True, info
        try:
            start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
        except ValueError:
            info["note"] = "instrumentation_start unparseable — treating baseline as active"
            return True, info
        now = datetime.now(timezone.utc)
        if start_dt.tzinfo is None:
            start_dt = start_dt.replace(tzinfo=timezone.utc)
        elapsed = (now - start_dt).days
        info["days_elapsed"] = max(0, elapsed)
        active = elapsed < window_days
        info["active"] = active
        if active:
            info["note"] = (
                f"Day {max(0, elapsed) + 1} of {window_days}: measurement only, no targets"
            )
        return active, info

    def _banded_kpi(
        self,
        current: float | None,
        target: float,
        unit: str,
        *,
        higher_is_better: bool,
        bands: list[tuple[float, str]],
        below_band: str,
        data_quality: str = "real",
        error: str | None = None,
    ) -> dict[str, Any]:
        kpi = self._kpi(
            current,
            target,
            unit,
            higher_is_better=higher_is_better,
            data_quality=data_quality,
            error=error,
        )
        if current is None:
            kpi["band"] = "no_data"
            return kpi
        band = below_band
        for threshold, name in bands:
            if higher_is_better and current >= threshold:
                band = name
                break
            if not higher_is_better and current <= threshold:
                band = name
                break
        kpi["band"] = band
        return kpi

    def _baseline_kpi(
        self,
        current: float | None,
        unit: str,
        data_quality: str,
        error: str | None,
        baseline_active: bool,
    ) -> dict[str, Any]:
        """Measurement-only shaping: info status, no target while baselining."""
        if baseline_active:
            result: dict[str, Any] = {
                "current": current,
                "target": None,
                "unit": unit,
                "status": "info" if current is not None else "no_data",
                "data_quality": data_quality,
                "baseline": "measurement_only",
            }
            if error:
                result["error"] = error
            return result
        return self._kpi(current, None, unit, data_quality=data_quality, error=error)

    @staticmethod
    def _iso_days_ago(days: int) -> str:
        from datetime import timedelta

        return (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
