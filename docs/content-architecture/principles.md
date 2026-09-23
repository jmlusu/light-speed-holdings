# LightSpeed Content Architecture Principles

## Design Principles

1. **Single Source of Truth**: All content definitions live in Git-managed YAML/JSON under /docs/content-architecture/. Nothing is hardcoded in application code or trapped in Notion.

2. **Vocabulary Control**: Key concepts must have exactly one canonical definition. "AI Company Builder" cannot simultaneously be a service, blog category, product, methodology, and company division. Controlled vocabulary in glossary.md prevents this.

3. **Ontology First**: The entity-relationship model (ontology.yaml) is the foundational artifact. All downstream work (content types, sitemap, metadata) derives from it.

4. **Four-Layer Architecture**: 
   - Layer 1: Business Model → Problem → Capability → Service → Engagement Model → Outcome
   - Layer 2: Knowledge → Insight → Research → Use Case → Framework → Methodology → Policy
   - Layer 3: Experience → Case Study → Demonstration → Resource → Event → Testimonial
   - Layer 4: Content Graph → Sitemap → Navigation → Presentation → Page → Search → AI traversal

5. **Machine-Readable Output**: Every artifact has a machine-readable schema (YAML/JSON) so AI agents can discover, validate, and traverse the model automatically.

6. **Evidence-Backed Claims**: All claims about LightSpeed's knowledge and capabilities must reference the evidence ledger (65 claims: 18 evidenced / 29 qualified / 18 unqualified from ADR-020). Unqualified claims must be flagged.

7. **Notion-Git Divide**: GitHub = canonical architecture/schemata/code; Notion = human-readable research/strategy; Website CMS = published content derived from canonical model.

8. **Future AI Ready**: Architecture must support traversal from Client profile → Industry → Business problem → AI use cases → Capabilities → Services → Evidence → Engagement model. Every entity has a well-defined traversal path.

## Operating Contract for All LCA Agents

**Context**: Current architecture state, including existing constraints or decisions
**Constraints**:
- No concept may have multiple canonical definitions
- All output must follow the structured format (Findings, Proposed entities, Relationships, Terminology issues, Conflicts, Missing information, Recommendations, Confidence, Evidence)
- Machine-readable output only (YAML/JSON); no prose-only artifacts
- Evidence ledger must be referenced for all claims about LightSpeed's knowledge/capabilities
- Integration with existing files per ADR-020: siteContent.ts and useCaseCatalogData.ts are available; claims ledger available

**Required output format**:
- **Findings**: What was discovered or confirmed
- **Proposed entities**: New or modified entity definitions
- **Relationships**: New or modified relationship definitions
- **Terminology issues**: Conflicts, duplicates, ambiguous terms
- **Conflicts**: Disagreements or open questions
- **Missing information**: What's needed to proceed
- **Recommendations**: Suggested next steps
- **Confidence**: Score 0.0–1.0
- **Evidence**: References to supporting data (claims ledger, ADRs, source-of-truth)

## Key Concepts (to be defined in glossary.md)

- AI Company Builder
- Service
- Capability
- Problem
- Business Outcome
- AI Use Case
- Insight
- Research
- Use Case
- Framework
- Methodology
- Case Study
- Demonstration
- Resource
- Engagement Model

## Current State

- Initial directory structure created
- Principles established
- Ontology scaffolding in progress
- Evidence ledger referenced (65 claims: 18 evidenced / 29 qualified / 18 unqualified)
- Company registry as base for agent team definitions
- Existing content model and use case catalog available per ADR-020