---
title: "Auto-evolve proposal: 5 eligible archives (2026-08-15 → 2026-08-17)"
date: 2026-08-19
trigger:
  reason: close
  eligible_count: 5
  threshold: 5
  window: 10
  excludes: ["auto-evolve-harness-", "auto-evolve"]
---

# Auto-evolve Proposal

## Candidate Archives

| # | Archive ID | Title | Validation | Key Decisions |
|---|------------|-------|------------|---------------|
| 1 | over-engineering-cleanup-... | Over-engineering cleanup: remove dead modules, consolidate duplicated layers, drop unused deps | pass | Batch-gated validation A→B→C→D; 212 pre-existing failures tracked as baseline; Windows PermissionError retry added to atomic_write |
| 2 | implement-j-a-r-v-i-s-theme-system-105 | J.A.R.V.I.S. theme system (#105) | pass | Scoped dashboard-only tests, not full suite; backward-compat brand-*/surface-* CSS retained; dark-mode only |
| 3 | phase-b-async-approval-engine-42 | Phase B: Async Approval Engine (#42) | pass | File-based suspend store over Temporal for single-machine; 30-day retention with daemon sweep; lint-ecl used as extra gate; ADR-017 recorded |
| 4 | phase-b-opentelemetry-tracing-40 | Phase B: OpenTelemetry Tracing (#40) | unknown | Archived at phase: "plan" — never entered implement; validation explicitly "Pending"; OTel API (not SDK) recorded as ADR-016 |
| 5 | security-hardening-...-canary-release | Security Hardening: Env Key Sanitization, Dashboard Auth Finalization, Trivy Scanning, S3 Backup, Canary Release | unknown | Parked mid-flight to unblock cleanup change; 212 test failures tracked as baseline by #1; validation explicitly "Pending" |

## Evidence: Repeated Failures / Verification Gaps / User Corrections / Reusable Constraints

### Verification Gaps

1. **2 of 5 archived changes have `validation_status: unknown`** — neither provides evidence of passing any gate. Changes #4 and #5 were archived without proof of validation.
2. **Change #4 archived at `phase: "plan"`** — never entered implement phase. The harness allowed a planned-only change to close.
3. **Change #2 ran only scoped dashboard tests**, not the full suite. "Full suite was in progress at timeout" was noted but not enforced.
4. **No lockfile atomicity check** — change #1 correctly regenerated `uv.lock` in the same commit as `pyproject.toml` dep changes, but this was discipline, not enforcement.

### User Corrections

- Change #1 documented rework of derived gauges (`task_success_rate_pct` recomputed from live inbox state; `cycle_success_rate_pct` removed) — original monitoring designed against phantom data.
- Change #1 notes "double-wrap through `build_user_prompt_typed`" was a bug fixed during consolidation — a latent prompt-rendering defect discovered during cleanup.
- Change #2 retained backward-compat CSS classes, signaling token migration isn't atomic and downstream templates may break.

### Reusable Constraints (Rules to Clarify / Keep)

| Constraint | Source | Current ECL Status | Proposed Action |
|-----------|--------|-------------------|-----------------|
| `uv.lock` must be regenerated in same commit as `pyproject.toml` dep changes | #1 | Not mentioned | Add as verification hint in ECL §4 |
| `__init__` re-export chains must be updated in same commit as module deletions | #1 | Not mentioned | Add as verification hint in ECL §4 |
| Archived changes must have `validation_status: pass`, not `unknown` | #4, #5 | §4 mentions populating `validation_results` but doesn't gate on pass | Add hard gate in ECL §4 |
| Archived `phase` must be `validate` or `implement`, not `plan` | #4 | Not enforced | Add gate in ECL §4 |
| Full test suite should run at archive, not just scoped subset | #2 | Not mentioned | Add guidance in ECL §4 |
| Parked changes' test failures should be excluded from other changes' baselines | #1, #5 | Not addressed | Add guidance in ECL §3 or §4 |
| ADRs referenced in changes should exist in `docs/adr/` before plan_review approval | #3, #4 | Not enforced | Add check in ECL §5 |

## Scoring & Recommendations

Scoring: archive evidence (0-40), project relevance (0-30), rule clarity impact (0-30). ≥80 = accept.

| # | Candidate Change | Evidence | Relevance | Clarity | Score | Recommendation |
|---|-----------------|----------|-----------|---------|-------|----------------|
| 1 | Over-engineering Cleanup | 35 | 15 | 15 | 65 | REJECT — confirms existing rules work, no new harness delta |
| 2 | Theme System | 28 | 20 | 20 | 68 | REJECT — scoped-only testing is a symptom, not a harness rule |
| 3 | Async Approval Engine | 36 | 15 | 14 | 65 | REJECT — clean pass, no new harness delta |
| 4 | OpenTelemetry Tracing | 10 | 28 | 28 | 66 | REJECT as standalone — but its gaps drive two rule improvements (phase gate + validation gate) |
| 5 | Security Hardening | 8 | 25 | 25 | 58 | REJECT as standalone — but its gaps drive parking isolation guidance |

**No individual archive scores ≥80.** However, the cross-archive pattern analysis reveals 6 concrete harness improvements that collectively address the dominant gap (incomplete validation at archive). These are proposed as ECL.md clarifications, not new sections or scripts.

## Accepted Candidates (Score ≥ 80 + Auditor Approval)

Individual archives: none ≥80.

**Cross-archive harness improvements (proposed as ECL.md edits):**

| # | Improvement | Evidence Source | Type | Risk |
|---|-------------|----------------|------|------|
| C1 | Add `validation_status: pass` gate to archive stage (§4) | Changes #4, #5 | Hard gate | Low — existing archive script already checks summary.md; gate is declarative |
| C2 | Add `phase` must be `validate` or `implement` to archive stage (§4) | Change #4 | Hard gate | Low — prevents planned-only changes from closing |
| C3 | Add lockfile atomicity hint to verification (§4) | Change #1 | Guidance | None — informational only |
| C4 | Add full-suite regression hint to validation (§4) | Change #2 | Guidance | None — informational only |
| C5 | Add parking failure isolation note (§3 or §4) | Changes #1, #5 | Guidance | None — process clarification |
| C6 | Add ADR existence check to plan review gate (§5) | Changes #3, #4 | Soft gate | Low — `docs/adr/` already exists |

## Application Plan

1. Edit `docs/ECL.md` §3 or §4 to add the 6 clarifications above.
2. Run `.\scripts\lint-ecl.ps1` to confirm structure.
3. Run `uv run ruff check src/ && uv run mypy src/ && uv run pytest` to confirm no regressions.
4. Record result in `harness/evolution/results.tsv`.
5. Run `.\scripts\harness-evolve.ps1 mark-complete`.
