"""CLI command for validating agent naming conventions and config references."""

from __future__ import annotations

from pathlib import Path

import typer
import yaml

app = typer.Typer(help="Validate agent naming conventions and config references")


def _scan_yaml_for_agent_refs(filepath: Path) -> list[tuple[int, str, str]]:
    """Scan a YAML file for fields that look like agent references.

    Returns list of (line_number, field_name, value) tuples.
    Heuristic: looks for common agent-reference field names and string values
    that look like agent IDs (lowercase, may contain hyphens/underscores).
    """
    refs: list[tuple[int, str, str]] = []
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return refs

    # Fields that typically contain agent references
    agent_fields = {
        "owner",
        "executive",
        "chair",
        "authority",
        "reports_to",
        "required_approvals",
        "required_attendees",
        "members",
        "direct_reports",
    }

    for line_no, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # Parse "field_name: value" or "field_name: [values]"
        if ":" not in stripped:
            continue
        key_part, _, val_part = stripped.partition(":")
        key = key_part.strip().strip('"').strip("'")
        val = val_part.strip()

        if key not in agent_fields:
            continue

        # Handle inline list: ["agent1", "agent2"]
        if val.startswith("["):
            try:
                items = yaml.safe_load(val)
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, str):
                            refs.append((line_no, key, item))
            except yaml.YAMLError:
                pass
        elif val and val != "[]":
            # Single quoted or unquoted value
            clean_val = val.strip('"').strip("'")
            if clean_val and clean_val != "all_board":
                refs.append((line_no, key, clean_val))

    return refs


def _collect_config_files(config_dir: Path) -> list[Path]:
    """Recursively collect all YAML files under config directory."""
    return sorted(config_dir.rglob("*.yaml"))


@app.command()
def naming(
    registry_path: str = typer.Option(
        "company-registry.yaml",
        help="Path to the agent registry YAML",
    ),
) -> None:
    """Check that registry IDs follow underscore convention and generated filenames follow hyphen convention."""
    from ai_company.generator import AgentGenerator

    gen = AgentGenerator(registry_path=registry_path)
    data = gen.load_registry()

    if isinstance(data, list):
        agents = data
    else:
        agents = data.get("company", {}).get("agents", [])

    errors: list[str] = []
    for agent in agents:
        agent_id = agent.get("id", "")
        # Registry IDs should use underscores (Python convention)
        if "-" in agent_id:
            errors.append(f"Registry ID '{agent_id}' uses hyphens — should use underscores")

        # Generated filename should use hyphens (OpenCode convention)
        expected_filename = agent_id.replace("_", "-") + ".md"
        actual_path = gen.output_dir / expected_filename
        if not actual_path.exists():
            # Check if the underscore version exists (backward compat)
            underscore_path = gen.output_dir / f"{agent_id}.md"
            if underscore_path.exists():
                errors.append(
                    f"File '{agent_id}.md' exists but should be '{expected_filename}' "
                    f"(hyphens for OpenCode)"
                )
            else:
                errors.append(
                    f"Expected '{expected_filename}' not found in {gen.output_dir}"
                )

    if errors:
        typer.echo(f"Naming errors found: {len(errors)}", err=True)
        for e in errors:
            typer.echo(f"  ERROR: {e}", err=True)
        raise typer.Exit(1)
    else:
        typer.echo("All naming conventions are correct.")


@app.command()
def references(
    config_dir: str = typer.Option(
        "config",
        help="Path to the config directory",
    ),
    registry_path: str = typer.Option(
        "company-registry.yaml",
        help="Path to the agent registry YAML",
    ),
) -> None:
    """Check that all agent references in config files resolve to generated agent files."""
    from ai_company.generator import AgentGenerator

    config_path = Path(config_dir)
    if not config_path.exists():
        typer.echo(f"Config directory not found: {config_path}", err=True)
        raise typer.Exit(1)

    # Build set of known agent names (hyphenated filenames without .md)
    gen = AgentGenerator(registry_path=registry_path)
    generated = gen.generate_all(clean=False)
    known_agents: set[str] = {p.stem for p in generated}

    # Also add common role-based aliases that the system understands
    known_agents.update({
        "department_executive",
        "department-executive",
        "team_lead",
        "team-lead",
        "hiring_manager",
        "hiring-manager",
        "hiring-manager-chro",
        "department-exec-chro",
        "requestor",
        "peer_review",
        "peer-review",
        "all_board",
        "all-board",
        "board",
        "department_heads",
        "department-heads",
        "engineering_team",
        "engineering-team",
        "ceo",
        "human-ceo-board",
        "cfo-human-ceo",
        "cto-ciso",
        # Governance role labels (human-readable, not agent IDs)
        "Board of Directors",
        "Chief of Staff",
        "Department Executive",
        "Agent",
    })

    errors: list[str] = []
    warnings: list[str] = []
    config_files = _collect_config_files(config_path)

    for filepath in config_files:
        refs = _scan_yaml_for_agent_refs(filepath)
        for line_no, field, ref in refs:
            # Skip compound references (e.g., "cfo-human-ceo")
            # These are multi-agent authority specs, not single agent IDs
            if "-" in ref and len(ref.split("-")) > 2:
                # Compound reference — check individual parts
                parts = ref.split("-")
                for part in parts:
                    if part and part not in known_agents:
                        warnings.append(
                            f"{filepath.relative_to(config_path.parent)}:{line_no} "
                            f"field '{field}': compound part '{part}' in '{ref}' "
                            f"not a known agent"
                        )
                continue

            if ref not in known_agents:
                # Check if underscore version exists (naming mismatch)
                underscore_version = ref.replace("-", "_")
                if underscore_version in known_agents:
                    errors.append(
                        f"{filepath.relative_to(config_path.parent)}:{line_no} "
                        f"field '{field}': '{ref}' should be '{ref}' "
                        f"(underscore version '{underscore_version}' exists in registry)"
                    )
                else:
                    errors.append(
                        f"{filepath.relative_to(config_path.parent)}:{line_no} "
                        f"field '{field}': '{ref}' does not resolve to a known agent"
                    )

    if warnings:
        typer.echo(f"Warnings: {len(warnings)}")
        for w in warnings:
            typer.echo(f"  WARN: {w}")

    if errors:
        typer.echo(f"Reference errors found: {len(errors)}", err=True)
        for e in errors:
            typer.echo(f"  ERROR: {e}", err=True)
        raise typer.Exit(1)
    else:
        typer.echo("All config references resolve correctly.")


_REQUIRED_CONFIG_FILES = [
    "orchestrator/approvals.yaml",
    "orchestrator/escalation.yaml",
    "orchestrator/scheduler.yaml",
    "company/agent-registry.json",
    "company/departments.yaml",
    "company/config/kpis.yaml",
    "config/company/kpis.yaml",
    "config/company/budget.yaml",
    "config/company/strategy.yaml",
    "config/company/vision.yaml",
    "config/company/company.yaml",
    "config/company/culture.yaml",
    "config/company/governance.yaml",
    "config/company/policies.yaml",
    "config/decision/approval_matrix.yaml",
    "config/decision/risk_matrix.yaml",
    "config/decision/decision_tree.yaml",
    "config/departments/departments.yaml",
    "config/workflows/workflows.yaml",
    "config/board/meetings.yaml",
    "config/board/committees.yaml",
    "config/board/voting.yaml",
    "config/routing.yaml",
    "config/tool_allowlist.yaml",
]


def _check_stale_dates(filepath: Path) -> list[str]:
    """Return warnings for any dates from 2024 or earlier in the file."""
    warnings: list[str] = []
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return warnings
    for line_no, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "2024" in stripped or "2023" in stripped or "2022" in stripped:
            warnings.append(f"  line {line_no}: possibly stale date -> {stripped}")
    return warnings


@app.command()
def config(
    project_root: str = typer.Option(
        ".",
        help="Path to the ai-company project root",
    ),
) -> None:
    """Validate all config files: parseability, existence, stale dates."""
    root = Path(project_root)
    passed = 0
    failed = 0
    warned = 0

    typer.echo("Config Validation Report")
    typer.echo("=" * 60)

    for rel_path in _REQUIRED_CONFIG_FILES:
        filepath = root / rel_path
        if not filepath.exists():
            typer.echo(f"  FAIL  {rel_path} -- FILE NOT FOUND")
            failed += 1
            continue

        if filepath.suffix == ".yaml" or filepath.suffix == ".yml":
            try:
                import yaml
                with open(filepath, "r", encoding="utf-8") as f:
                    yaml.safe_load(f)
            except Exception as exc:
                typer.echo(f"  FAIL  {rel_path} -- INVALID YAML: {exc}")
                failed += 1
                continue

        stale = _check_stale_dates(filepath)
        if stale:
            typer.echo(f"  WARN  {rel_path} -- stale dates detected:")
            for w in stale:
                typer.echo(w)
            warned += 1
        else:
            typer.echo(f"  OK    {rel_path}")

        passed += 1

    typer.echo("=" * 60)
    typer.echo(f"Summary: {passed} passed, {failed} failed, {warned} warnings")

    # Write report file
    import json
    from datetime import datetime

    report = {
        "validated_at": datetime.now().isoformat(),
        "passed": passed,
        "failed": failed,
        "warnings": warned,
        "files_checked": len(_REQUIRED_CONFIG_FILES),
    }
    report_path = root / "orchestrator" / "config-validation-report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    typer.echo(f"\nReport written to {report_path}")

    if failed:
        raise typer.Exit(1)


@app.command()
def all(
    registry_path: str = typer.Option(
        "company-registry.yaml",
        help="Path to the agent registry YAML",
    ),
    config_dir: str = typer.Option(
        "config",
        help="Path to the config directory",
    ),
) -> None:
    """Run all validation checks: naming conventions + config references."""
    from ai_company.generator import AgentGenerator

    typer.echo("Running all validation checks...")
    typer.echo("=" * 50)

    # 1. Generate agents
    gen = AgentGenerator(registry_path=registry_path)
    generated = gen.generate_all(clean=False)
    typer.echo(f"Generated agents: {len(generated)}")

    # 2. Validate generated files for OpenCode compliance
    gen_errors = gen.validate_generated()
    if gen_errors:
        typer.echo(f"\nGenerated file errors: {len(gen_errors)}")
        for e in gen_errors:
            typer.echo(f"  ERROR: {e['file']}: {e['error']}")
    else:
        typer.echo("Generated files: All valid (OpenCode 1.18.4 compliant)")

    # 3. Check naming conventions
    typer.echo("\n--- Naming Convention Check ---")
    naming_errors: list[str] = []
    data = gen.load_registry()
    if isinstance(data, list):
        agents = data
    else:
        agents = data.get("company", {}).get("agents", [])

    known_agents: set[str] = {p.stem for p in generated}

    # Add role-based aliases and governance labels
    known_agents.update({
        "department_executive", "department-executive",
        "team_lead", "team-lead",
        "hiring_manager", "hiring-manager",
        "hiring-manager-chro", "department-exec-chro",
        "requestor", "peer_review", "peer-review",
        "all_board", "all-board", "board",
        "department_heads", "department-heads",
        "engineering_team", "engineering-team",
        "ceo", "human-ceo-board", "cfo-human-ceo", "cto-ciso",
        "Board of Directors", "Chief of Staff",
        "Department Executive", "Agent",
    })

    for agent in agents:
        agent_id = agent.get("id", "")
        if "-" in agent_id:
            naming_errors.append(f"Registry ID '{agent_id}' uses hyphens")

    if naming_errors:
        for err in naming_errors:
            typer.echo(f"  ERROR: {err}")
    else:
        typer.echo("Registry IDs: All use underscores (correct)")

    # 4. Check config references
    typer.echo("\n--- Config Reference Check ---")
    config_path = Path(config_dir)
    ref_errors: list[str] = []
    if config_path.exists():
        config_files = _collect_config_files(config_path)
        for filepath in config_files:
            refs = _scan_yaml_for_agent_refs(filepath)
            for line_no, field, ref in refs:
                # Skip compound references
                if "-" in ref and len(ref.split("-")) > 2:
                    continue
                if ref not in known_agents:
                    ref_errors.append(
                        f"{filepath.relative_to(config_path.parent)}:{line_no} "
                        f"'{ref}' in '{field}'"
                    )

        if ref_errors:
            for err in ref_errors:
                typer.echo(f"  ERROR: {err}")
        else:
            typer.echo("Config references: All resolve correctly")
    else:
        typer.echo(f"Config directory not found: {config_path}")

    # 5. Summary
    total_errors = len(gen_errors) + len(naming_errors) + len(ref_errors)
    typer.echo("\n" + "=" * 50)
    if total_errors:
        typer.echo(f"VALIDATION FAILED: {total_errors} error(s) found")
        raise typer.Exit(1)
    else:
        typer.echo("All checks passed!")
