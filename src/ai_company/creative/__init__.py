#!/usr/bin/env python3
"""Consolidated creative production engine.

Public surface:

* ``CreativeBrief`` / ``ExecutionManifest`` — the brief and manifest contracts
* ``route_brief`` — Creative Director routing (chain + specialist + model route)
* ``run_production`` — the full route -> produce -> QA -> approval pipeline
* ``AdapterRegistry`` / ``default_registry`` — replaceable tool adapters
* ``save_manifest`` / ``load_manifest`` / ``list_runs`` — run persistence
"""

from __future__ import annotations

from ai_company.creative.adapters import (
    AdapterRegistry,
    ComfyUIAdapter,
    OpenDesignAdapter,
    PresentationAdapter,
    ToolAdapter,
    default_registry,
)
from ai_company.creative.models import (
    AdapterStatus,
    AgentAssignments,
    ApprovalRecord,
    ApprovalStatus,
    ArtifactType,
    CreativeBrief,
    ExecutionManifest,
    QaResult,
    QaVerdict,
    RouteInfo,
    RunStatus,
    SkillChain,
)
from ai_company.creative.pipeline import (
    ApprovalDecision,
    Approver,
    QaCheck,
    default_qa,
    run_production,
)
from ai_company.creative.routing import (
    ROUTES,
    ProductionRoute,
    build_chain,
    route_brief,
    specialist_for,
)
from ai_company.creative.store import (
    default_out_root,
    list_runs,
    load_manifest,
    run_dir,
    save_manifest,
)

__all__ = [
    "ROUTES",
    "AdapterRegistry",
    "AdapterStatus",
    "AgentAssignments",
    "ApprovalDecision",
    "ApprovalRecord",
    "ApprovalStatus",
    "Approver",
    "ArtifactType",
    "ComfyUIAdapter",
    "CreativeBrief",
    "ExecutionManifest",
    "OpenDesignAdapter",
    "PresentationAdapter",
    "ProductionRoute",
    "QaCheck",
    "QaResult",
    "QaVerdict",
    "RouteInfo",
    "RunStatus",
    "SkillChain",
    "ToolAdapter",
    "build_chain",
    "default_out_root",
    "default_qa",
    "default_registry",
    "list_runs",
    "load_manifest",
    "route_brief",
    "run_dir",
    "run_production",
    "save_manifest",
    "specialist_for",
]
