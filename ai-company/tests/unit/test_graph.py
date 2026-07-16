"""Tests for the Graph engine."""

from __future__ import annotations

import pytest

from ai_company.graph.engine import Graph, GraphEdge, GraphEngine, GraphNode
from ai_company.models import (
    Agent,
    BoardMember,
    Company,
    CompanyRegistry,
    DecisionNode,
    DecisionTreeConfig,
    Department,
    Executive,
    Workflow,
    WorkflowStep,
)


@pytest.fixture()
def registry() -> CompanyRegistry:
    return CompanyRegistry(
        company=Company(id="test", name="Test"),
        executives=[
            Executive(id="ceo", title="CEO", name="CEO", reports_to=""),
            Executive(id="cto", title="CTO", reports_to="ceo"),
            Executive(id="cfo", title="CFO", reports_to="ceo"),
        ],
        departments=[
            Department(id="eng", name="Engineering", executive="cto"),
            Department(id="fin", name="Finance", executive="cfo"),
        ],
        specialists=[
            Agent(id="dev", name="Developer", department="eng", reports_to="cto"),
            Agent(id="analyst", name="Analyst", department="fin", reports_to="cfo"),
        ],
        board=[
            BoardMember(id="dir1", name="Alice", role="Chair"),
        ],
        workflows=[
            Workflow(
                id="hire", name="Hiring", trigger="manual", owner="hr",
                steps=[
                    WorkflowStep(id="post", name="Post Job"),
                    WorkflowStep(id="review", name="Review"),
                    WorkflowStep(id="offer", name="Offer"),
                ],
            ),
        ],
        decision_tree=DecisionTreeConfig(
            nodes=[
                DecisionNode(id="root", question="Approve?", type="branch", children=["yes", "no"]),
                DecisionNode(id="yes", action="approved", type="action"),
                DecisionNode(id="no", action="rejected", type="action"),
            ]
        ),
    )


@pytest.fixture()
def engine(registry: CompanyRegistry) -> GraphEngine:
    return GraphEngine(registry)


# ---------------------------------------------------------------------------
# Low-level graph tests
# ---------------------------------------------------------------------------

class TestGraph:
    def test_add_node(self):
        g = Graph("test")
        g.add_node(GraphNode("a", "A"))
        assert "a" in g.nodes

    def test_add_edge(self):
        g = Graph("test")
        g.add_node(GraphNode("a", "A"))
        g.add_node(GraphNode("b", "B"))
        g.add_edge(GraphEdge("a", "b", "connects"))
        assert len(g.edges) == 1

    def test_get_children(self):
        g = Graph("test")
        g.add_node(GraphNode("a", "A"))
        g.add_node(GraphNode("b", "B"))
        g.add_edge(GraphEdge("a", "b", "parent"))
        children = g.get_children("a")
        assert len(children) == 1
        assert children[0].id == "b"

    def test_get_parents(self):
        g = Graph("test")
        g.add_node(GraphNode("a", "A"))
        g.add_node(GraphNode("b", "B"))
        g.add_edge(GraphEdge("a", "b", "parent"))
        parents = g.get_parents("b")
        assert len(parents) == 1
        assert parents[0].id == "a"

    def test_to_dict(self):
        g = Graph("test")
        g.add_node(GraphNode("a", "A"))
        d = g.to_dict()
        assert d["name"] == "test"
        assert len(d["nodes"]) == 1


# ---------------------------------------------------------------------------
# GraphEngine tests
# ---------------------------------------------------------------------------

class TestGraphEngine:
    def test_build_org_chart(self, engine: GraphEngine):
        graph = engine.build_org_chart()
        assert graph.name == "org_chart"
        assert "ceo" in graph.nodes
        assert "cto" in graph.nodes
        assert "eng" in graph.nodes
        assert "dev" in graph.nodes

    def test_org_chart_edges(self, engine: GraphEngine):
        graph = engine.build_org_chart()
        # cto reports to ceo
        cto_parents = graph.get_parents("cto")
        assert any(p.id == "ceo" for p in cto_parents)

    def test_build_decision_graph(self, engine: GraphEngine):
        graph = engine.build_decision_graph()
        assert "root" in graph.nodes
        assert "yes" in graph.nodes
        assert "no" in graph.nodes

    def test_build_workflow_graph(self, engine: GraphEngine):
        graph = engine.build_workflow_graph()
        assert "hire" in graph.nodes
        assert "hire.post" in graph.nodes
        assert "hire.review" in graph.nodes

    def test_build_knowledge_graph(self, engine: GraphEngine):
        graph = engine.build_knowledge_graph()
        assert "ceo" in graph.nodes
        assert "eng" in graph.nodes

    def test_get_graph_lazy(self, engine: GraphEngine):
        graph = engine.get_graph("org_chart")
        assert graph is not None
        assert len(graph.nodes) > 0

    def test_list_graphs(self, engine: GraphEngine):
        graphs = engine.list_graphs()
        assert len(graphs) == 4
        names = [g["name"] for g in graphs]
        assert "org_chart" in names
        assert "workflow_graph" in names

    def test_find_path(self, engine: GraphEngine):
        path = engine.find_path("org_chart", "ceo", "dev")
        assert path is not None
        assert path[0] == "ceo"
        assert path[-1] == "dev"

    def test_find_path_no_path(self, engine: GraphEngine):
        path = engine.find_path("org_chart", "dev", "ceo")
        # dev doesn't point to ceo (it's the reverse)
        assert path is None
