---
title: "Client Site Phase 3 - Trust Evidence and Related Content"
slug: "client-site-phase-3-trust-evidence-and-related-content"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "completed"
spec_review: "approved"
plan_review: "approved"
modules: ["site-frontend"]
files:
  - "src/pages/TrustPage.tsx"
  - "src/pages/FAQPage.tsx"
  - "src/pages/LeadershipPage.tsx"
  - "src/pages/NewsPage.tsx"
  - "src/pages/InsightsPage.tsx"
  - "src/pages/ResourcesPage.tsx"
  - "src/pages/EventsPage.tsx"
  - "src/components/site/RelatedLinks.tsx"
  - "src/data/siteContent.ts"
tags: ["site", "trust", "content", "phase-3"]
validation_status: "pass"
validation_results:
  - script: bun run lint
    result: "passed - tsc clean"
  - script: bun run build
    result: "passed - vite build green"
  - script: bun run test
    result: "passed - 17/17 tests"
created_at: "2026-09-23"
updated_at: "2026-09-23"
session_id: "acf21912-6a5a-4666-bceb-3f7d773aed1d"
owner_agent: "jmlus"
claimed_at: "2026-09-23"
---

# Summary

## Outcome

- Trust evidence strip on `/trust` (`trustEvidence` in siteContent, honesty badges, operational controls only).
- Honesty policy section on Trust.
- Shared `RelatedLinks` component; applied to Trust, FAQ, Leadership, News, Insights, Resources, Events.
- FAQ/Leadership CTA wired to `onRequestBriefing` (was discarded).
- Leadership advisory note clarifies role titles, not named individuals.

## Decisions

- Reuse existing proven claims only (governance gates, HITL matrix, audit trails, DPA posture) — no invented certifications or third-party seals.
- Shared `RelatedLinks` component replaces ad-hoc related strips on News/Insights and is extended to Trust, FAQ, Leadership, Resources, Events.
- Wire Trust/FAQ/Leadership `CtaBand` to `onRequestBriefing` (props already present on Trust; FAQ/Leadership currently discard the prop).

## Validation

- `bun run lint` — pass (tsc only, no errors).
- `bun run build` — pass (vite build, pre-existing chunk/CSS warnings only).
- `bun run test` — pass (17/17 tests).
- `pwsh scripts/lint-ecl.ps1` — pass.

## Next Step

- Close completed; optional harness auto-evolve remains deferred.
