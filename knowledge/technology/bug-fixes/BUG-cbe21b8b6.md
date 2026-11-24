# fix(llm): let callers override cache cap and type the budget level

**ID:** BUG-cbe21b8b6
**Date:** 2026-11-10
**Resolved:** unresolved
**Commit:** cbe21b8b6f2d17900f04d07ba496efc6b16afa1d
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

## Root Cause (filled by the resolving engineer)

Recorded in the commit message: 1. The tracker could not forward a cap override: check_cache_budget(day) was hard-wired to DEFAULT_CACHE_READ_CAP, so no caller could tighten or loosen the limit without editing source. It now accepts cap and forwards it unchanged to the analytics ladder; a non-positive cap short-circuits to ok and never blocks.

_Source: commit cbe21b8b6f2d17900f04d07ba496efc6b16afa1d message (verbatim excerpt)._

## Fix (filled by the resolving engineer)

Closes two gaps from the cache-cap audit.
1. The tracker could not forward a cap override: check_cache_budget(day) was hard-wired to DEFAULT_CACHE_READ_CAP, so no caller could tighten or loosen the limit without editing source. It now accepts cap and forwards it unchanged to the analytics ladder; a non-positive cap short-circuits to ok and never blocks.
2. CacheBudgetStatus.level was an untyped str, so a typo like 'blok' would fail open silently - the task would keep running with a dead budget gate. It is now Literal['ok','warn','compact','block'], so mypy rejects a bad level at build time.
Fail-open now reports the caller's cap instead of a fabricated default, so a status object never lies about the limit it was measured against.
Tests: 27 -> 31. No call site changed - the cap is exposed, not yet wired to a dashboard or CLI setting.

_Source: commit cbe21b8b6f2d17900f04d07ba496efc6b16afa1d message (verbatim)._

## Files Changed

src/ai_company/data/cost_analytics.py
src/ai_company/llm/cost_tracker.py
tests/unit/test_cache_budget.py

_Source: GitHub commit cbe21b8b6f2d17900f04d07ba496efc6b16afa1d file list, filtered to text/source files._

## Diagnostic Commands

2. CacheBudgetStatus.level was an untyped str, so a typo like 'blok' would fail open silently - the task would keep running with a dead budget gate. It is now Literal['ok','warn','compact','block'], so mypy rejects a bad level at build time.

## Verification

Not recorded in the commit message.

Commit is not present in the current origin/main history (possibly squash-merged or from a PR head); landing was not verified from this repository.

## Link an Issue

If this is a tracked bug, add Closes #N to a future commit or
file an issue and link it so the record becomes issue-backed.
