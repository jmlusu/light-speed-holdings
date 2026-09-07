# Archify Diagram Generation

`ai-company archify` turns the company registry into interactive Archify
diagrams (SVG/HTML) and validates them. It is the CLI surface over
`src/ai_company/archify/` (converter + Node renderer wrapper).

## What it generates

`ai-company archify generate` writes four JSON IR sources into
`docs/diagrams/`:

| Diagram | Source file | Quality profile |
|---------|-------------|-----------------|
| Architecture (leadership) | `architecture.json` | `standard` |
| Workflow | `hiring.workflow.json` | `showcase` |
| Sequence | `hiring.sequence.json` | `showcase` |
| Dataflow | `hiring.dataflow.json` | `showcase` |

The **architecture** diagram is authored at `standard` because the leadership
org chart is dense (20+ nodes across the board/exec/staff tiers) and cannot
fit the sub-1706px viewBox that `showcase`'s desktop-readability gate demands.
The workflow/sequence/dataflow diagrams are authored at `showcase`.

## Commands

### `generate`

```
ai-company archify generate [--scope leadership|full]
```

Regenerates the four JSON IR sources from `company-registry.yaml`.
`--scope full` emits the full 100+ agent graph instead of the leadership subset.

### `validate`

```
ai-company archify validate <diagram_type> [file] [--quality standard|showcase]
```

Validates a JSON IR source against the Archify renderer (requires Node.js >= 18).
Without `file`, it validates the default source for that type. Without
`--quality`, it uses the authored profile for the type. Exits non-zero on a
failed validation.

### `deliver`

```
ai-company archify deliver <diagram_type> [file] [-o out.html] [--quality X] [--open]
```

Renders + validates a source to a self-contained interactive HTML artifact.
Only a **passing** artifact is written. Prints the artifact's SHA-256 and byte
size.

### `compare`

```
ai-company archify compare <diagram_type> <base.json> <head.json> [-o out.html] [--open]
```

Renders a Before/Delta/After comparison HTML from two validated snapshots —
useful for reviewing how a registry change reshapes a diagram.

## Validation & CI

The `archify-check` job in `.github/workflows/ci.yml` is part of the merge
gate. It:

1. Regenerates all four JSON sources from the registry.
2. Fails if the committed `docs/diagrams/*.json` drifted (run
   `ai-company archify generate` and commit the regenerated output).
3. Validates each source at its authored quality profile.

## SVG/HTML rendering

Rendering shells out to the bundled Archify Node CLI at
`.opencode/skills/archify/bin/archify.mjs`. If Node.js (>= 18) is unavailable,
the renderer degrades cleanly with a readable hint instead of a raw subprocess
traceback (`ArchifyNotAvailable`).

## Layout notes

- Component positions are computed as a compact tidy tree: parents are
  centered over their children, subtrees are packed with an 8px horizontal gap
  floor, and root leaves are absorbed back into the depth-0 band so a wide set
  of disconnected roots does not stretch the canvas.
- A post-pass resolves any same-row collisions the parent-centering step can
  introduce, enforcing the validator's minimum spacing.
