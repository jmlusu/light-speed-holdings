# Deep Dive Analysis: WeBuild-AI Business Model → Light Speed Holdings

> **Date**: 2026-08-28
> **Scope**: Maps WeBuild-AI's business model (UK-based enterprise AI consultancy) onto Light Speed Holdings (LSH) as a use case for the `ai-company` platform.

## Executive Summary

WeBuild-AI is a UK-based AI consultancy generating revenue from **three streams**: consulting fees, proprietary platform licensing, and equity stakes in ventures they co-build. Light Speed Holdings (LSH) already has **~70% of the infrastructure** needed to replicate or exceed WeBuild-AI's model — the gap is primarily in **consulting service packaging**, **industry accelerators**, and **client-facing delivery tooling**.

---

## 1. WeBuild-AI Business Model (What They Sell)

| Component | What It Is | Revenue Driver |
|-----------|-----------|----------------|
| **Deliberate AI Toolkit** (6 tools: Ignite, Switch, Query, Build, Unify, Learn) | Proprietary SaaS-like platform bundled with consulting | Platform licensing fees |
| **5 Pathfinder Playbook phases**: Research → Rethink → Reboot → Restart → Reframe | Prescriptive transformation methodology | Consulting fees (day rates, fixed-price) |
| **Forward-Deployed Engineers** | Embed engineers within client teams | Consulting fees (embedded staffing) |
| **AI Design Sprint** | 5-day concept-to-prototype engagement | Premium sprint pricing |
| **Venture Co-Build (Restart)** | Build AI-native ventures from scratch for enterprise clients | Equity stakes + consulting |
| **Thought Leadership** | Whitepapers, governance frameworks, blog | Lead generation (no direct revenue) |

**Target clients**: Enterprise (Financial Services, Energy, Retail). Pricing is enterprise sales-led (no public rates).

---

## 2. LSH Capability Map → WeBuild-AI Component Coverage

### Strong Coverage (Ready or Nearly Ready)

| WeBuild-AI Component | LSH Equivalent | Status | Gap |
|----------------------|---------------|--------|-----|
| **Ignite** (prompt library) | `prompts/` templates, `generator.py` Jinja2 engine | Functional | No industry-specific prompt packs |
| **Switch** (model flexibility) | `llm/client.py` + `model_router.py` — 5 providers, tier fallback, cost tracking | Functional | No per-task model toggle UI |
| **Query** (AI chat over docs) | `memory/engine.py` (6 types + vector search) + `executor/agent_loop.py` (ReAct) | Functional | No document ingestion pipeline for client data |
| **Build** (agent studio) | `generator.py` + `company-registry.yaml` (135 agents) + `cli/agents.py` | Functional | No visual agent builder; YAML-only |
| **Unify** (knowledge hub) | `memory/vector_store.py` + `ml/embeddings.py` (sentence-transformer) | Functional | No client-facing data connector framework |
| **Governance & Risk** | `orchestrator/approval.py` + `decision/engine.py` + `security/*` (RBAC, PII, content filter) | Functional | No EU AI Act compliance module |
| **AI Agents & Automation** | Full executor: ReAct loop, HITL gate, dead-letter, daemon, A/B testing | Production-ready | — |
| **Orchestration** | MessageBus, scheduler, escalation, suspend store, briefing generator | Production-ready | — |
| **Dashboard / Monitoring** | FastAPI dashboard, 8 KPI collectors, WebSocket, RBAC, Prometheus metrics | Production-ready | No client-facing portal |
| **Cost Analytics** | `data/cost_analytics.py` + `llm/cost_tracker.py` — per-agent, per-model, budget enforcement | Functional | No client-facing cost reports |
| **Workflow Engine** | `workflow/engine.py` — step tracking, SLA monitoring, FileStore persistence | Functional | No visual workflow builder |

### Partial Coverage (Needs Extension)

| WeBuild-AI Component | LSH Has | What's Missing |
|----------------------|---------|----------------|
| **Reframe** (monetize data) | `data/revenue_analytics.py` — ROI, revenue attribution | No data marketplace, no partnership connectors, no channel/sales pipeline for data products |
| **Restart** (venture building) | `company bootstrapper` + agent registry + full orchestration | No structured venture lifecycle (ideation → validation → MVP → launch → scale). No client investment tracking. No equity modeling. |
| **Operating Model Design** | `hr/` module + `graph/org_chart` + org health KPIs | No org design templates, no role-architecture mapping, no operating model assessment tooling |
| **Industry Focus** | `service-catalog-malawi.md` (regional focus) | No industry vertical templates (FS, Energy, Retail). No domain-specific agent presets. |
| **Forward-Deployed Engineers** | Agent onboarding (7-state lifecycle) + governance gates | No client-site deployment mechanism, no client workspace isolation, no multi-tenant data separation |

### Missing (New Modules Needed)

| WeBuild-AI Component | What LSH Needs | Effort Estimate |
|----------------------|---------------|-----------------|
| **Strategy & Roadmap Service** | `services/strategy.py` — structured discovery → roadmap generation workflow; assessment templates; ROI modeling tools | Medium (2-3 sprints) |
| **AI Design Sprint (5-day)** | `services/sprint.py` — sprint lifecycle management: kickoff → research → prototype → demo → backlog; template-driven; time-boxed task orchestration | Medium (2 sprints) |
| **Industry Accelerators** | `accelerators/` — per-vertical agent presets, prompt packs, workflow templates, KPI dashboards (FS, Energy, Retail) | Large (4-6 sprints) |
| **Client Portal / Self-Service** | `dashboard/client_portal.py` — client-facing read-only dashboard, project status, cost reports, deliverables tracker | Medium (2-3 sprints) |
| **Content & Thought Leadership Engine** | `services/content.py` — automated whitepaper drafts, blog generation, case study templates from project data | Small (1 sprint) |
| **Venture Lifecycle Tracker** | `data/venture_store.py` — ideation → validation → MVP → launch → scale stages; investment/equity tracking; milestone management | Medium (2-3 sprints) |
| **Client Engagement CRM** | Extend `services/client_intake.py` → full CRM: client profiles, engagement history, revenue tracking, renewal management | Medium (2 sprints) |
| **Knowledge Transfer & Training** | `services/training.py` — client team upskilling tracking, learning paths, certification; maps to WeBuild-AI's "Awareness & Education" service | Small (1 sprint) |

---

## 3. Revenue Model Comparison

| Revenue Stream | WeBuild-AI | LSH (Current) | LSH Opportunity |
|---------------|-----------|---------------|-----------------|
| **Consulting fees** | Enterprise day rates + fixed-price sprints | Not tracked as a product | `cli/consulting.py` exists but no pricing/package framework |
| **Platform licensing** | Deliberate AI Toolkit bundled with engagements | Open source (`ai-company` v0.5.1) | Could offer **managed hosting tier** with RBAC + client portals |
| **Venture equity** | Co-build ventures, take equity stakes | No equity tracking | `data/venture_store.py` (new module) |
| **Managed services** | Ongoing platform support + embedded teams | Not modeled | Monthly retainer model via `client` CLI + workflow SLAs |
| **Training & workshops** | "Awareness & Education" service line | Not modeled | `services/training.py` (new module) |

---

## 4. Strategic Recommendation: Priority Order

### Phase 1 — Client Delivery Readiness (1-2 sprints)
1. **Client Portal** — extend dashboard with read-only client view (project status, costs, deliverables)
2. **Strategy Service** — formalize `services/strategy.py` with discovery → roadmap workflow
3. **Sprint Service** — formalize 5-day sprint lifecycle in `services/sprint.py`
4. **Pricing Framework** — add package definitions to `service-catalog-malawi.md` (tiered: Starter / Growth / Enterprise)

### Phase 2 — Industry Verticalization (2-4 sprints)
5. **Industry Accelerators** — agent presets + prompt packs + KPI dashboards for FS, Energy, Retail (or Malawi-focused verticals: Agri, Finance, Telecom)
6. **Venture Lifecycle Tracker** — stage-gated venture management with investment tracking
7. **Training Module** — client upskilling paths and certification

### Phase 3 — Platform Monetization (4-6 sprints)
8. **Multi-tenant Architecture** — client workspace isolation, RBAC per tenant
9. **Managed Hosting Tier** — production deployment with SLA, monitoring, support
10. **Knowledge Marketplace** — shared accelerators, prompt packs, workflow templates across clients

---

## 5. What LSH Already Does Better Than WeBuild-AI

| Capability | LSH Advantage |
|-----------|---------------|
| **Agent Orchestration** | 135 agents, 5-tier approval, ReAct executor, dead-letter queue — WeBuild-AI has no equivalent depth |
| **Governance** | Full audit trail, HITL gates, PII detection, content filtering, encryption at rest — enterprise-grade |
| **Cost Control** | Per-agent/per-model budget enforcement, circuit breaker, rate limiting — WeBuild-AI doesn't expose this |
| **Memory** | 6 memory types + vector search + consolidation scheduler — richer than WeBuild-AI's "Unify" |
| **Open Source** | `ai-company` is open; WeBuild-AI's toolkit is gated behind consulting — LSH can build community |
| **Malawi Market** | Mobile money integration (Airtel, TNM), dual-currency FX — WeBuild-AI has no emerging market presence |

---

## 6. Key Insight

The core strategic opportunity is this: **WeBuild-AI sells a proprietary platform bundled with expensive consultants. LSH can offer the same capabilities as open-source infrastructure + managed services + industry accelerators at a fraction of the cost.**

WeBuild-AI's "80% cost savings at 30% of cost" claim is against traditional IT — LSH could claim **60-70% savings against WeBuild-AI** by being open-source-first with optional managed hosting.
