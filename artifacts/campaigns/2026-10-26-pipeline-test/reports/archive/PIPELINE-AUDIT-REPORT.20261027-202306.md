# Pipeline Audit Report — /build-campaign

**Campaign:** `2026-10-26-pipeline-test`
**Generated:** 27 October 2026 20:01
**Detected state:** TEXT ONLY
**Audio in `notebooklm/`:** none
**Media branch:** skipped — text-only campaign
**Status:** COMPLETE — all gates passed

---

## 1. Input inspection

| Signal | Value |
|--------|-------|
| Source | `notebooklm/raw-briefing.md` |
| Source SHA-256 | `75d75d3160e518b3f9f4e81477887783187d6adfb742000e0097ffa373dbd854` |
| Words | 1,126 |
| Sections / headings | 5 |
| Paragraphs | 16 |
| Bullets | 12 |
| Data tables | 1 (4 rows) |
| Audio files (`*.mp3` / `*.wav`) | 0 |

The state is derived only from files present on disk. No campaign content was
supplied by this report.

---

## 2. Template decision

| Rule | Result |
|------|--------|
| Threshold | > 600 words **or** any data table -> 4-page unabridged |
| Observed | 1,126 words, 1 table(s) |
| Template | `static/brand/templates/executive-briefing-4pp.html` |
| Page budget | 4 |
| Rendered pages | 4 |
| Final type scale | 1.00 (1.00 = full brand scale) |

**Content preservation.** The full source is rendered: every paragraph, bullet,
table row and heading. No sentence was trimmed, condensed or paraphrased. The
only fitting lever is the brand type scale; if content had still overflowed, the
renderer would have added pages rather than drop text.

---

## 3. Assets built

| File | Type | Detail | Size | Palette |
|------|------|--------|------|---------|
| `open-design/executive-briefing-branded.pdf` | PDF | 4 pages, A4, unabridged | 248 KB | PASS |
| `text/linkedin-primary.md` | Copy | 1,824 chars | 2 KB | n/a |

Palette gate: `.agents/skills/ls-visual-storytelling/scripts/check_brand_palette.py` at 3% tolerance.

---

## 4. Skipped assets

| Asset | Reason |
|-------|--------|
| `open-design/video-short-1080x1920.mp4` | no NotebookLM audio (*.mp3 / *.wav) in notebooklm/ — State 1 |
| `open-design/video-overview-16x9.mp4` | no NotebookLM audio (*.mp3 / *.wav) in notebooklm/ — State 1 |
| `open-design/infographic-square-1080x1080.png` | no NotebookLM audio (*.mp3 / *.wav) in notebooklm/ — State 1 |
| `open-design/infographic-landscape-1600x900.png` | no NotebookLM audio (*.mp3 / *.wav) in notebooklm/ — State 1 |
| `text/x-thread.md` | media branch skipped — State 1 |
| `text/facebook-post.md` | media branch skipped — State 1 |
| `text/instagram-caption.md` | media branch skipped — State 1 |

---

## 5. Content-integrity gate

Re-extracted the rendered PDF and matched every source block as a contiguous
token sequence (punctuation-, hyphenation- and line-break-insensitive), so a
silently dropped clause fails the run.

| Metric | Value |
|--------|-------|
| Source blocks checked | 49 |
| Missing blocks | 0 |

None. Every source block was found in the rendered PDF.

---

## 6. Gates

| Gate | Result | Value |
|------|--------|-------|
| page_count | PASS | 4 pages (budget 4) |
| a4 | PASS | [(595.0, 841.9), (595.0, 841.9), (595.0, 841.9), (595.0, 841.9)] |
| title_present | PASS | Scaling Agentic AI Architecture |
| text_integrity | PASS | 49 blocks, 0 missing |
| palette_pdf | PASS | 4 page(s) @ 3% |
| css_colours | PASS | [] |
| linkedin_limit | PASS | 1,538 / 2,800 chars |
| palette_all | PASS | 4 raster(s) @ 3% |
| assets_present | PASS | 2 files |

---

## 7. Reproduce

```bash
uv run python scripts/build_campaign.py artifacts/campaigns/2026-10-26-pipeline-test
```

The same run is available as `/build-campaign` (or its alias
`/generate-all-assets`), and as `build-campaign.bat` on Windows.

---

## 8. Honest notes

- Media assets (State 2) are rendered by the repository's deterministic Pillow
  and ffmpeg generator (`scripts/generate_all_assets.py`), not by the Open
  Design / HyperFrames CLI. The `ls-od-video` and `ls-visual-storytelling`
  skills supply the design rules that the generator implements; no skill CLI was
  executed.
- Video palette is gated on the source PNG frames, which are authoritative.
  H.264 `yuv420p` is lossy, so a decoded frame is measured for information only
  and is not gated.
- Nothing was published. All output is staged in the campaign folder.
