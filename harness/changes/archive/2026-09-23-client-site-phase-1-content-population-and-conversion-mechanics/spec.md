# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: requirement-first
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: Client-facing site has dead-end resource/event cards and no newsletter path; Phase 1 of the approved multi-phase site plan.
- Current behavior: Resource and event cards render ArrowRight but no click handler; CtaBand always links to `/contact`; no NewsletterSignup component exists.
- Source of evidence: `src/pages/ResourcesPage.tsx`, `src/pages/EventsPage.tsx`, `src/components/site/CtaBand.tsx`, approved plan (Phase 4 conversion mechanics).

## User Scenarios And Success

- Primary user/system scenario: Visitor clicks a resource or event CTA and is routed into a lead-capture path (briefing modal or newsletter form) with context preserved.
- Success criteria: Cards clickable; newsletter form posts to `/api/enquiry`; Events page has speaker CTA wired to briefing modal.
- Acceptance criteria: `bun run lint` and `bun run build` pass; no dead ArrowRight affordances on Resources/Events; NewsletterSignup renders on News and Insights.

## Non-Goals

- Real PDF file hosting or download delivery pipeline.
- New Turnstile actions beyond `contact` / `briefing`.
- LLM Ask LightSpeed v2.
- Full editorial content authoring for every thin section.

## Constraints

- Brand tokens only (navy/red/cyan, Arial, 4px grid).
- Reuse existing enquiry Turnstile + honeypot pattern.
- Honesty badges / claims index unchanged unless a numeric claim is introduced (none planned).

## Assumptions

- Executive Briefing modal is the single lead-capture entry for gated downloads and speaker inquiries until dedicated forms ship.

## Open Questions

- None blocking.

## Resolved Clarifications

- Newsletter uses existing enquiry API with `form: contact` and `enquiryType: Newsletter subscription` (no edge `EXPECTED_ACTIONS` change).
- Resource gate = briefing modal prefill, not a new download API.
