# LightSpeed Holdings — Brand Assets

**Canonical source of truth for all brand materials.**

This directory contains the official, version-controlled brand assets for LightSpeed Holdings Limited. All public-facing and operational touchpoints consume from this directory.

**Tagline:** ASPIRE. ACT. ACHIEVE.

---

## Directory Structure

```
brand/
├── README.md                 # This file
├── CHANGELOG.md              # Version history of brand asset changes
├── logos/                    # All logo variants
│   ├── full/                 # Full logo (icon + wordmark)
│   ├── icon/                 # Icon mark only
│   ├── text/                 # Text wordmark only
│   ├── grayscale/            # Monochrome variants
│   └── print/                # Vector formats (SVG, PDF, EPS)
├── print/                    # Physical materials
│   ├── letterhead/           # Letterhead templates
│   └── business-cards/       # Business card designs
├── digital/                  # Digital assets
│   ├── email-signatures/     # Email signature templates
│   ├── social/               # Social media templates
│   └── favicons/             # Browser/app icons
├── tokens/                   # Design tokens
│   ├── brand-tokens.json     # Source of truth for colors, fonts, spacing
│   └── brand-tokens.css      # CSS custom properties
└── guidelines/               # Brand guidelines
    └── brand-guidelines.md   # Full brand guidelines document
```

---

## Usage

### For Agents & Developers
- **Quick reference:** `static/brand/BRAND_GUIDELINES.md`
- **Full guidelines:** `docs/INVESTOR_BRAND_READINESS_PLAN.md`
- **Roadmap:** `docs/BRAND_ADOPTION_ROADMAP.md`

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
*Last updated: 2026-08-27*
