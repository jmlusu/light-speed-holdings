import os

print("Phase 6: Building the Bridge...")

generator_code = '''import yaml
from jinja2 import Environment, DictLoader
from pathlib import Path

AGENT_TEMPLATE_STR = """---
name: {{ name }}
description: {{ description }}
tools: {{ tools | default([]) | tojson }}
---

# {{ title }}

You are the {{ title }} at Light Speed Holdings.

## Core Responsibilities
{% for responsibility in responsibilities | default([]) %}
- {{ responsibility }}
{% endfor %}

## Reporting Structure
- **Reports To**: {{ reports_to | default('CEO') }}
- **Direct Reports**: {{ direct_reports | default([]) | join(', ') if direct_reports else 'None' }}

## Behavioral Guidelines
{{ guidelines | default('Maintain professional standards and execute tasks efficiently.') }}

## Standard Operating Procedures (SOP)

### Checking Your Inbox
Before taking action, always check your inbox for pending tasks:

    python -m ai_company.cli inbox --agent {{ id }}

### Delegating a Task
If a task requires subordinates, delegate it immediately:

    python -m ai_company.cli delegate --sender {{ id }} --receiver "[SUBORDINATE_ID]" --instruction "[YOUR_INSTRUCTION]"

### Completing a Task
When you finish a task, record your findings and mark it complete:

    python -m ai_company.cli complete --task-id "[TASK_ID]" --result "[YOUR_RESULT_SUMMARY]"

"""

class AgentGenerator:
    def __init__(self, registry_path="company-registry.yaml", output_dir=".opencode/agents"):
        self.registry_path = Path(registry_path)
        self.output_dir = Path(output_dir)
        self.env = Environment(loader=DictLoader({"agent.md": AGENT_TEMPLATE_STR}))
        self.template = self.env.get_template("agent.md")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_registry(self):
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry not found at: {self.registry_path.absolute()}")
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def generate_all(self):
        data = self.load_registry()
        agents = data.get('company', {}).get('agents', [])
        print(f"Generating {len(agents)} agents for {data['company']['name']}...")
        for agent in agents:
            self._generate_agent(agent)
        print("Generation complete! Agents now include SOP instructions.")

    def _generate_agent(self, agent_data):
        rendered = self.template.render(**agent_data)
        output_file = self.output_dir / f"{agent_data['id']}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rendered)
        print(f"  Generated: {output_file}")
'''

with open('src/ai_company/generator.py', 'w', encoding='utf-8') as f:
    f.write(generator_code)
print("Updated src/ai_company/generator.py")

cli_code = '''import click
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
    print(f"\nInbox for [{agent}] ({len(tasks)} task(s)):")
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
    print("\nLight Speed Holdings - System Status")
    print("=" * 40)
    print(f"Total Messages: {len(tasks)}")
    print(f"Pending Tasks:  {pending}")
    print(f"Completed:      {completed}")
    print("=" * 40)

if __name__ == '__main__':
    cli()
'''

with open('src/ai_company/cli.py', 'w', encoding='utf-8') as f:
    f.write(cli_code)
print("Updated src/ai_company/cli.py")

print("Phase 6 setup complete!")
