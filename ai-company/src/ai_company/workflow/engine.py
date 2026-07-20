"""Workflow engine -- executes and manages company workflows.

Persists workflow instances to disk via FileStore so they survive
restarts.  Each instance is stored as JSON under
``workflows/instances/{instance_id}.json``.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from ai_company.models import (
    CompanyRegistry,
    Task,
    TaskPriority,
    TaskStatus,
    Workflow,
    WorkflowStep,
)
from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """Manages workflow execution, step tracking, and SLA monitoring.

    Instance state is persisted to disk via FileStore, so running
    workflows survive process restarts.

    Args:
        registry: The loaded CompanyRegistry.
        state_dir: Directory for persisting workflow instance state.
    """

    def __init__(
        self,
        registry: CompanyRegistry,
        state_dir: str | Path = "workflows/instances",
    ) -> None:
        self.registry = registry
        self._workflows: dict[str, Workflow] = {w.id: w for w in registry.workflows}
        self._instances: dict[str, WorkflowInstance] = {}
        self._store = FileStore(Path(state_dir), backup=True)
        self._load_instances()

    # ── Persistence ───────────────────────────────────────────────────

    def _instance_filename(self, instance_id: str) -> str:
        return f"{instance_id}.json"

    def _load_instances(self) -> None:
        """Load all persisted workflow instances from disk."""
        files = self._store.list_files(pattern="*.json")
        for f in files:
            data = self._store.read_json(f.name)
            if data is None:
                continue
            try:
                wf_id = data.get("workflow_id", "")
                workflow = self._workflows.get(wf_id)
                if workflow is None:
                    logger.warning(
                        "Skipping instance %s: workflow '%s' not found.",
                        data.get("instance_id", "?"), wf_id,
                    )
                    continue
                instance = WorkflowInstance.from_dict(data, workflow)
                self._instances[instance.instance_id] = instance
            except Exception as exc:
                logger.warning("Failed to load instance from %s: %s", f, exc)

    def _save_instance(self, instance: WorkflowInstance) -> None:
        """Persist a single workflow instance to disk."""
        filename = self._instance_filename(instance.instance_id)
        self._store.write_json(filename, instance.to_dict())

    def _delete_instance(self, instance: WorkflowInstance) -> None:
        """Remove a workflow instance from disk."""
        filename = self._instance_filename(instance.instance_id)
        self._store.delete(filename)

    # ── Public API ────────────────────────────────────────────────────

    def list_workflows(self) -> list[dict[str, Any]]:
        """List all available workflows."""
        return [
            {
                "id": w.id,
                "name": w.name,
                "trigger": w.trigger,
                "owner": w.owner,
                "steps": len(w.steps),
            }
            for w in self.registry.workflows
        ]

    def list_instances(self, workflow_id: str = "") -> list[dict[str, Any]]:
        """List all running workflow instances, optionally filtered."""
        instances = self._instances.values()
        if workflow_id:
            instances = [i for i in instances if i.workflow.id == workflow_id]
        return [i.status() for i in instances]

    def get_workflow(self, workflow_id: str) -> Workflow | None:
        """Get a workflow definition by ID."""
        return self._workflows.get(workflow_id)

    def start(
        self,
        workflow_id: str,
        context: dict[str, Any] | None = None,
    ) -> str:
        """Start a new workflow instance. Returns the instance ID."""
        workflow = self._workflows.get(workflow_id)
        if workflow is None:
            raise ValueError(f"Workflow '{workflow_id}' not found")

        instance_id = f"{workflow_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        instance = WorkflowInstance(
            instance_id=instance_id,
            workflow=workflow,
            context=context or {},
        )
        self._instances[instance_id] = instance
        self._save_instance(instance)
        return instance_id

    def get_status(self, instance_id: str) -> dict[str, Any] | None:
        """Get the status of a workflow instance."""
        instance = self._instances.get(instance_id)
        if instance is None:
            return None
        return instance.status()

    def advance(self, instance_id: str) -> dict[str, Any]:
        """Advance a workflow to its next step."""
        instance = self._instances.get(instance_id)
        if instance is None:
            raise ValueError(f"Instance '{instance_id}' not found")
        result = instance.advance()
        self._save_instance(instance)
        return result

    def complete_step(self, instance_id: str, result: str = "") -> dict[str, Any]:
        """Mark the current step as completed."""
        instance = self._instances.get(instance_id)
        if instance is None:
            raise ValueError(f"Instance '{instance_id}' not found")
        result_data = instance.complete_step(result)
        self._save_instance(instance)
        return result_data

    def cancel(self, instance_id: str) -> dict[str, Any]:
        """Cancel a workflow instance."""
        instance = self._instances.get(instance_id)
        if instance is None:
            raise ValueError(f"Instance '{instance_id}' not found")
        result = instance.cancel()
        self._save_instance(instance)
        return result

    def to_tasks(self, instance_id: str) -> list[Task]:
        """Convert workflow steps to Task objects for the executor."""
        instance = self._instances.get(instance_id)
        if instance is None:
            return []
        return instance.to_tasks()


class WorkflowInstance:
    """Tracks the state of a running workflow."""

    def __init__(
        self,
        instance_id: str,
        workflow: Workflow,
        context: dict[str, Any],
    ) -> None:
        self.instance_id = instance_id
        self.workflow = workflow
        self.context = context
        self.current_step_index = 0
        self.step_results: dict[str, str] = {}
        self.started_at = datetime.now()
        self.completed_at: datetime | None = None
        self.status_label = "running"

    # ── Serialization ─────────────────────────────────────────────────

    def to_dict(self) -> dict[str, Any]:
        """Serialize the instance to a dict for persistence."""
        return {
            "instance_id": self.instance_id,
            "workflow_id": self.workflow.id,
            "workflow_name": self.workflow.name,
            "context": self.context,
            "current_step_index": self.current_step_index,
            "step_results": self.step_results,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "status": self.status_label,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        workflow: Workflow,
    ) -> WorkflowInstance:
        """Deserialize an instance from a dict."""
        instance = cls(
            instance_id=data["instance_id"],
            workflow=workflow,
            context=data.get("context", {}),
        )
        instance.current_step_index = data.get("current_step_index", 0)
        instance.step_results = data.get("step_results", {})
        started = data.get("started_at", "")
        if started:
            try:
                instance.started_at = datetime.fromisoformat(started)
            except (ValueError, TypeError):
                instance.started_at = datetime.now()
        completed = data.get("completed_at")
        if completed:
            try:
                instance.completed_at = datetime.fromisoformat(completed)
            except (ValueError, TypeError):
                pass
        instance.status_label = data.get("status", "running")
        return instance

    # ── Status & mutations ────────────────────────────────────────────

    def status(self) -> dict[str, Any]:
        """Return current workflow status."""
        current = self._current_step()
        return {
            "instance_id": self.instance_id,
            "workflow_id": self.workflow.id,
            "workflow_name": self.workflow.name,
            "status": self.status_label,
            "current_step": current.name if current else None,
            "current_step_index": self.current_step_index,
            "total_steps": len(self.workflow.steps),
            "completed_steps": len(self.step_results),
            "step_results": self.step_results,
        }

    def advance(self) -> dict[str, Any]:
        """Move to the next step."""
        if self.status_label != "running":
            return {"error": f"Workflow is {self.status_label}", **self.status()}

        if self.current_step_index >= len(self.workflow.steps) - 1:
            self.status_label = "completed"
            self.completed_at = datetime.now()
            return {"message": "Workflow completed", **self.status()}

        self.current_step_index += 1
        return {"message": "Advanced to next step", **self.status()}

    def complete_step(self, result: str = "") -> dict[str, Any]:
        """Mark the current step as completed with a result."""
        if self.status_label != "running":
            return {"error": f"Workflow is {self.status_label}", **self.status()}

        current = self._current_step()
        if current:
            self.step_results[current.id] = result

        # Auto-advance if not last step
        if self.current_step_index >= len(self.workflow.steps) - 1:
            self.status_label = "completed"
            self.completed_at = datetime.now()
            return {"message": "Workflow completed", **self.status()}

        self.current_step_index += 1
        return {"message": "Step completed, advanced", **self.status()}

    def cancel(self) -> dict[str, Any]:
        """Cancel the workflow."""
        self.status_label = "cancelled"
        self.completed_at = datetime.now()
        return {"message": "Workflow cancelled", **self.status()}

    def to_tasks(self) -> list[Task]:
        """Convert all workflow steps to Task objects."""
        tasks = []
        for i, step in enumerate(self.workflow.steps):
            status = TaskStatus.COMPLETED if step.id in self.step_results else (
                TaskStatus.IN_PROGRESS if i == self.current_step_index else TaskStatus.PENDING
            )
            task = Task(
                id=f"{self.instance_id}_{step.id}",
                name=step.name,
                description=step.action,
                assignee=step.owner or self.workflow.owner,
                status=status,
                priority=TaskPriority.HIGH if i == self.current_step_index else TaskPriority.MEDIUM,
            )
            tasks.append(task)
        return tasks

    def _current_step(self) -> WorkflowStep | None:
        """Get the current step."""
        if 0 <= self.current_step_index < len(self.workflow.steps):
            return self.workflow.steps[self.current_step_index]
        return None
