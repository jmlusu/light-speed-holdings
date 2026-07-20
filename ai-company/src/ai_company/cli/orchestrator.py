"""
Orchestrator management commands for autonomous coordination.
"""

from typing import Optional

import typer

app = typer.Typer(help="Autonomous coordination management")
scheduler_app = typer.Typer(help="Manage scheduled tasks")
escalation_app = typer.Typer(help="Manage escalation rules")
approval_app = typer.Typer(help="Manage approval gates")
postmortem_app = typer.Typer(help="Manage incident postmortems")

app.add_typer(scheduler_app, name="scheduler")
app.add_typer(escalation_app, name="escalation")
app.add_typer(approval_app, name="approval")
app.add_typer(postmortem_app, name="postmortem")


# ─── tick ────────────────────────────────────────────────────────────


@app.command()
def tick() -> None:
    """Run one orchestrator cycle: check due tasks, escalations, approvals."""
    from ai_company.orchestrator.approval import ApprovalGate
    from ai_company.orchestrator.escalation import EscalationManager
    from ai_company.orchestrator.scheduler import Scheduler

    scheduler = Scheduler()
    escalation = EscalationManager()
    gate = ApprovalGate()

    pending_tasks = scheduler.get_pending_tasks()
    pending_escalations = escalation.get_pending_escalations()
    pending_approvals = gate.get_pending_requests()

    typer.echo("Orchestrator Tick")
    typer.echo("=" * 40)

    # ── Scheduled tasks ──
    typer.echo(f"\nScheduled tasks due: {len(pending_tasks)}")
    if pending_tasks:
        for task in pending_tasks:
            typer.echo(f"  [{task.id}] {task.name}")
            if task.task_template:
                for k, v in task.task_template.items():
                    typer.echo(f"    {k}: {v}")
        # Mark them completed so they reschedule
        for task in pending_tasks:
            scheduler.mark_completed(task.id)
            typer.echo(f"  Marked '{task.id}' completed, rescheduled.")
    else:
        typer.echo("  (none)")

    # ── Escalations ──
    typer.echo(f"\nPending escalations: {len(pending_escalations)}")
    if pending_escalations:
        for evt in pending_escalations:
            typer.echo(f"  [{evt.rule_id}] {evt.from_agent} -> {evt.to_agent}")
            typer.echo(f"    Reason: {evt.reason}")
            typer.echo(f"    Task: {evt.task_id}")
    else:
        typer.echo("  (none)")

    # ── Approvals ──
    typer.echo(f"\nPending approvals: {len(pending_approvals)}")
    if pending_approvals:
        for req in pending_approvals:
            typer.echo(f"  [{req.id}] {req.agent_id}: {req.action}")
            typer.echo(f"    {req.description}")
    else:
        typer.echo("  (none)")

    # ── Summary ──
    total = len(pending_tasks) + len(pending_escalations) + len(pending_approvals)
    typer.echo(f"\nTotal items needing attention: {total}")


# ─── briefing ────────────────────────────────────────────────────────


@app.command()
def briefing() -> None:
    """Generate a daily executive briefing from the inbox and registry."""
    from ai_company.orchestrator.briefing import BriefingGenerator

    gen = BriefingGenerator()
    active_agents, task_count = gen.generate()
    typer.echo(f"Active agents: {active_agents}, pending tasks: {task_count}")


# ─── scheduler subcommands ──────────────────────────────────────────


@scheduler_app.command("list")
def scheduler_list() -> None:
    """List all scheduled tasks."""
    from ai_company.orchestrator.scheduler import Scheduler

    tasks = Scheduler().list_tasks()
    if not tasks:
        typer.echo("No scheduled tasks.")
        return

    typer.echo("")
    typer.echo("Scheduled Tasks")
    typer.echo("=" * 40)
    for task in tasks:
        status = "enabled" if task.enabled else "disabled"
        typer.echo(f"  {task.id}: {task.name} [{status}]")
        typer.echo(f"    Interval: {task.interval_minutes or 'N/A'} min")
        if task.next_run:
            typer.echo(f"    Next run: {task.next_run}")
        typer.echo("")


@scheduler_app.command("add")
def scheduler_add(
    task_id: str = typer.Argument(..., help="Unique task ID"),
    name: str = typer.Option(..., help="Task name"),
    interval: int = typer.Option(60, help="Interval in minutes"),
) -> None:
    """Add a new scheduled task."""
    from ai_company.orchestrator.scheduler import Scheduler

    task = Scheduler().add_task(task_id, name, interval_minutes=interval)
    typer.echo(f"Task '{name}' added. Next run: {task.next_run}")


@scheduler_app.command("remove")
def scheduler_remove(
    task_id: str = typer.Argument(..., help="Task ID to remove"),
) -> None:
    """Remove a scheduled task."""
    from ai_company.orchestrator.scheduler import Scheduler

    if Scheduler().remove_task(task_id):
        typer.echo(f"Task '{task_id}' removed.")
    else:
        typer.echo(f"Task '{task_id}' not found.")
        raise typer.Exit(1)


# ─── escalation subcommands ─────────────────────────────────────────


@escalation_app.command("list")
def escalation_list() -> None:
    """List all escalation rules."""
    from ai_company.orchestrator.escalation import EscalationManager

    rules = EscalationManager().list_rules()
    if not rules:
        typer.echo("No escalation rules.")
        return

    typer.echo("")
    typer.echo("Escalation Rules")
    typer.echo("=" * 40)
    for rule in rules:
        typer.echo(f"  {rule.id}: {rule.name}")
        typer.echo(f"    Trigger: {rule.trigger}")
        typer.echo(f"    Escalate To: {rule.escalate_to}")
        typer.echo(f"    Max Retries: {rule.max_retries}, Timeout: {rule.timeout_minutes} min")
        typer.echo("")


@escalation_app.command("add")
def escalation_add(
    rule_id: str = typer.Argument(..., help="Unique rule ID"),
    name: str = typer.Option(..., help="Rule name"),
    trigger: str = typer.Option(..., help="Escalation trigger condition"),
    escalate_to: str = typer.Option(..., help="Agent to escalate to"),
    max_retries: int = typer.Option(3, help="Max retries before escalation"),
    timeout: int = typer.Option(30, help="Timeout in minutes"),
) -> None:
    """Add a new escalation rule."""
    from ai_company.orchestrator.escalation import EscalationManager

    EscalationManager().add_rule(rule_id, name, trigger, escalate_to, max_retries, timeout)
    typer.echo(f"Escalation rule '{name}' added.")


@escalation_app.command("remove")
def escalation_remove(
    rule_id: str = typer.Argument(..., help="Rule ID to remove"),
) -> None:
    """Remove an escalation rule."""
    from ai_company.orchestrator.escalation import EscalationManager

    if EscalationManager().remove_rule(rule_id):
        typer.echo(f"Rule '{rule_id}' removed.")
    else:
        typer.echo(f"Rule '{rule_id}' not found.")
        raise typer.Exit(1)


@escalation_app.command("pending")
def escalation_pending() -> None:
    """List unresolved escalation events."""
    from ai_company.orchestrator.escalation import EscalationManager

    events = EscalationManager().get_pending_escalations()
    if not events:
        typer.echo("No pending escalations.")
        return

    typer.echo("")
    typer.echo("Pending Escalations")
    typer.echo("=" * 40)
    for evt in events:
        typer.echo(f"  [{evt.rule_id}] {evt.from_agent} -> {evt.to_agent}")
        typer.echo(f"    Reason: {evt.reason}")
        typer.echo(f"    Task: {evt.task_id}")
        typer.echo("")


# ─── approval subcommands ───────────────────────────────────────────


@approval_app.command("pending")
def approval_pending() -> None:
    """List pending approval requests."""
    from ai_company.orchestrator.approval import ApprovalGate

    pending = ApprovalGate().get_pending_requests()
    if not pending:
        typer.echo("No pending approval requests.")
        return

    typer.echo("")
    typer.echo("Pending Approvals")
    typer.echo("=" * 40)
    for req in pending:
        typer.echo(f"  {req.id}: {req.action}")
        typer.echo(f"    Agent: {req.agent_id}")
        typer.echo(f"    Description: {req.description}")
        if req.expires_at:
            typer.echo(f"    Expires: {req.expires_at}")
        typer.echo("")


@approval_app.command("approve")
def approval_approve(
    request_id: str = typer.Argument(..., help="Request ID to approve"),
    approved_by: str = typer.Option("human-operator", help="Who approved"),
    notes: Optional[str] = typer.Option(None, help="Approval notes"),
) -> None:
    """Approve a pending request."""
    from ai_company.orchestrator.approval import ApprovalGate

    if ApprovalGate().approve(request_id, approved_by, notes):
        typer.echo(f"Request '{request_id}' approved by {approved_by}.")
    else:
        typer.echo(f"Error: Request '{request_id}' not found or already processed.")
        raise typer.Exit(1)


@approval_app.command("reject")
def approval_reject(
    request_id: str = typer.Argument(..., help="Request ID to reject"),
    rejected_by: str = typer.Option("human-operator", help="Who rejected"),
    notes: Optional[str] = typer.Option(None, help="Rejection notes"),
) -> None:
    """Reject a pending request."""
    from ai_company.orchestrator.approval import ApprovalGate

    if ApprovalGate().reject(request_id, rejected_by, notes):
        typer.echo(f"Request '{request_id}' rejected by {rejected_by}.")
    else:
        typer.echo(f"Error: Request '{request_id}' not found or already processed.")
        raise typer.Exit(1)


# ─── postmortem subcommands ──────────────────────────────────────────


@postmortem_app.command("list")
def postmortem_list() -> None:
    """List all postmortems."""
    from ai_company.orchestrator.escalation import PostmortemStore

    store = PostmortemStore()
    postmortems = store.list_all()
    if not postmortems:
        typer.echo("No postmortems found.")
        return

    typer.echo("")
    typer.echo("Postmortems")
    typer.echo("=" * 50)
    for pm in postmortems:
        typer.echo(f"  {pm.incident_id}: {pm.title}")
        typer.echo(f"    Severity: {pm.severity} | Status: {pm.status}")
        typer.echo(f"    Affected agent: {pm.affected_agent or 'N/A'}")
        typer.echo(f"    Date: {pm.date}")
        typer.echo("")


@postmortem_app.command("show")
def postmortem_show(
    incident_id: str = typer.Argument(..., help="Incident ID to display"),
) -> None:
    """Show details of a specific postmortem."""
    from ai_company.orchestrator.escalation import PostmortemStore

    store = PostmortemStore()
    pm = store.load(incident_id)
    if not pm:
        typer.echo(f"Postmortem '{incident_id}' not found.")
        raise typer.Exit(1)

    typer.echo(f"\n{'=' * 50}")
    typer.echo(f"INCIDENT: {pm.incident_id} — {pm.title}")
    typer.echo(f"{'=' * 50}")
    typer.echo(f"  Date:           {pm.date}")
    typer.echo(f"  Severity:       {pm.severity}")
    typer.echo(f"  Status:         {pm.status}")
    typer.echo(f"  Affected Agent: {pm.affected_agent or 'N/A'}")
    typer.echo(f"  Department:     {pm.department or 'N/A'}")
    typer.echo(f"  Escalation:     {pm.escalation_rule or 'N/A'}")
    typer.echo(f"  Prepared By:    {pm.prepared_by or 'N/A'}")
    typer.echo(f"  Reviewed By:    {pm.reviewed_by or 'N/A'}")

    typer.echo("\nRoot Cause:")
    typer.echo(f"  {pm.root_cause}")

    if pm.timeline:
        typer.echo("\nTimeline:")
        for entry in pm.timeline:
            typer.echo(f"  [{entry.time}] {entry.description}")

    if pm.resolution_steps:
        typer.echo("\nResolution Steps:")
        for i, step in enumerate(pm.resolution_steps, 1):
            typer.echo(f"  {i}. {step}")

    if pm.action_items:
        typer.echo("\nAction Items:")
        for item in pm.action_items:
            typer.echo(f"  [{item.id}] {item.action} — Owner: {item.owner} ({item.status})")

    if pm.lessons_learned:
        typer.echo("\nLessons Learned:")
        for lesson in pm.lessons_learned:
            typer.echo(f"  - {lesson}")

    if pm.prevention_measures:
        typer.echo("\nPrevention Measures:")
        for measure in pm.prevention_measures:
            typer.echo(f"  - {measure}")
    typer.echo("")


@postmortem_app.command("create")
def postmortem_create(
    incident_id: str = typer.Argument(..., help="Incident ID (e.g. INC-TASK-001)"),
    title: str = typer.Option(..., help="Short incident title"),
    severity: str = typer.Option("medium", help="Severity: low, medium, high, critical"),
    affected_agent: str = typer.Option("", help="Agent that caused/was affected"),
    department: str = typer.Option("", help="Department affected"),
) -> None:
    """Create a new postmortem skeleton."""
    from ai_company.orchestrator.escalation import Postmortem, PostmortemStore

    store = PostmortemStore()
    existing = store.load(incident_id)
    if existing:
        typer.echo(f"Error: Postmortem '{incident_id}' already exists.")
        raise typer.Exit(1)

    pm = Postmortem(
        incident_id=incident_id,
        title=title,
        severity=severity,
        affected_agent=affected_agent,
        department=department,
        status="draft",
    )
    store.save(pm)
    typer.echo(f"Postmortem '{incident_id}' created at orchestrator/postmortems/{incident_id}.json")


@postmortem_app.command("update")
def postmortem_update(
    incident_id: str = typer.Argument(..., help="Incident ID to update"),
    root_cause: Optional[str] = typer.Option(None, help="Root cause description"),
    status: Optional[str] = typer.Option(None, help="New status: draft, in-progress, resolved"),
    reviewed_by: Optional[str] = typer.Option(None, help="Reviewer name"),
) -> None:
    """Update an existing postmortem."""
    from ai_company.orchestrator.escalation import PostmortemStore

    store = PostmortemStore()
    pm = store.load(incident_id)
    if not pm:
        typer.echo(f"Postmortem '{incident_id}' not found.")
        raise typer.Exit(1)

    updated = False
    if root_cause is not None:
        pm.root_cause = root_cause
        updated = True
    if status is not None:
        pm.status = status
        updated = True
    if reviewed_by is not None:
        pm.reviewed_by = reviewed_by
        updated = True

    if updated:
        from datetime import datetime
        pm.last_updated = datetime.now().isoformat()
        store.save(pm)
        typer.echo(f"Postmortem '{incident_id}' updated.")
    else:
        typer.echo("No fields to update. Use --root-cause, --status, or --reviewed-by.")
        raise typer.Exit(1)


@postmortem_app.command("render")
def postmortem_render(
    incident_id: str = typer.Argument(..., help="Incident ID to render as markdown"),
) -> None:
    """Render a postmortem to markdown using the Jinja2 template."""
    from pathlib import Path

    from jinja2 import Environment, FileSystemLoader

    from ai_company.orchestrator.escalation import PostmortemStore

    store = PostmortemStore()
    pm = store.load(incident_id)
    if not pm:
        typer.echo(f"Postmortem '{incident_id}' not found.")
        raise typer.Exit(1)

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(str(templates_dir)), autoescape=True)
    template = env.get_template("postmortem.md.j2")

    rendered = template.render(
        incident_id=pm.incident_id,
        title=pm.title,
        date=pm.date,
        severity=pm.severity,
        affected_agent=pm.affected_agent,
        department=pm.department,
        escalation_rule=pm.escalation_rule,
        duration=pm.duration,
        status=pm.status,
        root_cause=pm.root_cause,
        impact={
            "tasks_before": pm.impact.tasks_before,
            "tasks_during": pm.impact.tasks_during,
            "tasks_after": pm.impact.tasks_after,
            "agents_before": pm.impact.agents_before,
            "agents_during": pm.impact.agents_during,
            "agents_after": pm.impact.agents_after,
            "downtime_minutes": pm.impact.downtime_minutes,
        },
        timeline=[{"time": e.time, "description": e.description} for e in pm.timeline],
        resolution_steps=pm.resolution_steps,
        action_items=[
            {"id": a.id, "action": a.action, "owner": a.owner, "due_date": a.due_date, "status": a.status}
            for a in pm.action_items
        ],
        lessons_learned=pm.lessons_learned,
        prevention_measures=pm.prevention_measures,
        prepared_by=pm.prepared_by,
        reviewed_by=pm.reviewed_by,
        last_updated=pm.last_updated,
    )

    out_path = Path(f"docs/postmortems/{incident_id}.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    typer.echo(f"Rendered to {out_path}")
