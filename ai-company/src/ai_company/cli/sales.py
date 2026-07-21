"""Sales department commands."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import typer
import yaml

app = typer.Typer(help="Sales department operations")
SALES_DIR = Path("sales")


def _load_pipeline() -> dict:
    """Load the sales pipeline from YAML."""
    pipeline_file = SALES_DIR / "pipeline.yaml"
    if not pipeline_file.exists():
        return {"deals": [], "leads": []}
    with open(pipeline_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"deals": [], "leads": []}


def _save_pipeline(data: dict) -> None:
    """Persist the sales pipeline to YAML."""
    SALES_DIR.mkdir(exist_ok=True)
    pipeline_file = SALES_DIR / "pipeline.yaml"
    with open(pipeline_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


@app.command()
def list_leads() -> None:
    """List all sales leads."""
    data = _load_pipeline()
    leads = data.get("leads", [])

    if not leads:
        typer.echo("No leads found.")
        return

    typer.echo("")
    typer.echo("Sales Leads")
    typer.echo("===========")
    for lead in leads:
        status = lead.get("status", "new")
        typer.echo(f"  {lead['id']}: {lead['name']} [{status}]")
        typer.echo(f"    Source: {lead.get('source', 'N/A')}")
        typer.echo("")


@app.command()
def add_lead(
    lead_id: str = typer.Argument(..., help="Unique lead ID"),
    name: str = typer.Option(..., help="Lead name"),
    source: str = typer.Option("website", help="Lead source"),
) -> None:
    """Add a new sales lead."""
    data = _load_pipeline()
    leads = data.get("leads", [])

    for lead in leads:
        if lead["id"] == lead_id:
            typer.echo(f"Error: Lead '{lead_id}' already exists.")
            raise typer.Exit(1)

    new_lead = {
        "id": lead_id,
        "name": name,
        "source": source,
        "status": "new",
        "created_at": datetime.now().isoformat(),
    }
    leads.append(new_lead)
    data["leads"] = leads
    _save_pipeline(data)
    typer.echo(f"Lead '{name}' added successfully.")


@app.command()
def list_deals() -> None:
    """List all deals in the pipeline."""
    data = _load_pipeline()
    deals = data.get("deals", [])

    if not deals:
        typer.echo("No deals found.")
        return

    typer.echo("")
    typer.echo("Sales Pipeline")
    typer.echo("==============")
    for deal in deals:
        value = deal.get("value", 0)
        typer.echo(f"  {deal['id']}: {deal['name']} - ${value:,.2f}")
        typer.echo(f"    Stage: {deal.get('stage', 'prospecting')}")
        typer.echo("")


@app.command()
def add_deal(
    deal_id: str = typer.Argument(..., help="Unique deal ID"),
    name: str = typer.Option(..., help="Deal name"),
    value: float = typer.Option(0.0, help="Deal value"),
) -> None:
    """Add a new deal to the pipeline."""
    data = _load_pipeline()
    deals = data.get("deals", [])

    for deal in deals:
        if deal["id"] == deal_id:
            typer.echo(f"Error: Deal '{deal_id}' already exists.")
            raise typer.Exit(1)

    new_deal = {
        "id": deal_id,
        "name": name,
        "value": value,
        "stage": "prospecting",
        "created_at": datetime.now().isoformat(),
    }
    deals.append(new_deal)
    data["deals"] = deals
    _save_pipeline(data)
    typer.echo(f"Deal '{name}' added successfully.")


@app.command()
def pipeline_summary() -> None:
    """Show pipeline summary."""
    data = _load_pipeline()
    deals = data.get("deals", [])
    leads = data.get("leads", [])

    total_value = sum(d.get("value", 0) for d in deals)
    active_deals = sum(1 for d in deals if d.get("stage") not in ["closed_won", "closed_lost"])

    typer.echo("")
    typer.echo("Sales Pipeline Summary")
    typer.echo("=====================")
    typer.echo(f"  Total Leads: {len(leads)}")
    typer.echo(f"  Active Deals: {active_deals}")
    typer.echo(f"  Pipeline Value: ${total_value:,.2f}")
    typer.echo("")
