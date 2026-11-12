#!/usr/bin/env python3
"""Creative Director routing: brief -> skill chain, specialist, model route.

Implements the ``ls-creative-director`` routing table inside the runtime, so a
brief can be routed deterministically instead of re-derived by every agent:

* exactly one primary production skill, ``ls-design-system`` always first,
  ``ls-artifact-qa`` always last;
* one production specialist agent per artifact type (validated against
  ``company/agent-registry.json``);
* the model route comes from the existing ``ModelRouter`` — no second routing
  system is introduced here.

It also connects the knowledge workflow: content-heavy briefs are checked for
``source_research`` links (``research/``, ``knowledge/``) so production does
not invent facts.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING

from ai_company.creative.models import (
    AgentAssignments,
    ArtifactType,
    CreativeBrief,
    ExecutionManifest,
    RouteInfo,
    RunStatus,
    SkillChain,
)
from ai_company.paths import get_project_root

if TYPE_CHECKING:
    from ai_company.model_router import ModelRouter

DIRECTOR_AGENT = "creative-director"
BRAND_BASE_SKILL = "ls-design-system"
QA_GATE_SKILL = "ls-artifact-qa"

# Brief types whose long-form content must rest on existing research
# (ls-creative-director rule 5: production skills may not invent facts).
CONTENT_HEAVY: frozenset[ArtifactType] = frozenset(
    {
        ArtifactType.WHITEPAPER,
        ArtifactType.CAMPAIGN,
        ArtifactType.DOCS,
        ArtifactType.INFOGRAPHIC,
    }
)


@dataclass(frozen=True)
class ProductionRoute:
    """One row of the Creative Director routing table."""

    primary: str
    specialist: str
    support: tuple[str, ...] = ()


# Mirrors the routing table in the ls-creative-director skill. The specialist
# is the registry agent that owns the matching production capability.
ROUTES: dict[ArtifactType, ProductionRoute] = {
    ArtifactType.WEBSITE: ProductionRoute(
        primary="ls-frontend-design",
        specialist="lead-frontend",
        support=("ls-diagramming", "ls-visual-storytelling"),
    ),
    ArtifactType.DECK: ProductionRoute(
        primary="ls-presentation-design",
        specialist="product-marketing-manager",
        support=("ls-diagramming", "ls-visual-storytelling"),
    ),
    ArtifactType.WHITEPAPER: ProductionRoute(
        primary="ls-document-design",
        specialist="thought-leadership-author",
        support=("ls-diagramming", "ls-visual-storytelling"),
    ),
    ArtifactType.CAMPAIGN: ProductionRoute(
        primary="ls-social-media-design",
        specialist="social-media-manager",
        support=("ls-visual-storytelling", "ls-brand-advertising"),
    ),
    ArtifactType.AD: ProductionRoute(
        primary="ls-brand-advertising",
        specialist="content-creator",
        support=("ls-social-media-design",),
    ),
    ArtifactType.DIAGRAM: ProductionRoute(
        primary="ls-diagramming",
        specialist="technical-documentation-lead",
    ),
    ArtifactType.INFOGRAPHIC: ProductionRoute(
        primary="ls-visual-storytelling",
        specialist="content-creator",
        support=("ls-diagramming",),
    ),
    ArtifactType.DOCS: ProductionRoute(
        primary="ls-documentation-engineering",
        specialist="technical-documentation-lead",
    ),
}


def build_chain(artifact_type: ArtifactType) -> SkillChain:
    """Build the skill chain for an artifact type (brand first, QA last)."""
    route = ROUTES[artifact_type]
    return SkillChain(
        primary=route.primary,
        brand_base=BRAND_BASE_SKILL,
        support=list(route.support),
        qa_gate=QA_GATE_SKILL,
    )


def specialist_for(artifact_type: ArtifactType) -> str:
    """Registry name of the production specialist for an artifact type."""
    return ROUTES[artifact_type].specialist


def default_registry_path() -> Path:
    """Path of the agent registry used for model routing and validation."""
    return get_project_root() / "company" / "agent-registry.json"


@lru_cache(maxsize=8)
def _agent_names(registry_path: str) -> frozenset[str]:
    """Known agent names from an agent-registry.json file (cached by path)."""
    path = Path(registry_path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return frozenset()
    if not isinstance(data, list):
        return frozenset()
    names: set[str] = set()
    for entry in data:
        if isinstance(entry, dict):
            name = entry.get("name")
            if isinstance(name, str):
                names.add(name)
    return frozenset(names)


def specialist_known(specialist: str, registry_path: Path | None = None) -> bool:
    """Whether the specialist exists in the agent registry."""
    path = registry_path or default_registry_path()
    return specialist in _agent_names(str(path))


def knowledge_warnings(brief: CreativeBrief, project_root: Path) -> list[str]:
    """Warnings that connect a brief to the knowledge/research workflow."""
    warnings: list[str] = []
    if not brief.source_research:
        if brief.artifact_type in CONTENT_HEAVY:
            warnings.append(
                "no source_research linked — attach research from research/ or knowledge/ "
                "before production; production skills must not invent facts"
            )
        return warnings
    for ref in brief.source_research:
        candidate = Path(ref)
        if candidate.is_absolute():
            exists = candidate.exists()
        else:
            exists = (project_root / candidate).exists() or candidate.exists()
        if not exists:
            warnings.append(f"source_research path not found: {ref}")
    return warnings


def resolve_model_route(
    brief: CreativeBrief,
    *,
    router: ModelRouter | None = None,
    priority: str = "medium",
) -> RouteInfo:
    """Resolve the model route for the production specialist via ModelRouter."""
    if router is None:
        from ai_company.model_router import ModelRouter

        root = get_project_root()
        router = ModelRouter(
            config_path=str(root / "company" / "models.yaml"),
            registry_path=str(root / "company" / "agent-registry.json"),
        )
    specialist = specialist_for(brief.artifact_type)
    route = router.resolve(
        agent_name=specialist,
        agent_type="Specialist",
        priority=priority,
        task_prompt=f"{brief.title}: {brief.core_thesis}",
    )
    return RouteInfo(
        provider=route.provider,
        model=route.model,
        tier=route.tier,
        reason=route.reason,
        agent=specialist,
    )


def route_brief(
    brief: CreativeBrief,
    *,
    router: ModelRouter | None = None,
    priority: str = "medium",
    project_root: Path | None = None,
    retry_of: str | None = None,
) -> ExecutionManifest:
    """Interpret and route a brief into a new execution manifest.

    Fills chain, agents, model route and knowledge warnings, then marks the
    manifest ``routed``. Never raises for environment problems: a failed model
    route becomes a warning so the run can still be inspected and retried.
    """
    root = Path(project_root) if project_root is not None else get_project_root()
    manifest = ExecutionManifest.new(brief, retry_of=retry_of)
    manifest.chain = build_chain(brief.artifact_type)

    specialist = specialist_for(brief.artifact_type)
    known = specialist_known(specialist, root / "company" / "agent-registry.json")
    manifest.agents = AgentAssignments(specialist=specialist, specialist_known=known)
    if not known:
        manifest.warnings.append(f"specialist '{specialist}' not found in agent registry")

    try:
        manifest.route = resolve_model_route(brief, router=router, priority=priority)
    except Exception as exc:  # noqa: BLE001 — routing must not kill the run
        manifest.warnings.append(f"model route unresolved: {exc}")

    manifest.warnings.extend(knowledge_warnings(brief, root))
    manifest.status = RunStatus.ROUTED
    manifest.touch()
    return manifest
