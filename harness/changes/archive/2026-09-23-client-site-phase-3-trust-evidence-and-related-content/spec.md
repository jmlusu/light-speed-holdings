# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: plan-first
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: Phase 3 content population for trust and IA — Trust page lacks evidence strip and honesty policy; related-content strips are ad-hoc; Trust/FAQ/Leadership CTAs drop the briefing callback.
- Current behavior: TrustPage only renders responsibleAi + securityTopics cards; FAQ/Leadership destructure only `theme`; News/Insights have inline related Link markup.
- Source of evidence: `src/pages/TrustPage.tsx`, `src/pages/FAQPage.tsx`, `src/pages/LeadershipPage.tsx`, `src/pages/NewsPage.tsx`, `src/pages/InsightsPage.tsx`, `src/data/siteContent.ts` (`GOVERNANCE_SOLUTION`, `honestyPolicy`), ADR-020, Phase 1 close next step.

## User Scenarios And Success

- Primary user/system scenario: Institutional visitor lands on /trust, sees evidence-backed controls with honesty status, can open a briefing, and can navigate to adjacent trust/leadership/FAQ content without dead ends.
- Success criteria: Trust evidence strip renders proven claims; honesty policy present on Trust; RelatedLinks shared component used on Trust/FAQ/Leadership (+ existing related pages); FAQ/Leadership CTA opens briefing modal when context provides callback.
- Acceptance criteria: `bun run lint` and `bun run build` pass; no new numeric claims; brand tokens only.

## Non-Goals

- Third-party certification seals or audited ISO/SOC badges (do not invent).
- Real PDF hosting or dedicated speaking form (deferred from Phase 1).
- LLM Ask LightSpeed changes.
- Harness auto-evolve (pending.md tracked separately; does not block this change).

## Constraints

- Brand tokens only (navy/red/cyan, Arial, 4px grid).
- Evidence items must map to existing siteContent / GOVERNANCE_SOLUTION facts.
- Honesty badges mandatory on evidence cards.
- Reuse existing CtaBand `onRequestBriefing` API.

## Assumptions

- `withSite` already supplies `onRequestBriefing` to these pages; wiring the prop is sufficient.
- Harness evolution pending remains non-blocking per ECL §9.

## Open Questions

- None blocking.

## Resolved Clarifications

- Trust evidence = operational controls we run, not external cert logos.
- Shared RelatedLinks is the IA pattern; no per-page custom related markup after this change.
