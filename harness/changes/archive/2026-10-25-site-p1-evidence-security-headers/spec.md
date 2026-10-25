# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: plan-first (continuation of `2026-10-25-site-claims-nav-sitemap-next-session`, Deferred Tasks T028-T035)
- Questions asked this round: 0

## Goal And Evidence

Close the three P1 items the prior change deferred. Evidence that each is real:

| Item | Evidence of the gap | Where |
|---|---|---|
| FAQ evidence field | `faq-registry.json` describes itself as "28 evidence-controlled questions and answers" but no entry carries an `evidence` field; `src/data/faqs.ts` renders 6 FAQs with no evidence field either. | measured 2026-10-25 |
| Media-registry honesty | ADR-027 requires AI-generated imagery to be non-person and disclosed; no registry maps the site's rendered image assets to origin, licence or disclosure. | `docs/adr/027-ai-generated-imagery-policy.md` |
| Security headers | Production `HEAD /` returns HSTS (Vercel default), `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`. `Content-Security-Policy`, `Permissions-Policy` and `Cross-Origin-Opener-Policy` are absent on `/`, `/contact` and `/api/ping`. | measured 2026-10-25, see `summary.md` |

## User Scenarios And Success

1. **Auditor / institutional buyer** opens the site's FAQ and can trace each answer to a named source, or sees it marked UNKNOWN. Success: no FAQ answer ships without an evidence entry; a test enforces it.
2. **Prospective client** browsing imagery is not misled about what is a real photograph versus an illustration. Success: every image the site renders has a registry entry naming its kind, origin and licence; where AI-generated or illustrative, the site says so.
3. **Security reviewer** inspects response headers and sees a policy that constrains script origins, denies device permissions, and isolates the browsing context. Success: headers present on production and a test prevents their removal.
4. **Engineer** changing any of the above breaks a test rather than silently regressing. Success: three new guard tests, all failing on the pre-change tree (negative control).

## Non-Goals

- Enforcing the CSP in this change. It ships as `Content-Security-Policy-Report-Only`; enforcement is a dated follow-up after real-traffic observation. Rationale: the contact form depends on Cloudflare Turnstile and a wrong `script-src` silently kills the only revenue path.
- Rewriting FAQ or marketing copy for style. Only evidence fields, count corrections and factual disclosure lines.
- Registering the entire brand asset library. Scope is assets the public site actually renders.
- P2 backlog items from the prior change (`#303`, `#306`, `#307`, `#308`, `#376`, `#378`, `#387`, `#305` remainder, dead-file deletion, sector source collapse).

## Constraints

- `main` is protected: branch + PR, 6 required checks. One PR per P1 item for revert granularity.
- Main checkout is on `feat/deck-gate` with uncommitted work. All edits happen in dedicated worktrees under `%TEMP%\opencode\p1-*`.
- No claim may be promoted to `verified` without a mechanically checkable source (AGENTS.md §15).
- Local verification toolchain: `node node_modules/typescript/bin/tsc --noEmit` (global `npx tsc` is TypeScript 7 and fails on `baseUrl`), `npx vitest run`.
- PowerShell 5.1: no `&&`; multi-statement/quoting-heavy commands go to a temp `.ps1`.

## Assumptions

- Vercel applies the `headers` block in `vercel.json` to every path matched by `source: "/(.*)"`, including rewritten SPA routes (confirmed by the three headers already live).
- The only third-party origin the site loads is `challenges.cloudflare.com` (Turnstile script + iframe), derived by scanning `index.html`, `src/` and `api/`.
- Inline styles are unavoidable (`style-src 'unsafe-inline'`): 99 `style={{...}}` occurrences across 15 files under `src/` (127 `style=` attributes total), plus Framer Motion runtime styles. The earlier figure of 52 in the planning draft was a miscount from a non-recursive glob; corrected during implementation.

## Open Questions

None blocking. The CSP enforcement date is recorded as a deferred task, not an open question.

## Resolved Clarifications

- **CSP mode:** Report-Only now, enforce later. Chosen over enforcing immediately because Turnstile breakage is silent and business-critical.
- **FAQ evidence shape:** `{ source, status, note }`, where `status` is `verified` or `unknown`; a `verified` entry must name a repo path that exists.
- **Media registry scope:** assets the site renders (catalog SVGs, logos, OG image), not the whole `static/brand/` tree.
