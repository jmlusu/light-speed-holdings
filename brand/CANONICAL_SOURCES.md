# LightSpeed Brand — Canonical Sources Registry

**Owner:** Brand Strategist | **Maintainer:** Chief of Staff
**Last updated:** 2026-09-16 (Ticket #309)

## The Rule

`brand/**` at the repo root is the **single canonical source of truth** for all
LightSpeed Holdings brand assets: design tokens, guidelines, logos, print and
digital masters.

- Agents, skills, and generators MUST read from `brand/**`.
- `static/brand/**` and `public/brand/**` are **runtime/web mirrors** for
  deployment. Never hand-edit assets in a mirror — regenerate or copy from
  canonical via `scripts/sync-brand.ps1`.
- A symlink is deliberately NOT used: Windows + git cannot track symlinks
  reliably in this repo, and Vite/Vercel deploy from `public/` while other
  static surfaces read `static/`. A committed copy-on-sync script is the
  mechanism for #309 / roadmap task 4.5.

## Never Edit In The Mirror

| Mirror path | Purpose | Sync source |
|-------------|---------|-------------|
| `static/brand/logos/**` | Runtime builds, image imports | `brand/logos/**` |
| `static/brand/print/**` | Print asset copies | `brand/print/**` |
| `static/brand/guidelines/**` | Guideline copies | `brand/guidelines/**` |
| `static/brand/tokens/**` | Token copies | `brand/tokens/**` |
| `static/brand/digital/**` | Digital asset copies | `brand/digital/**` |
| `public/brand/**` | Website media root (`/brand/...`) | `brand/**` (mirror of root) |

Mirror-only content that has no canonical source (kept in mirrors):
- `static/brand/templates/**` (generators + prebuilt decks/HTML)
- `static/brand/social/**` (generated social outputs)
- `static/brand/BRAND_GUIDELINES.md` (quick reference; canonical is
  `brand/guidelines/brand-guidelines.md`)

## Canonical Paths (Read These)

| Asset | Canonical path | Notes |
|-------|----------------|-------|
| Design tokens (JSON) | `brand/tokens/brand-tokens.json` | Full palette, type scale, spacing, logo specs |
| Design tokens (CSS) | `brand/tokens/brand-tokens.css` | Web/runtime variables |
| Brand guidelines | `brand/guidelines/brand-guidelines.md` | Human-readable system |
| Logo suite | `brand/logos/fulllogo/**`, `brand/logos/icononly/**`, `brand/logos/grayscale/**`, `brand/logos/textonly/**` | Never recreate; official files only |
| Print masters | `brand/print/**` | Letterheads, business cards, signatures |
| Digital/social covers | `brand/digital/**` | SVG/PDF masters |
| This registry | `brand/CANONICAL_SOURCES.md` | You are here |
| Changelog | `brand/CHANGELOG.md` | Brand asset changes |

## Sync Command

```powershell
pwsh scripts/sync-brand.ps1          # copy canonical -> both mirrors (no delete)
pwsh scripts/sync-brand.ps1 -DryRun  # preview what would be copied
```

Run after adding/changing any canonical asset, then verify with
`git status` that the mirrors picked up the change.
