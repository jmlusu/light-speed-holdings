---
name: ls-notebooklm-packager
description: "Compiles the NotebookLM hand-off for a LightSpeed campaign: turns a verified dossier into a single grounding markdown pack plus six engineered Studio prompts (Audio Overview, Executive Briefing, Strategic Institutional FAQ, 60-second Video Shorts script, Infographic Data Extraction Table, 4-page Comprehensive Executive Report), and the copy-paste instructions a human operator needs to run them supervised. Enforces the facts-only rule — every claim in the pack must already exist in the dossier, and a brief never gets to add one. Runs after the dossier is verified, feeds the multimodal asset factory, and stops before publication. Trigger on: 'notebooklm', 'package for notebooklm', 'source dossier', 'source pack', 'studio prompt', 'audio overview prompt', 'notebooklm grounding', 'video shorts prompt', 'infographic data prompt', '4-page report prompt'."
---

# LightSpeed NotebookLM Packager

NotebookLM is a grounding tool, not a generator of new claims. Your job is to hand it a source pack that is *already true* and prompts that keep its output inside that factual perimeter. Anything NotebookLM invents beyond the pack is a defect you caused by leaving a gap in the pack.

## Preconditions

1. **A verified dossier exists** at `artifacts/campaigns/{slug}/dossier.md`. If it does not, stop — a source pack is a projection of the dossier, never a substitute for it.
2. **Every claim in the dossier is traceable.** Read its provenance section; if a claim has no source, it does not go in the pack.
3. **Run a superlative sweep over the dossier itself**, not just the copy. `first`, `only`, `leading`, `largest` are permitted only where independently corroborated. The dossier is upstream of every other artifact, so a superlative that survives there propagates into the pack, the prompts, the audio, and the operator's talking points. Scan the preamble and body, not just the bullets.
4. **No emoji, `™` on first mention** of LightSpeed Holdings Limited, brand tagline "ASPIRE. ACT. ACHIEVE." where a signature line appears.

## What gets produced

Two files, both under `artifacts/campaigns/{slug}/notebooklm/`:

| File | Role |
|------|------|
| `source-pack.md` | The single upload. Grounding only — no prompts, no framing for the reader. |
| `studio-prompts.md` | The six prompts, copy-paste ready. Never uploaded. |

NotebookLM takes **one** source per notebook in this workflow. Do not split the pack into multiple files; a second source dilutes grounding and makes citation ambiguous.

Prompts 1–3 serve the legacy PDF/text surface. Prompts 4–6 feed the multimodal asset factory: `/generate-all-assets` consumes their **output** (not the prompts) when it builds video, infographic, carousel and report assets. A prompt that invents a fact therefore lands an invented fact in a rendered MP4 or PNG, where it is far harder to retract than a line of copy.

## The Source Pack contract

### Required sections

```markdown
# Source Pack for NotebookLM
## Campaign: {slug}

### Executive Summary
<2-3 sentences. What the campaign asserts, for whom, and why it matters.>

### Key Claims (Verified)
- **<Dimension>:** <claim>. <scope qualifier where the number alone would mislead.>
```

Add further `###` sections only for material the prompts will actually draw on (e.g. an architecture summary, a policy stance). Every bullet in `Key Claims` must name its dimension in bold so the model can cite by dimension rather than by paragraph.

### Claim traceability rule

Every sentence must be checkable against the dossier or the repository. This is the whole point of the file.

- **A number carries its scope.** `4` is meaningless; "four Python quality gates (ruff, mypy, bandit, pytest)" is defensible. A bare "4 CI gates" is false when the repository's required branch checks number six — the count and the scope must match, or the figure is invented by omission.
- **No new synthesis.** You may compress and reorder. You may not add an inference the dossier did not assert, even if it seems obviously true.
- **Name the proof.** A field-anchored case is stronger than an abstract capability claim; cite the specific deployment rather than gesturing at "real-world results".
- **Keep dates and version qualifiers** ("forthcoming", "draft") — dropping them turns a live process into a settled fact.

### Length

Aim for 400–900 words. NotebookLM grounds best on a dense, self-contained pack: long enough to answer follow-ups, short enough that a single upload remains readable end to end.

## The six Studio prompts

Write each as a quoted, self-contained instruction. The model cannot see the campaign, the brand, or this skill — only the pack.

Every prompt must state **role**, **audience**, **format**, and **the specific facts to emphasise**. Vague prompts produce generic output that then reads as a LightSpeed claim.

### 1. Audio Overview (Podcast Deep Dive)

Role: technically literate analyst. Format: spoken script, 10–15 minutes. Emphasise: the central engineering tradeoff and the field proof-case. Instruct it to stay inside the pack, and to name a gap rather than fill one.

### 2. Executive Briefing (2-page, HBR style)

Role: strategy summariser. Audience: C-suite or ministerial. Format: two pages, prose not bullets. Emphasise: architecture, commercial model, governance — the three things that audience is actually deciding on.

### 3. Strategic Institutional FAQ

Role: institutional-relations writer. Format: question/answer. Emphasise: the standing objections the institution will raise (bandwidth, data protection, technology debt, skepticism), the policy position, and the operational proof. Each answer must cite the pack.

### 4. Video Shorts Script (60 seconds, Reels / TikTok)

Role: short-form video scriptwriter. Audience: a non-specialist professional scrolling a feed. Format: a strict 60-second script as a timed beat table — `| beat | timecode | on-screen subtitle (≤42 chars) | visual note |` — covering hook (0–3s), the single claim (3–25s), the field proof (25–45s), the implication (45–55s), CTA (55–60s).

Emphasise **one** claim only. A 60-second short that argues two things argues neither. Put the field proof in the middle, because that is the beat a skeptical viewer stays for.

Hard limits, because a rendered short is expensive to retract:

- Every spoken and on-screen line must be a sentence that exists in the pack. A subtitle is a compression, never an addition.
- Subtitle lines are ≤42 characters so they survive a 9:16 safe area without reflow.
- The hook may not contain a superlative (`first`, `only`, `leading`, `largest`) unless the pack already carried it.
- No CTA that promises an outcome the pack does not claim. "Read the playbook" is safe; "cut your costs 40%" is an invention.

### 5. Infographic Data Extraction Table

Role: data extraction analyst. Format: one markdown table, `| metric | exact value | unit / scope | source section | status |`, one row per figure the pack actually contains.

`status` is **verified** or **gap**. This column is the point of the prompt: it is the difference between an infographic and a fabrication.

- `exact value` is copied, never rounded, recalculated, or derived. If the pack says "five-tier", the value is `5`, not `4` or `6`.
- `unit / scope` carries the qualifier that makes the number honest. `90 agents` is a headcount; `89 AI + 1 human` is the same figure with its scope intact. Record the scope or the renderer will ship the misleading version.
- Anything the pack does not state is recorded as a `gap` row with `NOT IN SOURCE` in the value column — never estimated, never interpolated from a neighbouring figure.
- Do not average, total, or compute percentages across rows. A derived ratio is a new claim.

The extraction table is what the infographic generator renders from. A gap row becomes a deliberate omission or an explicitly labelled gap in the graphic; it never becomes a plausible-looking number.

### 6. Four-Page Comprehensive Executive Report

Role: executive report author. Audience: board, ministerial, or institutional investment committee. Format: **exactly four pages**, prose and tables, no page longer than ~350 words.

| Page | Content |
|------|---------|
| 1 | Executive summary + the key metrics table from prompt 5 |
| 2 | Architecture: how it works, the offline-first / local-inference argument |
| 3 | Field evidence + governance and compliance posture |
| 4 | Commercial gaps, risks, and the explicit recommendation or ask |

Emphasise: architecture, commercial model, governance — the three things that audience is deciding on. State the gaps on page 4 rather than smoothing them over; a report that hides its unknowns is not decision-grade.

Constraints: paragraphs of 60–90 words; no bullet-only pages (pages 2 and 3 must argue in prose); every figure must also appear in the prompt 5 table, so the two artifacts cannot drift apart. Name a gap rather than filling one.

Do not ship a seventh prompt that asks NotebookLM to "expand", "imagine", or "project" — that is an instruction to invent.

## Operator handoff

End `studio-prompts.md` with the supervised sequence, because this is Option A: a human runs it, in order, reviewing between steps.

1. Create the notebook; upload `source-pack.md` as the **single** source.
2. Apply prompt 1; read the full output before generating prompt 2. A grounding error in the audio will repeat in everything downstream.
3. Apply prompts 2–6 in order, reviewing each output against the pack before moving on. Prompts 4–6 drive rendered assets, so an unreviewed claim there becomes a burned-in subtitle or a printed figure.
4. Review each output against the pack. Any claim not in the pack is a defect — delete it, don't publish it.
5. Confirm the two ship-gates before release: `™` on first mention, and no claim beyond the dossier.
6. Hand the prompt 4 script, prompt 5 table and prompt 6 report to `/generate-all-assets`, which compiles them into video, infographic, carousel and PDF assets under the campaign folder.
7. Publication stays a human action. This skill stages; it does not publish.

## QA gates

- [ ] `source-pack.md` and `studio-prompts.md` both exist under `notebooklm/`
- [ ] Every claim traces to the dossier or the repository — none added
- [ ] Every number carries a scope that matches its source
- [ ] Superlatives swept *in the dossier*, not only in the copy
- [ ] No emoji; `™` on first mention
- [ ] Six prompts present, each with role, audience, format, emphasis
- [ ] Prompt 4: ≤42-char subtitles, beats sum to 60 seconds, no superlative in the hook
- [ ] Prompt 5: every row `verified` or `gap`; no derived, averaged or interpolated figures
- [ ] Prompt 6: exactly four pages with the page plan honoured, figures matching the prompt 5 table
- [ ] Operator sequence present and ordered, with the review checkpoints stated
- [ ] Nothing published, and no publication implied

## Known limits, stated plainly

- **NotebookLM will hallucinate around a thin pack.** The fix is a denser pack, never a firmer instruction. If an output keeps drifting, the pack is missing a section — add it from the dossier.
- **Audio Overviews paraphrase.** Do not rely on the audio for precise figures; the pack and the briefings are the citable artifacts.
- **A prompt cannot un-invent a claim.** If a figure is wrong in the pack, every downstream artifact reproduces it faithfully. Verify before packaging.
