---
title: "site P1 evidence security headers"
slug: "site-p1-evidence-security-headers"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "completed"
spec_review: "approved"
plan_review: "approved"
modules: ["website", "src", "public", "docs", "vercel"]
files: ["vercel.json", "docs/DEPLOYMENT.md", "src/__tests__/security-headers.test.ts", "src/data/faqs.ts", "src/data/registries/faq-registry.json", "src/__tests__/faq-evidence.test.ts", "docs/website/SPEC.md", "src/data/registries/media-registry.json", "src/__tests__/media-registry.test.ts", "src/components/SiteFooter.tsx", "src/__tests__/footer-disclosure.test.tsx", "docs/marketing/digital-asset-register.md", ".gitignore", "AGENTS.md"]
tags: ["site", "security-headers", "csp", "faq", "evidence", "media", "honesty", "governance"]
validation_status: "pass"
created_at: "2026-10-25"
updated_at: "2026-10-25"
session_id: "4ba27b38-e001-4583-a268-99c12d32653a"
owner_agent: "jmlus"
claimed_at: "2026-10-25"
---

# Summary

## Outcome

Closed the three P1 website items the previous change deferred, plus one governance correction the CEO required mid-session. Four PRs, one per item for revert granularity:

| PR | Branch | Delivered |
|---|---|---|
| #517 | `feat/site-security-headers` | 8 security headers declared in `vercel.json` (5 new, 3 kept) and an 18-test guard that parses the policy into directive/source pairs. CSP ships as `Content-Security-Policy-Report-Only`. |
| #519 | `feat/site-faq-evidence` | Evidence on all 6 rendered FAQs and all 28 canonical registry entries: 72 evidence entries, **65 verified, 7 unknown**. Guard pins the 28-entry count and resolves every `verified` source. |
| #520 | `feat/site-media-registry` | `media-registry.json` covering all 13 image paths the site renders (origin, licence, kind, disclosure), a footer disclosure sentence, and 7 guard tests. |
| #518 | `chore/worktree-policy` | Standing consent rule for worktrees (`AGENTS.md` §7), deviation record (§17), `.worktrees/` gitignored. |

## Decisions

- **CSP is Report-Only.** The contact form depends on Cloudflare Turnstile; a wrong `script-src` breaks it silently and no build step notices. Enforcing is a dated follow-up (2026-11-01) after production observation.
- **No CSP report collector.** The CISO's blocker ("Report-Only without a collector observes nothing") was resolved by narrowing the claim, not by adding an endpoint: a public log sink is its own abuse surface. Observation is an automated console scan of four routes plus manual DevTools, documented in `docs/DEPLOYMENT.md`.
- **HSTS declared explicitly** (`max-age=63072000; includeSubDomains; preload`) rather than left as a Vercel default, so the guard protects it. `preload` has no effect until the domain is submitted.
- **FAQ evidence shape** `{ source, status, note? }`; `verified` requires a claim id whose classification is publishable, or `path#anchor` literally present in the file. Seven answers are marked `unknown` rather than promoted.
- **Media registry scope is the live reference set**, not the brand tree. `favicon.ico` and `og-default.png` are `origin: unknown` (no authoring record exists); `hero-background.jpg` is `kind: "missing"`.
- **Worktrees moved inside the repository** to `.worktrees/`. The native `worktree_create` tool places them at `%LOCALAPPDATA%\..\opencode\worktree\<hash>\<name>` (observed), which cannot satisfy the CEO's requirement, so placement uses `git worktree add .worktrees/<name>`.

## Validation

Local, per worktree, after the rebase onto `origin/main` (`8637ac35`):

| Check | Result |
|---|---|
| `node node_modules/typescript/bin/tsc --noEmit` | exit 0 in all four worktrees |
| `npx vitest run` (headers) | 12 files, **127 passed** (109 baseline + 18 new) |
| `npx vitest run` (faq) | 12 files, **115 passed** (109 + 6) |
| `npx vitest run` (media) | 13 files, **116 passed** (109 + 7) |
| Negative controls | Each guard failed when its fix was removed, naming the missing header / `faq-14` / `glyph-tools.svg`; all restored byte-identically and re-passed. |
| `git check-ignore -v .worktrees/` | `.gitignore:219:.worktrees/` |

CI: all four PRs green before merge.

Post-deploy, against `https://lightspeedholdings.vercel.app`:

| Check | Result |
|---|---|
| Headers on `/`, `/contact`, `/use-cases`, `/ai-company-builder` | all 8 present, values match `vercel.json` |
| `GET /api/ping` | 200, all 8 present (`HEAD` → 405 by design) |
| Console scan, 4 routes | only the predicted inert `upgrade-insecure-requests` notice; no violation |
| Footer disclosure | present in the live DOM on `/contact` and `/use-cases` |
| Turnstile | script loads from `challenges.cloudflare.com`, `render()` produces the widget markup, a synthetic `challenges.cloudflare.com` iframe loads |

Not verified, and not claimed: a real end-to-end contact submit (the widget mounts only at step 5 of the form), and the disclosure at 375/1024/1440 widths (no screenshots taken). See T048.

## Next Step

- Merge #521 (this record), remove the worktrees, delete the merged branches.
