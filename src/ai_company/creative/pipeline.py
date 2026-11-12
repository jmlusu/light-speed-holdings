#!/usr/bin/env python3
"""Creative production pipeline — the Creative Director's execution path.

Stages (each persisted to ``manifest.json`` as it completes):

1. **Route**     — interpret the brief, pick the skill chain + specialist,
                   resolve the model route through the existing ``ModelRouter``
                   (``routing.route_brief``).
2. **Produce**   — select an available, wired tool adapter and write outputs
                   into the run directory.
3. **QA**        — artifact QA gate (default: deterministic brand/output
                   checks; pluggable so ``ls-artifact-qa`` style checks can be
                   supplied by the executor).
4. **Approve**   — human approval gate. Only offered after QA passes, and QA
                   pass is never recorded as approval. The approver callable
                   represents the Human CEO's decision.

Failure handling: any production exception or missing adapter marks the run
``failed`` with the error recorded; rerun by calling ``run_production`` again
with ``retry_of=<failed run_id>`` — the new manifest links back to the failure.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from ai_company.creative.adapters import AdapterRegistry, default_registry
from ai_company.creative.models import (
    ApprovalRecord,
    ApprovalStatus,
    CreativeBrief,
    ExecutionManifest,
    QaResult,
    QaVerdict,
    RunStatus,
    utc_now,
)
from ai_company.creative.routing import route_brief
from ai_company.creative.store import default_out_root, save_manifest

if TYPE_CHECKING:
    from ai_company.model_router import ModelRouter

#: Suffixes read for content checks during default QA.
READABLE_SUFFIXES: frozenset[str] = frozenset(
    {".md", ".json", ".txt", ".html", ".css", ".tsx", ".ts", ".py"}
)

LEGACY_RED = "#E63946"
CANONICAL_RED = "#DC3641"


@dataclass(frozen=True)
class ApprovalDecision:
    """Outcome of the human approval gate for one run."""

    approved: bool
    by: str = "human_ceo"
    note: str = ""


#: QA hook: full manifest + run directory -> verdict. Pluggable per run.
QaCheck = Callable[[ExecutionManifest, Path], QaResult]

#: Approval hook: full manifest -> decision. Represents the Human CEO.
Approver = Callable[[ExecutionManifest], ApprovalDecision]


def default_qa(manifest: ExecutionManifest, run_dir: Path) -> QaResult:
    """Deterministic artifact QA: outputs exist, brand tokens reconciled.

    Checks:
      * ``outputs_exist``   — every recorded output exists and is non-empty
      * ``no_legacy_red``   — no readable output carries the legacy red ``#E63946``
      * ``brand_tokens``    — canonical red ``#DC3641`` detected (else skipped,
        with a note, for palette-free artifacts)

    Deeper visual/UX/accessibility review is the ``ls-artifact-qa`` gate run
    by the specialist agent; this check is the offline floor.
    """
    checks: dict[str, str] = {}
    notes: list[str] = []
    outputs = manifest.outputs

    missing = [p for p in outputs if not Path(p).exists() or Path(p).stat().st_size == 0]
    if not outputs:
        checks["outputs_exist"] = "fail"
        notes.append("no outputs recorded for the run")
    elif missing:
        checks["outputs_exist"] = "fail"
        notes.append("missing or empty outputs: " + ", ".join(missing))
    else:
        checks["outputs_exist"] = "pass"

    legacy_hits: list[str] = []
    canonical_seen = False
    readable = 0
    for item in outputs:
        path = Path(item)
        if path.suffix.lower() not in READABLE_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore").upper()
        except OSError:
            continue
        readable += 1
        if LEGACY_RED in text:
            legacy_hits.append(item)
        if CANONICAL_RED in text:
            canonical_seen = True

    if legacy_hits:
        checks["no_legacy_red"] = "fail"
        notes.append("legacy red #E63946 found in: " + ", ".join(legacy_hits))
    else:
        checks["no_legacy_red"] = "pass"

    if canonical_seen:
        checks["brand_tokens"] = "pass"
    elif readable:
        checks["brand_tokens"] = "skipped"
        notes.append("no canonical brand red #DC3641 detected in readable outputs")
    else:
        checks["brand_tokens"] = "skipped"
        notes.append("no readable outputs to scan for brand tokens")

    failed = any(value == "fail" for value in checks.values())
    return QaResult(
        verdict=QaVerdict.FAIL if failed else QaVerdict.PASS,
        checks=checks,
        notes=notes,
    )


def run_production(
    brief: CreativeBrief,
    *,
    out_root: Path | None = None,
    project_root: Path | None = None,
    router: ModelRouter | None = None,
    registry: AdapterRegistry | None = None,
    qa: QaCheck | None = None,
    approver: Approver | None = None,
    priority: str = "medium",
    retry_of: str | None = None,
) -> ExecutionManifest:
    """Run the full creative pipeline for a brief and return its manifest.

    The manifest is persisted after every stage transition, so an interrupted
    or failed run remains fully inspectable and retryable.
    """
    out = Path(out_root) if out_root is not None else default_out_root(project_root)
    manifest = route_brief(
        brief,
        router=router,
        priority=priority,
        project_root=project_root,
        retry_of=retry_of,
    )
    save_manifest(manifest, out)

    adapters = registry if registry is not None else default_registry()
    manifest.adapters = adapters.statuses()
    manifest.touch()
    save_manifest(manifest, out)

    adapter = adapters.select(brief.artifact_type)
    if adapter is None:
        manifest.status = RunStatus.FAILED
        detail = "; ".join(
            f"{status.name}={'yes' if status.available else 'no'}" for status in manifest.adapters
        )
        manifest.errors.append(
            f"no available production adapter for '{brief.artifact_type.value}' ({detail})"
        )
        manifest.touch()
        save_manifest(manifest, out)
        return manifest

    run_directory = out / manifest.run_id
    manifest.status = RunStatus.PRODUCING
    manifest.touch()
    save_manifest(manifest, out)

    try:
        outputs = adapter.produce(brief, run_directory)
    except Exception as exc:  # noqa: BLE001 — record failure, never lose the manifest
        manifest.status = RunStatus.FAILED
        manifest.errors.append(f"production failed via adapter '{adapter.name}': {exc}")
        manifest.touch()
        save_manifest(manifest, out)
        return manifest

    manifest.outputs = [str(item) for item in outputs]
    manifest.touch()
    save_manifest(manifest, out)

    manifest.status = RunStatus.QA
    manifest.touch()
    qa_check = qa if qa is not None else default_qa
    manifest.qa = qa_check(manifest, run_directory)
    manifest.touch()
    save_manifest(manifest, out)

    if not manifest.qa.passed:
        manifest.warnings.append(
            "QA failed — approval gate not offered; fix the artifact and rerun"
        )
        manifest.touch()
        save_manifest(manifest, out)
        return manifest

    manifest.status = RunStatus.AWAITING_APPROVAL
    manifest.touch()
    save_manifest(manifest, out)

    if approver is None:
        manifest.warnings.append(
            "QA passed but no approver supplied — run parked awaiting CEO approval"
        )
        manifest.touch()
        save_manifest(manifest, out)
        return manifest

    decision = approver(manifest)
    manifest.approval = ApprovalRecord(
        status=ApprovalStatus.APPROVED if decision.approved else ApprovalStatus.REJECTED,
        approved_by=decision.by,
        decided_at=utc_now(),
        note=decision.note,
        qa_passed=True,
    )
    manifest.status = RunStatus.APPROVED if decision.approved else RunStatus.REJECTED
    manifest.touch()
    save_manifest(manifest, out)
    return manifest
