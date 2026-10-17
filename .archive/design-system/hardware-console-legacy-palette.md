# Design System Decisions — LightSpeed Holdings Website

**Author:** Product Designer
**Date:** 2026-09-10
**Scope:** `src/brand/brand-tokens.css` and `src/index.css`
**Platform:** React + Tailwind CSS v4 (Vite)

---

## Executive Summary

The site's visual identity is a **dark hardware-console aesthetic** (Dieter Rams / Teenage Engineering). The current brand tokens (navy/red/cyan) are inherited from the corporate print brand and are decorative-only on the web. The actual site runs on slate/zinc grays + orange (`#F97316`). This document establishes a token system that matches the site's real identity, eliminates hardcoded values, and creates a consistent foundation.

---

## 1. Color Palette

### Decision: Zinc-based neutrals + orange accent

The hardware-console identity demands cool, metallic neutrals — not warm grays. Zinc (`zinc-950` through `zinc-100`) provides the right blue-gray tone for bead-blasted metal surfaces. Orange (`#F97316`) stays as the sole working accent. Navy (`#070A40`) is retained for logo/brand moments only.

### CSS Custom Properties (add to `brand-tokens.css`)

```css
:root {
  /* ── Ink Ramp (3 levels) ─────────────────────────────────── */
  --ink-primary:    #18181B;   /* zinc-900  — primary text on light */
  --ink-secondary:  #71717A;   /* zinc-500  — secondary/muted text */
  --ink-tertiary:   #A1A1AA;   /* zinc-400  — placeholder, hint text */

  /* ── Surface Ramp (dark theme) ───────────────────────────── */
  --surface-base:   #09090B;   /* zinc-950  — page background */
  --surface-raised: #18181B;   /* zinc-900  — cards, panels */
  --surface-well:   #27272A;   /* zinc-800  — inset wells, inputs */
  --surface-border: #3F3F46;   /* zinc-700  — borders, dividers */
  --surface-border-subtle: #27272A; /* zinc-800 — subtle dividers */

  /* ── Surface Ramp (light theme) ──────────────────────────── */
  --surface-light-base:    #FAFAFA; /* zinc-50  — page background */
  --surface-light-raised:  #FFFFFF; /* white    — cards, panels */
  --surface-light-well:    #F4F4F5; /* zinc-100 — inset wells */
  --surface-light-border:  #E4E4E7; /* zinc-200 — borders */
  --surface-light-border-subtle: #F4F4F5; /* zinc-100 — subtle dividers */

  /* ── Text on dark surfaces ───────────────────────────────── */
  --on-surface:      #FAFAFA;  /* zinc-50  — primary text on dark */
  --on-surface-dim:  #A1A1AA;  /* zinc-400 — secondary text on dark */
  --on-surface-faint:#52525B;  /* zinc-600 — disabled on dark */

  /* ── Text on light surfaces ──────────────────────────────── */
  --on-surface-light:     #18181B; /* zinc-900 — primary text on light */
  --on-surface-light-dim: #71717A; /* zinc-500 — secondary on light */

  /* ── Accent: Orange ──────────────────────────────────────── */
  --accent:        #F97316;    /* orange-500 — primary accent */
  --accent-hover:  #EA580C;    /* orange-600 — hover state */
  --accent-dim:    rgba(249, 115, 22, 0.15); /* tinted background */
  --accent-glow:   rgba(249, 115, 22, 0.4);  /* glow/shadow */
  --on-accent:     #FFFFFF;    /* white — text on orange */

  /* ── Success ─────────────────────────────────────────────── */
  --success:       #10B981;    /* emerald-500 */
  --success-dim:   rgba(16, 185, 129, 0.15);

  /* ── Warning ─────────────────────────────────────────────── */
  --warning:       #F59E0B;    /* amber-500 */
  --warning-dim:   rgba(245, 158, 11, 0.15);

  /* ── Error / Danger ──────────────────────────────────────── */
  --error:         #EF4444;    /* red-500 */
  --error-dim:     rgba(239, 68, 68, 0.15);

  /* ── Brand (print/logo use only — not for UI chrome) ────── */
  --brand-navy:    #070A40;
  --brand-red:     #E63946;
  --brand-cyan:    #00BFFF;
}
```

### Why these values

| Token | Value | Rationale |
|-------|-------|-----------|
| `--ink-primary` | `#18181B` | Zinc-900. Cooler than gray-800; reads as machined metal on light. |
| `--ink-secondary` | `#71717A` | Zinc-500. Neutral mid-tone for secondary labels. |
| `--ink-tertiary` | `#A1A1AA` | Zinc-400. For placeholders, hints, disabled text. |
| `--surface-base` (dark) | `#09090B` | Zinc-950. Near-black with blue undertone — not pure black. |
| `--surface-raised` (dark) | `#18181B` | Zinc-900. Cards on dark background. |
| `--surface-well` (dark) | `#27272A` | Zinc-800. Inset wells, input backgrounds. |
| `--surface-border` (dark) | `#3F3F46` | Zinc-700. Visible but not harsh borders on dark. |
| `--accent` | `#F97316` | Orange-500. The site's working accent — hardware LED glow. |

### Mapping: Old hardcoded → New token

| Old Value | Occurrences | New Token | Notes |
|-----------|-------------|-----------|-------|
| `#2D3748` (text on light) | ~30 | `var(--ink-primary)` | Used as text color in light theme |
| `#2D3748` (placeholder text) | ~10 | `var(--ink-tertiary)` | Placeholder text in inputs (both themes) |
| `#0b102f` (card bg) | ~20 | `var(--surface-raised)` | Dark card background |
| `#1b2554` (card border) | ~20 | `var(--surface-border)` | Dark card border |
| `#0e163b` (well bg) | ~15 | `var(--surface-well)` | Dark inset well background |
| `#1e2a58` (well border) | ~15 | `var(--surface-border-subtle)` | Dark well border |
| `#CBD5E1` → `var(--on-surface)` (hardware contexts) | many | Keep as-is in hardware component classes | These are skeuomorphic effect colors, not semantic |

---

## 2. Typography

### Decision: Space Grotesk (display) + Inter (body) + JetBrains Mono (code/labels)

**Space Grotesk** is a proportional sans-serif derived from Space Mono. It has the geometric precision and technical feel of hardware engravings without being a monospace (which would hurt readability at body sizes). It pairs naturally with Inter for body text.

**JetBrains Mono** is already used in the dashboard (`--jarvis-font-mono`). Using it for labels/badges/mono contexts across the site creates consistency between dashboard and marketing surfaces.

### Google Fonts Import

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
```

### CSS Custom Properties (add to `brand-tokens.css`)

```css
  /* ── Typography ──────────────────────────────────────────── */
  --font-display: 'Space Grotesk', system-ui, sans-serif;
  --font-body:    'Inter', system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;

  /* ── Font Weights ────────────────────────────────────────── */
  --weight-regular:  400;
  --weight-medium:   500;
  --weight-semibold: 600;
  --weight-bold:     700;

  /* ── Type Scale (rem — base 16px) ────────────────────────── */
  --text-xs:    0.75rem;   /* 12px — captions, labels */
  --text-sm:    0.875rem;  /* 14px — body small */
  --text-base:  1rem;      /* 16px — body */
  --text-lg:    1.125rem;  /* 18px — body large */
  --text-xl:    1.25rem;   /* 20px — subtitle */
  --text-2xl:   1.5rem;    /* 24px — heading sm */
  --text-3xl:   1.875rem;  /* 30px — heading md */
  --text-4xl:   2.25rem;   /* 36px — heading lg */
  --text-5xl:   3rem;      /* 48px — display */
  --text-6xl:   3.75rem;   /* 60px — display xl */
```

### Usage Rules

| Context | Font | Weight | Tailwind Class |
|---------|------|--------|----------------|
| Page titles, hero text | Space Grotesk | 700 | `font-[family-name:var(--font-display)] font-bold` |
| Section headings (h2-h3) | Space Grotesk | 600 | `font-[family-name:var(--font-display)] font-semibold` |
| Body paragraphs | Inter | 400 | `font-[family-name:var(--font-body)]` |
| UI labels, nav items | Inter | 500 | `font-[family-name:var(--font-body)] font-medium` |
| Code, terminal output, badges | JetBrains Mono | 400-600 | `font-mono` |
| Hardware debossed labels | JetBrains Mono | 500 | Existing `.hardware-debossed-*` classes |

---

## 3. Spacing Scale

### Decision: 4px base, 8 steps, linear progression with one jump

The site uses many values between 4px and 96px. A clean 8-step scale covers all needs.

### CSS Custom Properties (add to `brand-tokens.css`)

```css
  /* ── Spacing Scale (4px base) ────────────────────────────── */
  --space-1:  0.25rem;   /*  4px — tight gap, icon padding */
  --space-2:  0.5rem;    /*  8px — inline gap, small padding */
  --space-3:  0.75rem;   /* 12px — compact section gap */
  --space-4:  1rem;      /* 16px — standard padding */
  --space-5:  1.5rem;    /* 24px — card padding, section gap */
  --space-6:  2rem;      /* 32px — large section gap */
  --space-7:  3rem;      /* 48px — major section break */
  --space-8:  4rem;      /* 64px — hero spacing, page margins */
```

### Why this progression

Steps 1-4 are linear (4px increments) for the small, high-frequency values. Step 5 jumps to 24px (the most common "medium" spacing in the codebase). Steps 6-8 follow a 16px progression for layout-level spacing.

### Mapping: Current Tailwind usage → Token

| Tailwind Usage | Pixel Value | Token | Tailwind Equivalent |
|---------------|-------------|-------|---------------------|
| `p-1`, `gap-1` | 4px | `--space-1` | `p-1` / `gap-1` |
| `p-2`, `gap-2` | 8px | `--space-2` | `p-2` / `gap-2` |
| `p-3`, `gap-3` | 12px | `--space-3` | `p-3` / `gap-3` |
| `p-4`, `gap-4` | 16px | `--space-4` | `p-4` / `gap-4` |
| `p-5`, `gap-5`, `gap-6` | 20-24px | `--space-5` | `p-6` (24px) |
| `p-6`, `gap-8` | 24-32px | `--space-5` / `--space-6` | `p-6` / `p-8` |
| `p-8`, `gap-12` | 32-48px | `--space-6` / `--space-7` | `p-8` / `p-12` |
| `py-24`, `py-28` | 96-112px | `--space-8` × 1.5-2 | `py-24` / `py-28` |

**Note:** In practice, most components should use Tailwind's built-in spacing utilities (`p-4`, `gap-6`, etc.) which align to the same 4px grid. The CSS variables are for component-level styles, gradients, and non-Tailwind contexts.

---

## 4. Border Radius

### Decision: 2 values — `1rem` (panels) and `0.375rem` (controls)

The hardware-console aesthetic favors **subtle rounding** — panels get slightly rounded corners like machined edges, controls get minimal rounding like buttons on real hardware. The current 7 different values collapse to 2.

### CSS Custom Properties (add to `brand-tokens.css`)

```css
  /* ── Border Radius (2 values) ────────────────────────────── */
  --radius-panel:   1rem;       /* 16px — cards, modals, panels */
  --radius-control: 0.375rem;   /*  6px — buttons, badges, inputs, tags */
```

### Mapping: Current → New

| Old Value | Tailwind | Pixel | New Token | Use For |
|-----------|----------|-------|-----------|---------|
| `rounded-full` | — | 9999px | **Keep as `rounded-full`** | Avatars, dots, pills (circles only) |
| `rounded-3xl` | 1.5rem | 24px | `--radius-panel` | Modals, large cards → reduce to 16px |
| `rounded-2xl` | 1rem | 16px | `--radius-panel` | Cards, panels → keep |
| `rounded-xl` | 0.75rem | 12px | `--radius-control` | Buttons, badges → reduce to 6px |
| `rounded-lg` | 0.5rem | 8px | `--radius-control` | Inputs, small cards → reduce to 6px |
| `rounded-md` | 0.375rem | 6px | `--radius-control` | Tabs, nav items → keep |
| `rounded-xs` | 0.125rem | 2px | `--radius-control` | Minimal → increase to 6px |

**Exception:** `rounded-full` is retained for truly circular elements (avatar circles, status dots, progress rings). It is not a general-purpose radius.

### Tailwind Integration (Tailwind v4)

In `brand-tokens.css`, extend Tailwind's theme:

```css
@theme {
  --radius-panel: 1rem;
  --radius-control: 0.375rem;
}
```

This makes `rounded-panel` and `rounded-control` available as Tailwind utilities.

---

## 5. Fix `#2D3748`

### The Problem

`#2D3748` is Tailwind CSS v2's `gray-700`. It was removed in v3+ (replaced by `slate-700` / `zinc-700`). It appears **47 times** across 5 component files, used as:

1. **Text color on light surfaces** (primary use) — 30+ occurrences
2. **Placeholder text color in inputs** — ~10 occurrences

### The Fix

| Usage Pattern | Current | Replacement | Token |
|--------------|---------|-------------|-------|
| `text-[#2D3748]` on light bg | Hardcoded gray | `text-[var(--ink-primary)]` | `--ink-primary: #18181B` |
| `placeholder:text-[#2D3748]` | Hardcoded gray | `placeholder:text-[var(--ink-tertiary)]` | `--ink-tertiary: #A1A1AA` |

### Files to Update

| File | Occurrences | Primary Pattern |
|------|-------------|-----------------|
| `src/components/CorporateLanding.tsx` | 30 | `text-[#2D3748]` → `text-[var(--ink-primary)]` |
| `src/components/FloatingNav.tsx` | 1 | `text-[#2D3748]` → `text-[var(--ink-primary)]` |
| `src/components/InteractiveOperatingModel.tsx` | 5 | Mix of text + placeholder |
| `src/components/TemplatesArtifacts.tsx` | 3 | `text-[#2D3748]` → `text-[var(--ink-primary)]` |
| `src/components/TransformationDiagnostic.tsx` | 4 | `text-[#2D3748]` → `text-[var(--ink-primary)]` |

### Specific Replacement Rules

```bash
# For text-on-light usage (the majority):
# Replace: text-[#2D3748]
# With:    text-[var(--ink-primary)]

# For placeholder text usage:
# Replace: placeholder:text-[#2D3748]
# With:    placeholder:text-[var(--ink-tertiary)]

# Edge case — some lines use it in both light and dark branches:
#   isLight ? 'text-[#2D3748]' : 'text-[#2D3748]'
# These should become:
#   isLight ? 'text-[var(--ink-primary)]' : 'text-[var(--on-surface-dim)]'
```

---

## Implementation Instructions

### Step 1: Add Google Fonts import to `index.css`

Add at the top of `src/index.css`, **before** the Tailwind import:

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
@import "tailwindcss";
@import "./brand/brand-tokens.css";
```

### Step 2: Replace `brand-tokens.css` `:root` block

Replace the entire `:root { ... }` in `src/brand/brand-tokens.css` with the new tokens defined in sections 1-4 above. Keep the comments and structure clean.

### Step 3: Add `@theme` block for Tailwind v4 integration

After the `:root` block in `brand-tokens.css`, add:

```css
@theme {
  /* Radius utilities */
  --radius-panel: 1rem;
  --radius-control: 0.375rem;

  /* Font families */
  --font-family-display: 'Space Grotesk', system-ui, sans-serif;
  --font-family-body: 'Inter', system-ui, sans-serif;
  --font-family-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;

  /* Spacing */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-3: 0.75rem;
  --spacing-4: 1rem;
  --spacing-5: 1.5rem;
  --spacing-6: 2rem;
  --spacing-7: 3rem;
  --spacing-8: 4rem;
}
```

This makes `font-display`, `font-body`, `font-mono`, `rounded-panel`, `rounded-control`, and `p-1` through `p-8` (and their `gap-`, `m-`, etc. variants) available as native Tailwind utilities.

### Step 4: Update `src/index.css` surface variables

Replace the `@layer base` block's variable declarations. Remove the duplicate `--surface-dark-base` / `--surface-light-base` overrides and consolidate:

```css
@layer base {
  :root {
    --surface-dark-base: var(--surface-base);
    --surface-dark-card: var(--surface-raised);
    --surface-dark-well: var(--surface-well);
    --surface-light-base: var(--surface-light-base);
    --surface-light-card: var(--surface-light-raised);
    --surface-light-well: var(--surface-light-well);
    --accent-orange: var(--accent);
    --accent-orange-glow: var(--accent-glow);
    --accent-amber: var(--warning);
    --accent-green: var(--success);
  }
  /* ... rest of base layer ... */
}
```

### Step 5: Fix `#2D3748` across all component files

Global find-and-replace in these files:

- `src/components/CorporateLanding.tsx`
- `src/components/FloatingNav.tsx`
- `src/components/InteractiveOperatingModel.tsx`
- `src/components/TemplatesArtifacts.tsx`
- `src/components/TransformationDiagnostic.tsx`

**Replacement patterns:**

1. `text-[#2D3748]` → `text-[var(--ink-primary)]` (light theme text)
2. `placeholder:text-[#2D3748]` → `placeholder:text-[var(--ink-tertiary)]`
3. Conditional `isLight ? 'text-[#2D3748]' : 'text-[#2D3748]'` → `isLight ? 'text-[var(--ink-primary)]' : 'text-[var(--on-surface-dim)]'`

### Step 6: Migrate hardcoded card/well colors (optional, recommended)

These are lower priority but complete the token adoption:

- `bg-[#0b102f]` → `bg-[var(--surface-raised)]`
- `border-[#1b2554]` → `border-[var(--surface-border)]`
- `bg-[#0e163b]` → `bg-[var(--surface-well)]`
- `border-[#1e2a58]` → `border-[var(--surface-border-subtle)]`

---

## Verification Checklist

| Check | How |
|-------|-----|
| Fonts load | Open Network tab → verify Google Fonts requests for Space Grotesk, Inter, JetBrains Mono |
| Tokens apply | Inspect any card → `--surface-raised` should resolve to `#18181B` in dark mode |
| `#2D3748` eliminated | `grep -r "#2D3748" src/` should return 0 results |
| Radius consistency | No `rounded-3xl`, `rounded-2xl`, `rounded-lg` in new code — only `rounded-panel`, `rounded-control`, `rounded-full` |
| Build passes | `npm run build` succeeds with no CSS errors |
| Visual regression | Screenshot key pages before/after — dark theme should look nearly identical (zinc tones are close to current slate) |

---

## Files Changed Summary

| File | Action |
|------|--------|
| `src/brand/brand-tokens.css` | **Replace** `:root` block; **add** `@theme` block |
| `src/index.css` | **Add** Google Fonts import; **consolidate** surface variables |
| `src/components/CorporateLanding.tsx` | **Replace** 30× `#2D3748` with token references |
| `src/components/FloatingNav.tsx` | **Replace** 1× `#2D3748` |
| `src/components/InteractiveOperatingModel.tsx` | **Replace** 5× `#2D3748` |
| `src/components/TemplatesArtifacts.tsx` | **Replace** 3× `#2D3748` |
| `src/components/TransformationDiagnostic.tsx` | **Replace** 4× `#2D3748` |
