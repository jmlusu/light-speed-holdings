# PROXY Baseline — Calibration Run (NOT authoritative)

**Status:** PROXY — for harness calibration only. **Do NOT quote in public artifacts.**
**Method:** No live access to ChatGPT/Perplexity/Gemini from the AFK build environment;
the 5 probes below were run through the repository's `websearch` tool (live web results,
top ~8–10 hits) on **2026-09-16**. This tests *searchable-index* visibility, not engine
behavior.
**Purpose:** (1) validate the keyword set fires real questions; (2) predict where the
real-engine scores will land; (3) give #315 the list of entities we are currently
losing to. Real numbers come only from the CEO's live run of `harness.ps1` (README §6).

---

## 1. Probe results (5 of 20 keywords — the highest-signal ones for brand/category)

### P1 — "What is Lightspeed Holdings?" (k01)
- **Surfaced entities:** Lightspeed Commerce (Montreal POS company, `lightspeedhq.com`),
  Lightspeed Financial Services LLC. **lightspeedholdings.com did NOT surface.**
- **Reading:** full brand collision — a searcher asking about us gets the Canadian POS
  company. Expect real engines to name Lightspeed Commerce and say **nothing** about us:
  `named=n`, mostly score 1/0. Highest-priority fix for #315: differentiate the brand at
  the searchable layer (exact-match copy, Schema.org/Organization markup, LinkedIn).

### P2 — "Who is Jacob Jack Mlusu?" (k02)
- **Surfaced entities:** correct LinkedIn profile (`linkedin.com/in/jack-mlusu-50027428`,
  Lilongwe, strategy/transformation) — surfaced correctly; plus homonym noise
  (unrelated names, people-search sites).
- **Reading:** the name is indexed. **lightspeedholdings.com did not surface next to it.**
  Expect k02 to be our **best-scoring** keyword — possibly score 2 (named, right LinkedIn)
  but with `cited_correct` depending on whether engines cite his LightSpeed role. This is
  the one keyword with a realistic path to score 3 today.

### P3 — "state of agentic AI in Malawi" (k13 signal)
- **Surfaced entities:** Government/UNESCO readiness work (NCST RAM validation),
  academic papers on AI in Malawi. **No LightSpeed / Pharos Malawi Agentic AI Monitor.**
- **Reading:** the *topic* is live and citable — the Monitor has a real category to own.
  Any score-1 (Generic) here is pure missed-opportunity evidence for #317.

### P4 — "H-A-O-M-T-G-V framework" (k05)
- **Surfaced entities:** only generic agent-governance frameworks from other sites
  (aiagentgovernance.org, etc.). **Nothing OURS.**
- **Reading:** this is the **hallucination-risk** keyword: engines will be tempted to
  invent an attribution for the acronym (or claim it is from an unrelated source).
  Watch for `named=y, cited_correct=n` false attributions → score 2 + HALLUCINATION flag.
  This keyword is the canary for whether the framework is published *searchably*.

### P5 — "company run by 144 AI agents" (k06 signal)
- **Surfaced entities:** the category is real and crowded — Orbyt Labs (12 agents),
  Tesseract Labs (23), KORRO (autonomous), human0, Thicket (13), Dutch Zero-Human
  Company. **No LightSpeed.**
- **Reading:** we are currently **unnamed in our own category**. Engines will cite one of
  these competitors. Strong evidence for the #313/#315 gap: the meta-deployment case
  study is not findable yet.

---

## 2. What the proxy does NOT tell us

- Search-engine top-10 indexing ≠ ChatGPT/Perplexity/Gemini retrieval. Real engines may
  cite pages that do not appear in the search top-10 (and vice versa).
- Consumer UIs have freshness lag and grounding differences; API transcripts are
  calibration only (README §7).
- Proxy = 5 keywords; the live run measures the full 60 (20 × 3).

## 3. Baseline hypothesis to test on the live run

| Expectation | Keywords | Hypothesized outcome |
|---|---|---|
| Near-zero citation | k01, k05, k06, k13 | score 1 (Generic) or 0; Score-2 only if hallucination |
| Partial citation | k02 | named + correct LinkedIn; `cited_correct` risk |
| Competitor domination | k03, k04, k06, k07 | engines cite other agentic companies (Orbyt, Tesseract, KORRO…) |
| Unknown territory | k11, k12, k20 | Generic answers; engines that answer well = score 1 |
| Policy-freshness risk | k14, k15, k16 | Generic policy summaries; our tracking docs not cited |

If the live run lands inside these expectations, the **AI Citation Rate baseline ≈ 2–5%**
(all engines) and the actionable story for #313/#315/#317 is: *"the engines know the
category and the person, but not the company — publish the artifacts, then re-run."*

## 4. File hygiene

- Delete or supersede this file after the first **live** baseline is complete
  (keep a one-line history note in README §8's cycle checklist instead).
- Never cite `proxy-baseline.md` as evidence in customer/partner-facing material.
