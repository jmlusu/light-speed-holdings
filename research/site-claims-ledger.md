# Site Claims & Evidence Ledger

- Status: DRAFT v1 — descriptions good, pending owner review
- Date: 2026-09-15
- Owner: content-writer + research
- Ticket: T1, issue #252
- Supersedes: none

Classification: (a) fully evidenced / (b) qualified — labeled, internally consistent, or hedged / (c) unqualified — no provenance or contradicted.

Provenance read against repo root `C:\Users\jmlus\light-speed-holdings` (this workspace is a worktree copy). Line numbers are for the SPA sources under `src/` of that repo.

## 1. Home

| Claim | Location | Class | Evidence / Note |
|---|---|---|---|
| Proof strip: 90 Verified Agent Configurations / 2,373 Automated Regression Tests / 20 Departments Onboarded / 5-Tier (Human Approval Gates) | HomePage.tsx:31-35; HeroSection.tsx:79,170 | (a) | 90 & 20 verified via company-registry.yaml (90 agent ids, 20 distinct departments), docs/source-of-truth.yaml (90 = 89 AI + 1 human CEO); counted 2026-09-23. 2,373 documented live `pytest --collect-only` on 2026-09-10 (results/use-case-fact-pack.md:79); caveat: static `def test_` count is 2,211 + 25 parametrize decorators. 5-Tier backed by src/ai_company/executor/hitl_gate.py + tests. |
| "...every decision auditable" | HeroSection.tsx:79 | (b) — RESOLVED | Absolute quality claim; audit-trail design exists but no support that all 90 agents' decisions are auditable. **Remediated 2026-09-16:** copy now reads "decision logs auditable on request" (HeroSection.tsx:79). |
| "One human CEO directs 140+ AI agents" | siteContent.ts:38 | (b) — RESOLVED | Internal inconsistency: canonical is 90 (89 AI + 1 human CEO) per docs/source-of-truth.yaml (counted 2026-09-23). **Remediated:** site now uses canonical 90. |
| "10-day turnaround, ≥4.5/5 satisfaction, 30-day support window" | siteContent.ts:124 | (b) | Labeled commitment; no published satisfaction/measurement data. |
| "20-25 paid clients and 8 lighthouse clients in first 12 months" | siteContent.ts:125 | (b) | Forward target, not a delivered result; check whether surfaced to page. |
| "We target 99.99% platform uptime" | siteContent.ts:96 | (b) | Target, not measured; no SLO artifacts on site. Copy is explicitly hedged ("We target") and framed as an internal practice note — acceptable as a stated goal, not a delivered result. |

## 2. About

No metric claims. AboutSection.tsx is qualitative ("institutional charter // sovereign mission"; "Jack Mlusu, Founder & CEO, architect of the Pharos Policy Track"). No classified rows.

## 3. AI Company Builder

| Claim | Location | Class | Evidence / Note |
|---|---|---|---|
| "Governed 90-Agent Swarm & 20-Department Topology" + "5-tier HITL gates" | AiCompanyBuilderSection.tsx:75-76 | (a) | Registry + hitl_gate.py backing as above. |
| FOW-01 "1-human, 89-agent organisation"; FOW-03 "proven in-house daily" | siteContent.ts:665-666 | (a) | 90 registry-verified; daily operation corroborated by evidence probes + repo-audit. |
| "10x-100x operational throughput with sub-second verified dispatch" | AiCompanyBuilderSection.tsx:246 | (b) — RESOLVED | Absolute performance claim, no bench artifact. **Remediated:** copy now reads "Designed for 10x–100x operational throughput with sub-second verified dispatch" (design intent, not measured). |
| "Sub-second latency SLA guarantees" | AiCompanyBuilderSection.tsx:418 | (b) — RESOLVED | SLA stated but no measurement/provenance. **Remediated:** now "Sub-second latency SLAs (target)". |
| Simulated console: "Entire AI Company generated in 1.42s", "2,373 tests passing", "342 Workflow Dispatch & Escalation Channels", "1,280 indexed memory vectors", "90 agents / 20 departments / 1 board" | AiCompanyBuilderOsExplorer.tsx:61-96,255,304,308 | (b) — RESOLVED | Typing-animation demo output; not a tagged measured run. 2,373 is documented (see Home), remainder unverifiable. **Remediated:** terminal header now labels output "SIMULATED OUTPUT — NOT A LIVE RUN" (AiCompanyBuilderOsExplorer.tsx:393). |
| 90-day pilot → full scale; "2-Week Advisory Sprint to 90-Day Co-Built Pilot" | siteContent.ts:638; OfferingDetailCard.tsx:242; PillarNavigationCard.tsx:17 | (b) | Engagement-model offer, not a result claim. |
| Licensing: MWK 3,500,000 (~$2,000) + $200/mo support | siteContent.ts:642; OfferingsPage.tsx:247,263 | (b) | Internally consistent MWK/USD; pricing is offer, not evidence. |

## 4. Technology

| Claim | Location | Class | Evidence / Note |
|---|---|---|---|
| Metrics bundle 144 / 2,373 / 20 / 5-TIER | siteContent.ts:593-598; TechnologyPage.tsx:25 | (a) | As Home. |
| Four-gate CI "ruff + mypy + bandit + 2,373 pytest gates must pass before a change lands" | TechnologyPage.tsx:26; EvidencePage.tsx:64-65 | (b) | CI gates exist (pre-commit ruff/mypy/bandit, pytest); 2,373 is a documented collection count, not a full passing run artifact. |
| Five-Tier Human Approval Gates | siteContent.ts:574 (GOVERNANCE_FACTS 1) | (a) | hitl_gate.py + tier-enforcement tests. |
| SHA-256 chained append-only audit trails | siteContent.ts:575 | (b) | Design/implementation claim; artifacts not published. |
| RBAC + least privilege | siteContent.ts:576 | (a) | Dashboard RBAC tests exist (tests/unit/test_dashboard_rbac.py). |
| Data Protection by Default (Malawi DPA) | siteContent.ts:577 | (b) | Policy claim, self-reported. |
| Four-Gate Onboarding G1-G4; provider-agnostic/Ollama | siteContent.ts:578-580 | (b) | Process claims; G1-G4 in client-onboarding policy. |
| Canonical 7-tool runtime vocabulary | siteContent.ts:582; TechnologyPage.tsx:24 | (a) | ToolRunner canonical list (AGENTS.md §8) + tool-vocabulary tests. |
| Zero-Cloud Boundary deployment option | siteContent.ts:587 | (b) | Product option claim. |

## 5. Solutions

| Claim | Location | Class | Evidence / Note |
|---|---|---|---|
| Agentic AI: "90-agent operation runs daily" proof label | siteContent.ts:248 | (a) | Registry + evidence probes. |
| Digital Transformation: "Fieldable in 2026 — ready for client engagement"; pricing "to be validated with prospects" | siteContent.ts:1141; useCaseCatalogData.ts:107 | (b) — RESOLVED | Past-tense "pricing validated against real prospects" removed 2026-09-16; reverified 2026-09-23 — src now future-tense, matches USE-CASE-CATALOG.md:76. |
| Data & Intelligence: "In pilot with UNDP Malawi stakeholders" | siteContent.ts:331 | (b) | Self-reported pilot; no external or repo artifact. |
| Automation: "gated on G1-G4 security review" | siteContent.ts:372 | (b) | Process claim; G1-G4 policy exists. |
| Strategy & Advisory: "90-day pilot window" | siteContent.ts:411 | (b) | Offer, not result. |
| Governance: "SADC framework — region's first operational governance standard — authored by the CEO and submitted to member-state ministers and regulators" | siteContent.ts:461-462; EvidencePage.tsx:162; siteContent.ts:777 | (b) — RESOLVED | Unverifiable superlative + submission claim; no submission artifact in repo. **Remediated:** siteContent.ts:777 → "authored by the CEO as a policy proposal"; EvidencePage.tsx:162 → "graduated-autonomy governance standard… authored by the CEO as a policy proposal targeted at SADC Member State digital ministers"; siteContent.ts:461 already qualified ("proposes", "targeted at"). |
| Financial services: "actively sought by COMESA/IDEA" | siteContent.ts:527 | (b) | Internal-only provenance (results/use-case-fact-pack.md:246 attributes to docs/Pharos/case-study-pipeline.md). |

## 6. Industries

| Claim | Location | Class | Evidence / Note |
|---|---|---|---|
| Public Sector: "in pilot with UNDP Malawi stakeholders" | siteContent.ts:508 | (b) | Self-reported; consistent with Solutions.Data. |
| Financial: "No signed engagement exists; no paid client deployments to date." | siteContent.ts:534 | (a) | Corroborated by results/use-case-fact-pack.md + EvidencePage honesty policy. |
| Healthcare: "No confirmed partnership with any named health organisation" | siteContent.ts:553 | (a) | Corroborated by EvidencePage PC-02. |
| Agriculture: "fieldable 2026" | siteContent.ts:565 | (b) | Honesty-badged status. |
| Government: National AI Strategy consultation submission "published" | siteContent.ts:489 | (b) | Self-reported; artifact not located in repo evidence. |

## 7. Work / Evidence

| Claim | Location | Class | Evidence / Note |
|---|---|---|---|
| METRICS 144 / 2,373 / 20 / 5-TIER with explicit sources | EvidencePage.tsx:31-52 | (a) | Sources verified (company-registry.yaml, pytest collection doc, hitl_gate.py). |
| PC-01 J&S StopOver Bar "world's smallest AI-native bar" | EvidencePage.tsx:103; siteContent.ts:726 | (b) — RESOLVED | Unsupported superlative; no sizing data. **Remediated:** superlative removed from EvidencePage.tsx:103, siteContent.ts:726, and useCaseCatalogData.ts:470 — now "A real, non-tech SME in Malawi running agentic decision support…". |
| PC-04 Meta-deployment: "90 agents / 20 departments / five-tier... operating daily" | EvidencePage.tsx:110; siteContent.ts:732 | (a) | Registry + evidence probes + repo-audit (own operations). |
| PC-02 Health: "in pilot... no confirmed partnership" | EvidencePage.tsx:117 | (a) | Matches Industry.Healthcare disclaimer. |
| PC-03 "No signed engagement exists" (VSLA) | EvidencePage.tsx:124 | (a) | Matches industry-financial honesty statement. |
| PC-05 Partnership with Ministry of Agriculture "in pilot development" | EvidencePage.tsx:131 | (b) | Self-reported; internal case-study pipeline only. |
| POL-02 Governance pattern in-house: 5-tier, immutable trails, RACI, risk tiers, G1-G4 onboarding | EvidencePage.tsx:148; siteContent.ts:765 | (a) | Tested code paths (hitl, tier enforcement, executor audit trail, client-onboarding policy). |
| POL-03 Partnership with MUBAS / UNIMA | EvidencePage.tsx:155 | (b) | Self-reported academic partnerships. |
| SADC: "region's first operational governance standard — authored by CEO, submitted to Member State digital ministers and regulators, central banks, regional development banks" | EvidencePage.tsx:162 | (b) — RESOLVED | No submission artifact; unverifiable superlative. **Remediated:** now "governance standard … authored by the CEO as a policy proposal targeted at SADC Member State digital ministers, telecom regulators (MACRA, CRASA), central banks, and regional development banks." |
| HONESTY_POLICY "Benchmarks are dated and regenerated on every release" | EvidencePage.tsx:84 | (b) | Process claim; partially true (reports/ run 2026-09-14). |

## 8. Insights / Pharos

| Claim | Location | Class | Evidence / Note |
|---|---|---|---|
| TOME I "12 min read / 1,420 Executive Downloads" | PharosSection.tsx:18-19 | (b) — RESOLVED | PHAROS_HITS=0 across docs, src, company, reports, results, config, brand. No download-tracking artifact. **Remediated:** all four fabricated download counts removed from PharosSection.tsx; footer now renders `{wp.tome} — {wp.author}`. |
| TOME II "15 min read / 980 Executive Downloads" | PharosSection.tsx:30-31 | (b) — RESOLVED | Same. **Remediated:** count removed. |
| TOME III "18 min read / 2,150 Technical Downloads" | PharosSection.tsx:42-43 | (b) — RESOLVED | Same. **Remediated:** count removed. |
| TOME IV "20 min read / 1,840 Central Bank Downloads" | PharosSection.tsx:54-55 | (b) — RESOLVED | Same. Read-time estimates were minor (c). **Remediated:** count removed (read-time may remain). |

## 9. Offerings

| Claim | Location | Class | Evidence / Note |
|---|---|---|---|
| Offer A1-A4 pricing (MWK/USD, turnaround) | OfferingsPage.tsx:65-97 | (b) | Pricing offer; note USE-CASE-CATALOG pricing-validation tension. |
| Offer B/C "BLOCKED — DO NOT SELL" + governance notes | OfferingsPage.tsx:107-149,156-197 | (a) | BLOCKED state documented in USE-CASE-CATALOG.md + client-onboarding policy. |
| Offer E1 "FIELDABLE IN 2026 — PROVEN IN-HOUSE" license | OfferingsPage.tsx:241 | (b) | Engine in-house = (a); fieldable-license status self-declared = (b). |
| Enterprise line "in active development — modules not yet built" | OfferingsPage.tsx:500,531 | (a) | Explicit honest disclosure matching catalog status. |
| "Minimum viable deployment MWK 150,000 (~$85)" | OfferingsPage.tsx:62; siteContent.ts:151 | (b) | Internally consistent conversion. |
| "Verified Institutional Benchmark — audited telemetry in live production deployments across SADC commercial banking, national revenue authorities, and transport corridors" | OfferingDetailCard.tsx:182-190 | (b) — RESOLVED | Contradicted EvidencePage.tsx:380 "Nothing has been delivered to paying clients yet" and repo-audit (own-company deployment only). **Remediated:** now "Verified In-House Reference — Verified against LightSpeed's own running operations and regenerated benchmarks — not client deployments. Engagements with paying clients have not yet delivered." |
| Governance badge "Basel IV / King IV / SADC Regulatory Compliant" | CoreOfferingsSection.tsx:43 | (b) — RESOLVED | Unqualified compliance-certification claim; no certification artifact. **Remediated:** now "Designed to align with SADC / King IV / Basel IV governance patterns". |
| "Zero Cloud SaaS Leakage" | CoreOfferingsSection.tsx:216 | (b) — RESOLVED | Absolute guarantee. **Remediated:** now "Designed for Zero Cloud Leakage". |
| "144 Verified Agent Configurations in Production" | CoreOfferingsSection.tsx:78 | (a) | 144 verified; "in production" = own operations (context matters for the word "Production"). |
| "deliver production code with zero data leakage" | OfferingDetailCard.tsx:245 | (b) — RESOLVED | Absolute guarantee. **Remediated:** now "deliver production code under our standard confidentiality and security controls." |
| Comparison table "9-month review cycles" (industry generic) | CoreOfferingsSection.tsx:232 | (b) — RESOLVED | Illustrative figure, no source. **Remediated:** figure removed — now "infrequent review cycles". |
| "All hosted in-region, compliant with Malawi DPA" | OfferingsPage.tsx:155; siteContent.ts:330 | (b) | Policy claim. |
| OH B1 hosting "MWK 100,000/mo recurring" | OfferingsPage.tsx:148 | (b) | Pricing offer. |
| Haomtgv Governance tab rings: "100% Statutory Compliance // Zero Ungoverned State Changes"; "<180ms" routing; "0.00% (Strict Air-Gap)"; "100% BLOCKED EGRESS"; "5 Discrete Risk Tiers // 0% Hallucinated Commits"; "48hr → 14.2s mobile money settlement audit; 25k+ smallholders served"; "Tested across 90 agents running daily"; "PROVEN IN PRODUCTION" | HaomtgvGovernanceFramework.tsx:96,144,146,223,237-246,243-246,452,461,768,1002,1005 | (b) — RESOLVED | **Remediated:** :96 → "Policy-mapped Compliance // No Ungoverned State Changes"; :144 → "<180ms" removed (design description only) & :146 → "Sub-Second Local Dispatch // Race-Condition-Free by Design"; :223 → "0% Hallucinated Commits (internal tests)"; :246 → "SHA-256 Hash Chaining // Field deployments pending" + principle "In Design for Field Use"; :452 → "STRICT AIR-GAP POSTURE"; :461 → "PROVEN IN-HOUSE OPERATIONS"; :768 → "0.00% (Strict Air-Gap Policy)"; :1002 → "<180ms) target"; :1005 → "egress blocked by design"; :1282 → "PROVEN IN-HOUSE: Operating daily…". |
| "48hr → 14.2s mobile money settlement audit; 25k+ smallholders served"; "48h → 14.2s Latency Collapse" | HaomtgvGovernanceFramework.tsx:244,246 | (b) — RESOLVED | No repo artifact. **Remediated:** 14.2s/25k claims removed entirely — replaced with "In Design for Field Use: mobile money settlement audit and smallholder-serving workflows are under development, not yet delivered." / "Field deployments pending". |

## 10. Contact / Footer

| Claim | Location | Class | Evidence / Note |
|---|---|---|---|
| "A human reviews every submission and responds within 12 business hours" (+ modal duplicate) | ContactSection.tsx:45,55,94; ExecutiveBriefingModal.tsx:113 | (b) — RESOLVED | Unverifiable service promise; no SLA telemetry. **Remediated:** ContactSection.tsx:92 and modal/confirmation copy now read "we respond to qualified enquiries within two business days". |
| "Offices in Southern Africa and International Advisory Network" | ContactSection.tsx:59 | (b) — RESOLVED | Presence claim; no registrations found. **Remediated:** now "Based in Lilongwe, Malawi, with an international advisory network across Southern Africa". |
| Engagement scopes "2-Week Sprint / 90-Day Pilot / Enterprise / Boardroom" + "Within 30 days" default | ContactSection.tsx:17-19,197-200 | (b) | Freelancer model, no result claim. |
| "Strict non-disclosure agreement standard" | ContactSection.tsx:51 | (b) | Qualitative policy. |

## 11. Data Ledger (provenance counts)

| Item | Claimed | Verified | Source / Note |
|---|---|---|---|
| Agent configurations | 90 | 90 | company-registry.yaml (AGENT_IDS=90); docs/source-of-truth.yaml (89 AI + 1 human CEO); counted 2026-09-23; cards.reconcile registry=90 live=90 |
| Departments | 20 | 20 | company-registry.yaml DISTINCT_DEPARTMENTS=20; evidence json tree.departments company=20 config=20 |
| Regression tests | 2,373 | 2,373 (documented), 2,211 + 25 parametrize (static) | results/use-case-fact-pack.md:79 live `pytest --collect-only -q` 2026-09-10; static count differs — recommend re-run before quoting |
| HITL gates | 5-TIER | code exists | src/ai_company/executor/hitl_gate.py + tier-enforcement tests |
| Auditable decisions | "every decision auditable" | partial | audit-trail design; no full-coverage evidence. **RESOLVED:** copy hedged to "decision logs auditable on request" |
| 48hr→14.2s settlement audit | search | 0 artifacts | only site source + Playwright site capture. **RESOLVED:** claim removed |
| 25k+ smallholders | search | 0 artifacts | same. **RESOLVED:** claim removed |
| Pharos downloads 1,420/980/2,150/1,840 | search | 0 artifacts | repo-wide PHAROS_HITS=0. **RESOLVED:** counts removed |
| <180ms / 0.00% egress / 100% blocked egress | search | 0 artifacts | absolute figures only in Haomtgv component. **RESOLVED:** hedged to design language / (target) |
| Governance-compliant badges (Basel IV / King IV / SADC) | search | 0 artifacts | unqualified certification language. **RESOLVED:** now "Designed to align with…" |
| World's smallest AI-native bar | search | 0 artifacts | unsupported superlative. **RESOLVED:** removed across EvidencePage/siteContent/useCaseCatalogData |

## 12. Contradiction / Consistency Notes

- `siteContent.ts:38` "140+ AI agents" vs canonical 90 everywhere else. **RESOLVED:** site now uses 90.
- `siteContent.ts:290` pricing "validated against real prospects" (past) vs `USE-CASE-CATALOG.md:76` "is to be validated with prospects before publishing" (future). — see ticket (b / CONTRADICTION row §5); aligned 2026-09-16 to future-tense; reverified 2026-09-23 (now (b) — RESOLVED).
- OfferingDetailCard.tsx:182-190 "delivered to … commercial banking, national revenue authorities, transport corridors" vs EvidencePage.tsx:380 "Nothing has been delivered to paying clients yet". **RESOLVED:** benchmark box now "Verified In-House Reference… not client deployments."
- USE-CASE-CATALOG.md:506 "All claims trace to real repository files" is itself violated by Pharos download counts, 14.2s/25k, and benchmark telemetry. **RESOLVED:** all three clusters removed/hedged.
- `siteContent.ts` claim:034 National AI Strategy consultation submission "published" vs artifact `national-ai-strategy-comments.md` Status DRAFT. **RESOLVED 2026-09-23:** re-badged to "prepared / drafted for submission" at siteContent.ts:583/626/852/867, useCaseCatalogData.ts:381, EvidencePage.tsx:162. Group 3 partners/pilots rows 025/029/030/040/042 verified already hedged (no copy change).

## 13. Tally

Total: 67 classified claims — (a) 18, qualified (b) 26, (b) — RESOLVED 23, (b / CONTRADICTION) 0. This reconciled count (67 vs the previously declared 65) is canonical per `research/site-claims-index.yaml` and `research/site-claims-audit.md`. As of 2026-09-16: all 18 legacy (c) rows remediated to (b) — hedged or labeled (verified `npm run build` + `npm run lint` green). Claim:024 reclassified to (b) — RESOLVED on 2026-09-23 (future-tense verified in src; see §12). Claim:034 reclassified to (b) — RESOLVED on 2026-09-23 (copy re-badged "published" → "prepared / drafted for submission"; see §12).
