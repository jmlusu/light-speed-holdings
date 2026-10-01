# Review

## Intake Review

- Status: approved (2026-09-29)
- Notes: Source spec `CUSTOMER_JOURNEY_CONVERSION_ARCHITECTURE.md` present and in scope; five user clarifications recorded in `summary.md`.

## Spec Review

- Status: approved (2026-09-29)
- Open high-impact clarifications: none — the 5 decisions in `summary.md` close them.
- WHAT/HOW separation: `spec.md` states journey-stage outcomes and acceptance criteria; `plan.md` owns phase sequencing and file-level how.

## Plan Review

- Status: approved (2026-09-29)
- Spec gaps found from planning: Insights content format, newsletter provider, analytics store beyond the edge buffer — parked as fog on Wayfinder map #368, not spec gaps.

## Code Review

- Status: in review — Phase 1 (#369) submitted 2026-09-29.

## Phase Gates (ls-artifact-qa)

### Phase 1 — Homepage (#369) — 2026-09-29

- Evidence: `harness/qa/home-hero-report.json` (probe), `harness/qa/home-hero-{1280x800,390x844}.png`, `harness/qa/paths-{desktop,mobile}.png`.
- VISUAL: PASS — 0px horizontal overflow at 1280x800 and 390x844; section hierarchy reads Orientation → Three Paths → Immersive; cards balanced 3-col desktop, stacked mobile; 4px-grid spacing.
- BRAND: PASS — tokens only (`ls-navy`/`ls-red`/`ls-cyan` on navy base), Arial scale, red/cyan/navy stage chips, no invented colors.
- UX: PASS — one primary CTA per card (Solutions / AI Company Builder / Contact), stage badges EXPLORATION/AWARENESS/INTENT; all links resolve (`/solutions`, `/what-we-do`, `/sectors`, `/ai-company-builder`, `#operating-model`, `#workforce`, `/proof`, `/contact`, `/ask`); fixed-nav element-shot overlap on mobile is the app-wide floating-nav pattern, not a section defect; hero `#thesis` dead anchor replaced with `#operating-model`.
- ACCESSIBILITY: PASS with one parked finding — 0 missing alt, 0 empty headings (42 headings), semantic h2→h3, ≥44px tap targets. Parked: white-on-`#E63946` CTA micro-text (12px bold) measures ≈4.19:1, under AA 4.5:1 for normal text. This is the brand-sanctioned pairing (`brand-tokens.json` `onRed: #FFFFFF`) used by the existing hero CTA — the new cards inherit it, not introduce it. Changing it would invent an off-spec on-accent color. Raised as a brand/WCAG reconciliation follow-up, not a Phase 1 blocker.
- CONTENT: PASS — no invented metrics (90 agents, 17 tests from `metrics.ts`), honesty badges intact, knowledge-boundary note on Ask row, no dead-end pages.
- VERDICT: **APPROVE** (Phase 1 gate met; contrast finding parked as cross-cutting follow-up owned by Phase 6/§40 a11y pass).

### Phase 2 — Solutions + Sectors cross-linking (#370) — 2026-09-30

- Evidence: `harness/qa/solutions-report.json`, `harness/qa/sectors-report.json` (probes), `harness/qa/solutions-probe-{1280x800,390x844}.png`, `harness/qa/sectors-probe-{1280x800,390x844}.png`, `harness/qa/solutions-full.png`, `harness/qa/sectors-full.png` (scrolled full-page), element shots `sol-card-desktop.png`, `sector-card-desktop.png`, `sector-gov-desktop.png`, `sector-card-mobile.png`.
- VISUAL: PASS — 0px horizontal overflow at 1280x800 and 390x844 on both routes (scrollWidth == viewport); all 6 solution cards and all 5 sector cards render after scroll (blank regions in unscrolled full-page shots are the `Reveal` opacity-0 screenshot artifact, verified by `stillHiddenAbove40px: 0` in scrolled shots); WORKS IN / SOLUTIONS FOR THIS SECTOR chips wrap cleanly on 390px.
- BRAND: PASS — navy base, red eyebrows (`WHAT WE DO`, `SECTORS`, `THE NEXT STEP`), cyan tier badges, Arial scale, existing pill-chip styles for sector/solution chips; no invented colors or fonts.
- UX: PASS — bidirectional cross-links work both directions: solution card → `/sectors#<sector-id>` (verified chips under `#ai-company-builder`, `#business-automation`), sector card → `/solutions#<solution-slug>` (verified on `#financial-services`, `#healthcare`, `#government`); anchors carry `scroll-mt-28` for the fixed nav; Governance Solution correctly shows no WORKS IN strip (horizontal solution, no slug); no dead ends — every chip lands on a section that exists.
- ACCESSIBILITY: PASS — 0 missing alt, 0 empty headings (13 headings on /solutions, 12 on /sectors), heading hierarchy intact; white-on-red contrast remains covered by parked issue #376 (cross-cutting, not introduced here).
- CONTENT: PASS — SectorsPage now renders the 5 canonical sectors from `sector-registry.ts` with §11 four-tier legend intact; duplicate evidence resolved (education keeps UNIMA student-management claim; government carries only the advisory National AI Strategy line with explicit "no ministerial production deployment claimed"); homepage SectorsSection switched to canonical 5 (legacy 9-sector `sectors.ts` still used only by `governance.test.ts`); no invented metrics or proof.
- VERDICT: **APPROVE** (Phase 2 gate met; T030–T032 complete).

### Phase 3 — Proof + Insights article & route (#371) — 2026-09-30

- Evidence: `harness/qa/{proof,insights,article}-report.json` (probes), `harness/qa/{proof,insights,article}-probe-{1280x800,390x844}.png`, `harness/qa/proof-full.png`, `harness/qa/insights-full{,-mobile}.png`, `harness/qa/article-full{,-mobile}.png` (scrolled full-page, `stillHiddenAbove40px: 0` on all).
- VISUAL: PASS — 0px horizontal overflow at 1280x800 and 390x844 on /proof (17 headings, heights 1280x/390x captured), /insights (12 headings), and /insights/sadc-ai-opportunity (16 headings); 7 anchored Proof sections + evidence-ladder strip read in order; Featured Insight cards stack cleanly on mobile; 12 category chips wrap on 390px; article typography (meta line, SOURCES box, block renderer) holds the 4px grid.
- BRAND: PASS — navy base, red eyebrows, cyan tier/evidence badges, Arial scale; honesty badges use `HonestyTone` styles only; no invented colors or fonts; prose tone matches site voice (no AI-slop patterns).
- UX: PASS — `insightTeasers` link to real `/insights/<slug>` routes (3 articles live); article journey CTAs ordered Primary "Explore Related Thinking" → 4 secondaries (Ask LightSpeed / Explore Solutions / Explore Sectors / Contact); related solution/sector links land on existing anchors `/solutions#<slug>` + `/sectors#<id>` with `scroll-mt-28`; miss-slug falls back via Navigate (no dead end); NewsletterSignup → CtaBand closes the page per idiom; RelatedLinks on 5 pages verified in Phase 2/3 lint run.
- ACCESSIBILITY: PASS — 0 missing alt, 0 empty headings across all three routes (17/12/16 headings); semantic heading hierarchy h1→h2→h3; `useParams` route inside RouterProvider renders correctly (first precedent); white-on-red contrast remains covered by parked issue #376 (cross-cutting).
- CONTENT: PASS — metrics only from `metrics.ts`; claims hedged per `research/site-claims-ledger.md` (no "world's smallest", "submitted to ministers"→"policy proposal", decision logs "auditable on request"); sector badges (PROVEN EXPERIENCE / CURRENT CAPACITY) are canonical `sector-registry.ts` values, not invented; 3 articles carry explicit source lines (SADC framework, pillars 01/03, post-01 feed); insights delivered as data module (`src/data/insights.ts`, not MDX) — decision to record on map #368.
- Tooling note: `harness/qa/{visual_check.cjs,shot_full.cjs}` patched this phase (`waitUntil: "load"` + 1500ms settle) — Cloudflare Turnstile retries DNS-failing `brunhild.challenges.cloudflare.com` so `networkidle` never settles; app itself loads fine (QA-tooling issue, not an app bug).
- VERDICT: **APPROVE** (Phase 3 gate met; T040–T042 complete).

### Phase 4 — Contact + Newsletter + Ask boundary (#372) — 2026-09-30

- Evidence: `harness/qa/artifacts/{contact,insights,ask}-{1280x800,390x844}` reports + screenshots (via patched `visual_check.cjs`), `harness/qa/artifacts/ask-boundary-1280.png`, `ask-empty-1280.png`, `ask-boundary-390.png`; interactive probe `harness/qa/ask_interact.cjs` (new) → `{boundaryPanel, boundaryReply, restartedToSector, emptyMatchPanel, emptyMatchCta, ariaLive, mobileBoundary}` all true.
- VISUAL: PASS — 0px horizontal overflow on /contact (6 headings), /insights (12), /ask (7) at 1280x800 and 390x844; boundary and empty-match panels render centered inside the chat card on the 4px grid; three-button exit rows wrap cleanly.
- BRAND: PASS — navy base, red primary CTA (`CTAS.primary`), cyan boundary/empty-state accents (`ls-cyan/5` panel, ShieldCheck), Arial scale; no invented colors or fonts.
- UX: PASS — no dead ends anywhere in the Ask flow: out-of-scope ask → boundary panel with 3 exits (Start a Conversation / Explore Solutions / Verify Our Proof); no-match discovery → honest "No published match" panel with the same exits; typed input from results/cta/boundary restarts discovery instead of silently dropping; input placeholder adapts ("Or type to ask something else..."); ContactSection CTAs stage-labelled (`Continue — Diagnosis` etc.), SLA copy now "two business days" everywhere (one place, no strays).
- ACCESSIBILITY: PASS — 0 missing alt, 0 empty headings on all three routes; `aria-live="polite"` + `role="log"` + `aria-label` on the assistant messages container (§79); white-on-red contrast remains covered by parked #376 (cross-cutting).
- CONTENT: PASS — fabrication paths closed: `matchSolutions` no longer falls back to `solutions.slice(0, 3)`; "90-agent workforce" line appended only when agents actually matched; agent honesty badge derives from registry `honestyStatus` (hardcoded "Proven" removed); boundary refusal names exactly what stays out (secrets, credentials, prompts, internal info) per §15; empty match states the gap honestly per §78; newsletter confirmation promises double opt-in before first issue — fulfilment is manual until the provider is chosen (HITL fog on #368).
- VERDICT: **APPROVE** (Phase 4 gate met; T050–T053 complete).

### Phase 5 — Journey instrumentation client (#373) — 2026-09-30

- Evidence: `harness/qa/artifacts/p5-{home,contact,ask,insights}-{1280x800,390x844}.png` reports; new functional probe `harness/qa/journey_probe.cjs` → 9/9 checks true (`capturedPosts: 18`, page/solution/sector/proof/insight events present with correct slugs, `envelopeValid`, `stableSession`, `noPageErrors`); `bun run lint` = 0, `bun run build` = 0, `bun run test` = 38/38.
- VISUAL: PASS — instrumentation is invisible by design; regression probes on /, /contact, /ask, /insights all `horizontalOverflowPx: 0` at 1280x800 and 390x844.
- BRAND: PASS — no visual changes; hook is logic-only.
- UX: PASS — events fire unobtrusively: route-level `page_view` in SiteLayout, `solution_view`/`sector_view` on deep-link hashes, `proof_view`/`insight_view` on mount, `cta_clicked` on every CtaBand action, `ask_started`/`ask_completed` on discovery, `newsletter_*`/`contact_*` on funnel commit/success; nothing blocks or alters the journey on failure (fetch/beacon failures and invalid types are dropped silently; dev 404 from missing `/api` never surfaces).
- ACCESSIBILITY: PASS — 0 missing alt, 0 empty headings on all four routes; no DOM/ARIA changes.
- CONTENT: PASS — client whitelist mirrors `api/journey-events.ts` exactly (12 event types, 5 stages); only whitelisted fields sent (eventType, route, contentType, solution, sector, cta, journeyStage, timestamp, sessionId, metadata); sessionId is per-tab sessionStorage (no cross-session identity); no PII captured.
- VERDICT: **APPROVE** (Phase 5 gate met; T060–T062 complete; live 201 from deployed endpoint deferred to Phase 6 T073).

## Validation Review

- Status: pending — Phase 6 (#374) owns the §40 walk-through.
