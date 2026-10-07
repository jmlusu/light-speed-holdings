# LightSpeed Brand — Canonical Sources Registry

**Owner:** Brand Strategist | **Maintainer:** Chief of Staff
**Last updated:** 2026-10-05 (Ticket #309 / Website Transformation Directive, Phase 2)

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
| `static/brand/logo/**` | New logo system, runtime builds | `brand/logo/**` |
| `static/brand/logos/**` | Runtime builds, image imports (legacy) | `brand/logos/**` |
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
| **New logo system (Directive §6)** | `brand/logo/**` | 8 variants (`logo-full`, `logo-dark-bg`, `logo-light-bg`, `logo-mark`, `logo-mark-mono`, `logo-favicon`, `logo-avatar`, `logo-og`) in SVG + PNG. Canonical public brand mark. |
| Design tokens (JSON) | `brand/tokens/brand-tokens.json` | Full palette, type scale, spacing, logo specs |
| Design tokens (CSS) | `brand/tokens/brand-tokens.css` | Web/runtime variables |
| Brand guidelines | `brand/guidelines/brand-guidelines.md` | Human-readable system |
| Logo suite (legacy, deprecated) | `brand/logos/fulllogo/**`, `brand/logos/icononly/**`, `brand/logos/grayscale/**`, `brand/logos/textonly/**` | Official legacy files only; kept until site references migrate to `brand/logo/`. Never recreate. |
| Archived logo explorations | `.archive/brand/logos/**` | Style explorations (Glassmorphism, Skeuomorphism, Analog Nostalgia, icononly experiments) removed from `brand/logos/` + mirrors on 2026-10-05. Historical only. |
| Print masters | `brand/print/**` | Letterheads, business cards, signatures |
| Digital/social covers | `brand/digital/**` | SVG/PDF masters |
| This registry | `brand/CANONICAL_SOURCES.md` | You are here |
| Changelog | `brand/CHANGELOG.md` | Brand asset changes |

## Sync Command

```powershell
pwsh scripts/build/sync-brand.ps1          # copy canonical -> both mirrors (no delete)
pwsh scripts/build/sync-brand.ps1 -DryRun  # preview what would be copied
pwsh scripts/build/sync-brand.ps1 -Prune   # delete mirror-only files in sync dirs
pwsh scripts/build/sync-brand.ps1 -Verify  # hash-compare mirrors vs canonical (exit 1 on drift)
```

Sync dirs: `logo`, `tokens`, `guidelines`, `logos`, `print`, `digital`.

Run after adding/changing any canonical asset, then verify with
`git status` that the mirrors picked up the change.
