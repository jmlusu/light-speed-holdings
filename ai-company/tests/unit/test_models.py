"""Tests for domain models."""

import pytest
from pydantic import ValidationError

from ai_company.models.models import (
    Agent,
    AgentType,
    ApprovalEntry,
    BoardMember,
    Budget,
    Company,
    CompanyRegistry,
    Committee,
    Culture,
    DecisionNode,
    Department,
    DepartmentBudget,
    Executive,
    Governance,
    KPI,
    Meeting,
    Permission,
    Policy,
    Project,
    Risk,
    Seniority,
    Strategy,
    Task,
    TaskPriority,
    TaskStatus,
    Vision,
    VotingConfig,
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
            id="cfo", name="CFO", title="CFO",
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
