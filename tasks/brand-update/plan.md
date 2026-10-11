# Plan — Brand Logo System Migration + Red Standardization

**Status:** Approved (executing)
**Created:** 2026-10-09
**Scope owner:** Human CEO
**Ticket:** #309 (logo system v1.2.0), #381 (amended policy)

## Objective

Migrate the repo to the new `brand/logo/` logo system (8 variants × SVG+PNG),
standardize the brand red on `#DC3641` (WCAG-AA), archive legacy logo/print
families, and truth-up docs + mirrors so canonical source and runtime mirrors
agree.

## Ground rules

- `brand/**` is the single canonical source; `static/brand/**` + `public/brand/**`
  are runtime/web mirrors. Never hand-edit mirrors — regenerate via
  `scripts/build/sync-brand.ps1`. Exception this pass: mirror-only files
  (`static/brand/templates/**`, `static/brand/social/**`) have no canonical source
  and are edited directly.
- Work surgically: the working tree carries unrelated modifications. Touch only
  brand-task targets.
- J.A.R.V.I.S. CEO Dashboard theme is out of scope (untouched).
- Grey-light token divergence is document-only (no value changes).

## Canonical logo system (new)

`brand/logo/` (singular) — 16 files, 8 families × `.png` + `.svg`:
`logo-full`, `logo-dark-bg`, `logo-light-bg`, `logo-mark`, `logo-mark-mono`,
`logo-favicon`, `logo-avatar`, `logo-og`.

Legacy `brand/logos/` (plural) does not exist in canonical; content survives only
in mirrors and is pruned.

## Workstreams

### WS-A — Web + skill logo refs (broken → new)
- `src/pages/Index.tsx:36` + `:107` → `/brand/logo/logo-full.png`
  (currently broken `/brand/logo/fulllogo*.png`).
- `src/components/site/Logo.tsx:19` → `/brand/logo/logo-full.svg` (full),
  `/brand/logo/logo-mark.svg` (icon). Used by `FloatingNav.tsx` + `SiteFooter.tsx`.
- `.agents/skills/ls-design-system/SKILL.md` — `brand/logos/**` → `brand/logo/**`;
  red `#E63946` → `#DC3641`.
- `.opencode/integrations/open-design/README.md` + `QUICK-REFERENCE.md` — same.

### WS-B — Red `#E63946` → `#DC3641`
- `brand/tokens/brand-tokens.json:21`
- `brand/tokens/brand-tokens.css`: `--ls-red` (L8), `--color-ls-red` (L75),
  `--ls-red-rgb` (L146 → `220, 54, 65`), `--ls-shadow-red` (L175 →
  `rgba(220,54,65,0.15)`)
- `brand/digital/social-card-spec.md`, `brand/guidelines/brand-guidelines.md`,
  `_carousel-concepts.txt`
- Leave `.archive/design-system/**`.

### WS-C — Docs truth-up
- `brand/README.md` L18–71 (legacy tree → new logo system; note archived print).
- `brand/guidelines/brand-guidelines.md` §3 L41–50 + L108.
- `brand/digital/social-card-spec.md` (`icononly.png` → `logo-mark`).
- `reports/issue-381-amended-policy.md:111`.
- Add `brand/CHANGELOG.md` entry.

### WS-D — Archive + sync
- Move `brand/print/**` → `.archive/brand/print/**` (preserve family subdirs).
- Edit mirror-only `static/brand/templates/**` legacy refs directly.
- Run `pwsh scripts/build/sync-brand.ps1 -Prune` (drops `static|public/brand/logos/**`).

### WS-E — Verify
- `pwsh scripts/build/sync-brand.ps1 -Verify` exits 0.
- Grep: zero legacy refs (`brand/logos`, `fulllogo`, `icononly`, `E63946`)
  outside `.archive/`.
- `ruff` / `mypy` / `pytest` if any Python touched.
- Playwright QA (`ls-artifact-qa`) on `Index.tsx` header + footer logo.

## Out of scope

- J.A.R.V.I.S. dashboard theme.
- `public/logos/*.svg` partner/trust-strip marks.
- Grey-light token values.
- Unrelated dirty-tree changes.
