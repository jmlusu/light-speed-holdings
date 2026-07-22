"""Organization Chart Implementation - Component A
Registry normalization and data processing for organizational hierarchy.

This module handles normalization of agent data from company-registry.yaml,
extracting hierarchical relationships, reporting chains, and span of control.
"""

from __future__ import annotations

import yaml
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field


class Department(BaseModel):
    """Department information with hierarchical context."""

    id: str = Field(..., description="Unique department identifier")
    name: str = Field(..., description="Human-readable department name")
    executive: str = Field(..., description="Executive leading this department")
    type: str = Field(default="department", description="Node type")
    tier: int = Field(default=1, description="Executive tier (1-3)")
    span_of_control: int = Field(default=0, description="Number of direct reports")
    capacity: int = Field(default=0, description="Utilization percentage 0-100")
    critical_skills: List[str] = Field(default_factory=list, description="Critical skills for department")
    succession_risk: str = Field(default="low", description="Succession risk level")
    performance_rating: float = Field(default=5.0, description="Performance rating 1-10")
    last_updated: str = Field(default_factory=datetime.now().isoformat, description="Last update timestamp")


class ReportingChain(BaseModel):
    """Hierarchical relationship and reporting chain information."""

    agent_id: str = Field(..., description="Agent identifier")
    name: str = Field(..., description="Agent name")
    role: str = Field(..., description="Agent role/title")
    department: str = Field(..., description="Department name")
    tier: int = Field(default=1, description="Executive tier")
    parent_id: Optional[str] = Field(default=None, description="Immediate manager/parent")
    children: List[str] = Field(default_factory=list, description="Direct reports")
    depth: int = Field(default=0, description="Hierarchical depth from root")
    critical_skills: List[str] = Field(default_factory=list, description="Agent's critical skills")
    succession_risk: str = Field(default="low", description="Succession risk")
    performance_rating: float = Field(default=5.0, description="Performance rating")
    capacity: int = Field(default=0, description="Utilization percentage")
    last_updated: str = Field(default_factory=datetime.now().isoformat, description="Last update timestamp")


class RegistryNormalizer:
    """Handles normalization of agent registry data with department context.

    This class reads the company-registry.yaml file, applies data cleaning
    and validation rules, and creates unified department and reporting structure.
    """

    def __init__(self, registry_path: Optional[str] = None):
        self.registry_path = registry_path or "company-registry.yaml"
        self.departments: Dict[str, Department] = {}
        self.reporting_chains: Dict[str, ReportingChain] = {}
        self.department_summary: Dict[str, Dict[str, Any]] = {}

    def load_registry(self) -> List[Dict[str, Any]]:
        """Load and parse the company registry YAML file."""
        registry_file = Path(self.registry_path)
        if not registry_file.exists():
            raise FileNotFoundError(f"Registry file not found: {self.registry_path}")

        with open(registry_file, 'r') as f:
            data = yaml.safe_load(f)

        return data.get('company', {}).get('agents', [])

    def extract_department_context(self, registry_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract department context from registry data."""
        departments = {}
        executives_by_dept = {}

        for agent in registry_data:
            agent_id = agent.get('id', '')
            department = agent.get('department', '')
            title = agent.get('title', '')

            # Initialize department record
            if department not in departments:
                departments[department] = {
                    'id': agent_id,
                    'name': department,
                    'executive': agent_id,
                    'direct_reports': [],
                    'specialists': [],
                    'tier': self._calculate_tier(title, agent_id),
                    'type': 'executive' if title.endswith('Officer') or title == 'Chief of Staff' else 'specialist',
                }
                executives_by_dept[department] = agent_id

            dept_record = departments[department]

            # Classify agent based on role and structure
            if agent.get('direct_reports') or agent.get('reports_to') == 'CEO':
                dept_record['direct_reports'].append(agent_id)
            elif agent.get('type') == 'specialist' or 'Lead' in title or 'Engineer' in title or 'Owner' in title:
                dept_record['specialists'].append(agent_id)

        # Calculate span of control and department metrics
        for dept_name, dept_info in departments.items():
            dept_info['span_of_control'] = len(dept_info['direct_reports'])
            dept_info['total_agents'] = len(dept_info['direct_reports']) + len(dept_info['specialists'])
            dept_info['capacity'] = self._calculate_department_capacity(dept_info)

        return {
            'departments': departments,
            'executives_by_dept': executives_by_dept,
        }

    def _calculate_tier(self, title: str, agent_id: str) -> int:
        """Calculate executive tier based on title and role."""
        if title.endswith('Officer') or title == 'Chief of Staff':
            return 1
        elif 'VP' in title or 'Director' in title or 'Lead' in title:
            return 2
        elif 'Owner' in title or 'Engineer' in title or 'Analyst' in title:
            return 3
        return 3

    def _calculate_department_capacity(self, dept_info: Dict[str, Any]) -> int:
        """Calculate department utilization capacity."""
        base_capacity = 70
        span_factor = min(dept_info['span_of_control'] * 5, 30)
        return min(base_capacity + span_factor, 100)

    def build_reporting_chains(self, registry_data: List[Dict[str, Any]],
                              dept_context: Dict[str, Any]) -> List[ReportingChain]:
        """Build hierarchical reporting chains from registry data."""
        reporting_chains = []

        for agent in registry_data:
            agent_id = agent.get('id', '')
            if not agent_id:
                continue

            # Extract hierarchy information
            parent_id = agent.get('reports_to', '')
            if not parent_id:
                # For top-level execs, find their reports_to
                if 'direct_reports' in agent and agent['direct_reports']:
                    # This is an executive with direct reports, skip as parent will be handled elsewhere
                    continue

            # Calculate depth by traversing up the hierarchy
            depth = self._calculate_depth(agent_id, registry_data)

            # Extract critical skills from responsibilities
            responsibilities = agent.get('responsibilities', [])
            critical_skills = self._extract_critical_skills(responsibilities)

            # Determine succession risk based on role criticality
            succession_risk = self._assess_succession_risk(agent)

            # Determine performance rating (simplified logic)
            performance_rating = self._calculate_performance_rating(agent, dept_context)

            chain = ReportingChain(
                agent_id=agent_id,
                name=agent.get('name', agent_id),
                role=agent.get('title', agent.get('name', agent_id)),
                department=agent.get('department', ''),
                tier=self._calculate_tier(agent.get('title', ''), agent_id),
                parent_id=parent_id if parent_id and parent_id != 'CEO' else '',
                children=agent.get('direct_reports', []),
                depth=depth,
                critical_skills=critical_skills,
                succession_risk=succession_risk,
                performance_rating=performance_rating,
                capacity=self._calculate_agent_capacity(agent, dept_context),
                last_updated=datetime.now().isoformat(),
            )

            reporting_chains.append(chain)
            self.reporting_chains[agent_id] = chain

        return reporting_chains

    def _calculate_depth(self, agent_id: str, registry_data: List[Dict[str, Any]]) -> int:
        """Calculate hierarchical depth for an agent."""
        depth = 0
        current = agent_id

        while current:
            agent = next((a for a in registry_data if a.get('id') == current), None)
            if not agent:
                break

            parent = agent.get('reports_to', '')
            if not parent or parent == 'CEO' or not any(a.get('id') == parent for a in registry_data):
                break

            depth += 1
            current = parent

        return depth

    def _extract_critical_skills(self, responsibilities: List[str]) -> List[str]:
        """Extract critical skills from agent responsibilities."""
        critical_skill_keywords = [
            'architect', 'design', 'lead', 'manage', ' oversee',
            'coordinate', 'strategize', 'evaluate', 'audit', 'compliance'
        ]

        skills = []
        for resp in responsibilities:
            if any(keyword in resp.lower() for keyword in critical_skill_keywords):
                # Extract skill from responsibility
                skill_words = resp.lower().split()
                for word in skill_words:
                    if len(word) > 3 and word not in ['the', 'and', 'for', 'from', 'with', 'this', 'that', 'they', 'been']:
                        skills.append(word.capitalize())

        return list(set(skills))[:5]  # Limit to top 5 skills

    def _assess_succession_risk(self, agent: Dict[str, Any]) -> str:
        """Assess succession risk for an agent."""
        role = agent.get('title', '').lower()
        if 'chief' in role or 'president' in role or 'founder' in role:
            return "high"
        elif 'vice president' in role or 'director' in role:
            return "medium"
        elif 'manager' in role or 'lead' in role:
            return "medium"
        return "low"

    def _calculate_performance_rating(self, agent: Dict[str, Any], dept_context: Dict[str, Any]) -> float:
        """Calculate performance rating for an agent."""
        # Base rating on role criticality and department capacity
        title = agent.get('title', '').lower()
        department = agent.get('department', '')

        base_rating = 7.0

        # Adjust based on role criticality
        if 'chief' in title or 'president' in title:
            base_rating += 1.5
        elif 'vice president' in title or 'director' in title:
            base_rating += 1.0
        elif 'manager' in title or 'lead' in title:
            base_rating += 0.5

        # Adjust based on department capacity
        if department in dept_context['departments']:
            dept_capacity = dept_context['departments'][department].get('capacity', 70)
            if dept_capacity > 85:
                base_rating -= 1.0
            elif dept_capacity < 60:
                base_rating += 0.5

        return max(1.0, min(10.0, base_rating))

    def _calculate_agent_capacity(self, agent: Dict[str, Any], dept_context: Dict[str, Any]) -> int:
        """Calculate agent utilization capacity."""
        base_capacity = 60

        title = agent.get('title', '').lower()
        department = agent.get('department', '')

        # Adjust based on role level
        if 'chief' in title or 'president' in title:
            base_capacity = 85
        elif 'vice president' in title or 'director' in title:
            base_capacity = 75
        elif 'manager' in title or 'lead' in title:
            base_capacity = 65

        # Adjust based on department capacity
        if department in dept_context['departments']:
            dept_capacity = dept_context['departments'][department].get('capacity', 70)
            base_capacity = min(base_capacity + (dept_capacity - 70) * 0.2, 100)

        return int(base_capacity)

    def create_unified_structure(self, registry_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create unified department and reporting structure."""
        # Extract department context
        dept_context = self.extract_department_context(registry_data)

        # Build reporting chains
        reporting_chains = self.build_reporting_chains(registry_data, dept_context)

        # Create department records with enriched data
        for dept_name, dept_info in dept_context['departments'].items():
            # Enrich with actual agent data from registry
            dept_agents = [
                agent for agent in registry_data
                if agent.get('department') == dept_name
            ]

            dept_info['agents'] = dept_agents
            dept_info['executive_name'] = next(
                (agent.get('name') for agent in dept_agents if agent.get('id') == dept_info['executive']),
                dept_info['executive']
            )
            dept_info['specialist_count'] = len(dept_info['specialists'])
            dept_info['executive_count'] = len(dept_info['direct_reports'])
            dept_info['succession_risks'] = [
                chain.name for chain in reporting_chains
                if chain.department == dept_name and chain.succession_risk in ['high', 'medium']
            ]
            dept_info['avg_performance'] = self._calculate_dept_avg_performance(
                dept_agents, dept_context
            )

        # Create department objects
        for dept_name, dept_info in dept_context['departments'].items():
            self.departments[dept_name] = Department(**dept_info)

        return {
            'departments': list(self.departments.values()),
            'reporting_chains': reporting_chains,
            'department_summary': self._create_department_summary(),
            'hierarchy_root': self._find_hierarchy_root(reporting_chains),
        }

    def _calculate_dept_avg_performance(self, dept_agents: List[Dict[str, Any]], dept_context: Dict[str, Any]) -> float:
        """Calculate average performance rating for a department."""
        if not dept_agents:
            return 0.0

        # Use the average performance rating calculated during chain building
        scores = []
        for agent in dept_agents:
            agent_id = agent.get('id', '')
            if agent_id in self.reporting_chains:
                scores.append(self.reporting_chains[agent_id].performance_rating)

        return sum(scores) / len(scores) if scores else 5.0

    def _create_department_summary(self) -> Dict[str, Dict[str, Any]]:
        """Create summary statistics for all departments."""
        summary = {}

        for dept_name, dept_info in self.departments.items():
            dept_chains = [
                chain for chain in self.reporting_chains.values()
                if chain.department == dept_name
            ]

            summary[dept_name] = {
                'total_agents': len(dept_chains),
                'executive_count': len([c for c in dept_chains if c.tier == 1]),
                'specialist_count': len([c for c in dept_chains if c.tier > 1]),
                'avg_capacity': sum(c.capacity for c in dept_chains) / len(dept_chains) if dept_chains else 0,
                'avg_performance': sum(c.performance_rating for c in dept_chains) / len(dept_chains) if dept_chains else 0,
                'critical_skills': list(set(skill for c in dept_chains for skill in c.critical_skills)),
                'succession_risk_count': len([c for c in dept_chains if c.succession_risk in ['high', 'medium']]),
            }

        return summary

    def _find_hierarchy_root(self, reporting_chains: List[ReportingChain]) -> str:
        """Find the root of the organization hierarchy."""
        # Find agents with no parent (except human-ceo)
        roots = [
            chain.agent_id for chain in reporting_chains
            if not chain.parent_id or chain.parent_id == ''
        ]

        # The CEO should be the root
        if 'human-ceo' in roots:
            return 'human-ceo'

        # Default to first root found
        return roots[0] if roots else 'unknown'

    def validate_data_consistency(self, unified_structure: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate data consistency and return any errors."""
        errors = []

        # Check for missing departments
        for agent in self.reporting_chains.values():
            if agent.department and agent.department not in self.departments:
                errors.append(f"Agent {agent.agent_id} references unknown department: {agent.department}")

        # Check for orphaned agents (agents without parents that aren't root)
        for agent in self.reporting_chains.values():
            if agent.parent_id and agent.parent_id not in [a.agent_id for a in self.reporting_chains.values()]:
                if agent.parent_id != 'human-ceo' and agent.parent_id != 'CEO':
                    errors.append(f"Agent {agent.agent_id} has invalid parent: {agent.parent_id}")

        # Check for duplicate agent IDs
        agent_ids = [agent.agent_id for agent in self.reporting_chains.values()]
        duplicates = [id for id in agent_ids if agent_ids.count(id) > 1]
        if duplicates:
            errors.append(f"Duplicate agent IDs found: {list(set(duplicates))}")

        return {'errors': errors}

    def normalize(self) -> Dict[str, Any]:
        """Perform complete registry normalization."""
        try:
            registry_data = self.load_registry()
            unified_structure = self.create_unified_structure(registry_data)
            validation = self.validate_data_consistency(unified_structure)

            return {
                'success': True,
                'data': unified_structure,
                'validation': validation,
                'processed_at': datetime.now().isoformat(),
                'agent_count': len(registry_data),
                'department_count': len(self.departments),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'processed_at': datetime.now().isoformat(),
            }


# Convenience function for direct use
def normalize_registry(registry_path: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function to normalize registry data."""
    normalizer = RegistryNormalizer(registry_path)
    return normalizer.normalize()
