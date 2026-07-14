<#
.SYNOPSIS
    Verifies generated OpenCode agent files and registry consistency.

.DESCRIPTION
    Checks that the company registry is valid JSON, contains the expected number
    of agents, and that each registered agent file exists with expected
    OpenCode subagent front matter.
#>

[CmdletBinding()]
param(
    [string]$RegistryPath = ".\company\agent-registry.json",

    [int]$ExpectedCount = 18,

    [switch]$RunOpenCode
)

$errors = [System.Collections.Generic.List[string]]::new()

if (-not (Test-Path $RegistryPath)) {
    Write-Error "Registry not found: $RegistryPath"
    exit 1
}

try {
    $registry = Get-Content -Path $RegistryPath -Raw | ConvertFrom-Json
}
catch {
    Write-Error "Registry is not valid JSON: $_"
    exit 1
}

if (@($registry).Count -ne $ExpectedCount) {
    $errors.Add("Expected $ExpectedCount registry entries, found $(@($registry).Count).")
}

$seenNames = [System.Collections.Generic.HashSet[string]]::new()
foreach ($agent in @($registry)) {
    if (-not $agent.name) {
        $errors.Add("Registry entry is missing a name.")
        continue
    }

    if (-not $seenNames.Add([string]$agent.name)) {
        $errors.Add("Duplicate registry entry: $($agent.name).")
    }

    if (-not $agent.file) {
        $errors.Add("Registry entry '$($agent.name)' is missing a file path.")
        continue
    }

    $agentPath = Join-Path (Get-Location) $agent.file
    if (-not (Test-Path $agentPath)) {
        $errors.Add("Missing agent file for '$($agent.name)': $($agent.file).")
        continue
    }

    $agentText = Get-Content -Path $agentPath -Raw
    if ($agentText -notmatch "(?s)^---\s+description:.+?mode: subagent\s+permission:\s+") {
        $errors.Add("Invalid OpenCode front matter: $($agent.file).")
    }

    if ($agent.role -and $agentText -notmatch [regex]::Escape("# $($agent.role)")) {
        $errors.Add("Missing role heading in $($agent.file): $($agent.role).")
    }
}

if ($RunOpenCode) {
    $openCodeCommand = Get-Command opencode -ErrorAction SilentlyContinue
    if ($openCodeCommand) {
        & opencode agent list
        if ($LASTEXITCODE -ne 0) {
            $errors.Add("opencode agent list failed with exit code $LASTEXITCODE.")
        }
    }
    else {
        $errors.Add("opencode is not installed or is not on PATH.")
    }
}

if ($errors.Count -gt 0) {
    foreach ($item in $errors) {
        Write-Error $item
    }
    exit 1
}

Write-Host "Agent verification passed: $ExpectedCount registry entries and matching agent files." -ForegroundColor Green
