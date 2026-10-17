# Research Evidence - Post 10: What Should an AI Agent Decide?

**Post:** 10
**Framework Layer:** G - Gates Approve
**Generated:** 2026-09-28

## Claim-to-Source Map

| Claim | Source | Verified |
|-------|--------|----------|
| Five-tier matrix ADR-017: `autonomous → HITL-approved → reviewed → snoozed → cleared` (exact order) | ADR-017; `orchestrator/approval.py`; series plan §4 | ✅ |
| Approval sweep transitions expired PENDING → EXPIRED; EXPIRED is terminal, requires re-submission | AGENTS.md §9.1 | ✅ |
| Audit log records who, what, when, tier, outcome ("who authorized this action, by name, is it logged") | Approval/orchestration design; regulator framing in Posts 7–8 copy | ✅ |
| Agents propose; humans dispose; one matrix applied uniformly across departments | Series design synthesis (Posts 5–8); approval engine single surface | ✅ |
| Tiers attach to action classes, not agents; autonomy earned per class, never granted at onboarding | Series plan G-layer design principle; ADR-017 rationale | ✅ |
| Tier 5 not delegable regardless of performance; self-modifying governance is Tier-5 violation | Series plan forbidden-class design; safety boundaries AGENTS.md §7 | ✅ |
| Registry enumerates agents with scope and permissions; prerequisite for tier enforcement | `company-registry.yaml`; ADR-032 | ✅ |
| Tasks carry leases; failures → dead-letter path; SLA clocks per workflow step | `orchestrator/message_bus.py`; `workflow/engine.py` | ✅ |
| Queue parks Tier-2+ actions; audit records approver | `orchestrator/approval.py` queue design | ✅ |
| Data-access actions default Tier 2 (HITL-approved) or higher; no model promotes its own tier | Posts 8–9 copy blocks; approval matrix config | ✅ |
| Canonical seven tools: read, edit, grep, list, bash, webfetch, task; ToolRunner validates, unknown tools error | AGENTS.md §8; `models/models.py` | ✅ |
| Tool sandbox bounds execution: edit cannot rewrite approval matrix; task cannot spawn unregistered agent | AGENTS.md §8 alias policy + registry loader design | ✅ |
| Circuit breakers stop runaway loops regardless of tier | LLM platform design (llm-platform-owner) | ✅ |
| Honesty badges surface model confidence/uncertainty at decision point | Honesty-badge artifacts in Pharos/publishing docs | ✅ |
| Expired approvals are governance data; boards should read the count weekly | Series synthesis (AGENTS.md §9.1 + Posts 5–7) | ✅ |
| 90 agents, 20 departments canonical | ADR-032; series plan core thesis | ✅ |
| Spend thresholds as decision classes; exceeding envelope escalates | Cost analytics + approval design (Posts 4, 8) | ✅ |
| New action classes start snoozed (Tier 4) or HITL-approved (Tier 2); promote to Tier 1 after measured reliability | Series plan G-layer copy; KPI-003 reliability linkage | ✅ |
| "Every one of these exists as code or config in our stack" (registry, queue, matrix, sweep, audit, sandbox, breakers, badges) | Verified across modules cited above | ✅ |

## Excluded Claims (do NOT include in draft)

| Claim | Reason |
|-------|--------|
| Specific incident counts or audit findings ("we caught N violations") | No incident-count artifact cited in repo |
| Regulatory positions attributed to MACRA/DPA on tier design | No such position on record; only landscape framing |
| Third-party governance frameworks' tier mappings (ISO, NIST, EU AI Act articles) | Not in repo source set for this series |
| Claims that our matrix is "first" or "unique" regionally | Unverifiable marketing claim |
| Performance uplift from gates ("gates reduced errors by X%") | No measured artifact |

## Notes

- RACI table is a series-designed synthesis of ADR-017 + approval engine structure, not a verbatim repo artifact: flagged in draft as "one page a board can read."
- Tier-5 forbidden list items (secret exfiltration, self-modifying governance, unauthorized tier changes, irreversible external commitments without co-signature) derive from AGENTS.md §7 safety boundaries + series plan design; presented as our list, not a standard's list.
- "Regulator asks" phrasing intentionally echoes Posts 7–8 framing (MACRA questions) without attributing new positions.