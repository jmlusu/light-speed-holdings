"""Sync company/agent-registry.json from company-registry.yaml.

This module ensures the legacy JSON registry (consumed by the dashboard,
model_router, executor, and other components) stays in sync with the
single source of truth: company-registry.yaml.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


def _agent_yaml_to_json(agent: dict[str, Any]) -> dict[str, Any]:
    """Convert a single agent from YAML registry format to JSON registry format.

    The YAML uses snake_case keys; the legacy JSON uses camelCase.
    The JSON also adds a 'permission' field derived from the agent type.
    """
    # Build the JSON agent object
    json_agent: dict[str, Any] = {
        "name": agent.get("id", "").replace("_", "-"),
        "role": agent.get("name", agent.get("id", "")),
        "type": _map_type(agent.get("type", "default"), agent.get("id", "")),
        "department": agent.get("department", ""),
        "reportsTo": _convert_id_to_name(agent.get("reports_to", "")),
        "directReports": [_convert_id_to_name(d) for d in agent.get("direct_reports", [])],
        "description": agent.get("description", ""),
        "responsibilities": agent.get("responsibilities", []),
        "guidelines": agent.get("guidelines", ""),
        "tools": agent.get("tools", []),
        "permission": _derive_permission(agent.get("type", "default")),
    }

    # Include optional fields
    if agent.get("model_tier"):
        json_agent["model_tier"] = agent["model_tier"]
    if agent.get("technical_domain"):
        json_agent["technical_domain"] = agent["technical_domain"]

    return json_agent


def _map_type(raw_type: str, agent_id: str) -> str:
    """Map YAML type field to JSON type."""
    if raw_type == "board":
        return "Board"
    if raw_type == "executive":
        return "Executive"
    if raw_type == "specialist":
        return "Specialist"
    # For 'default' type: infer from id
    executive_ids = {
        "human_ceo", "chief_of_staff", "cto", "coo", "caio",
        "cfo", "cpo", "cmo", "hr", "ciso", "cio", "cdo",
        "clo", "cso", "ceo_advisor", "customer_success",
        "sales", "legal",
    }
    if agent_id in executive_ids:
        return "Executive"
    return "Specialist"


def _derive_permission(raw_type: str) -> str:
    """Derive permission level from agent type."""
    if raw_type == "board":
        return "ReviewOnly"
    if raw_type == "executive":
        return "Execute"
    return "Execute"


def _convert_id_to_name(agent_id: str) -> str:
    """Convert an underscored agent ID to a hyphenated name."""
    return agent_id.replace("_", "-") if agent_id else ""


def sync_registry(
    yaml_path: str | Path = "company-registry.yaml",
    json_path: str | Path = "company/agent-registry.json",
) -> int:
    """Regenerate agent-registry.json from company-registry.yaml.

    Returns the number of agents written to the JSON file.
    """
    yaml_path = Path(yaml_path)
    json_path = Path(json_path)

    if not yaml_path.exists():
        raise FileNotFoundError(f"YAML registry not found: {yaml_path}")

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    agents = data.get("company", {}).get("agents", []) if isinstance(data, dict) else data

    json_agents = [_agent_yaml_to_json(a) for a in agents]

    # Ensure parent directory exists
    json_path.parent.mkdir(parents=True, exist_ok=True)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_agents, f, indent=2, ensure_ascii=False)

    logger.info("Synced %d agents from %s to %s", len(json_agents), yaml_path, json_path)
    return len(json_agents)


def verify_sync(
    yaml_path: str | Path = "company-registry.yaml",
    json_path: str | Path = "company/agent-registry.json",
) -> list[str]:
    """Verify YAML and JSON registries are in sync.

    Returns a list of error strings. Empty list means they are in sync.
    """
    errors: list[str] = []
    yaml_path = Path(yaml_path)
    json_path = Path(json_path)

    if not yaml_path.exists():
        return [f"YAML registry not found: {yaml_path}"]
    if not json_path.exists():
        return [f"JSON registry not found: {json_path}"]

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    yaml_agents = data.get("company", {}).get("agents", []) if isinstance(data, dict) else data

    with open(json_path, "r", encoding="utf-8") as f:
        json_agents = json.load(f)

    yaml_ids = set(a.get("id", "").replace("_", "-") for a in yaml_agents)
    json_names = set(a.get("name", "") for a in json_agents)

    missing = yaml_ids - json_names
    extra = json_names - yaml_ids

    if missing:
        errors.append(f"Agents in YAML but not in JSON ({len(missing)}): {sorted(missing)}")
    if extra:
        errors.append(f"Agents in JSON but not in YAML ({len(extra)}): {sorted(extra)}")

    return errors


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    count = sync_registry()
    print(f"Synced {count} agents to company/agent-registry.json")
