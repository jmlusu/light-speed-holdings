"""
Orchestrator management commands for autonomous coordination.
"""

from typing import Optional
import typer

app = typer.Typer(help="Autonomous coordination management")
scheduler_app = typer.Typer(help="Manage scheduled tasks")
escalation_app = typer.Typer(help="Manage escalation rules")
approval_app = typer.Typer(help="Manage approval gates")

app.add_typer(scheduler_app, name="scheduler")
app.add_typer(escalation_app, name="escalation")
app.add_typer(approval_app, name="approval")


@scheduler_app.command("list")
def scheduler_list():
    """List all scheduled tasks."""
    from ai_company.orchestrator.scheduler import Scheduler

    scheduler = Scheduler()
    tasks = scheduler.list_tasks()

    if not tasks:
        typer.echo("No scheduled tasks.")
        return

    typer.echo("")
    typer.echo("Scheduled Tasks")
    typer.echo("================")
    for task in tasks:
        status = "enabled" if task.enabled else "disabled"
        typer.echo(f"  {task.id}: {task.name} [{status}]")
        typer.echo(f"    Interval: {task.interval_minutes or 'N/A'} minutes")
        typer.echo("")


@scheduler_app.command("add")
def scheduler_add(
    task_id: str = typer.Argument(..., help="Unique task ID"),
    name: str = typer.Option(..., help="Task name"),
    interval: int = typer.Option(60, help="Interval in minutes"),
):
    """Add a new scheduled task."""
    from ai_company.orchestrator.scheduler import Scheduler

    scheduler = Scheduler()
    scheduler.add_task(task_id, name, interval_minutes=interval)
    typer.echo(f"Scheduled task '{name}' added.")


@escalation_app.command("list")
def escalation_list():
    """List all escalation rules."""
    from ai_company.orchestrator.escalation import EscalationManager

    manager = EscalationManager()
    rules = manager.list_rules()

    if not rules:
        typer.echo("No escalation rules.")
        return

    typer.echo("")
    typer.echo("Escalation Rules")
    typer.echo("================")
    for rule in rules:
        typer.echo(f"  {rule.id}: {rule.name}")
        typer.echo(f"    Trigger: {rule.trigger}")
        typer.echo(f"    Escalate To: {rule.escalate_to}")
        typer.echo("")


@escalation_app.command("add")
def escalation_add(
    rule_id: str = typer.Argument(..., help="Unique rule ID"),
    name: str = typer.Option(..., help="Rule name"),
    trigger: str = typer.Option(..., help="Escalation trigger condition"),
    escalate_to: str = typer.Option(..., help="Agent to escalate to"),
):
    """Add a new escalation rule."""
    from ai_company.orchestrator.escalation import EscalationManager

    manager = EscalationManager()
    manager.add_rule(rule_id, name, trigger, escalate_to)
    typer.echo(f"Escalation rule '{name}' added.")


@approval_app.command("pending")
def approval_pending():
    """List pending approval requests."""
    from ai_company.orchestrator.approval import ApprovalGate

    gate = ApprovalGate()
    pending = gate.get_pending_requests()

    if not pending:
        typer.echo("No pending approval requests.")
        return

    typer.echo("")
    typer.echo("Pending Approvals")
    typer.echo("=================")
    for req in pending:
        typer.echo(f"  {req.id}: {req.action}")
        typer.echo(f"    Agent: {req.agent_id}")
        typer.echo(f"    Description: {req.description}")
        typer.echo("")


@approval_app.command("approve")
def approval_approve(
    request_id: str = typer.Argument(..., help="Request ID to approve"),
    approved_by: str = typer.Option("human_operator", help="Who approved"),
):
    """Approve a pending request."""
    from ai_company.orchestrator.approval import ApprovalGate

    gate = ApprovalGate()
    if gate.approve(request_id, approved_by):
        typer.echo(f"Request '{request_id}' approved.")
    else:
        typer.echo(f"Error: Request '{request_id}' not found or already processed.")
        raise typer.Exit(1)


@approval_app.command("reject")
def approval_reject(
    request_id: str = typer.Argument(..., help="Request ID to reject"),
    rejected_by: str = typer.Option("human_operator", help="Who rejected"),
    notes: Optional[str] = typer.Option(None, help="Rejection notes"),
):
    """Reject a pending request."""
    from ai_company.orchestrator.approval import ApprovalGate

    gate = ApprovalGate()
    if gate.reject(request_id, rejected_by, notes):
        typer.echo(f"Request '{request_id}' rejected.")
    else:
        typer.echo(f"Error: Request '{request_id}' not found or already processed.")
        raise typer.Exit(1)
