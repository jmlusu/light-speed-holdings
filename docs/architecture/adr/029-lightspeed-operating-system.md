# ADR-029: LightSpeed Operating System (LSOS) as Public Product Story

**Status:** Accepted
**Date:** 2026-09-24
**ECL:** LightSpeed AI Company Builder + Web Experience Architecture v2.0
**Cross-refs:** [AI_COMPANY_BUILDER_UX.md](../../AI_COMPANY_BUILDER_UX.md), [PUBLIC_INTERNAL_BOUNDARY.md](../../PUBLIC_INTERNAL_BOUNDARY.md), ADR-027, ADR-030

## Context

The public product narrative for `/ai-company-builder` needs a coherent frame for how LightSpeed runs itself: builder organization, operations, intelligence, and governance — plus the internal Python AI OS (CLI, orchestrator, registry generator, dashboard, memory). Exposing that OS naively leaks internals (ADR-027). The product story must be honest (ADR-020: no fake success states) while progressive disclosure serves executives first and technical audiences second.

## Decision

1. **LSOS is the canonical public product story** for the AI Company Builder surface: a four-layer narrative that maps to the real system without publishing private artifacts:

   | Layer | Public story | Internal counterpart (never egressed raw) |
   |-------|--------------|-------------------------------------------|
   | **Builder organization** | 90 agents / 20 departments as an ownership model people can inspect | `company-registry.yaml`, generated cards |
   | **Operations** | How work flows: journeys, queues, demo CLI | orchestrator message_bus, inbox, HITL |
   | **Intelligence** | Decision engine, memory types, semantic fabric | decision engine, 6-type memory (ADR-019), cost tracker |
   | **Governance** | HAOMTGV + 5-tier HITL as the differentiator | tier_rules, ApprovalGate, RBAC dashboard |

2. **Progressive disclosure rule:** public pages lead with organizational/governance outcomes; technical depth (IaC tree, simulated CLI, tool vocabulary) is one click deeper and **always labeled demo/simulated** when it is not live tenant execution.

3. **No live-tenant implication:** builder CLI/org-graph output is illustrative. Never present simulated runs as real multi-tenant execution (ADR-020 honesty rules).

4. **Data path for any agent/department rendering** follows ADR-027/028 only (public artifact), never internal registry JSON.

5. **Counts and claims** derive from test-backed constants / `source-of-truth.yaml` (90, 20, 2373 tests, 5-tier) — not marketing prose like “140+ agents.”

## Alternatives

| Option | Why not |
|--------|---------|
| Publish full OS docs as the product | Crosses ADR-027 boundary (guidelines, permissions, inbox) |
| Pure marketing metaphor with no system truth | Fails ADR-020 honesty; collapses under technical buyer scrutiny |
| Separate “OS” microsite on another stack | Second front door risk (see ADR-035); diverges from Vercel SPA |
| Hide OS entirely | Loses differentiation on `/ai-company-builder` and Trust/Proof |

## Rationale

- LSOS gives one name to the multi-artifact v2 story (org model + ops + intelligence + governance) without new runtime surface.
- Maps cleanly onto the five builder UX modes (Organization · Agent · Operations · Intelligence · Governance) — LSOS layers are the narrative spine; modes are the interaction spine.
- Keeps marketing and engineering aligned on the same layered model while the transform gate enforces what may leave the boundary.

## Consequences

- `/ai-company-builder` copy, comparison matrix, and governance tab are written as LSOS layers (UX dispositions still follow `AI_COMPANY_BUILDER_UX.md` retain/refine/replace).
- Technical depth remains behind progressive disclosure and demo labels.
- Any LSOS diagram in the primary v2 doc must show the public transform chokepoint between internal OS and public story.
- If a future “OS” claim needs a metric or benchmark, it becomes a governed evidence claim under ADR-033 — not a hard-coded boast.
