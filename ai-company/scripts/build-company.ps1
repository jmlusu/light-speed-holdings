$executives = Get-Content `
    ".\templates\definitions\executives.json" `
    -Raw |
    ConvertFrom-Json

foreach ($exec in $executives)
{
    .\scripts\new-opencode-agent.ps1 `
        -Id $exec.Id `
        -Title $exec.Title `
        -Department $exec.Department `
        -Role $exec.Role `
        -ReportsTo $exec.ReportsTo
}