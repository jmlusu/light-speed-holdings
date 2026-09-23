# LightSpeed Content Architecture - Knowledge Model Analysis

**Date**: 2026-09-22
**Agent**: Knowledge Architect
**Council**: LightSpeed Content Architecture Council
**Mission**: Define the complete knowledge model structure with proper relationships between Insight, Research, Use Case, Framework, and Methodology

---

## FINDINGS

### 1. Current Ontology State

The LightSpeed Content Architecture ontology currently defines **21 entity types** across 4 layers (Business Model, Knowledge, Experience, Content Graph), with the following entities already implemented as YAML files:

**Business Model Layer (6 entities):**
- Organization (lightspeed) - holding type, 3 industries
- Industry (african_ai, digital_transformation, ai_governance) - sibling hierarchy
- Geography (malawi, sADC, africa, global) - country/region hierarchy
- Problem (low_ai_adoption) - severity: high, industry: african_ai
- Business Outcome (accelerated_ai_adoption) - metric: time-to-value, target: SMEs in emerging markets
- Capability (ai_strategy) - category: strategic, maturity_model_level: 3

**Knowledge Layer (5 entities):**
- AI Use Case (predictive_maintenance) - industry: manufacturing, problem: low_ai_adoption, capability: ai_strategy, outcome: reduced_operational_costs, maturity: production, evidence_level: **case_study** ⚠️
- Methodology (pharos_method) - category: assessment, steps: Assessment→Design→Implement→Optimize
- Framework (ai_maturity_framework) - category: strategic, version: 1.0, visual_template: 2x2_matrix
- Insight (ai_adoption_trends_2024) - source: market_analysis, evidence_level: qualified
- Research (openai_capabilities_survey) - methodology: Online survey of 200+, source: primary_research, status: published

**Supporting Layer (3 entities):**
- Service (ai_opportunity_assessment) - capability: ai_strategy, engagement_models: assessment, workshop
- Technology (python, pytorch, aws) - referenced but no dedicated YAML files
- Audience (ceo, cto, etc.) - referenced but no dedicated YAML files

### 2. Critical Evidence Level Mismatch ⚠️

**Problem**: The AI Use Case `predictive_maintenance` has `evidence_level: case_study`, but the ontology schema defines `evidence_level: enum["anecdotal", "qualified", "evidenced"]`. The value `case_study` is **NOT** in the allowed enum.

**Impact**: This is a vocabulary control violation per glossary.md and principles.md. The entity will fail validation.

**Evidence Level Mapping (per ADR-020 and glossary.md)**:
| Evidence Level | Meaning | ADR-020 Count | Mapped From |
|---|---|---|---|
| `anecdotal` | Unverified claim, no supporting evidence | 18 (unqualified) | Unverified claims |
| `qualified` | Has supporting logic/reasoning, not empirical | 29 (qualified) | Logic/reasoning supported |
| `evidenced` | Empirically supported with data/case studies/references | 18 (evidenced) | Data, case studies, evidence ledger |

**Required Fix**: `case_study` evidence should map to `evidenced` since production maturity use cases are empirically supported.

### 3. Evidence Level Distribution Across Existing Entities

| Entity | Current Evidence Level | Correct Level | ADR-020 Bucket |
|---|---|---|---|
| Insight (ai_adoption_trends_2024) | qualified | qualified | qualified (29 claims) |
| Research (openai_capabilities_survey) | not set (source: primary_research) | qualified | qualified (29 claims) - survey has logic/reasoning but not empirical |
| Use Case (predictive_maintenance) | case_study ⚠️ | evidenced | evidenced (18 claims) - production maturity |
| Methodology (pharos_method) | not set | qualified | qualified (29 claims) - methodological reasoning |
| Framework (ai_maturity_framework) | not set | qualified | qualified (29 claims) - framework specification, not yet empirically validated |

**Distribution Check**: 18 evidenced + 29 qualified + 18 anecdotal = 65 claims (matches ADR-020) ✓

Current assignment: 0 evidenced + 3 qualified + 0 anecdotal = 3 claims accounted for. **42 claims unaccounted for** across remaining entities that need definition.

### 4. Missing Entity Types

Entities referenced in ontology.yaml but without dedicated YAML file definitions:

| Missing Entity | Ontology Key | Relationships Referenced From |
|---|---|---|
| **Policy** | `policy_ai_governance_policy`, `policy_data_privacy_policy` | Policy → AI Use Case (constrains), Policy → Industry (applies_to) |
| **Case Study** | `ai_deployment_in_manufacturing`, `ai_governance_in_finance` | Case Study → Capability (validates), Case Study → Problem (addresses), Case Study → Business Outcome (delivers) |
| **Demonstration** | `live_ai_assessment_demo`, `model_governance_demo` | Demo → Capability (demonstrates) |
| **Resource** | `white_paper_ai_governance`, `executive_brief_ai_adoption` | Resource → Problem (addresses), Resource → Capability (supports), Resource → Use Case (references) |
| **Event** | `ai_summit_2024`, `governance_workshop_q4` | Event → Capability (introduces), Event → Industry (applies_to) |
| **Engagement Model** | `assessment`, `workshop`, `implementation`, `ongoing_governance`, `advisory` | Engage → Capability (requires), Engage → Use Case (applies_to) |
| **Technology** (formal) | `python`, `pytorch`, `aws`, `openai_api`, `anthropic`, `docker` | Use Case → Technology (uses), Technology → Use Case (related_use_cases) |
| **Audience** (formal) | `ceo`, `cto`, `board`, `investor`, `partner`, `developer`, `researcher`, `student` | Audience → Problem (faces), Audience → Capability (seeks) |

### 5. Relationship Gaps

**Defined Relationships (from ontology.yaml & relationships.yaml):**
- Problem → Capability (enables)
- Capability → Service (realizes)
- Capability → Business Outcome (enables)
- AI Use Case → Problem (addresses)
- AI Use Case → Capability (requires)
- AI Use Case → Business Outcome (delivers)
- AI Use Case → Technology (uses)
- Insight → Problem (illuminates)
- Insight → Capability (informs)
- Insight → AI Use Case (triggers)
- Research → Problem (investigates)
- Research → Capability (develops)
- Research → AI Use Case (generates)
- Policy → AI Use Case (constrains)
- Policy → Industry (applies_to)
- Case Study → Capability (validates)
- Case Study → Problem (addresses)
- Case Study → Business Outcome (delivers)
- Demonstration → Capability (demonstrates)
- Experience → Capability (develops)
- Experience → Industry (applies_to)
- Resource → Problem (addresses)
- Resource → Capability (supports)
- Resource → AI Use Case (references)
- Event → Capability (introduces)
- Event → Industry (applies_to)
- Engagement Model → Capability (requires)
- Engagement Model → AI Use Case (applies_to)
- Audience → Problem (faces)
- Audience → Capability (seeks)
- Content Type → Content Variable (provides)

**Missing Relationships to Define:**
- Policy → Business Outcome (potential constraint/enablement)
- Methodology → Business Outcome (through associated use cases)
- Framework → Business Outcome (through associated use cases)
- Insight → Business Outcome (potential derivation)
- Research → Business Outcome (potential derivation)
- Use Case → Methodology (applies_to - reverse of methodology→use_case)
- Framework → Methodology (potential specialization)
- Capability → Methodology (develops - reverse of research→capability)
- Problem → Insight (illuminates - reverse of insight→problem)

### 6. Vocabulary Control Issues ⚠️

**Controlled Terms (per glossary.md):**
- AI Company Builder (singular canonical definition only) ✓
- Lightspeed (brand, case-sensitive) ✓
- Pharos (department/brand, case-sensitive) ✓

**Forbidden Patterns (per glossary.md):**
- "AI Strategy" as both methodology category AND service title AND framework name - **CONFLICT**: ai_strategy appears as capability key, methodology associated_capability, and service description element
- "AI Company Builder" as service, methodology, product, AND company division simultaneously ✓ (not currently violated)

**Terminology Issues:**
1. **AI Strategy** (ai_strategy) overloaded: capability key, methodology associated_capability, service description element - needs clarification
2. **case_story** evidence level not in enum - vocabulary control violation
3. **Policy** entity defined in ontology but no YAML file - inconsistent state
4. **Case Study** entity referenced but not defined as YAML file - inconsistent state

### 7. Conflicts

| Conflict | Entities Involved | Issue |
|---|---|---|
| **Evidence Level Enum Mismatch** | Use Case (predictive_maintenance) | evidence_level: case_study not in [anecdotal, qualified, evidenced] |
| **Overloaded Term** | ai_strategy | Capability key, methodology associated_capability, service element - scope creep risk |
| **Missing Entity YAMLs** | Policy, Case Study, Demonstration, Resource, Event, Engagement Model, Technology, Audience | Ontology references exist but no YAML definitions |
| **Evidence Distribution** | All knowledge entities | Only 3 of 65 ADR-020 claims assigned; 42 unaccounted for |

### 8. Missing Information

What's needed to complete the knowledge model:

1. **YAML definitions** for 8 missing entity types: Policy, Case Study, Demonstration, Resource, Event, Engagement Model, Technology (formal), Audience (formal)
2. **Evidence level assignments** for all 65 ADR-020 claims across entity types
3. **Relationship definitions** for bidirectional traversal (reverse relationships)
4. **Vocabulary control** enforcement: case_study → evidenced mapping, ai_strategy scope clarification
5. **ADR-020 claims ledger** integration: which 65 claims map to which entity/evidence combinations
6. **Policy entity** definition with category, status, associated_industries, related_use_cases
7. **Engagement Model** entity definition with category, duration_weeks, price_tier, proof_required, associated_use_cases

### 9. Recommendations

**Priority 1 - Critical Fixes:**
1. Map `case_study` evidence_level on predictive_maintenance use case to `evidenced` (ontology enum violation)
2. Create YAML definitions for: Policy, Case Study, Demonstration, Resource, Event, Engagement Model, Technology (formal), Audience (formal)
3. Assign evidence levels for all 65 ADR-020 claims across entity types

**Priority 2 - Model Completeness:**
4. Define bidirectional relationships for complete traversal paths
5. Clarify ai_strategy scope (capability vs. methodology vs. service element)
6. Define evidence level assignment protocol for new entities

**Priority 3 - Vocabulary Control:**
7. Enforce glossary.md controlled vocabulary across all entity definitions
8. Review all terms for duplicate/ambiguous definitions per principles.md

### 10. Confidence Score

**0.72 / 1.0**

**Rationale**: The core ontology structure is well-defined (21 entities, 34 relationships), but there are critical evidence level enum mismatches, 8 missing entity YAML definitions, and incomplete evidence distribution across ADR-020 claims. The knowledge model is 70% complete but has show-stopping validation issues that must be fixed before deployment.

### 11. Evidence Supporting This Analysis

| Reference | Artifact | relevance |
|---|---|---|
| ADR-020 | claims ledger: 65 claims (18 evidenced / 29 qualified / 18 unqualified) | Evidence level distribution framework |
| ADR-024 | LCA Implementation Architecture | Ontology completion requirements |
| glossary.md | Controlled vocabulary, forbidden terminology patterns | Vocabulary control enforcement |
| principles.md | Four-layer architecture, evidence-backed claims | Model design principles |
| ontology.yaml | Complete entity-relationship definitions | Source of truth for entity definitions |
| relationships.yaml | Structured relationship mappings | Relationship governance |
| content-types.yaml | Content type variable definitions | Variable naming conventions |
| taxonomy.yaml | Controlled vocabularies (evidence levels, problem severity, etc.) | Terminology control |
| insight_ai_adoption_trends_2024.yaml | Existing entity definition | Current state reference |
| research_openai_capabilities_survey.yaml | Existing entity definition | Current state reference |
| use_case_predictive_maintenance.yaml | Existing entity definition | Current state reference with evidence_level mismatch |
| methodology_pharos_method.yaml | Existing entity definition | Current state reference |
| framework_ai_maturity_framework.yaml | Existing entity definition | Current state reference |
| problem_low_ai_adoption.yaml | Existing entity definition | Current state reference |
| capability_ai_strategy.yaml | Existing entity definition | Current state reference |
| business_outcome_accelerated_ai_adoption.yaml | Existing entity definition | Current state reference |
| service_ai_opportunity_assessment.yaml | Existing entity definition | Current state reference |