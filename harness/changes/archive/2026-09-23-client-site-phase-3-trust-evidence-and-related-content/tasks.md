# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation.

## Implementation

- [x] T002 [P] Add `trustEvidence` to `src/data/siteContent.ts` from existing governance/security facts with honesty labels.
- [x] T003 [P] Create `src/components/site/RelatedLinks.tsx`.
- [x] T004 [P] Extend TrustPage with evidence + honesty policy + RelatedLinks + CtaBand `onRequestBriefing`.
- [x] T005 [P] Wire FAQPage and LeadershipPage CTA to `onRequestBriefing`; add RelatedLinks.
- [x] T006 [P] Refactor News/Insights/Resources/Events related strips to RelatedLinks.

## Validation

- [x] T007 Run `bun run lint`, `bun run build`, `pwsh scripts/lint-ecl.ps1`.

## Deferred Tasks

- Harness auto-evolve (`harness/evolution/pending.md`) — separate maintenance track.
- Third-party certification seals (not inventible without evidence).
