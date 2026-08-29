"""Agent onboarding CLI commands with HITL gate integration.

Usage:
    ai-company onboarding request --agent-id <id> --role <role> --department <dept>
    ai-company onboarding approve <request_id> --by <approver>
    ai-company onboarding reject <request_id> --by <rejector> --reason <reason>
    ai-company onboarding status <request_id>
    ai-company onboarding list [--state <state>]
    ai-company onboarding advance <request_id>
    ai-company onboarding security-review <request_id> --reviewer <reviewer> --approved/--rejected
    ai-company onboarding complete-generation <request_id>
    ai-company onboarding complete-testing <request_id> --passed/--failed
    ai-company onboarding archive <request_id>
    ai-company onboarding retry <request_id>
"""

from __future__ import annotations

import typer

from ai_company.data import get_database

app = typer.Typer(help="Agent onboarding with HITL approval gate")


@app.command()
def request(
    agent_id: str = typer.Option(..., help="Unique agent identifier"),
    role: str = typer.Option(..., help="Agent role (e.g. backend-engineer)"),
    department: str = typer.Option(..., help="Department"),
    name: str = typer.Option("", help="Human-readable agent name (defaults to agent_id)"),
    tools: str = typer.Option("", help="Comma-separated tool permissions"),
    responsibilities: str = typer.Option("", help="Comma-separated responsibilities"),
    reports_to: str = typer.Option("", help="Parent agent ID or name"),
    guidelines: str = typer.Option("", help="Free-text guidelines"),
    expires: int = typer.Option(48, help="Approval window in hours"),
) -> None:
    """Submit an agent onboarding request through the HITL gate.

    Creates an approval request visible in the dashboard Approvals tab.
    The request expires after --expires hours (default 48).
    """
    from ai_company.services.onboarding import OnboardingService

    tool_list = [t.strip() for t in tools.split(",") if t.strip()] if tools else []
    resp_list = (
        [r.strip() for r in responsibilities.split(",") if r.strip()] if responsibilities else []
    )

    svc = OnboardingService(database=get_database())
    result = svc.request_onboarding(
        agent_id=agent_id,
        role=role,
        department=department,
        name=name,
        tools=tool_list,
        responsibilities=resp_list,
        reports_to=reports_to,
        guidelines=guidelines,
        expires_in_hours=expires,
    )

    if not result.success or result.data is None:
        typer.echo(f"Error: {'; '.join(result.errors)}", err=True)
        raise typer.Exit(1)

    data = result.data
    typer.echo(f"Onboarding request submitted: {data['request_id']}")
    typer.echo(f"  Agent:      {data['agent_id']}")
    typer.echo(f"  Name:       {data['name']}")
    typer.echo(f"  Role:       {data['role']}")
    typer.echo(f"  Department: {data['department']}")
    typer.echo(f"  Tier:       {data['tier']}")
    typer.echo(f"  Approval:   {data['approval_request_id']}")
    typer.echo(f"  State:      {data['state']}")
    typer.echo("")
    typer.echo("The request is now visible in the dashboard Approvals tab.")
    typer.echo(f"Expires in {expires} hours if not approved.")


@app.command()
def approve(
    request_id: str = typer.Argument(..., help="Onboarding request ID"),
    by: str = typer.Option("human-ceo", help="Approver identity"),
    notes: str = typer.Option("", help="Approval notes"),
) -> None:
    """Approve a pending onboarding request.

    Transitions the request from approval to active.
    """
    from ai_company.services.onboarding import OnboardingService

    svc = OnboardingService(database=get_database())
    result = svc.approve_onboarding(request_id, approved_by=by, notes=notes)

    if not result.success or result.data is None:
        typer.echo(f"Error: {'; '.join(result.errors)}", err=True)
        raise typer.Exit(1)

    data = result.data
    typer.echo(f"Onboarding request '{request_id}' approved by {by}")
    typer.echo(f"  Agent: {data['agent_id']}")
    typer.echo(f"  State: {data['state']}")


@app.command()
def reject(
    request_id: str = typer.Argument(..., help="Onboarding request ID"),
    by: str = typer.Option("human-ceo", help="Rejection identity"),
    reason: str = typer.Option(..., help="Rejection reason"),
) -> None:
    """Reject a pending onboarding request.

    Archives the request with the rejection reason.
    """
    from ai_company.services.onboarding import OnboardingService

    svc = OnboardingService(database=get_database())
    result = svc.reject_onboarding(request_id, rejected_by=by, reason=reason)

    if not result.success or result.data is None:
        typer.echo(f"Error: {'; '.join(result.errors)}", err=True)
        raise typer.Exit(1)

    data = result.data
    typer.echo(f"Onboarding request '{request_id}' rejected by {by}")
    typer.echo(f"  Agent:  {data['agent_id']}")
    typer.echo(f"  Reason: {data['rejection_reason']}")
    typer.echo(f"  State:  {data['state']}")


@app.command()
def status(
    request_id: str = typer.Argument(..., help="Onboarding request ID"),
) -> None:
    """Show the current status of an onboarding request."""
    from ai_company.services.onboarding import OnboardingService

    svc = OnboardingService(database=get_database())
    result = svc.get_status(request_id)

    if not result.success or result.data is None:
        typer.echo(f"Error: {'; '.join(result.errors)}", err=True)
        raise typer.Exit(1)

    data = result.data
    typer.echo("")
    typer.echo("Onboarding Request Status")
    typer.echo("=" * 40)
    typer.echo(f"  Request ID:  {data['id']}")
    typer.echo(f"  Agent ID:    {data['agent_id']}")
    typer.echo(f"  Name:        {data.get('name', 'N/A')}")
    typer.echo(f"  Role:        {data['role']}")
    typer.echo(f"  Department:  {data['department']}")
    typer.echo(f"  Type:        {data.get('agent_type', 'N/A')}")
    typer.echo(f"  Reports to:  {data.get('reports_to', 'N/A')}")
    typer.echo(f"  Tools:       {', '.join(data.get('tools', [])) or 'none'}")
    typer.echo(f"  State:       {data['state']}")
    typer.echo(f"  Approval ID: {data.get('approval_request_id', 'N/A')}")
    typer.echo(f"  HITL Tier:   {data.get('hitl_tier', 'N/A')}")
    typer.echo(f"  Security:    {data.get('security_reviewer', 'N/A')}")
    typer.echo(f"  Created:     {data.get('created_at', 'N/A')}")
    typer.echo(f"  Updated:     {data.get('updated_at', 'N/A')}")
    if data.get("error"):
        typer.echo(f"  Error:       {data['error']}")
    typer.echo("")


@app.command(name="list")
def list_requests(
    state: str = typer.Option("", help="Filter by state"),
) -> None:
    """List all onboarding requests."""
    from ai_company.services.onboarding import OnboardingService

    svc = OnboardingService(database=get_database())
    result = svc.list_requests(state=state)

    if not result.success or result.data is None:
        typer.echo(f"Error: {'; '.join(result.errors)}", err=True)
        raise typer.Exit(1)

    requests = result.data
    if not requests:
        typer.echo("No onboarding requests found.")
        return

    typer.echo("")
    typer.echo("Agent Onboarding Requests")
    typer.echo("=" * 70)
    for r in requests:
        typer.echo(f"  {r['id']}: {r['agent_id']} ({r['role']}) [{r.get('state', 'unknown')}]")
        typer.echo(f"    Department: {r.get('department', 'N/A')}")
        typer.echo(f"    Created:    {r.get('created_at', 'N/A')}")
    typer.echo("")


@app.command()
def advance(
    request_id: str = typer.Argument(..., help="Onboarding request ID"),
) -> None:
    """Advance an onboarding request to its next logical state.

    The next state is determined by the happy-path order:
    requested → config_review → security_review → generating → testing → approval → active
    """
    from ai_company.services.onboarding import OnboardingService

    svc = OnboardingService(database=get_database())
    result = svc.advance_to_next(request_id)

    if not result.success or result.data is None:
        typer.echo(f"Error: {'; '.join(result.errors)}", err=True)
        raise typer.Exit(1)

    data = result.data
    typer.echo(f"Request '{request_id}' advanced to state '{data['state']}'")
    typer.echo(f"  Agent: {data['agent_id']}")


@app.command()
def security_review(
    request_id: str = typer.Argument(..., help="Onboarding request ID"),
    reviewer: str = typer.Option("cto", help="Security reviewer ID"),
    approved: bool = typer.Option(True, help="Whether approved or rejected"),
    reason: str = typer.Option("", help="Rejection reason (if rejected)"),
) -> None:
    """Record the CTO security review outcome.

    If approved, transitions to generating. If rejected, transitions to rejected.
    """
    from ai_company.services.onboarding import OnboardingService

    svc = OnboardingService(database=get_database())
    result = svc.security_review(request_id, reviewer=reviewer, approved=approved, reason=reason)

    if not result.success or result.data is None:
        typer.echo(f"Error: {'; '.join(result.errors)}", err=True)
        raise typer.Exit(1)

    data = result.data
    status = "approved" if data["approved"] else "rejected"
    typer.echo(f"Security review for '{request_id}' {status} by {data['reviewer']}")
    typer.echo(f"  Agent: {data['agent_id']}")
    typer.echo(f"  State: {data['state']}")


@app.command()
def complete_generation(
    request_id: str = typer.Argument(..., help="Onboarding request ID"),
    result: str = typer.Option("", help="Step result data"),
) -> None:
    """Complete the generation step and advance to testing."""
    from ai_company.services.onboarding import OnboardingService

    svc = OnboardingService(database=get_database())
    res = svc.complete_generation(request_id, result=result)

    if not res.success or res.data is None:
        typer.echo(f"Error: {'; '.join(res.errors)}", err=True)
        raise typer.Exit(1)

    data = res.data
    typer.echo(f"Generation completed for request '{request_id}'")
    typer.echo(f"  Agent: {data['agent_id']}")
    typer.echo(f"  State: {data['state']}")


@app.command()
def complete_testing(
    request_id: str = typer.Argument(..., help="Onboarding request ID"),
    passed: bool = typer.Option(True, help="Whether tests passed or failed"),
    result: str = typer.Option("", help="Step result data"),
) -> None:
    """Complete the testing step and advance to approval or failed."""
    from ai_company.services.onboarding import OnboardingService

    svc = OnboardingService(database=get_database())
    res = svc.complete_testing(request_id, passed=passed, result=result)

    if not res.success or res.data is None:
        typer.echo(f"Error: {'; '.join(res.errors)}", err=True)
        raise typer.Exit(1)

    data = res.data
    status = "passed" if data["passed"] else "failed"
    typer.echo(f"Testing {status} for request '{request_id}'")
    typer.echo(f"  Agent: {data['agent_id']}")
    typer.echo(f"  State: {data['state']}")


@app.command()
def archive(
    request_id: str = typer.Argument(..., help="Onboarding request ID"),
) -> None:
    """Archive an onboarding request."""
    from ai_company.services.onboarding import OnboardingService

    svc = OnboardingService(database=get_database())
    result = svc.archive(request_id)

    if not result.success or result.data is None:
        typer.echo(f"Error: {'; '.join(result.errors)}", err=True)
        raise typer.Exit(1)

    data = result.data
    typer.echo(f"Request '{request_id}' archived")
    typer.echo(f"  Agent: {data['agent_id']}")
    typer.echo(f"  State: {data['state']}")


@app.command()
def retry(
    request_id: str = typer.Argument(..., help="Onboarding request ID"),
) -> None:
    """Retry a failed onboarding request by transitioning back to generating."""
    from ai_company.services.onboarding import OnboardingService

    svc = OnboardingService(database=get_database())
    result = svc.retry_from_failure(request_id)

    if not result.success or result.data is None:
        typer.echo(f"Error: {'; '.join(result.errors)}", err=True)
        raise typer.Exit(1)

    data = result.data
    typer.echo(f"Request '{request_id}' retry initiated")
    typer.echo(f"  Agent: {data['agent_id']}")
    typer.echo(f"  State: {data['state']}")
