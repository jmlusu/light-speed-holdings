# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Discovery + current-state baseline → `harness/changes/active/summary.md`. (Done 2026-09-24)
- [x] T002 [P] Confirm full brief text (§33–§35) with user; lock deliverable filenames in plan.md. (Done 2026-09-24 — BRIEF_LOCK.md)

## Implementation

- [x] T003 [P] Author `docs/architecture/AGENT_CONSOLIDATION_152_TO_90.md` (registry-owner). Validation: cites e2bdb0c7 + source-of-truth 90/20. (Done 2026-09-24 — 62 removed = 49 MERGE + 10 REASSIGN + 2 REDEFINE + 1 RETIRE; 90 RETAIN)
- [x] T004 [P] Author `docs/architecture/AI_WORKFORCE_90.md` (registry-owner). Validation: 90 = 64 specialist + 19 executive + 7 board; departments table matches departments.yaml. (Done 2026-09-24 — census verified; 7 MANDATORY §9 fields missing on registry)
- [x] T005 [P] Author `docs/architecture/PUBLIC_INTERNAL_BOUNDARY.md` (security-architect). Validation: explicit public vs internal surface list (site routes, registry JSON, dashboard, inbox, secrets). (Done 2026-09-24 — 5 violations: full registry import, guidelines public, tools/permission public, ops fixtures public, no transform)
- [x] T006 [P] Author `docs/architecture/WEB_INFORMATION_ARCHITECTURE_V2.md` (product-designer + lead-frontend). Validation: covers all 32 App.tsx child routes + redirects. (Done 2026-09-24 — §4 full table; counts keep 15 / merge 12 / redirect 4 / retire 0 / create 3; §5.1 single-hop vercel fix; §4.1 slug drift)
- [x] T007 [P] Author `docs/architecture/PUBLIC_AGENT_REGISTRY_SCHEMA.md` (data-engineer). Validation: YAML ↔ JSON ↔ TS field map; no secrets fields. (Done 2026-09-24 — allowlist schema; static module path; CI denylist)
- [x] T009 [P] Author `docs/architecture/EVIDENCE_ARCHITECTURE.md` (technical-documentation-lead). Validation: proof/evidence/work consolidation story. (Done 2026-09-24 — /proof canonical; flags /offerings·/solutions·/industries divergence for Architecture Lead)
- [x] T008 [P] Author `docs/architecture/ROUTE_MIGRATION_V2.md` (lead-frontend). Validation: resolves offerings/work/evidence double-hop vs vercel.json; lists dead imports. (Done 2026-09-24 — §2 single-hop targets; §3.1 dead: SolutionsPage, IndustriesPage, WorkPage, OfferingsPage, EvidencePage)
- [x] T010 [P] Author `docs/architecture/AI_COMPANY_BUILDER_UX.md` (product-designer). Validation: builder UX flows tied to ai-company-builder + ask routes. (Done 2026-09-24 — §3 five modes mapped; §4 journeys + §20 Ask Option A; §5 retain/refine/replace)
- [x] T011 [P] Author `docs/architecture/V2_IMPLEMENTATION_ROADMAP.md` (technical-documentation-lead). Validation: phased plan, depends-on graph across T003–T010. (Done 2026-09-24 — P0–P7; critical path P0→P1→P2→…; P1 gates follow-up ECL)
- [x] T012 Author primary `docs/architecture/LIGHTSPEED_AI_COMPANY_BUILDER_WEB_ARCHITECTURE_V2.md` with Mermaid diagrams; links all nine artifacts. Validation: no orphan artifact. (Done 2026-09-24 — 17 sections; D1–D12 = 12 mermaid blocks in §5; rulings 1–6; artifact index links all 9 + primary + ADR + harness refs)
- [x] T013 Author ADRs (025+) for v2 decisions; record ADR path choice + note duplicate 020 collision. Validation: numbered, one decision each. (Done 2026-09-24 — 11 ADRs 025–035 in `docs/architecture/adr/` + README index; all Accepted; duplicate-020 + path choice noted in README + ADR-025)

## Validation

- [x] T014 `pwsh scripts/lint-ecl.ps1` + `pwsh scripts/validate-drift.ps1` green. (Done 2026-09-24 — validate-drift: 87 files, no drift; lint-ecl: passed)
- [x] T015 Count audit: grep new architecture docs for stale 145/152 claims; fix or footnote as historical. (Done 2026-09-24 — all hits in `docs/architecture/**` historical/footnoted/companion-filename/stale-callout only; zero live 145/152/140+ claims; live counts remain 90/20)
- [x] T016 Update summary.md Outcome + Decisions; mark tasks complete. (Done 2026-09-24)

- [x] T017 [P] §7.4 deployment comparison → `harness/changes/active/ref/deployment-comparison.md`. (Done 2026-09-24)

## Review / Close

- [x] T018 Fix 3 pre-existing registry-trim pytest failures (offers agent-ids, routines receivers, AISTUDIO_PREVIEW CSP) + restore merge-regression assertion. Validation: full suite 2457/1/0 exit 0; commit `b52de2c`. (Done 2026-09-24)
- [x] T019 Record validation evidence in `summary.md` (`validation_results`, `validation_status: pass`, `phase: validate`) + `reviews/HANDOFF_CLOSEOUT.md` §C.1 + `reviews/REVIEW_CHECKLIST.md` §7.4. (Done 2026-09-24)
- [x] T020 Human sign-off: Architecture Lead + CEO complete `reviews/REVIEW_CHECKLIST.md` §0–§7; set `spec_review`/`plan_review` to `approved` in `summary.md`. (Done 2026-09-24 — user: "1. Approved. 2. Proceed.")
- [x] T021 Close: `pwsh -NoProfile -File .\scripts\harness-change.ps1 close completed` after T020; paste STATUS draft from handoff §E. (Done 2026-09-24)
- [x] T021b Re-run `lint-ecl.ps1` + `validate-drift.ps1` after validation note writes. (Done 2026-09-24 — validate-drift PASS 87 files; lint-ecl blocked solely on `plan_review` pending human approval — gate fires only at `phase: validate`.)

## Deferred Tasks

- Actual route code migration (separate ECL change after v2 doc approved).
