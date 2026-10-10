# Harness Evolution Pending

Generated at: 2026-10-07T22:57:58

## Trigger

- Reason: reindex
- Eligible archived changes since last evolution: 6
- Threshold: 5
- Scan window: 10
- INDEX source: harness/changes/INDEX.json
- Excludes: archive ids beginning with auto-evolve-harness- and archives tagged auto-evolve

## Candidate Archives

- harness/changes/archive/2026-09-25-ls-mem-implementation/summary.md
- harness/changes/archive/2026-09-25-ls-mem-phase-3-data-model/summary.md
- harness/changes/archive/2026-09-26-ls-mem-completion/summary.md
- harness/changes/archive/2026-10-03-customer-journey-conversion-architecture-implementation/summary.md
- harness/changes/archive/2026-10-04-audit-export-reads-canonical-jsonl-trail/summary.md
- harness/changes/archive/2026-10-07-2026-10-06-repository-sanitization/summary.md
- harness/changes/archive/2026-10-07-2026-10-07-decommission-followups/summary.md
- harness/changes/archive/2026-10-07-studio-scorecard-v1-instrumentation-t2-418/summary.md
- harness/changes/archive/2026-10-07-t4-competitive-landscape-oct-refresh-420/summary.md
- harness/changes/archive/2026-10-07-t5-canonical-org-truth-90-20/summary.md

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
