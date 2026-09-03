"""Shared helpers for the Sprint 4 T017-T019 dashboard endpoint contracts.

The isolated/keyed fixtures in the individual test modules rebind the
dashboard StateStore to a sandboxed temp directory.  Without provisioning,
state paths such as ``company/agent-registry.json`` resolve against that bare
temp dir, so agent/org/task endpoints return empty lists or 404s.  These
helpers mirror the canonical ``setup_dashboard_data`` fixture in
``tests/unit/test_dashboard.py`` so the dashboard tests exercise the real
registry, departments, config, and empty orchestrator state.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import yaml

from ai_company.dashboard.repository import get_state_store, reset_state_store

_FIXTURE_REGISTRY = [
    {
        "name": "chief-of-staff",
        "role": "Chief of Staff",
        "type": "executive",
        "department": "Executive",
        "reportsTo": "human-ceo",
        "directReports": ["lead-engineering", "lead-marketing"],
        "description": "Coordinates all departments",
        "responsibilities": ["Align company goals across all departments."],
    },
    {
        "name": "lead-engineering",
        "role": "Lead Engineer",
        "type": "specialist",
        "department": "Engineering",
        "reportsTo": "chief-of-staff",
        "directReports": [],
        "description": "Leads engineering efforts",
        "responsibilities": ["Own the engineering roadmap."],
    },
    {
        "name": "lead-marketing",
        "role": "Marketing Lead",
        "type": "specialist",
        "department": "Marketing",
        "reportsTo": "chief-of-staff",
        "directReports": [],
        "description": "Leads marketing efforts",
        "responsibilities": ["Own the marketing roadmap."],
    },
]


def provision_dashboard_data(tmp_path: Path) -> None:
    """Point the dashboard StateStore at *tmp_path* and write fixture state."""
    reset_state_store()
    get_state_store(tmp_path)

    (tmp_path / "company").mkdir(exist_ok=True)
    (tmp_path / "company" / "agent-registry.json").write_text(
        json.dumps(_FIXTURE_REGISTRY), encoding="utf-8"
    )

    departments = {
        "departments": [
            {
                "name": "Executive",
                "executive": "chief-of-staff",
                "agents": ["chief-of-staff"],
                "total_agents": 1,
            },
            {
                "name": "Engineering",
                "executive": "lead-engineering",
                "agents": ["lead-engineering"],
                "total_agents": 1,
            },
        ]
    }
    (tmp_path / "company" / "departments.yaml").write_text(yaml.dump(departments), encoding="utf-8")

    (tmp_path / "orchestrator").mkdir(exist_ok=True)
    (tmp_path / ".opencode").mkdir(exist_ok=True)

    (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
    (tmp_path / "orchestrator" / "approvals.yaml").write_text(
        yaml.dump({"requests": []}), encoding="utf-8"
    )
    (tmp_path / "orchestrator" / "escalation.yaml").write_text(
        yaml.dump({"rules": [], "events": []}), encoding="utf-8"
    )
    (tmp_path / "orchestrator" / "scheduler.yaml").write_text(
        yaml.dump({"tasks": []}), encoding="utf-8"
    )

    real_models = Path(__file__).resolve().parents[2] / "company" / "models.yaml"
    if real_models.exists():
        shutil.copy2(str(real_models), str(tmp_path / "company" / "models.yaml"))

    real_kpis = Path(__file__).resolve().parents[2] / "company" / "config" / "kpis.yaml"
    if real_kpis.exists():
        config_dir = tmp_path / "company" / "config"
        config_dir.mkdir(exist_ok=True)
        shutil.copy2(str(real_kpis), str(config_dir / "kpis.yaml"))
