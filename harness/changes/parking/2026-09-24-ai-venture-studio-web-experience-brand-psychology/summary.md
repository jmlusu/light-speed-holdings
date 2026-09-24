---
title: "AI Venture Studio Web Experience — Brand Psychology (Part 1)"
slug: "ai-venture-studio-web-experience-brand-psychology"
status: "parked"
location: "parking"
phase: "plan"
intake_status: "accepted"
spec_review: "pending"
plan_review: "pending"
modules: ["src/App.tsx", "src/index.css", "src/brand/brand-tokens.css", "brand/tokens"]
files:
  - "brand/ai_venture_studio_execution_plan.md"
  - "docs/adr/020-client-facing-site-guiding-principles.md"
tags: ["web", "brand", "venture-studio", "dual-mode", "parked-intake"]
validation_status: "unknown"
created_at: "2026-09-24"
updated_at: "2026-09-24"
owner_agent: "jmlus"
claimed_at: "2026-09-24"
---

# Summary

## Outcome

- Intake + discovery complete (read-only). **No code or token changes.** Parked at user request before plan approval or implementation.
- Source brief: `brand/ai_venture_studio_execution_plan.md` (Parts 1–5). Only **Part 1** is a web experience (visual identity, dual-mode psychology, micro-interactions); Parts 2–5 are strategy content that could become a page later.
- Existing site = repo-root Vite React SPA (React 18, Vite 6, Tailwind 4, `motion`, three.js `ThreeCanvas`), ~31 routes, light/dark toggle already in `src/App.tsx` + `src/index.css`.
- Skill chain when resumed: `ls-creative-director` → `ls-design-system` → `ls-frontend-design` → Playwright → `ls-artifact-qa`.

## Decisions

- Parked without creating an active ECL (active slot held by architecture v2.0 change).
- **Open (blocks implementation):**
  1. Palette — adopt Morning Mist `#F7F8F9` / Slate `#121518` (requires amending **ADR-020**, which currently voids alternate palettes) vs keep navy `#070A40` / red `#E63946` / cyan `#00BFFF` and ship Part 1 effects only.
  2. Scope — Part 1 UI only vs also a page for Parts 2–5.
  3. Surface — restyle existing home/site chrome vs new route (e.g. `/venture-studio`).
- If palette is adopted: define accent tokens (doc is thin on accents), sync `brand/tokens` + mirrors via `scripts/sync-brand.ps1`, sweep hardcoded hexes in `App.tsx` / `index.css` / components / `ThreeCanvas` fog.
- Effects separable from palette: ripple hover, ambient mist (tune existing particles), scroll easing `cubic-bezier(0.25, 1, 0.5, 1)`, reduced-motion respect.

## Validation

- Pending (no implementation).

## Next Step

- Resume: `.\scripts\harness-change.ps1 resume 2026-09-24-ai-venture-studio-web-experience-brand-psychology` (requires empty `active/`).
- Resolve the three open decisions, then approve plan and implement Part 1 (or full doc page).

## Transition Note

- User: "park this task for now." Active architecture v2.0 change left untouched; this entry records venture-studio web intake only.
