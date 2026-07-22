"""Data models for Organization Chart component.

This module contains the core data structures and domain models used by the
organization chart implementation, including the enhanced OrgNode specification
from the requirements.
"""

from __future__ import annotations

from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class ExecutiveTier(str, Enum):
    """Executive tier levels."""
    TIER_1 = "tier_1"  # CEO, President, Founder
    TIER_2 = "tier_2"  # VP, Director, Lead, Manager
    TIER_3 = "tier_3"  # Owner, Engineer, Analyst, Specialist


class SuccessionRisk(str, Enum):
    """Succession risk levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CriticalSkillCategory(str, Enum):
    """Categories of critical skills for organizational roles."""
    LEADERSHIP = "leadership"
    STRATEGIC = "strategic"
    TECHNICAL = "technical"
    FINANCIAL = "financial"
    COMPLIANCE = "compliance"
    OPERATIONS = "operations"
    MARKETING = "marketing"
    SALES = "sales"
    CUSTOMER_SUCCESS = "customer_success"
    LEGAL = "legal"


# Enhanced OrgNode model matching the specifications
class EnhancedOrgNode(BaseModel):
    """
    Enhanced organizational node with comprehensive attributes for executive dashboards.

    This model extends the basic OrgNode with additional fields required for
    phase 3 organization chart functionality including capacity planning,
    succession risk analysis, and performance metrics.
    """

    model_config = ConfigDict(
        frozen=True,
        validate_assignment=True,
        extra="forbid"
    )

    # Core identification
    name: str = Field(..., description="Unique agent name", min_length=1, max_length=100)
    role: str = Field(..., description="Agent's role/title", min_length=1, max_length=100)
    department: str = Field(..., description="Department name")

    # Hierarchical information
    tier: int = Field(default=1, description="Executive tier 1-3", ge=1, le=3)
    children: List["EnhancedOrgNode"] = Field(default_factory=list, description="Direct reports/subordinates")
    reports_to: Optional[str] = Field(default=None, description="Parent reference agent name")

    # Capacity and utilization
    capacity: int = Field(default=0, description="Utilization percentage 0-100", ge=0, le=100)
    span_of_control: int = Field(default=0, description="Number of direct reports", ge=0)

    # Skills and performance
    critical_skills: List[str] = Field(default_factory=list, description="Critical skills required")
    succession_risk: str = Field(default="low", description="Succession risk level")
    performance_rating: float = Field(default=5.0, description="Performance rating 1-10", ge=1.0, le=10.0)

    # Additional attributes
    last_updated: str = Field(default_factory=datetime.now().isoformat, description="ISO timestamp")

    # Metadata
    agent_type: str = Field(default="agent", description="Type classification")
    seniority: str = Field(default="mid", description="Seniority level")
    model_tier: str = Field(default="standard", description="Model tier (fast/standard/premium)")

    # Organizational metrics
    active_tasks: int = Field(default=0, description="Number of active tasks assigned")
    completed_tasks: int = Field(default=0, description="Number of completed tasks")
    failure_rate: float = Field(default=0.0, description="Failure rate percentage 0-100", ge=0.0, le=100.0)
    cost_impact: float = Field(default=0.0, description="Financial impact in USD")

    # Team health indicators
    team_morale: float = Field(default=0.0, description="Team morale score 0-100", ge=0.0, le=100.0)
    employee_satisfaction: float = Field(default=0.0, description="Employee satisfaction score 0-100", ge=0.0, le=100.0)

    # Executive-specific metrics
    budget_responsibility: float = Field(default=0.0, description="Budget responsibility in USD")
    headcount_responsibility: int = Field(default=1, description="Number of people responsible for")
    strategic_importance: int = Field(default=5, description="Strategic importance 1-10", ge=1, le=10)

    # Timing and duration
    tenure_days: int = Field(default=0, description="Tenure in days")
    average_response_time: float = Field(default=0.0, description="Average response time in seconds")

    # Risk and compliance
    security_clearance_level: int = Field(default=1, description="Security clearance level", ge=1, le=5)
    compliance_violations: int = Field(default=0, description="Number of compliance violations")
    last_audit_date: Optional[str] = Field(default=None, description="Last audit date ISO format")

    @property
    def is_executive(self) -> bool:
        """Check if node is an executive level role."""
        return self.tier <= 2

    @property
    def has_critical_skills_gaps(self) -> bool:
        """Check if critical skills are missing."""
        # This would require comparison with a skills database
        return len(self.critical_skills) == 0

    @property
    def utilization_score(self) -> float:
        """Calculate utilization score based on multiple factors."""
        workload_factor = self.capacity / 100.0
        performance_factor = self.performance_rating / 10.0
        task_factor = min((self.active_tasks + self.completed_tasks) / 20.0, 1.0)

        return (workload_factor * 0.4 + performance_factor * 0.4 + task_factor * 0.2) * 100

    @property
    def risk_score(self) -> float:
        """Calculate overall risk score for the role."""
        # Combine multiple risk factors
        succession_risk_weight = {"low": 0.1, "medium": 0.3, "high": 0.6}.get(self.succession_risk, 0.1)
        performance_weight = (10.0 - self.performance_rating) / 10.0
        failure_weight = self.failure_rate / 100.0

        return (succession_risk_weight * 0.4 + performance_weight * 0.3 + failure_weight * 0.3) * 100

    @property
    def health_score(self) -> float:
        """Calculate overall health score for the role."""
        performance_health = self.performance_rating / 10.0 * 100
        utilization_health = 100 - abs(self.capacity - 70)  # Optimal around 70%
        satisfaction_health = (self.team_morale + self.employee_satisfaction) / 2.0

        return (performance_health * 0.5 + utilization_health * 0.2 + satisfaction_health * 0.3)

    @property
    def is_at_risk(self) -> bool:
        """Check if role is at risk based on multiple factors."""
        return (
            self.succession_risk == "high" or
            self.performance_rating < 3.0 or
            self.capacity > 90 or
            self.failure_rate > 20.0 or
            self.health_score < 60.0
        )

    @property
    def can_accept_more_load(self) -> bool:
        """Check if role can accept additional workload."""
        return self.capacity < 85 and self.performance_rating >= 7.0 and self.health_score > 70.0

    @property
    def needs_support(self) -> bool:
        """Check if role needs additional support."""
        return (
            self.performance_rating < 5.0 or
            self.health_score < 65.0 or
            self.succession_risk in ["medium", "high"] or
            self.capacity > 80
        )


class DepartmentSummary(BaseModel):
    """Summary statistics for a department."""

    name: str = Field(..., description="Department name")
    total_agents: int = Field(default=0, description="Total number of agents")
    executive_count: int = Field(default=0, description="Number of executive-level agents")
    specialist_count: int = Field(default=0, description="Number of specialist agents")
    avg_capacity: float = Field(default=0.0, description="Average capacity utilization")
    avg_performance: float = Field(default=0.0, description="Average performance rating")
    critical_skills: List[str] = Field(default_factory=list, description="Critical skills needed")
    succession_risk_count: Dict[str, int] = Field(default_factory=dict, description="Count by risk level")
    budget_utilization: float = Field(default=0.0, description="Budget utilization percentage")
    team_morale: float = Field(default=0.0, description="Average team morale")


class HierarchyMetrics(BaseModel):
    """Metrics about the organization hierarchy."""

    total_nodes: int = Field(default=0, description="Total number of nodes")
    total_edges: int = Field(default=0, description="Total number of hierarchical connections")
    max_depth: int = Field(default=0, description="Maximum hierarchy depth")
    avg_depth: float = Field(default=0.0, description="Average hierarchy depth")
    breadth: int = Field(default=0, description="Maximum breadth at any level")
    avg_breadth: float = Field(default=0.0, description="Average breadth")
    avg_span_of_control: float = Field(default=0.0, description="Average span of control")
    max_span_of_control: int = Field(default=0, description="Maximum span of control")
    leaf_nodes: int = Field(default=0, description="Number of leaf nodes (no children)")
    branching_factor: float = Field(default=0.0, description="Average branching factor")


class CapacityAnalysis(BaseModel):
    """Capacity analysis for organizational nodes."""

    node_id: str = Field(..., description="Node identifier")
    current_load: int = Field(default=0, description="Current workload units")
    max_capacity: int = Field(default=100, description="Maximum capacity")
    utilization_percentage: float = Field(default=0.0, description="Utilization percentage")
    available_capacity: int = Field(default=0, description="Available capacity units")
    capacity_buffer: float = Field(default=0.0, description="Buffer percentage")
    underloaded_nodes: List[str] = Field(default_factory=list, description="Nodes with low utilization")
    overloaded_nodes: List[str] = Field(default_factory=list, description="Nodes with high utilization")
    optimal_nodes: List[str] = Field(default_factory=list, description="Nodes at optimal utilization")


class PerformanceMetrics(BaseModel):
    """Performance metrics for organizational nodes."""

    node_id: str = Field(..., description="Node identifier")
    performance_rating: float = Field(default=0.0, description="Performance rating 1-10")
    completion_rate: float = Field(default=0.0, description="Task completion rate percentage")
    failure_rate: float = Field(default=0.0, description="Failure rate percentage")
    average_response_time: float = Field(default=0.0, description="Average response time")
    cost_efficiency: float = Field(default=0.0, description="Cost efficiency score")
    quality_score: float = Field(default=0.0, description="Quality score 0-100")
    time_to_completion: float = Field(default=0.0, description="Average time to completion")
    team_health: float = Field(default=0.0, description="Team health score 0-100")


class ExecutiveDashboardData(BaseModel):
    """Complete data for executive dashboard."""

    hierarchy_root: EnhancedOrgNode
    department_summaries: List[DepartmentSummary]
    hierarchy_metrics: HierarchyMetrics
    critical_issues: List[Dict[str, Any]]
    optimization_opportunities: List[Dict[str, Any]]
    recent_changes: List[Dict[str, Any]]
    key_insights: List[str]
    generated_at: str = Field(default_factory=datetime.now().isoformat)
    refresh_interval_minutes: int = Field(default=15, description="Dashboard refresh interval")


class RegistryNormalizerData(BaseModel):
    """Normalized registry data structure."""

    departments: List[EnhancedOrgNode]
    executive_roles: List[EnhancedOrgNode]
    specialist_roles: List[EnhancedOrgNode]
    reporting_chains: List[Dict[str, Any]]
    department_context: Dict[str, Any]
    validation_results: Dict[str, Any]
    processed_at: str = Field(default_factory=datetime.now().isoformat)
    data_integrity_score: float = Field(default=0.0, description="Data integrity score 0-100")


# Utility classes for data transformation
class DataTransformer:
    """Utility class for transforming data between different formats."""

    @staticmethod
    def orgnode_to_enhanced(org_node: EnhancedOrgNode) -> EnhancedOrgNode:
        """Convert basic OrgNode to EnhancedOrgNode."""
        return EnhancedOrgNode(
            name=org_node.name,
            role=org_node.role,
            department=org_node.department,
            tier=getattr(org_node, 'tier', 1),
            children=[DataTransformer.orgnode_to_enhanced(child) for child in org_node.children],
            reports_to=getattr(org_node, 'reports_to', None),
            capacity=getattr(org_node, 'capacity', 0),
            span_of_control=getattr(org_node, 'span_of_control', 0),
            critical_skills=getattr(org_node, 'critical_skills', []),
            succession_risk=getattr(org_node, 'succession_risk', 'low'),
            performance_rating=getattr(org_node, 'performance_rating', 5.0),
            last_updated=getattr(org_node, 'last_updated', datetime.now().isoformat()),
        )

    @staticmethod
    def registry_to_enhanced(registry_data: List[Dict[str, Any]]) -> List[EnhancedOrgNode]:
        """Convert registry data to EnhancedOrgNode objects."""
        enhanced_nodes = []

        for agent in registry_data:
            # Build hierarchy relationships
            children = []

            # Find direct reports — match on id (not name) since reports_to uses id
            agent_id = agent.get('id', '')
            agent_name = agent.get('name', '')
            for other_agent in registry_data:
                if other_agent.get('reports_to') in (agent_id, agent_name):
                    child_node = DataTransformer._agent_to_enhanced(other_agent)
                    children.append(child_node)

            enhanced_node = DataTransformer._agent_to_enhanced(agent)
            enhanced_node = enhanced_node.model_copy(update={"children": children})

            enhanced_nodes.append(enhanced_node)

        return enhanced_nodes

    @staticmethod
    def _agent_to_enhanced(agent_data: Dict[str, Any]) -> EnhancedOrgNode:
        """Convert agent dictionary to EnhancedOrgNode."""
        return EnhancedOrgNode(
            name=agent_data.get('name', agent_data.get('id', '')),
            role=agent_data.get('title', agent_data.get('name', '')),
            department=agent_data.get('department', ''),
            tier=DataTransformer._calculate_tier(agent_data),
            reports_to=agent_data.get('reports_to'),
            capacity=DataTransformer._calculate_capacity(agent_data),
            span_of_control=DataTransformer._calculate_span_of_control(agent_data),
            critical_skills=DataTransformer._extract_critical_skills(agent_data),
            succession_risk=DataTransformer._assess_succession_risk(agent_data),
            performance_rating=DataTransformer._calculate_performance_rating(agent_data),
        )

    @staticmethod
    def _calculate_tier(agent_data: Dict[str, Any]) -> int:
        """Calculate tier based on agent data."""
        title = agent_data.get('title', '').lower()

        if 'ceo' in title or 'chief' in title or 'president' in title:
            return 1
        elif 'vp' in title or 'director' in title or 'lead' in title or 'manager' in title:
            return 2
        else:
            return 3

    @staticmethod
    def _calculate_capacity(agent_data: Dict[str, Any]) -> int:
        """Calculate capacity utilization."""
        base_capacity = 60

        title = agent_data.get('title', '').lower()
        if 'chief' in title or 'ceo' in title:
            return 85
        elif 'vp' in title or 'director' in title:
            return 75
        elif 'manager' in title or 'lead' in title:
            return 65
        else:
            return base_capacity

    @staticmethod
    def _calculate_span_of_control(agent_data: Dict[str, Any]) -> int:
        """Calculate span of control."""
        direct_reports = agent_data.get('direct_reports', [])
        return len(direct_reports)

    @staticmethod
    def _extract_critical_skills(agent_data: Dict[str, Any]) -> List[str]:
        """Extract critical skills from agent data."""
        # Simplified skill extraction based on title and responsibilities
        title = agent_data.get('title', '').lower()
        skills = []

        if 'architect' in title or 'design' in title:
            skills.extend(['System Design', 'Architecture', 'Technical Leadership'])
        if 'lead' in title or 'manager' in title:
            skills.extend(['Team Leadership', 'Project Management', 'Stakeholder Management'])
        if 'analyst' in title:
            skills.extend(['Data Analysis', 'Statistical Analysis', 'Insight Generation'])
        if 'engineer' in title:
            skills.extend(['Software Development', 'Code Quality', 'Testing'])
        if 'owner' in title:
            skills.extend(['Business Ownership', 'Operations Management', 'Customer Success'])

        return list(set(skills))

    @staticmethod
    def _assess_succession_risk(agent_data: Dict[str, Any]) -> str:
        """Assess succession risk."""
        title = agent_data.get('title', '').lower()

        if 'ceo' in title or 'president' in title:
            return "high"
        elif 'vp' in title or 'director' in title:
            return "medium"
        elif 'manager' in title or 'lead' in title:
            return "medium"
        else:
            return "low"

    @staticmethod
    def _calculate_performance_rating(agent_data: Dict[str, Any]) -> float:
        """Calculate performance rating."""
        # Base rating
        rating = 7.0

        # Adjust based on role criticality
        title = agent_data.get('title', '').lower()
        if 'ceo' in title or 'chief' in title:
            rating += 1.0
        elif 'vp' in title or 'director' in title:
            rating += 0.5

        # Ensure rating is within bounds
        return max(1.0, min(10.0, rating))


# Factory class for creating data structures
class DataFactory:
    """Factory for creating organization chart data structures."""

    @staticmethod
    def create_enhanced_node(name: str, role: str, department: str, **kwargs) -> EnhancedOrgNode:
        """Create an EnhancedOrgNode."""
        return EnhancedOrgNode(
            name=name,
            role=role,
            department=department,
            **kwargs
        )

    @staticmethod
    def create_department_summary(name: str, agents: List[EnhancedOrgNode]) -> DepartmentSummary:
        """Create a department summary."""
        total_agents = len(agents)
        executive_count = len([a for a in agents if a.tier <= 2])
        specialist_count = len([a for a in agents if a.tier > 2])

        avg_capacity = sum(a.capacity for a in agents) / total_agents if total_agents > 0 else 0
        avg_performance = sum(a.performance_rating for a in agents) / total_agents if total_agents > 0 else 0

        # Count succession risks
        risk_counts: dict[str, int] = {}
        for agent in agents:
            risk = agent.succession_risk
            risk_counts[risk] = risk_counts.get(risk, 0) + 1

        return DepartmentSummary(
            name=name,
            total_agents=total_agents,
            executive_count=executive_count,
            specialist_count=specialist_count,
            avg_capacity=avg_capacity,
            avg_performance=avg_performance,
            critical_skills=[],  # Would be calculated from agents
            succession_risk_count=risk_counts,
            budget_utilization=0.0,  # Would be calculated from budget data
            team_morale=0.0,  # Would be calculated from team metrics
        )

    @staticmethod
    def create_hierarchy_metrics(nodes: List[EnhancedOrgNode]) -> HierarchyMetrics:
        """Create hierarchy metrics from nodes."""
        if not nodes:
            return HierarchyMetrics()

        # Calculate depths
        depths = []
        for node in nodes:
            depth = 0
            current = node
            while current.reports_to and current.reports_to != 'human-ceo':
                # Find parent
                parent = next((n for n in nodes if n.name == current.reports_to), None)
                if parent:
                    depth += 1
                    current = parent

            depths.append(depth)

        # Calculate spans of control
        spans = [node.span_of_control for node in nodes]
        avg_span = sum(spans) / len(spans) if spans else 0

        # Count leaf nodes (nodes without children)
        leaf_nodes = len([n for n in nodes if not n.children])

        # Calculate branching factor
        internal_nodes = len([n for n in nodes if n.children])
        branching_factor = sum(len(n.children) for n in nodes) / internal_nodes if internal_nodes > 0 else 0

        return HierarchyMetrics(
            total_nodes=len(nodes),
            total_edges=len([n for n in nodes if n.reports_to]),
            max_depth=max(depths) if depths else 0,
            avg_depth=sum(depths) / len(depths) if depths else 0,
            breadth=0,  # Would need level analysis
            avg_breadth=0.0,  # Would need level analysis
            avg_span_of_control=avg_span,
            max_span_of_control=max(spans) if spans else 0,
            leaf_nodes=leaf_nodes,
            branching_factor=branching_factor,
        )


# Singleton imports for convenience
EnhancedOrgNode.__doc__ = """
Enhanced organizational node with comprehensive attributes for executive dashboards.

This is the main data model used throughout the organization chart implementation,
providing rich contextual information for phase 3 executive dashboard functionality.
"""
