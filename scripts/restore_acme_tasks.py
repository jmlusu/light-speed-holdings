"""Restore Acme Corp demo tasks to the database.

DEMO-ONLY utility: re-seeds the Acme Corp ``proj-acme-chatbot`` demo
dataset that ``ai-company dashboard cleanup`` is designed to remove. Use
it to validate cleanup behaviour (per-class counts, ``include_test`` API
filters) against a known baseline in a NON-PRODUCTION database. Every
task it creates carries the ``proj-acme-chatbot`` demo marker so cleanup
removes the entire dataset — no partial survivors.
"""

import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_company.data import TaskStore, init_database
from ai_company.models.task import Task, TaskPriority
from ai_company.paths import get_database_path


def restore_acme_tasks():
    """Create the 5 Acme Corp chatbot project tasks."""
    db = init_database(str(get_database_path()))
    store = TaskStore(db)

    now = datetime.now(timezone.utc).isoformat()

    tasks = [
        Task(
            id=str(uuid.uuid4()),
            sender_id="sales",
            receiver_id="chief-of-staff",
            instruction="[proj-acme-chatbot-001] New client lead: Acme Corp (Malawi). Wants a WhatsApp chatbot for customer support. Budget: MWK 1,500,000 setup + MWK 100,000/mo. Contact: +265 991 234 567. Urgency: normal.",
            status="pending",
            priority=TaskPriority.HIGH,
            created_at=now,
        ),
        Task(
            id=str(uuid.uuid4()),
            sender_id="chief-of-staff",
            receiver_id="conversation_designer",
            instruction="[proj-acme-chatbot-001] Design WhatsApp chatbot conversation flows for Acme Corp customer support",
            status="completed",
            priority=TaskPriority.HIGH,
            created_at=now,
        ),
        Task(
            id=str(uuid.uuid4()),
            sender_id="chief-of-staff",
            receiver_id="integration_engineer",
            instruction="[proj-acme-chatbot-001] Set up WhatsApp Business API integration for Acme Corp",
            status="completed",
            priority=TaskPriority.HIGH,
            created_at=now,
        ),
        Task(
            id=str(uuid.uuid4()),
            sender_id="chief-of-staff",
            receiver_id="backend_engineer",
            instruction="[proj-acme-chatbot-001] Build backend for Acme Corp WhatsApp chatbot",
            status="completed",
            priority=TaskPriority.HIGH,
            created_at=now,
        ),
        Task(
            id=str(uuid.uuid4()),
            sender_id="chief-of-staff",
            receiver_id="human-ceo",
            instruction="[proj-acme-chatbot-001] QA review for Acme Corp chatbot project",
            status="completed",
            priority=TaskPriority.HIGH,
            created_at=now,
        ),
    ]

    for task in tasks:
        if not TaskStore.is_test_task(task.model_dump()):
            raise RuntimeError(
                f"Acme demo task {task.id} does not match the demo marker — "
                "cleanup would leave it behind. Refusing to seed."
            )
        store.send_task(task)
        print(f"Created: {task.receiver_id} - {task.instruction[:60]}...")

    print(f"\nRestored {len(tasks)} Acme Corp demo tasks.")
    print(f"Total tasks in database: {store.count()}")
    print("WARNING: this is DEMO data. Run `ai-company dashboard cleanup` to remove it.")


if __name__ == "__main__":
    restore_acme_tasks()
