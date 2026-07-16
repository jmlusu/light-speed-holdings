"""
Customer Success department commands.
"""

from pathlib import Path
import typer
import yaml
from datetime import datetime

app = typer.Typer(help="Customer Success operations")
CS_DIR = Path("customer_success")


def _load_tickets() -> dict:
    tickets_file = CS_DIR / "tickets.yaml"
    if not tickets_file.exists():
        return {"tickets": []}
    with open(tickets_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"tickets": []}


def _save_tickets(data: dict):
    CS_DIR.mkdir(exist_ok=True)
    tickets_file = CS_DIR / "tickets.yaml"
    with open(tickets_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


@app.command()
def list_tickets():
    """List all customer support tickets."""
    data = _load_tickets()
    tickets = data.get("tickets", [])

    if not tickets:
        typer.echo("No tickets found.")
        return

    typer.echo("")
    typer.echo("Customer Support Tickets")
    typer.echo("========================")
    for ticket in tickets:
        priority = ticket.get("priority", "medium")
        typer.echo(f"  {ticket['id']}: {ticket['subject']} [{priority}]")
        typer.echo(f"    Status: {ticket.get('status', 'open')}")
        typer.echo("")


@app.command()
def create_ticket(
    ticket_id: str = typer.Argument(..., help="Unique ticket ID"),
    subject: str = typer.Option(..., help="Ticket subject"),
    priority: str = typer.Option("medium", help="Ticket priority (low, medium, high, critical)"),
):
    """Create a new support ticket."""
    data = _load_tickets()
    tickets = data.get("tickets", [])

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            typer.echo(f"Error: Ticket '{ticket_id}' already exists.")
            raise typer.Exit(1)

    new_ticket = {
        "id": ticket_id,
        "subject": subject,
        "priority": priority,
        "status": "open",
        "created_at": datetime.now().isoformat(),
    }
    tickets.append(new_ticket)
    data["tickets"] = tickets
    _save_tickets(data)
    typer.echo(f"Ticket '{subject}' created successfully.")


@app.command()
def resolve(ticket_id: str = typer.Argument(..., help="Ticket ID to resolve")):
    """Resolve a support ticket."""
    data = _load_tickets()
    tickets = data.get("tickets", [])

    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if not ticket:
        typer.echo(f"Error: Ticket '{ticket_id}' not found.")
        raise typer.Exit(1)

    ticket["status"] = "resolved"
    ticket["resolved_at"] = datetime.now().isoformat()
    _save_tickets(data)
    typer.echo(f"Ticket '{ticket['subject']}' resolved!")


@app.command()
def satisfaction_report():
    """Generate customer satisfaction report."""
    data = _load_tickets()
    tickets = data.get("tickets", [])

    total = len(tickets)
    resolved = sum(1 for t in tickets if t.get("status") == "resolved")
    open_tickets = total - resolved

    typer.echo("")
    typer.echo("Customer Satisfaction Report")
    typer.echo("===========================")
    typer.echo(f"  Total Tickets: {total}")
    typer.echo(f"  Resolved: {resolved}")
    typer.echo(f"  Open: {open_tickets}")
    if total > 0:
        resolution_rate = (resolved / total) * 100
        typer.echo(f"  Resolution Rate: {resolution_rate:.1f}%")
    typer.echo("")
