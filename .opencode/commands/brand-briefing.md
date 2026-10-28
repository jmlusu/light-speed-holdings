---
description: Convert a campaign's raw NotebookLM briefing into a 100% brand-compliant 2-page PDF
---

!`uv run python scripts/brand_briefing.py $ARGUMENTS`

The `/brand-briefing` converter ran above. Report the result to the user and stop.

- **`STATUS: OK`** — the PDF is ready. Tell the user it is ready, give the absolute
  PDF path, the page count, the palette result for each page, and the QA report
  path. Do not summarise or restate the briefing's content; the PDF is the artifact.
- **`STATUS: FAILED`** — quote the failing gate and its numbers verbatim, say the
  PDF is not brand-compliant, and stop. Do not describe it as ready.
- **No `STATUS:` line, or a traceback** — report that the converter failed and paste
  the error. Do not retry with different flags unless the user asks.

Hard rules: never hand-edit or post-process the PDF, never re-run with a looser
`--tolerance` to force a pass, and never claim brand compliance that a gate did
not report.

Usage notes for the user (only mention if relevant):

- `/brand-briefing` — uses the most recent campaign under `artifacts/campaigns/`
  that has `notebooklm/raw-briefing.md`.
- `/brand-briefing artifacts/campaigns/<slug>` — targets a specific campaign.
