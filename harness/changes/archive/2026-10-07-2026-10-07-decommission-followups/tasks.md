# Tasks

- [x] T001 Rewire `memory` CLI to legacy + rewrite wiring test
- [x] T002 Delete lsmem engine, skills, docs, tests, Clean-LSMEM script
- [x] T003 Update USER-GUIDE, CLI-DESIGN, pre-commit exclusion
- [x] T004 Validate decommission (ruff, mypy, pytest, live smoke, zero-refs grep)
- [x] T005 Commit: refactor(memory) decommission LS-MEM
- [x] T006 Prove milestones `.py`, delete `.js`, README Python-only, commit
- [x] T007 Delete unreferenced runtime junk (~275 MB)
- [x] T008 Record live-relocation deferral evidence (daemon PIDs, queue diff)
- [x] T009 Reference-sweep + delete `tmp/` (126 files), commit
- [x] T010 Verify submodule pin (local + upstream + clone metadata)
- [x] T011 Full health gate green
- [x] T012 Close ECL change

## Deferred Tasks

- Live runtime relocation (orchestrator/memory live paths): stop the
  daemon first, then move + migrate + validate + restart. Evidence in
  summary.md.
- Fresh-clone content fetch (2.7 GB): exercise only if/when the tool is
  needed; recommend CI avoid `--recurse-submodules` by default.
- Owner promotion (merge) decision for both this and the prior change.
