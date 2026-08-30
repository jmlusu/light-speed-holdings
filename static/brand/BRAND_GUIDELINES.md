# LightSpeed Holdings Limited — Brand Quick Reference

**For agents, developers, and team members.**

| Document | Location | Purpose |
|----------|----------|---------|
| **Brand Guidelines** | `docs/INVESTOR_BRAND_READINESS_PLAN.md` | Full brand guidelines with compliance rules |
| **Brand Roadmap** | `docs/BRAND_ADOPTION_ROADMAP.md` | Organization-wide adoption plan & tracking |
| **Quick Reference** | This file | Fast lookup for agents and developers |

---

## Brand Identity

| Element | Value |
|---------|-------|
| **Company Name** | LIGHTSPEED HOLDINGS LIMITED |
| **Tagline** | ASPIRE. ACT. ACHIEVE. |
| **Primary Color** | Dark Navy `#070A40` |
| **Accent — Red** | `#E63946` |
| **Accent — Cyan** | `#00BFFF` |
| **Logo Symbol** | Lighthouse/shield emblem with signal waves |

---

## Logo Variants

| Variant | File | Use For |
|---------|------|---------|
| **Full Logo** | `logos/fulllogo/fulllogo.png` | Headers, covers, presentations |
| **Full Logo (Transparent)** | `logos/fulllogo/fulllogo_transparent.png` | Dark backgrounds, overlays |
| **Icon Only** | `logos/icononly/icononly.png` | Avatars, favicons, small spaces |
| **Icon Only (Transparent)** | `logos/icononly/icononly_transparent.png` | Dark backgrounds |
| **Text Only** | `logos/textonly/textonly.png` | When icon is already present |
| **Grayscale** | `logos/grayscale/grayscale.png` | B&W print, legal documents |
| **Vector (Print)** | `logos/fulllogo/vector/print.svg` | All print materials |
| **Vector (Print, Transparent)** | `logos/fulllogo/vector/print_transparent.svg` | Print on colored backgrounds |

## Colors

| Name | Hex | Usage |
|------|-----|-------|
| Navy Primary | `#070A40` | Headlines, logo text, primary brand |
| Red Accent | `#E63946` | Signal waves, accent elements |
| Cyan Accent | `#00BFFF` | Shield base, accent elements |
| Light Grey | `#F2F2F2` | Backgrounds |
| White | `#FFFFFF` | Clean backgrounds |

## Minimum Sizes

| Context | Full Logo | Icon Only |
|---------|-----------|-----------|
| Print | 30mm wide | 12mm wide |
| Screen | 120px wide | 32px wide |

## Clear Space

Minimum clear space = height of the "L" in "LIGHTSPEED" on all sides of the logo.

## Rules

1. **Never** recreate the logo — always use official assets
2. **Never** stretch, rotate, or distort the logo
3. **Never** change logo colors
4. **Always** maintain clear space
5. **Always** use vector (SVG/PDF/EPS) for print
6. **Always** use transparent PNGs on non-white backgrounds
7. **Always** use `™` on first mention: "LightSpeed Holdings Limited™"

## Dashboard Exception

The CEO Dashboard (`src/ai_company/dashboard/`) uses the J.A.R.V.I.S. theme with the "LS" placeholder. This is an internal tool, NOT public-facing brand. Do NOT rebrand the dashboard.

## Asset Directory

```
static/brand/
├── logos/          # All logo variants
├── templates/      # Pitch deck, one-pager, board templates
├── print/          # Letterhead, business cards, email signatures
├── social/         # Facebook, LinkedIn, Twitter assets
├── BRAND_GUIDELINES.md  # This file
└── README.md       # Asset inventory and usage notes
```
