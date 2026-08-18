"""Operations department KPI collector — SOP compliance, DLQ health, state hygiene, capacity."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from ai_company.dashboard.kpis.base import KPICollector

logger = logging.getLogger(__name__)


class OperationsKPICollector(KPICollector):
    """Collects live metrics for the Operations department."""

    department = "operations"

    def collect(self) -> dict[str, Any]:
        tasks = self._tasks_from_sqlite()
        if tasks is None:
            tasks = self._tasks_from_bus()

        dlq_path = self.root / ".opencode" / "dead_letter.json"
        dlq_entries = []
        if dlq_path.exists():
            try:
                import json

                with open(dlq_path, "r", encoding="utf-8") as fh:
                    dlq_entries = json.load(fh)
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("Failed to read DLQ state %s: %s", dlq_path, exc)

        inbox_path = self.root / ".opencode" / "inbox.json"
        inbox_tasks = []
        if inbox_path.exists():
            try:
                import json

                with open(inbox_path, "r", encoding="utf-8") as fh:
                    inbox_tasks = json.load(fh)
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("Failed to read inbox state %s: %s", inbox_path, exc)

        scheduler = self._load_yaml("orchestrator/scheduler.yaml")
        escalation_data = self._load_yaml("orchestrator/escalation.yaml")
        escalation_events = escalation_data.get("events", [])

        # ── SOP Compliance Checks ──────────────────────────────────────
        # Count departments with current SOPs (docs/sop/*.md files)
        sop_dir = self.root / "docs" / "sop"
        # Map department names to SOP files
        dept_sop_map = {
            "engineering": "engineering-sop.md",
            "hr": "hr-sop.md",
            "finance": "finance-sop.md",
            "marketing": "marketing-sop.md",
            "sales": "sales-sop.md",
            "customer_success": "customer-success-sop.md",
            "legal": "legal-sop.md",
            "operations": "operations-sop.md",
        }
        departments_with_sop = sum(
            1 for fname in dept_sop_map.values() if (sop_dir / fname).exists()
        )
        total_departments = len(dept_sop_map)
        sop_coverage_pct = (
            round((departments_with_sop / total_departments * 100), 1)
            if total_departments > 0
            else 0.0
        )

        # Check SOP freshness (last updated within 90 days)
        from datetime import timedelta

        now = datetime.now()
        stale_sops = 0
        for fname in dept_sop_map.values():
            fpath = sop_dir / fname
            if fpath.exists():
                try:
                    import re

                    content = fpath.read_text(encoding="utf-8")
                    # Extract "Last Updated" date from header
                    match = re.search(r"Last Updated:\s*([A-Za-z]+\s+\d{4})", content)
                    if match:
                        updated_str = match.group(1)
                        # Parse month year format (e.g., "July 2026")
                        from datetime import datetime as dt

                        updated_dt = dt.strptime(updated_str, "%B %Y")
                        if now - updated_dt > timedelta(days=90):
                            stale_sops += 1
                except Exception as exc:  # noqa: BLE001 - a bad SOP file must not break collection
                    logger.warning("Failed to parse SOP freshness for %s: %s", fname, exc)

        # ── DLQ Health ─────────────────────────────────────────────────
        dlq_count = len(dlq_entries)
        dlq_recent = sum(
            1
            for e in dlq_entries
            if e.get("moved_at")
            and (now - datetime.fromisoformat(e["moved_at"].replace("Z", "+00:00"))).days < 7
        )

        # Compute DLQ retry rate: percentage of DLQ entries that had retries (retry_count > 0)
        dlq_retried = sum(1 for e in dlq_entries if (e.get("task", {}).get("retry_count") or 0) > 0)
        dlq_retry_rate = round((dlq_retried / dlq_count * 100), 1) if dlq_count > 0 else None
        dlq_retry_quality = "real" if dlq_count > 0 else "error"
        dlq_retry_error = None if dlq_count > 0 else "No DLQ entries available"

        # ── Inbox Health ───────────────────────────────────────────────
        inbox_total = len(inbox_tasks)
        inbox_pending = sum(1 for t in inbox_tasks if t.get("status") == "pending")
        inbox_in_progress = sum(1 for t in inbox_tasks if t.get("status") == "in_progress")
        inbox_stale = sum(
            1
            for t in inbox_tasks
            if t.get("status") == "in_progress"
            and t.get("updated_at")
            and (
                now - datetime.fromisoformat(t["updated_at"].replace("Z", "+00:00"))
            ).total_seconds()
            > 1800
        )

        # ── State File Hygiene ─────────────────────────────────────────
        # Check registry integrity
        registry_path = self.root / "company-registry.yaml"
        registry_valid = registry_path.exists()
        registry_agent_count = 0
        if registry_valid:
            try:
                import yaml

                with open(registry_path, "r", encoding="utf-8") as fh:
                    data = yaml.safe_load(fh)
                    registry_agent_count = len(data.get("company", {}).get("agents", []))
            except Exception as exc:  # noqa: BLE001 - a bad registry must not break collection
                logger.warning("Failed to load registry %s: %s", registry_path, exc)
                registry_valid = False

        # Check generated agents match registry
        agents_dir = self.root / ".opencode" / "agents"
        generated_agents = list(agents_dir.glob("*.md")) if agents_dir.exists() else []
        gen_count = len(generated_agents)

        # ── Capacity & Scaling ─────────────────────────────────────────
        scheduled_tasks = scheduler.get("tasks", [])
        open_escalations = [e for e in escalation_events if not e.get("resolved", False)]

        return {
            "department": self.department,
            "collected_at": now.isoformat(),
            "kpis": {
                # SOP Compliance
                "sop_coverage_pct": self._kpi(sop_coverage_pct, 100, "%"),
                "sop_stale_count": self._kpi(stale_sops, 0, "count", higher_is_better=False),
                "sop_departments_covered": self._kpi(
                    departments_with_sop, total_departments, "count"
                ),
                # DLQ Health
                "dlq_total_entries": self._kpi(dlq_count, None, "count"),
                "dlq_recent_entries": self._kpi(dlq_recent, None, "count"),
                "dlq_retry_rate": self._kpi(
                    dlq_retry_rate, 80, "%", data_quality=dlq_retry_quality, error=dlq_retry_error
                ),
                # Inbox Health
                "inbox_total_tasks": self._kpi(inbox_total, None, "count"),
                "inbox_pending_tasks": self._kpi(inbox_pending, None, "count"),
                "inbox_in_progress_tasks": self._kpi(inbox_in_progress, None, "count"),
                "inbox_stale_tasks": self._kpi(inbox_stale, 0, "count", higher_is_better=False),
                # State Hygiene
                "registry_valid": self._kpi(1 if registry_valid else 0, 1, "bool"),
                "registry_agent_count": self._kpi(registry_agent_count, None, "count"),
                "generated_agent_count": self._kpi(gen_count, registry_agent_count, "count"),
                "agent_sync_status": self._kpi(
                    1 if gen_count == registry_agent_count else 0, 1, "bool"
                ),
                # Capacity & Escalation
                "scheduled_tasks": self._kpi(len(scheduled_tasks), None, "count"),
                "open_escalations": self._kpi(
                    len(open_escalations), 0, "count", higher_is_better=False
                ),
                "escalation_rate_pct": self._kpi(
                    round((len(open_escalations) / max(inbox_total, 1) * 100), 1),
                    15,
                    "%",
                    higher_is_better=False,
                ),
            },
        }
