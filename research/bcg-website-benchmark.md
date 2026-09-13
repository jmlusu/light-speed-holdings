# BCG Website Benchmark — Feature Adoption Plan for LightSpeed Holdings

**Prepared:** 2026-09-11
**Benchmark target:** https://www.bcg.com (2025 "Vicine" redesign, hero/keyvisual pages, /publications, /about)
**Internal baseline:** `website/index.html` (single static page, vanilla JS + Three.js r128 CDN, no build step)
**Method:** Three-agent parallel review (frontend, strategy, product design) + direct homepage fetch

---

## 1. Review Team

| Agent (`subagent_type`) | Scope | Key outputs |
|-------------------------|-------|-------------|
| `lead-frontend` | BCG technique inventory; feasibility against the static vanilla-JS/Three.js stack | Feasibility matrix, P0/P1/P2 roadmap, gap list, files to extend |
| `cmo` | Strategic trust-signal + brand-fit review | Content plan, on-brand/off-brand verdicts, copy directions |
| `product-designer` | BCG IA/motion critique vs. LightSpeed page flow | Homepage revision, motion recipe, a11y/perf constraints, anti-patterns |

---

## 2. Skills Pipeline (for subsequent implementation)

| Layer | Skill | Role |
|-------|-------|------|
| Brand base | `ls-design-system` | **Load first.** Brand tokens are the single source of truth; the live site violates them |
| Orchestrator | `ls-creative-director` | Routes the brief to a production skill, then to QA |
| Production | `ls-frontend-design` | On-brand rebuild (navy/red/cyan, Arial scale, 4px grid) |
| Support | `ls-diagramming`, `ls-visual-storytelling` | System-pipeline SVG, fleet data-viz, infographic assets |
| Gatekeeper | `ls-artifact-qa` | APPROVE / FIX loop on every artifact (Playwright visual checks) |
| Quality rails | `building-accessible-interfaces`, `performance-optimizer` | reduced-motion, focus management, Three.js budget |

---

## 3. BCG Technique Inventory (what to borrow)

| Technique | Where on BCG | Purpose | Relevance | Effort (our stack) |
|-----------|--------------|---------|-----------|--------------------|
| Scroll-triggered reveals (IntersectionObserver) | Throughout | Communicative, not ambient, motion | High | Easy |
| Animated stat counters/callouts | Editorial stat callouts, impact pages | Proof via numbers | High | Easy |
| Sticky-nav state + scrollspy | Global nav | Orientation, premium polish | High | Easy |
| Hover micro-interactions | Cards, links, CTAs | Depth + affordance | Med | Easy |
| Video hero (poster fallback, loop) | Capability pages ("AI V2 Hero Video") | "Modern AI-era firm" signal | High | Moderate |
| Featured-insights rail | Homepage | Proof-of-expertise under hero | High | Moderate |
| Inline SVG data-viz / pipeline diagrams | Scroll-driven storytelling microsites | Dense-narrative explanation | Med-High | Moderate |
| Parallax drift on backdrop typography | Multiple | Depth without JS dependency | Med | Easy–Moderate |
| Mega-menu with image cards | Global nav (2025 redesign) | Route expertise ≤2 clicks | Med (only if multi-page) | Hard / skip |
| Personalization / bookmarking | "My Saved Content" | Engagement + sign-ups | Low | Hard / skip (needs backend) |

---

## 4. Prioritized Roadmap

### P0 — Fix foundations before adding "premium"
1. **Repair dead nav anchors.** `#workforce`, `#evidence`, `#insights` (index.html:46-48) point at sections that do not exist. Add the sections or retarget links.
2. **Mobile navigation.** `.nav-links` is `display:none` under 992px with no hamburger — mobile users lose all navigation. Add a toggle + drawer with focus trap and Escape close.
3. **Reduced-motion + visibility handling in `scene3d.js`.** Pause the rAF loop when the tab is hidden and under `prefers-reduced-motion: reduce`.
4. **Scroll reveals** across `#problem`, `#system`, `#capabilities`, `#industries` card grids (once-only, 8-14px fade-up, 240ms ease-out, stagger ≤60ms, max 6 items/batch).

### P1 — BCG-grade proof & polish
5. **Animated stat counters** in `#industries` + `#capabilities` footers (3.8X / 99.4% / <42MS / 85 SEC / -92% / 144 agents), rendered to final value instantly under reduced-motion.
6. **Sticky-nav scrollspy**: highlight current section; shrink pill on scroll.
7. **New `#evidence` section** (fixes the dead anchor) — client-impact cards with topic chip, sector, date, metric footer. Publish method alongside every number (SADC audiences prize humility; avoid unsupported repetitions of claims like "99.4%").
8. **New `#insights` section** (fixes the dead anchor) — editorial rail modeled on BCG `/publications` cards (chip → sector, type label, date, dek, "Learn More"). Build real content; a dead blog damages trust more than none.
9. **Hover upgrade**: cyan `#00BFFF` corner accent on `.chamfer-card`, arrow translate on `.btn-pill-*`, `:focus-visible` outlines (2px, 2px offset) on every control.

### P2 — Distinctive motion & video
10. **Parallax drift on `.backdrop-typography`** tied to the existing `scrollProgress`; disabled under reduced-motion.
11. **Video hero** — muted loop with poster fallback and **click-to-play** (never autoplay), WebM + MP4, ~10-20s loop; or a 90-second motion-graphics explainer with local voices (avoid glossy NY-style corporate video — reads as imported). Requires a produced asset.
12. **Animated SVG pipeline visualization** of the 6-step system (`#system`, index.html:172-197) — BCG's scroll-driven-narrative pattern.

### Additional pages (static, link-consistent)
- `/insights` — "The Lighthouse Brief": *"Sovereign AI, decoded for the leaders who must decide."*
- `/evidence` — Proof: *"Deployments, metrics, and the methodology behind every number."*
- `/about` / `/leadership` — *"Rooted in Lilongwe. Built for Africa. Answerable to results."*
- `/industries/<sector>` — one reusable deep-dive template (hero proposition → stats → related insights).
- `/subscribe` — The Sovereign-AI Briefing (newsletter strip before footer, BCG pattern).
- `/join` — Careers: *"Build the continent's most advanced AI fleet — from the continent."*

---

## 5. Brand Compliance (pre-requisite to any of the above)

- The live site palette (zinc `#09090b`, emerald `#34d399`, amber `#fbbf24`, purple `#a855f7`) **diverges from brand tokens** — navy `#070A40` / red `#E63946` / cyan `#00BFFF`, Arial type scale, 4px grid, radii 4/8/16. Align surfaces to navy; reserve red for the single primary action; cyan for links/labels.
- The "LS" text badge **recreates the logo** (violates brand rule #1). Use official assets from `static/brand/logos/`.
- Red `#E63946` was used for "signal waves/accent" — keep it as accent/CTA, not large surfaces (reads as alarm in government contexts).

---

## 6. BCG Anti-Patterns to Avoid

1. Autoplay hero video / keyvisuals — payload bloat + autoplay traps; poster + click-to-play instead.
2. Auto-advancing insight carousels — need pause + visible controls; a static grid is safer for a small firm.
3. Mega-menu with 30+ imaged entries — keep ≤7 top-level destinations.
4. JS-only navigation — keep anchor nav with no-JS fallbacks.
5. Account-gated content ("My Saved Content") — friction kills trust for a one-page firm.
6. Constant background animation — already a risk with the always-on 3D stage; do not compound.
7. CTA sprawl — one primary action per band (BCG green-only discipline; LightSpeed red-only).

---

## 7. Performance & Accessibility Floor

- Self-host the three Google font families (heavy); lazy-load the Three.js script.
- Cap `devicePixelRatio` to 1.5; drop ~3,000 → ~500 particles on mobile.
- Replace multiple 24px `backdrop-filter` cards with cheaper translucent surfaces; stop fixed 12vw backdrop text on mobile.
- Budget for the 3D scene: pause offscreen; `context-lost` fallback message.
- Bump body text `#71717a` to ≥4.5:1 contrast; add skip-to-content link; labeled form inputs with a real backend handler + `aria-live` success.
- Every new motion must respect `prefers-reduced-motion: reduce` (BCG-grade accessibility is a hard bar).

---

## 8. Files to Extend

| File | Change |
|------|--------|
| `website/index.html` | Fix/add sections + anchors (`#evidence`, `#insights`, `#workforce`), hero proof card, spotlight chips, official logo |
| `website/assets/css/style.css` | Brand-token palette, reveals, hover, sticky/scrollspy, scroll-snap rail, motion media queries |
| `website/assets/js/main.js` | IntersectionObserver reveals, counters, scrollspy, mobile nav toggle, reduced-motion gate |
| `website/assets/js/scene3d.js` | Visibility pause + motion gate, DPR/particle caps |

---

## 9. Bottom Line

BCG's trust comes from **structured proof, named voices, dated output, and quantified claims with method** — not from flash. LightSpeed's highest-leverage moves are cheap and on-brand: the evidence page, the animated fleet visualization, and a sustained insights cadence. Video and parallax are secondary. Do P0 (foundations incl. brand compliance) before any "premium" feature.

---

*Sources: bcg.com homepage + capabilities/publications/about pages (fetched 2026-09-11); internal review of `website/`, `brand/tokens/`, `static/brand/`, `.agents/skills/ls-design-system` and `ls-frontend-design`.*
