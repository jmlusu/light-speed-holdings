"""Human Resources department commands."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import typer
import yaml

app = typer.Typer(help="Human Resources operations")
onboard_app = typer.Typer(help="Agent onboarding lifecycle")
app.add_typer(onboard_app, name="onboard")

HR_DIR = Path("hr")


# ── Roster helpers ────────────────────────────────────────────────────


def _load_agents_roster() -> dict[str, Any]:
    """Load the HR agent roster from YAML."""
    roster_file = HR_DIR / "roster.yaml"
    if not roster_file.exists():
        return {"agents": []}
    with open(roster_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"agents": []}


def _save_agents_roster(data: dict[str, Any]) -> None:
    """Persist the HR agent roster to YAML."""
    HR_DIR.mkdir(exist_ok=True)
    roster_file = HR_DIR / "roster.yaml"
    with open(roster_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


# ── Roster commands ───────────────────────────────────────────────────


@app.command()
def list_agents() -> None:
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
def deactivate(agent_id: str = typer.Argument(..., help="Agent ID to deactivate")) -> None:
    """Deactivate an agent from the workforce.

    Args:
        agent_id: Agent ID to deactivate.
    """
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
def workforce_report() -> None:
    """Generate workforce statistics report."""
    data = _load_agents_roster()
    agents = data.get("agents", [])

    total = len(agents)
    active = sum(1 for a in agents if a.get("status") == "active")
    inactive = total - active

    departments: dict[str, int] = {}
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


# ── Onboarding lifecycle commands ─────────────────────────────────────


def _get_manager() -> Any:
    """Lazy-load the OnboardingManager."""
    from ai_company.hr.onboarding import OnboardingManager

    return OnboardingManager()


@onboard_app.command("request")
def onboard_request(
    agent_id: str = typer.Argument(..., help="Snake-case agent ID"),
    name: str = typer.Option(..., "--name", "-n", help="Agent name"),
    role: str = typer.Option(..., "--role", "-r", help="Agent role"),
    department: str = typer.Option(..., "--department", "-d", help="Department"),
    agent_type: str = typer.Option("specialist", "--type", "-t", help="Agent type"),
    reports_to: str = typer.Option("", "--reports-to", help="Parent agent ID or name"),
) -> None:
    """Submit a new agent onboarding request."""
    mgr = _get_manager()
    req = mgr.create_request(
        agent_id=agent_id,
        name=name,
        role=role,
        department=department,
        agent_type=agent_type,
        reports_to=reports_to,
    )
    typer.echo(f"Onboarding request created: {req.request_id}")
    typer.echo(f"  Agent: {req.agent_id} ({req.name})")
    typer.echo(f"  Department: {req.department}")
    typer.echo(f"  Status: {req.status.value}")
    typer.echo("")
    typer.echo("Next step: ai-company hr onboard advance " + req.request_id)


@onboard_app.command("status")
def onboard_status(
    request_id: str = typer.Argument(..., help="Onboarding request ID"),
) -> None:
    """Show the status of an onboarding request."""
    from ai_company.hr.onboarding import STATE_LABELS, is_terminal

    mgr = _get_manager()
    req = mgr.get_request(request_id)
    if not req:
        typer.echo(f"Error: Request '{request_id}' not found.")
        raise typer.Exit(1)

    label = STATE_LABELS.get(req.status, req.status.value)
    terminal = " (terminal)" if is_terminal(req.status) else ""

    typer.echo("")
    typer.echo(f"Onboarding Request: {req.request_id}")
    typer.echo("=" * 40)
    typer.echo(f"  Agent:     {req.agent_id} ({req.name})")
    typer.echo(f"  Role:      {req.role}")
    typer.echo(f"  Department: {req.department}")
    typer.echo(f"  Status:    {req.status.value}{terminal}")
    typer.echo(f"  Label:     {label}")
    typer.echo(f"  Created:   {req.created_at}")
    typer.echo(f"  Updated:   {req.updated_at}")
    if req.security_reviewer:
        typer.echo(f"  Security reviewer: {req.security_reviewer} ({req.security_reviewed_at})")
    if req.approval_request_id:
        typer.echo(f"  Approval ID: {req.approval_request_id}")
    if req.error:
        typer.echo(f"  Error: {req.error}")
    typer.echo("")


@onboard_app.command("advance")
def onboard_advance(
    request_id: str = typer.Argument(..., help="Onboarding request ID"),
) -> None:
    """Advance an onboarding request to the next state."""
    from ai_company.hr.onboarding import STATE_LABELS

    mgr = _get_manager()
    req = mgr.get_request(request_id)
    if not req:
        typer.echo(f"Error: Request '{request_id}' not found.")
        raise typer.Exit(1)

    try:
        req = mgr.advance(req)
    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(1) from None

    label = STATE_LABELS.get(req.status, req.status.value)
    typer.echo(f"Advanced to: {req.status.value}")
    typer.echo(f"  Label: {label}")
    typer.echo("")
    if req.status.value == "active":
        typer.echo("Agent is now active and deployed.")
    else:
        typer.echo(f"Next step: ai-company hr onboard advance {req.request_id}")


@onboard_app.command("approve")
def onboard_approve(
    request_id: str = typer.Argument(..., help="Onboarding request ID"),
) -> None:
    """Approve an onboarding request (moves to ACTIVE)."""
    mgr = _get_manager()
    req = mgr.get_request(request_id)
    if not req:
        typer.echo(f"Error: Request '{request_id}' not found.")
        raise typer.Exit(1)

    try:
        req = mgr.approve(req)
    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(1) from None

    typer.echo(f"Agent '{req.agent_id}' approved and activated.")
    typer.echo(f"  Request: {req.request_id}")
    typer.echo(f"  Status:  {req.status.value}")


@onboard_app.command("reject")
def onboard_reject(
    request_id: str = typer.Argument(..., help="Onboarding request ID"),
    reason: str = typer.Option("", "--reason", help="Rejection reason"),
) -> None:
    """Reject an onboarding request."""
    mgr = _get_manager()
    req = mgr.get_request(request_id)
    if not req:
        typer.echo(f"Error: Request '{request_id}' not found.")
        raise typer.Exit(1)

    try:
        req = mgr.reject(req, reason=reason)
    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(1) from None

    typer.echo(f"Request '{request_id}' rejected.")
    if reason:
        typer.echo(f"  Reason: {reason}")


@onboard_app.command("list")
def onboard_list(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
) -> None:
    """List all onboarding requests."""
    from ai_company.hr.onboarding import STATE_LABELS, OnboardingStatus

    mgr = _get_manager()
    filter_status = None
    if status:
        try:
            filter_status = OnboardingStatus(status)
        except ValueError:
            typer.echo(f"Error: Invalid status '{status}'.")
            typer.echo(f"Valid: {', '.join(s.value for s in OnboardingStatus)}")
            raise typer.Exit(1) from None

    requests = mgr.list_requests(status=filter_status)

    if not requests:
        typer.echo("No onboarding requests found.")
        return

    typer.echo("")
    typer.echo("Onboarding Requests")
    typer.echo("===================")
    for req in requests:
        label = STATE_LABELS.get(req.status, req.status.value)
        typer.echo(f"  {req.request_id}: {req.agent_id} [{req.status.value}]")
        typer.echo(f"    {label}")
        typer.echo(f"    Dept: {req.department} | Created: {req.created_at[:10]}")
        typer.echo("")
