# Spec: Open Design Integration

## Objective

Make **Open Design (`od`)** the render layer for LightSpeed Holdings creative work, and bind it to the existing agent team through enforceable skills.

The integration adds:

1. Nine `ls-od-*` skills in `.agents/skills/` that teach agents how to drive the `od` daemon, select the right rendering template, apply LightSpeed brand tokens, and gate output through `ls-artifact-qa`.
2. **Agent binding:** the 12 existing agents are bound to `ls-od-*` skills as specified in this spec's agent binding table and documented in `docs/OPEN-DESIGN.md` §7 and `AGENTS.md` §14. No `skills:` registry field, generator, or template changes are made (no enforcement layer), and no new agents are added to `company-registry.yaml`.
3. Submodule content in `open-design/` (LightSpeed design system + HyperFrames house-style override), committed on `lightspeed/format-pass`, with the main-repo pin bumped.
4. Repo wiring: MCP entry, integration config update, working quickstart script, and `docs/OPEN-DESIGN.md`.

**Success criteria:**

- `od` daemon can be started, queried, and stopped from PowerShell on this machine.
- `od mcp` stdio server is registered in root `opencode.json` and exposes the daemon tools to OpenCode agents.
- All nine skills are discoverable, follow the repo `ls-*` frontmatter format, and contain no invented `--skill` ids.
- The binding table covers exactly 12 agents, documented consistently in this spec, `docs/OPEN-DESIGN.md` §7, and `AGENTS.md` §14; no registry, generator, or template changes are made.
- `uv run ruff check src/ tests/`, `uv run mypy src/`, `uv run pytest`, the generator drift check, and `pwsh scripts/maintenance/lint-ecl.ps1` pass.
- The PR contains only open-design integration paths; unrelated pre-existing worktree changes are not committed.

**Non-goals:**

- Adding new company agents or departments.
- Changing the project version (`pyproject.toml` / `CHANGELOG.md` / tag).
- Replacing `ls-creative-director`, `ls-presentation-design`, `ls-frontend-design`, or `ls-artifact-qa`; they remain the orchestration and QA layers.
- Paid media generation without an approved budget.
- Modifying `recovery/marketing-site/*`.

## Architecture

| Layer | Responsibility | Location |
|-------|----------------|----------|
| Render runtime | `od` daemon, CLI, MCP server, media pipeline | `open-design/` submodule |
| Skill adapters | Agent-facing instructions for the runtime | `.agents/skills/ls-od-*` |
| Orchestration | Brief intake and routing | `ls-creative-director` |
| QA gate | Visual, brand, UX, accessibility, content checks | `ls-artifact-qa` |
| Agent binding | Specified in this spec; documented in `docs/OPEN-DESIGN.md` §7 and `AGENTS.md` §14 (no registry `skills:` field) | `specs/open-design-integration.md`, `docs/OPEN-DESIGN.md`, `AGENTS.md` |

### Skill catalog

| Skill | Scope |
|-------|-------|
| `ls-od-runtime` | Daemon lifecycle, CLI verb map, MCP wiring, Windows failure modes, verification |
| `ls-od-catalogue` | Choosing between functional skills and design templates; id selection rules |
| `ls-od-brand` | `design-systems/lightspeed/DESIGN.md`, brand-token handoff, brand QA |
| `ls-od-project` | `od project create-design-system`, `import-folder`, `duplicate`, `info` |
| `ls-od-prototype` | `web-prototype*`, `saas-landing`, `mobile-app`, `mobile-onboarding`, `wireframe-*` |
| `ls-od-live-artifact` | `live-artifact`, `live-dashboard`, `dashboard`, `kanban-board`, `orbit-*` |
| `ls-od-deck` | `html-ppt*`, `guizang-ppt`, `kami-deck`, `ib-pitch-book`, `magazine-poster` |
| `ls-od-image` | `od media generate` / `od media wait`, `image-poster`, budget gate |
| `ls-od-video` | `hyperframes` (primary), `video-shortform`, `motion-frames`, `sprite-animation` |

### Agent binding (12 agents)

| Agent | Registry line | Skills |
|-------|---------------|--------|
| `creative_director` | ~3900s | all nine |
| `cmo` | 309 | `ls-od-runtime`, `ls-od-catalogue`, `ls-od-deck` |
| `social_media_manager` | 1334 | `ls-od-image`, `ls-od-deck` |
| `marketing_owner` | 1335 | `ls-od-catalogue`, `ls-od-deck`, `ls-od-image` |
| `technical_documentation_lead` | 1909 | `ls-od-live-artifact`, `ls-od-deck` |
| `product_marketing_manager` | 2133 | `ls-od-deck`, `ls-od-image` |
| `product_designer` | 2487 | `ls-od-brand`, `ls-od-prototype`, `ls-od-live-artifact` |
| `lead_frontend` | 2799 | `ls-od-prototype`, `ls-od-live-artifact` |
| `senior_frontend_engineer` | 2890 | `ls-od-prototype` |
| `market_analyst` | 3070 | `ls-od-live-artifact`, `ls-od-deck` |
| `content_creator` | 3160 | `ls-od-image`, `ls-od-video`, `ls-od-deck` |
| `media_generation_owner` | 3915 | `ls-od-runtime`, `ls-od-image`, `ls-od-video` |

## Commands

| Action | Command |
|--------|---------|
| Install runtime | `pnpm install` (in `open-design/`) |
| Start daemon | `od daemon start --headless` |
| Daemon status | `od daemon status --json` |
| Stop daemon | `od daemon stop` |
| MCP server | `od mcp` |
| MCP install preview | `od mcp install opencode --print --json` |
| List skills | `od skill list --json` |
| List design systems | `od design-systems list` |
| Run a template | `od run start --project <projectId> --skill <id> --json` |
| Image generation | `od media generate ...` then `od media wait <taskId>` |
| Submodule guard | `pnpm guard` |
| Submodule types | `pnpm typecheck` |
| Regenerate agents | `uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` |
| Python tests | `uv run pytest` |
| Lint | `uv run ruff check src/ tests/` |
| Type check | `uv run mypy src/` |
| Harness lint | `pwsh scripts/maintenance/lint-ecl.ps1` |

## Project Structure

```
.agents/skills/
├── ls-od-runtime/SKILL.md
├── ls-od-catalogue/SKILL.md
├── ls-od-brand/SKILL.md
├── ls-od-project/SKILL.md
├── ls-od-prototype/SKILL.md
├── ls-od-live-artifact/SKILL.md
├── ls-od-deck/SKILL.md
├── ls-od-image/SKILL.md
└── ls-od-video/SKILL.md

open-design/                                  (submodule, branch lightspeed/format-pass)
├── design-systems/lightspeed/DESIGN.md
└── design-templates/hyperframes/house-style.md

docs/OPEN-DESIGN.md
specs/open-design-integration.md
tasks/open-design-plan.md
tasks/open-design-todo.md
scripts/maintenance/open-design-quickstart.ps1
opencode.json
.opencode/integrations/open-design/agent-config.yaml
AGENTS.md
company-registry.yaml
src/ai_company/models/models.py
src/ai_company/generator.py
templates/specialist.md.j2
templates/executive.md.j2
templates/agents/agent.md.j2
tests/unit/test_registry.py
tests/unit/test_generator*.py
```

## Code Style

- **Python:** `ruff` + `mypy` clean; Pydantic `Field(default_factory=list)` for new list fields; no comments unless required.
- **Jinja:** preserve existing whitespace; the new block is wrapped in `{% if skills %}...{% endif %}` so empty values render byte-identically.
- **Registry YAML:** 2-space indentation, `skills:` as a block list under each agent entry, matching the existing `tools:` shape.
- **Skills:** frontmatter is exactly:
  ```yaml
  ---
  name: ls-od-<name>
  description: "One paragraph. Trigger on: 'phrase', 'phrase'."
  ---
  ```
  Body starts with `# Title`, then `## When To Use`, `## ...`, `## Verification`. Use the `ls-design-system` skill as the formatting reference.
- **Docs:** Markdown, no emojis, relative repo paths, PowerShell examples for Windows.

## Testing Strategy

| Change | Test |
|--------|------|
| `Agent.skills` field | `tests/unit/test_registry.py`: optional, defaults to `[]`, accepts list |
| Generator skill block | Unit test renders a specialist/executive with and without `skills`; asserts section present/absent |
| Empty-value compatibility | Regenerate and confirm unmapped cards are byte-identical |
| Registry mapping | Parse `company-registry.yaml` and assert the 12 agents carry the expected skill ids |
| Skills | Frontmatter parseable; every `od --skill` id referenced exists in `open-design/design-templates` |
| Runtime | Manual smoke: `od daemon start --headless`, `od daemon status --json`, `od mcp --help` |
| CI | `ruff`, `mypy`, `pytest`, generator drift, archify, ECL lint |

## Boundaries

**Always:**

- Read `.ai-company/constitution/11-GIT-STANDARDS.md` before git work.
- Work on `feat/open-design-integration`; open a PR; merge only when the 6 required checks are green.
- Commit path-scoped (`git commit -- <paths>`); leave unrelated worktree changes alone.
- Regenerate `.opencode/agents/*.md` after registry/template changes.
- Validate `--skill` ids against `open-design/design-templates/` before documenting them.
- Use LightSpeed brand tokens from `brand/tokens/brand-tokens.json`.

**Ask First:**

- Adding a 13th agent to the binding map.
- Editing shared `open-design/design-templates/*` beyond `hyperframes/house-style.md`.
- Any media generation that spends money.
- Changing the daemon's global config or installing MCP into a non-repo scope.

**Never:**

- Invent `--skill` ids or CLI flags.
- Run `od media generate` without an approved budget.
- Hand-edit `.opencode/agents/*.md` or `harness/changes/INDEX.json`.
- Bump the version.
- Touch `recovery/marketing-site/*`.
- Commit the pre-existing staged files unrelated to this integration.
