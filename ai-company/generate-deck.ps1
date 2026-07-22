# Generate Milestones Deck PowerShell Script
# This script generates the AI Company Builder milestones presentation

Write-Host "AI Company Builder - Milestones Deck Generator" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js from https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Check if npm is installed
try {
    $npmVersion = npm --version
    Write-Host "✅ npm version: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install npm (usually comes with Node.js)" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
npm install

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Generating milestones deck..." -ForegroundColor Yellow
node scripts/generate-milestones-deck.js

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Presentation generated successfully!" -ForegroundColor Green
    Write-Host "📁 File location: docs/milestones-deck.pptx" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can now open the presentation in PowerPoint or LibreOffice." -ForegroundColor White
} else {
    Write-Host "❌ Failed to generate presentation" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")