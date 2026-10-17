"""Foaster-style AI consulting engagement CLI commands.

Provides commands for starting consulting engagements, deploying interview
agents, tracking progress, reviewing roadmaps, and feeding learnings
back into the knowledge flywheel.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import typer
import yaml

app = typer.Typer(help="Foaster-style AI consulting engagements")
ENGAGEMENTS_DIR = Path("consulting")
MEMORY_DIR = Path("memory")


def _get_memory_store() -> Any:
    """Get the memory store for knowledge flywheel integration."""
    from ai_company.memory.engine import MemoryStore

    return MemoryStore(base_dir=str(MEMORY_DIR))


def _store_engagement_learning(
    memory_type: str,
    content: str,
    engagement_id: str,
    agent_id: str = "",
    tags: list[str] | None = None,
) -> None:
    """Store a learning from an engagement in the memory engine."""
    store = _get_memory_store()
    all_tags = (tags or []) + ["consulting", engagement_id]
    store.store(
        memory_type=memory_type,
        content=content,
        agent_id=agent_id,
        tags=all_tags,
        metadata={"engagement_id": engagement_id, "source": "foaster_engagement"},
    )


def _load_engagements_file() -> dict[str, Any]:
    """Load engagements YAML from the consulting data directory."""
    engagements_file = ENGAGEMENTS_DIR / "engagements.yaml"
    if not engagements_file.exists():
        return {"engagements": []}
    with open(engagements_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"engagements": []}


def _save_engagements_file(data: dict[str, Any]) -> None:
    """Persist engagements YAML to the consulting data directory."""
    ENGAGEMENTS_DIR.mkdir(exist_ok=True)
    engagements_file = ENGAGEMENTS_DIR / "engagements.yaml"
    with open(engagements_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


@app.command()
def start(
    client_id: str = typer.Option(..., "--client", "-c", help="Client ID from the client registry"),
    name: str = typer.Option(..., "--name", "-n", help="Engagement name"),
    scope: str = typer.Option("ai_transformation", "--scope", "-s", help="Engagement scope"),
    departments: str = typer.Option(
        "all", "--departments", "-d", help="Comma-separated list of departments to interview"
    ),
) -> None:
    """Start a new Foaster-style AI consulting engagement."""
    data = _load_engagements_file()
    engagements = data.get("engagements", [])

    engagement_id = f"eng_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    new_engagement = {
        "id": engagement_id,
        "client_id": client_id,
        "name": name,
        "scope": scope,
        "departments": [d.strip() for d in departments.split(",")],
        "status": "onboarding",
        "current_step": "onboarding",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "steps_completed": [],
        "interview_results": [],
        "workflow_maps": [],
        "opportunities": [],
        "roadmap": None,
        "client_feedback": None,
    }
    engagements.append(new_engagement)
    data["engagements"] = engagements
    _save_engagements_file(data)

    typer.echo(f"Consulting engagement '{name}' started with ID '{engagement_id}'.")
    typer.echo(f"  Client: {client_id}")
    typer.echo(f"  Scope: {scope}")
    depts = new_engagement["departments"]
    typer.echo(f"  Departments: {', '.join(depts) if isinstance(depts, list) else depts or 'N/A'}")
    typer.echo("")
    typer.echo("Next steps:")
    typer.echo(
        f"  1. Deploy interview agents: ai-company consulting deploy-interviews --engagement {engagement_id}"
    )
    typer.echo(
        f"  2. Check status:            ai-company consulting status --engagement {engagement_id}"
    )


@app.command()
def status(
    engagement_id: str = typer.Option(..., "--engagement", "-e", help="Engagement ID"),
) -> None:
    """Check the status of a consulting engagement."""
    data = _load_engagements_file()
    engagements = data.get("engagements", [])

    engagement = next((e for e in engagements if e["id"] == engagement_id), None)
    if not engagement:
        typer.echo(f"Error: Engagement '{engagement_id}' not found.")
        raise typer.Exit(1)

    typer.echo(f"Engagement: {engagement['name']} ({engagement['id']})")
    typer.echo(f"  Client: {engagement['client_id']}")
    typer.echo(f"  Status: {engagement['status']}")
    typer.echo(f"  Current Step: {engagement['current_step']}")
    typer.echo(f"  Departments: {', '.join(engagement['departments'])}")
    typer.echo(f"  Created: {engagement['created_at']}")
    typer.echo(f"  Updated: {engagement['updated_at']}")

    if engagement["steps_completed"]:
        typer.echo(f"  Steps Completed: {', '.join(engagement['steps_completed'])}")

    if engagement["interview_results"]:
        typer.echo(f"  Interviews Completed: {len(engagement['interview_results'])}")

    if engagement["opportunities"]:
        typer.echo(f"  Opportunities Identified: {len(engagement['opportunities'])}")

    if engagement["roadmap"]:
        typer.echo("  Roadmap: Drafted")


@app.command()
def list_engagements() -> None:
    """List all consulting engagements."""
    data = _load_engagements_file()
    engagements = data.get("engagements", [])

    if not engagements:
        typer.echo("No consulting engagements found.")
        return

    typer.echo(f"{'ID':<25} {'Name':<30} {'Client':<15} {'Status':<15}")
    typer.echo("-" * 85)
    for e in engagements:
        typer.echo(f"{e['id']:<25} {e['name']:<30} {e['client_id']:<15} {e['status']:<15}")


@app.command()
def deploy_interviews(
    engagement_id: str = typer.Option(..., "--engagement", "-e", help="Engagement ID"),
    employees: str = typer.Option(
        "all", "--employees", help="Comma-separated employee emails or 'all'"
    ),
) -> None:
    """Deploy interview agents for an engagement."""
    data = _load_engagements_file()
    engagements = data.get("engagements", [])

    engagement = next((e for e in engagements if e["id"] == engagement_id), None)
    if not engagement:
        typer.echo(f"Error: Engagement '{engagement_id}' not found.")
        raise typer.Exit(1)

    if engagement["current_step"] != "onboarding":
        typer.echo(
            f"Error: Engagement must be in 'onboarding' state. Current: {engagement['current_step']}"
        )
        raise typer.Exit(1)

    employee_list = [e.strip() for e in employees.split(",")]
    engagement["status"] = "interviewing"
    engagement["current_step"] = "deploy_interviews"
    engagement["updated_at"] = datetime.now().isoformat()
    engagement["employee_list"] = employee_list

    _save_engagements_file(data)

    typer.echo(f"Interview agents deployed for engagement '{engagement_id}'.")
    typer.echo(f"  Employees to interview: {len(employee_list)}")
    typer.echo("  Interview agents: interview_agent")
    typer.echo("")
    typer.echo("Next steps:")
    typer.echo(
        f"  1. Check interview progress: ai-company consulting status --engagement {engagement_id}"
    )
    typer.echo(
        f"  2. Synthesize data:          ai-company consulting synthesize --engagement {engagement_id}"
    )


@app.command()
def synthesize(
    engagement_id: str = typer.Option(..., "--engagement", "-e", help="Engagement ID"),
) -> None:
    """Synthesize interview data into workflow maps."""
    data = _load_engagements_file()
    engagements = data.get("engagements", [])

    engagement = next((e for e in engagements if e["id"] == engagement_id), None)
    if not engagement:
        typer.echo(f"Error: Engagement '{engagement_id}' not found.")
        raise typer.Exit(1)

    if engagement["current_step"] != "deploy_interviews":
        typer.echo(
            f"Error: Engagement must be in 'deploy_interviews' state. Current: {engagement['current_step']}"
        )
        raise typer.Exit(1)

    engagement["status"] = "analyzing"
    engagement["current_step"] = "synthesize_data"
    engagement["updated_at"] = datetime.now().isoformat()

    _save_engagements_file(data)

    typer.echo(f"Interview data synthesis started for engagement '{engagement_id}'.")
    typer.echo("  Agent: workflow_mapper")
    typer.echo("")
    typer.echo("Next steps:")
    typer.echo(
        f"  1. Identify opportunities: ai-company consulting identify --engagement {engagement_id}"
    )
    typer.echo(
        f"  2. Check status:           ai-company consulting status --engagement {engagement_id}"
    )


@app.command()
def identify(
    engagement_id: str = typer.Option(..., "--engagement", "-e", help="Engagement ID"),
) -> None:
    """Identify AI transformation opportunities."""
    data = _load_engagements_file()
    engagements = data.get("engagements", [])

    engagement = next((e for e in engagements if e["id"] == engagement_id), None)
    if not engagement:
        typer.echo(f"Error: Engagement '{engagement_id}' not found.")
        raise typer.Exit(1)

    if engagement["current_step"] != "synthesize_data":
        typer.echo(
            f"Error: Engagement must be in 'synthesize_data' state. Current: {engagement['current_step']}"
        )
        raise typer.Exit(1)

    engagement["current_step"] = "identify_opportunities"
    engagement["updated_at"] = datetime.now().isoformat()

    _save_engagements_file(data)

    typer.echo(f"AI opportunity identification started for engagement '{engagement_id}'.")
    typer.echo("  Agent: opportunity_identifier")
    typer.echo("")
    typer.echo("Next steps:")
    typer.echo(f"  1. Draft roadmap: ai-company consulting draft --engagement {engagement_id}")
    typer.echo(f"  2. Check status:  ai-company consulting status --engagement {engagement_id}")


@app.command()
def draft(
    engagement_id: str = typer.Option(..., "--engagement", "-e", help="Engagement ID"),
) -> None:
    """Draft the transformation roadmap."""
    data = _load_engagements_file()
    engagements = data.get("engagements", [])

    engagement = next((e for e in engagements if e["id"] == engagement_id), None)
    if not engagement:
        typer.echo(f"Error: Engagement '{engagement_id}' not found.")
        raise typer.Exit(1)

    if engagement["current_step"] != "identify_opportunities":
        typer.echo(
            f"Error: Engagement must be in 'identify_opportunities' state. Current: {engagement['current_step']}"
        )
        raise typer.Exit(1)

    engagement["current_step"] = "draft_roadmap"
    engagement["updated_at"] = datetime.now().isoformat()

    _save_engagements_file(data)

    typer.echo(f"Transformation roadmap drafting started for engagement '{engagement_id}'.")
    typer.echo("  Agent: opportunity_identifier")
    typer.echo("")
    typer.echo("Next steps:")
    typer.echo(f"  1. Submit for review: ai-company consulting review --engagement {engagement_id}")
    typer.echo(f"  2. Check status:      ai-company consulting status --engagement {engagement_id}")


@app.command()
def review(
    engagement_id: str = typer.Option(..., "--engagement", "-e", help="Engagement ID"),
    approve: bool = typer.Option(False, "--approve", help="Approve the roadmap"),
    reject: bool = typer.Option(False, "--reject", help="Reject the roadmap"),
    feedback: str = typer.Option("", "--feedback", "-f", help="Feedback for the roadmap"),
) -> None:
    """Review and approve/reject the transformation roadmap."""
    data = _load_engagements_file()
    engagements = data.get("engagements", [])

    engagement = next((e for e in engagements if e["id"] == engagement_id), None)
    if not engagement:
        typer.echo(f"Error: Engagement '{engagement_id}' not found.")
        raise typer.Exit(1)

    if engagement["current_step"] != "draft_roadmap":
        typer.echo(
            f"Error: Engagement must be in 'draft_roadmap' state. Current: {engagement['current_step']}"
        )
        raise typer.Exit(1)

    if approve:
        engagement["status"] = "reviewed"
        engagement["current_step"] = "expert_review"
        engagement["roadmap_approved"] = True
        engagement["expert_feedback"] = feedback
        engagement["updated_at"] = datetime.now().isoformat()
        _save_engagements_file(data)

        typer.echo(f"Roadmap approved for engagement '{engagement_id}'.")
        typer.echo(f"  Expert feedback: {feedback if feedback else 'None'}")
        typer.echo("")
        typer.echo("Next steps:")
        typer.echo(
            f"  1. Present to client: ai-company consulting present --engagement {engagement_id}"
        )

    elif reject:
        engagement["current_step"] = "draft_roadmap"
        engagement["roadmap_approved"] = False
        engagement["expert_feedback"] = feedback
        engagement["updated_at"] = datetime.now().isoformat()
        _save_engagements_file(data)

        typer.echo(f"Roadmap rejected for engagement '{engagement_id}'.")
        typer.echo(f"  Feedback: {feedback if feedback else 'No feedback provided'}")
        typer.echo("")
        typer.echo("Roadmap will be revised based on feedback.")

    else:
        typer.echo("Error: Must specify --approve or --reject.")
        raise typer.Exit(1)


@app.command()
def present(
    engagement_id: str = typer.Option(..., "--engagement", "-e", help="Engagement ID"),
    feedback: str = typer.Option("", "--feedback", "-f", help="Client feedback"),
) -> None:
    """Present the roadmap to the client and capture feedback."""
    data = _load_engagements_file()
    engagements = data.get("engagements", [])

    engagement = next((e for e in engagements if e["id"] == engagement_id), None)
    if not engagement:
        typer.echo(f"Error: Engagement '{engagement_id}' not found.")
        raise typer.Exit(1)

    if engagement["current_step"] != "expert_review":
        typer.echo(
            f"Error: Engagement must be in 'expert_review' state. Current: {engagement['current_step']}"
        )
        raise typer.Exit(1)

    engagement["status"] = "completed"
    engagement["current_step"] = "client_presentation"
    engagement["client_feedback"] = feedback
    engagement["completed_at"] = datetime.now().isoformat()
    engagement["updated_at"] = datetime.now().isoformat()
    _save_engagements_file(data)

    typer.echo(f"Roadmap presented to client for engagement '{engagement_id}'.")
    typer.echo(f"  Client feedback: {feedback if feedback else 'Pending'}")
    typer.echo("")
    typer.echo("Next steps:")
    typer.echo(
        f"  1. Feed learnings: ai-company consulting feed-knowledge --engagement {engagement_id}"
    )


@app.command()
def feed_knowledge(
    engagement_id: str = typer.Option(..., "--engagement", "-e", help="Engagement ID"),
) -> None:
    """Feed engagement learnings back into the knowledge flywheel."""
    data = _load_engagements_file()
    engagements = data.get("engagements", [])

    engagement = next((e for e in engagements if e["id"] == engagement_id), None)
    if not engagement:
        typer.echo(f"Error: Engagement '{engagement_id}' not found.")
        raise typer.Exit(1)

    if engagement["status"] != "completed":
        typer.echo(f"Error: Engagement must be completed. Current: {engagement['status']}")
        raise typer.Exit(1)

    # Store learnings in the memory engine (flywheel)
    _store_engagement_learning(
        memory_type="episodic",
        content=f"Completed consulting engagement '{engagement['name']}' for client '{engagement['client_id']}'. "
        f"Scope: {engagement['scope']}. Departments: {', '.join(engagement['departments'])}. "
        f"Client feedback: {engagement.get('client_feedback', 'None')}",
        engagement_id=engagement_id,
        agent_id="consulting_lead",
        tags=["engagement_complete", engagement["client_id"]],
    )

    _store_engagement_learning(
        memory_type="semantic",
        content=f"Client '{engagement['client_id']}' engaged for {engagement['scope']} transformation. "
        f"Key departments: {', '.join(engagement['departments'])}. "
        f"Interview count: {len(engagement.get('interview_results', []))}. "
        f"Opportunities found: {len(engagement.get('opportunities', []))}",
        engagement_id=engagement_id,
        agent_id="consulting_lead",
        tags=["client_profile", engagement["client_id"]],
    )

    if engagement.get("expert_feedback"):
        _store_engagement_learning(
            memory_type="semantic",
            content=f"Expert feedback on roadmap for engagement '{engagement_id}': "
            f"{engagement['expert_feedback']}",
            engagement_id=engagement_id,
            agent_id="consulting_lead",
            tags=["expert_feedback", "roadmap_review"],
        )

    _store_engagement_learning(
        memory_type="procedural",
        content=f"Consulting engagement workflow for {engagement['scope']}: "
        f"onboarding -> interviews -> synthesis -> opportunity identification -> "
        f"roadmap drafting -> expert review -> client presentation",
        engagement_id=engagement_id,
        agent_id="consulting_lead",
        tags=["workflow_pattern", engagement["scope"]],
    )

    engagement["knowledge_fed"] = True
    engagement["knowledge_fed_at"] = datetime.now().isoformat()
    engagement["updated_at"] = datetime.now().isoformat()
    _save_engagements_file(data)

    typer.echo(f"Learnings fed to knowledge base for engagement '{engagement_id}'.")
    typer.echo("  The knowledge flywheel has been updated with:")
    typer.echo("    - Episodic memory: Engagement experience and outcomes")
    typer.echo("    - Semantic memory: Client profile and scope details")
    typer.echo("    - Feedback memory: Expert review corrections")
    typer.echo("    - Procedural memory: Workflow patterns for this scope")
    typer.echo("")
    typer.echo("These learnings will improve future engagements via memory recall.")
