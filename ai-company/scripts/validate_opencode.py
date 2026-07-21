"""Validate OpenCode agent files for 1.18.4 format compliance.

Checks every .md file in .opencode/agents/ for:
- Valid YAML frontmatter between --- delimiters
- Required fields: description, mode, tools
- tools field has boolean values
- No forbidden fields: name, permission
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

FORBIDDEN_FIELDS = {"name", "permission"}
REQUIRED_FIELDS = {"description", "mode", "tools"}
VALID_MODES = {"primary", "subagent"}
EXPECTED_TOOLS = {"write", "edit", "bash", "read", "grep", "list", "webfetch", "websearch"}


def parse_frontmatter(content: str) -> tuple[dict | None, str]:
    """Extract YAML frontmatter and body from markdown file."""
    if not content.startswith("---"):
        return None, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content

    try:
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2]
        return frontmatter if isinstance(frontmatter, dict) else None, body
    except yaml.YAMLError:
        return None, content


def validate_agent(filepath: Path) -> list[str]:
    """Validate a single agent file. Returns list of errors."""
    errors = []
    content = filepath.read_text(encoding="utf-8")
    frontmatter, _ = parse_frontmatter(content)

    if frontmatter is None:
        errors.append("No valid YAML frontmatter found")
        return errors

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            errors.append(f"Missing required field: {field}")

    # Check forbidden fields
    for field in FORBIDDEN_FIELDS:
        if field in frontmatter:
            errors.append(f"Forbidden field present: {field}")

    # Check mode value
    mode = frontmatter.get("mode")
    if mode and mode not in VALID_MODES:
        errors.append(f"Invalid mode: {mode!r} (expected {VALID_MODES})")

    # Check tools structure
    tools = frontmatter.get("tools")
    if tools is not None:
        if not isinstance(tools, dict):
            errors.append(f"tools must be a dict, got {type(tools).__name__}")
        else:
            # Check for boolean values
            for key, value in tools.items():
                if not isinstance(value, bool):
                    errors.append(f"tools.{key} must be bool, got {type(value).__name__}: {value!r}")

    return errors


def main() -> int:
    """Validate all agent files and report results."""
    agents_dir = Path(".opencode/agents")
    if not agents_dir.exists():
        print(f"ERROR: {agents_dir} not found")
        return 1

    agent_files = sorted(agents_dir.glob("*.md"))
    if not agent_files:
        print(f"ERROR: No .md files found in {agents_dir}")
        return 1

    total = len(agent_files)
    passed = 0
    failed = 0
    warnings = 0

    print(f"Validating {total} agent files in {agents_dir}/\n")

    for filepath in agent_files:
        errors = validate_agent(filepath)
        if errors:
            failed += 1
            print(f"FAIL  {filepath.name}")
            for error in errors:
                print(f"      - {error}")
        else:
            passed += 1

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed, {total} total")
    print(f"{'='*60}")

    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
