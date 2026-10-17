Use this prompt:

Audit the repository’s Git state and report **Committed vs Staged vs Uncommitted/Untracked** changes.

Do not modify, stage, commit, reset, stash, or delete anything.

Check and reconcile:
1. **Committed** — changes already included in the current HEAD/latest commit and branch status.
2. **Staged** — changes in the Git index awaiting commit.
3. **Uncommitted** — modified/deleted files in the working tree but not staged.
4. **Untracked** — new files Git is not tracking.
5. **Ahead/Behind Remote** — compare the current branch with its upstream GitHub branch.
6. **Divergence/Conflicts** — identify merge conflicts, detached HEAD, or other abnormal Git state.

Use Git commands such as `git status`, `git diff`, `git diff --cached`, `git log`, and upstream comparison as needed.

Return a concise CEO-readable report with:

**Git State**
- Branch:
- HEAD:
- Remote/upstream:
- Ahead/behind:
- Overall status: CLEAN / CHANGES PENDING / CONFLICTED

**Committed**
- Commit:
- Summary:
- Files affected:

**Staged**
- Count:
- Files:
- Summary of changes:

**Uncommitted**
- Count:
- Files:
- Summary of changes:

**Untracked**
- Count:
- Files:

**Action Required**
- Clearly state exactly what, if anything, needs to be committed, reviewed, discarded, or investigated.

Do not assume that “working tree clean” means the repository is fully synchronized with GitHub. Verify both local Git state and remote tracking state.