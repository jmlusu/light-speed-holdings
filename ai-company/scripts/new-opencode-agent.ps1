param(

    [Parameter(Mandatory=$true)]
    [string]$Id,

    [Parameter(Mandatory=$true)]
    [string]$Title,

    [Parameter(Mandatory=$true)]
    [string]$Department,

    [Parameter(Mandatory=$true)]
    [string]$Role,

    [string]$ReportsTo = "Chief of Staff"

)

$template = ".\templates\agents\executive.md"

$output = ".\.opencode\agents\$Id.md"

if (!(Test-Path ".\.opencode\agents")) {

    New-Item `
        -ItemType Directory `
        -Path ".\.opencode\agents" `
        -Force | Out-Null

}

$content = Get-Content $template -Raw

$content = $content.Replace("{{DESCRIPTION}}",$Role)

$content = $content.Replace("{{TITLE}}",$Title)

$content = $content.Replace("{{ROLE}}",$Role)

$content = $content.Replace("{{DEPARTMENT}}",$Department)

$content = $content.Replace("{{REPORTS_TO}}",$ReportsTo)

$content = $content.Replace("{{MISSION}}","TODO")

$content = $content.Replace("{{RESPONSIBILITIES}}","- TODO")

$content = $content.Replace("{{DELEGATION}}","- TODO")

$content = $content.Replace("{{DELIVERABLES}}","- TODO")

$content = $content.Replace("{{METRICS}}","- TODO")

$content = $content.Replace("{{EDIT}}","ask")

$content = $content.Replace("{{BASH}}","ask")

$content | Set-Content $output

Write-Host ""
Write-Host "Agent created successfully." -ForegroundColor Green
Write-Host $output
Write-Host ""