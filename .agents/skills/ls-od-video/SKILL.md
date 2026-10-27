---
name: ls-od-video
description: "Produce HyperFrames-first motion graphics and short video with Open Design, from scaffold through render and QA. Trigger on: 'od video', 'hyperframes od', 'open design video', 'render motion graphics', 'od media scaffold'."
---

# Open Design Video

Produce motion graphics and short video through Open Design, with HyperFrames
as the default engine. HyperFrames keeps the composition as HTML, animates it
with GSAP, and renders frame-accurately in a headless browser. The daemon owns
the render; you own the composition and the review.

## When To Use

- Title cards, lower thirds, product reveals, motion posters, short social
  clips, animated data frames, and looping background panels.
- Any brief where motion is driven by HTML, CSS, or GSAP and must be
  deterministic at a fixed duration.
- Deliverables that need exact text, brand colors, and frame-accurate timing
  rather than generated footage.

Use `ls-od-image` for stills and `ls-artifact-qa` before delivery.

## HyperFrames First

The `hyperframes` design template is the primary path.

- HTML is the source of truth. The composition lives in `index.html` inside a
  cache folder, not in the project root.
- Prefer the scaffold path. `od media scaffold` creates `hyperframes.json`,
  `meta.json`, and `index.html` without running a global install.
- Keep the composition under `.hyperframes-cache/<id>/`; the leading dot keeps
  it out of the file viewer. Only the finished `.mp4` belongs in the project
  root.
- Do not run `hyperframes render` yourself; the daemon owns rendering through
  a Chrome-bound subprocess.
- Read the project metadata before authoring: `videoModel`, `videoLength`, and
  `videoAspect` are locked and are not yours to override.

Fallbacks, only when they fit better than HyperFrames:

- `video-shortform` — a single shot of 10 seconds or less. Note that
  `hyperframes-html` is a local HTML-to-MP4 renderer, not photoreal
  text-to-video. Treat the brief as a motion card or title frame and ask at
  most one clarifying question.
- `motion-frames` — one full-bleed looping CSS frame for a 16:9 hero. No
  timeline, no scene changes.
- `sprite-animation` — a pixel-art explainer with looping CSS keyframes and no
  JavaScript.

Author multi-composition timelines, audio-reactive overlays, or TTS captions
from scratch only when the human explicitly asked for them.

## Frame Specifications

Two delivery formats. Author each as its own composition — a 16:9 timeline
stretched into 9:16 fails the safe-area rule and the type scale at once.

### 9:16 Vertical — Video Shorts (Reels / TikTok)

- **Canvas:** `1080 × 1920`, 30 fps, 60 s max (Reels/TikTok cut at 60 s; a
  60-second short is the target, 15 s is the floor).
- **Backdrop:** Navy `#070A40`, full bleed, ~80% of the frame.
- **Soundwave:** animated Cyan `#00BFFF` waveform, the single motion element.
  Keep it in the lower third behind the subtitle band, amplitude driven by the
  narration envelope, never a static decoration. Cyan is instrumentation here,
  so it stays a stroke — never a large fill.
- **Accent:** Red `#E63946` for the one argued number and the CTA chevron only.
  One red element per scene.
- **Subtitle track:** burn-in readiness requires a separate, deterministic
  track — one line at a time, ≤42 characters, ≤2 lines on screen, max 3 s per
  card. Position the band in the **lower-middle** third: a 9:16 frame loses
  ~15% to UI chrome at the bottom and ~12% to the caption rail at the top, so
  the safe band is roughly y = 1150–1620 at 1080×1920.
- **Safe margins:** ≥96px left/right, ≥250px top, ≥300px bottom. Nothing
  load-bearing outside it.
- **Cyan-on-dark caution:** white body text on navy; cyan for the waveform and
  eyebrows only. Never white on cyan.

### 16:9 Landscape — LinkedIn / YouTube overview

- **Canvas:** `1920 × 1080`, 30 fps, 60–120 s.
- **Backdrop:** Navy `#070A40` with the navy left rail (4px at web scale,
  scaled to ~6px at 1920).
- **Type:** title 28pt, subtitle 16pt, body 14pt, eyebrow/footer 8pt (house
  style). Headlines 60px+ at 1920×1080.
- **Subtitle band:** lower third, same ≤42-character line discipline; YouTube
  and LinkedIn both render their own closed captions, so keep the burn-in band
  clear of the platform's control bar (bottom ~10%).
- **Safe margins:** ≥96px all edges.

### Subtitle discipline (both formats)

- The script comes from the NotebookLM prompt 4 beat table. A subtitle is a
  **compression of a line that exists in the pack**, never a new claim.
- One line, one breath. If a line breaks mid-phrase it reads as a glitch.
- No subtitle without a spoken line behind it, and no spoken line without a
  subtitle — the two tracks are the same content.
- Figures in a subtitle carry their scope (`90 agents` not `90`).

## Commands

```bash
COMP_REL=".hyperframes-cache/$(date +%s)-<slug>"

"$OD_NODE_BIN" "$OD_BIN" media scaffold \
  --project "$OD_PROJECT_ID" \
  --composition-dir "$COMP_REL"

"$OD_NODE_BIN" "$OD_BIN" media generate \
  --project "$OD_PROJECT_ID" \
  --surface video \
  --model hyperframes-html \
  --composition-dir "$COMP_REL" \
  --output "<descriptive-name>.mp4"

"$OD_NODE_BIN" "$OD_BIN" media wait "<taskId>" --since "<nextSince>"
```

- `--composition-dir` must be new and live directly under
  `.hyperframes-cache`. The scaffold refuses existing paths.
- `--project` is required on scaffold unless `OD_PROJECT_ID` is set.
- `media generate` returns one JSON line. On a fast finish it contains the
  file; on a slow finish it contains `taskId` and `nextSince` with exit code 0.
- `media wait` exits 0 when done, 2 when still running, 5 on failure. Poll
  again with the new `nextSince` after a 2; stop and report on a 5.
- Add `--json` to scaffold when a machine-readable result is needed.
- The examples are POSIX shell. On PowerShell use
  `& $env:OD_NODE_BIN $env:OD_BIN media scaffold ...` and supply a manual
  timestamp for the cache slug.

Before dispatch, check the composition structure: the root duration is set,
the palette is declared, and text sits inside the frame's safe area.

## Local Render Path (no daemon)

When the Open Design daemon is not running (`OD_BIN` unset) or a paid render is
not approved, HyperFrames is unavailable but the frame discipline still applies.
Render deterministically with Pillow frames + ffmpeg, which is already installed:

```bash
uv run python scripts/generate_all_assets.py --campaign artifacts/campaigns/<slug>
```

That script composes each frame from exact brand-token hexes with text
anti-aliasing disabled, so every visible pixel is on-palette, then encodes with
ffmpeg. Use it for brand-critical shorts and overviews; use HyperFrames when the
brief needs GSAP choreography or audio-reactive motion.

Two ffmpeg facts that decide whether the output survives QA:

- **`-pix_fmt yuv420p` is required for platform playback** (Reels, TikTok, X,
  YouTube all reject 4:4:4). It is also lossy: decoded frames will not be
  bit-exact to the source palette, so **run the palette gate on the source
  frames, not on decoded video.** State which one you measured.
- **`-movflags +faststart`** moves the moov atom to the front so the file starts
  playing before it finishes downloading.

## House Style

Motion defaults come from
`open-design/design-templates/hyperframes/house-style.md`:

- Entrances run 0.3–0.6 seconds with varied easing; avoid one uniform fade.
- Overlap entries instead of sequencing every element.
- Keep ambient background decoratives moving slowly; they give the frame life
  without competing with the message.
- Headlines sit at 700–900 weight and 60px or larger at 1920×1080; body text at
  300–400 weight and 20px or larger.

The file's `## LightSpeed Holdings` section overrides the generic defaults,
including the cyan-on-dark and pure-white cautions:

- Navy `#070A40` carries about 80% of the composition. Red `#E63946` is the
  action color at about 10%. Cyan `#00BFFF` is instrumentation at about 10%.
- Light surfaces use Morning Mist `#F7F8F9`; nested dark panels use Deep
  Mineral `#121518`. No other hues, gradients, glow, or pure `#000`.
- Arial, with Helvetica as fallback, is the only typeface. Display weights are
  700–900 with 1.1 leading and −0.02em tracking; body is 400–500. In 16:9,
  title 28pt, subtitle 16pt, body 14pt, eyebrow/footer 8pt.
- Motion is 120–240ms for UI and 400–600ms for reveals with
  `cubic-bezier(0.2, 0, 0, 1)`. Use opacity and 8–16px rises only; no bounce,
  parallax, letter-by-letter headlines, shimmer, or glitch. Honor
  `prefers-reduced-motion`.
- Use a navy left rail (4px web, 0.15in slide), a left-aligned spine, one idea
  per scene, and asymmetric balance. Flat surfaces, 1px borders, navy-tinted
  shadows, and at most two elevation levels.
- White text on navy; navy on light; white on red; navy on cyan. Never white
  on cyan. Body copy is 16px/1.5, max about 72ch; secondary text is `#6B7280`.
  Use red only for short emphasis.
- Use the official LightSpeed speed-mark logo from `brand/logo/` (e.g. `logo-light-bg.png` on dark, `logo-full.png` on light) with clear
  space equal to the "L" height. Never distort, recolor, or place it on busy
  imagery. Add `™` on the first mention of "LightSpeed Holdings Limited".
- Charts use navy axes, cyan for the primary series, and red for the single
  argued series.
- Do not rebrand the CEO dashboard, use off-palette colors, use the accent
  left-stripe card pattern as decoration, center body copy, or exceed roughly
  10% red or cyan in any scene.

Do not introduce a second, conflicting override layer. The LightSpeed section
in `house-style.md` is the source of truth.

`visual-styles.md` holds eight named presets. Use one only when the brief names
it and it does not conflict with the brand tokens.

## Render Loop

1. Read project metadata and confirm `videoModel`, `videoLength`, and
   `videoAspect`.
2. Scaffold into a new `.hyperframes-cache/<id>/` directory.
3. Author the composition: set the root duration, declare the palette, lay out
   the hero frame first, then add entrances. Keep edits minimal.
4. Check the root duration, palette, and text safe area against the brief.
5. Dispatch the render and capture `taskId` and `nextSince`.
6. Wait until exit 0. On exit 5, stop and report the error line rather than
   retrying.
7. Inspect the MP4: duration, dimensions, first and last frame, text
   legibility, and placeholder content.
8. Re-render only after a specific, named fix. Batch fixes into one render.

## Budget Gate

Each render is a paid job, and `media generate` has no dry-run flag.

- Confirm duration, aspect, model, and the number of renders with the human
  before the first dispatch.
- One render per approved cut. Do not re-render for speculative polish.
- Keep the composition source in the cache so a later fix is cheap.
- Do not generate variants or alternate cuts without explicit approval.
- If the brief is still moving, settle it before scaffolding.

## Handoff To QA

- Run `ls-artifact-qa` on the rendered file and on at least one extracted
  frame.
- Provide the output path, duration, dimensions, model, and composition
  directory.
- QA checks: brand tokens, type legibility, safe margins, clipped text,
  motion pacing, contrast, and audio if present.
- Fix the composition, re-render, and re-run QA. Do not ship on FIX.

## Verification

- The returned file exists at the expected path.
- Duration and dimensions match the brief and project metadata.
- Dimensions are the **exact** canvas: `1080 × 1920` for the vertical short,
  `1920 × 1080` for the landscape overview — verified with `ffprobe`, not assumed
  from the composition source.
- Palette gate run on source frames (reported as such) or on an extracted frame
  with the result stated honestly.
- Subtitle track present, one line at a time, inside the platform safe band.
- No placeholder text, debug overlays, missing fonts, or black frames.
- Palette, type, and logo match the brand tokens.
- The filename is quoted in the reply, with model, duration, and dimensions.
- The composition source remains under `.hyperframes-cache/` for the next
  revision (or, on the local path, under the campaign's `video/frames/`).
