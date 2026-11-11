# Animation Audit Verdict: HomePage

**Review Skill**: `review-animations` (open-design skills)
**Standard Reference**: Emil Kowalski's craft bar / animations.dev
**Date**: 2026-11-11

## Verdict: BLOCK

### Blocking Issues (4 items — must fix before approve):

| # | Issue | Standard | File:Line | Fix |
|---|-------|----------|-----------|-----|
| 1 | `transition-all` in PathwayCard, Reveal, CtaBand | Escalation trigger #71 | `PathwayCard.tsx:35`, `Reveal.tsx:16`, `CtaBand.tsx:61` | Replace with specific `transition-transform`/`transition-opacity` properties |
| 2 | Duration exceedances (700ms Reveal, 500ms hero image) | Standard #4: UI < 300ms | `Reveal.tsx:16`, `HomePage.tsx:34` | Reduce to 300ms |
| 3 | `transition-colors` on CTA buttons (non-GPU) | Standard #7: GPU-only properties | `HomePage.tsx:60,68` | Replace with `transition-property: background-color, border-color` + keep scale transforms |
| 4 | Incorrect easing (cubic-bezier 0.25,1,0.5,1) | Standard #3: custom strong curves required | `Reveal.tsx:16` | Use `cubic-bezier(0.23, 1, 0.32, 1)` (ease-out) |

### Additional Issues (improve but not blocking):

5. **Hover motion not gated** behind `@media (hover: hover) and (pointer: fine)` — Standard #8
6. **`animate-pulse` on hero badge** — May violate Standard #2 (frequency-appropriate) if seen 100+/day
7. **Reduced motion** — Reveal component handles this correctly via `useInView` hook, but all animations should be verified with prefers-reduced-motion enabled

### Passed Items (no issues found):

- No `scale(0)` animations found — Standard #5 compliant
- CTA button scale transforms (0.97-0.98) are GPU-accelerated — Standard #7 compliant
- No popovers/tooltips with `transform-origin: center` on HomePage — Standard #5 compliant
- Asymmetric enter/exit timing — CTA active states use `active:scale-[0.98]` which is correct (press slower, release snaps)
- Cohesive motion personality — navy/red/cyan brand theme with crisp, fast motion throughout
- `prefers-reduced-motion` handled in `useInView` hook and `index.css` reduced-motion media query

### Recommended Fix Order:

1. **Critical**: Remove `transition-all`, reduce durations to 300ms, fix `transition-colors` → specific properties, correct easing curve
2. **High**: Add hover motion pointer gating, verify reduced motion behavior
3. **Medium**: Decide on `animate-pulse` — remove, reduce, or make reduced-motion aware

After fixing the 4 blocking issues, the HomePage motion quality will meet the premium craft bar standard with justified, GPU-accelerated, sub-300ms animations that respect reduced motion and pointer capabilities.

**Verdict**: **BLOCK** — pending the 4 critical animation corrections listed above.
