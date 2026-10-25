# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation. Two independent reviews recorded in `reviews/review.md` (CISO, QA Lead); all findings resolved before code.
- [x] T002 Create three implementation worktrees from `origin/main` plus this record, under `.worktrees/` in the repository root.

## Implementation

### A. Security headers (branch `feat/site-security-headers`, PR #517)

- [x] T010 [P] [US3] Add CSP-Report-Only, Permissions-Policy, COOP, X-DNS-Prefetch-Control and explicit HSTS to `vercel.json`; keep the existing three unchanged.
- [x] T011 [P] [US3] Add `src/__tests__/security-headers.test.ts` — parses the policy into directive→source-set pairs, detects duplicate header keys and directives, rejects any CSP origin outside `'self'`, `data:`, `https://challenges.cloudflare.com`.
- [x] T012 [P] [US3] Document the header table, the Report-Only caveat (no collector; console-scan observation; `frame-ancestors`/`upgrade-insecure-requests` inert) and the `vercel.live` preview noise in `docs/DEPLOYMENT.md`.

### B. FAQ evidence (branch `feat/site-faq-evidence`, PR #519)

- [x] T020 [P] [US1] Add `FaqEvidence`, `registryId` and `evidence` to `src/data/faqs.ts` (6 rendered FAQs).
- [x] T021 [P] [US1] Add `evidence` to all 28 entries in `src/data/registries/faq-registry.json`; description states the real counts (65 verified, 7 unknown); `lastUpdated: 2026-10-25`. Q/A text unchanged.
- [x] T022 [P] [US1] Add `src/__tests__/faq-evidence.test.ts` — pins 28, asserts description counts, evidence presence, `registryId` resolution, claim classification, and literal `path#anchor` presence.

### C. Media registry (branch `feat/site-media-registry`, PR #520)

- [x] T030 [P] [US2] Create `src/data/registries/media-registry.json` — 13 entries covering the live reference set.
- [x] T031 [P] [US2] Add `src/__tests__/media-registry.test.ts` — count pin, independent reference enumeration from `src/**` + `index.html`, path existence, missing-asset agreement, provenance/disclosure rules, and a pinned exclusion for the separate FastAPI dashboard manifest.
- [x] T032 [P] [US2] Add the disclosure sentence to `src/components/SiteFooter.tsx` and assert it in `src/__tests__/footer-disclosure.test.tsx`.

### D. Governance (branch `chore/worktree-policy`, PR #518)

- [x] T033 Add `.worktrees/` to `.gitignore`; verified with `git check-ignore -v .worktrees/`.
- [x] T034 Add the standing consent rule to `AGENTS.md` §7 and the deviation row to §17.

## Validation

- [x] T040 [P] Per worktree: `node node_modules/typescript/bin/tsc --noEmit` → exit 0.
- [x] T041 [P] Per worktree: `npx vitest run` green — 127 / 115 / 116 tests.
- [x] T042 [P] Negative control per guard: fix removed, named failure observed, restored byte-identically, green again.
- [x] T043 `lint-ecl.ps1` PASS on this record (`ECL lint passed`, 29 files scanned, 0 failures); `validation_status: pass`.
- [x] T044 Post-deploy headers: `HEAD`/`GET` against production returned all eight headers on `/`, `/contact`, `/use-cases`, `/ai-company-builder` and `GET /api/ping` (`HEAD` returns 405 there by design). Values match `vercel.json` byte for byte.
- [x] T045 Console scan (the documented observation method) on `/`, `/contact`, `/use-cases`, `/ai-company-builder`: the only Content Security Policy message is `The Content Security Policy directive 'upgrade-insecure-requests' is ignored when delivered in a report-only policy` — the predicted inert directive, not a violation.
- [x] T046 Footer disclosure present in the live DOM on `/contact` and `/use-cases` (`Illustrations on this site are original vector artwork created in-house.`).
- [x] T047 Turnstile reachability under the policy: the script from `https://challenges.cloudflare.com/turnstile/v0/api.js` loads (`window.turnstile` is an object), `turnstile.render()` produces the widget markup with a hidden `cf-turnstile-response` input, and a synthetic `https://challenges.cloudflare.com` iframe loads — so `script-src` and `frame-src` permit the widget host.
- [ ] T048 **Not verified:** a real end-to-end submit through the 5-step contact form (the widget only mounts at step 5), and the disclosure at 375 / 1024 / 1440 widths (no screenshots taken). Not claimed as done.

## Deferred Tasks

- CSP enforcement (flip Report-Only to enforcing) after console-scan observation on production; target 2026-11-01. **New finding for that task:** Cloudflare's own challenge page policy lists sub-hosts our policy does not cover — `hagen.challenges.cloudflare.com`, `brunhild.challenges.cloudflare.com` and several `*.dnstest.challenges.cloudflare.com`. `https://challenges.cloudflare.com` does not match subdomains, so whether Turnstile needs them must be settled before enforcing or the form can break silently.
- Remove `upgrade-insecure-requests` from the report-only policy, or accept it: it emits a console error on every page load, which is permanent noise in the very channel used to observe violations.
- `style-src` narrowing to `style-src-attr 'unsafe-inline'` after inline-style usage is removed.
- `logo-full-v2.svg` is byte-identical to `logo-icon-v2.svg` and `favicon.svg` (same SHA-256) and is titled "favicon" — no wordmark lockup exists. Re-export or rename as its own brand-tree change.
- `public/assets/manifest.json` is unimported and 97 of its 122 asset paths do not exist — cleanup change.
- `src/data/useCases.ts` is unimported and references 8 non-existent `public/assets/catalog/*` files — delete or repair.
- `public/hero-background.jpg` referenced by unused `ClosingCTASection` and absent from the tree — same cleanup change.
- `claim.9-llm-providers` says nine providers while `USE-CASE-CATALOG.md` says "Ten LLM providers"; faq-12 carries the conflict as a note, unresolved.
- P2 backlog from the prior change (`#303`, `#306`, `#307`, `#308`, `#376`, `#378`, `#387`, `#305` remainder).
