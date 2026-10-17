"""Registry write seam — the single front door for mutating company-registry.yaml.

company-registry.yaml is the single source of truth (see sync.py, generator.py,
loader.py). All mutations to the registry MUST go through this module so that:

1. Validation happens before any file is touched.
2. The YAML, generated agent files (.md), and derived JSON
   (company/agent-registry.json) stay consistent.
3. A failed write rolls back cleanly (backup + restore).

This module currently exposes set_reports_to(); extend it with further semantic
functions (e.g. set_department, add_agent) as the dashboard needs them. Do not
add raw "dump this dict" helpers — the interface is the test surface.
"""

from __future__ import annotations

import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast

import yaml

logger = logging.getLogger(__name__)

DEFAULT_YAML_PATH = Path("company-registry.yaml")
DEFAULT_JSON_PATH = Path("company/agent-registry.json")

# Virtual root used as a manager in the YAML/JSON (human_ceo reports_to "board").
# The dashboard API uses "__root__" as an alias for the same concept.
VIRTUAL_ROOTS = frozenset({"board", "__root__"})


def _normalize_id(value: str) -> str:
    """Normalize a hyphenated or underscored agent id to the YAML underscore form."""
    return value.replace("-", "_") if value else value


def _load_yaml_fresh(yaml_path: Path) -> dict[str, Any]:
    """Load the registry YAML fresh (bypassing the loader cache — write path)."""
    if not yaml_path.exists():
        raise FileNotFoundError(f"Registry not found: {yaml_path}")
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data is None:
        return {"company": {"agents": []}}
    if not isinstance(data, dict):
        raise ValueError(f"Registry YAML root must be a mapping, got {type(data).__name__}")
    return cast(dict[str, Any], data)


def _save_yaml(data: dict[str, Any], yaml_path: Path) -> None:
    """Persist the registry YAML. sort_keys=False preserves authoring order.

    The registry has no comments (verified); YAML anchors are expanded into
    equivalent plain data on dump — functionally identical, formatting changes.
    This matches the existing onboarding write path.
    """
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def _backup_yaml(yaml_path: Path) -> Path:
    """Create a timestamped backup of the YAML registry for rollback."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = yaml_path.with_suffix(f".yaml.bak.{timestamp}")
    shutil.copy2(yaml_path, backup_path)
    return backup_path


def _get_agents(data: dict[str, Any]) -> list[dict[str, Any]]:
    agents = data.get("company", {}).get("agents", [])
    return [a for a in agents if isinstance(a, dict)]


def _find_agent(agents: list[dict[str, Any]], agent_ref: str) -> dict[str, Any] | None:
    """Find an agent by id or hyphenated name, accepting either separator form."""
    target = _normalize_id(agent_ref)
    for agent in agents:
        if agent.get("id") == target:
            return agent
    return None


def _known_manager_ids(agents: list[dict[str, Any]]) -> set[str]:
    return {a.get("id", "") for a in agents if a.get("id")}


def _would_create_cycle(agents: list[dict[str, Any]], agent_id: str, new_manager_id: str) -> bool:
    """Walk up from new_manager_id via reports_to; if we reach agent_id, it's a cycle."""
    manager_map = {a.get("id", ""): a.get("reports_to", "") for a in agents}
    visited: set[str] = set()
    cursor = new_manager_id
    while cursor and cursor not in visited:
        if cursor == agent_id:
            return True
        visited.add(cursor)
        cursor = manager_map.get(cursor, "")
    return False


def set_reports_to(
    agent_ref: str,
    manager_ref: str,
    *,
    yaml_path: Path | str = DEFAULT_YAML_PATH,
    json_path: Path | str = DEFAULT_JSON_PATH,
) -> dict[str, Any]:
    """Reassign an agent's reports_to in the YAML registry, then sync derived outputs.

    Accepts agent/manager references in either hyphenated (dashboard JSON name)
    or underscored (YAML id) form. The virtual roots "board" and "__root__" are
    accepted as manager values and stored as "board" in the YAML.

    Pipeline:
    1. Load YAML fresh and validate (agent exists, manager valid, no self-assign,
       no cycle).
    2. Backup YAML, mutate, write.
    3. Regenerate agent .md files (AgentGenerator reads the updated YAML).
    4. Sync company/agent-registry.json from the updated YAML.
    5. On any failure after the backup: restore the YAML backup and re-raise.

    Returns {"ok": True, "agent": <hyphenated name>, "reports_to": <manager name>}.

    Raises:
        FileNotFoundError: registry YAML missing.
        ValueError: validation failure (unknown agent/manager, self-assign, cycle).
    """
    from ai_company.generator import AgentGenerator
    from ai_company.registry.sync import sync_registry

    yaml_path = Path(yaml_path)
    json_path = Path(json_path)

    data = _load_yaml_fresh(yaml_path)
    agents = _get_agents(data)

    agent = _find_agent(agents, agent_ref)
    if agent is None:
        raise ValueError(f"Agent '{agent_ref}' not found in registry")

    agent_id = agent["id"]

    # Resolve manager: virtual root or an existing agent id (normalized).
    if manager_ref in VIRTUAL_ROOTS:
        manager_id = "board"
    else:
        manager = _find_agent(agents, manager_ref)
        if manager is None:
            raise ValueError(f"Manager '{manager_ref}' not found in registry")
        manager_id = manager["id"]

    if agent_id == manager_id:
        raise ValueError("Agent cannot report to itself")

    if _would_create_cycle(agents, agent_id, manager_id):
        raise ValueError("Reassignment would create a cycle")

    backup_path = _backup_yaml(yaml_path)
    logger.info("Registry backed up to %s", backup_path)

    try:
        agent["reports_to"] = manager_id
        _save_yaml(data, yaml_path)
        logger.info("Updated %s reports_to -> %s in %s", agent_id, manager_id, yaml_path)

        generated = AgentGenerator().generate_all()
        logger.info("Regenerated %d agent files", len(generated))

        sync_registry(yaml_path=str(yaml_path), json_path=str(json_path))
        logger.info("Synced registry to %s", json_path)
    except Exception:
        logger.error("Write failed — rolling back registry to %s", backup_path)
        shutil.copy2(backup_path, yaml_path)
        raise

    return {
        "ok": True,
        "agent": agent_id.replace("_", "-"),
        "reports_to": manager_id.replace("_", "-"),
    }


__all__ = ["set_reports_to", "VIRTUAL_ROOTS"]
