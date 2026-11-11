# HomePage Animation Review Findings

**Review Date**: 2026-11-11
**Skill Invoked**: `review-animations`
**Standards Reference**: `open-design skills review-animations` (Emil Kowalski's craft bar / animations.dev)

---

## Findings Table

| Before | After | Why | Severity |
|--------|-------|-----|----------|
| `transition-opacity duration-500 ease-out` (Hero img) | `transition-opacity 300ms ease-out` | UI animations must stay under 300ms per craft bar Standard #4; 500ms is 67% over budget | **High** |
| `transition-all hover:-translate-y-0.5` (PathwayCard) | `transition-transform 200ms ease-out` | `transition-all` is an aggressive escalation trigger (unbounded property animation); only animate changed properties; `hover:-translate-y-0.5` is fine as transform but needs specific transition | **High** |
| `transition-all` (PathwayCard link) | `transition-color 200ms ease-out, transform 150ms ease-out` | `transition-all` violates Standard #7 (GPU-only) and is an escalation trigger; replace with specific properties | **High** |
| `transition-colors` (CTA buttons) | `transition-property: background-color, border-color; transition-duration: 200ms; transition-timing-function: cubic-bezier(0.23, 1, 0.32, 1)` | `transition-colors` animates non-GPU properties (color); per Standard #7, only `transform` and `opacity` should be animated on UI elements for GPU acceleration | **High** |
| `duration-700 [transition-timing-function:cubic-bezier(0.25,1,0.5,1)]` (Reveal) | `duration-300 [transition-timing-function:cubic-bezier(0.23, 1, 0.32, 1)]` | Duration 700ms exceeds 300ms UI budget (Standard #4); easing cubic-bezier(0.25,1,0.5,1) is not the recommended `ease-out` curve (cubic-bezier(0.23, 1, 0.32, 1)) per Standard #3 | **High** |
| `cubic-bezier(0.25,1,0.5,1)` (Reveal default easing) | `cubic-bezier(0.23, 1, 0.32, 1)` | Built-in CSS easings are too weak; custom strong curves required per Standard #3; entering/exiting elements use `ease-out` | **Medium** |
| `duration-500` (Hero image transition) | `duration-300` | UI animations must stay under 300ms per Standard #4 | **Medium** |
| `transition-shadow` (Solutions grid items) | Keep as-is (specific property) | `transition-shadow` targets only `box-shadow` property; while box-shadow can trigger repaint, it's a single specific property and is acceptable when no `transition-all` is used | **Low** |
| `hover:scale-[1.02] active:scale-[0.98]` (CTA button 1) | Keep as-is (transform-only, GPU-accelerated) | Scale transforms are GPU-accelerated per Standard #7; the 0.97-0.98 scale range is within the recommended 0.95-0.98 button press feedback range | **Low** |
| `hover:scale-[1.01] active:scale-[0.99]` (CTA button 2) | Keep as-is (transform-only, GPU-accelerated) | Same as above; within acceptable range for button press feedback | **Low** |
| `animate-pulse` (HeroSection badge) | Consider removing or reducing frequency | `animate-pulse` on a frequently-seen hero badge may violate Standard #2 (frequency-appropriate); tens/day actions should have reduced/removed animation; if this is seen 100+/day, it should have no animation | **Medium** |
| No `prefers-reduced-motion` hover gating | Add `@media (hover: hover) and (pointer: fine) { ... }` gates on hover motion | Standard #8 requires hover animations be gated behind `@media (hover: hover) and (pointer: fine)` to prevent false hovers on touch devices | **Medium** |

---

## Block / Approve Verdict

**Verdict: BLOCK** — The HomePage has multiple critical animation violations that prevent approval:

### Blocking Issues (must fix before approve):

1. **`transition-all` usage** in PathwayCard and Reveal component — This is an explicit aggressive escalation trigger (Standard #71 in SKILL.md: "Flag these on sight, hard: `transition: all`"). It animates unbounded properties including layout properties, violating GPU-only property standard (#7) and creating performance risks.

2. **Duration exceedances** — Multiple animations exceed the 300ms UI budget:
   - Reveal component: 700ms (Standard #4: "UI animations stay under 300ms")
   - Hero image: 500ms (Standard #4)
   Both are feel-breaking regressions per the verdict criteria.

3. **`transition-colors` on CTA buttons** — Animates non-GPU properties (color), violating Standard #7 ("Only animate `transform` and `opacity` — they skip layout/paint and run on the GPU"). Color transitions trigger layout recalc and paint, causing performance degradation.

4. **Incorrect easing** — Reveal uses `cubic-bezier(0.25,1,0.5,1)` which is not the recommended `ease-out` curve `cubic-bezier(0.23, 1, 0.32, 1)` per Standard #3. Built-in CSS easings are too weak; custom strong curves are expected.

### Additional Issues (should fix for premium quality):

5. **`animate-pulse` on hero badge** — May violate Standard #2 (frequency-appropriate) if the hero section is seen 100+/day. Consider removing or making it respect `prefers-reduced-motion`.

6. **Hover motion not gated** — Hover animations should be behind `@media (hover: hover) and (pointer: fine)` per Standard #8 to prevent false hovers on touch devices.

### Recommendation:

**Fix the blocking issues first** (transition-all, durations, transition-colors, easing), then address the additional issues for a premium animation craft bar compliance. After fixes, the HomePage motion quality should meet the premium standard with justified, GPU-accelerated, sub-300ms animations that respect reduced motion and pointer capabilities.

**Verdict**: **BLOCK** — pending fixes for the four critical animation violations listed above.
