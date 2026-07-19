# Legal Standard Operating Procedure

**Document ID:** SOP-LEGAL-001
**Department:** Legal
**Owner:** Legal Executive
**Classification:** Internal
**Last Updated:** July 2026

---

## 1. Purpose

This Standard Operating Procedure establishes the processes for contract management, compliance oversight, intellectual property protection, data privacy, and regulatory adherence within Light Speed Holdings' AI Company Builder. It ensures the organization operates within legal boundaries while maintaining the agility needed for an AI-native company.

## 2. Scope

This SOP applies to all legal activities including:

- Contract creation, review, and management
- Intellectual property protection and licensing
- Data privacy and protection compliance (GDPR, CCPA)
- Terms of Service and Privacy Policy maintenance
- Regulatory compliance for AI/ML systems
- Open source license compliance
- Risk assessment and mitigation
- Legal dispute management

## 3. Roles and Responsibilities

| Role | Agent/Person | Responsibilities |
|------|-------------|-----------------|
| Legal Lead | Executive | Legal strategy, contract approval, compliance oversight |
| Compliance Officer | Specialist | Regulatory monitoring, audit preparation, policy enforcement |
| CTO | `cto` | Technical compliance, security measures, IP protection |
| CFO | Department executive | Financial compliance, tax obligations, vendor contracts |
| CEO / Founder | Human operator | Final legal decisions, board governance, strategic risk |

## 4. Contract Management

### 4.1 Contract Types

| Contract Type | Typical Value | Approval Required | Review Cycle |
|--------------|--------------|-------------------|-------------|
| Customer subscription | $49 - $10,000/mo | Sales Lead + Legal | Annual |
| Vendor/LLM provider | Variable | CFO + Legal | Annual |
| Employment/contractor | Variable | HR Lead + Legal | Per hire |
| Partnership agreement | Variable | CEO + Legal | Per deal |
| Open source license | N/A | CTO + Legal | Per inclusion |

### 4.2 Contract Workflow

**Step 1: Request**

- Initiator submits a contract request via the `MessageBus`
- Include: contract type, counterparty, key terms, urgency level

**Step 2: Draft**

- Legal Lead or designated agent creates the initial draft
- Use approved templates where available
- Include all required clauses (see Section 4.3)

**Step 3: Review**

- Technical review by CTO (for technical contracts)
- Financial review by CFO (for financial commitments)
- Legal review by Legal Lead (for all contracts)

**Step 4: Negotiation**

- Track all negotiation changes in the contract record
- Escalate non-standard terms to Legal Lead
- Document all concessions and their rationale

**Step 5: Execution**

- Obtain required signatures
- Store executed contract in the contract repository
- Notify relevant parties of execution

**Step 6: Monitoring**

- Track key dates (renewal, termination, SLA deadlines)
- Automated reminders 60 days before renewal
- Performance monitoring against contract terms

### 4.3 Required Contract Clauses

Every contract must include:

1. **Scope of services**: Clear description of what is provided
2. **Term and termination**: Duration and exit provisions
3. **Payment terms**: Amount, schedule, late payment penalties
4. **Intellectual property**: Ownership and licensing of work product
5. **Confidentiality**: Non-disclosure obligations
6. **Data protection**: GDPR/CCPA compliance provisions
7. **Limitation of liability**: Cap on damages
8. **Indemnification**: Mutual indemnification provisions
9. **Dispute resolution**: Governing law and arbitration/mediation
10. **Force majeure**: Excusable non-performance events

## 5. Intellectual Property

### 5.1 IP Ownership

Light Speed Holdings' IP includes:

| IP Type | Ownership | Protection Method |
|---------|-----------|------------------|
| Source code | Light Speed Holdings | Proprietary license (Apache 2.0 at v1.0) |
| Agent definitions | Light Speed Holdings | `company-registry.yaml` (trade secret) |
| Prompt templates | Light Speed Holdings | Trade secret |
| Brand assets | Light Speed Holdings | Trademark |
| Documentation | Light Speed Holdings | Copyright |
| Customer data | Customer | Privacy Policy, DPA |

### 5.2 Open Source Compliance

The AI Company Builder uses the following open source components:

| License | Components | Obligations |
|---------|-----------|-------------|
| Apache 2.0 | Target license at v1.0 | Attribution, state changes |
| MIT | Python dependencies | Attribution |
| GPL | None currently | N/A |

**Compliance requirements:**

1. Maintain a Software Bill of Materials (SBOM) in `pyproject.toml`
2. Include license headers in all source files
3. Include attribution notices in distribution packages
4. Review new dependencies for license compatibility before adding
5. Never include GPL-licensed code in proprietary components

### 5.3 IP Protection Measures

- All source code is version-controlled in a private repository
- API keys and secrets are stored in environment variables, never in source
- Agent prompt templates are considered trade secrets
- Customer data is isolated and encrypted
- Regular security audits of the `ToolRunner` sandbox

## 6. Data Privacy

### 6.1 Data Categories

| Data Type | Category | Retention | Protection |
|-----------|----------|-----------|-----------|
| Agent configurations | Business data | Duration of service | Encryption at rest |
| Task data | Business data | 90 days | Encryption at rest |
| LLM usage logs | Operational data | 90 days | Access controls |
| Cost tracking data | Financial data | 1 year | Access controls |
| Customer PII | Personal data | Per Privacy Policy | Encryption, access controls |
| API keys | Credentials | Duration of service | Environment variables only |

### 6.2 GDPR Compliance

For customers in the EU:

| Requirement | Implementation | Evidence |
|------------|---------------|---------|
| Lawful basis | Consent + legitimate interest | Privacy Policy, consent records |
| Data minimization | Only collect necessary data | Data inventory |
| Purpose limitation | Use data only for stated purposes | Privacy Policy |
| Storage limitation | Retention periods defined | Data retention schedule |
| Right of access | Customers can request their data | Data export mechanism |
| Right to erasure | Customers can delete their data | Data deletion mechanism |
| Data portability | Export in standard formats | JSON/CSV export |
| Breach notification | 72-hour notification to authority | Incident response plan |

### 6.3 CCPA Compliance

For customers in California:

- **Right to know**: Customers can request what data we collect
- **Right to delete**: Customers can request data deletion
- **Right to opt out**: Customers can opt out of data sale (we do not sell data)
- **Non-discrimination**: No different service based on privacy choices

### 6.4 Data Processing

LLM data processing considerations:

1. **Data sent to LLM providers**: Task prompts and agent context are sent to the selected provider (OpenAI, Anthropic, DeepSeek, or Ollama)
2. **Local processing option**: Ollama models process data locally with no external transmission
3. **Data retention by providers**: Governed by each provider's data policy
4. **Customer notification**: Privacy Policy discloses LLM data processing

## 7. Regulatory Compliance

### 7.1 AI/ML Regulations

| Regulation | Jurisdiction | Relevance | Status |
|-----------|-------------|-----------|--------|
| EU AI Act | European Union | AI system risk classification | Monitoring |
| NIST AI RMF | United States | AI risk management framework | Voluntary compliance |
| ISO 42001 | International | AI management system standard | Monitoring |

### 7.2 Software Compliance

| Requirement | Implementation | Verification |
|------------|---------------|-------------|
| Export controls | No restricted technology | Annual review |
| Accessibility | WCAG 2.1 AA for dashboard | Quarterly audit |
| Industry standards | SOC 2 Type II (target) | Annual audit |

## 8. Risk Assessment

### 8.1 Legal Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| IP infringement | Low | High | License review, legal opinions |
| Data breach | Medium | Critical | Encryption, access controls, insurance |
| Contract dispute | Medium | Medium | Clear contracts, documentation |
| Regulatory change | Medium | Medium | Monitoring, legal counsel |
| Open source contamination | Low | High | License review, SBOM |

### 8.2 Risk Review Cadence

| Review | Frequency | Owner | Focus |
|--------|-----------|-------|-------|
| Contract portfolio review | Quarterly | Legal Lead | Active contracts, renewals |
| Regulatory monitoring | Monthly | Compliance Officer | New regulations, guidance |
| Security audit | Quarterly | CTO | Vulnerabilities, compliance |
| Insurance review | Annually | CFO | Coverage adequacy |

## 9. Escalation Procedures

| Condition | Escalate To | SLA |
|-----------|------------|-----|
| Potential IP infringement | Legal Lead + CEO | Immediate |
| Data breach suspected | Legal Lead + CTO + CEO | Immediate |
| Regulatory inquiry | Legal Lead + CEO | 24 hours |
| Contract dispute > $10,000 | Legal Lead + CFO | 24 hours |
| New regulation impact | Compliance Officer + Legal Lead | 1 week |
| Customer privacy complaint | Legal Lead + CS Lead | 24 hours |

## 10. Key Performance Indicators

| KPI | Target | Frequency | Owner |
|-----|--------|-----------|-------|
| Contract review turnaround | < 5 business days | Per contract | Legal Lead |
| Compliance audit pass rate | 100% | Per audit | Compliance Officer |
| Legal dispute count | 0 | Quarterly | Legal Lead |
| IP filing completeness | 100% | Per filing | Legal Lead |
| Privacy complaint resolution | < 48 hours | Per complaint | Legal Lead |
| Regulatory monitoring coverage | 100% of applicable regulations | Monthly | Compliance Officer |

## 11. Compliance Requirements

- All contracts must be reviewed before execution
- Open source licenses must be reviewed before inclusion
- Data processing activities must be documented
- Privacy Policy must be updated within 30 days of data practice changes
- Legal risk assessments must be conducted quarterly
- All legal matters must be documented in the contract repository

## 12. Related Documents

- `docs/legal/terms-of-service.md` - Standard Terms of Service
- `docs/legal/privacy-policy.md` - Privacy Policy
- `LICENSE` - Software license (Proprietary, transitioning to Apache 2.0)
- `docs/COMPANY-CONSTITUTION.md` - Governance and compliance framework
- `docs/RISK-REGISTER.md` - Risk register and mitigation plans

---

*This document is maintained by the Legal department. Updates require Legal Lead approval.*
