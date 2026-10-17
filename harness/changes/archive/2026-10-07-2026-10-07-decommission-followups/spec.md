# Specification

## Scope

Execute the five owner directives from the 2026-10-06 sanitization handoff
as one follow-up change: LS-MEM decommission, milestones consolidation,
runtime relocation, `tmp/` purge, submodule verification.

## Acceptance Criteria

### LS-MEM decommission
- [x] `ai-company memory` resolves to `ai_company.cli.memory` (legacy JSON store)
- [x] Zero `lsmem` references in src/tests/scripts
- [x] `src/ai_company/lsmem/`, both skill deploys, 7 LS-MEM docs, 8 LS-MEM
  tests, `Clean-LSMEM.ps1` removed
- [x] Living docs updated (USER-GUIDE, CLI-DESIGN, pre-commit exclusion)
- [x] History preserved: ADR-025, harness archives, git history

### Milestones consolidation
- [x] `.py` proven (generates 15-slide deck; output discarded)
- [x] `.js` removed; README documents the Python path

### Runtime relocation
- [x] Unreferenced junk deleted (~275 MB)
- [x] Live paths left in place with recorded evidence (running daemon +
  live queue); relocation deferred, not dropped

### tmp/ purge
- [x] Reference sweep clean; 126 tracked files removed; `tmp/` gitignored

### Submodule verification
- [x] `.gitmodules` parses; gitlink recorded; pin fetched from upstream;
  fresh shallow clone carries both

## Resolved Clarifications

- Owner directives 2026-10-07 (5 items) are the full spec; no open questions
  except the recorded deferrals (live relocation, content fetch, promotion).
