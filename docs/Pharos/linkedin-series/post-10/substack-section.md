# Substack Section - Post 10: What Should an AI Agent Decide?

**Series:** AI-Native Organizations (11 posts)
**Post:** 10
**Issue:** November digest - "AI-Native Organizations: Use Cases & Governance" (policy brief component)

## Monthly Digest Slice

This issue's decision-rights brief: what an AI agent may decide alone, what requires a shared call, and what is forbidden outright: the five-tier matrix (ADR-017), the RACI a board reads in one page, and the gate stack that makes it auditable.

### The Five Tiers

| Tier | Name | Agent authority | Human requirement |
|------|------|-----------------|-------------------|
| 1 | Autonomous | Acts without pausing | Audited after |
| 2 | HITL-approved | Proposes; parks in queue | Named human approves first |
| 3 | Reviewed | Executes | Human reviews within SLA |
| 4 | Snoozed | Paused | Human must clear the class |
| 5 | Cleared | Forbidden | Not delegable at all |

Two properties matter more than the labels. **Tiers attach to action classes, not agents** : the same agent is Tier-1 for formatting and Tier-2 for sending, and autonomy is earned per class through measured reliability, never granted at onboarding. **Tier 5 is a wall, not a higher approval** : secret exfiltration, self-modifying governance, unauthorized tier changes, and irreversible external commitments without co-signature are not delegable regardless of performance; a model proposing its own promotion is executing a violation, not making a request.

### The RACI in One Line

The agent is always **Responsible** for execution proposals; the named human is always **Accountable** for anything above Tier 1. One matrix across all departments — the per-department governance dialect is how drift starts. Expired approvals are governance data: the approval sweep moves stale PENDING requests to EXPIRED (terminal, re-submission required), and the expired count tells you whether the human layer is real.

### The Gate Stack (Mechanisms, Not Slogans)

- **Registry**: enumerates agents, scope, permissions
- **Queue**: parks Tier-2+ actions; leases and SLA clocks
- **Approval matrix**: versioned ADR; tiers attach to action classes
- **Approval sweep**: PENDING → EXPIRED, terminal
- **Audit log**: who, what, when, tier, outcome
- **Tool sandbox**: the canonical seven tools bound what any action could do
- **Circuit breakers**: stop runaway loops regardless of tier
- **Honesty badges**: confidence surfaced at the decision point

Regulator questions ("who authorized this, by name, is it logged, can the principal delegate less tomorrow?") are answered by artifacts, not slides.

### What to Copy

- Start new action classes at Tier 2 or Tier 4; promote to Tier 1 only after measured reliability in your own queue
- Write the forbidden list first, cheap to write, expensive to skip
- Wire gates to one queue; approval without a queue is an inbox, a queue without tiers is dispatch
- Publish the expired count weekly

### Key Takeaways

- Decision rights start with purpose (H): every tier is a delegation from a named human authority, never a grant the system gave itself
- G and O are one system: the queue provides timing, the tiers provide permission, the audit log provides proof
- Sandboxes and tiers both fail closed: either one alone leaves an audit finding
- Gates without counters are untested; a matrix with zero escalations has never been exercised

### CTA

Download the Malawi Agentic AI Monitor to explore how these patterns apply in-Malawi context.

### Archive Link

Previous issues compile Posts 1–10. Post 11 (lessons from building LightSpeed) closes the series; the policy brief synthesizes Posts 8–10.