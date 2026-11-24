# fix: add static/brand/ to Vercel ignore pattern and .vercelignore re-inclusions

**ID:** BUG-c29d1c8b9
**Date:** 2026-10-26
**Resolved:** unresolved
**Commit:** c29d1c8b9d1d728af396561413c2d5e47ad3726f
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

## Root Cause (filled by the resolving engineer)

Not stated in the commit message. The commit records the change below but no explicit cause; inferring one from the diff would be speculation.

_Source: commit c29d1c8b9d1d728af396561413c2d5e47ad3726f message; no cause stated._

## Fix (filled by the resolving engineer)

- Add static/brand/ to site_pattern in vercel-ignore-build.sh so pitch deck/brand template changes trigger builds
- Add !/static/brand/ negation patterns to .vercelignore to prevent ENOENT errors during Vercel build upload

_Source: commit c29d1c8b9d1d728af396561413c2d5e47ad3726f message (verbatim)._

## Files Changed

.vercelignore
scripts/deploy/vercel-ignore-build.sh

_Source: GitHub commit c29d1c8b9d1d728af396561413c2d5e47ad3726f file list, filtered to text/source files._

## Diagnostic Commands

Not recorded in the commit message.

## Verification

Not recorded in the commit message.

Commit is not present in the current origin/main history (possibly squash-merged or from a PR head); landing was not verified from this repository.

## Link an Issue

If this is a tracked bug, add Closes #N to a future commit or
file an issue and link it so the record becomes issue-backed.
