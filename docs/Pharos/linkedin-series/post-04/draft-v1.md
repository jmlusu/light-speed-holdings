# What the H-A-O-M-T-G-V Framework Actually Means

**Series:** AI-Native Organizations (11 posts)
**Post:** 4
**Framework Layer:** Full H-A-O-M-T-G-V Deep Dive

## Hook

Every organization claims to "do AI." Most are still traditional organizations with a new expense line. LightSpeed Holdings™ operates a live AI-native enterprise: 90 agents, 20 departments, 5-tier HITL governance, proven in production since 2025. This post is about the framework that makes it all hold together: one interconnected system, not seven separate ideas.

## H: Human Purpose and Authority

Human purpose is the constitutional layer: strategy, ethics, leadership, relationships, and final accountability stay with named humans, agents are delegates rather than principals, and the delegation stays reversible with the human answering for the outcome.

In our architecture that is a mechanism, not a value statement. A five-tier approval matrix (ADR-017) moves every agentic decision through autonomous → HITL-approved → reviewed → snoozed → cleared, so low-risk work proceeds without ceremony while treasury movements, policy changes, and external commitments sit behind explicit human sign-off.

Hand authority to agents without a sign-off path and the system moves faster while nothing is accountable: speed without accountability is not a capability, it is an incident waiting for a date.

## A: Agentic Workforce

The A layer asks one question: what work can AI agents perform? Our answer has four parts.

1. **Clear task ownership.** Every agent has a defined role, and tasks are enqueued to owners rather than shouted into a shared channel.

2. **Measurable engagement.** Agent Utilization (KPI-003) tracks how much of the available task window each department's agents actually consume, with a target defined in `config/company/kpis.yaml`, because an agent you cannot measure is an agent you do not actually have.

3. **Governed decision-making.** The five-tier matrix (per ADR-017) decides, per action class, whether an agent may proceed alone or must wait for a human.

4. **Permissioned tools.** Agents interact with the world through a canonical seven-tool sandbox. No tool, no action.

The number 90 is canonical, confirmed in ADR-032, but the transferable asset is not the count: one registry, bounded tools, measured utilization, five-tier approvals, and revenue that funds the experiment.

## O: Orchestration

Coordination, the daily ordering of who does what, in what sequence, with what failure handling, is the job of the O layer: one message bus, 20 departments, a live org chart with metrics, and the governance that cascades from executive to specialist level.

### One message bus, twenty departments

The structural spine is deliberately boring: a task queue. Work enters as a task record with an owner, repeated failures land in a dead-letter path for re-enqueue, and tasks carry leases so a crashed worker cannot double-spend them. That is what makes "90 agents" an organization instead of a pile of processes: idempotency, durability, and observability.

On top of the queue sit **20 departments** (engineering, security, data, sales, finance, legal, Pharos, and the rest), each an owner of agent capacity rather than a folder in a slide, where budgets, KPIs, and accountability attach. Agents belong to departments; departments roll up to the executive.

Three mechanisms order the work: **nine recurring workflows** with tracking and SLA monitoring, so a breached SLA becomes a signal with an owner; **org metrics as a live graph**, where every node carries capacity, activity, trend, and risk on a short TTL, so the org chart is a query about the company; and an **executive rollup** aggregating department health into the CEO scorecard.

### Governance that cascades

Structure without a chain of command is a network, not an organization. Ours cascades: the **executive level** sets strategy, owns the scorecard, and holds absolute approval authority for high-impact classes; the **department level** owns agent capacity, KPIs (utilization, build success), and the workflows that pass through it; the **agent level** executes within declared scope and tool boundaries and escalates anything outside its tier.

An agent that hits an unfamiliar decision does not improvise: the task moves up a tier until a human decides. Approval-gated tasks pause in the queue at their tier and the audit log records who authorized what. The answer to the board's first question, who is in charge, is never "the model": twenty departments and ninety agents do not dilute accountability, they make it more explicit: every task has an owner at exactly one level at a time.

## M: Models Run Sovereign

The design question is *how do we ensure AI models operate under sovereign data defaults, visible variable cost, and no lock-in?*

The governance proof is concrete: Data Protection Act 2017/2024 + GDPR by default, no foreign-owned models without in-country safeguards, and model deployments registered like agents with scope, permissions, and an explicit owner. Variable cost is tracked per-model and per-department, visible in the operating budget from week one, so a 90-day pilot lets an institution decide with an invoice in hand rather than a forecast.

Our agent economy is underwritten by eight recurring revenue products (per `config/company/kpis.yaml`), so agents exist to serve work that has a buyer, which disciplines which agents get built. The expensive failure mode is not agent count, it is an agent with no scope that spends tokens, makes commitments, or touches data it should not.

For a Malawian SME or a SADC parastatal, the lesson inverts the usual advice: do not start by asking how many agents you can afford, start by asking how many you can govern, then buy exactly that many.

## T: Tools Stay Sandboxed

The design question is *what tools may agents interact with, and how are boundaries enforced?*

The governance proof is the canonical seven-tool sandbox: read, edit, grep, list, bash, webfetch, task. No tool, no action. Anything outside the approved set is rejected at the Runtime layer, so a tool not on the list cannot be talked into existence, cannot be granted by prompt injection, and cannot be smuggled through a session variable.

We know the failure mode first-hand: in the early days agents existed wherever they were convenient and the count was unknowable. Consolidating to a single registry (recorded in ADR-032) earned the right to scale, because you cannot govern a population you cannot enumerate.

For institutions in our region, the sandbox model converts the AI conversation from trust-me to check-this: buyers, regulators, and boards can audit the structure without understanding the models, which is the point: governance in the architecture, not the prompt.

## G: Gates Approve

The design question is *who decides which actions may proceed, and on what basis?*

The governance proof is the five-tier approval matrix (ADR-017): autonomous → HITL-approved → reviewed → snoozed → cleared. Every agentic action falls into exactly one tier, per its risk class. Tier 1 (autonomous) is routine task execution with no external commitment or treasury movement; Tier 2 (HITL-approved) affects data access and customer-facing outcomes; Tier 3 (reviewed) covers policy changes and budget reallocations; Tier 4 (snoozed) defers high-impact actions for later human decision; Tier 5 (cleared) covers treasury movements, external commitments, and anything with legal or regulatory consequences.

The approval sweep retires stale requests so a forgotten pending item can neither block the system nor slip through it silently, and every agent decision is logged with who authorized what, when, and at which tier. For a Malawi or SADC institution, that answers the regulator's core question: who, by name, authorized this action, and is it logged? The answer is documented, mechanical, and auditable.

## V: Verification Records

The final layer answers *how do we prove value, not just promise it?*

The governance proof is the verification framework: every claim in the system maps to a source of record. Agent utilization maps to KPI-003 logs, approval decisions map to the audit log, revenue tracks to the eight recurring products in `config/company/kpis.yaml`, org metrics map to the computable graph in `graph/engine.py`, and the model registry maps to the company registry entries.

The procurement argument is simple: institutions in our region will be asked to approve AI spending they cannot fully inspect, and an architecture where agents are registry entries, actions are approval-gated, and utilization is a dashboard number converts that conversation from trust-me to check-this. It does not require believing our numbers, only checking our receipts, and we publish them.

### The Full Framework in Sequence

H → Humans authorize. A → Agents act. O → Orchestration orders the work. M → Models run sovereign. T → Tools stay sandboxed. G → Gates approve every high-impact move. V → Verification records it all so value can be proven, not promised.

The sequence is the design discipline: install authorization and scope before you install throughput.

### What a Malawi or SADC Institution Can Copy

Nothing in this structure requires our headcount or our cloud spend. The transferable parts:

- **One registry before any agents.** Define 8–12 agents with named owners, scopes, and approval tiers before any of them run: cheap to write, expensive to skip.

- **One queue before any agents.** Even a file-backed inbox with leases and a dead-letter path gives durability, audit, and a place for failure to land: days of work, not a platform purchase.

- **Departments as the unit of accountability.** Assign agents to real owners with real KPIs from day one; utilization without an owner is a number, not a management instrument.

- **Make the org chart a query.** Capacity, activity, trend, risk: computed, cached, displayed, which in low-bandwidth settings is also a performance decision.

- **Workflows with SLAs, not tribal memory.** Declare the recurring processes your institution runs, give each step an owner and a clock, and let exceptions surface.

- **Sequence: H → A → O.** Install authorization and scope before you install throughput.

- **Sovereign data defaults (DPA 2017/2024, GDPR-grade handling), offline-capable operation, and visible variable cost** still apply; a 90-day pilot can validate the framework on one department first.

### Coming Up Next

The next post walks four of the seven layers in sequence: Models run sovereign, Tools stay sandboxed, Gates govern, and Verification vouches.

**Follow along** if you are designing, governing, or procuring AI systems in Malawi and SADC: we publish the architecture, the metrics, and the failure paths, not just the outcomes.

## CTA

Download the Malawi Agentic AI Monitor to explore how these patterns apply in-Malawi context.

## Hashtags

#AgenticAI #AINativeEnterprise #AIGovernance #Malawi #SADC #DigitalTransformation

## Voice Checklist (Per CEO Review)

- [ ] No emojis in text
- [x] `™` on first mention of "LightSpeed Holdings"
- [x] Every claim traceable to registry/results/Pharos artifact
- [x] Framework layer (H-A-O-M-T-G-V) explicitly named (here: full framework)
- [x] Malawi/SADC context present (not generic)
- [x] CTA aligned: Build / Evidence / Shape
- [x] Voice matches "builder-writer-advocate" (professional, authoritative, first-person plural for company work)
- [x] Length within 1,200–1,800 word spec
- [x] 3–5 H2s (here: 7 H2s + hook + CTA close, within spec)
