# Brand Tokens — Human-Readable Overview

**Source of truth:** [`brand/tokens/brand-tokens.json`](tokens/brand-tokens.json) (machine-readable)
**CSS custom properties:** [`brand/tokens/brand-tokens.css`](tokens/brand-tokens.css) and [`src/brand/brand-tokens.css`](../src/brand/brand-tokens.css)
**Full guidelines:** [`brand/guidelines/brand-guidelines.md`](guidelines/brand-guidelines.md)
**Owner:** Brand Strategist / CMO

> Agents creating any artifact (website, deck, document, social post, ad, diagram, infographic) MUST load the `ls-design-system` skill before producing creative output.

---

## Color Palette

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| `--ls-navy` | `#070A40` | `7, 10, 64` | Headlines, logo text, primary brand surfaces, slide rails |
| `--ls-red` | `#E63946` | `230, 57, 70` | Signal waves, accent elements, CTAs, key highlights |
| `--ls-cyan` | `#00BFFF` | `0, 191, 255` | Shield base, links on dark, taglines on navy |
| `--ls-grey-light` | `#F7F8F9` \* | — | Light backgrounds (Morning Mist) |
| `--ls-bg-light` | `#F7F8F9` | — | Light surface background (Morning Mist) |
| `--ls-bg-dark` | `#121518` | — | Dark surface background (Deep Mineral) |
| `--ls-white` | `#FFFFFF` | — | Clean backgrounds, text on navy |
| `--ls-grey-dark` | `#6B7280` | — | Secondary text, captions |
| `--ls-grey-light-text` | `#9CA3AF` | — | Tertiary text on dark surfaces |

\* Canonical [`brand-tokens.json`](tokens/brand-tokens.json) defines `grey-light` as `#F2F2F2`; `src/brand/brand-tokens.css` uses `#F7F8F9` (Morning Mist). Divergence pending a brand decision — do not add new grey values.

### On-surface text

| Token | Value | Context |
|-------|-------|---------|
| `--ls-on-navy` | `#FFFFFF` | Text on navy surfaces |
| `--ls-on-red` | `#FFFFFF` | Text on red accent surfaces |
| `--ls-on-cyan` | `#070A40` | Text on cyan accent surfaces |

### RGB channels (for `rgba()`)

| Token | Value |
|-------|-------|
| `--ls-navy-rgb` | `7, 10, 64` |
| `--ls-red-rgb` | `230, 57, 70` |
| `--ls-cyan-rgb` | `0, 191, 255` |

Use in CSS: `rgba(var(--ls-red-rgb), 0.3)`

### Color rules

- Navy is dominant. Red and cyan are accents — roughly 80/10/10 navy/red/cyan on brand surfaces.
- Do NOT add new colors without a documented brand decision.

---

## Typography

| Token | Value | Usage |
|-------|-------|-------|
| `--ls-font-display` | `Arial, sans-serif` | Hero headlines, cover titles |
| `--ls-font-heading` | `Arial, sans-serif` | Section titles, slide titles |
| `--ls-font-body` | `Arial, sans-serif` | Paragraph text, slide body |
| `--ls-font-caption` | `Arial, sans-serif` | Captions, footnotes, disclaimers |
| `--ls-weight-display` | `700` | Display headings |
| `--ls-weight-heading` | `700` | Section headings |
| `--ls-weight-body` | `400` | Body copy |

### Type scale (pt)

| Token | Size | Usage |
|-------|------|-------|
| `--ls-size-display-xl` | 36pt | Hero display |
| `--ls-size-title-xl` | 32pt | Page title |
| `--ls-size-title-lg` | 28pt | Section title |
| `--ls-size-title-md` | 24pt | Subsection title |
| `--ls-size-title-sm` | 18pt | Card title |
| `--ls-size-subtitle` | 16pt | Subtitle |
| `--ls-size-body-lg` | 16pt | Large body |
| `--ls-size-body` | 14pt | Body |
| `--ls-size-body-sm` | 13pt | Small body |
| `--ls-size-caption` | 12pt | Caption |

Do not invent sizes outside this scale.

---

## Spacing (4px base unit)

| Token | Value |
|-------|-------|
| `--ls-space-1` | 4px |
| `--ls-space-2` | 8px |
| `--ls-space-3` | 12px |
| `--ls-space-4` | 16px |
| `--ls-space-5` | 24px |
| `--ls-space-6` | 32px |
| `--ls-space-7` | 48px |
| `--ls-space-8` | 64px |
| `--ls-space-9` | 96px |

All spacing must be multiples of 4px.

---

## Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `--ls-radius-sm` | 4px | Buttons, small elements |
| `--ls-radius-md` | 8px | Cards, panels |
| `--ls-radius-lg` | 16px | Feature sections, modals |

---

## Grid

| Token | Value |
|-------|-------|
| `--ls-grid-columns` | 12 |
| `--ls-gutter` | 24px |
| `--ls-margin` | 48px |
| `--ls-page-max-width` | 1200px |

---

## Layout

| Token | Value | Usage |
|-------|-------|-------|
| `--ls-slide-width` | 10in | PPTX slide width (4:3) |
| `--ls-slide-height` | 7.5in | PPTX slide height |
| Navy rail | 0.15in | Left edge of content slides |

---

## Motion

| Token | Value |
|-------|-------|
| `--transition-slow` | 500ms ease |
| `--transition-medium` | 300ms ease |
| `--transition-fast` | 150ms ease |
| `--ease-spatial` | cubic-bezier(0.4, 0, 0.2, 1) |

---

## Dark Mode

| Token | Light | Dark |
|-------|-------|------|
| Background | `--ls-bg-light` (`#F7F8F9`) | `--ls-bg-dark` (`#121518`) |
| Surface | `--ls-surface-light` (`#FFFFFF`) | `--ls-surface-dark` (`#1A1D21`) |
| Text | `--ls-text-light` (`#121518`) | `--ls-text-dark` (`#F7F8F9`) |
| Text secondary | `--ls-text-secondary-light` (`#6B7280`) | `--ls-text-secondary-dark` (`#9CA3AF`) |
| Border | `--ls-border-light` (`#E5E7EB`) | `--ls-border-dark` (`#2A2D31`) |

Dark mode toggles via `.dark` class on `<html>` (class-based, not OS preference).

> **Naming note:** In CSS use `var(--ls-bg-light)` / `var(--ls-bg-dark)` etc. (defined in `:root`). The names `ls-mist` / `ls-slate` exist only as Tailwind palette entries (`--color-ls-mist` / `--color-ls-slate` in `@theme`), usable as classes like `bg-ls-slate` — there is no `--ls-mist` / `--ls-slate` custom property.
>
> **Location note:** Surface/text/border (`--ls-bg-*`, `--ls-text-*`, `--ls-surface-*`, `--ls-border-*`), RGB channel, and motion tokens are defined only in [`src/brand/brand-tokens.css`](../src/brand/brand-tokens.css), not in the standalone `brand/tokens/brand-tokens.css`.

---

## Implementation

### CSS

```css
@import "brand/tokens/brand-tokens.css";

.my-component {
  background: var(--ls-navy);
  color: var(--ls-on-navy);
  padding: var(--ls-space-4);
  border-radius: var(--ls-radius-md);
}
```

### Tailwind v4 (`src/brand/brand-tokens.css`)

```html
<div class="bg-ls-navy text-ls-white p-4 rounded-md">
```

### JSON (design tooling / scripts)

```python
import json
tokens = json.load(open("brand/tokens/brand-tokens.json"))
navy = tokens["color"]["navy"]["value"]  # "#070A40"
```

---

## Compliance Checklist

- [ ] Logo from official assets, never recreated
- [ ] Logo clear space respected (1× "L" height on all sides)
- [ ] Only palette colors used
- [ ] Vector format for print, transparent PNG on dark
- [ ] `™` on first mention of company name
- [ ] Type sizes from the brand scale
- [ ] Spacing multiples of 4px
- [ ] Tagline spelled exactly "ASPIRE. ACT. ACHIEVE."
