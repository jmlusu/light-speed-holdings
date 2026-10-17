# LightSpeed Content Architecture Glossary

## Controlled Vocabulary

This glossary defines the canonical terminology for the LightSpeed Content Architecture. All agents must use these terms exclusively; no synonyms or variants are permitted in canonical YAML/JSON definitions.

### Core Concepts

**AI Company Builder**
- Definition: The organizational capability and framework by which LightSpeed builds and scales AI companies in emerging markets
- Scope: This term must have exactly one canonical definition. It must NOT simultaneously appear as a service, blog category, product, methodology, or company division.
- Source: company-registry.yaml, ADR-020

**Service**
- Definition: A packaged offering delivered to an audience to address a problem using capabilities, with an engagement model and expected business outcomes
- Scope: Concrete, deliverable offering with defined engagement model, price tier, and proof requirements

**Capability**
- Definition: A measurable competency or technology skill that enables services and AI use cases
- Scope: Abstract competency, not a service itself; enables services and use cases

**Problem**
- Definition: A business challenge or pain point that LightSpeed's content/capabilities address
- Scope: Must have severity (low/medium/high/critical) and belong to an industry

**Business Outcome**
- Definition: A measurable business result achieved through LightSpeed engagement
- Scope: Must have a metric and target definition

### Technical Concepts

**Industry**
- Key values: african_ai, digital_transformation, ai_governance
- Hierarchical structure with parent/child relationships

**Geography**
- Key values: malawi, sADC, africa, global
- Hierarchical relationships (country → region → subregion → continent)

**Technology**
- Key values: python, pytorch, openai_api, anthropic, aws, docker
- Category: programming_language, framework, cloud_platform, ai_model, tool, infrastructure

**Methodology**
- Category: assessment, deployment, governance, optimization, research
- Associated capabilities and use cases

**Framework**
- Versioned conceptual or methodological structure
- Visual templates: 2x2_matrix, waterfall, circular

### Knowledge Concepts

**Insight**
- Source: primary_research, market_analysis, internal_data, partner_data, academic
- Evidence level: anecdotal, qualified, evidenced

**Research**
- Methodology: primary_research, market_analysis, internal_data, partner_data, academic
- Status: draft, peer_review, published, superseded

**Use Case**
- Maturity: prototype, validated, production, scaled
- Evidence level: anecdotal, qualified, evidenced

**Policy**
- Category: ai_governance, data_privacy, ethics, compliance, industry_regulations
- Status: draft, approved, retired

### Proof Concepts

**Case Study**
- Evidence level: anecdotal, qualified, evidenced
- Must address a problem and validate a capability

**Demonstration**
- Format: interactive, video, walkthrough, live
- Demonstrates a capability in action

**Testimonial**
- Client endorsement or testimonial

### Resource Concepts

**White Paper**
- In-depth authoritative report

**Executive Brief**
- Concise executive-level summary

**Report**
- Data or analysis report

**Presentation**
- Slide deck or presentation

**Video**
- Video asset

**Event**
- Conference, workshop, roundtable, webinar, hybrid

**Engagement Model**
- Category: assessment, workshop, implementation, ongoing_governance, advisory
- Duration in weeks; price tier; proof required flag

### Audience Concepts

**Audience Role**
- ceo, cto, board, investor, partner, developer, researcher, student
- Seniority: entry, mid, senior, executive, board

**Preferred Engagement**
- Must reference valid Engagement Model keys from ontology

### Content Type Concepts

**Content Type Category**
- core, knowledge, proof, resources, conversion

**Content Variable**
- Reserved names (never add to variable lists): FIRST_NAME, LAST_NAME, EMAIL, RESEND_UNSUBSCRIBE_URL

### Evidence Levels (controlled vocabulary)
- anecdotal: Unverified claim, no supporting evidence
- qualified: Has supporting logic or reasoning, but not empirical evidence
- evidenced: Empirically supported with data, case studies, or references to the evidence ledger (65 claims: 18 evidenced / 29 qualified / 18 unqualified from ADR-020)

### Reserved Terms (glossary control)
These terms have protected status and must not be redefined or duplicated:
- AI Company Builder (singular canonical definition only)
- Lightspeed (brand, case-sensitive)
- Pharos (department/brand, case-sensitive)

### Forbidden Terminology Patterns
- "AI Company Builder" appearing as both a service key AND a capability key AND a product name simultaneously
- "AI Strategy" used as both a methodology category AND a service title AND a framework name
- Any concept that serves as service, methodology, product, AND company division in the same context

## Terminology Issue Categories

1. **Duplicate Concepts**: Same concept defined under multiple keys or entity types
2. **Ambiguous Terms**: Terms without clear, single definitions
3. **Scope Creep**: Concepts that outgrow their original category (e.g., methodology becoming a service)
4. **Brand Dilution**: Brand terms used generically without proper attribution
5. **Evidence Gaps**: Claims about capabilities without referenced evidence ledger entries