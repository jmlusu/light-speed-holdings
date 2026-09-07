"""Tests for the Archify diagram converter (registry -> JSON IR).

These unit tests are hermetic: they build a small synthetic registry and check
the generated JSON IR structure and layout invariants without invoking Node.js
(the renderer/validation path is covered separately by the CLI + CI gate).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_company.archify.converter import (
    build_architecture,
    build_dataflow,
    build_sequence,
    build_workflow,
    generate_specs,
)
from ai_company.models import (
    BoardMember,
    Company,
    CompanyRegistry,
    Executive,
    Workflow,
    WorkflowStep,
)


@pytest.fixture()
def registry() -> CompanyRegistry:
    board = [
        BoardMember(id="board_chair", name="Board Chair", role="Chair"),
        BoardMember(id="board_finance", name="Finance Lead", role="Finance"),
    ]
    executives = [
        Executive(
            id="human_ceo",
            name="Human CEO",
            title="CEO",
            department="Office of the CEO",
            reports_to="board",
        ),
        Executive(
            id="cto",
            name="CTO",
            title="Chief Technology Officer",
            department="Engineering",
            reports_to="human_ceo",
        ),
        Executive(
            id="cfo",
            name="CFO",
            title="Chief Financial Officer",
            department="Finance",
            reports_to="human_ceo",
        ),
        Executive(
            id="cdo",
            name="CDO",
            title="Chief Data Officer",
            department="Data",
            reports_to="cto",
        ),
    ]
    return CompanyRegistry(
        company=Company(id="test", name="Test Co"),
        workflows=[
            Workflow(
                id="hiring",
                name="Hiring Workflow",
                trigger="job_requisition",
                owner="hr",
                steps=[
                    WorkflowStep(
                        id="post",
                        name="Post Job",
                        action="Create job posting",
                        owner="recruiter",
                    ),
                    WorkflowStep(
                        id="review",
                        name="Review",
                        action="Screen",
                        owner="recruiter",
                    ),
                ],
            )
        ],
        executives=executives,
        board=board,
    )


def _validate_layout(architecture: dict, threshold: float = 8.0) -> None:
    """Assert same-row components respect a minimum horizontal gap."""
    rows: dict[float, list[dict]] = {}
    for c in architecture["components"]:
        rows.setdefault(round(c["pos"][1], 1), []).append(c)
    for _y, row in rows.items():
        row.sort(key=lambda c: c["pos"][0])
        prev_right = None
        for c in row:
            left = c["pos"][0]
            if prev_right is not None:
                # allow tiny float fuzz but enforce the floor
                assert left - prev_right >= threshold - 0.01, (
                    f"components too close on row {_y}: {c['id']}"
                )
            prev_right = left + c["size"][0]


def test_generate_specs_returns_full_set(registry: CompanyRegistry) -> None:
    specs = generate_specs(registry)
    kinds = {s.diagram_type for s in specs}
    assert kinds == {"architecture", "workflow", "sequence", "dataflow"}
    assert all(s.data for s in specs)


def test_architecture_leadership_structure(registry: CompanyRegistry) -> None:
    arch = build_architecture(registry, scope="leadership")
    assert arch["diagram_type"] == "architecture"
    assert arch["meta"]["quality_profile"] == "standard"
    ids = {c["id"] for c in arch["components"]}
    # leadership scope includes executives + board
    assert {"board-chair", "human-ceo", "cto", "cfo", "cdo"} <= ids
    # board chair reports to human-ceo
    assert any(
        conn.get("from") == "board-chair" and conn.get("to") == "human-ceo"
        for conn in arch.get("connections", [])
    )
    _validate_layout(arch)


def test_architecture_full_scope_has_boundaries(registry: CompanyRegistry) -> None:
    # add a second engineer so the Engineering department has >= 2 members and
    # emits a department boundary
    extra = Executive(
        id="vp_engineering",
        name="VP Engineering",
        title="VP Engineering",
        department="Engineering",
        reports_to="cto",
    )
    registry.executives = list(registry.executives) + [extra]
    arch = build_architecture(registry, scope="full")
    assert arch["meta"]["quality_profile"] == "standard"
    assert any(b["label"] == "Engineering" for b in arch.get("boundaries", [])), (
        "full scope expects at least the Engineering department boundary"
    )
    _validate_layout(arch)


def test_workflow_build(registry: CompanyRegistry) -> None:
    wf = build_workflow(registry, workflow_id="hiring")
    assert wf["diagram_type"] == "workflow"
    assert wf["meta"]["quality_profile"] == "showcase"
    assert "hiring" in wf["meta"]["title"].lower()


def test_sequence_build(registry: CompanyRegistry) -> None:
    seq = build_sequence(registry, workflow_id="hiring")
    assert seq["diagram_type"] == "sequence"
    assert seq["meta"]["quality_profile"] == "showcase"


def test_dataflow_build(registry: CompanyRegistry) -> None:
    df = build_dataflow(registry, workflow_id="hiring")
    assert df["diagram_type"] == "dataflow"
    assert df["meta"]["quality_profile"] == "showcase"


def test_json_serializable(registry: CompanyRegistry, tmp_path: Path) -> None:
    for spec in generate_specs(registry):
        target = tmp_path / spec.json_name
        target.write_text(json.dumps(spec.data), encoding="utf-8")
        assert target.exists()
