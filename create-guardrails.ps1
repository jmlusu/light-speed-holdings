$dir  = 'C:\Users\jmlus\light-speed-holdings\.ai-company\constitution'
$path = Join-Path $dir '16-AGENT-GUARDRAILS.md'

if (Test-Path $path) { Write-Error "Already exists, not overwriting: $path"; return }
New-Item -ItemType Directory -Force -Path $dir | Out-Null

$content = @'
# 16 - Agent Guardrails

Read this before any git, PR, or CI work. Short always-on rules live in `AGENTS.md` under "Hard Rules"; this file holds the detail.

## Destructive actions
- Never delete, overwrite, or `git restore`/`git checkout` files you did not create in this session. This includes untracked files and pre-existing uncommitted changes.
- Before any removal, run `git status --short` and list what will be affected. If a file's origin is unclear, treat it as the user's and leave it alone.
- If you created a temp file (e.g. `gitstatus.txt`), delete only that file, by exact path.
- Do not `git add .` or `git add -A`. Stage files by explicit path.
- Ask before: `reset --hard`, `clean`, force-push, branch deletion, or bulk deletes.

## Hooks and quality gates
- Never use `--no-verify` without asking first. State which hook failed and why.
- If a hook fails for an environment reason (e.g. `[WinError 5]`), report it and ask. Do not bypass it.
- Do not commit files that trip the large-file hook without approval.
- No empty or "trigger CI" commits. To re-run CI, ask the user to re-run the job or use `gh run rerun`.
- Do not change `git config` (identity, hooks path). Use the existing identity.

## Debugging discipline
- Before editing code to fix a CI failure, run the cheap checks: `git ls-files <path>`, `git status`, and `.gitignore`. A file existing locally does not prove it exists in CI.
- Compare local and CI environments (tracked files, cwd, runtime, versions) before theorizing.
- No more than 2 fix attempts on the same hypothesis. Then stop and report what you have ruled out.
- Do not rewrite a test to make it pass unless the user approves the changed contract.

## CI and PR monitoring
- Open PRs with `gh pr create`. Pushing a branch and printing a `/pull/new/` URL is not creating a PR.
- Observe CI with `gh pr checks <n>` or `gh run view`. `webfetch` on GitHub pages is not reliable for check status.
- If you cannot read CI status, say so and ask for `gh auth login` or pasted output. Do not fall back to re-running local tests and calling it monitoring.
- Do not search config files or env for tokens (`grep GITHUB_TOKEN`, etc.). Ask the user for access.

## Reporting
- "Done" means verified in the target environment (CI included). "Local only" means verified on this machine. "Unverified" means not checked.
- Never write "all gates green" or "PR created" unless command output in this session shows it.
- If the task is incomplete or blocked, lead with that.

## Budget
- Do not re-run the same verification (`vitest`, `tsc`, `vite build`) unless the code changed since the last run.
- Do not fetch the same URL repeatedly. If the page did not change state after 2 fetches, escalate.
'@

[System.IO.File]::WriteAllText($path, $content, (New-Object System.Text.UTF8Encoding($false)))
Get-Item $path | Select-Object FullName, Length
