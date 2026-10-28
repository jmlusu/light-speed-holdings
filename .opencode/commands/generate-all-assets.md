---
description: Alias of /build-campaign — one-touch multimodal campaign build from notebooklm/raw-briefing.md and any NotebookLM audio
---

!`uv run python scripts/build_campaign.py $ARGUMENTS`

`/generate-all-assets` is the exact alias of `/build-campaign` and ran the same
routing logic above. Report the result to the user and stop.

- **`STATUS: OK`** — every gate passed. State the detected state (TEXT ONLY or
  TEXT + AUDIO), then list only the assets the run actually built, with their real
  numbers as printed: the PDF path, page count and page budget; the LinkedIn
  length; and, when the media branch ran, the two MP4 dimensions/durations, the
  two infographic dimensions, and the three copy files. Give the
  `text_integrity` result (blocks checked / missing) and the audit report path
  (`artifacts/campaigns/<slug>/PIPELINE-AUDIT-REPORT.md`). Do not restate the
  campaign's content; the files are the deliverable.
- **`STATUS: FAILED`** — quote the failing gate and its numbers verbatim, say the
  affected artifact is not ready, and stop. Do not describe it as ready.
- **No `STATUS:` line, or a traceback** — report that the build failed and paste
  the error. Do not retry with different flags unless the user asks.

Hard rules: never hand-edit or post-process a rendered asset; never re-run with a
looser `--tolerance` to force a palette pass; never substitute a placeholder for
a missing gate; never claim brand compliance or content completeness that a gate
did not report. The PDF must carry every paragraph, bullet and table row from
`notebooklm/raw-briefing.md` — if `text_integrity` reports a missing block, the
run is not shippable. Media assets require NotebookLM audio in
`notebooklm/` (`*.mp3` / `*.wav`); `--force-media` exists for QA only and must be
disclosed as forced if used.

Usage notes for the user (only mention if relevant):

- `/generate-all-assets` — most recent campaign with `notebooklm/raw-briefing.md`.
- `/generate-all-assets artifacts/campaigns/<slug>` — a specific campaign.
- `/generate-all-assets <slug> --skip-video` — everything except the two MP4s.
- `/generate-all-assets <slug> --force-media` — QA only: exercise the media
  branch when no audio exists; the audit records the override.
