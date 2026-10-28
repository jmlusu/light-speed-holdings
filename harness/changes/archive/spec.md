# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: requirement-first (CEO directive listing exact deliverables, pixel sizes and gates)
- Questions asked this round: 0 (sizes, palette and gates were all specified; the only open choice was render engine, resolved in `plan.md`)

## Goal And Evidence

- Real problem or user request: the Creative Production Stack could produce one artifact per run (a deck, a briefing PDF, a diagram). A campaign had no way to turn one verified dossier into the full multimodal set a launch actually needs — vertical video, platform-sized infographics, a carousel, a branded report and social copy — without a human driving five separate skills in five separate sessions.
- Current behavior before this change: `ls-notebooklm-packager` did not exist, so there was no engineered source pack or Studio prompt set. `ls-visual-storytelling`, `ls-od-image`, `ls-od-video` and `ls-document-design` were generic (no pixel matrix, no 9:16 spec, no 4-page A4 spec). `ls-artifact-qa` had no MP4 path. No script assembled a campaign.
- Source of evidence: the six skill files at the pre-change commit, and `scripts/brand_briefing.py` — the existing single-artifact generator whose contract (`STATUS: OK|FAILED`, palette gate, `qa/assets/*.json` evidence) this change reuses rather than reinvents.

## User Scenarios And Success

- Primary user/system scenario: a campaign owner drops a verified `dossier.md` and (optionally) a NotebookLM `source-pack.md` into `artifacts/campaigns/{slug}/`, runs `/generate-all-assets`, and gets the complete campaign set plus a QA manifest. Nothing in the output may introduce a fact that is not in those two files.
- Success criteria: one command produces every listed asset at the specified dimensions; every asset passes the brand palette gate; the QA manifest records a PASS/FAIL per gate; the run exits non-zero and prints `STATUS: FAILED` if any gate fails.
- Acceptance criteria (the seven assets named in the directive):
  1. `video/video-short-1080x1920.mp4` — 9:16, 1080×1920
  2. `video/video-overview-16x9.mp4` — 16:9, 1920×1080
  3. `infographics/infographic-square-1080x1080.png`
  4. `infographics/infographic-landscape-1600x900.png`
  5. `carousels/social-carousel.pdf`
  6. `reports/comprehensive-report-branded.pdf` — 4 pages, A4
  7. `social-copy/threads-and-captions.md`

  Plus the platform variants the skill matrix requires: `infographic-landscape-1200x628.png` (Facebook), `carousels/instagram/card-1..6.png` (carousel source pages).

## Non-Goals

- Generating original narrative or analysis. Every sentence in every asset is either verbatim dossier text or a number extracted from it. Filler is verbatim source text (ghost numerals, pull quotes), never invented copy.
- Paid cloud rendering. Open Design (`OD_BIN`) and HeyGen are not configured in this environment; the local renderer is the supported fallback and is documented as such.
- Voiceover, music or audio mixing. The videos are silent by design (no BGM catalogue is available offline).
- Publishing. This produces files; `ls-social-media-manager` publishes them.
- Adding these assets to git. See `plan.md` "Risks And Mitigations" — campaign output stays in `artifacts/`.

## Constraints

- Brand palette gate is authoritative: Navy `#070A40`, Red `#E63946`, Cyan `#00BFFF` (+ the documented neutrals), enforced by `check_brand_palette.py` at a 3.0% off-palette tolerance.
- Grounding gate: no claim in any asset that cannot be traced to `dossier.md` or `notebooklm/source-pack.md`.
- `main` is protected (6 required checks); work lands via PR.
- Available toolchain: ffmpeg, Pillow, PyMuPDF, Jinja2, python-pptx, Chrome, MiKTeX `pdftoppm`. **Not** available: Python Playwright, reportlab, Open Design daemon.
- `check-added-large-files --maxkb=500` in pre-commit — 1.6 MB MP4s cannot be committed.

## Assumptions

- The dossier is the fact ceiling. A campaign with a thin dossier produces a thin asset set rather than a padded one.
- A 60-second runtime at 30 fps (1800 frames) is the right length for both cuts; the beat plan was sized to fill it exactly rather than leaving trailing dead time.
- `pdftoppm` anti-aliasing must be off (`-aa no`) for palette measurement to be meaningful on rasterised vector text.

## Open Questions

- None remaining. (The one open question — local renderer vs. Open Design paid render — is resolved in `plan.md` under "Technical Approach".)

## Resolved Clarifications

- **Which render engine?** Local deterministic renderer (Pillow + ffmpeg), because `OD_BIN` is unset and the OD daemon is not running in this environment. Recorded in `plan.md`; the OD path remains documented in `ls-od-video` as the preferred route when a daemon is available.
- **What tolerance for the palette gate?** 3.0 percent, not 0.03. Cards measured 0.2–0.3% off-palette (legitimate antialiasing); the default had to exceed that to be usable while still failing a genuinely off-brand asset (a non-brand asset measures in the tens of percent).
- **Is a decoded video frame a valid palette test?** No. H.264 `yuv420p` is lossy, so decoded frames measure ~98–99% "off palette" while the source frames measure 99.9%+ on-palette. Video is therefore gated on source frames; the decoded-frame number is recorded as informational only.
