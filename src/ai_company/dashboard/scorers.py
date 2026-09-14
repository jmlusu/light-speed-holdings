"""Standalone KPI scorers for Org Health and Executive Scorecard.

This module contains the raw computation logic for operational metrics,
decoupled from the OrgHealthCalculator class to avoid circular imports.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ai_company.data.database import Database

logger = logging.getLogger(__name__)


def score_task_success_rate(tasks: list[dict[str, Any]]) -> float | None:
    """Ratio of completed tasks to total tasks (0-100)."""
    total = len(tasks)
    if total == 0:
        return None
    completed = sum(1 for t in tasks if t.get("status") == "completed")
    return (completed / total) * 100


def score_agent_utilization(tasks: list[dict[str, Any]], root: Path) -> float | None:
    """Active agents vs registered agents (0-100)."""
    from ai_company.dashboard.data_service import _count_registered_agents

    total_registered = _count_registered_agents(root)
    if total_registered == 0:
        return None

    active_agents = {
        agent
        for task in tasks
        for agent in (task.get("sender_id"), task.get("receiver_id"))
        if agent
    }
    if not active_agents:
        return 0.0
    return min(100.0, (len(active_agents) / total_registered) * 100)


def score_cost_efficiency(database: Database | None) -> float | None:
    """Budget utilization vs spend (0-100)."""
    from ai_company.dashboard.data_service import get_cost_summary

    summary = get_cost_summary(database=database)
    if summary is None:
        return None
    total_spent = float(summary.get("total_spent", 0) or 0)
    budget = float(summary.get("budget", 0) or 0)
    if budget <= 0:
        return None
    # Efficiency = 100 - (spent/budget * 100), clamped
    utilization = (total_spent / budget) * 100
    return max(0.0, min(100.0, 100.0 - utilization + 50.0))


def score_error_rate(tasks: list[dict[str, Any]]) -> float | None:
    """Error/exception rate across agent operations (0-100, inverted)."""
    total = len(tasks)
    if total == 0:
        return None
    error_tasks = sum(1 for t in tasks if t.get("status") in ("failed", "error", "cancelled"))
    error_rate = (error_tasks / total) * 100
    return max(0.0, 100.0 - error_rate)


def score_task_throughput(
    tasks: list[dict[str, Any]], target_per_day: float = 10.0
) -> float | None:
    """Tasks completed per day, normalized to 0-100 vs target."""
    total = len(tasks)
    if total == 0:
        return None
    completed = sum(1 for t in tasks if t.get("status") == "completed")
    # Compute days from the oldest task timestamp to now
    timestamps = []
    for t in tasks:
        ts = t.get("created_at", "")
        if ts:
            try:
                timestamps.append(datetime.fromisoformat(ts))
            except (ValueError, TypeError):
                continue
    if not timestamps:
        return None
    oldest = min(timestamps)
    now = datetime.now(timezone.utc)
    days = max(1, (now - oldest).days)
    tasks_per_day = completed / days
    return min(100.0, (tasks_per_day / target_per_day) * 100)


def score_escalation_rate(tasks: list[dict[str, Any]]) -> float | None:
    """Escalation rate across tasks (0-100, inverted)."""
    total = len(tasks)
    if total == 0:
        return None
    escalated = sum(1 for t in tasks if t.get("status") == "escalated")
    escalation_rate = (escalated / total) * 100
    return max(0.0, 100.0 - escalation_rate)


def score_security_posture(tasks: list[dict[str, Any]], root: Path) -> float | None:
    """Audit trail health and compliance indicators (0-100)."""
    from ai_company.dashboard.repository import get_state_store

    store = get_state_store()

    audit_events = []
    # Audit trail check (relies on .opencode/audit)
    try:
        for event in store.iter_jsonl(".opencode/audit"):
            if isinstance(event, dict):
                audit_events.append(event)
    except Exception:  # noqa: BLE001
        pass

    if not audit_events:
        return None

    # Factor 1: Audit trail completeness (events exist) — 40%
    completeness_score = min(100.0, len(audit_events) / 10.0 * 100)

    # Factor 2: No critical/error severity events — 30%
    severity_events = sum(1 for e in audit_events if e.get("severity") in ("error", "critical"))
    total_events = len(audit_events)
    severity_score = max(0.0, 100.0 - (severity_events / max(1, total_events) * 100))

    # Factor 3: Compliance tasks completed — 30%
    compliance_keywords = {"compliance", "audit", "security", "review", "approval"}
    compliance_tasks = [
        t
        for t in tasks
        if any(kw in (t.get("instruction", "") or "").lower() for kw in compliance_keywords)
    ]
    if compliance_tasks:
        compliance_completed = sum(1 for t in compliance_tasks if t.get("status") == "completed")
        compliance_score = (compliance_completed / len(compliance_tasks)) * 100
    else:
        compliance_score = 80.0  # Neutral default when no compliance tasks exist

    return (completeness_score * 0.4) + (severity_score * 0.3) + (compliance_score * 0.3)


def score_strategic_alignment(tasks: list[dict[str, Any]], root: Path) -> float | None:
    """Percentage of tasks mapped to active goals and departments (0-100)."""
    total = len(tasks)
    if total == 0:
        return None

    # Load registry to get department mapping
    try:
        from ai_company.dashboard.repository import get_state_store

        store = get_state_store()
        registry = store.read_json("company/agent-registry.json", default=[])
    except Exception:  # noqa: BLE001
        registry = []

    agent_departments: dict[str, str] = {}
    for agent in registry:
        name = agent.get("name", "")
        dept = agent.get("department", "")
        if name and dept:
            agent_departments[name] = dept

    # Count tasks assigned to agents with known departments
    aligned = 0
    for t in tasks:
        receiver = t.get("receiver_id", "")
        sender = t.get("sender_id", "")
        if receiver in agent_departments or sender in agent_departments:
            aligned += 1

    return (aligned / total) * 100
