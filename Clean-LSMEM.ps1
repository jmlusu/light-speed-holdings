<# 
 .SYNOPSIS
   LS-MEM Phase 6 - Cleanup & verification automation
 .DESCRIPTION
   Runs the exact sequence of checks and housekeeping chores that
   close out the LS-MEM workstream.
 .NOTES
   * Requires git, uv, mypy, ruff, pytest and the ECL lint script to be
     on the PATH (as they are after `uv sync --extra dev`).
   * The script stops on the first failure - review the output and fix
     before re-running.
#>

# -------------------------------------------------
# 1. Confirm the LS-MEM commit
Write-Host "=== LS-MEM Phase 6 Cleanup ===" -ForegroundColor Cyan
Write-Host "1. Verifying latest commit..." -ForegroundColor Yellow
$lastCommit = git log --oneline -1
if (-not $lastCommit) {
    Write-Error "No commits found."
    exit 1
}
Write-Host "   $lastCommit" -ForegroundColor Green

# 2. Check working-tree state
Write-Host "2. Checking working-tree state..." -ForegroundColor Yellow
$status = git status --porcelain

# Expected untracked / modified patterns that are *allowed* after the close.
$allowedUntracked = @(
    '?? docs/architecture/adr/036-three-js-exception-immersive-homepage.md',
    '?? docs/research/immersive-3d-website-research.md',
    '?? harness/changes/parking/2026-09-26-immersive-3d-homepage-rebuild-full-webgl-lusion-igloo-class/',
    '?? src/components/ImmersiveStage.tsx',
    '?? src/components/home/',
    '?? src/data/homeImmersiveCopy.ts',
    '?? src/hooks/useScrollProgress.test.ts',
    '?? src/hooks/useScrollProgress.ts',
    '?? src/three/'
)

# Anything that is a *tracked* modification (starts with ` M `) must be absent
# except the known `open-design` submodule dirty flag.
$unexpected = $status | Where-Object {
    # tracked modifications
    ($_ -match '^ M ') -and
    # exclude the submodule line that is always present
    ($_ -notmatch '^ M open-design')
    # or untracked files that are NOT in the allowed list
} | Where-Object {
    # keep only untracked that are NOT in the allowed list
    ($_ -match '^\?\? ') -and
    ($_ -notin $allowedUntracked)
}

if ($unexpected) {
    Write-Warning "Unexpected changes:`n$($unexpected -join "`n")"
    exit 1
}
Write-Host "   Working tree clean (expected untracked files only)." -ForegroundColor Green

# 3. Run the final gate (mypy + ruff check + pytest)
Write-Host "3. Running final gate (mypy + ruff check + pytest)..." -ForegroundColor Yellow
& uv run mypy src/ | Out-Null
$exit = $LASTEXITCODE
if ($exit -ne 0) {
    Write-Error "mypy failed (exit $exit)."
    exit $exit
}
& uv run ruff check src/ | Out-Null
$exit = $LASTEXITCODE
if ($exit -ne 0) {
    Write-Error "ruff check failed (exit $exit)."
    exit $exit
}
& uv run pytest -q 2>&1 | Select-Object -Last 5
$exit = $LASTEXITCODE
if ($exit -ne 0) {
    Write-Error "pytest failed (exit $exit)."
    exit $exit
}
Write-Host "   Gate passed." -ForegroundColor Green

# 4. Lint-ECL archive gate
Write-Host "4. Running lint-ECL archive gate..." -ForegroundColor Yellow
& pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/lint-ecl.ps1
$eclExit = $LASTEXITCODE
if ($eclExit -ne 0) {
    Write-Error "ECL lint failed (exit $eclExit)."
    exit $eclExit
}
Write-Host "   ECL lint passed." -ForegroundColor Green

# 5. Clean up orphaned stashes
Write-Host "5. Dropping orphaned stashes..." -ForegroundColor Yellow
$stashes = git stash list
if ($stashes) {
    # Drop every stash that is present – the script’s earlier runs already
    # produced only the ones we want to keep, so a clean slate is safest.
    foreach ($stash in ($stashes -split "`n")) {
        $name = $stash.Split()[0]   # e.g. "stash@{0}"
        git stash drop $name | Out-Null
    }
}
Write-Host "   Stashes cleared." -ForegroundColor Green

# 6. Prune stale remote-tracking branches
Write-Host "6. Pruning stale remote-tracking branches..." -ForegroundColor Yellow
git remote prune origin | Out-Null
Write-Host "   Pruned." -ForegroundColor Green

# 7. (Optional) Delete the local ls-mem-phase3 branch
Write-Host "7. Remove local `ls-mem-phase3` branch?" -ForegroundColor Yellow
$confirm = Read-Host "(y/N)"
if ($confirm -match '^[Yy]$') {
    git branch -d ls-mem-phase3 | Out-Null
    Write-Host "   Branch deleted." -ForegroundColor Green
} else {
    Write-Host "   Keeping local branch." -ForegroundColor Yellow
}

Write-Host "=== LS-MEM Phase 6 Cleanup Complete ===" -ForegroundColor Cyan