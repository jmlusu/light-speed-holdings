param(
    [string]$Issue = ""
)

# Capture a bug-fix record whenever a commit closes a GitHub issue
# OR uses the conventional `fix:` prefix (conventional commits
# semantically denote a bug fix). The record lands in
# knowledge/technology/bug-fixes/ and is automatically indexed by
# the post-commit graphify hook, so the org knowledge graph stays
# current without anyone manually writing a known-issues document.

$msg = git log -1 --pretty=%B 2>&1
$subject = ($msg -split [Environment]::NewLine | Select-Object -First 1)
$sha = git rev-parse HEAD 2>&1
$shortSha = $sha.Substring(0, [Math]::Min(9, $sha.Length))
$date = Get-Date -Format "yyyy-MM-dd"

$isIssueBacked = $false
if (-not $Issue) {
    $match = [regex]::Match($msg, '(Closes|Fixes) #(\d+)')
    if ($match.Success) {
        $Issue = $match.Groups[2].Value
        $isIssueBacked = $true
    }
}

if (-not $Issue) {
    if ($subject -notmatch '^fix(\([^)]*\))?:') { exit 0 }
    $Issue = $shortSha
    $isIssueBacked = $false
}

$dir = "knowledge/technology/bug-fixes"
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
$out = Join-Path $dir "BUG-${Issue}.md"
if (Test-Path $out) { Write-Host "BUG-${Issue} already captured; skipping"; exit 0 }

if ($isIssueBacked) {
    $title = (gh issue view $Issue --json title --jq '.title' 2>&1) -join ""
    $body = (gh issue view $Issue --json body --jq '.body' 2>&1) -join ""
    $state = (gh issue view $Issue --json state --jq '.state' 2>&1) -join ""
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
} else {
    $md = @"
# ${subject}

**ID:** BUG-${Issue}
**Date:** ${date}
**Resolved:** unresolved
**Commit:** `${sha}
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

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

## Link an Issue

If this is a tracked bug, add `Closes #N` to a future commit or
file an issue and link it so the record becomes issue-backed.
"@
}

Set-Content -Path $out -Value $md -Encoding UTF8
if ($isIssueBacked) {
    Write-Host "Captured BUG-${Issue}: ${title}"
} else {
    Write-Host "Captured BUG-${Issue} (no issue): ${subject}"
}
