"""Graph engine — manages organizational and knowledge graphs.

Graph types:
1. OrgChart — organizational hierarchy (who reports to whom)
2. DecisionGraph — decision dependencies (what depends on what)
3. WorkflowGraph — workflow step dependencies (what feeds into what)
4. KnowledgeGraph — knowledge entity relationships (who knows what)
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ai_company.models import CompanyRegistry


class GraphNode:
    """A node in a graph."""

    def __init__(self, id: str, label: str, node_type: str = "", **attrs: Any) -> None:
        self.id = id
        self.label = label
        self.node_type = node_type
        self.attrs = attrs

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "label": self.label, "type": self.node_type, **self.attrs}


class GraphEdge:
    """An edge in a graph."""

    def __init__(self, source: str, target: str, relationship: str = "", **attrs: Any) -> None:
        self.source = source
        self.target = target
        self.relationship = relationship
        self.attrs = attrs

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "relationship": self.relationship,
            **self.attrs,
        }


class Graph:
    """A simple directed graph."""

    def __init__(self, name: str = "") -> None:
        self.name = name
        self.nodes: dict[str, GraphNode] = {}
        self.edges: list[GraphEdge] = []

    def add_node(self, node: GraphNode) -> None:
        self.nodes[node.id] = node

    def add_edge(self, edge: GraphEdge) -> None:
        self.edges.append(edge)

    def get_node(self, node_id: str) -> GraphNode | None:
        return self.nodes.get(node_id)

    def get_children(self, node_id: str) -> list[GraphNode]:
        """Get all nodes that this node points to."""
        child_ids = [e.target for e in self.edges if e.source == node_id]
        return [self.nodes[cid] for cid in child_ids if cid in self.nodes]

    def get_parents(self, node_id: str) -> list[GraphNode]:
        """Get all nodes that point to this node."""
        parent_ids = [e.source for e in self.edges if e.target == node_id]
        return [self.nodes[pid] for pid in parent_ids if pid in self.nodes]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
        }


class GraphEngine:
    """Builds and manages company graphs from a CompanyRegistry."""

    def __init__(self, registry: CompanyRegistry) -> None:
        self.registry = registry
        self._graphs: dict[str, Graph] = {}

    def build_org_chart(self) -> Graph:
        """Build the organizational hierarchy graph."""
        graph = Graph(name="org_chart")

        # Add CEO node
        ceo = next(
            (
                e
                for e in self.registry.executives
                if e.reports_to in ("", "board", "board_of_directors")
            ),
            None,
        )
        if ceo:
            graph.add_node(GraphNode(ceo.id, ceo.name or ceo.title, "executive", title=ceo.title))

        # Add all other executives
        for ex in self.registry.executives:
            graph.add_node(GraphNode(ex.id, ex.name or ex.title, "executive", title=ex.title))
            if ex.reports_to:
                graph.add_edge(GraphEdge(ex.reports_to, ex.id, "reports_to"))

        # Add departments with executive links
        for dept in self.registry.departments:
            graph.add_node(GraphNode(dept.id, dept.name, "department"))
            if dept.executive:
                graph.add_edge(GraphEdge(dept.executive, dept.id, "leads"))

        # Add specialists
        for spec in self.registry.specialists:
            graph.add_node(
                GraphNode(spec.id, spec.name or spec.id, "specialist", department=spec.department)
            )
            if spec.reports_to:
                graph.add_edge(GraphEdge(spec.reports_to, spec.id, "manages"))

        self._graphs["org_chart"] = graph
        return graph

    def build_decision_graph(self) -> Graph:
        """Build the decision dependency graph."""
        graph = Graph(name="decision_graph")

        for node in self.registry.decision_tree.nodes:
            graph.add_node(GraphNode(node.id, node.question or node.action, node.type))
            for child_id in node.children:
                graph.add_edge(GraphEdge(node.id, child_id, "leads_to"))

        self._graphs["decision_graph"] = graph
        return graph

    def build_workflow_graph(self) -> Graph:
        """Build the workflow step dependency graph."""
        graph = Graph(name="workflow_graph")

        for wf in self.registry.workflows:
            graph.add_node(GraphNode(wf.id, wf.name, "workflow"))
            prev_id: str | None = None
            for step in wf.steps:
                step_id = f"{wf.id}.{step.id}"
                graph.add_node(GraphNode(step_id, step.name, "step", workflow=wf.id))
                graph.add_edge(GraphEdge(wf.id, step_id, "contains"))
                if prev_id:
                    graph.add_edge(GraphEdge(prev_id, step_id, "next"))
                prev_id = step_id

        self._graphs["workflow_graph"] = graph
        return graph

    def build_knowledge_graph(self) -> Graph:
        """Build the knowledge entity relationship graph."""
        graph = Graph(name="knowledge_graph")

        # Link executives to their departments
        for ex in self.registry.executives:
            graph.add_node(GraphNode(ex.id, ex.name or ex.title, "person"))
        for dept in self.registry.departments:
            graph.add_node(GraphNode(dept.id, dept.name, "department"))
            if dept.executive:
                graph.add_edge(GraphEdge(dept.executive, dept.id, "oversees"))

        # Link specialists to departments
        for spec in self.registry.specialists:
            graph.add_node(GraphNode(spec.id, spec.name or spec.id, "agent"))
            if spec.department:
                graph.add_edge(GraphEdge(spec.department, spec.id, "contains"))

        # Link board members
        for bm in self.registry.board:
            graph.add_node(GraphNode(bm.id, bm.name or bm.role, "board_member", role=bm.role))

        self._graphs["knowledge_graph"] = graph
        return graph

    def get_graph(self, name: str) -> Graph | None:
        """Get a named graph, building it if necessary."""
        if name not in self._graphs:
            builders = {
                "org_chart": self.build_org_chart,
                "decision_graph": self.build_decision_graph,
                "workflow_graph": self.build_workflow_graph,
                "knowledge_graph": self.build_knowledge_graph,
            }
            builder = builders.get(name)
            if builder:
                builder()
        return self._graphs.get(name)

    def list_graphs(self) -> list[dict[str, Any]]:
        """List all available graphs with their sizes."""
        self._ensure_all_built()
        return [
            {"name": g.name, "nodes": len(g.nodes), "edges": len(g.edges)}
            for g in self._graphs.values()
        ]

    def _ensure_all_built(self) -> None:
        """Build all graphs if not already built."""
        for name in ("org_chart", "decision_graph", "workflow_graph", "knowledge_graph"):
            if name not in self._graphs:
                self.get_graph(name)

    def find_path(self, graph_name: str, start_id: str, end_id: str) -> list[str] | None:
        """Find a path between two nodes in a graph using BFS."""
        graph = self.get_graph(graph_name)
        if graph is None:
            return None

        from collections import deque

        visited: set[str] = set()
        queue: deque[list[str]] = deque([[start_id]])

        while queue:
            path = queue.popleft()
            current = path[-1]

            if current == end_id:
                return path

            if current in visited:
                continue
            visited.add(current)

            for child in graph.get_children(current):
                if child.id not in visited:
                    queue.append(path + [child.id])

        return None


def compute_org_metrics(
    agents: list[dict[str, Any]],
    tasks: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Compute per-agent live metrics + succession risk for an org chart.

    Pure function over plain dicts so it is unit-testable without I/O.  *agents*
    are registry entries keyed by ``name``; *tasks* are live task dicts from the
    shared MessageBus (SQLite-first read).  Returns a mapping of ``name`` to
    ``{"metrics": {...}, "risk": {...}}`` (see :data:`_safe_node_metrics` /
    :data:`_safe_node_risk`).  Names absent from *tasks* still get a zeroed
    metrics block so the frontend can always render a capacity bar.
    """
    children_map: dict[str, list[str]] = {}
    for a in agents:
        parent = a.get("reports_to", "")
        if parent:
            children_map.setdefault(parent, []).append(str(a.get("name", "")))

    per_name: dict[str, dict[str, Any]] = {str(a.get("name", "")): a for a in agents}

    by_agent: dict[str, list[dict[str, Any]]] = {name: [] for name in per_name}
    for task in tasks:
        if not isinstance(task, dict):
            continue
        sender = task.get("sender_id")
        receiver = task.get("receiver_id")
        if sender in by_agent:
            by_agent[sender].append(task)
        if receiver in by_agent and receiver != sender:
            by_agent[receiver].append(task)

    result: dict[str, dict[str, Any]] = {}
    now = datetime.now(timezone.utc)
    for name, agent in per_name.items():
        agent_tasks = by_agent.get(name, [])
        result[name] = {
            "metrics": _safe_node_metrics(agent_tasks, now),
            "risk": _safe_node_risk(agent, children_map.get(name, []), per_name),
        }
    return result


def _safe_node_metrics(tasks: list[dict[str, Any]], now: datetime) -> dict[str, Any]:
    """Compute capacity/activity for one agent's task list (never raises)."""
    active = sum(1 for t in tasks if t.get("status") == "in_progress")
    queued = sum(1 for t in tasks if t.get("status") == "pending")
    completed = sum(1 for t in tasks if t.get("status") == "completed")
    capacity = round(active / (active + queued) * 100, 1) if (active + queued) else 0.0

    # Utilization trend: completed count in the last 7 days vs the prior 7.
    recent_7 = 0
    prior_7 = 0
    for t in tasks:
        if t.get("status") != "completed":
            continue
        created = _parse_ts(t.get("created_at"))
        if created is None:
            continue
        age_days = (now - created).total_seconds() / 86400.0
        if 0 <= age_days <= 7:
            recent_7 += 1
        elif 7 < age_days <= 14:
            prior_7 += 1
    if recent_7 == prior_7:
        trend = "stable" if (recent_7 > 0 or prior_7 > 0) else None
    else:
        trend = "up" if recent_7 > prior_7 else "down"

    return {
        "active": active,
        "queued": queued,
        "completed": completed,
        "capacity": capacity,
        "utilization_trend": trend,
    }


def _safe_node_risk(
    agent: dict[str, Any],
    direct_reports: list[str],
    per_name: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Derive succession/bus-factor risk for one agent (never raises)."""
    skills = agent.get("skills") or agent.get("skillset") or []
    if isinstance(skills, str):
        try:
            skills = [s.strip() for s in skills.split(",") if s.strip()]
        except ValueError:  # pragma: no cover - defensive
            skills = []
    unique_skills = len({str(s) for s in skills if s}) if isinstance(skills, list) else 0

    tenure_days: float | None = None
    since = agent.get("since") or agent.get("created_at")
    started = _parse_ts(since) if since else None
    if started is not None:
        tenure_days = (datetime.now(timezone.utc) - started).total_seconds() / 86400.0
    tenure_label = _tenure_label(tenure_days)

    num_reports = len(direct_reports)
    risk = "high"
    if num_reports >= 3 and unique_skills >= 3 and tenure_days is not None and tenure_days >= 365:
        risk = "low"
    elif num_reports >= 2 and unique_skills >= 2:
        risk = "medium"

    return {
        "succession_risk": risk,
        "direct_reports": num_reports,
        "bus_factor": num_reports,
        "unique_skills": unique_skills,
        "tenure": tenure_label,
        "last_review": agent.get("last_review"),
    }


def _tenure_label(tenure_days: float | None) -> str:
    if tenure_days is None:
        return "unknown"
    if tenure_days >= 365:
        return "senior"
    if tenure_days >= 90:
        return "established"
    return "recent"


def _parse_ts(value: Any) -> datetime | None:
    """Best-effort parse of an ISO-ish timestamp to a tz-aware datetime."""
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value))
    except (ValueError, TypeError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def org_chart_summary(
    agents: list[dict[str, Any]],
    metrics: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Summarize an org chart: totals + average span of control.

    ``metrics`` is the output of :func:`compute_org_metrics`.  Agents whose
    ``reports_to`` matches no one are counted as executives when their type is
    ``executive``; every agent with a manager counts toward span of control.
    """
    total = len(agents)
    executives = sum(1 for a in agents if str(a.get("type", "")).lower() == "executive")
    specialists = sum(1 for a in agents if str(a.get("type", "")).lower() == "specialist")

    children_map: dict[str, list[str]] = {}
    for a in agents:
        parent = a.get("reports_to", "")
        if parent:
            children_map.setdefault(parent, []).append(str(a.get("name", "")))

    spans = [len(children_map.get(str(a.get("name", "")), [])) for a in agents]
    avg_span = round(sum(spans) / total, 2) if total else 0.0

    avg_capacity = 0.0
    capacities = [
        m.get("metrics", {}).get("capacity")
        for m in metrics.values()
        if isinstance(m.get("metrics"), dict)
    ]
    usable = [c for c in capacities if isinstance(c, (int, float))]
    if usable:
        avg_capacity = round(sum(usable) / len(usable), 1)

    at_risk = sum(
        1
        for m in metrics.values()
        if isinstance(m.get("risk"), dict) and m.get("risk", {}).get("succession_risk") == "high"
    )
    return {
        "total_agents": total,
        "executives": executives,
        "specialists": specialists,
        "avg_span_of_control": avg_span,
        "avg_capacity": avg_capacity,
        "at_risk_count": at_risk,
    }
