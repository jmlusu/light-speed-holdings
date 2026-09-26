# Harness Evolution Pending

Generated at: 2026-09-25T00:38:51

## Trigger

- Reason: close
- Eligible archived changes since last evolution: 5
- Threshold: 5
- Scan window: 10
- INDEX source: harness/changes/INDEX.json
- Excludes: archive ids beginning with auto-evolve-harness- and archives tagged auto-evolve

## Candidate Archives

- harness/changes/archive/2026-09-22-add-curated-remote-scrapes-to-the-malawi-job-search-track/summary.md
- harness/changes/archive/2026-09-22-fix-athena-serialize-decimal-salary-ranges-in-jsonl-store/summary.md
- harness/changes/archive/2026-09-23-client-site-phase-1-content-population-and-conversion-mechanics/summary.md
- harness/changes/archive/2026-09-23-client-site-phase-3-trust-evidence-and-related-content/summary.md
- harness/changes/archive/2026-09-23-narrative-and-positioning-track-lightspeed-narrative-positioning-document/summary.md
- harness/changes/archive/2026-09-24-ai-venture-studio-web-experience-brand-psychology/summary.md
- harness/changes/archive/2026-09-24-lightspeed-ai-company-builder-web-experience-architecture-v2-0/summary.md
- harness/changes/archive/2026-09-24-ls-mem-phase-2-architecture/summary.md
- harness/changes/archive/2026-09-24-v2-implementation-p2-public-registry-transform/summary.md
- harness/changes/archive/2026-09-25-ls-mem-phase-3-data-model/summary.md

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
