# Capability Taxonomy Analysis
## LightSpeed Content Architecture Council

## Findings

### 1. Taxonomy Flow Status: PARTIALLY DEFINED
The core flow **Problem → Capability → Service → Engagement Model → Business Outcome** has only 5 of the expected entity types defined in YAML files, though the ontology.yaml provides structural relationships for all types.

**Defined entities (in both ontology.yaml and YAML files):**
- Problem: `low_ai_adoption` (key, title, description, industry: african_ai, severity: high)
- Capability: `ai_strategy` (key, title, description, category: strategic, maturity_model_level: 3, enables: accelerated_ai_adoption)
- Service: `ai_opportunity_assessment` (key, title, description, capability: ai_strategy, engagement_models: [assessment, workshop], price_tier: professional, duration_weeks: 4)
- Business Outcome: `accelerated_ai_adoption` (key, title, description, metric: time-to-value, target: SMEs in emerging markets, enabled_by: [ai_strategy])
- Engagement Model: `assessment` (key, title, description, category: assessment, duration_weeks: 4, capability: ai_strategy, proof_required: true)

**Missing entity types from YAML files (though ontology.yaml has relationship definitions):**
- Additional Problem entities (skills_gap, data_infrastructure_lack, change_resistance, talent_shortage)
- Additional Capability entities (machine_learning_operations, data_governance, ai_ethics, change_management, technology_integration)
- Additional Service entities (ai_implementation, model_deployment, ai_training, ai_governance_framework, change_management_service)
- Additional Engagement Model categories (implementation, ongoing_governance, advisory) — only "assessment" defined
- Additional Business Outcome entities (reduced_operational_costs, improved_decision_making, enhanced_customer_experience, competitive_advantage, accelerated_time_to_market)

### 2. Relationship Gaps and Inconsistencies

**a) Problem → Capability relationships (ontology.yaml: "enables" with strength/evidence_level):**
- Currently only `low_ai_adoption → ai_strategy` is implied
- Missing: evidence_level assignments for all Problem → Capability links
- The 65-claim evidence ledger (18 evidenced / 29 qualified / 18 unqualified from ADR-020) must populate these evidence levels

**b) Capability → Service relationship (ontology.yaml: "realizes", one-to-many):**
- `ai_strategy → ai_opportunity_assessment` is defined
- Missing: Other services that realize ai_strategy, and their engagement models

**c) Capability → Business Outcome relationship (ontology.yaml: "enables" with strength):**
- `ai_strategy → accelerated_ai_adoption` is defined
- Missing: strength ratings and evidence_level for all Capability → Outcome links
- `accelerated_ai_adoption` target is "SMEs in emerging markets" — needs evidence level

**d) Engagement Model → Capability relationship (ontology.yaml: "requires"):**
- `assessment → ai_strategy` is defined in engagement_model_assessment.yaml
- Missing: "requires" relationships for other engagement model categories (implementation, ongoing_governance, advisory)

**e) Engagement Model → AI Use Case relationship (ontology.yaml: "applies_to"):**
- `assessment → predictive_maintenance` is defined in engagement_model_assessment.yaml
- Missing: applies_to links for other engagement models and use cases

### 3. Evidence Ledger Reference (ADR-020: 65 claims: 18 evidenced / 29 qualified / 18 unqualified)

The evidence ledger must inform all evidence_level assignments:

**18 evidenced claims** — empirically supported with data, case studies, or references:
- Should be referenced for Problem → Capability and Capability → Outcome links where LightSpeed has documented proof
- Example: `low_ai_adoption → ai_strategy` at "evidenced" level if supported by case studies

**29 qualified claims** — have supporting logic/reasoning but not empirical evidence:
- Should be used for Problem → Capability and Capability → Outcome links with logical reasoning
- Example: `ai_strategy enables accelerated_ai_adoption` at "qualified" level is reasonable but not yet empirically verified in all contexts

**18 unqualified claims** — unverified, no supporting evidence:
- Should NOT be assigned as evidence_level without proper justification
- Must be flagged for review or removed from taxonomy until evidenced

**Taxonomy impact:** All evidence_level fields in Problem → Capability, Capability → Service, Capability → Business Outcome relationships must reference the ADR-020 ledger. Claims without ADR-020 support should be marked "qualified" at most, or "anecdotal" if only logical connection exists.

### 4. Terminology Issues

**a) "AI Strategy" Disambiguation:**
- Defined as a **Capability** key: `ai_strategy`
- Must NOT simultaneously appear as a service key, methodology category, or product name (forbidden per glossary.md)
- Current usage: capability_ai_strategy.yaml, capability field in service_ai_opportunity_assessment.yaml — correct usage

**b) Engagement Model Category Taxonomy:**
- taxonomy.yaml lists 5 categories: assessment, workshop, implementation, ongoing_governance, advisory
- Only "assessment" is defined in entity YAML files
- Missing: engagement_model_implementation.yaml, engagement_model_ongoing_governance.yaml, engagement_model_advisory.yaml

**c) Price Tier Vocabulary:**
- Consistent across all entities: entry, professional, enterprise, custom
- All defined entities use "professional" tier — need more tier distribution

**d) "Accelerated AI Adoption" as Both Capability Enablement and Business Outcome:**
- Appears as `enables` target from ai_strategy (Capability → Business Outcome)
- Also appears as the business outcome key: `accelerated_ai_adoption`
- This is consistent — a capability enables an outcome, and the outcome is named "accelerated_ai_adoption"
- No conflict, but must maintain clear distinction in relationships

### 5. Conflicts

**No critical conflicts detected.** The following minor inconsistencies need resolution:

1. **Evidence level inconsistency:** `service_ai_opportunity_assessment.yaml` has `proof: []` (empty), while `engagement_model_assessment.yaml` has `proof_required: true`. These should be aligned — if proof is required, the service should reference proof types.

2. **Maturity model level:** `capability_ai_strategy.yaml` has `maturity_model_level: 3` (Defined), but no other capabilities define maturity levels. Should either add maturity levels to all capabilities or remove from ai_strategy.

3. **Related problems asymmetry:** `problem_low_ai_adoption.yaml` has `related_problems: []`, but `business_outcome_accelerated_ai_adoption.yaml` has `related_problems: [low_ai_adoption]`. The problem should reference the outcomes it contributes to, and outcomes should reference the problems they solve.

### 6. Missing Information

**A. Missing Problem entities (4 recommended):**
1. `skills_gap` — "Insufficient AI talent and skills within organizations"
   - industry: african_ai, severity: high, related_problems: [low_ai_adoption]
   
2. `data_infrastructure_lack` — "Inadequate data collection, storage, and processing infrastructure"
   - industry: african_ai, severity: high, related_problems: [low_ai_adoption]
   
3. `change_resistance` — "Organizational resistance to AI cultural and process change"
   - industry: african_ai, severity: medium, related_problems: [low_ai_adoption]
   
4. `talent_shortage` — "Lack of AI-specialized personnel across technical and strategic roles"
   - industry: african_ai, severity: high, related_problems: [low_ai_adoption]

**B. Missing Capability entities (5 recommended):**
1. `machine_learning_operations` — "Operationalizing ML models into production environments"
   - category: technical, maturity_model_level: 2, enables: [reduced_operational_costs], implemented_by: [model_deployment_service]
   
2. `data_governance` — "Managing data assets for AI compliance, quality, and accessibility"
   - category: governance, maturity_model_level: 3, enables: [improved_decision_making], implemented_by: [ai_governance_framework]
   
3. `ai_ethics` — "Ensuring ethical AI implementation aligned with values and regulations"
   - category: governance, maturity_model_level: 2, enables: [competitive_advantage], implemented_by: [ethics_review_service]
   
4. `change_management` — "Managing organizational change for AI adoption"
   - category: organizational, maturity_model_level: 3, enables: [accelerated_ai_adoption], implemented_by: [change_management_service]
   
5. `technology_integration` — "Integrating AI solutions with existing technology stacks"
   - category: technical, maturity_model_level: 2, enables: [enhanced_customer_experience], implemented_by: [api_integration_service]

**C. Missing Service entities (5 recommended):**
1. `model_deployment_service` — "Deploying and managing ML models in production"
   - capability: machine_learning_operations, engagement_models: [implementation], price_tier: enterprise
   
2. `ai_governance_framework` — " establishing AI governance structure and processes"
   - capability: data_governance, engagement_models: [ongoing_governance], price_tier: enterprise
   
3. `ai_ethics_review_service` — "Ethical review and compliance validation for AI systems"
   - capability: ai_ethics, engagement_models: [assessment], price_tier: professional
   
4. `change_management_service` — "Guiding organizational through AI adoption change"
   - capability: change_management, engagement_models: [advisory, workshop], price_tier: professional
   
5. `api_integration_service` — "Connecting AI capabilities to existing business systems"
   - capability: technology_integration, engagement_models: [implementation], price_tier: enterprise

**D. Missing Engagement Model entities (3 recommended, completing taxonomy.yaml):**
1. `engagement_model_implementation` — category: implementation, duration_weeks: 8-12, proof_required: true
2. `engagement_model_ongoing_governance` — category: ongoing_governance, duration_weeks: 52 (annual), proof_required: true
3. `engagement_model_advisory` — category: advisory, duration_weeks: 4-8, proof_required: false

**E. Missing Business Outcome entities (5 recommended):**
1. `reduced_operational_costs` — "Cost savings from AI-optimized processes" — metric: "cost-reduction-percent", target: "SMEs in emerging markets"
2. `improved_decision_making` — "Better business decisions through AI analytics" — metric: "decision-quality-score", target: "executive leadership"
3. `enhanced_customer_experience` — "Improved customer satisfaction through AI personalization" — metric: "NPS-increase", target: "SMEs with customer-facing AI"
4. `competitive_advantage` — "Sustainable market advantage from AI differentiation" — metric: "time-to-market-reduction", target: "SMEs in emerging markets"
5. `accelerated_time_to_market` — "Faster product/ service launch enabled by AI" — metric: "weeks-reduced", target: "SMEs in emerging markets"

### 7. Recommendations

**Priority 1: Populate evidence levels from ADR-020 ledger**
- Assign evidence_level to all Problem → Capability, Capability → Service, and Capability → Business Outcome relationships
- 18 claims are "evidenced" — identify which relationships these support and assign accordingly
- 29 claims are "qualified" — use for relationships with logical reasoning but no empirical data
- 18 claims are "unqualified" — remove or flag for evidence generation

**Priority 2: Define missing entity YAML files**
- Create YAML files for all missing Problem, Capability, Service, Engagement Model, and Business Outcome entities
- Follow the exact schema from ontology.yaml and existing entity files
- Update entities/index.yaml to include new definitions

**Priority 3: Complete engagement model taxonomy**
- Create engagement_model_implementation.yaml, engagement_model_ongoing_governance.yaml, engagement_model_advisory.yaml
- Update taxonomy.yaml to confirm all 5 categories: assessment, workshop, implementation, ongoing_governance, advisory
- Map each engagement model to its capability and price tier

**Priority 4: Establish relationship strength and evidence consistency**
- Assign strength ratings (weak/moderate/strong/critical) for all relationships
- Align proof/engagement_models across services and their engagement models
- Ensure bidirectional consistency: Problem → Outcome and Outcome → Problem should reference each other

**Priority 5: Update entity index and glossary**
- Add new entity definitions to entities/index.yaml
- Verify no terminology conflicts with glossary.md reserved terms
- Ensure all new entities use controlled vocabulary from glossary.md

### 8. Confidence Assessment

| Area | Confidence Level | Rationale |
|------|-----------------|-----------|
| Taxonomy structure framework | High | ontology.yaml provides solid structural relationships; flow is logically consistent |
| Entity relationship patterns | High | Existing YAML files follow consistent schemas; patterns are clear |
| Evidence level assignments | Medium | Requires ADR-020 ledger consultation; 65 claims must be mapped to specific relationships |
| Missing entity definitions | Medium | Based on taxonomy gaps identified; could vary with additional domain research |
| Engagement model completion | High | taxonomy.yaml already defines 5 categories; only need YAML entity files |
| Price tier distribution | Low-Medium | Currently all "professional"; need domain knowledge to assign appropriate tiers |
| Capability maturity model levels | Medium | ai_strategy at level 3 is reasonable; other capabilities need domain expertise |

**Overall Confidence: Medium-High** — The structural framework is solid and consistent with existing definitions. The main uncertainty lies in evidence level assignments (requiring ADR-020 mapping) and the specific definitions of missing entities (requiring domain expert input).

### 9. Evidence References

- **ADR-020 evidence ledger**: 65 total claims (18 evidenced / 29 qualified / 18 unqualified) — must inform all evidence_level assignments across the taxonomy
- **ontology.yaml**: Core entity definitions and relationship schemas (Problem ↔ Capability ↔ Service ↔ Business Outcome ↔ Engagement Model)
- **glossary.md**: Controlled vocabulary — "AI Company Builder" singular definition, "Lightspeed" and "Pharos" brand terms, forbidden terminology patterns
- **taxonomy.yaml**: Industry, engagement model, evidence level, maturity model, problem severity, and price tier taxonomies
- **Existing entity YAML files**: problem_low_ai_adoption.yaml, capability_ai_strategy.yaml, service_ai_opportunity_assessment.yaml, engagement_model_assessment.yaml, business_outcome_accelerated_ai_adoption.yaml — serve as templates for new entity definitions
- **entities/index.yaml**: Current index of 6 entities — must be updated to include all new definitions
- **use_case_predictive_maintenance.yaml**: Demonstrates Problem → Capability → Outcome flow in practice
- **insight_ai_adoption_trends_2024.yaml**: Evidence-qualified insight linking problem, capability, and use case
- **case_study_ai_governance_finance.yaml**: Case study with evidence_level: qualified, problem: low_ai_adoption, capability: ai_governance_policy, outcome: reduced_operational_costs

---
*Analysis generated for LightSpeed Content Architecture Council capability taxonomy build-out.*