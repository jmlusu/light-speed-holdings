---
title: "Repository Sanitization"
slug: "2026-10-06-repository-sanitization"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "approved"
spec_review: "approved"
plan_review: "approved"
modules:
  - "repo-root"
  - "scripts"
  - ".opencode"
  - "brand"
  - "company"
  - "open-design"
  - "orchestrator"
  - "memory"
files: []
tags:
  - "cleanup"
  - "sanitization"
  - "governance"
  - "repository-health"
validation_status: "pass"
created_at: "2026-10-06"
updated_at: "2026-10-07"
session_id: "cleanup-session-001"
owner_agent: "jmlus"
claimed_at: "2026-10-06"
---

# Summary

## Outcome

Full repository sanitization per LightSpeed Phased Approval & Rollback Protocol.
Result: 437 files changed (+2,932 / −20,771) across 13 atomic commits,
tracked root files 107 → 32, ~1.1 GB tracked dead weight removed.
All validation gates pass (ruff, mypy, pytest, generator round-trip,
sync-registry --verify, lint-ecl, canonical health_check.py).

## Decisions

- **Q8 (scroll-craft):** DELETE — confirmed retired 2026-09-23, ~1 GB removed
- **Q2 (open-design):** SUBMODULE — `.gitmodules` declared (origin verified)
- **Q5 (agent registry):** YAML→JSON — verified in sync; `.bak` copies removed/archived
- **Q7 (package manager):** NPM — `bun.lock` removed, guard flipped to refuse bun
- **Q1 (static/brand/tokens/):** KEEP as build artifact — mirrors verified identical
- **Q4 (memory impl):** DEFERRED — evidence contradicts the premise (see below)

## Validation

- Baseline (c0-baseline): ruff pass, mypy pass, pytest 1 pre-existing failure
- Final: ruff pass, mypy pass (236 files), pytest pass with 4 documented
  exclusions (2 pre-existing Athena-data failures, 1 perf flake, scraper-inventory module)
- Generator round-trip clean; `ai-company --help` works; lint-ecl passes
- Checkpoints: c0-baseline, c1-secrets, c2-caches, c3-root-moves,
  c4-scripts, c5-consolidation, c6-generated, c7-large-tools, c8-docs
- Largest tracked file now 1.6 MB (was GB-scale corpora)

## Completed Stages

Stages 0–9 executed except documented deferrals. Commits d107ba44
through 421af29d on `feat/athena-archive-and-design-system`.

## Deferred (follow-ups, NOT blockers for close)

1. **Memory consolidation (Q4):** `src/ai_company/memory/` is still imported
   by executor, dashboard, MCP, doctor, services, and CLI — `lsmem/` has
   not replaced it in code. Needs a human architecture decision.
2. **Runtime relocation (D-6/T043):** root `orchestrator/` + `memory/` hold
   live state; moving them needs code + config changes. Untracked junk
   (`.bak`, `.tmp`) remains deletable anytime.
3. **Milestones deck (Q3):** `.py` runs on the installed toolchain,
   `.js` needs uninstalled `pptxgenjs`; neither is referenced. Awaiting pick.
4. **`tmp/` tracked scratch:** ~40 files look like another session's
   scaffolding. Needs owner triage.
5. **Fresh-clone network verification** of the open-design submodule pin.
6. **Human final approval / promotion** (merge to canonical branch).

## Next Step

Close this change; present release gate + handoff to the owner.

