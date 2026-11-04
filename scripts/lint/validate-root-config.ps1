# validate-root-config.ps1
#
# Enforces the CEO Override Governance Protocol for root configuration files.
# See AGENTS.md section 18 and docs/governance-audit.md.
#
# Behaviour
#   - Reads the staged file list for the commit in progress.
#   - If neither AGENTS.md nor opencode.json is staged: exit 0 (no-op).
#   - If either is staged and the commit message does NOT contain a
#     "[CEO-OVERRIDE: <reason>]" tag: print guidance and exit 1 (blocks).
#   - If either is staged and the tag IS present: print confirmation and exit 0.
#
# This script validates only. It does not write to docs/governance-audit.md;
# the audit entry is recorded by the Human CEO's commit companion because the
# final commit SHA does not exist yet at commit-msg time.

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$CommitMsgFile
)

$ErrorActionPreference = 'Stop'

$protectedFiles = @('AGENTS.md', 'opencode.json')

function Get-RepoRoot {
    $root = & git rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($root)) {
        return $null
    }
    return $root.Trim()
}

$repoRoot = Get-RepoRoot
if (-not $repoRoot) {
    Write-Host "validate-root-config: not inside a git repository; skipping."
    exit 0
}

Push-Location $repoRoot
try {
    # Resolve the commit message file. pre-commit runs this hook with
    # pass_filenames: false at the commit-msg stage, so no path is supplied.
    if ([string]::IsNullOrWhiteSpace($CommitMsgFile)) {
        $gitDir = (& git rev-parse --git-dir 2>$null)
        if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($gitDir)) {
            Write-Host "validate-root-config: cannot resolve .git directory; skipping."
            exit 0
        }
        $gitDir = $gitDir.Trim()
        if (-not [System.IO.Path]::IsPathRooted($gitDir)) {
            $gitDir = Join-Path $repoRoot $gitDir
        }
        $CommitMsgFile = Join-Path $gitDir 'COMMIT_EDITMSG'
    }

    if (-not (Test-Path -LiteralPath $CommitMsgFile)) {
        Write-Host "validate-root-config: no commit message file at '$CommitMsgFile'; skipping."
        exit 0
    }

    $staged = @(& git diff --cached --name-only 2>$null)
    if ($LASTEXITCODE -ne 0) {
        Write-Host "validate-root-config: unable to read staged files; skipping."
        exit 0
    }

    $touched = @()
    foreach ($file in $protectedFiles) {
        foreach ($stagedFile in $staged) {
            $normalized = ($stagedFile -replace '\\', '/').Trim()
            if ($normalized -eq $file) {
                $touched += $file
            }
        }
    }

    if ($touched.Count -eq 0) {
        exit 0
    }

    $message = Get-Content -LiteralPath $CommitMsgFile -Raw
    if ($null -eq $message) { $message = '' }

    $tagPattern = '\[CEO-OVERRIDE:\s*\S[^\]]*\]'
    $tagMatch = [System.Text.RegularExpressions.Regex]::Match($message, $tagPattern)

    $fileList = ($touched | Sort-Object -Unique) -join ', '

    if (-not $tagMatch.Success) {
        Write-Host ''
        Write-Host 'BLOCKED: CEO override required for root configuration files.' -ForegroundColor Red
        Write-Host ''
        Write-Host "  Staged root config files: $fileList"
        Write-Host ''
        Write-Host '  AGENTS.md section 18 requires every commit that modifies AGENTS.md or'
        Write-Host '  opencode.json to carry an explicit override tag in its message:'
        Write-Host ''
        Write-Host '      [CEO-OVERRIDE: <operational reason>]'
        Write-Host ''
        Write-Host '  Only the Human CEO supplies this reason. Agents must not add it on'
        Write-Host '  their own authority. Unstage the file(s) or amend the message.'
        Write-Host ''
        exit 1
    }

    Write-Host "validate-root-config: CEO override tag present for $fileList - allowed."
    Write-Host "  reason: $($tagMatch.Value)"
    exit 0
}
finally {
    Pop-Location
}
