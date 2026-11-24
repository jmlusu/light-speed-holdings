param(
    [string]$Issue = ""
)

# Capture a bug record only when the commit is linked to a GitHub issue, and
# populate every section from sourced content. Empty "To be filled" records are
# no longer written: 72 such placeholders had accumulated by 2026-11-24 because
# every conventional `fix:` commit produced a file that nobody completed.

$msg = git log -1 --pretty=%B 2>&1
$subject = ($msg -split [Environment]::NewLine | Select-Object -First 1)
$sha = git rev-parse HEAD 2>&1
$date = Get-Date -Format "yyyy-MM-dd"

$isIssueBacked = $false
if (-not $Issue) {
    $match = [regex]::Match($msg, '(Closes|Fixes) #(\d+)')
    if ($match.Success) {
        $Issue = $match.Groups[2].Value
        $isIssueBacked = $true
    }
}

if (-not $isIssueBacked) {
    Write-Host "Commit $sha has no linked issue; no bug record written."
    exit 0
}

$title = (gh issue view $Issue --json title --jq '.title' 2>&1) -join ""
$body = (gh issue view $Issue --json body --jq '.body' 2>&1) -join ""
$state = (gh issue view $Issue --json state --jq '.state' 2>&1) -join ""

$commitBody = (git show -s --format=%b HEAD 2>&1) -join "`n"
$changed = @(git diff-tree --no-commit-id --name-only -r HEAD 2>&1 | Where-Object { $_ })

if ($commitBody.Trim()) {
    $fix = $commitBody.Trim()
} else {
    $fix = "No fix detail was recorded in the commit message; see issue #${Issue}."
}

if ($changed.Count -gt 0) {
    $files = ($changed | Select-Object -First 40) -join "`n"
    if ($changed.Count -gt 40) {
        $files += "`n... and $($changed.Count - 40) more files"
    }
} else {
    $files = "No changed files were reported by git."
}

$md = @"
# $title

**ID:** BUG-${Issue}
**Date:** $date
**Resolved:** $state
**Commit:** $sha
**Issue:** #${Issue}

## Original Issue Body

$body

## Root Cause

See the linked issue above. No separate root-cause analysis was recorded for this fix.

## Fix

$fix

## Files Changed

$files

## Verification

Not recorded automatically. Add the commands and outcome during review.
"@

$dir = "knowledge/technology/bug-fixes"
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
$out = Join-Path $dir "BUG-${Issue}.md"
if (Test-Path $out) { Write-Host "BUG-${Issue} already captured; skipping"; exit 0 }

[System.IO.File]::WriteAllText($out, $md, [System.Text.UTF8Encoding]::new($false))
Write-Host "Captured BUG-${Issue}: $title"
