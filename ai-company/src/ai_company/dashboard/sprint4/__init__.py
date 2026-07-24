"""Sprint 4 KPI tracking for the CEO dashboard.

Provides:
- SprintMilestone tracking (planned vs completed)
- Sprint velocity computation
- Sprint burn-down data
- Sprint 4 KPI collector
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any


def _load_json(base: Path, rel_path: str | Path) -> Any:
    import json

    path = base / rel_path
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _load_yaml(base: Path, rel_path: str | Path) -> Any:
    import yaml

    path = base / rel_path
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except (yaml.YAMLError, OSError):
        return {}


def sprint4_status(base: Path | None = None) -> dict[str, Any]:
    """Return Sprint 4 progress snapshot.

    Reads from ``company/config/sprint4.yaml`` and computes
    milestone completion, burn-down, and velocity metrics.
    """
    root = base or Path(__file__).resolve().parents[4]

    sprint_data = _load_yaml(root, "company/config/sprint4.yaml")
    milestones = sprint_data.get("milestones", [])
    tasks = _load_json(root, ".opencode/inbox.json")

    # Count tasks by sprint reference
    sprint_tasks = [t for t in tasks if t.get("sprint") == "sprint4"]
    completed = sum(1 for t in sprint_tasks if t.get("status") == "completed")
    in_progress = sum(1 for t in sprint_tasks if t.get("status") == "in_progress")
    pending = sum(1 for t in sprint_tasks if t.get("status") == "pending")
    failed = sum(1 for t in sprint_tasks if t.get("status") == "failed")
    total = len(sprint_tasks)

    # Milestone completion
    milestone_statuses = []
    for m in milestones:
        mid = m.get("id", "")
        m_tasks = [t for t in sprint_tasks if t.get("milestone") == mid]
        m_total = len(m_tasks)
        m_done = sum(1 for t in m_tasks if t.get("status") == "completed")
        m_in_progress = sum(1 for t in m_tasks if t.get("status") == "in_progress")
        m_pending = sum(1 for t in m_tasks if t.get("status") == "pending")
        m_failed = sum(1 for t in m_tasks if t.get("status") == "failed")

        pct = round((m_done / m_total * 100), 1) if m_total > 0 else 0.0
        milestone_statuses.append(
            {
                "id": mid,
                "name": m.get("name", mid),
                "target_date": m.get("target_date", ""),
                "total_tasks": m_total,
                "completed": m_done,
                "in_progress": m_in_progress,
                "pending": m_pending,
                "failed": m_failed,
                "completion_pct": pct,
                "status": "complete" if pct >= 100 else "at_risk" if pct < 50 and m_pending > 0 else "on_track",
            }
        )

    overall_pct = round((completed / total * 100), 1) if total > 0 else 0.0

    # Burn-down: remaining work per day (mocked from milestone dates)
    burn_down = _compute_burn_down(milestones, sprint_tasks)

    return {
        "sprint": "sprint4",
        "collected_at": datetime.now().isoformat(),
        "overall": {
            "total_tasks": total,
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "failed": failed,
            "completion_pct": overall_pct,
        },
        "milestones": milestone_statuses,
        "burn_down": burn_down,
        "velocity": _compute_velocity(sprint_tasks),
    }


def _compute_burn_down(
    milestones: list[dict[str, Any]], sprint_tasks: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Compute remaining work per milestone target date."""
    from datetime import date

    burn_down: list[dict[str, Any]] = []
    today = date.today().isoformat()

    for m in milestones:
        target = m.get("target_date", "")
        if not target:
            continue
        m_tasks = [t for t in sprint_tasks if t.get("milestone") == m.get("id", "")]
        remaining = sum(1 for t in m_tasks if t.get("status") != "completed")
        burn_down.append(
            {
                "date": target,
                "milestone": m.get("id", ""),
                "remaining": remaining,
                "total": len(m_tasks),
            }
        )

    # Add today's entry if not present
    if burn_down and burn_down[-1].get("date") != today:
        total_remaining = sum(
            1 for t in sprint_tasks if t.get("status") != "completed"
        )
        burn_down.append(
            {"date": today, "milestone": "sprint4", "remaining": total_remaining, "total": len(sprint_tasks)}
        )

    return burn_down


def _compute_velocity(sprint_tasks: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute sprint velocity from completed tasks."""
    completed_tasks = [t for t in sprint_tasks if t.get("status") == "completed"]
    total_tasks = len(sprint_tasks)

    # Points: each completed task = 1 point (simplified)
    points_completed = len(completed_tasks)

    return {
        "points_completed": points_completed,
        "total_points": total_tasks,
        "velocity_pct": round((points_completed / total_tasks * 100), 1) if total_tasks > 0 else 0.0,
    }
