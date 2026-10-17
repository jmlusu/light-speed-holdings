---
title: "Auto-evolve proposal: 10 eligible archives (2026-08-31 → 2026-09-23)"
date: 2026-09-23
trigger:
  reason: close
  eligible_count: 6
  threshold: 5
  window: 10
  excludes: ["auto-evolve-harness-", "auto-evolve"]
---

# Auto-evolve Proposal

## Candidate Archives (current window, rebuilt 2026-09-23)

| # | Archive ID | Title | Validation | Key Decisions |
|---|------------|-------|------------|---------------|
| 1 | 2026-08-31-ceo-alert-center | CEO Alert Center | **passed** (gate: `pass`) | FileStore alert store; active→ack/snooze/cleared lifecycle; RBAC-gated writes; dedupe by rule key; `spec_review: pending` still present |
| 2 | 2026-08-31-executive-kpi-scorecard-rich-org-chart | Executive KPI Scorecard + Rich Org Chart | **passed** (gate: `pass`) | Weighted executive health; source=`real_telemetry`/`configured`; 30s-TTL org metrics; `phase: done` + `spec_review: pending` |
| 3 | 2026-09-14-pharos-content-intelligence-p0 | Pharos P0: routine engine + content KPIs | pass | Crash-safe mark-before-send `RoutineScheduler`; tags-based provenance; full suite 2117 |
| 4 | 2026-09-14-pharos-content-intelligence-p1-p2 | Pharos P1/P2: deep-research, publishing rails, Whisper, MCP | pass | stdio JSON-RPC MCP; dry-run publisher default; full suite 2162 |
| 5 | 2026-09-21-athena-mvp | Athena MVP – Job & Consultancy Application Platform | pass | Job/consultancy application platform MVP |
| 6 | 2026-09-22-add-curated-remote-scrapes… | Add curated remote scrapes to Malawi job-search track | pass | Curated remote scrapes track |
| 7 | 2026-09-22-fix-athena-decimal-salary-ranges | fix(athena): serialize Decimal salary ranges in JSONL | pass | Decimal→JSON-safe serialization in JSONL store |
| 8 | 2026-09-23-client-site-phase-1… | Client Site Phase 1 – Content Population + Conversion | **passed** (gate: `pass`) | Content population + conversion mechanics; closed with `validation_status: "passed"` after §4 already required `pass` |
| 9 | 2026-09-23-client-site-phase-3… | Client Site Phase 3 – Trust Evidence + Related Content | **unknown** (gate: `pass`) | Trust evidence + related content; `phase: "plan"` + `validation_status: "unknown"` at archive despite Validation section recording `bun run lint`/`build`/`lint-ecl` pass |
| 10 | 2026-09-23-narrative-and-positioning-track… | Narrative and Positioning Track | **passed** (gate: `pass`) | LightSpeed narrative & positioning document; closed with `validation_status: "passed"` after §4 already required `pass` |

Outside the last-10 window but same class of evidence (eligible set, 24 total):

| Archive ID | Validation | Notable |
|------------|------------|---------|
| 2026-08-30-cleanup-dummy-tasks | pass | **Unresolved git conflict markers** in `summary.md` front matter (`<<<<<<< HEAD` / `=======` / `>>>>>>> origin/main` around `updated_at`) |
| 2026-08-08-sprint-4-quality-completeness | pass | `phase: done` (not a valid archive phase) |
| 2026-08-11-sprint-7-tool-vocabulary… | **unknown** | Validation section: "Pending final gates" |
| 2026-08-17-phase-b-opentelemetry-tracing-40 | **unknown** | `phase: plan`; Validation section: "Pending (see tasks.md)" |
| 2026-08-17-security-hardening…canary-release | **unknown** | Validation section: "Pending." |

## Evidence: Repeated Failures / Verification Gaps / User Corrections / Reusable Constraints

### Verification Gaps

1. **2026-09-16 rules were written but never enforced on archives.** ECL §4 now states (lines 43–45) that `validation_status` must be exactly `pass`, `phase` must be `validate`/`implement`, and `spec_review` must be resolved before archiving. `scripts/lint-ecl.ps1` still only validates the *active* change (when `active/summary.md` exists) plus INDEX freshness and version consistency — **it never scans `archive/*/summary.md`**. Every archive gate violation therefore passes CI/lint indefinitely.

2. **New violations continued after the rule shipped.** Archives closed on 2026-09-23 (`client-site-phase-1`, `narrative`, `client-site-phase-3`) violate the literal §4 vocabulary that was already on main since 2026-09-16. Text-only rules without an enforcer do not stick.

3. **Close-time gate is incomplete.** `harness-change.ps1` `Validate-Change` for `status: completed` only asserts `Get-ValidationStatus -eq "pass"` (and pending-task explanation). It does **not** assert `phase ∈ {validate, implement}` nor `spec_review` resolution. Combined with (2), `phase: "plan"` and `spec_review: "pending"` archives exist.

4. **`Get-ValidationStatus` early-return path.** When front matter has `validation_status: "passed"` / `"unknown"`, the function returns that raw value (not normalized). Close *should* throw `-ne "pass"` — yet those archives exist as completed. Either close was bypassed, front matter was edited after close, or an older script path ran. **Lint re-scan of archives is the durable fix** regardless of which path produced the drift.

5. **Conflict markers survived a merge into archive content.** `2026-08-30-cleanup-dummy-tasks/summary.md` still contains unresolved `<<<<<<<`/`=======`/`>>>>>>>` around `updated_at`. ECL has no archive hygiene check for conflict markers; lint does not scan archive text.

6. **Historical `unknown` + `plan` archives are process debt.** OTel (`phase: plan`, Validation "Pending") and tool-vocabulary/security-hardening (`unknown`, "Pending") were flagged as vocabulary sources in 2026-09-16 and remain uncleared.

### User Corrections

- None new this window. Prior corrections that still bind: no invented numbers/facts; close must not defer full suite to "Next Step" (2026-09-16 C1); side-effect files git-restored before archive (2026-09-16 C6).

### Reusable Constraints (Rules to Clarify / Keep)

| Constraint | Source | Current ECL Status | Current Enforcer | Proposed Action |
|-----------|--------|--------------------|------------------|-----------------|
| Archive front-matter gates (`validation_status=pass`, `phase∈{validate,implement}`, `spec_review≠pending`) | 9 violating archives incl. 3 closed *after* §4 text landed | Stated in §4 L43–45 | **None for archives** — lint only checks active | **C1:** extend `lint-ecl.ps1` to scan every `archive/*/summary.md` |
| Close-time phase + spec_review gates for completed | phase-3 (`plan`), ceo/kpi (`pending`) | Stated in §4 | Partial — validation_status only in `Validate-Change` | **C2:** add `phase` + `spec_review` assertions to `Validate-Change` completed branch |
| No git conflict markers in harness change files | cleanup-dummy-tasks front matter | Not stated | None | **C3:** lint fails on `<<<<<<<`/`>>>>>>>` in active+archive summaries |
| Data remediation so gates can pass honestly | 9 archive violations | §4 says non-evidence changes "must remain active or parked" | N/A | **C4:** one-time fix of vocabulary drift where Validation evidence exists; park/re-status only where evidence is truly absent (do not invent `pass`) |

## Scoring & Recommendations

Scoring: archive evidence (0-40), project relevance (0-30), rule clarity impact (0-30). ≥80 = accept.

| # | Candidate Change | Evidence | Relevance | Clarity | Score | Recommendation |
|---|-----------------|----------|-----------|---------|-------|----------------|
| 1 | CEO Alert Center | 28 | 14 | 16 | 58 | REJECT standalone — vocabulary/spec_review drift source |
| 2 | Executive KPI + Org Chart | 26 | 14 | 16 | 56 | REJECT standalone — vocabulary/phase/spec_review drift source |
| 3 | Pharos P0 | 38 | 18 | 14 | 70 | REJECT standalone — clean pass, no new harness delta |
| 4 | Pharos P1/P2 | 40 | 18 | 14 | 72 | REJECT standalone — clean pass |
| 5 | Athena MVP | 34 | 16 | 10 | 60 | REJECT standalone — clean pass |
| 6 | Malawi remote scrapes | 34 | 14 | 10 | 58 | REJECT standalone — clean pass |
| 7 | Athena Decimal fix | 36 | 16 | 12 | 64 | REJECT standalone — clean pass |
| 8 | Client Site Phase 1 | 36 | 26 | 30 | **92** | ACCEPT as evidence — closed **after** §4 with illegal `passed` |
| 9 | Client Site Phase 3 | 40 | 26 | 30 | **96** | ACCEPT as evidence — `unknown` + `phase: plan` despite recorded gates |
| 10 | Narrative Track | 34 | 24 | 30 | **88** | ACCEPT as evidence — closed **after** §4 with illegal `passed` |

**Cross-archive harness improvements (score derived from #8–#10 + residual window violations):**

| # | Improvement | Evidence Source | Type | Risk | Auditor Score | Decision |
|---|-------------|----------------|------|------|---------------|----------|
| C1 | `lint-ecl.ps1`: fail when any `archive/*/summary.md` completed entry has `validation_status≠pass`, `phase∉{validate,implement}`, or `spec_review=pending` | #1, #2, #8, #9, #10 + 4 more | Enforcement of existing §4 | None — clarifies existing rule | **97** (40+28+29) | **APPROVE** |
| C2 | `harness-change.ps1` `Validate-Change`: for completed, also require `phase` ∈ {validate, implement} and `spec_review` ≠ pending | #1, #2, #9 | Close-time gate | None — matches §4 L44–45 | **88** (34+27+27) | **APPROVE** |
| C3 | `lint-ecl.ps1`: fail on `<<<<<<<` / `>>>>>>>` conflict markers in active or archive `summary.md` | cleanup-dummy-tasks | Hygiene | None | **79** (30+24+25) | **REJECT** (below 80) |
| C4 | One-time archive data remediation (normalize vocabulary where evidence exists; **never invent `pass` or `approved`**) | 9 violations | Application | Low — data honesty | **91** (38+29+24) | **APPROVE** (amended wording below) |

### C4 honesty amendments (auditor flags — binding)

1. **Strike** "or Validation evidence" for `spec_review`. Resolving `pending` → `approved` requires `reviews/review.md` (or equivalent Spec Review section) showing approved status. Green tests are not a spec review.
2. **Retract** any implication that C4 alone makes `lint-ecl.ps1` green. Archives whose spec_review or Validation remain honestly unresolved will keep C1 red until those are resolved or the change is re-statused — that is correct behavior, not a lint bug.
3. **`client-site-phase-3` `validation_status: unknown`:** do not flip to `pass` on the three recorded gates alone (no full-suite evidence). Either re-run the required suite and record it, or leave `unknown` and accept C1 failure until revalidated.
4. Conflict-marker cleanup in cleanup-dummy-tasks is **not** part of approved C4 scope (C3 rejected); may still be fixed opportunistically as data hygiene but is not required for this cycle.

## Accepted Candidates (Score ≥ 80 + Auditor Approval)

| # | Improvement | Score | Target |
|---|-------------|-------|--------|
| C1 | Archive front-matter scan in lint | 97 APPROVE | `scripts/lint-ecl.ps1` |
| C2 | Close-time phase + spec_review gates | 88 APPROVE | `scripts/harness-change.ps1` |
| C4 | Honest front-matter remediation (amended) | 91 APPROVE | `harness/changes/archive/*/summary.md` |
| C3 | Conflict-marker scan | 79 REJECT | *not applied this cycle* |

## Application Plan

1. ~~Request independent auditor score~~ — done: C1/C2/C4 approve, C3 reject.
2. Apply C1, C2, C4 only (score ≥ 80 + approval). Do not apply C3.
3. Remediate archive front matter (C4, amended):
   - `passed` → `pass` where Validation section records pass outcomes (#1, #2, #8, #10).
   - `phase: done` → `validate` where implementation/validate evidence exists (#2, sprint-4).
   - `phase: plan` → `validate` **only** if Validation evidence supports completed gates; otherwise leave `plan` and accept C1 failure until revalidated (#9 / phase-3 Validation has lint/build/lint-ecl only — **leave `unknown` unless full suite re-run**).
   - `spec_review: pending` → `approved` **only** if `reviews/` (or equivalent Spec Review record) shows approved; otherwise leave pending and accept C1 failure.
   - Archives with Validation text "Pending" (OTel, security-hardening, tool-vocab): re-run minimal gates or leave flagged — **never write `pass` without evidence**.
4. Run gates: `.\scripts\lint-ecl.ps1`, `uv run ruff check src/`, `uv run mypy src/`. If C1 fails only on honestly unresolved archives, record that in results.tsv rather than faking data.
5. Append one terminal row to `harness/evolution/results.tsv`.
6. Run `.\scripts\harness-evolve.ps1 mark-complete`.

---

**Auditor:** process-quality-manager (independent), 2026-09-23. Scores above.
