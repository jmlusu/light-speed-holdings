"""Archify integration — registry to typed JSON IR diagram sources.

Converts the loaded :class:`CompanyRegistry` (from ``ai_company.registry``)
into Archify JSON IR documents for the four supported diagram types:

- ``architecture`` — agent hierarchy + department boundaries + tool detail in cards
- ``workflow`` — business workflows from ``config/workflows/workflows.yaml``
- ``sequence`` — the same workflow steps as a call chain over time
- ``dataflow`` — the workflow data hand-offs (step outputs -> next step inputs)

The caller renders these with ``ai_company.archify.renderer`` (which wraps the
Archify Node.js CLI under ``.opencode/skills/archify/bin/archify.mjs``).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ai_company.models import CompanyRegistry

# ---------------------------------------------------------------------------
# Archify schema constants
# ---------------------------------------------------------------------------

_COMPONENT_DEFAULT = "backend"
_COMPONENT_TYPES = frozenset(
    {"frontend", "backend", "database", "cloud", "security", "messagebus", "external"}
)

# Map of department name -> Archify component type for the architecture diagram.
_DEPARTMENT_TYPE: dict[str, str] = {
    "Executive": "external",
    "Security": "security",
    "IT": "cloud",
    "Data": "database",
    "AI Research": "cloud",
    "Operations": "messagebus",
    "Product": "frontend",
    "Marketing": "frontend",
    "People": "frontend",
    "Customer Success": "frontend",
    "Finance": "database",
    "Legal": "security",
    "Strategy": "frontend",
    "Sales": "frontend",
    "Technology": "backend",
    "Board": "external",
    "QA": "backend",
}

# Executive IDs that report to the board / human CEO and form the top of the
# hierarchy diagram. Used to pick the natural primary path.
_TOP_AGENT_IDS = frozenset(
    {"human_ceo", "chief_of_staff", "cto", "coo", "caio", "cfo", "ciso", "clo", "cso"}
)


@dataclass(frozen=True)
class DiagramSpec:
    """One generated Archify JSON IR document plus its output filename."""

    diagram_type: str
    json_name: str
    html_name: str
    title: str
    data: dict[str, Any]


def _component_type(department: str) -> str:
    """Return an Archify component type for a department name."""
    return _DEPARTMENT_TYPE.get(department, _COMPONENT_DEFAULT)


def _safe_agent_id(agent_id: str) -> str:
    """Archify ids must match ``[A-Za-z0-9_.-]+`` — use the registry hyphen form."""
    return agent_id.replace("_", "-")


def _tool_summary(agent: Any) -> list[str]:
    """Render an agent's granted tools as short card items (``read``, ``edit``, ...)."""
    tools = sorted(set(getattr(agent, "tools", None) or []))
    if not tools:
        return []
    return [", ".join(tools)]


def _responsibilities(agent: Any, limit: int = 2) -> list[str]:
    """Render up to ``limit`` responsibilities as card strings."""
    items: list[str] = []
    for resp in getattr(agent, "responsibilities", None) or []:
        text = resp if isinstance(resp, str) else str(resp)
        if len(text) > 60:
            text = text[:57] + "..."
        items.append(text)
        if len(items) >= limit:
            break
    return items


def build_architecture(
    registry: CompanyRegistry,
    scope: str = "leadership",
) -> dict[str, Any]:
    """Build an ``architecture`` JSON IR document.

    ``scope`` controls node granularity:

    - ``leadership`` (default): the board + executive layer; department
      boundaries wrap their executive; tool/responsibility detail goes in cards.
    - ``full``: every agent (executive + specialist) as a node, wired by
      ``reports_to`` relationships. Use ``standard`` quality for this scope;
      it exceeds the ~12-primary-node showcase ceiling by design.

    components that are literally the board/Human CEO render as ``external``
    (actors outside the agent runtime); security/legal/data get semantic types.
    """
    title = (
        f"{registry.company.name} — Agent Hierarchy"
        if scope == "leadership"
        else f"{registry.company.name} — Full Agent Graph"
    )

    components: list[dict[str, Any]] = []
    connections: list[dict[str, Any]] = []
    boundaries: list[dict[str, Any]] = []
    cards: list[dict[str, Any]] = []

    # leadership scope: executives + board only
    agent_pool: list[Any] = list(registry.executives) + list(registry.board)
    if scope == "full":
        agent_pool += list(registry.specialists)

    # de-dup by id (board members may overlap with executives in some configs)
    by_id = {_safe_agent_id(a.id): a for a in agent_pool}

    board_member_ids = {_safe_agent_id(b.id) for b in registry.board}
    department_members: dict[str, list[str]] = {}
    for agent in agent_pool:
        is_board = _safe_agent_id(agent.id) in board_member_ids
        dept = getattr(agent, "department", None) or ""
        comp_type = "external" if is_board or agent.id == "human_ceo" else _component_type(dept)
        components.append(
            {
                "id": _safe_agent_id(agent.id),
                "type": comp_type,
                "label": agent.name or agent.id,
                "sublabel": (
                    ""
                    if scope == "leadership"
                    else (_department_label(dept) if not is_board else _board_sublabel(agent))
                ),
            }
        )
        dept_key = dept or "Unassigned"
        if not is_board and agent.id != "human_ceo":
            department_members.setdefault(dept_key, []).append(_safe_agent_id(agent.id))

    # reporting edges (reports_to -> agent) — no self loops, only known ids.
    # "board" is a group id: the Human CEO reports to it; draw the edge to the
    # board chair as the apex representative.
    ceo_reports_to_board = False
    for agent in agent_pool:
        child_id = _safe_agent_id(agent.id)
        reports_to = getattr(agent, "reports_to", None)
        if not reports_to:
            continue
        parent_id = (
            _safe_agent_id("board_chair") if reports_to == "board" else _safe_agent_id(reports_to)
        )
        if parent_id == child_id or parent_id not in by_id:
            continue
        ceo_reports_to_board = ceo_reports_to_board or reports_to == "board"
        connections.append(
            {
                "id": f"conn-{parent_id}-to-{child_id}",
                "from": parent_id,
                "to": child_id,
            }
        )

    # explicit free-placement layout: components require pos/size.
    gap_x = 8 if scope == "leadership" else _POS_GAP_X
    _assign_positions(components, connections, gap_x=gap_x)
    _route_connections(components, connections)

    # department boundaries (region) stacking the executives they own.
    # Leadership omits them: their 9px titles would cap the viewBox well below
    # what a 10-wide exec row can reach; the cards carry the department detail.
    if scope == "full":
        for dept, member_ids in sorted(department_members.items()):
            if len(member_ids) < 2:
                continue
            boundaries.append({"kind": "region", "label": dept, "wraps": sorted(member_ids)})

    # cards: title = department, items = responsibilities; tools appended
    if scope == "leadership":
        for dept, agent in sorted(
            (
                (getattr(a, "department", None) or "Unassigned", a)
                for a in registry.executives + registry.board
            ),
            key=lambda pair: pair[0],
        ):
            dot = _dept_dot(dept)
            items = _responsibilities(agent)
            items += _tool_summary(agent)
            if items:
                cards.append({"dot": dot, "title": f"{dept} — {agent.name}", "items": items})
    else:
        cards.append(_tool_legend_card())

    data: dict[str, Any] = {
        "schema_version": 1,
        "diagram_type": "architecture",
        "meta": {
            "title": title,
            "quality_profile": "standard",
            "viewBox": _extent_viewbox(components, connections),
        },
        "components": components,
    }
    if connections:
        data["connections"] = connections
    if boundaries:
        data["boundaries"] = boundaries
    if cards:
        data["cards"] = cards
    return data


def _department_label(department: str | None) -> str:
    """Short sublabel under an agent node, or omit when unknown."""
    if not department:
        return ""
    if department == "Board":
        return "Board of Directors"
    return department


def _board_sublabel(member: Any) -> str:
    """Board members carry a role (e.g. 'Finance Committee Chair')."""
    role = getattr(member, "role", None)
    return role if role else "Board of Directors"


# Free-placement layout constants (px).
_POS_ORIGIN = (60, 90)  # first node starts here
_POS_ROW_H = 115  # vertical step between hierarchy depths
_POS_GAP_X = 36  # gap between sibling subtrees within a depth row
_NODE_HEIGHT = 60


def _assign_positions(
    components: list[dict[str, Any]],
    connections: list[dict[str, Any]],
    gap_x: float = _POS_GAP_X,
) -> None:
    """Assign ``pos``/``size`` to every component with a compact tidy tree.

    Subtrees are packed left-to-right with sibling gaps based on their natural
    width, and every parent is centered over the span its own children occupy.
    Packing each subtree independently keeps the whole diagram as narrow as the
    widest row can be, while centering parents keeps reporting edges short and
    free of cross-parent crossings.

    Root *leaves* (roots with no children of their own) are absorbed back into
    the depth-0 band within the widest row's span instead of being appended to
    the far right — with several disconnected roots this keeps the canvas at the
    larger tree's width rather than its width plus every orphan.
    """
    by_id = {c["id"]: c for c in components}
    children_of: dict[str, list[str]] = {}
    parent_of: dict[str, str] = {}
    for conn in connections:
        children_of.setdefault(conn["from"], []).append(conn["to"])
        parent_of.setdefault(conn["to"], conn["from"])

    # BFS depth (shortest root distance, stable by input order).
    depth: dict[str, int] = {}
    roots = [c["id"] for c in components if c["id"] not in parent_of]
    frontier = list(roots)
    for node_id in frontier:
        depth[node_id] = 0
    while frontier:
        nxt: list[str] = []
        for node_id in frontier:
            for kid in children_of.get(node_id, []):
                if kid not in depth:
                    depth[kid] = depth[node_id] + 1
                    nxt.append(kid)
        frontier = nxt
    for c in components:  # any disconnected leftovers
        depth.setdefault(c["id"], 0)
    if not depth:
        return

    size_cache = {n["id"]: _node_bbox_size(n) for n in components}
    # Keep x minimal: parent is centered over its children's span, but must not
    # drift left of the left-most child.
    placed: dict[str, tuple[float, float]] = {}

    def _shift_subtree(
        node_id: str,
        delta: float,
        _depth: dict[str, int],
        _kids: dict[str, list[str]],
        _placed: dict[str, tuple[float, float]],
    ) -> None:
        """Shift ``node_id`` and every descendant right by ``delta`` px."""
        left, right = _placed[node_id]
        _placed[node_id] = (left + delta, right + delta)
        for kid in _kids.get(node_id, []):
            if _depth.get(kid, -1) > _depth.get(node_id, -1):
                _shift_subtree(kid, delta, _depth, _kids, _placed)

    def layout_subtree(node_id: str, x_left: float) -> tuple[float, float]:
        """Recursively place ``node_id``'s subtree at ``x_left``.

        Returns the subtree's packed ``(left, right)`` x-range.
        """
        kids = [
            k
            for k in children_of.get(node_id, [])
            if k in by_id and depth.get(k, 0) > depth.get(node_id, -1)
        ]
        w, h = size_cache[node_id]
        if not kids:
            placed[node_id] = (x_left, x_left + w)
            return (x_left, x_left + w)

        child_x: float = x_left
        child_box = []
        for kid in kids:
            box = layout_subtree(kid, child_x)
            child_box.append(box)
            child_x = box[1] + gap_x  # next sibling to the right
        left = min(b[0] for b in child_box)
        right = max(b[1] for b in child_box)
        center = (left + right) / 2.0
        # True tree centering: a parent sits over its children's midpoint even
        # when its own card is wider than the span (a single child keeps dx~0,
        # so the edge can stay a clean straight vertical). The global x-shift
        # below re-normalises any leftward drift.
        placed[node_id] = (center - w / 2.0, center + w / 2.0)
        return (min(left, placed[node_id][0]), max(right, placed[node_id][1]))

    root_x: float = _POS_ORIGIN[0]
    for root_id in roots:
        if root_id in placed:
            continue
        layout_subtree(root_id, root_x)
        box = placed[root_id]
        root_x = box[1] + gap_x
    for c in components:  # disconnected leftovers / safety
        if c["id"] not in placed:
            w, h = size_cache[c["id"]]
            placed[c["id"]] = (root_x, root_x + w)
            root_x += w + gap_x

    # Absorb depth-0 leaf roots back into the depth-0 band. They were appended
    # after every tree above; moving them left into free row-0 gaps keeps the
    # canvas at the widest row's span instead of that span + all orphan roots.
    min_x = min(v[0] for v in placed.values())
    occupied: list[tuple[float, float]] = [
        placed[node["id"]]
        for node in components
        if depth[node["id"]] == 0 and children_of.get(node["id"])
    ]
    occupied.sort()
    for node in sorted(
        (n for n in components if depth[n["id"]] == 0 and not children_of.get(n["id"])),
        key=lambda n: placed[n["id"]][0],
    ):
        w, _h = size_cache[node["id"]]
        candidate: float = min_x
        for left, right in occupied:
            if candidate + w + gap_x <= left:  # fits before this occupied card
                break
            candidate = max(candidate, right + gap_x)
        placed[node["id"]] = (candidate, candidate + w)
        occupied.append((candidate, candidate + w))
        occupied.sort()

    # Resolve any same-row collisions left by tree centering. True-centering a
    # parent over a wide child span can shift it left over an already-placed
    # sibling; pushing the right-hand node right restores the gap_x floor
    # without changing the tree's reporting structure.
    by_depth: dict[int, list[str]] = {}
    for n in components:
        by_depth.setdefault(depth[n["id"]], []).append(n["id"])
    for _d_row, ids in by_depth.items():
        ids = sorted(ids, key=lambda i: placed[i][0])
        last_right: float | None = None
        for nid in ids:
            left, _right = placed[nid]
            w, _h = size_cache[nid]
            if last_right is not None and left < last_right + gap_x + 1e-6:
                new_left = last_right + gap_x
                delta = new_left - left
                # shift this node AND its whole subtree right so children keep
                # reporting to a consistent parent position
                _shift_subtree(nid, delta, depth, children_of, placed)
            last_right = placed[nid][1]

    shift = _POS_ORIGIN[0] - min_x
    for node in components:
        w, h = size_cache[node["id"]]
        left, _right = placed[node["id"]]
        node["pos"] = [
            left + shift,
            _POS_ORIGIN[1] + depth[node["id"]] * _POS_ROW_H,
        ]
        node["size"] = [w, h]


def _route_connections(components: list[dict[str, Any]], connections: list[dict[str, Any]]) -> None:
    """Give every connection a truthful orthogonal elbow route.

    Parents sit one row above children (BFS depth), so the natural route is:
    exit the parent's *bottom*, run a short vertical stub, cross horizontally
    to the child's center column, then descend into the child's *top*. Explicit
    ``via`` points + ``fromSide``/``toSide`` make the route truthful, which is
    what Archify's showcase ``clean-flow/endpoint-side-direction`` check demands
    for free-placement diagrams.

    Sibling edges of the *same* parent share one horizontal band (visual fan,
    allowed — shared semantic endpoint). Edges from *different* parents in the
    same row get distinct bands so their horizontal runs never merge into an
    ambiguous corridor.
    """
    by_id: dict[str, dict[str, Any]] = {c["id"]: c for c in components}

    # Tree layout: a parent's children all live in the next row, so that
    # parent's edges share one horizontal band (allowed — shared semantic
    # endpoint). Edges from *different* parents must use distinct bands, else
    # their horizontal runs merge into an ambiguous corridor.
    groups: dict[str, list[dict[str, Any]]] = {}
    for conn in connections:
        groups.setdefault(conn["from"], []).append(conn)

    # Stagger bands per parent row so each parent gets a unique yet readable y:
    # both the source stub (parent bottom -> band) and the target stub (band ->
    # child top) stay above Archify's 8px micro-segment floor.
    row_bands: dict[tuple[int, int], int] = {}
    band_mid: dict[str, float] = {}
    for parent_id, kids in sorted(groups.items()):
        parent_node = by_id[parent_id]
        child_top = min(by_id[k["to"]]["pos"][1] for k in kids)
        parent_bottom = parent_node["pos"][1] + parent_node["size"][1]
        gap = max(10.0, child_top - parent_bottom)
        row_key = (int(parent_node["pos"][1]), int(child_top))
        slot = row_bands.get(row_key, 0)
        row_bands[row_key] = slot + 1
        n_in_row = row_bands[row_key]
        step = max(6.0, min((gap - 16.0) / max(1, n_in_row), 14.0))
        band_mid[parent_id] = parent_bottom + 8.0 + slot * step

    for conn in connections:
        parent = by_id.get(conn["from"])
        child = by_id.get(conn["to"])
        if parent is None or child is None:
            continue
        px = parent["pos"][0]
        pw = parent["size"][0]
        cx = child["pos"][0]
        cw = child["size"][0]
        parent_cx = px + pw / 2.0
        child_cx = cx + cw / 2.0
        dx = child_cx - parent_cx
        if abs(dx) < 24.0:
            # Child near-centered under its parent: with true tree centering
            # dx->0, so the renderer can draw a clean straight vertical line.
            conn.pop("via", None)
            conn["route"] = "straight"
            conn["fromSide"] = "bottom"
            conn["toSide"] = "top"
            continue
        mid_y = band_mid.get(
            conn["from"],
            (parent["pos"][1] + parent["size"][1] + child["pos"][1]) / 2.0,
        )
        conn["fromSide"] = "bottom"
        conn["toSide"] = "top"
        conn["via"] = [
            [parent_cx, round(mid_y, 1)],
            [child_cx, round(mid_y, 1)],
        ]


def _extent_viewbox(
    components: list[dict[str, Any]], connections: list[dict[str, Any]]
) -> list[int]:
    """Tight viewBox that fits every component and edge elbow, with padding."""
    max_x = _POS_ORIGIN[0]
    max_y = _POS_ORIGIN[1]
    for node in components:
        max_x = max(max_x, node["pos"][0] + node["size"][0])
        max_y = max(max_y, node["pos"][1] + node["size"][1])
    for conn in connections:
        for via in conn.get("via", []):
            max_x = max(max_x, via[0])
            max_y = max(max_y, via[1])
    return [int(max_x + 120), int(max_y + 120)]


def _node_bbox_size(node: dict[str, Any]) -> tuple[float, float]:
    """Width that fits the (sub)label plus padding, clamped."""
    label = str(node.get("label", ""))
    sub = str(node.get("sublabel", "") or "")
    label_w = len(label) * 6.5 + 12
    sub_w = len(sub) * 5.2 + 20
    w = max(108, label_w, sub_w)
    return min(w, 340), _NODE_HEIGHT


def _dept_dot(department: str) -> str:
    """Stable card dot color per department bucket."""
    palette = ["cyan", "emerald", "rose", "orange", "violet", "amber", "slate"]
    if not department:
        return palette[0]
    return palette[abs(hash(department)) % len(palette)]


def _tool_legend_card() -> dict[str, Any]:
    return {
        "dot": "cyan",
        "title": "Tool legend",
        "items": [
            "read / grep / list — inspect repository and state",
            "edit / bash — modify files and run commands",
            "task — delegate to a sub-agent",
            "webfetch — fetch external content",
        ],
    }


def build_workflow(registry: CompanyRegistry, workflow_id: str = "hiring") -> dict[str, Any]:
    """Build a ``workflow`` JSON IR document from a registry workflow.

    Lanes are the agents (owners) participating in the workflow; nodes are the
    workflow steps; phases group contiguous clusters of columns; the main path
    follows the step order. Uses schema_version 2 (readable layout contract).
    """
    workflow = next(
        (w for w in registry.workflows if w.id == workflow_id or w.name == workflow_id),
        None,
    )
    if workflow is None and registry.workflows:
        workflow = registry.workflows[0]
    if workflow is None:
        raise ValueError(f"No workflows in registry to render '{workflow_id}'")

    steps = workflow.steps
    owners: list[str] = []
    for step in steps:
        owner = str(getattr(step, "owner", "") or "")
        if owner and owner not in owners:
            owners.append(owner)

    lanes = [{"id": _safe_agent_id(owner), "label": owner} for owner in owners]

    # nodes: one per step; col advances per step (workflow is linear step order)
    nodes: list[dict[str, Any]] = []
    for idx, step in enumerate(steps):
        label = step.name
        sublabel = getattr(step, "action", "") or None
        width = _node_width(label, sublabel)
        nodes.append(
            {
                "id": _safe_agent_id(step.id),
                "lane": _safe_agent_id(str(step.owner or "")),
                "col": idx,
                "type": _step_type(getattr(step, "action", "")),
                "label": label,
                "sublabel": sublabel,
                "width": width,
            }
        )

    # edges follow step order; approval steps get the security variant
    edges: list[dict[str, Any]] = []
    for idx in range(len(steps) - 1):
        spec = {
            "id": f"w-{_safe_agent_id(steps[idx].id)}-to-{_safe_agent_id(steps[idx + 1].id)}",
            "from": _safe_agent_id(steps[idx].id),
            "to": _safe_agent_id(steps[idx + 1].id),
        }
        if "approval" in getattr(steps[idx], "action", "") or "approval" in str(
            getattr(steps[idx + 1], "action", "")
        ):
            spec["variant"] = "security"
        edges.append(spec)

    main_path = [_safe_agent_id(s.id) for s in steps]

    cards = [
        {
            "dot": "cyan",
            "title": workflow.name,
            "items": [
                f"Trigger: {workflow.trigger or 'manual'}",
                f"Owner: {workflow.owner or 'unassigned'}",
                f"{len(steps)} steps across {len(owners)} owners",
            ],
        }
    ]

    data: dict[str, Any] = {
        "schema_version": 2,
        "diagram_type": "workflow",
        "meta": {
            "title": f"{workflow.name} — Workflow",
            "quality_profile": "showcase",
        },
        "lanes": lanes,
        "nodes": nodes,
        "edges": edges,
        "mainPath": main_path,
        "cards": cards,
    }
    return data


def _step_type(action: str) -> str:
    """Map a workflow action string to an Archify node type."""
    if any(tok in action for tok in ("approval", "approve", "gate", "sign")):
        return "security"
    if any(tok in action for tok in ("offer", "onboard", "create", "make")):
        return "backend"
    if any(tok in action for tok in ("interview", "source", "select")):
        return "frontend"
    if any(tok in action for tok in ("budget", "finance", "verify")):
        return "database"
    return "backend"


def _short_label(value: str, length: int) -> str:
    """Truncate a label to ``length`` chars with an ellipsis."""
    value = value.strip()
    return value if len(value) <= length else value[: length - 1] + "…"


def _node_width(label: str, sublabel: str | None = None) -> float:
    """Estimate node width (px) so labels fit at the 6px legible minimum.

    Archify validates at ~4.5px/character for labels and ~3.7px/char for
    sublabels; we size from the widest of both, clamped to a sane maximum.
    """
    label_w = len(label) * 9
    sub_w = (len(sublabel) if sublabel else 0) * 8
    return min(max(116, label_w, sub_w) + 16, 260)


def build_sequence(registry: CompanyRegistry, workflow_id: str = "hiring") -> dict[str, Any]:
    """Build a ``sequence`` JSON IR document from a workflow.

    Participants are the workflow owners; each step becomes a message from its
    owner to the next *distinct* owner (consecutive steps by the same owner are
    folded into a single call label) so no message has a zero-width span. SLA
    steps carry a security/emphasis variant.
    """
    workflow = next(
        (w for w in registry.workflows if w.id == workflow_id or w.name == workflow_id),
        None,
    )
    if workflow is None and registry.workflows:
        workflow = registry.workflows[0]
    if workflow is None:
        raise ValueError(f"No workflows in registry to render '{workflow_id}'")
    steps = workflow.steps
    if not steps:
        raise ValueError("Workflow has no steps to sequence")

    owners: list[str] = []
    for step in steps:
        owner = str(getattr(step, "owner", "") or "")
        if owner and owner not in owners:
            owners.append(owner)

    participants = [
        {
            "id": _safe_agent_id(o),
            "type": _participant_type(o),
            "label": _participant_label(o),
        }
        for o in owners
    ]

    # Fold consecutive same-owner steps into one message to that in the next
    # distinct owner; a single-owner tail step needs no message at all.
    messages: list[dict[str, Any]] = []
    y = 170
    i = 0
    while i < len(steps):
        src = str(getattr(steps[i], "owner", "") or owners[0])
        labels = [steps[i].name]
        j = i + 1
        while j < len(steps) and str(getattr(steps[j], "owner", "")) == src:
            labels.append(steps[j].name)
            j += 1
        if j < len(steps):
            dst = str(getattr(steps[j], "owner", ""))
            messages.append(
                {
                    "id": f"msg-{_safe_agent_id(steps[i].id)}",
                    "from": _safe_agent_id(src),
                    "to": _safe_agent_id(dst),
                    "y": y,
                    "label": " → ".join(labels),
                    "variant": (
                        "security"
                        if any("approval" in getattr(steps[k], "action", "") for k in range(i, j))
                        else "default"
                    ),
                }
            )
            y += 43
        i = j

    data: dict[str, Any] = {
        "schema_version": 1,
        "diagram_type": "sequence",
        "meta": {
            "title": f"{workflow.name} — Call Sequence",
            "quality_profile": "showcase",
            "column_fit": "spread",
            "viewBox": [max(820, 140 + len(owners) * 160), max(760, y + 140)],
            "animation": "trace",
        },
        "participants": participants,
        "messages": messages,
    }
    return data


def _participant_label(owner: str) -> str:
    """Short label that fits the ~86px sequence participant box."""
    low = owner.lower()
    if low == "department_executive":
        return "Dept Exec"
    if low in {"chro", "hr"}:
        return "People"
    if low == "recruiter":
        return "Recruiting"
    if low == "cfo":
        return "Finance"
    if low.isupper() or len(owner) <= 12:
        return owner
    words = [w.capitalize() for w in owner.replace("_", " ").split()]
    label = " ".join(words)
    return label if len(label) <= 14 else label[:13] + "…"


def _participant_type(owner: str) -> str:
    """Map an owner id to a semantic participant type."""
    low = owner.lower()
    if "financial" in low or "budget" in low:
        return "database"
    if "security" in low or "approval" in low:
        return "security"
    if "recruit" in low or "hr" in low or "chro" in low:
        return "frontend"
    return "backend"


def build_dataflow(registry: CompanyRegistry, workflow_id: str = "hiring") -> dict[str, Any]:
    """Build a ``dataflow`` JSON IR document from a workflow's steps.

    Steps are placed into up to five pipeline ``stages`` in order; each stage
    holds one or more step ``nodes`` stacked in ``row`` order. Data ``flows``
    connect each step to the next step by a *different* owner (self-handoffs
    are the same node, so no zero-width flow is produced) and are labelled with
    the source step's ``outputs`` when present — a truthful rendering of the
    workflow's data contract, no invented fields.
    """
    workflow = next(
        (w for w in registry.workflows if w.id == workflow_id or w.name == workflow_id),
        None,
    )
    if workflow is None and registry.workflows:
        workflow = registry.workflows[0]
    if workflow is None:
        raise ValueError(f"No workflows in registry to render '{workflow_id}'")
    steps = workflow.steps
    if not steps:
        raise ValueError("Workflow has no steps to render as data flow")

    max_step_width = max(
        (
            _node_width(
                _short_label(str(s.name), 12), _short_label(str(getattr(s, "owner", "") or ""), 12)
            )
            for s in steps
        ),
        default=112,
    )
    # Cap stages so the right-most node stays inside the ~930px that keeps
    # node text readable (>=6px) at a 1440px desktop viewport.
    max_stages = max(
        2, int((930 - _DF_STAGE_CX - _DF_PAD_RIGHT - max_step_width) // _DF_STAGE_DX) + 1
    )
    stage_count = min(5, len(steps), max_stages)
    stage_of: list[int] = []
    for idx in range(len(steps)):
        stage_of.append(min(idx * stage_count // len(steps), stage_count - 1))

    stages = [{"label": f"Stage {s + 1}"} for s in range(stage_count)]
    if workflow.name:
        phases = _STAGE_PHASES.get(len(steps), ["Request", "Approve", "Source", "Title"])
        stages = [
            {"label": phases[s] if s < len(phases) else f"Stage {s + 1}"}
            for s in range(stage_count)
        ]

    nodes: list[dict[str, Any]] = []
    stage_row: dict[int, int] = {}
    for idx, step in enumerate(steps):
        stage = stage_of[idx]
        label = _short_label(step.name, 12)
        sublabel = _short_label(str(getattr(step, "owner", "") or ""), 12)
        width = min(_node_width(label, sublabel), 148)
        nodes.append(
            {
                "id": _safe_agent_id(step.id),
                "type": _step_type(getattr(step, "action", "")),
                "label": label,
                "sublabel": sublabel,
                "stage": stage,
                "row": stage_row.get(stage, 0),
                "width": width,
                "height": 58,
            }
        )
        stage_row[stage] = stage_row.get(stage, 0) + 1

    flows: list[dict[str, Any]] = []
    node_by_id = {n["id"]: n for n in nodes}
    for idx in range(len(steps) - 1):
        src = str(getattr(steps[idx], "owner", "") or "")
        dst = str(getattr(steps[idx + 1], "owner", "") or "")
        if src == dst:
            continue
        outputs = getattr(steps[idx], "outputs", None) or []
        label = ", ".join(str(o) for o in outputs) if outputs else steps[idx].name
        if len(label) > 16:
            label = label[:15] + "…"
        from_node = node_by_id.get(_safe_agent_id(steps[idx].id))
        to_node = node_by_id.get(_safe_agent_id(steps[idx + 1].id))
        flow: dict[str, Any] = {
            "id": f"flow-{_safe_agent_id(steps[idx].id)}-to-{_safe_agent_id(steps[idx + 1].id)}",
            "from": _safe_agent_id(steps[idx].id),
            "to": _safe_agent_id(steps[idx + 1].id),
            "label": label,
            "variant": (
                "security"
                if any("approval" in getattr(steps[k], "action", "") for k in (idx, idx + 1))
                else "default"
            ),
        }
        if from_node is not None and to_node is not None:
            fx, fy = _df_center(from_node)
            tx, ty = _df_center(to_node)
            label_dy = 0.0
            if abs(ty - fy) < 1.0 and tx > fx:
                label_dy = 40.0  # sit below the node row so the label clears both nodes
            flow["labelAt"] = [round((fx + tx) / 2.0, 1), round((fy + ty) / 2.0 + label_dy, 1)]
        flows.append(flow)

    cards = [
        {
            "dot": "cyan",
            "title": f"{workflow.name} — Data Contract",
            "items": [
                f"{len(steps)} steps across {stage_count} stages",
                "Arrows label each hand-off's output data",
                "Same-owner hand-offs stay local to one node",
            ],
        }
    ]

    data: dict[str, Any] = {
        "schema_version": 1,
        "diagram_type": "dataflow",
        "meta": {
            "title": f"{workflow.name} — Data Flow",
            "quality_profile": "showcase",
            "viewBox": _dataflow_viewbox(stages, nodes),
        },
        "stages": stages,
        "nodes": nodes,
        "flows": flows,
        "cards": cards,
    }
    return data


# Data-flow geometry constants (see renderers/dataflow/README.md).
_DF_STAGE_CX = 100  # first stage center x
_DF_STAGE_DX = 215  # center-to-center stage spacing
_DF_ROW_TOP = 128  # first row top y
_DF_ROW_DY = 114  # top-to-top row spacing
_DF_PAD_RIGHT = 60  # margin past the widest node
_DF_PAD_BOTTOM = 80  # margin below the lowest row


def _dataflow_viewbox(stages: list[dict[str, Any]], nodes: list[dict[str, Any]]) -> list[int]:
    """Tight-but-padded viewBox covering every stage and node."""
    last_stage = len(stages) - 1
    max_width = max((n.get("width", 112) for n in nodes), default=112)
    max_row = max((n.get("row", 0) for n in nodes), default=0)
    width = max(620, _DF_STAGE_CX + last_stage * _DF_STAGE_DX + max_width + _DF_PAD_RIGHT)
    width = min(width, 930)
    height = max(520, _DF_ROW_TOP + max_row * _DF_ROW_DY + 58 + _DF_PAD_BOTTOM)
    return [int(width), int(height)]


def _df_center(node: dict[str, Any]) -> tuple[float, float]:
    """Center point of a data-flow node from stage/row geometry."""
    cx = _DF_STAGE_CX + node["stage"] * _DF_STAGE_DX
    cy = _DF_ROW_TOP + node["row"] * _DF_ROW_DY + 58 / 2.0
    return cx, cy


_STAGE_PHASES: dict[int, list[str]] = {
    6: ["Request", "Approve", "Source", "Decision", "Onboard"],
    5: ["Request", "Approve", "Source", "Decision", "Onboard"],
    4: ["Request", "Source", "Decision", "Onboard"],
    3: ["Request", "Execute", "Close"],
    2: ["Request", "Execute"],
}


def generate_specs(registry: CompanyRegistry, scope: str = "leadership") -> list[DiagramSpec]:
    """Generate the default set of diagram specs for ``ai-company archify generate``."""
    if not registry.workflows:
        raise ValueError("Registry has no workflows; cannot generate diagram set")
    workflow_id = registry.workflows[0].id
    return [
        DiagramSpec(
            diagram_type="architecture",
            json_name="architecture.json",
            html_name="architecture.html",
            title=f"{registry.company.name} — Agent Hierarchy",
            data=build_architecture(registry, scope=scope),
        ),
        DiagramSpec(
            diagram_type="workflow",
            json_name=f"{workflow_id}.workflow.json",
            html_name=f"{workflow_id}.workflow.html",
            title=f"{workflow_id} workflow",
            data=build_workflow(registry, workflow_id=workflow_id),
        ),
        DiagramSpec(
            diagram_type="sequence",
            json_name=f"{workflow_id}.sequence.json",
            html_name=f"{workflow_id}.sequence.html",
            title=f"{workflow_id} sequence",
            data=build_sequence(registry, workflow_id=workflow_id),
        ),
        DiagramSpec(
            diagram_type="dataflow",
            json_name=f"{workflow_id}.dataflow.json",
            html_name=f"{workflow_id}.dataflow.html",
            title=f"{workflow_id} dataflow",
            data=build_dataflow(registry, workflow_id=workflow_id),
        ),
    ]
