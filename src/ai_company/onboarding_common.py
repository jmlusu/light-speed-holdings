"""Shared definitions for agent onboarding (HR manager + services).

Both onboarding implementations use the same lifecycle states and labels,
but intentionally keep separate transition tables: the services flow allows
``FAILED -> GENERATING`` (retry), while HR treats ``FAILED`` as terminal.
Only the identical pieces live here: the state enum, the display labels,
the registry-entry converter, and the raw registry YAML helpers.
"""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

import yaml


class OnboardingState(str, Enum):
    """Lifecycle states for an agent onboarding request.

    Maps to SOP-HR-001 steps:
      requested (step 1) → config_review (step 2) → security_review (step 3)
      → generating (step 4) → testing (step 5) → approval (step 6)
      → active (step 7)
    """

    REQUESTED = "requested"
    CONFIG_REVIEW = "config_review"
    SECURITY_REVIEW = "security_review"
    GENERATING = "generating"
    TESTING = "testing"
    APPROVAL = "approval"
    ACTIVE = "active"
    REJECTED = "rejected"
    FAILED = "failed"
    ARCHIVED = "archived"


# Human-readable labels for CLI display.
STATE_LABELS: dict[OnboardingState, str] = {
    OnboardingState.REQUESTED: "Staffing request submitted",
    OnboardingState.CONFIG_REVIEW: "Agent configuration under review",
    OnboardingState.SECURITY_REVIEW: "Security review (CTO sign-off)",
    OnboardingState.GENERATING: "Generating agent files",
    OnboardingState.TESTING: "Running validation tests",
    OnboardingState.APPROVAL: "Awaiting human approval",
    OnboardingState.ACTIVE: "Agent deployed and active",
    OnboardingState.REJECTED: "Request rejected",
    OnboardingState.FAILED: "Generation/testing failed",
    OnboardingState.ARCHIVED: "Agent archived",
}


def request_to_registry_entry(req: Any) -> dict[str, Any]:
    """Convert an onboarding request to a company-registry.yaml agent entry."""
    entry: dict[str, Any] = {
        "id": req.agent_id,
        "name": req.name,
        "title": req.role,
        "description": req.role,
        "type": req.agent_type,
        "department": req.department,
        "reports_to": req.reports_to,
        "responsibilities": req.responsibilities,
        "guidelines": req.guidelines,
        "tools": req.tools,
    }
    return entry


def load_registry_yaml(path: Path) -> dict[str, Any]:
    """Load the raw company-registry.yaml."""
    if not path.exists():
        raise FileNotFoundError(f"Registry not found: {path}")
    with open(path, encoding="utf-8") as f:
        data: dict[str, Any] = yaml.safe_load(f)
    if data is None:
        return {"company": {"name": "AI Company", "agents": []}}
    return data


def save_registry_yaml(data: dict[str, Any], path: Path) -> None:
    """Persist the raw company-registry.yaml."""
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def backup_registry(path: Path) -> Path:
    """Create a timestamped backup of company-registry.yaml for rollback."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = path.with_suffix(f".yaml.bak.{timestamp}")
    shutil.copy2(path, backup_path)
    return backup_path


def get_existing_ids(data: dict[str, Any]) -> set[str]:
    """Extract all agent IDs from the registry."""
    agents = data.get("company", {}).get("agents", [])
    return {a.get("id", "") for a in agents if isinstance(a, dict)}
