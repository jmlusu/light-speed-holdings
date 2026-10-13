# Pharos artifact QA, 2026-10-12

**Auditor:** ls-artifact-qa (Playwright probe + source + brand-token audit)
**Date:** 2026-10-12
**Scope:** three public HTML artifacts dated 2026-10-12
**Method:** `visual_check.cjs` at 1280x800 and 375x667; full-file source read; brand tokens from `brand/tokens/brand-tokens.json`; content claims cross-checked against `company-registry.yaml`, `pyproject.toml`, `package.json`, `docs/Pharos/pillars/`, and in-artifact provenance blocks.
**Evidence mode:** read-only audit, no artifact was modified. Screenshots and probe JSON written only under `docs/Pharos/qa/`.

---

## Summary

| # | Artifact | Verdict |
|---|----------|---------|
| 1 | `public/infographics/inside-the-90-agent-company.html` | **APPROVE** (one brand-token exception noted; not blocking) |
| 2 | `public/infographics/open-source-stack.html` | **FIX → re-render** (mobile horizontal overflow 394 px; same brand-token exception) |
| 3 | `public/visuals/graduated-autonomy-ladder.html` | **APPROVE** |

---

## Probe results

Run: `node .agents/skills/ls-artifact-qa/scripts/visual_check.cjs <path> --viewport 1280x800 --viewport 375x667`

| Check | 90-agent 1280 | 90-agent 375 | OSS 1280 | OSS 375 | Ladder 1280 | Ladder 375 |
|-------|---------------|--------------|----------|---------|-------------|------------|
| horizontalOverflowPx | 0 | 0 | 0 | **394** | 0 | 0 |
| missingAltCount | 0 | 0 | 0 | 0 | 0 | 0 |
| emptyHeadingCount | 0 | 0 | 0 | 0 | 0 | 0 |
| untypedImageCount | 0 | 0 | 0 | 0 | 0 | 0 |
| decorativeWithAltCount | 0 | 0 | 0 | 0 | 0 | 0 |
| informativeMissingAltCount | 0 | 0 | 0 | 0 | 0 | 0 |
| altQualityFailures | 0 | 0 | 0 | 0 | 0 | 0 |
| logoAltMismatchCount | 0 | 0 | 0 | 0 | 0 | 0 |
| imgCount / headingCount | 1 / 6 | 1 / 6 | 1 / 13 | 1 / 13 | 1 / 15 | 1 / 15 |
| scrollHeight | 3258 | 5997 | 5994 | 14261 | 4386 | 8616 |

Artifacts: `_probe-90agent-{1280x800,375x667}.png`, `_probe-oss-*.png`, `_probe-ladder-*.png`, matching `.json` files, same directory.

Logo: all three reference `/logo-full-v2.svg` (exists), `data-ls-image-type="brand-mark"`, first instance `alt="LightSpeed Holdings Limited"`. Probe: `logoAltMismatchCount: 0`.

---

## Artifact 1: Inside the 90-Agent Company

`public/infographics/inside-the-90-agent-company.html` (647 lines, 38,866 bytes)

### Visual QA
- Desktop: single-column navy narrative with white stat cards; clear numbered section rhythm (1–5); red section rules on brand; readable type scale.
- Mobile 375: stacks cleanly; SVG topology and governance panels scroll horizontally inside `.svg-scroll` (document overflow 0); scroll-hint shown ≤1023 px.
- Cyan dot matrix (agent layer) reads as intentional schematic; caption correctly says "not a reporting-line org chart."
- Minor: desktop governance SVG "T4 · CEO Only" sublabel is tight against the red gate border at 1280. Legible, not clipped.

### Brand QA
- Declared tokens: navy `#070A40`, red `#E63946`, cyan `#00BFFF`, morning-mist, deep-mineral, grey-light, grey-dark, white, grey-light-text. They match `brand-tokens.json`.
- **Exception:** line 279 `h1 .accent, .tagline, footer .foot-tag { color: #0077A8; }` is **off-palette**. It is not in `brand-tokens.json`. Contrast of `#0077A8` on white is approximately **5.0:1**, which passes WCAG AA normal text. `#00BFFF` on white would fail at roughly 1.7:1, so `#0077A8` appears to be a deliberate darkened cyan for light surfaces. Recommend adding it as a named token (for example `cyan-text`) rather than a one-off hex, or obtaining brand sign-off to keep the literal.
- Tagline "ASPIRE. ACT. ACHIEVE." is present in header and footer; logo min-size is not violated (renders above the 120 px full-logo floor on desktop).

### UX QA
- Section numbering (1–5) and "Source:" lines under every stat support scanning.
- Scroll-hint pattern (`aria-hidden`, shown only on narrow viewports) is correct and matches ladder/OSS.
- Honest-status panel is visually distinct (red left border) and hard to miss. Good trust design.
- No interactive controls beyond the logo link; no dead CTAs.

### Accessibility QA
- Landmarks: `<header>`, `<main>`, `<footer>`; sections use `aria-labelledby`.
- SVGs: `role="img"` with `<title>`/`<desc>` via `aria-labelledby`.
- Lists: `role="list"` / `listitem` on tools and CI gates; `aria-label` on the tools list.
- Headings: 6 total, none empty; hierarchy h1 → h2 per section holds.
- **Gap (non-blocking):** no `:focus-visible` style and no `prefers-reduced-motion` block. No animations are present, so reduced-motion is moot; focus style only matters for the logo link, so add it for parity with ladder.

### Content QA
- "90 agents / 89 AI + 1 Human CEO / 20 departments": **verified**. `company-registry.yaml` has 90 `id` entries and 20 unique departments (AI Research … Technology).
- HITL tiers are named T0–T4 with the five implementers; this matches pillar 01 and in-repo tier_rules references.
- The SHA-256 chain is described as an implementation fact with code paths (`__seq` / `__prev_hash`); it is hedged in the honest-status panel ("proven in-house"; "no client deployment is claimed").
- "Not yet deployed to paying clients" matches the canonical fact (no paid client deliveries).
- The 2,373 regression tests are correctly **dated** (2026-09-10, `pytest --collect-only`) and are not presented as live.
- No SADC adoption claim on this artifact.

### Verdict: APPROVE
Ship. Optionally fold `#0077A8` into brand tokens in a follow-up; this is not a re-render blocker.

---

## Artifact 2: The Open-Source Stack Behind a 90-Agent Company

`public/infographics/open-source-stack.html` (760 lines / 809 with trailing, 41,807 bytes)

### Visual QA
- Desktop: strong 5-panel structure (thesis stats → stack table → cost logic → honest status → provenance); the dark "external market anchor" callout is well differentiated.
- **Mobile FAIL:** `horizontalOverflowPx: 394` at 375×667 (`scrollWidth` 769). Full-page screenshot shows content laid out in the left ~375 px with a blank white gutter to the right for the entire page height.
- **Root cause (two compounding issues):**
  1. **Table mobile escape.** `@media (max-width: 760px)` sets `.table-wrap { overflow-x: visible }` (line 420) while converting `table.stack` to stacked cards. Long unbroken path strings in cells (for example `src/ai_company/llm/providers/{openai_compatible,ollama,llamacpp,base}.py`) expand cells past the viewport, and `overflow-x: visible` lets that expansion become document-level overflow. Desktop is fine: `table-wrap` keeps `overflow-x: auto` and `min-width: 720px` scrolls inside the page.
  2. **SVG min-width never reset on screen.** `.svg-scroll svg { min-width: 920px }` (line 164) is reset only inside `@media print` (lines 167–169), not on mobile. The router diagram is correctly wrapped in `.svg-scroll { overflow-x: auto; max-width: 100% }`, so alone it should scroll internally. Combined with issue (1) widening the document, the diagram sits in the widened layout and the gutter becomes visible. Artifact 1 and ladder share the same `.svg-scroll` pattern and pass mobile, so the table-escape is the differentiator.
- Desktop table and SVG scroll containers behave correctly.

### Brand QA
- Token set in `:root` matches `brand-tokens.json`.
- **Exception:** line 469 has the same `#0077A8` rule as artifact 1 (`h1 .accent`, `.tagline`, `footer .foot-tag`). It is off-palette; the same AA-passing darkened cyan. Same recommendation applies.
- Header/footer, tagline, logo instance handling: compliant.

### UX QA
- Cost-logic cards use "mechanism, not measurement" framing consistently; the ban-list of non-asserted numbers is a distinctive honesty device.
- Scroll-hint is present for the router SVG.
- **Mobile UX is broken by the overflow.** Horizontal page scroll on a phone with a mostly empty gutter reads as a defect, not a diagram affordance.
- The external-anchor caveat block is long but scannable; fine on desktop.

### Accessibility QA
- Landmarks and `aria-labelledby` sections are present (13 headings, none empty).
- Router SVG: `role="img"`, rich `<desc>`.
- Logo: first-instance alt is correct; probe is clean on alt/heading/logo.
- **Gaps:** no `:focus-visible` styles (logo link); no `prefers-reduced-motion` (no motion to gate); the mobile overflow is itself an accessibility/usability defect, since it forces horizontal scroll of the whole page.

### Content QA
- **Versions verified against repo:**
  - Pydantic ≥2.8 → `pyproject.toml` `"pydantic>=2.8"` ✓
  - Python ≥3.12 ✓
  - Vite 6.1 / React 18.3 / Tailwind CSS 4.0 → `package.json` `vite ^6.1.0`, `react ^18.3.1`, `tailwindcss ^4.0.0` ✓
  - FastAPI, Typer, uvicorn, Jinja2 are declared without invented versions ✓
- uv.lock "0 license fields" and package-lock "292 license fields" are presented as dated repo observations with paths, consistent with the evidence policy (verifiable, not inflated).
- Honest status: "Savings percentages are not claimed — there are no measured client deployments yet." This matches the canonical no-paid-deliveries fact.
- MODEL_COSTS is correctly labelled as a "dated pricing ledger, not billing evidence."
- The ban-list includes "SADC readiness or AU strategy framing — proposal status only", which is the correct hedge (the framework is a proposal, not adopted).
- Third-party price anchors (Groq $0.075/M input, etc.) carry vendor/tracker caveats and fetch dates, which is acceptable for thought leadership with the stated caveats.
- J&S StopOver Bar is not claimed as a paid client on this page (the case pipeline is explicitly "not a revenue claim").

### Verdict: FIX → re-render
Do not ship to mobile channels until the overflow is fixed. Re-render after the CSS changes below. Desktop-only embeds could ship earlier if needed, but one artifact should pass both viewports.

**Specific fix instructions (re-render checklist):**

1. **Contain table cells on mobile** (primary fix). In the `@media (max-width: 760px)` block (~line 417):
   - Keep the stacked-card conversion, **or** revert to a horizontally scrollable table. Do not use `overflow-x: visible` on `.table-wrap` while cells can grow.
   - If keeping stacked cards: add to `table.stack tbody td` (and `.path` / `code` inside cells):
     - `overflow-wrap: anywhere;` (or `word-break: break-word` as fallback)
     - change `td::before { flex: 0 0 40% }` to `flex: 0 0 38%; min-width: 0;` and ensure the value span can shrink (`min-width: 0` on the flex child).
   - Preferred simpler alternative: delete the `.table-wrap { overflow-x: visible }` and `table.stack { min-width: 0 }` overrides. Leave the desktop scroll-container pattern (`overflow-x: auto; max-width: 100%`) active at all widths so the 720 px table scrolls inside its box on phones.
2. **Reset SVG min-width on screen, not only print.** After line 166, add:
   ```css
   @media (max-width: 1023px) {
     .scroll-hint { display: block; }
     .svg-scroll svg { min-width: 0; }
   }
   ```
   (Merge with the existing `@media (max-width: 1023px)` rule; keep the `@media print` reset.)
3. **Brand token (optional in the same pass):** replace `#0077A8` with a token reference once it is added to `brand-tokens.json`, or leave it and track it with the brand owner.
4. **Parity (optional):** add ladder's `:focus-visible` outline rule for the logo link.
5. **Re-verify:** re-run `visual_check.cjs` at 1280x800 and 375x667; require `horizontalOverflowPx === 0` at both; confirm the table remains readable (stacked cards or in-box scroll).

---

## Artifact 3: The Graduated Autonomy Ladder

`public/visuals/graduated-autonomy-ladder.html` (573 lines, 30,683 bytes)

### Visual QA
- Desktop and mobile are both clean; document overflow is 0 at both viewports.
- The ladder SVG (4 rungs + red autonomy ceiling) is the focal point and reads correctly; the color logic line (cyan base → navy rising → red ceiling) matches the fills.
- The evidence ladder strip ("PROPOSED — this document" highlighted) is a strong honesty visual.
- The two-taxonomy panel (SADC draft Tiers 1–4 vs LightSpeed HITL T0–4) is visually separated and correctly not conflated.

### Brand QA
- All declared hex values are brand tokens (`#070A40`, `#E63946`, `#00BFFF`, greys/white). There is **no `#0077A8`** on this artifact.
- Tagline, logo first-instance alt, footer lockup: compliant.
- The CTA button uses red on white, which is on-brand.

### UX QA
- The reservations panel (four skeptic objections) maps to sales/playbook use; each card has "THE ANSWER" plus its source path.
- The CTA "Stress-test this draft with us" is a single clear action; its link target is the site root, which is acceptable for a public one-pager.
- Scroll-hint on the ladder SVG at ≤759 px.
- Mobile: reservations and controls grids collapse to one column without overflow.

### Accessibility QA
- Best of the three: `:focus-visible` on the logo link (line 53) and the CTA (line 314); SVG `role="img"` with title/desc; sections labelled; 15 headings, none empty; list roles on reservations/controls/evidence strip.
- Evidence strip future rungs are correctly `aria-hidden="true"`, so they are non-informational for AT until real.
- No motion to gate; no reduced-motion block needed.

### Content QA
- **Honest status banner (top):** "Policy proposal by LightSpeed Holdings' CEO. Not adopted by SADC or any government. No paid client deployments yet." This is **exactly correct** per the canonical facts.
- Four-tier framing is the **SADC policy taxonomy**, not LightSpeed's ops model. The artifact explicitly distinguishes the operational HITL T0–T4 (5 tiers) in panel 4, so there is no confusion with the 5-tier HITL canonical fact.
- Rung names/controls are claimed "quoted verbatim" from `docs/Pharos/policy-drafts/sadc-agentic-ai-governance-framework.md` with § anchors, which is a verifiable provenance pattern.
- No paid-client, adoption, or measured-savings overclaim was found.
- "No number, statistic, adoption claim, or client claim appears on this page without a source or a hedge." This holds under inspection.

### Verdict: APPROVE
Ship. No re-render required.

---

## Palette-antialiasing conclusion (artifact 1 prior pixel check)

**Prior observation:** ~5.44% exact brand-color pixel coverage on `inside-the-90-agent-company.html`.

**Independent conclusion:** the low exact-hex coverage is **antialiasing and edge blending, not an off-palette design.**

Basis:
1. **Declared colors are brand tokens.** Every `#hex` in CSS/SVG on artifact 1 is a `brand-tokens.json` value except the single light-surface text rule `#0077A8`, which is used for accent text on white and not for large fills or the dot matrix.
2. **High-edge-density content.** The agent-layer diagram is an 89-dot cyan matrix plus borders, rules, and large body text. Subpixel/gray antialiasing at every glyph and shape edge converts exact `#00BFFF`/`#070A40`/`#E63946` pixels into intermediate values that a strict equality pixel count will not match.
3. **No large off-palette fills.** Backgrounds and cards use `--navy`, `--white`, `--morning-mist`, `--grey-light` exactly. A wrong-palette redesign would show up as large contiguous non-token regions, which the screenshots do not show.
4. **`#0077A8` is text-only.** Its footprint is a few dozen heading/tagline glyphs, which is far too small to explain a multi-percent coverage gap. It is a separate, documented brand exception, not the antialiasing story.

**Action:** no palette rework is required for the 5.44% figure. Track `#0077A8` as a tokenization/brand-sign-off item (artifacts 1 and 2 only).

---

## Cross-artifact recommendations (non-blocking)

1. Add `:focus-visible` logo-link styling to artifacts 1 and 2 (copy the ladder lines 53 pattern).
2. Tokenize `#0077A8` as `cyan-text` (or an equivalent) in `brand-tokens.json` and reference it from artifacts 1–2; re-run brand QA after.
3. Share one mobile SVG/table containment snippet across the three generators/templates so the OSS overflow cannot regress: `.svg-scroll svg { min-width: 0 }` under `max-width: 1023px`, and never `overflow-x: visible` on wide tables.

---

## Fix-pass gate (artifact 2 only)

Re-render `open-source-stack.html` with the three CSS changes in its FIX section, then re-run:

```powershell
node .agents/skills/ls-artifact-qa/scripts/visual_check.cjs "public\infographics\open-source-stack.html" --viewport 1280x800 --viewport 375x667 --out docs/Pharos/qa/_probe-oss.png --json docs/Pharos/qa/_probe-oss.json
```

Accept only when `horizontalOverflowPx === 0` at both viewports and all other probe counters stay 0.
