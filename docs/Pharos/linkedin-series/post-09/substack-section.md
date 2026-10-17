# Substack Section - Post 9: Measuring AI-native Organizations

**Series:** AI-Native Organizations (11 posts)
**Post:** 9
**Issue:** November digest: "AI-Native Organizations: Use Cases & Governance" (builder component)

## Monthly Digest Slice

This issue's builder essay: measuring AI-native organizations. How the V (Value & Impact) layer turns architecture claims into board-checkable numbers, including the numbers that do not flatter us.

### The Measurement Chain

Input → Process → Output → Outcome, mirroring the OKR shape an institution already knows:

- **Input** - what did we fund and equip: registered agents, model spend, department capacity
- **Process** - did the system work as designed: Agent Utilization (KPI-003), Build Success Rate (KPI-004), SLA adherence, dead-letter volume
- **Output** - what work shipped: tasks completed, audits logged, decisions cleared per tier
- **Outcome** - did the organization get better: ARR trajectory (KPI-001), customer satisfaction (KPI-002), employee NPS (KPI-005)

Two rules hold it together. **No owner, no KPI**: every KPI carries a named owner, a target, a formula, and a source printed next to it; a number nobody acts on is decoration. And **the denominator must be governed**: utilization is computed against `company-registry.yaml`, so the registry (ADR-032) is a prerequisite for measurement, not a housekeeping chore.

### The Honesty Test

Two facts from our own KPI file:

1. KPI-003 Agent Utilization reads **1.5 percent against an 80 percent target** (30-day window), while KPI-004 Build Success Rate reads **100.0 against 99.5**. We publish both. An organization that quotes only its flattering metrics is running marketing, not measurement.

2. KPI-001 (ARR), KPI-002 (customer satisfaction), and KPI-005 (employee NPS) carry `current: null` and render as "n/a", because no real source exists yet, per the CEO's 2026-08-08 decision: *KPIs must be computed from real sources, not hardcoded dummy values.* The null marks work still owed. A KPI you cannot trace is a KPI you should not quote to a board.

### What to Instrument

**First 30 days:** one registry (denominators), one queue (process data), utilization weekly, one success rate, one dead-letter count. Five numbers, all traceable to files you already own.

**By 90 days:** cost per agent and per department on the invoice; decisions by approval tier; SLA adherence per workflow; department trend on a live org graph; one outcome metric with a real source behind it.

**Resist:** composite "AI maturity scores," untraceable productivity percentages, and benchmarks that compare your computed numbers to someone's self-reported ones.

### Key Takeaways

- Value measurement sits last in H→A→O→M→T→G→V because it consumes what the other six layers produce: no registry means no denominator, no queue means no process data, no gates means no decision ledger
- Sovereignty questions audit the same way: registry entries, policy records, logs; claims you cannot evidence at audit time are claims to stop making
- Low numbers are features. Publish them.
- Nulls are features. Mark them.

### CTA

Download the Malawi Agentic AI Monitor to explore how these patterns apply in-Malawi context.

### Archive Link

Previous issues compile Posts 1–9. Post 10 (decision rights) arrives next; the policy brief synthesizes Posts 8–10.