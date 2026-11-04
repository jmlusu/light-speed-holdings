import json
from datetime import datetime, timedelta
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

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
    cutoff = datetime.now() - timedelta(days=days)
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
        created_at = task.get("created_at") or task.get("timestamp") or ""
        try:
            if created_at.endswith("Z"):
                created_at = created_at[:-1] + "+00:00"
            task_time = datetime.fromisoformat(created_at)
        except (ValueError, TypeError, AttributeError):
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
    cutoff = datetime.now() - timedelta(days=days)

    # Initialize database and cost analytics
    db = Database()
    analytics = CostAnalytics(db)

    # Get agent breakdown
    if agent:
        agent_total = analytics.get_agent_total_by_id(agent)
        agent_daily = analytics.agent_daily_costs_by_id(agent, days=days)
        agent_breakdown = {
            "agent_id": agent,
            "total_cost_usd": round(agent_total, 6),
            "period": period,
            "total_days": days,
            "daily_breakdown": [
                {
                    "day": r["day"],
                    "total_cost_usd": round(r["total_cost"], 6),
                    "prompt_tokens": r["prompt_tokens"],
                    "completion_tokens": r["completion_tokens"],
                    "calls": r["calls"],
                }
                for r in agent_daily
            ],
        }
    else:
        # Get all-agent breakdown
        agent_breakdown_list = analytics.breakdown_by_agent_id(days=days)
        agent_breakdown = {
            "agent_breakdown": [
                {
                    "agent_id": r["agent_id"],
                    "total_cost_usd": round(r["cost_usd"], 6),
                    "prompt_tokens": r["prompt_tokens"],
                    "completion_tokens": r["completion_tokens"],
                    "calls": r["calls"],
                }
                for r in agent_breakdown_list
            ],
            "total_cost_usd": round(sum(r["cost_usd"] for r in agent_breakdown_list), 6),
            "total_prompt_tokens": sum(r["prompt_tokens"] for r in agent_breakdown_list),
            "total_completion_tokens": sum(r["completion_tokens"] for r in agent_breakdown_list),
            "total_calls": sum(r["calls"] for r in agent_breakdown_list),
        }

    # Get daily cost trend for the period
    daily_trend = analytics.daily_cost_trend(days=days)

    typer.echo("Cost Metrics Summary")
    typer.echo(f"Period: {period}")
    if agent:
        typer.echo(f"Agent: {agent}")
        typer.echo(f"Total Cost: ${agent_total:.6f}")
    else:
        typer.echo(f"Total Cost: ${agent_breakdown['total_cost_usd']:.6f}")
    typer.echo(
        f"Total Prompt Tokens: {agent_breakdown.get('total_prompt_tokens', sum(r['prompt_tokens'] for r in agent_breakdown_list))}"
    )
    typer.echo(
        f"Total Completion Tokens: {agent_breakdown.get('total_completion_tokens', sum(r['completion_tokens'] for r in agent_breakdown_list))}"
    )
    typer.echo(
        f"Total Calls: {agent_breakdown.get('total_calls', sum(r['calls'] for r in agent_breakdown_list))}"
    )
    typer.echo("")

    if agent:
        typer.echo(f"Agent '{agent}' cost over {period}:")
        for day in agent_breakdown["daily_breakdown"]:
            typer.echo(
                f"  {day['day']}: ${day['total_cost_usd']:.6f} "
                f"({day['prompt_tokens']} prompt + {day['completion_tokens']} completion, "
                f"{day['calls']} calls)"
            )
    else:
        typer.echo(f"Cost by agent over {period}:")
        for entry in agent_breakdown.get("agent_breakdown", []):
            typer.echo(
                f"  {entry['agent_id']}: ${entry['total_cost_usd']:.6f} "
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
        ts = entry.get("first_failed_at", "Unknown")
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
