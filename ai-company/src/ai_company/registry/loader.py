"""Registry loader — reads company-registry.yaml and config/ into raw dicts.

company-registry.yaml is the single source of truth for all agents.
Config files provide non-agent configuration (vision, strategy, culture, etc.).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _load_yaml(path: Path) -> dict[str, Any] | list[Any] | None:
    """Load a single YAML file. Returns None if missing."""
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class RegistryLoader:
    """Reads company-registry.yaml and config/ YAML files into a single raw dict.

    company-registry.yaml is the single source of truth for all agents.
    Agents are partitioned into executives, specialists, and board by their
    ``type`` field.
    """

    # Config files that remain separate from the registry.
    # These contain non-agent organizational configuration.
    CONFIG_FILE_MAP: dict[str, str] = {
        "company": "company/company.yaml",
        "vision": "company/vision.yaml",
        "strategy": "company/strategy.yaml",
        "culture": "company/culture.yaml",
        "governance": "company/governance.yaml",
        "policies": "company/policies.yaml",
        "kpis": "company/kpis.yaml",
        "budget": "company/budget.yaml",
        "committees": "board/committees.yaml",
        "board_meetings": "board/meetings.yaml",
        "voting": "board/voting.yaml",
        "departments": "departments/departments.yaml",
        "workflows": "workflows/workflows.yaml",
        "approval_matrix": "decision/approval_matrix.yaml",
        "risk_matrix": "decision/risk_matrix.yaml",
        "decision_tree": "decision/decision_tree.yaml",
    }

    def __init__(
        self,
        config_dir: Path,
        registry_path: Path | None = None,
    ) -> None:
        self.config_dir = config_dir
        # Default: company-registry.yaml at project root (one level up from config/)
        if registry_path is None:
            registry_path = config_dir.parent / "company-registry.yaml"
        self.registry_path = registry_path

    def load_all(self) -> dict[str, Any]:
        """Load every known config file and return a merged dict.

        Agents come from company-registry.yaml (single source of truth).
        Non-agent config comes from config/ files.
        Missing files are silently skipped (empty dict / empty list).
        """
        result: dict[str, Any] = {}

        # Load agents from the single-source registry
        agents_raw = self._load_agents_from_registry()
        result["executives"] = agents_raw["executives"]
        result["specialists"] = agents_raw["specialists"]
        result["board"] = agents_raw["board"]

        # Load non-agent config from config/ files
        for key, rel_path in self.CONFIG_FILE_MAP.items():
            raw = _load_yaml(self.config_dir / rel_path)
            if raw is None:
                result[key] = [] if key in ("policies", "kpis", "workflows") else {}
            else:
                result[key] = raw

        return result

    def _load_agents_from_registry(self) -> dict[str, list[dict[str, Any]]]:
        """Parse company-registry.yaml and partition agents by type.

        Returns dict with keys: executives, specialists, board.
        """
        raw = _load_yaml(self.registry_path)
        if raw is None:
            return {"executives": [], "specialists": [], "board": []}

        agents = []
        if isinstance(raw, dict):
            agents = raw.get("company", {}).get("agents", [])
        elif isinstance(raw, list):
            agents = raw

        executives: list[dict[str, Any]] = []
        specialists: list[dict[str, Any]] = []
        board: list[dict[str, Any]] = []

        for agent in agents:
            if not isinstance(agent, dict):
                continue
            agent_type = agent.get("type", "default")

            if agent_type == "executive":
                executives.append(agent)
            elif agent_type == "board":
                board.append(agent)
            else:
                # Everything else (specialist, default, etc.) goes to specialists
                specialists.append(agent)

        return {
            "executives": executives,
            "specialists": specialists,
            "board": board,
        }

    def load_single(self, key: str) -> Any:
        """Load a single config file by its registry key."""
        rel_path = self.CONFIG_FILE_MAP.get(key)
        if rel_path is None:
            raise KeyError(f"Unknown config key: {key}")
        return _load_yaml(self.config_dir / rel_path)
