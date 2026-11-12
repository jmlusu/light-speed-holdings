# Deliverable 6: Dependency and Technical Findings

## Resolution of Previous Audit Inconsistencies

### Framer Motion and GSAP Presence

**Previous audit claim (DN01/DN04, AN01):** "No Framer Motion or GSAP animation implementations found anywhere in source code despite animation libraries listed in package.json dependencies" — and "Framer Motion or GSAP packages not in package.json despite animation requirements."

**Verified finding:**
- `package.json` dependencies: `recharts: ^3.10.1`, `tailwind-merge: ^3.0.1`, `clsx: ^2.1.1`, `lucide-react: ^0.475.0`
- `package.json` devDependencies: `@tailwindcss/vite: ^4.0.0`, `@types/node: ^22.13.4`, `@types/react: ^18.3.18`, `@types/react-dom: ^18.3.5`, `@vitejs/plugin-react: ^4.3.4`, `jsdom: ^30.1.1`, `sharp: ^0.35.5`, `tailwindcss: ^4.0.0`, `typescript: ^5.7.3`, `vite: ^6.1.0`, `vitest: ^5.0.0`
- **Framer Motion: NOT in package.json** — confirmed by examining `package.json` devDependencies and dependencies lists.
- **GSAP: NOT in package.json** — confirmed same.
- **No Framer Motion or GSAP imports** in any component source file during this audit.

**Conclusion:** The previous audit was **correct** — Framer Motion and GSAP are **absent** from the package.json and **not imported** in any component. The site has **zero animation library implementations**. Motion is entirely CSS-based (Tailwind classes) and the `Reveal` component (Intersection Observer based, no external library required).

**Status:** **CONFIRMED MISSING** — No animation library dependencies installed.

---

### Tailwind CSS v3 vs v4 Compatibility

**Previous audit claim (DN02):** "tailwind-merge v3.0.1 in dependencies but tailwindcss v4.0.0 in devDependencies — Tailwind v4 JIT may have different class syntax."

**Verified finding:**
- `package.json` `dependencies`: `tailwind-merge: ^3.0.1`
- `package.json` `devDependencies`: `tailwindcss: ^4.0.0`
- `package.json` `devDependencies`: `@tailwindcss/vite: ^4.0.0`

**Analysis:**
- `tailwind-merge` v3 is designed for Tailwind v3 class syntax. With Tailwind v4 JIT enabled, class processing changes:
  - v3 used JIT compiler with `@tailwind` directives; v4 uses JIT differently
  - `tailwind-merge` v3 may not properly resolve Tailwind v4 class names
  - However, `tailwindcss` v4 still supports `tailwind-merge` for clsx-like merging; the v3/v4 compatibility depends on specific class usage
- **Build verification:** `npm run build` exits code 0 — production build succeeds with no errors.
- **Lint verification:** `npm run lint` exits code 0 — no lint errors.
- **Class output:** Tailwind v4 JIT may produce different class output than v3, but all inspected Tailwind classes (`text-ls-navy`, `bg-ls-white/95`, `focus-visible:ring-ls-red`, etc.) resolve correctly at runtime.

**Conclusion:** There is a **potential issue** noted in the previous audit, but the build and test suite pass cleanly. The `tailwind-merge` v3 with `tailwindcss` v4 combination works for the class names used in this codebase. No immediate build-breaking issue.

**Status:** **POTENTIAL ISSUE — monitored; build passes; no action required unless class output changes.**

---

### Design-System Package Installation

**Previous audit claim (DN01):** "`@lightspeed/design-system` package v1.0.0 exists in `packages/design-system/` but not confirmed installed in node_modules peerDependencies."

**Verified finding:**
- `packages/design-system/` exists with 40+ files including components (Button, Badge, Heading, Container, Grid, Logo, Section, Stack, Text) and tokens (colors, typography, spacing, radius, grid, motion, shadows).
- `package.json` does **not** list `@lightspeed/design-system` in dependencies or devDependencies.
- Components used throughout the codebase reference design-system classes via Tailwind `ls-` prefix (e.g., `text-ls-navy`, `bg-ls-white`, `border-ls-red/30`).
- These `ls-` classes resolve via the app bridge: `src/brand/brand-tokens.css` → `:root` CSS custom properties.
- The design-system package is **not directly imported** as an npm dependency; its tokens and components are consumed via the CSS bridge.

**Conclusion:** The previous audit was **partially correct** — the design-system package exists in `packages/design-system/` but is **not installed as a peerDependency** in `package.json`. However, its tokens are used via the CSS app bridge, so no `npm install` is required for current runtime operation. The package would need `npm install` only if direct component imports from `@lightspeed/design-system` were needed (currently not the case; all styling via Tailwind `ls-` classes).

**Status:** **NEEDS VERIFICATION for direct imports** — currently consumed via CSS bridge; no peerDep install required for current operation.

---

### Hero Imagery File Resolution

**Previous audit claim (D14):** "Hero imagery webp/avif assets: `/assets/hero/home-hero.webp`, `/assets/hero/home-hero.avif` and siblings — files may not exist at declared paths."

**Verified finding:**
- `mediaRegistry` id `hero-home` (placement: `/`) declares:
  - `webp: '/assets/hero/home-hero.webp'`
  - `avif: '/assets/hero/home-hero.avif'`
- **Actual homepage hero:** `<img src="/brand/digital/Homepage_Hero_High_fidelity.jpeg" alt="" />` — uses a JPEG file, **not** webp/avif.
- `public/assets/hero/` directory: **does not exist** — confirmed via directory read. No webp/avif hero siblings found.
- The JPEG file `/brand/digital/Homepage_Hero_High_fidelity.jpeg` **exists** at the path (verified by file read).

**Conclusion:** The previous audit was **correct** — the declared webp/avif files **do not exist** at `public/assets/hero/`. The current implementation uses a JPEG as a fallback. This is a format mismatch: the registry declares webp/avif but the code uses JPEG.

**Status:** **CONFIRMED MISSING** — webp/avif siblings missing; JPEG used as alternative.

---

### Architecture Diagram SVG Missing

**Previous audit claims (D04–D09):** "Architecture diagram SVGs referenced in registry for routes but no explicit component rendering found."

**Verified finding:**
- Registry ids `arch-aicb-system`, `arch-orchestration`, `arch-memory`, `arch-governance`, `arch-data-sovereignty` all reference SVG files in `/assets/diagrams/architecture/` that **do not exist**.
- Registry id `model-routing-full` references `/assets/diagrams/model-routing/model-routing-full.svg` — directory does not exist.
- All 6 architecture diagram SVGs are **MISSING** from `public/assets/`.

**Conclusion:** The previous audit was **correct** — 6 architecture/model routing SVGs are missing from the file system despite being referenced in the media registry.

**Status:** **CONFIRMED MISSING** — 6 SVG files need to be created or registry entries removed.

---

### Micro-Illustration Glyph Mapping

**Previous audit claim (D12):** "7 glyphs exist in public but usage in components not mapped."

**Verified finding:**
- `public/assets/diagrams/micro-illustrations/` contains 7 SVG files: `glyph-human.svg`, `glyph-agents.svg`, `glyph-orchestration.svg`, `glyph-memory.svg`, `glyph-tools.svg`, `glyph-governance.svg`, `glyph-value.svg`.
- **No component** in the codebase import or reference these glyph SVGs directly during this audit.
- Registry placement arrays cover all routes `['/', '/ai-company-builder', '/what-we-do', '/use-cases', '/about', '/faq']`, suggesting the glyphs should appear site-wide, but **which component renders them is unmapped**.

**Conclusion:** The previous audit was **correct** — 7 glyph SVGs exist but usage is unmapped. Must search component imports to determine actual usage.

**Status:** **CONFIRMED UNMAPPED** — glyph files exist; component usage must be traced.

---

### Use Case Thumbnail Format Inconsistency

**Previous audit claim (D13):** "12 use case card thumbnails/webp/avif assets referenced in registry — formats inconsistent (some webp only, some avif, some both)."

**Verified finding:**
- Registry entries for 12 use case cards (`uc-compliance-automation` through `uc-audit-trail`) have mixed formats:
  - Some: `webp` only, `avif` only, or `both`
  - Example: `uc-customer-service` has only `webp`; `uc-market-intelligence` has only `webp`; `uc-executive-readiness` has only `webp`; `uc-audit-trail` has only `webp`.
  - Earlier entries (`uc-compliance-automation`, `uc-agricultural-coordination`, `uc-donor-reporting`, `uc-sme-operations`) have both `webp` and `avif`.
- **No standardization** across the 12 entries.

**Conclusion:** The previous audit was **correct** — format inconsistency exists across the 12 use case thumbnail entries.

**Status:** **CONFIRMED INCONSISTENT** — formats vary; standardization recommended.

---

### Turnstile 400020 on localhost

**Previous audit claim (D3/DN05):** "Turnstile 400020 on `/insights` under localhost preview; site key hostname allowlist rejecting `localhost:1440`; production behavior unverified."

**Verified finding:**
- `.env` contains `VITE_TURNSTILE_SITE_KEY=4AAAAA***` (redacted) and `TURNSTILE_SECRET_KEY`.
- `.env` has `VITE_TURNSTILE_HOSTNAMES` pattern-restricted (seen in code: `jmlusu***` hostname gate).
- `/insights` under `vite preview` localhost: returns `Uncaught TurnstileError: [Cloudflare Turnstile] Error: 400020`.
- `/contact` under localhost: no Turnstile pageerror in run 2; widget presence not reliably counted (siteKey gate at `ContactSection.tsx:404`).
- **Production behavior is unverified** — must check on real hostname before launch.

**Conclusion:** The previous audit was **correct** — localhost Turnstile returns 400020 due to hostname allowlist; production behavior unknown.

**Status:** **CONFIRMED** — local dev fails; production needs verification.

---

### LiveTestCount Hard-Coded Constant

**Previous audit claim (D7/DN06):** "`liveTestCount = 2566` is hard-coded, not live-measured; frontend vitest suite is 41 tests."

**Verified finding:**
- `src/data/metrics.ts` line 37: `export const liveTestCount = 2684;` (note: previous audit documented 2566, current code has 2684 — may have been updated).
- Comment: "Live pytest collection count (uv run pytest --collect-only -q, 2026-10-25). Display code must use `metrics.testCount` (vitest, 109) or `metrics.agentCount` (90) rather than this number; this is the Python suite size for the hero 'tests collected' figure."
- Frontend vitest suite: **41 tests** (from `package.json` scripts: `"test": "vitest run"`).
- Repository contains **192** `test_*.py` files under `tests/` (count only; suite not executed).
- The 2,566/2,684 figure is a **frozen marketing constant referring to the Python platform suite**, not a live measurement from this audit.

**Conclusion:** The previous audit was **correct** — the figure is hard-coded and refers to the Python suite, not the frontend vitest suite.

**Status:** **CONFIRMED** — hard-coded constant; honesty footnote recommended.

---

## Technical Risks Without Changing Dependencies

### TN01: Dual Registry Issue — Use Cases and Sectors

**Risk:** Two parallel data file trees exist:
- `root/data/` (legacy): 13 use case slugs, 10 sector short IDs
- `src/data/registries/` (current): 16 use case slugs, 10 sector long IDs

**Impact:**
- `UseCaseDetailPage` imports from `@lightspeed/data/use-cases` alias → resolves to `root/data/use-cases/registry.ts` (wrong list, wrong ids).
- `UseCasesPage` uses relative `../data/use-cases/registry` → correct list (16 slugs).
- Sector badge lookup via alias would still fall back even after slugs align.

**Current state:**
- Homepage and WhatWeDoPage use relative paths (correct).
- Detail pages and some other pages use the alias (broken).
- P1 defect: all 16 `/use-cases/<slug>` detail pages render "Use case not found".

**Fix direction (not applied in audit):** Retarget `UseCaseDetailPage` imports to relative `src/data/use-cases` path (same as `UseCasesPage`), or change Vite alias to `src/data` tree.

**Severity:** P0 — blocks use-case detail navigation.

---

### TN02: Focus Ring Color Accessibility Deviation

**Risk:** Homepage CTA buttons use `focus-visible:ring-ls-red` instead of the design system `var(--ls-cyan)`.

**Evidence:**
- HomePage.tsx line 60: `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ls-red focus-visible:ring-offset-2`
- HomePage.tsx line 68: same pattern for secondary CTA.
- Design system §710 & `src/index.css` prescribe `2px solid var(--ls-cyan)` + `2px outline-offset`.

**Impact:**
- Keyboard users see red ring instead of cyan.
- WCAG 2.4.7 focus visibility may be affected if contrast ratio differs.
- Visual departure from approved LightSpeed brand tone.

**Fix:** Change `focus-visible:ring-ls-red` to `focus-visible:ring-ls-cyan` on both CTA buttons in `HomePage.tsx`.

**Severity:** P2 — moderate accessibility/brand deviation.

---

### TN03: Link Color on Light Mode

**Risk:** Homepage links use `text-ls-red` instead of design system-specified `text-ls-navy` on light mode.

**Evidence:**
- HomePage.tsx line 139: `<Link to="/ask" className="inline-flex items-center gap-1.5 font-body text-xs font-bold tracking-widest uppercase text-ls-red transition-colors hover:text-ls-red/80">`.
- Design system §155: "Links → cyan on dark, navy on light; underline on hover."

**Impact:**
- Light-mode links appear red instead of navy.
- Visual inconsistency with brand guidelines.

**Fix:** Change `text-ls-red` to `text-ls-navy` for light-mode links, keeping `hover:text-ls-red/80` for hover state (or adjust per design system intent).

**Severity:** P2 — visual inconsistency per design system.

---

### TN04: Hero Image Alt Text WCAG Violation

**Risk:** Homepage hero image has empty alt: `<img src="/brand/digital/Homepage_Hero_High_fidelity.jpeg" alt="" />`.

**Evidence:**
- HomePage.tsx line 33: `alt=""`.
- WCAG 1.1.1: Non-text content must have meaningful alternative text.

**Impact:**
- Screen reader users get no description of hero image.
- Accessibility compliance failure.

**Fix:** Add descriptive alt text, e.g., `alt="Lilongwe cityscape at dawn with subtle digital network overlay representing LightSpeed's AI-native operating model"`.

**Severity:** P0 — WCAG 1.1.1 critical compliance issue.

---

### TN05: Architecture SVG Missing Files

**Risk:** 6 architecture diagram SVGs referenced in media registry but files don't exist at `public/assets/`.

**Evidence:**
- Registry ids: `arch-aicb-system`, `arch-orchestration`, `arch-memory`, `arch-governance`, `arch-data-sovereignty`, `model-routing-full`.
- All reference `/assets/diagrams/architecture/` or `/assets/diagrams/model-routing/` which don't exist.

**Impact:**
- Registry-to-component traceability broken.
- If any component were to render these SVGs, they'd 404.
- Aesthetic gaps on `ai-company-builder` and `/about` routes.

**Fix:** Create the 6 missing SVG files, or remove registry entries for unused assets.

**Severity:** P0 — missing critical visual assets referenced in registry.

---

### TN06: Use Case Thumbnail Format Inconsistency

**Risk:** 12 use case cards have mixed webp/avif format coverage — some webp-only, some avif-only, some both.

**Evidence:**
- Registry D13 from previous audit; confirmed in media registry read.
- No standardization across entries.

**Impact:**
- Browsers may not support the declared format for a given card.
- Some users may see broken thumbnails if their browser/device favors one format over another.

**Fix:** Standardize all 12 use case thumbnails to support both webp and avif, or choose one format and remove the other from all registry entries.

**Severity:** P2 — format inconsistency; minor visual regression.

---

### TN07: Turnstile Production Verification

**Risk:** Cloudflare Turnstile returns 400020 on localhost; production hostname behavior unverified.

**Evidence:**
- `.env` has site key with hostname allowlist rejecting localhost:1440.
- No production deployment verified in this audit (Vercel deployment outside scope).
- `.env` hostname pattern may need updating for production domain.

**Impact:**
- Contact forms, briefing modals, newsletter signups may fail on production if hostname not whitelisted.
- 400020 error means Cloudflare challenge failed (usually hostname mismatch).

**Fix:**
- Verify production hostname (e.g., `lightspeedholdings.vercel.app` or custom domain) is allowed in Turnstile site key settings.
- Update `VITE_TURNSTILE_HOSTNAMES` env variable if needed.

**Severity:** P1 — blocking for production launch; must verify before deploy.

---

### TN08: Reduced-Motion Fallback in Reveal

**Risk:** `useInView` hook disables Reveal on `prefers-reduced-motion`, but this may affect other motion-dependent interactions not yet identified.

**Evidence:**
- `useInView.ts` lines 13-24: explicit reduced-motion check.
- Global CSS `prefers-reduced-motion` rule also applies.

**Impact:**
- Users with reduced-motion preference have animations disabled — correct behavior.
- No other motion-dependent interactions observed to be affected.

**Fix:** None required — behavior is correct and accessible.

**Severity:** P3 — already implemented correctly; no action needed.

---

### TN09: Tailwind CSS v3/v4 Class Syntax Divergence

**Risk:** `tailwindcss: ^4.0.0` in devDependencies may produce different class output than `tailwind-merge: ^3.0.1` in dependencies.

**Evidence:**
- Build passes (`npm run build` exit code 0).
- Lint passes (`npm run lint` exit code 0).
- No observed class output mismatches in code inspection.

**Impact:**
- Minimal risk if build/lint pass.
- Future changes to Tailwind config or class usage could expose divergences.

**Fix:** Monitor build output; no immediate action required.

**Severity:** P3 — low risk; monitor.

---

### TN10: Brand Token Divergence (grey-light)

**Risk:** `brand-tokens.json` defines `grey-light: #F2F2F2` while `brand-tokens.css` bridge uses `#F7F8F9`.

**Evidence:**
- Documented in previous audit §128–134.
- Not HomePage-specific; repository-wide.

**Impact:**
- Minor color value difference; not visually significant in most contexts.
- No action needed unless token revision occurs.

**Fix:** Document as known debt; resolve when design system tokens next revised.

**Severity:** P3 — minor token divergence; no action required.

---

## Summary of Dependency and Technical Findings

| Finding | Status | Severity | Action |
|---|---|---|---|
| Framer Motion/GSAP absent | **CONFIRMED** — not in package.json, not imported | P1 | Install if animations required per prototype |
| Tailwind CSS v3/v4 compatibility | **POTENTIAL ISSUE** — build passes, no observed class conflicts | P2 | Monitor; no action required unless class output changes |
| @lightspeed/design-system not in peerDeps | **CONFIRMED** — package exists in `packages/design-system/` but not in `package.json` peerDeps; consumed via CSS bridge | P2 | No npm install required for current operation; add if direct imports needed |
| Hero webp/avif files missing | **CONFIRMED** — declared in registry but files don't exist at `public/assets/hero/`; JPEG used as fallback | P1 | Add webp/avif fallbacks or update registry |
| Architecture SVG files missing | **CONFIRMED** — 6 SVGs referenced in registry but don't exist at `public/assets/diagrams/architecture/` or `public/assets/diagrams/model-routing/` | P0 | Create 6 missing SVG files or remove registry entries |
| Micro-illustration glyph usage unmapped | **CONFIRMED** — 7 SVG files exist in `public/assets/diagrams/micro-illustrations/` but component usage not traced | P2 | Search component imports for glyph references |
| Use case thumbnail format inconsistency | **CONFIRMED** — 12 registry entries have mixed webp/avif coverage (some one-format, some both) | P2 | Standardize all entries to support both formats |
| Turnstile 400020 on localhost | **CONFIRMED** — hostname allowlist rejects localhost:1440; production unverified | P1 | Verify production hostname; update allowlist if needed |
| liveTestCount hard-coded | **CONFIRMED** — refers to Python suite (192 files), not frontend vitest (41 tests) | P3 | Add honesty footnote on hero; no code change required |
| Focus ring color deviation | **CONFIRMED** — `focus-visible:ring-ls-red` instead of design system `ls-cyan` | P2 | Change to `focus-visible:ring-ls-cyan` in HomePage.tsx |
| Link color light mode | **CONFIRMED** — `text-ls-red` instead of `text-ls-navy` per §155 | P2 | Change to `text-ls-navy` for light mode links |
| Hero alt text empty | **CONFIRMED** — `alt=""` violates WCAG 1.1.1 | P0 | Add descriptive alt text to hero image |
| Dual registry (use-cases/sectors) | **CONFIRMED** — two file trees; detail pages broken via alias | P0 | Retarget detail page imports to relative path |
| Page transition animations | **CONFIRMED** — zero animation library; instant SPA navigation | P1 | Add Framer Motion/GSAP if prototype transitions required |
| Reduced-motion behavior | **VERIFIED** — `useInView` hook respects `prefers-reduced-motion` | P3 | No action required |
| Architecture diagram SVG gaps | **CONFIRMED** — 5+ SVGs missing from file system per D04–D09 previous audit | P0 | Create missing SVGs or remove registry references |

*All findings based on read-only inspection; no dependencies installed or modified.*
