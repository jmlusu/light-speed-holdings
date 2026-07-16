"""Registry parser — converts raw YAML dicts into typed Pydantic models."""

from __future__ import annotations

from typing import Any

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


def _unwrap(data: dict[str, Any], key: str) -> dict[str, Any]:
    """Unwrap a top-level YAML key if present (e.g. company.yaml has company: {...})."""
    if key in data and isinstance(data[key], dict):
        return data[key]
    return data


def _unwrap_list(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    """Unwrap a top-level YAML key that contains a list."""
    if key in data and isinstance(data[key], list):
        return data[key]
    if key in data and isinstance(data[key], dict):
        return data[key].get(key, [])
    return []


def _list_of(data: Any, model_cls: type) -> list:
    """Parse a list of dicts into model instances, skipping invalid entries."""
    if not isinstance(data, list):
        return []
    items = []
    for item in data:
        if isinstance(item, dict):
            try:
                items.append(model_cls(**item))
            except Exception:
                continue
    return items


class RegistryParser:
    """Parses raw YAML dicts into a typed CompanyRegistry."""

    def parse(self, raw: dict[str, Any]) -> CompanyRegistry:
        """Parse all raw data into a CompanyRegistry."""
        return CompanyRegistry(
            company=self._parse_company(raw.get("company", {})),
            vision=self._parse_vision(raw.get("vision", {})),
            strategy=self._parse_strategy(raw.get("strategy", {})),
            culture=self._parse_culture(raw.get("culture", {})),
            governance=self._parse_governance(raw.get("governance", {})),
            policies=self._parse_policies(raw.get("policies", {})),
            kpis=self._parse_kpis(raw.get("kpis", {})),
            budget=self._parse_budget(raw.get("budget", {})),
            board=self._parse_board(raw.get("board", {})),
            committees=self._parse_committees(raw.get("committees", {})),
            board_meetings=self._parse_meetings(raw.get("board_meetings", {})),
            voting=self._parse_voting(raw.get("voting", {})),
            executives=self._parse_executives(raw.get("executives", {})),
            departments=self._parse_departments(raw.get("departments", {})),
            specialists=self._parse_specialists(raw.get("specialists", {})),
            workflows=self._parse_workflows(raw.get("workflows", {})),
            approval_matrix=self._parse_approval_matrix(raw.get("approval_matrix", {})),
            risk_matrix=self._parse_risk_matrix(raw.get("risk_matrix", {})),
            decision_tree=self._parse_decision_tree(raw.get("decision_tree", {})),
        )

    def _parse_company(self, data: dict[str, Any]) -> Company:
        data = _unwrap(data, "company")
        if not data:
            return Company(id="default", name="AI Company")
        return Company(**data)

    def _parse_vision(self, data: dict[str, Any]) -> Vision:
        data = _unwrap(data, "vision")
        if not data:
            return Vision()
        return Vision(**data)

    def _parse_strategy(self, data: dict[str, Any]) -> Strategy:
        data = _unwrap(data, "strategy")
        if not data:
            return Strategy()
        return Strategy(**data)

    def _parse_culture(self, data: dict[str, Any]) -> Culture:
        data = _unwrap(data, "culture")
        if not data:
            return Culture()
        return Culture(**data)

    def _parse_governance(self, data: dict[str, Any]) -> Governance:
        data = _unwrap(data, "governance")
        if not data:
            return Governance()
        return Governance(**data)

    def _parse_policies(self, data: dict[str, Any]) -> list[Policy]:
        data = _unwrap(data, "policies")
        items = data.get("policies", []) if isinstance(data, dict) else []
        return _list_of(items, Policy)

    def _parse_kpis(self, data: dict[str, Any]) -> list[KPI]:
        data = _unwrap(data, "kpis")
        items = data.get("kpis", []) if isinstance(data, dict) else []
        return _list_of(items, KPI)

    def _parse_budget(self, data: dict[str, Any]) -> Budget:
        data = _unwrap(data, "budget")
        if not data:
            return Budget()
        return Budget(**data)

    def _parse_board(self, data: dict[str, Any]) -> list[BoardMember]:
        # board.yaml can have either {"members": [...]} or {"board": [...]}
        if isinstance(data, dict):
            items = data.get("members", data.get("board", []))
        elif isinstance(data, list):
            items = data
        else:
            items = []
        return _list_of(items, BoardMember)

    def _parse_committees(self, data: dict[str, Any]) -> list[Committee]:
        data = _unwrap(data, "committees")
        items = data.get("committees", []) if isinstance(data, dict) else []
        return _list_of(items, Committee)

    def _parse_meetings(self, data: dict[str, Any]) -> list[BoardMeeting]:
        # meetings.yaml can have {"meetings": [...]} or be a list directly
        if isinstance(data, dict):
            items = data.get("meetings", data.get("board_meetings", []))
        elif isinstance(data, list):
            items = data
        else:
            items = []
        return _list_of(items, BoardMeeting)

    def _parse_voting(self, data: dict[str, Any]) -> VotingConfig:
        data = _unwrap(data, "voting")
        if not data:
            return VotingConfig()
        return VotingConfig(**data)

    def _parse_executives(self, data: dict[str, Any]) -> list[Executive]:
        items = _unwrap_list(data, "executives")
        return _list_of(items, Executive)

    def _parse_departments(self, data: dict[str, Any]) -> list[Department]:
        items = _unwrap_list(data, "departments")
        return _list_of(items, Department)

    def _parse_specialists(self, data: dict[str, Any]) -> list[Agent]:
        items = _unwrap_list(data, "specialists")
        return _list_of(items, Agent)

    def _parse_workflows(self, data: dict[str, Any]) -> list[Workflow]:
        data = _unwrap(data, "workflows")
        items = data.get("workflows", []) if isinstance(data, dict) else []
        return _list_of(items, Workflow)

    def _parse_approval_matrix(self, data: dict[str, Any]) -> list[ApprovalEntry]:
        data = _unwrap(data, "approval_matrix")
        items = data.get("approval_matrix", []) if isinstance(data, dict) else []
        return _list_of(items, ApprovalEntry)

    def _parse_risk_matrix(self, data: dict[str, Any]) -> RiskMatrixConfig:
        data = _unwrap(data, "risk_matrix")
        if not data:
            return RiskMatrixConfig()
        return RiskMatrixConfig(**data)

    def _parse_decision_tree(self, data: dict[str, Any]) -> DecisionTreeConfig:
        data = _unwrap(data, "decision_tree")
        if not data:
            return DecisionTreeConfig()
        return DecisionTreeConfig(**data)
