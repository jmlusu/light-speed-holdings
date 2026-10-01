# Feed v1: Post 10 - What Should an AI Agent Decide?

Derived 2026-10-02 from `draft-v1.md` (CEO-approved). Verbatim extracts only - no new claims.

---

"Let the agent handle it" is not a governance strategy. The single hardest question in an AI-native organization is not how capable the models are: it is which decisions a machine is allowed to make alone, which require a shared call with a human in the loop, and which are forbidden outright regardless of how well the system performs. This closes the G (Gates Approve) layer with decision rights: the five-tier matrix our own agents at LightSpeed Holdings™ operate under (ADR-017), and the one-page version a board can read in a single sitting.

The five tiers, exact per ADR-017: autonomous, HITL-approved, reviewed, snoozed, cleared. Tier 1 autonomous acts without pausing and is audited after: routing, formatting, status updates. Tier 2 HITL-approved proposes and parks in the approval queue until a named human approves before execution: data access, external sends, spend. Tier 3 reviewed executes with a human retro review within SLA: customer commitments. Tier 4 snoozed is paused pending escalation, and a human must clear the class: new integrations. Tier 5 cleared is forbidden and not delegable at all: secret exfiltration, self-modifying governance, and irreversible external commitments without human co-signature.

Two properties matter more than the labels. Tiers attach to action classes, not to agents, and autonomy is earned per action class through demonstrated reliability, never granted at onboarding. Tier 5 is not a higher approval; it is a wall. A model that proposes raising its own tier is executing a Tier 5 violation.

The registry is what makes decision rights enforceable at all: 90 agents, 20 departments, each registered with scope and permissions in company-registry.yaml. You cannot attach tiers to actions you cannot enumerate. Gates and queues are one system: without the queue, approval is a screenshot habit; without gates, the queue is just dispatch. The audit log records who approved what, when, and at which tier. Expired approvals are governance data too: the approval sweep transitions stale pending requests to EXPIRED, which means a human did not answer in time. Boards should read that count weekly.

For a Malawi or SADC institution: start at Tier 2 by default and promote to Tier 1 only after measured reliability in your own queue; write the forbidden list first; keep one matrix across departments; publish the expired count; and wire gates to one queue. Approval without a queue is an inbox; a queue without approval tiers is dispatch.

Follow along if you design, govern, or procure AI systems in Malawi and SADC: we publish the architecture, the metrics, and the failure paths, not just the outcomes.

Download the Malawi Agentic AI Monitor to explore how these patterns apply in-Malawi context.

#AgenticAI #AIGovernance #DecisionRights #Malawi #SADC
