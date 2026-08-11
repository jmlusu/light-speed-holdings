param(
  [Parameter(Position = 0)]
  [ValidateSet("check", "collect", "mark-complete")]
  [string]$Command = "check",

  [int]$Threshold = 5,
  [int]$Window = 10,
  [string]$Reason = "manual"
)

$ErrorActionPreference = "Stop"

$Root = (Get-Location).Path
$Changes = Join-Path $Root "harness/changes"
$IndexPath = Join-Path $Changes "INDEX.json"
$Evolution = Join-Path $Root "harness/evolution"
$StatePath = Join-Path $Evolution "state.json"
$PendingPath = Join-Path $Evolution "pending.md"
$ResultsPath = Join-Path $Evolution "results.tsv"
$Proposals = Join-Path $Evolution "proposals"

function Ensure-EvolutionDirs {
  foreach ($dir in @($Evolution, $Proposals)) {
    if (-not (Test-Path -LiteralPath $dir)) {
      New-Item -ItemType Directory -Path $dir | Out-Null
    }
  }
}

function Write-Text([string]$Path, [string]$Content) {
  $parent = Split-Path -Parent $Path
  if ($parent -and -not (Test-Path -LiteralPath $parent)) {
    New-Item -ItemType Directory -Path $parent | Out-Null
  }
  Set-Content -Encoding UTF8 -LiteralPath $Path -Value $Content
}

function Read-State {
  Ensure-EvolutionDirs
  if (-not (Test-Path -LiteralPath $StatePath)) {
    $initial = [ordered]@{
      enabled = $true
      threshold = $Threshold
      window = $Window
      last_evolved_archive_count = 0
      last_evolved_change_id = $null
      last_score = $null
      last_run_at = $null
      pending = $false
    }
    Write-Text $StatePath (($initial | ConvertTo-Json -Depth 5) + "`n")
  }
  return Get-Content -Encoding UTF8 -Raw -LiteralPath $StatePath | ConvertFrom-Json
}

function Write-State($State) {
  Write-Text $StatePath (($State | ConvertTo-Json -Depth 8) + "`n")
}

function Test-AutoEvolveArchive($Item) {
  $id = [string]$Item.id
  if ($id -match "^auto-evolve-harness-") { return $true }
  foreach ($tag in @($Item.tags)) {
    if ([string]$tag -eq "auto-evolve") { return $true }
  }
  return $false
}

function Get-ArchiveItems {
  if (-not (Test-Path -LiteralPath $IndexPath)) {
    throw "Missing harness/changes/INDEX.json. Run scripts/harness-change.ps1 reindex first."
  }
  $raw = Get-Content -Encoding UTF8 -Raw -LiteralPath $IndexPath
  if ([string]::IsNullOrWhiteSpace($raw)) { return @() }
  $parsed = $raw | ConvertFrom-Json
  $items = @($parsed | ForEach-Object { $_ })
  return @($items | Where-Object {
    $_.location -eq "archive" -and -not (Test-AutoEvolveArchive $_)
  } | Sort-Object updated_at, id)
}

function Ensure-ResultsHeader {
  if (-not (Test-Path -LiteralPath $ResultsPath)) {
    Write-Text $ResultsPath "timestamp`tchange_id`told_score`tnew_score`tstatus`tdimension`tnote`teval_mode`n"
  }
}

function Add-ResultRow([string]$ChangeId, [string]$OldScore, [string]$NewScore, [string]$Status, [string]$Dimension, [string]$Note, [string]$EvalMode) {
  Ensure-ResultsHeader
  if ($Status -notin @("keep", "revert", "rejected", "noop")) {
    throw "status must be keep, revert, rejected, or noop."
  }
  if ($EvalMode -notin @("independent_review", "dry_run", "full_test")) {
    throw "eval_mode must be independent_review, dry_run, or full_test."
  }
  $timestamp = (Get-Date).ToString("s")
  $line = @($timestamp, $ChangeId, $OldScore, $NewScore, $Status, $Dimension, ($Note -replace "`t", " "), $EvalMode) -join "`t"
  Add-Content -Encoding UTF8 -LiteralPath $ResultsPath -Value $line
}

function New-Pending([object[]]$ArchiveItems, $State, [string]$TriggerReason) {
  if (Test-Path -LiteralPath $PendingPath) {
    Write-Output "Harness evolution already pending: harness/evolution/pending.md"
    return
  }
  $candidateItems = @($ArchiveItems | Select-Object -Last $State.window)
  $candidateLines = @()
  foreach ($item in $candidateItems) {
    $path = [string]$item.path
    if (-not $path) { $path = "harness/changes/archive/$($item.id)" }
    $candidateLines += "- $path/summary.md"
  }
  $now = (Get-Date).ToString("s")
  $content = @"
# Harness Evolution Pending

Generated at: $now

## Trigger

- Reason: $TriggerReason
- Eligible archived changes since last evolution: $($ArchiveItems.Count - [int]$State.last_evolved_archive_count)
- Threshold: $($State.threshold)
- Scan window: $($State.window)
- INDEX source: harness/changes/INDEX.json
- Excludes: archive ids beginning with auto-evolve-harness- and archives tagged auto-evolve

## Candidate Archives

$($candidateLines -join "`n")

These candidates are the trigger snapshot. Before processing, rebuild ``harness/changes/INDEX.json``
and use the current eligible archive window so changes closed after this file was generated are not
missed.

## Instruction For Codex

Run harness auto-evolve:
1. Read docs/ECL.md and this pending file.
2. Rebuild ``harness/changes/INDEX.json``, then inspect the current eligible archive window first.
3. Read spec/plan/tasks/reviews only when evidence requires it.
4. Extract repeated failures, verification gaps, user corrections, and reusable constraints.
5. Generate ``harness/evolution/proposals/YYYY-MM-DD-auto-evolve.md`` from the proposal template in docs/ECL.md before editing harness files.
6. Request one independent auditor/subagent score before applying.
7. Apply only accepted candidates with archive evidence, project relevance, score >= 80, and independent approval.
8. Prefer clarifying existing rules over adding new sections, documents, scripts, or workflows.
9. Run harness checks and relevant business gates.
10. Record one terminal result in ``harness/evolution/results.tsv``.
11. Run ``harness-evolve mark-complete`` after writing the result.
"@
  Write-Text $PendingPath $content
  $State.pending = $true
  Write-State $State
  Write-Output "Created harness/evolution/pending.md"
}

function Check-Evolution {
  Ensure-EvolutionDirs
  Ensure-ResultsHeader
  $state = Read-State
  if (-not $state.enabled) {
    Write-Output "Harness auto-evolve disabled in harness/evolution/state.json."
    return
  }
  if (-not $state.threshold) { $state.threshold = $Threshold }
  if (-not $state.window) { $state.window = $Window }
  $archives = @(Get-ArchiveItems)
  if ([int]$state.last_evolved_archive_count -gt $archives.Count) {
    $state.last_evolved_archive_count = $archives.Count
    Write-State $state
  }
  $delta = [Math]::Max(0, $archives.Count - [int]$state.last_evolved_archive_count)
  if ($delta -lt [int]$state.threshold) {
    Write-Output "Harness evolution not due ($delta/$($state.threshold) new archived changes)."
    return
  }
  New-Pending $archives $state $Reason
}

function Collect-EvolutionInput {
  Check-Evolution
  if (Test-Path -LiteralPath $PendingPath) {
    Write-Output "Read: harness/evolution/pending.md"
  }
}

function Mark-Complete {
  $state = Read-State
  $archives = @(Get-ArchiveItems)
  $state.last_evolved_archive_count = $archives.Count
  $last = @($archives | Select-Object -Last 1)
  $state.last_evolved_change_id = if ($last.Count -gt 0) { $last[0].id } else { $null }
  $state.last_run_at = (Get-Date).ToString("s")
  $state.pending = $false
  Write-State $state
  if (Test-Path -LiteralPath $PendingPath) {
    Remove-Item -LiteralPath $PendingPath
  }
  Ensure-ResultsHeader
  Write-Output "Marked harness evolution complete."
}

switch ($Command) {
  "check" { Check-Evolution }
  "collect" { Collect-EvolutionInput }
  "mark-complete" { Mark-Complete }
  default { throw "Command required: check/collect/mark-complete" }
}
