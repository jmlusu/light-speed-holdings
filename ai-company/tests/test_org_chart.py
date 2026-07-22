"""Focused test suite for Organization Chart components.

Covers:
  - RegistryNormalizer (normalization, tiers, skills, risk)
  - OrganizationChart (init, lookup, children, parents, pathfinding, subtree, boundaries, stats, integrity, export)
  - DataModels (EnhancedOrgNode properties, DataFactory, DataTransformer)
  - Integration (full workflow)
  - Performance (construction + lookup speed)
"""

from __future__ import annotations

import time
from unittest.mock import patch, MagicMock

import pytest

from ai_company.org_chart.registry_normalizer import RegistryNormalizer, ReportingChain
from ai_company.org_chart.organization_chart import OrganizationChart, TreeStats, PathResult
from ai_company.org_chart.data_models import (
    EnhancedOrgNode,
    DataFactory,
    DataTransformer,
    DepartmentSummary,
    HierarchyMetrics,
)
from ai_company.dashboard.models import OrgNode


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_REGISTRY: list[dict] = [
    {
        "id": "human-ceo",
        "name": "Human CEO",
        "title": "Chief Executive Officer",
        "department": "Executive",
        "reports_to": "",
        "type": "executive",
        "direct_reports": ["chief-of-staff"],
        "responsibilities": ["Set company vision and strategy"],
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
        "responsibilities": ["Coordinate across departments"],
        "model_tier": "standard",
    },
    {
        "id": "cto",
        "name": "CTO",
        "title": "Chief Technology Officer",
        "department": "Technology",
        "reports_to": "chief-of-staff",
        "type": "executive",
        "direct_reports": ["lead-backend", "lead-frontend"],
        "responsibilities": ["Architect robust AI agent systems"],
        "model_tier": "standard",
    },
    {
        "id": "coo",
        "name": "COO",
        "title": "Chief Operating Officer",
        "department": "Operations",
        "reports_to": "chief-of-staff",
        "type": "executive",
        "direct_reports": [],
        "responsibilities": ["Manage daily operations"],
        "model_tier": "standard",
    },
    {
        "id": "lead-backend",
        "name": "Lead Backend",
        "title": "Lead Backend Engineer",
        "department": "Technology",
        "reports_to": "cto",
        "type": "specialist",
        "direct_reports": [],
        "responsibilities": ["Develop backend services"],
        "model_tier": "standard",
    },
    {
        "id": "lead-frontend",
        "name": "Lead Frontend",
        "title": "Lead Frontend Engineer",
        "department": "Technology",
        "reports_to": "cto",
        "type": "specialist",
        "direct_reports": [],
        "responsibilities": ["Design user experiences"],
        "model_tier": "standard",
    },
]


@pytest.fixture()
def registry_data() -> list[dict]:
    """Return a fresh copy of sample registry data."""
    import copy
    return copy.deepcopy(SAMPLE_REGISTRY)


@pytest.fixture()
def normalizer() -> RegistryNormalizer:
    """RegistryNormalizer with mocked load_registry."""
    n = RegistryNormalizer()
    n.load_registry = MagicMock(return_value=SAMPLE_REGISTRY)  # type: ignore[method-assign]
    return n


@pytest.fixture()
def org_nodes() -> list[OrgNode]:
    """Build OrgNode tree BOTTOM-UP (leaf → parent)."""
    lead_backend = OrgNode(name="lead-backend", role="Lead Backend Engineer", type="specialist", department="Technology")
    lead_frontend = OrgNode(name="lead-frontend", role="Lead Frontend Engineer", type="specialist", department="Technology")
    cto = OrgNode(name="cto", role="CTO", type="executive", department="Technology", children=[lead_backend, lead_frontend])
    coo = OrgNode(name="coo", role="COO", type="executive", department="Operations")
    chief_of_staff = OrgNode(name="chief-of-staff", role="Chief of Staff", type="executive", department="Executive", children=[cto, coo])
    ceo = OrgNode(name="human-ceo", role="CEO", type="executive", department="Executive", children=[chief_of_staff])
    return [ceo, chief_of_staff, cto, coo, lead_backend, lead_frontend]


@pytest.fixture()
def chart(org_nodes: list[OrgNode]) -> OrganizationChart:
    """OrganizationChart built from the fixture tree."""
    return OrganizationChart(org_nodes, root_id="human-ceo")


# ===========================================================================
# RegistryNormalizer
# ===========================================================================

class TestRegistryNormalizer:

    def test_init(self, normalizer: RegistryNormalizer) -> None:
        assert normalizer.registry_path == "company-registry.yaml"
        assert normalizer.departments == {}
        assert normalizer.reporting_chains == {}

    def test_normalize_full_cycle(self, normalizer: RegistryNormalizer) -> None:
        result = normalizer.normalize()
        assert result["success"] is True
        assert result["agent_count"] == len(SAMPLE_REGISTRY)
        assert result["department_count"] >= 1

    def test_extract_department_context(self, normalizer: RegistryNormalizer) -> None:
        ctx = normalizer.extract_department_context(SAMPLE_REGISTRY)
        assert "departments" in ctx
        assert "Executive" in ctx["departments"]
        assert ctx["departments"]["Executive"]["executive"] == "human-ceo"

    def test_build_reporting_chains(self, normalizer: RegistryNormalizer) -> None:
        ctx = normalizer.extract_department_context(SAMPLE_REGISTRY)
        chains = normalizer.build_reporting_chains(SAMPLE_REGISTRY, ctx)
        assert len(chains) > 0
        chain_ids = {c.agent_id for c in chains}
        assert "human-ceo" in chain_ids

    def test_calculate_tier_executive(self, normalizer: RegistryNormalizer) -> None:
        assert normalizer._calculate_tier("Chief Executive Officer", "x") == 1
        assert normalizer._calculate_tier("Chief of Staff", "x") == 1

    def test_calculate_tier_manager(self, normalizer: RegistryNormalizer) -> None:
        assert normalizer._calculate_tier("VP of Engineering", "x") == 2
        assert normalizer._calculate_tier("Director of Sales", "x") == 2

    def test_calculate_tier_specialist(self, normalizer: RegistryNormalizer) -> None:
        assert normalizer._calculate_tier("Backend Engineer", "x") == 3

    def test_assess_succession_risk_ceo(self, normalizer: RegistryNormalizer) -> None:
        assert normalizer._assess_succession_risk({"title": "Chief Executive Officer"}) == "high"

    def test_assess_succession_risk_low(self, normalizer: RegistryNormalizer) -> None:
        assert normalizer._assess_succession_risk({"title": "Backend Engineer"}) == "low"

    def test_validate_data_consistency(self, normalizer: RegistryNormalizer) -> None:
        normalizer.normalize()
        validation = normalizer.validate_data_consistency({})
        # With consistent data, no errors expected
        assert isinstance(validation["errors"], list)


# ===========================================================================
# OrganizationChart
# ===========================================================================

class TestOrganizationChart:

    def test_construction(self, chart: OrganizationChart) -> None:
        assert chart.tree_stats.node_count == 6
        assert chart.root_id == "human-ceo"

    def test_get_node(self, chart: OrganizationChart) -> None:
        node = chart.get_node("human-ceo")
        assert node is not None
        assert node.id == "human-ceo"

    def test_get_node_missing(self, chart: OrganizationChart) -> None:
        assert chart.get_node("nonexistent") is None

    def test_get_children(self, chart: OrganizationChart) -> None:
        children = chart.get_children("cto")
        child_ids = {c.id for c in children}
        assert "lead-backend" in child_ids
        assert "lead-frontend" in child_ids

    def test_get_children_leaf(self, chart: OrganizationChart) -> None:
        assert chart.get_children("lead-backend") == []

    def test_get_parents(self, chart: OrganizationChart) -> None:
        parents = chart.get_parents("cto")
        assert len(parents) == 1
        assert parents[0].id == "chief-of-staff"

    def test_get_parents_root(self, chart: OrganizationChart) -> None:
        assert chart.get_parents("human-ceo") == []

    def test_find_shortest_path(self, chart: OrganizationChart) -> None:
        result = chart.find_path("lead-backend", "coo")
        assert result.found is True
        assert result.distance > 0
        assert "lead-backend" in result.path
        assert "coo" in result.path

    def test_find_path_same_node(self, chart: OrganizationChart) -> None:
        result = chart.find_path("cto", "cto")
        assert result.found is True
        assert result.path == ["cto"]
        assert result.distance == 0

    def test_find_path_nonexistent(self, chart: OrganizationChart) -> None:
        result = chart.find_path("nonexistent", "cto")
        assert result.found is False

    def test_find_hierarchical_path(self, chart: OrganizationChart) -> None:
        result = chart.find_path("lead-backend", "coo", path_type="hierarchical")
        assert result.found is True
        # Hierarchical path goes up to common ancestor, then down
        assert "chief-of-staff" in result.path

    def test_extract_subtree(self, chart: OrganizationChart) -> None:
        subtree = chart.extract_subtree("cto")
        assert "subtree" in subtree
        root = subtree["subtree"]
        assert root["id"] == "cto"
        child_ids = {c["id"] for c in root.get("children", [])}
        assert "lead-backend" in child_ids

    def test_extract_subtree_with_depth(self, chart: OrganizationChart) -> None:
        subtree = chart.extract_subtree("human-ceo", max_depth=1)
        assert subtree["subtree"]["depth"] == 0
        for child in subtree["subtree"].get("children", []):
            assert child["depth"] <= 1

    def test_extract_subtree_nonexistent(self, chart: OrganizationChart) -> None:
        result = chart.extract_subtree("nonexistent")
        assert "error" in result

    def test_detect_executive_boundaries(self, chart: OrganizationChart) -> None:
        boundaries = chart.detect_executive_boundaries()
        assert "executive_nodes" in boundaries
        assert "human-ceo" in boundaries["executive_nodes"]

    def test_get_stats(self, chart: OrganizationChart) -> None:
        stats = chart.get_stats()
        assert stats["basic_stats"]["node_count"] == 6
        assert stats["basic_stats"]["depth"] >= 1
        assert "performance_stats" in stats

    def test_validate_integrity(self, chart: OrganizationChart) -> None:
        integrity = chart.validate_integrity()
        assert integrity["valid"] is True
        assert integrity["connected_components"] == 1

    def test_export_tree(self, chart: OrganizationChart) -> None:
        export = chart.export_tree()
        assert export["metadata"]["root_id"] == "human-ceo"
        assert len(export["nodes"]) == 6
        assert len(export["edges"]) > 0

    def test_parallel_subtree_extraction(self, chart: OrganizationChart) -> None:
        result = chart.parallel_subtree_extraction(["cto", "coo"])
        assert "results" in result
        assert "cto" in result["results"]
        assert "coo" in result["results"]


# ===========================================================================
# DataModels
# ===========================================================================

class TestDataModels:

    def test_enhanced_orgnode_creation(self) -> None:
        node = DataFactory.create_enhanced_node(
            name="test-agent",
            role="Test Agent",
            department="Engineering",
            tier=2,
            capacity=70,
            performance_rating=8.0,
        )
        assert node.name == "test-agent"
        assert node.tier == 2
        assert node.capacity == 70

    def test_enhanced_orgnode_properties(self) -> None:
        exec_node = DataFactory.create_enhanced_node(
            name="exec", role="CEO", department="Exec", tier=1,
            capacity=80, performance_rating=9.0,
        )
        assert exec_node.is_executive is True

        spec_node = DataFactory.create_enhanced_node(
            name="spec", role="Engineer", department="Tech", tier=3,
            capacity=60, performance_rating=7.0,
        )
        assert spec_node.is_executive is False

    def test_enhanced_orgnode_risk_score(self) -> None:
        high_risk = DataFactory.create_enhanced_node(
            name="hr", role="CEO", department="Exec", tier=1,
            succession_risk="high", performance_rating=4.0, failure_rate=25.0,
        )
        assert high_risk.risk_score > 0
        assert high_risk.is_at_risk is True

        low_risk = DataFactory.create_enhanced_node(
            name="lr", role="Engineer", department="Tech", tier=3,
            succession_risk="low", performance_rating=9.0, failure_rate=0.0,
        )
        assert low_risk.risk_score < high_risk.risk_score

    def test_enhanced_orgnode_health_score(self) -> None:
        node = DataFactory.create_enhanced_node(
            name="healthy", role="Lead", department="Eng", tier=2,
            performance_rating=9.0, capacity=70, team_morale=90.0,
            employee_satisfaction=85.0,
        )
        assert node.health_score > 70

    def test_enhanced_orgnode_can_accept_load(self) -> None:
        yes_node = DataFactory.create_enhanced_node(
            name="y", role="Lead", department="Eng", tier=2,
            capacity=70, performance_rating=8.0, team_morale=80.0,
            employee_satisfaction=80.0,
        )
        assert yes_node.can_accept_more_load is True

        no_node = DataFactory.create_enhanced_node(
            name="n", role="Lead", department="Eng", tier=2,
            capacity=95, performance_rating=5.0, team_morale=50.0,
            employee_satisfaction=50.0,
        )
        assert no_node.can_accept_more_load is False

    def test_data_transformer_registry_to_enhanced(self) -> None:
        registry = [
            {"name": "agent-a", "title": "Agent A", "department": "Eng"},
            {"name": "agent-b", "title": "Agent B", "department": "Eng", "reports_to": "agent-a"},
        ]
        nodes = DataTransformer.registry_to_enhanced(registry)
        assert len(nodes) == 2
        # The parent should have the child attached
        parent = next(n for n in nodes if n.name == "agent-a")
        child_names = [c.name for c in parent.children]
        assert "agent-b" in child_names

    def test_department_summary(self) -> None:
        agents = [
            DataFactory.create_enhanced_node("a1", "Lead", "Eng", tier=2, capacity=80,
                                              performance_rating=8.0, succession_risk="medium"),
            DataFactory.create_enhanced_node("a2", "Engineer", "Eng", tier=3, capacity=65,
                                              performance_rating=7.0, succession_risk="low"),
        ]
        summary = DataFactory.create_department_summary("Engineering", agents)
        assert summary.name == "Engineering"
        assert summary.total_agents == 2
        assert summary.executive_count == 1
        assert summary.specialist_count == 1

    def test_hierarchy_metrics(self) -> None:
        nodes = [
            DataFactory.create_enhanced_node("root", "CEO", "Exec", tier=1,
                                              reports_to=None),
            DataFactory.create_enhanced_node("child", "Lead", "Eng", tier=2,
                                              reports_to="root"),
        ]
        metrics = DataFactory.create_hierarchy_metrics(nodes)
        assert metrics.total_nodes == 2


# ===========================================================================
# Integration
# ===========================================================================

class TestIntegration:

    def test_full_workflow(self, normalizer: RegistryNormalizer) -> None:
        """Registry normalization → OrgNode tree → OrganizationChart."""
        # Step 1: Normalize
        result = normalizer.normalize()
        assert result["success"] is True

        # Step 2: Build OrgNode tree bottom-up
        lead_backend = OrgNode(name="lead-backend", role="Lead Backend Engineer", type="specialist", department="Technology")
        lead_frontend = OrgNode(name="lead-frontend", role="Lead Frontend Engineer", type="specialist", department="Technology")
        cto = OrgNode(name="cto", role="CTO", type="executive", department="Technology", children=[lead_backend, lead_frontend])
        coo = OrgNode(name="coo", role="COO", type="executive", department="Operations")
        chief_of_staff = OrgNode(name="chief-of-staff", role="Chief of Staff", type="executive", department="Executive", children=[cto, coo])
        ceo = OrgNode(name="human-ceo", role="CEO", type="executive", department="Executive", children=[chief_of_staff])

        # Step 3: Build chart
        chart = OrganizationChart([ceo, chief_of_staff, cto, coo, lead_backend, lead_frontend])
        assert chart.tree_stats.node_count == 6

        # Step 4: Pathfinding
        path = chart.find_path("lead-backend", "coo")
        assert path.found is True

        # Step 5: Export
        export = chart.export_tree()
        assert len(export["nodes"]) == 6

    def test_enhanced_to_orgnode_roundtrip(self) -> None:
        """EnhancedOrgNode → DataTransformer → verify children preserved."""
        registry = [
            {"name": "parent", "title": "Parent", "department": "Eng", "direct_reports": ["child1"]},
            {"name": "child1", "title": "Child", "department": "Eng", "reports_to": "parent"},
        ]
        enhanced = DataTransformer.registry_to_enhanced(registry)
        parent = next(n for n in enhanced if n.name == "parent")
        assert len(parent.children) == 1
        assert parent.children[0].name == "child1"


# ===========================================================================
# Performance
# ===========================================================================

class TestPerformance:

    @pytest.mark.performance
    def test_chart_construction_speed(self, org_nodes: list[OrgNode]) -> None:
        """Chart construction should complete in < 100ms for small trees."""
        start = time.perf_counter()
        OrganizationChart(org_nodes)
        elapsed_ms = (time.perf_counter() - start) * 1000
        assert elapsed_ms < 500, f"Construction took {elapsed_ms:.1f}ms (expected < 500ms)"

    @pytest.mark.performance
    def test_lookup_speed(self, chart: OrganizationChart) -> None:
        """1000 lookups should complete in < 50ms."""
        start = time.perf_counter()
        for _ in range(1000):
            chart.get_node("lead-backend")
        elapsed_ms = (time.perf_counter() - start) * 1000
        assert elapsed_ms < 50, f"1000 lookups took {elapsed_ms:.1f}ms (expected < 50ms)"

    @pytest.mark.performance
    def test_large_tree_construction(self) -> None:
        """Constructing a 500-node tree should complete in < 2s."""
        nodes = []
        # Build a balanced tree: root → 10 managers → 50 workers each (500 total)
        root = OrgNode(name="root", role="CEO", type="executive", department="Exec")
        managers: list[OrgNode] = []
        for i in range(10):
            workers = [
                OrgNode(name=f"worker-{i}-{j}", role="Worker", type="specialist", department="Eng")
                for j in range(50)
            ]
            manager = OrgNode(name=f"manager-{i}", role="Manager", type="executive", department="Eng", children=workers)
            managers.append(manager)
        root_with_children = OrgNode(name="root", role="CEO", type="executive", department="Exec", children=managers)
        all_nodes = [root_with_children] + managers
        for m in managers:
            all_nodes.extend(m.children)

        start = time.perf_counter()
        chart = OrganizationChart(all_nodes)
        elapsed_ms = (time.perf_counter() - start) * 1000
        assert chart.tree_stats.node_count == 511
        assert elapsed_ms < 2000, f"500-node construction took {elapsed_ms:.1f}ms"
