# Harness Evolution Pending

Generated at: 2026-08-11T22:27:16

## Trigger

- Reason: close
- Eligible archived changes since last evolution: 5
- Threshold: 5
- Scan window: 10
- INDEX source: harness/changes/INDEX.json
- Excludes: archive ids beginning with auto-evolve-harness- and archives tagged auto-evolve

## Candidate Archives

- harness/changes/archive/2026-08-08-sprint-4-quality-completeness/summary.md
- harness/changes/archive/2026-08-09-sprint-5-t009-oauth2-client-credentials/summary.md
- harness/changes/archive/2026-08-10-audit-fixes-and-runtime-hardening/summary.md
- harness/changes/archive/2026-08-11-sprint-7-documentation-reconciliation-and-remaining-gap-019-fixes/summary.md
- harness/changes/archive/2026-08-11-sprint-7-tool-vocabulary-hitl-expiry-quality-hardening-doc-reconciliation/summary.md

These candidates are the trigger snapshot. Before processing, rebuild `harness/changes/INDEX.json`
and use the current eligible archive window so changes closed after this file was generated are not
missed.

## Instruction For Codex

Run harness auto-evolve:
1. Read docs/ECL.md and this pending file.
2. Rebuild `harness/changes/INDEX.json`, then inspect the current eligible archive window first.
3. Read spec/plan/tasks/reviews only when evidence requires it.
4. Extract repeated failures, verification gaps, user corrections, and reusable constraints.
5. Generate `harness/evolution/proposals/YYYY-MM-DD-auto-evolve.md` from the proposal template in docs/ECL.md before editing harness files.
6. Request one independent auditor/subagent score before applying.
7. Apply only accepted candidates with archive evidence, project relevance, score >= 80, and independent approval.
8. Prefer clarifying existing rules over adding new sections, documents, scripts, or workflows.
9. Run harness checks and relevant business gates.
10. Record one terminal result in `harness/evolution/results.tsv`.
11. Run `harness-evolve mark-complete` after writing the result.
