"""Workflow engine — executes and manages company workflows."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from ai_company.models import (
    CompanyRegistry,
    Task,
    TaskPriority,
    TaskStatus,
    Workflow,
    WorkflowStep,
)


class WorkflowEngine:
    """Manages workflow execution, step tracking, and SLA monitoring."""

    def __init__(self, registry: CompanyRegistry) -> None:
        self.registry = registry
        self._workflows: dict[str, Workflow] = {w.id: w for w in registry.workflows}
        self._instances: dict[str, WorkflowInstance] = {}

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

    def get_workflow(self, workflow_id: str) -> Workflow | None:
        """Get a workflow definition by ID."""
        return self._workflows.get(workflow_id)

    def start(self, workflow_id: str, context: dict[str, Any] | None = None) -> str:
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
        return instance.advance()

    def complete_step(self, instance_id: str, result: str = "") -> dict[str, Any]:
        """Mark the current step as completed."""
        instance = self._instances.get(instance_id)
        if instance is None:
            raise ValueError(f"Instance '{instance_id}' not found")
        return instance.complete_step(result)

    def cancel(self, instance_id: str) -> dict[str, Any]:
        """Cancel a workflow instance."""
        instance = self._instances.get(instance_id)
        if instance is None:
            raise ValueError(f"Instance '{instance_id}' not found")
        return instance.cancel()

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
