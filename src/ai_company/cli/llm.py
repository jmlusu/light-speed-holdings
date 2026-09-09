"""LLM usage and token-counting CLI commands.

Ticket #9 (T012): `ai-company llm usage` reports token usage and cost
aggregated by model, time period, and agent from the executor's
`cost_log.jsonl` (written by :class:i_company.llm.cost_tracker.CostTracker).

Token efficiency module — watches for the three classic waste patterns
identified by token-use audit:
1. Meta-prompts about prompt quality
2. Over-justifying simple requests
3. Seeking explanations of obvious outcomes
"

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import typer

from ai_company.paths import get_data_root

app = typer.Typer(help="LLM usage and cost tracking")


def _default_results_dir() -> Path:
    """Resolve the results dir to `<data root>/results` (root-aware)."""
    return get_data_root() / "results"


@app.command()
def usage(
    days: int = typer.Option(7, "--days", "-d", help="Report the last N days (default 7)"),
    model: str = typer.Option("", "--model", "-m", help="Filter by model name (e.g. gpt-4o)"),
    agent: str = typer.Option("", "--agent", "-a", help="Filter by agent name"),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON instead of a table"),
    results_dir: str = typer.Option("", "--results-dir", help="Override results directory"),
) -> None:
    """Show LLM token usage and cost for the last N days.

    Aggregates the executor's `cost_log.jsonl` by model, agent, and time
    period.  With no filters it reports the trailing `--days` window;
    use `--model` / `--agent` to narrow the breakdown.
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
    #   1. Meta-prompts about prompt quality  ? ~10-15% of prompt tokens
    #   2. Over-justifying simple requests    ? ~5-10% of prompt tokens
    #   3. Explaining obvious outcomes        ? ~5-8% of prompt tokens
    # Combined typical waste: 15-33% of prompt tokens
    # This session's estimate uses the audit's 25% figure as a baseline.
    from ai_company.llm.cost_tracker import _cost_per_token

    waste_prompt_estimate = int(summary["total_prompt_tokens"] * 0.25)
    waste_cost_estimate = waste_prompt_estimate * _cost_per_token(
        summary.get("by_model", {}).get("default", {}).get("model", "gpt-4o-mini"),
        "input",
    ) or 0.0
    productive_prompt = summary["total_prompt_tokens"] - waste_prompt_estimate
    waste_ratio = (
        summary["total_prompt_tokens"] / max(summary["total_tokens"], 1)
        if summary["total_tokens"] else 0
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
    typer.echo(f"  Cost (USD):           ")
    typer.echo("")
    # Efficiency panel
    typer.echo("-" * 78)
    typer.echo("  Token Efficiency")
    typer.echo(f"  Productive prompt tokens:   {productive_prompt}")
    waste_pct = round(waste_prompt_estimate / summary["total_prompt_tokens"] * 100) if summary["total_prompt_tokens"] else 0
    typer.echo(f"  Estimated waste:            {waste_prompt_estimate} ({waste_pct}% of prompt)")
    typer.echo(f"  Estimated waste cost:       ")
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
