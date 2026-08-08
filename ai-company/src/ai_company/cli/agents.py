"""Agent management commands.

Uses the new registry system (registry.load_registry()) instead of the
legacy ``company/agent-registry.json`` file.
"""

from __future__ import annotations

import typer

from ai_company.executor.context import Severity, parse_agent_spec

app = typer.Typer(help="Manage AI agents")


@app.command("list")
def list_agents(
    type: str = typer.Option("", help="Filter by type: Executive, Board, Specialist"),
    department: str = typer.Option("", help="Filter by department"),
) -> None:
    """List registered AI agents from the unified registry."""
    from ai_company.registry import load_registry

    try:
        registry = load_registry()
    except SystemExit:
        typer.echo("Registry not found or invalid. Run 'ai-company company run' first.")
        raise typer.Exit(1) from None

    # Build a unified agent list from executives + board + specialists
    agents: list[dict[str, str]] = []

    for ex in registry.executives:
        agents.append(
            {
                "role": ex.title or ex.name,
                "type": "Executive",
                "department": ex.department,
                "reports_to": ex.reports_to,
            }
        )

    for bm in registry.board:
        agents.append(
            {
                "role": bm.role or bm.name,
                "type": "Board",
                "department": "",
                "reports_to": "board_of_directors",
            }
        )

    for spec in registry.specialists:
        agents.append(
            {
                "role": spec.name or spec.id,
                "type": "Specialist",
                "department": spec.department,
                "reports_to": spec.reports_to,
            }
        )

    # Apply filters
    if type:
        agents = [a for a in agents if a["type"].lower() == type.lower()]
    if department:
        agents = [a for a in agents if a["department"].lower() == department.lower()]

    typer.echo("")
    typer.echo(f"{'Role':<35} {'Type':<14} {'Department':<25} {'Reports To':<20}")
    typer.echo("-" * 94)
    for a in agents:
        dept = a.get("department", "") or ""
        typer.echo(f"{a['role']:<35} {a['type']:<14} {dept:<25} {a.get('reports_to', ''):<20}")
    typer.echo(f"\nTotal: {len(agents)} agents")


@app.command("validate")
def validate_agents(
    agent: str = typer.Option(
        "",
        "--agent",
        help="Validate a single agent by name (omit to validate all spec files)",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit a machine-readable JSON report instead of a table",
    ),
    agents_dir: str = typer.Option(
        ".opencode/agents",
        help="Directory containing agent .md files",
    ),
) -> None:
    """Validate agent spec cards for required fields (mission, responsibilities, tools).

    Scans every ``.opencode/agents/*.md`` file by default, parses each spec with
    ``parse_agent_spec()`` and runs ``AgentContext.validate()``. Prints a summary
    report (total agents, valid count, issues found, per-agent issues) and exits
    non-zero when any ERROR-severity issue is found, so CI can gate on it.
    """
    import json
    import logging
    from pathlib import Path

    # Machine-readable output must not be contaminated by log records emitted
    # by the validation layer (they are already summarized in the JSON report).
    if json_output:
        logging.getLogger("ai_company.executor.context").disabled = True

    agents_path = Path(agents_dir)
    if not agents_path.is_dir():
        typer.echo(f"Agents directory not found: {agents_dir}")
        raise typer.Exit(1)

    if agent:
        agent_files = [agents_path / f"{agent}.md"]
    else:
        agent_files = sorted(agents_path.glob("*.md"))
        if not agent_files:
            typer.echo(f"No agent spec files found in {agents_dir}")
            raise typer.Exit(1)

    report: list[dict] = []
    errors = 0
    warnings = 0
    valid_count = 0

    for agent_file in agent_files:
        if not agent_file.exists():
            report.append(
                {
                    "name": agent_file.stem,
                    "valid": False,
                    "issues": [
                        {
                            "field": "file",
                            "severity": Severity.ERROR.value,
                            "message": f"Agent spec not found: {agent_file.name}",
                        }
                    ],
                }
            )
            errors += 1
            continue

        agent_name = agent_file.stem
        context = parse_agent_spec(agent_name, str(agents_path))
        raw_issues = context.validate()

        issues = [
            {
                "field": issue.field,
                "severity": issue.severity.value,
                "message": issue.message,
            }
            for issue in raw_issues
        ]
        agent_errors = sum(1 for i in raw_issues if i.severity is Severity.ERROR)
        agent_warnings = sum(1 for i in raw_issues if i.severity is Severity.WARNING)
        valid = agent_errors == 0

        errors += agent_errors
        warnings += agent_warnings
        if valid:
            valid_count += 1

        report.append({"name": agent_name, "valid": valid, "issues": issues})

    total = len(report)
    invalid = total - valid_count

    if json_output:
        typer.echo(
            json.dumps(
                {
                    "total_agents": total,
                    "valid": valid_count,
                    "invalid": invalid,
                    "errors": errors,
                    "warnings": warnings,
                    "agents": report,
                },
                indent=2,
            )
        )
    else:
        _print_validation_report(report, total, valid_count, invalid, errors, warnings)

    if errors > 0:
        raise typer.Exit(1)


def _print_validation_report(
    report: list[dict],
    total: int,
    valid: int,
    invalid: int,
    errors: int,
    warnings: int,
) -> None:
    """Print a human-readable validation report to stdout."""
    typer.echo("")
    typer.echo(f"{'Agent':<35} {'Status':<8} {'Errors':<8} {'Warnings':<9}")
    typer.echo("-" * 60)
    for entry in report:
        agent_errors = sum(1 for i in entry["issues"] if i["severity"] == "ERROR")
        agent_warnings = sum(1 for i in entry["issues"] if i["severity"] == "WARNING")
        status = "OK" if entry["valid"] else "FAILED"
        typer.echo(f"{entry['name']:<35} {status:<8} {agent_errors:<8} {agent_warnings:<9}")
        for issue in entry["issues"]:
            typer.echo(f"    {issue['severity']} {issue['field']}: {issue['message']}")
    typer.echo("")
    typer.echo(
        f"Validated: {total} | Valid: {valid} | Invalid: {invalid} "
        f"| Errors: {errors} | Warnings: {warnings}"
    )
