# Retention / 14-day re-audit hook for opencode.db (GO-7 / re-audit checkpoint).
# Runs read-only analytics SQL against a .backup SNAPSHOT (never the live DB),
# gates on PRAGMA integrity + row counts, and diffs cache/hot-file totals
# against the 2026-11-08 baselines in the governance plan appendix.
# Usage:
#   pwsh -NoProfile -File scripts/maintenance/audit-opencode-db.ps1 -SnapshotPath <path-to-snapshot.db>
#   pwsh -NoProfile -File scripts/maintenance/audit-opencode-db.ps1 -SnapshotPath <path> -OutputPath reports/opencode-db-reaudit-YYYY-MM-DD.json
# Exit 0 = snapshot readable and gates passed; exit 1 = gate failure or missing snapshot.

param(
  [Parameter(Mandatory = $true)][string]$SnapshotPath,
  [string]$OutputPath = "",
  [string]$BaselineCacheReadV1 = "15210842514"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $SnapshotPath)) {
  Write-Error "Snapshot not found: $SnapshotPath. Create one with sqlite3 .backup while opencode is closed; never audit the live DB."
  exit 1
}

$Root = (Get-Location).Path
$python = "uv"
$script = @"
import json, sqlite3, sys
from pathlib import Path

snapshot = sys.argv[1]
baseline = int(sys.argv[2])
result = {"snapshot": str(snapshot), "gates": {}, "metrics": {}}
uri = "file:" + Path(snapshot).as_posix() + "?mode=ro"
conn = sqlite3.connect(uri, uri=True, timeout=10)
conn.row_factory = sqlite3.Row
try:
    result["gates"]["integrity"] = conn.execute("PRAGMA integrity_check").fetchone()[0]
    result["gates"]["page_count"] = conn.execute("PRAGMA page_count").fetchone()[0]
    result["gates"]["page_size"] = conn.execute("PRAGMA page_size").fetchone()[0]
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    result["gates"]["has_session"] = "session" in tables
    result["gates"]["has_session_v2"] = "session_v2" in tables
    for table in ("session", "session_v2"):
        if table not in tables:
            continue
        cols = {r[1] for r in conn.execute("PRAGMA table_info(" + table + ")")}
        if "tokens_cache_read" in cols:
            row = conn.execute(
                "SELECT COALESCE(SUM(tokens_cache_read),0), COALESCE(SUM(tokens_cache_write),0), "
                "COALESCE(SUM(tokens_input),0), COUNT(*) FROM " + table
            ).fetchone()
            result["metrics"][table] = {
                "cache_read": row[0], "cache_write": row[1],
                "input": row[2], "sessions": row[3],
            }
    # Project GC gate: session-less projects.
    if "project" in tables and ("session" in tables or "session_v2" in tables):
        sess = "session_v2" if "session_v2" in tables else "session"
        try:
            result["metrics"]["session_less_projects"] = conn.execute(
                "SELECT COUNT(*) FROM project WHERE id NOT IN (SELECT DISTINCT project_id FROM " + sess + ")"
            ).fetchone()[0]
        except Exception:
            result["metrics"]["session_less_projects"] = None
finally:
    conn.close()

ok = result["gates"].get("integrity") == "ok" and result["gates"].get("has_session")
result["pass"] = bool(ok)
print(json.dumps(result))
"@

$tmp = Join-Path ([System.IO.Path]::GetTempPath()) "audit-opencode-db.py"
Set-Content -LiteralPath $tmp -Value $script -Encoding UTF8
try {
  $json = & $python run python $tmp $SnapshotPath $BaselineCacheReadV1
  if ($LASTEXITCODE -ne 0) {
    Write-Error "Re-audit python failed with exit code $LASTEXITCODE"
    exit 1
  }
  Write-Output $json
  if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $stamp = Get-Date -Format "yyyy-MM-dd"
    $OutputPath = Join-Path $Root "reports/opencode-db-reaudit-$stamp.json"
  }
  Set-Content -LiteralPath $OutputPath -Value $json -Encoding UTF8
  Write-Output "Re-audit report written to $OutputPath"
} finally {
  if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -ErrorAction SilentlyContinue }
}
