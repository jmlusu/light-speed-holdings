"""Model routing CLI commands."""

from typing import Optional

import typer

app = typer.Typer(help="Model routing policy and resolution")


@app.command()
def show() -> None:
    """Show the full routing table: providers, tiers, and per-agent resolution."""
    from ai_company.model_router import ModelRouter

    router = ModelRouter()

    # Providers
    typer.echo("Providers")
    typer.echo("=" * 60)
    for p in router.list_providers():
        typer.echo(f"  {p.id:<12} backend={p.backend:<10} model={p.default_model}")
        if p.api_base:
            typer.echo(f"  {'':12} api_base={p.api_base}")
    typer.echo("")

    # Tiers
    typer.echo("Tiers")
    typer.echo("=" * 60)
    for t in router.list_tiers():
        typer.echo(f"  {t.id:<12} {t.description}")
        for i, prov in enumerate(t.providers):
            arrow = "  ->" if i > 0 else "   "
            typer.echo(f"  {arrow} {prov.provider}/{prov.model}")
    typer.echo("")

    # Per-agent resolution
    typer.echo("Agent Routing")
    typer.echo("=" * 60)
    typer.echo(f"  {'Agent':<25} {'Provider':<12} {'Model':<25} {'Tier'}")
    typer.echo(f"  {'-'*25} {'-'*12} {'-'*25} {'-'*12}")
    for name, route in sorted(router.resolve_all_agents().items()):
        typer.echo(f"  {name:<25} {route.provider:<12} {route.model:<25} {route.tier}")


@app.command()
def resolve(
    agent: str = typer.Argument(..., help="Agent name to resolve"),
    priority: str = typer.Option("medium", help="Task priority: low, medium, high, critical"),
    context: Optional[str] = typer.Option(None, help="Context override: escalation, approval"),
) -> None:
    """Resolve which model a specific agent would use."""
    from ai_company.model_router import ModelRouter

    router = ModelRouter()
    route = router.resolve(agent_name=agent, priority=priority, context=context)

    typer.echo(f"Agent:    {agent}")
    typer.echo(f"Provider: {route.provider}")
    typer.echo(f"Model:    {route.model}")
    typer.echo(f"Tier:     {route.tier}")
    typer.echo(f"Reason:   {route.reason}")


@app.command()
def check() -> None:
    """Check which providers are reachable."""
    import urllib.request

    from ai_company.model_router import ModelRouter

    router = ModelRouter()

    typer.echo("Provider Health Check")
    typer.echo("=" * 60)
    for p in router.list_providers():
        if p.backend == "ollama":
            url = f"{p.api_base}/api/tags"
        elif p.backend == "openai":
            url = f"{p.api_base}/models"
        elif p.backend == "anthropic":
            url = "https://api.anthropic.com/v1/messages"
        else:
            typer.echo(f"  {p.id:<12} SKIP (unknown backend: {p.backend})")
            continue

        try:
            req = urllib.request.Request(url, method="GET")
            if p.backend == "anthropic":
                req.add_header("anthropic-version", "2023-06-01")
            resp = urllib.request.urlopen(req, timeout=5)
            typer.echo(f"  {p.id:<12} OK ({resp.status})")
        except Exception as e:
            typer.echo(f"  {p.id:<12} DOWN ({type(e).__name__}: {e})")
