# ADR-025: Agent Consolidation 152 → 90

**Status:** Accepted
**Date:** 2026-09-24
**ECL:** LightSpeed AI Company Builder + Web Experience Architecture v2.0
**Cross-refs:** [AGENT_CONSOLIDATION_152_TO_90.md](../../AGENT_CONSOLIDATION_152_TO_90.md), [AI_WORKFORCE_90.md](../../AI_WORKFORCE_90.md), [ADR-025 (LS-MEM SQLite Engine Coexistence)](../../adr/025-lsmem-sqlite-engine-coexistence.md) (separate series — always cite the path with ADR-025)

## Context

The roster grew organically to 152 agent IDs across 20 departments. Many IDs were duplicates, title variants, tier duplicates, or capabilities with no consuming product. Operating a 152-agent org with ambiguous ownership (multiple owners per capability) undermines the accountability chain and inflates public claims that cannot be maintained.

Commit `e2bdb0c7` already applied the trim: 62 removed, 90 retained, 0 added. This ADR ratifies the trim as the canonical org boundary and records the classification methodology so future trims/expansions reuse it.

**Historical numbering quirk:** `docs/adr/` contains two ADR-020 files (`020-pharos-content-intelligence.md` and `020-client-facing-site-guiding-principles.md`). Legacy files are not renamed; new ADRs continue from 025 under `docs/architecture/adr/`. ADR-011 does not exist (gap recorded in summary). A second file, `docs/adr/025-lsmem-sqlite-engine-coexistence.md`, also carries number 025 in the legacy series — cite ADR-025 with its path.

## Decision

1. **Canonical roster = 90 agents** (89 AI + 1 human CEO), 20 departments, matching `docs/source-of-truth.yaml` drift gates. Registry triple-count: `company-registry.yaml` 90 = `.opencode/agents/*.md` 90 = `company/agent-registry.json` 90.
2. **152 is historical only.** Pre-trim roster lives in `harness/changes/active/ref/agents_152.txt`; post-trim in `agents_90.txt`. Prose that still says stale counts (e.g. 145/152) must be footnoted as historical or updated — never asserted as current.
3. **Every removed ID carries exactly one classification class** (ordered rules): RETIRE (1) → MERGE (49) → REASSIGN (10) → REDEFINE (2) → CREATE NEW (0). Retained IDs are RETAIN (90). Totals: 62 removed + 90 retained = 152.
4. **Full migration matrix is the record of truth** for where each capability landed (`AGENT_CONSOLIDATION_152_TO_90.md` §4), including decision-rights transfer and residual risks R1–R10.
5. **Future roster changes re-run the same methodology** (or a successor ADR amending it). Silent reintroduction of removed IDs is forbidden; required capabilities re-enter via CREATE NEW with Architecture Lead approval.

## Alternatives

| Option | Why not |
|--------|---------|
| Keep 152 | Ambiguous ownership; 62 IDs had no distinct accountability value |
| Ad-hoc deletions without matrix | Orphaned capabilities; no audit trail for where duties went |
| Aggressive further trim below 90 | Not required by product; 90 already aligns departments and public SoT |
| Publish no org model | Leaves marketing and product free to invent counts (stale 145 claims already present) |

## Rationale

- One owner per capability (see ADR-026) requires eliminating duplicate titles, tier ladders, and parallel execution roles.
- MERGE-heavy (49/62) preserves capability under a named retained owner rather than dropping scope.
- Zero CREATE NEW means no capability was orphaned while still required — validation gate passed.
- Docs-only record is reversible; the commit of record (`e2bdb0c7`) is the irreversible artifact and is already shipped.

## Consequences

- All public and internal claims use 90/20; `source-of-truth.yaml` gates enforce it.
- Merge targets (creative_director, security_compliance_lead, hr, ux_research_lead, etc.) carry absorbed scope — watch residual risks R4, R6, R8.
- Residual open items: V1 dual BD/strategy exec (see ADR-026), V9 QA dual-lead decision_rights, V10 fullstack dual-target routing.
- Mobile capability (RETIRE `mobile_developer`) needs CREATE NEW + cto/human_ceo approval if a mobile product returns.
