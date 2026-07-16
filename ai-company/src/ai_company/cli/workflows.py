"""
Workflow management commands.
"""

from typing import Optional, List
from pathlib import Path
import typer
import yaml

app = typer.Typer(help="Manage company workflows")
WORKFLOWS_DIR = Path("company")
WORKFLOWS_FILE = WORKFLOWS_DIR / "workflows.yaml"


def _load_workflows() -> dict:
    if not WORKFLOWS_FILE.exists():
        return {"workflows": []}
    with open(WORKFLOWS_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"workflows": []}


def _save_workflows(data: dict):
    WORKFLOWS_DIR.mkdir(exist_ok=True)
    with open(WORKFLOWS_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


@app.command()
def list():
    """List all registered workflows."""
    data = _load_workflows()
    workflows = data.get("workflows", [])

    if not workflows:
        typer.echo("No workflows registered.")
        return

    typer.echo("")
    typer.echo("Registered Workflows")
    typer.echo("====================")
    for wf in workflows:
        typer.echo(f"  {wf['id']}: {wf['name']}")
        typer.echo(f"    Trigger: {wf.get('trigger', 'manual')}")
        typer.echo(f"    Steps: {len(wf.get('steps', []))}")
        typer.echo("")


@app.command()
def create(
    workflow_id: str = typer.Argument(..., help="Unique workflow ID"),
    name: str = typer.Option(..., help="Workflow name"),
    trigger: str = typer.Option("manual", help="Workflow trigger (manual, scheduled, event)"),
):
    """Create a new workflow."""
    data = _load_workflows()
    workflows = data.get("workflows", [])

    for wf in workflows:
        if wf["id"] == workflow_id:
            typer.echo(f"Error: Workflow '{workflow_id}' already exists.")
            raise typer.Exit(1)

    new_workflow = {
        "id": workflow_id,
        "name": name,
        "trigger": trigger,
        "steps": [],
        "status": "active",
    }
    workflows.append(new_workflow)
    data["workflows"] = workflows
    _save_workflows(data)
    typer.echo(f"Workflow '{name}' created successfully.")


@app.command()
def run(workflow_id: str = typer.Argument(..., help="Workflow ID to execute")):
    """Execute a workflow."""
    data = _load_workflows()
    workflows = data.get("workflows", [])

    workflow = next((wf for wf in workflows if wf["id"] == workflow_id), None)
    if not workflow:
        typer.echo(f"Error: Workflow '{workflow_id}' not found.")
        raise typer.Exit(1)

    typer.echo(f"Executing workflow: {workflow['name']}")
    steps = workflow.get("steps", [])
    for i, step in enumerate(steps, 1):
        typer.echo(f"  Step {i}: {step.get('name', 'Unnamed step')}")
    typer.echo("Workflow execution completed.")


@app.command()
def remove(workflow_id: str = typer.Argument(..., help="Workflow ID to remove")):
    """Remove a workflow."""
    data = _load_workflows()
    workflows = data.get("workflows", [])
    original_len = len(workflows)

    data["workflows"] = [wf for wf in workflows if wf["id"] != workflow_id]

    if len(data["workflows"]) == original_len:
        typer.echo(f"Error: Workflow '{workflow_id}' not found.")
        raise typer.Exit(1)

    _save_workflows(data)
    typer.echo(f"Workflow '{workflow_id}' removed.")
