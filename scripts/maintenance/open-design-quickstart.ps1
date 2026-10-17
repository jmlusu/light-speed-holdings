# Open Design Quick Start for LightSpeed Holdings
# Usage: .\scripts\open-design-quickstart.ps1

param(
    [Parameter(Mandatory=$true)]
    [string]$Prompt,
    
    [string]$Model = "claude-sonnet-4.5",
    [string]$Format = "html",
    [string]$OutputDir = "output\design"
)

Write-Host "Creating artifact with Open Design..." -ForegroundColor Cyan
Write-Host "  Model: $Model" -ForegroundColor Gray
Write-Host "  Format: $Format" -ForegroundColor Gray
Write-Host "  Output: $OutputDir" -ForegroundColor Gray
Write-Host ""

# Load brand tokens
$brandTokens = Get-Content "brand\tokens\brand-tokens.json" | ConvertFrom-Json

# Create artifact
open-design create `
    --model $Model `
    --prompt $Prompt `
    --brand "brand\tokens\brand-tokens.json" `
    --output $OutputDir `
    --format $Format

Write-Host ""
Write-Host "Artifact created successfully!" -ForegroundColor Green
