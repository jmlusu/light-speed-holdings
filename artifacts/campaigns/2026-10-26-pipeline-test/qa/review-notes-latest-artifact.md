# Review notes — current artifact (4-page `/build-campaign` output)

**Artifact:** `open-design/executive-briefing-branded.pdf`
**Producer:** `scripts/build_campaign.py` (`/build-campaign`) — rebuilt 27 Oct 2026 19:48
**Template:** `static/brand/templates/executive-briefing-4pp.html` → `briefing-flow.html`
**Pages:** 4 · 10,659 chars of extractable text
**Its own audit:** `PIPELINE-AUDIT-REPORT.md` — all 8 gates PASS

This note does not overturn that audit. It records three defects found on review that
the pipeline's gates do not test for.

---

## 1. Text layer is broken (tagline and date) — **real, affects accessibility**

The pipeline's gates check page count, A4 box, title presence, content integrity,
palette and asset presence. None of them read the PDF text layer back as a human
would copy it.

Measured with `pymupdf` text extraction on the delivered PDF:

| Metric | Value |
|--------|-------|
| Runs of space-separated single letters/digits | **9** |
| Examples | `A S P I R E `, `A C H I E V E `, `2 0 2 6` |

Effect: copying "ASPIRE. ACT. ACHIEVE." out of the footer yields the letters split
apart, and a screen reader reads it as individual characters. The brand tagline is
the one line in the document most likely to be copied.

Cause: letter-spacing above ~0.1 em makes Chromium emit real spaces between glyphs.
The eyebrow and footer tagline in `briefing-flow.html` are above that threshold.

Fix: cap tracking at `0.08em` and re-render. Two CSS values, no layout risk.
(An earlier 2-page build in this campaign had the same defect and was fixed exactly
this way; the pipeline template carries the older values.)

## 2. Machine text on the cover

The masthead subtitle reads:

> `Unabridged edition · 1,126 words · 5 sections · 1 data table(s)`

- `1 data table(s)` is an unrendered pluralisation placeholder.
- `Unabridged edition · 1,126 words` is pipeline metadata, not reader-facing
  information. A client briefing does not need to state its own word count.

Fix: drop the word/section counts from the cover, or move them to the audit report;
render `1 data table` correctly.

## 3. Page 1 ends with ~200 px of dead space

Section 1 finishes two-thirds down page 1 and the rest of the page is blank, because
the flow engine breaks at section boundaries. Nothing is truncated — but the page
looks unfinished, and it is the cover page.

Fix: allow the next section to start on page 1, or balance section lengths.

---

## What is *correct* in this artifact

- 4 pages A4, palette gate PASS at 3% on all four rasters (this is a genuine
  improvement over the 2-page build, which failed the same gate at 300 dpi).
- Type scale 1.00 — no off-scale sizes, unlike the `--fit: 0.86` shrink in
  `scripts/brand_briefing.py`.
- Content integrity: 49/49 source blocks present, 0 missing. Nothing trimmed.
- Metric strip sits on navy with cyan numerals — contrast is fine.
- Footer tagline is correctly uppercase in the *rendering* (the defect in §1 is in
  the text layer, not the visual).
