# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: mixed (strategy doc + exploratory Q&A)
- Questions asked this round: 3 (all resolved 2026-09-24)

## Goal And Evidence

- Real problem or user request: Implement a web experience for `brand/ai_venture_studio_execution_plan.md` — primarily Part 1 (Visual Identity & Brand Psychology for Lightspeed Holdings website): dual-mode themes, lower cognitive load, ripple navigation, ambient mist, cascading smooth scroll.
- Current behavior: SPA already has dual light/dark (navy/grey-light), three.js particles, basic reveals; no ripple, no custom scroll easing, no CSS reduced-motion guard.
- Source of evidence: `brand/ai_venture_studio_execution_plan.md`; ADR-020; explore of `src/`, `brand/`.

## User Scenarios And Success

- Primary scenario: Visitor lands on Lightspeed site and experiences calm, trustworthy dual-mode UI with soft interaction feedback per Part 1.
- Success: Part 1 effects implemented on **current** palette; `bun run lint` + `test` + `build` green; reduced-motion respected; contrast ≥4.5:1.
- Acceptance: No hex/token changes; ripple/mist/scroll/reduced-motion present; home surface updated.

## Non-Goals

- Parts 2–5 as content page (deferred).
- New palette / ADR-020 amendment / token sync.
- Dashboard J.A.R.V.I.S. theme.
- Full site rewrite or framework change.
- Changes to `ThreeCanvas` fog/particles.

## Constraints

- ADR-020: navy/red/cyan remain design authority — **no palette swap**.
- One active ECL at a time (architecture v2.0 parked awaiting human plan_review).
- Hero mist = CSS gradients only (decision A).

## Assumptions

- Implementation stays in repo-root Vite SPA.
- Dual-mode naming optional; hexes unchanged.

## Open Questions

- All three resolved 2026-09-24: palette keep navy/red/cyan; scope Part 1 only; surface restyle home; mist CSS option A.

## Spec Gaps Found From Planning

- Morning Mist/Slate accent tokens undefined — **moot** (palette not adopted).

## Risks And Mitigations

- Global `*` transition fights ripple → animate transform/opacity only.
- CtaBand scale + ripple compound → ripple on `::after`/inner.
- Home is conversion surface → additive effects only; easy revert.

## Verification Plan

- `bun run lint` && `bun run test` && `bun run build`
- Playwright visual_check → `ls-artifact-qa`
- Contrast/overflow/alt + reduced-motion checks
