"""Generates a daily briefing from the agent registry and message bus."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

from ai_company.orchestrator.message_bus import MessageBus

logger = logging.getLogger(__name__)


class BriefingGenerator:
    """Produces a daily executive briefing markdown file."""

    def __init__(
        self,
        registry_path: str = "company/agent-registry.json",
        inbox_path: str = ".opencode/inbox.json",
        output_path: str = ".opencode/daily_briefing.md",
    ) -> None:
        self.registry_path = Path(registry_path)
        self.bus = MessageBus(storage_path=inbox_path)
        self.output_path = Path(output_path)

    def _load_registry(self) -> dict[str, dict]:
        if not self.registry_path.exists():
            return {}
        with open(self.registry_path, "r", encoding="utf-8") as f:
            agents = json.load(f)
        return {a["name"]: a for a in agents}

    def generate(self) -> tuple[int, int]:
        """Generate briefing. Returns (active_agents, pending_task_count)."""
        agents = self._load_registry()
        pending_tasks: dict[str, list[dict]] = {}

        for task_dict in self.bus._load_tasks():
            if task_dict.get("status") == "pending":
                receiver = task_dict["receiver_id"]
                pending_tasks.setdefault(receiver, []).append(task_dict)

        today = datetime.now().strftime("%Y-%m-%d")
        lines = [
            "# Daily Executive Briefing",
            f"**Date:** {today}\n",
        ]

        active_agents = 0
        for agent_id, tasks in pending_tasks.items():
            if agent_id not in agents:
                continue
            agent = agents[agent_id]
            active_agents += 1
            dept = agent.get("department", "N/A")
            reports_to = agent.get("reportsTo", "N/A")
            lines.append(f"## Action Required: {agent['role']} (`{agent_id}`)")
            lines.append(f"**Department:** {dept} | **Reports To:** {reports_to}\n")
            lines.append("**OpenCode Execution Prompt:**\n```text")
            lines.append(
                f"You are the {agent['role']}. You have {len(tasks)} pending task(s) in your inbox.\n"
            )
            for task in tasks:
                sender_name = agents.get(task["sender_id"], {}).get("role", task["sender_id"])
                lines.append(f"TASK ID: {task['id']}")
                lines.append(f"FROM: {sender_name}")
                lines.append(f"INSTRUCTION: {task['instruction']}\n")
            lines.append("Please execute these tasks using your available tools.")
            lines.append("```\n---\n")

        if active_agents == 0:
            lines.append(
                "**No pending tasks.** The company is idle or waiting for executive directives."
            )

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text("\n".join(lines), encoding="utf-8")
        logger.info("Briefing generated at: %s", self.output_path)

        return active_agents, sum(len(t) for t in pending_tasks.values())
