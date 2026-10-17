"""Client onboarding and engagement management CLI commands.

Provides commands for registering clients, checking governance gates,
and creating offer engagements with automatic blocking of Offers B/C
until board-ratified policies are in place.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import typer
import yaml

from ai_company.data import get_database
from ai_company.models.task import TaskPriority
from ai_company.services.client_intake import ClientIntakeService, GovernanceGateError

app = typer.Typer(help="Client onboarding and engagement management (Malawi service portfolio)")
CLIENTS_DIR = Path("sales")


def _load_clients_file() -> dict[str, Any]:
    """Load client YAML from the sales data directory."""
    clients_file = CLIENTS_DIR / "clients.yaml"
    if not clients_file.exists():
        return {"clients": []}
    with open(clients_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"clients": []}


def _save_clients_file(data: dict[str, Any]) -> None:
    """Persist client YAML to the sales data directory."""
    CLIENTS_DIR.mkdir(exist_ok=True)
    clients_file = CLIENTS_DIR / "clients.yaml"
    with open(clients_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


@app.command()
def register(
    client_id: str = typer.Option(..., "--id", "-i", help="Unique client ID"),
    name: str = typer.Option(..., "--name", "-n", help="Client organization name"),
    client_type: str = typer.Option(
        "ngo", "--type", "-t", help="Client type: ngo, sme, agency, individual"
    ),
    email: str = typer.Option("", "--email", "-e", help="Primary contact email"),
    currency: str = typer.Option("USD", "--currency", "-c", help="Billing currency: USD or MWK"),
) -> None:
    """Register a new client in the onboarding system."""
    data = _load_clients_file()
    clients = data.get("clients", [])

    for client in clients:
        if client["id"] == client_id:
            typer.echo(f"Error: Client '{client_id}' already exists.")
            raise typer.Exit(1)

    new_client = {
        "id": client_id,
        "name": name,
        "type": client_type,
        "contact_email": email,
        "currency": currency,
        "created_at": datetime.now().isoformat(),
        "governance_gates_passed": False,
    }
    clients.append(new_client)
    data["clients"] = clients
    _save_clients_file(data)

    typer.echo(f"Client '{name}' registered with ID '{client_id}'.")
    typer.echo(f"  Type: {client_type}")
    typer.echo(f"  Currency: {currency}")
    typer.echo("")
    typer.echo("Next steps:")
    typer.echo(f"  1. Set governance gates: ai-company client gate --client-id {client_id}")
    typer.echo(f"  2. Check readiness:       ai-company client check-gates --client-id {client_id}")
    typer.echo(
        f"  3. Create engagement:     ai-company client engage --client-id {client_id} --offer offer_a"
    )


@app.command("list")
def list_clients(
    client_type: str = typer.Option("", "--type", "-t", help="Filter by client type"),
) -> None:
    """List all registered clients."""
    data = _load_clients_file()
    clients = data.get("clients", [])

    if client_type:
        clients = [c for c in clients if c.get("type") == client_type]

    if not clients:
        typer.echo("No clients found.")
        return

    typer.echo("")
    typer.echo("Registered Clients")
    typer.echo("==================")
    for c in clients:
        gates = c.get("governance_gates_passed", False)
        gate_str = "✓" if gates else "✗"
        typer.echo(
            f"  {c['id']}: {c['name']} [{c['type']}] ({c.get('currency', 'USD')}) gates:{gate_str}"
        )
    typer.echo("")


@app.command("gate")
def set_gate(
    client_id: str = typer.Option(..., "--client-id", "-c", help="Client ID"),
    gate: str = typer.Option(..., "--gate", "-g", help="Gate: contract, dpa, compliance, security"),
    passed: bool = typer.Option(True, "--passed/--failed", help="Gate status"),
    reviewer: str = typer.Option("", "--reviewer", "-r", help="Reviewer agent/ID"),
) -> None:
    """Set a governance gate status for a client."""
    valid_gates = ("contract", "dpa", "compliance", "security")
    if gate not in valid_gates:
        typer.echo(f"Error: gate must be one of: {', '.join(valid_gates)}")
        raise typer.Exit(1)

    gates_file = CLIENTS_DIR / "governance_gates.yaml"
    if gates_file.exists():
        with open(gates_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {"gates": {}}
    else:
        data = {"gates": {}}

    client_gates = data["gates"].setdefault(client_id, {})
    client_gates[gate] = passed
    if reviewer:
        client_gates[f"{gate}_by"] = reviewer
        client_gates[f"{gate}_at"] = datetime.now().isoformat()

    CLIENTS_DIR.mkdir(exist_ok=True)
    with open(gates_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)

    status = "PASSED" if passed else "FAILED"
    typer.echo(f"Gate '{gate}' for client '{client_id}': {status}")
    if reviewer:
        typer.echo(f"  Reviewer: {reviewer}")


@app.command("check-gates")
def check_gates(
    client_id: str = typer.Option(..., "--client-id", "-c", help="Client ID"),
) -> None:
    """Check all governance gates for a client."""
    service = ClientIntakeService(database=get_database())
    result = service.check_governance_gates(client_id)

    if result.success:
        gates = result.data.get("gates", {}) if result.data else {}
        typer.echo(f"All governance gates PASSED for client '{client_id}':")
        for g, passed in gates.items():
            icon = "✓" if passed else "✗"
            typer.echo(f"  {icon} {g}")
        typer.echo("")
        typer.echo("Client is cleared for engagement creation.")
    else:
        typer.echo(f"Governance gates NOT satisfied for client '{client_id}':")
        gates = result.metadata.get("gates", {})
        for g, passed in gates.items():
            icon = "✓" if passed else "✗"
            typer.echo(f"  {icon} {g}")
        typer.echo("")
        missing = result.metadata.get("missing", [])
        typer.echo(f"Missing gates: {', '.join(missing)}")
        typer.echo("")
        typer.echo("Set missing gates with:")
        for g in missing:
            typer.echo(f"  ai-company client gate --client-id {client_id} --gate {g} --passed")


@app.command("engage")
def create_engagement(
    client_id: str = typer.Option(..., "--client-id", "-c", help="Client ID"),
    offer: str = typer.Option(
        ..., "--offer", "-o", help="Offer code: offer_a, offer_b, offer_c, offer_d, offer_e"
    ),
    description: str = typer.Option(..., "--description", "-d", help="Project description"),
    lead_agent: str = typer.Option("", "--lead", "-l", help="Lead agent ID"),
    priority: str = typer.Option(
        "medium", "--priority", "-p", help="Task priority: low, medium, high, critical"
    ),
) -> None:
    """Create a client engagement (pushes a task to the inbox).

    Enforces offer-blocking: Offers B and C are BLOCKED until board-ratified
    governance policies are in place.
    """
    priority_map = {
        "low": TaskPriority.LOW,
        "medium": TaskPriority.MEDIUM,
        "high": TaskPriority.HIGH,
        "critical": TaskPriority.CRITICAL,
    }
    task_priority = priority_map.get(priority.lower(), TaskPriority.MEDIUM)

    # Guard: refuse demo/test engagements. The probe mirrors the instruction
    # built by ClientIntakeService.create_engagement so detection stays in
    # lock-step with the refined markers (proj-acme-chatbot etc.).
    from ai_company.data.task_store import TaskStore

    probe_instruction = (
        f"Execute client engagement for {client_id} under {offer}.\n"
        f"Description: {description}\n"
        f"Lead agent: {lead_agent or 'chief_of_staff'}\n"
    )
    if TaskStore.is_test_task({"id": "", "instruction": probe_instruction}):
        typer.echo("Error: Cannot create test/demo client engagements.")
        raise typer.Exit(1)

    service = ClientIntakeService(database=get_database())

    try:
        result = service.create_engagement(
            client_id=client_id,
            offer_code=offer,
            description=description,
            lead_agent=lead_agent,
            priority=task_priority,
        )
        if result.success and result.data is not None:
            task = result.data
            typer.echo(f"Engagement task created: {task.id[:8]}")
            typer.echo(f"  Client: {client_id}")
            typer.echo(f"  Offer: {offer}")
            typer.echo(f"  Lead agent: {lead_agent or 'chief_of_staff'}")
            typer.echo(f"  Priority: {priority}")
            typer.echo(f"  Requires approval: {task.requires_approval}")
            typer.echo("")
            typer.echo("Task is now in the inbox. human_ceo must approve before agent execution.")
        else:
            typer.echo(f"Error creating engagement: {result.errors}")
            raise typer.Exit(1)
    except GovernanceGateError as e:
        typer.echo(f"BLOCKED: {e}")
        typer.echo("")
        typer.echo("This offer (B or C) is blocked until board-ratified governance policies are")
        typer.echo("in place. See config/company/malawi_offers.yaml for unblock conditions.")
        raise typer.Exit(1) from e


@app.command("engagements")
def list_engagements() -> None:
    """List all pending client engagements from the inbox."""
    service = ClientIntakeService(database=get_database())
    result = service.list_engagements()

    if not result.success or not result.data:
        typer.echo("No pending client engagements found.")
        return

    typer.echo("")
    typer.echo("Pending Client Engagements")
    typer.echo("==========================")
    for eng in result.data:
        typer.echo(f"  {eng['task_id'][:8]} | {eng['client']} | {eng['offer']}")
        typer.echo(f"    {eng['description'][:80]}")
        typer.echo(
            f"    Approval: {'required' if eng['requires_approval'] else 'auto'} | Priority: {eng['priority']}"
        )
    typer.echo("")


@app.command("offers")
def list_offers() -> None:
    """List all Malawi offers and their governance status."""
    service = ClientIntakeService(database=get_database())
    offers = service._offers.get("offers", {})

    typer.echo("")
    typer.echo("Malawi Service Portfolio")
    typer.echo("========================")
    for offer_id, offer in offers.items():
        state = offer.get("governance_state", "unknown")
        risk = offer.get("risk_level", "unknown")
        blocked_str = " [BLOCKED]" if state == "blocked" else ""
        typer.echo(f"  {offer_id} ({offer.get('slug', '?')}){blocked_str}")
        typer.echo(f"    Name: {offer.get('name', 'N/A')}")
        typer.echo(f"    Risk: {risk}")
        typer.echo(f"    State: {state}")
        typer.echo(f"    Currency: {offer.get('currency', 'N/A')}")
        agents = offer.get("agents", [])
        if agents:
            typer.echo(f"    Agents: {', '.join(agents)}")
        if offer.get("blocked_reason"):
            typer.echo(f"    Blocked: {offer['blocked_reason']}")
        typer.echo("")
