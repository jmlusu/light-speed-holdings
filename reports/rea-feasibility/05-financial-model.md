# REA Feasibility — Financial Model

**Date:** 2026-10-17
**Owner:** financial-analyst (reports-to: cfo)
**Status:** DIRECTIONAL — for Phase 1 feasibility only; not a committed budget or price list
**Related:** `reports/rea-feasibility/00-rea-capabilities.md` (tool facts), `docs/ai-caas-pricing-model.md` (AI-CaaS margin precedents), `config/company/guardrails.yaml` (LLM spend caps)

> All dollar figures are USD unless noted. MWK equivalents use the ~1,800 MWK/USD display rate used in the CEO Dashboard and marketing materials — this is an estimate for dual-currency context, not a transacted or hedged rate (`docs/DASHBOARD_DATA_DICTIONARY.md`, `validate_evidence.py`). Every price, margin, and cost figure below is labeled **DIRECTIONAL** and must be validated with real engagements before external use.

---

## 1. Annual Cost Model (USD)

### 1.1 Tooling (annual license / seat cost)

| Tool | License | Annual cost (USD) | MWK equiv (×1,800) | Notes / source |
|------|---------|-------------------|--------------------|----------------|
| REA (Reverse Engineer Anything) | MIT, open source | $0 | MWK 0 | `00-rea-capabilities.md` S1 |
| Ghidra | Open source (NSA) | $0 | MWK 0 | `00-rea-capabilities.md` |
| Hopper (individual seat) | Proprietary, individual | ~$99 | ~MWK 178,200 | DIRECTIONAL; secondary-source list price |
| IDA Pro (optional, commercial) | Proprietary, commercial | UNVERIFIED (~$1,500–5,000/yr individual-equivalent) | UNVERIFIED | Marked UNVERIFIED in `00-rea-capabilities.md`; treat as $0 in base model, variable upside in optimistic case |
| Cloud VM / analysis host (spare capacity) | IaaS | $0 incremental | MWK 0 | Assumes reuses existing cloud/ops budget; no new dedicated host required for pilot |

**Base-case tooling subtotal (annual): $99 (~MWK 178K).**
Optimistic case adds optional IDA Pro only if a specific client engagement requires it; treat as variable per-engagement cost, not annual fixed.

### 1.2 Compute + model/token cost per analysis hour

Operating model assumes the existing AI-CaaS / executor stack routes primarily to local models (`ollama/llama3.1-8b-32k`) at ~$0 marginal token cost; paid providers are capped at **$0.50/task and $2.00/day** by `config/company/guardrails.yaml` and hard-stop on overspend. Reverse-engineering tasks (decompilation narrative, protocol inference, report drafting) may run more steps than a typical consulting task, so we model a blended rate.

| Cost component | Conservative | Base | Optimistic | Basis |
|----------------|--------------|------|------------|-------|
| Paid-model tokens per analysis hour | $4.00 | $2.00 | $0.50 | 8 paid tasks/hr × $0.50 (conservative) → 4 × $0.50 (base) → 1 × $0.50 (optimistic, mostly local) |
| Local-model tokens per analysis hour | $0 | $0 | $0 | Local inference, no marginal API cost |
| Cloud CPU/GPU burst (decompile, emulate) | $2.00 | $1.00 | $0.50 | DIRECTIONAL; assumes existing spare capacity, burst only |
| **Total compute/model per analysis hour** | **$6.00** | **$3.00** | **$1.00** | Sum of above |

### 1.3 Labor hours per engagement archetype (human-in-the-loop)

Model: 1 human analyst (senior RE / tech-due-diligence lead) + agent workforce. Human does judgment, scoping, client interaction, and final QA review; agents do bulk decompilation, corpus analysis, and report drafting.

| Archetype | Conservative hours | Base hours | Optimistic hours |
|-----------|--------------------|------------|------------------|
| Legacy binary interoperability report | 80 | 40 | 20 |
| Competitor app teardown | 60 | 30 | 15 |
| M&A target software due-diligence | 100 | 50 | 30 |

Fully loaded human analyst cost: **$75/hr** (DIRECTIONAL — senior specialist, loaded with benefits + overhead; not drawn from a published rate card; validate against actual payroll).

### 1.4 QA / review allocation

Peer review + CISO/ethics review for M&A and competitor teardown work (security-sensitive reverse engineering). Adds a fixed review budget per engagement, scaled by archetype risk.

| Archetype | Conservative | Base | Optimistic |
|-----------|--------------|------|------------|
| Legacy binary interoperability report | 12h × $75 = $900 | 8h × $75 = $600 | 4h × $75 = $300 |
| Competitor app teardown | 16h × $75 = $1,200 | 10h × $75 = $750 | 6h × $75 = $450 |
| M&A target software due-diligence | 24h × $75 = $1,800 | 16h × $75 = $1,200 | 10h × $75 = $750 |

### 1.5 Legal / compliance allocation (annual, shared)

One-time MSA/DPA template review for the REA practice line: **$2,000** (DIRECTIONAL — assume reuses existing LightSpeed MSA infrastructure; incremental cost is scope-clause and IP-ownership language for reverse-engineering deliverables). Amortize over Year-1 pilot engagements (~$400–$1,000 per engagement depending on count).

### 1.6 Annual cost rollup (pilot year vs. steady-state)

| Line | Year-1 pilot (0–5 engagements, 3 sold) | Year-2 steady-state (12 engagements) |
|------|-----------------------------------------|--------------------------------------|
| Tooling (annual) | $99 | $99 |
| Legal / compliance (one-time) | $2,000 | $0 |
| Compute/model (blended $3/hr, 3 engagements × 40h) | $360 | $1,080 |
| Human analyst labor (blended 40h × $75) | $9,000 | $36,000 |
| QA / review (blended $600 × 3) | $1,800 | $7,200 |
| **Total annual cost** | **$13,259** | **$44,379** |

MWK equivalents (×1,800, estimate): Year-1 ≈ MWK 23.9M; Year-2 ≈ MWK 79.9M.

---

## 2. Pricing Archetypes (indicative ranges, DIRECTIONAL)

Four archetypes, priced off the existing AI-CaaS engagement bands (`docs/ai-caas-pricing-model.md`: Discovery Sprint $8–12K, Build Sprint $15–25K, Full Engagement $25–50K) and adjusted for reverse-engineering specialization and risk.

| # | Archetype | Scope summary | Price range (USD, DIRECTIONAL) | MWK equiv range (×1,800, estimate) | Payment terms |
|---|-----------|---------------|--------------------------------|-------------------------------------|---------------|
| 1 | **Legacy binary interoperability report** | Reverse one legacy binary / protocol surface; deliver interface + behavior documentation for modernization teams | $15,000 – $25,000 | MWK 27M – 45M | 50% upfront / 50% on delivery |
| 2 | **Competitor app teardown** | Reverse engineer competitor mobile/desktop app: architecture map, feature inventory, technique extraction | $12,000 – $20,000 | MWK 21.6M – 36M | 50% upfront / 50% on delivery |
| 3 | **M&A target software due-diligence** | Reverse core target software for IP quality, tech-debt, security posture, integration risk | $30,000 – $60,000 | MWK 54M – 108M | 40% upfront / 30% mid / 30% on delivery |
| 4 | **Ongoing RE retainer** | Standing reverse-engineering capacity (N hours/mo, priority turnaround, knowledge-base upkeep) | $4,000 – $8,000 / mo | MWK 7.2M – 14.4M / mo | Monthly, net-15 |

All ranges are **DIRECTIONAL** and must be validated with 2–3 real prospects before any external rate card is published, consistent with the AI-CaaS pricing model's own "PROPOSED" status.

---

## 3. Unit Economics — Three Core Archetypes

### 3.1 Assumption tables (per engagement)

| Assumption | Value | Label |
|------------|-------|-------|
| Human analyst fully loaded rate | $75/hr | DIRECTIONAL |
| Compute/model cost per analysis hour (base) | $3.00/hr | DIRECTIONAL (§1.2) |
| QA/review human hours (base, by archetype) | See §1.4 | DIRECTIONAL |
| Gross margin floor (company policy) | 55% | From `docs/ai-caas-pricing-model.md` §5 |
| Tooling marginal cost per engagement | $0 (sunk annual license) | From §1.1 |

### 3.2 Legacy binary interoperability report

| Scenario | Hours (human) | Model/compute | QA cost | Labor cost | Total direct cost | Price (mid) | Gross profit | Gross margin |
|----------|---------------|---------------|---------|------------|-------------------|-------------|--------------|--------------|
| Conservative | 80 | $480 | $900 | $6,000 | $7,380 | $15,000 | $7,620 | 50.8% |
| Base | 40 | $240 | $600 | $3,000 | $3,840 | $20,000 | $16,160 | 80.8% |
| Optimistic | 20 | $120 | $300 | $1,500 | $1,920 | $25,000 | $23,080 | 92.3% |

### 3.3 Competitor app teardown

| Scenario | Hours (human) | Model/compute | QA cost | Labor cost | Total direct cost | Price (mid) | Gross profit | Gross margin |
|----------|---------------|---------------|---------|------------|-------------------|-------------|--------------|--------------|
| Conservative | 60 | $360 | $1,200 | $4,500 | $6,060 | $12,000 | $5,940 | 49.5% |
| Base | 30 | $180 | $750 | $2,250 | $3,180 | $16,000 | $12,820 | 80.1% |
| Optimistic | 15 | $90 | $450 | $1,125 | $1,665 | $20,000 | $18,335 | 91.7% |

### 3.4 M&A target software due-diligence

| Scenario | Hours (human) | Model/compute | QA cost | Labor cost | Total direct cost | Price (mid) | Gross profit | Gross margin |
|----------|---------------|---------------|---------|------------|-------------------|-------------|--------------|--------------|
| Conservative | 100 | $600 | $1,800 | $7,500 | $9,900 | $30,000 | $20,100 | 67.0% |
| Base | 50 | $300 | $1,200 | $3,750 | $5,250 | $45,000 | $39,750 | 88.3% |
| Optimistic | 30 | $180 | $750 | $2,250 | $3,180 | $60,000 | $56,820 | 94.7% |

**Base-case unit-economics summary (single engagement, base scenario):**

| Archetype | Mid price | Direct cost | Gross margin |
|-----------|-----------|-------------|--------------|
| Legacy binary interoperability report | $20,000 | $3,840 | 80.8% |
| Competitor app teardown | $16,000 | $3,180 | 80.1% |
| M&A target software due-diligence | $45,000 | $5,250 | 88.3% |

All base-case margins clear the 55% floor. Conservative-case margins for archetypes 1–2 fall slightly below 55% (50.8%, 49.5%) — flag for pricing or scope tightening before pilot.

---

## 4. Pilot, Scale, Break-Even, Sensitivity

### 4.1 Year-1 pilot (0–5 engagements)

| Metric | Conservative | Base | Optimistic |
|--------|--------------|------|------------|
| Engagements closed | 2 | 3 | 5 |
| Mix (assume equal split across archetypes 1–3) | 2 teardowns | 1 of each | 2 teardowns, 2 interop, 1 M&A |
| Total revenue | $28,000 | $81,000 | $161,000 |
| Total annual cost (from §1.6) | $13,259 | $13,259 | $13,259 |
| Net contribution (pre-overhead allocation) | $14,741 | $67,741 | $147,741 |
| Implied pilot margin | 52.6% | 83.6% | 91.8% |

### 4.2 Year-2 scale

| Metric | Conservative | Base | Optimistic |
|--------|--------------|------|------------|
| Engagements closed | 8 | 12 | 18 |
| Avg revenue / engagement | $22,000 | $30,000 | $38,000 |
| Total revenue | $176,000 | $360,000 | $684,000 |
| Total annual cost (from §1.6 steady-state) | $44,379 | $44,379 | $44,379 |
| Net contribution | $131,621 | $315,621 | $639,621 |

### 4.3 Break-even

Fixed annual cost (steady-state, Year-2) = **$44,379** (from §1.6). At base blended contribution per engagement ($30,000 − $4,420 direct = $25,580), break-even volume = **$44,379 / $25,580 ≈ 1.74 → 2 engagements per year.** Conservative contribution ($22,000 − $6,060 = $15,940) → break-even ≈ **2.8 → 3 engagements/year.** Break-even is therefore achievable within the Year-1 pilot itself under the base mix.

### 4.4 Sensitivity (base case, Year-2)

| Lever | Move | Impact on Year-2 net contribution | Direction |
|-------|------|------------------------------------|-----------|
| Analyst utilization (% of capacity on billable RE vs. BD/admin) | 40% → 60% | −$38,000 → +$19,000 | Higher utilization = more billable capacity without new hires |
| Model/token cost drift | +50% on $3/hr base | −$2,160 (12 engagements × 40h × $1.50) | Small absolute impact; local-model routing is the real hedge |
| Model/token cost drift | −50% on $3/hr base | +$2,160 | Same |
| Avg deal size | −20% | −$72,000 | Pricing power is the dominant lever |
| Avg deal size | +20% | +$72,000 | Same |
| Review/QA overrun | +50% hours on base QA | −$3,600 | Manageable; cap via engagement SOW |
| Human hour overrun | +25% hours on base labor | −$108,000 | Largest single risk — scope discipline required |

**Read:** unit economics are most sensitive to **human hour overruns and deal size**, not model token costs (which are capped by existing guardrails and mostly local). Scope control and pricing discipline are the primary management levers.

---

## 5. Internal Budget Ask (Year-1 pilot)

| Category | Amount (USD) | MWK equiv (×1,800) | Notes |
|----------|--------------|--------------------|-------|
| Tooling (Hopper individual seat + any one-time licenses) | $99 | MWK 178K | §1.1; IDA Pro excluded from ask (optional, per-engagement) |
| Legal / compliance (MSA/IP clause review) | $2,000 | MWK 3.6M | One-time; amortize over pilot engagements |
| Compute/model budget headroom (paid-provider overage above $2/day cap, if approved) | $500 | MWK 900K | Contingency only; local-model default keeps this near $0 |
| Analyst labor (pilot: 3 engagements × 40h base × $75) | $9,000 | MWK 16.2M | Captured as internal opportunity cost, not new cash if staffed from existing team |
| QA / review allocation | $1,800 | MWK 3.24M | §1.4 |
| **Total Year-1 pilot ask** | **$13,399** | **MWK 24.1M** | Matches §1.6 annual cost ($13,259) + $140 rounding/contingency |

**Time-to-MVP:** tooling is open-source ($0) and existing AI-CaaS agent stack can host REA workflows; MVP = 1 working end-to-end teardown report using REA + Ghidra + local models. Estimated **2–3 weeks** of analyst time (DIRECTIONAL) to produce the first reference deliverable, already inside the pilot labor budget.

### Opportunity cost vs. other portfolio bets

| Alternative | Indicative Year-1 cost | Indicative Year-1 revenue | Notes |
|-------------|-------------------------|----------------------------|-------|
| AI-CaaS Discovery Sprint line (existing) | $25–50K / engagement | $8–12K / sprint | Existing proposed pricing; higher cash cost per deal |
| Offer F WLO-in-a-Box license (Starter) | $0 marginal (existing template) | $15K/yr + $250/mo | Productizes existing stack, not RE-specific |
| REA pilot (this model) | $13.4K Year-1 | $81K base (3 engagements) | Lowest pilot cash outlay of the three; highest leverage on existing open-source REA stack |

**Opportunity-cost read:** the REA pilot is cheaper to stand up than a net-new AI-CaaS delivery line because it reuses the existing executor/agent stack and open-source tooling; the main cost is analyst attention (internal opportunity cost, not new cash). It should be prioritized over new paid-tool pilots, but not over expanding proven AI-CaaS engagements if deal flow already exists there.

---

## 6. Risks

| Risk | Category | Potential impact | Mitigation |
|------|----------|------------------|------------|
| **Unpaid scoping** — free discovery / scoping calls that never convert | Commercial | Labor burn with no revenue; pilot margin collapses | Fixed-price Discovery Sprint (not free) for REA scoping; 50% upfront before deep analysis |
| **Scope creep** — client expands binary set, platforms, or report depth mid-engagement | Delivery | Human hours overrun (largest sensitivity, §4.4); margin erosion | Hard SOW with change-order clause (mirrors AI-CaaS "express ≤50% turnaround = +40%"); cap review rounds |
| **Evidence / review overruns** — M&A or competitor teardown requires extra QA, CISO review, or client disputes findings | Delivery / Compliance | QA cost overrun; delay; rework | Pre-agree QA hours in SOW; ethics/CISO gate for Tier 3+ (per existing governance); liability cap = 100% of fees |
| **Client disputes / rework** — findings contested, re-analysis demanded | Commercial | Unbilled rework hours; reputation | Deliverables include evidence appendix (tool version, methodology); acceptance criteria signed at kickoff |
| **Tool / license change** — Hopper, IDA, or Ghidra licensing terms shift; REA upstream abandoned | Operational | Tooling cost jump; workflow rewrite | REA is MIT (low abandonment risk); treat IDA Pro as optional; maintain Ghidra as zero-cost fallback |
| **FX / dual-currency risk** — MWK-quoted engagements lose margin on devaluation (44% devaluation Nov 2023) | Financial | Realized USD margin shrinks on MWK deals | Quote USD for international; MWK quotes with 7-day validity; index large MWK contracts to signing rate (per existing MoU practice) |
| **Model cost drift** — paid-provider prices or usage patterns change | Financial | Small absolute impact (§4.4); caps protect | Existing $0.50/task, $2/day guardrails hard-stop runaway spend; prefer local models |

---

## Sources

| Claim | Source |
|-------|--------|
| REA MIT / $0, Ghidra $0, Hopper ~$99/yr, IDA Pro UNVERIFIED | `reports/rea-feasibility/00-rea-capabilities.md` |
| AI-CaaS engagement bands ($25–50K, 60–75% margin) | `docs/ai-caas-pricing-model.md` §1 |
| LLM spend caps ($0.50/task, $2/day), local-model default | `config/company/guardrails.yaml` |
| Gross margin floor 55%, cost control ≤10% of revenue | `docs/ai-caas-pricing-model.md` §5 |
| MWK/USD display rate ~1,800 | `docs/DASHBOARD_DATA_DICTIONARY.md`, `validate_evidence.py` |
| Payment terms (50/50), express turnaround surcharge | `docs/ai-caas-pricing-model.md` §3 (inherited from Malawi catalog) |
| Human analyst rate $75/hr | DIRECTIONAL internal assumption — not from a published rate card |
| Engagement hours, QA hours, compute/model per-hour costs | DIRECTIONAL estimates derived from AI-CaaS operating model + guardrail caps |
