# LightSpeed Content Architecture (LCA)

## Overview

The LightSpeed Content Architecture (LCA) establishes a canonical content model and knowledge structure that both the website and future AI capabilities can consume. It answers four core questions:

1. **What does LightSpeed know?** (Knowledge model)
2. **What does LightSpeed offer?** (Service and capability model)
3. **How are those things related?** (Ontology and relationships)
4. **How should that knowledge be presented?** (Content graph and presentation)

## Directory Structure

```
/docs/content-architecture/
├── README.md              ← This file
├── principles.md          ← Architecture principles and operating contract
├── glossary.md            ← Controlled vocabulary for key concepts
├── ontology.yaml          ← Core entity and relationship definitions
├── entities/              ← Individual entity definitions (YAML)
├── relationships.yaml     ← Structured relationship definitions
├── content-types.yaml     ← Content type registry (core, knowledge, proof, resources, conversion)
├── sitemap.yaml           ← Derived navigation and traversal structure
├── metadata-schema.json   ← Machine-readable metadata definitions
├── taxonomy.yaml          ← Controlled vocabularies and categorizations
└── validation-rules.yaml  ← Schema and validation rules
```

## Operating Contract

Every agent working on LCA receives:

**Context**: The current state of the architecture, including any existing constraints or decisions
**Constraints**: Design principles, forbidden patterns, integration requirements
**Required output format**: A structured response containing:
- **Findings**: What was discovered or confirmed
- **Proposed entities**: New or modified entity definitions
- **Relationships**: New or modified relationship definitions
- **Terminology issues**: Conflicts, duplicates, ambiguous terms
- **Conflicts**: Disagreements or open questions
- **Missing information**: What's needed to proceed
- **Recommendations**: Suggested next steps
- **Confidence**: Score 0.0–1.0
- **Evidence**: References to supporting data (claims ledger, ADRs, source-of-truth)

## Notation vs GitHub Division

- **GitHub (canonical)**: Architecture schemata, code, YAML/JSON definitions, validation rules
- **Notion (human-readable)**: Research, strategy documents, brainstorming
- **Website CMS**: Published content derived from the canonical model
- **Knowledge graph**: Entity relationships derived from ontology.yaml
- **AI agents**: Research/generation/validation tools using the canonical model
- **OpenCode**: Implementation and automated validation

## Current State

- Initial directory structure created
- Ontology scaffolding in progress
- Evidence ledger referenced (65 claims: 18 evidenced / 29 qualified / 18 unqualified from ADR-020)
- Company registry as base for agent team definitions
- Existing content model (siteContent.ts) and use case catalog (useCaseCatalogData.ts) available for integration/skip per ADR-020 guidance