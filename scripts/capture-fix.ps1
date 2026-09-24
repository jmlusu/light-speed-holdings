param(
    [string]$Issue = ""
)

# Capture a bug-fix record whenever a commit closes a GitHub issue.
# The record lands in knowledge/technology/bug-fixes/ and is
# automatically indexed by the post-commit graphify hook, so the
# org's knowledge graph (graphify-out/) stays current without
# anyone manually writing a known-issues document.

$msg = git log -1 --pretty=%B 2>&1
if (-not $Issue) {
    $match = [regex]::Match($msg, '(Closes|Fixes) #(\d+)')
    if (-not $match.Success) { exit 0 }
    $Issue = $match.Groups[2].Value
}

$dir = "knowledge/technology/bug-fixes"
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
$out = Join-Path $dir "BUG-${Issue}.md"
if (Test-Path $out) { Write-Host "BUG-${Issue} already captured; skipping"; exit 0 }

$title = (gh issue view $Issue --json title --jq '.title' 2>&1) -join ""
$body = (gh issue view $Issue --json body --jq '.body' 2>&1) -join ""
$state = (gh issue view $Issue --json state --jq '.state' 2>&1) -join ""
$sha = git rev-parse HEAD 2>&1
$date = Get-Date -Format "yyyy-MM-dd"

$md = @"
# `${title}

**ID:** BUG-${Issue}
**Date:** ${date}
**Resolved:** ${state}
**Commit:** `${sha}
**Issue:** #${Issue}

## Original Issue Body

${body}

## Root Cause (filled by the resolving engineer)

To be filled

## Fix (filled by the resolving engineer)

To be filled

## Files Changed

To be filled

## Diagnostic Commands

To be filled

## Verification

To be filled
"@

Set-Content -Path $out -Value $md -Encoding UTF8
Write-Host "Captured BUG-${Issue}: ${title}"
