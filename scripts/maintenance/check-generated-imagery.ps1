<#
.SYNOPSIS
  Generated-imagery register guard.

.DESCRIPTION
  Enforces docs/adr/027-ai-generated-imagery-policy.md section 6 (provenance must
  be recorded for every generated illustration) against the register at
  public/assets/generated/manifest.json.

  Checks:
    FAIL  an image file under public/assets/generated/ has no manifest entry.
    WARN  a manifest entry names a file that does not exist.
    FAIL  a manifest entry is missing a required field or provenance field.
    FAIL  a manifest entry is not kind "illustration" / generated true.
    FAIL  a manifest entry path is outside assets/generated/.
    FAIL  duplicate id or path in the manifest.

  The manifest file itself is ignored. Subdirectories are not scanned. An empty
  directory is a passing state.

  Runs under Windows PowerShell 5.1 and PowerShell 7 (no version-specific
  cmdlets), so it can be wired into both pre-commit and CI.

.PARAMETER Root
  Repository root. Defaults to the current directory.

.EXAMPLE
  pwsh -NoProfile -File scripts/maintenance/check-generated-imagery.ps1
#>
[CmdletBinding()]
param(
    [string]$Root = (Get-Location).Path,
    [switch]$Quiet
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Red = "$([char]27)[31m"
$Green = "$([char]27)[32m"
$Yellow = "$([char]27)[33m"
$Cyan = "$([char]27)[36m"
$Reset = "$([char]27)[0m"

function Write-Status {
    param([string]$Message, [string]$Color = $Cyan)
    if (-not $Quiet) { Write-Host "$Color$Message$Reset" }
}
function Write-Pass {
    param([string]$Message)
    if (-not $Quiet) { Write-Host "$Green[PASS]$Reset $Message" }
}
function Write-Fail {
    param([string]$Message)
    Write-Host "$Red[FAIL]$Reset $Message"
    $script:failed = $true
}
function Write-Warn {
    param([string]$Message)
    Write-Host "$Yellow[WARN]$Reset $Message"
    $script:warnings++
}

$script:failed = $false
$script:warnings = 0

$generatedDir = Join-Path $Root 'public\assets\generated'
$manifestPath = Join-Path $generatedDir 'manifest.json'
$imageExtensions = @('.png', '.jpg', '.jpeg', '.webp', '.gif', '.avif', '.svg', '.bmp', '.tif', '.tiff')
$requiredTop = @('id', 'path', 'kind', 'generated', 'subject', 'provenance')
$requiredProvenance = @('vendor', 'model', 'prompt_sha256', 'generated_at', 'edited_by', 'post_processing')

Write-Status '=== Generated Imagery Register Check ==='

if (-not (Test-Path -LiteralPath $manifestPath)) {
    Write-Fail 'Register not found: public/assets/generated/manifest.json'
    Write-Host "$Red[FAILURE]$Reset Generated imagery check failed."
    exit 1
}

try {
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
} catch {
    Write-Fail "Register is not valid JSON: $($_.Exception.Message)"
    Write-Host "$Red[FAILURE]$Reset Generated imagery check failed."
    exit 1
}

if ($null -eq $manifest.assets) {
    Write-Fail "Register is missing the 'assets' array."
    Write-Host "$Red[FAILURE]$Reset Generated imagery check failed."
    exit 1
}

$entries = @($manifest.assets)

# --- image files on disk (manifest itself excluded; subdirectories ignored) ---
$diskFiles = @()
if (Test-Path -LiteralPath $generatedDir) {
    $diskFiles = @(
        Get-ChildItem -LiteralPath $generatedDir -File |
            Sort-Object Name |
            Where-Object { $imageExtensions -contains $_.Extension.ToLowerInvariant() -and $_.Name -ne 'manifest.json' } |
            ForEach-Object { $_.Name }
    )
}

$seenIds = @{}
$seenPaths = @{}
$registeredNames = @{}

foreach ($entry in $entries) {
    $label = if ($entry.PSObject.Properties.Match('id') -and $entry.id) { $entry.id } else { '<missing id>' }

    foreach ($field in $requiredTop) {
        $present = $entry.PSObject.Properties.Match($field) -and $null -ne $entry.$field -and -not ($entry.$field -is [string] -and [string]::IsNullOrWhiteSpace($entry.$field))
        if (-not $present) {
            Write-Fail "[$label] missing required field '$field' (ADR-027 section 6)."
        }
    }

    if ($entry.PSObject.Properties.Match('kind') -and $entry.kind -ne 'illustration') {
        Write-Fail "[$label] kind must be 'illustration' (found '$($entry.kind)'); ADR-027 section 4."
    }
    if ($entry.PSObject.Properties.Match('generated') -and $entry.generated -ne $true) {
        Write-Fail "[$label] generated must be true (found '$($entry.generated)'); ADR-027 section 4."
    }
    if ($entry.PSObject.Properties.Match('path') -and $entry.path -notmatch '^assets/generated/') {
        Write-Fail "[$label] path must start with 'assets/generated/' (found '$($entry.path)')."
    }

    if ($entry.PSObject.Properties.Match('provenance') -and $null -ne $entry.provenance) {
        foreach ($field in $requiredProvenance) {
            $p = $entry.provenance
            $present = $p.PSObject.Properties.Match($field) -and $null -ne $p.$field -and -not ($p.$field -is [string] -and [string]::IsNullOrWhiteSpace($p.$field))
            if (-not $present) {
                Write-Fail "[$label] missing provenance field '$field' (ADR-027 section 6)."
            }
        }
    }

    if ($entry.PSObject.Properties.Match('id')) {
        if ($seenIds.ContainsKey($entry.id)) { Write-Fail "duplicate id '$($entry.id)'." } else { $seenIds[$entry.id] = $true }
    }
    if ($entry.PSObject.Properties.Match('path')) {
        if ($seenPaths.ContainsKey($entry.path)) { Write-Fail "duplicate path '$($entry.path)'." } else { $seenPaths[$entry.path] = $true }
        $registeredNames[($entry.path -replace '^assets/generated/', '')] = $true
    }
}

# --- file on disk with no entry ---
foreach ($name in ($diskFiles | Sort-Object)) {
    if (-not $registeredNames.ContainsKey($name)) {
        Write-Fail "unregistered generated image: public/assets/generated/$name (add a manifest entry; ADR-027 section 6)."
    }
}

# --- entry naming a file that is absent ---
foreach ($entry in $entries) {
    if ($entry.PSObject.Properties.Match('path') -and $entry.path) {
        $name = $entry.path -replace '^assets/generated/', ''
        if ($diskFiles -notcontains $name) {
            Write-Warn "manifest entry '$($entry.id)' names a missing file: public/$($entry.path)."
        }
    }
}

Write-Status '=== Summary ==='
if ($script:failed) {
    Write-Host "$Red[FAILURE]$Reset Generated imagery check failed ($($diskFiles.Count) file(s), $($entries.Count) entr(ies))."
    exit 1
}
if ($script:warnings -gt 0) {
    Write-Host "$Yellow[WARNINGS]$Reset Generated imagery check passed with $($script:warnings) warning(s) ($($diskFiles.Count) file(s), $($entries.Count) entr(ies))."
    exit 0
}
Write-Host "$Green[SUCCESS]$Reset Generated imagery check passed ($($diskFiles.Count) file(s), $($entries.Count) entr(ies))."
exit 0
