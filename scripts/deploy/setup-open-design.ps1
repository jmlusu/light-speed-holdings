# Open Design Integration Setup Script for Windows
# Run this script to set up Open Design integration with LightSpeed Holdings

param(
    [switch]$SkipInstall,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "LightSpeed Holdings - Open Design Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check prerequisites
Write-Host "[1/5] Checking prerequisites..." -ForegroundColor Yellow

# Check Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "  ERROR: Node.js is required. Install from https://nodejs.org" -ForegroundColor Red
    exit 1
}
Write-Host "  OK: Node.js $(node --version)" -ForegroundColor Green

# Check Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "  ERROR: Git is required. Install from https://git-scm.com" -ForegroundColor Red
    exit 1
}
Write-Host "  OK: Git installed" -ForegroundColor Green

# Step 2: Create output directories
Write-Host ""
Write-Host "[2/5] Creating output directories..." -ForegroundColor Yellow

$dirs = @(
    "output\design",
    "output\design\websites",
    "output\design\decks",
    "output\design\documents",
    "output\design\diagrams",
    "output\design\infographics",
    "output\design\ads"
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "  Exists: $dir" -ForegroundColor Gray
    }
}

# Step 3: Verify brand tokens
Write-Host ""
Write-Host "[3/5] Verifying brand tokens..." -ForegroundColor Yellow

$brandTokensPath = "brand\tokens\brand-tokens.json"
if (Test-Path $brandTokensPath) {
    $tokens = Get-Content $brandTokensPath | ConvertFrom-Json
    Write-Host "  Brand tokens loaded" -ForegroundColor Green
    Write-Host "    Navy: $($tokens.color.navy.value)" -ForegroundColor Gray
    Write-Host "    Red: $($tokens.color.red.value)" -ForegroundColor Gray
    Write-Host "    Cyan: $($tokens.color.cyan.value)" -ForegroundColor Gray
} else {
    Write-Host "  ERROR: Brand tokens not found at $brandTokensPath" -ForegroundColor Red
    exit 1
}

# Step 4: Verify integration files
Write-Host ""
Write-Host "[4/5] Verifying integration files..." -ForegroundColor Yellow

$integrationFiles = @(
    ".opencode\integrations\open-design\config.json",
    ".opencode\integrations\open-design\team.json",
    ".opencode\integrations\open-design\README.md",
    ".opencode\integrations\open-design\QUICK-REFERENCE.md"
)

foreach ($file in $integrationFiles) {
    if (Test-Path $file) {
        Write-Host "  OK: $file" -ForegroundColor Green
    } else {
        Write-Host "  MISSING: $file" -ForegroundColor Red
    }
}

# Step 5: Summary
Write-Host ""
Write-Host "[5/5] Setup complete!" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Install Open Design desktop app from https://github.com/nexu-io/open-design/releases" -ForegroundColor White
Write-Host "  2. Sign in with AMR (no API key needed)" -ForegroundColor White
Write-Host "  3. Use the Creative Director agent to create artifacts:" -ForegroundColor White
Write-Host "     opencode --agent creative-director 'Create a landing page for SADC policymakers'" -ForegroundColor White
Write-Host ""
Write-Host "Quick reference: .opencode\integrations\open-design\QUICK-REFERENCE.md" -ForegroundColor Cyan
