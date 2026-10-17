# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: requirement-first
- Parent issue: #105
- Blocked by: #101 (visual-language decision, CLOSED), #104 (shell prototype, CLOSED)

## Goal And Evidence

- Real problem or user request: Ship the J.A.R.V.I.S. theme as a real, tested change to the existing dashboard (#105).
- Current behavior: Dashboard uses generic slate/sky color palette (`surface-*`/`brand-*` Tailwind classes) with no design token system, no self-hosted fonts, and no glass-panel treatment.
- Source of evidence: #101 resolution (design-token spec), #104 resolution (shell prototype with approved surfaces).

## User Scenarios And Success

- Primary user/system scenario: CEO views the dashboard and sees a cohesive, futuristic J.A.R.V.I.S.-inspired interface with glass panels, cyan accents, self-hosted typography, and state-communicating animations.
- Success criteria: All 7 templates + command-center render with J.A.R.V.I.S. tokens; CSP unchanged; `prefers-reduced-motion` respected; all tests pass.
- Acceptance criteria:
  1. `control-plane-theme.css` defines all CSS custom properties from #101 spec.
  2. Self-hosted fonts (Rajdhani, JetBrains Mono) load without CDN.
  3. Header/nav use jarvis tokens with scan-line texture.
  4. All panels use `.jarvis-glass` treatment.
  5. Charts use token-derived palette.
  6. `ruff check src/` passes.
  7. `mypy src/` passes.
  8. Dashboard tests pass.

## Non-Goals

- Agent-flow particles, event pulse, full particle layer (#108).
- Command bar vocabulary / execution (map #33 ticket #50).
- Light-mode support (dark-only per #101).

## Constraints

- CSP unchanged: `font-src 'self' data:`, `style-src 'self' 'unsafe-inline'`, no new CDN deps.
- No new frontend framework: extends existing FastAPI + Alpine.js + Tailwind stack.
- Dark-mode only: `<html class=dark>` hardcoded.
- `prefers-reduced-motion` must disable all animations.

## Assumptions

- Both prerequisites (#101, #104) are closed with approved resolutions.
- Self-hosted font file sizes (~50KB total) are acceptable.
- Template migration is mechanical (class replacement) with no logic changes.

## Open Questions

- None. All questions resolved via #101 and #104.

## Resolved Clarifications

- Palette locked in #101 resolution.
- Typography locked in #101 resolution (Rajdhani + JetBrains Mono, self-hosted).
- Glass treatment locked in #101 resolution (rgba 0.72 + 12px blur).
- Animation scope locked in #101 resolution (pulse only; particles deferred).
