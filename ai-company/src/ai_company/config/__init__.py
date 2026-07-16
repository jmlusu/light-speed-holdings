"""Config loader — reads all config/ YAML files into a CompanyRegistry."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from ai_company.models import (
    Agent,
    ApprovalEntry,
    BoardMember,
    BoardMeeting,
    Budget,
    Company,
    CompanyRegistry,
    Committee,
    Culture,
    DecisionTreeConfig,
    Department,
    Executive,
    Governance,
    KPI,
    Policy,
    RiskMatrixConfig,
    Strategy,
    Vision,
    VotingConfig,
    Workflow,
)


_CONFIG_DIR = Path("config")

_COMPANY_FILES = {
    "company": "company/company.yaml",
    "vision": "company/vision.yaml",
    "strategy": "company/strategy.yaml",
    "culture": "company/culture.yaml",
    "governance": "company/governance.yaml",
    "policies": "company/policies.yaml",
    "kpis": "company/kpis.yaml",
    "budget": "company/budget.yaml",
}

_BOARD_FILES = {
    "board": "board/board.yaml",
    "committees": "board/committees.yaml",
    "meetings": "board/meetings.yaml",
    "voting": "board/voting.yaml",
}

_EXECUTIVES_FILE = "executives/executives.yaml"
_DEPARTMENTS_FILE = "departments/departments.yaml"
_SPECIALISTS_FILE = "agents/specialists.yaml"

_WORKFLOWS_FILE = "workflows/workflows.yaml"

_DECISION_FILES = {
    "approval_matrix": "decision/approval_matrix.yaml",
    "risk_matrix": "decision/risk_matrix.yaml",
    "decision_tree": "decision/decision_tree.yaml",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    """Load a single YAML file, return empty dict if missing."""
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def load_config(config_dir: Path | str | None = None) -> CompanyRegistry:
    """Load all config YAML files and return a validated CompanyRegistry."""
    base = Path(config_dir) if config_dir else _CONFIG_DIR

    company_data = _load_yaml(base / _COMPANY_FILES["company"])
    vision_data = _load_yaml(base / _COMPANY_FILES["vision"])
    strategy_data = _load_yaml(base / _COMPANY_FILES["strategy"])
    culture_data = _load_yaml(base / _COMPANY_FILES["culture"])
    governance_data = _load_yaml(base / _COMPANY_FILES["governance"])
    policies_data = _load_yaml(base / _COMPANY_FILES["policies"])
    kpis_data = _load_yaml(base / _COMPANY_FILES["kpis"])
    budget_data = _load_yaml(base / _COMPANY_FILES["budget"])

    board_data = _load_yaml(base / _BOARD_FILES["board"])
    committees_data = _load_yaml(base / _BOARD_FILES["committees"])
    meetings_data = _load_yaml(base / _BOARD_FILES["meetings"])
    voting_data = _load_yaml(base / _BOARD_FILES["voting"])

    executives_data = _load_yaml(base / _EXECUTIVES_FILE)
    departments_data = _load_yaml(base / _DEPARTMENTS_FILE)
    specialists_data = _load_yaml(base / _SPECIALISTS_FILE)

    workflows_data = _load_yaml(base / _WORKFLOWS_FILE)
    approval_data = _load_yaml(base / _DECISION_FILES["approval_matrix"])
    risk_data = _load_yaml(base / _DECISION_FILES["risk_matrix"])
    decision_tree_data = _load_yaml(base / _DECISION_FILES["decision_tree"])

    return CompanyRegistry(
        company=Company(**company_data) if company_data else Company(id="default", name="AI Company"),
        vision=Vision(**vision_data) if vision_data else Vision(),
        strategy=Strategy(**strategy_data) if strategy_data else Strategy(),
        culture=Culture(**culture_data) if culture_data else Culture(),
        governance=Governance(**governance_data) if governance_data else Governance(),
        policies=[Policy(**p) for p in policies_data.get("policies", [])],
        kpis=[KPI(**k) for k in kpis_data.get("kpis", [])],
        budget=Budget(**budget_data) if budget_data else Budget(),
        board=[BoardMember(**b) for b in board_data.get("members", [])],
        committees=[Committee(**c) for c in committees_data.get("committees", [])],
        board_meetings=[BoardMeeting(**m) for m in meetings_data.get("meetings", [])],
        voting=VotingConfig(**voting_data) if voting_data else VotingConfig(),
        executives=[Executive(**e) for e in executives_data.get("executives", [])],
        departments=[Department(**d) for d in departments_data.get("departments", [])],
        specialists=[Agent(**s) for s in specialists_data.get("specialists", [])],
        workflows=[Workflow(**w) for w in workflows_data.get("workflows", [])],
        approval_matrix=[ApprovalEntry(**a) for a in approval_data.get("approval_matrix", [])],
        risk_matrix=RiskMatrixConfig(**risk_data) if risk_data else RiskMatrixConfig(),
        decision_tree=DecisionTreeConfig(**decision_tree_data) if decision_tree_data else DecisionTreeConfig(),
    )
