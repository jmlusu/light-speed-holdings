# Plan

## Technical Approach

One Python generator, not six bash steps. `scripts/generate_all_assets.py` reads the campaign directory once, derives a single fact set, and lays out every asset from that set so the numbers cannot drift between a video caption and a report table.

- **Facts first.** `scope_of()` returns the *source line* containing a number, not a character window around it. The earlier character-window version cut mid-word and leaked markdown headings (`### 2.`) into the report's provenance column.
- **Renderers per medium, one layout vocabulary.** Pillow for the PNG infographics and carousel cards, Jinja2 HTML → headless Chrome → PDF for the report (with `pdftoppm` only to rasterise pages for QA), Pillow frame generation piped to ffmpeg for video.
- **Video is generated frame-first.** 1800 frames are drawn to a temp directory and encoded with ffmpeg. This is slower than an ffmpeg filter graph but it is the only way the palette gate can measure the actual pixels the encoder was given rather than a lossy decode.
- **Gates run in-process and are all reported, not short-circuited**, so one run tells the operator every problem instead of the first one.
- **Machine contract matches the incumbent:** `STATUS: OK` / `STATUS: FAILED` on the last line, manifest at `qa/assets/assets-manifest.json`, full log via `Tee-Object`.

## Impacted Modules And Files

| File | Change |
|---|---|
| `scripts/generate_all_assets.py` | New — ~1990-line generator: dossier parsing, fact extraction, 3 infographics, 6-card carousel + PDF, 4-page report, 2 videos, social copy, 11 QA gates |
| `.agents/skills/ls-notebooklm-packager/SKILL.md` | New — source pack anatomy plus six engineered Studio prompts (audio overview, executive briefing, FAQ, 60s video shorts, infographic data table, 4-page report) |
| `.agents/skills/ls-visual-storytelling/SKILL.md` | Platform export matrix; carousel composition rules |
| `.agents/skills/ls-od-image/SKILL.md` | Exact pixel table per platform |
| `.agents/skills/ls-od-video/SKILL.md` | Frame specification (9:16 and 16:9), beat plan, local render fallback path |
| `.agents/skills/ls-document-design/SKILL.md` | 4-page A4 report anatomy |
| `.agents/skills/ls-artifact-qa/SKILL.md` | MP4 QA block (ffprobe dimensions, duration, source-frame palette) |
| `.opencode/commands/generate-all-assets.md` | New — slash command, `!` bash invocation, hard rules, `--skip-video` / `--keep-frames` |
| `scripts/build_campaign.py` | New — `/build-campaign` router: State 1/2 detection, markdown → flow blocks, pagination, unabridged PDF via headless Chrome, LinkedIn post, media branch, palette + integrity gates, audit report |
| `scripts/brand_briefing.py` | New (committed here) — earlier single-artifact generator; supplies PDF print, logo geometry, page count and palette rasterisation to the router |
| `static/brand/templates/briefing-flow.html` | New — shared unabridged flow engine: brand CSS, masthead, metric strip, tables, compact density |
| `static/brand/templates/executive-briefing-4pp.html` | New — thin wrapper, `variant='standard'`, 4-page budget |
| `static/brand/templates/executive-briefing-2pp.html` | New — thin wrapper, `variant='compact'`, 2-page budget |
| `.opencode/commands/build-campaign.md` | New — the one-touch master command and its STATUS contract |
| `build-campaign.bat` | New — Windows one-click launcher, pure ASCII |

Not committed by this change: `artifacts/` (campaign output, and the MP4s exceed `check-added-large-files`). The earlier note deferring `scripts/brand_briefing.py` is superseded — the router imports it, so it is committed.

## Extension Approach — `/build-campaign`

One router over the existing engines rather than a second generator. `scripts/build_campaign.py` inspects `notebooklm/`, parses the briefing into atomic **flow blocks** (heading / paragraph / bullets / table), paginates them, and renders through a single shared template so the 2-page and 4-page variants cannot drift apart.

- **Pagination is capacity-driven, and the render arbitrates.** The line-cost model is an estimate; `build_pdf` walks a `(fill, fit)` ladder — tightest page fill at `fit 1.00` first, and only reaches a smaller type scale once looser fill has been exhausted. A page budget that cannot be met adds a page; nothing is ever dropped.
- **Evidence over assumption.** Page fill, line pitch and per-page capacity were measured from rasterised output rather than estimated; the constants in the scripts reflect those measurements.
- **One template, thin variants.** `briefing-flow.html` holds all brand CSS and layout; the 4-page and 2-page files set only `variant` plus the page budget.

## Interfaces, Data, Permissions

- **Input contract:** `artifacts/campaigns/{slug}/dossier.md` (required) and `artifacts/campaigns/{slug}/notebooklm/source-pack.md` (used when present). No network access, no credentials, no LLM call — the script is deterministic and offline.
- **Output contract:** fixed relative paths under the campaign directory (listed in `spec.md`), plus `qa/assets/assets-manifest.json` and `qa/generate-run.log`.
- **Exit codes:** `0` all gates pass, `1` a gate failed. Callers gate on the final `STATUS:` line.
- **Permissions:** writes only inside `artifacts/campaigns/{slug}/`; no repo files, no git operations.

## Spec Gaps Found From Planning

- The directive named seven assets but the platform matrix implies more (Facebook 1200×628, and the six carousel source pages that the PDF is built from). Resolved by emitting them too — they cost nothing once the layout functions exist, and the command's asset list documents them.
- The directive did not say whether the carousel PDF should be the Instagram or LinkedIn aspect. Resolved as one 1080×1080 PDF (works as a LinkedIn document post) plus the individual square PNGs for Instagram.

## Risks And Mitigations

- **Output drifts from the dossier.** Mitigated by a `grounding` gate that scans the generated copy for claims absent from the sources, and by the rule that filler is verbatim source text.
- **MP4s bloat the repository.** Mitigated by policy, not by `.gitignore` (which would hide them from `git status`): `artifacts/` stays untracked, and `check-added-large-files --maxkb=500` would block a 1.6 MB video anyway.
- **Palette gate produces false confidence on video.** Mitigated by measuring source frames and labelling the decoded number `informational` in the manifest and log.
- **Full run is slow** (3600 PNG frames). Mitigated by `--skip-video` for layout iteration and `--keep-frames` to inspect the exact pixels that were encoded.
- **Layout dead space.** The first carousel pass pooled slack into two voids because a one-sentence card centred its copy. Mitigated by anchoring copy to the top rule (y=200) and pinning the dominant element to the footer (y=966), with ghost outlined numerals filling body cards.

## Verification Plan

1. `uv run ruff check scripts/generate_all_assets.py` — lint.
2. Full pipeline on a real campaign directory, twice end-to-end, asserting the final `STATUS: OK` line.
3. `ffprobe` on both MP4s — dimensions, fps, duration, frame count.
4. `check_brand_palette.py` over all 13 raster/PDF assets at 3.0% tolerance.
5. `pdftoppm` / PyMuPDF page counts and A4 geometry for the report; PyMuPDF text extraction to prove the report body is source text.
6. `pwsh scripts/maintenance/lint-ecl.ps1` and `harness-change.ps1 validate` for this record.
