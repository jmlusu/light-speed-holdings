"""CLI commands for the autonomous executor."""

from __future__ import annotations

import json
from pathlib import Path

import typer

app = typer.Typer(help="Autonomous task execution loop")


@app.command()
def start(
    poll_interval: float = typer.Option(5.0, help="Seconds between polling cycles"),
    config: str = typer.Option("company/models.yaml", help="Path to models config"),
    registry: str = typer.Option("company/agent-registry.json", help="Path to agent registry"),
) -> None:
    """Start the continuous execution loop."""
    from ai_company.executor.loop import Executor

    executor = Executor(
        poll_interval=poll_interval,
        config_path=config,
        registry_path=registry,
    )
    executor.start()


@app.command()
def tick(
    config: str = typer.Option("company/models.yaml", help="Path to models config"),
    registry: str = typer.Option("company/agent-registry.json", help="Path to agent registry"),
) -> None:
    """Process all pending tasks in a single pass."""
    from ai_company.executor.loop import Executor

    executor = Executor(
        config_path=config,
        registry_path=registry,
    )
    count = executor.tick()
    typer.echo(f"Processed {count} task(s).")
    typer.echo(f"Stats: {json.dumps(executor.stats.to_dict(), indent=2)}")


@app.command()
def run_task(
    task_id: str = typer.Argument(..., help="Task ID to execute"),
    config: str = typer.Option("company/models.yaml", help="Path to models config"),
    registry: str = typer.Option("company/agent-registry.json", help="Path to agent registry"),
) -> None:
    """Execute a single task by ID."""

    from ai_company.executor.loop import Executor
    from ai_company.models.task import Task

    executor = Executor(
        config_path=config,
        registry_path=registry,
    )

    # Load the specific task
    inbox_path = Path(executor.bus.storage_path)
    if not inbox_path.exists():
        typer.echo("No inbox found.")
        raise typer.Exit(1)

    tasks = json.loads(inbox_path.read_text(encoding="utf-8"))
    task_data = next((t for t in tasks if t.get("id") == task_id), None)

    if not task_data:
        typer.echo(f"Task '{task_id}' not found.")
        raise typer.Exit(1)

    task = Task(**task_data)
    typer.echo(f"Executing task: {task.instruction[:80]}...")
    executor._process_task(task)
    typer.echo(f"Done. Stats: {json.dumps(executor.stats.to_dict(), indent=2)}")


@app.command()
def status() -> None:
    """Show executor status and pending tasks."""
    from ai_company.orchestrator.message_bus import MessageBus

    bus = MessageBus()
    inbox_path = Path(bus.storage_path)

    if not inbox_path.exists():
        typer.echo("No inbox found.")
        return

    tasks = json.loads(inbox_path.read_text(encoding="utf-8"))
    status_counts: dict[str, int] = {}
    for t in tasks:
        s = t.get("status", "unknown")
        status_counts[s] = status_counts.get(s, 0) + 1

    typer.echo("Executor Status")
    typer.echo("=" * 40)
    typer.echo(f"Total tasks: {len(tasks)}")
    for status, count in sorted(status_counts.items()):
        typer.echo(f"  {status}: {count}")

    # Show pending tasks
    pending = [t for t in tasks if t.get("status") == "pending"]
    if pending:
        typer.echo(f"\nPending tasks ({len(pending)}):")
        for t in pending[:10]:
            typer.echo(f"  [{t.get('id', '?')[:8]}] -> {t.get('receiver_id', '?')}: {t.get('instruction', '?')[:60]}")
