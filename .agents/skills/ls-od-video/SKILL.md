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
- No placeholder text, debug overlays, missing fonts, or black frames.
- Palette, type, and logo match the brand tokens.
- The filename is quoted in the reply, with model, duration, and dimensions.
- The composition source remains under `.hyperframes-cache/` for the next
  revision.
