# Anti-Pattern: Unstable Hook Execution & Stash Timeout

## Symptom
Pre-commit hook silently reverts all unstaged tracked edits (prune deletions, logo overwrites, script rewrites). The change that was committed appears correct on the machine that produced it, but CI checks out a clean tree missing those edits. The failure is invisible on the machine that produced the commit.

## Root Cause
The pre-commit hook runs a **slow synchronous post-commit graph-rebuild** (~27 min run time). This blocks the post-commit stage before pre-commit can restore its stash. The hook process is killed (shell timeout) and the stash restore never runs, silently reverting every unstaged tracked edit.

## Anti-Pattern Code
```powershell
# BAD: Slow synchronous hook blocks stash restore
# Pre-commit hook with ~27 min run time blocks pipeline
& $harnessEvolve check -Reason "some reason"
# If this takes > typical shell timeout, stash restore fails silently

# CORRECT: Background the hook so it exits quickly (<1 s)
# and the stash restore always completes
& $harnessEvolve check -Reason "some reason" &
# or wrap in a timeout so hook exits quickly
```

## Fix Pattern
1. **Background long-running hooks** so they exit quickly (<1 s)
2. **Use a backgrounded hook wrapper** so the hook exits in <1 s and the stash restore always completes
3. **Fix root cause separately** (c7609025): background the rebuild hook via a backgrounded hook wrapper

## Reference Bugs
- BUG-9d688faee: Slow synchronous post-commit graph-rebuild hook (~27 min run) blocked the post-commit stage before pre-commit could restore its stash

## Prevention
- Never let a post-commit hook block the pipeline for 27 minutes
- Background long-running hooks so they exit quickly (<1 s)
- Ensure the stash restore always completes before the hook session ends
- If a hook must run slowly, wrap it so it doesn't block the stash restore cycle
- Reference: Root cause of the loss class was fixed separately in c7609025 by backgrounding that rebuild hook via a backgrounded hook wrapper so the hook exits in <1 s and the stash restore always completes.
