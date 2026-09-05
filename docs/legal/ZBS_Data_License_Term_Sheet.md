# DATA LICENSE AGREEMENT — TERM SHEET
## Light Speed Holdings × Zodiak Broadcasting Station (ZBS)
### "Chichewa Audio Archive License for National Language Data Trust"

**Status:** DRAFT — For Discussion Only
**Date:** August 2026
**Confidentiality:** CONFIDENTIAL

---

## 1. PARTIES

| Party | Role | Entity |
|-------|------|--------|
| **Light Speed Holdings Inc.** | Licensee / AI Platform Developer | Delaware C-Corp |
| **Zodiak Broadcasting Station** | Licensor / Media Archive Owner | Malawi Registered Company |

---

## 2. LICENSED MATERIALS

### 2.1 Audio Archive
- **Volume**: ~7,000 hours of Chichewa broadcast recordings
- **Format**: WAV/MP3 (various bitrates); metadata in CSV/JSON
- **Coverage**: 2015-2026; News, agriculture programs, talk shows, dramas, music
- **Dialects**: Central (standard), Northern, Southern — approximately 60/25/15 split
- **Speakers**: Professional announcers, farmers, experts, officials, callers

### 2.2 Text Corpus (Included)
- **Volume**: ~50M words (published articles, scripts, transcripts)
- **Format**: Plain text / JSONL with metadata
- **Source**: ZBS News digital archive, program scripts, social media captions

### 2.3 Metadata (Included)
- Broadcast date/time, program name, speaker IDs (where available), topic tags, geographic focus

---

## 3. GRANT OF RIGHTS

### 3.1 License Scope
| Right | Granted | Terms |
|-------|---------|-------|
| **Training Use** | ✅ Yes | Perpetual, worldwide, irrevocable (except termination for cause) |
| **Inference Use** | ✅ Yes | Models trained on Licensed Materials may be deployed commercially |
| **Model Weight Distribution** | ✅ Yes | Fine-tuned model weights may be shared with Malawi Govt, WB, OI |
| **Derivative Works** | ✅ Yes | Annotated transcripts, aligned datasets, synthetic derivatives |
| **Sub-licensing** | ❌ No | Except to: Malawi Govt, World Bank, Opportunity International (named partners) |
| **Public Release of Raw Audio** | ❌ No | Only aggregated statistics, benchmark results, model cards |
| **Broadcast/Rebroadcast** | ❌ No | Not a content distribution license |

### 3.2 Exclusivity
- **Exclusive for**: Chichewa language model training (no other party gets this archive for AI training)
- **Non-exclusive for**: ZBS may license same archive for non-AI purposes (research, education, commercial sync)

### 3.3 Territory
Worldwide (model deployment); Data processing primarily in Malawi/EU

---

## 4. COMPENSATION

### 4.1 License Fees
| Year | Annual Fee | Payment Schedule |
|------|------------|------------------|
| Year 1 | **$50,000** | 50% on Effective Date; 50% on Day 90 (data delivery milestone) |
| Year 2 | **$35,000** | Annual in advance |
| Year 3 | **$35,000** | Annual in advance |
| **Total (3 years)** | **$120,000** | |

### 4.2 Revenue Share
- **10% of Net Revenue** from ZBS-branded services ("ZBS AI" hotline, co-branded apps)
- **Net Revenue** = Gross revenue minus: payment processing, telecom costs, direct third-party costs
- **Reporting**: Quarterly within 30 days; Annual audit right
- **Minimum Annual Guarantee**: $5,000 (Year 2+), creditable against revenue share

### 4.3 Co-Branded "ZBS AI" Hotline (IVR + WhatsApp)
| Term | Detail |
|------|--------|
| **Brand** | "ZBS AI powered by Light Speed" / "ZBS UlangiziAI" |
| **Revenue Split** | 60% ZBS / 40% Light Speed (after telecom/platform costs) |
| **Operations** | Light Speed runs platform; ZBS provides promotion, content, farmer trust |
| **Data** | ZBS owns caller data; Light Speed processes per DPA |

---

## 5. DELIVERY & QUALITY

### 5.1 Delivery Milestones
| Milestone | Deadline | Acceptance Criteria |
|-----------|----------|---------------------|
| **NDA Execution** | Day 1 | Mutual NDA signed |
| **Sample Delivery** | Day 14 | 100 hours (stratified by dialect, year, program type) |
| **Quality Audit** | Day 21 | Light Speed completes audio quality + metadata review |
| **Full Delivery** | Day 60 | Complete archive + metadata on encrypted drives / secure transfer |
| **Ingestion Complete** | Day 90 | Pipeline processed; dataset versioned on HuggingFace (private) |

### 5.2 Quality Standards
- **Audio**: Minimum 16kHz sample rate; <10% clipping; speaker diarization feasible
- **Metadata**: ≥90% records have date, program, topic; ≥70% have speaker region
- **Transcription Baseline**: Whisper-large-v3 WER < 25% on sample (pre-fine-tune)
- **Remediation**: If >15% of hours fail quality, ZBS provides replacement or pro-rata fee reduction

---

## 6. INTELLECTUAL PROPERTY

### 6.1 Ownership
- **Copyright in Recordings**: Remains with ZBS (or original rights holders)
- **Copyright in Transcripts/Annotations**: Joint (Light Speed creates; ZBS owns source)
- **Model Weights**: Light Speed owns; ZBS receives royalty-free license for own use
- **Benchmark Results**: Light Speed owns; ZBS may use for marketing

### 6.2 Attribution
- Model cards / publications: "Training data includes Zodiak Broadcasting Station archive, used under license"
- ZBS AI hotline: "Powered by ZBS archive + Light Speed platform"

### 6.3 Moral Rights
ZBS retains right to object to derogatory use of archive (e.g., hate speech generation, political manipulation)

---

## 7. DATA PROTECTION & COMPLIANCE

### 7.1 Personal Data in Archive
- **Caller voices**: May contain identifiable voices (call-in shows)
- **Speaker names**: Announcers, public figures, some callers
- **Treatment**: Light Speed will:
  - Anonymize/pseudonymize before training (speaker ID hashing)
  - Not attempt speaker re-identification
  - Delete raw audio after model training complete (retain only model weights + anonymized transcripts)

### 7.2 Malawi Data Protection Act 2024 Compliance
- **Lawful Basis**: Legitimate interest (AI development for public good) + ZBS consent
- **Data Subject Rights**: Not practicable for training data; withdrawal → model retraining without
- **DPA**: Light Speed = Processor; ZBS = Controller (for archive)

### 7.3 MACRA / Broadcasting Compliance
- ZBS warrants license complies with Communications Act, broadcasting licenses
- No breach of artist/performer rights (ZBS clears or indemnifies)

---

## 8. CONFIDENTIALITY (MUTUAL NDA TERMS)

### 8.1 Confidential Information
- This Agreement terms, pricing, technical architecture
- ZBS: Archive content, unreleased programs, business metrics
- Light Speed: Model architecture, training methods, pipeline code

### 8.2 Exceptions
- Publicly known; Independently developed; Required by law (with notice)

### 8.3 Term
- **During Agreement + 3 years** post-termination
- **Trade Secrets**: Indefinite (training methodology, pipeline architecture)

### 8.4 Permitted Disclosure
- Employees/Contractors with need-to-know + NDA
- World Bank, Malawi Govt, OI (under their NDAs)
- Legal/financial advisors (under confidentiality)

---

## 9. WARRANTIES & INDEMNIFICATION

### 9.1 ZBS Warrants
- Owns/controls rights to license Archive for AI training
- No third-party claims (performers, music rights, news wire services) — **OR** ZBS will clear/indemnify
- Archive does not contain illegal content (hate speech, defamation, child exploitation)

### 9.2 Light Speed Warrants
- Will use Archive only per permitted scope
- Will implement industry-standard security (encryption at rest/transit, access controls)
- Will not attempt to reverse-engineer ZBS proprietary broadcast technology

### 9.3 Indemnification
| Claim Type | Indemnifying Party |
|------------|-------------------|
| IP Infringement (Archive content) | ZBS |
| IP Infringement (Model/Platform) | Light Speed |
| Data Protection Violation | Respective party per DPA roles |
| Regulatory Breach (MACRA, DPA) | Respective party |

### 9.4 Liability Cap
- **Aggregate Cap**: Total fees paid (3 years = $120k) — **except** IP infringement, data breach (gross negligence), willful misconduct

---

## 10. TERM & TERMINATION

| Provision | Term |
|-----------|------|
| **Initial Term** | 3 years from Effective Date |
| **Auto-Renewal** | 1-year terms unless 90-day notice |
| **Termination for Cause** | 60-day cure period (material breach) |
| **Termination for Convenience** | Not permitted Year 1; 180-day notice Year 2+ |
| **ZBS Termination Right** | If Light Speed uses Archive outside scope (immediate) |

### 10.1 Effect of Termination
- **License survives** for models already trained (perpetual inference right)
- **Raw Archive**: Return or certified destruction within 30 days
- **Derived Datasets**: Light Speed retains anonymized transcripts/alignments
- **Revenue Share**: Continues for ZBS-branded services during wind-down (180 days)

---

## 11. CO-MARKETING & PUBLICITY

| Activity | Terms |
|----------|-------|
| **Press Release** | Joint announcement within 30 days of signing (draft approval required) |
| **Logos** | Mutual use on websites, presentations, model cards |
| **Case Study** | Co-authored after 6-month pilot; mutual approval |
| **Conferences** | Joint speaking at Malawi AI Forum, AfricaCom, Indaba |
| **Social Media** | Cross-posting; ZBS gets approval on farmer-facing messaging |

---

## 12. DISPUTE RESOLUTION

1. **Executive Escalation** (15 days) — CEO/MD level
2. **Mediation** (Lilongwe, Malawi Arbitration Centre) — 30 days
3. **Arbitration** (Malawi Arbitration Act, English law, Lilongwe seat) — Binding
4. **Governing Law**: Malawi Law

---

## 13. SIGNATURES

| Light Speed Holdings | Zodiak Broadcasting Station |
|---------------------|----------------------------|
| Name: _______________ | Name: _______________ |
| Title: _______________ | Title: _______________ |
| Date: _______________ | Date: _______________ |

---

## APPENDIX A: SAMPLE DELIVERY SPECIFICATION

### Directory Structure (Encrypted Drive / SFTP)
```
/zbs-archive/
  ├── audio/
  │   ├── 2015/ 2016/ ... 2026/
  │   │   ├── news/ agriculture/ talkshows/ drama/ music/
  │   │   │   ├── program_001.wav
  │   │   │   └── program_001.json (metadata)
  │   │   └── ...
  │   └── manifest.csv (all files with checksums)
  ├── text/
  │   ├── news_articles.jsonl
  │   ├── program_scripts.jsonl
  │   └── social_captions.jsonl
  └── metadata/
      ├── speakers.csv (speaker_id, name, role, region, gender)
      ├── programs.csv (program_id, name, type, language, schedule)
      └── topics.csv (topic_id, name, hierarchy, keywords)
```

### Metadata Schema (JSON per audio file)
```json
{
  "file_id": "zbs_2023_ag_0042",
  "path": "audio/2023/agriculture/program_0042.wav",
  "checksum_sha256": "a1b2c3...",
  "duration_seconds": 1847,
  "sample_rate": 22050,
  "channels": 1,
  "broadcast_date": "2023-03-15",
  "broadcast_time": "06:30",
  "program_id": "ag_morning_show",
  "program_name": "Ulimi Wathu",
  "topic_ids": ["maize", "fertilizer", "AIP"],
  "speaker_ids": ["spk_announcer_01", "spk_farmer_12", "spk_expert_03"],
  "dialect_region": "central",
  "quality_score": 0.92,
  "transcription_status": "pending"
}
```

---

## APPENDIX B: MUTUAL NDA (STANDALONE — FOR IMMEDIATE EXECUTION)

*See separate document: `ZBS_Mutual_NDA.md` — 3-page mutual NDA for immediate signature to enable 100hr sample delivery by Day 14.*

---

*End of Term Sheet — Subject to Legal Review and Mutual Agreement*
