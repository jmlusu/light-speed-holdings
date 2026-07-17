"""KPI collector — reads operational data and produces department KPI snapshots."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


def _load_json(path: Path) -> Any:
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_yaml(path: Path) -> Any:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def collect_engineering_kpis(base: Path) -> dict[str, Any]:
    """Collect KPI values for the engineering department."""
    tasks = _load_json(base / ".opencode" / "inbox.json")
    escalations = _load_yaml(base / "orchestrator" / "escalation.yaml")
    scheduler = _load_yaml(base / "orchestrator" / "scheduler.yaml")

    total = len(tasks)
    completed = sum(1 for t in tasks if t.get("status") == "completed")
    failed = sum(1 for t in tasks if t.get("status") == "failed")
    escalated = sum(1 for t in tasks if t.get("status") == "escalated")

    completion_rate = (completed / total * 100) if total > 0 else 0
    escalation_rate = (escalated / total * 100) if total > 0 else 0

    events = escalations.get("events", [])
    open_escalations = [e for e in events if not e.get("resolved", False)]

    scheduled = scheduler.get("tasks", [])

    return {
        "department": "engineering",
        "collected_at": datetime.now().isoformat(),
        "kpis": {
            "task_completion_rate": {
                "current": round(completion_rate, 1),
                "target": 95,
                "unit": "%",
                "status": "on_track" if completion_rate >= 95 else "below_target",
            },
            "escalation_rate": {
                "current": round(escalation_rate, 1),
                "target": 5,
                "unit": "%",
                "status": "on_track" if escalation_rate <= 5 else "above_target",
            },
            "total_tasks": {
                "current": total,
                "target": None,
                "unit": "count",
                "status": "info",
            },
            "failed_tasks": {
                "current": failed,
                "target": 0,
                "unit": "count",
                "status": "on_track" if failed == 0 else "above_target",
            },
            "open_escalations": {
                "current": len(open_escalations),
                "target": 0,
                "unit": "count",
                "status": "on_track" if len(open_escalations) == 0 else "above_target",
            },
            "scheduled_tasks": {
                "current": len(scheduled),
                "target": None,
                "unit": "count",
                "status": "info",
            },
        },
    }


def collect_all_kpis(base: Path | None = None) -> dict[str, Any]:
    """Collect KPIs for all departments. Returns a snapshot dict."""
    project_base = base or Path(__file__).parent.parent.parent.parent

    snapshots: dict[str, Any] = {
        "collected_at": datetime.now().isoformat(),
        "departments": {},
    }

    snapshots["departments"]["engineering"] = collect_engineering_kpis(project_base)

    return snapshots


def save_snapshot(snapshots: dict[str, Any], output_dir: Path | None = None) -> Path:
    """Save KPI snapshot to a JSON file."""
    out = output_dir or Path("orchestrator/kpi_snapshots")
    out.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = out / f"snapshot-{ts}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(snapshots, f, indent=2, default=str)

    return path
