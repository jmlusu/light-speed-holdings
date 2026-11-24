# fix(orchestrator): co-locate escalation events with config path

**ID:** BUG-3eddc5a19
**Date:** 2026-10-04
**Resolved:** unresolved
**Commit:** 3eddc5a194bbf0d00d3598541c00c952d72a2365
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

## Root Cause (filled by the resolving engineer)

Recorded in the commit message: EscalationManager now derives its event-store path from config_path (events_path defaults to None) instead of a shared CWD-relative file, so each config path gets an isolated store and instances stop accumulating each other's events.

_Source: commit 3eddc5a194bbf0d00d3598541c00c952d72a2365 message (verbatim excerpt)._

## Fix (filled by the resolving engineer)

EscalationManager now derives its event-store path from config_path (events_path defaults to None) instead of a shared CWD-relative file, so each config path gets an isolated store and instances stop accumulating each other's events.
Also restores .gitignore from origin/main (clobbered in 3030ed02), keeps local-artifact additions, adds the required .mimocode block, and reverts orchestrator/approvals.yaml to origin/main (local daemon state).

_Source: commit 3eddc5a194bbf0d00d3598541c00c952d72a2365 message (verbatim)._

## Files Changed

.gitignore
src/ai_company/orchestrator/escalation.py
orchestrator/approvals.yaml

_Source: GitHub commit 3eddc5a194bbf0d00d3598541c00c952d72a2365 file list, filtered to text/source files._

## Diagnostic Commands

Not recorded in the commit message.

## Verification

Not recorded in the commit message.

Commit is not present in the current origin/main history (possibly squash-merged or from a PR head); landing was not verified from this repository.

## Link an Issue

If this is a tracked bug, add Closes #N to a future commit or
file an issue and link it so the record becomes issue-backed.
