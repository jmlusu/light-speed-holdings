---
name: ls-od-image
description: "Generate brand-consistent images, posters, and social assets with the Open Design media pipeline, including prompt structure, waiting for tasks, and budget control. Trigger on: 'od image', 'open design image', 'generate poster od', 'od media generate', 'image-poster'."
---

# Open Design Images

Produce finished still assets through the Open Design media pipeline. The
pipeline dispatches to the configured image model, writes the file into the
project, and returns the filename. This skill covers prompt assembly, task
waiting, and the spend gate.

## When To Use

- Posters, key art, editorial illustrations, cover art, OG images, blog heroes.
- Social stills that need a rendered image rather than an HTML composition.
- Any request where the deliverable is one or more PNG/JPEG assets.

Use `ls-design-system` for the token definitions and official logo assets this
skill applies.

## Budget Gate

`od media generate` has no dry-run or print-only flag. Calling it submits a
paid job immediately.

- Before the first call, confirm with the human: image count, model, aspect,
  and whether variations are wanted.
- Default to one image per request. Do not generate a grid of options
  speculatively.
- Re-running for a small fix is a new paid job. Batch the fixes into one
  re-render.
- If the model or count was not explicitly approved, stop and ask.

## Commands

Inside Open Design the daemon exports `OD_NODE_BIN`, `OD_BIN`,
`OD_PROJECT_ID`, and `OD_PROJECT_DIR`. Use them; do not call provider APIs
directly.

```bash
"$OD_NODE_BIN" "$OD_BIN" media generate \
  --project "$OD_PROJECT_ID" \
  --surface image \
  --model "gpt-image-2" \
  --aspect "1:1" \
  --quality "high" \
  --output "hero-poster.png" \
  --prompt "<assembled prompt>"
```

- `--prompt-file <path|->` reads a long prompt from a file or stdin.
- `--aspect` accepts `1:1`, `16:9`, `9:16`, `4:3`, `3:4`.
- `--quality` applies to OpenDesign Cloud images; `gpt-image-2` accepts
  `low`, `medium`, `high`.
- Output is one JSON line. A fast job returns `{"file": ...}`. A slow job
  returns `{"taskId": "...", "nextSince": <n>}` with exit code 0.

When a task ID comes back, poll:

```bash
"$OD_NODE_BIN" "$OD_BIN" media wait "<taskId>" --since "<nextSince>"
```

Exit code 0 means done, 2 means still running (poll again with the new
`nextSince`), 5 means failed. Poll until it reaches 0 or 5.

The examples are POSIX shell. On PowerShell use
`& $env:OD_NODE_BIN $env:OD_BIN media generate ...` and poll the same way.

`media scaffold` is for HyperFrames video compositions only. Do not use it for
images.

## Prompt Structure

Assemble the prompt in this order before calling the tool:

1. **Subject and composition** — what is in frame, where, at what scale, and
   the crop.
2. **Lighting and mood** — studio or natural, warm or cool, key plus rim plus
   fill.
3. **Palette and texture** — brand hex anchors: navy `#070A40`, red `#E63946`,
   cyan `#00BFFF`. Tint neutrals toward navy instead of using dead gray.
4. **Camera and lens** — only when photographic realism is requested.
5. **Avoid list** — no warped text, no extra fingers, no fake logos, no
   placeholder marks, no generic neon gradient.

Rules:

- No in-frame text unless the human asked for it. Real copy belongs in a
  separate overlay pass.
- One accent hue per asset. Navy field, red primary accent, cyan used sparingly.
- Arial is the brand face. If type appears in frame, specify Arial and a size
  that survives a thumbnail crop.
- Keep the composition on a 4px spacing rhythm where layout is described.

The `image-poster` design template is the reference implementation for this
workflow.

## Asset Storage

- Write to `output/design/` unless the human specified another path.
- Use a short descriptive filename in `--output`; the returned `file.name` is
  the source of truth.
- Record the prompt, model, aspect, and task ID with the asset so the render is
  reproducible.
- Never overwrite an approved asset. Version it with `-v2`, `-v3`.
- Do not leave rejected renders in the delivery folder.

## Brand Consistency

- Load `ls-design-system` first and use its tokens rather than inventing
  colors or type.
- Never recolor, redraw, or approximate the logo. Use the official asset.
- Cyan is an intentional brand accent, not the generic cyan-on-dark AI tell.
  Give it one role and keep it out of large fills.
- Check the result against the official logo files in `brand/logo/` and the
  brand tokens when the asset carries identity.
- At thumbnail size the subject must still read; if it does not, simplify the
  composition rather than adding contrast filters.

## Verification

- The returned file exists at the expected path.
- Dimensions match the requested aspect ratio.
- No placeholder text, watermark, malformed logo, or extra anatomy.
- Palette and type match the brand tokens.
- The filename is quoted in the reply, with model, aspect, and a one-paragraph
  summary of the prompt used.
- No additional image was generated beyond the approved count.
