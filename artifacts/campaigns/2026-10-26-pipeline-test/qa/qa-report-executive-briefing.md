# ls-artifact-qa — Executive Briefing (2pp A4)

> **SUPERSEDED — 27 Oct 2026, 19:48.** The 2-page artifact this report audited no
> longer exists on disk: `scripts/build_campaign.py` (`/build-campaign`) rebuilt
> `open-design/executive-briefing.{html,pdf}` as a **4-page unabridged** document
> and destroyed the bytes. The verdict, hashes and gate numbers below describe a
> file that is gone. They are retained only as a record of that artifact.
> Current artifact findings: `review-notes-latest-artifact.md`.


**Artifact:** `open-design/executive-briefing-branded.pdf` (rendered from `open-design/executive-briefing.html`)
**Campaign:** `2026-10-26-pipeline-test`
**Gate:** ls-artifact-qa v1 — Visual / Brand / UX / Accessibility / Content
**Verdict: APPROVE** (one honest caveat on the 300 dpi palette gate, §2.2)

---

## 0. Evidence base

| Source | Command | Result |
|--------|---------|--------|
| Brand verification | `qa/verify_briefing.py` | 5 gates, `VERDICT: PASS` |
| Machine output | `qa/brand-verification.json` | full gate payload |
| Rendered pages | `qa/page-1@300.png`, `qa/page-2@300.png` | PyMuPDF 300 dpi |
| Palette-gate rasters | `qa/pdf-{300,600}dpi-{1,2}.png` | poppler `pdftoppm` |
| HTML probe | `ls-artifact-qa/scripts/visual_check.cjs` | exit 0 |
| Text-layer probe | inline `pymupdf` extraction | 3,890 chars, 0 broken runs |
| Artifact identity | `qa/artifact-hashes.md` | SHA-256 of both files |

**Rasteriser note.** The palette gate is run on poppler output, not PyMuPDF. PyMuPDF
rounds every channel down by up to 1 LSB, turning `#070A40` into `#070940` and failing a
pixel-exact gate for a rasteriser reason rather than an artifact defect. The PDF content
stream itself stores exact token values.

---

## 1. Visual QA — PASS

| Check | Result |
|-------|--------|
| Page count | 2 (no spill page) |
| Page box | 595.0 × 841.9 pt = A4, both pages |
| Page 1 content height | 1103.3 px of 1121.4 px box (18.1 px headroom) |
| Page 2 content height | 1111.3 px of 1121.4 px box (10.1 px headroom) |
| Horizontal overflow | 0 px |
| Clipping | none — `.page` is `overflow: hidden` and content is inside the box on both pages |
| Footer position | pinned to the page bottom via `margin-top: auto` on a flex column, identical on both pages |
| Logo crop | 44 × 39.4 mm window over the artwork bounding box; 9 mm from the top trim to the "L" cap (cap height 8.3 mm, so ≥ 1× clear space) and 14 mm from the left trim |

The masthead metric strip sits on the navy field (cyan numerals at 8.79:1), not on white —
an earlier build let the strip fall outside the navy band, which put cyan on white at
≈1.9:1. That was caught on review and fixed before sign-off.

---

## 2. Brand QA

### 2.1 Palette and identity — PASS

| Gate | Scope | Result |
|------|-------|--------|
| G1 CSS source | every colour declared in `<style>` | **PASS** — 7 declared, 0 off-palette, 0 raw colour keywords |
| G2 PDF content | every `rg`/`RG` operator that actually paints | **PASS** — 0 off-palette |
| G4 edge proof | every off-palette raster pixel classified | **PASS** — **0 foreign colours outside the logo artwork** |

Colours actually painted (G2, operator counts):

| Token | Name | Fill ops |
|-------|------|----------|
| `#070A40` | navy | 25 |
| `#00BFFF` | cyan | 25 |
| `#9CA3AF` | grey-light-text | 12 |
| `#F2F2F2` | grey-light | 10 |
| `#FFFFFF` | white | 7 |
| `#E63946` | red | 3 |
| — | strokes | 0 |

`#000000` appears in the PDF as Chromium's default colour pre-state on 8 segments that
immediately get overridden by an image or fill; G2 classifies it as *declared, unpainted*
and it is not counted as ink.

Palette dominance (share of visible pixels, 300 dpi):

| | navy | grey-light | white | cyan | red | grey-light-text |
|---|---|---|---|---|---|---|
| Page 1 | 34.82 % | 27.50 % | 32.42 % | 0.89 % | 0.01 % | 0.49 % |
| Page 2 | 17.17 % | 9.32 % | 68.37 % | 0.69 % | 0.71 % | 0.32 % |

Red stays under 1 % on both pages — it is a decision gate and a hairline rule, not a
surface. Cyan stays under 1 % — dividers, metric numerals, section rules.

### 2.2 Official palette gate — PASS at 600 dpi, FAIL at 300 dpi

| dpi | Page 1 | Page 2 | Gate |
|-----|--------|--------|------|
| 600 | 97.69 % on-palette (2.31 % off) | 98.30 % on-palette (1.70 % off) | **PASS** |
| 300 | 3.87 % off | 3.42 % off | **FAIL** (tolerance 3 %) |

**This is stated as measured, not massaged.** The 300 dpi failure is text anti-aliasing:
at 300 dpi a 12 pt glyph stem is barely wider than a pixel, so nearly every edge pixel is
a partial blend. G4 proves the blends are legitimate — it walks every off-palette colour on
both pages and finds that **all** of them lie within 8 units of a line between two brand
tokens, and **zero** are foreign. At 600 dpi the anti-aliasing band is physically narrower
relative to the page, and the same document passes.

What is *not* claimed: that the artifact is 100 % on-palette at every resolution. It is
100 % on-palette in the PDF colour operators (G2) and free of foreign colours (G4); the
pixel-share number is resolution-dependent.

### 2.3 Typography and logo — PASS

- Fonts embedded: `Arial-BoldMT`, `ArialMT` only — no fallback substitution.
- Rendered sizes: 12.0 / 13.0 / 14.0 / 16.0 / 18.0 / 24.0 pt — **all on** the brand scale, none off-scale.
- Logo: official `brand/logo/logo-full.png`, 1 logo instance, `alt="LightSpeed Holdings Limited"`, typed `brand-mark`, tagline lockup intact within the artwork.
- Wordmark and tagline appear in the masthead lockup; the footer carries "LightSpeed Holdings Limited™ · Confidential" and "ASPIRE. ACT. ACHIEVE.".

The logo plate is a flat dark tone; `mix-blend-mode: lighten` resolves it onto `#070A40`
so no foreign colour enters the header and the artwork itself is never recoloured
(ADR-027). G4 confirms 1,906 artwork colours on page 1, all inside the sanctioned crop box.

---

## 3. UX QA — PASS

| Check | Result |
|-------|--------|
| Reading hierarchy | masthead → metric strip → Executive Summary → 4 pillars (p1); evidence → commercial callout → regulation → actions → decision gate (p2) |
| Page completeness | each page is self-contained; footer carries page N of 02 on both |
| Destination clarity | the document ends on an explicit decision gate, not a summary — the reader is told what is unverified |
| Scan path | 4 metrics in the header give the whole position in one glance; pillars are numbered and parallel |
| Empty / overflow states | none — no truncated card, no orphaned heading, no hyphenless widow exceeding one line |

---

## 4. Accessibility QA — PASS after two fixes

Contrast, measured on the token values:

| Pair | Ratio | AA normal (4.5) | AA large (3.0) |
|------|-------|-----------------|----------------|
| navy on white | 18.64 : 1 | PASS | PASS |
| white on navy | 18.64 : 1 | PASS | PASS |
| cyan on navy | 8.79 : 1 | PASS | PASS |
| grey-light-text on navy | 7.34 : 1 | PASS | PASS |
| navy on grey-light | 16.65 : 1 | PASS | PASS |
| grey-dark on white | 4.83 : 1 | PASS | PASS |
| red on white | 4.17 : 1 | n/a | PASS (14 pt bold) |

Two failures were found on review and fixed rather than shipped:

1. **Section kickers and footer line** used `#9CA3AF` on white — 2.54 : 1, well under AA.
   Changed to `#6B7280` (4.83 : 1). Both are brand tokens; no new colour was introduced.
2. **Decision-gate label** was 12 pt red — 4.17 : 1, under AA for normal text. Raised to
   14 pt bold, which qualifies as large text (≥ 14 pt bold) where the 3.0 : 1 threshold
   applies. Still on the brand scale.

Structure and semantics:

| Check | Result |
|-------|--------|
| Heading count | 10, **0 empty** |
| Images | 1, **0 missing alt**, 0 untyped, 0 invalid type |
| Logo alt | matches the canonical name, **0 mismatches** |
| Horizontal overflow | **0 px** (reflow-safe at 1280 px viewport) |
| Colour-only meaning | none — every red element also carries a text label; the decision gate is a bordered box *and* a labelled heading |
| Text layer | 3,890 chars extract cleanly; **0** runs of spaced single letters; **0** U+FFFD |

The text-layer check exists because letter-spacing above ~0.1 em makes Chromium insert
real spaces between glyphs, which breaks copy-paste and screen readers
("A S P I R E .  A C T ."). All tracking in the artifact is capped at 0.08 em and the
build verifies extraction, so this cannot regress silently.

---

## 5. Content QA — PASS

Every claim traces to `notebooklm/raw-briefing.md`:

| Claim in artifact | Source line |
|-------------------|-------------|
| 89 AI agents, 20 departments, 1 human CEO | L14, L63 |
| 5-tier HITL, timeouts escalate, never auto-approve | L64 |
| 4-gate CI: ruff / mypy / bandit / pytest | L42–44, L64 |
| Ollama, llama.cpp, quantized GGUF, zero cloud round-trip | L7 |
| Zero-Cloud Boundary, exfiltration eliminated by design | L7 |
| J&S StopOver Bar field validation | L65 |
| Malawi DPA 2024 + National AI Strategy | L46 |
| Mandates: open-weight models / local hosting / air-gapped inference | L46 |
| Pricing mechanics unverified | L56 |
| Payment-rail integration unverified | L57 |
| Unit economics, hardware costs, gateway verification required | L59 |

Consistency and grammar:

- Figures agree across both pages (89 / 20 / 1 / 5 used once each, in the metric strip).
- No claim of revenue, cost, savings or market size appears — the briefing makes none, and the decision gate says so explicitly.
- Currency/emdash typography is consistent; no orphaned hyphens; no duplicated words.
- Confidentiality line is present on both pages.

---

## 6. Caveats and open items

1. **300 dpi palette gate fails at 3.87 % / 3.42 %** (tolerance 3 %) from anti-aliasing. 600 dpi passes. G4 proves zero foreign colours. Reported as-is.
2. **Output-path collision.** `scripts/brand_briefing.py` — a different generator invoked by a concurrent session — writes the same two paths and did so twice during this run (18:26, 18:29). Its output is preserved at `open-design/_collision-backup/`; it scales type by `--fit: 0.86`, which puts rendered sizes off the brand scale and would fail G5. Confirm `qa/artifact-hashes.md` before trusting any gate result.
3. **Not committed.** `artifacts/` and `scripts/brand_briefing.py` are untracked in git.
4. The 300 dpi gate tolerance is a skill default; it is not tuned per artifact here, and no attempt was made to pass it by changing the tolerance.
