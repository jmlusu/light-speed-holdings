param(
  [Parameter(Position = 0)]
  [ValidateSet("new", "status", "validate", "park", "resume", "close", "search", "context", "reindex", "index-json")]
  [string]$Command,

  [Parameter(Position = 1, ValueFromRemainingArguments = $true)]
  [string[]]$Args
)

$ErrorActionPreference = "Stop"

$Root = (Get-Location).Path
$Changes = Join-Path $Root "harness/changes"
$Active = Join-Path $Changes "active"
$Parking = Join-Path $Changes "parking"
$Archive = Join-Path $Changes "archive"
$IndexPath = Join-Path $Changes "INDEX.json"
$Template = Join-Path $Root "harness/templates/change"
$Evolution = Join-Path $Root "harness/evolution"
$EvolutionPending = Join-Path $Evolution "pending.md"
$HarnessEvolve = Join-Path $Root "scripts/harness-evolve.ps1"

function Ensure-Dirs {
  foreach ($dir in @($Changes, $Active, $Parking, $Archive, $Template, (Join-Path $Template "reviews"), $Evolution, (Join-Path $Evolution "proposals"))) {
    if (-not (Test-Path -LiteralPath $dir)) {
      New-Item -ItemType Directory -Path $dir | Out-Null
    }
  }
}

function Get-DateText {
  return (Get-Date).ToString("yyyy-MM-dd")
}

function ConvertTo-Slug([string]$Text) {
  $slug = $Text.ToLowerInvariant() -replace "[^a-z0-9]+", "-"
  $slug = $slug.Trim("-")
  if ([string]::IsNullOrWhiteSpace($slug)) { $slug = "change" }
  return $slug
}

function Read-Text([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path)) { return "" }
  return Get-Content -Encoding UTF8 -Raw -LiteralPath $Path
}

function Write-Text([string]$Path, [string]$Content) {
  $parent = Split-Path -Parent $Path
  if ($parent -and -not (Test-Path -LiteralPath $parent)) {
    New-Item -ItemType Directory -Path $parent | Out-Null
  }
  Set-Content -Encoding UTF8 -LiteralPath $Path -Value $Content
}

function Parse-FrontMatter([string]$Path) {
  $text = Read-Text $Path
  $result = @{}
  if (-not $text.StartsWith("---")) { return $result }
  $lines = $text -split "`r?`n"
  for ($i = 1; $i -lt $lines.Length; $i++) {
    if ($lines[$i] -eq "---") { break }
    if ($lines[$i] -match "^\s*([^:#]+):\s*(.*)\s*$") {
      $key = $Matches[1].Trim()
      $value = $Matches[2].Trim().Trim('"')
      if ($value -match "^\[(.*)\]$") {
        $items = $Matches[1].Split(",") | ForEach-Object { $_.Trim().Trim('"') } | Where-Object { $_ }
        $result[$key] = @($items)
      } else {
        $result[$key] = $value
      }
    }
  }
  return $result
}

function Set-FrontMatterValues([string]$Path, [hashtable]$Values) {
  $text = Read-Text $Path
  if (-not $text.StartsWith("---")) { throw "$Path has no front matter." }
  foreach ($key in $Values.Keys) {
    $value = $Values[$key]
    $line = if ($value -is [array]) {
      $quoted = $value | ForEach-Object { '"' + ($_ -replace '"', '\"') + '"' }
      "${key}: [" + ($quoted -join ", ") + "]"
    } else {
      "${key}: `"$value`""
    }
    if ($text -match "(?m)^$([regex]::Escape($key)):\s*.*$") {
      $text = [regex]::Replace($text, "(?m)^$([regex]::Escape($key)):\s*.*$", [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $line }, 1)
    } else {
      $lines = $text -split "`r?`n"
      for ($i = 1; $i -lt $lines.Length; $i++) {
        if ($lines[$i] -eq "---") {
          $before = @($lines[0..($i - 1)])
          $after = @($lines[$i..($lines.Length - 1)])
          $text = (@($before + $line + $after) -join "`n")
          break
        }
      }
    }
  }
  Write-Text $Path $text
}

function Get-SectionLines([string]$Path, [string]$Heading) {
  $text = Read-Text $Path
  if (-not $text) { return @() }
  $lines = $text -split "`r?`n"
  $found = $false
  $items = New-Object System.Collections.Generic.List[string]
  foreach ($line in $lines) {
    if ($line -match "^##\s+$([regex]::Escape($Heading))\s*$") {
      $found = $true
      continue
    }
    if ($found -and $line -match "^##\s+") { break }
    if ($found -and $line.Trim()) {
      $items.Add($line.Trim())
    }
  }
  return @($items)
}

function Get-ValidationStatus([string]$SummaryPath, [hashtable]$Meta) {
  if ($Meta.ContainsKey("validation_status") -and $Meta["validation_status"]) {
    return $Meta["validation_status"]
  }
  $validation = (Get-SectionLines $SummaryPath "Validation") -join " "
  if ($validation -match "(?i)\bpass(ed)?\b|success|ok") { return "pass" }
  if ($validation -match "(?i)\bfail(ed)?\b|error|blocked") { return "fail" }
  return "unknown"
}

function Get-IndexEntries {
  $entries = New-Object System.Collections.Generic.List[object]
  foreach ($pair in @(@("parking", $Parking), @("archive", $Archive))) {
    $location = $pair[0]
    $base = $pair[1]
    if (-not (Test-Path -LiteralPath $base)) { continue }
    Get-ChildItem -LiteralPath $base -Directory | ForEach-Object {
      $summary = Join-Path $_.FullName "summary.md"
      if (-not (Test-Path -LiteralPath $summary)) { return }
      $meta = Parse-FrontMatter $summary
      $decisions = Get-SectionLines $summary "Decisions" | Where-Object { $_ -notmatch "Pending" }
      $relativePath = (Resolve-Path -LiteralPath $_.FullName -Relative).TrimStart([char[]]@(".", "\"))
      $entries.Add([ordered]@{
        id = $_.Name
        title = $meta["title"]
        status = $meta["status"]
        location = $location
        modules = @($meta["modules"])
        files = @($meta["files"])
        tags = @($meta["tags"])
        decisions = @($decisions)
        validation_status = Get-ValidationStatus $summary $meta
        path = ($relativePath -replace "\\", "/")
        updated_at = $meta["updated_at"]
      })
    }
  }
  return $entries.ToArray()
}

function Get-IndexJson {
  $entries = Get-IndexEntries
  if ($entries.Count -eq 0) { return "[]`n" }
  $json = $entries | ConvertTo-Json -Depth 8
  return ($json + "`n")
}

function Reindex {
  Ensure-Dirs
  $entries = Get-IndexEntries
  Write-Text $IndexPath (Get-IndexJson)
  Write-Output "Rebuilt harness/changes/INDEX.json ($($entries.Count) entries)."
}

function Invoke-EvolutionCheck([string]$Reason) {
  if (-not (Test-Path -LiteralPath $HarnessEvolve)) { return }
  try {
    & $HarnessEvolve check -Reason $Reason
  } catch {
    Write-Warning "Auto-evolve check failed: $($_.Exception.Message)"
  }
}

function Show-EvolutionReminder {
  if (Test-Path -LiteralPath $EvolutionPending) {
    Write-Warning "Harness evolution is pending: harness/evolution/pending.md"
  }
}

function Assert-NoActive {
  $summary = Join-Path $Active "summary.md"
  if (Test-Path -LiteralPath $summary) {
    throw "Active change exists. Run 'status', then 'park', 'close', or finish it before starting a new change."
  }
}

function New-Change([string]$Title) {
  Ensure-Dirs
  if ([string]::IsNullOrWhiteSpace($Title)) { throw "Missing title." }
  Assert-NoActive
  $date = Get-DateText
  $slug = ConvertTo-Slug $Title
  Write-Text (Join-Path $Active "summary.md") @"
---
title: "$Title"
slug: "$slug"
status: "in_progress"
location: "active"
phase: "intake"
intake_status: "pending"
spec_review: "pending"
plan_review: "pending"
modules: []
files: []
tags: []
validation_status: "unknown"
created_at: "$date"
updated_at: "$date"
---

# Summary

## Outcome

Pending.

## Decisions

- Pending.

## Validation

- Pending.

## Next Step

- Run Intake Review, then update ``spec.md`` and ``plan.md``.
"@
  Write-Text (Join-Path $Active "spec.md") @"
# Spec

## Intake Review

- Intake type: Small Change | Structured Change
- Input shape: requirement-first | plan-first | mixed
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request:
- Current behavior:
- Source of evidence:

## User Scenarios And Success

- Primary user/system scenario:
- Success criteria:
- Acceptance criteria:

## Non-Goals

- Pending.

## Constraints

- Pending.

## Assumptions

- Pending.

## Open Questions

- [NEEDS CLARIFICATION: Replace with a specific high-impact question, or remove before implementation.]

## Resolved Clarifications

- Pending.
"@
  Write-Text (Join-Path $Active "plan.md") @"
# Plan

## Technical Approach

- Pending.

## Impacted Modules And Files

- Pending.

## Interfaces, Data, Permissions

- Pending.

## Spec Gaps Found From Planning

- Pending.

## Risks And Mitigations

- Pending.

## Verification Plan

- Pending.
"@
  Write-Text (Join-Path $Active "tasks.md") @"
# Tasks

## Format

- ``- [ ] T001 [P?] [US?] Action with target path and validation note``
- ``[P]`` means parallel-safe. ``[US1]`` maps to a user story when stories exist.

## Setup / Intake

- [ ] T001 Review ``spec.md`` and ``plan.md`` gates before implementation.

## Implementation

- [ ] T002 Pending implementation task with target path.

## Validation

- [ ] T003 Pending validation task with command or scenario.

## Deferred Tasks

- None.
"@
  Write-Text (Join-Path $Active "reviews/review.md") @"
# Review

## Intake Review

- Status: pending
- Notes:

## Spec Review

- Status: pending
- Open high-impact clarifications:
- WHAT/HOW separation:

## Plan Review

- Status: pending
- Spec gaps found from planning:

## Code Review

- Status: pending

## Validation Review

- Status: pending
"@
  Write-Output "Created active change: $Title"
  Show-EvolutionReminder
}

function Validate-Change([string]$Dir) {
  $required = @("summary.md", "spec.md", "tasks.md")
  $isActive = ((Resolve-Path -LiteralPath $Dir).Path -eq (Resolve-Path -LiteralPath $Active).Path)
  if ($isActive) {
    $required = @("summary.md", "spec.md", "plan.md", "tasks.md")
  }
  foreach ($file in $required) {
    if (-not (Test-Path -LiteralPath (Join-Path $Dir $file))) {
      throw "Missing $file in $Dir"
    }
  }
  if (-not (Test-Path -LiteralPath (Join-Path $Dir "reviews"))) {
    throw "Missing reviews/ in $Dir"
  }
  $summary = Join-Path $Dir "summary.md"
  $meta = Parse-FrontMatter $summary
  $status = $meta["status"]
  if (-not $status) { throw "summary.md missing status front matter." }
  $phase = $meta["phase"]
  $planReview = $meta["plan_review"]
  $spec = Read-Text (Join-Path $Dir "spec.md")
  $reviewText = ""
  $reviewPath = Join-Path $Dir "reviews/review.md"
  if (Test-Path -LiteralPath $reviewPath) { $reviewText = Read-Text $reviewPath }
  $tasks = Read-Text (Join-Path $Dir "tasks.md")
  if ($isActive -and $phase -match "^(implement|validate|done)$" -and $spec -match "\[NEEDS CLARIFICATION:") {
    throw "spec.md has high-impact [NEEDS CLARIFICATION] markers. Resolve them or move the change back to intake/plan before implementation."
  }
  if ($isActive -and $phase -match "^(implement|validate|done)$" -and $planReview -ne "approved" -and $reviewText -notmatch "(?is)Plan Review.*Status:\s*approved") {
    throw "summary.md plan_review must be approved before implementation. Record plan approval in summary.md or reviews/review.md."
  }
  if ($isActive -and $tasks -match "(?m)^- \[[ xX]\] (?!T\d{3})" -and $tasks -notmatch "## Deferred Tasks") {
    throw "tasks.md task lines must use T### ids with target paths and validation notes so agents can execute them predictably."
  }
  if ($status -eq "completed") {
    $validation = Get-ValidationStatus $summary $meta
    if ($validation -ne "pass") { throw "completed change must have validation_status: pass or a passing Validation section." }
    if ($tasks -match "- \[ \] " -and $tasks -notmatch "## Deferred Tasks\s+(\r?\n)+-\s+(None|Deferred|Explained)") {
      throw "completed change has pending tasks without a Deferred Tasks explanation."
    }
  }
}

function Show-Status {
  Ensure-Dirs
  $summary = Join-Path $Active "summary.md"
  if (-not (Test-Path -LiteralPath $summary)) {
    Write-Output "No active change."
    return
  }
  $meta = Parse-FrontMatter $summary
  Write-Output "Active: $($meta["title"])"
  Write-Output "Status: $($meta["status"])"
  Write-Output "Phase: $($meta["phase"])"
}

function New-ClosedId([hashtable]$Meta) {
  $date = Get-DateText
  if ($Meta["updated_at"] -match "^\d{4}-\d{2}-\d{2}$") { $date = $Meta["updated_at"] }
  $slug = $Meta["slug"]
  if (-not $slug) { $slug = ConvertTo-Slug $Meta["title"] }
  $id = "$date-$slug"
  return $id
}

function Move-Active([string]$TargetBase, [string]$Status, [string]$Reason) {
  Ensure-Dirs
  $summary = Join-Path $Active "summary.md"
  if (-not (Test-Path -LiteralPath $summary)) { throw "No active change." }
  $meta = Parse-FrontMatter $summary
  if ($TargetBase -eq $Archive -and $Status -notin @("completed", "blocked", "abandoned")) {
    throw "close status must be completed, blocked, or abandoned."
  }
  if ($Status -eq "completed") { Validate-Change $Active }
  $targetLocation = if ($TargetBase -eq $Parking) { "parking" } else { "archive" }
  $newStatus = if ($TargetBase -eq $Parking) { "parked" } else { $Status }
  Set-FrontMatterValues $summary @{
    status = $newStatus
    location = $targetLocation
    updated_at = (Get-DateText)
  }
  if ($Reason) {
    Add-Content -Encoding UTF8 -LiteralPath $summary -Value "`n## Transition Note`n`n- $Reason`n"
  }
  $meta = Parse-FrontMatter $summary
  $id = New-ClosedId $meta
  $target = Join-Path $TargetBase $id
  $n = 2
  while (Test-Path -LiteralPath $target) {
    $target = Join-Path $TargetBase "$id-$n"
    $n++
  }
  Move-Item -LiteralPath $Active -Destination $target
  New-Item -ItemType Directory -Path $Active | Out-Null
  Reindex
  if ($TargetBase -eq $Archive) { Invoke-EvolutionCheck "close" }
  Write-Output "Moved active change to $target"
}

function Resume-Change([string]$Id) {
  Ensure-Dirs
  Assert-NoActive
  $source = Join-Path $Parking $Id
  if (-not (Test-Path -LiteralPath $source)) { throw "Parking change not found: $Id" }
  $summary = Join-Path $source "summary.md"
  if (Test-Path -LiteralPath $summary) {
    Set-FrontMatterValues $summary @{
      status = "in_progress"
      location = "active"
      updated_at = (Get-DateText)
    }
  }
  Move-Item -LiteralPath $source -Destination $Active
  Reindex
  Write-Output "Resumed $Id into active. Run validate before continuing."
}

function Search-Index([string]$Query) {
  if (-not (Test-Path -LiteralPath $IndexPath)) { Reindex }
  $items = Get-Content -Encoding UTF8 -Raw -LiteralPath $IndexPath | ConvertFrom-Json
  $items | Where-Object { ($_ | ConvertTo-Json -Depth 8) -match [regex]::Escape($Query) } |
    Select-Object id,title,status,location,path,validation_status | Format-Table -AutoSize
}

function Show-Context {
  Write-Output "Required:"
  foreach ($p in @("AGENTS.md", "docs/ECL.md", "harness/changes/active/summary.md", "harness/changes/active/spec.md", "harness/changes/active/plan.md", "harness/changes/active/tasks.md")) {
    if (Test-Path -LiteralPath (Join-Path $Root $p)) { Write-Output "- $p" }
  }
  if (-not (Test-Path -LiteralPath (Join-Path $Root "harness/changes/active/summary.md")) -and
      (Test-Path -LiteralPath $EvolutionPending)) {
    Write-Output "- harness/evolution/pending.md"
  }
  if (-not (Test-Path -LiteralPath (Join-Path $Root "harness/changes/active/summary.md")) -and
      (Test-Path -LiteralPath (Join-Path $Root "docs/STATUS.md"))) {
    Write-Output "- docs/STATUS.md"
  }
  Write-Output ""
  Write-Output "History index:"
  if (Test-Path -LiteralPath $IndexPath) { Write-Output "- harness/changes/INDEX.json" } else { Write-Output "- Run scripts/harness-change.ps1 reindex" }
}

Ensure-Dirs
switch ($Command) {
  "new" { New-Change ($Args -join " ") }
  "status" { Show-Status }
  "validate" { Validate-Change $Active; Write-Output "ECL active change is valid." }
  "park" { Move-Active $Parking "parked" ($Args -join " ") }
  "resume" { Resume-Change $Args[0] }
  "close" { Move-Active $Archive $Args[0] "" }
  "search" { Search-Index ($Args -join " ") }
  "context" { Show-Context }
  "reindex" { Reindex; Invoke-EvolutionCheck "reindex" }
  "index-json" { Write-Output (Get-IndexJson) }
  default { throw "Command required: new/status/validate/park/resume/close/search/context/reindex" }
}
