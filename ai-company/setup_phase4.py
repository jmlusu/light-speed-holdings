import os

print("🚀 Phase 4: Building the Agent Orchestration & Communication Layer...")

os.makedirs('src/ai_company/orchestrator', exist_ok=True)

# 1. Create the Task Model (Pydantic)
with open('src/ai_company/models/task.py', 'w', encoding='utf-8') as f:
    f.write("""from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal, Optional
import uuid

class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str
    receiver_id: str
    instruction: str
    status: Literal["pending", "in_progress", "completed", "failed"] = "pending"
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    result: Optional[str] = None
""")
print("✅ Created src/ai_company/models/task.py")

with open('src/ai_company/orchestrator/__init__.py', 'w', encoding='utf-8') as f:
    f.write("")

# 2. Create the Message Bus
with open('src/ai_company/orchestrator/message_bus.py', 'w', encoding='utf-8') as f:
    f.write("""import json
from pathlib import Path
from typing import List
from ai_company.models.task import Task

class MessageBus:
    def __init__(self, storage_path=".opencode/inbox.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self.storage_path.write_text('[]', encoding='utf-8')

    def _load_tasks(self) -> List[dict]:
        return json.loads(self.storage_path.read_text(encoding='utf-8'))

    def _save_tasks(self, tasks: List[dict]):
        self.storage_path.write_text(json.dumps(tasks, indent=2), encoding='utf-8')

    def send_task(self, task: Task):
        tasks = self._load_tasks()
        tasks.append(task.model_dump())
        self._save_tasks(tasks)
        print(f"📨 Task {task.id} sent from [{task.sender_id}] to [{task.receiver_id}].")

    def get_inbox(self, agent_id: str) -> List[Task]:
        tasks = self._load_tasks()
        return [Task(**t) for t in tasks if t['receiver_id'] == agent_id]

    def get_sent(self, agent_id: str) -> List[Task]:
        tasks = self._load_tasks()
        return [Task(**t) for t in tasks if t['sender_id'] == agent_id]
""")
print("✅ Created src/ai_company/orchestrator/message_bus.py")

# 3. Update CLI to include Orchestration Commands
with open('src/ai_company/cli.py', 'w', encoding='utf-8') as f:
    f.write("""import click
from ai_company.generator import AgentGenerator
from ai_company.validator import CompanyValidator
from ai_company.orchestrator.message_bus import MessageBus
from ai_company.models.task import Task

@click.group()
def cli():
    \"\"\"Light Speed Holdings AI Company Builder CLI.\"\"\"
    pass

@cli.command()
def generate():
    \"\"\"Generate all OpenCode agent files from the registry.\"\"\"
    generator = AgentGenerator()
    generator.generate_all()

@cli.command()
def validate():
    \"\"\"Validate the company registry for structural integrity.\"\"\"
    validator = CompanyValidator()
    success = validator.validate()
    if not success:
        raise SystemExit(1)

@cli.command()
@click.option('--sender', required=True, help='ID of the agent sending the task')
@click.option('--receiver', required=True, help='ID of the agent receiving the task')
@click.option('--instruction', required=True, help='The task instructions')
def delegate(sender, receiver, instruction):
    \"\"\"Delegate a task from one agent to another.\"\"\"
    bus = MessageBus()
    task = Task(sender_id=sender, receiver_id=receiver, instruction=instruction)
    bus.send_task(task)

@cli.command()
@click.option('--agent', required=True, help='ID of the agent')
def inbox(agent):
    \"\"\"View the inbox for a specific agent.\"\"\"
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

if __name__ == '__main__':
    cli()
""")
print("✅ Updated src/ai_company/cli.py with orchestration commands")

print("\n🎯 Phase 4 setup complete!")
