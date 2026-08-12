# Data Processing Addendum (DPA)
## — GDPR / Malawi Data Protection Act 2017 / Donor Data Annex C —

> This Addendum is incorporated into every SOW for Offer B (BPA/chatbots) and
> Offer C (data/reporting) where client or donor personal data is processed.

---

## 1. Parties

- **Data Controller:** {{client_name}} ("Controller")
- **Data Processor:** Light Speed Holdings ("Processor")

## 2. Processing Details

### 2.1 Purpose of Processing
As specified in the applicable SOW: {{purpose_description}}

### 2.2 Categories of Data Subjects
- End customers (for chatbot data)
- NGO beneficiaries / program participants (for reporting)
- Survey respondents
- Staff / partner contact lists

### 2.3 Types of Personal Data
- Identity data (names, contact details)
- Demographic data
- Usage/interaction data (chat logs, survey responses)
- Financial data (payment references)

### 2.4 Data Processing Activities
| Activity | Description | Subprocessor | Lawful Basis |
|----------|-------------|-------------|--------------|
| Data collection | Surveys, forms, chatbot interactions | survey_researcher agent | Contractual |
| Data cleaning | Validation, deduplication | data_engineer agent | Contractual |
| Analysis | Dashboards, reports, insights | data_scientist agent | Legitimate interest |
| LLM processing | Data passed to LLM provider APIs for analysis | OpenAI/DeepSeek API | Contractual / Legitimate interest |
| Storage | Results persisted in client delivery folder | FileStore (encrypted) | Contractual |

## 3. Subprocessor Disclosure (Cross-border Transfer)

Processor uses cloud-based LLM provider APIs (OpenAI, DeepSeek, Grok) that are
hosted outside Malawi (USA, Singapore). Client acknowledges and consents to
this cross-border transfer by signing this Addendum. Processor's
`data_privacy_officer` maintains a Data Transfer Impact Assessment.

**Safeguards:** Standard contractual clauses are incorporated by reference via
the MSA, and Processor routes data to the cheapest provider tier by default
to minimize exposure. Client may request data not be sent to premium providers.

## 4. Data Security Measures

1. **Encryption at rest:** All client data encrypted via `ciso` security architecture.
2. **Access control:** RBAC enforced by `security_compliance_lead`; least-privilege.
3. **Audit logging:** All data access logged via `audit_trail_owner` (GAP-008 compliant).
4. **Agent isolation:** Each client engagement uses a separate agent hierarchy;
   cross-client data isolation enforced by `MessageBus` task routing.

## 5. Data Subject Rights

Processor will, upon Client's written instruction, assist Client in fulfilling:
- Right to access (via `data_privacy_officer`)
- Right to rectification (via `data_engineer`)
- Right to erasure / 30-day post-delivery deletion (default retention: 30 days)
- Right to data portability (export via `data_engineer`)

## 6. Retention and Deletion

| Data Type | Retention Period | Owner Agent |
|-----------|-----------------|-------------|
| Raw donor data | 30 days post-delivery | data_privacy_officer |
| Cleaned datasets | 30 days post-delivery | data_engineer |
| Aggregated dashboards | 30 days post-delivery | business_intelligence_engineer |
| Survey responses | 30 days post-delivery | survey_researcher |
| Audit logs | 1 year (audit trail policy) | audit_trail_owner |

Extended retention requires explicit written agreement and a separate storage SOW.

## 7. Breach Notification

Processor shall notify Controller **within 24 hours** of becoming aware of a
personal data breach, via the `incident_response_lead`. Notification includes:
(a) nature of breach, (b) categories/numbers of affected data subjects,
(c) likely consequences, (d) measures taken to address.

## 8. Liability

For Offer C (donor reporting), Processor's liability for data protection breaches
under this Addendum is limited to the fees paid for the specific reporting project,
per Section 8 of the MSA. Processor's total aggregate liability shall not exceed
the fees paid under the MSA in the 12 months preceding the claim.

---

**Acknowledged and accepted:**

| Controller (Client) | Processor (Light Speed Holdings) |
|---------------------|----------------------------------|
| Signature: _________ Date: ____ | Signature: _________ Date: ____ |
| Name: _______ | Name: _______ |
| Title: _______ | Title: _______ |
