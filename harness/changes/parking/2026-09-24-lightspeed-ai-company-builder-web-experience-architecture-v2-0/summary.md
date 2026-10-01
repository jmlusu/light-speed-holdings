---
title: "LightSpeed AI Company Builder + Web Experience Architecture v2.0"
slug: "lightspeed-ai-company-builder-web-experience-architecture-v2-0"
status: "parked"
location: "parking"
phase: "plan"
intake_status: "accepted"
spec_review: "pending"
plan_review: "pending"
modules: []
files: []
tags: ["architecture", "v2", "web", "agent-registry"]
validation_status: "unknown"
created_at: "2026-09-24"
updated_at: "2026-09-24"
session_id: "41fdc305-4941-42f4-aaa9-26f655382bf2"
owner_agent: "jmlus"
claimed_at: "2026-09-24"
---

# Summary

## Outcome

- Discovery / current-state baseline complete (read-only). No code or registry changes this session — **docs-only ECL** (authoring complete; implementation deferred to follow-up ECL).
- **T012 primary doc written (2026-09-24):** `docs/architecture/LIGHTSPEED_AI_COMPANY_BUILDER_WEB_ARCHITECTURE_V2.md` — 17-section synthesis; exactly 12 Mermaid diagrams D1–D12 (current/target arch, 90-agent org, single-owner, lifecycle, dispatch, public/private, registry dataflow, LSOS, builder UX, web IA, migration); artifact index links all nine support files (no orphans).
- **T013 ADRs written (2026-09-24):** 11 ADRs **025–035** in `docs/architecture/adr/` + `README.md` index; all **Accepted**; path = `docs/architecture/adr/` per BRIEF_LOCK; duplicate-020 collision noted (legacy `docs/adr/` not renamed).
- **Supporting artifacts T003–T011 all authored** under `docs/architecture/` (consolidation matrix, workforce-90, public/internal boundary, web IA v2, public registry schema, route migration, evidence, builder UX, implementation roadmap).
- **T014 validation green (2026-09-24):** `validate-drift.ps1` (87 files, no drift) + `lint-ecl.ps1` (passed).
- **T015 count audit clean (2026-09-24):** every 145/152 hit under `docs/architecture/**` is historical, footnoted, companion-filename, or an explicit stale-claim callout — **zero live claims**; canonical live counts remain **90 agents / 20 departments**.
- **Rulings embedded in primary doc (§15 Decision Log):** (1) routes — `/what-we-do` hub with live `/solutions` + `/sectors`, edge `/offerings`→`/solutions` single hop, `/industries`→`/sectors` single hop, `/work`·`/evidence`→`/proof` single hop, details retained; (2) public registry sink = `src/data/generated/agent-registry.public.json` (boundary `public/` path non-normative); (3) `head_of_business_development` sole exec of BD, `cso` sole exec of strategy (dual mandate rejected); (4) canonical host = Vercel SPA from `main` (`ai.studio` redirect/re-scope); (5) ADRs 025+ under `docs/architecture/adr/` with duplicate-020 note (no history rename); (6) live counts only 90/20.
- T006 authored `docs/architecture/WEB_INFORMATION_ARCHITECTURE_V2.md` (32-route table, action counts, single-hop redirects, homepage 13 sections, slug-drift fix list).
- T010 authored `docs/architecture/AI_COMPANY_BUILDER_UX.md` (five modes, executive/technical journeys, Ask §20 Option A, retain/refine/replace).
- `pwsh scripts/lint-ecl.ps1` + `pwsh scripts/validate-drift.ps1` green after these writes.

## Current-State Baseline (verified 2026-09-24)

### Registry / workforce
- Canonical counts aligned across three surfaces: `company-registry.yaml` = 90 ids, `.opencode/agents/*.md` = 90 cards, `company/agent-registry.json` = 90 agents.
- Canonical claim (docs/source-of-truth.yaml): 90 agents (89 AI + 1 human CEO), 20 departments.
- Trim 152→90 already committed (`e2bdb0c7`). Stale 145/152 claims remain in `docs/STATUS.md` (dated milestone log, excluded from drift gates), `docs/EXECUTIVE-STRATEGY-EXPANSION.md` ("145 specialized agents"), narrative/parking harness files (historical).
- `company/departments.yaml` now has 20 department entries including `pharos` — the "19 missing pharos" note in source-of-truth.yaml comment and parked narrative change is stale and needs reconciliation in a doc pass.

### Dual runtime (hybrid repo)
1. **Python AI Company Builder**: Python 3.12+, Typer CLI (`src/ai_company/`, package `ai-company`, uv). Key subsystems: generator (YAML→md cards), registry loader/parser/validator/sync, orchestrator (message_bus, approval/HITL, escalation, scheduler, briefing), executor (daemon, loop, tool_runner, dead_letter, hitl_gate), llm (multi-provider, circuit_breaker, cost_tracker), memory (6-type store + governance ADR-019), security (rbac, pii, content_filter, encryption), workflow engine, dashboard (separate FastAPI layer — not fully enumerated this pass).
2. **React web experience**: Vite 6 + React 18 + TS 5.7 + Tailwind 4 + react-router-dom 7, bun package manager, repo-root `src/`. 31 page components, site-context (theme + briefing), AskLightSpeed component, `src/data/{companyData,siteContent,useCaseCatalogData}.ts`. Edge: `vercel.json` (SPA rewrite, 2 redirects, `api/enquiry.ts` on cpt1).

### Routes (src/App.tsx) — 32 child routes
- Live: `/`, `what-we-do`, `proof`, `solutions/:slug`, `industries/:slug`, `technology`, `insights`, `about`, `ai-company-builder`, `ask`, `contact`, `legal/privacy`, `legal/terms`, `why`, `how-we-help` (+`/engagement`), `process`, `geography`, `leadership`, `faq`, `resources`, `events`, `news`, `careers`, `deliverables`, `outcomes`, `partnerships`, `trust`.
- SPA redirects: `solutions`→`what-we-do`, `industries`→`what-we-do`, `offerings`→`what-we-do`, `work`→`proof`, `evidence`→`proof`, `*`→`/`.
- **Redirect conflict**: vercel edge sends `/offerings`→`/solutions` then SPA sends `/solutions`→`what-we-do` (double hop); `/work`→`/evidence` (edge) then →`/proof` (SPA). Target model should collapse to one hop to `what-we-do` / `proof`.
- Dead imports still wired: `WorkPage`, `OfferingsPage`, `EvidencePage` imported but their routes are pure redirects (candidates for removal in route rationalization).

### ADRs
- Live ADRs at `docs/adr/` (001–005, 010, 012–020, 022–024 + duplicate-numbered 020s: `020-pharos-content-intelligence.md` and `020-client-facing-site-guiding-principles.md`). No `006–009`, `011`, `021`. New v2 ADRs continue from 025; decide location: `docs/adr/` (existing) vs `docs/architecture/adr/` (brief §35) — propose `docs/adr/` as canonical with index note, or symlink/alias.
- Number collision to fix: two ADR-020 files.

### Deployment targets (to compare in baseline)
- https://lightspeedholdings.ai.studio, https://light-speed-holdings.vercel.app/, https://github.com/jmlusu/light-speed-holdings (fetch in discovery appendix or road-map task).

### Docs drift risks for v2 doc pass
- README says both "90 agents across 20 departments" (line 96) and "89 AI Agents" framing elsewhere — verify AI/human split phrasing.
- STATUS.md milestone lines still say 145 (historical, gate-exempt).
- EXECUTIVE-STRATEGY-EXPANSION.md still claims 145 agents — live doc, not archive.

## Decisions

- ECL change created and discovery completed before any authoring (per ECL + brief constraint: no code rewrite before discovery/target/migration path).
- Proceed to author 9 supporting artifacts + primary v2 doc + ADRs + Mermaid under `docs/architecture/`.
- **Path lock (T013):** v2 ADRs live at `docs/architecture/adr/` (BRIEF_LOCK §34); legacy `docs/adr/` 001–024 stay put; numbering continues 025+; duplicate-020 recorded, not renamed.
- **Full brief accepted:** T002 brief text confirmed + filenames locked in `BRIEF_LOCK.md`.
- **All authoring tasks complete (T003–T013); validation complete (T014–T016).** Change is ready for Architecture Lead + CEO review / close.

## Validation

- Registry triple-count check: 90/90/90 pass.
- Drift manifest (source-of-truth.yaml) at 90/20 — **`validate-drift.ps1` green (87 files, 2026-09-24)**.
- **`lint-ecl.ps1` green (2026-09-24)** after all authoring writes.
- **T015 count audit:** no live 145/152/140+ under `docs/architecture/**` — historical-only.
- No generation/pytest run (no source changes — docs-only).

## Next Step

- ~~Intake → spec~~ Done. All implementation + validation tasks **[x] complete**.
- **Now:** Architecture Lead + CEO review of primary v2 doc + 11 ADRs; then close this ECL change (park/close via harness). Route code migration = separate follow-up ECL (Deferred).

## Authoring Progress

- **T008 done (2026-09-24):** `docs/architecture/ROUTE_MIGRATION_V2.md` — full 34-entry route inventory; double-hop fix (edge targets = SPA finals: `/offerings`→`/what-we-do`, `/work`→`/proof`, `/evidence`→`/proof`); dead imports: WorkPage, OfferingsPage, EvidencePage, SolutionsPage, IndustriesPage; slug mismatches (footer legacy solution slugs + `/industries/development` vs content `education`); stack keep (React Router 7 / Vite — no rewrite); two Mermaid graphs; §37 decisions D1–D10.
- **T003–T013 + T014–T016 all done (2026-09-24):** 9 support artifacts + primary (12 Mermaid) + 11 ADRs (025–035) + README index; drift + ECL lint green; count audit clean; summary updated.


## Transition Note

- concurrent v2.0 residual; restoring P2 public registry transform
