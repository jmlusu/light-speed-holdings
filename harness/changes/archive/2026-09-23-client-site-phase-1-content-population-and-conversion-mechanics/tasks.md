# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation.

## Implementation

- [x] T002 [P] Extend `src/components/site/CtaBand.tsx` with optional `onRequestBriefing` prop; when set, button invokes callback instead of only Link navigation.
- [x] T003 [P] Wire `src/pages/ResourcesPage.tsx` resource cards and CTA to `onRequestBriefing` with resource title prefill.
- [x] T004 [P] Wire `src/pages/EventsPage.tsx` event cards and "Request a Speaker" CTA to `onRequestBriefing`.
- [x] T005 Create `src/components/NewsletterSignup.tsx` posting to `/api/enquiry` (`form: contact`, `enquiryType: Newsletter subscription`) with honeypot + Turnstile.
- [x] T006 [P] Mount NewsletterSignup on `NewsPage` and `InsightsPage`; add Insights ↔ News cross-links if low-cost.

## Validation

- [x] T007 Run `bun run lint` and `bun run build`; fix any errors.

## Deferred Tasks

- Real PDF hosting for resource downloads (needs assets + storage decision).
- Dedicated speaking-inquiry form separate from briefing modal.
- Content authoring for thin editorial sections (separate content track).
