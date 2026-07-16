import click
from ai_company.generator import AgentGenerator
from ai_company.validator import CompanyValidator
from ai_company.orchestrator.message_bus import MessageBus
from ai_company.orchestrator.briefing import BriefingGenerator
from ai_company.models.task import Task

@click.group()
def cli():
    pass

@cli.command()
def generate():
    generator = AgentGenerator()
    generator.generate_all()

@cli.command()
def validate():
    validator = CompanyValidator()
    success = validator.validate()
    if not success:
        raise SystemExit(1)

@cli.command()
@click.option('--sender', required=True)
@click.option('--receiver', required=True)
@click.option('--instruction', required=True)
def delegate(sender, receiver, instruction):
    bus = MessageBus()
    task = Task(sender_id=sender, receiver_id=receiver, instruction=instruction)
    bus.send_task(task)

@cli.command()
@click.option('--agent', required=True)
def inbox(agent):
    bus = MessageBus()
    tasks = bus.get_inbox(agent)
    if not tasks:
        print(f"Inbox for {agent} is empty.")
        return
    print(f"
Inbox for [{agent}] ({len(tasks)} task(s)):")
    print("-" * 60)
    for t in tasks:
        print(f"ID: {t.id}")
        print(f"From: {t.sender_id} | Status: {t.status.upper()}")
        print(f"Instruction: {t.instruction}")
        print("-" * 60)

@cli.command()
@click.option('--task-id', required=True)
@click.option('--result', required=True)
def complete(task_id, result):
    bus = MessageBus()
    tasks = bus._load_tasks()
    found = False
    for t in tasks:
        if t['id'] == task_id:
            t['status'] = 'completed'
            t['result'] = result
            found = True
            break
    if found:
        bus._save_tasks(tasks)
        print(f"Task {task_id} marked as COMPLETED.")
    else:
        print(f"Task {task_id} not found.")

@cli.command()
def briefing():
    bg = BriefingGenerator()
    active, total = bg.generate()
    print(f"Company Status: {active} active agents, {total} total pending tasks.")

@cli.command()
def status():
    bus = MessageBus()
    tasks = bus._load_tasks()
    pending = len([t for t in tasks if t['status'] == 'pending'])
    completed = len([t for t in tasks if t['status'] == 'completed'])
    print("
Light Speed Holdings - System Status")
    print("=" * 40)
    print(f"Total Messages: {len(tasks)}")
    print(f"Pending Tasks:  {pending}")
    print(f"Completed:      {completed}")
    print("=" * 40)

if __name__ == '__main__':
    cli()
