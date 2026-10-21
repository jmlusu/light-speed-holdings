---
name: ls-od-deck
description: "Render HTML presentation decks with Open Design, including narrative structure, slide sourcing from existing templates, speaker notes, and export. Trigger on: 'od deck', 'html deck od', 'open design slides', 'render deck od', 'html-ppt'."
---

# Open Design Decks

Open Design renders decks as static HTML from shipped templates in `open-design/design-templates/`. Build the argument first, start from an existing template, render through `od`, then QA the artifact.

## When To Use

- The user asks for an Open Design deck, an `html-ppt` deck, or HTML slides.
- Existing notes, a report, or a strategy document must become a presentable deck.
- A deck needs speaker notes, presenter mode, or HTML-first export.
- For native PowerPoint generation instead, use `ls-presentation-design`.

## Template Families

Start from a shipped template. Do not invent a template ID or a folder name.

| Family | Use |
|--------|-----|
| `html-ppt` | General HTML deck studio. 36 themes, 31 layouts, 15 full-deck templates, presenter mode. Default for strategy and consulting decks. |
| `html-ppt-<variant>` | Focused full-deck variants such as `html-ppt-pitch-deck`, `html-ppt-product-launch`, `html-ppt-tech-sharing`, `html-ppt-weekly-report`, and the `html-ppt-zhangzara-*` visual systems. Match the variant to audience and tone. |
| `guizang-ppt` | Single-file magazine-style deck with serif headlines, WebGL hero backgrounds, and horizontal paging. Use for launches, salons, and talks with a strong visual identity. |
| `kami-deck` | Academic lab-meeting deck: design, results, caveats, and next experiment. Use for research reviews with a PI or lab group. |
| `ib-pitch-book` | Investor pitch book: market map, moat, unit economics, and the ask. Use for growth-equity fundraising. |
| `magazine-poster` | Editorial newsprint poster with an oversized serif headline, two-column body, and numbered sections. Use for essay, manifesto, or launch-poster briefs. |
| `simple-deck` | Operating review: growth, burn, and a path to sustainability. Use for leadership and corporate-strategy reviews. |
| `replit-deck` | Product and technical management deck for PRDs, roadmaps, RFCs, architecture reviews, and retros. Use for feature business cases and decision documents. |

**Do not use `magazine-web-ppt` as a template ID.** It is not a shipped directory. The `guizang-ppt` folder's frontmatter `name` is `magazine-web-ppt`, but the folder and CLI identifier are `guizang-ppt`. For a magazine deck use `guizang-ppt`; for a poster use `magazine-poster`.

Common `html-ppt` variants include `html-ppt-course-module`, `html-ppt-graphify-dark-graph`, `html-ppt-hermes-cyber-terminal`, `html-ppt-knowledge-arch-blueprint`, `html-ppt-obsidian-claude-gradient`, `html-ppt-pitch-deck`, `html-ppt-presenter-mode-reveal`, `html-ppt-product-launch`, `html-ppt-taste-brutalist`, `html-ppt-taste-editorial`, `html-ppt-tech-sharing`, `html-ppt-testing-safety-alert`, `html-ppt-weekly-report`, `html-ppt-xhs-pastel-card`, `html-ppt-xhs-white-editorial`, and the `html-ppt-zhangzara-*` families.

Read the chosen template's `SKILL.md` and copy its example or template assets. `html-ppt` requires copied layouts and token-based colors; `guizang-ppt` requires copying `assets/template.html` and placing images beside `index.html`.

## Narrative Structure

1. **Thesis** — one sentence stating the recommendation and the decision the audience must make.
2. **Storyline** — sequence the argument: hook, context, problem, evidence, options, recommendation, next steps. Cut any slide that does not serve the thesis.
3. **Slide architecture** — assign every slide one beat from the sequence. Typical mapping:

| Beat | Purpose |
|------|---------|
| `title` | Deck title, audience, date, confidentiality |
| `context` | Why this topic, why now |
| `problem` | The decision or gap that forces action |
| `evidence` | Facts, figures, proof points, source lines |
| `options` | Alternatives, trade-offs, and evaluation criteria |
| `recommendation` | The proposed choice and expected outcome |
| `next steps` | Owners, dates, and the ask |

4. **Charts and diagrams** — place a visual only where it advances the beat. Keep charts inside the template palette; route complex diagrams through `ls-diagramming`.
5. **One idea per slide** — short titles, limited bullets, no full script on the slide. Put the argument in the speaker notes.
6. **Speaker notes** — write what to say, the proof point, and the transition for every slide.

## Commands

Verified Open Design CLI shape:

```bash
od run start --project <projectId> --skill html-ppt --json
od run start --project <projectId> --skill html-ppt --follow
od run info <runId>
```

- `--skill <id>[,<id>]` selects the template. Use a shipped folder ID such as `html-ppt` or `guizang-ppt`.
- Attach `--design-system lightspeed` when the project is created (`od project create --design-system lightspeed`); `od run start` does not accept it.
- `--json` emits the run payload for scripts. `--follow` streams until completion.
- The conceptual scenario form `od run <scenario> --skill <id> --json` is not a current CLI form; scenario metadata lives in each template's `od.scenario`, and the CLI selects the template through `--skill`. Use the `start` subcommand shown above.

## Speaker Notes And Export

- `html-ppt`: wrap notes in `<div class="notes">...</div>` inside each slide. Press `S` for presenter mode; press `N` for the quick notes drawer.
- `guizang-ppt`: wrap notes in `<aside class="notes">...</aside>` or the template's notes block. The deck is a single `index.html`.
- Never place presenter-only text on the visible slide. Slide content is audience-facing; notes carry the script and cues.
- The rendered artifact is HTML, with `index.html` as the entry. Export formats follow the integration configuration: `html`, `svg`, `png`, `pdf`, and `pptx`.

## Handoff To QA

Hand the rendered deck to `ls-artifact-qa` before delivery. QA checks visual hierarchy, text overflow, contrast, responsive behavior, presenter notes, and consistency across slides. Fix findings and re-run QA; do not ship on a failing verdict.

## Verification

- [ ] Template ID exists under `open-design/design-templates/`; no invented IDs and no `magazine-web-ppt`.
- [ ] Narrative has one thesis and every slide maps to a beat.
- [ ] `od run start ... --json` exits 0 and returns a run ID or artifact path.
- [ ] `index.html` opens and paging works.
- [ ] Every slide has speaker notes; no presenter-only text is visible.
- [ ] `ls-artifact-qa` returns APPROVE.
- [ ] When brand mode is on, the deck follows the LightSpeed 10 × 7.5in navy/red/cyan system.
