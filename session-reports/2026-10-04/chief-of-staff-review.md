---

# Chief of Staff Operational Feedback
## Website Transformation & Repository Consolidation Directive

---

## Executive Summary

The directive is **comprehensive, well-structured, and correctly prioritized**. It correctly identifies this as a **business-critical priority** (not cosmetic) and establishes the right architectural-first approach. The two-track model (Launch + Architectural Hardening) is the correct strategic choice.

However, the **phased plan (Phases 0-7) needs operational hardening** to be executable without resource conflicts, timeline overruns, or quality regressions.

---

## 1. Phased Implementation Plan — Realism & Sequencing Assessment

### Current Phase Structure (from §36)

| Phase | Scope | Risk Level |
|-------|-------|------------|
| **Phase 0** | Repository audit + 6 canonical docs | **HIGH** — Scope creep risk; "no destructive changes" but audit alone is 2-3 weeks |
| **Phase 1** | Canonicalize 8 data registries | **HIGH** — Cross-cutting; touches every page; source of truth conflicts |
| **Phase 2** | Design system + logo | **MEDIUM** — Well-scoped but depends on Phase 1 tokens |
| **Phase 3** | Global shell (header, nav, footer, theme, typography, motion) | **MEDIUM** — Foundation for all pages; must be right |
| **Phase 4** | 13 core pages implementation | **VERY HIGH** — 13 pages in one phase is unrealistic; 3-4 months of work |
| **Phase 5** | Media implementation | **MEDIUM** — Can parallelize but needs design system finalized |
| **Phase 6** | SEO/a11y/performance | **LOW** — Standard hardening |
| **Phase 7** | Full route QA | **LOW** — Standard |

### **Critical Sequencing Issues**

1. **Phase 0 → Phase 1 dependency is too tight** — The 6 canonical docs (especially `WEBSITE_ARCHITECTURE.md`, `CONTENT_ARCHITECTURE.md`, `LIGHTSPEED_DESIGN_SYSTEM.md`) must be **approved and baselined** before Phase 1 starts. Currently they're just "produced."

2. **Phase 4 is a "mega-phase"** — 13 pages with distinct content, interactions, and data needs cannot be one phase. This will cause:
   - Resource contention (frontend, content, design all maxed)
   - Integration debt (pages built in isolation, shell integration fails)
   - QA bottleneck (all 13 pages hit QA simultaneously)

3. **Phase 5 (Media) should start earlier** — Media architecture (§19-20) informs page layouts. Waiting until Phase 5 forces rework.

4. **No explicit "Track A / Track B" split in phases** — The two-track model (§41) is described but not mapped to phases.

### **Recommended Phase Restructure**

```
TRACK A (LAUNCH - 8-10 weeks)
├── Sprint 0 (Week 1-2):   Foundation & Canonicalization
│   ├── Phase 0A: Rapid repo audit → REPOSITORY_CLEANUP_PLAN.md (decision log only)
│   ├── Phase 0B: Architecture & Content Architecture baselined (CEO sign-off)
│   ├── Phase 0C: Design System v1 baselined (tokens, logo, typography, motion)
│   └── Phase 0D: Claims Governance v1 baselined
│
├── Sprint 1-2 (Week 3-6): Shell + Core Pages (MVP)
│   ├── Phase 1: Global Shell (header, nav, footer, theme, CTA system, typography, motion)
│   ├── Phase 2: Home + AI Company Builder (highest traffic / highest conversion)
│   ├── Phase 3: What We Do + Solutions (engagement model + capabilities)
│   └── Phase 4: Use Cases + Sectors (evidence + sector taxonomy)
│
├── Sprint 3 (Week 7-8): Remaining Pages + Media
│   ├── Phase 5: Insights + About + FAQ + Contact + Assessment + Legal
│   ├── Phase 6: Media integration (Hero, H-A-O-M-T-G-V, Org Chart, Model Routing, Africa Economics)
│   └── Phase 7: SEO / Accessibility / Performance hardening
│
└── Sprint 4 (Week 9-10): Launch QA & Go-Live
    ├── Phase 8: Full route QA (§37 checklist)
    ├── Phase 9: Staging validation + CEO sign-off
    └── Phase 10: Production deploy + monitoring

TRACK B (ARCHITECTURAL HARDENING - Continuous, non-blocking)
├── Phase B1: Repository cleanup execution (from REPOSITORY_CLEANUP_PLAN.md)
├── Phase B2: apps/ control-plane / athena separation
├── Phase B3: packages/ design-system / content-model / shared-types extraction
├── Phase B4: services/ orchestrator / governance / memory / audit extraction
├── Phase B5: data/ agents / solutions / use-cases / sectors / insights / claims extraction
├── Phase B6: Legacy route removal + redirect map
└── Phase B7: Technical debt paydown (duplicate components, stale tokens, obsolete UI)
```

---

## 2. Cross-Functional Dependencies

### Dependency Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TRACK A CRITICAL PATH                                 │
└─────────────────────────────────────────────────────────────────────────────┘

DESIGN SYSTEM (Phase 0C) ──────────────────┬──► GLOBAL SHELL (Phase 1)
                                           │
CONTENT ARCHITECTURE (Phase 0B) ───────────┼──► REGISTRIES (Phase 1 data)
                                           │
CLAIMS GOVERNANCE (Phase 0D) ──────────────┤
                                           ▼
                            ┌──────────────────────────────┐
                            │     CORE PAGES (Phases 2-5)  │
                            │  Home, ACB, WWD, Solutions,  │
                            │  Use Cases, Sectors, Insights│
                            └──────────────┬───────────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    ▼                      ▼                      ▼
             MEDIA ARCHITECTURE      SEO/A11Y/PERF           FULL QA
             (Phase 6)               (Phase 7)               (Phase 8)

┌─────────────────────────────────────────────────────────────────────────────┐
│                        TRACK B (PARALLEL, NON-BLOCKING)                     │
└─────────────────────────────────────────────────────────────────────────────┘

REPO CLEANUP PLAN (Phase 0A) ──► REPO CLEANUP EXECUTION (B1)
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    ▼                      ▼                      ▼
             APP STRUCTURE            PACKAGE EXTRACTION      SERVICE EXTRACTION
             SEPARATION (B2)          (B3)                    (B4)
                                           │
                                           ▼
                                    DATA EXTRACTION (B5)
                                           │
                                           ▼
                                    LEGACY REMOVAL (B6)
```

### Key Dependency Conflicts to Manage

| Dependency | Conflict | Mitigation |
|------------|----------|------------|
| **Design System ↔ Global Shell** | Shell needs tokens; Design System needs shell context for real-world validation | **Co-design**: Design System v1 = tokens only; Shell implements; Design System v2 = refined from shell feedback |
| **Content Architecture ↔ Registries** | Registries need IA; IA needs registry audit | **Phase 0B**: IA defines structure; Phase 1 populates from audit |
| **Media Architecture ↔ Pages** | Pages need media specs; Media needs page contexts | **Phase 0B**: Media Architecture defines *types* and *placement strategy*; Pages consume; Phase 6 produces actual assets |
| **Claims Governance ↔ Use Cases** | Use Cases need evidence status; Claims Gov defines statuses | **Phase 0D**: Claims Governance v1 = status taxonomy only; Phase 4 applies |
| **Track A Pages ↔ Track B Repo Structure** | Track A works in current structure; Track B restructures | **Track A owns `apps/web/`**; Track B creates new structure *alongside*; migration at Track A done |

---

## 3. Track A / Track B Coordination — Resource Conflict Prevention

### Resource Allocation Model

| Role | Track A (Launch) | Track B (Hardening) | Conflict Risk |
|------|------------------|---------------------|---------------|
| **Frontend Engineers (2-3)** | 100% (Phases 1-8) | 0% (until Track A done) | **NONE** — Dedicated to launch |
| **Content/IA Lead (1)** | 60% (Phases 0B, 1, 2-5) | 40% (B1 audit, B5 data extraction) | **MEDIUM** — Time-box Track B to 1 day/week |
| **Design Lead (1)** | 80% (Phases 0C, 1, 6) | 20% (B3 design-system package) | **LOW** — Design System package is extraction, not creation |
| **Backend/Platform (1-2)** | 20% (shell integration, build) | 80% (B2, B3, B4, B6, B7) | **LOW** — Different codebases |
| **QA/Accessibility (1)** | 100% (Phase 8) | 0% | **NONE** — Dedicated at end |
| **DevOps (0.5)** | 20% (staging, deploy) | 80% (monorepo tooling, CI for new structure) | **LOW** — Different pipelines |
| **Chief of Staff (you)** | 30% (governance, checkpoints) | 30% (Track B progress, blocker removal) | **NONE** — Orchestration role |

### Coordination Mechanisms

| Mechanism | Cadence | Purpose |
|-----------|---------|---------|
| **Daily Standup (Track A)** | Daily, 15 min | Sprint progress, blockers, Track B dependencies |
| **Weekly Sync (Track A + B)** | Weekly, 30 min | Cross-track dependencies, repo structure decisions, resource rebalancing |
| **Phase Gate Reviews** | Per phase (see §4) | Formal sign-off before next phase |
| **Architecture Decision Log** | Continuous | All Track B structural decisions recorded in `docs/adr/` for Track A awareness |
| **Shared Kanban** | Continuous | Single board with Track A / Track B swimlanes; WIP limits per track |

### **Critical Rule: Track A Never Waits for Track B**

- Track B produces **artifacts** (cleanup plan, extracted packages, new structure) that Track A *may* adopt later
- Track A works in **current `apps/web/` structure** — no migration during launch
- Track B's `apps/control-plane/`, `apps/athena/`, `packages/` extraction happens in **parallel branches**
- **Merge strategy**: Track B merges to `main` only when Track A is in code freeze (Phase 8+)

---

## 4. Governance / Checkpoints per Phase

### Phase Gate Framework

| Phase | Gate Name | Entry Criteria | Exit Criteria | Decision Authority | Artifacts |
|-------|-----------|----------------|---------------|-------------------|-----------|
| **0A** | **Audit Complete** | Repo access granted | `REPOSITORY_CLEANUP_PLAN.md` with KEEP/REFACTOR/DEPRECATE/MOVE/DELETE for every top-level path | Chief of Staff | Cleanup plan + risk register |
| **0B** | **Architecture Baselined** | 0A complete | `WEBSITE_ARCHITECTURE.md` + `CONTENT_ARCHITECTURE.md` + `USE_CASE_ARCHITECTURE.md` + `MEDIA_ARCHITECTURE.md` approved | CEO + Chief of Staff | 4 signed architecture docs |
| **0C** | **Design System v1 Baselined** | 0B complete | `LIGHTSPEED_DESIGN_SYSTEM.md` + `src/brand/tokens/brand-tokens.json` + logo assets approved | CEO + Creative Director | Design system doc + tokens + logo package |
| **0D** | **Claims Governance v1 Baselined** | 0B complete | `CLAIMS_GOVERNANCE.md` with status taxonomy + evidence requirements approved | CEO + Legal Owner | Claims governance doc |
| **1** | **Shell Complete** | 0C, 0D complete | Global shell (header, nav, footer, theme, CTA, typography, motion) working on all routes; responsive; accessible | Lead Frontend + Chief of Staff | Shell component library + storybook |
| **2** | **Home + ACB Complete** | 1 complete | Home + AI Company Builder pages: content complete, media placed, responsive, accessible, SEO-ready, CEO approved | CEO + Chief of Staff | 2 production-ready pages |
| **3** | **WWD + Solutions Complete** | 2 complete | What We Do + Solutions: content complete, media placed, responsive, accessible, SEO-ready | CPO + Chief of Staff | 2 production-ready pages |
| **4** | **Use Cases + Sectors Complete** | 3 complete | Use Case explorer + detail pages + Sectors: filters working, evidence status correct, media placed | Consulting Lead + Chief of Staff | Use Case + Sector pages |
| **5** | **Remaining Pages Complete** | 4 complete | Insights + About + FAQ + Contact + Assessment + Legal: complete | Pharos Lead + Chief of Staff | 6 production-ready pages |
| **6** | **Media Integrated** | 0B, 5 complete | All media types (A-K) placed per placement strategy (§20); no generic placeholders on core pages | Creative Director + Chief of Staff | Media audit report |
| **7** | **Hardening Complete** | 6 complete | SEO (all pages), Accessibility (WCAG AA), Performance (Lighthouse >90) | QA Lead + Chief of Staff | Lighthouse reports + aXe reports |
| **8** | **Launch QA Pass** | 7 complete | §37 checklist 100% pass; no P0/P1 bugs; CEO sign-off | CEO + Chief of Staff | QA sign-off doc |
| **9** | **Production Go-Live** | 8 complete | Staging validated; DNS switched; monitoring active; rollback plan tested | CEO + DevOps | Deployment runbook |

### Gate Enforcement Rules

1. **No phase starts without prior gate exit criteria met** — Hard stop
2. **Gate reviews are time-boxed (2 hours max)** — Pre-read artifacts 24h before
3. **Failed gate = automatic 1-week remediation sprint** — No "conditional pass"
4. **CEO sign-off required for Phases 0B, 0C, 0D, 2, 8, 9** — Strategic alignment
5. **Chief of Staff owns gate scheduling and artifact preparation** — No surprises

---

## 5. Resources, Owners, Timelines per Phase

### Track A Resource Plan (8-10 weeks)

| Phase | Duration | Owner | Resources | Key Milestones |
|-------|----------|-------|-----------|----------------|
| **0A** | 1 week | Chief of Staff | 1 PM, 1 FE, 1 BE | Day 3: Audit 50% done; Day 5: Cleanup plan delivered |
| **0B** | 1 week | CPO + Chief of Staff | 1 PM, 1 Content, 1 FE (review) | Day 3: IA draft; Day 5: 4 docs CEO-approved |
| **0C** | 1 week (parallel 0B) | Creative Director | 1 Design, 1 FE (tokens impl) | Day 3: Tokens draft; Day 5: Design system + logo CEO-approved |
| **0D** | 3 days (parallel 0B) | Legal Owner | 1 Legal, 1 Content | Day 3: Claims governance CEO-approved |
| **1** | 1.5 weeks | Lead Frontend | 2 FE, 1 Design (review) | Day 4: Header/Nav/Footer done; Day 7: Theme/Typo/Motion done; Day 10: Shell gate |
| **2** | 1.5 weeks | CPO + Creative Director | 2 FE, 1 Content, 1 Design | Day 4: Home content done; Day 7: ACB content done; Day 10: Both pages gate |
| **3** | 1 week | CPO | 2 FE, 1 Content | Day 3: WWD done; Day 5: Solutions done; Day 7: Gate |
| **4** | 1.5 weeks | Consulting Lead | 2 FE, 1 Content, 1 Design | Day 4: Use Case explorer; Day 7: Use Case detail; Day 10: Sectors; Day 11: Gate |
| **5** | 1 week | Pharos Lead + HR | 2 FE, 1 Content | Day 3: Insights+About; Day 5: FAQ+Contact+Assessment+Legal; Day 7: Gate |
| **6** | 1 week | Creative Director | 1 Design, 1 FE, 1 Media specialist | Day 3: Hero+H-A-O-M-T-G-V; Day 5: Org Chart+Model Routing+Africa Econ; Day 7: Gate |
| **7** | 1 week | QA Lead | 1 QA, 1 FE, 1 DevOps | Day 3: SEO done; Day 5: A11y done; Day 7: Perf done; Day 7: Gate |
| **8** | 1 week | Chief of Staff | 1 QA, 1 FE, 1 DevOps, CEO | Day 2: §37 checklist; Day 4: Bug fix; Day 5: CEO sign-off |
| **9** | 2 days | DevOps | 1 DevOps, 1 FE | Day 1: Deploy; Day 2: Monitor + validate |

**Total Track A: ~10 weeks (with 1-week buffer = 11 weeks)**

### Track B Resource Plan (Continuous, 12-16 weeks)

| Phase | Duration | Owner | Resources | Dependencies |
|-------|----------|-------|-----------|--------------|
| **B1** | 2-3 weeks | Registry Owner | 1 BE, 1 DevOps | 0A complete |
| **B2** | 2 weeks | Platform Engineer | 1 BE, 1 DevOps | B1 50% done |
| **B3** | 2 weeks | Platform Engineer | 1 BE, 1 FE (design-system) | B2 started |
| **B4** | 2 weeks | Orchestration Owner | 2 BE | B2 started |
| **B5** | 2 weeks | Registry Owner | 1 BE, 1 Content | B3, B4 started |
| **B6** | 1 week | DevOps | 1 DevOps, 1 FE | Track A Phase 8 (code freeze) |
| **B7** | Ongoing | VP Engineering | 1 BE | Continuous |

**Track B runs in parallel; no Track A dependency after Phase 0A**

---

## 6. Ensuring Phase 0 (Repository Cleanup) Doesn't Block

### The Core Problem
Phase 0 as written ("Audit the entire repository... Produce 6 canonical docs") is **unbounded**. A thorough audit of this repository (AI Company Builder + website + Athena + internal dashboards + generated artifacts) could take **3-4 weeks** if done comprehensively.

### Solution: **Rapid Audit + Decision Log** (Time-boxed to 1 week)

#### Week 1 Execution Plan

| Day | Activity | Owner | Output |
|-----|----------|-------|--------|
| **Day 1** | Automated inventory | DevOps + FE | `repo-inventory.json` (all paths, size, last modified, imports) |
| **Day 2** | Classification workshop (2hr) | Chief of Staff + CPO + Lead FE + Creative Director | Every top-level path → KEEP/REFACTOR/DEPRECATE/MOVE/DELETE |
| **Day 3** | Architecture decisions (2hr) | CEO + CPO + CTO + Creative Director | Route map, IA, design system direction, media strategy confirmed |
| **Day 4** | Doc drafting (parallel) | Content + Design + Legal | 6 canonical docs v0.1 |
| **Day 5** | Review + CEO sign-off | All leads + CEO | 6 docs baselined; Cleanup plan v1.0 |

#### Audit Scope Reduction (Pareto Principle)

**Audit ONLY what affects Track A launch:**
- `apps/web/` (or current website root)
- `src/` (shared components, tokens, utilities)
- `public/` (assets)
- `docs/` (current architecture docs)
- `package.json` / build config

**DEFER (Track B):**
- `apps/control-plane/` → B2
- `apps/athena/` → B2
- `services/` → B4
- `data/` → B5
- Generated artifacts → B1 cleanup
- Legacy website components → B6 removal

#### Cleanup Plan Template (Lightweight)

```markdown
# REPOSITORY_CLEANUP_PLAN.md (v1.0)

## Track A Critical Path (DO NOT TOUCH until Track A done)
| Path | Status | Reason |
|------|--------|--------|
| apps/web/ | KEEP | Track A workspace |
| src/components/ | KEEP | Shared UI |
| src/brand/tokens/ | KEEP | Design system source |
| public/ | KEEP | Static assets |

## Track B Cleanup (Parallel, Non-Blocking)
| Path | Classification | Migration Target | Owner | Risk | Timeline |
|------|----------------|------------------|-------|------|----------|
| apps/control-plane/ | MOVE | apps/control-plane/ (new structure) | Platform Eng | MEDIUM | B2 |
| apps/athena/ | MOVE | apps/athena/ (new structure) | Platform Eng | MEDIUM | B2 |
| src/legacy-design-tokens/ | DELETE | N/A | Design Lead | LOW | B1 |
| components/Proof*/ | DEPRECATE | Use Case components | FE Lead | HIGH | B1 |
| duplicate Home/ | DELETE | N/A | FE Lead | LOW | B1 |
| generated/ | DELETE | N/A | DevOps | LOW | B1 |
| ... | ... | ... | ... | ... | ... |

## Decisions Requiring CEO Input
- [ ] Athena: separate subdomain vs. /athena route
- [ ] Control plane: separate repo vs. monorepo app
- [ ] Legacy offer pages: redirect vs. archive
```

---

## 7. Recommended Immediate Actions (This Week)

### For You (Chief of Staff)

1. **Today**: Set up Track A / Track B Kanban board with swimlanes and WIP limits
2. **Day 1**: Schedule Phase 0A audit workshop (2hr, Day 2) + Architecture decision meeting (2hr, Day 3)
3. **Day 1**: Assign Track A dedicated resources (2 FE, 1 Content, 1 Design, 1 QA) — **protect their time**
4. **Day 2**: Run automated repo inventory (`bash` script → `repo-inventory.json`)
5. **Day 3**: Run architecture decision meeting — get CEO sign-off on 4 key decisions:
   - Route map (final)
   - IA structure (final)
   - Design system direction (final)
   - Media strategy (final)
6. **Day 4-5**: Draft and baseline 6 canonical docs
7. **Day 5**: Phase 0 gate review — **Track A Sprint 1 starts Monday**

### For CEO

- **Day 3**: Attend architecture decision meeting (2hr) — make the 4 key decisions
- **Day 5**: Review and sign off 6 canonical docs (30 min)
- **Week 2+**: Bi-weekly 30-min check-in on Track A progress (gate reviews)

### For Track Leads

- **Creative Director**: Own Design System v1 (Phase 0C) — deliver tokens + logo by Day 5
- **CPO**: Own Content Architecture (Phase 0B) — deliver IA + registries structure by Day 5
- **Legal Owner**: Own Claims Governance (Phase 0D) — deliver status taxonomy by Day 4
- **Lead Frontend**: Prepare Shell component architecture — ready to execute Phase 1 Week 2

---

## 8. Risk Register (Top 5)

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Phase 0 scope creep** | HIGH | HIGH | Time-box to 1 week; only audit Track A paths; defer rest to Track B |
| **Phase 4 (13 pages) bottleneck** | HIGH | HIGH | Split into 3 sub-phases (Home+ACB, WWD+Solutions, Use Cases+Sectors, Rest) |
| **Design System ↔ Shell integration failures** | MEDIUM | HIGH | Co-design: tokens first, shell implements, refine tokens from shell feedback |
| **Content/IA resource contention (Track A + B)** | MEDIUM | MEDIUM | Content lead 60/40 split; Track B content work time-boxed to 1 day/week |
| **CEO review delays on gate artifacts** | MEDIUM | HIGH | Pre-read 24h before; 30-min focused review; decisions documented immediately |

---

## Final Recommendation

**Approve the restructured 10-week Track A plan with 1-week Phase 0.** The two-track model is sound but must be operationally separated — Track A gets dedicated resources and a fixed timeline; Track B runs in parallel on structural cleanup without blocking launch.

**Key success factors:**
1. **Phase 0 time-boxed to 1 week** (rapid audit + 4 decision meetings + 6 doc baselines)
2. **Track A resources 100% dedicated** (no Track B pull)
3. **Phase gates with CEO sign-off at strategic points** (0B, 0C, 0D, 2, 8, 9)
4. **Track B produces artifacts, not dependencies** — Track A adopts when ready
5. **Weekly cross-track sync** to catch integration risks early

The directive's vision is correct. This execution framework makes it deliverable.

---

*Prepared by: Chief of Staff*
*Date: 2026-10-04*
*Classification: INTERNAL — EXECUTION PLANNING*
