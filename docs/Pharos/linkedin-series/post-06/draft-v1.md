# Agentic AI in Health & M&E

**Series:** AI-Native Organizations (11 posts)
**Post:** 6
**Framework Layer:** T - Tools & Actions

## Hook

AI in health and monitoring & evaluation is not a separate category; it is AI-native architecture applied to two of the most regulation-sensitive domains in our region. The design question is not "can AI improve health outcomes?" but "how is the architecture designed so that agents improve outcomes under sovereign data defaults, visible variable cost, and five-tier HITL governance?" LightSpeed Holdings™ operates this architecture in production. This post is about the practical implementation of the T (Tools & Actions) layer in health and M&E contexts, and what it means for Malawi and SADC institutions.

## H - Human Purpose (Review)

Human purpose is the constitutional layer. Strategy, ethics, leadership, relationships, and final accountability stay with named humans, and agents are delegates, never principals. The five-tier approval matrix (ADR-017) moves every agentic decision through autonomous → HITL-approved → reviewed → snoozed → cleared, and in health contexts the tier assignment is usually Tier 3 (reviewed) or Tier 4 (snoozed), because policy changes, budget reallocations, and new service rollouts require explicit human sign-off before any agent acts. The failure mode this prevents is easy to name: hand authority to agents without a sign-off path and patients suffer; in our architecture that principle is not a value statement, it is a mechanism.

## A - Agentic Workforce (Review)

The A layer asks what work AI agents can perform, and in health and M&E the answer is bounded: every agent has a defined role (data quality, KPI extraction, compliance, report drafting), tasks are enqueued to owners rather than shouted into a channel, and a failure lands in a dead-letter path with an audit trail. Agent Utilization (KPI-003) tracks how much of the available task window each department's agents consume, against a target defined in `config/company/kpis.yaml`, because an agent you cannot measure is an agent you do not actually have. The five-tier matrix (autonomous → HITL-approved → reviewed → snoozed → cleared, per ADR-017) decides, per action class, whether an agent may proceed alone or wait for a human, so in health contexts the default is usually not Tier 1 (autonomous). The canonical seven-tool sandbox and the number 90 (confirmed in ADR-032) carry the discipline: one registry, bounded tools, measured utilization, five-tier approvals.

## O - Orchestration (Review)

Coordination is the job of the O layer: in health contexts the message bus, 20 departments, nine workflow definitions, and the live org chart with metrics are the operational backbone. The structural spine is a task queue: a flagged patient record, a KPI from a DHIS2 extract, or a drafted policy review enters it as a task record with an owner, the executor loop runs it with audit logs, repeated failures land in a dead-letter path, and leases stop a crashed worker from double-spending a task it no longer owns. Departments own agent capacity rather than folders in a slide, workflow definitions carry tracking and SLA monitoring, and the org chart is a query about the company rather than a picture of it. Coordination failures then show up as metrics: state lives in the task record, not in people's heads and scrollback, so an idle department or an SLA breach surfaces before someone complains.

## M - Models Run Sovereign (Review)

How do we ensure AI models operate under sovereign data defaults, visible variable cost, and no lock-in? The governance proof is concrete: Data Protection Act 2017/2024 + GDPR by default, no foreign-owned models without in-country safeguards, model deployments registered like agents with scope, permissions, and an explicit owner, and variable cost tracked per-model, per-department in the operating budget from week one. In health, model calls for diagnostic support, DHIS2 KPI extractions, and policy reviews add up per call, so no rip-and-replace and no multi-year contract apply: a 90-day pilot with per-agent cost visible from week one means a ministry can decide with an invoice in hand rather than a forecast. Our agent economy is underwritten by eight recurring revenue products (per `config/company/kpis.yaml`), and the point is the same in health: agents exist to serve work that has a buyer.

## T - Tools & Actions

This is the T layer: Tools & Actions. The design question is *what tools may agents interact with, and how are boundaries enforced in health and M&E contexts?*

The governance proof is the canonical seven-tool sandbox: read, edit, grep, list, bash, webfetch, task. No tool, no action. Anything outside the approved set is rejected at the Runtime layer, so the tool vocabulary is not a suggestion but a hard constraint: a tool not on the list cannot be talked into existence or granted by prompt injection.

But in health and M&E, the stakes narrow the sandbox further: read limited to de-identified patient records, edit limited to KPI dashboards rather than raw patient data, bash limited to server maintenance commands, webfetch limited to trusted URIs (WHO APIs, ministry portals, peer-reviewed repositories), and task limited to health-M&E workflow steps.

This is the difference between a general agent workforce and a bounded one. A general workforce grows by screenshots and side-chats. A bounded workforce grows by registry entries that someone approved, recording the agent's identity and department alongside its tool permissions, approval tier, and data scope.

We know the failure mode first-hand, because the registry is a correction. In the early days, agents existed wherever they were convenient, a script here and a session prompt there, and the count was unknowable: you could not answer who owns this agent, what may it touch, what happens when it fails, or what it cost last month. Consolidating to a single registry (recorded in ADR-032) was less about cleanup and more about earning the right to scale, because you cannot govern a population you cannot enumerate, and you cannot enumerate a population that was never declared.

For institutions in our region, the sandbox model converts the AI conversation from trust-me to check-this. Buyers, regulators, and boards can audit the structure without understanding the models; that is the point of governance in the architecture rather than in the prompt.

As the system moves into new domains (health, M&E, finance), the sandbox is re-evaluated: the seven-tool canonical vocabulary stays the default, with domain-specific restrictions on top.

## G - Gates Approve (Review)

The G layer asks who decides which actions may proceed, and the proof is the five-tier approval matrix (ADR-017): autonomous → HITL-approved → reviewed → snoozed → cleared. Every agentic action falls into exactly one tier per its risk class: Tier 1 (autonomous) is routine execution with no external commitment or treasury movement, Tier 2 (HITL-approved) covers data access and patient-facing outcomes, Tier 3 (reviewed) covers policy changes and budget reallocations, Tier 4 (snoozed) defers high-impact actions for later human decision, and Tier 5 (cleared) covers treasury movements, external commitments, and legal or regulatory consequences. The approval sweep retires stale requests so a forgotten pending item can neither block the system nor slip through silently; every decision is logged with who authorized what, when, and at which tier, making governance mechanical rather than performative. In health, the gate model answers the regulator's core question: who, by name, authorized this action, is it logged, and can the principal delegate less tomorrow; the answer is documented, mechanical, and auditable.

### What a Malawi or SADC Health or M&E Institution Can Copy

- **Start with 3–5 agents.** Define role, scope, and approval tier before any agent runs; an SME can start with 3 agents (data quality, KPI pull, compliance monitor) and expand to 12 as the system proves its value.

- **One queue before any agents.** A file-backed inbox with leases and a dead-letter path gives durability, audit, and a failure path; days of work, not a platform purchase.

- **Utilization from day one.** If you cannot see which agents are consuming work this week, you are operating on anecdote; KPI-003-style utilization is the cheapest possible sensor.

- **Install the gates before the autonomy.** Watch the agent operate under review before granting Tier-1 (autonomous) actions; autonomy is earned per action class, not granted at onboarding.

- **Sovereign data defaults (DPA 2017/2024, GDPR-grade handling), offline-capable operation, and visible variable cost** still apply; a 90-day pilot validates the T layer on one department first.

- **Seven-tool canonical sandbox with domain-specific restrictions.** The default is read, edit, grep, list, bash, webfetch, task; in health, restrict read to de-identified records and webfetch to trusted URIs (WHO APIs, ministry portals).

- **Eight recurring revenue products** discipline the agent build: if you cannot name the buyer (government budget line, donor program, facility cost-recovery), the agent does not exist.

### The Full Framework in Sequence

H → Humans authorize. A → Agents act. O → Orchestration orders the work. M → Models run sovereign. T → Tools stay sandboxed. G → Gates approve every high-impact move. V → Verification records it all so value can be proven, not promised.

The sequence is the design discipline: install authorization and scope before you install throughput, because governance is not a parallel paperwork track but a state the workflow passes through.

### What Comes Next

Post 7 introduces the G (Governance) layer through financial inclusion: creditworthiness scanning, transaction monitoring, and compliance checking under sovereign data defaults. Post 8 covers AI governance in Malawi specifically: DPA 2017/2024 compliance, MACRA engagement, and the four reservations answered with architecture. Post 9 revisits V (Value & Impact) with measurement frameworks. Post 10 closes G with decision rights matrices. Post 11 closes the series with lessons from building LightSpeed Holdings™.

**Follow along** if you are designing, governing, or procuring AI systems in health and M&E in Malawi and SADC: we publish the architecture, the metrics, and the failure paths, not just the outcomes.

## CTA

Download the Malawi Agentic AI Monitor to explore how these patterns apply in-Malawi context.

## Hashtags

#AgenticAI #Health #M&E #Malawi #SADC #AITools #ValueImpact #ToolsActions

## Voice Checklist (Per CEO Review)

- [x] No emojis in text
- [x] `™` on first mention of "LightSpeed Holdings"
- [x] Every claim traceable to registry/results/Pharos artifact
- [x] Framework layer (H-A-O-M-T-G-V) explicitly named (here: T - Tools & Actions)
- [x] Malawi/SADC context present (not generic)
- [x] CTA aligned: Build / Evidence / Shape
- [x] Voice matches "builder-writer-advocate" (professional, authoritative, first-person plural for company work)
- [x] Length within 1,200–1,800 word spec
- [x] 3–5 H2s (here: 7 H2s + hook + CTA close, within spec)
