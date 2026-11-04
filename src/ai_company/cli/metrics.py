import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

import typer

metrics_app = typer.Typer(help="Operational metrics and health monitoring")


def _parse_timestamp(value: object) -> Optional[datetime]:
    """Parse an ISO-8601 timestamp into a timezone-aware UTC datetime."""
    if not isinstance(value, str) or not value:
        return None
    text = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(text)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


@metrics_app.command("atc")
def agent_task_completion(
    period: str = typer.Option("7d", help="Time period (e.g., 1d, 7d, 30d)"),
    agent: Optional[str] = typer.Option(None, help="Filter by agent ID"),
) -> None:
    """Calculate Agent Task Completion rate."""
    days = int(period.rstrip("d"))
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

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
        try:
            task_time = _parse_timestamp(task.get("created_at") or task.get("timestamp"))
        except (ValueError, TypeError):
            continue
        if task_time is None:
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
                    entry_time = _parse_timestamp(
                        entry.get("first_failed_at") or entry.get("last_failed_at")
                    )
                    if (
                        entry_time is not None
                        and entry_time >= cutoff
                        and (
                            agent is None
                            or str(entry.get("agent_id", "")).lower() == str(agent).lower()
                        )
                    ):
                        dead_letter_count += 1
                except (json.JSONDecodeError, ValueError, TypeError):
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


@metrics_app.command("cost")
def cost_metrics(
    period: str = typer.Option("30d", help="Time period (e.g., 1d, 7d, 30d)"),
    agent: Optional[str] = typer.Option(None, help="Filter by agent ID"),
) -> None:
    """Calculate cost metrics for agent or all agents.

    Uses the SQLite cost tracker backend for efficient aggregation.
    Supports filtering by agent_id for per-agent cost attribution.
    """
    from ai_company.data.cost_analytics import CostAnalytics
    from ai_company.data.database import Database

    days = int(period.rstrip("d"))

    # Initialize database and cost analytics
    db = Database()
    analytics = CostAnalytics(db)

    agent_total = 0.0
    total_cost = 0.0
    total_prompt = 0
    total_completion = 0
    total_calls = 0
    agent_daily: list[dict[str, Any]] = []
    agent_rows: list[dict[str, Any]] = []

    # Get agent breakdown
    if agent:
        agent_total = analytics.get_agent_total_by_id(agent)
        agent_daily = analytics.agent_daily_costs_by_id(agent, days=days)
        total_prompt = sum(r["prompt_tokens"] for r in agent_daily)
        total_completion = sum(r["completion_tokens"] for r in agent_daily)
        total_calls = sum(r["calls"] for r in agent_daily)
    else:
        # Get all-agent breakdown
        agent_rows = analytics.breakdown_by_agent_id(days=days)
        total_cost = sum(r["cost_usd"] for r in agent_rows)
        total_prompt = sum(r["prompt_tokens"] for r in agent_rows)
        total_completion = sum(r["completion_tokens"] for r in agent_rows)
        total_calls = sum(r["calls"] for r in agent_rows)

    # Get daily cost trend for the period
    daily_trend = analytics.daily_cost_trend(days=days)

    typer.echo("Cost Metrics Summary")
    typer.echo(f"Period: {period}")
    if agent:
        typer.echo(f"Agent: {agent}")
        typer.echo(f"Total Cost: ${agent_total:.6f}")
    else:
        typer.echo(f"Total Cost: ${total_cost:.6f}")
    typer.echo(f"Total Prompt Tokens: {total_prompt}")
    typer.echo(f"Total Completion Tokens: {total_completion}")
    typer.echo(f"Total Calls: {total_calls}")
    typer.echo("")

    if agent:
        typer.echo(f"Agent '{agent}' cost over {period}:")
        for day in agent_daily:
            typer.echo(
                f"  {day['day']}: ${day['total_cost']:.6f} "
                f"({day['prompt_tokens']} prompt + {day['completion_tokens']} completion, "
                f"{day['calls']} calls)"
            )
    else:
        typer.echo(f"Cost by agent over {period}:")
        for entry in agent_rows:
            typer.echo(
                f"  {entry['agent_id']}: ${entry['cost_usd']:.6f} "
                f"({entry['prompt_tokens']} prompt + {entry['completion_tokens']} completion, "
                f"{entry['calls']} calls)"
            )

    typer.echo("")
    typer.echo(f"Daily cost trend (last {days} days):")
    for day in daily_trend:
        typer.echo(
            f"  {day['day']}: ${day['total_cost']:.6f} "
            f"({day['call_count']} calls, {day['agent_count']} agents, {day['model_count']} models)"
        )


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
        ts = entry.get("first_failed_at") or "Unknown"
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
