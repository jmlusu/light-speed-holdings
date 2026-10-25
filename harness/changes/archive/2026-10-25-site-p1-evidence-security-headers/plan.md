# Plan

## Technical Approach

Three independent workstreams, one PR each, all branched from `origin/main` (`c829d329`). Each lands a guard test so the fix cannot silently regress. A fourth branch carries this ECL record and merges last.

| PR | Branch | Worktree | Scope |
|---|---|---|---|
| A | `feat/site-security-headers` | `%TEMP%\opencode\p1-headers` | `vercel.json` headers + guard test + `docs/DEPLOYMENT.md` |
| B | `feat/site-faq-evidence` | `%TEMP%\opencode\p1-faq` | `src/data/faqs.ts`, `faq-registry.json`, guard test, docs |
| C | `feat/site-media-registry` | `%TEMP%\opencode\p1-media` | `media-registry.json`, guard test, disclosure line, docs |
| D | `chore/site-p1-ecl-record` | `%TEMP%\opencode\p1-ecl` | ECL record + `INDEX.json`, merges last |

### A. Security headers

Add to the existing `headers` entry in `vercel.json`:

- `Content-Security-Policy-Report-Only`: `default-src 'self'`; `script-src 'self' https://challenges.cloudflare.com`; `frame-src https://challenges.cloudflare.com`; `style-src 'self' 'unsafe-inline'`; `img-src 'self' data:`; `font-src 'self' data:`; `connect-src 'self' https://challenges.cloudflare.com`; `form-action 'self'`; `base-uri 'self'`; `object-src 'none'`; `frame-ancestors 'self'`; `upgrade-insecure-requests`.
- `Permissions-Policy`: `camera=(), microphone=(), geolocation=(), payment=(), usb=()`.
- `Cross-Origin-Opener-Policy`: `same-origin`.
- `X-DNS-Prefetch-Control`: `off`.
- Keep the three existing headers unchanged.

Guard test reads `vercel.json` and asserts every required key/value pair, so deleting a header fails CI without network access.

### B. FAQ evidence

- Extend `Faq` in `src/data/faqs.ts` with `evidence: FaqEvidence[]`; populate all 6 rendered FAQs from existing repo sources (claims registry, ADR-027, `src/data/metrics.ts`, `docs/`).
- Add `evidence` to all 28 entries in `src/data/registries/faq-registry.json`; correct the description to the real count and add `lastUpdated: 2026-10-25`.
- Any answer that cannot be sourced is marked `status: "unknown"` rather than promoted.
- Guard test: every FAQ (both files) has at least one evidence entry; every `verified` entry's `source` resolves to an existing file or a claim id present in `claims-registry.json`; the registry description count equals the array length.

### C. Media registry

- New `src/data/registries/media-registry.json`: `{ id, path, kind, origin, licence, disclosure }` for every image the site renders (catalog SVGs referenced by `src/data/useCases.ts`, brand logos in `public/brand/` and `public/*.svg`, `public/og-default.png`).
- `kind` ∈ `logo | illustration | diagram | photograph | ai-generated`. Anything not provable from the repo is `unknown` with a note, never guessed.
- One disclosure sentence on the site, placed where imagery is shown, only if the registry proves it (e.g. all catalog art is authored SVG → state that; do not claim "no stock photography" unless the registry supports it).
- Guard test: every image path referenced from `src/data/useCases.ts` and every file in `public/assets/catalog/` has a registry entry; every entry's `path` exists; no entry has empty `origin`/`licence`.

## Impacted Modules And Files

- `vercel.json`, `docs/DEPLOYMENT.md`, `src/__tests__/security-headers.test.ts`
- `src/data/faqs.ts`, `src/data/registries/faq-registry.json`, `src/__tests__/faq-evidence.test.ts`, `docs/website/SPEC.md` (FAQ section note)
- `src/data/registries/media-registry.json`, `src/__tests__/media-registry.test.ts`, `src/pages/UseCasesPage.tsx` or `src/components/SiteFooter.tsx` (disclosure), `docs/marketing/digital-asset-register.md` (pointer)
- `harness/changes/active/*`, `harness/changes/INDEX.json`

## Interfaces, Data, Permissions

- New exported type `FaqEvidence` and required `evidence` field on `Faq`. No runtime behaviour change; no new dependency; no new network origin.
- New JSON registries are build-time data, not secrets.
- No permission changes: header work is configuration only.

## Spec Gaps Found From Planning

- The prior plan said "FAQ evidence field" without defining the shape; this plan fixes the shape.
- ADR-027 mandates disclosure for AI-generated imagery but no site-level disclosure exists; the media registry is the mechanism.
- `faq-registry.json` claims 28 items while only 6 are rendered — both must carry evidence, but only the 6 are user-visible. Recorded so reviewers do not expect 28 rendered FAQs.

## Risks And Mitigations

| Risk | Mitigation |
|---|---|
| CSP breaks Turnstile in production | Ship `Report-Only`; verify contact form on a preview URL; enforcement is a separate dated task |
| `frame-ancestors`/COOP conflict with Vercel defaults | Values chosen to match the existing `X-Frame-Options: SAMEORIGIN` |
| FAQ evidence becomes decorative | Test requires the source path to exist and the claim id to resolve |
| Media registry asserts unprovable provenance | `unknown` is a valid value; agent must not guess; guard allows `unknown` only with a note |
| Parallel worktrees share one `node_modules` junction | Read-only use of dependencies; no installs in worktrees |

## Verification Plan

### Pre-merge (per PR)

- `node node_modules/typescript/bin/tsc --noEmit` in the worktree → exit 0.
- `npx vitest run` in the worktree → all tests pass, including the new guard.
- Negative control: run the new guard against the pre-change file set and confirm it fails.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/maintenance/lint-ecl.ps1` → PASS (PR D).

### Post-merge / post-deploy

- `HEAD https://lightspeedholdings.vercel.app/` shows `Permissions-Policy`, `Cross-Origin-Opener-Policy`, `Content-Security-Policy-Report-Only`.
- Contact page loads and Turnstile renders on production (manual + Playwright check).
- `faq-registry.json` description count matches entries; `/use-cases` disclosure visible.
- GitHub checks green on `main`; Vercel deployment `success`.

# Health

### Browser verification (3 widths: 375, 1024, 1440)

- `/use-cases` disclosure visible and not clipped at 375.
- `/contact` Turnstile widget renders with the new headers.

### ECL gate

- `lint-ecl.ps1` PASS; `summary.md` `validation_status: pass`; `phase: validate`; `plan_review: approved`; `spec_review: approved`.

### Change close

- Archive to `harness/changes/archive/2026-10-25-site-p1-evidence-security`, reindex, PR D merges.
