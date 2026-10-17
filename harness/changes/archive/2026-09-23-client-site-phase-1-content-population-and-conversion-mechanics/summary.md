---
title: "Client Site Phase 1 - Content Population and Conversion Mechanics"
slug: "client-site-phase-1-content-population-and-conversion-mechanics"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "completed"
spec_review: "approved"
plan_review: "approved"
modules: ["site-frontend", "enquiry-api"]
files:
  - "src/pages/ResourcesPage.tsx"
  - "src/pages/EventsPage.tsx"
  - "src/pages/NewsPage.tsx"
  - "src/pages/InsightsPage.tsx"
  - "src/components/site/CtaBand.tsx"
  - "src/components/NewsletterSignup.tsx"
  - "src/lib/enquiry.ts"
tags: ["site", "conversion", "content", "phase-1"]
validation_status: "pass"
validation_results:
  - script: bun run lint
    result: "passed - tsc clean"
  - script: bun run build
    result: "passed - vite build green"
  - script: pwsh scripts/lint-ecl.ps1
    result: "passed - ECL lint passed"
created_at: "2026-09-23"
updated_at: "2026-09-23"
session_id: "acf21912-6a5a-4666-bceb-3f7d773aed1d"
owner_agent: "jmlus"
claimed_at: "2026-09-23"
---

# Summary

## Outcome

- Wired resource and event cards to the Executive Briefing modal (download gate / speaking inquiry prefill).
- Extended `CtaBand` with optional `onRequestBriefing` so CTAs open the modal with context.
- Added `NewsletterSignup` (Turnstile action `contact`, enquiryType `Newsletter subscription`) on News and Insights.
- Added News ↔ Insights ↔ Resources ↔ Events related links.

## Decisions

- Reuse `/api/enquiry` + Turnstile (`form: contact|briefing`) for newsletter and speaking inquiry — no new edge action required in this change.
- Resource cards open the existing Executive Briefing modal prefilled with the resource title (honest gate until real PDFs exist).
- No LLM; no new backend email provider; brand tokens unchanged.

## Validation

- `bun run lint` — passed (tsc clean).
- `bun run build` — passed (vite build green).
- `pwsh scripts/lint-ecl.ps1` — passed at close.

## Next Step

- Close via harness if no further gaps; then Phase 3 content population / Phase 6 dynamic IA.
