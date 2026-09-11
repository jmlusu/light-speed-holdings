"""Learning event collector — captures task outcomes for continuous improvement.

Listens for task lifecycle events from the MessageBus broadcast callback
and extracts structured learning data from completed/failed tasks.  This
module is the "experience collector" that feeds the memory engine with
post-task knowledge for semantic and procedural extraction.

Usage::

    from ai_company.memory.learning_collector import LearningCollector
    from ai_company.orchestrator.message_bus import MessageBus

    collector = LearningCollector(results_dir="results", memory_dir="memory")
    bus = MessageBus(broadcast_callback=collector.on_task_event)
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from ai_company.memory.integration import (
    get_store,
    init_memory,
    record_knowledge,
    record_procedure,
    record_task_outcome,
)

logger = logging.getLogger(__name__)

# Events that trigger learning capture
_LEARNING_EVENTS = frozenset({"completed", "failed", "timed_out", "escalated"})


class LearningCollector:
    """Captures task outcomes and extracts learning data from the MessageBus.

    When a task reaches a terminal state (completed, failed, timed_out,
    escalated), the collector:
    1. Records an episodic memory of the outcome
    2. Reads the loop result artifacts for tool traces
    3. Extracts semantic knowledge (what was learned)
    4. Extracts procedural knowledge (how to do it again)
    5. Stores everything in the memory engine for future recall

    Args:
        results_dir: Directory containing loop result artifacts
            (default: ``results``).
        memory_dir: Directory for memory store (default: ``memory``).
    """

    def __init__(
        self,
        results_dir: str | Path = "results",
        memory_dir: str | Path = "memory",
    ) -> None:
        self.results_dir = Path(results_dir)
        # Ensure memory store is initialized
        self._store = get_store() or init_memory(str(memory_dir))

    def on_task_event(self, task_dict: dict[str, Any], event: str) -> None:
        """Handle a task lifecycle event from the MessageBus.

        Only processes terminal events (completed, failed, timed_out, escalated).
        Extracts learning data from the task's loop result artifacts.

        Args:
            task_dict: The task data as a dictionary.
            event: The event type string.
        """
        if event not in _LEARNING_EVENTS:
            return

        task_id = task_dict.get("id", "")
        receiver_id = task_dict.get("receiver_id", "")
        instruction = task_dict.get("instruction", "")
        status = task_dict.get("status", event)
        result_text = task_dict.get("result", "")

        if not task_id or not instruction:
            return

        # 1. Record episodic memory of the outcome
        self._record_outcome(
            task_id=task_id,
            agent_id=receiver_id,
            instruction=instruction,
            status=status,
            result_summary=result_text,
        )

        # 2. Read loop result artifacts for deeper analysis
        artifacts = self._load_loop_artifacts(task_id)

        # 3. Extract semantic knowledge from successful completions
        if status == "completed" and artifacts:
            self._extract_semantic_knowledge(
                task_id=task_id,
                agent_id=receiver_id,
                instruction=instruction,
                artifacts=artifacts,
            )

        # 4. Extract procedural knowledge from tool usage patterns
        if artifacts and artifacts.get("tool_results"):
            self._extract_procedural_knowledge(
                task_id=task_id,
                agent_id=receiver_id,
                instruction=instruction,
                artifacts=artifacts,
            )

    def _record_outcome(
        self,
        task_id: str,
        agent_id: str,
        instruction: str,
        status: str,
        result_summary: str,
    ) -> None:
        """Record an episodic memory of the task outcome."""
        try:
            record_task_outcome(
                task_id=task_id,
                agent_id=agent_id,
                instruction=instruction,
                status=status,
                result_summary=result_summary,
            )
            logger.debug("Recorded episodic memory for task %s", task_id)
        except Exception:  # noqa: BLE001 - memory recording must not break execution
            logger.debug("Failed to record episodic memory for task %s", task_id, exc_info=True)

    def _load_loop_artifacts(self, task_id: str) -> dict[str, Any] | None:
        """Load loop result artifacts for a completed task.

        Looks for ``results/{task_id}/loop_result.json`` which contains
        the full tool trace, token usage, and cost data.
        """
        result_file = self.results_dir / task_id / "loop_result.json"
        if not result_file.exists():
            return None
        try:
            with open(result_file, encoding="utf-8") as f:
                data: dict[str, Any] = json.load(f)
            return data if isinstance(data, dict) else None
        except (json.JSONDecodeError, OSError):
            return None

    def _extract_semantic_knowledge(
        self,
        task_id: str,
        agent_id: str,
        instruction: str,
        artifacts: dict[str, Any],
    ) -> None:
        """Extract semantic knowledge from a successful task completion.

        Creates a semantic memory entry summarizing what was accomplished,
        which tools were used, and any patterns observed.
        """
        tool_results = artifacts.get("tool_results", [])
        tools_used = [r.get("tool", "") for r in tool_results if r.get("status") == "success"]
        iterations = artifacts.get("iterations", 0)
        total_cost = artifacts.get("total_cost_usd", 0)

        if not tools_used:
            return

        # Build a concise knowledge summary
        tool_list = ", ".join(dict.fromkeys(tools_used))  # dedupe, preserve order
        content = (
            f"Task completed: {instruction[:200]}\n"
            f"Tools used: {tool_list}\n"
            f"Iterations: {iterations}, Cost: ${total_cost:.4f}"
        )

        tags = ["task-completed", agent_id] + list(dict.fromkeys(tools_used))[:5]

        try:
            record_knowledge(
                agent_id=agent_id,
                topic=f"task-pattern-{task_id}",
                content=content,
                tags=tags,
            )
            logger.debug("Extracted semantic knowledge from task %s", task_id)
        except Exception:  # noqa: BLE001
            logger.debug(
                "Failed to extract semantic knowledge from task %s", task_id, exc_info=True
            )

    def _extract_procedural_knowledge(
        self,
        task_id: str,
        agent_id: str,
        instruction: str,
        artifacts: dict[str, Any],
    ) -> None:
        """Extract procedural knowledge from tool usage patterns.

        Identifies error-recovery patterns and successful tool sequences
        to build procedural memory for future reference.
        """
        tool_results = artifacts.get("tool_results", [])
        if len(tool_results) < 2:
            return

        # Detect error-recovery patterns: a failed tool call followed by
        # a successful one with a different approach
        error_recovery = []
        for i in range(1, len(tool_results)):
            prev = tool_results[i - 1]
            curr = tool_results[i]
            if prev.get("status") == "error" and curr.get("status") == "success":
                error_pattern = prev.get("result", "")[:100]
                recovery_action = curr.get("tool", "")
                if error_pattern and recovery_action:
                    error_recovery.append(
                        f"Error '{error_pattern}' recovered by '{recovery_action}'"
                    )

        if not error_recovery:
            return

        content = (
            f"Procedural knowledge for: {instruction[:150]}\n"
            f"Error recovery patterns:\n" + "\n".join(f"- {p}" for p in error_recovery[:5])
        )

        try:
            record_procedure(
                agent_id=agent_id,
                procedure=f"error-recovery-{task_id}",
                context=content,
                tags=["procedure", "error-recovery", agent_id],
            )
            logger.debug("Extracted procedural knowledge from task %s", task_id)
        except Exception:  # noqa: BLE001
            logger.debug(
                "Failed to extract procedural knowledge from task %s", task_id, exc_info=True
            )
