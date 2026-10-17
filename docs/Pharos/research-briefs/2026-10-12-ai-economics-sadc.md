# Research Brief — The Dual-Economy Economics of Agentic AI in Malawi / SADC

**Date:** 2026-10-12 · **Author:** market-analyst · **Status:** First-party provenance only
**Consumer:** CEO voice article (author may use claims below; may not add numbers not present here)

**Grounding rule:** every claim carries `path:line` provenance or is explicitly hedged. Gaps in §5 are NOT assertable — the author must not invent around them.

---

## 1. Dual-economy pricing rationale

LightSpeed prices on two rails because its market is two markets. The catalog states it directly: pricing is "anchored in dual currency (MWK for local clients, ~USD for international)" (`docs/client-facing/USE-CASE-CATALOG.md:76`). The published MWK ladder (all "~USD" conversions are labeled estimates in the source; all require prospect validation before public use, `USE-CASE-CATALOG.md:97`):

| Line item | MWK | ~USD (estimate) | Source |
|---|---|---|---|
| Licensing | 3,500,000 | ~$2,000 | `docs/marketing/competitive-landscape.md:20` |
| Support retainer | (USD-denominated) | $200/mo | `competitive-landscape.md:20`; `content/drafts/faq.md:171` |
| Minimum viable deployment | 150,000 | ~$85 | `competitive-landscape.md:20`; `USE-CASE-CATALOG.md:91` (A4) |
| Business website (A1) | 800,000 | ~$450 | `USE-CASE-CATALOG.md:88` |
| E-commerce store (A2) | 1,800,000 | ~$1,000 | `USE-CASE-CATALOG.md:89` |
| WhatsApp chatbot (B1) | 1,500,000 | ~$850 + MWK 100,000/mo hosting | `USE-CASE-CATALOG.md:109,116` |
| One-off payment terms | 50% upfront / 50% on delivery | — | `USE-CASE-CATALOG.md:97` |

The rationale, in the company's own words: "dual-economy pricing so institutions pay for what they run, not for idle hyperscaler capacity" (`src/data/insights.ts:69`). Mobile-money rails (Airtel Money, TNM Mpamba) are "built in from day one, not bolted on" (`insights.ts:68`; `USE-CASE-CATALOG.md:82`). International NGO / USD-quoted work is documented in the FAQ and catalog; no public rate card exists (`competitive-landscape.md:20`; FAQ honesty language `content/drafts/faq.md`).

**Safe phrasing:** "offer language, not transacted revenue — pricing is stated in MWK with ~USD estimates and is explicitly pending prospect validation" (`USE-CASE-CATALOG.md:97`).

## 2. Market context table

| Fact | Number | Source | Safe phrasing |
|---|---|---|---|
| Population | ~22.2m; ~62% under 25; median age 19.2; ~18–20% urban | `results/pestel-lightspeed-2026.md:81` | "PESTEL 2026 baseline" — cite as internal scan |
| GDP growth | 1.9% (2025) → 2.3% (2026 projected) | `pestel-...md:45` | "slow growth, projected" |
| Inflation | 28.4% avg 2025 → ~22% avg 2026 projected | `pestel-...md:46` | "easing but high" |
| FX | MWK peg ~1,716–1,751/USD; 44% devaluation Nov 2023 | `pestel-...md:48` | explains USD-denominated risk; do NOT convert MWK prices to USD at invented rates |
| MSME base | ~1.6m MSMEs, 90%+ informal | `pestel-...md:56` | "the addressable market is informal-first" |
| Internet penetration | 27.7% vs SADC 59.8%; 80% usage gap | `pestel-...md:82` | "connectivity is the constraint, not demand" |
| Mobile money | 75% of adults active; MWK 8.6tn volume 2025 | `pestel-...md:85` | "payment rails already exist — agents can ride them" |
| Policy | National AI Strategy + DTS in drafting; UNESCO RAM validated Jul 2026; DPA 2024 in force, not AI-specific; AU Continental AI Strategy Jul 2024 | `docs/Pharos/roadmap.md:9-18` | "category being defined, not settled" |
| SADC framework | SADC "Agentic AI Governance Framework" is LightSpeed's own policy proposal — NOT an adopted standard | `insights.ts:45-46,80` | must be labeled as a proposal; engagement is "advisory and pilot work, not deployed client systems" (`insights.ts:80`) |

## 3. Customer / pipeline reality

**Honest status — the single most important constraint on the article:** "Nothing has been delivered to paying clients yet" (`src/data/insights.ts:80`); "no paying clients delivered yet; proof stack is internal" (`competitive-landscape.md:20`); "all offers are fieldable in 2026, in pilot, or in active development" (`content/drafts/faq.md:153`).

Documented pipeline states (`faq.md:153`; `USE-CASE-CATALOG.md:84,105,214,229,244`):

- **LIVE:** J&S StopOver Bar — "a real, non-tech SME already running agentic decision support" (`case-study-pipeline.md:11`), inventory/procurement/pricing agents. The only LIVE commercial proof point.
- **PROVEN IN-HOUSE:** the 90-agent company itself — 89 AI agents + 1 human CEO across 20 departments, "verified by direct count of the company registry on 23 September 2026" (`pillars/01-built-a-90-agent-company.md:34-37`; `competitive-landscape.md:20`).
- **PILOT:** agricultural coop, health M&E ("no confirmed partnership with any named health organization has been signed", `USE-CASE-CATALOG.md:229`), VSLA/SACCO ("no signed engagement exists", `USE-CASE-CATALOG.md:244`).
- **BLOCKED:** Offer B (WhatsApp automation) "blocked" pending G1–G4 security review (`USE-CASE-CATALOG.md:105,116`).

## 4. Competitive / alternative frame

The competitor's real name is *not another AI vendor* — it is the current manual stack, plus global consultancies priced out of the market.

- **The buyer's actual alternative:** their existing sheets. Sales script: "No rip-and-replace; we sit beside your current M&E sheets for one cycle" (`docs/venture-studio/12-T3-call-scripts.md:15,39,58`). B3 explicitly automates "Kobo/Google-Forms-to-spreadsheet" (`USE-CASE-CATALOG.md:111`).
- **Rip-and-replace avoidance as doctrine:** the system "integrates with the existing stack in a ninety-day pilot instead of ripping it out" (`docs/Pharos/articles/h-a-o-m-t-g-v-seven-layers.md:146-147`); 90-day pilots are a documented offer, classified "(b) offer, not result" (`research/site-claims-ledger.md:37,62`).
- **The four objections risk officers actually raise** — bandwidth/devices, data location, forever-maintenance, prior-AI-failure (`seven-layers.md:133-136`) — with the repo's answer: "they are afraid of ungoverned deployment," not the technology (`seven-layers.md:129-131`).
- **Category gap (internal claim, label as such):** "Nearly every Malawi player above sells custom software... None sells a governed agentic organization. The 'AI company builder' category is empty locally" (`competitive-landscape.md:29`). Named local players (Rexplore, Hyets, KCS, Tensorview, NxtGen) all have "Public pricing: Not publicly disclosed" (`competitive-landscape.md:41,54,63,74`) — do NOT invent their prices. BCG / Deloitte Africa / Accenture sell governance-shaped messaging "at enterprise rates" (`competitive-landscape.md:30`) — no SADC-specific price points exist in-repo.
- **NOT in repo:** no "doctors' queues" / clinic-queue alternative frame exists (grep, 2026-10-12). The author must source it externally or drop it.

## 5. Gap list — do not assert

- Any TAM / SAM / SOM figure for Malawi or SADC agentic AI (none exists in-repo).
- Any "% of African enterprises" adoption / readiness statistic.
- Competitor pricing (undisclosed — see §4) or global-consultancy day rates.
- FX conversions of MWK prices beyond the catalog's own "~USD" estimates and the documented ~$2,000 note.
- Signed-revenue figures, win rates, pipeline values, conversion metrics.
- "Doctors' queues" as a named alternative (see §4).
- AI Bill status: pillar articles say "due December 2026" (`pillars/03-...md:15-16`), but the Oct 7 competitive refresh records it as **stalled** (`harness/changes/archive/2026-10-07-t4-competitive-landscape-oct-refresh-420/summary.md:25`). If the article cites the Bill, cite the stalled status or say "announced Aug 2026, status moving."

## 6. Candidate claim sentences (copy-ready)

1. "We price in MWK for Malawian institutions and USD for international NGOs — dual-economy pricing so institutions pay for what they run, not for idle hyperscaler capacity" (`USE-CASE-CATALOG.md:76`; `insights.ts:69`).
2. "Seventy-five percent of Malawian adults already transact on mobile money — MWK 8.6 trillion in 2025 — so our agents ride rails that already exist, rather than asking anyone to adopt a new payment habit" (`pestel-...md:85`).
3. "Nothing has been delivered to paying clients yet; what exists is the operating evidence — a governed 90-agent company running daily, one LIVE non-tech SME (J&S StopOver Bar), and pilots that are honest about being pilots" (`insights.ts:80`; `faq.md:153`; `case-study-pipeline.md:11`).
4. "When a minister or a risk officer says no to AI, they are rarely rejecting the technology — they are raising four legitimate reservations, and the answer is ninety-day pilots that sit beside the current spreadsheets, not rip-and-replace" (`seven-layers.md:129-131,133-136,146-147`; `12-T3-call-scripts.md:15`).
5. "Malawi's National AI Strategy is still being drafted and the UNESCO readiness assessment was validated in July 2026 — the category is being defined now, which is precisely why the governance architecture has to ship before the throughput" (`roadmap.md:9-18`; `insights.ts:60`).

---

*Provenance verified 2026-10-12 against the paths above. Re-verify PESTEL line numbers and the AI Bill status before publication if more than 30 days have passed.*
