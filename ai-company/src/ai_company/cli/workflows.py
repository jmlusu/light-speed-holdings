"""Workflow management commands — now with WorkflowEngine integration."""

from __future__ import annotations

from pathlib import Path

import typer
import yaml

from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Manage company workflows")
console = Console()
WORKFLOWS_DIR = Path("config/workflows")
WORKFLOWS_FILE = WORKFLOWS_DIR / "workflows.yaml"


def _load_workflows() -> dict:
    if not WORKFLOWS_FILE.exists():
        return {"workflows": []}
    with open(WORKFLOWS_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"workflows": []}


@app.command()
def list() -> None:
    """List all registered workflows."""
    from ai_company.registry import load_registry
    from ai_company.workflow.engine import WorkflowEngine

    try:
        registry = load_registry()
    except SystemExit:
        console.print("[red]Failed to load registry[/red]")
        raise typer.Exit(1)

    engine = WorkflowEngine(registry)
    workflows = engine.list_workflows()

    if not workflows:
        console.print("No workflows registered.")
        return

    table = Table(title="Registered Workflows")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Trigger", style="yellow")
    table.add_column("Owner")
    table.add_column("Steps", justify="right")

    for wf in workflows:
        table.add_row(wf["id"], wf["name"], wf["trigger"], wf["owner"], str(wf["steps"]))

    console.print(table)


@app.command()
def run(
    workflow_id: str = typer.Argument(..., help="Workflow ID to execute"),
) -> None:
    """Start a workflow execution."""
    from ai_company.registry import load_registry
    from ai_company.workflow.engine import WorkflowEngine

    try:
        registry = load_registry()
    except SystemExit:
        console.print("[red]Failed to load registry[/red]")
        raise typer.Exit(1)

    engine = WorkflowEngine(registry)
    try:
        instance_id = engine.start(workflow_id)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

    status = engine.get_status(instance_id)
    console.print(f"[green]Started workflow:[/green] {workflow_id}")
    console.print(f"  Instance: {instance_id}")
    if status:
        console.print(f"  Current step: {status['current_step']}")


@app.command()
def status(
    instance_id: str = typer.Argument(..., help="Workflow instance ID"),
) -> None:
    """Show workflow execution status."""
    from ai_company.registry import load_registry
    from ai_company.workflow.engine import WorkflowEngine

    try:
        registry = load_registry()
    except SystemExit:
        console.print("[red]Failed to load registry[/red]")
        raise typer.Exit(1)

    engine = WorkflowEngine(registry)
    status = engine.get_status(instance_id)
    if status is None:
        console.print(f"[red]Instance '{instance_id}' not found[/red]")
        raise typer.Exit(1)

    console.print(f"Workflow: {status['workflow_name']}")
    console.print(f"Status: {status['status']}")
    console.print(f"Step: {status['current_step_index'] + 1}/{status['total_steps']}")
    console.print(f"Current: {status['current_step']}")


@app.command()
def advance(
    instance_id: str = typer.Argument(..., help="Workflow instance ID"),
) -> None:
    """Advance a workflow to its next step."""
    from ai_company.registry import load_registry
    from ai_company.workflow.engine import WorkflowEngine

    try:
        registry = load_registry()
    except SystemExit:
        console.print("[red]Failed to load registry[/red]")
        raise typer.Exit(1)

    engine = WorkflowEngine(registry)
    try:
        result = engine.advance(instance_id)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

    if "error" in result:
        console.print(f"[red]{result['error']}[/red]")
    else:
        console.print(f"[green]{result.get('message', 'Advanced')}[/green]")
        console.print(f"  Current step: {result.get('current_step', 'N/A')}")


@app.command("instances")
def list_instances(
    workflow_id: str = typer.Option("", help="Filter by workflow ID"),
) -> None:
    """List all workflow instances (running, completed, cancelled)."""
    from ai_company.registry import load_registry
    from ai_company.workflow.engine import WorkflowEngine

    try:
        registry = load_registry()
    except SystemExit:
        console.print("[red]Failed to load registry[/red]")
        raise typer.Exit(1)

    engine = WorkflowEngine(registry)
    instances = engine.list_instances(workflow_id)

    if not instances:
        console.print("No workflow instances found.")
        return

    table = Table(title="Workflow Instances")
    table.add_column("Instance ID", style="cyan")
    table.add_column("Workflow", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Step", justify="right")
    table.add_column("Progress", justify="right")

    for inst in instances:
        total = inst["total_steps"]
        completed = inst["completed_steps"]
        progress = f"{completed}/{total}"
        table.add_row(
            inst["instance_id"],
            inst["workflow_name"],
            inst["status"],
            inst.get("current_step") or "-",
            progress,
        )

    console.print(table)


@app.command("complete")
def complete_step(
    instance_id: str = typer.Argument(..., help="Workflow instance ID"),
    result: str = typer.Option("", help="Result of the completed step"),
) -> None:
    """Complete the current step and advance the workflow."""
    from ai_company.registry import load_registry
    from ai_company.workflow.engine import WorkflowEngine

    try:
        registry = load_registry()
    except SystemExit:
        console.print("[red]Failed to load registry[/red]")
        raise typer.Exit(1)

    engine = WorkflowEngine(registry)
    try:
        res = engine.complete_step(instance_id, result)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

    if "error" in res:
        console.print(f"[red]{res['error']}[/red]")
    else:
        console.print(f"[green]{res.get('message', 'Step completed')}[/green]")
        if res.get("current_step"):
            console.print(f"  Current step: {res['current_step']}")
