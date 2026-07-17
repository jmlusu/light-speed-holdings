"""Integration tests — memory, graph, scheduler, KPI collector."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml


@pytest.fixture()
def project_base(tmp_path: Path) -> Path:
    """Create a minimal project structure for integration testing."""
    company_dir = tmp_path / "company"
    company_dir.mkdir()

    registry = [
        {
            "id": "test-agent",
            "name": "Test Agent",
            "role": "Test Agent",
            "type": "Specialist",
            "department": "engineering",
            "reportsTo": "lead-engineer",
            "tools": ["python"],
            "permissions": ["read"],
        },
        {
            "id": "lead-engineer",
            "name": "Lead Engineer",
            "role": "Lead Engineer",
            "type": "Executive",
            "department": "engineering",
            "reportsTo": "cto",
            "tools": [],
            "permissions": ["read", "write"],
        },
    ]
    (company_dir / "agent-registry.json").write_text(
        json.dumps(registry, indent=2), encoding="utf-8"
    )

    departments = {
        "departments": [
            {
                "name": "Engineering",
                "executive": "lead-engineer",
                "agents": ["test-agent"],
                "total_agents": 1,
            }
        ]
    }
    (company_dir / "departments.yaml").write_text(
        yaml.dump(departments), encoding="utf-8"
    )

    import shutil
    real_models = Path(__file__).resolve().parents[2] / "company" / "models.yaml"
    if real_models.exists():
        shutil.copy2(str(real_models), str(company_dir / "models.yaml"))

    orchestrator_dir = tmp_path / "orchestrator"
    orchestrator_dir.mkdir()

    opencode_dir = tmp_path / ".opencode"
    opencode_dir.mkdir()
    (opencode_dir / "inbox.json").write_text("[]", encoding="utf-8")

    return tmp_path


class TestMemoryStore:
    """Test memory store CRUD operations."""

    def test_memory_store_and_recall(self, project_base: Path) -> None:
        from ai_company.memory.engine import MemoryStore

        store = MemoryStore(base_dir=str(project_base / "memory"))
        store.store("episodic", "Test memory entry")
        count = store.count("episodic")
        assert count >= 1

    def test_memory_recall_by_query(self, project_base: Path) -> None:
        from ai_company.memory.engine import MemoryStore

        store = MemoryStore(base_dir=str(project_base / "memory"))
        store.store("semantic", "Python is a programming language")
        results = store.recall("semantic", query="Python")
        assert len(results) >= 1

    def test_memory_all_types(self, project_base: Path) -> None:
        from ai_company.memory.engine import MemoryStore

        store = MemoryStore(base_dir=str(project_base / "memory"))
        for mem_type in ["episodic", "semantic", "procedural", "relational", "temporal", "aggregate"]:
            store.store(mem_type, f"Entry for {mem_type}")
        stats = store.stats()
        for mem_type in ["episodic", "semantic", "procedural", "relational", "temporal", "aggregate"]:
            assert stats.get(mem_type, 0) >= 1


class TestGraph:
    """Test Graph class directly."""

    def test_graph_add_nodes_and_edges(self) -> None:
        from ai_company.graph.engine import Graph, GraphEdge, GraphNode

        graph = Graph(name="test-graph")
        graph.add_node(GraphNode(id="ceo", label="CEO", node_type="Executive"))
        graph.add_node(GraphNode(id="cto", label="CTO", node_type="Executive"))
        graph.add_node(GraphNode(id="dev", label="Developer", node_type="Specialist"))
        graph.add_edge(GraphEdge(source="ceo", target="cto", relationship="reports_to"))
        graph.add_edge(GraphEdge(source="cto", target="dev", relationship="reports_to"))

        ceo = graph.get_node("ceo")
        assert ceo is not None
        assert ceo.label == "CEO"

        children = graph.get_children("ceo")
        assert len(children) == 1
        assert children[0].id == "cto"

    def test_graph_to_dict(self) -> None:
        from ai_company.graph.engine import Graph, GraphNode

        graph = Graph(name="test-dict")
        graph.add_node(GraphNode(id="a", label="A"))
        data = graph.to_dict()
        assert "nodes" in data
        assert len(data["nodes"]) == 1


class TestScheduler:
    """Test scheduler add/remove/list cycle."""

    def test_scheduler_full_cycle(self, project_base: Path) -> None:
        from ai_company.orchestrator.scheduler import Scheduler

        scheduler = Scheduler(config_path=str(project_base / "orchestrator" / "scheduler.yaml"))
        task = scheduler.add_task("int-test", "Integration Test Task", interval_minutes=30)
        assert task.id == "int-test"

        tasks = scheduler.list_tasks()
        assert len(tasks) == 1

        assert scheduler.remove_task("int-test") is True
        assert len(scheduler.list_tasks()) == 0


class TestKpiCollector:
    """Test KPI collector with empty data."""

    def test_collect_engineering_kpis(self, project_base: Path) -> None:
        from ai_company.dashboard.kpi_collector import collect_engineering_kpis

        result = collect_engineering_kpis(project_base)
        assert result["department"] == "engineering"
        assert "kpis" in result
        assert "task_completion_rate" in result["kpis"]
        assert result["kpis"]["total_tasks"]["current"] == 0

    def test_collect_all_kpis(self, project_base: Path) -> None:
        from ai_company.dashboard.kpi_collector import collect_all_kpis

        result = collect_all_kpis(project_base)
        assert "departments" in result
        assert "engineering" in result["departments"]

    def test_save_snapshot(self, project_base: Path) -> None:
        from ai_company.dashboard.kpi_collector import collect_all_kpis, save_snapshot

        snapshots = collect_all_kpis(project_base)
        path = save_snapshot(snapshots, output_dir=project_base / "kpi_snapshots")
        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "departments" in data


class TestOrchestratorTick:
    """Test orchestrator tick cycle with minimal data."""

    def test_orchestrator_tick_runs(self, project_base: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(project_base)
        from ai_company.orchestrator.approval import ApprovalGate
        from ai_company.orchestrator.escalation import EscalationManager
        from ai_company.orchestrator.scheduler import Scheduler

        scheduler = Scheduler(config_path=str(project_base / "orchestrator" / "scheduler.yaml"))
        escalation = EscalationManager(config_path=str(project_base / "orchestrator" / "escalation.yaml"))
        gate = ApprovalGate(config_path=str(project_base / "orchestrator" / "approvals.yaml"))

        assert scheduler.get_pending_tasks() == []
        assert escalation.get_pending_escalations() == []
        assert gate.get_pending_requests() == []
