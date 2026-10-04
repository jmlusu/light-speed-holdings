# Local runner for the canonical audit trail export (ECL:
# audit-export-reads-canonical-jsonl-trail).  The trail under .opencode/audit
# is gitignored, so CI can never export it - this script (optionally via
# Task Scheduler) is the exporter; CI only runs a freshness guard (decision D-a).
#
# Usage:
#   .\scripts\export-audit-evidence.ps1                 # today (UTC), no commit
#   .\scripts\export-audit-evidence.ps1 -Date 2026-10-03 # backfill a date
#   .\scripts\export-audit-evidence.ps1 -Commit -Push    # export + commit + push
param(
    [string]$Date = "",
    [switch]$Commit,
    [switch]$Push
)

$ErrorActionPreference = "Stop"

if ($Date -eq "") {
    $Date = (Get-Date).ToUniversalTime().ToString("yyyy-MM-dd")
}
if ($Date -notmatch '^\d{4}-\d{2}-\d{2}$') {
    Write-Error "Invalid -Date '$Date', expected YYYY-MM-DD"
    exit 1
}
if ($Push -and -not $Commit) {
    Write-Error "-Push requires -Commit"
    exit 1
}

$Root = Split-Path -Parent $PSScriptRoot
$EvidenceDir = Join-Path $Root "reports\evidence"
$ExportFile = Join-Path $EvidenceDir "audit-$Date.jsonl"
$RunLog = Join-Path $EvidenceDir "audit-export-runs.jsonl"
$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)

Push-Location $Root
try {
    uv run python -m ai_company.audit.export --date $Date --output $EvidenceDir
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Audit export failed (exit $LASTEXITCODE) - source trail missing?"
        exit $LASTEXITCODE
    }

    # Run log distinguishes a quiet day (events=0, file untouched) from a
    # missed run (no new line at all) - decision D-d.
    $Events = 0
    if (Test-Path -LiteralPath $ExportFile) {
        $Events = [System.IO.File]::ReadAllLines($ExportFile).Count
    }
    $RunAt = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    $Entry = '{"date":"' + $Date + '","events":' + $Events + ',"run_at":"' + $RunAt + '"}'
    [System.IO.File]::AppendAllText($RunLog, $Entry + "`n", $Utf8NoBom)
    Write-Host "Exported $Events events for $Date"

    if (-not $Commit) {
        return
    }

    # Refuse to fold local exports into someone else's in-progress merge.
    if (Test-Path -LiteralPath (Join-Path $Root ".git\MERGE_HEAD")) {
        Write-Error "Merge in progress - commit or abort the merge before -Commit"
        exit 1
    }

    if (Test-Path -LiteralPath $ExportFile) {
        git add -- $ExportFile
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
    git add -- $RunLog
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    $Staged = git diff --cached --name-only -- $ExportFile $RunLog
    if (-not $Staged) {
        Write-Host "Nothing to commit for $Date."
        return
    }

    git commit -m "audit: evidence export $Date ($Events events)"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    if ($Push) {
        $Branch = git rev-parse --abbrev-ref HEAD
        git push origin "HEAD:refs/heads/$Branch"
        if ($LASTEXITCODE -ne 0) {
            git pull --rebase --autostash origin $Branch
            if ($LASTEXITCODE -ne 0) {
                Write-Error "git pull --rebase failed; resolve manually, then push"
                exit $LASTEXITCODE
            }
            git push origin "HEAD:refs/heads/$Branch"
            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        }
    }
}
finally {
    Pop-Location
}
