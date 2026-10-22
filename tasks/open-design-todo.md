# Todo: Open Design Integration

## Wave 0

- [x] Write `specs/open-design-integration.md`
- [x] Write `tasks/open-design-plan.md`
- [x] Write `tasks/open-design-todo.md`
- [x] Create `feat/open-design-integration` from `origin/main`

## Wave 1: Foundational skills

- [x] `ls-od-runtime/SKILL.md`
- [x] `ls-od-catalogue/SKILL.md`
- [x] `ls-od-brand/SKILL.md`
- [x] Rewrite `scripts/maintenance/open-design-quickstart.ps1`

## Wave 2: Use-case skills

- [x] `ls-od-project/SKILL.md`
- [x] `ls-od-prototype/SKILL.md`
- [x] `ls-od-live-artifact/SKILL.md`
- [x] `ls-od-deck/SKILL.md`
- [x] `ls-od-image/SKILL.md`
- [x] `ls-od-video/SKILL.md`

## Wave 3: Routing

- [x] Update `ls-creative-director`
- [x] Update `ls-frontend-design`
- [x] Update `ls-presentation-design`
- [x] Update `ls-social-media-design`
- [x] Update `ls-artifact-qa`

## Wave 4: Agent binding

- [x] Add `skills` to `Agent`
- [x] Pass `skills` through `generate_from_registry`
- [x] Add guarded `## Skills` block to specialist template
- [x] Add guarded `## Skills` block to executive template
- [x] Add guarded `## Skills` block to agent template
- [x] Add `skills:` to 12 registry entries
- [x] Add registry/generator tests
- [x] Regenerate agents and verify unmapped cards unchanged

## Wave 5: Submodule and wiring

- [x] Add `open-design/design-systems/lightspeed/DESIGN.md` (uncommitted, submodule)
- [x] LightSpeed section added to HyperFrames `house-style.md` (uncommitted)
- [x] Reconcile `.opencode/integrations/open-design/agent-config.yaml` (12 agents, verified)
- [x] Write `docs/OPEN-DESIGN.md` (verified daemon v0.22.1, MCP entry, skill bindings)
- [ ] Update `AGENTS.md` §14 — AGENTS.md §9.4 deletion question unresolved; requires user clarification before editing §14
- [ ] Commit submodule change (`open-design/design-systems/lightspeed/`) and bump repo pin; the working tree has the files but the commit on `lightspeed/format-pass` has not been made
- [ ] Defer: add `od` MCP entry to root `opencode.json` — installer writes global config, not repo-local; hand-edit if desired, do not commit machine-specific paths

## Verification

- [x] `uv run ruff check src/ tests/`
- [x] `uv run mypy src/`
- [x] `uv run pytest`
- [x] Generator drift check (47 passed, all targeted agent cards unchanged)
- [x] `pwsh scripts/maintenance/lint-ecl.ps1` (27 files, 0 failures/warnings)
- [x] `od daemon status --json` smoke test (v0.22.1, 7456)
- [x] Confirm every documented `--skill` id exists (verified catalogue)
- [ ] Review PR diff contains only intended paths — AGENTS.md §9.4 deletion must be resolved first (see below)
- [ ] Open PR and confirm 6 required checks — blocked on AGENTS.md §9.4
