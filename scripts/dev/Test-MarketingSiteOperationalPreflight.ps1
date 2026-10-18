#!/usr/bin/env pwsh
# Dirty-Worktree Preflight Check
# Ensures sensitive files aren't modified without -AllowDirtyWorktree
# Wire: required before Start/Stop (manage-marketing-site.ps1 fails closed),
#       optional for Monitor/Status

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
    # git status --porcelain covers staged, unstaged AND untracked files.
    # (2026-10-17 fix: `git diff --name-only HEAD` missed untracked files.)
    $statusLines = @(git status --porcelain 2>$null | Where-Object { $_ })
    if ($LASTEXITCODE -ne 0) {
        Write-Host "git status failed - cannot verify worktree state (fail closed)"
        exit 1
    }

    if ($statusLines.Count -eq 0) {
        return $false  # No modifications, pass through
    }

    foreach ($line in $statusLines) {
        if ($line.Length -lt 4) { continue }
        $path = $line.Substring(3).Trim()
        if ($path -like '* -> *') {
            $path = (($path -split ' -> ')[-1]).Trim()
        }
        $path = $path.Trim('"')
        foreach ($pattern in $SensitivePatterns) {
            if ($path -like "$pattern*") {
                return $true  # Sensitive file modified
            }
        }
    }

    return $false  # Only non-sensitive files modified
}

Write-Host "Checking for sensitive file modifications..."

$sensitiveDirty = Test-SensitiveFilesModified

if ($sensitiveDirty -and -not $AllowDirtyWorktree) {
    Write-Host "Sensitive files modified without -AllowDirtyWorktree. "
    Write-Host "Please commit/Stash changes or rerun with -AllowDirtyWorktree."
    exit 1
}

if ($sensitiveDirty) {
    Write-Host "Sensitive files modified with -AllowDirtyWorktree (allowed)"
} else {
    Write-Host "No sensitive file modifications - preflight passed"
}

Write-Host "Preflight check complete"
exit 0
