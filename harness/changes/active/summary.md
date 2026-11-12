---
title: "T5 competitive landscape Nov refresh (#447)"
slug: "t5-competitive-landscape-nov-refresh-447"
status: "in_progress"
location: "active"
phase: "validate"
intake_status: "approved"
spec_review: "approved"
plan_review: "approved"
modules:
  - docs/marketing
  - docs/venture-studio
files:
  - docs/marketing/competitive-landscape.md
  - docs/venture-studio/scoreboard-v1.md
tags:
  - docs
  - competitive-landscape
  - t5-447
validation_status: "pass"
created_at: "2026-11-10"
updated_at: "2026-11-12"
session_id: "614ef677-9074-42ba-8904-3ad377641de6"
owner_agent: "jmlus"
claimed_at: "2026-11-10"
---

# Summary

## Outcome

Refreshed `docs/marketing/competitive-landscape.md` from Baseline v2 (2026-10-07) to
Baseline v3 (state as of 2026-11-10) and wrote the first-ever §8 "November 2026 Delta"
(T5 #447). The §7 monthly checklist is advanced to 2026-12-16, every new factual line
carries a source URL with an access date and a VERIFIED / VENDOR CLAIM / UNCONFIRMED
honesty tag per ADR-020/033, and the missing October §8 is recorded transparently rather
than back-filled. `docs/venture-studio/scoreboard-v1.md` gains decision entry 7, mirroring
the entry-6 pattern for T4 #420.

## Decisions

- Baseline v3 header references §8 and the v2 date, so a reader arriving after the refresh can see what moved and when.
- Wedge-table verdicts stay "NO flips": the November moves are real but do not close the local category gap, so the "empty locally" claim is retained on evidence rather than dropped for narrative convenience.
- The October §8 gap is disclosed in the delta section instead of being reconstructed; reconstructing it would have meant inventing history.
- Gap 5 (the stale "no competitive landscape document exists" claim in `social-media-positioning-status.md`) stays out of scope and is deferred, not silently dropped.

## Validation

- `ruff check src/` - PASS (all checks passed)
- `mypy src/` - PASS (234 source files, no issues)
- `pytest` full non-e2e suite - PASS (see validation_results for the exact counts)
- `pwsh scripts/maintenance/lint-ecl.ps1` - PASS (ECL lint passed; ps-antipattern scan 29 files, 0 failures)
- `npx tsc --noEmit` - PASS (site type check)
- `npx vitest run` - PASS (16 files, 145 tests)
- Negative control: none applicable - documentation-only change with no runtime behaviour, so there is no pre-fix artifact for the gates to reject.

## Next Step

- Archived. Next monthly refresh is due 2026-12-16; the 18-item re-check list in §8 is the input for that cycle.
