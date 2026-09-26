# Team Structure

## Executive Leadership

| Role | Name | Decision Authority |
|------|------|-------------------|
| **CEO** | Jack Mlusu | Final authority on all venture-studio decisions; locked palette ADR-020 enforcement |
| **Chief of Staff** | [Designated] | Coordinates cross-team alignment; 75/100 subagent evaluation score |
| **CMO** | [Designated] | Market positioning, category creation, demand generation; 68/100 evaluation score |
| **CTO** | [Designated] | Technology architecture, CI/CD, platform health |
| **CFO** | [Designated] | Budget, API cost tracking, financial forecasting |
| **CSO** | [Designated] | Corporate strategy, M&A, market expansion |

## Engineering & Product

| Role | Focus | Key Deliverables |
|------|-------|------------------|
| **Lead Backend** | API standards, database patterns, server-side architecture | Message bus, orchestrator, domain models |
| **Lead Frontend** | UI architecture, component standards, frontend toolchain | Vite React SPA, Tailwind 4, HeroMist, ripple effects, smooth scroll |
| **Product Owner** | Product backlog, user stories, sprint goals | Homepage execution plan, venture-studio docs Parts 2–5 |
| **UX Research Lead** | User research, feature prioritization, onboarding flows | Accessibility audits, visual QA reports |

## Creative Production

| Role | Focus | Key Deliverables |
|------|-------|------------------|
| **Creative Director** | Orchestrator of LightSpeed Creative Production Stack | Design system enforcement, brief intake, production skill routing |
| **Brand Advertising** | Commercial creative for ads, billboards, social campaigns | Brand tokens, on-brand artifact generation |
| **Presentation Design** | Executive communication, board presentations, decks | PPTX generation, speaker notes, branded templates |
| **Social Media Design** | Multi-channel campaign generation | LinkedIn articles, X threads, Instagram carousels |
| **Document Design** | Whitepapers, strategy reports, policy papers | Executive reports, investment memoranda |
| **Artifact QA** | Final gate on every creative artifact | Visual/QA/Brand/UX/Accessibility/Content approval |

## Governance

| Body | Function | Frequency |
|------|----------|-----------|
| **ApprovalGate** | Periodic sweep of PENDING → EXPIRED approvals; HITL expiry | Daily |
| **ECL Board** | Change lifecycle, context loading, harness workflow | Per change |
| **Dashboard RBAC** | Key rotation, access control | Every 90 days (scheduled) + on compromise |

## Subagent Evaluation Summary (from current session)

| Subagent | Score | Key Takeaways |
|----------|-------|---------------|
| **Chief-of-Staff** | 75/100 | Artifacts committed but 25% incomplete; CEO "legacy content intact" concern; ECL slot conflict; CI diagram validation |
| **Caio** | 55/100 | Part 1 effects 95% complete on paper; Parts 2–5 strategic docs 100% on paper; KPIs not instrumented; governance framework gaps |
| **Lead-Frontend** | 72/100 | 85% of Part 1 effects properly implemented; hook noise (`detect-private-key`, `validate-drift`); reduced-motion gating limiting HeroMist |
| **QA-Lead** | 65/100 | Lint 17/17, build, lint pass reliably; visual QA gaps: `qa-report.json` targets `localhost:3000` but site runs at `localhost:4173`; Playwright APPROVE unverifiable |
| **Head-of-Business-Development** | 65/100 | Documentation deliverables strong (Parts 2–5); ECL parked not closed; KPIs defined but not instrumented; legacy content dilutes new positioning; registry uses legacy tool aliases |
| **CMO** | 68/100 | Documentation artifacts excellent (~90% complete, owned category with clear moat); marketing deliverable ~55% market-ready; website still has legacy content conflicting with ADR-020 locked palette |

## Active Session Conflicts

- **`v2-implementation-p2-public-registry-transform`** (session `deee1150-1546-48a2-bd96-c89d2f891d70`, phase implement) — holds active ECL slot
- **`LS-MEM Phase 2 - Architecture`** — concurrent LS-MEM work
- **Do NOT stage, park, or close these sessions' files**

## Key Constraints (ADR-020 Locked)

- **Palette**: Navy `#070A40` / Red `#E63946` / Cyan `#00BFFF` — no amendments
- **Tokens**: Must not edit; any edits must be reverted
- **Website**: Part 1 only shipped; Parts 2–5 documentation only — no code/registry/deploy changes
- **Legacy content**: Must remain intact and visible where ADR-020 does not override
