"""Domain models for AI Company Builder v2.

Every object in the company is represented as a Pydantic model.
All models support YAML/JSON serialization and full validation.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AgentType(str, Enum):
    HUMAN = "human"
    AI = "ai"


class Seniority(str, Enum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    ESCALATED = "escalated"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MeetingFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"


class EnforcementType(str, Enum):
    AUTOMATED = "automated"
    MANUAL = "manual"


class VotingMajority(str, Enum):
    SIMPLE = "simple"
    SUPER = "super"
    UNANIMOUS = "unanimous"


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------

class EntityBase(BaseModel):
    """Base for all named entities."""
    id: str = Field(..., min_length=1, description="Unique identifier")
    name: str = Field(default="", description="Human-readable name")


# ---------------------------------------------------------------------------
# Company
# ---------------------------------------------------------------------------

class CompanyStructure(BaseModel):
    type: str = "corporation"
    board_of_directors: bool = True
    executive_team: bool = True
    departments: bool = True


class Company(EntityBase):
    legal_name: str = ""
    founded: str = ""
    industry: str = ""
    headquarters: str = ""
    website: str = ""
    ceo: str = ""
    mission: str = ""
    vision: str = ""
    values: list[str] = Field(default_factory=list)
    structure: CompanyStructure = Field(default_factory=CompanyStructure)


class Vision(BaseModel):
    mission: str = ""
    long_term_goals: list[LongTermGoal] = Field(default_factory=list)
    quarterly_objectives: list[QuarterlyObjective] = Field(default_factory=list)


class LongTermGoal(BaseModel):
    goal: str
    timeline: str = ""
    metrics: list[str] = Field(default_factory=list)


class QuarterlyObjective(BaseModel):
    quarter: str
    objectives: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Strategy
# ---------------------------------------------------------------------------

class StrategyKPI(BaseModel):
    name: str
    target: float = 0
    unit: str = ""


class StrategyPillar(BaseModel):
    name: str
    description: str = ""
    priorities: list[str] = Field(default_factory=list)
    kpis: list[StrategyKPI] = Field(default_factory=list)


class QuarterlyFocus(BaseModel):
    current_quarter: str = ""
    focus_area: str = ""


class Strategy(BaseModel):
    pillars: list[StrategyPillar] = Field(default_factory=list)
    quarterly_focus: QuarterlyFocus = Field(default_factory=QuarterlyFocus)


# ---------------------------------------------------------------------------
# Culture
# ---------------------------------------------------------------------------

class CultureValue(BaseModel):
    name: str
    description: str = ""
    behaviors: list[str] = Field(default_factory=list)


class MeetingCadence(BaseModel):
    daily_standup: bool = False
    weekly_sync: bool = True
    monthly_all_hands: bool = True
    quarterly_review: bool = True


class CommunicationConfig(BaseModel):
    style: str = "Direct, concise, data-driven"
    tools: list[str] = Field(default_factory=list)
    meeting_cadence: MeetingCadence = Field(default_factory=MeetingCadence)


class Culture(BaseModel):
    values: list[CultureValue] = Field(default_factory=list)
    communication: CommunicationConfig = Field(default_factory=CommunicationConfig)
    norms: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Governance
# ---------------------------------------------------------------------------

class DecisionRight(BaseModel):
    level: str
    authority: str
    scope: list[str] = Field(default_factory=list)


class EscalationRule(BaseModel):
    trigger: str
    action: str


class GovernanceApproval(BaseModel):
    action: str
    required_approvals: list[str] = Field(default_factory=list)
    sla_hours: int = 24


class Governance(BaseModel):
    decision_rights: list[DecisionRight] = Field(default_factory=list)
    escalation_rules: list[EscalationRule] = Field(default_factory=list)
    approval_matrix: list[GovernanceApproval] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Policy
# ---------------------------------------------------------------------------

class Policy(EntityBase):
    category: str = ""
    description: str = ""
    rules: list[str] = Field(default_factory=list)
    enforcement: EnforcementType = EnforcementType.MANUAL
    ci_check: bool = False


# ---------------------------------------------------------------------------
# KPI
# ---------------------------------------------------------------------------

class KPI(EntityBase):
    category: str = ""
    target: float = 0
    current: float = 0
    unit: str = ""
    frequency: str = "monthly"
    owner: str = ""


# ---------------------------------------------------------------------------
# Budget
# ---------------------------------------------------------------------------

class DepartmentBudget(BaseModel):
    name: str
    budget: float = 0
    headcount: int = 0
    priorities: list[str] = Field(default_factory=list)


class Contingency(BaseModel):
    percentage: float = 5
    amount: float = 0
    approval_required: str = "cfo"


class Budget(BaseModel):
    fiscal_year: int = 2024
    total_budget: float = 0
    currency: str = "USD"
    departments: list[DepartmentBudget] = Field(default_factory=list)
    contingency: Contingency = Field(default_factory=Contingency)


# ---------------------------------------------------------------------------
# Board
# ---------------------------------------------------------------------------

class BoardMember(EntityBase):
    role: str = ""
    type: str = "independent"
    expertise: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    term_start: str = ""
    term_end: str = ""


class Committee(EntityBase):
    chair: str = ""
    members: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    meeting_frequency: str = "quarterly"


class BoardMeeting(EntityBase):
    frequency: str = "quarterly"
    agenda_items: list[str] = Field(default_factory=list)
    required_attendees: list[str] = Field(default_factory=list)
    quorum: int = 4


class VotingRule(BaseModel):
    type: str = ""
    quorum: int = 4
    majority: VotingMajority = VotingMajority.SIMPLE
    requires_unanimous: bool = False


class VotingConfig(BaseModel):
    default_rules: VotingRule = Field(default_factory=lambda: VotingRule(type="default"))
    decisions: list[VotingRule] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Executive
# ---------------------------------------------------------------------------

class Executive(EntityBase):
    title: str = ""
    department: str = ""
    reports_to: str = ""
    type: AgentType = AgentType.AI
    mission: str = ""
    responsibilities: list[str] = Field(default_factory=list)
    decision_rights: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Department
# ---------------------------------------------------------------------------

class Department(EntityBase):
    executive: str = ""
    mission: str = ""
    budget_category: str = ""
    headcount_target: int = 0


# ---------------------------------------------------------------------------
# Agent / Specialist
# ---------------------------------------------------------------------------

class Agent(EntityBase):
    department: str = ""
    reports_to: str = ""
    mission: str = ""
    type: AgentType = AgentType.AI
    responsibilities: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    seniority: Seniority = Seniority.MID


# ---------------------------------------------------------------------------
# Project
# ---------------------------------------------------------------------------

class ProjectPhase(BaseModel):
    name: str
    description: str = ""
    duration_weeks: int = 4
    deliverables: list[str] = Field(default_factory=list)


class Project(EntityBase):
    department: str = ""
    owner: str = ""
    description: str = ""
    phases: list[ProjectPhase] = Field(default_factory=list)
    budget: float = 0
    start_date: str = ""
    end_date: str = ""


# ---------------------------------------------------------------------------
# Workflow
# ---------------------------------------------------------------------------

class WorkflowStep(BaseModel):
    id: str
    name: str
    action: str = ""
    owner: str = ""
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    sla_hours: int = 0
    sla_minutes: int = 0
    sla_days: int = 0


class Workflow(EntityBase):
    description: str = ""
    trigger: str = ""
    owner: str = ""
    steps: list[WorkflowStep] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Meeting
# ---------------------------------------------------------------------------

class MeetingAgendaItem(BaseModel):
    topic: str
    presenter: str = ""
    duration_minutes: int = 10
    notes: str = ""


class MeetingDecision(BaseModel):
    decision: str
    owner: str = ""
    deadline: str = ""


class Meeting(EntityBase):
    date: str = ""
    attendees: list[str] = Field(default_factory=list)
    agenda: list[MeetingAgendaItem] = Field(default_factory=list)
    decisions: list[MeetingDecision] = Field(default_factory=list)
    notes: str = ""


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

class Task(EntityBase):
    """Task model — supports both legacy (sender/receiver) and new (assignee) patterns."""

    name: str = ""
    description: str = ""
    assignee: str = ""

    # Legacy fields for backward compatibility with message_bus, executor, specialists
    sender_id: str = ""
    receiver_id: str = ""
    instruction: str = ""

    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    dependencies: list[str] = Field(default_factory=list)
    due_date: str = ""
    tags: list[str] = Field(default_factory=list)

    # Legacy completion fields
    created_at: str = ""
    completed_at: str = ""
    result: str = ""
    requires_approval: bool = False
    approved_by: str = ""


# ---------------------------------------------------------------------------
# Risk
# ---------------------------------------------------------------------------

class Risk(EntityBase):
    category: str = ""
    description: str = ""
    likelihood: int = Field(default=3, ge=1, le=5)
    impact: int = Field(default=3, ge=1, le=5)
    level: RiskLevel = RiskLevel.MEDIUM
    mitigation: str = ""
    owner: str = ""


# ---------------------------------------------------------------------------
# Decision
# ---------------------------------------------------------------------------

class DecisionRecord(EntityBase):
    description: str = ""
    decision_maker: str = ""
    alternatives: list[str] = Field(default_factory=list)
    chosen_option: str = ""
    rationale: str = ""
    date: str = ""
    status: str = "pending"


# ---------------------------------------------------------------------------
# Permission
# ---------------------------------------------------------------------------

class Permission(BaseModel):
    read: bool = True
    grep: bool = True
    list: bool = True
    edit: bool = False
    bash: bool = False
    task: bool = False


# ---------------------------------------------------------------------------
# Integration
# ---------------------------------------------------------------------------

class Integration(EntityBase):
    type: str = ""
    description: str = ""
    config: dict[str, Any] = Field(default_factory=dict)
    enabled: bool = True


# ---------------------------------------------------------------------------
# Tool
# ---------------------------------------------------------------------------

class Tool(EntityBase):
    description: str = ""
    category: str = ""
    permissions: Permission = Field(default_factory=Permission)


# ---------------------------------------------------------------------------
# Decision Engine Models
# ---------------------------------------------------------------------------

class ApprovalEntry(BaseModel):
    action: str
    risk_level: str = "low"
    required_approvals: list[str] = Field(default_factory=list)
    sla_hours: int = 24
    auto_approve: bool = False


class RiskCategory(BaseModel):
    name: str
    description: str = ""
    owner: str = ""


class RiskLevelConfig(BaseModel):
    min_score: int
    max_score: int
    level: str
    action: str
    review_frequency: str = "monthly"


class RiskMatrixConfig(BaseModel):
    categories: list[RiskCategory] = Field(default_factory=list)
    risk_levels: list[RiskLevelConfig] = Field(default_factory=list)


class DecisionNode(BaseModel):
    id: str
    question: str = ""
    action: str = ""
    authority: str = ""
    type: str = "branch"
    children: list[str] = Field(default_factory=list)
    sla_hours: int = 0


class DecisionTreeConfig(BaseModel):
    nodes: list[DecisionNode] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Registry (aggregated)
# ---------------------------------------------------------------------------

class CompanyRegistry(BaseModel):
    """Top-level registry loaded from all config/ YAML files."""
    company: Company = Field(default_factory=lambda: Company(id="default", name="AI Company"))
    vision: Vision = Field(default_factory=Vision)
    strategy: Strategy = Field(default_factory=Strategy)
    culture: Culture = Field(default_factory=Culture)
    governance: Governance = Field(default_factory=Governance)
    policies: list[Policy] = Field(default_factory=list)
    kpis: list[KPI] = Field(default_factory=list)
    budget: Budget = Field(default_factory=Budget)
    board: list[BoardMember] = Field(default_factory=list)
    committees: list[Committee] = Field(default_factory=list)
    board_meetings: list[BoardMeeting] = Field(default_factory=list)
    voting: VotingConfig = Field(default_factory=VotingConfig)
    executives: list[Executive] = Field(default_factory=list)
    departments: list[Department] = Field(default_factory=list)
    specialists: list[Agent] = Field(default_factory=list)
    workflows: list[Workflow] = Field(default_factory=list)
    approval_matrix: list[ApprovalEntry] = Field(default_factory=list)
    risk_matrix: RiskMatrixConfig = Field(default_factory=RiskMatrixConfig)
    decision_tree: DecisionTreeConfig = Field(default_factory=DecisionTreeConfig)
