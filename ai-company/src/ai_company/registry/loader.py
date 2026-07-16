"""Registry loader — reads all YAML files from config/ into raw dicts."""

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
    """Reads all config/ YAML files into a single raw dict structure."""

    # Maps top-level key → relative path within config/
    FILE_MAP: dict[str, str] = {
        "company": "company/company.yaml",
        "vision": "company/vision.yaml",
        "strategy": "company/strategy.yaml",
        "culture": "company/culture.yaml",
        "governance": "company/governance.yaml",
        "policies": "company/policies.yaml",
        "kpis": "company/kpis.yaml",
        "budget": "company/budget.yaml",
        "board": "board/board.yaml",
        "committees": "board/committees.yaml",
        "board_meetings": "board/meetings.yaml",
        "voting": "board/voting.yaml",
        "executives": "executives/executives.yaml",
        "departments": "departments/departments.yaml",
        "specialists": "agents/specialists.yaml",
        "workflows": "workflows/workflows.yaml",
        "approval_matrix": "decision/approval_matrix.yaml",
        "risk_matrix": "decision/risk_matrix.yaml",
        "decision_tree": "decision/decision_tree.yaml",
    }

    def __init__(self, config_dir: Path) -> None:
        self.config_dir = config_dir

    def load_all(self) -> dict[str, Any]:
        """Load every known config file and return a merged dict.

        Missing files are silently skipped (empty dict / empty list).
        """
        result: dict[str, Any] = {}
        for key, rel_path in self.FILE_MAP.items():
            raw = _load_yaml(self.config_dir / rel_path)
            if raw is None:
                # Provide sensible defaults for missing files
                result[key] = [] if key in ("policies", "kpis", "workflows") else {}
            else:
                result[key] = raw
        return result

    def load_single(self, key: str) -> Any:
        """Load a single config file by its registry key."""
        rel_path = self.FILE_MAP.get(key)
        if rel_path is None:
            raise KeyError(f"Unknown config key: {key}")
        return _load_yaml(self.config_dir / rel_path)
