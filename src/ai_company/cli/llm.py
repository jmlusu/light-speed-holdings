"""LLM usage and token-counting CLI commands.

Ticket #9 (T012): ``ai-company llm usage`` reports token usage and cost
aggregated by model, time period, and agent from the executor's
``cost_log.jsonl`` (written by :class:`ai_company.llm.cost_tracker.CostTracker`).

Token efficiency module — watches for the three classic waste patterns
identified by token-use audit:
1. Meta-prompts about prompt quality
2. Over-justifying simple requests
3. Seeking explanations of obvious outcomes
"""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import typer

from ai_company.paths import get_data_root

app = typer.Typer(help="LLM usage and cost tracking")


def _default_results_dir() -> Path:
    """Resolve the results dir to ``<data root>/results`` (root-aware)."""
    return get_data_root() / "results"


@app.command()
def usage(
    days: int = typer.Option(7, "--days", "-d", help="Report the last N days (default 7)"),
    model: str = typer.Option("", "--model", "-m", help="Filter by model name (e.g. gpt-4o)"),
    agent: str = typer.Option("", "--agent", "-a", help="Filter by agent name"),
    source: str = typer.Option(
        "", "--source", "-s", help="Filter by source (ai-company-cli|opencode-desktop)"
    ),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON instead of a table"),
    results_dir: str = typer.Option("", "--results-dir", help="Override results directory"),
) -> None:
    """Show LLM token usage and cost for the last N days.

    Aggregates the executor's ``cost_log.jsonl`` by model, agent, and time
    period.  With no filters it reports the trailing ``--days`` window;
    use ``--model`` / ``--agent`` / ``--source`` to narrow the breakdown.
    """
    from ai_company.llm.cost_tracker import CostTracker

    log_dir = Path(results_dir) if results_dir else _default_results_dir()
    tracker = CostTracker(results_dir=log_dir)

    end = date.today().isoformat()
    start = (date.today() - timedelta(days=max(0, days - 1))).isoformat()
    summary = tracker.get_usage_summary(
        start_date=start,
        end_date=end,
        model=model or None,
        agent_name=agent or None,
        source=source or None,
    )

    if json_output:
        typer.echo(json.dumps(summary, indent=2, default=str))
        return

    if summary["call_count"] == 0:
        typer.echo(
            f"No LLM usage recorded in {log_dir / 'cost_log.jsonl'} for the last {days} day(s)."
        )
        return

    # -- Waste/efficiency analysis -------------------------------------
    # Rough estimates based on the audit's three waste patterns:
    #   1. Meta-prompts about prompt quality  → ~10-15% of prompt tokens
    #   2. Over-justifying simple requests    → ~5-10% of prompt tokens
    #   3. Explaining obvious outcomes        → ~5-8% of prompt tokens
    # Combined typical waste: 15-33% of prompt tokens
    # This session's estimate uses the audit's 25% figure as a baseline.
    from ai_company.llm.cost_tracker import _cost_per_token

    waste_prompt_estimate = int(summary["total_prompt_tokens"] * 0.25)
    waste_cost_estimate = (
        waste_prompt_estimate
        * _cost_per_token(
            summary.get("by_model", {}).get("default", {}).get("model", "gpt-4o-mini"),
            "input",
        )
        or 0.0
    )
    productive_prompt = summary["total_prompt_tokens"] - waste_prompt_estimate
    waste_ratio = (
        summary["total_prompt_tokens"] / max(summary["total_tokens"], 1)
        if summary["total_tokens"]
        else 0
    )

    typer.echo(
        f"LLM Usage — {start} to {end}"
        f"{'  (filter: model=%s, agent=%s)' % (model or '*', agent or '*')}"
    )
    typer.echo("=" * 78)
    typer.echo(f"  Calls:                {summary['call_count']}")
    typer.echo(f"  Prompt tokens:        {summary['total_prompt_tokens']}")
    typer.echo(f"  Completion tokens:    {summary['total_completion_tokens']}")
    typer.echo(f"  Total tokens:         {summary['total_tokens']}")
    typer.echo(f"  Cost (USD):           ${summary['total_cost_usd']:.6f}")
    typer.echo("")
    # Efficiency panel
    typer.echo("-" * 78)
    typer.echo("  Token Efficiency")
    typer.echo(f"  Productive prompt tokens:   {productive_prompt}")
    waste_pct = (
        round(waste_prompt_estimate / summary["total_prompt_tokens"] * 100)
        if summary["total_prompt_tokens"]
        else 0
    )
    typer.echo(f"  Estimated waste:            {waste_prompt_estimate} ({waste_pct}% of prompt)")
    typer.echo(f"  Estimated waste cost:       {waste_cost_estimate:.6f}")
    typer.echo(f"  Waste ratio (prompt/total): {waste_ratio:.1%}")
    typer.echo("")

    if summary["by_model"]:
        typer.echo("By Model")
        typer.echo("-" * 78)
        typer.echo(f"  {'Model':<30} {'Calls':>6} {'Prompt':>10} {'Completion':>12} {'Cost $':>10}")
        for name, entry in sorted(summary["by_model"].items()):
            typer.echo(
                f"  {name:<30} {entry['calls']:>6} {entry['prompt_tokens']:>10} "
                f"{entry['completion_tokens']:>12} {entry['cost_usd']:>10.6f}"
            )
        typer.echo("")

    if summary["by_agent"]:
        typer.echo("By Agent")
        typer.echo("-" * 78)
        typer.echo(f"  {'Agent':<30} {'Calls':>6} {'Prompt':>10} {'Completion':>12} {'Cost $':>10}")
        for name, entry in sorted(summary["by_agent"].items()):
            typer.echo(
                f"  {name:<30} {entry['calls']:>6} {entry['prompt_tokens']:>10} "
                f"{entry['completion_tokens']:>12} {entry['cost_usd']:>10.6f}"
            )
        typer.echo("")

    if summary.get("by_source"):
        typer.echo("By Source")
        typer.echo("-" * 78)
        typer.echo(
            f"  {'Source':<30} {'Calls':>6} {'Prompt':>10} {'Completion':>12} {'Cost $':>10}"
        )
        for name, entry in sorted(summary["by_source"].items()):
            typer.echo(
                f"  {name:<30} {entry['calls']:>6} {entry['prompt_tokens']:>10} "
                f"{entry['completion_tokens']:>12} {entry['cost_usd']:>10.6f}"
            )


@app.command("sync-opencode")
def sync_opencode(
    project: str = typer.Option(
        "",
        "--project",
        "-p",
        help="Filter sessions by directory substring (default light-speed-holdings)",
    ),
    since: str = typer.Option("", "--since", help="Only sessions on/after YYYY-MM-DD"),
    all_sessions: bool = typer.Option(
        False, "--all", help="Ingest all projects (not just --project)"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Report what would be ingested without writing"
    ),
    limit: int = typer.Option(500, "--limit", help="Max sessions to scan (default 500)"),
    db_path: str = typer.Option("", "--db-path", help="Override opencode.db path"),
    results_dir: str = typer.Option("", "--results-dir", help="Override results directory"),
) -> None:
    """Sync OpenCode Desktop usage into the canonical cost store.

    Reads ``opencode.db`` read-only and appends one record per Desktop
    session with ``source=opencode-desktop``. Idempotent: re-running
    inserts 0 new rows (dedup on ``event_id``).
    """
    from ai_company.llm.cost_tracker import CostTracker
    from ai_company.llm.opencode_usage import iter_opencode_sessions

    project_filter = "" if all_sessions else (project or "light-speed-holdings")
    log_dir = Path(results_dir) if results_dir else _default_results_dir()

    records = list(
        iter_opencode_sessions(
            db_path or None,
            project=project_filter or None,
            since=since or None,
            limit=limit,
        )
    )
    if dry_run:
        total_prompt = sum(r["prompt_tokens"] for r in records)
        total_comp = sum(r["completion_tokens"] for r in records)
        total_cost = round(sum(r["cost_usd"] for r in records), 6)
        typer.echo(f"[dry-run] {len(records)} session(s) would be synced")
        typer.echo(f"  prompt={total_prompt} completion={total_comp} cost=${total_cost}")
        return

    tracker = CostTracker(results_dir=log_dir, database=None)
    # Snapshot event_ids already in the store so a re-sync reports only new
    # rows. CostTracker.record_usage early-outs on a duplicate event_id and
    # returns the existing record without appending; whether the returned
    # object is a fresh record (not the pre-existing one) tells whether a
    # new row was actually appended.
    seen_event_ids = {r.event_id for r in tracker._records if r.event_id}
    inserted = 0
    for rec in records:
        event_id = rec["event_id"]
        existing = (
            next((r for r in tracker._records if r.event_id == event_id), None)
            if event_id
            else None
        )
        was_seen = bool(event_id) and event_id in seen_event_ids
        returned = tracker.record_usage(
            model=rec["model"],
            provider=rec["provider"],
            agent_name=rec["agent_name"],
            task_id=rec["task_id"],
            prompt_tokens=rec["prompt_tokens"],
            completion_tokens=rec["completion_tokens"],
            iteration=rec["iteration"],
            files_read=rec["files_read"],
            source=rec["source"],
            session_id=rec["session_id"],
            event_id=event_id,
            cache_read=rec["cache_read"],
            cache_write=rec["cache_write"],
            cost_source=rec["cost_source"],
            metadata=rec["metadata"],
            cost_usd=rec["cost_usd"],
            timestamp=rec["timestamp"],
        )
        # Count only rows that were actually appended: the event_id was new
        # and record_usage created a fresh record instead of returning the
        # existing one. Empty event_id always appends.
        if not was_seen and returned is not existing:
            inserted += 1
            if event_id:
                seen_event_ids.add(event_id)
    typer.echo(
        f"Synced {inserted} OpenCode Desktop session(s) from {db_path or 'default opencode.db'}"
    )
    typer.echo(f"Results dir: {log_dir}")
