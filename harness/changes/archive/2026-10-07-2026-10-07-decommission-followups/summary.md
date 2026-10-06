---
title: "Decommission follow-ups"
slug: "2026-10-07-decommission-followups"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "approved"
spec_review: "approved"
plan_review: "approved"
modules:
  - "src/ai_company/lsmem"
  - "src/ai_company/memory"
  - "src/ai_company/cli"
  - "scripts/build"
  - "orchestrator"
  - "memory"
  - "tmp"
files: []
tags:
  - "decommission"
  - "ls-mem"
  - "consolidation"
  - "follow-up"
validation_status: "pass"
created_at: "2026-10-07"
updated_at: "2026-10-07"
session_id: "cleanup-session-002"
owner_agent: "jmlus"
claimed_at: "2026-10-07"
---

# Summary

## Outcome

Execute the five owner directives from the 2026-10-06 sanitization handoff:
decommission LS-MEM, consolidate the milestones deck on Python, relocate
runtime state, delete `tmp/` scratch, verify the open-design submodule pin.

## Decisions (owner, 2026-10-07)

1. **Decommission LS-MEM** — JSON `MemoryStore` is the single memory engine.
2. **Milestones: keep `.py`** (runs on installed `python-pptx`); drop `.js`
   (`pptxgenjs` not installed; neither referenced anywhere).
3. **Runtime relocation: approved** — executed to the maximum safe extent
   (see deferral below).
4. **`tmp/`: delete** — 126 tracked scratch files, zero references.
5. **Fresh-clone verification: handled** — pin verified upstream + clone
   carries declaration (2.7 GB content fetch intentionally not exercised).

## Validation

- ruff pass; mypy pass (225 files, lsmem 11 gone)
- pytest: memory + CLI suites 38 pass; full suite green via health check
- `ai-company memory list` works against the live legacy store (data intact)
- Milestones `.py` generates the 15-slide deck (output discarded, not committed)
- `sync-brand -Verify`, generator round-trip, lint-ecl: pass
- Canonical gate: `uv run python scripts/health_check.py` → ALL HEALTH CHECKS PASSED

## Partially Deferred (evidence-backed)

- **Live runtime relocation:** a daemon (2× python) + dashboard (uvicorn)
  are running and `orchestrator/approvals.yaml` carries 274 uncommitted
  insertions (live queue). Deleted ~275 MB of unreferenced junk
  (`.bak`, `.RUN2GENERATED`, `.tmp`); moving live paths while the daemon
  writes them would split-brain the queue. Requires stopping the daemon first.
- **Fresh-clone content fetch:** declaration + pin + upstream availability
  verified; the 2.7 GB download itself not exercised. Recommend CI avoid
  `--recurse-submodules` unless the tool is needed.

## Next Step

Close this change.

