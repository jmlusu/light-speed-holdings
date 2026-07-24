"""Agent management commands.

Uses the new registry system (registry.load_agents()) instead of the
legacy ``company/agent-registry.json`` file.
"""

from __future__ import annotations

from pathlib import Path

import typer

app = typer.Typer(help="Manage AI agents")


@app.command("list")
def list_agents(
    type: str = typer.Option("", help="Filter by type: Executive, Board, Specialist"),
    department: str = typer.Option("", help="Filter by department"),
) -> None:
    """List registered AI agents from the unified registry."""
    from ai_company.registry import load_agents

    try:
        agents = load_agents()
    except SystemExit:
        typer.echo("Registry not found or invalid. Run 'ai-company company run' first.")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error loading agents: {e}")
        raise typer.Exit(1)

    # Build a unified agent list
    agent_list: list[dict[str, str]] = []

    for a in agents:
        agent_type = a.get("type", "default")
        if agent_type == "executive":
            display_type = "Executive"
        elif agent_type == "board":
            display_type = "Board"
        else:
            display_type = "Specialist"

        agent_list.append({
            "role": a.get("title") or a.get("name") or a["id"],
            "type": display_type,
            "department": a.get("department", ""),
            "reports_to": a.get("reports_to", ""),
        })

    # Apply filters
    if type:
        agent_list = [a for a in agent_list if a["type"].lower() == type.lower()]
    if department:
        agent_list = [a for a in agent_list if a["department"].lower() == department.lower()]

    typer.echo("")
    typer.echo(f"{'Role':<35} {'Type':<14} {'Department':<25} {'Reports To':<20}")
    typer.echo("-" * 94)
    for a in agent_list:
        dept = a.get("department", "") or ""
        typer.echo(f"{a['role']:<35} {a['type']:<14} {dept:<25} {a.get('reports_to', ''):<20}")
    typer.echo(f"\nTotal: {len(agent_list)} agents")


@app.command("validate")
def validate_agents(
    agents_dir: str = typer.Option(
        ".opencode/agents",
        help="Path to the directory containing agent spec .md files",
    ),
) -> None:
    """Validate agent spec files for required fields and correct types."""
    agents_path = Path(agents_dir)

    if not agents_path.exists():
        typer.echo(f"Agents directory not found: {agents_dir}")
        raise typer.Exit(1)

    spec_files = sorted(agents_path.glob("*.md"))

    if not spec_files:
        typer.echo("No agent spec files found in the directory.")
        raise typer.Exit(1)

    from ai_company.executor.context import parse_agent_spec

    passed = 0
    failed = 0

    for spec_file in spec_files:
        agent_name = spec_file.stem
        ctx = parse_agent_spec(agent_name, str(agents_path))
        errors = ctx.validate()

        if errors:
            failed += 1
            typer.echo(f"FAIL: {agent_name}")
            for err in errors:
                typer.echo(f"  - {err}")
        else:
            passed += 1
            typer.echo(f"PASS: {agent_name}")

    typer.echo("")
    typer.echo(f"{passed} passed, {failed} failed out of {passed + failed} agents")

    if failed > 0:
        raise typer.Exit(1)