<#
.SYNOPSIS
    Agent Factory for the AI Company OpenCode build.
    Generates a standardized OpenCode subagent markdown file, registers it in the
    company registry, and (optionally) appends it to the org chart.

.DESCRIPTION
    Every agent created by this script follows the same OpenCode-native structure:
    YAML front matter (description, mode, permission) + a standardized body
    (Identity, Mission, Responsibilities, Delegation, Decision Rights,
    Deliverables, Success Metrics, Operating Principles).

    This replaces hand-writing each executive/board/specialist file so that
    100+ agents stay consistent as the company grows.

.PARAMETER Name
    Agent file name in kebab-case, e.g. "cto", "board-finance", "backend-engineer".
    Becomes .opencode/agents/<Name>.md

.PARAMETER Role
    Human-readable title, e.g. "Chief Technology Officer".

.PARAMETER Type
    Executive | Board | Specialist
    Drives the default permission profile and default sections.

.PARAMETER Department
    Optional department label shown in the Identity block.

.PARAMETER ReportsTo
    Optional reporting line shown in the Identity block. Defaults based on Type.

.PARAMETER Mission
    One-sentence mission statement. If omitted, a placeholder is inserted for
    you to fill in by hand.

.PARAMETER Responsibilities
    Array of responsibility bullet strings.

.PARAMETER DelegatesTo
    Array of subagent/role names this agent can delegate to via the task tool.
    Ignored for Board type (boards never delegate or execute).

.PARAMETER Deliverables
    Array of deliverable bullet strings.

.PARAMETER PermissionProfile
    Execute        -> edit: ask, bash: ask, task: allow      (can propose changes, can delegate)
    AdvisoryDelegate -> edit: deny, bash: deny, task: allow   (analysis-only, but can delegate research)
    AdvisoryOnly   -> edit: deny, bash: deny, no task field   (pure analysis, no delegation)
    ReviewOnly     -> edit: deny, bash: deny, no task field   (Board default - never executes)
    If omitted, a sensible default is chosen based on Type.

.PARAMETER RegistryPath
    Path to the company registry JSON file. Defaults to .\company\agent-registry.json

.PARAMETER OrgChartPath
    Path to the org chart markdown file. Defaults to .\company\org-chart.md

.PARAMETER SkipOrgChart
    Switch. If set, skips updating the org chart file.

.PARAMETER Force
    Switch. Overwrites an existing agent file if one already exists.

.PARAMETER DryRun
    Switch. Prints what would be created/updated without writing anything to disk.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[a-z0-9]+(-[a-z0-9]+)*$')]
    [string]$Name,

    [Parameter(Mandatory = $true)]
    [string]$Role,

    [Parameter(Mandatory = $true)]
    [ValidateSet('Executive', 'Board', 'Specialist')]
    [string]$Type,

    [string]$Department = "",

    [string]$ReportsTo = "",

    [string]$Mission = "",

    [string[]]$Responsibilities = @(),

    [string[]]$DelegatesTo = @(),

    [string[]]$Deliverables = @(),

    [ValidateSet('Execute', 'AdvisoryDelegate', 'AdvisoryOnly', 'ReviewOnly')]
    [string]$PermissionProfile = "",

    [string]$RegistryPath = ".\company\agent-registry.json",

    [string]$OrgChartPath = ".\company\org-chart.md",

    [switch]$SkipOrgChart,

    [switch]$Force,

    [switch]$DryRun
)

# ---------------------------------------------------------------------------
# 1. Resolve defaults based on Type
# ---------------------------------------------------------------------------

if (-not $ReportsTo) {
    switch ($Type) {
        'Executive'  { $ReportsTo = "Chief of Staff" }
        'Board'      { $ReportsTo = "Human CEO (via CEO Advisor)" }
        'Specialist' { $ReportsTo = "Executive Sponsor" }
    }
}

if (-not $PermissionProfile) {
    switch ($Type) {
        'Executive'  { $PermissionProfile = 'Execute' }
        'Board'      { $PermissionProfile = 'ReviewOnly' }
        'Specialist' { $PermissionProfile = 'Execute' }
    }
}

if ($Type -eq 'Board' -and $DelegatesTo.Count -gt 0) {
    Write-Warning "Board agents never delegate or execute. Ignoring -DelegatesTo for '$Name'."
    $DelegatesTo = @()
}

if (-not $Mission) {
    $Mission = "TODO: define the one-sentence mission for $Role."
}

# ---------------------------------------------------------------------------
# 2. Build the permission block
# ---------------------------------------------------------------------------

function Get-PermissionBlock {
    param([string]$Profile)

    switch ($Profile) {
        'Execute' {
            return @("permission:", "  read: allow", "  grep: allow", "  list: allow", "  edit: ask", "  bash: ask", "  task: allow") -join "`n"
        }
        'AdvisoryDelegate' {
            return @("permission:", "  read: allow", "  grep: allow", "  list: allow", "  edit: deny", "  bash: deny", "  task: allow") -join "`n"
        }
        'AdvisoryOnly' {
            return @("permission:", "  read: allow", "  grep: allow", "  list: allow", "  edit: deny", "  bash: deny") -join "`n"
        }
        'ReviewOnly' {
            return @("permission:", "  read: allow", "  grep: allow", "  list: allow", "  edit: deny", "  bash: deny") -join "`n"
        }
    }
}

$permissionBlock = Get-PermissionBlock -Profile $PermissionProfile

# ---------------------------------------------------------------------------
# 3. Build the body sections
# ---------------------------------------------------------------------------

function Format-BulletList {
    param([string[]]$Items, [string]$Placeholder)

    if ($Items.Count -eq 0) {
        return "- $Placeholder"
    }
    
    $bulletList = [System.Collections.Generic.List[string]]::new()
    foreach ($item in $Items) {
        $bulletList.Add("- $item")
    }
    return $bulletList -join "`n"
}

$responsibilitiesBlock = Format-BulletList -Items $Responsibilities -Placeholder "TODO: list core responsibilities"
$deliverablesBlock     = Format-BulletList -Items $Deliverables -Placeholder "TODO: list expected deliverables"

$delegationSection = ""
if ($Type -ne 'Board') {
    $delegationBlock = Format-BulletList -Items $DelegatesTo -Placeholder "TODO: list subagents this role delegates to"
    $delegationSection = @("", "---", "", "# Delegation", "Delegate to:", $delegationBlock) -join "`n"
}

$decisionRightsSection = ""
$outputFormatSection = ""

if ($Type -eq 'Board') {
    $decisionRightsSection = @(
        "", "---", "", "# Decision Rights", "May:",
        "- Challenge assumptions and request further analysis",
        "- Recommend a decision be delayed pending more data",
        "", "Cannot:",
        "- Execute work",
        "- Modify files or project artifacts",
        "- Approve or authorize decisions unilaterally"
    ) -join "`n"

    $outputFormatSection = @(
        "", "---", "", "# Operating Principles",
        "Never execute work.", "Never modify files.", "Always challenge before agreeing.",
        "", "---", "", "# Output Format",
        "Always respond using this structure:", "",
        "## Executive Summary", "## Strengths", "## Weaknesses", "## Risks", "## Recommendations"
    ) -join "`n"
}
else {
    $decisionRightsSection = @(
        "", "---", "", "# Decision Rights", "May:",
        "- Recommend decisions within this role's domain",
        "- Request more information before proceeding",
        "", "Cannot:",
        "- Approve company spending",
        "- Change overall business strategy",
        "- Sign contracts or binding agreements"
    ) -join "`n"

    $outputFormatSection = @(
        "", "---", "", "# Success Metrics",
        "- TODO: define 3-5 measurable success metrics for this role",
        "", "---", "", "# Operating Principles",
        "Prefer simple, reversible decisions over complex, irreversible ones.",
        "Escalate strategic conflicts to the CEO Advisor rather than resolving them unilaterally."
    ) -join "`n"
}

# ---------------------------------------------------------------------------
# 4. Assemble the full markdown file
# ---------------------------------------------------------------------------

$description = "$Role"
if ($Type -eq 'Board') {
    $description = "$Role responsible for board-level review and challenge"
}

$agentMarkdown = @(
    "---",
    "description: $description",
    "mode: subagent",
    $permissionBlock,
    "---",
    "# $Role",
    "",
    "## Identity",
    "Role: $Role",
    "Reports To: $ReportsTo",
    "Department: $(if ($Department) { $Department } else { `"TBD`" })",
    "",
    "---",
    "",
    "# Mission",
    $Mission,
    "",
    "---",
    "",
    "# Responsibilities",
    $responsibilitiesBlock,
    $delegationSection,
    $decisionRightsSection,
    "",
    "---",
    "",
    "# Deliverables",
    $deliverablesBlock,
    $outputFormatSection
) -join "`n"

# ---------------------------------------------------------------------------
# 5. Write the agent file
# ---------------------------------------------------------------------------

$agentDir = ".\.opencode\agents"
$agentFile = Join-Path $agentDir "$Name.md"

if ($DryRun) {
    Write-Host "----- DRY RUN: $agentFile -----" -ForegroundColor Yellow
    Write-Host $agentMarkdown
}
else {
    if (-not (Test-Path $agentDir)) {
        [void](New-Item -ItemType Directory -Path $agentDir -Force)
    }

    if ((Test-Path $agentFile) -and -not $Force) {
        Write-Error "Agent file '$agentFile' already exists. Use -Force to overwrite."
        return
    }

    Set-Content -Path $agentFile -Value $agentMarkdown -Encoding utf8
    Write-Host "Created agent: $agentFile" -ForegroundColor Green
}

# ---------------------------------------------------------------------------
# 6. Register the agent in the company registry (JSON)
# ---------------------------------------------------------------------------

$registryEntry = [ordered]@{
    name        = $Name
    role        = $Role
    type        = $Type
    department  = $Department
    reportsTo   = $ReportsTo
    file        = ".opencode/agents/$Name.md"
    permission  = $PermissionProfile
    createdDate = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
}

if ($DryRun) {
    Write-Host "----- DRY RUN: registry entry for $RegistryPath -----" -ForegroundColor Yellow
    $jsonOut = ConvertTo-Json -InputObject $registryEntry
    Write-Host $jsonOut
}
else {
    $registryDir = Split-Path $RegistryPath -Parent
    if ($registryDir -and -not (Test-Path $registryDir)) {
        [void](New-Item -ItemType Directory -Path $registryDir -Force)
    }

    $registryList = [System.Collections.Generic.List[object]]::new()

    if (Test-Path $RegistryPath) {
        $rawJson = Get-Content -Path $RegistryPath -Raw
        $existing = ConvertFrom-Json -InputObject $rawJson
        if ($null -ne $existing) {
            foreach ($item in @($existing)) {
                if ($item.name -ne $Name) {
                    $registryList.Add($item)
                }
            }
        }
    }

    $registryList.Add([pscustomobject]$registryEntry)
    $registryJson = $registryList | Sort-Object name | ConvertTo-Json -Depth 5
    Set-Content -Path $RegistryPath -Value $registryJson -Encoding utf8
    Write-Host "Updated registry: $RegistryPath" -ForegroundColor Green
}

# ---------------------------------------------------------------------------
# 7. Update the org chart
# ---------------------------------------------------------------------------

if (-not $SkipOrgChart) {
    $orgChartEntry = "- **$Role** (``$Name``) - $Type; reports to $ReportsTo"

    if ($DryRun) {
        Write-Host "----- DRY RUN: org chart entry for $OrgChartPath -----" -ForegroundColor Yellow
        Write-Host $orgChartEntry
    }
    else {
        $orgChartDir = Split-Path $OrgChartPath -Parent
        if ($orgChartDir -and -not (Test-Path $orgChartDir)) {
            [void](New-Item -ItemType Directory -Path $orgChartDir -Force)
        }

        $orgChartLines = [System.Collections.Generic.List[string]]::new()
        if (Test-Path $OrgChartPath) {
            foreach ($line in Get-Content -Path $OrgChartPath) {
                if ($line -notlike "*``$Name``*") {
                    $orgChartLines.Add($line)
                }
            }
        }
        else {
            $orgChartLines.Add("# AI Company Org Chart")
            $orgChartLines.Add("")
        }

        $orgChartLines.Add($orgChartEntry)
        Set-Content -Path $OrgChartPath -Value $orgChartLines -Encoding utf8
        Write-Host "Updated org chart: $OrgChartPath" -ForegroundColor Green
    }
}
