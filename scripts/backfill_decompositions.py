"""Backfill decomposition subtasks into the inbox as executable tasks.

Reads all .json files from .opencode/decompositions/ and creates
inbox tasks for any subtasks with status="pending".
"""

from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from ai_company.data import TaskStore, init_database  # noqa: E402
from ai_company.models.task import Task, TaskPriority  # noqa: E402
from ai_company.orchestrator.message_bus import MessageBus  # noqa: E402
from ai_company.paths import get_database_path  # noqa: E402


def backfill_decompositions() -> int:
    """Read decomposition files and inject pending subtasks into inbox.

    Returns the number of tasks created.
    """
    decompositions_dir = project_root / ".opencode" / "decompositions"
    if not decompositions_dir.exists():
        print(f"No decompositions directory found at {decompositions_dir}")
        return 0

    database = init_database(str(get_database_path()))
    bus = MessageBus(database=database)

    # Get existing task IDs to avoid duplicates
    existing_tasks = bus.get_pending_tasks()
    existing_ids = {t.id for t in existing_tasks}

    tasks_created = 0

    for decomp_file in decompositions_dir.glob("*.json"):
        if decomp_file.suffix == ".bak":
            continue

        print(f"Processing {decomp_file.name}...")

        try:
            with open(decomp_file, "r", encoding="utf-8") as f:
                decomposition = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"  Error reading {decomp_file.name}: {e}")
            continue

        parent_id = decomposition.get("parent_id", "")
        subtasks = decomposition.get("subtasks", [])

        for subtask in subtasks:
            subtask_id = subtask.get("id", "")
            instruction = subtask.get("instruction", "")
            status = subtask.get("status", "pending")

            if status != "pending":
                print(f"  Skipping subtask {subtask_id[:8]} (status={status})")
                continue

            if subtask_id in existing_ids:
                print(f"  Skipping subtask {subtask_id[:8]} (already in inbox)")
                continue

            # Create task from subtask
            task = Task(
                id=subtask_id or str(uuid.uuid4()),
                sender_id="task-decomposer",
                receiver_id="chief_of_staff",
                instruction=instruction,
                priority=TaskPriority.MEDIUM,
                parent_task_id=parent_id,
            )

            # Guard: never backfill demo/test subtasks (proj-acme-chatbot,
            # 'Test ' instruction prefix, test-/verify- ids) into real data.
            if TaskStore.is_test_task(task.model_dump()):
                print(f"  Skipping demo/test subtask {task.id[:8]}")
                continue

            bus.send_task(task)
            existing_ids.add(task.id)
            tasks_created += 1
            print(f"  Created task {task.id[:8]}: {instruction[:60]}...")

    return tasks_created


def main() -> None:
    """Main entry point."""
    print("Backfilling decomposition subtasks into inbox...")
    print()

    tasks_created = backfill_decompositions()

    print()
    print(f"Done. Created {tasks_created} tasks.")
    if tasks_created > 0:
        print("Tasks are now in the inbox waiting for the executor to process them.")
        print("Start the executor with: ai-company executor start")


if __name__ == "__main__":
    main()
