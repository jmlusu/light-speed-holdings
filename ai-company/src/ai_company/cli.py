import click
from ai_company.generator import AgentGenerator
from ai_company.validator import CompanyValidator
from ai_company.orchestrator.message_bus import MessageBus
from ai_company.orchestrator.briefing import BriefingGenerator
from ai_company.models.task import Task

@click.group()
def cli():
    """Light Speed Holdings AI Company Builder CLI."""
    pass

@cli.command()
def generate():
    """Generate all OpenCode agent files from the registry."""
    generator = AgentGenerator()
    generator.generate_all()

@cli.command()
def validate():
    """Validate the company registry for structural integrity."""
    validator = CompanyValidator()
    success = validator.validate()
    if not success:
        raise SystemExit(1)

@cli.command()
@click.option('--sender', required=True, help='ID of the agent sending the task')
@click.option('--receiver', required=True, help='ID of the agent receiving the task')
@click.option('--instruction', required=True, help='The task instructions')
def delegate(sender, receiver, instruction):
    """Delegate a task from one agent to another."""
    bus = MessageBus()
    task = Task(sender_id=sender, receiver_id=receiver, instruction=instruction)
    bus.send_task(task)

@cli.command()
@click.option('--agent', required=True, help='ID of the agent')
def inbox(agent):
    """View the inbox for a specific agent."""
    bus = MessageBus()
    tasks = bus.get_inbox(agent)
    if not tasks:
        print(f"📭 Inbox for {agent} is empty.")
        return
    
    print("")
    print(f"📥 Inbox for [{agent}] ({len(tasks)} task(s)):")
    print("-" * 60)
    for t in tasks:
        print(f"ID: {t.id}")
        print(f"From: {t.sender_id} | Status: {t.status.upper()}")
        print(f"Instruction: {t.instruction}")
        print("-" * 60)

@cli.command()
def briefing():
    """Generate the daily executive briefing for OpenCode."""
    bg = BriefingGenerator()
    active, total = bg.generate()
    print(f"📈 Company Status: {active} active agents, {total} total pending tasks.")

@cli.command()
def status():
    """Show a quick overview of the company message bus."""
    bus = MessageBus()
    tasks = bus._load_tasks()
    
    pending = len([t for t in tasks if t['status'] == 'pending'])
    completed = len([t for t in tasks if t['status'] == 'completed'])
    
    print("\n🏢 Light Speed Holdings - System Status")
    print("=" * 40)
    print(f"📨 Total Messages: {len(tasks)}")
    print(f"⏳ Pending Tasks:  {pending}")
    print(f"✅ Completed:      {completed}")
    print("=" * 40)

if __name__ == '__main__':
    cli()
