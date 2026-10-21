# Implementation Plan: Open Design Integration

## Overview

Deliver the open-design render layer in five waves. Wave 1 and 2 are independent skill authoring and run in parallel. Wave 3 wires routing. Wave 4 implements enforced agent binding. Wave 5 finishes the submodule, config, docs, verification, and PR.

Branch: `feat/open-design-integration` (from `origin/main`).
Spec: `specs/open-design-integration.md`.

## Architecture Decisions

| Decision | Rationale |
|----------|-----------|
| `od` as render layer, skills as adapters | Keeps the runtime replaceable and agent instructions repo-local |
| No new agents | User decision; skills attach to the existing 90-agent org |
| Option B (enforced `skills:`) | Makes binding visible in every generated card, not advisory |
| Insert block at end of `extra_sections` | Both `specialist.md.j2` and `executive.md.j2` expose that block; `metrics` stays untouched |
| `{% if skills %}` guard | Empty values must render byte-identically for the 78 unmapped agents |
| Submodule content on `lightspeed/format-pass` | Keeps the fork's extension points and the pin aligned |
| Path-scoped commits | The worktree has 353 lines of unrelated pre-existing changes |

## Wave 0: Spec and tasks

**Deliverables**

- `specs/open-design-integration.md`
- `tasks/open-design-plan.md`
- `tasks/open-design-todo.md`

**Exit:** spec covers Objective, Commands, Project Structure, Code Style, Testing Strategy, Boundaries.

## Wave 1: Foundational skills (parallel)

| Skill | Owner | Notes |
|-------|-------|-------|
| `ls-od-runtime` | subagent A | Daemon lifecycle, CLI map, MCP, Windows failure modes, quickstart script rewrite |
| `ls-od-catalogue` | subagent B | Skill-vs-template decision tree, id selection rules |
| `ls-od-brand` | subagent B | LightSpeed tokens, design-system handoff, brand QA |

**Exit:** three `SKILL.md` files exist; every command and id is verifiable against `open-design/`.

## Wave 2: Use-case skills (parallel)

| Skill | Owner | Template ids |
|-------|-------|--------------|
| `ls-od-project` | subagent C | project subcommands |
| `ls-od-prototype` | subagent C | `web-prototype*`, `saas-landing`, `mobile-app`, `mobile-onboarding`, `wireframe-*` |
| `ls-od-live-artifact` | subagent D | `live-artifact`, `live-dashboard`, `dashboard`, `kanban-board`, `orbit-*` |
| `ls-od-deck` | subagent E | `html-ppt*`, `guizang-ppt`, `kami-deck`, `ib-pitch-book`, `magazine-poster` |
| `ls-od-image` | subagent F | `od media generate` / `wait`, `image-poster` |
| `ls-od-video` | subagent F | `hyperframes`, `video-shortform`, `motion-frames`, `sprite-animation` |

**Exit:** six `SKILL.md` files exist; no invented ids.

## Wave 3: Routing and cross-references

- `ls-creative-director`: add the nine skills to its routing table.
- `ls-frontend-design`: delegate prototype/live-artifact rendering to `ls-od-prototype` / `ls-od-live-artifact`.
- `ls-presentation-design`: delegate deck rendering to `ls-od-deck`.
- `ls-social-media-design`: delegate asset rendering to `ls-od-image` / `ls-od-deck`.
- `ls-artifact-qa`: add an open-design artifact check.

**Exit:** existing skills reference the new layer without changing their core workflow.

## Wave 4: Enforced agent binding

1. `models.py`: add `skills: list[str] = Field(default_factory=list)` to `Agent`.
2. `generator.py`: pass `skills` through `generate_from_registry`; `_generate_from_local_registry` already forwards raw YAML.
3. `templates/specialist.md.j2`, `templates/executive.md.j2`, `templates/agents/agent.md.j2`: guarded `## Skills` block at end of `extra_sections`.
4. `company-registry.yaml`: add `skills:` to the 12 mapped entries.
5. `tests/unit/test_registry.py`: field validation.
6. Regenerate `.opencode/agents/*.md`; verify unmapped cards unchanged.

**Exit:** 12 cards show `## Skills`; all other cards byte-identical; tests pass.

## Wave 5: Submodule, wiring, docs, PR

1. `open-design/design-systems/lightspeed/DESIGN.md`.
2. `open-design/design-templates/hyperframes/house-style.md` LightSpeed section.
3. Commit inside the submodule on `lightspeed/format-pass`; bump the pin.
4. `opencode.json`: add `od` MCP server entry.
5. `.opencode/integrations/open-design/agent-config.yaml`: reconcile skill names.
6. `scripts/maintenance/open-design-quickstart.ps1`: replace the nonexistent `open-design create` flow.
7. `docs/OPEN-DESIGN.md`; `AGENTS.md` §14 row.
8. Run verification; push; open the PR.

**Exit:** all checks green; PR body lists waves, tests, risks, and rollback.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| `better-sqlite3` native build fails on Windows | Document WSL2 fallback; do not block content PR on a local build |
| Pre-existing dirty worktree contaminates the PR | Path-scoped commits; verify `git log --name-only` |
| Registry edit breaks YAML anchors | Edit in place; parse with `load_registry` before regenerating |
| Unmapped cards drift | Diff generated output before/after; guard block is conditional |
| `--skill` id typo | Cross-check every id against `open-design/design-templates/` |
| Version-check failure | Do not bump the version |
