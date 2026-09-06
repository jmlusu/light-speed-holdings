# MUTUAL NON-DISCLOSURE AGREEMENT
## Light Speed Holdings Inc. × Zodiak Broadcasting Station
### For Chichewa Audio Archive Evaluation

**Effective Date:** _______________
**Confidentiality:** CONFIDENTIAL — EXECUTE BEFORE DATA SHARING

---

## 1. PARTIES

| Disclosing Party | Receiving Party | Entity |
|------------------|-----------------|--------|
| **Zodiak Broadcasting Station** | Light Speed Holdings Inc. | Malawi Registered Company / Delaware C-Corp |
| **Light Speed Holdings Inc.** | Zodiak Broadcasting Station | Delaware C-Corp / Malawi Registered Company |

**Collectively:** "Parties" | **Individually:** "Party"

---

## 2. PURPOSE

Evaluation of ZBS's Chichewa audio archive (~7,000 hours) for potential licensing to train a Chichewa-language agricultural AI model ("UlangiziAI v2") under the Malawi National Language Data Trust initiative, backed by World Bank and Gates Foundation.

---

## 3. CONFIDENTIAL INFORMATION

### 3.1 Definition
"Confidential Information" means any non-public information disclosed by either Party (Discloser) to the other (Recipient), whether oral, written, electronic, or visual, including:

**ZBS Confidential Information:**
- Audio recordings, transcripts, metadata, broadcast schedules
- Speaker identities, caller details, unaired content
- Business metrics, advertising rates, audience data
- Technical broadcast infrastructure, proprietary formats
- This Agreement's existence and terms

**Light Speed Confidential Information:**
- Model architecture, training methodology, pipeline code
- Agent orchestration platform design, APIs, SDKs
- Commercial terms, pricing, funding strategy
- Partner negotiations, go-to-market plans
- This Agreement's existence and terms

### 3.2 Exclusions
Information that: (a) is publicly known without breach; (b) was known to Recipient prior without obligation; (c) is independently developed without use of Confidential Information; (d) is received from third party without restriction.

---

## 4. OBLIGATIONS

### 4.1 Standard of Care
Recipient shall protect Confidential Information with **at least the same degree of care** it uses for its own confidential information (minimum: reasonable care).

### 4.2 Permitted Use
Confidential Information may only be used for: **Evaluation of the archive for AI training suitability** — including audio quality assessment, dialect coverage analysis, transcription benchmarking, and license term negotiation.

### 4.3 Permitted Disclosure
Recipient may disclose to:
- Employees, contractors, advisors with **need-to-know** and **bound by written confidentiality** no less protective than this Agreement
- World Bank, Malawi Government, Opportunity International — **only under their executed NDAs**
- Legal/financial regulators — **with prompt notice to Discloser** (unless prohibited by law)

### 4.4 Prohibited Actions
- No reverse engineering, decompilation, or speaker re-identification
- No copying beyond evaluation needs (max 200 hours for benchmarking)
- No training models on full archive without executed License Agreement
- No disclosure to competitors, media, or social platforms

---

## 5. DATA PROTECTION (SPECIAL PROVISIONS)

### 5.1 Personal Data in Archive
ZBS warrants archive may contain: caller voices, names, locations, phone numbers. Light Speed agrees to:
- Process only on encrypted, access-controlled systems
- Anonymize/pseudonymize before any model training
- Not attempt speaker re-identification
- Delete evaluation copies within 30 days of License execution or termination

### 5.2 Malawi Data Protection Act 2024
Both Parties comply with DPA 2024. For evaluation phase: ZBS = Controller; Light Speed = Processor.

---

## 6. INTELLECTUAL PROPERTY

### 6.1 No License Granted
This NDA grants **no license** under any IP rights. All Confidential Information remains Discloser's property.

### 6.2 Residuals
Recipient's unaided memory of general concepts/know-how (not specific data) is not restricted — **except** specific audio content, transcripts, speaker identities, and training methodology.

### 6.3 Feedback
Any suggestions, bug reports, or improvements provided by either Party may be freely used by the other without obligation.

---

## 7. TERM & TERMINATION

| Provision | Term |
|-----------|------|
| **Agreement Term** | 12 months from Effective Date |
| **Confidentiality Survival** | 3 years post-termination (Trade Secrets: indefinite) |
| **Termination** | Either Party may terminate with 15 days written notice |
| **Immediate Termination** | Material breach; insolvency; regulatory action |

### 7.1 Return/Destruction
Upon termination or Discloser's request: Recipient shall **return or certify destruction** of all Confidential Information (including copies) within 15 days. One archival copy may be retained by legal counsel for compliance.

---

## 8. REMEDIES

- **Injunctive Relief**: Breach causes irreparable harm; Discloser entitled to equitable relief without bond
- **Damages**: Actual + consequential damages
- **Attorney Fees**: Prevailing party recovers reasonable fees

---

## 9. GENERAL

### 9.1 Governing Law
Malawi Law. Courts of Lilongwe have exclusive jurisdiction.

### 9.2 Assignment
Neither Party may assign without consent — **except** to affiliate or acquirer of substantially all assets (assignee bound by this NDA).

### 9.3 Entire Agreement
This NDA supersedes all prior discussions. Amendments only in writing signed by both Parties.

### 9.4 Counterparts
May be executed in counterparts (including electronic/DocuSign), each an original.

### 9.5 No Partnership
Nothing herein creates partnership, joint venture, or agency relationship.

---

## 10. SIGNATURES

| LIGHT SPEED HOLDINGS INC. | ZODIAK BROADCASTING STATION |
|---------------------------|----------------------------|
| Signature: _______________ | Signature: _______________ |
| Name: _______________ | Name: _______________ |
| Title: _______________ | Title: _______________ |
| Date: _______________ | Date: _______________ |
| **Authorized Signatory** | **Authorized Signatory** |

---

## APPENDIX A: EVALUATION PROTOCOL (ATTACHED TO NDA)

### A.1 Sample Delivery (Day 1-3 post-NDA)
- **Volume**: 100 hours (stratified sample)
- **Format**: Encrypted USB drive / SFTP (AES-256)
- **Stratification**:
  - 40% Central dialect (standard)
  - 30% Northern dialect
  - 20% Southern dialect
  - 10% Code-switched (Chichewa-English)
  - By year: 2015-2018 (20%), 2019-2022 (40%), 2023-2026 (40%)
  - By program: News (30%), Agriculture (30%), Talk shows (20%), Drama/Music (20%)

### A.2 Evaluation Activities (Day 3-21)
| Activity | Tool/Method | Output |
|----------|-------------|--------|
| Audio quality audit | FFmpeg + custom scripts | Quality report (SNR, clipping, sample rate) |
| Speaker diarization test | pyannote.audio | Diarization error rate (DER) |
| ASR baseline | Whisper-large-v3 (zero-shot) | Word Error Rate (WER) by dialect |
| Topic classification | Keyword + embedding | Topic coverage map |
| Metadata completeness | Automated validation | % records with required fields |

### A.3 Deliverable to ZBS (Day 21)
- **Evaluation Report** (PDF): Quality scores, dialect coverage, WER benchmarks, licensing recommendation
- **Sample Transcripts** (10 hours): Whisper output + human spot-check (5%)
- **License Decision**: Proceed / Modify scope / Decline (with reasoning)

### A.4 Data Handling During Evaluation
| Control | Implementation |
|---------|----------------|
| Encryption at rest | VeraCrypt container / LUKS / AWS KMS |
| Encryption in transit | SFTP / TLS 1.3 |
| Access control | Named individuals only; MFA; audit logs |
| Logging | All access timestamped; retained 90 days |
| Deletion | Secure wipe (NIST 800-88) post-evaluation |

---

*End of Mutual NDA — Execute Before Any Data Transfer*
