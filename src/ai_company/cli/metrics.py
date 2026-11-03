import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import typer

metrics_app = typer.Typer(help="Operational metrics and health monitoring")


@metrics_app.command("atc")
def agent_task_completion(
    period: str = typer.Option("7d", help="Time period (e.g., 1d, 7d, 30d)"),
    agent: Optional[str] = typer.Option(None, help="Filter by agent ID"),
) -> None:
    """Calculate Agent Task Completion rate."""
    days = int(period.rstrip("d"))
    cutoff = datetime.now() - timedelta(days=days)

    inbox_path = Path(".opencode/inbox.json")
    dead_letter_path = Path("data/orchestrator/dead_letter.jsonl")

    if not inbox_path.exists():
        typer.echo("Error: inbox.json not found", err=True)
        raise typer.Exit(1)

    try:
        with open(inbox_path, encoding="utf-8") as f:
            tasks = json.load(f)
    except json.JSONDecodeError as err:
        typer.echo("Error: inbox.json is not valid JSON", err=True)
        raise typer.Exit(1) from err

    filtered_tasks = []
    for task in tasks:
        created_at = task.get("created_at") or task.get("timestamp") or ""
        try:
            if created_at.endswith("Z"):
                created_at = created_at[:-1] + "+00:00"
            task_time = datetime.fromisoformat(created_at)
        except (ValueError, TypeError, AttributeError):
            continue
        if task_time >= cutoff and (
            agent is None or str(task.get("agent_id", "")).lower() == str(agent).lower()
        ):
            filtered_tasks.append(task)

    total = len(filtered_tasks)
    completed = sum(1 for t in filtered_tasks if str(t.get("status", "")).lower() == "completed")
    failed = sum(
        1 for t in filtered_tasks if str(t.get("status", "")).lower() in ["failed", "error"]
    )

    atc_rate = (completed / total * 100) if total > 0 else 100.0

    dead_letter_count = 0
    if dead_letter_path.exists():
        with open(dead_letter_path, encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    ts = entry.get("first_failed_at") or entry.get("last_failed_at") or ""
                    if ts.endswith("Z"):
                        ts = ts[:-1] + "+00:00"
                    entry_time = datetime.fromisoformat(ts)
                    if entry_time >= cutoff and (
                        agent is None
                        or str(entry.get("agent_id", "")).lower() == str(agent).lower()
                    ):
                        dead_letter_count += 1
                except (json.JSONDecodeError, ValueError, TypeError, AttributeError):
                    continue

    typer.echo(f"Period: {period}")
    typer.echo(f"Agent: {agent or 'All'}")
    typer.echo(f"Total Tasks in Inbox: {total}")
    typer.echo(f"Completed: {completed}")
    typer.echo(f"Failed: {failed}")
    typer.echo(f"ATC Rate: {atc_rate:.1f}%")
    typer.echo(f"Dead Letters (same period): {dead_letter_count}")

    if total > 0 and atc_rate < 90:
        typer.echo("WARNING: ATC rate below 90% target", err=True)
    if dead_letter_count > 0:
        typer.echo(f"WARNING: {dead_letter_count} unresolved dead letters in period", err=True)
    if total == 0:
        typer.echo("INFO: No tasks found in inbox for this period.")


@metrics_app.command("dead-letter")
def dead_letter_report(
    status: str = typer.Option("unresolved", help="Filter by status (unresolved/resolved/all)"),
    limit: int = typer.Option(10, help="Max entries to show"),
) -> None:
    """Report on dead-letter queue."""
    dead_letter_path = Path("data/orchestrator/dead_letter.jsonl")

    if not dead_letter_path.exists():
        typer.echo("No dead-letter queue found")
        return

    entries = []
    with open(dead_letter_path, encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                is_resolved = entry.get("resolved", False)
                if status == "unresolved" and is_resolved:
                    continue
                if status == "resolved" and not is_resolved:
                    continue
                entries.append(entry)
            except json.JSONDecodeError:
                continue

    typer.echo(f"Dead-letter entries ({status}): {len(entries)}")
    for entry in entries[:limit]:
        ts = entry.get("first_failed_at", "Unknown")
        reason = entry.get("failure_reason", "Unknown")
        agent = entry.get("agent_id", "unknown")
        typer.echo(f"  - [{ts}] {reason} (agent: {agent})")


@metrics_app.command("summary")
def operational_summary() -> None:
    """Unified operational metrics summary."""
    typer.echo("=== Operational Metrics Summary ===")
    typer.echo(
        "Run 'ai-company metrics atc' and 'ai-company metrics dead-letter' for detailed breakdowns."
    )
