"""Marketing department commands."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import typer
import yaml

app = typer.Typer(help="Marketing department operations")
CAMPAIGNS_DIR = Path("marketing")


def _load_campaigns() -> dict:
    """Load marketing campaigns from YAML."""
    campaigns_file = CAMPAIGNS_DIR / "campaigns.yaml"
    if not campaigns_file.exists():
        return {"campaigns": []}
    with open(campaigns_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"campaigns": []}


def _save_campaigns(data: dict) -> None:
    """Persist marketing campaigns to YAML."""
    CAMPAIGNS_DIR.mkdir(exist_ok=True)
    campaigns_file = CAMPAIGNS_DIR / "campaigns.yaml"
    with open(campaigns_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


@app.command()
def list_campaigns() -> None:
    """List all marketing campaigns."""
    data = _load_campaigns()
    campaigns = data.get("campaigns", [])

    if not campaigns:
        typer.echo("No campaigns found.")
        return

    typer.echo("")
    typer.echo("Marketing Campaigns")
    typer.echo("===================")
    for campaign in campaigns:
        status = campaign.get("status", "draft")
        typer.echo(f"  {campaign['id']}: {campaign['name']} [{status}]")
        typer.echo(f"    Channel: {campaign.get('channel', 'N/A')}")
        typer.echo("")


@app.command()
def create_campaign(
    campaign_id: str = typer.Argument(..., help="Unique campaign ID"),
    name: str = typer.Option(..., help="Campaign name"),
    channel: str = typer.Option("email", help="Marketing channel"),
) -> None:
    """Create a new marketing campaign."""
    data = _load_campaigns()
    campaigns = data.get("campaigns", [])

    for c in campaigns:
        if c["id"] == campaign_id:
            typer.echo(f"Error: Campaign '{campaign_id}' already exists.")
            raise typer.Exit(1)

    new_campaign = {
        "id": campaign_id,
        "name": name,
        "channel": channel,
        "status": "draft",
        "created_at": datetime.now().isoformat(),
        "metrics": {"impressions": 0, "clicks": 0, "conversions": 0},
    }
    campaigns.append(new_campaign)
    data["campaigns"] = campaigns
    _save_campaigns(data)
    typer.echo(f"Campaign '{name}' created successfully.")


@app.command()
def launch(campaign_id: str = typer.Argument(..., help="Campaign ID to launch")) -> None:
    """Launch a marketing campaign."""
    data = _load_campaigns()
    campaigns = data.get("campaigns", [])

    campaign = next((c for c in campaigns if c["id"] == campaign_id), None)
    if not campaign:
        typer.echo(f"Error: Campaign '{campaign_id}' not found.")
        raise typer.Exit(1)

    campaign["status"] = "active"
    campaign["launched_at"] = datetime.now().isoformat()
    _save_campaigns(data)
    typer.echo(f"Campaign '{campaign['name']}' launched!")


@app.command()
def metrics(campaign_id: str = typer.Argument(..., help="Campaign ID")) -> None:
    """View campaign metrics."""
    data = _load_campaigns()
    campaigns = data.get("campaigns", [])

    campaign = next((c for c in campaigns if c["id"] == campaign_id), None)
    if not campaign:
        typer.echo(f"Error: Campaign '{campaign_id}' not found.")
        raise typer.Exit(1)

    m = campaign.get("metrics", {})
    typer.echo("")
    typer.echo(f"Metrics for: {campaign['name']}")
    typer.echo("=" * 40)
    typer.echo(f"  Impressions: {m.get('impressions', 0)}")
    typer.echo(f"  Clicks: {m.get('clicks', 0)}")
    typer.echo(f"  Conversions: {m.get('conversions', 0)}")
    typer.echo("")
