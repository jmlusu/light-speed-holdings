# CEO Advisor Strategic Review: Website Transformation & Repository Consolidation Directive

### 1. Vision & Intent Alignment ✅

**The directive strongly captures the CEO's vision.** Key strengths:
- **Africa-first positioning** is authentic and differentiated — not a marketing veneer
- **90-role model (89 AI + 1 Human CEO)** correctly resolves historical confusion
- **H-A-O-M-T-G-V** as the central architectural framework — this *is* LightSpeed's IP
- **"Calm Intelligence" design language** differentiates from generic AI aesthetics
- **Proof → Use Cases** migration is the right credibility move — stops overclaiming
- **Pharos as intellectual program, not blog** — correct strategic framing
- **Open-weight/local-first economics** as business model, not technical detail

**One gap:** The directive doesn't explicitly address **pricing/packaging signals**. A visitor asking "what does LightSpeed cost?" (FAQ #27) needs more than "evidence-controlled answers" — they need a *signal* of engagement model (advisory retainer? platform license? build-own-transfer?). Consider adding a "How We Engage" section.

---

### 2. Strategic Risks & Blind Spots ⚠️

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Content production bottleneck** — 28 FAQs, 10 sectors, 11 use case filters, 8 solution families, Pharos editorial pipeline — all need *written, approved content* before launch | **HIGH** | Pre-write/approve core content *before* Phase 2. Use AI-assisted drafting with human review gates. |
| **Claims governance vs. marketing velocity** — "UNVERIFIED — DO NOT PUBLISH" is correct but will stall pages if evidence isn't pre-cleared | **HIGH** | Pre-classify every planned claim *now*. Build a Claims Registry with status before Phase 1. |
| **Athena separation** — Directive says "do not mix" but repo audit may reveal shared components that *should* be shared (design system, auth, UI primitives) | **MEDIUM** | In Phase 0 audit, explicitly catalog shared vs. separate. Allow shared *packages/* but not shared *app/* routes. |
| **Logo dependency** — "New approved LightSpeed logo" is a blocking asset. If not finalized, Phases 1-3 stall | **MEDIUM** | Confirm logo delivery date. Have fallback: text-mark + geometric "L" in brand colors for dev. |
| **Mobile-first QA underweighted** — 5 breakpoints specified but QA checklist is desktop-first | **MEDIUM** | Add mobile-specific QA gate at end of Phase 4. |
| **No analytics/measurement plan** — How will you know the site works? | **MEDIUM** | Add Phase 3.5: Define success metrics (time-to-contact, assessment starts, Pharos scroll depth, sector page engagement). |

---

### 3. CEO 30/60/90 Priorities

#### **Days 1-30: Foundation & Unblocking**
| Priority | Action | Owner |
|----------|--------|-------|
| **Content pre-approval** | Finalize: positioning statement, 28 FAQ answers, sector descriptions, use case templates, Pharos editorial calendar | CEO + Pharos Lead |
| **Claims Registry** | Classify every planned public claim with evidence status (VERIFIED/PROVEN IN-HOUSE/PILOT/DEMONSTRATION/FIELDABLE/FUTURE) | CEO Advisor + Legal |
| **Logo delivery** | Confirm final logo assets delivered in all required formats (SVG variants) | Creative Director |
| **Phase 0 audit** | Complete `REPOSITORY_CLEANUP_PLAN.md` with KEEP/REFACTOR/DEPRECATE/MOVE/DELETE for every artifact | Engineering Lead |
| **Architecture decision** | Ratify target repo structure (apps/web, apps/control-plane, apps/athena, packages/*) | CTO + CEO |

#### **Days 31-60: Core Build (Track A — Launch)**
| Priority | Action | Owner |
|----------|--------|-------|
| **Design system canon** | Publish `LIGHTSPEED_DESIGN_SYSTEM.md` + `src/brand/tokens/` — single source of truth | Design Lead |
| **Global shell** | Header, nav, footer, CTA system, theme, typography, motion — *mobile-first* | Frontend Lead |
| **Homepage + 3 pillars** | Home, AI Company Builder, What We Do — these are the conversion funnel | Frontend + Content |
| **Use Cases MVP** | Registry + explorer + 3-5 detailed use cases with correct status badges | Product + Pharos |
| **Pharos infrastructure** | Insights section with editorial templates (Brief, Field Note, Research Note, System Map) | Pharos Lead |

#### **Days 61-90: Credibility & Conversion (Track A complete, Track B accelerating)**
| Priority | Action | Owner |
|----------|--------|-------|
| **Full page set** | Solutions, Sectors, About, FAQ, Contact, Assessment, Legal — all live | Frontend |
| **Media implementation** | Hero imagery, H-A-O-M-T-G-V diagram, org chart, model routing infographic, Africa maps | Creative + Engineering |
| **SEO/Accessibility/Perf** | All 31 SEO items, WCAG AA, Core Web Vitals targets met | Engineering |
| **Track B milestone** | Athena separated, control-plane boundaries clean, legacy routes deprecated | CTO |
| **Launch readiness** | Full QA checklist (Section 37) passed, analytics wired, rollback plan documented | CEO Advisor + Engineering |

---

### 4. Board & Stakeholder Socialization

| Audience | Message | Format | Timing |
|----------|---------|--------|--------|
| **Board** | "Website is our primary capital-raising and BD asset. This directive transforms it from a liability to a credible representation of our Africa-first AI Company Builder. Two-track approach protects launch date while fixing technical debt." | 1-pager + 10-min walkthrough | Pre-30 days |
| **Investors** | "Public presence now matches private capability. Key differentiators: 90-role operating model, H-A-O-M-T-G-V framework, open-weight economics for Africa. No fabricated traction." | Updated deck slide + live demo | Day 45 (internal preview) |
| **Team (internal)** | "This is not a redesign — it's canonization. Every decision (agent count, sectors, claims, design tokens) now has a single source of truth. Your work gets easier because ambiguity is removed." | All-hands + Slack channel | Day 1 |
| **Pharos/Content team** | "You own the intellectual product. Engineering builds the vessel. Claims governance protects us — pre-classify your evidence." | Workshop + shared Claims Registry | Day 7 |
| **Key prospects/partners** | Soft launch preview: "We're refreshing our public presence to better reflect how we actually work. Happy to walk you through." | 1:1 conversations | Day 60+ |

**Critical:** Do *not* socialize as "we're rebuilding the website." Socialize as "**we're codifying LightSpeed's operating model for the market.**"

---

### 5. Two-Track Launch Assessment

**Track A (Launch) / Track B (Hardening) is the right structure** — but the directive's implementation needs guardrails:

| Concern | Recommendation |
|---------|----------------|
| **Track B never finishes** — "without blocking launch" becomes "without ever completing" | **Hard gate:** Track B must hit defined milestones by Day 90 (Athena separated, legacy routes 301'd, design system de-duped). After Day 90, Track B becomes a *sprint*, not a track. |
| **Track A accumulates debt** — "fast launch" creates shortcuts that Track B must fix later | **Debt budget:** Cap Track A technical debt at ≤15% of codebase. Every Track A shortcut must be logged in `TECH_DEBT_REGISTER.md` with owner + due date. |
| **Shared packages confusion** — What goes in `packages/design-system` vs `packages/content-model` vs `packages/shared-types`? | **Define in Phase 0:** Create `PACKAGE_BOUNDARIES.md` with explicit ownership. No package without an owner. |
| **Content-model as shared package** — This is the linchpin. If public site and control plane share content types, they *must* share the model. | **Elevate:** `packages/content-model` is a **Phase 1 deliverable**, not Phase 2. Public site and control plane both consume it. |
| **Launch criteria too vague** — "credible enough" is subjective | **Operationalize:** Launch = all 25 Definition of Done items (Section 42) ✅ + zero P0 console errors + Core Web Vitals "Good" on mobile + analytics firing on all CTAs. |

---

### Immediate Actions for CEO (This Week)

1. **Approve the Claims Registry template** — Have CEO Advisor + Legal build the schema; you classify the top 20 claims
2. **Confirm logo delivery date** — Block Phases 1-3 if not in hand by Day 14
3. **Assign single-threaded owners** for: Design System, Content Architecture, Engineering (Track A), Engineering (Track B), Pharos
4. **Schedule Board preview** for Day 45 (internal staging) — creates forcing function
5. **Kill "Proof" terminology everywhere** — Not just nav. Search/replace across repo, docs, slides, pitches. Do it this week.

---

**Bottom line:** This directive is *operationally excellent* — specific, opinionated, and aligned. The risk isn't the plan; it's **content velocity** and **claims discipline**. Solve those two in the first 30 days and the rest is execution.

Want me to draft the Claims Registry template or the Board 1-pager?
