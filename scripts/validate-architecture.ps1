<#PSScriptInfo
.VERSION 1.0
.GUID 8f7a3b2c-9d4e-4f1a-8b6c-2d5e7f9a1b3c
.AUTHOR LightSpeed Architecture Team
.COPYRIGHT (c) 2026 LightSpeed Holdings
.TAGS validation, architecture, drift, boundary
.PROJECTURI https://github.com/lightspeed-holdings/light-speed-holdings
.LICENSEURI MIT
.RELEASENOTES
Initial architecture validation script for v2. Enforces:
- Public/private boundary (no internal registry imports in src/)
- Canonical counts (90 agents / 20 departments)
- No legacy tool names in public surfaces
- No stale 145/152/140+ claims in non-historical docs
- Single-hop redirects
- Public artifact schema compliance
#>

param(
    [switch]$Strict,
    [switch]$Quiet,
    [string]$Root = (Get-Location).Path
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Colors for output
$Red = "$([char]27)[31m"
$Green = "$([char]27)[32m"
$Yellow = "$([char]27)[33m"
$Cyan = "$([char]27)[36m"
$Reset = "$([char]27)[0m"

function Write-Status {
    param([string]$Message, [string]$Color = $Cyan)
    if (-not $Quiet) { Write-Host "$Color$Message$Reset" }
}

function Write-Pass {
    param([string]$Message)
    if (-not $Quiet) { Write-Host "$Green[PASS]$Reset $Message" }
}

function Write-Fail {
    param([string]$Message)
    Write-Host "$Red[FAIL]$Reset $Message"
    $script:failed = $true
}

function Write-Warn {
    param([string]$Message)
    Write-Host "$Yellow[WARN]$Reset $Message"
}

$script:failed = $false
$script:warnings = 0

# ============================================================
# 1. PUBLIC/PRIVATE BOUNDARY CHECKS
# ============================================================
Write-Status "=== 1. Public/Private Boundary Checks ==="

# 1.1 No internal registry import in src/
$internalImports = Get-ChildItem -Path "$Root\src" -Recurse -Include "*.ts","*.tsx" |
    Select-String -Pattern "company/agent-registry\.json" |
    Select-Object -Unique Path, LineNumber, Line

if ($internalImports) {
    Write-Fail "Internal registry imports found in src/ (violates PUBLIC_INTERNAL_BOUNDARY.md V1):"
    $internalImports | ForEach-Object { Write-Host "  $($_.Path):$($_.LineNumber) $($_.Line.Trim())" }
} else {
    Write-Pass "No internal registry imports in src/"
}

# 1.2 No guidelines/permission fields in public data modules
$forbiddenFields = @("guidelines", "permission", "model_tier", "approval_level", "escalation_path",
                     "initialTasks", "initialApprovals", "initialEscalations", "initialKPIs",
                     "llm_cost", "cost_per_task", "DASHBOARD_", "API_KEY", "secret", "token")

$publicDataFiles = Get-ChildItem -Path "$Root\src\data" -Recurse -Include "*.ts","*.tsx"
foreach ($field in $forbiddenFields) {
    $matches = $publicDataFiles | Select-String -Pattern $field
    if ($matches) {
        Write-Fail "Forbidden field '$field' found in public data modules:"
        $matches | Select-Object -Unique Path, LineNumber | ForEach-Object { Write-Host "  $($_.Path):$($_.LineNumber)" }
        $script:warnings++
    }
}

# 1.3 Public artifact exists and has correct structure
$publicArtifact = "$Root\src\data\generated\agent-registry.public.json"
if (Test-Path $publicArtifact) {
    Write-Pass "Public artifact exists at src/data/generated/agent-registry.public.json"
    $json = Get-Content $publicArtifact -Raw | ConvertFrom-Json

    # Check envelope
    $requiredEnvelope = @("schema_version", "generated_at", "source", "meta", "agents", "departments")
    foreach ($key in $requiredEnvelope) {
        if (-not $json.PSObject.Properties.Match($key)) {
            Write-Fail "Public artifact missing required envelope key: $key"
        }
    }

    # Check counts
    if ($json.meta.agents -ne 90) { Write-Fail "Public artifact meta.agents = $($json.meta.agents), expected 90" }
    elseif ($json.meta.departments -ne 20) { Write-Fail "Public artifact meta.departments = $($json.meta.departments), expected 20" }
    else { Write-Pass "Public artifact counts: 90 agents / 20 departments" }

    # Check agent count
    if ($json.agents.Count -ne 90) { Write-Fail "Public artifact agents array length = $($json.agents.Count), expected 90" }
    else { Write-Pass "Public artifact has 90 agent entries" }

    # Check for forbidden fields in agents
    $forbiddenInAgents = @("guidelines", "permission", "model_tier", "approval_level", "escalation_path",
                           "workflows", "inputs", "outputs", "write", "execute", "delegate", "code_interpreter", "web_search")
    $badAgents = $json.agents | Where-Object {
        $agent = $_
        $forbiddenInAgents | Where-Object { $agent.PSObject.Properties.Match($_) }
    }
    if ($badAgents) {
        Write-Fail "Forbidden fields found in public agent entries:"
        $badAgents | ForEach-Object { Write-Host "  Agent $($_.id): $($forbiddenInAgents | Where-Object { $_.PSObject.Properties.Match($_) } -join ', ')" }
    } else {
        Write-Pass "No forbidden fields in public agent entries"
    }

    # Check tools are canonical 7 only
    $canonicalTools = @("read", "edit", "grep", "list", "bash", "webfetch", "task")
    $badTools = $json.agents | Where-Object { $_.tools } | ForEach-Object {
        $agent = $_
        $agent.tools | Where-Object { $canonicalTools -notcontains $_ }
    }
    if ($badTools) {
        Write-Fail "Non-canonical tools found in public agents: $($badTools | Select-Object -Unique -join ', ')"
    } else {
        Write-Pass "All public agent tools are canonical 7"
    }

    # Check department count
    if ($json.departments.Count -ne 20) { Write-Fail "Public artifact departments array length = $($json.departments.Count), expected 20" }
    else { Write-Pass "Public artifact has 20 department entries" }
} else {
    Write-Warn "Public artifact not found at src/data/generated/agent-registry.public.json (expected after P2)"
    $script:warnings++
}

# ============================================================
# 2. CANONICAL COUNTS CHECK
# ============================================================
Write-Status "=== 2. Canonical Counts Check ==="

# 2.1 source-of-truth.yaml
$sotFile = "$Root\docs\source-of-truth.yaml"
if (Test-Path $sotFile) {
    $sot = Get-Content $sotFile -Raw
    # Parse current_value fields
    $agentMatch = [System.Text.RegularExpressions.Regex]::Match($sot, 'agent_count:.*?current_value:\s*(\d+)', [System.Text.RegularExpressions.RegexOptions]::Singleline)
    if ($agentMatch.Success -and $agentMatch.Groups[1].Value -eq "90") { Write-Pass "source-of-truth.yaml: agents = 90" }
    else { Write-Fail "source-of-truth.yaml agents not 90 (found: $($agentMatch.Groups[1].Value))" }

    $deptMatch = [System.Text.RegularExpressions.Regex]::Match($sot, 'department_count:.*?current_value:\s*(\d+)', [System.Text.RegularExpressions.RegexOptions]::Singleline)
    if ($deptMatch.Success -and $deptMatch.Groups[1].Value -eq "20") { Write-Pass "source-of-truth.yaml: departments = 20" }
    else { Write-Fail "source-of-truth.yaml departments not 20 (found: $($deptMatch.Groups[1].Value))" }
} else {
    Write-Fail "source-of-truth.yaml not found"
}

# 2.2 Registry triple-count (company-registry.yaml, .opencode/agents/*.md, company/agent-registry.json)
$registryYaml = "$Root\company-registry.yaml"
if (Test-Path $registryYaml) {
    # Agents are under company.agents with pattern "  - id:" (2 spaces, dash, space)
    $matches = [System.Text.RegularExpressions.Regex]::Matches((Get-Content $registryYaml -Raw), "^  - id:", [System.Text.RegularExpressions.RegexOptions]::Multiline)
    $agentCount = $matches.Count
    if ($agentCount -eq 90) { Write-Pass "company-registry.yaml: $agentCount agents" }
    else { Write-Fail "company-registry.yaml: $agentCount agents (expected 90)" }
}

$opencodeAgents = Get-ChildItem -Path "$Root\.opencode\agents" -Filter "*.md" -ErrorAction SilentlyContinue
if ($opencodeAgents) {
    if ($opencodeAgents.Count -eq 90) { Write-Pass ".opencode/agents/: $($opencodeAgents.Count) cards" }
    else { Write-Fail ".opencode/agents/: $($opencodeAgents.Count) cards (expected 90)" }
}

$internalJson = "$Root\company\agent-registry.json"
if (Test-Path $internalJson) {
    $json = Get-Content $internalJson -Raw | ConvertFrom-Json
    if ($json.Count -eq 90) { Write-Pass "company/agent-registry.json: $($json.Count) agents" }
    else { Write-Fail "company/agent-registry.json: $($json.Count) agents (expected 90)" }
}

# 2.3 Departments.yaml
$deptYaml = "$Root\company\departments.yaml"
if (Test-Path $deptYaml) {
    # Departments are under departments: with pattern "  - id:" (2 spaces, dash, space)
    $matches = [System.Text.RegularExpressions.Regex]::Matches((Get-Content $deptYaml -Raw), "^  - id:", [System.Text.RegularExpressions.RegexOptions]::Multiline)
    $deptCount = $matches.Count
    if ($deptCount -eq 20) { Write-Pass "company/departments.yaml: $deptCount departments" }
    else { Write-Fail "company/departments.yaml: $deptCount departments (expected 20)" }
}

# ============================================================
# 3. LEGACY TOOL NAMES CHECK
# ============================================================
Write-Status "=== 3. Legacy Tool Names Check ==="

$legacyTools = @("write", "execute", "delegate", "code_interpreter", "web_search", "websearch")
$allPublicFiles = Get-ChildItem -Path "$Root\src" -Recurse -Include "*.ts","*.tsx" -Filter "*.json"

foreach ($tool in $legacyTools) {
    $matches = $allPublicFiles | Select-String -Pattern "(^|[^a-z])$tool([^a-z]|$)" -CaseSensitive
    if ($matches) {
        Write-Fail "Legacy tool name '$tool' found in public files:"
        $matches | Select-Object -Unique Path, LineNumber | ForEach-Object { Write-Host "  $($_.Path):$($_.LineNumber)" }
    } else {
        Write-Pass "No legacy tool '$tool' in public files"
    }
}

# ============================================================
# 4. STALE CLAIMS CHECK (145/152/140+ agents)
# ============================================================
Write-Status "=== 4. Stale Claims Check ==="

$stalePatterns = @("145\s+agents?", "152\s+agents?", "140\+\s+agents?", "151\s+agents?")
$docFiles = Get-ChildItem -Path "$Root\docs" -Recurse -Filter "*.md" | Where-Object { $_.FullName -notmatch "STATUS\.md$" } # Exempt historical
$srcDataFiles = Get-ChildItem -Path "$Root\src\data" -Recurse -Include "*.ts","*.tsx"
$readmeFile = "$Root\README.md"

$allCheckFiles = $docFiles + $srcDataFiles + @($readmeFile)

foreach ($pattern in $stalePatterns) {
    $matches = @($allCheckFiles | Select-String -Pattern $pattern -CaseSensitive)
    if ($matches.Count -gt 0) {
        Write-Fail "Stale agent count pattern '$pattern' found:"
        $uniqueMatches = @{}
        foreach ($m in $matches) {
            $key = "$($m.Path):$($m.LineNumber)"
            if (-not $uniqueMatches.ContainsKey($key)) {
                $uniqueMatches[$key] = $m
            }
        }
        $uniqueMatches.Values | ForEach-Object { Write-Host "  $($_.Path):$($_.LineNumber) $($_.Line.Trim())" }
    } else {
        Write-Pass "No stale pattern '$pattern' in checked files"
    }
}

# ============================================================
# 5. REDIRECT VALIDATION (requires network, optional)
# ============================================================
Write-Status "=== 5. Redirect Validation (requires live host) ==="

$redirects = @(
    @{ Source = "/offerings"; Target = "/solutions" },
    @{ Source = "/work"; Target = "/proof" },
    @{ Source = "/evidence"; Target = "/proof" },
    @{ Source = "/industries"; Target = "/sectors" },
    @{ Source = "/technology"; Target = "/what-we-do" },
    @{ Source = "/why"; Target = "/about" },
    @{ Source = "/process"; Target = "/what-we-do" },
    @{ Source = "/geography"; Target = "/about" },
    @{ Source = "/leadership"; Target = "/about" },
    @{ Source = "/deliverables"; Target = "/what-we-do" },
    @{ Source = "/outcomes"; Target = "/proof" },
    @{ Source = "/partnerships"; Target = "/about" },
    @{ Source = "/trust"; Target = "/proof" },
    @{ Source = "/how-we-help"; Target = "/what-we-do" },
    @{ Source = "/how-we-help/engagement"; Target = "/what-we-do" }
)

# Check vercel.json has correct redirects
$vercelFile = "$Root\vercel.json"
if (Test-Path $vercelFile) {
    $vercel = Get-Content $vercelFile -Raw | ConvertFrom-Json
    if ($vercel.redirects) {
        $vercelRedirects = $vercel.redirects | ForEach-Object { @{ Source = $_.source; Target = $_.destination } }
        foreach ($r in $redirects) {
            $match = $vercelRedirects | Where-Object { $_.Source -eq $r.Source }
            if ($match) {
                if ($match.Target -eq $r.Target) { Write-Pass "vercel.json: $($r.Source) -> $($r.Target)" }
                else { Write-Fail "vercel.json: $($r.Source) -> $($match.Target) (expected $($r.Target))" }
            } else {
                Write-Fail "vercel.json: Missing redirect for $($r.Source)"
            }
        }
    } else {
        Write-Fail "vercel.json has no redirects section"
    }
} else {
    Write-Fail "vercel.json not found"
}

# ============================================================
# 6. CANONICAL SLUGS CHECK
# ============================================================
Write-Status "=== 6. Canonical Slugs Check ==="

$canonicalSolutions = @("ai-company-builder", "digital-presence", "business-automation", "enterprise-deployment", "boardroom-briefing")
$canonicalSectors = @("financial-services", "healthcare", "agriculture", "education", "government")

$legacySolutionSlugs = @("agentic-ai", "digital-transformation", "data-intelligence", "automation", "strategy-advisory")
$legacySectorSlugs = @("development")

$allPublicFiles = Get-ChildItem -Path "$Root\src" -Recurse -Include "*.ts","*.tsx" -Filter "*.json"

# Check for legacy solution slugs
foreach ($slug in $legacySolutionSlugs) {
    $matches = $allPublicFiles | Select-String -Pattern "/solutions/$slug" -CaseSensitive
    if ($matches) {
        Write-Fail "Legacy solution slug '$slug' found in public files:"
        $matches | Select-Object -Unique Path, LineNumber | ForEach-Object { Write-Host "  $($_.Path):$($_.LineNumber)" }
    } else {
        Write-Pass "No legacy solution slug '$slug' in public files"
    }
}

# Check for legacy sector slugs
foreach ($slug in $legacySectorSlugs) {
    $matches = $allPublicFiles | Select-String -Pattern "/industries/$slug|/sectors/$slug" -CaseSensitive
    if ($matches) {
        Write-Fail "Legacy sector slug '$slug' found in public files:"
        $matches | Select-Object -Unique Path, LineNumber | ForEach-Object { Write-Host "  $($_.Path):$($_.LineNumber)" }
    } else {
        Write-Pass "No legacy sector slug '$slug' in public files"
    }
}

# ============================================================
# 7. PUBLIC AGENT REGISTRY SCHEMA COMPLIANCE
# ============================================================
Write-Status "=== 7. Public Agent Registry Schema Compliance ==="

if (Test-Path $publicArtifact) {
    $json = Get-Content $publicArtifact -Raw | ConvertFrom-Json

    # Check all agents have required fields
    $requiredFields = @("id", "name", "title", "type", "department", "department_id", "reports_to", "mission")
    $missingRequired = @()
    foreach ($agent in $json.agents) {
        foreach ($field in $requiredFields) {
            $agentId = if ($agent.PSObject.Properties.Match('id')) { $agent.id } else { 'unknown' }
            if (-not $agent.PSObject.Properties.Match($field) -or [string]::IsNullOrEmpty($agent.$field)) {
                $missingRequired += "Agent ${agentId}: missing $field"
            }
        }

        # Validate type enum
        if ($agent.type -notin @("executive", "specialist", "board")) {
            $missingRequired += "Agent $($agent.id): invalid type '$($agent.type)'"
        }

        # Validate id format (kebab-case)
        if ($agent.id -notmatch '^[a-z0-9]+(-[a-z0-9]+)*$') {
            $missingRequired += "Agent $($agent.id): invalid id format (not kebab-case)"
        }
    }

    if ($missingRequired) {
        Write-Fail "Public agent schema violations:"
        $missingRequired | ForEach-Object { Write-Host "  $_" }
    } else {
        Write-Pass "All public agents have required fields with valid values"
    }

    # Type census
    $typeCounts = $json.agents | Group-Object type
    $exec = ($typeCounts | Where-Object Name -eq "executive").Count
    $spec = ($typeCounts | Where-Object Name -eq "specialist").Count
    $board = ($typeCounts | Where-Object Name -eq "board").Count

    if ($exec -eq 19 -and $spec -eq 64 -and $board -eq 7) {
        Write-Pass "Type census: 19 executive / 64 specialist / 7 board = 90"
    } else {
        Write-Fail "Type census mismatch: $exec executive / $spec specialist / $board board = $($exec+$spec+$board)"
    }
}

# ============================================================
# 8. BRAND TOKEN COMPLIANCE (basic check)
# ============================================================
Write-Status "=== 8. Brand Token Compliance (basic) ==="

$brandTokens = @(
    @{ Name = "navy"; Hex = "070A40" },
    @{ Name = "red"; Hex = "E63946" },
    @{ Name = "cyan"; Hex = "00BFFF" }
)

# Check for invented colors in new architecture docs (docs/architecture/*.md)
$archDocs = Get-ChildItem -Path "$Root\docs\architecture" -Filter "*.md"
$hexColorRegex = '#([0-9a-fA-F]{6})'
foreach ($doc in $archDocs) {
    $content = Get-Content $doc.FullName -Raw
    $matches = [System.Text.RegularExpressions.Regex]::Matches($content, $hexColorRegex)
    foreach ($match in $matches) {
        $hex = $match.Groups[1].Value.ToUpper()
        $known = $brandTokens | Where-Object { $_.Hex -eq $hex }
        if (-not $known -and $hex -notin @("FFFFFF", "F2F2F2", "000000")) {
            Write-Warn "Potential non-brand color #$hex in $($doc.Name) (verify against ADR-020)"
            $script:warnings++
        }
    }
}

# ============================================================
# SUMMARY
# ============================================================
Write-Status "=== Validation Summary ==="
if ($script:failed) {
    Write-Host "$Red[FAILURE]$Reset Architecture validation failed. Fix above issues before proceeding."
    exit 1
} elseif ($script:warnings -gt 0) {
    Write-Host "$Yellow[WARNINGS]$Reset Architecture validation passed with $($script:warnings) warning(s). Review recommended."
    exit 0
} else {
    Write-Host "$Green[SUCCESS]$Reset All architecture validation checks passed."
    exit 0
}
