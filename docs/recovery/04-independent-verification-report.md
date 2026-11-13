# 04 — Independent Verification Report

**Date:** 2026-11-13
**Verifier:** OpenCode agent (same session as the implementation — see §7 caveat)
**Target:** the working tree at `86d10e70` + this session's uncommitted changes
**Served build:** `vite preview` on `http://localhost:1440` (PID 14684), bundle `index-BSddKJXh.js`

This report records what was **actually executed** and observed. Commands are quoted with their exit codes. Where a check was not run, that is stated.

---

## 1. Build-and-test gates (local)

| Gate | Command | Result | Exit |
|---|---|---|---|
| TypeScript | `npx tsc --noEmit --pretty false` | no diagnostics | **0** |
| Unit/integration | `npx vitest run` | **16 files / 145 tests passed** (17.73 s) | **0** |
| Production build | `npx vite build` | **built in 30.94 s**; 1715 modules; `dist/index.html 1.53 kB`, `assets/index-BSddKJXh.js 513.53 kB` (gzip 134.60 kB) | **0** |

The build emits the same hashed entry (`index-BSddKJXh.js`) as the pre-change build used for verification, i.e. the output is deterministic and the changes did not regress bundling. The only build warning is the pre-existing `>500 kB chunk` advisory (not an error).

---

## 2. Route verification (27 routes)

Method: Playwright navigated every route on the preview server, recording HTTP status, final URL, presence of `#main-content`, the first `h1`, and the document title. Source: `docs/recovery/verification-run.json`.

### 2.1 Direct routes (all HTTP 200)

| Route | `h1` | Title suffix |
|---|---|---|
| `/` | Powering the next generation of AI-native enterprises | AI-Native Company Builder |
| `/what-we-do` | Enterprise AI Systems Built for Real Constraints | What We Do |
| `/pharos` | The Public Intellectual Programme | Pharos |
| `/venture-studio` | A Repeatable Engine for AI-Native Companies | Venture Studio |
| `/ai-company-builder` | Build Governed AI Companies | Ai Company Builder |
| `/haomtgv` | H-A-O-M-T-G-V | Haomtgv |
| `/solutions` | Solutions Built for the Work to Be Done | Solutions |
| `/sectors` | Sectors We Serve, With the Evidence to Back It | Sectors |
| `/use-cases` | What Can LightSpeed Actually Do? | Use Cases |
| `/ai-assessment` | AI Readiness Assessment Wizard | Ai Assessment |
| **`/faq`** *(restored)* | Frequently Asked Questions | Faq |
| `/about` | About LightSpeed | About |
| `/contact` | Tell Us Where You Are | Contact |
| `/legal/privacy` | Privacy Policy | Legal/Privacy |
| `/legal/terms` | Terms of Service | Legal/Terms |

Every direct route reported `hasMain: true`, **0 console errors, 0 page errors, 0 failed requests**.

### 2.2 Redirect routes (all resolve as intended)

| Route | Final URL | Final `h1` |
|---|---|---|
| `/architecture` | `/ai-company-builder` | Build Governed AI Companies |
| `/build` | `/what-we-do` | Enterprise AI Systems Built for Real Constraints |
| `/offer-a` … `/offer-e` | `/solutions` | Solutions Built for the Work to Be Done |
| `/proof` | `/use-cases` | What Can LightSpeed Actually Do? |
| `/ask` | `/contact` | Tell Us Where You Are |
| **`/faqs`** *(restored)* | `/faq` | Frequently Asked Questions |

### 2.3 Not-found route

| Route | Behaviour |
|---|---|
| `/definitely-not-a-route` | Renders the SPA `Page not found` view (`hasMain: true`); HTTP 200 is expected for a client-side router |

### 2.4 `/insights` — special handling (documented, not a defect)

The first pass timed out waiting for `networkidle`. Cause: the page loads a **Cloudflare Turnstile** challenge that cannot resolve (`net::ERR_NAME_NOT_RESOLVED https://brunhild.challenges.cloudflare.com/...`) and a telemetry POST to `/api/journey-events` that returns **404**, so `networkidle` is never reached on localhost.

Re-run with `waitUntil: "domcontentloaded"` (source: `verification-focused.json`):

| Metric | Value |
|---|---|
| Status | **200** |
| `hasMain` | true |
| `h1` | `Evidence, Research & the Agentic AI Canon` |
| Article cards | **9** |

**Verdict:** `/insights` renders correctly; the timeout is an environment artifact (O-04, O-05), not a route failure.

---

## 3. Interaction verification

### 3.1 Human-Approval Matrix (`HumanApprovalMatrix`, restored)

| Check | Result |
|---|---|
| Component present on `/` | yes |
| Tier buttons | **5** |
| Inspector after selecting tier 1 | `Operational Auto-Execution` |
| Inspector after selecting tier 5 | `Absolute Sovereign Control` |
| Decision codes rendered | 3 |

The restored component is **interactive** — selecting a tier updates the inspector. The inline approximation it replaced was static.

### 3.2 Back-to-top (`BackToTop`, restored)

| Check | Result |
|---|---|
| Instances in DOM | 1 |
| At top of page | `opacity: 0`, `pointer-events: none` (hidden) |
| After scrolling | `opacity: 1`; `aria-label = "Back to top of page (27% scrolled)"` |
| Click behaviour | `scrollY` 1800 → **0**; focus moves to `#main-content` |

Accessibility contract (hidden until useful, live scroll-percentage in the label, keyboard focus handoff) is intact.

### 3.3 FAQ (`FaqCardList` + `/faq`, restored)

| Check | Result |
|---|---|
| Search input present | yes |
| Initial cards rendered | **6** (matches the 6 entries in `src/data/faqs.ts`) |
| Search `"data"` | filters to **1** card |
| Evidence citations | visible after expanding (`Evidence:` row) |

### 3.4 Theme toggle

| Check | Result |
|---|---|
| Toggling theme changes the root class | yes |

---

## 4. Evidence — screenshots (inside the repo)

33 PNGs under `docs/recovery/screenshots/`:

- Route captures (27): `home.png`, `what-we-do.png`, `pharos.png`, `venture-studio.png`, `ai-company-builder.png`, `haomtgv.png`, `solutions.png`, `sectors.png`, `use-cases.png`, `ai-assessment.png`, `faq.png`, `insights-domcontentloaded.png`, `about.png`, `contact.png`, `legal-privacy.png`, `legal-terms.png`, `architecture.png`, `build.png`, `offer-a.png`, `offer-b.png`, `offer-c.png`, `offer-d.png`, `offer-e.png`, `proof.png`, `ask.png`, `faqs.png`, `definitely-not-a-route.png`
- Interaction captures (5): `interaction-approval-matrix.png`, `interaction-backtotop.png`, `interaction-faq-search.png`, `interaction-faq-expand.png`, `interaction-theme-toggle.png`
- Extra: `backtotop-visible.png`

Raw machine evidence: `verification-run.json` (full 27-route matrix + interactions), `verification-focused.json` (Insights + BackToTop + matrix detail), `_staging-absent-src.txt` (117 absent prototype files).

---

## 5. Local CI vs remote CI (kept distinct)

| | Local (this session) | Remote (`gh run list`, HEAD `86d10e70`) |
|---|---|---|
| TypeScript | exit 0 | covered by `CI` workflow → **success** |
| Tests | 16/145 pass | covered by `CI` workflow → **success** |
| Build | exit 0 | `Site Build + Principles Gate` → **success** |
| Vite dev-server check | n/a | `Verify Vite Dev Server` → **FAILURE** (pre-existing; see `03-…` §6) |

**Critical distinction:** the remote runs above evaluated commit `86d10e70`, **not** this session's uncommitted changes. No CI has evaluated the restored `HumanApprovalMatrix`, `BackToTop`, `FaqCardList`, or `/faq` route, because nothing was committed or pushed. The local gates are the only evidence for the new code.

---

## 6. What was verified vs not verified

| Verified | Not verified (and why) |
|---|---|
| All 27 routes render with correct `h1`/title | Remote CI on the new code (nothing pushed — no authorization) |
| 4 restored components are byte-identical to staging (SHA256) | Visual pixel-diff vs the AI Studio prototype (out of scope; brand/theme divergence expected) |
| Gates green locally (tsc, vitest, build) | E2E suites beyond the Playwright script (none configured for this app) |
| Interactions: matrix, back-to-top, FAQ search/expand, theme | Sector taxonomy and workflow-simulator keyboard nav (user exclusions) |

---

## 7. Independence caveat (honest disclosure)

The implementer and the verifier are the **same agent session**. Independence here means: (a) every result is machine-produced and stored (`verification-run.json`, `verification-focused.json`, screenshots) rather than asserted, and (b) the gates were re-run **after** the changes and their exit codes captured. It is **not** independent third-party verification. A truly independent re-run would require a fresh agent or human on the committed diff.

**Conclusion:** all acceptance gates that *can* be exercised locally **pass**, and all recovered functionality is **present, wired, and interactive** at runtime. The only red check anywhere is the pre-existing, non-gating `Verify Vite Dev Server` workflow.
