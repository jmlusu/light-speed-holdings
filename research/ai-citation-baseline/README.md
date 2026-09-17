# AI Citation / Social Proof Baseline

**Ticket:** #312 — "AI citation baseline audit (20 keywords x 3 engines)"
**Status:** METHODOLOGY LOCKED — awaiting the live run by the Human CEO
**Created:** 2026-09-16
**Owner:** Pharos — Agentic Research Lead (AFK agent build; live run is CEO-executed)
**Feeds:** #313 (intro post), #317 (Malawi Agentic AI Monitor), #315 (positioning pillars), and the "AI Citation Rate" KPI (Gap 5, step 6)

---

## 1. Why this exists

Before the CEO starts quoting *"what AI says about agentic AI companies"*, we need a
repeatable, honest baseline proving — or disproving — that ChatGPT, Perplexity and
Gemini actually **cite Lightspeed's real public artifacts** (lightspeedholdings.com,
the public GitHub repo, Pharos publications, newsletter streams) when asked about the
topics we own.

This baseline is the first citable **social-proof evidence** asset. It is also the
definition of the `AI Citation Rate` KPI:

> **AI Citation Rate** = (runs where the engine **named** LightSpeed or Jack Mlusu and
> the citation was **valid**) ÷ (total runs) per keyword, per engine, per release cycle.

If the rate is low, that is not a failure of the company — it is a **measurement of
public visibility** that tells us where to publish next. If the rate is high, it is the
quote evidence for #313/#315/#317.

---

## 2. Scope and units of measurement

| Item | Value |
|---|---|
| Keywords | **20** curated (see `keywords.md`) — derived from `docs/Pharos/positioning.md`, `research/site-claims-ledger.md`, `AGENTS.md`, `docs/ECL.md` |
| Engines (measured) | **ChatGPT**, **Perplexity**, **Gemini** |
| Total runs per cycle | **60** (20 keywords × 3 engines) |
| Optional calibration engine | **Big Pickle** (via `OPENCODE_API_KEY`) — internal proxy only, NOT counted in the ledger |
| Baseline ledger | `results-ledger.csv` (60 rows per cycle) |
| Transcript store | `transcripts/<YYYY-MM-DD>/<engine>/<NN>-<slug>.txt` (created by `harness.ps1`) |

---

## 3. Methodology

### 3.1 The 20 keywords

`keywords.md` maps every keyword to:
- the **moat territory** it tests (Company Building / Use Cases / Policy / Reservations),
- the **claim** it should surface,
- the **knowledge artifact** that should ground a correct citation (public site, repo docs, GitHub, newsletters, LinkedIn).

Keywords are deliberately phrased as **neutral buyer/journalist/regulator questions**.
Only the two brand keywords (k01, k02) name LightSpeed or Jack Mlusu — everything else
measures **organic** citation: if the engine knows us, it cites us without being told.

> Do not add "…and is it related to LightSpeed Holdings?" to the prompts. That would
> destroy the measurement. The prompts are deterministic and locked in `harness.ps1`.

### 3.2 Fresh chat per run

- **One fresh chat per keyword per engine.** No conversation history, no follow-up
  prompts, no "now search for X" corrections during the measured run.
- This is non-negotiable: the baseline measures **zeroth-turn** retrieval, the same
  surface a prospect or journalist hits on their first question.

### 3.3 Verbatim transcript capture

- Every run saves a **verbatim** transcript to
  `transcripts/<YYYY-MM-DD>/<engine>/<NN>-<slug>.txt` with the exact prompt, the exact
  engine reply, and engine metadata (model, grounding/citations where the API returns
  them).
- Automated runs (Gemini/Perplexity when keyed and `-Auto`) write transcripts
  automatically. Manual runs (ChatGPT always; any engine without a key) require the
  CEO to copy the reply into the transcript file. If the engine refuses or errors,
  record `REFUSED` / `ERROR` in the file — a refusal is data.
- **Never paraphrase a transcript.** The verbatim file is the evidence.

### 3.4 Attribution audit (per transcript)

For each transcript, answer the four ledger questions:

1. **named (y/n)** — Does the reply name "Lightspeed Holdings" or "Jack/Jacob Mlusu"
   (or refer to them unambiguously)? A reply that says "one company reports running
   144 agents" without the name is **not** named.
2. **cited_correct (y/n)** — Does the reply point to the **right** public material:
   `lightspeedholdings.com`, the GitHub repo (`github.com/jmlusu/light-speed-holdings`),
   a real Pharos publication or the correct LinkedIn profile? Citing
   "Lightspeed Commerce" (the Canadian POS company) is **incorrect**.
3. **citation_valid (y/n)** — Are the specific claims it makes about LightSpeed/Mlusu
   **true against `research/site-claims-ledger.md`**? Check the numbers (144 agents,
   20 departments, 5-tier HITL, 2,373 tests), the domain, the role history, the status
   of use cases (pilot vs delivered — nothing has been delivered to paying clients yet).
   Any invented metric, wrong scale, or fabricated artifact = **invalid**.
4. **score** — derived from 1–3 using the rubric in §4.

### 3.5 Hallucination flags

Any claim attributed to LightSpeed that contradicts the claim ledger is a
**hallucination flag** (append `HALLUCINATION:` + what was wrong in `notes`).

- A flagged run is **never** surfaced as social proof.
- Flags are **actionable**: they feed #315's correction/response workstream and tell us
  which public artifact is missing or ambiguous (e.g. "Gemini thinks 144-agent company
  is KORRO" ⇒ we need the meta-deployment case study public and unambiguous).
- After we publish a remediating artifact, **re-run the offending keyword** — dropping
  hallucination count over releases is itself a KPI.

### 3.6 Repeat cadence

Re-run the full 60-run cycle:

- **After every major public release** — site launch/update, new Monitor issue,
  whitepaper or framework publication, newsletter milestone, public case study.
- **At minimum quarterly** (aligned with the Pharos 12-month success metrics).

Each cycle gets a new `date` column value and new transcript directory; the ledger keeps
history so later tickets (#313 series) can compare deltas.

---

## 4. Scoring rubric (4-point)

| Score | Level | Decision rule | Meaning for social proof |
|---|---|---|---|
| **3** | **Named + Correct** | `named=y` AND `cited_correct=y` AND `citation_valid=y` | The engine names us, points to the right artifact, and every claim checks out. **Quotable.** |
| **2** | **Named + Inaccurate** | `named=y` AND (`cited_correct=n` OR `citation_valid=n`) | It names us but gets material wrong (wrong domain, wrong numbers, wrong company of that name). **Do not quote; hallucination flag in notes.** |
| **1** | **Generic** | `named=n` AND reply is substantive/on-topic for the keyword | It answers well but has never heard of us. **Missed-opportunity signal.** |
| **0** | **No evidence** | `named=n` AND reply is off-topic, empty, refused, or an error | Neither us nor even the topic. **Dead query or blocked engine.** |

Scoring is deliberately harsh on hallucinated attribution: **a wrong citation is worse
for the brand than silence**, so Named+Inaccurate (2) is lower than Generic (1).
Silence = opportunity; misattribution = damage.

Computed scores are written into `results-ledger.csv`. The baseline's headline metric
is *percent of 60 runs scoring 3* and *percent of runs naming us* (score ≥ 2).

---

## 5. Roll-up: the ranked "AI social-proof quotes" list

Results feed #313 / #315 / #317 as a **ranked quote list** (keep it in
`research/ai-social-proof-quotes.md` once the live run lands; first run = this baseline).

Ranking rules:

1. **Only score-3 runs are eligible.**
2. **Citation validity first** — cross-checked against the claim ledger, not just
   engine confidence.
3. **Material specificity second** — quotes naming concrete artifacts (domain, metrics,
   framework name, named case study) outrank vague praise.
4. **Multi-engine agreement third** — the same fact cited by ≥2 engines is stronger
   than a single-engine mention.
5. **Recency fourth** — fresher runs win; stale quotes are re-verified before use.

Quote card template (one per borrowable quote):

```text
QUOTE      : <verbatim engine text, truncated only with ellipsis>
ENGINE     : <ChatGPT | Perplexity | Gemini> <model> on <date>
KEYWORD    : <kNN-slug>
CLAIMS MADE: <what it asserts about LightSpeed>
VERIFIED   : <each claim: PASS/FAIL against site-claims-ledger.md>
SOURCE ART : <the artifact the engine cited>
USE FOR    : #313 intro | #317 Monitor | #315 pillar <name>
```

The intro post (#313) may quote **only** quotes that are (a) score-3 and (b) from the
most recent cycle.

---

## 6. Live-run instructions (Human CEO — ~20 minutes)

### Prereqs

- You are at a machine with this repo checked out (`research/ai-citation-baseline/`),
  PowerShell (`pwsh`), and an internet connection.
- `harness.ps1` is the driver. It reads `.env` for keys:
  - `GEMINI_API_KEY` → automated Gemini (`gemini-3.5-flash`) when `-Auto` is passed.
  - `PERPLEXITY_API_KEY` → automated Perplexity (`sonar`) when `-Auto` is passed.
    (Not currently in `.env`; add it to enable automation, otherwise Perplexity is manual.)
  - `OPENCODE_API_KEY` + `OPENCODE_API_BASE` → optional Big Pickle calibration.
- ChatGPT is **always manual** (the consumer surface is what we measure; no public API
  replicates its search behavior).

### Step 1 — Smoke the harness (2 min)

```powershell
pwsh -NoProfile -File research/ai-citation-baseline/harness.ps1 -KeywordsOnly
```

You should see all 20 prompts, deterministic and numbered. Then a dry WhatIf pass:

```powershell
pwsh -NoProfile -File research/ai-citation-baseline/harness.ps1 -Engine gemini -Auto -Limit 2 -WhatIf
```

Nothing should be sent; you should get `[WhatIf]` lines.

### Step 2 — Pick a mode

**Mode A (recommended, pure copy-paste):** run the plain harness and paste into the
real engine UIs:

```powershell
pwsh -NoProfile -File research/ai-citation-baseline/harness.ps1 -Engine all
```

For each keyword it prints `PROMPT to paste into a NEW <engine> chat:` and the
transcript target path.
- ChatGPT: open https://chatgpt.com — **new chat**, paste, wait for full reply, copy
  reply into `transcripts/<date>/chatgpt/<NN>-<slug>.txt` (or write `REFUSED`/`ERROR`).
- Perplexity: open https://www.perplexity.ai — same flow.
- Gemini: open https://gemini.google.com — same flow.
- Tip: keep three browser windows, one per engine, and paste straight down the list.

**Mode B (hybrid auto + manual):** let the harness call the engines that have keys:

```powershell
pwsh -NoProfile -File research/ai-citation-baseline/harness.ps1 -Engine all -Auto
```

Gemini (and Perplexity if keyed) transcripts are saved automatically; ChatGPT still
prints paste instructions. Big Pickle is available separately:
`-Engine bigpickle -Auto` (`OPENCODE_API_BASE` must be set).

Scoped runs also work: `-Engine gemini -Keyword k13`, `-Limit 5`, etc.

### Step 3 — Fill the ledger (10 min)

Open `results-ledger.csv` (60 rows pre-filled with keyword/engine/prompt and transcript
path templates). For each row set:

- `date` — today's date.
- `transcript_file` — the actual path created (or `MANUAL pending` if you skipped a run).
- `named`, `cited_correct`, `citation_valid` — y/n from §3.4.
- `score` — 0–3 from the rubric; the row also accepts the search term you used if you
  deviated (avoid — keep deterministic).
- `notes` — one line max; always include `HALLUCINATION: <what>` for score-2 runs.

Or use your spreadsheet app: it is a plain CSV with a header row.

### Step 4 — Verify and close

1. Confirm transcript count: 60 files (minus refusals/errors, which get a file too).
2. Confirm every row scored.
3. Record the baseline in `research/ai-social-proof-quotes.md` (create from §5) and in
   the next Monitor.
4. Update the KPI: `AI Citation Rate = score-3 runs ÷ 60` (+ breakdown per engine).
5. Comment the baseline location on the ticket (or tell a Pharos agent to).

Total: ~20 minutes. The harness removes all judgment about **what** to ask; you only
paste, copy, and score.

---

## 7. Definitions, edge cases, and honesty guardrails

- **"Lightspeed" alone is not a mention** — it collides with Lightspeed Commerce
  (Canadian POS, `lightspeedhq.com`). A reply about the Montreal company is
  `named=n` AND (usually) off-topic for our keywords; if it *wrongly* attributes
  agentic-AI work to Lightspeed Commerce, it is `named=y, cited_correct=n` → score 2
  with a brand-collision hallucination flag.
- **Name variants count**: "Lightspeed Holdings", "LightSpeed Holdings", "Jack Mlusu",
  "Jacob Mlusu" all count as named. "the 144-agent company in Malawi" without a name
  does **not**.
- **Engine refusal vs generic**: a benign "I don't follow specific companies" with a
  still-useful answer = 1 Generic. A hard refusal/error with no answer = 0.
- **Never manufacture evidence.** If the live run is skipped, the baseline is not
  "done" — it is pending. `proxy-baseline.md` exists only to calibrate the harness and
  is explicitly NOT authoritative. Do not quote proxy results in public artifacts.
- **Do not prompt-engineer the engines** (e.g. "search for lightspeedholdings.com").
  Full stop.
- **API transcripts are not identical to consumer-UI behavior.** Gemini API replies
  may lack the web UI's grounding; treat API transcripts as *calibration*, and prefer
  consumer-surface (manual) transcripts for the headline number.

---

## 8. Baseline storage & repeat protocol

| Item | Value |
|---|---|
| Baseline home | `research/ai-citation-baseline/` |
| Ledger | `research/ai-citation-baseline/results-ledger.csv` |
| Transcripts | `research/ai-citation-baseline/transcripts/<date>/<engine>/` |
| Row count (full cycle) | 60 (20 keywords × 3 engines) |
| Cadence | Every major public release + quarterly minimum |
| KPI | AI Citation Rate = score-3 runs ÷ 60; also track named-rate (score ≥ 2) and hallucination-rate (score 2 with flag) |

Cycle checklist (copy into the ticket comment after each live run):

- [ ] `harness.ps1` executed (mode A or B)
- [ ] 60 rows in `results-ledger.csv`, all scored
- [ ] transcripts/`<date>`/ exists with 60 files (incl. `REFUSED`/`ERROR` files)
- [ ] hallucination flags summarized (count + top offenders)
- [ ] `research/ai-social-proof-quotes.md` refreshed with score-3 quotes
- [ ] KPI updated; delta vs previous cycle noted
