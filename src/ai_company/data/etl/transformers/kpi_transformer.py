"""KPI Transformers.

Transform raw operational data into computed KPI values.
"""

from __future__ import annotations

import contextlib
import logging
from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any

from ai_company.data.etl.base import Transformer, TransformResult

logger = logging.getLogger(__name__)


class KPITimeseriesTransformer(Transformer[dict[str, Any], dict[str, Any]]):
    """Transform collected KPI snapshots into time-series records for storage."""

    def __init__(self) -> None:
        super().__init__("kpi_timeseries")

    def transform(self, records: list[dict[str, Any]], **kwargs: Any) -> TransformResult[dict[str, Any]]:
        """Transform a KPI snapshot (from collect_all_kpis) into kpi_values records.

        Input: collect_all_kpis() output with structure:
        {
            "collected_at": "...",
            "departments": {
                "engineering": {
                    "kpis": {
                        "task_completion_rate": {"current": 95.0, "target": 95, "unit": "%", "status": "on_track"},
                        ...
                    }
                }
            }
        }

        Output: List of records for kpi_values table
        """
        output: list[dict[str, Any]] = []
        errors: list[str] = []
        warnings: list[str] = []

        for record in records:
            collected_at = record.get("collected_at", datetime.now(timezone.utc).isoformat())
            departments = record.get("departments", {})

            for dept_id, dept_data in departments.items():
                kpis = dept_data.get("kpis", {})
                for kpi_key, kpi_value in kpis.items():
                    # Skip non-numeric KPIs (dict breakdowns like agents_by_department)
                    raw_current = kpi_value.get("current", 0)
                    if isinstance(raw_current, dict):
                        warnings.append(f"Skipping non-numeric KPI {dept_id}.{kpi_key} (dict)")
                        continue

                    try:
                        current_value = float(raw_current)
                    except (TypeError, ValueError):
                        warnings.append(f"Skipping non-numeric KPI {dept_id}.{kpi_key}")
                        continue

                    raw_target = kpi_value.get("target")
                    target_value: float | None = None
                    if raw_target is not None:
                        with contextlib.suppress(TypeError, ValueError):
                            target_value = float(raw_target)

                    output.append({
                        "timestamp": collected_at,
                        "department": dept_id,
                        "kpi_key": kpi_key,
                        "current_value": current_value,
                        "target_value": target_value,
                        "unit": kpi_value.get("unit", ""),
                        "status": kpi_value.get("status", "info"),
                    })

        return TransformResult(
            records=output,
            input_count=len(records),
            output_count=len(output),
            errors=errors,
            warnings=warnings,
        )


class CompanyKPITransformer(Transformer[dict[str, Any], dict[str, Any]]):
    """Transform raw telemetry into company-level KPIs (KPI-001 through KPI-005)."""

    def __init__(self) -> None:
        super().__init__("company_kpi")

    def transform(self, records: list[dict[str, Any]], **kwargs: Any) -> TransformResult[dict[str, Any]]:
        """Compute company-level KPIs from task telemetry.

        Expects records to contain task data from inbox.json or tasks table.
        """
        # This transformer expects the raw task list as input
        tasks = records
        if not tasks:
            return TransformResult(
                records=[],
                input_count=0,
                output_count=0,
                errors=["No task data provided"],
            )

        # Compute KPI-003: Agent Utilization Rate
        # = distinct active agents in 30-day window / registered agents * 100
        cutoff = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        window_tasks = [t for t in tasks if t.get("created_at", "") >= cutoff]

        active_agents = set()
        for t in window_tasks:
            if t.get("sender_id"):
                active_agents.add(t["sender_id"])
            if t.get("receiver_id"):
                active_agents.add(t["receiver_id"])

        # Load registered agents count from registry
        import yaml

        from ai_company.paths import get_project_root

        registry_path = get_project_root() / "company-registry.yaml"
        registered_count = 0
        if registry_path.exists():
            with open(registry_path, "r", encoding="utf-8") as f:
                registry = yaml.safe_load(f) or {}
            registered_count = len(registry.get("company", {}).get("agents", []))

        utilization = round(len(active_agents) / registered_count * 100, 1) if registered_count > 0 else 0

        # Compute KPI-004: Build Success Rate
        # = completed / (completed + failed) * 100 over 30-day window
        completed = sum(1 for t in window_tasks if t.get("status") == "completed")
        failed = sum(1 for t in window_tasks if t.get("status") == "failed")
        build_success = round(completed / (completed + failed) * 100, 1) if (completed + failed) > 0 else 0

        now_iso = datetime.now(timezone.utc).isoformat()

        output = [
            {
                "kpi_id": "KPI-003",
                "name": "Agent Utilization Rate",
                "current": utilization,
                "target": 80,
                "unit": "percent",
                "frequency": "weekly",
                "owner": "coo",
                "source": ".opencode/inbox.json + company-registry.yaml",
                "formula": "distinct active agents in 30-day window / registered agents * 100",
                "computed_at": now_iso,
            },
            {
                "kpi_id": "KPI-004",
                "name": "Build Success Rate",
                "current": build_success,
                "target": 99.5,
                "unit": "percent",
                "frequency": "daily",
                "owner": "cto",
                "source": ".opencode/inbox.json",
                "formula": "completed / (completed + failed) * 100 over 30-day window",
                "computed_at": now_iso,
            },
        ]

        return TransformResult(
            records=output,
            input_count=len(tasks),
            output_count=len(output),
            errors=[],
            warnings=[],
        )


class DepartmentKPITransformer(Transformer[dict[str, Any], dict[str, Any]]):
    """Transform raw telemetry into department-specific KPIs."""

    def __init__(self) -> None:
        super().__init__("department_kpi")

    def transform(self, records: list[dict[str, Any]], **kwargs: Any) -> TransformResult[dict[str, Any]]:
        """Transform task/audit/cost records into department KPIs.

        This is a lightweight version that mirrors the KPI collectors
        but operates on raw records for batch ETL processing.
        """
        # For batch ETL, we expect pre-collected KPI snapshots as input
        # (output from collect_all_kpis). Just pass through with validation.
        return KPITimeseriesTransformer().transform(records, **kwargs)


class CostAggregationTransformer(Transformer[dict[str, Any], dict[str, Any]]):
    """Transform cost_records into daily/weekly/monthly aggregations."""

    def __init__(self, period: str = "daily") -> None:
        super().__init__(f"cost_{period}_aggregation")
        self.period = period

    def transform(self, records: list[dict[str, Any]], **kwargs: Any) -> TransformResult[dict[str, Any]]:
        """Aggregate cost records by time period.

        Input: Raw cost_records from SQLite
        Output: Aggregated summaries
        """
        if not records:
            return TransformResult(records=[], input_count=0, output_count=0)

        from collections import defaultdict

        # Group by period
        buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for record in records:
            ts = record.get("timestamp", "")
            if not ts:
                continue
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except ValueError:
                continue

            if self.period == "daily":
                key = dt.strftime("%Y-%m-%d")
            elif self.period == "weekly":
                # Monday start of week
                monday = dt - timedelta(days=dt.weekday())
                key = monday.strftime("%Y-%m-%d")
            elif self.period == "monthly":
                key = dt.strftime("%Y-%m")
            else:
                key = dt.strftime("%Y-%m-%d")

            buckets[key].append(record)

        output: list[dict[str, Any]] = []
        for period_key, period_records in buckets.items():
            total_cost = sum(r.get("cost_usd", 0) for r in period_records)
            total_prompt = sum(r.get("prompt_tokens", 0) for r in period_records)
            total_completion = sum(r.get("completion_tokens", 0) for r in period_records)
            total_calls = len(period_records)

            # By model
            by_model: dict[str, dict[str, Any]] = defaultdict(lambda: {"cost": 0.0, "prompt": 0, "completion": 0, "calls": 0})
            for r in period_records:
                model = r.get("model", "unknown")
                by_model[model]["cost"] += r.get("cost_usd", 0)
                by_model[model]["prompt"] += r.get("prompt_tokens", 0)
                by_model[model]["completion"] += r.get("completion_tokens", 0)
                by_model[model]["calls"] += 1

            # By agent
            by_agent: dict[str, dict[str, Any]] = defaultdict(lambda: {"cost": 0.0, "calls": 0})
            for r in period_records:
                agent = r.get("agent_name", "unknown")
                by_agent[agent]["cost"] += r.get("cost_usd", 0)
                by_agent[agent]["calls"] += 1

            output.append({
                "period": self.period,
                "period_key": period_key,
                "period_type": self.period,
                "total_cost_usd": round(total_cost, 6),
                "total_prompt_tokens": total_prompt,
                "total_completion_tokens": total_completion,
                "total_calls": total_calls,
                "by_model": {m: {"cost_usd": round(v["cost"], 6), "prompt_tokens": v["prompt"], "completion_tokens": v["completion"], "calls": v["calls"]} for m, v in by_model.items()},
                "by_agent": {a: {"cost_usd": round(v["cost"], 6), "calls": v["calls"]} for a, v in by_agent.items()},
                "computed_at": datetime.now(timezone.utc).isoformat(),
            })

        return TransformResult(
            records=output,
            input_count=len(records),
            output_count=len(output),
            errors=[],
            warnings=[],
        )


class AgentPerformanceTransformer(Transformer[dict[str, Any], dict[str, Any]]):
    """Transform task and audit records into agent performance metrics."""

    def __init__(self, days: int = 30) -> None:
        super().__init__("agent_performance")
        self.days = days

    def transform(self, records: list[dict[str, Any]], **kwargs: Any) -> TransformResult[dict[str, Any]]:
        """Compute per-agent performance from tasks and audit events.

        Expects records to be a dict with 'tasks' and 'audit_events' keys,
        or a flat list that will be separated by type.
        """
        # Separate tasks and audit events
        tasks = [r for r in records if "receiver_id" in r or "sender_id" in r]
        audit_events = [r for r in records if "event_type" in r and "agent_id" in r]

        if "tasks" in kwargs:
            tasks = kwargs["tasks"]
        if "audit_events" in kwargs:
            audit_events = kwargs["audit_events"]

        cutoff = (datetime.now(timezone.utc) - timedelta(days=self.days)).isoformat()

        # Get all agent IDs
        agent_ids = set()
        for t in tasks:
            if t.get("sender_id"):
                agent_ids.add(t["sender_id"])
            if t.get("receiver_id"):
                agent_ids.add(t["receiver_id"])
            if t.get("assignee"):
                agent_ids.add(t["assignee"])
        for e in audit_events:
            if e.get("agent_id"):
                agent_ids.add(e["agent_id"])

        output: list[dict[str, Any]] = []

        for agent_id in agent_ids:
            if not agent_id:
                continue

            # Task metrics
            tasks_sent = [t for t in tasks if t.get("sender_id") == agent_id and t.get("created_at", "") >= cutoff]
            tasks_received = [t for t in tasks if (t.get("receiver_id") == agent_id or t.get("assignee") == agent_id) and t.get("created_at", "") >= cutoff]

            sent_counts = Counter(t.get("status", "pending") for t in tasks_sent)
            recv_counts = Counter(t.get("status", "pending") for t in tasks_received)

            total_sent = sum(sent_counts.values())
            total_recv = sum(recv_counts.values())
            completed_recv = recv_counts.get("completed", 0)
            failed_recv = recv_counts.get("failed", 0)
            total_finished = completed_recv + failed_recv

            completion_rate = round(completed_recv / total_finished * 100, 2) if total_finished > 0 else 0
            error_rate = round(failed_recv / total_finished * 100, 2) if total_finished > 0 else 0

            # Audit events
            agent_audit = [e for e in audit_events if e.get("agent_id") == agent_id and e.get("timestamp", "") >= cutoff]
            event_counts = Counter(e.get("event_type", "") for e in agent_audit)
            tool_counts = Counter(e.get("tool", "") for e in agent_audit if e.get("tool"))

            # Cost metrics (if available in audit metadata)
            total_cost = 0.0
            prompt_tokens = 0
            completion_tokens = 0
            llm_calls = 0
            for e in agent_audit:
                meta = e.get("metadata", {})
                if isinstance(meta, str):
                    import json
                    try:
                        meta = json.loads(meta)
                    except json.JSONDecodeError:
                        meta = {}
                total_cost += float(meta.get("cost", 0) or 0)
                prompt_tokens += int(meta.get("prompt_tokens", 0) or 0)
                completion_tokens += int(meta.get("completion_tokens", 0) or 0)
                if meta.get("cost") is not None:
                    llm_calls += 1

            # Error events
            error_events = sum(1 for e in agent_audit if e.get("event_type") == "error" or e.get("severity") in ("error", "critical"))

            now_iso = datetime.now(timezone.utc).isoformat()
            period_start = (datetime.now(timezone.utc) - timedelta(days=self.days)).isoformat()
            period_end = now_iso

            output.append({
                "agent_id": agent_id,
                "period_days": self.days,
                "period_start": period_start,
                "period_end": period_end,
                "tasks_sent": total_sent,
                "tasks_received": total_recv,
                "tasks_completed": completed_recv,
                "tasks_failed": failed_recv,
                "completion_rate_pct": completion_rate,
                "error_rate_pct": error_rate,
                "sent_by_status": dict(sent_counts),
                "received_by_status": dict(recv_counts),
                "audit_events": dict(event_counts),
                "tool_usage": [{"tool": t, "calls": c} for t, c in tool_counts.most_common()],
                "total_cost_usd": round(total_cost, 6),
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "llm_calls": llm_calls,
                "error_events": error_events,
                "computed_at": now_iso,
            })

        return TransformResult(
            records=output,
            input_count=len(tasks) + len(audit_events),
            output_count=len(output),
            errors=[],
            warnings=[],
        )


__all__ = [
    "KPITimeseriesTransformer",
    "CompanyKPITransformer",
    "DepartmentKPITransformer",
    "CostAggregationTransformer",
    "AgentPerformanceTransformer",
]
