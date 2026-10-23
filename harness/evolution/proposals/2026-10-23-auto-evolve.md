---
title: "Auto-evolve proposal: 10 eligible archives (2026-09-25 to 2026-10-07)"
date: "2026-10-23"
trigger:
  reason: "reindex"
  eligible_count: 10
  threshold: 5
  window: 10
  excludes: ["auto-evolve-harness-", "auto-evolve"]
disposition: "record-only"
---

# Auto-evolve Proposal (Record-Only)

**This run is recorded, not applied.** Per CEO decision (2026-10-23), the 2026-10-07
backlog is a record-only evolution: candidates are scored and the constraints are
documented here as reusable knowledge, but no harness, governance, or source file
was changed by this run. The only files this run modified are the evolution
bookkeeping files (`state.json`, `results.tsv`, `INDEX.json`) and this proposal.

## Candidate Archives

| # | Archive ID | Title | Validation | Key Decisions |
|---|------------|-------|------------|---------------|
| 1 | 2026-09-25-ls-mem-implementation | LS-MEM implementation | pass | 7/7 reviewer blockers remediated; mypy 0 errors; gateway 5-gate + human approval; offline/deny-by-default tests; dual skill paths hash-identical |
| 2 | 2026-09-25-ls-mem-phase-3-data-model | LS-MEM phase 3 data model | pass | 13/13 handoff §8 memory types modelled; versioned schema, forward-only migrations; ADR-019/ADR-025 cross-refs |
| 3 | 2026-09-26-ls-mem-completion | LS-MEM completion | pass | Full non-e2e suite green (105 passed / 1 skipped); CLI lifecycle smoke; security report §7 CEO/HITL items; audit chain head verification |
| 4 | 2026-10-03-customer-journey-conversion-architecture-implementation | Customer journey conversion architecture implementation | **unknown** | Production Vercel build green; ls-artifact-qa 12/12; **ECL §4.1 gap: `validation_status` is `unknown`, not `pass`** |
| 5 | 2026-10-04-audit-export-reads-canonical-jsonl-trail | Audit export reads canonical JSONL trail | pass | Issue-5 fix: export repointed from decoy DB to hash-chained trail; local export runner + run log; CI freshness guard; backfill verified |
| 6 | 2026-10-07-2026-10-06-repository-sanitization | Repository sanitization | pass | 437 files changed (+2,932 / −20,771); ~1.1 GB dead weight removed; tracked files 107 → 32; baselines clean |
| 7 | 2026-10-07-2026-10-07-decommission-followups | Decommission follow-ups | pass | LS-MEM decommissioned (JSON MemoryStore single engine); `tmp/` deleted (126 scratch files); milestones `.py` kept |
| 8 | 2026-10-07-studio-scorecard-v1-instrumentation-t2-418 | Studio scorecard v1 instrumentation (T2 #418) | pass | 4 metrics + tracker YAML + new page + API; additive-only; pytest 2521 passed; ECL slot freed 2026-10-07 |
| 9 | 2026-10-07-t4-competitive-landscape-oct-refresh-420 | T4 competitive landscape Oct refresh (#420) | pass | Policy deltas (Malawi AI Bill stalled, national strategies in consultation); 8 external moves verified; 18-item re-check list |
| 10 | 2026-10-07-t5-canonical-org-truth-90-20 | T5 canonical org truth 90/20 | pass | Single-source census (90 agents = 89 AI + 1 human CEO); 20 departments; soT manifest correct; full suite green |

## Evidence: Verification Gaps / User Corrections / Reusable Constraints

### Verification Gaps

1. **`validation_status` not exactly `pass` at archive time**: `2026-10-03-customer-journey-conversion-architecture-implementation` archived with `validation_status: "unknown"` despite green sub-gates. ECL §4.1 requires exactly `pass`; changes without validation evidence must stay active or be parked.
2. **Stale-backlog risk**: this backlog was generated 2026-10-07 and sat unprocessed until 2026-10-23 (16 days, threshold exceeded since ~2026-10-11). The `pending.md` trigger has no staleness escalation.
3. **Bookkeeping-vs-application ambiguity**: nothing in the ECL forced this run to state whether accepted candidates would be *applied* or only *recorded*, which allowed a results row to imply documentation that did not exist.

### User Corrections

1. **Record-only decision (2026-10-23)**: CEO directed this evolution be record-only, i.e. no constraint documents or harness scripts are edited by this run.
2. **Accepted-candidates-only rule**: rejected candidates must be dropped, not carried forward.
3. **Branch review approved, merge gated on CI**: merge only after all 6 required checks are genuinely green.

### Reusable Constraints (Recorded, Not Applied)

1. **`validation_status` must be exactly `pass`** before archiving (ECL §4.1, already in force).
2. **Audit export must read the hash-chained JSONL trail**, never a decoy/legacy DB path; guard with a CI freshness check.
3. **Decommissions leave a single operational engine**; parallel legacy engines are removed rather than left dormant.
4. **Repo hygiene is a gate, not a chore**: 100+ tracked scratch files and GB-scale dead weight indicate the archive/close flow is not cleaning up; cleanup must be a close-gate item.
5. **Org census derives from a single source of truth manifest** (agent count, department count) and is validated by drift checks, not by hand-counted tables.
6. **Additive-only instrumentation overrides**: a candidate scoring 79 may be accepted on override when the change is purely additive (new optional fields, new tracker YAML, new collector/endpoint) and freed the ECL slot.
7. **Backlog staleness escalation**: a `pending.md` older than 7 days should be flagged in `harness-evolve check` output rather than silently waiting for the next trigger.
8. **Evolution dispositions must be explicit**: each `results.tsv` row must state `applied` or `record-only` and must not claim documentation that does not exist (AGENTS.md §15).

## Scoring

Scale: archive evidence (0–40), project relevance (0–30), rule clarity impact (0–30). ≥80 = accept.

| # | Candidate | Proposal | Auditor | Approve | Recommendation |
|---|-----------|----------|---------|---------|----------------|
| 1 | 2026-09-25-ls-mem-implementation | 83 | 85 | Yes | Accept |
| 2 | 2026-09-25-ls-mem-phase-3-data-model | 91 | 92 | Yes | Accept |
| 3 | 2026-09-26-ls-mem-completion | 98 | 100 | Yes | Accept |
| 4 | 2026-10-03-customer-journey-conversion-architecture-implementation | 64 | 75 | No | Reject — ECL §4.1 `validation_status: "unknown"` gap |
| 5 | 2026-10-04-audit-export-reads-canonical-jsonl-trail | 93 | 95 | Yes | Accept |
| 6 | 2026-10-07-2026-10-06-repository-sanitization | 83 | 85 | Yes | Accept |
| 7 | 2026-10-07-2026-10-07-decommission-followups | 91 | 93 | Yes | Accept |
| 8 | 2026-10-07-studio-scorecard-v1-instrumentation-t2-418 | 79 | 82 | Conditional | Accept on override — additive-only, slot freed, gates green |
| 9 | 2026-10-07-t4-competitive-landscape-oct-refresh-420 | 61 | 58 | No | Reject — low project relevance, no reusable internal pattern |
| 10 | 2026-10-07-t5-canonical-org-truth-90-20 | 98 | 100 | Yes | Accept |

## Accepted (7 + 1 override)

1. `2026-09-25-ls-mem-implementation` (85) — core memory engine, blockers remediated.
2. `2026-09-25-ls-mem-phase-3-data-model` (92) — 13/13 memory types, versioned schema.
3. `2026-09-26-ls-mem-completion` (100) — full suite green, CLI lifecycle complete.
4. `2026-10-04-audit-export-reads-canonical-jsonl-trail` (95) — audit integrity fix with CI guard.
5. `2026-10-07-2026-10-06-repository-sanitization` (85) — repo health, deferrals documented.
6. `2026-10-07-2026-10-07-decommission-followups` (93) — LS-MEM decommission, cleanup.
7. `2026-10-07-t5-canonical-org-truth-90-20` (100) — single-source org census.
8. `2026-10-07-studio-scorecard-v1-instrumentation-t2-418` (79 → override) — additive-only instrumentation.

## Rejected (2)

- `2026-10-07-t4-competitive-landscape-oct-refresh-420` (58) — external competitive data only; no reusable internal governance pattern.
- `2026-10-03-customer-journey-conversion-architecture-implementation` (64) — archived with `validation_status: "unknown"`, failing the ECL §4.1 gate; re-validating it is a separate change, not an auto-evolve application.

## Application Plan

**Record-only.** No files are edited by this run beyond evolution bookkeeping
(`state.json`, `results.tsv`, `INDEX.json`) and this proposal. The reusable
constraints above are retained as recorded knowledge for a future evolution run
that is explicitly in `applied` mode.

## 10 Script Reference

| Command | Script | Purpose |
|---------|--------|---------|
| `.\scripts\maintenance\harness-change.ps1 reindex` | harness-change.ps1 | Rebuild `INDEX.json` |
| `.\scripts\maintenance\harness-evolve.ps1 check` | harness-evolve.ps1 | Check auto-evolve threshold, generate `pending.md` |
| `.\scripts\maintenance\harness-evolve.ps1 mark-complete` | harness-evolve.ps1 | Mark evolution complete, clear `pending` |
| `.\scripts\maintenance\lint-ecl.ps1` | lint-ecl.ps1 | Validate ECL structure |

## 11 Rules

- `harness/changes/INDEX.json` is generated by script only. Never hand-edit.
- Active change files override `docs/STATUS.md` for the current task.
- Archive history is loaded selectively through STATUS paths or INDEX, never wholesale.
- A record-only evolution changes no file outside `harness/evolution/` and `INDEX.json`.
- Every `results.tsv` row must describe only changes that are independently verifiable in the diff (AGENTS.md §15).
