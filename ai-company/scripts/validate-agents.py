#!/usr/bin/env python
"""Validate agent IDs in company-registry.yaml and generated filenames.

Pre-commit hook that enforces:
1. All agent IDs in company-registry.yaml use hyphen-only (kebab-case) format.
2. Generated filenames in .opencode/agents/ match registry entries exactly.

Exit code 0 if all checks pass, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "company-registry.yaml"
AGENTS_DIR = ROOT / ".opencode" / "agents"

# Regex for kebab-case: lowercase letters, digits, hyphens only.
# Must start with a letter, must not start/end with a hyphen.
KEBAB_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")


def validate_registry_ids() -> list[str]:
    """Check that all agent IDs in the registry use kebab-case."""
    errors: list[str] = []
    if not REGISTRY.exists():
        errors.append(f"Registry not found: {REGISTRY}")
        return errors

    with open(REGISTRY, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    agents = data.get("company", {}).get("agents", [])
    if not agents:
        errors.append("No agents found in registry")
        return errors

    for agent in agents:
        agent_id = agent.get("id", "")
        if not KEBAB_RE.match(agent_id):
            errors.append(
                f"Agent ID '{agent_id}' is not kebab-case "
                f"(use lowercase letters, digits, and hyphens only)"
            )

    return errors


def validate_generated_filenames() -> list[str]:
    """Check that generated filenames match registry agent IDs exactly."""
    errors: list[str] = []
    if not REGISTRY.exists():
        errors.append(f"Registry not found: {REGISTRY}")
        return errors

    if not AGENTS_DIR.exists():
        errors.append(f"Agents directory not found: {AGENTS_DIR}")
        return errors

    with open(REGISTRY, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    agents = data.get("company", {}).get("agents", [])
    if not agents:
        errors.append("No agents found in registry")
        return errors

    registry_ids = {agent["id"] for agent in agents}
    generated_files = {
        f.stem for f in AGENTS_DIR.glob("*.md")
    }

    # Every registry ID must have a matching generated file.
    missing = registry_ids - generated_files
    if missing:
        for mid in sorted(missing):
            errors.append(
                f"Registry ID '{mid}' has no matching file "
                f"in {AGENTS_DIR}/"
            )

    # Every generated file must have a matching registry ID.
    extra = generated_files - registry_ids
    if extra:
        for mid in sorted(extra):
            errors.append(
                f"Generated file '{mid}.md' has no matching "
                f"registry ID"
            )

    return errors


def main() -> int:
    all_errors: list[str] = []

    all_errors.extend(validate_registry_ids())
    all_errors.extend(validate_generated_filenames())

    if all_errors:
        print("Agent ID validation FAILED:", file=sys.stderr)
        for err in all_errors:
            print(f"  ERROR: {err}", file=sys.stderr)
        return 1

    print("Agent ID validation PASSED: all IDs use kebab-case and "
          "generated filenames match registry entries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
