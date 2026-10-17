# Review Checklist — Architecture v2.0 (docs-only ECL)

**Change:** LightSpeed AI Company Builder + Web Experience Architecture v2.0
**Reviewers:** Architecture Lead (primary), Human CEO (approve/route + product rulings)
**Mode:** Docs only — no code, registry, or deploy changes in this change.
**How to use:** Check each box or mark `BLOCK` + note. All must be green before `close completed`.

---

## 0. Preconditions (5 min)

| # | Check | Pass? |
|---|--------|-------|
| 0.1 | Active change is still this one: `harness/changes/active/summary.md` title matches | [ ] |
| 0.2 | `tasks.md` — **no unchecked** T-items (T001–T017) | [ ] |
| 0.3 | `pwsh scripts/lint-ecl.ps1` green | [ ] |
| 0.4 | `pwsh scripts/validate-drift.ps1` green (87 files, 90/20) | [ ] |
| 0.5 | Working tree: only intended docs + harness files dirty (no secrets, no registry edits) | [ ] |

---

## 1. Primary document (30–45 min)

**File:** [`docs/architecture/LIGHTSPEED_AI_COMPANY_BUILDER_WEB_ARCHITECTURE_V2.md`](../../docs/architecture/LIGHTSPEED_AI_COMPANY_BUILDER_WEB_ARCHITECTURE_V2.md)

| # | Check | Pass? |
|---|--------|-------|
| 1.1 | Executive summary matches problem → target → outcomes without marketing fluff | [ ] |
| 1.2 | Scope states **no implementation in this change**; points to roadmap P1 gate | [ ] |
| 1.3 | **Exactly 12** Mermaid blocks, labeled **D1–D12**, fences balanced | [ ] |
| 1.4 | D1 current + D2 target architectures are truthful vs baseline (hybrid Python + React) | [ ] |
| 1.5 | D3 org chart consistent with **90 = 19 exec + 64 specialist + 7 board**, 20 depts | [ ] |
| 1.6 | D7 public/private boundary matches NEVER-EXPOSE list in boundary doc | [ ] |
| 1.7 | D8 registry dataflow: YAML → internal JSON → public transform → SPA | [ ] |
| 1.8 | D12 migration phases match roadmap **P0–P7** | [ ] |
| 1.9 | Artifact index links **all 9** support docs (no orphans) + ADRs + harness refs | [ ] |
| 1.10 | §15 Decision Log includes rulings R1–R6 (see §3 below) | [ ] |
| 1.11 | Counts: only **90 / 20** as live; 152/145 only historical footnotes | [ ] |

---

## 2. Nine supporting artifacts (20–30 min)

Read headings + tables; open Mermaid if needed. One row per file.

| # | Artifact | Exists | Core claim spot-check | Pass? |
|---|----------|--------|------------------------|-------|
| 2.1 | `AGENT_CONSOLIDATION_152_TO_90.md` | [ ] | 62 removed fully classified; cites `e2bdb0c7` | [ ] |
| 2.2 | `AI_WORKFORCE_90.md` | [ ] | Census 19/64/7; 7 MANDATORY §9 gaps listed; V1 dual-owner open | [ ] |
| 2.3 | `PUBLIC_INTERNAL_BOUNDARY.md` | [ ] | NEVER/EXPOSE lists; V1–V5 violations; no “it’s fine” handwave | [ ] |
| 2.4 | `WEB_INFORMATION_ARCHITECTURE_V2.md` | [ ] | All ~32 App.tsx routes dispositioned | [ ] |
| 2.5 | `PUBLIC_AGENT_REGISTRY_SCHEMA.md` | [ ] | Allowlist fields; denylist (guidelines/permission/legacy tools); sink path | [ ] |
| 2.6 | `ROUTE_MIGRATION_V2.md` | [ ] | Single-hop targets; dead imports listed | [ ] |
| 2.7 | `EVIDENCE_ARCHITECTURE.md` | [ ] | `/proof` canonical; content salvage before delete | [ ] |
| 2.8 | `AI_COMPANY_BUILDER_UX.md` | [ ] | Five modes; Ask Option A; demo honesty labels | [ ] |
| 2.9 | `V2_IMPLEMENTATION_ROADMAP.md` | [ ] | P0–P7; critical path; **implementation deferred** | [ ] |

---

## 3. Architecture Lead rulings (must agree or revise primary §15)

| # | Ruling | Agree? |
|---|--------|--------|
| 3.1 | **R1 Routes:** `/what-we-do` hub; live `/solutions` + `/sectors`; edge `/offerings`→`/solutions`; `/industries`→`/sectors`; `/work`·`/evidence`→`/proof` (single hop) | [ ] |
| 3.2 | **R2 Public sink:** `src/data/generated/agent-registry.public.json` static import (not `public/` fetch) | [ ] |
| 3.3 | **R3 Single-owner:** BD dept exec = `head_of_business_development`; `cso` = strategy only | [ ] |
| 3.4 | **R4 Canonical host:** Vercel SPA from `main`; AI Studio redirect or re-scope | [ ] |
| 3.5 | **R5 ADR path:** `docs/architecture/adr/` for 025+; legacy duplicate 020 **not** renamed | [ ] |
| 3.6 | **R6 Counts:** live = 90/20 only | [ ] |

---

## 4. ADRs (15 min)

**Dir:** `docs/architecture/adr/` (11 files + `README.md`)

| # | Check | Pass? |
|---|--------|-------|
| 4.1 | Numbering **025–035**, one decision per ADR | [ ] |
| 4.2 | Sections: Context / Decision / Alternatives / Rationale / Consequences / Status | [ ] |
| 4.3 | Status **Accepted** (or intentional Proposed) consistent with README index | [ ] |
| 4.4 | ADR-025 notes historical duplicate-020; no legacy renames | [ ] |
| 4.5 | Decisions align with primary rulings + sibling artifacts (spot-check 027, 028, 031) | [ ] |

**Legacy ADR note:** `docs/adr/` 001–024 unchanged; gaps (006–009, 011, 021) historical — out of scope.

---

## 5. Cross-consistency (15 min)

| # | Check | Pass? |
|---|--------|-------|
| 5.1 | Sibling docs still flag `/offerings`·`/solutions` divergence only as “pending Architecture Lead” — primary is authoritative | [ ] |
| 5.2 | No doc claims code was migrated or deployed | [ ] |
| 5.3 | No live **145 / 152 / 140+** claims under `docs/architecture/**` (grep) | [ ] |
| 5.4 | Source-of-truth still **90 / 20** | [ ] |
| 5.5 | Roadmap critical path readable; P1 is gate for implementation ECL | [ ] |
| 5.6 | Boundary violations (V1 full registry import etc.) still listed as **open work**, not “fixed” | [ ] |

---

## 6. CEO / product decisions (flag if changing)

| # | Decision | Accept default? |
|---|----------|-----------------|
| 6.1 | Sectors vs Industries naming (`/sectors` preferred) | [ ] Accept [ ] Change |
| 6.2 | Ask as primary nav CTA (Option A) | [ ] Accept [ ] Change |
| 6.3 | Canonical host = Vercel (AI Studio re-scope) | [ ] Accept [ ] Change |
| 6.4 | 152→90 consolidation as permanent baseline (no re-expand without CREATE NEW process) | [ ] Accept [ ] Change |
| 6.5 | No code rewrite / framework migration in this change | [ ] Accept [ ] Change |

---

## 7. Close gates (run at approval time)

| # | Gate | Evidence |
|---|------|----------|
| 7.1 | Spec review **approved** | `reviews/review.md` + `summary.md` `spec_review` |
| 7.2 | Plan review **approved** | `summary.md` `plan_review` |
| 7.3 | `phase: validate`, `validation_status: pass` | `summary.md` front matter |
| 7.4 | `validation_results` includes lint-ecl, validate-drift, **full pytest** | `summary.md` — suite run: **2457 pass / 1 skip / 0 fail** (see handoff §C.1; fixes in `b52de2c`) |
| 7.4b | **Pytest gate decided:** accept 3 pre-existing failures + `validation_status: pass` with note, **or** fix failures first | **Resolved:** failures **fixed** in `b52de2c`; suite green 2457/1/0 |
| 7.5 | STATUS.md handoff drafted (see `HANDOFF_CLOSEOUT.md` §B) | draft ready before close |
| 7.6 | Side-effect files restored (`docs/AGENT-REGISTRY-TABLE.md`, etc. if dirty) | `git status` clean-ish |
| 7.7 | `pwsh scripts/harness-change.ps1 close completed` after human **yes** | archive path recorded |
| 7.8 | Follow-up implementation ECL **not** opened yet (or only after this close) | intake rule |

---

## Sign-off

| Role | Name | Date | Result | Notes |
|------|------|------|--------|-------|
| Architecture Lead | Human CEO (as Architecture Lead) | 2026-09-24 | [x] Approve [ ] Request changes | T020 — user: "1. Approved. 2. Proceed." |
| Human CEO | Jack Mlusu | 2026-09-24 | [x] Approve [ ] Request changes | T020 — authorizing close completed |

**Result:** [x] Ready to close completed · [ ] Request changes (list below) · [ ] Park

**Change request notes:**

1.
2.
