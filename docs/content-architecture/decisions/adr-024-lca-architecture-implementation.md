# ADR-024: LightSpeed Content Architecture (LCA) Implementation

## Decision

Implement the LightSpeed Content Architecture (LCA) as a Git-managed, machine-readable ontology and knowledge structure under /docs/content-architecture/, serving as the single source of truth for all content, services, capabilities, and AI traversal paths.

## Why

The existing content model (siteContent.ts) and use case catalog (useCaseCatalogData.ts) are useful for application-level rendering but lack the formal ontology, relationship mapping, and machine-readability required for AI agent traversal, knowledge graph construction, and future-proof architecture. The LCA provides:

1. **Single source of truth**: All content definitions in YAML/JSON, not hardcoded or trapped in Notion
2. **AI readiness**: Enables traversal from Client profile → Industry → Business problem → AI use cases → Capabilities → Services → Evidence → Engagement model
3. **Vocabulary control**: Prevents concepts from having multiple canonical definitions (e.g., "AI Company Builder" as service, category, product, and division)
4. **Evidence-backed architecture**: All claims reference the evidence ledger (65 claims: 18 evidenced / 29 qualified / 18 unqualified from ADR-020)
5. **Downstream compatibility**: Derives content-types, sitemap, metadata schema, and validation rules from the ontology

## Alternatives Considered

1. **Notion-first approach**: Keep architecture in Notion, generate YAML from there
   - *Rejected*: ADR-020 guidance specifies GitHub = canonical, Notion = human-readable research; website CMS = published content derived from canonical model

2. **Code-first approach**: Embed content definitions directly in application code (TypeScript/React)
   - *Rejected*: Violates "single source of truth" principle; prevents AI agent traversal; makes knowledge graph construction impossible

3. **YAML-only without ontology**: Define content types and sitemap without formal entity-relationship model
   - *Rejected*: No traversal path definition; no vocabulary control; no machine-readable schema for AI agents; cannot support future Ask LightSpeed layer

4. **Partial ontology (core only)**: Define only core entities, skip knowledge/proof/conversion categories
   - *Rejected*: Fails the four-question requirement (what we know, offer, how related, how presented); creates downstream rework when those categories are needed

## Consequences

### Positive
- Canonical architecture usable by website CMS, AI agents, and knowledge graph
- Vocabulary control prevents concept dilution and duplication
- Machine-readable output enables automated validation and traversal
- Evidence-ledger integration ensures claims are substantiated
- Supports future AI layer (Ask LightSpeed traversal)

### Negative
- Initial setup cost: ontology definition, entity files, relationship mapping, validation rules
- All content team members must adopt new terminology and operating contract
- Existing siteContent.ts and useCaseCatalogData.ts must be integrated/skip per ADR-020 guidance (not overwritten)
- Decisions about term definitions must go through the Content Architecture Council (11 specialized agents + Orchestrator)

## Date

2026-09-22

## Owner

Content Architecture Council (multi-agent team per AGENTS.md#2)

## Status

Accepted