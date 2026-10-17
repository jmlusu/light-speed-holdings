For **Committed Changes**, explicitly distinguish:

1. **Committed locally and pushed to GitHub**
   - Commits on the current branch that are already present on the upstream GitHub branch.
   - Report commit SHA, date, author, commit message, and concise summary of files/changes.

2. **Committed locally but NOT pushed**
   - Commits that exist in local HEAD/history but are ahead of the upstream GitHub branch.
   - Report each commit SHA, commit message, and what changed.
   - Clearly state: **"Committed locally, not yet on GitHub."**

3. **Committed on GitHub but NOT present locally**
   - If the remote branch is ahead, identify the remote commits missing locally.
   - Clearly state: **"On GitHub, not present in local branch."**

4. **Current HEAD**
   - Report the exact HEAD commit SHA and commit message.
   - State whether HEAD matches the GitHub upstream branch.

Do NOT classify a change as "committed" merely because files are currently present in the repository. A change is **committed** only if it exists in a Git commit.

Use:
- `git status`
- `git log`
- `git log <upstream>..HEAD`
- `git log HEAD..<upstream>`
- `git diff HEAD`
- `git diff --cached`
- `git diff <upstream>...HEAD`

Then report the results using this structure:

**COMMITTED**
- **On GitHub:** [count] commits
- **Local only:** [count] commits
- **GitHub only:** [count] commits
- **HEAD:** `[SHA]` — `[commit message]`
- **HEAD vs GitHub:** MATCH / LOCAL AHEAD / REMOTE AHEAD / DIVERGED

For every **local-only commit**, list:
`[SHA] | [date] | [commit message] | [change summary]`

For every **GitHub-only commit**, list:
`[SHA] | [date] | [commit message] | [change summary]`

The purpose is to make it immediately clear to the CEO **what has actually been committed, what has actually reached GitHub, and what still needs to be pushed or reconciled.**