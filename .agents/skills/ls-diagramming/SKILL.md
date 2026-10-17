---
name: ls-diagramming
description: "The LightSpeed diagram engine. Produces technical, business, and strategy diagrams on a clear tool-choice matrix: Mermaid (architecture, process, flow), SVG/D3 (custom data visuals), Kroki as a fallback renderer, and brand-palette restyle always. Covers system architecture, API/data flows, agent architectures, AI pipelines, value chains, org structures, customer journeys, process maps, and 2x2/strategy frameworks. Renders in the LightSpeed brand (navy/red/cyan) unless embedded in another ls-* artifact. Trigger on: 'diagram', 'architecture diagram', 'flowchart', 'process map', 'org chart', 'sequence diagram', '2x2', 'pipeline', 'data flow'."
---

# LightSpeed Diagramming

Create precise, on-brand diagrams across the whole spectrum — from technical architecture to strategy frameworks.

## Preconditions

1. Load `ls-design-system` for palette + type when the diagram will live in a branded artifact.
2. Choose the tool by diagram type (matrix below) — do not default everything to one tool.

## Tool-Choice Matrix

| Diagram type | Primary | Fallback | Notes |
|--------------|---------|----------|-------|
| System architecture, infrastructure | Mermaid `flowchart` | SVG (hand-built) | keep node count ≤ ~15 per diagram |
| API / data flows, pipelines | Mermaid `flowchart` / `sequenceDiagram` | PlantUML via Kroki | |
| Agent architecture, AI pipelines | Mermaid `flowchart` | SVG | emphasize stages + HITL gates |
| Process maps, workflows | Mermaid `flowchart` | Image (`k-dense-sci-schematics`) | |
| Org structures | Mermaid `flowchart TD` | kroki | |
| Customer journeys | Mermaid `journey` (curated) or flowchart | SVG | custom beats default journey look |
| Sequence/collaboration | Mermaid `sequenceDiagram` | | |
| State / decision trees | Mermaid `stateDiagram` | | |
| Strategy 2×2, frameworks, matrices | SVG (hand-built, brand palette) | `k-dense-mckinsey-style` (2×2/waterfall/small multiples) | prefers clean SVG |
| Timelines, Gantt | Mermaid `gantt` / `timeline` | | |
| ER / data models | Mermaid `erDiagram` | | |
| Complex multi-format scientific visuals | `k-dense-sci-schematics` | `generate_image` | |

## Rendering

- **Mermaid → SVG/PNG:** prefer the `k-dense-mermaid-skill` (validates syntax, renders, auto-fixes). If mermaid-cli is unavailable, use **Kroki** (https://kroki.io) — diagram type → endpoint (e.g. `https://kroki.io/mermaid/svg/<encoded>`).
- **Custom SVG:** hand-write with brand colors when Mermaid is too rigid (2×2s, custom layouts).
- **PNG raster for docs/slides:** render SVG → PNG; keep ≥2× resolution for print.

## Brand Styling (when standalone or in ls-* artifacts)

- Node fills: navy `#070A40` for primary nodes; white/grey-light `#F2F2F2` for supporting; cyan `#00BFFF` for accent/highlight; red `#E63946` reserved for CTAs, warnings, the "ask".
- Edges: dark-grey `#6B7280`; highlighted paths cyan.
- Labels: Arial; node labels 12–14pt, edge labels 10–11pt.
- Never embed a non-brand chart theme inside a LightSpeed artifact.

## Diagram QA (before `ls-artifact-qa`)

- [ ] Tool chosen by the matrix, not habit
- [ ] Node count fits the diagram's intent (≤15 for architecture; more implies splitting)
- [ ] One clear flow direction; no crossing edge spaghetti
- [ ] Labels readable at final display size
- [ ] Brand palette applied
- [ ] Renders without syntax errors (validate via `k-dense-mermaid-skill` or Kroki response)

Deliver the source (`.mmd`/SVG) + rendered file (SVG/PNG) + a note on the chosen engine.
