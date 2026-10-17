---
title: "Auto-evolve proposal: 12 eligible archives (2026-09-25 → 2026-10-10)"
date: 2026-10-10
trigger:
  reason: manual
  eligible_count: 12
  threshold: 5
  window: 12
  excludes: ["auto-evolve-harness-", "auto-evolve"]
---

# Auto-evolve Proposal

## Candidate Archives

| # | Archive ID | Title | Validation | Key Decisions |
|---|------------|-------|------------|---------------|
| 1 | 2026-09-25-ls-mem-implementation | LS-MEM implementation | pass (retrospective) | Work done without active ECL; untracked deliverables at archive |
| 2 | 2026-09-25-ls-mem-phase-3-data-model | LS-MEM Phase 3 data model | pass (retrospective) | Data-model doc untracked at archive |
| 3 | 2026-09-26-ls-mem-completion | LS-MEM completion | pass (CISO audit) | 5 CEO decisions; 4 open HITL items archived as non-blocking |
| 4 | 2026-10-03-customer-journey-conversion-architecture-implementation | Customer journey conversion architecture | **unknown** (ArchiveExceptions allowlist) | Reviews pending at archive; slug also in parking/ |
| 5 | 2026-10-04-audit-export-reads-canonical-jsonl-trail | Audit export reads canonical JSONL trail | pass | CI can never export; phase stuck at implement; stale Next Step |
| 6 | 2026-10-07-2026-10-06-repository-sanitization | Repository sanitization | pass (4 exclusions) | Phased approval protocol; evidence-contradicts-premise |
| 7 | 2026-10-07-2026-10-07-decommission-followups | Decommission follow-ups | pass | Decommission LS-MEM; split-brain runtime-path rule |
| 8 | 2026-10-07-studio-scorecard-v1-instrumentation-t2-418 | Studio Scorecard v1 instrumentation | pass (isolated full suite) | Additive-only instrumentation; cross-session archive |
| 9 | 2026-10-07-t4-competitive-landscape-oct-refresh-420 | T4 competitive landscape Oct refresh | pass | Front-matter claims approved; reviews/review.md unfilled template |
| 10 | 2026-10-07-t5-canonical-org-truth-90-20 | T5 canonical org truth 90/20 | pass (**only** full validation_results array) | Computed census; ADR-025 history-as-history |
| 11 | 2026-10-10-correct-unsupported-narrative-claims-clinic-ngo-offer-e | Correct unsupported narrative claims | pass (partial suite) | Draft-then-apply; intake_status "pending" on completed archive |
| 12 | 2026-10-10-ops-runbook-marketing-site-dashboard-boundary | Ops runbook app-boundary | pass (docs-only per AGENTS §6) | Two-app boundary; G-1..G-6 deferred |

## Evidence: Repeated Failures / Verification Gaps / User Corrections / Reusable Constraints

### Verification Gaps

1. **Stale "Next Step" at close**: 7/12 archives carry unfinished-task Next Steps contradicting their own tasks.md (e.g. audit-export T003–T005 listed pending while tasks.md shows T001–T014 all [x]).
2. **Duplicate slug across trees**: customer-journey exists in both `parking/` (status parked, 2026-10-03) and `archive/` (completed, 2026-10-04); INDEX faithfully indexes both — filesystem defect, no lint gate forbids it.
3. **Non-standard front-matter enums pass lint**: `intake_status: "pending"` on completed narrative-claims; `intake_status: "complete"` on ls-mem-completion; `spec_review: "completed"` on t4; `validation_status: unknown` on customer-journey.
4. **`validation_results` array mandatory-in-prose only**: only t5 has the array; 11/12 use body prose lint cannot parse.
5. **Front-matter review claims not backed by reviews/**: t4 claims spec_review completed / plan_review approved while reviews/review.md is an unfilled template (all five sections pending).
6. **Suite-scope rule conflict**: ECL §4 requires full non-E2E suite unconditionally; AGENTS.md §6 exempts docs/harness-only changes. ops-runbook cites §6; narrative-claims ran partial suites citing neither cleanly.
7. **ArchiveExceptions allowlist**: exists solely to admit customer-journey's unknown validation_status; hand-maintained escape hatch weakening gate C1.

### User Corrections

- LS-MEM build (Sep 25–26, 5 CEO decisions) → decommissioned Oct 7 (5 owner directives) within 13 days; retrospective-record and untracked-deliverable patterns are both artifacts of that speed.
- Explicit user confirmations required for cross-session lifecycle edits (studio-scorecard archived T4 under confirmation; t4's own summary silent).
- narrative-claims: pending evolution ignored per user decision (2026-10-10).

### Reusable Constraints (Rules to Clarify / Keep)

- Isolated full-suite protocol (`--basetemp` + git status snapshot): studio-scorecard + t5 (strongest hygiene; currently a "hint").
- Single slug per change across active/parking/archive.
- t5 validation_results array is the model citizen to gate toward.
- CI can never export audit evidence; export runs locally (audit-export D-a).
- Never move live runtime paths while daemon writes them (decommission split-brain).

## Scoring & Recommendations

Scoring: archive evidence (0-40), project relevance (0-30), rule clarity impact (0-30). ≥80 = accept.

| # | Candidate Change | Evidence | Relevance | Clarity | Score | Recommendation |
|---|-----------------|----------|-----------|---------|-------|----------------|
| A1 | Clear "Next Step" at close (ECL §4 close-blocker) | 40 (7/12 archives) | 28 | 28 | **96** | **Accept** — clarify §4; lint hook |
| A2 | Unique slug across active/parking/archive (ECL §4) | 38 (1 dup pair, INDEX verified in sync) | 28 | 28 | **94** | **Accept** — clarify §4; lint gate |
| A3 | Standardize front-matter enums + lint (ECL §4) | 38 (4 archives) | 28 | 28 | **94** | **Accept** — codify closed sets; extend C1 |
| A4 | `validation_results` array mandatory at archive (ECL §4) | 38 (1/12 complies; t5 model) | 30 | 28 | **96** | **Accept** — make §4 text a gate |
| A5 | reviews/ must match front-matter review claims (ECL §4) | 36 (t4 unfilled template) | 26 | 28 | **90** | **Accept** — clarify §4; lint cross-check |
| A6 | Resolve AGENTS §6 vs ECL §4 suite-scope conflict (ECL §4) | 36 (2 archives cite conflicting rules) | 28 | 26 | **90** | **Accept** — ECL-side clarification only |
| A7 | Isolated-gate protocol normative (ECL §4 hint → required) | 34 (3 conventions; 2 strong precedents) | 24 | 24 | **82** | **Accept** — promote hint to requirement |
| A8 | Untracked deliverables flag `commit_pending` (ECL §4) | 30 (2 archives) | 22 | 24 | **76** | **Defer** — record in proposal; revisit next cycle |
| A9 | Bidirectional cross-session lifecycle records (ECL §3/§4) | 28 (t4/studio-scorecard asymmetry) | 22 | 24 | **74** | **Defer** — low frequency; revisit |
| A10 | Open HITL machine-readable close state (ECL §4) | 24 (1 archive) | 18 | 22 | **64** | **Defer** |

## Accepted Candidates (Score ≥ 80 + Auditor Approval)

Subject to independent auditor score (pending in this draft; auditor result recorded below before application):

- **A1** Clear "Next Step" at close — close-blocker in ECL §4
- **A2** Unique slug across active/parking/archive — ECL §4 + lint gate
- **A3** Standardize front-matter enums — closed sets + lint C1 extension
- **A4** `validation_results` array mandatory at archive — ECL §4 + lint gate
- **A5** reviews/ must match front-matter claims — ECL §4 + lint cross-check
- **A6** Suite-scope conflict resolution — ECL §4 clarification (AGENTS §6 reference only; no AGENTS.md edit this cycle — file is dirty from parallel session)
- **A7** Isolated-gate protocol normative — ECL §4 promotes existing hint

Deferred (below threshold): A8, A9, A10.

## Application Plan

Scope: `docs/ECL.md` §4 clarifications (A1–A7) + `scripts/maintenance/lint-ecl.ps1` gates. No new documents, no AGENTS.md edits (dirty from parallel session; A6 stays ECL-side; A11/A12 from evidence scan deferred pending AGENTS.md clean state).

1. ECL.md §4 additions (each a short clarification of an existing sentence, not a new section):
   - Next Step close-blocker (A1)
   - Unique slug rule (A2)
   - Front-matter enum closed sets (A3)
   - validation_results array mandatory at archive (A4)
   - reviews/ ↔ front-matter consistency (A5)
   - Docs/harness-only suite exemption pointer to AGENTS §6 (A6)
   - Isolated full-suite protocol as requirement when full suite runs (A7)
2. lint-ecl.ps1 gates:
   - New: duplicate-slug gate (A2)
   - Extend C1: archived summaries fail if Next Step contains unchecked task refs without "None — change closed" (A1); fail if `validation_results` array missing/empty (A4); warn/fail on non-standard enums (A3); warn if reviews/review.md exists with all-pending sections while front matter claims approved (A5).
3. Apply to the live tree only for future changes; historical archives remain as-is (no retroactive rewrites) — gates evaluate active/parking at close time and archives only for the new duplicate-slug + missing-array checks where safe to add without breaking the 53-entry baseline (lint-ecl must still pass on the current repo state; if a new gate fails on historical archives, scope the gate to close-time/new archives or document an explicit, minimal exception list).
4. Run lint-ecl.ps1; confirm PASS on current tree.
5. Record results.tsv row + `harness-evolve mark-complete`.
