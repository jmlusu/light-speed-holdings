# LightSpeed Site Claims Audit

Date: 2026-09-23
Source ledger: `research/site-claims-ledger.md`
Claim index: `research/site-claims-index.yaml` (canonical positional mapping `claim:001`..`claim:067`)

## 1. Purpose

Verify the classification status of every site claim, reconcile the ledger Tally against
the actual row count, and flag claims that still lack provenance (external artifact or
repo artifact). Outputs feed the claim-`evidence_references` wiring in the Content
Architecture Council (LCA) phase.

## 2. Headline Findings

1. **Count drift**: ledger Tally (`## 13. Tally`, L154) declares 65 claims; the actual
   classified row count is **67** (+2). **RESOLVED 2026-09-23**: Tally rewritten to book
   67 = (a) 18 / (b) 26 / (b) — RESOLVED 23 / (b / CONTRADICTION) 0; index `tally_drift` closed.
2. **RESOLVED overcount**: Tally states "all 18 (c) rows remediated to (b)". In fact
   **23 rows** carry `(b) — RESOLVED` (5 more than the declared remediation set; the extra
   ones are governance/badge remediations and the claim:034 re-badge — see §6). Tally now books all 23.
3. **Contradiction resolved**: `claim:024` (Sol. Digital Transformation, L59) — the
   site copy vs `USE-CASE-CATALOG.md:76` disagreement on whether pricing has already been
   validated against real prospects. **RESOLVED 2026-09-23**: past-tense phrase removed
   from `src/` (verified by grep); both sources now read "to be validated with prospects"
   (future tense). No code change required.
4. **26 plain `(b)` rows remain** unremediated. Most are offers/pricing/targets
   (acceptable while honesty-badged); the former Group 3 self-reported
   partnerships/pilots/submissions rows were closed 2026-09-23 (claim:034 re-badged, the
   other five verified hedged); the remaining are self-reported policy/process/design claims.
5. **No `(c)` rows remain** — every previously-flagged `(c)` row was remediated or
   reclassified into the current vocabulary.

## 3. Count Reconciliation

Tally (ledger L154): `Total: 65 classified claims — (a) 18, (b) 29, (c) 18. As of
2026-09-16: all 18 (c) rows remediated to (b) — hedged or labeled.`

Actual (index): 67 = (a) 18 + (b) 26 + (b) — RESOLVED 23 + (b / CONTRADICTION) 0
(claim:024 resolved 2026-09-23; claim:034 re-badged and reclassified same date).

The current ledger vocabulary splits the old "(b) qualified / (c) unqualified" into
plain `(b)`, `(b) — RESOLVED`, and `(b / CONTRADICTION)`, so per-bucket deltas are not
1:1. Headline deltas:

| Metric | Tally (L154) | Actual (index) | Δ |
|--------|--------------|----------------|---|
| Total rows | 65 | 67 | **+2** |
| (a) fully evidenced | 18 | 18 | 0 |
| Non-(a) rows | 47 | 49 | **+2** |
| Remediated (declared / actual) | 18 | 22 | **+4** |
| Contradiction | — (not tracked) | 0 (resolved) | n/a |

Cause of drift: rows added/classified since the Tally was written (2026-09-16). The
Tally is stale and must be rewritten.

## 4. Class Distribution (67 rows)

| Class | Count | Interpretation |
|-------|-------|----------------|
| (a) fully evidenced | 18 | repo/measured provenance (metrics bundles 144 / 2,373 / 20 / 5-TIER, 7-tool vocabulary, RBAC, honesty-badged de-risking rows 031/032/039/050/052). |
| (b) qualified (plain) | 26 | labeled, hedged, or internally consistent; several self-reported without artifact. |
| (b) — RESOLVED | 23 | previously flagged; copy remediated (verified `npm run build` + `npm run lint` green). |
| (b / CONTRADICTION) | 0 | none — claim:024 resolved 2026-09-23. |

## 5. Resolved Contradiction — claim:024 (CONTRADICTION → RESOLVED)

- **Claim**: Digital Transformation — "Fieldable in 2026 — pricing validated against real
  prospects before publishing".
- **Sources**: `src/data/siteContent.ts` (past-tense) vs
  `USE-CASE-CATALOG.md:76` ("is to be validated with prospects before publishing" —
  future tense, pending).
- **Verdict**: **RESOLVED 2026-09-23.** Grep over `src/` confirms the past-tense
  "validated against real prospects" phrase no longer exists anywhere. The surviving copy
  is future-tense and consistent: `useCaseCatalogData.ts:107` "Pricing is to be validated
  with prospects", `USE-CASE-CATALOG.md:76` matching, and the "Fieldable in 2026 — ready
  for client engagement" honesty badge (`siteContent.ts:1141`). The badge is present and
  the timing contradiction is gone; no code change was required. Reclassified to
  `(b) — RESOLVED` in the index on the same date.

## 6. RESOLVED Status (23) vs Tally's "18 remediated"

Rows carrying `(b) — RESOLVED` (23): 002, 003, 009, 010, 011, 024, 028, 034, 036, 043, 045,
046, 047, 048, 054, 055, 056, 058, 059, 062, 063, 064, 065.

The +5 beyond the declared 18 include governance/badge remediations (e.g., 002 "every
decision auditable", 003 "140+ AI agents", 028/043 SADC "region's first…" superlative,
055 Basel IV/King IV/SADC badge, 054 "Verified Institutional Benchmark" telemetry, 062
Haomtgv "100%" rings) and the claim:034 copy re-badge ("published" → "prepared / drafted
for submission", 2026-09-23). These rows were remediated outside the original (c)→(b)
sweep, so the Tally's "18" is an underestimate. All 23 carry remediation notes in the
ledger.

## 7. Remaining Unqualified Claims — 27 Plain (b), Grouped

### Group 1 — Offers, pricing & engagement-model copy (7)
Low risk; expected commercial copy. Keep honesty-badged; flag only if copy is ever
presented as delivered results.
- claim:012 (90-day pilot → full scale)
- claim:013 (licensing MWK 3,500,000)
- claim:027 (Strategy & Advisory 90-day pilot window)
- claim:049 (Offer A1-A4 pricing)
- claim:053 (MVD MWK 150,000)
- claim:061 (hosting MWK 100,000/mo)
- claim:066 (engagement scopes + "Within 30 days")

### Group 2 — Forward targets / hedged commitments (5)
Must never read as delivered. Current hedges ("We target", "fieldable 2026") are correct;
keep them.
- claim:004 (10-day turnaround / ≥4.5/5 satisfaction — labeled commitment, no published measurement)
- claim:005 (20-25 paid + 8 lighthouse clients in first 12 months — forward target)
- claim:006 ("We target 99.99% uptime")
- claim:033 ("fieldable 2026")
- claim:051 (Offer E1 fieldable-license status; engine itself is (a))

### Group 3 — Self-reported partnerships, pilots & submissions — CLOSED 2026-09-23
**Action was**: obtain an artifact (letter of engagement, press, report) or downgrade copy
to "in discussion" / "self-reported". **Outcome**: claim:034 (the one genuine
over-claim — copy said "published" while the artifact `national-ai-strategy-comments.md`
is `Status: DRAFT`) was re-badged to "prepared / drafted for submission" in 6 locations
and reclassified `(b) — RESOLVED`. The other five were verified already hedged in live
copy — no edits needed, rows annotated `(hedge verified 2026-09-23)`:
- claim:025 (Data & Intelligence "in pilot with UNDP Malawi stakeholders")
- claim:029 (Financial services "actively sought by COMESA/IDEA") — hedged `useCaseCatalogData.ts:500`
- claim:030 (Public Sector "in pilot with UNDP Malawi stakeholders")
- claim:034 (Government — National AI Strategy consultation submission) — RE-BADGED, `(b) — RESOLVED`
- claim:040 (PC-05 Ministry of Agriculture "in pilot development") — hedged `useCaseCatalogData.ts:321/323`, `EvidencePage.tsx:128-131`
- claim:042 (POL-03 MUBAS / UNIMA partnership) — hedged `EvidencePage.tsx:153-155`, `useCaseCatalogData.ts:531-534`

### Group 4 — Policy / process / design claims (9)
Self-reported; acceptable as qualified when the referenced policy/process exists in-repo.
Consider adding repo links to the claim notes.
- claim:015 (four-gate CI — gates exist)
- claim:017 (SHA-256 chained append-only audit trails — design, not published)
- claim:019 (Data Protection by Default, Malawi DPA)
- claim:020 (Four-Gate Onboarding G1-G4; provider-agnostic/Ollama)
- claim:022 (Zero-Cloud Boundary deployment option)
- claim:026 (Automation gated on G1-G4 security review)
- claim:044 (HONESTY_POLICY benchmarks dated/regenerated)
- claim:060 ("All hosted in-region, compliant with Malawi DPA")
- claim:067 ("Strict non-disclosure agreement standard")

## 8. Stale References — FIXED 2026-09-23

1. **Ledger Tally** (L154): rewritten to `67 = (a) 18 / (b) 26 / (b) — RESOLVED 23 /
   (b / CONTRADICTION) 0` (claim:024 and claim:034 reclassified 2026-09-23).
2. **`docs/content-architecture/validation-rules.yaml:84`**: updated to the corrected
   count and buckets (67 claims; 23 RESOLVED).

## 9. Artifacts

- `research/site-claims-index.yaml` — canonical positional mapping (`claim:001`..`claim:067`) with class, section, line, and claim text. **Supersedes the Tally.**
- `research/site-claims-ledger.md` — source ledger (Tally refreshed 2026-09-23).

## 10. Recommended Next Steps

1. ~~Reconcile `claim:024` in siteContent.ts vs USE-CASE-CATALOG.md~~ — **DONE 2026-09-23**: future-tense verified in src; row reclassified `(b) — RESOLVED`; no code change required.
2. ~~Rewrite ledger Tally (L154) + fix `validation-rules.yaml:84`~~ — **DONE 2026-09-23**: Tally books 67 = (a) 18 / (b) 26 / (b) — RESOLVED 23 / (b / CONTRADICTION) 0; validation rule now cites 23 RESOLVED.
3. ~~Chase artifacts for Group 3 (6 rows) or re-badge copy as "in discussion"~~ — **DONE 2026-09-23**: re-badged claim:034 "published" → "prepared / drafted for submission" in 6 locations (siteContent.ts:583/626/852/867, useCaseCatalogData.ts:381, EvidencePage.tsx:162); claim:025/029/030/040/042 verified already hedged in live copy (no edit needed). All six rows closed: claim:034 → `(b) — RESOLVED`, the rest annotated `(hedge verified 2026-09-23)`.
4. ~~Wire `evidence_references` into entity definitions~~ — **DONE 2026-09-23** (16 files, 43 refs, 21 distinct claims; post-wiring validation passed).
5. ~~Re-run `npm run build` + `npm run lint` after any copy change~~ — **DONE 2026-09-23**: `tsc --noEmit` clean, `vite build` green (28.7s, pre-existing chunk-size warning only), `npm run lint` clean after the claim:034 re-badge and claim:042/040/029/025/030 annotation pass.