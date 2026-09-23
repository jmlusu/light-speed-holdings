# Plan

## Technical Approach

- Deliver a single canonical narrative document plus a machine-checkable claims/evidence layer so every site number traces to provenance.
- Keep Ask LightSpeed rule-based (no LLM) for this change.
- Resolve parallel-work conflicts in favour of the newer Updated-upstream state (152-agent registry).

## Impacted Modules And Files

- `docs/NARRATIVE-AND-POSITIONING.md` (new)
- `research/site-claims-index.yaml`, `research/site-claims-ledger.md`, `research/site-claims-audit.md`
- `docs/content-architecture/entities/**` (~60 YAML entities + `index.yaml`)
- `analysis_taxonomy.md`, `knowledge-model-analysis.md`, `seo-specialist-analysis.md`
- `src/data/siteContent.ts`, `src/data/useCaseCatalogData.ts`, `src/pages/EvidencePage.tsx` (claim:034 re-badge)
- Conflict-resolved: `docs/AGENT-REGISTRY-TABLE.md`, `hr/onboarding_requests.yaml`, `orchestrator/approvals.yaml` (gitignored)

## Interfaces, Data, Permissions

- Claims use positional IDs `claim:001`..`claim:067`; entities may reference them via `evidence_references`.
- Brand palette and terminology fixed: navy #070A40 / red #E63946 / cyan #00BFFF, Arial, 4px grid, tagline ASPIRE. ACT. ACHIEVE.
- Canonical count: 152 agents (151 AI + 1 human CEO) across 20 departments.

## Spec Gaps Found From Planning

- 26 plain `(b)` self-reported claims remain unremediated (acceptable while honesty-badged).
- Content Architecture Council remains registry-only (no generated agent cards) — parked, closed.

## Risks And Mitigations

- Drift between narrative copy and registry counts — mitigated by `scripts/validate-drift.ps1` (87-file check, green).
- Stash conflicts reintroducing stale 144-agent data — mitigated by keeping Updated upstream and revalidating YAML.

## Verification Plan

- `scripts/validate-drift.ps1`, `tests/docs/test_doc_drift.py`, `pwsh scripts/lint-ecl.ps1` — all passed.
- `bun run build` — green.
- YAML safe_load on conflict-resolved files — OK.
