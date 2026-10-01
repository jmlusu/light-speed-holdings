# LightSpeed Architecture Decision Records — v2 Series (025+)

**Location:** `docs/architecture/adr/` (locked by ECL BRIEF_LOCK for Architecture v2.0)
**Legacy ADRs:** `docs/adr/` (001–024) — **not** moved; see numbering notes below.
**Template sections:** Context · Decision · Alternatives · Rationale · Consequences · Status

## Index

| ID | Title | Status |
|----|-------|--------|
| [025](025-agent-consolidation-152-to-90.md) | Agent Consolidation 152 → 90 | Accepted |
| [026](026-single-owner-architecture.md) | Single-Owner Architecture | Accepted |
| [027](027-public-internal-boundary.md) | Public vs Internal Boundary | Accepted |
| [028](028-public-agent-registry-schema.md) | Public Agent Registry Schema | Accepted |
| [029](029-lightspeed-operating-system.md) | LightSpeed Operating System as Public Product Story | Accepted |
| [030](030-ai-company-builder-architecture.md) | AI Company Builder Product Surface Architecture | Accepted |
| [031](031-route-consolidation.md) | Route Consolidation (Single-Hop Redirects) | Accepted |
| [032](032-data-architecture.md) | Data Architecture (YAML SoT → Public Transform → SPA) | Accepted |
| [033](033-dynamic-metrics-evidence.md) | Dynamic Metrics and Evidence Model | Accepted |
| [034](034-framework-strategy.md) | Framework Strategy — No Premature SPA/Framework Rewrite | Accepted |
| [035](035-canonical-production-host.md) | Canonical Production Host | Accepted |

**Count:** 11 ADRs (025–035). All **Accepted** unless noted in-file.

## Numbering and path notes

1. **Continuation:** v2 series starts at **025** per ECL lock. Highest legacy number is 024.
2. **Duplicate legacy 020:** `docs/adr/` contains both `020-pharos-content-intelligence.md` and `020-client-facing-site-guiding-principles.md`. Legacy files are **not renamed** (referenced by other docs). Collision is recorded once in ADR-025; do not reuse 020 in this series.
3. **Missing numbers:** `docs/adr/` has gaps (006–009, 011, 021). Gaps are historical; this index does not renumber legacy files.
4. **Path split:** Operational/runtime ADRs remain under `docs/adr/`. Architecture v2 decisions live here under `docs/architecture/adr/` per BRIEF_LOCK. Cross-link with relative paths (`../../` from this directory to `docs/architecture/*.md`, `../../../adr/` to legacy if needed).

## Related architecture package

Supporting docs in `docs/architecture/`: `AGENT_CONSOLIDATION_152_TO_90.md`, `AI_WORKFORCE_90.md`, `PUBLIC_INTERNAL_BOUNDARY.md`, `WEB_INFORMATION_ARCHITECTURE_V2.md`, `PUBLIC_AGENT_REGISTRY_SCHEMA.md`, `ROUTE_MIGRATION_V2.md`, `EVIDENCE_ARCHITECTURE.md`, `AI_COMPANY_BUILDER_UX.md`, `V2_IMPLEMENTATION_ROADMAP.md`, primary `LIGHTSPEED_AI_COMPANY_BUILDER_WEB_ARCHITECTURE_V2.md` (T012).
