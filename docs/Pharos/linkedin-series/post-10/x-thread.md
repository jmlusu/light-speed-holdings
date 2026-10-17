# X Thread — Post 10: What Should an AI Agent Decide?

🧵 "Let the agent handle it" is not a governance strategy. The hardest question in an AI-native org is not how capable the models are — it is which decisions a machine may make alone, which need a human, and which are forbidden outright. The decision-rights matrix, one thread. 🧵

1/7 🪜 Five tiers (ADR-017): 1 Autonomous — acts without pausing, audited after. 2 HITL-approved — proposes, parks in queue. 3 Reviewed — executes, human reviews after. 4 Snoozed — paused pending escalation. 5 Cleared — forbidden, not delegable at all.

2/7 🎯 Two properties matter more than the labels. First: tiers attach to ACTION CLASSES, not agents. The same agent is Tier-1 for formatting and Tier-2 for sending. Autonomy is earned per class through reliability — never granted at onboarding.

3/7 🧱 Second: Tier 5 is not a higher approval — it is a wall. Secret exfiltration. Self-modifying governance. Unauthorized tier changes. Irreversible external commitments without human co-signature. A model that proposes raising its own tier is executing a Tier-5 violation.

4/7 📋 The RACI in one line: the agent is always Responsible for execution proposals; the named human is always Accountable for anything above Tier 1. One matrix across all 20 departments — the per-department dialect is how governance drift starts.

5/7 ⚙️ The gate stack is mechanisms, not slogans: registry, queue, approval matrix (versioned ADR), approval sweep (PENDING → EXPIRED, terminal), audit log, tool sandbox, circuit breakers, honesty badges. Regulator questions are answered by artifacts, not slides.

6/7 📏 Copy this: start new action classes at Tier 2 or Tier 4. Write the forbidden list first (cheap to write, expensive to skip). Publish the expired-approval count — if nobody reports unanswered approvals, the human layer is theater.

7/7 📥 Download the Malawi Agentic AI Monitor to explore how these patterns apply in-Malawi context.

#AIGovernance #DecisionRights #AgenticAI #Malawi #SADC