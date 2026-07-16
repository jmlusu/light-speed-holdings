"""
Department management commands.
"""

from pathlib import Path
import typer
import yaml

app = typer.Typer(help="Manage company departments")
COMPANY_DIR = Path("company")
DEPARTMENTS_FILE = COMPANY_DIR / "departments.yaml"


def _load_departments() -> dict:
    if not DEPARTMENTS_FILE.exists():
        return {"departments": []}
    with open(DEPARTMENTS_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"departments": []}


def _save_departments(data: dict):
    COMPANY_DIR.mkdir(exist_ok=True)
    with open(DEPARTMENTS_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


@app.command()
def list():
    """List all company departments."""
    data = _load_departments()
    departments = data.get("departments", [])

    if not departments:
        typer.echo("No departments registered.")
        return

    typer.echo("")
    typer.echo("Company Departments")
    typer.echo("===================")
    for dept in departments:
        typer.echo(f"  {dept['id']}: {dept['name']}")
        typer.echo(f"    Executive: {dept.get('executive', 'N/A')}")
        typer.echo(f"    Purpose: {dept.get('purpose', 'N/A')}")
        typer.echo("")


@app.command()
def add(
    department_id: str = typer.Argument(..., help="Unique department ID"),
    name: str = typer.Option(..., help="Department name"),
    executive: str = typer.Option(..., help="Executive in charge"),
    purpose: str = typer.Option("", help="Department purpose"),
):
    """Add a new department."""
    data = _load_departments()
    departments = data.get("departments", [])

    for dept in departments:
        if dept["id"] == department_id:
            typer.echo(f"Error: Department '{department_id}' already exists.")
            raise typer.Exit(1)

    new_department = {
        "id": department_id,
        "name": name,
        "executive": executive,
        "purpose": purpose,
        "agents": [],
    }
    departments.append(new_department)
    data["departments"] = departments
    _save_departments(data)
    typer.echo(f"Department '{name}' added successfully.")


@app.command()
def remove(department_id: str = typer.Argument(..., help="Department ID to remove")):
    """Remove a department."""
    data = _load_departments()
    departments = data.get("departments", [])
    original_len = len(departments)

    data["departments"] = [d for d in departments if d["id"] != department_id]

    if len(data["departments"]) == original_len:
        typer.echo(f"Error: Department '{department_id}' not found.")
        raise typer.Exit(1)

    _save_departments(data)
    typer.echo(f"Department '{department_id}' removed.")


@app.command()
def agents(department_id: str = typer.Argument(..., help="Department ID")):
    """List agents in a department."""
    data = _load_departments()
    departments = data.get("departments", [])

    dept = next((d for d in departments if d["id"] == department_id), None)
    if not dept:
        typer.echo(f"Error: Department '{department_id}' not found.")
        raise typer.Exit(1)

    agents_list = dept.get("agents", [])
    typer.echo("")
    typer.echo(f"Agents in {dept['name']}")
    typer.echo("=" * (len(dept["name"]) + 10))

    if not agents_list:
        typer.echo("  No agents in this department.")
    else:
        for agent in agents_list:
            typer.echo(f"  - {agent}")
    typer.echo("")
