# Spec

## Intake Review

- Intake type: Small Change | Structured Change
- Input shape: requirement-first | plan-first | mixed
- Questions asked this round: 0

## Goal And Evidence

- **Real problem or user request**: Refresh competitive-landscape.md baseline v2 (2026-10-07) to November 2026 state (2026-11-10) per T5 #447.
- **Current behavior**: Baseline v2 outdated; §8 "October 2026 Delta" header link exists but section was never written; 18-item re-check list from Oct still open.
- **Source of evidence**: docs/marketing/competitive-landscape.md §§1–7, monthly checklist §7, policy sources (AU, SADC, MACRA, UNDP/World Bank, UNESCO); public company pages; LinkedIn staff counts; press releases.

## User Scenarios And Success

- **Primary user/system scenario**: T5 #447 competitive landscape Nov refresh — update baseline v2 → v3, write §8 November 2026 Delta, advance monthly checklist, post CEO brief, open PR, update map #416.
- **Success criteria**: competitive-landscape.md updated to v3; header updated to Baseline v3; §8 "November 2026 Delta" present with all required content; §7 monthly checklist advanced to next date (2026-12-16); source URLs stamped with access dates; honesty tags (VERIFIED / VENDOR CLAIM / UNCONFIRMED) per ADR-020/033; no fabricated metrics/dates/quotes.
- **Acceptance criteria**: Same as success criteria.

## Non-Goals

- No absorption of Issue #310 (SADC social-media competitor landscape) in this change. That remains a separate deliverable.
- No fabricated or estimated metrics beyond what is publicly verifiable.

## Constraints

- ADR-020/033 honesty tags (VERIFIED / VENDOR CLAIM / UNCONFIRMED) mandatory on all claims.
- §7 monthly checklist intact and advanced to 2026-12-16.
- ECL change lifecycle: complete → validate → lint-ecl.ps1 → phase transition.
- main is protected: branch + PR; 6 required checks must pass before merge.
- No unrelated dirty file modifications: data/orchestrator/cost_tracker.json, open-design submodule, src/data/generated/agent-registry.public.json left as-is.

## Assumptions

- All public data verified on or before 2026-11-10. Any post-date information left UNCONFIRMED.
- No player has launched a governed-agentic-org product between Oct and Nov refresh dates.

## Open Questions

- **Resolved:** the missing October delta is noted inside the November delta section itself, not in the section header - the header links to the new section and the section carries an honest note that the October entry was never written. Delivered in `docs/marketing/competitive-landscape.md` section 8.
  - The section header link (§8) currently points to a non-existent October delta; November refresh writes the first-ever §8 while adding an honest note about the October gap.

## Resolved Clarifications

- November 2026 Delta (§8) written from verified sources only.
- Baseline v3 header replaces v2; source URLs stamped.
- §7 monthly checklist advanced from 2026-11-16 to 2026-12-16.
- Gap 5 false claim in social-media-positioning-status.md addressed as a follow-on (not part of this change).
