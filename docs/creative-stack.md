# Creative Production Stack (ls-* skills)

Moved from `AGENTS.md` §14. `AGENTS.md` keeps the layer order and rules; this file has the layer table.

Branded creative output routes through a layered skill stack. All `ls-*` skills live in `.agents/skills/`.

**Layers (in order):**

| Layer | Skill(s) | Role |
|-------|----------|------|
| Brand base | `ls-design-system` | ALWAYS loaded first by any creative skill; brand tokens live in `brand/tokens/` (canonical-only, not mirrored) + `brand/guidelines/`; `static/brand/` + `public/brand/` mirror other brand assets — see `brand/CANONICAL_SOURCES.md` |
| Orchestrator | `ls-creative-director` | Brief intake (artifact/audience/objective/narrative/visual language) → routes to one production skill + support skills |
| Production | `ls-frontend-design`, `ls-presentation-design`, `ls-document-design`, `ls-social-media-design`, `ls-brand-advertising` | Generate the artifact, delegating rendering to existing engines (python-pptx, Vite React SPA at repo-root `src/`, k-dense-*, Playwright) |
| Support | `ls-diagramming`, `ls-documentation-engineering`, `ls-visual-storytelling` | Diagram/graphic/doc-IA assets used inside produced artifacts |
| Gatekeeper | `ls-artifact-qa` | ALWAYS runs last on every artifact: Visual / Brand / UX / Accessibility / Content QA → APPROVE or FIX→re-render. Includes Playwright visual checks via `ls-artifact-qa` skill (see `.agents/skills/ls-artifact-qa/`) |

**Rules:** Any creative task starts at `ls-creative-director` (or loads `ls-design-system` directly) and ends at `ls-artifact-qa`. Brand tokens are the single source of truth — never invent brand colors/fonts. Rendering reuses existing engines rather than rebuilding them.
