"""
Human Resources department commands.
"""

from pathlib import Path
import typer
import yaml
from datetime import datetime

app = typer.Typer(help="Human Resources operations")
HR_DIR = Path("hr")


def _load_agents_roster() -> dict:
    roster_file = HR_DIR / "roster.yaml"
    if not roster_file.exists():
        return {"agents": []}
    with open(roster_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"agents": []}


def _save_agents_roster(data: dict):
    HR_DIR.mkdir(exist_ok=True)
    roster_file = HR_DIR / "roster.yaml"
    with open(roster_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


@app.command()
def list_agents():
    """List all agents in the workforce."""
    data = _load_agents_roster()
    agents = data.get("agents", [])

    if not agents:
        typer.echo("No agents in roster.")
        return

    typer.echo("")
    typer.echo("Agent Workforce")
    typer.echo("===============")
    for agent in agents:
        status = agent.get("status", "active")
        typer.echo(f"  {agent['id']}: {agent['role']} [{status}]")
        typer.echo(f"    Department: {agent.get('department', 'N/A')}")
        typer.echo("")


@app.command()
def onboard(
    agent_id: str = typer.Argument(..., help="Agent ID to onboard"),
    role: str = typer.Option(..., help="Agent role"),
    department: str = typer.Option(..., help="Department"),
):
    """Onboard a new agent to the workforce."""
    data = _load_agents_roster()
    agents = data.get("agents", [])

    for agent in agents:
        if agent["id"] == agent_id:
            typer.echo(f"Error: Agent '{agent_id}' already exists.")
            raise typer.Exit(1)

    new_agent = {
        "id": agent_id,
        "role": role,
        "department": department,
        "status": "active",
        "onboarded_at": datetime.now().isoformat(),
    }
    agents.append(new_agent)
    data["agents"] = agents
    _save_agents_roster(data)
    typer.echo(f"Agent '{agent_id}' onboarded successfully.")


@app.command()
def deactivate(agent_id: str = typer.Argument(..., help="Agent ID to deactivate")):
    """Deactivate an agent from the workforce."""
    data = _load_agents_roster()
    agents = data.get("agents", [])

    agent = next((a for a in agents if a["id"] == agent_id), None)
    if not agent:
        typer.echo(f"Error: Agent '{agent_id}' not found.")
        raise typer.Exit(1)

    agent["status"] = "inactive"
    agent["deactivated_at"] = datetime.now().isoformat()
    _save_agents_roster(data)
    typer.echo(f"Agent '{agent_id}' deactivated.")


@app.command()
def workforce_report():
    """Generate workforce statistics report."""
    data = _load_agents_roster()
    agents = data.get("agents", [])

    total = len(agents)
    active = sum(1 for a in agents if a.get("status") == "active")
    inactive = total - active

    departments = {}
    for agent in agents:
        dept = agent.get("department", "Unknown")
        departments[dept] = departments.get(dept, 0) + 1

    typer.echo("")
    typer.echo("Workforce Report")
    typer.echo("================")
    typer.echo(f"  Total Agents: {total}")
    typer.echo(f"  Active: {active}")
    typer.echo(f"  Inactive: {inactive}")
    typer.echo("")
    typer.echo("By Department:")
    for dept, count in departments.items():
        typer.echo(f"  {dept}: {count}")
    typer.echo("")
