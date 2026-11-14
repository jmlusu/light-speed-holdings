<#
.SYNOPSIS
    Orphaned tool-call sweeper for opencode.db (dry-run default; read-only otherwise).

.DESCRIPTION
    Reports `part` rows whose tool status is still `running`/`pending`
    (baseline: running 93, pending 2). With -Apply (maintenance window,
    snapshot required) it marks stale rows as error with an orphaned
    marker. Never deletes rows — analytics must still see them.

    Apply SQL (after snapshot):
      UPDATE part SET data = json_set(data, '$.state.status', 'error',
        '$.state.error', 'orphaned: running exceeded 1h (sweeper ' || date('now') || ')',
        '$.state.orphaned', 1),
        time_updated = (strftime('%s','now') * 1000)
      WHERE json_extract(data,'$.type')='tool'
        AND json_extract(data,'$.state.status')='running'
        AND (COALESCE(time_updated, time_created) < (strftime('%s','now') - 3600) * 1000);

.EXAMPLE
    pwsh -File scripts/maintenance/sweep-orphaned-tool-calls.ps1

.EXAMPLE
    pwsh -File scripts/maintenance/sweep-orphaned-tool-calls.ps1 -Apply
#>
param(
    [string]$DbPath = "$env:USERPROFILE\.local\share\opencode\opencode.db",
    [switch]$Apply
)

$ErrorActionPreference = "Stop"

$dryRunSql = @"
SELECT json_extract(data,'$.tool') AS tool,
       json_extract(data,'$.state.status') AS status,
       COUNT(*) AS n
FROM part
WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.state.status') IN ('running','pending')
GROUP BY tool, status ORDER BY n DESC;
"@

Write-Output "--- orphaned rows by (tool, status) ---"
& sqlite3 -readonly $DbPath $dryRunSql
Write-Output ("Exit: {0}" -f $LASTEXITCODE)

if (-not $Apply) {
    Write-Output "DRY-RUN. Re-run with -Apply in a maintenance window (OpenCode closed, snapshot taken)."
    exit 0
}

$writers = Get-Process -Name "opencode" -ErrorAction SilentlyContinue
if ($writers) {
    Write-Error "OpenCode process still running. Close it before applying the sweep."
    exit 1
}
$applySql = @"
UPDATE part
SET data = json_set(data, '$.state.status', 'error',
  '$.state.error', 'orphaned: exceeded TTL without terminal update (sweeper ' || date('now') || ')',
  '$.state.orphaned', 1),
  time_updated = (strftime('%s','now') * 1000)
WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.state.status')='running'
  AND (COALESCE(time_updated, time_created) < (strftime('%s','now') - 3600) * 1000);
UPDATE part
SET data = json_set(data, '$.state.status', 'error',
  '$.state.error', 'orphaned: pending exceeded 24h (sweeper ' || date('now') || ')',
  '$.state.orphaned', 1),
  time_updated = (strftime('%s','now') * 1000)
WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.state.status')='pending'
  AND (COALESCE(time_updated, time_created) < (strftime('%s','now') - 86400) * 1000);
SELECT json_extract(data,'$.state.status') AS st, COUNT(*) FROM part
 WHERE json_extract(data,'$.type')='tool' GROUP BY st;
"@
& sqlite3 $DbPath $applySql
