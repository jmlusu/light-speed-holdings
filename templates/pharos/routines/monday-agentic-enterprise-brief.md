# Agentic Enterprise Brief — Monday (UTC 04:00)

Produce the weekly Pharos Agentic Enterprise Brief for the Human CEO.
Voice: authoritative yet forward‑looking, LightSpeed style. Audience: Malawi &
SADC institutional stakeholders (ministeries, SADC secretariat, UNDP/UNESCO‑ROSA,
banks, ICTAM). Cadence: every Monday, publishing a LinkedIn long‑form + distilled
email summary. Reference docs/Pharos/roadmap.md for the current quarter theme,
docs/Pharos/content-calendar.md for this week's slot, and the Agentic AI
Executive Lab workshop framework for structure.

## Prompt

Write a 800‑word briefing with the following sections, in order:
1. **Headline** — one sentence announcing the week's focus (draw from the
   quarterly theme in roadmap.md).
2. **Context** — 2‑3 sentences situating the theme within the Malawi‑SADC
   policy landscape (cite relevant regional initiatives).
3. **Evidence** — 2‑3 key statistics or findings, each with a citation tag
   referencing a primary source (use webfetch for up‑to‑date data; never cite
   Eden corpus as SADC evidence).
4. **Implication** — 2‑3 sentences on what the statistics mean for decision‑makers
   in the region.
5. **Opportunity** — one concrete opportunity for the CEO's initiative.
6. **Call‑to‑Action** — a single sentence framing the next step.

End with a footnote: "Data as of {date} (UTC). Sources verified via
k‑dense-research-lookup and regional verification pass."

## Prompt tokens

- `{date}` → today's UTC date (YYYY‑MM‑DD)
- `{quarter_theme}` → read from docs/Pharos/roadmap.md (if available)
