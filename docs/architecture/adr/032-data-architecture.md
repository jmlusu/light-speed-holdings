# ADR-032: Data Architecture (YAML SoT → Public Transform → SPA)

**Status:** Accepted
**Date:** 2026-09-24
**ECL:** LightSpeed AI Company Builder + Web Experience Architecture v2.0
**Cross-refs:** [PUBLIC_AGENT_REGISTRY_SCHEMA.md](../../PUBLIC_AGENT_REGISTRY_SCHEMA.md), [PUBLIC_INTERNAL_BOUNDARY.md](../../PUBLIC_INTERNAL_BOUNDARY.md), ADR-025, ADR-027, ADR-028, `docs/source-of-truth.yaml`

## Context

Org facts (agents, departments, KPIs, templates) must not be asserted in prose alone. The SPA currently imports internal registry JSON and hard-codes several proof metrics in components. Editorial content lives in `src/data/*.ts`. Drift gates already exist via `docs/source-of-truth.yaml` + `scripts/validate-drift.ps1`. Stale counts (145/152) persist in non-exempt docs.

## Decision

1. **Single source of truth hierarchy:**

   | Layer | Artifact | Role |
   |-------|----------|------|
   | 1 | `company-registry.yaml` + `company/departments.yaml` + `company/config/kpis.yaml` | Authoritative org data |
   | 2 | Generator/validator outputs (`.opencode/agents/*.md`, `company/agent-registry.json`) | Internal derived; **never public** |
   | 3 | Public transform → `src/data/generated/agent-registry.public.json` | Only agent/department egress (ADR-028) |
   | 4 | Editorial `src/data/siteContent.ts`, `useCaseCatalogData.ts`, etc. | Human-authored narrative content |
   | 5 | React pages/components | Render only; no hard-coded org counts or claim numbers |

2. **Counts are derived, never asserted.** Canonical: **90 agents** (89 AI + 1 human CEO), **20 departments** (including `pharos`), 25 KPIs / 8 KPI-enabled departments, 9 Jinja2 templates — enforced by `source-of-truth.yaml` claims + tests (`companyData.test.ts` `toBe(90)` etc.).

3. **`source-of-truth.yaml` is the claims gate** for documentation. Live docs must match `current_value` patterns; `docs/STATUS.md` / `docs/archive/` / `docs/adr/` remain historically exempt. New claim-bearing surfaces (homepage proof band, ProofPage) must not hard-code numbers that bypass this gate — prefer shared constants or generated data.

4. **departments.yaml includes `pharos`** (20 entries). Any comment or parked narrative claiming “19 missing pharos” is stale and must be reconciled in the doc-drift sweep (T015), not treated as truth.

5. **Transform reads validated YAML (preferred) or internal JSON; never writes back into Layer 1–2.** Public artifact is generated, not hand-edited; regenerate on every registry change (post-commit/CI alongside generator).

6. **Internal ops data** (tasks, approvals, KPI series, cost, audit) does **not** live in public `src/data/` modules (ADR-027 V4). If the dashboard needs fixtures, they belong behind RBAC on the internal side.

## Alternatives

| Option | Why not |
|--------|---------|
| Continue importing `company/agent-registry.json` in `src/` | ADR-027 V1–V3 — private fields in bundle |
| Runtime API for agent list | ADR-027/028 rejected |
| DB-backed CMS for org facts | Overkill; YAML + drift gates already work; no second SoT |
| Hard-code 90/20 in components only | Bypasses SoT; recreates stale-count class of bugs |
| Sidecar JSON per department | Parallel SoT; transform already covers departments |

## Rationale

- One pipeline with one chokepoint (public transform) matches boundary policy and keeps CI deterministic.
- Drift manifest already proven on README/USER-GUIDE/API-REFERENCE/ORGANIZATION — extending discipline to claim-bearing UI is the gap, not a new framework.
- Editorial vs factual split: narrative stays in TS data files; factual roster stays in YAML-derived artifacts.

## Consequences

- Follow-on ECL: implement transform (ADR-028); swap imports; move or delete ops fixtures from `src/data/companyData.ts` L41+; introduce shared constants for proof metrics or generate them from SoT.
- T015 count audit greps new architecture docs for 145/152 and fixes or footnotes them.
- Reconcile stale “missing pharos” comment in `source-of-truth.yaml` during doc pass.
- Registry field backfill (decision_rights, kpis, etc.) remains schema work under ADR-026 §9 — same SoT, later ECL.
