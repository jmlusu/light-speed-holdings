<#
.SYNOPSIS
    Validates that documentation files haven't drifted from their source of truth.

.DESCRIPTION
    Reads docs/source-of-truth.yaml and checks each claim:
    - Numeric claims: verifies docs contain the expected current_value via regex pattern
    - Anti-pattern claims: verifies scope files do NOT contain the anti-pattern regex

.PARAMETER Json
    Output machine-readable JSON instead of human-readable text (for CI integration).

.PARAMETER Verbose
    Print detailed output for each check.

.EXAMPLE
    .\scripts\validate-drift.ps1
    .\scripts\validate-drift.ps1 -Json
    .\scripts\validate-drift.ps1 -Verbose
#>

[CmdletBinding()]
param(
    [switch]$Json
)

$ErrorActionPreference = "Continue"
$Root = (Get-Location).Path
$ManifestPath = Join-Path $Root "docs\source-of-truth.yaml"

# ── Read manifest via Python (PowerShell lacks native YAML) ──────────────
if (-not (Test-Path -LiteralPath $ManifestPath)) {
    Write-Error "Manifest not found: $ManifestPath"
    exit 1
}

$manifestJson = python -c @"
import yaml, json, sys
with open(r'$($ManifestPath -replace '\\','\\')') as f:
    data = yaml.safe_load(f)
print(json.dumps(data))
"@ 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to parse YAML manifest: $manifestJson"
    exit 1
}

$manifest = $manifestJson | ConvertFrom-Json

# ── Collect results ──────────────────────────────────────────────────────
$drifts = [System.Collections.Generic.List[object]]::new()
$warnings = [System.Collections.Generic.List[object]]::new()
$checked = 0

foreach ($claimName in $manifest.claims.PSObject.Properties.Name) {
    $claim = $manifest.claims.$claimName

    # ── Anti-pattern claims (code checks) ────────────────────────────────
    if ($claim.anti_pattern) {
        $ap = $claim.anti_pattern
        $regex = $ap.regex
        $scope = $ap.scope
        $message = $ap.message

        # Expand glob scope (e.g. src/ai_company/cli/*.py)
        $scopeDir = Split-Path $scope -Parent
        $scopeFilter = Split-Path $scope -Leaf
        $scopeFull = Join-Path $Root $scopeDir

        if (-not (Test-Path -LiteralPath $scopeFull)) {
            $warnings.Add(@{
                claim   = $claimName
                message = "Scope directory not found: $scopeDir"
            })
            continue
        }

        $files = Get-ChildItem -Path $scopeFull -Filter $scopeFilter -File -ErrorAction SilentlyContinue
        foreach ($file in $files) {
            $checked++
            $content = Get-Content -LiteralPath $file.FullName -Raw -ErrorAction SilentlyContinue
            if (-not $content) { continue }

            $lineNum = 0
            foreach ($line in ($content -split "`n")) {
                $lineNum++
                if ([regex]::IsMatch($line, $regex)) {
                    $drifts.Add(@{
                        claim    = $claimName
                        file     = $file.FullName.Replace($Root + "\", "")
                        line     = $lineNum
                        expected = "Must NOT match: $regex"
                        actual   = $line.Trim()
                        message  = $message
                    })
                }
            }
        }
        continue
    }

    # ── Numeric / pattern claims (doc checks) ────────────────────────────
    if (-not $claim.current_value -or -not $claim.pattern) { continue }
    if (-not $claim.docs -or $claim.docs.Count -eq 0) { continue }

    $currentValue = [string]$claim.current_value
    $pattern = $claim.pattern
    $archivedExempt = $claim.archived_exempt -eq $true

    foreach ($doc in $claim.docs) {
        $docPath = Join-Path $Root $doc
        $checked++

        if (-not (Test-Path -LiteralPath $docPath)) {
            $warnings.Add(@{
                claim   = $claimName
                message = "Doc file not found: $doc"
            })
            continue
        }

        # Skip archived docs if exempt
        if ($archivedExempt -and $doc -match "^docs[\\/](archive|adr)[\\/]") {
            if ($VerbosePreference -eq "Continue" -or $PSCmdlet.MyInvocation.BoundParameters.ContainsKey('Verbose')) {
                Write-Verbose "Skipping archived exempt doc: $doc (claim: $claimName)"
            }
            continue
        }

        $content = Get-Content -LiteralPath $docPath -Raw -ErrorAction SilentlyContinue
        if (-not $content) { continue }

        # Find all matches of the pattern in the doc
        $matches = [regex]::Matches($content, $pattern)
        foreach ($m in $matches) {
            $matchedText = $m.Value

            # Extract the numeric portion from the match
            $numMatch = [regex]::Match($matchedText, '\d+')
            if (-not $numMatch.Success) { continue }

            $foundValue = $numMatch.Value

            # Compare: the found number must equal the current_value
            # For patterns like ">=3.12", extract the version number
            $expectedNum = [regex]::Match($currentValue, '\d+')
            if (-not $expectedNum.Success) { continue }

            if ($foundValue -ne $expectedNum.Value) {
                # Determine line number
                $beforeMatch = $content.Substring(0, $m.Index)
                $lineNum = ($beforeMatch -split "`n").Count

                $drifts.Add(@{
                    claim    = $claimName
                    file     = $doc
                    line     = $lineNum
                    expected = "$currentValue (pattern: $pattern)"
                    actual   = $matchedText
                    message  = "Doc contains stale value"
                })
            }
        }
    }
}

# ── Output ───────────────────────────────────────────────────────────────
if ($Json) {
    $output = @{
        status   = if ($drifts.Count -gt 0) { "drift_detected" } else { "clean" }
        drifts   = $drifts.ToArray()
        warnings = $warnings.ToArray()
        checked  = $checked
        timestamp = (Get-Date -Format "o")
    }
    $output | ConvertTo-Json -Depth 5
} else {
    if ($warnings.Count -gt 0) {
        Write-Host "`nWarnings:" -ForegroundColor Yellow
        foreach ($w in $warnings) {
            Write-Host "  [$($w.claim)] $($w.message)" -ForegroundColor Yellow
        }
    }

    if ($drifts.Count -gt 0) {
        Write-Host "`nDrift detected ($($drifts.Count) issue(s)):`n" -ForegroundColor Red
        foreach ($d in $drifts) {
            Write-Host "  Claim:    $($d.claim)" -ForegroundColor Red
            Write-Host "  File:     $($d.file)" -ForegroundColor Red
            Write-Host "  Line:     $($d.line)" -ForegroundColor Red
            Write-Host "  Expected: $($d.expected)" -ForegroundColor Red
            Write-Host "  Actual:   $($d.actual)" -ForegroundColor Red
            if ($d.message) {
                Write-Host "  Fix:      $($d.message)" -ForegroundColor DarkYellow
            }
            Write-Host ""
        }
        Write-Host "All claims verified. $checked file(s) checked. Drift detected." -ForegroundColor Red
    } else {
        Write-Host "All claims verified. No drift detected. ($checked file(s) checked)" -ForegroundColor Green
    }
}

# ── Exit code ────────────────────────────────────────────────────────────
if ($drifts.Count -gt 0) { exit 1 }
exit 0
