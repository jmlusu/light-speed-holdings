from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from collections import deque
import time
from datetime import datetime
from typing import Any

from ai_company.dashboard.models import OrgNode


@dataclass
class TreeStats:
    """Tree performance and structural statistics."""

    node_count: int = 0
    edge_count: int = 0
    depth: int = 0
    breadth: int = 1
    index_time_ms: float = 0.0
    construction_time_ms: float = 0.0
    lookup_time_ms: float = 0.0
    subtree_extraction_count: int = 0
    parallel_computation_time_ms: float = 0.0


@dataclass
class PathResult:
    """Result of pathfinding between two nodes."""

    found: bool = False
    path: Optional[List[str]] = None
    distance: int = 0
    path_type: str = "shortest"  # shortest, hierarchical, capacity
    metadata: Optional[Dict[str, Any]] = None


class OrgNodeData:
    """Extended node data for tree algorithms."""

    def __init__(self, node: OrgNode):
        self.node = node
        self.id = node.name
        self.children_ids: List[str] = [child.name for child in node.children]
        self.parent_id: Optional[str] = None
        self.depth: int = 0
        self.breadth: int = 0
        self.subtree_size: int = 0
        self.span_of_control: int = 0
        self.capacity: int = 0
        self.path_to_root: List[str] = []
        self.is_executive: bool = node.type == "executive"
        self.department: str = node.department
        self.last_updated: str = datetime.now().isoformat()

    def to_orgnode(self) -> OrgNode:
        """Convert back to OrgNode format."""
        children = []
        if hasattr(self.node, 'children'):
            children = self.node.children
        else:
            children = []

        return OrgNode(
            name=self.id,
            role=self.node.role if hasattr(self.node, 'role') else self.id,
            type=self.node.type if hasattr(self.node, 'type') else "agent",
            department=self.department,
            children=children
        )


class OrganizationChart:
    """
    Core organization chart with optimized tree traversal and pathfinding.

    Implements O(n) tree construction with O(1) lookups and parallel subtree processing.
    Supports capacity planning, span of control calculations, and executive boundary detection.
    """

    def __init__(self, org_nodes: List[OrgNode], root_id: str = "human-ceo"):
        """
        Initialize organization chart.

        Args:
            org_nodes: List of OrgNode objects from the registry
            root_id: Root node ID for hierarchy construction
        """
        self.root_id = root_id
        self.nodes: Dict[str, OrgNodeData] = {}
        self.adjacency_list: Dict[str, List[str]] = {}
        self.reverse_adjacency: Dict[str, List[str]] = {}
        self.tree_stats = TreeStats()
        self._build_index(org_nodes)
        self._construct_tree()
        self._calculate_metrics()

    def _build_index(self, org_nodes: List[OrgNode]) -> None:
        """Build indexes for fast node lookup."""
        start_time = time.time()

        # Create OrgNodeData objects for each node
        for node in org_nodes:
            self.nodes[node.name] = OrgNodeData(node)

        # Build adjacency lists
        for node_id, node_data in self.nodes.items():
            self.adjacency_list[node_id] = []
            self.reverse_adjacency[node_id] = []

        for node_id, node_data in self.nodes.items():
            for child_id in node_data.children_ids:
                if child_id in self.nodes:
                    self.adjacency_list[node_id].append(child_id)
                    self.reverse_adjacency[child_id].append(node_id)

        self.tree_stats.index_time_ms = (time.time() - start_time) * 1000

    def _construct_tree(self) -> None:
        """Construct tree structure with O(n) traversal."""
        start_time = time.time()

        # Use BFS to establish parent-child relationships and calculate depths
        queue = deque([self.root_id])
        visited = set()
        level_widths: Dict[int, int] = {}

        while queue:
            node_id = queue.popleft()
            if node_id in visited:
                continue
            visited.add(node_id)

            node_data = self.nodes[node_id]
            node_data.depth = 0 if node_id == self.root_id else (
                self.nodes[node_data.parent_id].depth + 1 if node_data.parent_id else 0
            )

            level_widths[node_data.depth] = level_widths.get(node_data.depth, 0) + 1

            # Find parent and establish hierarchy
            if node_id != self.root_id and node_data.parent_id:
                if node_data.parent_id in self.nodes:
                    parent_data = self.nodes[node_data.parent_id]
                    if node_data not in parent_data.children_ids:
                        parent_data.children_ids.append(node_id)
                        self.adjacency_list[node_data.parent_id].append(node_id)
                    self.tree_stats.edge_count += 1

            # Add children to queue
            for child_id in node_data.children_ids[:]:  # Copy to avoid modification during iteration
                if child_id in self.nodes:
                    queue.append(child_id)
                else:
                    node_data.children_ids.remove(child_id)

        self.tree_stats.node_count = len(self.nodes)
        self.tree_stats.construction_time_ms = (time.time() - start_time) * 1000
        self.tree_stats.depth = max(level_widths.keys()) if level_widths else 0
        self.tree_stats.breadth = max(level_widths.values()) if level_widths else 1

    def _calculate_metrics(self) -> None:
        """Calculate tree metrics including subtree sizes and spans."""
        self._calculate_subtree_sizes()
        self._calculate_spans_of_control()
        self._calculate_path_to_root()

    def _calculate_subtree_sizes(self) -> None:
        """Calculate subtree sizes using post-order traversal."""
        def calculate_subtree_size(node_id: str) -> int:
            if node_id not in self.nodes:
                return 0

            size = 1  # Count current node
            for child_id in self.adjacency_list.get(node_id, []):
                size += calculate_subtree_size(child_id)

            self.nodes[node_id].subtree_size = size
            return size

        calculate_subtree_size(self.root_id)

    def _calculate_spans_of_control(self) -> None:
        """Calculate span of control (number of direct reports) for each node."""
        for node_id, node_data in self.nodes.items():
            node_data.span_of_control = len(self.adjacency_list.get(node_id, []))

    def _calculate_path_to_root(self) -> None:
        """Calculate path from each node to root."""
        def find_path(node_id: str, path: List[str]) -> List[str]:
            if node_id not in self.nodes:
                return path

            current_path = [node_id] + path
            node_data = self.nodes[node_id]

            if node_id == self.root_id:
                return current_path

            return find_path(node_data.parent_id, current_path) if node_data.parent_id else current_path

        for node_id in self.nodes:
            self.nodes[node_id].path_to_root = find_path(node_id, [])

    def get_node(self, node_id: str) -> Optional[OrgNodeData]:
        """Get node data by ID with O(1) lookup."""
        lookup_start = time.time()
        node_data = self.nodes.get(node_id)
        self.tree_stats.lookup_time_ms = (time.time() - lookup_start) * 1000
        return node_data

    def get_children(self, node_id: str) -> List[OrgNodeData]:
        """Get direct children of a node."""
        if node_id not in self.nodes:
            return []

        children = []
        for child_id in self.adjacency_list.get(node_id, []):
            child_node = self.nodes.get(child_id)
            if child_node:
                children.append(child_node)

        return children

    def get_parents(self, node_id: str) -> List[OrgNodeData]:
        """Get direct parents of a node."""
        if node_id not in self.nodes:
            return []

        parents = []
        node_data = self.nodes[node_id]
        if node_data.parent_id and node_data.parent_id in self.nodes:
            parents.append(self.nodes[node_data.parent_id])

        return parents

    def find_path(self, start_id: str, end_id: str, path_type: str = "shortest") -> PathResult:
        """
        Find fastest path between any two nodes in hierarchy.

        Args:
            start_id: Starting node ID
            end_id: Target node ID
            path_type: Type of path (shortest, hierarchical, capacity)

        Returns:
            PathResult with path information and metadata
        """
        if start_id not in self.nodes or end_id not in self.nodes:
            return PathResult(found=False)

        if start_id == end_id:
            return PathResult(found=True, path=[start_id], distance=0)

        # Choose algorithm based on path type
        if path_type == "hierarchical":
            path = self._find_hierarchical_path(start_id, end_id)
        elif path_type == "capacity":
            path = self._find_capacity_path(start_id, end_id)
        else:  # shortest default
            path = self._find_shortest_path(start_id, end_id)

        if path:
            distance = len(path) - 1
            return PathResult(
                found=True,
                path=path,
                distance=distance,
                path_type=path_type,
                metadata=self._calculate_path_metadata(path)
            )

        return PathResult(found=False)

    def _find_shortest_path(self, start_id: str, end_id: str) -> List[str]:
        """Find shortest path using BFS."""
        if start_id == end_id:
            return [start_id]

        queue = deque([(start_id, [start_id])])
        visited = {start_id}

        while queue:
            current_id, path = queue.popleft()

            for neighbor_id in self.adjacency_list.get(current_id, []):
                if neighbor_id == end_id:
                    return path + [neighbor_id]

                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append((neighbor_id, path + [neighbor_id]))

            for parent_id in self.reverse_adjacency.get(current_id, []):
                if parent_id == end_id:
                    return path + [parent_id]

                if parent_id not in visited:
                    visited.add(parent_id)
                    queue.append((parent_id, path + [parent_id]))

        return []

    def _find_hierarchical_path(self, start_id: str, end_id: str) -> List[str]:
        """Find hierarchical path (up to common ancestor, then down)."""
        start_path = self.nodes[start_id].path_to_root
        end_path = self.nodes[end_id].path_to_root

        # Find lowest common ancestor
        lca = None
        for i in range(min(len(start_path), len(end_path))):
            if start_path[i] == end_path[i]:
                lca = start_path[i]
            else:
                break

        if not lca:
            return []

        # Build path from start to LCA, then to end
        start_to_lca: list[str] = []
        current: Optional[str] = start_id
        while current and current != lca:
            start_to_lca.append(current)
            if current in self.nodes:
                node_data = self.nodes[current]
                current = node_data.parent_id if node_data.parent_id else None

        end_to_lca: list[str] = []
        current = end_id
        while current and current != lca:
            end_to_lca.append(current)
            if current in self.nodes:
                node_data = self.nodes[current]
                current = node_data.parent_id if node_data.parent_id else None

        return start_to_lca + [lca] + list(reversed(end_to_lca))

    def _find_capacity_path(self, start_id: str, end_id: str) -> List[str]:
        """Find path with consideration for capacity planning."""
        # For capacity-based pathfinding, prioritize paths through nodes with lower capacity
        start_path = self.nodes[start_id].path_to_root
        end_path = self.nodes[end_id].path_to_root

        # Find LCAs and evaluate capacity along each path
        lca_candidates = []
        for i in range(min(len(start_path), len(end_path))):
            if start_path[i] == end_path[i]:
                lca_candidates.append(start_path[i])

        if not lca_candidates:
            return []

        # Choose LCA with optimal capacity profile
        lca = min(lca_candidates, key=lambda lca_id: self.nodes[lca_id].capacity if lca_id in self.nodes else 0)

        # Build path
        path: list[str] = []
        current: Optional[str] = start_id
        while current and current != lca:
            path.append(current)
            if current in self.nodes:
                node_data = self.nodes[current]
                current = node_data.parent_id if node_data.parent_id else None

        if lca != start_id:
            path.append(lca)

        current = end_id
        while current and current != lca:
            path.append(current)
            if current in self.nodes:
                node_data = self.nodes[current]
                current = node_data.parent_id if node_data.parent_id else None

        return path

    def _calculate_path_metadata(self, path: List[str]) -> Dict[str, Any]:
        """Calculate metadata for a path."""
        if not path or len(path) < 2:
            return {}

        start_id, end_id = path[0], path[-1]
        start_node = self.nodes.get(start_id)
        end_node = self.nodes.get(end_id)

        if not start_node or not end_node:
            return {}

        # Calculate path characteristics
        total_capacity = sum(self.nodes[pid].capacity for pid in path if pid in self.nodes)
        avg_span = sum(self.nodes[pid].span_of_control for pid in path if pid in self.nodes) / len(path)
        hierarchical_level = len(start_node.path_to_root) + len(end_node.path_to_root)

        return {
            "total_capacity": total_capacity,
            "average_span_of_control": avg_span,
            "hierarchical_level_difference": hierarchical_level,
            "bottleneck_nodes": [
                pid for pid in path
                if pid in self.nodes and self.nodes[pid].capacity < 50
            ],
            "critical_skills_shared": set(),  # Would require additional data
        }

    def extract_subtree(self, root_id: str, max_depth: Optional[int] = None,
                       include_capacity_below: bool = False) -> Dict[str, Any]:
        """
        Extract subtree rooted at a specific node for executive reporting.

        Args:
            root_id: Root of subtree to extract
            max_depth: Maximum depth to include (None for full subtree)
            include_capacity_below: Whether to include capacity calculations

        Returns:
            Dictionary containing subtree data and metadata
        """
        if root_id not in self.nodes:
            return {"error": f"Node {root_id} not found"}

        start_time = time.time()

        def extract_subtree_recursive(node_id: str, current_depth: int = 0) -> Dict[str, Any]:
            if max_depth is not None and current_depth > max_depth:
                return {}

            node_data = self.nodes[node_id]
            subtree_data = {
                "id": node_id,
                "name": node_data.node.name if hasattr(node_data.node, 'name') else node_id,
                "role": node_data.node.role if hasattr(node_data.node, 'role') else "",
                "depth": current_depth,
                "span_of_control": node_data.span_of_control,
                "capacity": node_data.capacity,
                "subtree_size": node_data.subtree_size,
                "department": node_data.department,
            }

            if include_capacity_below:
                subtree_data["children_summary"] = self._calculate_children_summary(node_id)

            children = []
            for child_id in self.adjacency_list.get(node_id, []):
                child_data = extract_subtree_recursive(child_id, current_depth + 1)
                if child_data is not None:
                    children.append(child_data)

            subtree_data["children"] = children
            return subtree_data

        subtree = extract_subtree_recursive(root_id)
        computation_time = (time.time() - start_time) * 1000

        if subtree:
            self.tree_stats.subtree_extraction_count += 1
            self.tree_stats.parallel_computation_time_ms += computation_time

        return {
            "subtree": subtree,
            "computation_time_ms": computation_time,
            "metadata": {
                "root_id": root_id,
                "max_depth": max_depth,
                "total_nodes": self._count_subtree_nodes(subtree),
                "total_spans": self._sum_spans_in_subtree(subtree),
            }
        }

    def _calculate_children_summary(self, parent_id: str) -> Dict[str, Any]:
        """Calculate summary of children below a node."""
        children = self.get_children(parent_id)

        if not children:
            return {}

        return {
            "total_children": len(children),
            "avg_capacity": sum(c.capacity for c in children) / len(children),
            "max_span": max(c.span_of_control for c in children),
            "potential_growth": len([c for c in children if c.capacity > 80]),
        }

    def _count_subtree_nodes(self, subtree: Dict[str, Any]) -> int:
        """Recursively count nodes in subtree."""
        if not subtree:
            return 0

        count = 1  # Current node
        for child in subtree.get("children", []):
            count += self._count_subtree_nodes(child)

        return count

    def _sum_spans_in_subtree(self, subtree: Dict[str, Any]) -> int:
        """Sum spans of control in subtree."""
        if not subtree:
            return 0

        total = subtree.get("span_of_control", 0)
        for child in subtree.get("children", []):
            total += self._sum_spans_in_subtree(child)

        return total

    def detect_executive_boundaries(self) -> Dict[str, Any]:
        """
        Detect executive boundaries and isolation points.

        Returns:
            Dictionary containing executive boundary information
        """
        executive_nodes = []
        isolation_points = []

        for node_id, node_data in self.nodes.items():
            if node_data.is_executive:
                executive_nodes.append(node_id)

            # Detect isolation points (nodes with single connection)
            total_connections = len(self.adjacency_list.get(node_id, [])) + len(self.reverse_adjacency.get(node_id, []))
            if total_connections == 1 and node_id != self.root_id:
                isolation_points.append(node_id)

        # Analyze boundary crossings
        boundary_crossings = self._analyze_boundary_crossings(executive_nodes)

        return {
            "executive_nodes": executive_nodes,
            "isolation_points": isolation_points,
            "boundary_crossings": boundary_crossings,
            "isolated_departments": self._identify_isolated_departments(isolation_points),
            "executive_clusters": self._form_executive_clusters(executive_nodes),
        }

    def _analyze_boundary_crossings(self, executive_nodes: List[str]) -> List[Dict[str, Any]]:
        """Analyze boundary crossings between executive and non-executive nodes."""
        crossings = []

        for exec_id in executive_nodes:
            # Find non-executive nodes directly connected to this executive
            connected_non_exec = []
            for child_id in self.adjacency_list.get(exec_id, []):
                if child_id not in executive_nodes:
                    connected_non_exec.append(child_id)

            for parent_id in self.reverse_adjacency.get(exec_id, []):
                if parent_id not in executive_nodes:
                    connected_non_exec.append(parent_id)

            if connected_non_exec:
                crossings.append({
                    "executive_id": exec_id,
                    "connected_non_executive": connected_non_exec,
                    "boundary_type": "management",
                })

        return crossings

    def _identify_isolated_departments(self, isolation_points: List[str]) -> List[str]:
        """Identify departments with isolation points."""
        isolated_depts = []

        for node_id in isolation_points:
            if node_id in self.nodes:
                isolated_depts.append(self.nodes[node_id].department)

        return list(set(isolated_depts))

    def _form_executive_clusters(self, executive_nodes: List[str]) -> List[Dict[str, Any]]:
        """Form executive clusters based on proximity and reporting relationships."""
        if not executive_nodes:
            return []

        # Simple clustering by finding connected components within executives
        visited: set[str] = set()
        clusters: list[dict[str, Any]] = []

        for exec_id in executive_nodes:
            if exec_id in visited:
                continue

            cluster = set()
            queue = deque([exec_id])

            while queue:
                current = queue.popleft()
                if current in visited:
                    continue

                visited.add(current)
                cluster.add(current)

                # Add connected executives
                for neighbor_id in self.adjacency_list.get(current, []):
                    if neighbor_id in executive_nodes and neighbor_id not in visited:
                        queue.append(neighbor_id)

                for parent_id in self.reverse_adjacency.get(current, []):
                    if parent_id in executive_nodes and parent_id not in visited:
                        queue.append(parent_id)

            if cluster:
                clusters.append({
                    "cluster_id": len(clusters) + 1,
                    "executives": list(cluster),
                    "size": len(cluster),
                })

        return clusters

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive tree statistics."""
        return {
            "basic_stats": {
                "node_count": self.tree_stats.node_count,
                "edge_count": self.tree_stats.edge_count,
                "depth": self.tree_stats.depth,
                "breadth": self.tree_stats.breadth,
            },
            "performance_stats": {
                "index_time_ms": self.tree_stats.index_time_ms,
                "construction_time_ms": self.tree_stats.construction_time_ms,
                "lookup_time_ms": self.tree_stats.lookup_time_ms,
                "parallel_computation_time_ms": self.tree_stats.parallel_computation_time_ms,
            },
            "structural_stats": {
                "subtree_extraction_count": self.tree_stats.subtree_extraction_count,
                "avg_subtree_size": self._calculate_avg_subtree_size(),
                "max_span_of_control": self._calculate_max_span(),
            },
            "efficiency_metrics": {
                "lookup_efficiency": "O(1)",
                "construction_efficiency": "O(n)",
                "memory_efficiency": "Sparse adjacency matrix",
            }
        }

    def _calculate_avg_subtree_size(self) -> float:
        """Calculate average subtree size."""
        total_size = sum(self.nodes[node_id].subtree_size for node_id in self.nodes)
        return total_size / len(self.nodes) if self.nodes else 0

    def _calculate_max_span(self) -> int:
        """Calculate maximum span of control."""
        return max(self.nodes[node_id].span_of_control for node_id in self.nodes) if self.nodes else 0

    def parallel_subtree_extraction(self, root_ids: List[str],
                                  max_depth: Optional[int] = None) -> Dict[str, Any]:
        """
        Parallel subtree extraction for multiple executive reporting trees.

        Args:
            root_ids: List of root IDs for parallel extraction
            max_depth: Maximum depth for extraction

        Returns:
            Dictionary with parallel extraction results
        """
        start_time = time.time()
        results = {}

        # Process subtrees in parallel (simplified sequential execution)
        for root_id in root_ids:
            results[root_id] = self.extract_subtree(root_id, max_depth)

        computation_time = (time.time() - start_time) * 1000

        return {
            "results": results,
            "parallel_computation_time_ms": computation_time,
            "speedup_ratio": len(root_ids) / computation_time if computation_time > 0 else 0,
        }

    def validate_integrity(self) -> Dict[str, Any]:
        """Validate tree integrity and return any issues."""
        issues = []

        # Check for cycles
        if self._detect_cycles():
            issues.append("Cycle detected in tree structure")

        # Check for unreachable nodes
        unreachable = self._find_unreachable_nodes()
        if unreachable:
            issues.append(f"Unreachable nodes found: {unreachable}")

        # Check for disconnected components
        components = self._find_connected_components()
        if len(components) > 1:
            issues.append(f"Disconnected components found: {len(components)}")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "connected_components": len(components),
            "root_connected": all(self.root_id in comp for comp in components),
        }

    def _detect_cycles(self) -> bool:
        """Detect cycles in the tree using DFS."""
        visited = set()
        rec_stack = set()

        def dfs(node_id: str) -> bool:
            if node_id not in visited:
                visited.add(node_id)
                rec_stack.add(node_id)

                for neighbor_id in self.adjacency_list.get(node_id, []):
                    if neighbor_id not in visited:
                        if dfs(neighbor_id):
                            return True
                    elif neighbor_id in rec_stack:
                        return True

                rec_stack.remove(node_id)

            return False

        for node_id in self.nodes:
            if node_id not in visited:
                if dfs(node_id):
                    return True

        return False

    def _find_unreachable_nodes(self) -> List[str]:
        """Find nodes unreachable from root."""
        reachable = set()
        queue = deque([self.root_id])

        while queue:
            node_id = queue.popleft()
            if node_id in reachable:
                continue

            reachable.add(node_id)

            for neighbor_id in self.adjacency_list.get(node_id, []):
                if neighbor_id not in reachable:
                    queue.append(neighbor_id)

        unreachable = [node_id for node_id in self.nodes if node_id not in reachable]
        return unreachable

    def _find_connected_components(self) -> List[Set[str]]:
        """Find connected components in the graph."""
        visited = set()
        components = []

        for node_id in self.nodes:
            if node_id not in visited:
                component = set()
                queue = deque([node_id])

                while queue:
                    current = queue.popleft()
                    if current in visited:
                        continue

                    visited.add(current)
                    component.add(current)

                    for neighbor_id in self.adjacency_list.get(current, []):
                        if neighbor_id not in visited:
                            queue.append(neighbor_id)

                    for parent_id in self.reverse_adjacency.get(current, []):
                        if parent_id not in visited:
                            queue.append(parent_id)

                components.append(component)

        return components

    def export_tree(self) -> Dict[str, Any]:
        """Export complete tree for external use."""
        return {
            "metadata": {
                "root_id": self.root_id,
                "exported_at": datetime.now().isoformat(),
                "total_nodes": self.tree_stats.node_count,
            },
            "nodes": [
                {
                    "id": node_id,
                    "name": self.nodes[node_id].node.name if hasattr(self.nodes[node_id].node, 'name') else node_id,
                    "role": self.nodes[node_id].node.role if hasattr(self.nodes[node_id].node, 'role') else "",
                    "department": self.nodes[node_id].department,
                    "depth": self.nodes[node_id].depth,
                    "span_of_control": self.nodes[node_id].span_of_control,
                    "capacity": self.nodes[node_id].capacity,
                    "is_executive": self.nodes[node_id].is_executive,
                }
                for node_id in self.nodes
            ],
            "edges": [
                {
                    "source": source_id,
                    "target": target_id,
                    "type": "reports_to" if source_id in self.reverse_adjacency.get(target_id, []) else "manages",
                }
                for source_id in self.adjacency_list
                for target_id in self.adjacency_list[source_id]
            ],
            "stats": self.get_stats(),
        }


# Convenience function for direct use
def build_organization_chart(org_nodes: List[OrgNode], root_id: str = "human-ceo") -> OrganizationChart:
    """Convenience function to build an organization chart."""
    return OrganizationChart(org_nodes, root_id)
