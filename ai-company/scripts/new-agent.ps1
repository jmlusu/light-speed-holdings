param(

    [Parameter(Mandatory)]

    [string]$Name,

    [Parameter(Mandatory)]

    [string]$Department

)

$folder = ".\$Department\$Name"

New-Item $folder -ItemType Directory -Force

New-Item "$folder\Agent.md" -ItemType File -Force

New-Item "$folder\Mission.md" -ItemType File -Force

New-Item "$folder\Tasks.md" -ItemType File -Force

New-Item "$folder\Memory.md" -ItemType File -Force

New-Item "$folder\agent.yaml" -ItemType File -Force

Write-Host ""

Write-Host "$Name created successfully."

Write-Host ""