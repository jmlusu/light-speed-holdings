# Deep Research Brief — {date}

**Routine:** {routine_name} (`{routine_id}`)
**Run ID:** {routine_run_id}
**Receiver:** {receiver_id}
**Research depth:** {research_depth}

## Context

This is a **deep-research** pass, not a single-pass brief. Before drafting a word
you must pull corroboration from the sources the company owns, then assemble an
evidence note that any Pharos writer can build on.

## Steps

1. **Recall context.** Query company memory (`MemoryStore.recall`) for prior
   drafts, decisions, and voice samples relevant to this pillar.
2. **Query the knowledge graph** (`GraphEngine`) for connected entities,
   departments, and decision dependencies touching the topic.
3. **Pull Pharos references** from `docs/Pharos/` (positioning, roadmap,
   stakeholder map, prior articles) and keep the mandated message on-brief.
4. **Corroborate externally.** Use webfetch/regional sources to confirm facts,
   policy positions, or institutional milestones. Never fabricate; mark any
   claim you could not verify as UNVERIFIED.
5. **Draft the brief** as a list of: findings (with source), the institutional
   angle (SADC / Malawi), and 1-2 publishable one-pagers the weekly cadence can
   use.

## Guardrails

- Institutional audience: ministries, SADC secretariat, UNDP/UNESCO-ROSA, banks,
  ICTAM. Evidence and citation move them; viral hooks do not.
- Never cite unverified claims as fact. Split assumptions from findings.
- Output the brief as markdown under the routine run id.
