# ADR-030: AI Company Builder Product Surface Architecture

**Status:** Accepted
**Date:** 2026-09-24
**ECL:** LightSpeed AI Company Builder + Web Experience Architecture v2.0
**Cross-refs:** [AI_COMPANY_BUILDER_UX.md](../../AI_COMPANY_BUILDER_UX.md), [WEB_INFORMATION_ARCHITECTURE_V2.md](../../WEB_INFORMATION_ARCHITECTURE_V2.md), ADR-029, ADR-020

## Context

`/ai-company-builder` currently stacks two tab systems (section tabs + OsExplorer tabs) that fragment exploration; `/ask` is a rule-based discovery step machine. Executives and technical visitors need different entry depths. Ask LightSpeed is the evaluation entry but is not yet the primary nav CTA. Route and data contracts must stay within ADR-027/028 and ADR-020 honesty rules.

## Decision

1. **Product surface routes (keep):**
   - `/ai-company-builder` — builder landing (primary product page).
   - `/ask` — Ask LightSpeed evaluation entry.
   - Agent detail remains an in-page **modal** (`AgentModal`), not a dedicated route, consuming public registry data only.

2. **Five exploration modes** (single top-level switcher, URL-synced via hash or `?mode=`): **Organization · Agent · Operations · Intelligence · Governance**. Inner domain panels (IaC tree, CLI, models) become secondary controls inside a mode — not peer navigation. `#governance` fragment is frozen.

3. **Ask LightSpeed — Option A (primary recommendation):** promote Ask to a **primary nav CTA** (evaluation/discovery layer framing). Keep the existing rule-based step machine (`welcome → problem → context → results → cta`); **no LLM** in this component (archived decision). CTA → `ExecutiveBriefingModal` with ADR-020 form SLA copy. Empty/honest states required; never present as live AI chat.

4. **Progressive disclosure:**
   - **Executive-first path:** 5-second value → credibility counts → governance/proof depth → briefing CTA. No CLI/IaC/tool-permission tables on the critical path.
   - **Technical-second path:** architecture fit → roster (canonical 7 tools) → simulated CLI (labeled demo) → governance integration → Ask/briefing.

5. **Component dispositions** (summary of UX spec §5): retain step machine + AgentModal + governance tab as primary; refine mode chrome and solution matching to canonical slugs; replace stacked tab labels with mode names. Visual tokens locked to ADR-020 (navy/red/cyan, Arial).

## Alternatives

| Option | Why not |
|--------|---------|
| Option B: Ask as modal-only / secondary link | Lower evaluation conversion; brief prefers central entry |
| LLM chatbot for Ask | Violates archived no-LLM decision; honesty and cost risks |
| Dedicated `/agents/:id` routes for every agent | 90 thin routes; modal already exists; SEO value low vs cost |
| Replace builder page with multi-page IA | Larger rewrite; brief constraint: redesign only with reason (§23) |
| Keep dual stacked tabs as orientation | Fragmented modes; a11y and URL state problems |

## Rationale

- One mode switcher fixes orientation and a11y (tablist pattern, roving tabindex, shareable URL).
- Option A keeps discovery honest (rule-based) while making evaluation reachable from global nav.
- Progressive disclosure matches time-poor executive audience without hiding technical proof.
- Static/public data contracts (90/20, canonical tools) keep the surface inside ADR-027/028.

## Consequences

- Frontend work (roadmap P4): mode switcher, URL sync, nav CTA for Ask, fragment freezes, a11y checklist, demo labels on CLI.
- AgentModal and governance roster depend on P2 public transform exit (no internal registry import).
- Content must drop stale “140+ agents” style copy; counts read from test-backed constants.
- Open UX questions Q1–Q6 in the UX doc resolve at implementation kickoff under this ADR’s constraints.
