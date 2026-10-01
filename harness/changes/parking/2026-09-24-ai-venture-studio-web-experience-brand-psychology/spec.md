# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: mixed (strategy doc + exploratory Q&A)
- Questions asked this round: 3 (all open — see Open Questions)

## Goal And Evidence

- Real problem or user request: Implement a web experience for `brand/ai_venture_studio_execution_plan.md` — primarily Part 1 (Visual Identity & Brand Psychology for Lightspeed Holdings website): dual-mode themes, lower cognitive load, ripple navigation, ambient mist particles, cascading smooth scroll.
- Current behavior: SPA already has dual light/dark (navy/grey-light), three.js particles, basic reveals; no ripple, no named Morning Mist/Slate themes, no custom scroll easing library.
- Source of evidence: `brand/ai_venture_studio_execution_plan.md`; ADR-020; explore of `src/`, `brand/`.

## User Scenarios And Success

- Primary scenario: Visitor lands on Lightspeed site and experiences calm, trustworthy dual-mode UI with soft interaction feedback per Part 1.
- Success: Part 1 effects implemented on chosen palette; `ls-artifact-qa` APPROVE; `bun run lint` + `bun run build` green.
- Acceptance: Tokens/themes match decision; reduced-motion respected; contrast ≥4.5:1.

## Non-Goals

- Parts 2–5 as engineering architecture (unless scoped as content page later).
- Dashboard J.A.R.V.I.S. theme (sanctioned exception).
- Full site rewrite or framework change.

## Constraints

- ADR-020: navy/red/cyan are design authority for lightspeedholdings.com unless a new ADR amends them.
- `brand/**` is canonical; mirrors via `scripts/sync-brand.ps1` only.
- One active ECL at a time; this change is parked.

## Assumptions

- Implementation stays in repo-root Vite SPA.
- User will decide palette before any token edits.

## Open Questions

- [NEEDS CLARIFICATION: palette — Morning Mist/Slate vs keep navy/red/cyan + effects only?]
- [NEEDS CLARIFICATION: scope — Part 1 only vs full doc as a page?]
- [NEEDS CLARIFICATION: surface — restyle existing home vs new route?]

## Spec Gaps Found From Planning

- Doc does not fully specify accent/CTA tokens for Morning Mist/Slate.
- Accent strategy if neutrals change but red/cy an CTAs remain.

## Risks And Mitigations

- Half-migrated palette → complete token sync + site-wide sweep + QA.
- Conflicting with active architecture ECL → do not resume until active is closed/parked.

## Verification Plan

- `bun run lint` && `bun run build`
- Playwright visual_check → `ls-artifact-qa`
- Contrast/overflow/alt checks per artifact QA
