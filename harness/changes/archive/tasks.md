# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation. The only high-impact question (render engine) resolved in `spec.md` "Resolved Clarifications"; review recorded in `reviews/review.md`.
- [x] T002 Fix the palette-gate contract before writing assets: confirm `check_brand_palette.py` exits 0/1/2 and that 3.0% is the default tolerance, so a generator run can gate on it directly.

## Implementation

### A. Source pack (`ls-notebooklm-packager`)

- [x] T010 [P] [US1] Create `.agents/skills/ls-notebooklm-packager/SKILL.md` — source-pack anatomy and six Studio prompts: Audio Overview, Executive Briefing, Institutional FAQ, 60-second Video Shorts (Reels/TikTok beats), Infographic Data Extraction Table, 4-page Comprehensive Executive Report.
- [x] T011 [P] [US1] State the facts-only rule in the skill: a prompt may not add a claim that is absent from the dossier; every extracted number must carry its source line.

### B. Platform specifications

- [x] T020 [P] [US1] `.agents/skills/ls-visual-storytelling/SKILL.md` — export matrix: X 1600×900, Facebook 1200×628, Instagram 1080×1080; carousel delivered as a LinkedIn PDF plus Instagram square PNGs.
- [x] T021 [P] [US1] `.agents/skills/ls-od-image/SKILL.md` — exact pixel table per platform, replacing the generic size advice.
- [x] T022 [P] [US1] `.agents/skills/ls-od-video/SKILL.md` — frame specification for 9:16 (1080×1920, animated cyan soundwave, navy backdrop, red accent, dynamic subtitle track) and 16:9 (1920×1080); beat plan; documented local-render fallback when no Open Design daemon is reachable.
- [x] T023 [P] [US1] `.agents/skills/ls-document-design/SKILL.md` — 4-page A4 branded report anatomy (cover, thesis/provenance, evidence, positions/next).
- [x] T024 [P] [US1] `.agents/skills/ls-artifact-qa/SKILL.md` — MP4 QA block: `ffprobe` dimensions, fps, duration, frame count, and source-frame palette measurement with the decoded-frame caveat.

### C. Generator (`scripts/generate_all_assets.py`)

- [x] T030 [US2] Dossier + source-pack parsing, fact extraction, and `scope_of()` returning the source *line* for each number.
- [x] T031 [US2] Three infographics at 1600×900, 1200×628 and 1080×1080 from the same fact set.
- [x] T032 [US2] Six-card carousel: cover + 3 pillars + 1 proof + CTA, written as 1080×1080 PNGs and assembled into `social-carousel.pdf`.
- [x] T033 [US2] 4-page A4 report: Jinja2 HTML → headless Chrome → PDF, navy section bands, red-rail pull quotes, pinned `.src` provenance rail, top-aligned body flow.
- [x] T034 [US2] Two 60-second videos: 1800 frames each at 30 fps drawn with Pillow and encoded with ffmpeg; subtitle track capped at 42 characters per line.
- [x] T035 [US2] `social-copy/threads-and-captions.md`: one X thread plus per-platform captions, `LightSpeed Holdings Limited™` on first mention, character counts printed and gated.
- [x] T036 [US3] Eleven QA gates (grounding, carousel_pages, report_pages, report_a4, report_text, report_rasteriser, video_dims ×2, x_posts, assets_present, palette) and a `qa/assets/assets-manifest.json` written every run.
- [x] T037 [US3] `--skip-video` and `--keep-frames` flags; stale `card-*.png` purged before write so a shorter carousel cannot leave orphan cards behind.
- [x] T038 [US3] Create `.opencode/commands/generate-all-assets.md` — `!` bash invocation, STATUS contract, hard rules, flag usage.

### D. Defect fixes found during validation

- [x] T040 Carousel dead space: copy anchored to the top rule (y=200), dominant element pinned to the footer (y=966); body cards carry ghost outlined numerals because a centred one-sentence block always pooled slack into two voids.
- [x] T041 Report duplication: architecture and positions sections deduped via the `matching()` helper so the same sentence could not appear twice.
- [x] T042 Invented copy removed: the "decision gate at day 90" line had no source; replaced with the dossier's own "integration seams rather than rip-and-replace". Added a `provenance` field rendered as "Traceability" on page 2.
- [x] T043 Social-copy acronym damage: `.title()` produced `Offline-First Agentic Ai`; replaced with an explicit `decap()` and a capitalisation map. Removed a duplicated "Full thread" block.
- [x] T044 Governance beat restored after it was lost to trimming: `take(body, 400)` instead of 150 so "timeouts escalate…" survives, and `sentence_with()` extracts the timeout sentence for both the video beat and an X post.

### E. `/build-campaign` router

- [x] T060 [US2] `scripts/build_campaign.py` — campaign resolution, State 1 / State 2 detection from files on disk, markdown → atomic flow blocks with line-cost estimates.
- [x] T061 [US2] Unabridged PDF: shared `briefing-flow.html` engine plus thin 4-page / 2-page wrappers, Jinja2 → headless Chrome → A4, masthead, metric strip, tables, running heads, footers.
- [x] T062 [US2] `text_integrity` gate — re-extract the rendered PDF and match every source block as a contiguous token sequence so a dropped clause fails the run.
- [x] T063 [US2] `text/linkedin-primary.md` generation with the 2,800-character limit gated.
- [x] T064 [US3] Media branch (State 2 only): reuse `generate_all_assets.py` renderers for both MP4s, both infographics and the three platform copy files; `--skip-video` and `--force-media` escape hatches.
- [x] T065 [US3] `PIPELINE-AUDIT-REPORT.md` — input inspection, template decision, assets built and skipped, integrity result, gate table, reproduce command, honest notes.
- [x] T066 [US3] Register `/build-campaign`, exact alias `/generate-all-assets`, and `build-campaign.bat`.

### F. Defect fixes found by validating the router

- [x] T070 Proportional pagination left page 1 of the 2-page route at 45% fill (visible void): replaced with capacity-driven fill; measured 80% after the fix.
- [x] T071 Line-cost model assumed 96 characters per line against the template's real ~112, and page capacity was under-set: recalibrated from measured renders.
- [x] T072 Orphaned section heading at a page foot after tightening fill: keep-with-next rule carries the heading to the next page.
- [x] T073 Tight fill pushed the 4-page campaign to `fit 0.92`: `(fill, fit)` probe ladder relaxes page fill at `fit 1.00` before shrinking type.
- [x] T074 Square infographic labels overflowed their cards: label now shrinks to card width.
- [x] T075 Stray `>` blockquote markers reached the PDF: stripped at parse time.
- [x] T076 `build-campaign.bat` carried 456 non-ASCII bytes that cmd.exe garbles: rewritten pure ASCII and verified by running it.

## Validation

- [x] T050 `uv run ruff check scripts/generate_all_assets.py` → `All checks passed!`
- [x] T051 Full pipeline run on `artifacts/campaigns/2026-10-26-pipeline-test` → final line `STATUS: OK`; run twice end-to-end.
- [x] T052 `ffprobe` — short: 1080×1920, 30 fps, 60.000 s, 1800 frames, 1.61 MB. Overview: 1920×1080, 30 fps, 60.000 s, 1800 frames, 1.68 MB.
- [x] T053 Palette gate → PASS on 13 files at 3% tolerance; source frames 99.93% (short) and 99.97% (overview) on-brand.
- [x] T054 Report geometry → 4 pages, each 595×842 pt (A4), rasterised with `pdftoppm -aa no`; text extraction returns 3926 characters of source prose.
- [x] T055 Carousel → `carousel_pages PASS (6)`; `social-carousel.pdf` 6 pages; 6 Instagram PNGs present, no orphaned `card-*.png`.
- [x] T056 Social copy → `x_posts PASS ([105, 159, 94])`, all under 280.
- [x] T057 `assets_present PASS (14 files)` — the 7 required assets plus the 3 platform variants and 4 QA artifacts.
- [x] T058 `pwsh scripts/maintenance/lint-ecl.ps1` and `pwsh scripts/maintenance/harness-change.ps1 validate` on this record.
- [x] T080 Real campaign via `/build-campaign` → `STATUS: OK`; 4 pages at fit 1.00; 49 blocks checked, 0 missing; 9/9 gates PASS.
- [x] T081 Page fill measured from the rendered PDF → 82 / 78 / 79 / 100 %.
- [x] T082 State 2 fixture (briefing + wav) → both MP4s present; `ffprobe` 1080×1920 and 1920×1080, h264, 30 fps, 60.000 s; both infographics; three copy files; all gates PASS.
- [x] T083 ≤600-word route on a 430-word fixture → `executive-briefing-2pp.html`, 2 pages, fit 1.00, 13 blocks / 0 missing, `STATUS: OK`.
- [x] T084 `uv run ruff check scripts/build_campaign.py scripts/generate_all_assets.py` → `All checks passed!`
- [x] T085 `build-campaign.bat 2026-10-26-pipeline-test` executed → exit 0, `STATUS: OK`.

## Deferred Tasks

- **Open Design path not exercised.** `OD_BIN` is unset and the daemon is not running, so every asset came from the local renderer. The OD route is documented in `ls-od-video` but has not been run against this generator. Revisit when a daemon is available.
- **Audio.** Both videos are silent. No BGM or SFX catalogue is reachable offline; adding a music bed and a voiceover is a separate change.
- **`scripts/brand_briefing.py` and `.opencode/commands/brand-briefing.md`** — `brand_briefing.py` is now committed because the router imports it; the standalone `brand-briefing.md` command remains out of scope.
- **`artifacts/` is not committed.** Campaign output (including 1.6 MB MP4s) stays untracked by policy and by `check-added-large-files --maxkb=500`.
