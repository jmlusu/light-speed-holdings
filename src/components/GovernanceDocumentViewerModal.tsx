import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  X, 
  Copy, 
  Check, 
  Download, 
  BookOpen, 
  FileText, 
  ShieldCheck, 
  Compass, 
  Landmark, 
  Briefcase, 
  Zap, 
  CheckCircle2, 
  Search,
  ExternalLink,
  ChevronRight,
  Terminal,
  Cpu,
  Layers,
  HelpCircle,
  Clock,
  DollarSign
} from 'lucide-react';
import { StatusLedPip, MachineScrewHead } from './TactileHardwareElements';

export interface GovernanceDoc {
  id: string;
  title: string;
  subtitle: string;
  category: 'constitution' | 'decision' | 'runbook' | 'reservations' | 'service-catalog' | 'skills';
  version: string;
  date: string;
  owner: string;
  status: string;
  icon: React.ReactNode;
  content: string;
}

export const GOVERNANCE_DOCUMENTS: GovernanceDoc[] = [
  {
    id: 'doc-constitution',
    title: 'AI Company Constitution',
    subtitle: '10 Core Principles, Escalation Matrix & Chain of Command',
    category: 'constitution',
    version: '1.0',
    date: '2026-09-12',
    owner: 'Human CEO & Chief of Staff',
    status: 'ACTIVE & AUTHORITATIVE',
    icon: <Landmark className="w-5 h-5 text-amber-500" />,
    content: `# AI Company Constitution

## Purpose

Build world-class AI-native companies where one human CEO supervises AI executives, managers, and specialists. Automate 70-90% of routine knowledge work while maintaining human oversight at every critical decision point.

## Principles

### Customer First
Every decision starts with the impact on the end customer. If a shortcut helps us but hurts the customer, we don't take it.

### Truth over Opinion
Decisions are based on data and evidence, not hierarchy or preference. An analyst with data outranks an executive with a hunch.

### Evidence over Assumptions
Before acting, gather evidence. If evidence is unavailable, state the assumption explicitly and plan to validate it.

### Simple over Complex
Choose the simplest solution that works. Complexity is a cost — it must justify itself.

### Automation before Manual Work
If a task is repeatable and rule-based, automate it. Human time is reserved for judgment, creativity, and oversight.

### Documentation before Memory
Write it down. Individual memory fades; documentation compounds. If it isn't written, it doesn't exist.

### Quality before Speed
Ship it right, then ship it fast. Rework costs more than patience.

### Security by Design
Security is not a layer added at the end. It is built into every system, every permission, every data flow from the start.

### Continuous Improvement
Every incident, every failure, every postmortem is a chance to get better. We never waste a good mistake.

### Ownership with Accountability
Every task has one owner. Ownership means you are responsible for the outcome, not just the output.

## Decision Order

Decisions flow through a clear chain of command. Each level can decide within its authority; anything beyond requires escalation.

\`\`\`
human-ceo          Final authority on all matters
    │
chief-of-staff     Operational coordination, interim authority
    │
┌───┼───┐
cto  cfo  coo     Executive-level decisions within department
    │
┌───┴───┐
dept heads         Department-level decisions, specialist oversight
    │
specialists        Task-level execution within defined scope
\`\`\`

**Rule:** If you are unsure whether you have authority, you don't. Escalate.

## Escalation

When a situation exceeds your authority or expertise, escalate immediately. Never sit on a problem.

\`\`\`
specialist          First responder — assess and attempt resolution
    │ (if unresolved or exceeds authority)
executive          Department-level decision-making
    │ (if exceeds department scope)
chief-of-staff     Cross-department coordination
    │ (if business-critical or irreversible)
human-ceo          Final call
\`\`\`

**SLA:** Escalations must be acknowledged within 15 minutes during operational hours.

## Company Values

| Value | What It Means in Practice |
|-------|--------------------------|
| **Integrity** | We do what we say. No hidden agendas, no shortcuts that compromise trust. |
| **Transparency** | Decisions and their reasoning are documented and accessible. No black boxes. |
| **Learning** | We invest in understanding why things work, not just making them work. |
| **Innovation** | We challenge assumptions and explore better ways, even when the current way is "fine." |
| **Execution** | Ideas are cheap. Delivery is what matters. We bias toward action. |
| **Customer Success** | Our success is measured by the customer's success, not our activity. |

## Amendments

This constitution may be amended by the human CEO with advisory input from the Chief of Staff. Amendments require:
1. Written proposal with rationale
2. Impact assessment on existing operations
3. 7-day review period before taking effect.`
  },
  {
    id: 'doc-decision-framework',
    title: 'Company Decision Framework',
    subtitle: '10-Step Protocol, Semantic Memory Logging & Approval Matrix',
    category: 'decision',
    version: '1.0',
    date: '2026-09-12',
    owner: 'Chief of Staff',
    status: 'ACTIVE ENFORCED',
    icon: <Compass className="w-5 h-5 text-amber-500" />,
    content: `# Company Decision Framework

Every significant decision must follow this framework. It ensures consistency, traceability, and accountability across all levels of the organization.

## When to Use This Framework

Use this framework when the decision:
- Affects more than one department
- Involves spending over $100 or equivalent token budget
- Is irreversible or difficult to undo
- Touches security, permissions, or data access
- Sets a precedent for future decisions

For small, reversible decisions within a single specialist's scope, document the choice in the task result — no formal framework needed.

## The 10-Step Framework

### 1. Problem Statement
One sentence. What is broken, missing, or suboptimal?

> *Example: "The orchestrator runs on-demand only, requiring manual triggering every 6 hours."*

### 2. Root Cause
Why does this problem exist? What is the underlying reason, not just the symptom?

> *Example: "No scheduling infrastructure was implemented during the orchestration milestone."*

### 3. Alternatives Considered
List at least two options, including "do nothing." For each, state the tradeoff.

| Option | Approach | Tradeoff |
|--------|----------|----------|
| A | GitHub Action with cron schedule | Simple, free, but limited to 6h intervals |
| B | Long-running daemon process | More flexible, but requires hosting |
| C | Do nothing (manual trigger) | No cost, but unsustainable at scale |

### 4. Recommendation
State the recommended option clearly. Explain why it wins over the alternatives.

> *Example: "Option A — GitHub Action. It is the simplest path that meets the requirement, requires no infrastructure, and can be upgraded to Option B later."*

### 5. Risks
What could go wrong? For each risk, state the likelihood and mitigation.

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| GitHub Actions outage | Low | Medium | Manual trigger as fallback |
| Cron misconfiguration | Medium | Low | Test in staging first |

### 6. Costs
What does this cost? Include token budget, compute, human time, and opportunity cost.

> *Example: "Zero ongoing cost. 2 hours of implementation time."*

### 7. Benefits
What do we gain? Quantify where possible.

> *Example: "Eliminates 4 manual triggers per day. Saves ~10 minutes of human time daily."*

### 8. Timeline
When will this be done? What are the milestones?

| Milestone | Target |
|-----------|--------|
| Implementation | Day 1 |
| Testing | Day 1 |
| Deployment | Day 2 |

### 9. Dependencies
What must be true before this can proceed? What does this block?

> *Example: "Requires orchestrator tick command (already implemented). Blocks nothing."*

### 10. Next Actions
Concrete, owned, time-bound steps.

| Action | Owner | Due |
|--------|-------|-----|
| Create \`autonomous.yml\` workflow | cto | Day 1 |
| Test cron schedule in fork | cto | Day 1 |
| Update STATUS.md | chief-of-staff | Day 2 |

## Decision Records

Every decision using this framework should be saved as a decision record in the memory engine:

\`\`\`bash
ai-company memory add --type semantic --content "Decision: [title]. Recommendation: [option]. Rationale: [brief reason]."
\`\`\`

## Approval Matrix

Decisions are classified by scope and require corresponding approval:

| Scope | Approver | Examples |
|-------|----------|---------|
| Task-level | Self (specialist) | Code style, file organization |
| Department-level | Executive | Tool selection, workflow changes |
| Cross-department | Chief of Staff | Architecture changes, new integrations |
| Business-critical | Human CEO | Budget, security, public-facing changes |`
  },
  {
    id: 'doc-op16-runbook',
    title: 'OP-16: One-Day Operating Proof Runbook',
    subtitle: 'Pre-flight, Budget Guardrails, Task Batch & Execution Sequence',
    category: 'runbook',
    version: '1.0',
    date: '2026-08-14',
    owner: 'Chief of Staff & Executor Lead',
    status: 'PLANNED PROOF',
    icon: <Terminal className="w-5 h-5 text-amber-500" />,
    content: `# OP-16: One-Day Operating Proof — Runbook

**Issue**: #16 (Run the one-day operating proof)
**Blocked by**: #15 (configured guardrails) — **status: satisfied** (\`config/company/guardrails.yaml\`)
**Status**: PLANNED — awaiting human sign-off before any LLM spend

## 1. Objective

Prove the executor + dashboard + memory + scheduler loop works end-to-end on the local Windows daemon: seed a small batch of safe tasks, let the executor process them under budget caps, verify the supporting cycles (daily briefing, KPI snapshot, governance retention, memory recall/consolidation), capture live dashboard + WebSocket state, and record what works / what breaks. Pass → gate #17 (sustained cadence).

**Scope change from the ticket**: #16 originally proposed working "existing pending inbox tasks" — the inbox was purged in Sprint 8 (\`.opencode/inbox.json\` is \`[]\`), so the proof seeds a small controlled batch instead of the old stale placeholders.

## 2. Pre-flight (no spend)

1. \`uv run ai-company executor status\` → expect "no daemon" + \`Total tasks: 0\`.
2. Confirm \`.opencode/inbox.json\` is \`[]\`; \`logs/\` exists.
3. **Provider reachability** — the executor needs at least one configured provider. Standard tier tries \`GEMINI_API_KEY\` → \`OPENCODE_API_KEY\` → local \`ollama\`. Check at least one is present in the environment (do not print the value).
4. \`scripts/backup.ps1\` → snapshot of \`.opencode/\`, \`company/\`, \`results/\`.
5. Port check: \`8421\` free for the dashboard (isolated from prod \`8420\`).
6. **Canary**: seed + tick ONE trivial task (see §4) via a single \`executor tick\` — proves provider auth end-to-end before the daemon run. Abort if the canary fails; diagnose provider config first.

## 3. Guardrails & budget

Loaded automatically from \`config/company/guardrails.yaml\` by \`_resolve_budgets\`:

| Cap | Value | Enforced |
|-----|-------|----------|
| Daily LLM budget | $2.00 USD | \`CostTracker.daily_budget_exceeded()\` + auto-suspend (\`suspend_daily\`) |
| Per-task budget | $0.50 USD | \`AgentLoop.check_budget()\` per iteration |
| Overspend action | suspend for rest of day | \`Executor.tick()\` returns 0 |

**Stop conditions**: task budget per task; daily budget for the whole run; manual abort (§7). Expected spend for the batch: ≤ ~$0.10 with a cheap model.

## 4. Task batch (3 read-only, standard-tier, no HITL parking expected)

Seeded via \`MessageBus.send_task\` (python one-liner), \`sender_id: human-ceo\`, \`priority: MEDIUM\`:

| # | Receiver | Instruction (self-contained, read-only) |
|---|----------|------------------------------------------|
| T1 | \`technical-documentation-lead\` | Read \`docs/STATUS.md\`; return a 5-bullet summary of current project state and the three biggest risks. Do not modify any files. |
| T2 | \`chief-of-staff\` | Read \`docs/TASK-BOARD.md\` and \`.opencode/inbox.json\`; report open task count and priority distribution. Do not modify any files. |
| T3 | \`threat-intelligence-analyst\` | Analyze \`.opencode/audit\` for error-level entries in the last 7 days; summarize recurring patterns. Do not modify any files. |

Rationale: read-only analysis tasks avoid \`write\`/\`bash\` tools so the tier-rules HITL gate (\`require_approval_from_tier: 2\`) should not park them. If a task does park: \`uv run ai-company orchestrator approval-approve <request_id>\`.

## 5. Execution sequence (the run)

1. Seed T1–T3 into the inbox.
2. \`uv run ai-company executor start --daemon --governance-interval 60\` (short retention interval so governance runs within the proof window; budgets auto-load from guardrails config).
3. Verify lifecycle: \`logs/executor-daemon.pid\` + \`logs/executor-daemon.json\` written; \`uv run ai-company executor status\` shows \`state: running\`.
4. Wait for task completion (poll \`executor status\`; expected minutes).
5. \`uv run ai-company orchestrator briefing\` → regenerates \`.opencode/daily_briefing.md\`.
6. Start dashboard: \`uv run ai-company dashboard --port 8421 --no-open\`; confirm \`GET /api/v1/...\` health + live task events over WebSocket.
7. Confirm KPI snapshot ran (daemon \`kpi-snapshot-interval\` 300s) and governance retention executed without error.
8. Stop daemon: \`uv run ai-company executor stop\`; re-run \`executor status\` → \`state: stopped\`, no orphan \`python\` executor process.

## 6. Success criteria (from #16)

- [ ] Daemon lifecycle: start → PID/status file → running → graceful stop.
- [ ] ≥2 of 3 tasks COMPLETED with \`results/{task_id}/loop_result.json\` artifacts; no unexpected DLQ entries (\`executor dlq-list\`).
- [ ] Cost tracking: usage recorded (cost log), per-task ≤ $0.50, daily ≤ $2.00.
- [ ] Daily briefing regenerated.
- [ ] KPI snapshot collected.
- [ ] Governance retention ran without error.
- [ ] Dashboard live on 127.0.0.1:8421 with WebSocket task updates.
- [ ] Memory recall ran before execution; outcomes recorded; consolidation ticked.

## 7. Rollback / abort

- **Abort run**: \`uv run ai-company executor stop\` (foreground: Ctrl+C).
- **Abort dashboard**: Ctrl+C on the uvicorn process.
- **Budget trip**: auto-suspend halts processing for the day (reset = next calendar day or manual cost reset — documented, no data loss).
- **Post-proof cleanup**: purge test tasks from the inbox (restore \`[]\`), keep \`results/*\` as evidence; optionally archive the batch under \`docs/archive/2026-08-13-op16-proof/\`.

## 8. Evidence to capture

\`logs/executor-daemon.log\`, \`logs/executor-daemon.json\` (final state), \`results/*/loop_result.json\`, \`.opencode/audit\`, cost export JSONL, \`.opencode/daily_briefing.md\`, dashboard health + WS observations, final \`executor status\` + \`dlq-list\` output. Summarized into the #16 issue.

**Timezone note**: all evidence timestamps are UTC — ISO-8601 with an explicit \`+00:00\` offset.

## 9. Gate outcome

- **PASS** (all green or minor fix-list): close #16 → plan #17 cadence from what worked.
- **PARTIAL** (core loop works, some cycle fails): log blockers, fix-list, targeted retry.
- **FAIL** (nothing executes end-to-end): diagnose top blocker (provider auth, config path, daemon file perms), then re-plan.

## 10. Risks & mitigations

| Risk | Mitigation |
|------|-----------|
| No provider key / auth failure | Pre-flight canary catches before any run; circuit breaker isolates provider |
| HITL parking blocks a task | Read-only task set; approve via \`orchestrator approval-approve\` if needed |
| Budget runaway | Hard $0.50/task + $2/day caps + auto-suspend (config-enforced) |
| Daemon orphan process | \`executor stop\` + verify PID gone; fallback \`Stop-Process\` by PID file |
| Dashboard port clash | Proof uses 8421 (prod is 8420) |`
  },
  {
    id: 'doc-reservations-strategy',
    title: 'Trust-by-Engineering: The Four Reservations Strategy',
    subtitle: 'Answers to Low-Bandwidth, Data Protection, Tech Debt & AI Skepticism',
    category: 'reservations',
    version: '1.0',
    date: '2026-09-11',
    owner: 'Office of the CEO (Reservations Council)',
    status: 'APPROVED STRATEGY',
    icon: <ShieldCheck className="w-5 h-5 text-amber-500" />,
    content: `# LightSpeed Holdings — Trust-by-Engineering: The Four Reservations Strategy

**Document Version:** 1.0
**Date:** September 11, 2026
**Owner:** Office of the CEO (Reservations Council)
**Approved by:** human-ceo (via board-strategy stress test)
**Companion docs:** \`docs/MISSION_AND_VISION.md\` (v2.0), \`docs/MALAWI_FOCUS_ALIGNMENT.md\` (v1.0)

---

## 1. Purpose

LightSpeed Holdings is positioned as the organization that genuinely understands — and credibly answers — the reservations decision-makers hold about AI in low-bandwidth, resource-constrained environments. This document is the source of truth for that answer doctrine. It defines:

1. The **four reservations** and our credible, honesty-badged answers.
2. The **engineering evidence** behind each answer.
3. The **capability DNA** that gives the answers depth (institutional, unnamed).
4. The **team** (Reservations Council) that owns and refreshes the doctrine.
5. How the answers flow into **demos** and **Pharos**.

## 2. The Four Reservations

| # | Reservation | The question behind it |
|---|-------------|------------------------|
| 1 | **Low-bandwidth / resource-constrained** | "This won't work on our devices, our connectivity, or our electricity reality." |
| 2 | **Data protection** | "Where does our data go? Does it leave our country?" |
| 3 | **Technology debt** | "Won't this rip out what we have — or become a system we must maintain forever?" |
| 4 | **Skepticism of AI** | "We tried AI before and it failed. Why would this be different, and how do we trust it?" |

## 3. Capability DNA (institutional, unnamed)

| Capability DNA | Reservation(s) it answers |
|----------------|---------------------------|
| Process-optimization engineering foundation — "every workload is a process to optimize; bandwidth is a budget, latency is a constraint we engineer to" | 1. Low-bandwidth |
| Enterprise data architecture across Fortune 500 telecom, finance, and healthcare estates — ETL, warehousing, and legacy integration at scale | 2. Data protection, 3. Technology debt |
| Public-sector regulatory delivery — defining product requirements inside regulated frameworks | 2. + 4. Trust |
| Development-sector M&E authority — global-health data systems delivered in low-connectivity field settings | 1. + 4. Trust |

## 4. The Answer Doctrine

### 4.1 Reservation 1 — Low-bandwidth / resource-constrained
> We design for the reality. Offline-first architecture, local inference via free models when connectivity or budget demands it, WhatsApp-native interfaces with no app download, and a PWA that queues work offline and syncs on reconnect. Traffic is routed quota-first on weak connections.

*Honesty badge:* **Proven in-house**

### 4.2 Reservation 2 — Data protection
> Your data stays on your infrastructure. Sovereign in-country processing is the default; every cross-border flow to an LLM provider is documented in our governance gate process and routed to the most privacy-preserving option. Malawi Data Protection Act 2017/2024 and GDPR are built in from day one. We never use client data to train models.

*Honesty badge:* **Proven in-house**

### 4.3 Reservation 3 — Technology debt
> Adopting AI should not mean ripping out what works. We integrate with your existing stack via API connectors during a 90-day pilot, we do not add a second system you must maintain, and your data and deliverables stay under your control — no lock-in.

*Honesty badge:* **Fieldable in 2026**

### 4.4 Reservation 4 — Skepticism of AI
> Most AI failures in this region are governance failures, not technology failures — a chatbot that hallucinates, a tool that violates data sovereignty, a system with no audit trail. We are governance-first: 5-tier human-in-the-loop approvals, immutable audit trails, risk-classified agent tiers, circuit breakers, red-team testing, and evaluation gates.

*Honesty badge:* **Proven in-house**

## 5. The Reservations Council

CSO, Board-Strategy, Chief of Staff, LLM Platform Owner, Capacity Planner, Platform Reliability Engineer, Mobile Developer, Data Privacy Officer, CISO, Compliance Officer, VP Engineering, Software Architect, Solution Architect, AI Ethics Officer, AI Safety Lead, Red-Team Engineer, Eval Benchmarks Engineer, Thought Leadership Lead, Solutions Engineer, Sales Owner.`
  },
  {
    id: 'doc-service-catalog',
    title: 'LightSpeed Malawi Service Catalog v1.0',
    subtitle: '5 Core Offers (A-E), MWK/USD Rates, Delivery SOP & 90-Day Roadmap',
    category: 'service-catalog',
    version: '1.0',
    date: '2026-08-12',
    owner: 'Human CEO & Sales Owner',
    status: 'PROPOSED & READY',
    icon: <Briefcase className="w-5 h-5 text-amber-500" />,
    content: `# Light Speed Holdings — Malawi Service Catalog

**Version:** 1.0 (draft for validation)
**Date:** 2026-08-12
**Owner:** human-ceo
**Status:** PROPOSED — pricing anchors to be validated with 2–3 real prospects before publishing

---

## 1. Positioning

Light Speed Holdings operates as an **AI-first services studio** in Malawi. One human CEO directs a workforce of **135+ AI agents** (executives, engineers, designers, writers, analysts, sales, support) to deliver client work through a defined delivery pipeline:

\`\`\`
client brief → inbox task → assigned agent(s) → human CEO review → client deliverable
\`\`\`

## 2. Offer Portfolio

### Offer A — Digital Presence (website + branding)

| Deliverable | What you get | Starting price | Turnaround |
|-------------|--------------|----------------|------------|
| **A1 — Business Website** | Up to 5 pages, mobile-first, contact form, WhatsApp button, hosting setup | MWK 800,000 (≈ $450) | 5–10 days |
| **A2 — E-commerce / Online store** | Product catalog, Airtel Money / Mpamba checkout integration, order alerts | MWK 1,800,000 (≈ $1,000) | 10–15 days |
| **A3 — Brand identity** | Logo, color system, fonts, social media kit, letterhead | MWK 500,000 (≈ $280) | 3–5 days |
| **A4 — Google Business + listings** | Map listing, business info management, review setup | MWK 150,000 (≈ $85) | 2–3 days |

### Offer B — Business Process Automation (BPA)

| Deliverable | What you get | Starting price | Turnaround |
|-------------|--------------|----------------|------------|
| **B1 — WhatsApp/customer chatbot** | FAQ + order/service automation on WhatsApp Business, human handoff | MWK 1,500,000 (≈ $850) + MWK 100k/mo | 7–14 days |
| **B2 — AI document/report generator** | Template-driven report generation (donor reports, payroll letters) | MWK 1,200,000 (≈ $680) | 7–14 days |
| **B3 — Form + survey automation** | Kobo/Google-Forms-to-spreadsheet pipeline, summary dashboards | MWK 900,000 (≈ $500) | 5–10 days |
| **B4 — Internal tool / dashboard** | Custom web dashboard for tracking stock, sales, students, or patients | MWK 2,500,000 (≈ $1,400) | 10–20 days |

### Offer C — Data, Analytics & Donor Reporting (The Differentiator)

| Deliverable | What you get | Starting price | Turnaround |
|-------------|--------------|----------------|------------|
| **C1 — Data cleaning & analysis** | Clean dataset + insights report (Excel/PDF) | MWK 700,000 (≈ $400) | 3–7 days |
| **C2 — Donor/project reports** | Narrative + data-visualized quarterly/annual reports compliant with donor templates | MWK 1,000,000 (≈ $550) | 5–10 days |
| **C3 — Interactive dashboard** | Live web dashboard for program KPIs (mobile-friendly, NGO-grade) | MWK 2,000,000 (≈ $1,100) | 10–15 days |
| **C4 — Survey design + analysis** | Questionnaire design, data collection setup, analysis | MWK 1,300,000 (≈ $720) | 7–14 days |

### Offer D — Digital Marketing

| Deliverable | What you get | Starting price | Turnaround |
|-------------|--------------|----------------|------------|
| **D1 — Social media management** | Content calendar, 12 posts/month, community management | MWK 350,000/mo (≈ $200/mo) | Ongoing |
| **D2 — Content pack** | 10 blog articles + 20 social captions | MWK 600,000 (≈ $340) | 5–10 days |
| **D3 — Google/Facebook ads setup** | Campaign setup, pixel, tracking, 2-week optimization | MWK 700,000 (≈ $400) + ad spend | 3–5 days |

### Offer E — Platform (Product Path)

| Deliverable | What you get | Price | Turnaround |
|-------------|--------------|-------|------------|
| **E1 — AI Company Builder license** | Onboarding, your own agent company running on your laptop/VPS | MWK 3,500,000 (≈ $2,000) + MWK 350k/mo | Setup 1–2 weeks |
| **E2 — Agent setup for agencies** | White-label agent team setup for agencies | Contact for quote | Custom |

## 3. Pricing & Payment Rules

- **50% upfront / 50% on delivery** for all one-off projects.
- **USD quotes** for NGO/international clients. **MWK quotes** for local SMEs.
- **Payment rails**: Airtel Money, TNM Mpamba, PayChangu, Bank Transfer.
- **Express delivery**: +40% surge for ≤50% standard turnaround.

## 4. Legal & Compliance Checklist (Malawi)

- [x] Business Registration Act compliance (Registrar General)
- [x] MRA Taxpayer Identification Number (TIN) & VAT registration
- [x] Airtel Money & TNM Mpamba merchant verification
- [x] Data Protection Act 2017/2024 compliance & privacy disclosures`
  },
  {
    id: 'doc-skill-policy',
    title: 'OpenCode Skill Curation Policy v1.0',
    subtitle: 'Vetting Checklist, CLI Installation, Directory Structure & 38 Skill Inventory',
    category: 'skills',
    version: '1.0',
    date: '2026-08-07',
    owner: 'Chief of Staff',
    status: 'ACTIVE GOVERNED',
    icon: <Cpu className="w-5 h-5 text-amber-500" />,
    content: `# Skill Curation Policy

**Version:** 1.0
**Date:** 2026-08-07
**Owner:** Chief of Staff
**Status:** Active

---

## Purpose

This document defines the policy for adding, vetting, and managing skills in the OpenCode agent ecosystem without modifying \`AGENTS.md\`. Skills are auto-discovered from \`.agents/skills/\` — this policy governs *which* skills enter that directory and *how*.

## Governance Model

| Role | Responsibility |
|------|----------------|
| **Chief of Staff** | Owns this policy, approves additions, runs monthly audits |
| **Registry Owner** | Executes vetting checklist, runs \`skill-check\`, updates manifests |
| **Generator Owner** | Validates skill format compatibility with OpenCode |
| **QA Lead** | Tests skill activation in fresh sessions |

## Skill Discovery Mechanism

> **OpenCode scans \`.agents/skills/\` at session start.** No \`opencode.json\` required. \`AGENTS.md\` is a human guide only — never read by the runtime.

## Vetting Checklist (Mandatory for Every New Skill)

1. **Identity & Collision Check**: Name unique, kebab-case, no semantic collisions.
2. **Format Validation**: Valid \`SKILL.md\` with frontmatter (\`name\`, \`description\`, \`mode\`, \`tools\`, \`permissions\`).
3. **License & Source**: MIT, Apache-2.0, or CC0 permissive licenses.
4. **Security Audit**: Code inspection, zero prompt injections, zero unauthorized network calls.
5. **Dependency Check**: Verified against standard CLI toolchain.

## Current Skill Inventory (38 Skills)

- **Original 28 Antigravity Skills**: \`agenttrace-session-audit\`, \`api-endpoint-builder\`, \`brooks-lint\`, \`bug-hunter\`, \`tdd\`, \`technical-change-tracker\`, \`triage\`, etc.
- **Added Tier-1 Skills (Addy Osmani Bundle)**: \`spec-driven-development\`, \`planning-and-task-breakdown\`, \`incremental-implementation\`, \`code-review-and-quality\`, \`security-and-hardening\`, \`git-workflow-and-versioning\`, \`ci-cd-and-automation\`, \`documentation-and-adrs\`, \`observability-and-instrumentation\`, \`shipping-and-launch\`.
- **Meta-Skill**: \`using-agent-skills\` (auto-routing lifecycle engine).`
  }
];

interface GovernanceDocumentViewerModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialDocId?: string;
  onOpenContactModal?: (intent?: string) => void;
  theme?: 'light' | 'dark';
}

export const GovernanceDocumentViewerModal: React.FC<GovernanceDocumentViewerModalProps> = ({
  isOpen,
  onClose,
  initialDocId = 'doc-constitution',
  onOpenContactModal,
  theme = 'dark'
}) => {
  const isLight = theme === 'light';
  const [selectedDocId, setSelectedDocId] = useState<string>(initialDocId);
  const [copied, setCopied] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const selectedDoc = GOVERNANCE_DOCUMENTS.find(d => d.id === selectedDocId) || GOVERNANCE_DOCUMENTS[0];

  const filteredDocs = GOVERNANCE_DOCUMENTS.filter(doc => 
    doc.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    doc.subtitle.toLowerCase().includes(searchQuery.toLowerCase()) ||
    doc.owner.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleCopy = () => {
    navigator.clipboard.writeText(selectedDoc.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([selectedDoc.content], { type: 'text/markdown' });
    element.href = URL.createObjectURL(file);
    element.download = `${selectedDoc.id}_${selectedDoc.title.replace(/[^a-zA-Z0-9]/g, '_')}.md`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-4 sm:p-6 lg:p-8 font-sans">
        {/* Backdrop */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="fixed inset-0 bg-black/85 backdrop-blur-md"
        />

        {/* Modal Window */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className={`relative w-full max-w-6xl rounded-3xl border shadow-2xl overflow-hidden z-10 max-h-[92vh] flex flex-col ${
            isLight ? 'bg-slate-50 border-slate-300 text-slate-800' : 'bg-[#090d16] border-amber-500/30 text-zinc-100'
          }`}
        >
          {/* Header */}
          <div className={`p-5 sm:p-6 border-b flex items-center justify-between shrink-0 ${
            isLight ? 'bg-white border-slate-200' : 'bg-zinc-950/90 border-amber-500/20'
          }`}>
            <div className="flex items-center gap-3">
              <StatusLedPip status="emerald" isLight={isLight} />
              <div>
                <span className="text-[10px] font-mono text-amber-500 font-extrabold uppercase tracking-widest block">
                  LIGHTSPEED GOVERNANCE & ARCHITECTURE REPOSITORY
                </span>
                <h2 className={`text-base sm:text-xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  Institutional Governance &amp; Operating Documents
                </h2>
              </div>
            </div>

            <button
              onClick={onClose}
              className={`p-2 rounded-xl border transition-all cursor-pointer ${
                isLight ? 'neu-btn-light text-slate-700 hover:text-red-600' : 'neu-btn-dark text-zinc-400 hover:text-amber-400'
              }`}
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Main Content Layout: Sidebar + Document Render */}
          <div className="flex flex-col md:flex-row flex-1 overflow-hidden">
            
            {/* Sidebar Navigator */}
            <div className={`w-full md:w-80 border-r p-4 flex flex-col gap-3 shrink-0 overflow-y-auto ${
              isLight ? 'bg-slate-100/70 border-slate-200' : 'bg-zinc-950/60 border-zinc-800'
            }`}>
              
              {/* Search Box */}
              <div className="relative">
                <Search className="w-4 h-4 text-zinc-400 absolute left-3 top-2.5" />
                <input
                  type="text"
                  placeholder="Filter documents..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className={`w-full pl-9 pr-3 py-1.5 rounded-xl border text-xs font-mono focus:outline-none ${
                    isLight 
                      ? 'bg-white border-slate-300 text-slate-900 focus:border-amber-500' 
                      : 'bg-zinc-900 border-zinc-700 text-zinc-100 focus:border-amber-500'
                  }`}
                />
              </div>

              <span className="text-[10px] font-mono font-bold text-amber-500 uppercase tracking-wider px-1">
                AVAILABLE GOVERNANCE SPECIFICATIONS ({filteredDocs.length})
              </span>

              {/* Doc List */}
              <div className="space-y-2 flex-1">
                {filteredDocs.map((doc) => {
                  const isSelected = doc.id === selectedDocId;
                  return (
                    <button
                      key={doc.id}
                      onClick={() => setSelectedDocId(doc.id)}
                      className={`w-full text-left p-3 rounded-xl border transition-all flex items-start gap-3 cursor-pointer ${
                        isSelected 
                          ? 'bg-amber-500/15 border-amber-500 text-amber-300 shadow-md' 
                          : isLight 
                            ? 'bg-white border-slate-200 hover:border-amber-400 text-slate-700' 
                            : 'bg-zinc-900/50 border-zinc-800/80 hover:border-zinc-700 text-zinc-300'
                      }`}
                    >
                      <div className="mt-0.5 shrink-0">{doc.icon}</div>
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center justify-between gap-1 mb-0.5">
                          <span className="text-xs font-bold font-display truncate">{doc.title}</span>
                          <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 font-bold shrink-0">
                            v{doc.version}
                          </span>
                        </div>
                        <p className="text-[10px] text-zinc-400 line-clamp-2 leading-relaxed">{doc.subtitle}</p>
                      </div>
                    </button>
                  );
                })}
              </div>

              {/* Quick Action Footer */}
              {onOpenContactModal && (
                <button
                  onClick={() => {
                    onClose();
                    onOpenContactModal(`Consultation on ${selectedDoc.title}`);
                  }}
                  className="w-full py-2.5 px-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-black font-mono text-xs uppercase tracking-wider transition-all flex items-center justify-center gap-2 shadow-md cursor-pointer"
                >
                  <Briefcase className="w-3.5 h-3.5" />
                  <span>Request Governance Review</span>
                </button>
              )}
            </div>

            {/* Document Details & Reader */}
            <div className="flex-1 flex flex-col overflow-hidden">
              
              {/* Document Sub-Header Toolbar */}
              <div className={`px-6 py-3 border-b flex flex-wrap items-center justify-between gap-3 text-xs font-mono shrink-0 ${
                isLight ? 'bg-white border-slate-200 text-slate-700' : 'bg-zinc-900/80 border-zinc-800 text-zinc-300'
              }`}>
                <div className="flex items-center gap-3">
                  <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 font-bold border border-emerald-500/30">
                    {selectedDoc.status}
                  </span>
                  <span className="hidden sm:inline text-zinc-500">•</span>
                  <span className="hidden sm:inline text-zinc-400">Owner: {selectedDoc.owner}</span>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={handleCopy}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 border-amber-500/30 transition-all font-bold cursor-pointer"
                  >
                    {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    <span>{copied ? 'Copied Markdown' : 'Copy Spec'}</span>
                  </button>

                  <button
                    onClick={handleDownload}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold transition-all shadow-md cursor-pointer"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>Download .MD</span>
                  </button>
                </div>
              </div>

              {/* Markdown Document Render Panel */}
              <div className="p-6 sm:p-8 overflow-y-auto space-y-6 flex-1 text-xs leading-relaxed font-sans">
                
                {/* Document Banner */}
                <div className={`p-5 rounded-2xl border ${
                  isLight ? 'bg-amber-50 border-amber-200' : 'bg-gradient-to-r from-amber-950/20 via-zinc-900 to-zinc-950 border-amber-500/30'
                }`}>
                  <div className="flex items-center gap-3 mb-2">
                    {selectedDoc.icon}
                    <h1 className="text-xl sm:text-2xl font-extrabold font-display text-amber-500">
                      {selectedDoc.title}
                    </h1>
                  </div>
                  <p className="text-xs text-zinc-400 font-mono mb-3">{selectedDoc.subtitle}</p>
                  <div className="flex flex-wrap items-center gap-4 text-[11px] font-mono text-zinc-400 border-t border-amber-500/20 pt-2.5">
                    <span><strong>Version:</strong> v{selectedDoc.version}</span>
                    <span>•</span>
                    <span><strong>Date:</strong> {selectedDoc.date}</span>
                    <span>•</span>
                    <span><strong>Authority:</strong> LightSpeed Holdings Governance Board</span>
                  </div>
                </div>

                {/* Preformatted Spec Content */}
                <div className={`p-6 rounded-2xl border font-mono whitespace-pre-wrap overflow-x-auto ${
                  isLight ? 'bg-white border-slate-300 text-slate-800' : 'bg-zinc-950 border-zinc-800 text-zinc-200'
                }`}>
                  {selectedDoc.content}
                </div>

              </div>

              {/* Document Footer */}
              <div className={`p-3.5 border-t flex items-center justify-between text-[11px] font-mono shrink-0 ${
                isLight ? 'bg-slate-100 border-slate-200 text-slate-600' : 'bg-zinc-950 border-zinc-800 text-zinc-400'
              }`}>
                <span>LIGHTSPEED HOLDINGS LIMITED // GOVERNANCE SUITE</span>
                <span className="text-emerald-400 font-bold flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  VERIFIED FIDUCIARY SPECIFICATION
                </span>
              </div>

            </div>

          </div>

        </motion.div>
      </div>
    </AnimatePresence>
  );
};
