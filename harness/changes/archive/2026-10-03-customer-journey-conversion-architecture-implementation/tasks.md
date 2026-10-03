# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.
- Wayfinder tickets: map #368, tickets #369�#375 (Phase 6 = #374).

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation.
- [x] T002 Park prior active ECL change (LinkedIn AI-Native Series) to `harness/changes/parking/2026-09-29-linkedin-ai-native-series`.
- [x] T005 Record the 5 user clarifications in `summary.md` (insights built now; sector-registry.ts; server analytics endpoint; 5 max sessions; qa-per-phase).

## Phase 0 � Foundation (sequential)

- [x] T010 Create `src/data/sector-registry.ts` � 5 canonical slugs (financial-services, healthcare, agriculture, education, government), evidence mapped from `src/data/sectors.ts`, `relevantSolutions` back-links. Validation: `bun run lint` exit 0. (Wayfinder #375, closed)
- [x] T011 Create `api/journey-events.ts` � edge POST endpoint, event-type + journey-stage whitelists, 200 events/hour/IP rate limit, batch support. Validation: `bun run lint` exit 0.
- [x] T012 Chart Wayfinder map + child tickets (map #368; tickets #369�#375; Foundation #375 closed with resolution).
- [x] T013 Brand token audit: `src/brand/brand-tokens.css` `@theme` exposes `--color-ls-*`; core hexes match canonical (navy `#070A40`, red `#E63946`, cyan `#00BFFF`, greys `#6B7280`/`#9CA3AF`); radii 4/8/16; Arial; imported first by `src/index.css`. PASS. Note: SPA extended surface palette (mist/mineral/water) is documented site surface, and `#F7F8F9` mist differs from canonical light grey `#F2F2F2` � pre-existing, out of this change's scope.

## Phase 1 � Homepage Journey Architecture (#369)

- [x] T020 [P] Rework `src/pages/HomePage.tsx` + `src/components/home/*` into awareness?exploration beats, no dead ends. Validation: `bun run lint && bun run build`.
- [x] T021 [P] `ls-artifact-qa` gate on homepage (Visual/Brand/UX/Accessibility/Content).

## Phase 2 � Solutions + Sectors cross-linking (#370)

- [x] T030 [P] Wire `src/pages/SectorsPage.tsx` to `sector-registry.ts` (5 canonical sectors, four evidence tiers preserved). Validation: `bun run lint && bun run build`.
- [x] T031 [P] Add solution?sector links on `SolutionsPage`, `WhatWeDoPage`, detail surfaces via `getSectorsBySolution` / `getSolutionsBySector`.
- [x] T032 [P] `ls-artifact-qa` gate on /solutions + /sectors.

## Phase 3 � Proof + Insights article & route (#371)

- [x] T040 [P] Weave Proof through journey pages (case/evidence cards; numbers only from `src/data/metrics.ts`). (DONE: ProofPage rewrite, 7 anchored sections + evidence-ladder strip; siteContent renames workCaseStudies→proofCaseStudies / workPolicy→proofPolicy + outcomeCategories + trustEvidence; RelatedLinks on 5 pages)
- [x] T041 [P] Build Insights article content module + `/insights/:slug` route; link `insightTeasers` to real articles. (DONE: `src/data/insights.ts` 3 articles + helpers; `InsightArticlePage.tsx` via useParams; App.tsx route `insights/:slug` wrapped withSite; InsightsPage rewritten, PharosSection deleted; lint/build/test EXIT 0, 38/38)
- [x] T042 [P] `ls-artifact-qa` gate on /proof + /insights. (DONE: verdict APPROVE in `reviews/review.md`; probes 0 overflow / 0 missing alt / 0 empty headings; scrolled full-page shots `stillHiddenAbove40px: 0`)

## Phase 4 � Contact 5-step + newsletter + Ask boundary (#372)

- [x] T050 [P] 5-step contact flow: progress, state preservation, Turnstile, stage-labelled CTAs (uses `src/lib/enquiry.ts`). (DONE: SLA copy → "two business days"; generic "Next Step" → `Continue — {step name}` per stage; §82 capture fields already present — no new fields, decision recorded)
- [x] T051 [P] Newsletter journey: capture ? confirmation ? double-opt-in handoff (provider = HITL decision). (DONE: confirmation panel now states the double-opt-in verification step; provider automation remains HITL fog — manual fulfilment until provider chosen, flagged on #372/#368)
- [x] T052 [P] Ask LightSpeed knowledge boundary: registry-backed answers, no fabrication, escalation to contact. (DONE: out-of-scope regex → boundary step + panel with 3 exits; matchSolutions fallback to first-3 removed → honest "No published match" panel; agent-count claim gated on matched>0; honesty badges from registry `honestyStatus`; aria-live + role=log; typed input restarts discovery from results/cta/boundary — no dead ends)
- [x] T053 [P] `ls-artifact-qa` gate on /contact + Ask flow. (DONE: verdict APPROVE in `reviews/review.md`; probes 0 overflow / 0 missing alt / 0 empty headings at 1280x800 + 390x844; new `harness/qa/ask_interact.cjs` — boundary, empty match, aria-live all true desktop+mobile)

## Phase 5 � Journey instrumentation client (#373)

- [x] T060 [P] Create `src/hooks/useJourneyEvents.ts` matching `api/journey-events.ts` whitelist; sessionId; batch + `sendBeacon`; fail-silent. Validation: `bun run lint`. (DONE: hook created — mirrored 12-type/5-stage allow-lists, sessionStorage sessionId, 10-event/5s batch timer, sendBeacon on pagehide/hidden, all failures silent; lint=0)
- [x] T061 [P] Wire route-level `page_view` + CTA/solution/sector/proof/insight events across pages. (DONE: `page_view` in SiteLayout; `solution_view`/`sector_view` on hashes (Solutions/Sectors); `proof_view` (Proof); `insight_view` index+article (Insights/InsightArticle); `cta_clicked` (CtaBand both branches); plus `ask_started`/`ask_completed`, `newsletter_started`/`newsletter_completed`, `contact_started`/`contact_completed` at funnel commit points)
- [x] T062 [P] `ls-artifact-qa` gate for any visible changes. (DONE: verdict APPROVE in `reviews/review.md`; regression probes 0 overflow / 0 missing alt / 0 empty headings at 1280x800 + 390x844 on /, /contact, /ask, /insights; new `harness/qa/journey_probe.cjs` 9/9 true, 18 POSTs captured, zero page errors)

## Phase 6 � Full regression + �40 DoD (#374, blocked by all)

- [ ] T070 Walk �40 definition of done criterion by criterion; record evidence.
- [ ] T071 Full `ls-artifact-qa` on all 9 primary routes.
- [ ] T072 Regression: `bun run lint && bun run test && bun run build`; route smoke; WCAG AA + 390px spot check.
- [ ] T073 Verify journey events POST to `/api/journey-events` returns 201.
- [ ] T074 Update `summary.md` validation + close ECL change via `scripts/harness-change.ps1`.

## Deferred Tasks

- Analytics store beyond the edge buffer (provider/cost HITL decision) � fog on map #368.
- Newsletter provider selection � fog on map #368 (Phase 4).
- ~~Insights content format decision (MDX vs data module)~~ — RESOLVED 2026-09-30: data module `src/data/insights.ts` (YAGNI on MDX; no MDX pipeline exists in this Vite SPA). Record on map #368 when closing #371.
