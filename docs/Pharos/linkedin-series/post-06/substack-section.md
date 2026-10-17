# Substack Section - Post 6: Agentic AI in Health & M&E

**Series:** AI-Native Organizations (11 posts)
**Post:** 6

## Monthly Digest Slice

This month's focus: Agentic AI in health and M&E. This issue unpacks the T (Tools & Actions) layer: practical implementations of sovereign data defaults, visible variable cost, and five-tier HITL governance in health and monitoring & evaluation contexts for Malawi and SADC institutions.

### T - Tools & Actions Overview

The T layer answers one design question: what tools may agents interact with, and how are boundaries enforced in health and M&E contexts?

**Canonical seven-tool sandbox:** read, edit, grep, list, bash, webfetch, task. No tool, no action. Anything outside the approved set is rejected at the Runtime layer.

**Domain-specific restrictions in health:**
- Read access: limited to de-identified patient records only
- Edit access: limited to KPI dashboards, not raw patient data
- Bash access: limited to server maintenance commands, not patient-system reconfiguration
- Webfetch access: limited to trusted URIs (WHO APIs, ministry portals, peer-reviewed repositories), not arbitrary web sites
- Task access: limited to health-M&E workflow steps, not general web searches

**The difference between general and bounded workforce:**
- General workforce grows by screenshots and side-chats
- Bounded workforce grows by registry entries that someone approved, and the registry records not just the agent's identity and department, but its tool permissions, its approval tier, its data scope

### Key Takeaways

- The seven-tool canonical sandbox is the default: read, edit, grep, list, bash, webfetch, task
- In health and M&E, domain-specific restrictions are added on top: read limited to de-identified records, edit limited to KPI dashboards, webfetch limited to trusted URIs
- If you cannot name the buyer (government budget line, donor program, facility cost-recovery), the agent does not exist
- Start with 3–5 agents. Define role, scope, and approval tier before any agent runs
- One queue before any agents. Even a file-backed inbox with leases and a dead-letter path gives you durability, audit, and a place for failure to land
- Utilization from day one. If you cannot see which agents are consuming work this week, you are operating on anecdote. KPI-003-style utilization is the cheapest possible sensor
- Install the gates before the autonomy. Tier-1 (autonomous) actions only after you have watched the agent operate under review for a period
- Sovereign data defaults (DPA 2017/2024, GDPR-grade handling), offline-capable operation, and visible variable cost still apply: a 90-day pilot can validate the T layer on one department before it touches the institution

### CTA

Download the Malawi Agentic AI Monitor to explore how these patterns apply in-Malawi context.

### Archive Link

Previous issues compile Posts 1–6 into the "AI-Native Organizations: The Framework" digest. Post 7 arrives late October.