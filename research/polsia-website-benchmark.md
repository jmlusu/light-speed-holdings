# Polsia Website Benchmark — Feature Adoption Plan for LightSpeed Holdings

**Prepared:** 2026-09-11
**Benchmark target:** https://polsia.com (React SPA; live terminal header, full-slide deck, 29 CSS keyframes)
**Internal baseline:** `website/index.html` (single static page, vanilla JS + Three.js r128 CDN, no build step)
**Method:** Six-agent parallel review (brand, frontend architecture, product design, growth, UX research, competitive intelligence) + direct fetch of the SPA shell and its compiled CSS bundle

---

## 1. Review Team

| Agent (`subagent_type`) | Lens | Key outputs |
|-------------------------|------|-------------|
| `brand-strategist` | Translate Polsia's terminal aesthetic into LightSpeed brand language | Brand translation table, signature visual moment, on-brand/off-brand verdicts |
| `frontend-architect` | Feasibility of each feature against the static vanilla-JS/Three.js stack | Feasibility ratings, z-index plan, performance budget, P0/P1/P2 roadmap |
| `product-designer` | Interaction/IA critique for a C-suite enterprise audience | Trust-builder vs. distraction ranking, interaction patterns, adoption risks |
| `growth-hacker` | Conversion mechanics (SaaS trial vs. Executive Briefing model) | Conversion map, hero CTA hierarchy fix, transferable vs. non-transferable mechanics |
| `ux-research-lead` | WCAG/a11y + evidence-based motion assessment for SADC/exec audiences | Motion budget, mandatory guardrails, test checklist, current-site audit |
| `head-of-competitive-intelligence` | Positioning gap, persuasive techniques, uncopyable differentiators | Positioning table, "signature" recommendation, must-not-copy list |

---

## 2. Skills Pipeline (for subsequent implementation)

| Layer | Skill | Role |
|-------|-------|------|
| Brand base | `ls-design-system` | **Load first.** Brand tokens (navy `#070A40` / red `#E63946` / cyan `#00BFFF`, Arial scale, 4px grid) are the single source of truth |
| Orchestrator | `ls-creative-director` | Brief intake → routes to a production skill, then to QA |
| Production | `ls-frontend-design` | On-brand implementation of the fleet log, reveals, hover polish |
| Support | `ls-diagramming`, `ls-visual-storytelling` | System-pipeline SVG, fleet data-viz assets |
| Gatekeeper | `ls-artifact-qa` | APPROVE / FIX loop on every artifact (`visual_check.js` Playwright probes) |
| Quality rails | `building-accessible-interfaces`, `performance-optimizer`, `reviewing-interface-quality` | reduced-motion, focus management, Three.js budget, final UI critique |

---

## 3. Polsia Technique Inventory (what to borrow)

| Technique | Where on Polsia | Purpose | Verdict | Effort (our stack) |
|-----------|-----------------|---------|---------|--------------------|
| **Live terminal header** (fixed 88px, mono, rotated log lines, 0.3s fade) | Landing hero | Signature "the AI is working" proof | **Adopt — as a real fleet log, on navy** | Moderate |
| **Scroll-reveal fade-blocks** (`.fade-block` opacity:0/translateY(28px) → `.entered`; IntersectionObserver, `prefers-reduced-motion` fallback) | All sections | Progressive disclosure of dense content | **Adopt (P0, highest ROI)** | Easy |
| **Pulsing announcement banner** (uppercase mono + pulsing dot) | Top bar | Urgency signal | Adopt only for real events | Easy |
| **Scroll-shrinking logo** (96px → smaller, on-dark/on-light crossfade) | Header | Premium polish | Adopt as nav-shrink variant | Moderate |
| **Hover scale/offset-print/button bevels** | Cards, buttons | Tactile affordance | **Adopt at ≤1.03–1.05 scale** | Easy |
| **Stat-evidence rhythm with numbers** | Slides | Credibility | **Adopt — but bind to verifiable engineering stats** | Easy |
| **Product-as-proof screenshots/widgets** | Slides, chat UI | "It's real" | Adopt as a live fleet widget sourced from actual telemetry | Moderate |
| Full-height 100vh slide-deck + fixed dot-rail | Landing | Cinematic rhythm + orientation | Reject (breaks Three.js scroll-lerp; truncates evidence) | Hard |
| Chat widgets / typing dots / ASCII spinners | Talk page | Conversational proof | Reject (consumer tone for this audience) | — |
| 3D / WebGL / parallax / video embeds | — | — | Absent on Polsia; our WebGL is our own differentiator, keep it | — |

---

## 4. Consolidated Feature Roadmap

### P0 — Highest leverage, ~1.5–2h total
1. **Scroll-reveal fade blocks** across `#problem`, `#system`, `#capabilities`, `#industries` grids. IntersectionObserver (threshold ~0.15, rootMargin `0 0 -40px`), add `.entered`, unobserve after fire. CSS: opacity 0 → 1 + translateY 12px, 0.4s, `prefers-reduced-motion: reduce` forces visible/static. CLS-safe (transform-only). ~25 lines across `style.css` + `main.js`.
2. **Hero CTA hierarchy swap** — promote `Request Your Executive Briefing →` to the filled `btn-pill-primary`; demote `Explore The System` to `btn-pill-secondary` (it is currently the reverse and the primary button is a dead end).
3. **Hover polish** — `.chamfer-card:hover` scale(1.03) (not 1.08) + `:focus-visible` rings (2px, 2px offset); subtle inner-gradient bevel on `.btn-pill-*`. Pure CSS.

### P1 — Proof loops & conversion surface
4. **Sticky bottom briefing bar** (48px, dark, single CTA + phone `+265 1 772 000`), appears after scroll depth >30%. Dedicated conversion surface.
5. **Real fleet-activity log ("NIGHT SHIFT EXECUTION")** — fixed top strip on navy, JetBrains Mono, cyan agent names / white action / red status (`⚠ REQUIRES HITL`). Lines reference real agent roles + canonical 7 tools from the registry. Requirements: offset initial camera Y in `scene3d.js` so the WebGL icosahedron clears the header; `setInterval` 3.5–4s swap ≤4 DOM nodes; pause via Page Visibility API + off-viewport IntersectionObserver; auto-pause after ~15s / `aria-live="polite"`. **Lines must be real or plausibly derived from `company/`/`results/` — never invented stats.**
6. **Live proof widget** — read-only snapshot of actual `org-heartbeat`/MessageBus counts (tasks dispatched, HITL gates passed, tests green, KB entries) in a `chamfer-card` near the hero.
7. **Animated stat counters** in card footers (3.8X / 99.4% / <42MS / 85 SEC), instant final value under reduced-motion.
8. **Sticky-nav shrink + scrollspy** — compress floating nav height/padding over the first 120px of scroll (rAF-gated); highlight active section.
9. **Event-driven announcement banner** (40px, red pulse dot) — shown **only** when a real briefing/event exists; dismissable; horse hidden otherwise (zero fake urgency).
10. **Sector-specific proof bar** — 3 anonymized-but-specific sector badges ('Central Bank — SADC Corridor', 'Ministry of Energy — National Grid', 'Pan-African Banking Group') between hero and problem section. Specificity is the proof.

### P2 — Distinctive, later
11. **Haunched ApprovalGate proof loop** — a short "task parks → approver clears → audit event logs" sequence; a proof loop Polsia structurally cannot show.
12. **Founder/principal directness** — one named principal with a one-paragraph "why this exists" statement on-page or `/about`.

---

## 5. Brand Compliance (pre-requisite to any of the above)

- **Never adopt Polsia's palette.** Deep orange `#e65100`/`#ff8a3d`, pure-black surfaces, and light-primary page backgrounds conflict with brand tokens — reject entirely.
- Fleet log backgrounds are **navy `#070A40`, not `#000000`** (black is off-brand).
- Use **JetBrains Mono** (already loaded in `index.html`) for the log; never the off-brand terminal font.
- Logo only from `static/brand/logos/`; nav-brand is text ("LIGHTSPEED") today — respect the 1× clear-space rule if an image variant is ever added; do not recreate the logo.
- Red `#E63946` stays an accent (status signals, pulse dot); it must not dominate surfaces.
- Every metric must be traceable to a real capability/`results/` entry; never publish unsourceable numbers.

---

## 6. Polsia Anti-Patterns to Avoid

1. **Fake terminal theatrics** — a live-looking feed must come from (or plausibly derive from) real telemetry; otherwise it is a liability the moment a buyer checks.
2. **"Runs your company while you sleep" positioning** — autonomy-without-governance. We lead with *auditied, human-gated autonomy*; never frame HITL gates as friction.
3. **29-keyframe motion density** — our site (post-adoption) should target ≤5 keyframes; ≤3 animated elements per viewport; one user-level switching of things at once.
4. **Auto-playing/looping continuous motion** — blink carets, endless pulsing, and always-on feeds violate WCAG SC 2.2.2 and 2.3.3. Everything auto-updating needs pause control or auto-pause.
5. **Chat widgets/typing bubbles** — consumer support idiom; we sell private briefings.
6. **100vh snap-scroll deck** — breaks our smooth scroll-lerp in `scene3d.js` and crops evidence-dense sections; the dot-rail alone can serve orientation if ever needed.
7. **Unverified magnitude claims** ("80% AI") — we publish stat counters only for numbers we can prove (fleet size, test counts, tool vocabulary, on-page metrics).

---

## 7. Performance & Accessibility Floor

- **Fix the current site first:** the Three.js scene runs `requestAnimationFrame` unconditionally — add `prefers-reduced-motion` gate (freeze one frame), pause on tab-hidden/off-viewport, cap `devicePixelRatio` to 1.5, drop ~3,000 → ~1,000 particles on low-core devices.
- Every adopted motion respects `prefers-reduced-motion: reduce` (BCG-grade bar): reveals visible/static, counters instant, terminal static, hover transform-free.
- Terminal containment: fixed-height container (zero CLS); rotate every 3.5–4s; cap visible lines at 3–4 DOM nodes; `aria-live="polite"`; Tab-reachable pause.
- CTA area must be layout-stable (explicit height/min-height) — no animation-driven reflow within 500px of any conversion element.
- Mobile: hide/clamp heavy elements (terminal collapses to a "Fleet active: 144 agents" stat badge; no dot-rail <768px); test 375/414/768px.

---

## 8. Files to Extend

| File | Change |
|------|--------|
| `website/index.html` | Hero CTA swap, sticky bottom bar, sector proof bar, event banner hook, fleet-log header, live-proof widget |
| `website/assets/css/style.css` | Reveal classes + `.entered`, hover scale/bevel, banner pulse keyframe, sticky-bar, fleet-log theme (navy/mono), motion media queries |
| `website/assets/js/main.js` | IntersectionObserver reveals, stat counters, sticky-bar threshold, terminal line rotator (interval + visibility pause), event banner toggle |
| `website/assets/js/scene3d.js` | Camera Y offset for header, reduced-motion gate, off-screen/tab-hidden pause, DPR/particle caps |

---

## 9. Bottom Line

Polsia's strongest asset is **visible operation** — a live terminal that makes "the system is working" visceral. Its transferable core is not the visual (which is off-brand) but the mechanism: *proof that the product runs*. LightSpeed's equivalent narrative is stronger because it is real and uncopyable — **a governed 144-agent fleet with a human-in-the-loop audit trail** — so our "signature" should be a live *audit* loop, not a generic terminal.

Highest-leverage moves, in order: (P0) scroll-reveals + hero CTA swap + hover polish — ~2h, delivers most of the "alive" feel; (P1) sticky briefing bar, a real fleet-activity log on navy, and a live proof widget sourced from actual telemetry; (P1) hero copy sharpened from "From Strategy to Intelligent Execution" (process) toward a clause naming the buyer's outcome, with sector-specific proof. Reject the slide-deck, chat widgets, orange palette, and any unverifiable claims. Fix the unconditionally-running WebGL loop before adding any motion.

---

*Sources: polsia.com SPA shell + compiled CSS bundle (fetched/analyzed 2026-09-11); internal review of `website/`, `brand/tokens/`, `.agents/skills/ls-design-system`, `.agents/skills/ls-frontend-design`, and the orchestrator's MessageBus/org-heartbeat telemetry surface.*
