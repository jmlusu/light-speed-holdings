# fix(dashboard): close unterminated alpine:init block in command-bar.js

**ID:** BUG-da80ea477
**Date:** 2026-09-26
**Resolved:** closed
**Commit:** `da80ea477b75c0d9625d215e8d07933ddfc02da0`
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

## Root Cause

`src/ai_company/dashboard/static/js/command-bar.js` opened
`document.addEventListener('alpine:init', (event) => {` but never closed it — the
file ended with the callback body and the `addEventListener` call both still open
(missing the final `});`). The browser therefore aborted the whole script during
parse, so the `alpine:init` handler never ran and the ⌘K command bar never
registered (`bindHotkeys()` / `groupedResults()` / `execute()` were all dead).
`node --check` reproduced it: `SyntaxError: missing ) after argument list`.

## Fix

Added the missing `});` at end of file to close the `alpine:init` listener.

## Files Changed

`src/ai_company/dashboard/static/js/command-bar.js`

## Diagnostic Commands

```powershell
node --check src/ai_company/dashboard/static/js/command-bar.js   # was exit 1
uv run graphify query "command-bar hotkeys execute"
```

## Verification

```powershell
node --check src/ai_company/dashboard/static/js/command-bar.js   # exit 0
```

Graph re-index after `da80ea4` shows 62 `command-bar*` nodes including
`bindHotkeys()` (L53), `close()` (L91), `groupedResults()` (L110),
`debouncedSearch()` (L138), `execute()` (L148). Pre-commit hooks passed on
re-stage; post-commit `capture bug-fix record` + `rebuild-graphify-graph` Passed.

## Pattern

An unterminated top-level listener swallows the entire script file, not just the
missing block — one missing `});` silently kills every feature in the file. Keep
`node --check` (or an equivalent parse gate) in the dashboard lint path so this
fails at commit time instead of at runtime.

## Link an Issue

If this is a tracked bug, add Closes #N to a future commit or
file an issue and link it so the record becomes issue-backed.
