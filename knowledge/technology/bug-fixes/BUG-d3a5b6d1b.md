# fix: add Vite dev server startup procedure and process manager guard

**ID:** BUG-d3a5b6d1b
**Date:** 2026-11-12
**Resolved:** resolved
**Commit:** d3a5b6d1b38941ae93f28a50d2e4936410be2842
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

## Root Cause (filled by the resolving engineer)

Not stated in the commit message. The commit records the change below but no explicit cause; inferring one from the diff would be speculation.

_Source: commit d3a5b6d1b38941ae93f28a50d2e4936410be2842 message; no cause stated._

## Fix (filled by the resolving engineer)

- Create START_VITE.md with startup instructions for Windows PowerShell
- Update README.md Development section with correct Vite ports (1441/1440)
- Add GitHub Actions CI check to verify Vite dev server availability
- Install pm2 for auto-restart across sessions
- Prevent recurrence of Vite process termination between sessions

_Source: commit d3a5b6d1b38941ae93f28a50d2e4936410be2842 message (verbatim)._

## Files Changed

.github/workflows/verify-vite.yml
.pre-commit-config.yaml
README.md
START_VITE.md

_Source: GitHub commit d3a5b6d1b38941ae93f28a50d2e4936410be2842 file list, filtered to text/source files._

## Diagnostic Commands

Not recorded in the commit message.

## Verification

- Add GitHub Actions CI check to verify Vite dev server availability

Commit is present in the current origin/main history; CI was not re-run for this record.

## Link an Issue

If this is a tracked bug, add Closes #N to a future commit or
file an issue and link it so the record becomes issue-backed.
