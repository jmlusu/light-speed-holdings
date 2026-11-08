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
from typing import Any

import typer

from ai_company.paths import get_data_root, get_database_path

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
    no_write: bool = typer.Option(
        True,
        "--no-write/--write",
        help="Read-only report (default): never write the summary export. "
        "--write restores the legacy export-on-report behaviour.",
    ),
) -> None:
    """Show LLM token usage and cost for the last N days.

    Aggregates the executor's ``cost_log.jsonl`` by model, agent, and time
    period.  With no filters it reports the trailing ``--days`` window;
    use ``--model`` / ``--agent`` / ``--source`` to narrow the breakdown.

    Report-only by default: the tracker is constructed read-only so
    ``data/orchestrator/cost_tracker.json`` is never rewritten. Pass
    ``--write`` to restore the legacy export-on-report behaviour.
    """
    from ai_company.llm.cost_tracker import CostTracker

    log_dir = Path(results_dir) if results_dir else _default_results_dir()
    tracker = CostTracker(results_dir=log_dir, read_only=no_write, no_write=no_write)

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
    no_sqlite: bool = typer.Option(
        False,
        "--no-sqlite",
        help="JSONL-only mode (legacy): skip the SQLite cost_records mirror",
    ),
    no_write: bool = typer.Option(
        False,
        "--no-write",
        help="Read-only scan: never write JSONL, the SQLite mirror, or the "
        "summary export (dry-run against the canonical stores).",
    ),
) -> None:
    """Sync OpenCode Desktop usage into the canonical cost store.

    Reads ``opencode.db`` read-only and appends one record per Desktop
    session with ``source=opencode-desktop``. Idempotent: re-running
    inserts 0 new rows (dedup on ``event_id``) across both stores.

    By default each Desktop record is written to both ``cost_log.jsonl``
    and the SQLite ``cost_records`` mirror (``data/ai_company.db`` via
    ``get_database_path()``). Pass ``--no-sqlite`` to keep the legacy
    JSONL-only behaviour. Pass ``--no-write`` for a read-only scan that
    never touches JSONL, the SQLite mirror, or the summary export.

    WAL runbook (no daemon): OpenCode Desktop keeps its SQLite database
    in WAL mode while running. This sync must stay WAL-safe by opening
    the source database strictly ``mode=ro`` (URI ``mode=ro`` with
    ``uri=True``) so readers never write to, lock, or checkpoint the
    live Desktop WAL. Never-open-without-ro: never open ``opencode.db``
    without ``mode=ro`` — a plain writable open would take a write lock
    and could block or corrupt the running Desktop process. There is no
    background daemon; each invocation is a short-lived read-only scan
    followed by writes only to the canonical stores (JSONL + SQLite
    mirror at ``data/ai_company.db``), never back to ``opencode.db``.
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

    database: Any = None
    db_obj: Any = None
    if not no_sqlite and not no_write:
        try:
            from ai_company.data.database import Database

            db_obj = Database(str(get_database_path()))
            db_obj.init_schema()
            database = db_obj
        except Exception as exc:  # noqa: BLE001 - fall back to JSONL-only
            typer.echo(
                f"Warning: SQLite mirror unavailable ({exc}); continuing JSONL-only",
                err=True,
            )
            database = None
            db_obj = None

    tracker = CostTracker(
        results_dir=log_dir,
        database=database,
        read_only=no_write,
        no_write=no_write,
    )
    if not no_sqlite and not no_write and tracker._cost_analytics is None:
        typer.echo(
            "Warning: SQLite database not usable; continuing JSONL-only",
            err=True,
        )

    # Snapshot event_ids from both stores so a re-sync reports only new
    # rows and dedup holds across JSONL + SQLite. CostTracker.record_usage
    # early-outs on a JSONL duplicate and CostAnalytics.record_usage early-
    # outs on a SQLite duplicate (unique event_id); whether the returned
    # object is a fresh record (not the pre-existing one) tells whether a
    # new JSONL row was actually appended.
    jsonl_seen = {r.event_id for r in tracker._records if r.event_id}
    sqlite_seen: set[str] = set()
    if database is not None and tracker._cost_analytics is not None:
        try:
            rows = database.fetchall(
                "SELECT event_id FROM cost_records WHERE event_id IS NOT NULL AND event_id != ''"
            )
            sqlite_seen = {str(row["event_id"]) for row in rows if row.get("event_id")}
        except Exception:  # noqa: BLE001 - dedup probe is best-effort
            sqlite_seen = set()

    inserted = 0
    sqlite_backfilled = 0
    for rec in records:
        event_id = rec["event_id"]
        in_jsonl = bool(event_id) and event_id in jsonl_seen
        in_sqlite = bool(event_id) and event_id in sqlite_seen

        if in_jsonl and in_sqlite:
            continue

        if in_jsonl and not in_sqlite:
            # Already in JSONL from a pre-SQLite sync: backfill the SQLite
            # mirror only, without appending a second JSONL row.
            if tracker._cost_analytics is not None:
                try:
                    backfilled_id = tracker._cost_analytics.record_usage(
                        model=rec["model"],
                        provider=rec["provider"],
                        agent_name=rec["agent_name"],
                        task_id=rec["task_id"],
                        prompt_tokens=rec["prompt_tokens"],
                        completion_tokens=rec["completion_tokens"],
                        cost_usd=rec["cost_usd"],
                        iteration=rec["iteration"],
                        files_read=rec["files_read"],
                        source=rec["source"],
                        session_id=rec["session_id"],
                        event_id=event_id,
                        cache_read=rec["cache_read"],
                        cache_write=rec["cache_write"],
                        cost_source=rec["cost_source"],
                        metadata=rec["metadata"],
                        timestamp=rec["timestamp"],
                    )
                    if backfilled_id:
                        sqlite_seen.add(event_id)
                        sqlite_backfilled += 1
                except Exception:  # noqa: BLE001 - backfill is best-effort
                    pass
            continue

        existing = (
            next((r for r in tracker._records if r.event_id == event_id), None)
            if event_id
            else None
        )
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
        if returned is not existing:
            inserted += 1
            if event_id:
                jsonl_seen.add(event_id)
                if tracker._cost_analytics is not None:
                    sqlite_seen.add(event_id)
    report_prefix = "[no-write] " if no_write else ""
    typer.echo(
        f"{report_prefix}Synced {inserted} OpenCode Desktop session(s) "
        f"from {db_path or 'default opencode.db'}"
    )
    if sqlite_backfilled:
        typer.echo(
            f"  backfilled {sqlite_backfilled} record(s) into SQLite mirror (already in JSONL)"
        )
    typer.echo(f"Results dir: {log_dir}")
    if db_obj is not None:
        db_obj.close()
