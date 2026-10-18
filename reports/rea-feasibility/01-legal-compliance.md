# Legal & Compliance Feasibility Assessment — Reverse Engineer Anything (REA)

**Prepared by:** Office of the Chief Legal Officer, LightSpeed Holdings
**Date:** 2026-10-17
**Series:** `reports/rea-feasibility/` — Paper 01 of the Phase 1 feasibility set
**Baseline:** `00-rea-capabilities.md` (shared-facts brief, 2026-10-17). REA's technical capabilities are taken as given from that brief and are **not** re-researched here.

---

## Desk-Research Disclaimer

This is an **internal desk-research risk memo**, not formal legal advice. It flags legal risk for referral to qualified local counsel in each relevant jurisdiction. It does not create or waive privilege, does not constitute an opinion of counsel, and must not be given to clients, partners, or regulators as advice. Every assertion below is drawn from publicly available sources cited by URL; items that could not be independently verified during this research pass are marked **UNVERIFIED**. Compliance with any framework described here is determined by independent evidence and validation — not by the existence of this memo.

---

## Corrections to the shared brief (`00-rea-capabilities.md`)

Three corrections to the baseline brief must be carried into all downstream papers:

1. **UK anti-circumvention provisions are CDPA Part VII ss. 296ZA and 296ZB**, not "s. 96–96ZA": https://www.legislation.gov.uk/ukpga/1988/48/part/VII. The shared brief states that s. 296ZA excludes computer programs from the definition of "copyright work" for circumvention purposes; that text was not independently re-read in this pass, so the exclusion is attributed to the shared brief and marked **UNVERIFIED** pending confirmation against the enacted text.
2. **DSM Directive Art. 3 is the text-and-data-mining exception for scientific research, not an interoperability exception**: https://www.legislation.gov.uk/eudr/2019/790/article/3. The mandatory reverse-engineering-for-interoperability exception in EU/EEA law is **Software Directive Art. 6** only.
3. **Malawi's Copyright Act 2016, s. 85(1)(c) contains an express interoperability exception for computer programmes** — a point in REA's favor that the brief did not foreground (see §1 and §5).

Citation changes: the Communications Act is **Act No. 34 of 2016** (the brief's "Cap 68:01" is not used); Directive (EU) 2016/943 is OJ L157, 15.6.2016, p. 1.

---

## 1. Anti-circumvention risk (technological protection measures)

### 1.1 United States — DMCA § 1201

- **17 U.S.C. § 1201(a)(1)(A)** prohibits circumventing a technological measure that effectively controls access to a work; **§ 1201(b)** reaches trafficking in tools, devices, and services that circumvent measures controlling *use* of a work: https://www.govinfo.gov/content/pkg/USCODE-2021-title17/html/USCODE-2021-title17-chap12-sec1201.htm
- **§ 1201(f)** provides a narrow interoperability exception (lawfully obtained copy, no other infringement, component primarily designed for interoperability, not marketed for non-interoperability use).
- The triennial rulemaking (9th cycle, effective 2024) grants **temporary, conditional exemptions**, not a blanket authorization for security testing or reverse engineering: https://www.copyright.gov/1201/2024/index.html
- **Risk:** REA is itself a tool. Used against access controls (licensing keys, paywalls, authenticated gates) on US-copyright works, REA and its operator face § 1201(a)/(b) exposure independent of copyright infringement. § 1201(f) covers only the narrow interoperability pathway.

### 1.2 EU / EEA — InfoSoc Art. 6 + Software Directive Arts. 6, 8

- **InfoSoc Directive Art. 6** mandates protection for technological measures and prohibits circumvention, tools, and trafficking, subject to a three-step limitation test; contractual arrangements contrary to Art. 6 are rendered ineffective within Member State law: https://www.legislation.gov.uk/eudr/2001/29/article/6 (paraphrase; exact sub-paragraph wording not quoted).
- **Software Directive Art. 6** (https://www.legislation.gov.uk/eudr/2009/24/article/6): reverse engineering of a lawfully obtained program is permitted **only** where the acts are necessary to achieve interoperability of an independently created program; information obtained must not be used for purposes beyond interoperability, must not be communicated to others except for interoperability, must not be used to develop a substantially similar program, and must not impede normal operation.
- **Software Directive Art. 8(1), verbatim:** "Any contractual provisions contrary to Article 6 or to the exceptions provided for in Article 5(2) and (3) shall be null and void." — https://www.legislation.gov.uk/eudr/2009/24/article/8
- **Risk:** EU Art. 6 is *purpose-bound* (interoperability only) and *information-use-bound*. Malawi's s. 85(1)(c) is broader on its face — an EU-target engagement cannot rely on it.

### 1.3 United Kingdom — CDPA Part VII

- **ss. 296ZA (circumvention) and 296ZB (circumvention devices/services)**: https://www.legislation.gov.uk/ukpga/1988/48/part/VII
- The brief's assertion that s. 296ZA excludes computer programs from the protected "copyright work" class would materially narrow UK exposure for software TPMs — **UNVERIFIED**, confirm against enacted text before relying on it.

### 1.4 Berne / WCT framework

- **Berne Art. 9(2)**: limitations confined to special cases, no unprejudiced normal exploitation, no unreasonable prejudice to the right-holder: https://www.wipo.int/edocs/pubdocs/en/copyright/891/wipo_pub_891.pdf
- **WCT Art. 11** (obligation to provide legal remedies against circumvention) and **Art. 10** (three-step test): https://www.wipo.int/wipolex/en/text/295166
- **Implication:** any national interoperability exception must be read narrowly under the three-step test; broad "reverse engineer anything" conduct will not fit inside special-case limits in most signatory states.

### 1.5 Malawi — Copyright Act 2016 (Act No. 26 of 2016)

- In force 13 March 2017 (except Part III); policy text via WIPO Lex 17267 (https://www.wipo.int/wipolex/en/legislation/details/17267), https://malawilii.org, and Part X pp. 59–60 at https://ictpolicyafrica.org.
- **s. 85(1)(c): express interoperability exception for computer programmes** — favorable to REA, subject to conditions.
- **s. 85(2)** cross-refers to **ss. 94–97** (offence provisions) — breaching the conditions of the exception may be an offence, not merely a civil wrong. The exact conditions in **s. 86(3) and s. 86(6)** and the **s. 87** general provision were not fully analyzed in this pass (**UNVERIFIED** in detail; see §5 and Must-Refer list).

**§1 bottom line:** TPM circumvention outside the interoperability carve-outs is the single largest legal exposure in this project, and the carve-outs differ materially across US/EU/UK/Malawi.

---

## 2. EULA / Terms-of-Service reverse-engineering clauses

| Jurisdiction | Enforceability posture | Authority |
|---|---|---|
| US | Contract claim survives copyright preemption; § 117 does not override an express license term | *Bowers v. Baystate Technologies*, 320 F.3d 1317 (Fed. Cir. 2003) — https://law.justia.com/cases/federal/appellate-courts/F3/320/1317/615628 |
| US | RE for interoperability can be fair use / DMCA-safe in the copyright dimension — but that does **not** defeat a contract claim | *Sega v. Accolade*, 977 F.2d 1510 (9th Cir. 1992) — https://www.copyright.gov/fair-use/summaries/segaenters-accolade-9thcir1992.pdf |
| EU/EEA | Contract clauses contradicting Software Directive Art. 6 are **null and void** | Software Directive Art. 8(1) (URL above) |
| UK | Post-retention status of Art. 8(1)-equivalent terms **UNVERIFIED** — confirm via UK counsel | — |
| Malawi | No verified statutory override found; contract law governs; interaction between a contractual RE ban and s. 85(1)(c) is **UNVERIFIED** | — |

**Analysis:** Most commercial targets' EULAs prohibit reverse engineering, decompilation, and circumvention. In the US, *Bowers* is decisive: even where copyright law would permit the acts (interoperability, fair use, § 117), a click-through license can convert them into breach. Practically, REA engagements against EULA-protected targets create contract exposure on top of any statutory exposure. Mitigation: contract clauses 1–2 below (authorized-target attestation and scope limits); REA targets must be **lawfully obtained** in every case.

**Risk:** High — contract claims are the most reliably pleaded cause of action against an REA practice.

---

## 3. Trade secrets, clean-room procedure, and client-deliverable disclosure

### 3.1 Statutory position

- **US — DTSA, 18 U.S.C. § 1839**: https://www.govinfo.gov/content/pkg/USCODE-2021-title18/html/USCODE-2021-title18-partI-chap90-sec1839.htm
  - **§ 1839(6)(B): "improper means" does not include reverse engineering, independent derivation, or other lawful means.** Reverse engineering of a lawfully obtained product is expressly *not* misappropriation.
  - Residual risk: acquisition by breach of an access duty (password circumvention, stolen credentials) *is* improper means regardless of downstream RE.
- **EU — Directive (EU) 2016/943** (OJ L157, 15.6.2016, p. 1), Art. 3 (commonly cited as Art. 3(1)(b)): lawful acquisition includes "observation, study, disassembly or testing of a product" made public or lawfully in the acquirer's possession, free from any legally valid duty limiting acquisition. EUR-Lex blocked the fetcher; text verified via UK mirror: https://www.legislation.gov.uk/eudr/2016/943/body/data.pdf. Implemented in the UK by the **Trade Secrets (Enforcement, etc.) Regulations 2018, SI 2018/597** (in force 9 June 2018): https://www.legislation.gov.uk/uksi/2018/597 (individual regulation-level wording **UNVERIFIED** — do not quote regulations without checking).
- **Malawi: no dedicated trade-secret statute was found.** The Patents Act Cap 49:02 (https://www.wipo.int/wipolex/en/legislation/details/9337) does not provide one. WIPO Lex tags a "Competition and Fair Trading Act" as Undisclosed Information (WIPO Lex 9199), but the country link was not confirmed — **UNVERIFIED**. Whether Malawi recognizes a common-law or competition-law trade-secret regime, and how it treats reverse engineering, **must be determined by local counsel**.

### 3.2 Clean-room procedure (required if REA output is delivered to clients)

The dominant *operational* risk is not REA on a public product — it is **commingling**: outputs for Client A that contain or derive from a third party's (or Client B's) confidential/proprietary information, delivered to a client who then discloses or deploys it. Required controls:

1. **Target authorization register** — every REA target logged with the client's attestation (clause 1).
2. **Separation of duties** — analysts on Client A targets never concurrently handle Client B targets in the same engagement workstream.
3. **Output scrubbing** — deliverables checked for verbatim proprietary strings, code fragments, credential material, or non-public configuration data before release.
4. **Source-of-truth logging** — every claim in a deliverable traceable to (a) the client's own materials, (b) lawfully observed behavior, or (c) public documentation.
5. **No cross-deliverable reuse** of extracted internals between clients without written authorization.

**Risk:** High operationally — trade-secret and breach-of-confidence claims are fact-intensive, jurisdiction-dependent, and (in Malawi) under-specified in statute.

---

## 4. Copyright in outputs / derivative-work risk

- **17 U.S.C. § 102(a)–(b)**: copyright protects original expression; **ideas, procedures, processes, methods of operation, and systems are not protected** — https://www.govinfo.gov/content/pkg/USCODE-2021-title17/html/USCODE-2021-title17-chap14-sec102.htm. Functional descriptions of observed behavior are on safer ground than reproduced code.
- **Derivative works:** reproducing decompiled source, structure, or protectable expression in a client deliverable implicates § 106(2) unless a defense applies.
- ***Google LLC v. Oracle America, Inc.*, No. 18-956, 593 U.S. 1 (2021)** (decided April 5, 2021): https://www.supremecourt.gov/opinions/20pdf/18-956_new_3fb4.pdf — declaring-code copying held fair use on those facts; syllabus: "anyone is free under the Copyright Act to write his or her own code to carry out exactly the same tasks." **Fair use is fact-specific; this is not a blanket safe harbor for REA outputs.**
- ***Sega*:** intermediate copying for interoperability fair use (US) — supports REA's core activity, not every downstream disclosure.
- **AI authorship — *Thaler v. Perlmutter* (D.C. Cir., March 18, 2025)**: https://media.cadc.uscourts.gov/opinions/docs/2025/03/23-5233.pdf — human-authorship requirement for US copyright registration. **Consequences:** (a) LightSpeed's AI-assisted deliverables may be unregistrable/unprotectable in the US; (b) the client's onward-use rights must be allocated by contract, not assumed. Cert petition No. 25-449 disposition **UNVERIFIED**.
- Malawi's originality/derivative-work rules under the 2016 Act were not separately analyzed in this pass (**UNVERIFIED**).

**Risk:** Medium — defensible when outputs describe rather than reproduce, and when the interoperability/fair-use posture is documented per engagement.

---

## 5. Malawi / SADC law

| Instrument | Status | Bearing on REA |
|---|---|---|
| **Copyright Act 2016 (Act No. 26 of 2016)** | In force 13 Mar 2017 (except Part III) | **s. 85(1)(c) interoperability exception (favorable)**; s. 85(2) → ss. 94–97 offences; conditions in s. 86 (incl. 86(3), 86(6)) **not fully analyzed (UNVERIFIED)**; s. 87 not analyzed |
| **Trade-secret regime** | **No dedicated statute found** | Gap — refer to counsel (see §3.1) |
| **WTO / TRIPS** | Malawi: WTO member since **31 May 1995**, GATT since 1964 — https://www.wto.org/english/thewto_e/countries_e/malawi_e.htm ; TRIPS notifications: https://notifications.wto.org/en/status-by-member/malawi | TRIPS obligations apply (incl. Art. 39 undisclosed information, Arts. 8–9 on enforcement/standards) |
| **Berne / WCT membership** | Not confirmed in this pass — **UNVERIFIED** | Affects how far WCT Art. 11-style obligations bind directly vs. via TRIPS |
| **Data Protection Act 2024 (Act No. 3 of 2024)** | Designated authority: **MACRA** — https://www.mca.ac.mw/mca-siteup/uploads/Data%20Protection%20Act%202024.pdf | Controller registration and cross-border transfer rules apply to any REA engagement processing personal data (Malawi, regional, or client-personnel data). Final Act section numbers for transfers **UNVERIFIED** (the 2021 *draft* Bill s. 35 is a draft, not law) |
| **Malabo Convention** | Not ratified (per https://dataprotection.africa/malawi) | No Malawi obligation from Malabo itself |
| **Electronic Transactions and Cyber Security Act No. 33 of 2016 (MCERT)** | In force | Authorization/access requirements relevant to REA's operation on Malawi-connected systems — **UNVERIFIED in detail; refer** |
| **Patents Act Cap 49:02** | In force — WIPO Lex 9337 | No trade-secret provision found |
| **SADC Model Law on Data Protection (revision 2021)**; **Model Law on Cybercrime (2012)** | Soft law, non-binding | Direction-of-travel only; not directly enforceable |
| **SADC–Malawi instrument signed 31 May 2017** (https://sadc.int/document/malawi) | Identity/nature of document **UNVERIFIED** | Do not cite substantively until identified |

**Constitutional note:** the shared brief's assertion of a constitutional privacy right (s. 21) rests on a secondary source — **UNVERIFIED** against the Constitution text.

**§5 bottom line:** Malawi is partly favorable (s. 85(1)(c)) but has real gaps (trade secrets, offence linkage, data protection specifics). All four are on the Must-Refer list.

---

## 6. Client-contract clauses (5 recommended)

Each clause below is a drafting starting point for review by Malawi-qualified counsel; wording is illustrative, not final.

1. **Authorized-target attestation.** Client represents and warrants that it is legally entitled to require analysis of each Named Target (listed in a schedule), that it has all licenses, permissions, and end-user consents necessary for the engagement, and that no Named Target will require circumvention of a technological protection measure except where a statutory interoperability exception is expressly invoked and documented in the engagement record. Lightspeed may rely on this attestation without independent verification.

2. **Scope and exclusion limits.** Services are limited to the Named Targets and stated methods (black-box observation, client-provided artifacts, lawfully obtained copies). **Excluded without exception:** cardholder data environments (see §7.1), telecommunications network elements and spectrum-licensed equipment (see §7.2), end-to-end encrypted messaging internals, authentication/authorization components of third-party production systems, and any target for which the client cannot evidence lawful access. No circumvention of access controls beyond documented statutory carve-outs.

3. **Client indemnity with cap carve-out.** Client shall defend and indemnify Lightspeed against claims arising from breach of the clause 1 attestation or from the client's unauthorized disclosure of deliverables. This obligation is **excluded from (carved out of) the general liability cap** in the master agreement, as are Lightspeed's indemnities for its own gross negligence or wilful misconduct — subject to counsel's confirmation that such carve-outs are enforceable under Malawi contract law (**UNVERIFIED — refer**).

4. **Output warranty disclaimer + IP allocation (AI-authorship caveat).** Deliverables are provided **as-is, for the client's internal decision-use**; Lightspeed **does not warrant** that outputs are free of third-party IP claims where outputs reflect or reproduce elements of a Named Target. Deliverables are deliverables of *observations and functional descriptions*; where any protectable expression arises, ownership/assignment terms apply subject to the **human-authorship limitation** (see §4, *Thaler*) — the parties acknowledge that certain AI-assisted output may be unprotectable by copyright, and the client assumes the risk of onward use.

5. **Governing law / dispute resolution with extraterritorial acknowledgment.** Governing law and seat: **Malawi**, arbitration seated in Malawi (institution to be designated by counsel), language of proceedings as agreed. **Acknowledgment:** this choice of law does not displace claims under the law of the US, EU/EEA, or UK where the Named Target or right-holder is domiciled there; the client accepts that those regimes (DMCA § 1201, InfoSoc Art. 6, CDPA Part VII) may apply to conduct on their territory notwithstanding this clause.

---

## 7. Sector overlays

### 7.1 Financial services
- **GLBA Safeguards Rule, 16 CFR Part 314** (https://www.govinfo.gov/content/pkg/CFR-2022-title16-vol1/pdf/CFR-2022-title16-vol1-part314.pdf; authority 15 U.S.C. 6801(b), 6805(b)(2); implements GLBA §§ 501, 505(b)(2)): §§ 314.1–314.6 — purpose/scope, definitions, standards, elements (written information security program), effective date, exceptions (incl. **§ 314.6** for institutions with <5,000 consumers). Includes a breach-notification element (**§ 314.4(j)**, effective 13 May 2024) and service-provider oversight obligations (subsection lettering **UNVERIFIED**). Applies when Lightspeed is a service provider to a covered US financial institution.
- **PCI DSS**: **v4.0.1 is the sole active version** (v4.0 retired 31 Dec 2024; future-dated requirements mandatory 31 Mar 2025) — https://blog.pcisecuritystandards.org/. Any engagement touching cardholder data requires a scoping determination (QSA) — **excluded by contract clause 2**.
- **Overlay risk: Medium** (High if scope drifts into cardholder data or customer-information handling).

### 7.2 Telecommunications
- **MACRA** licensing: telecommunication-licensees information at https://macra.mw/telecommunication-licensees ; **Communications Act 2016 (Act No. 34 of 2016), ss. 31–52** and the Communications (Telecommunications and Broadcasting Licensing) Regulations 2016. If LightSpeed *operates* a service (rather than consulting to a licensed operator), an application-services licence (voice/internet forms) is likely required — **confirm with MACRA/local counsel (UNVERIFIED in detail)**. Reverse engineering of network elements may additionally touch equipment authorization/type-approval rules (**UNVERIFIED**).
- Network elements excluded by contract clause 2. **Overlay risk: Medium.**

### 7.3 NGOs / donor-funded projects
- Donor grant agreements routinely prohibit reverse engineering of licensed software, impose data-protection and attribution flow-downs, and restrict sublicensing of findings. Each NGO engagement requires a clause-by-clause check of the prime grant's flow-down provisions; NGO-sector statutory specifics not researched (**UNVERIFIED**). **Overlay risk: Low–Medium**, driven by contract terms rather than statute.

### 7.4 Agriculture / natural resources / climate
- Lowest-risk sector for REA: targets are typically open datasets, sensor pipelines, and public-sector systems with no TPM'd commercial stacks. Residual exposure is **personal data** (farmer/worker data) under the Data Protection Act 2024 and donor data clauses. **Overlay risk: Low.**

---

## Risk-rating table

| # | Risk | Rating | Rationale (one line) |
|---|---|---|---|
| 1 | TPM circumvention outside interoperability carve-outs (DMCA § 1201(a)/(b); InfoSoc Art. 6; CDPA ss. 296ZA/296ZB; Malawi s. 85 conditions) | **High** | Statutory penalties attach to tool use and to the operator, independent of infringement. |
| 2 | EULA/ToS reverse-engineering bans enforced as contract claims | **High** | *Bowers*: copyright-side permission does not defeat a click-through license term. |
| 3 | Malawi gaps: no trade-secret statute found; s. 85(2) offence linkage (ss. 94–97); DPA 2024 registration/cross-border rules | **High** | Uncertain offense exposure and untested local regime for the home jurisdiction. |
| 4 | Cross-client / third-party disclosure of proprietary information in deliverables (clean-room failure) | **High** | Fact-intensive trade-secret and breach-of-confidence claims across multiple jurisdictions. |
| 5 | Client-contract exposure absent attestation, exclusions, indemnity (clause 1–3) | **High** | Unscheduled targets and unlimited liability convert a single bad engagement into corporate risk. |
| 6 | EU/EEA engagements: Software Directive Art. 6 is narrower than Malawi s. 85(1)(c) (purpose- and information-use-bound) | **Medium** | Art. 8(1) voids contrary EULA terms, but conduct beyond interoperability purpose remains unlawful. |
| 7 | Derivative-work / reproduction liability for outputs (17 U.S.C. § 106; § 102(b) as shield) | **Medium** | Defensible when outputs describe function rather than reproduce expression; fact-specific. |
| 8 | Output IP defects: AI-authorship unregistrability (*Thaler*) and unprotectability of deliverables | **Medium** | Client expectation of assignable IP may not hold in the US; allocate by contract. |
| 9 | Financial-sector overlays: GLBA 16 CFR Part 314 + PCI DSS v4.0.1 scope | **Medium** | Manageable via cardholder-data exclusion and service-provider obligations; High if scope drifts. |
| 10 | Telecommunications licensing (MACRA) if services touch licensed networks | **Medium** | Likely licence triggers for operating services; contract exclusion mitigates. |
| 11 | NGO/donor flow-down breach of RE prohibitions | **Low–Medium** | Contract-driven, engagement-by-engagement. |
| 12 | Agriculture / natural resources / climate engagements | **Low** | No typical TPM'd commercial targets; residual personal-data exposure only. |

---

## Must refer to qualified local counsel

1. **Malawi trade-secret regime** — whether any statute, common law, or the (unconfirmed) Competition and Fair Trading Act governs, and how reverse engineering is treated. *(UNVERIFIED)*
2. **Copyright Act 2016 s. 85(1)(c) scope and conditions** — full read of s. 86(3), s. 86(6), s. 87, and the offence linkage in s. 85(2) → ss. 94–97; whether breach of an exception condition is criminal. *(UNVERIFIED)*
3. **Electronic Transactions and Cyber Security Act No. 33 of 2016 (MCERT)** — authorization/access requirements applicable to REA operation. *(UNVERIFIED in detail)*
4. **Data Protection Act 2024** — controller registration obligations and cross-border transfer rules as enacted (final section numbers; the 2021 draft Bill s. 35 is not law). *(UNVERIFIED)*
5. **Malawi's Berne Convention / WCT membership status** — TRIPS applies as WTO member (31 May 1995); direct Berne/WCT membership not confirmed. *(UNVERIFIED)*
6. **Enforceability of the indemnity and liability-cap carve-outs** (contract clause 3) under Malawi contract law. *(UNVERIFIED)*
7. **MACRA licensing** — whether contemplated engagements require an application-services licence or equipment-authorization clearances. *(UNVERIFIED in detail)*
8. **PCI DSS scoping / QSA determination** for any engagement near cardholder data; confirm v4.0.1 control applicability. *(scope UNVERIFIED)*
9. **EU/EEA and UK engagements** — EU counsel sign-off required before any EU-target REA work (Art. 6 purpose/information limits are narrower than Malawi s. 85(1)(c)); UK counsel to confirm CDPA ss. 296ZA/296ZB text (incl. the computer-program exclusion attributed to the shared brief) and SI 2018/597 regulation-level wording. *(UNVERIFIED)*
10. **US counsel** on § 1201 posture for US-vendor targets and on *Thaler* cert disposition (No. 25-449) before relying on output IP assignments in the US market. *(UNVERIFIED)*
11. **GLBA applicability determination** — whether specific financial-sector clients bring LightSpeed within 16 CFR Part 314 as a service provider, and which subsections apply.

---

*End of memo. Prepared 2026-10-17. All URLs accessed during desk research on 2026-10-17. Items marked UNVERIFIED must not be represented to clients or counterparties as settled law.*
