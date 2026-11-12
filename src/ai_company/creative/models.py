#!/usr/bin/env python3
"""Creative production data models.

Defines the two contracts of the consolidated creative engine:

1. ``CreativeBrief`` — the structured intake handed to the Creative Director.
   It mirrors the five-question intake and brief block defined by the
   ``ls-creative-director`` skill (artifact type, audience, objective,
   narrative, visual language) plus the handoff fields (structure, channels,
   CTA, QA scope, source research).

2. ``ExecutionManifest`` — the per-run record produced by the pipeline:
   skill chain, agent assignments, model route, adapter availability,
   outputs, QA verdict, human approval, warnings and errors. One manifest
   per run, persisted as ``manifest.json`` next to the run's outputs.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


def utc_now() -> str:
    """Current UTC time as an ISO-8601 string (second precision)."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_run_id() -> str:
    """Generate a sortable, unique run identifier (``cr-<stamp>-<rand>``)."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"cr-{stamp}-{uuid4().hex[:6]}"


class ArtifactType(str, Enum):
    """Artifact classes the Creative Director routes (ls-creative-director table)."""

    WEBSITE = "website"
    DECK = "deck"
    WHITEPAPER = "whitepaper"
    CAMPAIGN = "campaign"
    AD = "ad"
    DIAGRAM = "diagram"
    INFOGRAPHIC = "infographic"
    DOCS = "docs"


class RunStatus(str, Enum):
    """Lifecycle of one creative production run."""

    CREATED = "created"
    ROUTED = "routed"
    PRODUCING = "producing"
    QA = "qa"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    FAILED = "failed"


class QaVerdict(str, Enum):
    """Outcome of the artifact QA gate."""

    PENDING = "pending"
    PASS = "pass"
    FAIL = "fail"


class ApprovalStatus(str, Enum):
    """Outcome of the human (CEO) approval gate.

    QA pass is never approval: the two gates are recorded separately.
    """

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class CreativeBrief(BaseModel):
    """Structured creative brief — the intake contract of the creative engine."""

    model_config = ConfigDict(extra="ignore")

    title: str = Field(..., min_length=1, description="Short human label for the deliverable")
    artifact_type: ArtifactType = Field(..., description="Class of output to produce")
    audience: str = Field(..., min_length=1, description="Who consumes it and what they care about")
    objective: str = Field(
        ..., min_length=1, description="The behaviour change the artifact must cause"
    )
    core_thesis: str = Field(..., min_length=1, description="The core message in 1-2 sentences")
    narrative_arc: str = Field(
        default="", description="Hook -> proof -> evidence -> close, if known"
    )
    visual_language: str = Field(
        default="lightspeed-design-system",
        description="Design language; defaults to the LightSpeed design system",
    )
    brand_base: str = Field(
        default="LightSpeed design system", description="Always the LightSpeed design system"
    )
    structure: list[str] = Field(
        default_factory=list, description="Section/page/slide outline if known"
    )
    channels: list[str] = Field(
        default_factory=list, description="Distribution channels (campaigns)"
    )
    cta: str = Field(default="", description="The single action requested of the audience")
    qa_scope: list[str] = Field(
        default_factory=lambda: ["visual", "brand", "ux", "content", "accessibility"],
        description="ls-artifact-qa checklist scope for this artifact",
    )
    source_research: list[str] = Field(
        default_factory=list,
        description="Repo-relative paths to research/knowledge sources the artifact must be built on",
    )
    format_hint: str = Field(
        default="",
        description="Optional format discriminator (e.g. deck_type: investor_pitch|board_meeting|keynote|training)",
    )

    def production_payload(self) -> dict[str, str]:
        """Bridge to the existing presentation pipeline brief dict.

        ``ai_company.presentation.pipeline.generate_content_from_brief``
        expects ``topic``/``audience``/``objective``/``narrative`` keys.
        """
        narrative = self.core_thesis
        if self.narrative_arc:
            narrative = f"{self.core_thesis} {self.narrative_arc}"
        return {
            "topic": self.title,
            "audience": self.audience,
            "objective": self.objective,
            "narrative": narrative,
        }


class RouteInfo(BaseModel):
    """Resolved model route (from the existing ModelRouter) for the run."""

    provider: str
    model: str
    tier: str
    reason: str
    agent: str = Field(default="", description="Agent name the route was resolved for")


class SkillChain(BaseModel):
    """The ls-creative-director skill chain chosen for the brief."""

    primary: str = Field(..., description="Exactly one primary production skill")
    brand_base: str = Field(default="ls-design-system", description="Always loaded first")
    support: list[str] = Field(default_factory=list, description="Optional additive support skills")
    qa_gate: str = Field(default="ls-artifact-qa", description="Always runs last before delivery")


class AgentAssignments(BaseModel):
    """Who interprets and who produces."""

    director: str = Field(default="creative-director", description="Orchestration entry point")
    specialist: str = Field(..., description="Production specialist agent (registry name)")
    specialist_known: bool = Field(
        default=True,
        description="Whether the specialist exists in company/agent-registry.json",
    )


class AdapterStatus(BaseModel):
    """Availability snapshot for one registered tool adapter."""

    name: str
    available: bool
    wired: bool = Field(description="Whether this pipeline can produce with the adapter today")
    detail: str = ""


class QaResult(BaseModel):
    """Artifact QA gate result (ls-artifact-qa scope recorded on the brief)."""

    verdict: QaVerdict = QaVerdict.PENDING
    checks: dict[str, str] = Field(
        default_factory=dict, description="check name -> pass|fail|skipped"
    )
    notes: list[str] = Field(default_factory=list)

    @property
    def passed(self) -> bool:
        """True only when every executed check passed."""
        return self.verdict is QaVerdict.PASS and all(v != "fail" for v in self.checks.values())


class ApprovalRecord(BaseModel):
    """Human approval gate. QA pass is recorded here but is NOT approval."""

    status: ApprovalStatus = ApprovalStatus.PENDING
    approved_by: str | None = Field(default=None, description="Who decided (e.g. human_ceo)")
    decided_at: str | None = None
    note: str = ""
    qa_passed: bool = Field(
        default=False, description="Whether QA passed before the gate was offered"
    )


class ExecutionManifest(BaseModel):
    """Per-run execution manifest: routing, production, QA, approval, failures."""

    model_config = ConfigDict(extra="ignore")

    run_id: str
    created_at: str
    updated_at: str
    status: RunStatus = RunStatus.CREATED
    brief: CreativeBrief
    chain: SkillChain | None = None
    agents: AgentAssignments | None = None
    route: RouteInfo | None = None
    adapters: list[AdapterStatus] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    qa: QaResult = Field(default_factory=QaResult)
    approval: ApprovalRecord = Field(default_factory=ApprovalRecord)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    retry_of: str | None = Field(
        default=None, description="run_id of the failed run this run retries"
    )

    @classmethod
    def new(cls, brief: CreativeBrief, retry_of: str | None = None) -> ExecutionManifest:
        """Create a fresh manifest for a brief."""
        now = utc_now()
        return cls(
            run_id=new_run_id(), created_at=now, updated_at=now, brief=brief, retry_of=retry_of
        )

    def touch(self) -> None:
        """Bump ``updated_at`` after a mutation."""
        self.updated_at = utc_now()
