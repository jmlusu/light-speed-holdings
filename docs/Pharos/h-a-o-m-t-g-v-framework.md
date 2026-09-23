# The H-A-O-M-T-G-V Agentic Governance Framework

**Canonical reference document.**

**Owner:** Pharos, on behalf of the Human CEO.
**Status:** Live. Reconciles every earlier description of the framework (Pharos
positioning, manifesto, LinkedIn long-form, and the corporate website) into a
single, simplified exposition.
**Audience:** Anyone who needs to explain or defend the framework — the CEO,
Pharos writers, sales, the reservations desk, and the Lighthouse pilot teams.

---

## 1. The one-line simplification

H-A-O-M-T-G-V is the seven-layer constitution of an AI-native enterprise:

> **Humans authorize. Agents act. Orchestration orders the work. Models run
> sovereign. Tools stay sandboxed. Gates approve every high-impact move. And
> verification records it all — so value can be proven, not promised.**

Each letter is one pillar. No pillar is optional, and no pillar can be swapped
for another. That is what makes it a framework and not a slogan.

**Memory line (one phrase per letter):**

| Letter | One phrase |
|--------|------------|
| H | Humans Authorize |
| A | Agents Act |
| O | Orchestration Orders |
| M | Models Run Sovereign |
| T | Tools Stay Tamed |
| G | Gates Govern |
| V | Verification Vouches |

---

## 2. Two registers, one framework

Earlier materials described H-A-O-M-T-G-V two different ways, which looked like
a contradiction. It was not. The same seven letters carry two registers:

| Register | What it names | Where it lives | Question it answers |
|----------|---------------|----------------|---------------------|
| **Design register** | Seven design questions for building an AI-native enterprise | `docs/Pharos/positioning.md:41-52`, manifesto, LinkedIn intro | *What should we build and why?* |
| **Proof register** | Seven deployed governance mechanisms | `src/components/MethodFramework.tsx:40-97`, corporate site | *What did we actually build to make it safe?* |

The resolution: **every layer has a design question and a governance proof.**
The framework only works when both are present. Design without proof is a
PowerPoint. Proof without design is a tool you cannot teach.

| Letter | Design question | Governance proof (what we actually run) |
|--------|-----------------|-----------------------------------------|
| H | What do humans remain accountable for? | 5-tier cryptographic approval gates; executive committee and board keep absolute authority; no high-impact action without human sign-off |
| A | What work can agents perform? | 90 role-bounded personas defined in `company-registry.yaml`, each with explicit domain scope and permission boundary |
| O | How do agents coordinate and how is the org structured? | Message bus at `.opencode/inbox.json`, task graphs, department topologies encoded as computable policy schemas |
| M | How does the organization run models and learn? | Sovereign, on-soil model runtimes (Big Pickle, Gemini, DeepSeek fallbacks) with zero telemetry leakage; six-type enterprise memory |
| T | How do agents interact with the world? | Canonical 7-tool sandbox; ToolRunner rejects anything outside `read` · `edit` · `grep` · `list` · `bash` · `webfetch` · `task` |
| G | How do we control agents? | 5-tier human-in-the-loop gates, policy engine, circuit breakers, HITL expiry sweeps (PENDING → APPROVED / REJECTED / EXPIRED) |
| V | What outcomes and proof are produced? | SHA-256 immutable audit chains, drift telemetry, KPI collectors — outcomes reported as evidence, not opinion |

---

## 3. The seven pillars

Each pillar is elaborated as: the question, what it means, the proof, the
failure mode if it is neglected, and what a regulator or client should check.

### H — Human Purpose & Authority

**The question.** What should humans remain accountable for?

**What it means.** The constitutional layer. Strategy, ethics, leadership,
relationships, and final accountability stay with named humans. Agents are
delegates, never principals; the delegation is reversible and the human is the
one who answers for the outcome.

**The proof.** A 5-tier approval matrix. Low-risk work proceeds; high-impact
actions, treasury disbursements, and policy changes sit behind cryptographic
human sign-off. An `ApprovalGate` sweeps expired `PENDING` approvals so a stale
request never blocks the system (or sneaks through). The human is the last line
of code in the organization.

**Failure mode.** Handing authority to agents without a sign-off path. The
system moves faster and nothing is accountable.

**Regulator check.** Who, by name, authorized this action? Is the authorization
logged cryptographically? Can the principal delegate less tomorrow?

### A — Agentic Workforce

**The question.** What work can AI agents perform?

**What it means.** A roster of discrete, role-bounded agent personas. Each agent
has an explicit domain scope, a declared tool permission set, and a
deterministic escalation path. The roster is the org chart of the machine side
of the house — readable, auditable, and reproducible.

**The proof.** 90 personas in `company-registry.yaml`, compiled by a Jinja2
generator into OpenCode agent cards (`.opencode/agents/*.md`) with strict
subagent sandboxing. 20 departments, defined reporting chains, RACI matrices.

**Failure mode.** Unbounded or implicit agents — "the AI" as a single magic
worker that no one can enumerate, scope, or audit.

**Regulator check.** Can you produce the full roster? Is every agent's scope and
permission boundary documented? What happens when a task exceeds that scope?

### O — Orchestration & Organization

**The question.** How do agents coordinate, and how is the organization
structured?

**What it means.** Agents do not improvise in parallel. Work moves through a
message bus as JSON tasks (`.opencode/inbox.json`), with task graphs, retry and
dead-letter handling, and observable lifecycles. Alongside the runtime, the
organization itself is expressed as computable topology: departments, budgets,
and data-classification matrices encoded as schemas rather than policy PDFs.

**The proof.** MessageBus task queue, executor loop, dead-letter replay for
`platform_reliability_engineer`, policy-as-code department schemas aligned to
Malawi DPA 2017/2024 and King IV governance principles.

**Failure mode.** Agents talking past each other, duplicate work, or an org
chart that exists in a deck but nowhere executable.

**Regulator check.** Where is a task born? Who owns it? What happens on failure?
Is the org structure itself enforceable, or only aspirational?

### M — Model & Memory

**The question.** How does the organization run models and learn?

**What it means.** Two distinct things share this pillar and are both required.
First, **model sovereignty**: inference runs in-country on sovereign runtimes —
air-gapped or national cloud — with no telemetry leaking to third-party public
clouds. Second, **enterprise memory**: the organization accumulates decisions,
context, and lessons learned in a structured store (six memory types in this
implementation) so it does not relearn what it already knows.

**The proof.** Big Pickle primary with Gemini and DeepSeek as fallbacks, routed
by a model router with a circuit breaker and cost tracker; on-soil deployment
compatibility; a typed memory store wired into the executor recall loop.

**Failure mode.** Running the model overseas while claiming sovereignty, or
building a system that forgets everything between tasks.

**Regulator check.** Where is the model physically running? What leaves the
jurisdiction? Can the organization answer the same question twice without
re-work, and does it record how?

### T — Tools & Actions

**The question.** How do agents interact with the world?

**What it means.** Agents act only through a closed, canonical tool vocabulary.
No arbitrary code execution, no hidden network calls, no gateways the governance
layer cannot see. Every action is one of a small set of verified primitives, so
"what can this agent do?" always has a finite, reviewable answer.

**The proof.** Seven canonical tools: `read`, `edit`, `grep`, `list`, `bash`,
`webfetch`, `task`. Runtime `ToolRunner` validation rejects unapproved calls and
legacy aliases (`write`, `execute`, `delegate`, `web_search`) are not admitted
into newly generated agent cards.

**Failure mode.** A model that can "do anything," including things the
governance layer does not know exist.

**Regulator check.** Enumerate the agent's tools. Who certified each one? What
happens if the agent tries an eighth?

### G — Governance & Policy

**The question.** How do we control agents?

**What it means.** Control is pre-execution, not post-mortem. Every agent
proposal is evaluated against thresholds, spending budgets, and regulatory
covenants before external write events fire. The rules are coded, not hoped
for: policy-as-code, an approval matrix, circuit breakers for runaway loops.

**The proof.** 5-tier approval gates with deterministic state transitions
(`PENDING` → `APPROVED` / `REJECTED` / `EXPIRED`), policy engine, rate limits,
circuit breakers, and the `ApprovalGate` expiry sweep that keeps stale requests
from blocking the inbox.

**Failure mode.** Review after the fact. "We check the logs next quarter" is not
governance; it is archaeology.

**Regulator check.** Is control applied before execution? What thresholds trip
which gates? Who wrote the policy, and when was it last audited?

### V — Verification & Value

**The question.** What outcomes and proof are produced?

**What it means.** Every prompt, tool invocation, human decision, and API
response is logged to cryptographic hash chains. Audit is a byproduct of
operation, not a separate exercise. On top of the trail, value is measured:
revenue, cost, productivity, service delivery, and social impact, reported by
KPI collectors and drift telemetry with honest status.

**The proof.** SHA-256 immutable audit chains; continuous evaluation and model
drift telemetry; dashboard KPI collectors; the honesty-badge discipline of the
Four Reservations doctrine (claims carry their verified status).

**Failure mode.** An untraceable black box claiming success. Trust in an AI
system without an audit trail is a mood, not a fact.

**Regulator check.** Produce the audit trail for any action. Is the KPI claimed
measured, or marketed? Can a third party verify the trail independently?

---

## 4. The governance core (cross-cutting mechanics)

Five mechanisms recur across the pillars and deserve their own section, because
they are what converts the framework from a diagram into an operating system.

1. **The 5-tier approval state machine.** High-stakes actions traverse explicit
   gates. States are deterministic and terminal: `PENDING`, `APPROVED`,
   `REJECTED`, `EXPIRED`. Expiry is actively swept so stale items cannot block
   or bypass. (See `security-compliance-lead`, `decision-engine-owner`,
   `ApprovalGate`.)
2. **The canonical 7-tool boundary.** The complete tool vocabulary is closed.
   ToolRunner validates at runtime and rejects unknown tools. Legacy aliases are
   backward-compatible only and never appear in newly generated agent cards.
   (AGENTS.md §8.)
3. **Policy-as-code.** Department boundaries, budgets, and data-classification
   matrices are schemas, not prose. It aligns with regional instruments (Malawi
   DPA 2017/2024, King IV) and makes "is this allowed?" a query, not a meeting.
4. **Sovereign inference.** Models run on-soil with fallback routing and
   circuit breakers. Sovereignty is a deployment property, not a promise.
5. **Immutably audited everything.** SHA-256 hash chains, drift telemetry, and
   KPI evidence make verification a byproduct of running the company.

---

## 5. Proof map (where each claim lives in the repo)

| Pillar | Grounding in the codebase |
|--------|---------------------------|
| H | `ApprovalGate`; `security-compliance-lead`; 5-tier approval matrix docs |
| A | `company-registry.yaml`; `templates/agents/agent.md.j2`; `.opencode/agents/*.md` |
| O | `src/ai_company/orchestrator/message_bus.py`; `.opencode/inbox.json`; `orchestration-owner` |
| M | `llm-platform-owner` (model router, cost tracker); `memory-owner` (six-type memory store) |
| T | AGENTS.md §8 canonical tool table; `ToolRunner` validation; `registry-owner` |
| G | Policy engine; `decision-engine-owner`; circuit breakers; `ApprovalGate` HITL sweep |
| V | Audit-trail package (`audit-trail-owner`); dashboard KPI collectors (`dashboard-owner`); drift evaluation |

---

## 6. Using the framework

**The briefing ladder.** Say less when the room knows less; keep all seven
pillars in every version.

| Level | Version | Fits |
|-------|---------|------|
| 0 | "Governed agentic AI — human-led, machine-executed, fully audited." | Elevator, one breath |
| 1 | The one-line simplification (section 1). | Introductions, LinkedIn |
| 2 | The seven questions (table in section 2). | Demos, reservations desk |
| 3 | Section 3, pillar by pillar. | Workshops, diligence |
| 4 | The whitepaper chapter (`docs/Pharos/whitepaper/`). | Policy and regulator rooms |

**The objections hook.** In a skeptical room, open with the failure mode column,
not the proof column. Regulators and risk officers have seen the failures; the
proofs are the answer to objections they already hold.

**The three-pillar narrative.** H-A-O-M-T-G-V is Company Builder evidence.
Section 6 of the manifesto shows how the same material serves Use Cases and
Policy. Never present the framework apart from the proof stack that earned it.

---

## 7. Sources and honesty

This document is canonical relative to earlier drafts. Earlier sources remain
valid for their specific claims:

- Design register: `docs/Pharos/positioning.md:41-52`
- Proof register: `src/components/MethodFramework.tsx:40-97`
- Manifesto narrative: `docs/Pharos/manifesto-draft.md:108-124`
- LinkedIn intro: `docs/Pharos/linkedin-intro-post.md:23-25`

If a later draft of this document contradicts a source above, this document
wins and the source should be updated. Figures quoted (90 agents, 20
departments, 5-tier gates, 7 tools, SHA-256) are verified against
`company-registry.yaml` and the agent roster at generation time.
