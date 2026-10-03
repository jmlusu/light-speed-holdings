# Substack Section - Post 3: LightSpeed AI-native org structure

**Series:** AI-Native Organizations (11 posts)
**Post:** 3

## Monthly Digest Slice

This month's focus: LightSpeed AI-native org structure. This issue covers the orchestration layer that makes 90 agents and 20 departments work together harmoniously.

### Orchestration Layer Overview

- **MessageBus task queue:** Crash-safe, idempotent task execution (`src/ai_company/executor/loop.py`)
- **Org metrics per department:** Capacity, activity, trend, risk via `graph/engine.py` `OrgNode` (30s TTL cache)
- **5-tier HITL governance:** From autonomous to cleared: every decision traceable
- **9 workflow definitions:** Step tracking + SLA monitoring

### Key Takeaways

- Orchestration is the operational backbone between agent design and business results
- Org metrics roll up from agent → department → enterprise
- 5-tier HITL ensures accountability at every decision tier
- 9 workflow definitions with SLA monitoring surface issues to the CEO dashboard

### CTA

Download the Malawi Agentic AI Monitor to explore how orchestration patterns apply in-Malawi context.

### Archive Link

Previous issues compile Posts 1–3 into the "AI-Native Organizations: The Framework" digest. Post 4 (HAOMT-G-V deep dive) arrives late October.