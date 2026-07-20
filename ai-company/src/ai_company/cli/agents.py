"""Agent management commands.

Uses the new registry system (registry.load_registry()) instead of the
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
    from ai_company.registry import load_registry

    try:
        registry = load_registry()
    except SystemExit:
        typer.echo("Registry not found or invalid. Run 'ai-company company run' first.")
        raise typer.Exit(1)

    # Build a unified agent list from executives + board + specialists
    agents: list[dict[str, str]] = []

    for ex in registry.executives:
        agents.append({
            "role": ex.title or ex.name,
            "type": "Executive",
            "department": ex.department,
            "reports_to": ex.reports_to,
        })

    for bm in registry.board:
        agents.append({
            "role": bm.role or bm.name,
            "type": "Board",
            "department": "",
            "reports_to": "board_of_directors",
        })

    for spec in registry.specialists:
        agents.append({
            "role": spec.name or spec.id,
            "type": "Specialist",
            "department": spec.department,
            "reports_to": spec.reports_to,
        })

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
