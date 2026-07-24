"""Agent management commands.

Uses the new registry system (registry.load_agents()) instead of the
legacy ``company/agent-registry.json`` file.
"""

from __future__ import annotations

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