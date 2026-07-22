# Verify Milestones Deck Setup PowerShell Script
# This script verifies that all files are in place for generating the milestones deck

Write-Host "Milestones Deck Setup Verification" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Run the Python verification script
python scripts/verify-setup.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Setup verification complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To generate the milestones deck:" -ForegroundColor Yellow
    Write-Host "1. Choose Node.js or Python (see README-milestones-deck.md)" -ForegroundColor White
    Write-Host "2. Run the appropriate generation script" -ForegroundColor White
    Write-Host "3. The presentation will be created at: docs/milestones-deck.pptx" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "❌ Setup verification failed" -ForegroundColor Red
    Write-Host "Please check the output above for missing files." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")