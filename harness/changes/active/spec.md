# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: plan-first (`brand/H.A.O.M.T.G.V. CSS Blueprint.md` is the design source of truth)
- Questions asked this round: 3

## Goal And Evidence

- Real problem or user request: build the approved HAOMTGV CSS hero from the blueprint and mount it on the `/haomtgv` page, which previously had no hero of its own.
- Current behavior: `src/pages/HAOMTVGPage.tsx` rendered a generic inline `<section>` hero (title + lead + brand bar) and duplicated `id="haomtgv-title"`. The `/haomtgv` nav link in `src/components/header/Header.tsx:21` had no route in `src/App.tsx`.
- Source of evidence: `brand/H.A.O.M.T.G.V. CSS Blueprint.md`; `src/components/home/HAOMTGVSection.tsx:24` (canonical layer copy); three CEO decisions recorded under Decisions.

## User Scenarios And Success

- Primary user/system scenario: a visitor lands on `/haomtgv` and reads the seven-layer model (Human, Agents, Orchestration, Memory, Tools, Governance, Value) as one authority-embedded system rather than a linear pipeline.
- Success criteria: hero renders at full viewport height on desktop, stacks under 1024px, animates in with a reduced-motion escape hatch, and survives `tsc` + `vite build` with no new errors.
- Acceptance criteria: single `id="haomtgv-title"` owner on the page; seven layers sourced from one shared module; connectors visible only at `lg` and anchored to the slab stack; no `framer-motion` dependency added.

## Non-Goals

- Replacing or editing the legacy `haomtgv-committed.tsx` at repo root.
- Changing `src/components/home/HAOMTGVSection.tsx` (HomePage variant stays as-is).
- Rebranding `brand/tokens/brand-tokens.css` to the blueprint palette.
- Sourcing or generating the dusk-terrace hero photograph.

## Constraints

- Palette conflict: the blueprint specifies ink `#050B1A`, cyan-glow `#22D3EE`, blue-core `#2563EB`, red-gov `#FF2D55`; brand tokens define `--ls-navy #070A40`, `--ls-cyan #00BFFF`, `--ls-red #E63946`. Blueprint values are implemented verbatim as local constants.
- `framer-motion` is not installed and is not added; animation is CSS keyframes + transitions.
- No hero raster exists in the repo; the photo layer is an optional slot with a gradient fallback.
- `main` is protected: delivery is branch + PR against 6 required checks.

## Assumptions

- The blueprint's layer semantics match the copy already published in `HAOMTGVSection.tsx`; no new claims were invented.
- `prefers-reduced-motion` is the accepted accessibility escape hatch for the hero choreography.

## Open Questions

- None blocking. Roster-gate question (`job_board`) is tracked separately as Task 4 and is not a dependency of the hero.

## Resolved Clarifications

- Hero background — CEO: "Yes — CSS gradient stand-in." A night-sky gradient with a baked sunset glow is the base layer; a photograph can be dropped in later via the `backgroundImage` prop.
- Canvas strategy — CEO: "Hybrid: full-viewport, 16:9 below 1024px." Full-bleed on desktop; the slab stack collapses to a vertical stack under `lg`.
- Roster gate — CEO: "Wire the gate and resolve the baseline." Requires a follow-up decision on whether `job_board` is approved (add to baseline → 91, or remove from registry → 90).
