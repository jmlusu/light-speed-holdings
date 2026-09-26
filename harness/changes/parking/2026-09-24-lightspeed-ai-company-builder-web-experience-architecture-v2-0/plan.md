# Plan

## Technical Approach

1. Docs-only authoring under `docs/architecture/` driven by the current-state baseline in `summary.md`.
2. Parallel workstreams (per brief §33 allocation) — proposed subagent mapping:
   - Chief-of-staff / solution-architect: primary v2 doc synthesis + Mermaid system diagrams.
   - Registry-owner: `AGENT_CONSOLIDATION_152_TO_90.md` + `AI_WORKFORCE_90.md` (facts from registry/departments/source-of-truth).
   - Product-designer + lead-frontend: `WEB_INFORMATION_ARCHITECTURE_V2.md` + `AI_COMPANY_BUILDER_UX.md` + `ROUTE_MIGRATION_V2.md` (from App.tsx inventory + vercel conflicts).
   - Security-architect: `PUBLIC_INTERNAL_BOUNDARY.md`.
   - Data-engineer: `PUBLIC_AGENT_REGISTRY_SCHEMA.md` (YAML↔JSON↔TS contract).
   - Technical-documentation-lead: `EVIDENCE_ARCHITECTURE.md` + `V2_IMPLEMENTATION_ROADMAP.md`.
   - Solution-architect (Architecture Lead role): primary v2 doc synthesis + Mermaid D1–D12.
   - Solution-architect / governance: ADRs 025+ under `docs/architecture/adr/` (BRIEF_LOCK path); note historical duplicate 020 in docs/adr/ without rename.
4. Synthesis last: one pass for cross-links, count consistency, Mermaid validity.

## Impacted Modules And Files

- Create: `docs/architecture/LIGHTSPEED_AI_COMPANY_BUILDER_WEB_ARCHITECTURE_V2.md`
- Create: `docs/architecture/AGENT_CONSOLIDATION_152_TO_90.md`
- Create: `docs/architecture/AI_WORKFORCE_90.md`
- Create: `docs/architecture/PUBLIC_INTERNAL_BOUNDARY.md`
- Create: `docs/architecture/WEB_INFORMATION_ARCHITECTURE_V2.md`
- Create: `docs/architecture/PUBLIC_AGENT_REGISTRY_SCHEMA.md`
- Create: `docs/architecture/ROUTE_MIGRATION_V2.md`
- Create: `docs/architecture/EVIDENCE_ARCHITECTURE.md`
- Create: `docs/architecture/AI_COMPANY_BUILDER_UX.md`
- Create: `docs/architecture/V2_IMPLEMENTATION_ROADMAP.md`
- Create: ADR files (025+ under agreed path)
- Update: this ECL folder only (spec/plan/tasks/summary)
- Read-only inputs: `company-registry.yaml`, `company/departments.yaml`, `company/agent-registry.json`, `docs/source-of-truth.yaml`, `src/App.tsx`, `vercel.json`, `src/data/*`, `docs/adr/*`, `src/ai_company/orchestrator/*`, `src/ai_company/executor/*`

## Interfaces, Data, Permissions

- No runtime interfaces changed. Public agent registry schema is documentation of an existing/future contract only.
- No secrets, no generated outputs, no `.env`.

## Spec Gaps Found From Planning

- Full brief text now provided; locked in BRIEF_LOCK.md + Resolved Clarifications.
- Live deployment comparison (3 URLs) in-scope per §7.4 — execute during baseline appendix.

## Risks And Mitigations

- Risk: wrong deliverable list if reconstruction differs from brief → Mitigation: confirm brief before final synthesis; filenames are cheap to rename pre-commit.
- Risk: count drift reintroduced in new docs → Mitigation: cite source-of-truth.yaml (90/20) everywhere; run validate-drift after write.
- Risk: too much parallel drift between 9 artifacts → Mitigation: primary doc owns thesaurus/section skeleton; artifacts link back with fixed IDs.

## Verification Plan

- File presence: all 10 architecture docs + ADRs.
- `pwsh scripts/lint-ecl.ps1`
- `pwsh scripts/validate-drift.ps1` (expect green; no claim changes)
- Grep new docs for `152 agents` / `145 agents` outside historical/triage context → must be intentional.
- Mermaid blocks: parse-level sanity (no unclosed fences).
