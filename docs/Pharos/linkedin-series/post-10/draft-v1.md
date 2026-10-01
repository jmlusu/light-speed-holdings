# What Should an AI Agent Decide?

**Series:** AI-Native Organizations (11 posts)
**Post:** 10
**Framework Layer:** G - Gates Approve

## Hook

"Let the agent handle it" is not a governance strategy. The single hardest question in an AI-native organization is not how capable the models are: it is which decisions a machine is allowed to make alone, which require a shared call with a human in the loop, and which are forbidden outright regardless of how well the system performs. LightSpeed Holdings™ operates this architecture in production. This post closes the G (Gates Approve) layer with decision rights: the five-tier matrix our own agents operate under (ADR-017), a RACI view of who decides what, and the one-page version a board can read in a single sitting. The design question: what may the agent decide?

## H - Human Purpose (Review)

Decision rights start with purpose. The H layer (Posts 1, 5) holds that strategy, ethics, leadership, relationships, and final accountability belong to named humans, so every tier in the matrix is ultimately a delegation *from* a human authority, not a grant the system gave itself. If no human can name the owner of a decision class, the class does not exist: it falls to the top tier, or it is forbidden.

The practical consequence for measurement: expired approvals are governance data, not noise. The approval sweep transitions stale PENDING requests to EXPIRED (AGENTS.md §9.1), and an EXPIRED request means a human did not answer in time; the tier held, but the human layer lagged. Boards should read that count weekly.

## A - Agentic Workforce (Review)

The A layer (Posts 2, 5) defined the workforce: 90 agents, 20 departments, each registered with scope and permissions in `company-registry.yaml`. The registry is what makes decision rights enforceable at all: you cannot attach tiers to actions you cannot enumerate, and you cannot enumerate actions without knowing which agents exist and what they may touch.

The workforce question that matters for gates: agents propose, humans dispose. Every agent action passes through the same approval surface regardless of department (sales, legal, finance, marketing), because a per-department governance dialect is exactly the drift the matrix exists to prevent. One matrix, applied uniformly, audited centrally.

## O - Orchestration (Review)

The O layer (Posts 3, 5) queued the work: tasks carry leases, failures land in a dead-letter path, SLA clocks run per workflow step. For decision rights, orchestration contributes the *timing* dimension: a Tier-1 (autonomous) action executes inside the queue without pausing; a Tier-2 (HITL-approved) action parks in the approval queue until a human responds or the request expires.

This is why gates and queues are one system, not two. Without the queue, approval is a screenshot habit; without gates, the queue is just dispatch. The audit log records who approved what, when, and at which tier: the artifact an auditor reads to answer "who authorized this action, by name, is it logged?"

## M - Models Run Sovereign (Review)

The M layer (Posts 4, 5) kept models in-country and registered. For decision rights, sovereignty adds a veto class: data-access decisions default to Tier 2 (HITL-approved) or higher, and no model, domestic or foreign, can promote its own tier. Tier assignment is a human configuration in the approval matrix, versioned like any other ADR; a model rollout that would silently raise autonomy is, by definition, a change that requires an approval the model cannot grant itself.

Cost governance rides the same rails: spend thresholds are decision classes too. An agent may transact within an approved envelope; exceeding it escalates to a named human (Tier 2 or 3 depending on materiality).

## T - Tools Stay Sandboxed (Review)

The T layer (Posts 6, 7) bounded agents to the canonical seven tools: read, edit, grep, list, bash, webfetch, task, with domain restrictions on top. This is the *mechanical* half of decision rights: even a Tier-1 autonomous action can only touch what the tool surface permits. `bash` in a restricted namespace cannot exfiltrate; `edit` cannot rewrite the approval matrix; `task` cannot spawn an agent outside the registry.

The pairing is the design: tiers decide *whether* an action runs; the tool sandbox decides *what* an action could ever do. Both must fail closed. An unrestricted tool with perfect approval tiers is one prompt injection away from an audit finding.

## V - Value & Impact (Review)

The V layer (Posts 9) measured the gates: decisions by tier, escalations, expired approvals, audit completeness. Decision rights without those counters are untested: a matrix that has never recorded a single escalation has never been exercised. The instrumentation question for this post: can your organization report, this week, how many actions ran autonomously, how many required a human, and how many expired unanswered?

## G - Gates Approve

This is the G layer's core contribution: the decision-rights matrix.

### The Five Tiers (ADR-017)

| Tier | Name | Agent authority | Human requirement | Typical actions |
|------|------|-----------------|-------------------|-----------------|
| 1 | Autonomous | Acts without pausing | None at execution; audited after | Format normalization, routing, drafting internal notes, routine status updates |
| 2 | HITL-approved | Proposes; parks in queue | Named human approves before execution | External sends above threshold, data access, spend within envelope |
| 3 | Reviewed | Executes; human reviews after | Retro review within SLA | Customer commitments, contract language, policy-facing text |
| 4 | Snoozed | Paused pending escalation | Human must clear the class | New integrations, novel action classes, anomaly-flagged work |
| 5 | Cleared | Forbidden | Not delegable at all | Secret exfiltration, self-modifying governance, unauthorized tier changes, irreversible external commitments without human co-signature |

The sequence, **autonomous → HITL-approved → reviewed → snoozed → cleared**, is exact per ADR-017. Two properties matter more than the labels:

1. **Tiers attach to action classes, not to agents.** The same agent is Tier-1 for formatting and Tier-2 for sending. Autonomy is earned per action class through demonstrated reliability, never granted at onboarding.
2. **Tier 5 is not a higher approval; it is a wall.** Some actions are not delegable regardless of performance. A model that proposes raising its own tier is executing a Tier-5 violation.

### The RACI View

One page a board can read:

| Decision class | Agent | Named human (owner) | Escalation | Consulted |
|----------------|-------|---------------------|------------|-----------|
| Routine internal ops (routing, formatting, status) | R/A (Tier 1) | I (audited) | - | - |
| External sends, data access, spend in envelope | R (proposes) | **A** (approves, Tier 2) | C | - |
| Customer commitments, contract language | R (drafts) | **A** (Tier 3 review) | C | Legal/finance as needed |
| New integrations, novel action classes | R (proposes) | **A** (Tier 4 clear) | C | CTO/security |
| Tier-5 forbidden actions | - (no authority) | **A** (never delegable) | I | CISO/CEO |
| Governance changes (matrix, registry, tiers) | - (cannot self-modify) | **A** (CEO/CTO per ADR) | I | Board where material |

Reading: the agent is always the **Responsible** party for execution proposals; the named human is always **Accountable** for anything above Tier 1; escalation and consultation are per-class. R = Responsible, A = Accountable, C = Consulted, I = Informed.

### The Gate Stack (mechanisms, not slogans)

- **Registry**: enumerates agents, scope, permissions (the denominator for everything)
- **Queue**: parks Tier-2+ actions; carries leases and SLA clocks
- **Approval matrix**: versioned ADR; attaches tiers to action classes
- **Approval sweep**: expires stale PENDING → EXPIRED (terminal; re-submission required)
- **Audit log**: who, what, when, tier, outcome
- **Tool sandbox**: bounds what any action could do, even when approved
- **Circuit breakers**: stop runaway loops regardless of tier
- **Honesty badges**: surface model confidence/uncertainty at the point of decision

Every one of these exists as code or config in our stack: the mechanisms a regulator asks about ("who authorized this, is it logged, can the principal delegate less tomorrow?") are answered by artifacts, not slides.

### What a Malawi or SADC Institution Can Copy

- **Start at Tier 2 by default.** New action classes begin snoozed (Tier 4) or HITL-approved (Tier 2); promote to Tier 1 only after measured reliability in your own queue, never by vendor promise.
- **Write the forbidden list first.** Tier 5 is cheap to write and expensive to skip: secret exfiltration, self-modifying governance, unauthorized tier changes, irreversible external commitments without co-signature.
- **One matrix across departments.** The per-department dialect is how drift starts.
- **Publish the expired count.** If nobody reports unanswered approvals, the human layer is theater.
- **Wire gates to one queue.** Approval without a queue is an inbox; a queue without approval tiers is dispatch.

### The Full Framework in Sequence

H → Humans authorize. A → Agents act. O → Orchestration orders the work. M → Models run sovereign. T → Tools stay sandboxed. G → Gates approve every high-impact move. V → Verification records it all.

Post 9 showed how the verification layer counts these decisions. This post showed where the decisions are allowed to originate. Post 11 closes the series with lessons from building LightSpeed, including the decisions we got wrong before the matrix existed.

### What Comes Next

Post 11 closes the series: lessons from building LightSpeed: the consolidation, the reliability failures, and the honesty badges, told first-person with the numbers attached.

**Follow along** if you design, govern, or procure AI systems in Malawi and SADC: we publish the architecture, the metrics, and the failure paths, not just the outcomes.

## CTA

Download the Malawi Agentic AI Monitor to explore how these patterns apply in-Malawi context.

## Hashtags

#AgenticAI #AIGovernance #DecisionRights #Malawi #SADC

## Voice Checklist (Per CEO Review)

- [x] No emojis in text
- [x] `™` on first mention of "LightSpeed Holdings"
- [x] Every claim traceable to registry/results/Pharos artifact (ADR-017 tiers, AGENTS.md §9.1 sweep, seven-tool vocabulary)
- [x] Framework layer (H-A-O-M-T-G-V) explicitly named (here: G - Gates Approve)
- [x] Malawi/SADC context present (not generic)
- [x] CTA aligned: Build / Evidence / Shape
- [x] Voice matches "builder-writer-advocate" (professional, authoritative, first-person plural for company work)
- [x] Length within 1,200–1,800 word spec
- [x] 3–5 H2s (here: layer sections + matrix/RACI/stack/copy/next, within spec)
