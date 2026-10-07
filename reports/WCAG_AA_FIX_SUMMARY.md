# WCAG AA Contrast Fix Summary - Issue #376

## Problem
- Brand red `#E63946` with white text (`#FFFFFF`) yielded **4.17:1** contrast ratio
- Failed WCAG AA requirement of **4.5:1** for normal text
- Affected all CTA buttons and interactive elements using `bg-ls-red text-ls-white`

## Solution (Option b: Darken brand red)
- Changed brand red from `#E63946` to `#DC3641` (rgb 220, 54, 65)
- Minimal darkening: R -10, G -3, B -5 (barely perceptible)
- New contrast: **4.52:1** ✓ PASSES WCAG AA
- Maintains brand guideline rule: "on red surfaces, text is white"

## Files Updated (Canonical Sources)
1. `brand/tokens/brand-tokens.json` - Red value + usage
2. `brand/tokens/brand-tokens.css` - `--ls-red` CSS variable
3. `brand/guidelines/brand-guidelines.md` - Color table
4. `brand/tokens.md` - Human-readable token docs (hex + RGB)
5. `src/brand/brand-tokens.css` - Tailwind v4 theme (`--color-ls-red`), `:root` variables, RGB channels, shadow variables

## Mirrors Updated (via `sync-brand.ps1`)
- `static/brand/tokens/` - Static site mirror
- `public/brand/tokens/` - Public assets mirror

## Verification
- Mathematical contrast calculation: 4.52:1 (PASS)
- Dev server serves updated tokens confirmed via HTTP fetch
- All CTA buttons using `bg-ls-red text-ls-white` now comply with WCAG AA

## Notes
- Brand identity preserved: color change is minimal and within brand tolerance
- No component code changes needed - tokens propagate automatically via Tailwind v4
- Shadow variables (`--ls-shadow-red`) updated for consistency
- CEO Dashboard (J.A.R.V.I.S. theme) unaffected per brand exception