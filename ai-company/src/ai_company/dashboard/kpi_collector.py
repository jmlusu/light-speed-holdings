"""KPI collector — reads operational data and produces department KPI snapshots.

.. deprecated::
    This module is kept for backward compatibility.  New code should use
    :mod:`ai_company.dashboard.kpis` which provides per-department collectors
    with a unified :func:`collect_all_kpis` entry point.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> Any:
    import json
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_yaml(path: Path) -> Any:
    import yaml
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def collect_engineering_kpis(base: Path) -> dict[str, Any]:
    """Collect KPI values for the engineering department.

    Delegates to :class:`ai_company.dashboard.kpis.engineering.EngineeringKPICollector`.
    """
    from ai_company.dashboard.kpis.engineering import EngineeringKPICollector
    return EngineeringKPICollector(project_root=base).collect()


def collect_all_kpis(base: Path | None = None) -> dict[str, Any]:
    """Collect KPIs for all departments. Returns a snapshot dict.

    Delegates to :func:`ai_company.dashboard.kpis.collect_all_kpis`.
    """
    from ai_company.dashboard.kpis import collect_all_kpis as _collect_all
    project_base = base or Path(__file__).parent.parent.parent.parent
    return _collect_all(project_root=project_base)


def save_snapshot(snapshots: dict[str, Any], output_dir: Path | None = None) -> Path:
    """Save KPI snapshot to a JSON file."""
    import json
    out = output_dir or Path("orchestrator/kpi_snapshots")
    out.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = out / f"snapshot-{ts}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(snapshots, f, indent=2, default=str)

    return path
