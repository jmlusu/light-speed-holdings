# Close-out Handoff — Architecture v2.0

**Change:** LightSpeed AI Company Builder + Web Experience Architecture v2.0
**Date:** 2026-09-24
**Mode:** Docs-only ECL · implementation deferred to follow-up change
**Prepared for:** Architecture Lead + Human CEO review → `close completed`

---

## A. What this change delivered

### A.1 Primary + support (10 architecture docs)

| Deliverable | Path |
|-------------|------|
| Primary | `docs/architecture/LIGHTSPEED_AI_COMPANY_BUILDER_WEB_ARCHITECTURE_V2.md` |
| 1–9 Support | `AGENT_CONSOLIDATION_152_TO_90.md`, `AI_WORKFORCE_90.md`, `PUBLIC_INTERNAL_BOUNDARY.md`, `WEB_INFORMATION_ARCHITECTURE_V2.md`, `PUBLIC_AGENT_REGISTRY_SCHEMA.md`, `ROUTE_MIGRATION_V2.md`, `EVIDENCE_ARCHITECTURE.md`, `AI_COMPANY_BUILDER_UX.md`, `V2_IMPLEMENTATION_ROADMAP.md` |

### A.2 ADRs

- **11 ADRs** `025`–`035` under `docs/architecture/adr/` + `README.md` index (all Accepted).
- Legacy `docs/adr/` 001–024 **untouched**; duplicate historical `020` recorded, not renamed.

### A.3 Diagrams

- Primary doc: **exactly 12** Mermaid diagrams **D1–D12** (current/target arch, 90-agent org, single-owner, lifecycle, dispatch, public/private, registry dataflow, LSOS, builder UX, web IA, migration).
- Additional Mermaid in support docs (consolidation procedure, boundary, routes, evidence, roadmap, etc.).

### A.4 Harness / evidence (this change folder)

- `summary.md` — baseline + Outcome + rulings
- `spec.md`, `plan.md`, `tasks.md` — T001–T017 all `[x]`
- `BRIEF_LOCK.md` — brief pointer + filename locks
- `reviews/REVIEW_CHECKLIST.md` — this review gate
- `reviews/HANDOFF_CLOSEOUT.md` — this note
- `ref/deployment-comparison.md`, `ref/agents_152.txt`, `ref/agents_90.txt`

### A.5 What was NOT done (by design)

- No edits to `company-registry.yaml`, generators, `App.tsx`, `vercel.json`, or site pages.
- No public registry transform implementation.
- No route code migration, dead-file deletion, or deploy cutover.
- No re-trim or CREATE NEW of agents.
- `docs/STATUS.md` **not** finalized until after human approval + close (ECL §7).

---

## B. Architecture Lead + CEO decisions embedded (primary §15)

| ID | Ruling |
|----|--------|
| R1 | Live `/solutions` + `/sectors` under `/what-we-do`; single-hop: `/offerings`→`/solutions`, `/industries`→`/sectors`, `/work`·`/evidence`→`/proof` |
| R2 | Public registry sink: `src/data/generated/agent-registry.public.json` (static import) |
| R3 | BD dept executive = `head_of_business_development`; `cso` = strategy only |
| R4 | Canonical public host = **Vercel SPA from `main`**; AI Studio redirect/re-scope |
| R5 | New ADRs at `docs/architecture/adr/` starting 025 |
| R6 | Live counts only **90 agents / 20 departments** |

**Open product labels (CEO can override at review):** Sectors vs Industries; Ask nav CTA (Option A default); AI Studio fate.

---

## C. Validation evidence (docs change)

| Gate | Result | When |
|------|--------|------|
| `pwsh scripts/lint-ecl.ps1` | **PASS** | after authoring + after review package |
| `pwsh scripts/validate-drift.ps1` | **PASS** (87 files, 90/20) | after authoring |
| T015 count audit (`docs/architecture/**`) | **PASS** — no live 145/152/140+ | 2026-09-24 |
| Primary Mermaid | 12 open/close fences balanced | verified |
| Artifact presence | 10/10 required docs exist | verified |
| `ruff` + `mypy` (touched files) | **PASS** (exit 0) | post-fix |
| Full `pytest` | **2457 passed / 1 skipped / 0 failed** (390s, exit 0) | 2026-09-24 post-fix |

### C.1 Pre-existing pytest failures — **FIXED 2026-09-24**

Baseline 3-red on `chore/registry-trim-90-skills-purge` (not introduced by docs ECL) were fixed in-session:

| Test | Cause | Fix applied |
|------|--------|-------------|
| `test_ai_caas_offers::test_offer_agents_exist_in_registry` | `config/company/ai_caas_offers.yaml` listed **`generator-owner`** + 7 other stale ids (152→90) | MERGE targets from `AGENT_CONSOLIDATION_152_TO_90.md`: `registry-owner`, `product-owner`, `ux-research-lead`, `workflow-owner`, `growth-hacker`, `senior-frontend-engineer`, `senior-backend-engineer`; dropped 2 duplicate merge targets |
| `test_routine::test_is_known_receiver_resolves_real_registry` | routines still **`content_writer`**; registry has **`content_creator`**; real-registry assertion was a merge regression (HEAD expected old id) | `routines.yaml` ×5 → `content_creator`; `DEFAULT_RECEIVER_ID`/seed/`publishing/queue.py` → `content_creator`; restored trim assertion from `890236e` (`content_creator` True, `content_writer` False) |
| `test_dashboard_security::test_ai_studio_preview_relaxes_framing` | `security_headers()` had **no `AISTUDIO_PREVIEW` branch** (ADR-024) | Implemented preview gate: CSP `frame-ancestors https://*.google.com https://*.aistudio.google`, omit `X-Frame-Options` when truthy; `AISTUDIO_PREVIEW=` in `.env.example` |

Full suite now **2457 passed / 1 skipped / 0 failed**; `validation_status: pass`. Side-effect YAMLs (`hr/onboarding_requests.yaml`, `orchestrator/approvals.yaml`) restored.

ECL archive still requires: `phase: validate`, `spec_review: approved`, `plan_review: approved`, `validation_status: pass`, full suite in `validation_results`. **Human sign-off (T020) remains.** Do not archive without explicit yes.

---

## D. Review flow (human)

1. Open `reviews/REVIEW_CHECKLIST.md` — work §0–§6 in order (~1–1.5 h).
2. Record result in `reviews/review.md` + set front-matter reviews to `approved` (or request changes).
3. If **Request changes:** leave change **active**; file fix tasks in `tasks.md`; do not archive.
4. If **Approve:** complete §7 checklist (tests, STATUS draft, git hygiene).
5. Run close (only after explicit human yes):

```powershell
pwsh -NoProfile -File .\scripts\harness-change.ps1 close completed
pwsh -NoProfile -File .\scripts\lint-ecl.ps1
```

6. Paste archive path into `docs/STATUS.md` (step E) and commit separately if desired.

---

## E. STATUS.md entry (draft — paste at close)

> **Update `Last Updated` to close date. Prepend under `## Current State`:**

```markdown
- **AI Company Builder + Web Experience Architecture v2.0 (2026-09-24, docs)**: Docs-only ECL — no code/registry/deploy changes. Authored primary `docs/architecture/LIGHTSPEED_AI_COMPANY_BUILDER_WEB_ARCHITECTURE_V2.md` (17 sections, 12 Mermaid D1–D12) + 9 support artifacts + ADRs **025–035** under `docs/architecture/adr/`. Canonical live counts remain **90 agents / 20 departments**. Rulings: live `/solutions`+`/sectors` under `/what-we-do`, single-hop redirects, public sink `src/data/generated/agent-registry.public.json`, BD→`head_of_business_development` / `cso`→strategy, Vercel SPA canonical. Boundary V1–V5 and §9 schema gaps remain **open for implementation**. Gates: lint-ecl ✅, validate-drift ✅ (87), count audit ✅, full pytest (see summary validation_results). ECL archived as `harness/changes/archive/<slug>`. Follow-up: implementation ECL per `V2_IMPLEMENTATION_ROADMAP.md` P2–P7 (registry transform → routes → UX → governance → QA) — **do not start until this change is closed**.
```

---

## F. Follow-up implementation ECL (after close only)

**Do not** open `harness-change.ps1 new` until this change is archived (one active change rule).

**Suggested intake title:** `v2-implementation-p2-public-registry-transform`
**Entry:** P1 exit from roadmap (this package approved + frozen).
**First work (P2):** public transform + schema allowlist + break `src/` → `company/agent-registry.json` imports (boundary V1–V5).
**Then:** P3 routes (`vercel.json` + `App.tsx` single-hop) → P4 builder UX → P5 content/evidence → P6 governance (V1 org rewire, §9 fields) → P7 QA/release.

Full phase map: [`docs/architecture/V2_IMPLEMENTATION_ROADMAP.md`](../../docs/architecture/V2_IMPLEMENTATION_ROADMAP.md).

**Deferred task from `tasks.md`:** actual route code migration (separate ECL after approval).

---

## G. Known residual risks (carry into implementation)

| ID | Risk | Owner phase |
|----|------|-------------|
| R-01 | Double-hop redirects live until P3 | P3 |
| V1–V5 | Full internal registry / ops fixtures still in SPA | P2 |
| R-03 | Two production frontends (Vercel vs AI Studio) | P4/P7 |
| R-04 | Stale 145/152 in STATUS history, EXECUTIVE-STRATEGY-EXPANSION, remote README, homepage “140+” | P5 content sweep |
| V1 | `cso` dual dept until registry edit | P6 |
| §9 | 7 MANDATORY ownership fields 0/90 | P2/P6 |
| Span | `chief_of_staff` 19 direct reports | P6 watch |

---

## H. One-paragraph handoff blurb (for chat / PR)

> Architecture v2.0 is **docs-complete and ready for Architecture Lead + CEO sign-off**. Ten architecture docs, twelve diagrams, and ADRs 025–035 define consolidation (152→90 already shipped), single-owner org model, public/internal boundary + registry schema, web IA and single-hop routes, evidence/`/proof` consolidation, builder UX, and an 8-phase implementation roadmap. Nothing was implemented in code this change. After review approval: set reviews approved, finish validation front-matter (full pytest), draft STATUS, then `harness-change.ps1 close completed`, then open the follow-up implementation ECL starting at P2 public registry transform.

---

## I. Command card

```powershell
# Status
pwsh -NoProfile -File .\scripts\harness-change.ps1 status

# Gates
pwsh -NoProfile -File .\scripts\lint-ecl.ps1
pwsh -NoProfile -File .\scripts\validate-drift.ps1
uv run pytest

# After human approval only
pwsh -NoProfile -File .\scripts\harness-change.ps1 close completed
```

**Stop:** Do not archive while `spec_review` is `pending` or `validation_status` is not `pass`. Do not edit `harness/changes/INDEX.json` by hand.
