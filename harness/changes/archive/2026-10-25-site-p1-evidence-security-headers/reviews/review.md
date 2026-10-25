# Reviews

## Plan Review — 2026-10-25

Two independent reviewers, both read-only, reviewed `spec.md` + `plan.md` before implementation.

### Reviewer 1 — CISO (security)

**Verdict: CHANGES REQUESTED** → resolved before implementation.

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | blocker | Report-Only CSP with no `report-uri`/`report-to` collects nothing, so "observe then enforce" was unexecutable. | Accepted with a narrower claim: no collector is added (a public log sink is its own abuse surface). Observation is redefined as an **automated console scan** of every route plus manual DevTools, and the plan says so explicitly. Enforcement remains a dated deferred task. |
| 2 | major | HSTS is a Vercel default, not declared, so the guard cannot protect it. | Accepted: declare `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`, mirroring what Vercel already sends, and assert it. |
| 3 | major | Guard asserting raw text would pass malformed values; `frame-ancestors` and `upgrade-insecure-requests` are inert in Report-Only. | Accepted: guard parses the policy into directive→source-set pairs and compares exactly. Plan states that `frame-ancestors`/`upgrade-insecure-requests` provide no control in Report-Only. |
| 4 | minor | `style-src 'unsafe-inline'` could be narrowed via `style-src-attr`. | Deferred: narrowing buys no security while `unsafe-inline` remains for attributes; recorded as a follow-up, not silently dropped. |
| 5 | minor | Permissions-Policy deny-set too thin. | Accepted: expanded to camera, microphone, geolocation, payment, usb, browsing-topics, display-capture, hid, serial, bluetooth, idle-detection, accelerometer, gyroscope, magnetometer. |
| 6 | minor | COOP needs no COEP; COEP would risk Turnstile. | Accepted: COOP only, no COEP. |
| 7 | minor | `vercel.live` preview toolbar will violate `script-src 'self'`. | Noted in `docs/DEPLOYMENT.md`; preview-only noise, not allowlisted. |
| 8 | minor | No extra directives needed. | Accepted: `default-src 'self'` inheritance, `frame-src` not `child-src`. |

### Reviewer 2 — QA Lead (testability)

**Verdict: CHANGES REQUESTED** → resolved before implementation.

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | blocker | Media enumeration targeted dead code: `src/data/useCases.ts` has no importer and its `public/assets/catalog/*` paths do not exist. Real render set is tiny. | Accepted. Verified independently: `useCases.ts` is unimported and its 8 catalog paths are absent. Registry scope is now the **live reference set** enumerated from `src/**` + `index.html` (7 glyphs, 2 logos, favicon, OG image). Dead-file deletion is recorded as a separate finding, not done here. |
| 2 | blocker | "count equals array length" is tautological. | Accepted: pin `toHaveLength(28)` and `description` contains `28`. |
| 3 | major | "source path exists" proves nothing; claims registry has `classification`, not `status`. | Accepted: `verified` requires either a claim id whose `classification` is not `UNVERIFIED`/`UNKNOWN`, or `path#anchor` where the file literally contains the anchor text. |
| 4 | major | No link between the 6 rendered FAQs and the 28 registry entries. | Accepted: add `registryId` to each rendered FAQ; assert it resolves and the question text matches. |
| 5 | major | CSP has no collector. | Same resolution as CISO #1: console-scan observation, stated honestly. |
| 6 | major | Negative control not executable as written. | Accepted: exact procedure recorded per test (stash the fix, run the guard, expect named failure, restore). |
| 7 | major | Disclosure line has no test. | Accepted: render `SiteFooter` under `MemoryRouter` and assert the exact sentence. |
| 8 | minor | Header guard must read `vercel.json` from disk and compare exact values. | Accepted (same as CISO #3). |
| 9 | minor | Post-deploy checks only `/`. | Accepted: `/`, `/contact`, `/api/ping`, one deep rewritten route. |

## Code Review — 2026-10-25 (orchestrator, pre-merge)

Each PR diff was read in full before merge. Findings, in order of severity.

| # | PR | Severity | Finding | Resolution |
|---|---|---|---|---|
| 1 | #519 | major | A description edit made after the subagent finished broke the guard (`expected ... to contain 'all 28 entries carry evidence entries'`), leaving the branch red. | Fixed the sentence to the wording the guard pins; `npx vitest run` → 115 passed. Recorded because the failure was mine, not the agent's. |
| 2 | #520 | major | `og-default.png` was filed as `kind: "logo"`, which is not what it is — it is a 1200x630 social card. | Added `social-card` to the allowed kinds and reclassified the entry. Both the registry and the guard changed together, so the guard still constrains the value. |
| 3 | #520 | major | The subagent reported 13 entries where the brief said 12. | Verified the arithmetic: 7 glyphs + 2 logos + hero-background + 3 `index.html` icons = 13. The brief was wrong; the pin is 13 with a comment stating the sum. |
| 4 | #520 | minor | The reference scan excludes `src/ai_company/**` (the separate FastAPI dashboard's PWA manifest, AGENTS.md §13). An unpinned exclusion is a hole. | The exclusion is asserted by value in the test, so it cannot widen silently. |
| 5 | #517 | minor | The docs and the test comment said 52 inline styles; the real count is 99 `style={{ }}` occurrences across 15 files (127 `style=` attributes). | Corrected both files and `spec.md`; the planning figure came from a non-recursive glob. |
| 6 | #519 | minor | `faq-registry.json` had a mojibake `§18` ("Directive A,A18") introduced by an earlier latin-1 round-trip. | Rewrote the description through `json.load`/`json.dump(ensure_ascii=False)`; the section mark is now plain `18` rather than a mangled glyph. |

Not fixed, recorded in `tasks.md` as deferred: `logo-full-v2.svg` carries no wordmark lockup, `public/assets/manifest.json` has 97 missing paths, `useCases.ts` points at files that do not exist.

## Validation Review — 2026-10-25

- `tsc --noEmit` exit 0 in all four worktrees, after the rebase onto `origin/main` `8637ac35`.
- Vitest: 127 (headers) / 115 (faq) / 116 (media) — each includes its new guard; the 109-test baseline is unchanged elsewhere.
- Negative controls executed per guard, with the named failure recorded in each PR body, then restored and re-run green.
- `lint-ecl.ps1` → `ECL lint passed` (29 files, 0 failures, 0 warnings).
- CI green on all four PRs before merge.
- **Post-deploy verified:** all eight headers on `/`, `/contact`, `/use-cases`, `/ai-company-builder` and `GET /api/ping`; footer disclosure in the live DOM; Turnstile script load and `render()` under the policy; console scan clean apart from the inert `upgrade-insecure-requests` notice.
- **Not verified:** an end-to-end contact submit (the widget mounts only at step 5), and the disclosure at 375/1024/1440 widths. Stated as unknown rather than asserted.
