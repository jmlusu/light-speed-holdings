---
title: "Auto-evolve proposal: 10 eligible archives (2026-08-17 → 2026-09-14)"
date: 2026-09-16
trigger:
  reason: close
  eligible_count: 7
  threshold: 5
  window: 10
  excludes: ["auto-evolve-harness-", "auto-evolve"]
---

# Auto-evolve Proposal

## Candidate Archives (current window, rebuilt 2026-09-16)

| # | Archive ID | Title | Validation | Key Decisions |
|---|------------|-------|------------|---------------|
| 1 | phase-b-async-approval-engine-42 | Phase B: Async Approval Engine (#42) | pass | File-based suspend store (not Temporal); 30-day retention with daemon sweep; HITL park persists loop state; webhook HMAC |
| 2 | phase-b-opentelemetry-tracing-40 | Phase B: OpenTelemetry Tracing (#40) | unknown | OTel API-only interface; correlated ContextVar; archived at plan phase previously flagged |
| 3 | security-hardening-...-canary-release | Security Hardening / Trivy / S3 backup / canary | unknown | `.env` gitignored; compose `${VAR:-}` fail-closed; Trivy on tagged releases only |
| 4 | dependency-remediation-...-streak-fix | Dependency remediation + monitoring streak fix | pass | Lockfile-only `uv lock` upgrade; streak-based health check; dependabot PR #155 merged; httpx2 deferred to issue |
| 5 | cleanup-dummy-tasks | Remove Dummy Tasks & Wire Real Organizational Data | pass | Marker-only dummy detection (receiver-name heuristic removed); case-sensitive `instr()/GLOB`; `include_test` param; full-suite gate 2223 passed |
| 6 | dashboard-hardening-c4-c5 | Dashboard Hardening: C4 Task Flow + C5 ReportStore | pass | ReportStore over `results/`; read-only traversal-guarded; codenames resolved via CEO; **full suite left in "Next Step" at archive** |
| 7 | ceo-alert-center | CEO Alert Center | passed | FileStore alert store; active→ack/snooze/cleared lifecycle; RBAC-gated writes; dedupe by rule key |
| 8 | executive-kpi-scorecard-rich-org-chart | Executive KPI Scorecard + Rich Org Chart | passed | Weighted executive health; source=`real_telemetry`/`configured`; 30s-TTL org metrics |
| 9 | pharos-content-intelligence-p0 | Pharos P0: routine engine + content KPIs | pass | Crash-safe mark-before-send `RoutineScheduler`; tags-based provenance; `--routine-interval`; full suite 2117 |
| 10 | pharos-content-intelligence-p1-p2 | Pharos P1/P2: deep-research, publishing rails, Whisper, MCP | pass | stdio JSON-RPC MCP; dry-run publisher default; optional `pharos-whisper` extra; full suite 2162 |

## Evidence: Repeated Failures / Verification Gaps / User Corrections / Reusable Constraints

### Verification Gaps

1. **Archive closed with full-suite gate deferred to "Next Step" (#6).** `dashboard-hardening-c4-c5` was archived after scoped dashboard/report suites only; its "Next Step" literally reads *"Full-suite `pytest -m "not e2e"` as the final gate, then close"* — i.e. it was owned as a remain-open item by the archive itself. ECL §4 says "run the full test suite" but does not forbid `status: completed` with the full run still pending. Two prior evolutions (2026-08-19) named this the dominant gap; it recurs.
2. **Archive front-matter vocabulary drift.** Two archives use `validation_status: "passed"` (#7, #8) — the ECL §4 contract is the literal value `pass`. #8 uses `phase: "done"` while ECL §4 requires `validate` or `implement` (lint-ecl.ps1's regex also accepts `done`, so the rule text and the enforcer disagree).
3. **`spec_review` left `pending` on archived changes (#7, #8).** Both the CEO Alert Center and Executive KPI archives were closed as completed with `spec_review: "pending"` still present. ECL §4 gate list covers `validation_status`/`phase` but nothing requires spec review to be resolved at archive.
4. **Concurrent-writer / live-daemon test crashes (#5).** `cleanup-dummy-tasks` documented two full-suite runs crashing at 100% in pytest tmp-dir teardown (`PermissionError` on `pytest-of-jmlus\pytest-current` held by the live dashboard process) plus a concurrent AI session hammering the same suite on shared files. The fix (unique `--basetemp` + pre/post `git status` snapshot, tree unchanged) is in the archive but not the shared rules. Pharos archives later used `--basetemp=".pytest_tmp_p0"` (same practice, ad hoc).
5. **Retroactive ECL accepted (#4).** Dependency remediation shipped directly to main and was recorded retroactively. Accepted for handoff continuity, but it is a process escape worth an explicit note (not a new gate).

### User Corrections

- **#5**: "Routing a task to the real `test-agent` receiver is legitimate and must NOT mark it as dummy." The over-broad receiver-name heuristic was removed after it false-positived on the real `test-agent` and broke tests.
- **#6**: Undocumented codenames "Path-of-RPG"/"FLORA" required CEO clarification → task-flow traceability + reports viewer. Corollary: undefined codenames in spec text cost a round-trip.
- **#9**: `plan.md`'s `metadata.routine_run_id` framing was reconciled to `tags` at implementation because the `Task` model drops arbitrary `metadata` dicts (`extra="ignore"`). Plan/implementation drift reconciled during impl, not at spec review.

### Reusable Constraints (Rules to Clarify / Keep)

| Constraint | Source | Current ECL Status | Proposed Action |
|-----------|--------|-------------------|-----------------|
| Full non-e2e suite must complete at archive; `status: completed` must not close with "full suite in Next Step" | #6, #5 | §4 says run full suite, no explicit prohibition on deferring | Clarify §4: full suite must be among `validation_results` at archive; "Next Step" may only list genuine follow-ups |
| Unique `--basetemp` + pre/post `git status` snapshot when live daemon or concurrent sessions exist | #5, #9, #10 | Not mentioned | Add as verification hint in §4 |
| `validation_status` must be exactly `pass`; `phase` must be `validate`/`implement` (not `done`) at archive | #7, #8, #2 | §4 states it; lint regex and archived data drift | Align lint-ecl.ps1 with §4 text (drop `done`); clarify vocabulary in §4 |
| `spec_review` must be resolved (not `pending`) before archive | #7, #8 | Not required | Add to §4 archive gates |
| Undefined codenames in spec must be defined before plan review | #6 | Not mentioned | Guidance in §5 plan review gate |
| Known side-effect files (`docs/AGENT-REGISTRY-TABLE.md`, `hr/onboarding_requests.yaml`, `orchestrator/approvals.yaml`) must be git-restored before archive | #5 | Not mentioned | Add to §4 as archive hygiene |

## Scoring & Recommendations

Scoring: archive evidence (0-40), project relevance (0-30), rule clarity impact (0-30). ≥80 = accept.

| # | Candidate Change | Evidence | Relevance | Clarity | Score | Recommendation |
|---|-----------------|----------|-----------|---------|-------|----------------|
| 1 | Async Approval Engine | 36 | 14 | 12 | 62 | REJECT as standalone — clean pass, no new harness delta |
| 2 | OpenTelemetry Tracing | 8 | 20 | 20 | 48 | REJECT — previously flagged `unknown`; feeds vocabulary gate only |
| 3 | Security Hardening | 10 | 20 | 18 | 48 | REJECT — previously flagged `unknown`; no new constraint |
| 4 | Dependency Remediation | 38 | 16 | 14 | 68 | REJECT as standalone — retroactive escape noted, not a rule |
| 5 | Cleanup Dummy Tasks | 38 | 18 | 20 | 76 | REJECT as standalone — but the `--basetemp` + side-effect hygiene are strong reuse candidates |
| 6 | Dashboard Hardening C4/C5 | 30 | 18 | 22 | 70 | REJECT as standalone — but the deferral-of-full-suite gap is the top reusable constraint |
| 7 | CEO Alert Center | 28 | 12 | 16 | 56 | REJECT — vocabulary drift source (`passed`, `spec_review: pending`) |
| 8 | Executive KPI + Org Chart | 26 | 12 | 16 | 54 | REJECT — vocabulary drift source (`done`, `passed`) |
| 9 | Pharos P0 | 38 | 26 | 20 | 84 | ACCEPT-adjacent — clean pass + reusable `--basetemp` and tags-provenance practice |
| 10 | Pharos P1/P2 | 40 | 26 | 20 | 86 | ACCEPT-adjacent — clean pass; dry-run publisher + MCP RBAC are reusable constraints |

**No individual archive scores need to be accepted on their own; the archive scores are evidence, not rules.** As in the two prior evolutions, the cross-archive pattern analysis yields 6 concrete clarifications (below) that address the material gaps: full-suite-at-archive, batch isolation, front-matter vocabulary, spec review resolution, codename definition, side-effect hygiene.

## Accepted Candidates (Score ≥ 80 + Auditor Approval)

Individual archives: none accepted as rules.
**Cross-archive harness improvements (proposed as ECL.md clarifications + one lint alignment):**

| # | Improvement | Evidence Source | Type | Risk |
|---|-------------|----------------|------|------|
| C1 | §4: full non-e2e suite must be listed in `validation_results` at archive; closing with "full-suite in Next Step" is invalid | #5, #6 | Clarification | None |
| C2 | §4: verification hint — unique `pytest --basetemp` + pre/post `git status` snapshot under concurrency | #5, #9, #10 | Guidance | None |
| C3 | §4: `validation_status` literal `pass` (not `passed`); `phase` literal `validate`/`implement` (not `done`) | #7, #8 | Clarification | Low — updates lint regex to match text |
| C4 | §4: `spec_review` must be resolved before archive | #7, #8 | Clarification | None |
| C5 | §5: undefined codenames/terms in spec must be defined before plan review | #6 | Guidance | None |
| C6 | §4: archive hygiene — git-restore known side-effect files before archive | #5 | Clarification | None |

## Application Plan

1. Edit `docs/ECL.md` §4/§5 with C1-C6.
2. Align `scripts/lint-ecl.ps1` with §4 vocabulary (drop `done` from the accepted phase set, consistent with rule text).
3. Run `.\scripts\lint-ecl.ps1` to confirm structure.
4. Run `uv run ruff check src/ && uv run mypy src/` to confirm no regressions (harness docs + script only, but cheap).
5. Record one terminal result in `harness/evolution/results.tsv`.
6. Run `.\scripts\harness-evolve.ps1 mark-complete`.
