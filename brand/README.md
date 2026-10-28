# LightSpeed Holdings — Brand Assets

**Canonical source of truth for all brand materials.**

This directory contains the official, version-controlled brand assets for LightSpeed Holdings Limited. All public-facing and operational touchpoints consume from this directory.

**Tagline:** ASPIRE. ACT. ACHIEVE.

---

## Directory Structure

```
brand/                        # Canonical. Runtime mirrors: static/brand/, public/brand/
├── README.md                 # This file
├── CHANGELOG.md              # Version history of brand asset changes
├── logo/                     # Logo concepts — each as SVG + PNG, most with a -transparent twin
│   ├── logo-full.*           # Full lockup — light/white backgrounds
│   ├── logo-light-bg.*       # Full lockup tuned for navy/dark backgrounds
│   ├── logo-dark-bg.*        # Full lockup for darker textured backgrounds
│   ├── logo-mark.*           # Bare speed-mark, where the wordmark is already present
│   ├── logo-mark-mono.*      # Single-colour mark
│   ├── logo-avatar.*         # Square avatar / round placements
│   ├── logo-favicon.*        # Browser tab / app icon
│   ├── logo-og.*             # 1200x630 share card
│   └── logo-no-background.*  # Mark on a transparent 1024x1024 canvas
├── print/                    # Physical materials
│   ├── letterhead/           # Letterhead templates
│   ├── business-cards/       # Business card designs
│   └── email-signatures/     # Email signature templates
├── digital/                  # Digital specs (e.g. social-card-spec.md)
├── tokens/                   # Design tokens (canonical-only — not mirrored)
│   ├── brand-tokens.json     # Source of truth for colors, fonts, spacing
│   └── brand-tokens.css      # CSS custom properties
└── guidelines/               # Brand guidelines
    └── brand-guidelines.md   # Canonical brand guidelines document
```

`static/brand/` additionally carries mirror-only working content with no canonical peer:
`templates/` (deck, document and social generators) and `social/` (generated output).


---

## Usage

### For Agents & Developers
- **Quick reference:** `static/brand/BRAND_GUIDELINES.md`
- **Canonical guidelines:** `brand/guidelines/brand-guidelines.md`
- **Tokens:** `brand/tokens/brand-tokens.json`
- **Provenance (canonical vs mirror vs archived):** `brand/CANONICAL_SOURCES.md`

### For Web/CLI Integration
- **Runtime serving:** `static/brand/` (symlinked or copied from `brand/`)
- **CSS tokens:** `brand/tokens/brand-tokens.css`

### For Print
- **Business cards:** `brand/print/business-cards/`
- **Letterhead:** `brand/print/letterhead/`
- **Always use vector formats (SVG/PDF/EPS) for print**

---

## Logo Usage Rules

1. **Never** recreate the logo — always use official assets
2. **Never** stretch, rotate, or distort the logo
3. **Never** change logo colors
4. **Always** maintain clear space (1x "L" height on all sides)
5. **Always** use vector (SVG/PDF/EPS) for print
6. **Always** use transparent PNGs on non-white backgrounds
7. **Always** use ™ on first mention: "LightSpeed Holdings Limited™"

---

## Minimum Sizes

| Variant | Print | Screen |
|---------|-------|--------|
| Full Logo | 30mm wide | 120px wide |
| Icon Only | 12mm wide | 32px wide |

---

## Dashboard Exception

The CEO Dashboard (`src/ai_company/dashboard/`) uses the J.A.R.V.I.S. theme with the "LS" placeholder. This is an internal tool, NOT public-facing brand. Do NOT rebrand the dashboard.

---

*For questions, contact: CEO or CMO*
*Last updated: 2026-10-28*
