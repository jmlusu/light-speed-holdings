# Plan

## Technical Approach

Per-item consolidation following the Phased Approval & Rollback Protocol:
for each removal, identify the canonical survivor, migrate consumers
(CLI wiring, tests, docs), verify zero references, remove, validate.

1. **LS-MEM:** rewire `memory` → legacy CLI first (consumers keep working),
   then delete engine + skills + docs + tests. Single atomic commit.
2. **Milestones:** prove `.py` by running it (discard output), delete `.js`,
   update README. Single commit.
3. **Runtime:** delete only provably unreferenced junk (`.bak`,
   `.RUN2GENERATED`, `.tmp`); probe live processes before touching live
   paths; defer live relocation with evidence when a daemon holds them.
4. **`tmp/`:** reference sweep (src/tests/scripts/config), then `git rm -r`.
5. **Submodule:** metadata checks + upstream pin fetch + shallow clone
   metadata test. No tree changes expected.

## Impacted Modules And Files

- `src/ai_company/cli/main.py`, `src/ai_company/lsmem/` (removed)
- `src/ai_company/cli/memory.py` (canonical survivor, untouched)
- `tests/memory/` (8 files removed, `test_git_safety.py` kept),
  `tests/unit/test_cli_commands.py` (wiring test rewritten)
- `.agents/skills/ls-memory/`, `.opencode/skills/ls-memory/` (removed)
- 7 LS-MEM docs (removed); USER-GUIDE, CLI-DESIGN (updated)
- `scripts/build/generate-milestones-deck.js` (removed); README (updated)
- `tmp/` (126 files removed); runtime junk (untracked, deleted from disk)

## Interfaces, Data, Permissions

- `ai-company memory` now serves the legacy JSON store; `knowledge`
  remains an alias to the same module. Live user memory data
  (2,049 episodic records) untouched and verified readable post-change.
- No permission/auth/config-format changes. No data migration performed.

## Spec Gaps Found From Planning

None — owner directives plus evidence gathered during execution cover
every item; deferrals recorded with reasons.

## Risks And Mitigations

| Risk | Mitigation |
|------|------------|
| Lsmem still imported somewhere missed | Repo-wide grep for `lsmem` post-removal (zero hits required) |
| Legacy `memory` CLI regressed | Rewritten wiring test + live `memory list` smoke |
| Live daemon split-brain on relocation | Probed processes first; moved nothing live |
| Skill deletion breaks agent discovery | Skills were unreferenced by registry/config; generator round-trip clean |

## Verification Plan

ruff + mypy + pytest (memory/CLI suites, then full health gate) +
generator round-trip + `sync-registry --verify` + lint-ecl +
`scripts/health_check.py` ALL PASS.
