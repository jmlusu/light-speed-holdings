"""Executive management commands."""

from __future__ import annotations

from pathlib import Path

import typer
import yaml

app = typer.Typer(help="Manage company executives")
COMPANY_DIR = Path("company")
EXECUTIVES_FILE = COMPANY_DIR / "executives.yaml"


def _load_executives() -> dict:
    """Load executive data from YAML."""
    if not EXECUTIVES_FILE.exists():
        return {"executives": []}
    with open(EXECUTIVES_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"executives": []}


def _save_executives(data: dict) -> None:
    """Persist executive data to YAML."""
    COMPANY_DIR.mkdir(exist_ok=True)
    with open(EXECUTIVES_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


@app.command("list")
def list_executives() -> None:
    """List all company executives."""
    data = _load_executives()
    executives = data.get("executives", [])

    if not executives:
        typer.echo("No executives registered.")
        return

    typer.echo("")
    typer.echo("Company Executives")
    typer.echo("==================")
    for exec in executives:
        typer.echo(f"  {exec['id']}: {exec['title']}")
        typer.echo(f"    Department: {exec.get('department', 'N/A')}")
        typer.echo(f"    Reports To: {exec.get('reports_to', 'N/A')}")
        typer.echo("")


@app.command()
def add(
    executive_id: str = typer.Argument(..., help="Unique executive ID"),
    title: str = typer.Option(..., help="Executive title"),
    department: str = typer.Option(..., help="Department"),
    reports_to: str = typer.Option(..., help="Who this executive reports to"),
    mission: str = typer.Option("", help="Executive mission statement"),
) -> None:
    """Add a new executive."""
    data = _load_executives()
    executives = data.get("executives", [])

    for exec in executives:
        if exec["id"] == executive_id:
            typer.echo(f"Error: Executive '{executive_id}' already exists.")
            raise typer.Exit(1)

    new_executive = {
        "id": executive_id,
        "title": title,
        "department": department,
        "reports_to": reports_to,
        "mission": mission,
        "responsibilities": [],
    }
    executives.append(new_executive)
    data["executives"] = executives
    _save_executives(data)
    typer.echo(f"Executive '{title}' added successfully.")


@app.command()
def remove(executive_id: str = typer.Argument(..., help="Executive ID to remove")) -> None:
    """Remove an executive."""
    data = _load_executives()
    executives = data.get("executives", [])
    original_len = len(executives)

    data["executives"] = [e for e in executives if e["id"] != executive_id]

    if len(data["executives"]) == original_len:
        typer.echo(f"Error: Executive '{executive_id}' not found.")
        raise typer.Exit(1)

    _save_executives(data)
    typer.echo(f"Executive '{executive_id}' removed.")


@app.command()
def hierarchy() -> None:
    """Display the executive hierarchy."""
    data = _load_executives()
    executives = data.get("executives", [])

    if not executives:
        typer.echo("No executives registered.")
        return

    typer.echo("")
    typer.echo("Executive Hierarchy")
    typer.echo("===================")

    roots = [e for e in executives if e.get("reports_to") == "human_operator"]
    for root in roots:
        _print_hierarchy(root, executives, indent=0)
    typer.echo("")


def _print_hierarchy(
    executive: dict,
    all_executives: list[dict],
    indent: int,
) -> None:
    """Recursively print the executive hierarchy tree."""
    prefix = "  " * indent
    typer.echo(f"{prefix}{executive['title']} ({executive['id']})")

    direct_reports = executive.get("direct_reports", [])
    for report_id in direct_reports:
        report = next((e for e in all_executives if e["id"] == report_id), None)
        if report:
            _print_hierarchy(report, all_executives, indent + 1)
