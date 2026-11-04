## Governance Audit Log

This log records every CEO Override applied to the two root configuration files,
`AGENTS.md` and `opencode.json`. Entries are appended chronologically and are never rewritten.

**Convention:** a change to either file is recorded here with its reason, actor, commit, and branch.

**Enforcement:** two layers exist, and they are not equal.

- `scripts/lint/validate-root-config.ps1`, wired as the `validate-root-config` hook in
  `.pre-commit-config.yaml` at the `commit-msg` stage. It inspects the staged file list and
  blocks the commit when the tag is missing. This is **local only** — `git commit --no-verify`
  bypasses it, and anyone who never ran `pre-commit install` is unaffected.
- There is **no server-side backstop**. No CI workflow checks for the tag, so a bypassed
  local hook produces no failure and no alert.

The hook validates only; it does not write this file. That is deliberate: the commit SHA does
not exist yet when a `commit-msg` hook runs, and a log that records a wrong SHA is worse than
one recorded a moment later by hand. Entries below are therefore appended manually, with the
real commit SHA.

Neither layer can see a **working-tree rewrite** (editor save, `git stash apply`,
`git restore`, or a second agent session sharing the checkout). Those create no commit, so no
hook fires — which is how `opencode.json` was replaced in place at 18:47 on 2026-10-28 with no
commit and no audit entry. No drift check for that exists yet.

### Entry format

```text
### YYYY-MM-DD HH:MM — [CEO-OVERRIDE: <reason>]
- **Actor:**
- **Files:**
- **Commit:**
- **Branch:**
```

## Entries

### 2026-11-04 19:44 — [CEO-OVERRIDE: Remove the @omniroute/opencode-plugin that never worked in this project (static provider.omniroute.models instead), delete the rule-enforcer plugin that PR #535 removed but the ce41c0a3 stash salvage re-added, and add the worktree directory config]

- **Actor:** jmlus <jmlus@example.com>
- **Files:** `opencode.json`, `docs/ARCHITECTURE-OMNIROUTE.md`, `.opencode/plugins/rule-enforcer.ts` (deleted)
- **Commit:** `942274e6`
- **Branch:** `chore/land-parked-work`

### 2026-11-04 19:45 — [CEO-OVERRIDE: Land parked worktree work by extracting the AGENTS.md sections 16 and 17 reference tables into docs/known-issues.md, docs/tool-issues.md, docs/creative-stack.md and docs/KEY-ROTATION.md]

- **Actor:** jmlus <jmlus@example.com>
- **Files:** `AGENTS.md`, `docs/KEY-ROTATION.md` (new), `docs/creative-stack.md` (new), `docs/tool-issues.md` (new), `docs/known-issues.md`, `docs/redesign/progress.md`, `.gitignore`
- **Commit:** `485887ec`
- **Branch:** `chore/land-parked-work`

### 2026-11-04 19:46 — [CEO-OVERRIDE: Externalize the open-design MCP entry to the global config so the committed opencode.json stops hard-coding absolute Windows paths to node.exe, the daemon cli.js and OD_DATA_DIR]

- **Actor:** jmlus <jmlus@example.com>
- **Files:** `opencode.json`, `docs/OPEN-DESIGN.md`
- **Commit:** `34bea55f`
- **Branch:** `chore/land-parked-work`
