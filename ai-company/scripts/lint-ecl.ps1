$ErrorActionPreference = "Stop"

$Root = (Get-Location).Path
$Changes = Join-Path $Root "harness/changes"
$Active = Join-Path $Changes "active"
$IndexPath = Join-Path $Changes "INDEX.json"
$HarnessChange = Join-Path $Root "scripts/harness-change.ps1"
$HarnessEvolve = Join-Path $Root "scripts/harness-evolve.ps1"
$StatusPath = Join-Path $Root "docs/STATUS.md"
$EvolutionState = Join-Path $Root "harness/evolution/state.json"

function Fail([string]$Message) {
  Write-Error $Message
  exit 1
}

if (-not (Test-Path -LiteralPath $Changes)) {
  Fail "Missing harness/changes. Run ecl-harness-engineer or create ECL harness structure."
}

foreach ($dir in @("active", "parking", "archive")) {
  if (-not (Test-Path -LiteralPath (Join-Path $Changes $dir))) {
    Fail "Missing harness/changes/$dir."
  }
}

if (-not (Test-Path -LiteralPath $HarnessChange)) {
  Fail "Missing scripts/harness-change.ps1."
}

if (-not (Test-Path -LiteralPath $HarnessEvolve)) {
  Fail "Missing scripts/harness-evolve.ps1."
}

if (-not (Test-Path -LiteralPath $EvolutionState)) {
  Fail "Missing harness/evolution/state.json."
}

if (-not (Test-Path -LiteralPath $StatusPath)) {
  Fail "Missing docs/STATUS.md. Create a lightweight handoff summary; active change files override it when present."
}

if (Test-Path -LiteralPath (Join-Path $Active "summary.md")) {
  foreach ($file in @("summary.md", "spec.md", "plan.md", "tasks.md")) {
    if (-not (Test-Path -LiteralPath (Join-Path $Active $file))) {
      Fail "Active change missing $file."
    }
  }
  if (-not (Test-Path -LiteralPath (Join-Path $Active "reviews"))) {
    Fail "Active change missing reviews/."
  }
  $summary = Get-Content -Encoding UTF8 -Raw -LiteralPath (Join-Path $Active "summary.md")
  $spec = Get-Content -Encoding UTF8 -Raw -LiteralPath (Join-Path $Active "spec.md")
  $tasks = Get-Content -Encoding UTF8 -Raw -LiteralPath (Join-Path $Active "tasks.md")
  $review = ""
  $reviewPath = Join-Path $Active "reviews/review.md"
  if (Test-Path -LiteralPath $reviewPath) { $review = Get-Content -Encoding UTF8 -Raw -LiteralPath $reviewPath }
  $phase = [regex]::Match($summary, '(?m)^phase:\s*"?([^"\r\n]+)"?').Groups[1].Value
  $planReview = [regex]::Match($summary, '(?m)^plan_review:\s*"?([^"\r\n]+)"?').Groups[1].Value
  if ($phase -match "^(implement|validate|done)$" -and $spec -match "\[NEEDS CLARIFICATION:") {
    Fail "Active spec.md still has high-impact [NEEDS CLARIFICATION] markers. Resolve them or move phase back to intake/plan."
  }
  if ($phase -match "^(implement|validate|done)$" -and $planReview -ne "approved" -and $review -notmatch "(?is)Plan Review.*Status:\s*approved") {
    Fail "Active change cannot enter implementation until plan_review is approved in summary.md or an equivalent approved Plan Review is recorded."
  }
  if ($tasks -match "(?m)^- \[[ xX]\] (?!T\d{3})") {
    Fail "tasks.md contains executable task lines without T### ids. Use '- [ ] T001 [P?] [US?] Action with target path and validation note'."
  }
}

if (-not (Test-Path -LiteralPath $IndexPath)) {
  Fail "Missing harness/changes/INDEX.json. Run: powershell -NoProfile -ExecutionPolicy Bypass -File scripts/harness-change.ps1 reindex"
}
$actual = Get-Content -Encoding UTF8 -Raw -LiteralPath $IndexPath
$expected = (& $HarnessChange index-json) -join "`n"
if ($actual.Trim() -ne $expected.Trim()) {
  Fail "harness/changes/INDEX.json is stale. Run: powershell -NoProfile -ExecutionPolicy Bypass -File scripts/harness-change.ps1 reindex"
}

Write-Output "ECL lint passed."
