"""
Specialist agent management commands.
"""

from pathlib import Path
import typer
import yaml
from datetime import datetime

app = typer.Typer(help="Manage specialist agents")
SPECIALISTS_DIR = Path("specialists")


def _load_specialists() -> dict:
    specialists_file = SPECIALISTS_DIR / "registry.yaml"
    if not specialists_file.exists():
        return {"specialists": []}
    with open(specialists_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"specialists": []}


def _save_specialists(data: dict):
    SPECIALISTS_DIR.mkdir(exist_ok=True)
    specialists_file = SPECIALISTS_DIR / "registry.yaml"
    with open(specialists_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


@app.command()
def list():
    """List all specialist agents."""
    data = _load_specialists()
    specialists = data.get("specialists", [])

    if not specialists:
        typer.echo("No specialists registered.")
        return

    typer.echo("")
    typer.echo("Specialist Agents")
    typer.echo("=================")
    for spec in specialists:
        status = spec.get("status", "active")
        typer.echo(f"  {spec['id']}: {spec['title']} [{status}]")
        typer.echo(f"    Department: {spec.get('department', 'N/A')}")
        typer.echo(f"    Reports To: {spec.get('reports_to', 'N/A')}")
        typer.echo("")


@app.command()
def add(
    specialist_id: str = typer.Argument(..., help="Unique specialist ID"),
    title: str = typer.Option(..., help="Specialist title"),
    department: str = typer.Option(..., help="Department"),
    reports_to: str = typer.Option(..., help="Executive this specialist reports to"),
    specialization: str = typer.Option("", help="Area of specialization"),
):
    """Add a new specialist agent."""
    data = _load_specialists()
    specialists = data.get("specialists", [])

    for spec in specialists:
        if spec["id"] == specialist_id:
            typer.echo(f"Error: Specialist '{specialist_id}' already exists.")
            raise typer.Exit(1)

    new_specialist = {
        "id": specialist_id,
        "title": title,
        "department": department,
        "reports_to": reports_to,
        "specialization": specialization,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "capabilities": [],
        "permissions": {"read": True, "write": True, "execute": True},
    }
    specialists.append(new_specialist)
    data["specialists"] = specialists
    _save_specialists(data)
    typer.echo(f"Specialist '{title}' added successfully.")


@app.command()
def remove(specialist_id: str = typer.Argument(..., help="Specialist ID to remove")):
    """Remove a specialist agent."""
    data = _load_specialists()
    specialists = data.get("specialists", [])
    original_len = len(specialists)

    data["specialists"] = [s for s in specialists if s["id"] != specialist_id]

    if len(data["specialists"]) == original_len:
        typer.echo(f"Error: Specialist '{specialist_id}' not found.")
        raise typer.Exit(1)

    _save_specialists(data)
    typer.echo(f"Specialist '{specialist_id}' removed.")


@app.command()
def assign_task(
    specialist_id: str = typer.Argument(..., help="Specialist ID"),
    task_id: str = typer.Option(..., help="Task ID to assign"),
    instruction: str = typer.Option(..., help="Task instruction"),
):
    """Assign a task to a specialist."""
    data = _load_specialists()
    specialists = data.get("specialists", [])

    specialist = next((s for s in specialists if s["id"] == specialist_id), None)
    if not specialist:
        typer.echo(f"Error: Specialist '{specialist_id}' not found.")
        raise typer.Exit(1)

    from ai_company.orchestrator.message_bus import MessageBus
    from ai_company.models.task import Task

    bus = MessageBus()
    task = Task(
        id=task_id,
        sender_id="human_operator",
        receiver_id=specialist_id,
        instruction=instruction,
    )
    bus.send_task(task)
    typer.echo(f"Task '{task_id}' assigned to '{specialist_id}'.")


@app.command()
def by_department(department: str = typer.Argument(..., help="Department name")):
    """List specialists by department."""
    data = _load_specialists()
    specialists = data.get("specialists", [])

    dept_specialists = [s for s in specialists if s.get("department", "").lower() == department.lower()]

    if not dept_specialists:
        typer.echo(f"No specialists found in department '{department}'.")
        return

    typer.echo("")
    typer.echo(f"Specialists in {department}")
    typer.echo("=" * (len(department) + 15))
    for spec in dept_specialists:
        typer.echo(f"  - {spec['title']} ({spec['id']})")
    typer.echo("")
