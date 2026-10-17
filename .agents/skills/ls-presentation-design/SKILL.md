---
name: ls-presentation-design
description: "The LightSpeed executive communication engine. Produces board presentations, investor decks, strategy decks, keynotes, conference and training decks. Enforces the branded LightSpeed layout (10x7.5in slides, navy left rail, navy/red/cyan palette, Arial scale). Pipeline: narrative -> storyline -> slide architecture -> charts -> speaker notes -> render (python-pptx via brand generators, or branded PPTX templates) -> ls-artifact-qa. Trigger on: 'make a deck', 'presentation', 'keynote', 'pitch deck', 'board slides', 'slides for X', '/create-keynote'."
---

# LightSpeed Presentation Design

The executive communication engine for LightSpeed Holdings. Every deck is branded, narrative-driven, and QA'd.

## Preconditions

1. Load `ls-design-system` — deck layout, palette, type scale, and logo rules come from it.
2. Identify the deck type to set tone and length:
   - **Investor pitch** — ~13–15 slides; hook → problem → solution → market → product → traction → team → financials → the ask.
   - **Board meeting** — ~9–10 slides; strategy decisions, KPI review, decisions needed, escalate.
   - **Keynote / conference** — narrative arc; fewer words, bigger ideas, strong visual metaphor.
   - **Training / internal** — objectives → method → walkthrough → practice → next steps.

## Pipeline

```
Brief ──► Narrative ──► Storyline ──► Slide architecture ──► Charts/Diagrams ──► Speaker notes ──► Render ──► QA
```

### 1. Narrative
One-sentence thesis + the change you want in the audience (from `ls-creative-director` brief). Every slide must serve the thesis or it gets cut.

### 2. Storyline
Sequence the argument: Hook → Context/Problem → What/How → Proof/Evidence → Implication → Ask/Call-to-action. For board decks the spine is: where we are, what changed, what we propose, what we need approved.

### 3. Slide Architecture
- Title slide: navy cover, logo, tagline in cyan, red accent divider, confidentiality/date.
- Content slides: white, navy left rail (0.15in), 28pt bold navy section title, body from brand scale.
- One idea per slide. Max ~6 bullets per slide, ~12 words per bullet.
- Data slides: KPI cards (light-grey rounded rects, big navy figure, dark-grey label) — see the traction slide in `generate-pitch-deck.py`.
- Closing slide: navy cover, "THANK YOU", contact block.

### 4. Charts & Diagrams
- Keep them inside the brand palette (navy/red/cyan/greys). Never default to a vendor chart theme.
- Prefer: bar (navy series, red highlight), line (navy, cyan trend), 2×2 or KPI cards.
- Complex system diagrams → route to `ls-diagramming`, then embed the rendered SVG/PNG.

### 5. Speaker Notes
Every slide gets speaker notes: what to say (2–4 sentences), the proof point, and the transition. Never put the full talk on the slide.

### 6. Render

**Preferred path — branded generators (python-pptx, installed v1.0.2):**
- Pitch deck → extend/clone `static/brand/templates/generate-pitch-deck.py`
- Board meeting → extend/clone `static/brand/templates/generate-board-meeting.py`
- Run with: `uv run python <script>.py`

**Alternative — branded template:** open `static/brand/templates/pitch-deck.pptx` or `board-meeting.pptx` and fill slides while preserving layout.

**Rich/SVG decks:** if the brief demands executive 2×2s, waterfalls, or small multiples, consider `k-dense-mckinsey-style` which renders those patterns to SVG/HTML export.

**16:9 override:** set slide size 13.333 × 7.5in for widescreen venues; keep navy rail + composition identical.

## Branded Deck Anatomy (Memorize)

| Zone | Spec |
|------|------|
| Cover background | Navy `#070A40` |
| Tagline on covers | Cyan `#00BFFF`, 18pt, "ASPIRE. ACT. ACHIEVE." |
| Red accent divider (covers) | 3in × 0.04in red rect centered |
| Section title | Arial 700, 28pt, navy |
| Content body | Arial 400, 12–14pt, navy |
| KPI card label | dark-grey `#6B7280`, 12pt |
| Left rail (content slides) | 0.15in navy rect, full height |

## Quality Gates (before `ls-artifact-qa`)

- [ ] One idea per slide
- [ ] ≤6 bullets/slide, ≤12 words/bullet
- [ ] Brand palette only; no vendor chart themes
- [ ] Logo = official asset; `™` on first mention
- [ ] Real facts/figures (not invented) — pull from `company/`, `results/`, docs, or the brief
- [ ] Speaker notes written for every slide
- [ ] Slide count matches deck type convention
- [ ] No overflow: text fits shapes, nothing clipped

Deliver the rendered file (PPTX/PDF), speaker notes, and QA verdict.
