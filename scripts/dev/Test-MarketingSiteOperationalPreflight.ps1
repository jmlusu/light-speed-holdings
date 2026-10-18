#!/usr/bin/env pwsh
# Dirty-Worktree Preflight Check
# Ensures sensitive files aren't modified without -AllowDirtyWorktree
# Wire: required before Start/Stop, optional for Monitor

param(
    [switch]$AllowDirtyWorktree
)

# Site-sensitive path patterns (per 2026-10-17 marketing site operations plan)
$SensitivePatterns = @(
    "src/",
    "public/",
    "index.html",
    "package.json",
    "bun.lock",
    "vite.config.ts",
    ".github/workflows/site-principles-gate.yml"
)

function Test-SensitiveFilesModified {
    # Check git diff for modified files in sensitive paths
    $modifiedFiles = @(cmd /c "git diff --name-only HEAD" 2>$null | Where-Object { $_ })

    if ($modifiedFiles.Count -eq 0) {
        return $false  # No modifications, pass through
    }

    foreach ($file in $modifiedFiles) {
        foreach ($pattern in $SensitivePatterns) {
            if ($file -like "$pattern*") {
                return $true  # Sensitive file modified
            }
        }
    }

    return $false  # Only non-sensitive files modified
}

Write-Host "Checking for sensitive file modifications..."

if (-not $AllowDirtyWorktree) {
    if (Test-SensitiveFilesModified) {
        Write-Host "Sensitive files modified without -AllowDirtyWorktree. "
        Write-Host "Please commit/Stash changes or rerun with -AllowDirtyWorktree."
        exit 1
    } else {
        Write-Host "No sensitive file modifications detected - preflight passed"
    }
} else {
    if (Test-SensitiveFilesModified) {
        Write-Host "Sensitive files modified with -AllowDirtyWorktree (allowed)"
    } else {
        Write-Host "No sensitive file modifications - preflight passed"
    }
}

Write-Host "Preflight check complete"
