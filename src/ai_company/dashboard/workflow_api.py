"""Workflow API service — bridges WorkflowEngine to the dashboard API.

Maintains a module-level singleton so the engine is created once and
shared across requests.  Thread-safety is delegated to the underlying
FileStore (atomic writes) and the GIL (dict reads are safe).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from ai_company.paths import get_data_root

logger = logging.getLogger(__name__)

_engine: Any = None


def get_workflow_engine() -> Any:
    """Return the shared WorkflowEngine singleton (lazily created)."""
    global _engine  # noqa: PLW0603
    if _engine is not None:
        return _engine

    try:
        from ai_company.models import CompanyRegistry, Workflow, WorkflowStep
        from ai_company.store.file_store import FileStore
        from ai_company.workflow.engine import WorkflowEngine

        state_dir = Path(get_data_root()) / "workflows" / "instances"
        state_dir.mkdir(parents=True, exist_ok=True)

        store = FileStore(Path(get_data_root()))

        # Load workflow definitions from config YAML
        raw_yaml: Any = store.read_yaml("config/workflows/workflows.yaml")
        raw_workflows: list[dict[str, Any]] = []
        if isinstance(raw_yaml, dict):
            raw_workflows = raw_yaml.get("workflows", [])

        workflows: list[Workflow] = []
        for wf_dict in raw_workflows:
            steps = []
            for s in wf_dict.get("steps", []):
                steps.append(
                    WorkflowStep(
                        id=s.get("id", ""),
                        name=s.get("name", ""),
                        action=s.get("action", ""),
                        owner=s.get("owner", ""),
                        inputs=s.get("inputs", []),
                        outputs=s.get("outputs", []),
                        sla_hours=s.get("sla_hours", 0),
                        sla_minutes=s.get("sla_minutes", 0),
                        sla_days=s.get("sla_days", 0),
                    )
                )
            workflows.append(
                Workflow(
                    id=wf_dict.get("id", ""),
                    name=wf_dict.get("name", ""),
                    description=wf_dict.get("description", ""),
                    trigger=wf_dict.get("trigger", ""),
                    owner=wf_dict.get("owner", ""),
                    steps=steps,
                )
            )

        registry = CompanyRegistry(workflows=workflows)

        _engine = WorkflowEngine(registry, state_dir=str(state_dir))
        logger.info("WorkflowEngine initialised with %d workflows", len(workflows))
    except Exception:  # noqa: BLE001
        logger.exception("Failed to initialise WorkflowEngine")
        # Create an empty engine so endpoints still return empty lists
        from ai_company.models import CompanyRegistry
        from ai_company.workflow.engine import WorkflowEngine

        _engine = WorkflowEngine(
            CompanyRegistry(),
            state_dir=str(Path(get_data_root()) / "workflows" / "instances"),
        )
    return _engine


def list_workflows() -> list[dict[str, Any]]:
    """Return all registered workflow definitions."""
    engine = get_workflow_engine()
    result: list[dict[str, Any]] = engine.list_workflows()
    return result


def list_instances(workflow_id: str = "") -> list[dict[str, Any]]:
    """Return running workflow instances, optionally filtered by workflow ID."""
    engine = get_workflow_engine()
    result: list[dict[str, Any]] = engine.list_instances(workflow_id=workflow_id)
    return result


def get_instance_status(instance_id: str) -> dict[str, Any] | None:
    """Return the status of a single workflow instance."""
    engine = get_workflow_engine()
    result: dict[str, Any] | None = engine.get_status(instance_id)
    return result


def start_workflow(
    workflow_id: str, context: dict[str, Any] | None = None
) -> str:
    """Start a new workflow instance; returns the instance ID."""
    engine = get_workflow_engine()
    result: str = engine.start(workflow_id, context=context)
    return result


def advance_workflow(instance_id: str) -> dict[str, Any]:
    """Advance a workflow instance to the next step."""
    engine = get_workflow_engine()
    result: dict[str, Any] = engine.advance(instance_id)
    return result


def complete_step(instance_id: str, result: str = "") -> dict[str, Any]:
    """Mark the current step as completed."""
    engine = get_workflow_engine()
    data: dict[str, Any] = engine.complete_step(instance_id, result=result)
    return data


def cancel_workflow(instance_id: str) -> dict[str, Any]:
    """Cancel a workflow instance."""
    engine = get_workflow_engine()
    data: dict[str, Any] = engine.cancel(instance_id)
    return data


def _build_instance_detail(status: dict[str, Any]) -> dict[str, Any]:
    """Enrich a workflow status dict with step detail for the API response.

    Adds a ``steps`` list with per-step status (completed / in_progress /
    pending) so the frontend can render the pipeline in one request.
    """
    engine = get_workflow_engine()
    workflow = engine.get_workflow(status.get("workflow_id", ""))
    if workflow is None:
        status["steps"] = []
        return status

    step_results: dict[str, str] = status.get("step_results", {})
    current_idx: int = status.get("current_step_index", 0)

    steps: list[dict[str, Any]] = []
    for i, step in enumerate(workflow.steps):
        if step.id in step_results:
            step_status = "completed"
            step_result = step_results[step.id]
        elif i == current_idx and status.get("status") == "running":
            step_status = "in_progress"
            step_result = ""
        elif i == current_idx and status.get("status") == "cancelled":
            step_status = "cancelled"
            step_result = ""
        else:
            step_status = "pending"
            step_result = ""
        steps.append(
            {
                "id": step.id,
                "name": step.name,
                "action": step.action,
                "owner": step.owner,
                "inputs": step.inputs,
                "outputs": step.outputs,
                "status": step_status,
                "result": step_result,
                "sla_hours": step.sla_hours,
                "sla_minutes": step.sla_minutes,
                "sla_days": step.sla_days,
            }
        )
    status["steps"] = steps
    return status
