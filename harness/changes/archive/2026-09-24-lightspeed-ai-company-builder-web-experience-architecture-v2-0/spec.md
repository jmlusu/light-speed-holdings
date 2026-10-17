# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: requirement-first
- Questions asked this round: 1 (brief confirmation — resolved; see Resolved Clarifications)

## Goal And Evidence

- Real problem or user request: Author the authoritative "LightSpeed AI Company Builder + Web Experience Architecture v2.0" document plus 9 supporting artifacts, new ADRs, and Mermaid diagrams under `docs/architecture/`. Establish discovery → current-state baseline → target model → migration path before any code rewrite. Assemble relevant agents per §33 work allocation.
- Current behavior: `docs/architecture/` contains only `LS-MEM-RECONNAISSANCE.md`. No v2 deliverables exist. Hybrid repo (Python builder + React site) with completed 152→90 registry trim but residual doc drift and route/redirect conflicts.
- Source of evidence: This session's discovery (registry 90/90/90, App.tsx routes, vercel.json, departments.yaml, source-of-truth.yaml, docs/adr/*, active ECL baseline in summary.md).

## User Scenarios And Success

- Primary user/system scenario: CEO/architect reads primary v2 doc and can navigate to each of the 9 supporting artifacts, ADRs, and diagrams for implementation planning; engineering team uses roadmap + route migration for execution.
- Success criteria:
  - Primary doc exists at `docs/architecture/LIGHTSPEED_AI_COMPANY_BUILDER_WEB_ARCHITECTURE_V2.md` with Mermaid diagrams.
  - All 9 supporting artifacts exist with the exact filenames from the brief §34.
  - New ADRs recorded (continue from 025; resolve 020 collision).
  - Baseline numbers (90 agents / 20 departments / route inventory) are accurate and cross-referenced.
- Acceptance criteria: Files present, internally consistent counts, lint-ecl green, no registry/code mutation unless separately approved.

## Non-Goals

- Regenerating agent cards or changing `company-registry.yaml`.
- Implementing route code changes (migration is documented, not executed, in this change).
- Deploying or comparing live deployment URLs via network unless user requests it.

## Constraints

- One active ECL change (this one). Do not hand-edit INDEX.json.
- Docs-only / harness-only writes under `docs/architecture/`, `docs/adr/` (or agreed ADR path), and this change folder.
- Canonical tool vocabulary and safety boundaries from AGENTS.md §8–9 apply to any delegated work.

## Assumptions

- Brief §34 deliverable filenames confirmed against user-provided full brief (2026-09-24).
- ADRs: continue numbering from 025; preferred location `docs/adr/` (existing convention) with cross-link from `docs/architecture/`.

## Open Questions

- None blocking. (Decision framework §37 applied per recommendation.)

## Resolved Clarifications

- 2026-09-24: Full brief provided by user. §34 filenames locked (match plan.md exactly). ADR path = `docs/architecture/adr/` per §35 (not docs/adr/). Nine supporting artifacts + primary + 12 Mermaid diagrams + ADRs confirmed. Deployment comparison (GitHub/Vercel/AI Studio) is in-scope per §7.4.
