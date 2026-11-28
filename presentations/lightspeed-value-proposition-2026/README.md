# Lightspeed Value Proposition Deck — HAOMTGV & Venture Studio

**Artifact:** `Lightspeed-Value-Proposition-HAOMTGV-Venture-Studio.pptx`
**Slides:** 10 (10in × 7.5in, 4:3) — deck geometry per `brand/tokens.md` §Layout
**Audience:** Executive briefing for prospective client / partner review
**Owner:** Marketing / Creative Direction

## Purpose

A single-slide-proof value proposition for Lightspeed Holdings Limited™:
the governed AI-native operating model (HAOMTGV) and the AI Venture Studio that
packages it, framed as one offering.

## Slide Map

| # | Title | One idea |
|---|-------|----------|
| 1 | Cover | We run the system we sell; AI executes, humans decide. |
| 2 | The Gap | Decision rights were unnamed — that is why AI stalled. |
| 3 | Value Proposition | One operating model. Proven on ourselves. Packaged for you to own. |
| 4 | HAOMTGV | Seven layers, one loop; Value returns to Human as evidence. |
| 5 | H + A | Intent above; execution below. 90 roles, one accountable human. |
| 6 | O + M + T | Deterministic routing, durable memory, isolated tools. |
| 7 | G | Governance is the product: five tiers, four gates, sealed record. |
| 8 | Venture Studio | A repeatable engine, not a pipeline. Shared core before differentiation. |
| 9 | Method | Four gates, four numbers; a failed gate parks or kills. |
| 10 | Close | Start with a gate, not a pilot. |

## Sources (primary, in-repo)

- `content/drafts/homepage.md` §01, §04–§06, §07, §12 (claims ledgers, honesty labels)
- `docs/venture-studio/03-operating-model.md`
- `docs/venture-studio/05-kpi-scorecard.md`
- `docs/venture-studio/02-sector-positioning.md`
- `docs/venture-studio/04-technical-architecture.md`
- `ai_venture_studio_client_presentation.md` §1–§9
- `src/components/haomtgv/layers.ts`

All counts labelled `PROVEN IN-HOUSE` are read from those sources; studio metrics
marked with targets remain labelled as targets.

## Build / Verify / Render

```bash
python presentations/lightspeed-value-proposition-2026/build_deck.py
python presentations/lightspeed-value-proposition-2026/verify_deck.py

# render for visual QA
"C:\Program Files\LibreOffice\program\soffice.com" --headless --convert-to pdf --outdir <tmp> <deck>.pptx
```

## Brand Contract

- Palette: navy #070A40 (dominant), red #E63946, cyan #00BFFF, grey-light #F2F2F2, white #FFFFFF, grey-dark #6B7280.
- Type: Arial; sizes from the 36/32/28/24/18/16/14/13/12 pt scale.
- Spacing: multiples of 4px; slide layout 10 × 7.5 in with 0.15 in navy rail on content slides.
- Logo: official `brand/logo/` assets only; cleared to the visible artwork box.
- Tagline: "ASPIRE. ACT. ACHIEVE."
- Honesty: no invented revenue, clients or capability; status labels preserved.
