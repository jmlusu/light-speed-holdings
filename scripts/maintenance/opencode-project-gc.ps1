<#
.SYNOPSIS
    Project GC dry-run for opencode.db (read-only; never deletes).

.DESCRIPTION
    Lists session-less `project` rows (baseline: 67 of 72) that would be
    candidates for deletion in a maintenance window. Deletion requires
    FK probes (project_directory/worktree/todo/permission joins) and a
    pre-change snapshot; see docs/opencode-db-p0-runbook.md.

.EXAMPLE
    pwsh -File scripts/maintenance/opencode-project-gc.ps1
#>
param(
    [string]$DbPath = "$env:USERPROFILE\.local\share\opencode\opencode.db",
    [int]$MinAgeDays = 30
)

$ErrorActionPreference = "Stop"
if (-not (Test-Path -LiteralPath $DbPath)) {
    Write-Error "DB not found: $DbPath"; exit 1
}
$sql = @"
SELECT p.id, p.worktree, p.name AS project_name, p.time_created,
       (SELECT COUNT(*) FROM session s WHERE s.project_id=p.id) AS v1_sessions,
       (SELECT COUNT(*) FROM session_v2 s WHERE s.project_id=p.id) AS v2_sessions
FROM project p
WHERE NOT EXISTS (SELECT 1 FROM session s WHERE s.project_id=p.id)
  AND NOT EXISTS (SELECT 1 FROM session_v2 s WHERE s.project_id=p.id)
  AND p.time_created < (strftime('%s','now') - $MinAgeDays*86400) * 1000
ORDER BY p.time_created;
"@
Write-Output "--- session-less projects older than $MinAgeDays days ---"
& sqlite3 -readonly $DbPath $sql
