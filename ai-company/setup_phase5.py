import os

print("🚀 Phase 5: Building the Automated Orchestration & Briefing Engine...")

# 1. Create the Briefing Generator
with open('src/ai_company/orchestrator/briefing.py', 'w', encoding='utf-8') as f:
    f.write('''import yaml
from pathlib import Path
from datetime import datetime
from ai_company.orchestrator.message_bus import MessageBus

class BriefingGenerator:
    def __init__(self, registry_path="company-registry.yaml"):
        self.registry_path = Path(registry_path)
        self.bus = MessageBus()

    def generate(self):
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        agents = {a['id']: a for a in data['company']['agents']}
        pending_tasks = {}
        
        # Gather all pending tasks
        for task_dict in self.bus._load_tasks():
            if task_dict['status'] == 'pending':
                receiver = task_dict['receiver_id']
                if receiver not in pending_tasks:
                    pending_tasks[receiver] = []
                pending_tasks[receiver].append(task_dict)
                
        print("📊 Generating Daily Executive Briefing...")
        
        today = datetime.now().strftime('%Y-%m-%d')
        briefing_md = f"# 🌅 Daily Executive Briefing for {data['company']['name']}\\n"
        briefing_md += f"**Date:** {today}\\n\\n"
        
        active_agents = 0
        for aid, tasks in pending_tasks.items():
            if aid in agents:
                agent = agents[aid]
                active_agents += 1
                briefing_md += f"## 🎯 Action Required: {agent['name']} ({agent['title']})\\n"
                briefing_md += f"**Department:** {agent['department']} | **Reports To:** {agent['reports_to']}\\n\\n"
                briefing_md += "**OpenCode Execution Prompt:**\\n```text\\n"
                briefing_md += f"You are the {agent['title']}. You have {len(tasks)} pending task(s) in your inbox.\\n\\n"
                for task in tasks:
                    sender_name = agents.get(task['sender_id'], {}).get('name', task['sender_id'])
                    briefing_md += f"TASK ID: {task['id']}\\n"
                    briefing_md += f"FROM: {sender_name}\\n"
                    briefing_md += f"INSTRUCTION: {task['instruction']}\\n\\n"
                briefing_md += "Please execute these tasks using your available tools.\\n```\\n\\n---\\n\\n"
                
        if active_agents == 0:
            briefing_md += "✅ **No pending tasks.** The company is idle or waiting for executive directives.\\n"
            
        output_path = Path(".opencode/daily_briefing.md")
        output_path.write_text(briefing_md, encoding='utf-8')
        print(f"✅ Briefing generated at: {output_path}")
        
        return active_agents, len(pending_tasks)
''')
print("✅ Created src/ai_company/orchestrator/briefing.py")

# 2. Update CLI to include Briefing and Status Commands
with open('src/ai_company/cli.py', 'w', encoding='utf-8') as f:
    f.write('''import click
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
    
    print("\\n🏢 Light Speed Holdings - System Status")
    print("=" * 40)
    print(f"📨 Total Messages: {len(tasks)}")
    print(f"⏳ Pending Tasks:  {pending}")
    print(f"✅ Completed:      {completed}")
    print("=" * 40)

if __name__ == '__main__':
    cli()
''')
print("✅ Updated src/ai_company/cli.py with briefing and status commands")

print("\\n🎯 Phase 5 setup complete!")
