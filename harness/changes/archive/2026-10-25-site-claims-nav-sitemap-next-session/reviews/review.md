# Review

## Intake Review

- Status: pending
- Notes:

## Spec Review

- Status: pending
- Open high-impact clarifications:
- WHAT/HOW separation:

## Plan Review

- Status: approved
- Reviewer: implementing session (self-review against `spec.md` and `plan.md`, 2026-10-25)
- Basis for approval: the plan's four P0 items map one-to-one onto the spec's four success criteria, each with an independent PR branch from `origin/main` and a co-located guard test. D1/D2/D3 are recorded as approved assumptions in `summary.md` and were executed as written. The gaps below were found while executing and were resolved in favour of the spec (the stricter document), not the plan.
- Spec gaps found from planning:
  1. **P0-1 scope was under-counted.** The plan listed five components plus two data files; the spec's success criterion ("zero occurrences ... outside a documented allowlist") is satisfied only if every occurrence in `src/` is fixed. Actual count was ~20 files across copy, registries and generated data. Resolved by expanding the change and documenting the allowlist in `src/__tests__/claims.test.ts`.
  2. **P0-1 insight articles were under-counted.** The plan named one article (`insights.ts:233` is actually a different article and the line had moved). Six published articles carried the old count. Resolved with an optional `correction` field rendered above each article; bodies untouched, per the spec constraint.
  3. **P0-4 `testCount` target is stale by construction.** The plan says 87 (the pre-change vitest total). Shipping the change adds guard tests, so the verified total becomes 109. Resolved by publishing 109 and making the guard test compare code to the registry description instead of a frozen literal.
  4. **P0-2 risk mitigation is conditional and did not trigger.** The plan's fallback (group Use Cases + Sectors under a "Proof" menu) was not needed: at 1024 px the nav ends at x=741 and the CTA starts at x=840. Measured, not assumed.
  5. **Task T008's third assertion was written loosely** (`a.type !== 'executive' || a.id !== 'human-ceo'`). Implemented as `agents.filter(a => a.id !== 'human-ceo').length === 89`, which states the same intent without relying on type naming.
  6. **Line numbers in the plan are advisory.** T006/T012/T013 targets had shifted; edits were applied by symbol/slug and the results verified by test.

## Code Review

- Status: approved
- Reviewer: implementing session, per-PR review on the pushed branches (2026-10-25)
- Notes: each branch was reviewed as a self-contained diff against `origin/main` and re-verified after rebase. Findings: (1) `metrics.testCount` describes the merged suite, so it was re-checked on `main` (109/109) rather than trusted from the branch; (2) the claims allowlist is limited to published article bodies, the historical claims registry and the metrics audit trail — everything else in `src/` is corrected; (3) no unrelated files were included in any of the three commits (the `ruff-templates` hook rewrite of an untouched deck script was reverted each time).

## Validation Review

- Status: approved
- Notes: see `summary.md` § Validation. `main` CI green at `7d3b0b01`; `main` tsc clean and 109/109 vitest; production deployment success with 20/20 browser checks and a 44-URL sitemap; `lint-ecl.ps1` PASS. P1/P2 items were not attempted and are recorded as out of scope.