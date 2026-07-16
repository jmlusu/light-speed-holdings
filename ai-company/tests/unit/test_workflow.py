"""Tests for the Workflow engine."""

from __future__ import annotations

import pytest

from ai_company.workflow.engine import WorkflowEngine
from ai_company.models import (
    CompanyRegistry,
    Company,
    Workflow,
    WorkflowStep,
)


@pytest.fixture()
def registry() -> CompanyRegistry:
    return CompanyRegistry(
        company=Company(id="test", name="Test"),
        workflows=[
            Workflow(
                id="hiring",
                name="Hiring Workflow",
                trigger="job_requisition",
                owner="hr",
                steps=[
                    WorkflowStep(id="post", name="Post Job", action="Create job posting", owner="recruiter"),
                    WorkflowStep(id="review", name="Review Resumes", action="Screen candidates", owner="recruiter"),
                    WorkflowStep(id="interview", name="Interview", action="Conduct interviews", owner="hiring_manager"),
                    WorkflowStep(id="offer", name="Make Offer", action="Extend offer", owner="hr"),
                ],
            ),
            Workflow(
                id="simple",
                name="Simple Workflow",
                trigger="manual",
                owner="ops",
                steps=[
                    WorkflowStep(id="s1", name="Step 1", action="Do thing"),
                ],
            ),
        ],
    )


@pytest.fixture()
def engine(registry: CompanyRegistry) -> WorkflowEngine:
    return WorkflowEngine(registry)


class TestWorkflowEngine:
    def test_list_workflows(self, engine: WorkflowEngine):
        workflows = engine.list_workflows()
        assert len(workflows) == 2
        ids = [w["id"] for w in workflows]
        assert "hiring" in ids
        assert "simple" in ids

    def test_get_workflow(self, engine: WorkflowEngine):
        wf = engine.get_workflow("hiring")
        assert wf is not None
        assert wf.name == "Hiring Workflow"
        assert len(wf.steps) == 4

    def test_get_workflow_not_found(self, engine: WorkflowEngine):
        assert engine.get_workflow("nonexistent") is None

    def test_start_workflow(self, engine: WorkflowEngine):
        instance_id = engine.start("hiring")
        assert instance_id.startswith("hiring_")
        status = engine.get_status(instance_id)
        assert status is not None
        assert status["status"] == "running"
        assert status["current_step"] == "Post Job"

    def test_start_unknown_workflow_raises(self, engine: WorkflowEngine):
        with pytest.raises(ValueError, match="not found"):
            engine.start("nonexistent")

    def test_complete_step(self, engine: WorkflowEngine):
        instance_id = engine.start("hiring")
        result = engine.complete_step(instance_id, "Posted on LinkedIn")
        assert result["message"] == "Step completed, advanced"
        assert result["current_step"] == "Review Resumes"
        assert "post" in result["step_results"]

    def test_advance_workflow(self, engine: WorkflowEngine):
        instance_id = engine.start("hiring")
        result = engine.advance(instance_id)
        assert result["current_step"] == "Review Resumes"

    def test_complete_all_steps(self, engine: WorkflowEngine):
        instance_id = engine.start("simple")
        result = engine.complete_step(instance_id, "done")
        assert result["status"] == "completed"

    def test_cancel_workflow(self, engine: WorkflowEngine):
        instance_id = engine.start("hiring")
        result = engine.cancel(instance_id)
        assert result["status"] == "cancelled"

    def test_cannot_advance_after_cancel(self, engine: WorkflowEngine):
        instance_id = engine.start("hiring")
        engine.cancel(instance_id)
        result = engine.advance(instance_id)
        assert "error" in result

    def test_to_tasks(self, engine: WorkflowEngine):
        instance_id = engine.start("hiring")
        tasks = engine.to_tasks(instance_id)
        assert len(tasks) == 4
        # First task should be in_progress
        assert tasks[0].status.value == "in_progress"
        # Rest should be pending
        assert tasks[1].status.value == "pending"

    def test_nonexistent_instance(self, engine: WorkflowEngine):
        assert engine.get_status("fake_id") is None
        with pytest.raises(ValueError):
            engine.advance("fake_id")
