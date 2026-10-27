---
description: Build every campaign asset — 9:16 and 16:9 video, infographics, carousel, 4-page PDF report and social copy — from a campaign's NotebookLM pack, gated on brand palette
---

!`uv run python scripts/generate_all_assets.py $ARGUMENTS`

The `/generate-all-assets` factory ran above. Report the result to the user and stop.

- **`STATUS: OK`** — every gate passed. Give the absolute campaign path and list each
  artifact with its real dimensions or page count as printed: the two MP4s
  (`1080x1920`, `1920x1080`), the three infographics, `social-carousel.pdf` and its
  card count, `comprehensive-report-branded.pdf` and its page count, and
  `threads-and-captions.md`. Give the palette result for each file and the manifest
  path (`qa/assets/assets-manifest.json`). Do not restate the campaign's content;
  the files are the deliverable.
- **`STATUS: FAILED`** — quote the failing gate and its numbers verbatim, say the
  affected artifact is not brand-compliant or not renderable, and stop. Do not
  describe it as ready.
- **No `STATUS:` line, or a traceback** — report that the generator failed and paste
  the error. Do not retry with different flags unless the user asks.

Hard rules: never hand-edit or post-process a rendered asset, never re-run with a
looser `--tolerance` to force a palette pass, never substitute a placeholder for a
missing gate, and never claim brand compliance that a gate did not report. Every
figure in every asset must trace to the campaign `dossier.md` or
`notebooklm/source-pack.md`; if a fact is absent the generator must leave it out,
not invent it.

Usage notes for the user (only mention if relevant):

- `/generate-all-assets` — uses the most recent campaign under `artifacts/campaigns/`
  that has a `notebooklm/` staging folder.
- `/generate-all-assets artifacts/campaigns/<slug>` — targets a specific campaign.
- `/generate-all-assets artifacts/campaigns/<slug> --skip-video` — everything except
  the two MP4s, for a fast copy-and-layout check.
- `/generate-all-assets artifacts/campaigns/<slug> --keep-frames` — keeps the PNG
  frame sequence under `video/frames/` for frame-level inspection.
