# Research: Immersive 3D Website for LightSpeed Holdings

> **Status:** Research only — no build decision made, no code changed.
> **Date:** 2026-09-26
> **Benchmarks:** igloo.inc, videinfra.com, lusion.co
> **Method:** Four parallel research streams (see §1), synthesized here.

---

## 1. Research Team & Method

| Agent (roster type) | Stream | Output |
|---|---|---|
| `agentic-research-lead` | Benchmark teardown of igloo.inc / videinfra.com / lusion.co — visual language, signature interactions, tech stacks, STEAL/AVOID | §2, §3 |
| `lead-frontend` | Technical approach: rendering layer, scroll/motion, assets, performance, a11y/SEO, QA — against the actual repo state | §4, §5 |
| `product-designer` | Immersive UX patterns, brand translation (ADR-020 constraints), IA + section narrative, fallback ladder | §6, §7 |
| `cmo` | Strategic case: audience fit, risks, phased recommendation, metrics | §8, §9 |

All streams were dispatched in parallel with no shared state; each was research-only (no file edits). Findings are synthesized below; conflicts between streams are called out explicitly in §10.

---

## 2. Executive Summary

**Bottom line (convergent across all four streams): the full igloo/lusion-class immersive flagship is not the right move today. The recommended path is phased:**

1. **Phase 0 (now):** CSS-first "constrained immersion" on the existing Vite React SPA + SEO/perf fundamentals. No WebGL.
2. **Phase 1 (60–120 days):** Exactly **one** substantive, progressive-enhanced WebGL moment (e.g. an interactive 90-agent org / HITL governance explorer) that doubles as a proof artifact — never decorative, never on conversion paths.
3. **Phase 2 (triggered):** Full scroll-driven 3D homepage, only when 2–3 published client case studies exist **and** a separate budget/awards push is explicitly approved.

**Why:** LightSpeed's #1 market wedge is "designed for low-bandwidth reality" (offline-first, WhatsApp-native). Africa averages **$3.51/GB** mobile data (5.4× global average). A multi-MB WebGL showcase would refute our own claim on the exact device the buyer judges us from. The benchmarks sell *craft as their product*; we sell *proof under constraint*. Separately, hard governance blockers already exist in-repo (§10.1).

**The one-line synthesis of the benchmarks:** ship **Vide Infra's architecture** (server-rendered HTML, declarative motion vocabulary, sticky numbered chapters, one WebGL band, pre-planned device-tier quality), arm it with **Lusion's interaction grammar** (preloader ritual, DOM-mapped 3D island, extreme display type, one accent per section), and spend **Igloo's craft budget on exactly one procedural system** — generated per-venture/agent shards — instead of a whole-site WebGL rewrite.

---

## 3. Benchmark Teardown (Stream 1)

### 3.1 igloo.inc — the ceiling of corporate-page craft

- Parent of Pudgy Penguins/OverpassIP; three-section scroll narrative by studio **Abeto (Vicente Lucendo)** + Bureaux. Awwwards **SOTY + Developer SOTY 2024**, Webby 2026 Winner (Best Visual Design).
- **Stack:** Three.js, three-mesh-bvh, Svelte, GSAP, Vite; Houdini/Blender for 3D; custom VDB→browser volume exporter.
- **Signature techniques:** procedural crystal-growth enclosures unique per project (scales with zero manual modelling); interactive particle footer with velocity-driven colour; SDF text in WebGL (avoids DOM relayout); in-engine real-time intro (no offline render); staged texture loading + background shader compilation; continuous low-end-device perf measurement during dev.
- **STEAL:** procedural content generation as a brand system (→ per-venture/agent "shards"); staged asset pipeline discipline; one hero idea carried through 3 sections; parameter-driven colour in data visuals; browser-based authoring loop.
- **AVOID:** empty `<body>` SPA (fatal for a firm whose product is published research); glitch/scramble type + frost-dissolve (reads crypto); autoplay audio; spectacle-to-copy ratio; no documented mobile design (riskiest of the three for mobile-first SADC).
- **Confidence note:** refs.gallery-only claims (KTX2, `prefers-reduced-motion`, WCAG AA, LCP ≈1s) are **unverified — do not cite**.

### 3.2 videinfra.com — the architecture a B2B site should ship

- London agency, 29 Awwwards / 31 CSSDA / 9 FWA; clients incl. British Airways, airBaltic. **Light, clean, minimal** — mostly disciplined SSR HTML with surgical WebGL.
- **What's actually in the HTML:** noscript path, `srcset` + placeholder lazy images, consent-denied-by-default analytics, `data-plugin` motion vocabulary (`reveal`, `parallax-clamp`, `preloader`, `cursor`), virtual-scroll sections, Barba.js transitions, numbered sticky chapters (01/02/03), giant inline SVG wordmark, `leading-trim` typography — and **one** WebGL band (awards canvas syncing fake DOM tiles into a WebGL zoom).
- **Nearest-industry precedent:** [AI in banking UX-design](https://videinfra.com/work/ai-in-banking-ux-design) — one-scroll WebGL narrative, mobile-optimized, SOTD/CSSDA/FWA.
- **Device doctrine (Madar interview):** WebGL mobile adaptation ≈ normal front-end effort *because* custom code, no page builders; **pre-planned reduced-quality tier** for low-power devices (drop reflections/soft light) — planned up front, not bolted on. AIR's mobile "was a separate design challenge, not a scaled-down site."
- **STEAL:** the architecture (SSR + declarative motion + sticky chapters + one WebGL moment); intro-overlay preloader (CSS, cheap); numbered counters for a "01 Research / 02 Build / 03 Venture" narrative; the **configurator pattern** (AIR multi-select office merge → engagement/venture explorer); device-tier quality scaling; consent-gated analytics + noscript.
- **AVOID:** luxury "mastership" tonality (we need quantified proof instead); legacy Symfony/Twig stack (copy the motion vocabulary, not the build system); third-party video embed (supply-chain + bandwidth); portfolio-card density (our primary content type is research artifacts).

### 3.3 lusion.co — the interaction grammar, and the performance debt to refuse

- Bristol studio (Edan Kwan); clients Coca-Cola, Porsche, Google, Cognition AI; **SOTY from Awwwards + FWA + CSSDA**. High-contrast monochrome (#F0F1FA on #000) with one saturated accent (#1A2FFB).
- **Stack:** Astro static shell + hoisted **1.25MB monolithic ESM bundle** (Three.js r158, postprocessing/SMAA, custom Tween, framer-motion 11); baked-simulation doctrine (Houdini cloth → 220KB gzip ArrayBuffer; vertex animation textures **983KB desktop / 246KB mobile** via 4096→1024 vertex tiering).
- **Signature techniques:** single persistent canvas behind DOM with **pixel-perfect DOM↔3D coordinate mapping**; "starts as a normal site, then reveals it's 3D" pacing; preloader ritual (mark + percentage counter); Rapier physics toy with stencil-buffer masking; fluid cursor follower; one display sans at up to 144px.
- **Mobile:** input-modality **swap** (accelerometer/tilt) rather than layout shrink — steal the *principle*, substitute scroll/tap. Counter-evidence: at v3 launch "the scroll jack on mobile is super frustrating" was the top user complaint → **no scroll-jacking on mobile, ever**.
- **Performance reality (independent measurement, Jul 2025):** **18.9MB total transfer, ~10s load (34s throttled 3G), CLS 0.59 (poor), INP 290ms.** Treat as the hard budget ceiling of what to refuse.
- **STEAL:** two-layer architecture (real HTML for everything readable + one canvas for atmosphere); preloader ritual; extreme display type discipline (few sizes, huge jumps, tight leading); accent-per-section (our cyan ≈ their blue; red reserved for CTA/errors); Labs-as-content (`exp-*` monthly experiments → mirrors Pharos research drops); baked/offline simulation principle; device-tiered assets as standard practice.
- **AVOID:** pure black base (our brand base is navy #070A40); 18.9MB payload / CLS 0.59; 1.25MB single bundle; mobile scroll-jacking; physics toys + satire drops (showreel); cursor-only interactions (meaningless where SADC traffic lives).

---

## 4. Pattern Library — the immersion checklist (Stream 1)

✅ = evidenced on ≥1 benchmark.

**Entry & narrative:** preloader ritual (logo + counter) [Lusion, Vide Infra]; in-engine intro sequence [Igloo]; CSS intro-overlay curtain [Vide Infra]; page transitions (Barba) [Vide Infra]; sticky numbered chapters + counters [Vide Infra]; scroll-linked camera / scene drift [all three].

**Scroll mechanics:** virtual/lerped scroll sections [Vide Infra]; parallax with clamp + section-in/out [Vide Infra]; staggered reveal vocabulary with per-element delay/distance [Vide Infra]; 2D→3D→2D transitions as narrative device [Lusion]; ⛔ **no scroll-jacking on mobile** [Lusion user backlash].

**WebGL/3D:** single persistent canvas behind DOM [Lusion, Igloo]; DOM↔3D coordinate mapping [Lusion]; DOM-to-WebGL sync for UI panels [Vide Infra awards band]; procedural/parametric geometry per item [Igloo, Lusion]; particle colour-by-velocity [Igloo]; physics + stencil masking [Lusion]; baked simulation assets (Houdini/VDB → compact buffers) [Igloo, Lusion]; post-processing (chromatic aberration, bloom, SMAA) [Igloo, Lusion]; **selective WebGL — one band on an otherwise HTML site** [Vide Infra].

**Motion & micro-interaction:** magnetic/clone-swap buttons [Vide Infra]; hover video previews in menus [Vide Infra]; reactive/fluid cursor [Lusion, Vide Infra]; giant inline SVG wordmark [Vide Infra]; `leading-trim` display type [Vide Infra]; showreel video instead of WebGL [Vide Infra].

**Performance & ops:** background shader compile + deferred textures [Igloo]; compressed/baked assets + instancing [Lusion]; **device-tier quality scaling, pre-planned** [Vide Infra, Lusion]; input-modality swap by device [Lusion]; noscript + deferred images [Vide Infra]; consent-denied-by-default analytics [Vide Infra]; continuous perf testing during dev [Igloo, Lusion]. ⚠️ Counter-evidence to plan against: Lusion's own 18.9MB / CLS 0.59 / 34s-on-3G.

**Transfer test (enterprise-trust vs showreel):** maps cleanly → HTML-first + one WebGL moment, DOM-mapped 3D island, sticky numbered chapters, procedural per-venture shards, staged loading, device-tier scaling, configurator-as-sales-tool, preloader ≤1.2s skippable, reveal data-attributes, giant wordmark, labs-as-content, consent/reduced-motion hygiene. Quarantine → SDF glitch/scramble type, physics toys, autoplay sound, near-black monochrome + satire, cyberpunk transitions, heavy payloads, mobile scroll-jacking, luxury poetry.

---

## 5. Technical Approach (Stream 2)

### 5.1 Repo reality check (verified 2026-09-26)

- Commit `30d268d` ("simplify website — remove 33 pages and components, drop unused deps") **removed `three`, `@react-three/*`, `@types/three`, `framer-motion`, `@playwright/test`**. This is a **greenfield 3D decision on a deliberately slimmed SPA**, not an upgrade.
- Current runtime deps: react 18.3.1, react-router-dom 7, clsx, tailwind-merge, lucide-react, @vercel/blob. Dev: tailwindcss 4, vite 6, vitest 5, typescript 5.7.
- **No code splitting today:** one JS chunk (`index-*.js`, **413.7 KB**) for all 11 routes; `App.tsx` statically imports every route.
- **Broken QA tooling:** `ls-artifact-qa`'s `scripts/visual_check.js` requires Playwright, but Playwright is absent from `package.json`/`bun.lock` (only an extraneous `node_modules` leftover). A clean install breaks the gate.

### 5.2 Key constraint: React 19 is a prerequisite for R3F v9

`@react-three/fiber@9` peers on react `>=19 <19.4`; `fiber@8` (react 18 line) is the **EOL major** — do not start new work on it. Viable paths: **(A)** React 19 upgrade → R3F v9 + drei; **(B)** raw `three` (0.186) in a lazy chunk, no React upgrade; **(C)** no WebGL at all — CSS scroll-driven + SVG/canvas 2D.

### 5.3 Recommended stack

| Layer | Choice | Rationale | Rejected / why |
|---|---|---|---|
| v1 baseline | CSS scroll-driven (`animation-timeline` behind `@supports`) + SVG + Tailwind 4, existing `useSmoothScroll` + reduced-motion CSS | ~0 KB; passes MASTER_SPEC §25 untouched | re-adding `motion` — deliberately removed in `30d268d` |
| Escalation renderer | `three` 0.186.x in a lazily-imported chunk | No React upgrade needed; WebGL2 baseline | `fiber@8` — EOL major |
| Component 3D (phase 2) | React 19 → `@react-three/fiber@9` + drei | Only supported line; declarative scenes, disposal handled | R3F on React 18 |
| WebGPU | Not for v1 | Production-ready at r171 but second renderer path; WebGL2 fallback still required | WebGPU-only |
| Scroll orchestration | GSAP 3.15 + ScrollTrigger + Lenis (free since Webflow acquisition) | Only sane way to pin + scrub a camera to scroll; integrate via `gsap.ticker` (`autoRaf={false}`) | CSS-only can't pin/scrub — but do use CSS for simple reveals |
| Assets | glTF/GLB + **Meshopt** + KTX2/BasisU via `gltf-transform`/`gltfpack` | Meshopt wins time-to-first-frame; KTX2 keeps GPU memory ~¼ | Draco: smaller transfer but slower decode + bigger decoder |
| Code splitting | `manualChunks` (three / motion / react / icons) + `React.lazy` per route | **Prerequisite** — today: one 413.7 KB chunk | Vite defaults insufficient once three enters the graph |
| SEO | `@prerenderer/rollup-plugin` + puppeteer, `domcontentloaded` + explicit waitTime (3D routes never hit `networkidle0`) | Only lever under the Vercel `/(.*)→/index.html` rewrite | Next/Astro migration — whole-framework rewrite |
| QA | Re-add `@playwright/test`; canvas **element-screenshot lit-pixel assertions** (≥1% lit) | Works without `preserveDrawingBuffer` | `canvas.toDataURL()` readbacks — blank-buffer ambiguity |

### 5.4 Performance budgets & device tiering

- **GPU-memory trap:** a 2048² RGBA texture = ~16 MB GPU (22 MB with mips) *from a 2 MB JPEG*; KTX2 stays ~¼ size in GPU memory. Mobile texture budget: 128 MB.
- Marketing-site targets: hero scene (JS+assets) ≤ 800 KB–1.5 MB; GLB phase ≤900 ms/~2 MB ceiling; first paint on 4G < 2 s. CI gates: non-3D route initial JS ≤120 KB gz, 3D route ≤250 KB gz, 3D LCP (mobile 4G) ≤2.5 s.
- **Tier function** (`src/three/tiers.ts`): `'none' | 'lite' | 'full'` from WebGL2 support, `prefers-reduced-motion`, `pointer: coarse`, `deviceMemory ≤4`, `connection effectiveType`. **Mount gates in order:** tier ≠ none → in view (IntersectionObserver) → `requestIdleCallback` → `import()`. Any failure → theme-aware static poster.
- Render hygiene: `frameloop="demand"` when off-screen/reduced; pause on `visibilitychange`; dispose geometry/materials/textures on unmount.
- Loader gotchas: wire DRACO/KTX2/Meshopt decoders explicitly (silent-failure prone); `KTX2Loader.detectSupport(renderer)` against the live renderer; content-hash GLB filenames + immutable cache.

### 5.5 A11y & SEO rules for a WebGL layer

- Canvas is **decorative**: `aria-hidden="true"`; all real content/CTAs live in the DOM. Never `display:none` the HTML fallback (kills a11y tree + keyboard).
- Text over canvas ≥4.5:1 (navy scrim), graphical controls ≥3:1; ≤3 flashes/sec.
- `prefers-reduced-motion` honored at init *and* on change → tier `none` → static poster.
- Scene lighting/background must respond to the existing `.dark` theme toggle or the canvas breaks in one mode.
- SEO gaps to fix regardless of 3D: missing `og:image`, `og:url`, `twitter:card`, `canonical`, JSON-LD; prerender critical routes; raw-HTML content completeness via GSC URL Inspection.

### 5.6 Proposed integration sketch

```
src/
├── three/            # NEW — isolated, lazy-only, never in root chunk
│   ├── tiers.ts      # getTier(): 'none'|'lite'|'full'   (pure, jsdom-testable)
│   ├── mountGate.ts  # tier → IntersectionObserver → requestIdleCallback → import()
│   ├── Scene.tsx     # raw-three or R3F wrapper; frameloop="demand"; loaders wired here
│   ├── CameraRig.tsx # scroll → camera via ScrollTrigger
│   ├── materials.ts  # reads brand/tokens ONLY — no hex literals; watches .dark
│   └── poster/       # static fallbacks per tier + theme
├── components/ImmersiveStage.tsx  # DOM layer ALWAYS renders; canvas mounts behind
└── App.tsx           # React.lazy per route + <Suspense>
```

---

## 6. Design / UX Direction (Stream 3)

### 6.1 Guiding architecture

**3D is the stage; DOM is the content.** Exactly three 3D moments on the homepage — hero (post-LCP canvas boot), AI Company Builder spotlight (the *one* pinned section, authored camera flight, never free orbit), optional 90-agent node-constellation (degradable to existing cards with zero layout shift). Interior routes stay `[static]` or `[DOM+motion]` — `/contact`, privacy, terms, insights must be instant. Metaphor: **the governed operations deck** — one continuous navy space; cyan = live/active, red = action/proof.

### 6.2 Brand translation (ADR-020 locked — no token edits)

Navy `#070A40` = canvas/floor (~90%+ of pixels); white = ink; cyan `#00BFFF` = the *single* "active system" glow (links, live data, focus); red `#E63946` = CTA and proof only; greys = muted ink + grid lines. This is the 80/10/10 rule as lighting: darkness at 90–95% depth so accents glow; max 2–3 glow hues; no glow on body text; scrim behind any text over the scene; grain off on small viewports; slow ambient motion by default, all off under reduced-motion.

### 6.3 Fallback ladder (every tier a designed state, identical content/CTAs)

| Tier | Trigger | Renders |
|---|---|---|
| T0 Full | Desktop, fine pointer, WebGL2, no reduced-motion, FPS ≥55 | Hero + spotlight 3D, authored camera flight, DPR ≤2 |
| T1 Reduced | coarse pointer / FPS watchdog (frame >20ms ×30, hysteresis) | Same content, cheaper scene: DPR ≤1.5, no post-processing, baked shadows, low particles |
| T2 Static-stage | No WebGL / saveData / low deviceMemory / sustained jank | CSS-only hero (navy gradient + grid + cyan glow), same DOM overlay + CTA, zero canvas bytes |
| T3 No-motion | `prefers-reduced-motion` (init + change); manual toggle offered | No pinning, no count-up/drift/parallax; scene renders once as a still or not at all |
| T4 No-JS / AT | JS off, screen reader, keyboard | Full HTML: all copy/links/badges/CTAs; canvas `aria-hidden`; `aria-live` mirrors scene state |

**Performance rules:** paint the outcome (headline + CTA) first; **WebGL must never be the LCP element**; LCP ≤2.5s mobile, FCP ≤1.5s, CLS ≤0.1 (3D never reflows content); pause render loop off-screen; no preloader gating content >1s.

### 6.4 Hard Do / Don't

**Do:** boot canvas after LCP; author the camera path (deterministic, scroll-driven, interruptible); content in DOM at every tier; `aria-hidden` canvas + parallel focusable layer; scrim for contrast; measure on a 3-year-old mid-range Android; cap DPR; pin at most one section; keep conversion routes static.
**Don't:** WebGL as LCP; free orbit-controls on a marketing site; scroll-hijack/dead-scroll frames; >1s preloader; `display:none` on HTML fallback; essential info only in the scene; strobing; `outline:none` without replacement; glow on body text; rebuild routes/framework (ADR-020: migrate in place).

---

## 7. Proposed Section Narrative (Stream 3)

| # | Section | Tag | Treatment |
|---|---|---|---|
| 1 | Hero | **[3D scene]** + DOM overlay | Static/CSS paints first (LCP); canvas boots after: navy volumetric field, 4px-grid plane, low-count cyan drift. Headline/CTA = DOM, scrimmed. |
| 2 | Thesis (4 cols + North Star) | DOM+motion | Existing cards, Reveal-on-enter; hairline cyan hover edge. |
| 3 | AI Company Builder spotlight | **[3D scene — the one pinned section]** | Dashboard rendered as a lit object (eclipse-horizon + beam); authored scroll camera; readable if scrolled fast. |
| 4 | Solutions (6 domains) | DOM+motion | Card grid; honesty badges carry the color story. |
| 5 | 90-agent workforce | **[3D enhancement over cards]** or DOM | Node constellation in cyan/red; degradable to numeric cards, zero CLS. |
| 6 | Sectors (7) | DOM+motion | Card grid + HonestyBadge. |
| 7 | Proof band (4 metrics) | DOM+motion | Count-up (final value in markup); red proof pill. |
| 8 | Insights | static | Typography + hover; crawlable. |
| 9 | About | static | As-is. |
| 10 | CtaBand | DOM+motion | Red CTA; single cyan light-line resolves toward it. |

Interior routes: `[static]`/`[DOM+motion]` only. Same routes, same DOM content, same honesty labeling — the immersive layer is a **skin over the existing IA**.

---

## 8. Strategy & Audience Fit (Stream 4)

### 8.1 Recommendation: PHASED

| Phase | What | Trigger / gate |
|---|---|---|
| **0 — Now (0–60d)** | No WebGL. Double down on existing CSS system (HeroMist, Reveal, ripple, smooth scroll) + SEO fundamentals (raw-HTML content, metadata, structured data) + page-weight budget. | Immediately; exit gate: Core Web Vitals green on mobile p75; 100% target pages return full content in raw HTML (GSC URL Inspection). |
| **1 — Constrained immersion (60–120d)** | **One** substantive progressive-enhanced WebGL moment: interactive 90-agent org / 5-tier HITL governance explorer on `/technology` or `/sectors`. Static HTML underneath; canvas skipped on Save-Data/low-GPU; lazy after interaction; ≤150 KB gz. **Never** on `/`, `/contact`, pricing, or any conversion path. | Phase 0 gates pass. Exit gate: conversion non-inferiority, WCAG 2.2 AA, zero indexed-page loss. |
| **2 — Full immersive flagship** | igloo/lusion-class scroll-driven 3D homepage. | Only when (a) 2–3 named published case studies exist, **or** (b) funded campaign/awards push budgeted, **or** (c) audience shifts to global investors — **plus** separate CEO budget approval. |

**Why not BUILD now:** (1) *self-refutation* — a heavy 3D site on metered African data live-demonstrates that our low-bandwidth claim is marketing; (2) *benchmarks aren't analogous buyers* — igloo sells to consumer-crypto communities, lusion sells 3D production itself, videinfra sells craft; our buyers evaluate reliability, audit trails, references; our own competitive scan says "no paying clients delivered yet; proof stack is internal" — immersion can't substitute for missing proof; (3) *cost misaligned* — full 3D sites run $20k–$200k+ (3–10× static), capital better spent on case studies; (4) *the repo already voted* — ThreeCanvas was removed in `30d268d`, Architecture v2 scopes WebGL out, QA-Lead rated it 65/100 with three.js unverifiable by current QA.

**Why not flat rejection:** no African consultancy owns immersive 3D (white space); the awards/press channel is a proven acquisition primitive (igloo = Awwwards SOTY 2024 via a small studio); our own docs argue immersion-as-evidence ("LightSpeed's engineering is visible in the product") — that's the seed of Phase 1.

### 8.2 Audience fit

| Segment | Evaluating | Full 3D effect | Verdict |
|---|---|---|---|
| Enterprises/government/parastatals (Malawi/SADC) | Trust, governance, references, procurement | Cost/risk signal; slow metered-mobile load confirms objection #1 | **Negative** |
| NGOs/DFIs/donors | Credibility, DPA/GDPR, a11y conformance, value for money | Neutral-to-negative (formal a11y requirements) | **Neg/Neutral** |
| Global investors/partners | Category leadership, execution quality | Positive only at flawless quality (poor 3D converts worse than static) | **Conditional (P2 bar)** |
| Press / Awwwards / awards | Novelty, craft, shareability | Strongly positive (igloo playbook) | **Strong positive (P2 trigger)** |
| Technical talent | Engineering ambition, craft culture | Positive — WebGL flagships recruit | **Positive** |
| End beneficiaries (WhatsApp surface) | Never see the site | None | **Irrelevant** |
| AI Company Builder license buyers | "Can I run this?" | Positive only as *interactive product demo*, not ambient decoration | **Positive for P1 shape** |

### 8.3 Risk register (condensed)

| # | Risk | Mitigation |
|---|---|---|
| R1 | SEO degradation (canvas text unindexable; Googlebot doesn't scroll IO-loaded content) | All copy static HTML outside canvas; GSC raw-HTML gate; prerender critical routes |
| R2 | Network cost contradicts our #1 wedge (Africa $3.51/GB; SA median mobile 14 Mbps) | WebGL ≤150 KB gz lazy post-hero; never on Save-Data/2G; text+proof path ≤1 MB / usable ≤5s on 3G |
| R3 | Accessibility/compliance failure (WCAG 1.1.1; WCAG 3.0 expanding to XR; W3C open on WebGL rules) | Semantic HTML canonical; axe 0 critical/serious; keyboard parity; VPAT-style note for procurement |
| R4 | "Style over substance" trust damage (NN/g: motion distracts from task goals; documented case: parallax redesign → bounce +40%, form conversions halved) | Phase 1 only; immersion must *carry information*; never between visitor and pricing/contact |
| R5 | Conversion regression (counter-evidence exists: subtle animated hero → +7% orders) | Non-inferiority test: enquiry conversion must not drop >5% relative; A/B with kill-switch |
| R6 | Cost/maintenance drag pre-revenue ($20k–200k+) | P1 capped scope; P2 needs named trigger + separate budget; QA must prove WebGL verification first |
| R7 | Low-end Android GPU fragmentation | Feature-detect + tier; indistinguishable static fallback; frame-time watchdog unmounts |
| R8 | Opportunity cost vs proof deficit (no paying clients yet) | P2 gated on published case studies; P1 must double as a proof artifact |

### 8.4 Metrics (hypothesis + target + method)

- **Primary:** qualified enquiry rate — non-inferiority (no drop >5% relative), stretch +10% in 90 days; A/B by route, 95% CI, pre-registered decision rule.
- **Performance gates:** LCP ≤2.5s mobile p75 (no regression); CLS <0.1; INP ≤200ms; initial route ≤500 KB; WebGL chunk ≤150 KB gz lazy; 3G+Save-Data path: full text usable ≤5s, ≤1 MB, canvas never loads. Breach → revert to Phase 0 variant.
- **SEO gates:** 100% target routes return full title/meta/H1/body in raw HTML; zero indexed-page loss (30-day GSC window).
- **Accessibility gate:** WCAG 2.2 AA — axe 0 critical/serious + manual NVDA/VoiceOver pass.
- **Engagement (directional only):** scroll depth ≥60% on the P1 explainer page; dwell time explicitly *not* a success criterion.
- **Kill criteria (pre-committed):** any gate fails at P1+14 days, or enquiry rate drops >5% relative with significance → revert, reopen only under a new trigger.

---

## 9. Suggested Sequence (cross-stream)

1. **Hygiene PR** — re-add `@playwright/test`; add `manualChunks`; `React.lazy` per route; gzip budget gate. *(Independent of any 3D decision; fixes real current defects.)*
2. **Governance PR** — ADR seeking the MASTER_SPEC §25 / #303 exception with budgets written in; ADR-020 amendment record (see §10.1).
3. **Phase 0** — SEO fundamentals (prerender, metadata, JSON-LD) + CSS-first polish on the existing system.
4. **Phase 1** — `src/three/` mount-gate scaffolding + poster fallbacks, then one substantive WebGL moment (governance explorer), Meshopt+KTX2, Playwright lit-pixel coverage.
5. **React 19 → R3F v9** — only after step 4 proves the seam is real.

---

## 10. Conflicts, Blockers & Open Questions

### 10.1 Governance blockers discovered (must clear before any build)

1. **MASTER_SPEC §25 + LEGACY_INVENTORY prohibit Three.js/GSAP** — verified: `MASTER_SPEC.md:671` ("Do not add Three.js, GSAP, video, shaders, or other heavy technologies simply because they are available") and `LEGACY_INVENTORY.md:111/154` (ThreeCanvas → **DELETE**, "Three.js is prohibited by MASTER_SPEC §25"). Requires an explicit spec-exception ADR naming the exact moments + budgets, with CTO sign-off, **before** installing anything.
2. **Ticket #303 confinement** — verified: `docs/client-facing/website-compliance-ticket-ledger.md:51` ("ThreeCanvas/WebGL + tactile motif confined to internal diagnostics only (#303)"). Ticket #303 itself is `OPEN (ready-for-agent)`, P2, first wave (`:11`). A public immersive site requires CEO/CMO re-ratification or supersession.
3. **ADR-020** locks palette + "migrate in place, no redesign/new framework." Recommended read: an immersive *skin over existing IA* is compatible, but record it as an amendment rather than assume it. Corroborating: `docs/architecture/adr/034-framework-strategy.md:26` — "evaluate Three.js only if builder UX actually needs WebGL — UX spec currently says **not required** for v2."

> **Stale-doc caveat:** `docs/venture-studio/07-09`, `effects-description.md`, and `TESTING.md` still describe `ThreeCanvas` as a live component (pre-`30d268d` state). `Plan.md:17` lists its site-wide presence as an open VIOLATION of #303. Read the ledger + MASTER_SPEC as authoritative, not the venture-studio effect docs.

### 10.2 Cross-stream conflicts to resolve

- **Scope tension:** CMO says homepage stays out of Phase 1 (conversion paths protected) while product-designer sketches 3 homepage 3D moments. Resolution implied by both: homepage gets *at most* the Builder spotlight in a later phase; Phase 1 ships on `/technology` or `/sectors`.
- **GSAP/Lenis:** lead-frontend recommends GSAP+Lenis for pinning; product-designer warns pinning is legitimate for *one* moment only. Compatible: adopt GSAP, budget exactly one pinned section.
- **CSS-only vs WebGL baseline:** CMO Phase 0 = CSS-only; lead-frontend "Path C first, architect for Path A" — these agree; Phase 1 is the promotion trigger.

### 10.3 Open questions for the CEO

1. Re-ratify or supersede ticket #303's WebGL confinement? *(Gates everything.)*
2. File the MASTER_SPEC §25 exception ADR + ADR-020 amendment?
3. Light/dark interplay: 3D only in dark mode (recommended), dark-only homepage, or double the scene cost for both modes?
4. Phase 1 location: `/technology` or `/sectors`? Homepage only, or interior proof page (recommended)?
5. Approve the bundle line item (three.js + GSAP ≈140–220 KB gz) or constrain to CSS-only "immersive"?
6. Device floor: design target = 3-year-old Snapdragon 6-series on constrained network (recommended), or desktop-first?
7. Accessibility bar: confirm WCAG 2.2 AA as contractual?
8. Grey token vs utility-class ban: brand tokens `#6B7280`/`#9CA3AF` authoritative for muted text? (Needed before contrast audit.)
9. Primary success KPI: briefing conversion rate (recommended) vs 5-second outcome comprehension vs bounce-at-3s?
10. Confirm non-negotiable: identical crawlable text/routes — no content that exists only in the scene?

---

## 11. Key Sources

**Benchmarks:** [Awwwards Igloo case study](https://www.awwwards.com/igloo-inc-case-study.html) · [Igloo SOTY 2024](https://www.awwwards.com/annual-awards-2024/site-of-the-year) · [Webgpu.com Igloo teardown](https://www.webgpu.com/showcase/igloo-inc-procedural-crystals/) · [Vide Infra AIR](https://videinfra.com/work/air) · [Vide Infra Madar interview (device tiers)](https://videinfra.com/blog/inside-the-making-of-madar-s-cutting-edge-corporate-website-a-conversation-with-the-agency-and-the-client) · [Vide Infra AI-in-banking](https://videinfra.com/work/ai-in-banking-ux-design) · [Codrops on Lusion (2026)](https://tympanus.net/codrops/2026/04/13/lusion-where-digital-craft-meets-ambitious-experimentation/) · [Lusion reverse-engineered (DOM↔3D)](http://mark-n.co/projects/lusion-reverse-engineered/) · [Lusion perf case study (18.9MB)](https://rdjarbeng.com/how-to-check-website-performance-a-case-study-on-lusion.co/) · [Lusion mobile scroll-jack backlash](https://www.reddit.com/r/web_design/comments/16hjop5/)

**Tech:** [R3F install/React pairing](https://r3f.docs.pmnd.rs/getting-started/installation) · [GSAP–Lenis sync pattern](https://gsap.com/community/forums/topic/40426-patterns-for-synchronizing-scrolltrigger-and-lenis-in-reactnext/) · [glTF optimization](https://threejsresources.com/3d-model-optimization) · [Khronos glTF-Compressor](https://github.com/KhronosGroup/glTF-Compressor) · [Google JS SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) · [web.dev vitals business impact](https://web.dev/case-studies/vitals-business-impact)

**UX/a11y:** [WCAG animation-from-interactions](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html) · [W3C WebGL accessibility discussion](https://github.com/w3c/wcag/discussions/4732) · [performance ladders](https://threejs-blocks.com/docs/concepts/performance-ladders) · [NN/g animation & UX](https://www.nngroup.com/articles/animation-purpose-ux/)

**Strategy:** [Africa mobile data prices](https://www.statista.com/chart/29144/cost-of-mobile-data-in-africa) · [interactive site cost bands](https://websbyspider.com/interactive-website-cost) · internal: `docs/marketing/competitive-landscape.md`, `docs/RESERVATIONS-STRATEGY.md`, `docs/venture-studio/*`, `docs/architecture/LIGHTSPEED_AI_COMPANY_BUILDER_WEB_ARCHITECTURE_V2.md`
