# LightSpeed Holdings Limited — Brand Quick Reference

**For agents, developers, and team members.**

This is a pointer, not a second source of truth. If anything here disagrees with the
documents below, those win — and this file should be fixed.

| Document | Location | Purpose |
|----------|----------|---------|
| **Brand Guidelines** | `brand/guidelines/brand-guidelines.md` | Canonical: identity, logo variants, colour rules, typography |
| **Brand Tokens** | `brand/tokens/brand-tokens.json` | Machine-readable colours, type scale, minimum logo sizes |
| **Asset Inventory** | `brand/README.md` | Directory layout of canonical assets |
| **Provenance** | `brand/CANONICAL_SOURCES.md` | What is canonical, what is a mirror, what is archived |

---

## Brand Identity

| Element | Value |
|---------|-------|
| **Company Name** | LIGHTSPEED HOLDINGS LIMITED |
| **Tagline** | ASPIRE. ACT. ACHIEVE. |
| **Primary Color** | Dark Navy `#070A40` |
| **Accent — Red** | `#E63946` |
| **Accent — Cyan** | `#00BFFF` |
| **Logo Symbol** | Angular speed-mark (cyan/blue slab + red chevron) |

---

## Logo Variants

Canonical location: **`brand/logo/`** — 8 variants, each with an SVG and a PNG sibling.
Runtime mirrors: `static/brand/logo/` and `public/brand/logo/`. Select by background.

| Variant | File | Use For |
|---------|------|---------|
| Full Logo | `logo-full.png` / `.svg` | Light/white backgrounds — headers, covers, presentations |
| Full Logo (light bg) | `logo-light-bg.png` / `.svg` | Dark or navy backgrounds |
| Full Logo (dark bg) | `logo-dark-bg.png` / `.svg` | Darker textured backgrounds |
| Mark | `logo-mark.png` / `.svg` | Bare speed-mark where the wordmark is already present |
| Mark (mono) | `logo-mark-mono.png` / `.svg` | Single-colour contexts, embossing, one-colour print |
| Avatar | `logo-avatar.png` / `.svg` | Square crops, social avatars, round placements |
| Favicon | `logo-favicon.png` / `.svg` | Browser tabs, small favicons |
| Open Graph | `logo-og.png` / `.svg` | 1200×630 social/OG share cards |

Most concepts also ship a `-transparent.png` twin, and the twin inherits the artwork's
intended background rather than being universally safe:

| Twin family | Ink | Usable on |
|-------------|-----|-----------|
| `logo-full-transparent`, `logo-og-transparent`, `logo-dark-bg-transparent` | white | dark only |
| `logo-light-bg-transparent`, `logo-mark-mono-transparent` | navy `#070A40` | light only |
| `logo-avatar-transparent`, `logo-favicon-transparent`, `logo-mark-transparent`, `logo-no-background` | mark only | light and dark |

So `logo-mark-mono-transparent.png` disappears on navy, and `logo-full-transparent.png`
disappears on white. Note the naming of `logo-light-bg`: it is the lockup tuned **for** dark
and navy backgrounds (a transparent twin for light backgrounds), which reads backwards. Full
matrix: `brand/guidelines/brand-guidelines.md` § 3.

## Colors

| Name | Hex | Usage |
|------|-----|-------|
| Navy Primary | `#070A40` | Headlines, primary brand surfaces |
| Red Accent | `#E63946` | Calls to action, accent elements |
| Cyan Accent | `#00BFFF` | Accent elements, taglines on navy |
| Light Grey | `#F2F2F2` | Backgrounds |
| White | `#FFFFFF` | Clean backgrounds |

## Minimum Sizes

From `brand/tokens/brand-tokens.json`:

| Context | Full Logo | Icon Only |
|---------|-----------|-----------|
| Print | 30mm wide | 12mm wide |
| Screen | 120px wide | 32px wide |

## Clear Space

Minimum clear space = height of the "L" in "LIGHTSPEED" on all sides of the logo.

## Rules

1. **Never** recreate the logo — always use official assets from `brand/logo/`
2. **Never** stretch, rotate, or distort the logo
3. **Never** change logo colors
4. **Always** maintain clear space
5. **Always** use vector (SVG/PDF/EPS) for print
6. **Always** use the transparent variant on non-white backgrounds
7. **Always** use `™` on first mention: "LightSpeed Holdings Limited™"
8. **Never** redraw or "clean up" logo artwork — the SVGs are vector masters

## Dashboard Exception

The CEO Dashboard (`src/ai_company/dashboard/`) uses the J.A.R.V.I.S. theme with the "LS" placeholder. This is an internal tool, NOT public-facing brand. Do NOT rebrand the dashboard.

## Asset Directory

```
brand/                     # Canonical. Mirrors: static/brand/, public/brand/
├── logo/                  # 8 logo concepts, SVG + PNG, plus transparent variants
├── guidelines/            # brand-guidelines.md (canonical guidance)
├── tokens/                # brand-tokens.json + brand-tokens.css (canonical-only)
├── print/                 # Letterhead, business cards, email signatures
├── digital/               # Social card specs and digital guidance
├── CHANGELOG.md           # Version history of brand asset changes
└── README.md              # Asset inventory and usage notes
```

`static/brand/` additionally carries mirror-only working content that has no canonical peer:
`templates/` (deck, document and social generators) and `social/` (generated output).
