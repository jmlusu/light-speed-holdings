"""
Legal department commands.
"""

from pathlib import Path
import typer
import yaml
from datetime import datetime

app = typer.Typer(help="Legal department operations")
LEGAL_DIR = Path("legal")


def _load_contracts() -> dict:
    contracts_file = LEGAL_DIR / "contracts.yaml"
    if not contracts_file.exists():
        return {"contracts": []}
    with open(contracts_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"contracts": []}


def _save_contracts(data: dict):
    LEGAL_DIR.mkdir(exist_ok=True)
    contracts_file = LEGAL_DIR / "contracts.yaml"
    with open(contracts_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


@app.command()
def list_contracts():
    """List all legal contracts."""
    data = _load_contracts()
    contracts = data.get("contracts", [])

    if not contracts:
        typer.echo("No contracts found.")
        return

    typer.echo("")
    typer.echo("Legal Contracts")
    typer.echo("===============")
    for contract in contracts:
        status = contract.get("status", "draft")
        typer.echo(f"  {contract['id']}: {contract['name']} [{status}]")
        typer.echo(f"    Party: {contract.get('party', 'N/A')}")
        typer.echo("")


@app.command()
def add_contract(
    contract_id: str = typer.Argument(..., help="Unique contract ID"),
    name: str = typer.Option(..., help="Contract name"),
    party: str = typer.Option(..., help="Contracting party"),
):
    """Add a new contract."""
    data = _load_contracts()
    contracts = data.get("contracts", [])

    for c in contracts:
        if c["id"] == contract_id:
            typer.echo(f"Error: Contract '{contract_id}' already exists.")
            raise typer.Exit(1)

    new_contract = {
        "id": contract_id,
        "name": name,
        "party": party,
        "status": "draft",
        "created_at": datetime.now().isoformat(),
    }
    contracts.append(new_contract)
    data["contracts"] = contracts
    _save_contracts(data)
    typer.echo(f"Contract '{name}' added successfully.")


@app.command()
def approve(contract_id: str = typer.Argument(..., help="Contract ID to approve")):
    """Approve a contract."""
    data = _load_contracts()
    contracts = data.get("contracts", [])

    contract = next((c for c in contracts if c["id"] == contract_id), None)
    if not contract:
        typer.echo(f"Error: Contract '{contract_id}' not found.")
        raise typer.Exit(1)

    contract["status"] = "approved"
    contract["approved_at"] = datetime.now().isoformat()
    _save_contracts(data)
    typer.echo(f"Contract '{contract['name']}' approved!")


@app.command()
def compliance_check():
    """Run compliance checks on active contracts."""
    data = _load_contracts()
    contracts = data.get("contracts", [])

    active = [c for c in contracts if c.get("status") == "active"]
    draft = [c for c in contracts if c.get("status") == "draft"]

    typer.echo("")
    typer.echo("Compliance Check")
    typer.echo("================")
    typer.echo(f"  Active Contracts: {len(active)}")
    typer.echo(f"  Draft Contracts: {len(draft)}")
    typer.echo("")
