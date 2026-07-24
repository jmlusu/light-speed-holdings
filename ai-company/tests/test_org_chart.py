"""Comprehensive test suite for Organization Chart component.

Tests cover:
1. RegistryNormalizer — normalization, tier calculation, skill extraction, risk assessment
2. OrganizationChart — tree construction, traversal, pathfinding, subtree extraction
3. Data models — EnhancedOrgNode, DepartmentSummary, HierarchyMetrics, DataTransformer, DataFactory
4. Integration — end-to-end workflows from registry through chart to metrics
"""

from __future__ import annotations

import time

import pytest

from ai_company.dashboard.models import OrgNode
from ai_company.org_chart.data_models import (
    DataFactory,
    DataTransformer,
    EnhancedOrgNode,
)
from ai_company.org_chart.organization_chart import OrganizationChart, PathResult
from ai_company.org_chart.registry_normalizer import RegistryNormalizer


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_registry_data() -> list[dict]:
    """Seven-agent hierarchy matching company-registry structure."""
    return [
        {
            "id": "human-ceo",
            "name": "Human CEO",
            "title": "Chief Executive Officer",
            "department": "Executive",
            "reports_to": "",
            "type": "executive",
            "direct_reports": ["chief-of-staff"],
            "responsibilities": [
                "Set company vision and strategy",
                "Make high-stakes decisions",
                "Represent company externally",
            ],
            "model_tier": "premium",
        },
        {
            "id": "chief-of-staff",
            "name": "Chief of Staff",
            "title": "Chief of Staff",
            "department": "Executive",
            "reports_to": "human-ceo",
            "type": "executive",
            "direct_reports": ["cto", "coo"],
            "responsibilities": [
                "Align company goals",
                "Orchestrate agent communication",
                "Monitor operational bottlenecks",
            ],
            "model_tier": "standard",
        },
        {
            "id": "cto",
            "name": "Chief Technology Officer",
            "title": "CTO",
            "department": "Technology",
            "reports_to": "chief-of-staff",
            "type": "executive",
            "direct_reports": ["lead-backend", "lead-frontend"],
            "responsibilities": [
                "Oversee technological infrastructure",
                "Architect AI agent systems",
                "Ensure system scalability",
            ],
            "model_tier": "standard",
        },
        {
            "id": "lead-backend",
            "name": "Lead Backend Engineer",
            "title": "Lead Backend Engineer",
            "department": "Technology",
            "reports_to": "cto",
            "type": "specialist",
            "direct_reports": [],
            "responsibilities": [
                "Develop backend services",
                "Maintain system architecture",
            ],
            "model_tier": "standard",
        },
        {
            "id": "lead-frontend",
            "name": "Lead Frontend Engineer",
            "title": "Lead Frontend Engineer",
            "department": "Technology",
            "reports_to": "cto",
            "type": "specialist",
            "direct_reports": [],
            "responsibilities": [
                "Develop frontend interfaces",
                "Design user experiences",
            ],
            "model_tier": "standard",
        },
        {
            "id": "coo",
            "name": "Chief Operating Officer",
            "title": "COO",
            "department": "Operations",
            "reports_to": "chief-of-staff",
            "type": "executive",
            "direct_reports": ["hr-lead"],
            "responsibilities": [
                "Optimize internal workflows",
                "Manage agent resource allocation",
            ],
            "model_tier": "standard",
        },
        {
            "id": "hr-lead",
            "name": "HR Lead",
            "title": "HR Lead",
            "department": "People",
            "reports_to": "coo",
            "type": "specialist",
            "direct_reports": [],
            "responsibilities": [
                "Manage HR processes",
                "Maintain employee records",
            ],
            "model_tier": "standard",
        },
    ]


@pytest.fixture
def org_nodes() -> list[OrgNode]:
    """Flat list of nested OrgNode objects (children are OrgNode, not strings)."""
    lead-backend = OrgNode(name="lead-backend", role="Lead Backend", type="specialist", department="Technology")
    lead-frontend = OrgNode(name="lead-frontend", role="Lead Frontend", type="specialist", department="Technology")
    cto = OrgNode(
        name="cto", role="CTO", type="executive", department="Technology",
        children=[lead-backend, lead-frontend],
    )
    hr_lead = OrgNode(name="hr-lead", role="HR Lead", type="specialist", department="People")
    coo = OrgNode(name="coo", role="COO", type="executive", department="Operations", children=[hr_lead])
    chief_of_staff = OrgNode(
        name="chief-of-staff", role="Chief of Staff", type="executive", department="Executive",
        children=[cto, coo],
    )
    human_ceo = OrgNode(
        name="human-ceo", role="CEO", type="executive", department="Executive",
        children=[chief_of_staff],
    )
    return [human_ceo, chief_of_staff, cto, lead-backend, lead-frontend, coo, hr_lead]


@pytest.fixture
def chart(org_nodes: list[OrgNode]) -> OrganizationChart:
    return OrganizationChart(org_nodes, root_id="human-ceo")


@pytest.fixture
def enhanced_nodes() -> list[EnhancedOrgNode]:
    """Four EnhancedOrgNode objects with varied tiers and risk profiles."""
    return [
        EnhancedOrgNode(
            name="ceo", role="Chief Executive Officer", department="Executive", tier=1,
            capacity=80, span_of_control=1, critical_skills=["Leadership", "Strategy"],
            succession_risk="low", performance_rating=9.5, agent_type="executive",
            model_tier="premium", active_tasks=5, completed_tasks=45, failure_rate=2.0,
            team_morale=95.0, employee_satisfaction=92.0,
        ),
        EnhancedOrgNode(
            name="cos", role="Chief of Staff", department="Executive", tier=1,
            capacity=75, span_of_control=3, critical_skills=["Coordination"],
            succession_risk="medium", performance_rating=8.5, agent_type="executive",
            model_tier="standard", active_tasks=8, completed_tasks=62, failure_rate=1.5,
            team_morale=88.0, employee_satisfaction=85.0,
        ),
        EnhancedOrgNode(
            name="cto", role="Chief Technology Officer", department="Technology", tier=1,
            capacity=70, span_of_control=2, critical_skills=["Architecture"],
            succession_risk="high", performance_rating=8.0, agent_type="executive",
            model_tier="standard", active_tasks=12, completed_tasks=78, failure_rate=3.0,
            team_morale=75.0, employee_satisfaction=80.0,
        ),
        EnhancedOrgNode(
            name="eng", role="Backend Engineer", department="Technology", tier=3,
            capacity=65, span_of_control=0, critical_skills=[],
            succession_risk="medium", performance_rating=7.5, agent_type="specialist",
            model_tier="standard", active_tasks=6, completed_tasks=34, failure_rate=5.0,
            team_morale=70.0, employee_satisfaction=75.0,
        ),
    ]


@pytest.fixture
def normalizer_with_data(sample_registry_data: list[dict]) -> RegistryNormalizer:
    """RegistryNormalizer with load_registry mocked to avoid disk I/O."""
    normalizer = RegistryNormalizer()
    normalizer.load_registry = lambda: sample_registry_data  # type: ignore[assignment]
    return normalizer


# ===================================================================
# TestRegistryNormalizer
# ===================================================================

class TestRegistryNormalizer:
    """Registry normalization, tier calculation, skill extraction, risk assessment."""

    def test_initialization(self) -> None:
        normalizer = RegistryNormalizer()
        assert normalizer.registry_path == "company-registry.yaml"
        assert normalizer.departments == {}
        assert normalizer.reporting_chains == {}

    def test_initialization_custom_path(self) -> None:
        normalizer = RegistryNormalizer(registry_path="/custom/path.yaml")
        assert normalizer.registry_path == "/custom/path.yaml"

    def test_load_registry_success(self, sample_registry_data: list[dict], tmp_path) -> None:
        import yaml

        registry_file = tmp_path / "company-registry.yaml"
        registry_file.write_text(yaml.dump({"company": {"agents": sample_registry_data}}))

        normalizer = RegistryNormalizer(registry_path=str(registry_file))
        data = normalizer.load_registry()

        assert len(data) == len(sample_registry_data)
        assert data[0]["id"] == "human-ceo"
        assert data[0]["title"] == "Chief Executive Officer"

    def test_load_registry_file_not_found(self) -> None:
        normalizer = RegistryNormalizer(registry_path="/nonexistent/path.yaml")
        with pytest.raises(FileNotFoundError):
            normalizer.load_registry()

    def test_extract_department_context(self, normalizer_with_data: RegistryNormalizer, sample_registry_data: list[dict]) -> None:
        dept_ctx = normalizer_with_data.extract_department_context(sample_registry_data)

        assert "departments" in dept_ctx
        assert "executives_by_dept" in dept_ctx
        assert "Executive" in dept_ctx["departments"]
        assert "Technology" in dept_ctx["departments"]
        assert "Operations" in dept_ctx["departments"]
        assert "People" in dept_ctx["departments"]
        assert len(dept_ctx["departments"]) == 4

    def test_calculate_tier(self) -> None:
        normalizer = RegistryNormalizer()

        assert normalizer._calculate_tier("Chief Executive Officer", "x") == 1
        assert normalizer._calculate_tier("Chief of Staff", "x") == 1
        assert normalizer._calculate_tier("VP Engineering", "x") == 2
        assert normalizer._calculate_tier("Director of Sales", "x") == 2
        assert normalizer._calculate_tier("Lead Engineer", "x") == 2
        assert normalizer._calculate_tier("Engineer", "x") == 3
        assert normalizer._calculate_tier("Analyst", "x") == 3

    def test_extract_critical_skills(self) -> None:
        normalizer = RegistryNormalizer()
        responsibilities = [
            "Architect robust AI agent systems",
            "Develop backend services",
            "Design user experiences",
        ]
        skills = normalizer._extract_critical_skills(responsibilities)

        assert isinstance(skills, list)
        assert len(skills) <= 5
        assert all(isinstance(s, str) for s in skills)
        skill_set = set(skills)
        expected_tokens = {
            "Architect", "Robust", "Agent", "Systems",
            "Design", "User", "Experiences",
        }
        assert skill_set.issubset(expected_tokens)
        assert len(skill_set & expected_tokens) > 0

    def test_extract_critical_skills_empty(self) -> None:
        normalizer = RegistryNormalizer()
        skills = normalizer._extract_critical_skills([])
        assert skills == []

    def test_assess_succession_risk(self) -> None:
        normalizer = RegistryNormalizer()

        assert normalizer._assess_succession_risk({"title": "Chief Executive Officer"}) == "high"
        assert normalizer._assess_succession_risk({"title": "President"}) == "high"
        assert normalizer._assess_succession_risk({"title": "Founder"}) == "high"
        assert normalizer._assess_succession_risk({"title": "Vice President"}) == "high"
        assert normalizer._assess_succession_risk({"title": "Director"}) == "medium"
        assert normalizer._assess_succession_risk({"title": "Manager"}) == "medium"
        assert normalizer._assess_succession_risk({"title": "Lead Engineer"}) == "medium"
        assert normalizer._assess_succession_risk({"title": "Engineer"}) == "low"

    def test_create_unified_structure(self, normalizer_with_data: RegistryNormalizer, sample_registry_data: list[dict]) -> None:
        unified = normalizer_with_data.create_unified_structure(sample_registry_data)

        assert "departments" in unified
        assert "reporting_chains" in unified
        assert "department_summary" in unified
        assert "hierarchy_root" in unified
        assert len(unified["departments"]) > 0
        assert isinstance(unified["reporting_chains"], list)
        assert unified["hierarchy_root"] != ""

    def test_validate_data_consistency(self, normalizer_with_data: RegistryNormalizer, sample_registry_data: list[dict]) -> None:
        normalizer_with_data.create_unified_structure(sample_registry_data)
        validation = normalizer_with_data.validate_data_consistency({})

        assert "errors" in validation
        assert isinstance(validation["errors"], list)

    def test_normalize_end_to_end(self, sample_registry_data: list[dict], tmp_path) -> None:
        import yaml

        registry_file = tmp_path / "company-registry.yaml"
        registry_file.write_text(yaml.dump({"company": {"agents": sample_registry_data}}))

        normalizer = RegistryNormalizer(registry_path=str(registry_file))
        result = normalizer.normalize()

        assert result["success"] is True
        assert "data" in result
        assert result["agent_count"] == len(sample_registry_data)
        assert result["department_count"] > 0
        data = result["data"]
        assert "departments" in data
        assert "reporting_chains" in data
        assert "department_summary" in data


# ===================================================================
# TestOrganizationChart
# ===================================================================

class TestOrganizationChart:
    """Tree construction, traversal, pathfinding, subtree extraction."""

    def test_chart_initialization(self, chart: OrganizationChart) -> None:
        assert chart.root_id == "human-ceo"
        assert len(chart.nodes) == 7

    def test_node_lookup(self, chart: OrganizationChart) -> None:
        node = chart.get_node("human-ceo")
        assert node is not None
        assert node.id == "human-ceo"
        assert node.is_executive is True
        assert node.department == "Executive"

    def test_node_lookup_nonexistent(self, chart: OrganizationChart) -> None:
        node = chart.get_node("nonexistent")
        assert node is None

    def test_children_lookup(self, chart: OrganizationChart) -> None:
        children = chart.get_children("cto")
        assert len(children) == 2
        child_ids = {c.id for c in children}
        assert child_ids == {"lead-backend", "lead-frontend"}

    def test_children_lookup_leaf(self, chart: OrganizationChart) -> None:
        children = chart.get_children("lead-backend")
        assert children == []

    def test_children_lookup_nonexistent(self, chart: OrganizationChart) -> None:
        children = chart.get_children("nonexistent")
        assert children == []

    def test_parents_lookup(self, chart: OrganizationChart) -> None:
        parents = chart.get_parents("lead-backend")
        assert isinstance(parents, list)

    def test_find_shortest_path(self, chart: OrganizationChart) -> None:
        result = chart.find_path("human-ceo", "lead-backend")
        assert result.found is True
        assert result.path is not None
        assert len(result.path) == 4
        assert result.path[0] == "human-ceo"
        assert result.path[-1] == "lead-backend"
        assert result.distance == 3
        assert result.path_type == "shortest"

    def test_find_path_same_node(self, chart: OrganizationChart) -> None:
        result = chart.find_path("cto", "cto")
        assert result.found is True
        assert result.path == ["cto"]
        assert result.distance == 0

    def test_find_path_nonexistent_node(self, chart: OrganizationChart) -> None:
        result = chart.find_path("human-ceo", "nonexistent")
        assert result.found is False

    def test_find_hierarchical_path(self, chart: OrganizationChart) -> None:
        result = chart.find_path("human-ceo", "lead-backend", "hierarchical")
        assert isinstance(result, PathResult)

    def test_find_capacity_path(self, chart: OrganizationChart) -> None:
        result = chart.find_path("human-ceo", "lead-backend", "capacity")
        assert isinstance(result, PathResult)

    def test_find_hierarchical_path_same_node(self, chart: OrganizationChart) -> None:
        result = chart.find_path("cto", "cto", "hierarchical")
        assert result.found is True
        assert result.path == ["cto"]

    def test_find_capacity_path_same_node(self, chart: OrganizationChart) -> None:
        result = chart.find_path("cto", "cto", "capacity")
        assert result.found is True
        assert result.path == ["cto"]

    def test_extract_subtree(self, chart: OrganizationChart) -> None:
        subtree_result = chart.extract_subtree("cto", max_depth=1)

        assert "subtree" in subtree_result
        assert "computation_time_ms" in subtree_result
        assert "metadata" in subtree_result
        subtree = subtree_result["subtree"]
        assert subtree["id"] == "cto"
        assert "children" in subtree
        assert len(subtree["children"]) == 2
        child_ids = {c["id"] for c in subtree["children"]}
        assert child_ids == {"lead-backend", "lead-frontend"}

    def test_extract_subtree_full_depth(self, chart: OrganizationChart) -> None:
        result = chart.extract_subtree("human-ceo")
        subtree = result["subtree"]
        assert subtree["id"] == "human-ceo"
        assert len(subtree["children"]) == 1
        assert subtree["children"][0]["id"] == "chief-of-staff"

    def test_extract_subtree_nonexistent(self, chart: OrganizationChart) -> None:
        result = chart.extract_subtree("nonexistent")
        assert "error" in result

    def test_detect_executive_boundaries(self, chart: OrganizationChart) -> None:
        boundaries = chart.detect_executive_boundaries()

        assert "executive_nodes" in boundaries
        assert "isolation_points" in boundaries
        assert "boundary_crossings" in boundaries
        assert "isolated_departments" in boundaries
        assert "executive_clusters" in boundaries
        exec_set = set(boundaries["executive_nodes"])
        assert {"human-ceo", "chief-of-staff", "cto", "coo"}.issubset(exec_set)
        assert "lead-backend" in boundaries["isolation_points"]
        assert "lead-frontend" in boundaries["isolation_points"]
        assert "hr-lead" in boundaries["isolation_points"]
        assert len(boundaries["boundary_crossings"]) >= 1

    def test_get_stats(self, chart: OrganizationChart) -> None:
        stats = chart.get_stats()

        assert "basic_stats" in stats
        assert "performance_stats" in stats
        assert "structural_stats" in stats
        assert "efficiency_metrics" in stats
        assert stats["basic_stats"]["node_count"] == 7
        assert stats["basic_stats"]["depth"] >= 0
        assert stats["efficiency_metrics"]["lookup_efficiency"] == "O(1)"
        assert stats["efficiency_metrics"]["construction_efficiency"] == "O(n)"

    def test_parallel_subtree_extraction(self, chart: OrganizationChart) -> None:
        root_ids = ["cto", "coo"]
        result = chart.parallel_subtree_extraction(root_ids, max_depth=1)

        assert "results" in result
        assert "parallel_computation_time_ms" in result
        assert "speedup_ratio" in result
        for rid in root_ids:
            assert rid in result["results"]
            assert "subtree" in result["results"][rid]

    def test_validate_integrity(self, chart: OrganizationChart) -> None:
        integrity = chart.validate_integrity()

        assert "valid" in integrity
        assert "issues" in integrity
        assert "connected_components" in integrity
        assert "root_connected" in integrity
        assert integrity["connected_components"] == 1
        assert integrity["root_connected"] is True

    def test_export_tree(self, chart: OrganizationChart) -> None:
        export = chart.export_tree()

        assert "metadata" in export
        assert "nodes" in export
        assert "edges" in export
        assert "stats" in export
        assert export["metadata"]["root_id"] == "human-ceo"
        assert export["metadata"]["total_nodes"] == 7
        assert len(export["nodes"]) == 7
        assert len(export["edges"]) >= 1

    def test_tree_construction_efficiency(self) -> None:
        def _build_binary_tree(depth: int, prefix: str) -> OrgNode:
            if depth == 0:
                return OrgNode(name=prefix, role="Leaf", type="specialist", department="Eng")
            left = _build_binary_tree(depth - 1, f"{prefix}-L")
            right = _build_binary_tree(depth - 1, f"{prefix}-R")
            return OrgNode(name=prefix, role="Manager", type="executive", department="Eng", children=[left, right])

        def _flatten(node: OrgNode) -> list[OrgNode]:
            result = [node]
            for child in node.children:
                result.extend(_flatten(child))
            return result

        root = _build_binary_tree(9, "n")
        all_nodes = _flatten(root)

        start = time.time()
        OrganizationChart(all_nodes, root_id="n")
        elapsed = time.time() - start
        assert elapsed < 1.0


# ===================================================================
# TestDataModels
# ===================================================================

class TestDataModels:
    """EnhancedOrgNode, DepartmentSummary, HierarchyMetrics, DataTransformer, DataFactory."""

    def test_enhanced_orgnode_creation(self, enhanced_nodes: list[EnhancedOrgNode]) -> None:
        assert len(enhanced_nodes) == 4
        ceo = enhanced_nodes[0]
        assert ceo.name == "ceo"
        assert ceo.role == "Chief Executive Officer"
        assert ceo.department == "Executive"
        assert ceo.tier == 1
        assert ceo.performance_rating == 9.5

    def test_enhanced_orgnode_properties(self, enhanced_nodes: list[EnhancedOrgNode]) -> None:
        ceo = enhanced_nodes[0]
        assert ceo.is_executive is True
        assert ceo.has_critical_skills_gaps is False
        assert ceo.utilization_score > 0
        assert ceo.health_score > 0
        assert ceo.can_accept_more_load is True
        assert ceo.needs_support is False

    def test_enhanced_orgnode_risk_assessment(self, enhanced_nodes: list[EnhancedOrgNode]) -> None:
        high_risk = enhanced_nodes[2]  # cto, succession_risk="high"
        assert high_risk.is_at_risk is True
        assert high_risk.risk_score > 0

        low_risk = enhanced_nodes[0]  # ceo, succession_risk="low"
        assert low_risk.is_at_risk is False

    def test_enhanced_orgnode_frozen(self) -> None:
        node = EnhancedOrgNode(name="x", role="Engineer", department="Tech")
        with pytest.raises(Exception):
            node.name = "y"  # type: ignore[misc]

    def test_enhanced_orgnode_skills_gap(self) -> None:
        node_no_skills = EnhancedOrgNode(name="a", role="Engineer", department="Tech", critical_skills=[])
        assert node_no_skills.has_critical_skills_gaps is True

        node_with_skills = EnhancedOrgNode(name="b", role="Engineer", department="Tech", critical_skills=["Python"])
        assert node_with_skills.has_critical_skills_gaps is False

    def test_enhanced_orgnode_needs_support(self) -> None:
        node = EnhancedOrgNode(
            name="overloaded", role="Lead", department="Tech", tier=2,
            capacity=90, performance_rating=6.0, succession_risk="medium",
            team_morale=50.0, employee_satisfaction=45.0,
        )
        assert node.needs_support is True

        comfortable = EnhancedOrgNode(
            name="comfortable", role="Engineer", department="Tech", tier=3,
            capacity=50, performance_rating=8.0, succession_risk="low",
            team_morale=80.0, employee_satisfaction=85.0,
        )
        assert comfortable.needs_support is False

    def test_department_summary_creation(self) -> None:
        exec1 = EnhancedOrgNode(name="exec-1", role="CEO", department="Tech", tier=1, capacity=90, performance_rating=9.0, succession_risk="high")
        spec1 = EnhancedOrgNode(name="spec-1", role="Engineer", department="Tech", tier=3, capacity=65, performance_rating=7.0, succession_risk="low")
        spec2 = EnhancedOrgNode(name="spec-2", role="Engineer", department="Tech", tier=3, capacity=80, performance_rating=8.0, succession_risk="low")

        summary = DataFactory.create_department_summary("Technology", [exec1, spec1, spec2])

        assert summary.name == "Technology"
        assert summary.total_agents == 3
        assert summary.executive_count == 1
        assert summary.specialist_count == 2
        assert summary.avg_capacity == pytest.approx((90 + 65 + 80) / 3)
        assert summary.avg_performance == pytest.approx((9.0 + 7.0 + 8.0) / 3)
        assert summary.succession_risk_count == {"high": 1, "low": 2}

    def test_hierarchy_metrics(self) -> None:
        specialist = EnhancedOrgNode(
            name="specialist", role="Engineer", department="Tech", tier=3,
            reports_to="manager", span_of_control=0,
        )
        manager = EnhancedOrgNode(
            name="manager", role="Manager", department="Tech", tier=2,
            reports_to="root", span_of_control=1, children=[specialist],
        )
        root = EnhancedOrgNode(
            name="root", role="CEO", department="Exec", tier=1,
            span_of_control=2, children=[manager],
        )

        metrics = DataFactory.create_hierarchy_metrics([root, manager, specialist])

        assert metrics.total_nodes == 3
        assert metrics.total_edges == 2
        assert metrics.max_depth == 2
        assert metrics.avg_span_of_control == pytest.approx(1.0)
        assert metrics.max_span_of_control == 2
        assert metrics.leaf_nodes == 1

    def test_hierarchy_metrics_empty(self) -> None:
        metrics = DataFactory.create_hierarchy_metrics([])
        assert metrics.total_nodes == 0

    def test_data_transformer_calculate_tier(self) -> None:
        assert DataTransformer._calculate_tier({"title": "CEO"}) == 1
        assert DataTransformer._calculate_tier({"title": "Chief Technology Officer"}) == 1
        assert DataTransformer._calculate_tier({"title": "President"}) == 1
        assert DataTransformer._calculate_tier({"title": "VP Engineering"}) == 2
        assert DataTransformer._calculate_tier({"title": "Director of Sales"}) == 2
        assert DataTransformer._calculate_tier({"title": "Lead Engineer"}) == 2
        assert DataTransformer._calculate_tier({"title": "Manager"}) == 2
        assert DataTransformer._calculate_tier({"title": "Software Engineer"}) == 3

    def test_data_transformer_calculate_capacity(self) -> None:
        assert DataTransformer._calculate_capacity({"title": "CEO"}) == 85
        assert DataTransformer._calculate_capacity({"title": "VP Sales"}) == 75
        assert DataTransformer._calculate_capacity({"title": "Manager"}) == 65
        assert DataTransformer._calculate_capacity({"title": "Engineer"}) == 60

    def test_data_transformer_span_of_control(self) -> None:
        assert DataTransformer._calculate_span_of_control({"direct_reports": ["a", "b", "c"]}) == 3
        assert DataTransformer._calculate_span_of_control({}) == 0

    def test_data_transformer_extract_critical_skills(self) -> None:
        skills = DataTransformer._extract_critical_skills({"title": "Lead Engineer"})
        assert "Team Leadership" in skills
        assert "Project Management" in skills
        assert "Software Development" in skills

        skills_ceo = DataTransformer._extract_critical_skills({"title": "CEO"})
        assert len(skills_ceo) == 0  # 'ceo' doesn't match any keyword patterns

    def test_data_transformer_assess_succession_risk(self) -> None:
        assert DataTransformer._assess_succession_risk({"title": "CEO"}) == "high"
        assert DataTransformer._assess_succession_risk({"title": "President"}) == "high"
        assert DataTransformer._assess_succession_risk({"title": "VP Engineering"}) == "medium"
        assert DataTransformer._assess_succession_risk({"title": "Manager"}) == "medium"
        assert DataTransformer._assess_succession_risk({"title": "Engineer"}) == "low"

    def test_data_transformer_performance_rating(self) -> None:
        assert DataTransformer._calculate_performance_rating({"title": "CEO"}) == 8.0
        assert DataTransformer._calculate_performance_rating({"title": "VP"}) == 7.5
        assert DataTransformer._calculate_performance_rating({"title": "Engineer"}) == 7.0

    def test_data_transformer_orgnode_to_enhanced(self) -> None:
        source = EnhancedOrgNode(
            name="src", role="Engineer", department="Tech", tier=2,
            capacity=75, critical_skills=["Python"], performance_rating=8.0,
        )
        result = DataTransformer.orgnode_to_enhanced(source)
        assert result.name == "src"
        assert result.role == "Engineer"
        assert result.tier == 2
        assert result.capacity == 75
        assert result.critical_skills == ["Python"]
        assert result.performance_rating == 8.0

    def test_data_factory_create_enhanced_node(self) -> None:
        node = DataFactory.create_enhanced_node("test-agent", "Engineer", "Tech", tier=2, capacity=60)
        assert isinstance(node, EnhancedOrgNode)
        assert node.name == "test-agent"
        assert node.role == "Engineer"
        assert node.department == "Tech"
        assert node.tier == 2
        assert node.capacity == 60


# ===================================================================
# TestIntegration
# ===================================================================

class TestIntegration:
    """End-to-end workflows and cross-component integration."""

    def test_registry_normalizer_integration(
        self, sample_registry_data: list[dict], tmp_path
    ) -> None:
        import yaml

        registry_file = tmp_path / "company-registry.yaml"
        registry_file.write_text(yaml.dump({"company": {"agents": sample_registry_data}}))

        normalizer = RegistryNormalizer(registry_path=str(registry_file))
        result = normalizer.normalize()

        assert result["success"] is True
        assert result["agent_count"] == len(sample_registry_data)
        assert result["department_count"] >= 3

        data = result["data"]
        assert "departments" in data
        assert "reporting_chains" in data
        assert "department_summary" in data

        summary = data["department_summary"]
        for dept_name in summary:
            assert "total_agents" in summary[dept_name]
            assert "executive_count" in summary[dept_name]

    def test_organization_chart_integration(self, org_nodes: list[OrgNode]) -> None:
        chart = OrganizationChart(org_nodes, root_id="human-ceo")

        result = chart.find_path("human-ceo", "hr-lead")
        assert result.found is True

        subtree = chart.extract_subtree("cto", max_depth=2)
        assert subtree["subtree"]["id"] == "cto"

        boundaries = chart.detect_executive_boundaries()
        assert "executive_nodes" in boundaries
        assert "isolation_points" in boundaries

    def test_complete_workflow(
        self, sample_registry_data: list[dict], org_nodes: list[OrgNode], tmp_path
    ) -> None:
        import yaml

        registry_file = tmp_path / "company-registry.yaml"
        registry_file.write_text(yaml.dump({"company": {"agents": sample_registry_data}}))

        normalizer = RegistryNormalizer(registry_path=str(registry_file))
        normalized = normalizer.normalize()
        assert normalized["success"] is True

        chart = OrganizationChart(org_nodes, root_id="human-ceo")

        start = time.time()
        path_result = chart.find_path("human-ceo", "hr-lead")
        query_ms = (time.time() - start) * 1000
        assert query_ms < 100
        assert path_result.found is True

        start = time.time()
        subtree = chart.extract_subtree("cto", max_depth=1)
        extract_ms = (time.time() - start) * 1000
        assert extract_ms < 100
        assert "subtree" in subtree

        tree_stats = chart.get_stats()
        assert tree_stats["performance_stats"]["lookup_time_ms"] < 10


@pytest.mark.performance
def test_performance_requirements() -> None:
    """Validate O(n) construction and O(1) lookup for a large organization."""

    def _build_binary_tree(depth: int, prefix: str) -> OrgNode:
        if depth == 0:
            return OrgNode(name=prefix, role="Leaf", type="specialist", department="Eng")
        left = _build_binary_tree(depth - 1, f"{prefix}-L")
        right = _build_binary_tree(depth - 1, f"{prefix}-R")
        return OrgNode(
            name=prefix, role="Manager", type="executive", department="Eng",
            children=[left, right],
        )

    def _flatten(node: OrgNode) -> list[OrgNode]:
        result = [node]
        for child in node.children:
            result.extend(_flatten(child))
        return result

    root = _build_binary_tree(9, "n")
    all_nodes = _flatten(root)

    start = time.time()
    chart = OrganizationChart(all_nodes, root_id="n")
    construction_ms = (time.time() - start) * 1000

    start = time.time()
    for i in range(100):
        node = chart.get_node("n")
        assert node is not None
    lookup_ms = (time.time() - start) * 1000 / 100

    start = time.time()
    for i in range(10):
        leaf_name = "n"
        for _ in range(9):
            leaf_name += "-R"
        result = chart.find_path("n", leaf_name)
        assert result.found is True
    pathfinding_ms = (time.time() - start) * 1000 / 10

    assert construction_ms < 1000
    assert lookup_ms < 10
    assert pathfinding_ms < 50
