---
title: "multimodal asset factory"
slug: "multimodal-asset-factory"
status: "in_progress"
location: "active"
phase: "validate"
intake_status: "completed"
spec_review: "approved"
plan_review: "approved"
modules: [".agents/skills", ".opencode/commands", "scripts", "static/brand/templates"]
files: [".agents/skills/ls-notebooklm-packager/SKILL.md", ".agents/skills/ls-visual-storytelling/SKILL.md", ".agents/skills/ls-od-image/SKILL.md", ".agents/skills/ls-od-video/SKILL.md", ".agents/skills/ls-document-design/SKILL.md", ".agents/skills/ls-artifact-qa/SKILL.md", "scripts/generate_all_assets.py", "scripts/build_campaign.py", "scripts/brand_briefing.py", "static/brand/templates/briefing-flow.html", "static/brand/templates/executive-briefing-4pp.html", "static/brand/templates/executive-briefing-2pp.html", ".opencode/commands/build-campaign.md", ".opencode/commands/generate-all-assets.md", "build-campaign.bat"]
tags: ["creative-production", "multimodal", "assets", "brand-palette", "grounding", "video", "carousel", "report", "skills", "harness"]
validation_status: "pass"
created_at: "2026-10-27"
updated_at: "2026-10-27"
session_id: "8a5b9c31-6d47-4f0e-9b2a-2f0c5f1e7a34"
owner_agent: "jmlus"
claimed_at: "2026-10-27"
---

# Summary

## Outcome

A campaign can now go from one verified dossier to the full multimodal launch set in a single command. `/generate-all-assets` produced **14 assets** on `artifacts/campaigns/2026-10-26-pipeline-test`, with all 11 QA gates passing and `STATUS: OK`.

| Deliverable | Result |
|---|---|
| `video/video-short-1080x1920.mp4` | 1080×1920, 30 fps, 60.000 s, 1800 frames, 1.61 MB |
| `video/video-overview-16x9.mp4` | 1920×1080, 30 fps, 60.000 s, 1800 frames, 1.68 MB |
| `infographics/infographic-square-1080x1080.png` | Instagram |
| `infographics/infographic-landscape-1600x900.png` | X |
| `infographics/infographic-landscape-1200x628.png` | Facebook (added — required by the platform matrix, not named in the directive) |
| `carousels/social-carousel.pdf` | 6 pages |
| `carousels/instagram/card-1..6.png` | 6 square pages, no orphans |
| `reports/comprehensive-report-branded.pdf` | 4 pages, each 595×842 pt (A4), 3926 chars of source text |
| `social-copy/threads-and-captions.md` | X posts at 105 / 159 / 94 chars |

Skills updated: `ls-notebooklm-packager` (new — source pack + six Studio prompts), `ls-visual-storytelling` (platform export matrix), `ls-od-image` (pixel table), `ls-od-video` (9:16 and 16:9 frame specs + local render fallback), `ls-document-design` (4-page A4 anatomy), `ls-artifact-qa` (MP4 QA block).

## Decisions

- **Local deterministic renderer, not Open Design.** `OD_BIN` is unset and no daemon is running, so the whole set was produced with Pillow + ffmpeg + headless Chrome. The OD route stays documented in `ls-od-video` as the preferred path when a daemon exists. This is a fallback that was actually exercised, not a claim that OD works.
- **3.0% palette tolerance, not 0.03.** Legitimate antialiasing put cards 0.2–0.3% off-palette; a genuinely off-brand asset lands in the tens of percent. 3.0 separates the two.
- **Video is gated on source frames, never on a decoded frame.** H.264 `yuv420p` is lossy: decoded frames measure ~98.6% off-palette while the same source frames measure 99.93% on-palette. Gating the decode would have failed a correctly rendered video; gating the source is the only honest measurement of what was rendered. The decoded number is recorded and labelled informational.
- **Every sentence is sourced.** Layout filler is verbatim dossier text — ghost outlined numerals from the source's own counts, red-rail pull quotes lifted from real sentences. One invented line ("decision gate at day 90") was found in review and replaced with the dossier's actual phrasing.
- **`scope_of()` returns the source line, not a character window.** The window version cut mid-word and leaked `### 2.` headings into the report's provenance column.
- **Copy anchored to the top rule, dominant element pinned to the footer.** A one-sentence card centred vertically pools its slack into two voids; anchoring both ends removed the dead space without padding the copy.

## Validation

| Check | Result |
|---|---|
| `uv run ruff check scripts/generate_all_assets.py` | `All checks passed!` |
| Full pipeline, run twice end-to-end | final line `STATUS: OK`, 14 assets |
| `ffprobe` on both MP4s | 1080×1920 / 1920×1080, 30 fps, 60.000 s, 1800 frames each |
| Palette gate (`check_brand_palette.py`, 3% tolerance) | PASS, 13 files; source frames 99.93% / 99.97% on-brand |
| Report geometry | 4 pages at 595×842 pt; rasterised with `pdftoppm -aa no`; 3926 chars extracted |
| Carousel | `carousel_pages PASS (6)`; 6 PDF pages; 6 PNGs, stale cards purged |
| Social copy | `x_posts PASS ([105, 159, 94])`, all under 280 |
| Asset inventory | `assets_present PASS (14 files)` |
| Grounding | `grounding PASS (no ungrounded claims)` |

Evidence: `artifacts/campaigns/2026-10-26-pipeline-test/qa/assets/assets-manifest.json` and `qa/generate-run.log`. A negative control was observed in the same run — the decoded video frame measurement fails at 3% tolerance — confirming the palette gate is not a no-op.

Not verified and not claimed: the Open Design render path, audio (both videos are silent), and independent human visual sign-off.

## Extension — `/build-campaign` master command

The factory was reachable only through `generate_all_assets.py`, which requires a
`dossier.md` and knows nothing about NotebookLM audio. Added a **router** on top:
`/build-campaign` (exact alias `/generate-all-assets`) inspects
`artifacts/campaigns/{slug}/notebooklm/`, picks State 1 (briefing only) or State 2
(briefing + `*.mp3`/`*.wav`), and always emits an unabridged branded PDF plus the
LinkedIn post; State 2 adds both MP4s, both infographics and three copy files.

| Deliverable (real campaign, State 1) | Result |
|---|---|
| `open-design/executive-briefing-branded.pdf` | 4 pages A4, type scale 1.00 (never shrunk), 248 KB |
| `text/linkedin-primary.md` | 1,538 / 2,800 chars |
| `text_integrity` | 49 blocks checked, 0 missing |
| Gates | 9 / 9 PASS, `STATUS: OK` |

State 2 was verified on a throwaway fixture (both MP4s measured with `ffprobe`,
both infographics, three copy files, all gates PASS) and the ≤600-word route on a
430-word fixture (2 pages, 13 blocks, 0 missing). The real campaign stays State 1
because it carries no NotebookLM audio.

### Content-preservation contract

Always >600 words **or** any data table → 4-page template; otherwise 2-page. The
only fitting lever is the brand type scale (`fit`), floored at 0.72; if content
still overflows, the renderer **adds a page** rather than dropping text.
`text_integrity` re-extracts the rendered PDF and matches every source block as a
contiguous token sequence, so a silently dropped clause fails the run.

### Defects found during validation

- Pagination spread blocks *proportionally* across the page budget, so each page
  filled to only `total_cost/total_capacity` of its height: the 2-page route
  rendered page 1 at **45% fill** with a visible void. Replaced with
  capacity-driven fill; page 1 now fills 80%, matching the 4-page route.
- The line-cost model assumed 96 characters per line against the template's real
  ~112, and page capacity was under-set. Both recalibrated against measured
  renders.
- Once fill tightened, a section heading was stranded at a page foot (orphan);
  added a keep-with-next rule that carries the heading forward.
- Tight fill pushed the 4-page campaign to `fit 0.92`, shrinking the brand type
  scale. `build_pdf` now walks a `(fill, fit)` ladder: page fill is relaxed at
  `fit 1.00` before type size is ever reduced.
- Square infographic labels overflowed their cards; `render_infographic` now
  shrinks the label to the card width.
- Stray `>` blockquote markers reached the PDF; stripped at parse time.
- The Windows launcher carried 456 non-ASCII bytes (box-drawing, ™) that cmd.exe
  renders as mojibake; rewritten in pure ASCII and verified by execution.

### Validation (this extension)

| Check | Result |
|---|---|
| Real campaign | 4 pages, fit 1.00, 49 blocks / 0 missing, 9/9 gates, `STATUS: OK` |
| Page fill, measured from the PDF | 82 / 78 / 79 / 100 % |
| State 2 fixture, `ffprobe` | 1080×1920 and 1920×1080, h264, 30 fps, 60.000 s |
| 2-page route (430 words) | 2 pages, fit 1.00, 13 blocks / 0 missing, `STATUS: OK` |
| `uv run ruff check scripts/build_campaign.py` | `All checks passed!` |
| `uv run mypy scripts/build_campaign.py` | 0 errors in this file; `scripts/` is excluded from the mypy config and CI gates `src/` only |
| `build-campaign.bat` executed | exit 0, `STATUS: OK` |

Not verified and not claimed: the Open Design / HyperFrames CLI path (State 2
media are deterministic Pillow + ffmpeg renders), any audio mix, and human visual
sign-off.

## Next Step

- Commit the six skill files, the generator and the command; open a PR (`main` is protected, 6 required checks). `artifacts/` and the pre-existing untracked `scripts/brand_briefing.py` + `.opencode/commands/brand-briefing.md` stay out of the commit.
- Second commit on the same branch carries the `/build-campaign` router, the three templates, `scripts/build_campaign.py`, `scripts/brand_briefing.py` (now a dependency, so it is committed rather than deferred) and `build-campaign.bat`.
