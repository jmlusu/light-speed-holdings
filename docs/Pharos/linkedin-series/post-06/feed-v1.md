# Feed v1: Post 6 - Agentic AI in Health & M&E

Derived 2026-10-02 from `draft-v1.md` (CEO-approved). Verbatim extracts only - no new claims.

---

AI in health and monitoring & evaluation is not a separate category; it is AI-native architecture applied to two of the most regulation-sensitive domains in our region. The design question is not "can AI improve outcomes?" but how the architecture is designed so agents improve under sovereign data defaults, visible variable cost, and five-tier HITL governance. This post is the T (Tools & Actions) layer, and what it means for Malawi and SADC institutions.

The governance proof is the canonical seven-tool sandbox: read, edit, grep, list, bash, webfetch, task. No tool, no action. A tool not on the list cannot be talked into existence, cannot be granted by prompt injection, cannot be smuggled through a session variable.

But in health and M&E, the stakes narrow the sandbox further. Read access might be limited to de-identified patient records only. Edit access might be limited to KPI dashboards, not raw patient data. Webfetch might be limited to trusted URIs (WHO APIs, ministry portals, peer-reviewed repositories), not arbitrary web sites.

A general workforce grows by screenshots and side-chats. A bounded workforce grows by registry entries someone approved, recording tool permissions, approval tier, and data scope. We know the failure mode first-hand: the registry is a correction (ADR-032), and consolidating to one registry was about earning the right to scale. You cannot govern a population you cannot enumerate, and you cannot enumerate a population that was never declared.

In health contexts, most actions sit at Tier 3 (reviewed) or Tier 4 (snoozed) per ADR-017: policy changes, budget reallocations, and new service rollouts require explicit human sign-off before any agent acts. Every decision is logged: who authorized what, when, and at which tier.

Sovereign data defaults (DPA 2017/2024, GDPR-grade handling), offline-capable operation, and visible variable cost apply from step one, not as a later compliance phase. At LightSpeed Holdings™, model deployments are registered like agents, and a 90-day pilot with cost visible from week one lets a ministry decide with an invoice in hand rather than a forecast.

For institutions in our region, the sandbox converts the AI conversation from trust-me to check-this: buyers, regulators, and boards can audit the structure without understanding the models. Start with 3–5 agents (data quality checker, KPI pull, compliance monitor), with role, scope, and approval tier defined before any agent runs.

Follow along if you are designing, governing, or procuring AI systems in health and M&E in Malawi and SADC. We publish the architecture, the metrics, and the failure paths, not just the outcomes.

Download the Malawi Agentic AI Monitor to explore how these patterns apply in-Malawi context.

#AgenticAI #Health #Malawi #SADC #ToolsActions
