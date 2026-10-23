<#
.SYNOPSIS
End-to-End Automated Git Merge Orchestrator with Auto-Fix Triggers.
.DESCRIPTION
Automates pre-merge validation, auto-fixing dirty states/submodules,
executing merges, handling conflict detection, and post-merge validation.
.PARAMETER TargetBranch
The branch to merge into (default: 'main').
.PARAMETER FeatureBranch
The feature branch to merge.
.PARAMETER AutoFix
If set, automatically stashes dirty states and updates submodules.
.PARAMETER TestCommand
Optional script block to execute test suite post-merge.
.EXAMPLE
    .\scripts\git\merge-orchestrator.ps1 -FeatureBranch feature/123-new-ui -AutoFix
.EXAMPLE
    .\scripts\git\merge-orchestrator.ps1 -FeatureBranch feature/456-fix-bug -TestCommand { python -m pytest tests/ -x -q }
#>
[CmdletBinding()]
param (
    [string]$TargetBranch = "main",
    [Parameter(Mandatory=$true)]
    [string]$FeatureBranch,
    [switch]$AutoFix,
    [scriptblock]$TestCommand = $null
)

$ErrorActionPreference = "Stop"

function Write-Header {
    param ([string]$Message)
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host " $Message" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
}

function Write-Step {
    param ([string]$Message)
    Write-Host "`n[CHECK] $Message" -ForegroundColor Yellow
}

function Write-Pass {
    param ([string]$Message)
    Write-Host "  [PASS] $Message" -ForegroundColor Green
}

function Write-Fix {
    param ([string]$Message)
    Write-Host "  [AUTO-FIX] $Message" -ForegroundColor Magenta
}

function Write-Fail {
    param ([string]$Message)
    Write-Host "  [FAIL] $Message" -ForegroundColor Red
    exit 1
}

# ==========================================
# CONCURRENCY GUARD & CHECKPOINT SETUP
# ==========================================
$lockFile = Join-Path (git rev-parse --git-dir 2>$null) "merge-orchestrator.lock"
$checkpointFile = Join-Path (git rev-parse --git-dir 2>$null) "merge-checkpoint.json"

# Check for existing lock
if (Test-Path $lockFile) {
    $lockContent = Get-Content $lockFile -Raw -ErrorAction SilentlyContinue
    Write-Host "`n  [ERROR] Another merge-orchestrator instance may be running." -ForegroundColor Red
    Write-Host "  Lock file: $lockFile" -ForegroundColor Red
    if ($lockContent) {
        Write-Host "  Lock content: $lockContent" -ForegroundColor Red
    }
    Write-Host "  If you are certain no other instance is running, remove the lock file:" -ForegroundColor Yellow
    Write-Host "    Remove-Item '$lockFile'" -ForegroundColor Yellow
    Write-Host "  Do NOT remove the lock if another orchestrator process is active." -ForegroundColor Yellow
    exit 1
}

# Create lock file with operation metadata
$operationId = [guid]::NewGuid().ToString()
$lockData = @{
    operationId = $operationId
    pid = $PID
    startTime = (Get-Date).ToUniversalTime().ToString("o")
    targetBranch = $TargetBranch
    featureBranch = $FeatureBranch
    host = $env:COMPUTERNAME
} | ConvertTo-Json -Compress
$lockData | Set-Content -Path $lockFile -Encoding UTF8

# Ensure lock is cleaned up on exit (even on error)
$cleanupLock = {
    if (Test-Path $lockFile) {
        $currentLock = Get-Content $lockFile -Raw -ErrorAction SilentlyContinue
        if ($currentLock -and $currentLock.Contains($operationId)) {
            Remove-Item -Path $lockFile -Force -ErrorAction SilentlyContinue
        }
    }
}
Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action $cleanupLock | Out-Null

# ==========================================
# PHASE 1: PRE-MERGE AUDIT & AUTO-FIX
# ==========================================
Write-Header "PHASE 1: PRE-MERGE AUDIT & REPOSITORY PREPARATION"

# 1. Working Directory Check & Auto-Stash
Write-Step "Checking working directory status..."
$dirtyStatus = git status --porcelain
$stashCreated = $false
$stashName = ""

if ($dirtyStatus) {
    if ($AutoFix) {
        $stashName = "autostash_pre_merge_$(Get-Date -Format 'yyyyMMdd_HHmmss')_${TargetBranch}"
        Write-Fix "Uncommitted changes detected. Auto-stashing as '$stashName'..."
        git stash push -u -m $stashName | Out-Null
        $stashCreated = $true
        Write-Pass "Working directory stashed successfully (including untracked files)."
    } else {
        Write-Fail "Working directory has uncommitted changes. Run with -AutoFix or stash manually."
    }
} else {
    Write-Pass "Working directory is clean."
}

# 2. Record Checkpoint (before any destructive operations)
Write-Step "Recording pre-operation checkpoint..."
$originalBranch = git rev-parse --abbrev-ref HEAD 2>&1
$originalSha = git rev-parse HEAD 2>&1
$submoduleCommits = git submodule status 2>$null
$mergeBaseSha = git merge-base $TargetBranch $FeatureBranch 2>$null
$targetSha = git rev-parse $TargetBranch 2>$null
$featureSha = git rev-parse $FeatureBranch 2>$null

$checkpoint = @{
    operationId = $operationId
    timestamp = (Get-Date).ToUniversalTime().ToString("o")
    originalBranch = $originalBranch
    originalSha = $originalSha
    targetBranch = $TargetBranch
    targetSha = $targetSha
    featureBranch = $FeatureBranch
    featureSha = $featureSha
    mergeBase = $mergeBaseSha
    stashCreated = $stashCreated
    stashName = $stashName
    submoduleCommits = if ($submoduleCommits) { $submoduleCommits -join "`n" } else { "" }
    workingTreeDirty = ($dirtyStatus -ne $null)
} | ConvertTo-Json -Depth 3

$checkpoint | Set-Content -Path $checkpointFile -Encoding UTF8
Write-Pass "Checkpoint recorded at: $checkpointFile"
Write-Host "  [CHECKPOINT] Operation ID: $operationId" -ForegroundColor Cyan
Write-Host "  [CHECKPOINT] Original branch: $originalBranch" -ForegroundColor Cyan
Write-Host "  [CHECKPOINT] Original SHA: $originalSha" -ForegroundColor Cyan
Write-Step "Checking git submodules..."
$submoduleStatus = git submodule status 2>$null
if ($LASTEXITCODE -eq 0 -and $submoduleStatus) {
    $dirtySubmodules = $submoduleStatus | Select-String -Pattern "^[+-U]"
    if ($dirtySubmodules) {
        if ($AutoFix) {
            Write-Fix "Submodules have dirty state. Running hard reset and clean before sync..."
            # Use -fd (not -fdx) to preserve ignored files like .env in submodules
            git submodule foreach --recursive "git reset --hard HEAD; git clean -fd" 2>&1 | Out-Null
            Write-Fix "Submodules hard-reset. Synchronizing and updating recursively..."
            git submodule sync --recursive | Out-Null
            git submodule update --init --recursive | Out-Null
            Write-Pass "Submodules updated and synchronized."
        } else {
            Write-Fail "Submodules have dirty/misaligned states. Run with -AutoFix or align manually."
        }
    } else {
        Write-Pass "Submodules are clean and synchronized."
    }
} else {
    Write-Pass "No submodules present or submodule check skipped."
}

# 3. Fetch Remote References
Write-Step "Fetching latest remote references..."
git fetch --all --prune | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Fail "Failed to fetch from remote origin."
}
Write-Pass "Remote references updated."

# 4. Divergence & Ancestry Audit
Write-Step "Validating branch ancestry and divergence..."
$mergeBase = git merge-base $TargetBranch $FeatureBranch 2>$null
if ($LASTEXITCODE -ne 0 -or -not $mergeBase) {
    Write-Fail "No common ancestor found between '$TargetBranch' and '$FeatureBranch'."
} else {
    Write-Pass "Common ancestor commit: $mergeBase"
}

$aheadCount = (git rev-list --count "$TargetBranch..$FeatureBranch" 2>$null).Trim()
$behindCount = (git rev-list --count "$FeatureBranch..$TargetBranch" 2>$null).Trim()
Write-Host "  [INFO] '$FeatureBranch' is $aheadCount commit(s) ahead and $behindCount commit(s) behind '$TargetBranch'." -ForegroundColor Yellow

# 5. Divergence Graph (guideline: map divergence before complex merge)
Write-Step "Displaying divergence graph for reference..."
git log --oneline -n 20 --all --graph -- "$TargetBranch" "$FeatureBranch" | Select-Object -First 30

# ==========================================
# PHASE 2: TARGET BRANCH PREPARATION
# ==========================================
Write-Header "PHASE 2: PREPARING TARGET BRANCH"

# Guideline: inspect stashes before branch switch
Write-Step "Inspecting existing stashes before branch switch..."
$stashList = git stash list
if ($stashList) {
    Write-Host "  [INFO] Existing stashes found:" -ForegroundColor Gray
    $stashList | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
}

Write-Step "Switching to target branch '$TargetBranch'..."
git checkout $TargetBranch | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Fail "Failed to checkout target branch '$TargetBranch'."
}

Write-Step "Pulling latest changes for '$TargetBranch'..."
git pull origin $TargetBranch | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Fail "Failed to pull latest changes for '$TargetBranch'."
}
Write-Pass "Target branch is up to date."

if ($submoduleStatus) {
    Write-Step "Re-verifying submodules on target branch..."
    git submodule update --init --recursive | Out-Null
    Write-Pass "Submodules updated for '$TargetBranch'."
}

# ==========================================
# PHASE 3: MERGE EXECUTION & CONFLICT HANDLING
# ==========================================
Write-Header "PHASE 3: EXECUTING MERGE"

Write-Step "Initiating non-fast-forward merge of '$FeatureBranch' into '$TargetBranch'..."
$mergeOutput = git merge --no-ff $FeatureBranch 2>&1
$mergeExitCode = $LASTEXITCODE

if ($mergeExitCode -ne 0) {
    Write-Host "`n  [WARNING] Merge conflicts detected!" -ForegroundColor Yellow
    Write-Step "Conflicted files list:"
    $conflictedFiles = git diff --name-only --diff-filter=U 2>$null
    if ($conflictedFiles) {
        foreach ($file in $conflictedFiles) {
            Write-Host "    - $file" -ForegroundColor Red
        }
    } else {
        Write-Host "    (Unable to list conflicted files)" -ForegroundColor Red
    }
    Write-Host "`n  [MERGE OUTPUT]" -ForegroundColor Yellow
    Write-Host "$mergeOutput" -ForegroundColor Gray
    Write-Host "`n  [ACTION REQUIRED] Please resolve conflicts in your editor." -ForegroundColor Yellow
    Write-Host "  After resolving conflicts, stage files with 'git add <file>' and run:" -ForegroundColor Yellow
    Write-Host "    git commit -m \"merge: integrate $FeatureBranch into $TargetBranch\"" -ForegroundColor Yellow
    if ($stashCreated) {
        Write-Host "`n  [REMINDER] Your pre-merge changes were stashed as '$stashName'." -ForegroundColor Cyan
        Write-Host "  To restore them after resolving conflicts, run:" -ForegroundColor Cyan
        Write-Host "    git stash pop" -ForegroundColor Cyan
    }
    exit 2
} else {
    Write-Pass "Merge executed cleanly without conflicts."
    Write-Host "`n  [MERGE OUTPUT]" -ForegroundColor Green
    Write-Host "$mergeOutput" -ForegroundColor Gray
}

# ==========================================
# PHASE 4: POST-MERGE VALIDATION & CLEANUP
# ==========================================
Write-Header "PHASE 4: POST-MERGE VALIDATION"

if ($TestCommand) {
    Write-Step "Executing test suite..."
    & $TestCommand
    if ($LASTEXITCODE -eq 0) {
        Write-Pass "Test suite completed successfully."
    } else {
        Write-Fail "Test suite failed post-merge. Please inspect errors before proceeding."
    }
} else {
    Write-Pass "No post-merge test command provided. Skipping test execution."
}

Write-Step "Displaying post-merge commit log..."
git log --oneline -n 5 --graph

Write-Host "`n========================================" -ForegroundColor Green
Write-Host " MERGE COMPLETED SUCCESSFULLY (LOCAL)" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# PR flow via gh (never push main directly - protected branch)
Write-Host "`n  [NEXT STEPS]" -ForegroundColor Cyan
Write-Host "  1. Push the feature branch to remote:" -ForegroundColor Cyan
Write-Host "       git push origin $FeatureBranch" -ForegroundColor Cyan
Write-Host "  2. Open a Pull Request targeting '$TargetBranch':" -ForegroundColor Cyan
Write-Host "       gh pr create --base $TargetBranch --head $FeatureBranch --title \"merge: $FeatureBranch into $TargetBranch\"" -ForegroundColor Cyan
Write-Host "  3. After PR approval and CI passes, merge via GitHub (auto-merge enabled)." -ForegroundColor Cyan

if ($stashCreated) {
    Write-Host "`n  [REMINDER] Your pre-merge changes were stashed as '$stashName'." -ForegroundColor Cyan
    Write-Host "  To restore them, run: git stash pop" -ForegroundColor Cyan
}

exit 0
