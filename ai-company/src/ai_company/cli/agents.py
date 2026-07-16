import json
from pathlib import Path

import typer

app = typer.Typer(help="Manage AI agents")

REGISTRY_PATH = Path("company/agent-registry.json")


@app.command()
def list(
    type: str = typer.Option("", help="Filter by type: Executive, Board, Specialist"),
    department: str = typer.Option("", help="Filter by department"),
) -> None:
    """List registered AI agents from the single registry."""
    if not REGISTRY_PATH.exists():
        typer.echo("Registry not found. Run 'ai-company generate' first.")
        raise typer.Exit(1)

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    if type:
        registry = [a for a in registry if a.get("type", "").lower() == type.lower()]
    if department:
        registry = [a for a in registry if a.get("department", "").lower() == department.lower()]

    typer.echo("")
    typer.echo(f"{'Role':<35} {'Type':<14} {'Department':<25} {'Reports To':<20}")
    typer.echo("-" * 94)
    for a in registry:
        dept = a.get("department", "") or ""
        typer.echo(f"{a['role']:<35} {a['type']:<14} {dept:<25} {a.get('reportsTo', ''):<20}")
    typer.echo(f"\nTotal: {len(registry)} agents")