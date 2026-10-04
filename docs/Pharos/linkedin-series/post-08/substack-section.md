# Substack Section - Post 8: AI Governance in Malawi

**Series:** AI-Native Organizations (11 posts)
**Post:** 8
**Issue:** November digest - "AI-Native Organizations: Use Cases & Governance" (policy brief component)

## Monthly Digest Slice

This issue's policy brief: AI governance in Malawi. The four reservations every SADC institution raises: bandwidth, data, debt, skepticism, mapped to engineering mechanisms, plus the policy landscape those mechanisms must satisfy.

### The Four Reservations, Engineered

**1. "Won't work in low bandwidth."** We operate in this reality daily. Offline-capable runtimes, local models where the workload allows, messaging-native interfaces, PWA queues that buffer until the link returns. Governance version: a Tier-3 review request reaches the named human on the channel they already use, carries the context to decide, and expires through the approval sweep if unanswered. If oversight requires a dashboard nobody can load, you have a screenshot habit, not oversight.

**2. "Where does the data go?"** Malawi's Data Protection Act 2017 (amended 2024) plus GDPR-grade handling as default. Data stays in-country; no foreign-owned models touch personal data without in-country safeguards; model deployments are registered like agents with scope, permissions, and a named owner. The registry is what an auditor reads to answer "who can see what." Data-access actions default to Tier 2 (HITL-approved) or higher; every decision logs who, what, when, and tier.

**3. "Technology debt and lock-in."** A 90-day pilot, no rip-and-replace, no multi-year lock-in, variable cost visible from week one: the cost curve is a dial, not a contract. KPI-003 (Agent Utilization) and KPI-004 (Build Success Rate) are computed from real sources, because a KPI you cannot trace is a KPI you should not quote to a board. And we track our own debt: ADR-032 consolidated stray scripts and session prompts into one registry, the precondition for scaling, not a cleanup project.

**4. "AI failed before."** The answer is not that AI is different now; it is that governance is the product. Five-tier HITL (ADR-017): autonomous → HITL-approved → reviewed → snoozed → cleared. Approval sweep, audit log, circuit breakers, honesty badges: mechanisms, not slogans. Autonomy is earned per action class, never granted at onboarding.

### The Policy Landscape

- **DPA 2017/2024**: the floor for any agent handling personal data
- **MACRA**: answers our gate model gives mechanically: who authorized this action, by name, is it logged, can the principal delegate less tomorrow
- **National AI Strategy consultation**: the moment to argue governance belongs in architecture, not policy documents alone
- **SADC Agentic AI Governance Framework**: a design that satisfies Malawi should travel regionally
- **UNDP and development partners**: fund pilots, so they care most about the 90-day, visible-cost answer

Every one of these asks: who decides, on what basis, how would we know? That is the G layer's design question verbatim. You do not need perfect regulation to install gates: you need a registry, a queue, an approval matrix, and an audit log.

### Key Takeaways

- Treat reservations as design requirements, not objections
- Map each reservation to a mechanism: bandwidth → offline/messaging queues; data → DPA defaults + readable registry; debt → 90-day pilot with visible cost; skepticism → five-tier HITL with audit logs
- Brief the regulator with structure, not slides: show the registry, the approval matrix, and a decision's audit trail
- Governance in the architecture, not in the prompt

### CTA

Download the Malawi Agentic AI Monitor to explore how these patterns apply in-Malawi context.

### Archive Link

Previous issues compile Posts 1–8. Post 9 (measurement frameworks) arrives next; the policy brief for this digest synthesizes Posts 8–10.