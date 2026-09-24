# Chapter — The H-A-O-M-T-G-V Framework: Governing Autonomous AI Agents

**Whitepaper chapter for *Governing Autonomous AI Agents* (2027 flagship, per
`docs/Pharos/content-calendar.md`).** Companion to Funding Treatise I (*The
H-A-O-M-T-G-V Governance Framework for Central Banks & Regulators*, referenced
in `src/components/ProofShowcase.tsx`).

**Status:** Draft for review. **Register:** policy / regulator-facing.

---

## 1. The problem: autonomy without a constitution

An autonomous AI agent is software that acts. It plans, calls tools, executes
transactions, and coordinates with other agents. That capacity changes the
character of the risk an institution carries: from *output risk* (what the AI
prints) to *action risk* (what the AI does, spends, commits, and signs on
behalf of whom).

Most governance frameworks written before agentic systems still govern outputs:
they set accuracy targets, publish usage guidelines, and review logs after the
fact. This chapter specifies a governance architecture for agents that **act**.
It is organized as seven layers, H-A-O-M-T-G-V, each with a design question, a
deployed control, a failure mode if omitted, and the institutional checkpoint a
regulator can apply.

The framework is not theoretical in origin. It is the operating constitution of
LightSpeed Holdings, a company run by a workforce of 90 agents across 20
departments under five-tier human-in-the-loop approvals, with immutable audit
trails. Every control named here is fielded in production.

## 2. Design principles

Five principles govern the layers that follow.

1. **Human accountability is non-delegable.** Delegation of execution is not
   delegation of responsibility. A named human principal remains the final
   accountable party for every high-impact action.
2. **Sovereignty is architectural, not aspirational.** Data and inference stay
   in-country unless a documented, approved cross-border flow exists.
3. **Minimum scope.** Agents are bounded in role, in permission, and in tool
   access. "Can" is not a default; it is a granted, reviewable property.
4. **Control precedes execution.** Approval is evaluated before an external
   write event fires, not reconstructed from logs after it.
5. **Proportionality.** Controls scale with risk. Advisory output faces lighter
   gates than a system that moves money or releases personal data.

## 3. The seven layers

Each layer states its control, its technical instantiation, and the failure it
prevents.

### H — Human Purpose & Authority

**Control.** Named humans hold final accountability for strategy, ethics,
leadership, relationships, and irreversible decisions. High-impact actions,
treasury disbursements, and policy changes require cryptographic human
sign-off.

**Instantiation.** A five-tier approval matrix; an approval gate that sweeps
expired `PENDING` requests to `EXPIRED` so stale or blocked items cannot drift
into execution.

**Failure prevented.** Autonomy without accountability — an agent acting where
no human is answerable.

**Institutional checkpoint.** Does the institution maintain a named principal
for each agent-assigned authority? Is sign-off cryptographic and logged?

### A — Agentic Workforce

**Control.** The agent population is a countable, documented roster. Each agent
has a defined domain, a permission boundary, and a deterministic escalation
path when work exceeds its scope.

**Instantiation.** Registry-defined personas (152 in the source deployment),
compiled mechanically into runtime agent cards; role-bounded subagents;
RACI-based reporting chains.

**Failure prevented.** An undifferentiated "AI" that no one can enumerate,
bound, or audit.

**Institutional checkpoint.** Can the institution produce the full agent
roster, each agent's scope of authority, and its permitted actions? What
happens when an agent is asked to exceed its scope?

### O — Orchestration & Organization

**Control.** Agent work is observable and sequentialized through a message bus:
every task has an owner, a lifecycle, and a failure path. The organization
itself is encoded as computable topology, so department boundaries, budgets,
and data classifications are enforceable schema, not prose.

**Instantiation.** JSON task queues, dead-letter handling and replay, policy
schemas aligned to the Malawi Data Protection Act 2017/2024 and King IV.

**Failure prevented.** Parallel agents colliding, duplicate work, and an org
structure that exists only on paper.

**Institutional checkpoint.** Where is a task born, who owns it until
completion, and what happens on failure? Are the institution's boundaries
enforceable in the system, or only in memos?

### M — Model & Memory

**Control.** Two obligations under one pillar. Inference runs on sovereign
infrastructure in-country with zero telemetry leakage to third-party public
clouds. The organization maintains structured institutional memory so decisions
and lessons persist.

**Instantiation.** On-soil runtimes with fallback models behind a router and
circuit breaker; multi-type memory store wired into the execution recall loop.

**Failure prevented.** Claimed sovereignty contradicted by offshore inference;
an organization that forgets its own decisions between tasks.

**Institutional checkpoint.** Where is the model physically running? What
leaves the jurisdiction? How is institutional knowledge retained and made
recoverable for audit?

### T — Tools & Actions

**Control.** Agents act only through a closed canonical tool vocabulary. There
is no arbitrary code execution and no action surface the governance layer
cannot enumerate.

**Instantiation.** Seven canonical primitives — `read`, `edit`, `grep`, `list`,
`bash`, `webfetch`, `task` — validated at runtime; unknown tools rejected;
legacy aliases excluded from new agent definitions.

**Failure prevented.** A model that can "do anything," including actions the
institution does not know exist.

**Institutional checkpoint.** Enumerate the agent's action surface. Who
certified each tool? What is the default when a tool is not on the list?

### G — Governance & Policy

**Control.** Policy is code applied before execution. Thresholds, budgets, and
regulatory covenants are evaluated pre-write; runaway loops are halted
programmatically.

**Instantiation.** Policy engine, five-tier approval state machine
(`PENDING` / `APPROVED` / `REJECTED` / `EXPIRED`), circuit breakers, rate
limits, and the approval-gate expiry sweep.

**Failure prevented.** Post-hoc review presented as governance.

**Institutional checkpoint.** Are controls applied before execution or after?
What thresholds trip which gates? Who authorizes the policy code, and when was
it last audited?

### V — Verification & Value

**Control.** Every prompt, tool invocation, human decision, and API response is
immutably recorded. Outcomes are measured and reported as evidence, with drift
telemetry signaling when a model degrades.

**Instantiation.** SHA-256 hash-chain audit trails; continuous evaluation;
dashboard KPI collectors; honest-status reporting of claims.

**Failure prevented.** An untraceable system reporting unverifiable success.

**Institutional checkpoint.** Produce the trail for a given action. Is each
reported KPI measured or marketed? Can a third party verify the trail?

## 4. Cross-mapping to regional instruments

| Instrument | Alignment in H-A-O-M-T-G-V |
|------------|-----------------------------|
| Malawi Data Protection Act (2017/2024) | M-layer sovereignty (in-country processing), A/O-layer boundaries on processing, V-layer trails for lawful-processing evidence |
| AU Continental AI Strategy | Positioning of institutional memory and human oversight as African AI-leadership capabilities; sovereignty pillar as deployment norm |
| SADC digital transformation agenda | O-layer interoperability of task/data definitions across member states; sandbox readiness in G-layer |
| King IV (governance) | H-layer (accountable leadership), G-layer (policy and delegation of authority), V-layer (transparent reporting) |
| GDPR (extraterritorial touchpoint) | Sovereign-first default with documented cross-border flows; data-minimization via minimum-scope (A/T layers) |

The mapping is deliberately bidirectional: each instrument is a requirements
source, and each layer is a capability an institution can inspect.

## 5. Obligations for adopting institutions

A regulator need not specify H-A-O-M-T-G-V's internal implementation. It
should require its substance, stated as institutional obligations:

1. Maintain and publish an up-to-date **agent roster** with scopes and
   permissions (A).
2. Maintain a **named-human accountability register** for every
   agent-assigned authority (H).
3. Demonstrate **pre-execution control**: show that high-impact actions cannot
   fire without an approved gate (G).
4. Demonstrate **sovereign custody**: state where inference runs and what, if
   anything, crosses the border (M).
5. Demonstrate **action-surface enumeration**: the set of tools an agent may
   call, and the rejection of anything outside it (T).
6. Produce **an actionable audit trail** for any nominated action on demand
   (V).
7. Show **consequence handling**: what the system does on failure, on expiry,
   and on rate-limit breach (O, G).

These obligations hold regardless of the underlying technology. That is the
point of a governance framework for autonomy: it binds the operating system,
not the vendor.

## 6. Assurance and future work

Three assurance tracks extend this chapter:

- **Independent verification.** Third-party auditors reproduce a nominated
  action's trail from the hash chain end-to-end.
- **Drift evaluation.** Model behavior is re-evaluated continuously so the
  framework governs a system whose capabilities change.
- **Regional sandbox.** A multi-agent regulatory sandbox (per the SADC draft
  framework) lets institutions pilot the G-layer controls under observation
  before policy is fixed.

Treatise I extends this chapter to the central-banking context, including
threshold calibration for monetary and treasury operations. This framework is
intended as the common platform beneath both documents.

---

*Companion to `docs/Pharos/h-a-o-m-t-g-v-framework.md` (canonical reference)
and the SADC Agentic AI Governance Framework draft.*
