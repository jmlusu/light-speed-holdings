# PowerShell anti-pattern scanner
# Gate for known historical failure modes (see knowledge/technology/bugs/registry.yaml):
#   FAIL: backtick immediately before dollar in a string (suppresses substitution) - BUG-d75423bb7
#   WARN: Get-ChildItem with no Sort-Object (enumeration order unstable) - BUG-93e21736a
# Usage: pwsh -NoProfile -File scripts/maintenance/scan-ps-antipatterns.ps1 [-Path <dir>]
param(
  [string]$Path = $PSScriptRoot
)

$ErrorActionPreference = "Stop"
$failCount = 0
$warnCount = 0

# Single-quoted pattern: backtick not preceded by another backtick, then escaped dollar.
# The lookbehind skips markdown code spans like (``$Name``), which are correct usage.
$backtickPattern = '(?<!`)`\$'
$sortPattern = 'Sort-Object\s+\w+'

$files = Get-ChildItem -LiteralPath $Path -Filter "*.ps1" -Recurse | Sort-Object FullName

foreach ($file in $files) {
  $content = Get-Content -Encoding UTF8 -Raw -LiteralPath $file.FullName

  if ($content -match $backtickPattern) {
    $lineNumbers = ($content -split "`n" | Select-String -Pattern $backtickPattern | ForEach-Object { $_.LineNumber }) -join ", "
    Write-Error "ANTI-PATTERN (FAIL): backtick before dollar suppresses variable substitution at $($file.FullName) lines $lineNumbers - BUG-d75423bb7" -ErrorAction Continue
    $failCount++
  }

  if ($content -match 'Get-ChildItem' -and $content -notmatch $sortPattern) {
    Write-Warning "ANTI-PATTERN (WARN): Get-ChildItem without Sort-Object - enumeration order unstable across platforms at $($file.FullName) - BUG-93e21736a"
    $warnCount++
  }
}

Write-Output "ps-antipattern scan: $($files.Count) files, $failCount failure(s), $warnCount warning(s)"
if ($failCount -gt 0) { exit 1 }
exit 0
