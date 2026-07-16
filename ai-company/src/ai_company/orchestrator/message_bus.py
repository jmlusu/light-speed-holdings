import json
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
