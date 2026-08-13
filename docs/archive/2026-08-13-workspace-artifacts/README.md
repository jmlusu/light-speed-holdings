# Workspace Artifacts Archive — 2026-08-13

**Decision record for issue #10 ("Decide the fate of feasibility-study and workspace artifacts")**

## Disposition

These one-off feasibility-study, reconciliation, and workspace artifacts are archived here rather than deleted. They preserve decision history and are safe to reference, but are no longer live planning documents. Their tracking moved to:

- Live task tracking: GitHub wayfinder maps #7 (finish-dev / operate) and #33 (mission-control dashboard)
- Living status: `docs/STATUS.md`
- Architecture decisions: `docs/adr/`

## Contents

| File | Origin | Reason archived |
|------|--------|-----------------|
| `DATA_RECONCILIATION_PLAN.md` | 2026-07 data reconciliation plan | Superseded — all 20 architecture gaps (GAP-001…020) resolved and verified in `docs/ARCHITECTURE-GAPS.md` |
| `MILESTONES-DECK-SETUP.md` | Milestones deck setup report | One-off workspace artifact |
| `MILESTONES-DECK-SUMMARY.md` | Milestones deck summary | One-off workspace artifact |
| `README-milestones-deck.md` | Milestones deck generator README | One-off workspace artifact |
| `RECONCILIATION_PLAN.md` | 2026-07 doc reconciliation plan | Superseded by Sprint 7 doc reconciliation (archived ECL `2026-08-11-sprint-7-*`) |
| `SPRINT3-DELEGATION-SUMMARY.md` | Sprint 3 delegation report | Historical sprint artifact — Sprint 3 complete |

## Decision

- **Archived** (this folder), not deleted: preserves decision history, reversible.
- **Not moved**: `scripts/generate-milestones-deck.js` / `generate-milestones-deck.py` (functional generation scripts, referenced from this archive README if needed).
- **Superseded docs** — see `docs/STATUS.md` (living state), `docs/ARCHITECTURE-GAPS.md` (all resolved), and the wayfinder maps on GitHub.
