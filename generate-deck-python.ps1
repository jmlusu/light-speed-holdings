# Generate Milestones Deck PowerShell Script (Python Version)
# This script generates the AI Company Builder milestones presentation using Python

Write-Host "AI Company Builder - Milestones Deck Generator (Python)" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "✅ Python version: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://python.org/" -ForegroundColor Yellow
    exit 1
}

# Check if uv is installed
try {
    $uvVersion = uv --version
    Write-Host "✅ uv version: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ uv is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Install uv from https://docs.astral.sh/uv/getting-started/installation/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
uv sync --extra dev

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Generating milestones deck..." -ForegroundColor Yellow
uv run python scripts/generate-milestones-deck.py

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
