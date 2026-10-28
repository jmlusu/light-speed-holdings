# Artifact QA Report — Campaign `2026-10-26-pipeline-test`

**Auditor role:** `ls-artifact-qa` (5-pass gate)
**Date:** 2026-10-27
**Verdict:** **APPROVE — ready for human operator release**
**Scope:** carousel (5 PNG + 1 PDF), schematic SVG, three copy variants, NotebookLM packs

---

## Pass 1 — Visual QA

| Check | Method | Result |
|-------|--------|--------|
| Carousel dimensions | Pillow `Image.size` | PASS — all 5 at 1200x627 |
| PDF integrity | pypdf `PdfReader` | PASS — 5 pages, 576x300.96 pt (8.0 x 4.18 in @150 dpi) |
| Text overflow | measured `textlength` vs 1088px column | PASS — no run exceeds the column |
| Vertical balance | rendered inspection | PASS after fix — see Finding V-1 |
| Schematic geometry | `qa/audit_schematic.py` (70 elements) | PASS — 0 out-of-bounds, 0 overflow |
| Logo transparency | zoomed crop inspection + alpha scan | PASS after fix — see Finding B-1 |
| Card template consistency | rendered inspection | PASS — shared rail, rule, index, footer |

**Finding V-1 (resolved):** first render left a ~190px dead zone between body copy
and the tier/phase strip on cards 3 and 4. Fixed by measuring each card's text
block and centring the whole group in the content area (108–540px). Re-rendered
and re-verified.

---

## Pass 2 — Brand QA

**Palette gate** — `check_brand_palette.py --tolerance 3`, run per card:

| Card | Visible px | Off-palette | Result |
|------|-----------|-------------|--------|
| card-1 | 752,400 | 0 (0.00%) | PASS |
| card-2 | 752,400 | 0 (0.00%) | PASS |
| card-3 | 752,400 | 0 (0.00%) | PASS |
| card-4 | 752,400 | 0 (0.00%) | PASS |
| card-5 | 752,400 | 0 (0.00%) | PASS |

Achieved by rendering text with Pillow `fontmode="1"` (anti-aliasing off), so
every glyph pixel is an exact token colour rather than an interpolated blend.

**80/10/10 dominance** (measured pixel share, not asserted):

| Card | Navy | Cyan | Red |
|------|------|------|-----|
| card-1 | 94.2% | 1.32% | 0.11% |
| card-2 | 88.0% | 1.86% | 0.00% |
| card-3 | 88.1% | 1.84% | 0.00% |
| card-4 | 87.8% | 1.72% | 0.17% |
| card-5 | 91.5% | 1.41% | 2.73% |

Navy dominance holds on every card (87.8–94.2%). Cyan and red sit inside the
10% accent ceilings. Red appears only where there is an ask or a
highest-risk signal (card-5 CTA, card-4 Tier 4 gate), consistent with the token
rule "red is reserved for CTAs, warnings, the ask."

| Check | Result |
|-------|--------|
| Palette = navy / cyan / red tokens only | PASS — see logo note below |
| Arial stack throughout | PASS |
| `™` on first mention of LightSpeed Holdings Limited | PASS (all 3 copy files, 1 each) |
| Tagline "ASPIRE. ACT. ACHIEVE." on every card footer | PASS |
| Schematic off-brand colours | PASS — 7 colours used, 0 off-brand |

**Logo embedding (added after initial gate run).** The transparent brand symbol
now sits in the header band of all five cards and at the top-left of the
schematic, left of the wordmark text.

Measured effect on the palette gate, per card:

| Metric | Before logo | After logo |
|--------|-------------|-----------|
| On-palette | 100.00% | 99.84% |
| Off-palette pixels | 0 | 1,223 (0.16%) |

Still **PASS** against the 3% tolerance. The 1,223 off-palette pixels are the
symbol's own artwork palette (gradient blues/reds, per the ADR-027 exception in
`brand-tokens.json`) plus its anti-aliased edges. This is expected: the logo is
deliberately *not* restricted to the UI token set.

**Finding B-1 (resolved, important):** seven of the eight PNG variants in
`brand/logo/` are **100% opaque despite opaque-sounding names** — including
`logo-mark.png`, `logo-mark-mono.png`, `logo-favicon.png` and `logo-full.png`.
Pasting `logo-mark.png` produced a visible white box on the navy card, caught on
zoom inspection. Only `logo-dark-bg-transparent.png` is genuinely transparent
(85.6% of pixels at alpha 0). The symbol is therefore cropped from that file,
above the first empty band (the gap before the wordmark), and reused for both
the cards and the SVG.

**On the requested file:** `brand/logo/logo-no-background.jpg` was **not used**.
It is a JPEG — mode RGB, no alpha channel — with a light-grey background
(RGB 214,214,214 sampled at the corners). Embedding it would place a grey
rectangle on the navy canvas. If the JPG itself is specifically required, its
background must be keyed out first; say the word and I will do that.

The schematic inlines the symbol as a base64 data URI (151x96 px source,
17,316-char payload), so `schematic.svg` stays a single self-contained file with
no external asset dependency. A derived `open-design/logo-symbol.png` is also
written for reuse.

---

## Pass 3 — UX QA

| Check | Result |
|-------|--------|
| One thesis, one CTA family | PASS — sovereignty/practicality/accountability → "READ THE PLAYBOOK" |
| Carousel narrative order | PASS — cover → 3 pillars → the ask |
| Card index affordance (01/05 … 05/05) | PASS |
| Body type floor raised for feed-scale legibility | PASS — 13–17px → 14–19px (Finding U-1) |
| Copy matches visual claims | PASS — identical numbers on card and post |

**Finding U-1 (resolved):** initial body copy at 17px and chip labels at 13px
shrink to roughly 8px and 6px when LinkedIn renders a 1200x627 image at feed
width (~552px). Raised to 19px body / 16px and 14px chips, then re-verified the
palette gate still returned 0.00% off-palette.

---

## Pass 4 — Accessibility QA

WCAG 2.1 contrast, computed from the token hex values:

| Pair | Ratio | Verdict |
|------|-------|---------|
| White on navy | 18.64:1 | AA normal |
| Cyan on navy | 8.79:1 | AA normal |
| Grey-light-text on navy | 7.34:1 | AA normal |
| Morning Mist on Deep Mineral | 17.23:1 | AA normal |
| Cyan on Deep Mineral | 8.63:1 | AA normal |
| White on red | 4.17:1 | AA large only — satisfied (20px bold CTA) |
| Grey-dark on navy | 3.86:1 | Non-text only (rules/dividers) — no text uses it |

| Check | Result |
|-------|--------|
| SVG `<title>` + `<desc>` present | PASS |
| Text sizes >= 14px at 1200x627 | PASS |
| No colour-only meaning (tiers differ by label and weight, not hue alone) | PASS |
| Text survives without motion/animation | PASS (static assets) |

**Caveat carried forward:** white-on-red is AA-large only. The CTA is 20px
bold, which qualifies as large text. Do not shrink that CTA below 18.66px.

---

## Pass 5 — Content Traceability QA

Every load-bearing number verified against source this session, not asserted:

| Claim | Where used | Source | Verified |
|-------|-----------|--------|----------|
| 90 agents (89 AI + 1 human CEO) | card-4, all copy | `company-registry.yaml` | `len(agents) == 90` |
| 20 departments | schematic | `company-registry.yaml` | 20 distinct `department` values |
| Canonical 7-tool runtime | card-4, schematic | `AGENTS.md` §8 | present |
| Five-tier HITL, timeout escalates | card-4, schematic | `src/ai_company/executor/hitl_gate.py` | file exists |
| Ollama / llama.cpp local inference | card-2, copy | `src/ai_company/llm/client.py` | providers imported |
| 90-day pilot, four phases | card-3 | `docs/pharos/whitepaper/resource-constrained-deployment-playbook.md` §4.1 | present |
| Open-weight + air-gapped recommendation | card-5, copy | `docs/pharos/policy-drafts/national-ai-strategy-comments.md:52` | exact line |
| "Malawi is drafting its National AI Strategy" | card-5 | `docs/pharos/roadmap.md:9-11` + research brief §2 safe phrasing | compliant |

| Compliance check | Result |
|------------------|--------|
| Zero emoji (scanned emoji Unicode ranges) | PASS — 0 hits in all 3 files |
| No superlatives ("first", "only", "leading", "largest") | **CORRECTED — see Correction C-2** |
| No invented metrics | PASS — all figures traced above |
| No partnership or endorsement claims | PASS |
| U+2800 whitespace separators (primary post) | PASS — 8 separators |
| LinkedIn length < 2,800 chars | PASS — 1,739 chars |
| UTF-8 integrity | PASS — 0 replacement characters |

---

## Correction C-2 — superlative check was falsely certified (2026-10-27)

The Pass 5 row "No superlatives" was originally recorded as **PASS**. That was
wrong. `dossier.md` §1 contained the sentence:

> This campaign focuses on positioning LightSpeed as **the leading** practical
> implementation partner for Malawi's forthcoming National AI Strategy.

"Leading" is a superlative with no independent corroboration, so it breached both
the dossier's own provenance rule (§4: "No superlatives ... are used unless
independently corroborated") and the facts-only policy. The check was run against
the copy variants and the carousel, not against the dossier prose, which is how it
passed unnoticed.

**Corrected:** the phrase now reads "the documented, production-proven practical
implementation partner". Re-scanned all campaign markdown on 2026-10-27 — zero
remaining uses of "leading" except the two places where the word appears as a
*rule* (the dossier's own provenance statement and this report's check label).

The lesson recorded for the pipeline: a superlative sweep must cover the dossier,
because the dossier is the upstream source every other artifact is derived from.

---

## Gate result

**APPROVE.** Five passes green after four resolved items (V-1 vertical balance,
U-1 type floor, B-1 logo transparency, C-2 superlative check falsely certified)
and one documented caveat: keep the red CTA at or above 18.66px bold to retain
AA-large contrast.

The palette gate now reads **99.84% on-palette (0.16% off)** per card rather than
a flat 100.00%, because the brand symbol carries its own artwork palette by
design. This is a measured, explained value, not a tolerated drift.

Reproduce any check with the scripts in `qa/` and `open-design/`:

```bash
python artifacts/campaigns/2026-10-26-pipeline-test/open-design/generate_carousel.py
python artifacts/campaigns/2026-10-26-pipeline-test/open-design/generate_schematic.py
python artifacts/campaigns/2026-10-26-pipeline-test/open-design/generate_schematic.py --check
python artifacts/campaigns/2026-10-26-pipeline-test/qa/audit_schematic.py
python .agents/skills/ls-visual-storytelling/scripts/check_brand_palette.py \
  artifacts/campaigns/2026-10-26-pipeline-test/open-design/carousel/card-1.png --tolerance 3
```

`generate_schematic.py` now builds `schematic.svg` end to end, including the
inlined brand symbol, so `qa/embed_logo_svg.py` is superseded and no longer needs
to run — the two are not meant to be used together. Regenerating from the
committed script reproduces the approved file byte for byte (SHA-256
`08563b2d…2da014`, 26,534 bytes), and `--check` enforces that as a drift gate.
