# Build Log — Wednesday (UTC 04:00)

Produce the weekly Pharos Build Log for the Human CEO.
Voice: pragmatic, focusing on delivered outputs and lessons learned. Audience:
Malawi & SADC institutional stakeholders. Cadence: every Wednesday, publishing a
LinkedIn post + distilled email summary. Reference docs/Pharos/roadmap.md for
current quarter theme, docs/Pharos/content-calendar.md for this week's slot,
and the previous week's Build Log for continuity.

## Prompt

Write a 600‑word Build Log with the following sections, in order:
1. **What was delivered** — list the three highest-impact artifacts completed
   this week (LinkedIn posts, research briefs, presentations, transcriptions).
2. **Key metrics** — posts published, engagements, subscriber delta vs the
   2,000 target (reference content_log.json and pharos_subscribers.json).
3. **Challenges** — 1‑2 obstacles encountered (data gaps, model cost, regional
   verification) and how they were mitigated.
4. **Insight** — one actionable insight or pattern observed during the week.
5. **Reflection** — a brief note on what worked / what to improve.

End with a footnote: "Data as of {date} (UTC). Source: content_log.json, pharos_subscribers.json."

## Prompt tokens

- `{date}` → today's UTC date (YYYY‑MM‑DD)
- `{subscriber_count}` → read from pharos_subscribers.json if available
- `{posts_this_week}` → count from content_log.json for the rolling 7‑day window
