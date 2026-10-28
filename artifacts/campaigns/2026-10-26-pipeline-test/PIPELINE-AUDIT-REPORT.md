# Pipeline Audit Report — /build-campaign

**Campaign:** `2026-10-26-pipeline-test`
**Generated:** 28 October 2026 10:27
**Detected state:** State 1 (Text only - fallback)
**Audio in `notebooklm/`:** 0 file(s)
**Status:** FAILED — see gates

---

## 1. Input inspection

| Signal | Value |
|--------|-------|
| Source | `None` |
| Words | 0 |
| Sections / headings | 0 |
| Paragraphs | 1 |
| Bullets | 0 |
| Data tables | 0 (0 rows) |
| Audio files | 0 |

The state is derived only from files present on disk.

---

## 2. Template decision

| Rule | Result |
|------|--------|
| Threshold | > 600 words or any data table -> dynamic template |
| Observed | 0 words, 0 table(s) |
| Template | `static/brand/templates/executive-briefing-dynamic.html` |
| Page budget | 2 |
| Rendered pages | 1 |

Content preserved in full.

---

## 3. Assets built

| File | Type | Detail | Size | Palette |
|------|------|--------|------|---------|
| `a4` | PASS | [(595.0, 841.9)] || `page_count` | PASS | 1 pages (budget 2) || `text_integrity` | FAIL | 2 blocks, 2 missing || `title_present` | PASS | Pipeline Verification |

---

## 4. Skipped assets

| Asset | Reason |
|-------|--------|
| `skipped_facebook-post.md` | skipped — State 1 |
| `skipped_infographic-landscape-1600x900.png` | skipped — State 1 |
| `skipped_infographic-square-1080x1080.png` | skipped — State 1 |
| `skipped_instagram-caption.md` | skipped — State 1 |
| `skipped_video-overview-16x9.mp4` | skipped — State 1 |
| `skipped_video-short-1080x1920.mp4` | skipped — State 1 |
| `skipped_x-thread.md` | skipped — State 1 |

---

## 5. Content-integrity gate

| Metric | Value |
|--------|-------|
| Source blocks checked | 2 |
| Missing blocks | 2 |

- `Pipeline build verification running on LightSpeed Holdings campaign infrastructure.`
- `No source briefing was available for this run.`

---

## 6. Gates

| Gate | Result | Value |
|------|--------|-------|
| a4 | PASS | [(595.0, 841.9)] |
| page_count | PASS | 1 pages (budget 2) |
| text_integrity | FAIL | 2 blocks, 2 missing |
| title_present | PASS | Pipeline Verification |

---

## 7. Reproduce

```bash
uv run python scripts/build_campaign.py 2026-10-26-pipeline-test
```

The same run is available as `/build-campaign` (or its alias `/generate-all-assets`), and as `build-campaign.bat` on Windows.

---

## 8. Honest notes

- GAP 1: PDF rendering via Chromium print-to-PDF with integrity verification.
- GAP 3: Social copy derived from briefing verbatim sentences, not paraphrased.
- Media assets (State 2) rendered by Pillow/ffmpeg generator.
- Nothing published. All output staged in campaign folder.
