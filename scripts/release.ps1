<#
.SYNOPSIS
    AI Company Builder — Release Script
.DESCRIPTION
    Bumps version, runs checks, regenerates agents, commits, tags, and pushes.
.PARAMETER BumpType
    Version bump type: patch (default), minor, or major.
.EXAMPLE
    .\scripts\release.ps1
    .\scripts\release.ps1 -BumpType minor
#>
param(
    [ValidateSet("patch", "minor", "major")]
    [string]$BumpType = "patch"
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "=== AI Company Builder Release ===" -ForegroundColor Cyan
Write-Host "Bump type: $BumpType"

# 1. Run checks
Write-Host "`n[1/6] Running tests..." -ForegroundColor Yellow
python -m pytest tests/ -x -q
if ($LASTEXITCODE -ne 0) { throw "Tests failed" }
python -m ruff check src/
if ($LASTEXITCODE -ne 0) { throw "Lint failed" }

# 2. Bump version
Write-Host "`n[2/6] Bumping version..." -ForegroundColor Yellow
$currentVersion = python -c "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])"
Write-Host "Current: $currentVersion"

$parts = $currentVersion -split '\.'
$major = [int]$parts[0]
$minor = [int]$parts[1]
$patch = [int]$parts[2]

switch ($BumpType) {
    "major" { $major++; $minor = 0; $patch = 0 }
    "minor" { $minor++; $patch = 0 }
    "patch" { $patch++ }
}

$newVersion = "$major.$minor.$patch"
Write-Host "New: $newVersion" -ForegroundColor Green

(Get-Content pyproject.toml) -replace "version = `"$currentVersion`"", "version = `"$newVersion`"" | Set-Content pyproject.toml

# 3. Update CHANGELOG
Write-Host "`n[3/6] Updating CHANGELOG..." -ForegroundColor Yellow
$date = Get-Date -Format "yyyy-MM-dd"
$changelogEntry = @"
## [$newVersion] - $date

### Changed
- Version bump to $vnewVersion

"@

$existing = Get-Content CHANGELOG.md -Raw
$changelogEntry + $existing | Set-Content CHANGELOG.md

# 4. Regenerate agents
Write-Host "`n[4/6] Regenerating agents..." -ForegroundColor Yellow
python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"

# 5. Git commit and tag
Write-Host "`n[5/6] Creating git tag..." -ForegroundColor Yellow
git add -A
git commit -m "release: v$newVersion"
git tag "v$newVersion"

# 6. Push
Write-Host "`n[6/6] Pushing..." -ForegroundColor Yellow
git push origin main --tags

Write-Host "`n=== Release v$newVersion complete ===" -ForegroundColor Cyan
Write-Host "Create a GitHub Release at: https://github.com/light-speed-holdings/ai-company/releases/new?tag=v$newVersion"
