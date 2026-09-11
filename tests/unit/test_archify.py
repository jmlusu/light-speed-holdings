"""Tests for the Archify diagram converter (registry -> JSON IR).

These unit tests are hermetic: they build a small synthetic registry and check
the generated JSON IR structure and layout invariants without invoking Node.js
(the renderer/validation path is covered separately by the CLI + CI gate).
"""

from __future__ import annotations

import json
from pathlib import Path
from zlib import crc32

import pytest

from ai_company.archify.converter import (
    _dept_dot,
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


# ---------------------------------------------------------------------------
# Regression guards for the CI "Validate all four diagrams" gate
# (cwd fix b220529 + deterministic dept colors 9e7e7b7)
# ---------------------------------------------------------------------------


def test_run_cli_uses_project_root_cwd(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """The Archify CLI must run with the project root as cwd (b220529).

    Regression for the CI ENOENT: relative inputs like
    ``docs/diagrams/architecture.json`` were resolved under
    ``.opencode/skills/archify`` because the subprocess cwd was the skill
    directory rather than the repository root.
    """
    from ai_company.archify import renderer as archify_renderer
    from ai_company.paths import get_project_root

    bin_path = tmp_path / "bin" / "archify.mjs"
    bin_path.parent.mkdir(parents=True)
    bin_path.write_text("#!/usr/bin/env node\n", encoding="utf-8")

    captured: dict[str, object] = {}

    class _FakeProc:
        returncode = 0
        stdout = "{}"
        stderr = ""

    class _FakeSubprocess:
        def run(self, *args: object, **kwargs: object) -> _FakeProc:
            captured["args"] = args
            captured["kwargs"] = kwargs
            return _FakeProc()

    monkeypatch.setattr(archify_renderer, "_node_available", lambda: True)
    monkeypatch.setattr(archify_renderer, "subprocess", _FakeSubprocess())

    archify_renderer._run_cli(
        bin_path,
        [
            "validate",
            "architecture",
            "docs/diagrams/architecture.json",
            "--quality",
            "standard",
            "--json",
        ],
    )

    kwargs = captured["kwargs"]
    assert isinstance(kwargs, dict)
    assert kwargs.get("cwd") == str(get_project_root())


def test_dept_dot_deterministic_across_calls() -> None:
    """Department card dot colors must be stable (9e7e7b7).

    Uses ``crc32`` instead of ``hash()`` so the output is independent of the
    per-process ``PYTHONHASHSEED`` randomization that made regenerated diagram
    JSON drift between CI runs.
    """
    palette = ["cyan", "emerald", "rose", "orange", "violet", "amber", "slate"]
    for dept in ("Engineering", "Finance", "Data", "Office of the CEO", "HR"):
        first = _dept_dot(dept)
        assert first == palette[crc32(dept.encode("utf-8")) % len(palette)]
        for _ in range(10):
            assert _dept_dot(dept) == first


def test_dept_dot_empty_defaults_first_palette_color() -> None:
    assert _dept_dot("") == "cyan"
