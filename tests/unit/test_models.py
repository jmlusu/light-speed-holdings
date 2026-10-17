"""Tests for domain models."""

import pytest
from pydantic import ValidationError

from ai_company.models.models import (
    Agent,
    AgentType,
    BoardMember,
    Budget,
    Company,
    CompanyRegistry,
    Department,
    DepartmentBudget,
    Executive,
    Seniority,
    Task,
    TaskEventType,
    TaskPriority,
    TaskResult,
    TaskStatus,
    Workflow,
    WorkflowStep,
)

# ---------------------------------------------------------------------------
# Executive
# ---------------------------------------------------------------------------


class TestExecutive:
    def test_create_executive(self):
        ex = Executive(id="cto", title="CTO", department="Tech", reports_to="ceo")
        assert ex.id == "cto"
        assert ex.title == "CTO"
        assert ex.type == AgentType.AI

    def test_executive_with_responsibilities(self):
        ex = Executive(
            id="cfo",
            name="CFO",
            title="CFO",
            responsibilities=["Budget", "Finance"],
        )
        assert "Budget" in ex.responsibilities

    def test_executive_requires_id(self):
        with pytest.raises(ValidationError):
            Executive(title="No ID")


# ---------------------------------------------------------------------------
# Department
# ---------------------------------------------------------------------------


class TestDepartment:
    def test_create_department(self):
        dept = Department(id="eng", name="Engineering", executive="cto")
        assert dept.id == "eng"
        assert dept.executive == "cto"

    def test_department_defaults(self):
        dept = Department(id="sales")
        assert dept.headcount_target == 0


# ---------------------------------------------------------------------------
# Agent / Specialist
# ---------------------------------------------------------------------------


class TestAgent:
    def test_create_agent(self):
        agent = Agent(id="dev-1", name="Dev", department="eng", reports_to="cto")
        assert agent.seniority == Seniority.MID

    def test_agent_with_tools(self):
        agent = Agent(id="dev-1", tools=["read_file", "write_file"])
        assert "read_file" in agent.tools


# ---------------------------------------------------------------------------
# Board
# ---------------------------------------------------------------------------


class TestBoardMember:
    def test_create_board_member(self):
        bm = BoardMember(id="dir-1", name="Alice", role="Chair")
        assert bm.type == "independent"


# ---------------------------------------------------------------------------
# Task (backward-compatible)
# ---------------------------------------------------------------------------


class TestTask:
    def test_legacy_fields(self):
        t = Task(
            id="t1",
            sender_id="user",
            receiver_id="agent",
            instruction="Do something",
        )
        assert t.sender_id == "user"
        assert t.receiver_id == "agent"
        assert t.instruction == "Do something"

    def test_new_fields(self):
        t = Task(id="t2", description="New style", assignee="agent-1")
        assert t.description == "New style"
        assert t.assignee == "agent-1"

    def test_defaults(self):
        t = Task(id="t3")
        assert t.status == TaskStatus.PENDING
        assert t.priority == TaskPriority.MEDIUM
        assert t.name == ""


# ---------------------------------------------------------------------------
# Workflow
# ---------------------------------------------------------------------------


class TestWorkflow:
    def test_create_workflow(self):
        wf = Workflow(
            id="hiring",
            name="Hiring",
            steps=[
                WorkflowStep(id="s1", name="Post Job"),
                WorkflowStep(id="s2", name="Review Resumes"),
            ],
        )
        assert len(wf.steps) == 2
        assert wf.steps[0].id == "s1"


# ---------------------------------------------------------------------------
# Budget
# ---------------------------------------------------------------------------


class TestBudget:
    def test_budget_defaults(self):
        b = Budget()
        assert b.total_budget == 0
        assert b.currency == "USD"

    def test_budget_with_departments(self):
        b = Budget(
            total_budget=1000000,
            departments=[
                DepartmentBudget(name="Eng", budget=500000, headcount=10),
            ],
        )
        assert len(b.departments) == 1


# ---------------------------------------------------------------------------
# CompanyRegistry
# ---------------------------------------------------------------------------


class TestCompanyRegistry:
    def test_default_registry(self):
        r = CompanyRegistry()
        assert r.company.id == "default"
        assert r.executives == []
        assert r.departments == []

    def test_full_registry(self):
        r = CompanyRegistry(
            company=Company(id="co", name="Acme"),
            executives=[Executive(id="ceo", title="CEO")],
            departments=[Department(id="eng")],
            specialists=[Agent(id="dev")],
        )
        assert r.company.name == "Acme"
        assert len(r.executives) == 1


# ---------------------------------------------------------------------------
# TaskEventType
# ---------------------------------------------------------------------------


class TestTaskEventType:
    def test_all_events_defined(self):
        expected = {
            "queued",
            "claimed",
            "running",
            "completed",
            "failed",
            "timeout",
            "cancelled",
            "escalated",
            "retrying",
        }
        assert {e.value for e in TaskEventType} == expected

    def test_event_is_string_serializable(self):
        assert TaskEventType.QUEUED == "queued"
        assert str(TaskEventType.RUNNING) == "TaskEventType.RUNNING"


# ---------------------------------------------------------------------------
# TaskResult
# ---------------------------------------------------------------------------


class TestTaskResult:
    def test_create_minimal(self):
        r = TaskResult(task_id="t1")
        assert r.task_id == "t1"
        assert r.status == TaskStatus.PENDING
        assert r.output == ""
        assert r.errors == []
        assert r.duration_seconds == 0.0
        assert r.tokens_used == 0
        assert r.cost_usd == 0.0
        assert r.attempt == 1

    def test_create_full(self):
        r = TaskResult(
            task_id="t2",
            status=TaskStatus.COMPLETED,
            output="Done",
            errors=[],
            duration_seconds=1.5,
            tokens_used=500,
            cost_usd=0.001,
            provider="gemini",
            model="gemini-2.5-flash",
            attempt=2,
            created_at="2026-08-20T12:00:00Z",
        )
        assert r.status == TaskStatus.COMPLETED
        assert r.output == "Done"
        assert r.provider == "gemini"
        assert r.attempt == 2

    def test_mark_success(self):
        r = TaskResult(task_id="t3")
        r.mark_success(
            output="Result text",
            duration=2.0,
            provider="openai",
            model="gpt-4o",
            tokens_used=1000,
            cost_usd=0.005,
        )
        assert r.status == TaskStatus.COMPLETED
        assert r.output == "Result text"
        assert r.duration_seconds == 2.0
        assert r.provider == "openai"
        assert r.model == "gpt-4o"
        assert r.tokens_used == 1000
        assert r.cost_usd == 0.005

    def test_mark_failure(self):
        r = TaskResult(task_id="t4")
        r.mark_failure("Timeout after 30s", duration=30.0)
        assert r.status == TaskStatus.FAILED
        assert r.errors == ["Timeout after 30s"]
        assert r.duration_seconds == 30.0

    def test_mark_failure_accumulates_errors(self):
        r = TaskResult(task_id="t5")
        r.mark_failure("First error", duration=1.0)
        r.mark_failure("Second error", duration=2.0)
        assert len(r.errors) == 2
        assert r.errors[0] == "First error"
        assert r.errors[1] == "Second error"
        assert r.duration_seconds == 2.0

    def test_extra_fields_ignored(self):
        r = TaskResult(task_id="t6", unknown_field="value")
        assert r.task_id == "t6"
        assert not hasattr(r, "unknown_field")

    def test_serialization_roundtrip(self):
        r = TaskResult(
            task_id="t7",
            status=TaskStatus.COMPLETED,
            output="Hello",
            duration_seconds=0.5,
            provider="gemini",
            model="gemini-2.5-flash",
        )
        data = r.model_dump()
        r2 = TaskResult.model_validate(data)
        assert r2.task_id == r.task_id
        assert r2.status == r.status
        assert r2.output == r.output
