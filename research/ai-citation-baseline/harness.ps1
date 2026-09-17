<#
.SYNOPSIS
Driver for the AI Citation Baseline (ticket #312). Emits the 20 deterministic prompts
and, when -Auto is passed and API keys exist in .env, calls Gemini / Perplexity /
Big Pickle and saves verbatim transcripts.

.DESCRIPTION
Engines measured in the ledger: chatgpt, perplexity, gemini.
Big Pickle (OPENCODE_API_KEY + OPENCODE_API_BASE) is an OPTIONAL internal calibration
engine; it is never counted in results-ledger.csv.

Mode A (default): prints prompt + paste/copy instructions for the Human CEO.
Mode B (-Auto): calls any keyed engine automatically (Gemini / Perplexity / Big Pickle).
ChatGPT is ALWAYS manual: the consumer UI is the surface we measure.

The prompts in $Script:Keywords are the canonical locked strings. They MUST stay
byte-identical with research/ai-citation-baseline/keywords.md and results-ledger.csv.

.EXAMPLE
pwsh -NoProfile -File research/ai-citation-baseline/harness.ps1 -KeywordsOnly
pwsh -NoProfile -File research/ai-citation-baseline/harness.ps1 -Engine all
pwsh -NoProfile -File research/ai-citation-baseline/harness.ps1 -Engine gemini -Auto -Limit 2 -WhatIf
pwsh -NoProfile -File research/ai-citation-baseline/harness.ps1 -Engine chatgpt -Keyword k01
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [ValidateSet('all', 'chatgpt', 'perplexity', 'gemini', 'bigpickle')]
    [string]$Engine = 'all',
    [string]$Keyword = '',
    [int]$Limit = 0,
    [switch]$Auto,
    [switch]$KeywordsOnly
)

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# --- paths ---------------------------------------------------------------
$Script:BaselineDir = $PSScriptRoot
$Script:TranscriptBase = Join-Path $Script:BaselineDir 'transcripts'
$Script:RepoRoot = Split-Path -Parent (Split-Path -Parent $Script:BaselineDir)
$Script:EnvFile = Join-Path $Script:RepoRoot '.env'

# --- canonical keyword registry (k01..k20) -------------------------------
# MUST match keywords.md + results-ledger.csv verbatim.
$Script:Keywords = [ordered]@{
    'k01' = @{ slug = 'lightspeed-holdings';         territory = 'CB'; prompt = 'What is Lightspeed Holdings? If you know of a specific company with that name, include its location, what it does, and any website you can cite.' }
    'k02' = @{ slug = 'jack-mlusu';                  territory = 'CB'; prompt = 'Who is Jacob Jack Mlusu? Summarize his background, current role, and any companies or publications associated with him, with sources.' }
    'k03' = @{ slug = 'agentic-ai-company';          territory = 'CB'; prompt = 'How do you build an agentic AI company - an organization where AI agents perform meaningful work? Describe key design decisions, governance mechanisms, and real examples you can cite.' }
    'k04' = @{ slug = 'ai-native-enterprise-africa'; territory = 'CB'; prompt = 'What does an AI-native enterprise look like in Africa? Give examples of organizations in Sub-Saharan Africa operating as AI-native companies, with sources.' }
    'k05' = @{ slug = 'haomtgv-framework';           territory = 'GP'; prompt = 'Explain the H-A-O-M-T-G-V framework for agentic AI governance. What do the seven layers mean, and where does the framework come from?' }
    'k06' = @{ slug = '144-agent-company';           territory = 'CB'; prompt = 'Is there a real company run by 144 AI agents? Which real AI-agent companies are operating today, at what scale, and how are they governed?' }
    'k07' = @{ slug = 'hitl-governance';             territory = 'GP'; prompt = 'How do human-in-the-loop (HITL) approval gates work for AI agents? What tier levels exist, and which companies implement them in production?' }
    'k08' = @{ slug = 'model-router';                territory = 'CB'; prompt = 'What is an AI model router, and why do companies running many AI agents need one? Give architecture examples with sources.' }
    'k09' = @{ slug = 'ceo-control-plane';           territory = 'CB'; prompt = 'What is a CEO control plane for an AI agent workforce - a dashboard that lets one human direct agents? How are message buses and task graphs used to route work? Give examples.' }
    'k10' = @{ slug = 'agent-registry-policy';       territory = 'CB'; prompt = 'What is an agent registry in an agentic AI company? How are agent roles, permissions, and policies catalogued and enforced?' }
    'k11' = @{ slug = 'agent-workforce-kpis';        territory = 'CB'; prompt = 'How do you measure the health and cost of an AI agent workforce? What KPIs - like task completion rate and cost per workflow - matter most?' }
    'k12' = @{ slug = 'ai-audit-trails';             territory = 'GP'; prompt = 'How do immutable audit trails work for AI agent actions? What makes an agent decision log trustworthy and verifiable?' }
    'k13' = @{ slug = 'agentic-ai-malawi';           territory = 'UC'; prompt = 'What is the current state of agentic AI in Malawi? Which companies or institutions are deploying AI agents, and what frameworks guide them?' }
    'k14' = @{ slug = 'agentic-ai-sadc';             territory = 'GP'; prompt = 'How are SADC countries preparing for agentic AI? Is there a regional governance standard for autonomous AI systems?' }
    'k15' = @{ slug = 'au-continental-ai-strategy';  territory = 'GP'; prompt = 'What does the African Union Continental AI Strategy require of member states, and how should countries like Malawi implement it?' }
    'k16' = @{ slug = 'malawi-data-protection-ai';   territory = 'GP'; prompt = 'How does the Malawi Data Protection Act (2017/2024) apply to AI systems and agentic AI? What does compliance require?' }
    'k17' = @{ slug = 'ai-small-business-africa';    territory = 'UC'; prompt = 'How can a small business in Africa practically use agentic AI? Give real examples of non-tech SMEs using AI agents, with sources.' }
    'k18' = @{ slug = 'js-stopover-bar';             territory = 'UC'; prompt = 'What is J&S StopOver Bar, and what role does AI play in its operations?' }
    'k19' = @{ slug = 'vsla-sacco-ai';               territory = 'UC'; prompt = 'How can AI agents help village savings and loan associations (VSLAs) and SACCOs with record-keeping and financial management?' }
    'k20' = @{ slug = '90-day-ai-pilot';             territory = 'RS'; prompt = 'What is a 90-day AI pilot, and how does it avoid legacy technology debt and rip-and-replace risk when deploying AI?' }
}

# --- helpers --------------------------------------------------------------
function Get-EnvValue {
    param([string]$Name)
    if (-not (Test-Path -LiteralPath $Script:EnvFile)) { return $null }
    $line = Get-Content -LiteralPath $Script:EnvFile | Where-Object {
        $_ -match '^[A-Za-z_][A-Za-z0-9_]*=' -and $_ -like ($Name + '=*')
    } | Select-Object -First 1
    if ($null -eq $line) { return $null }
    $value = $line.Substring($line.IndexOf('=') + 1).Trim()
    if ($value.Length -ge 2 -and $value[0] -eq '"' -and $value[$value.Length - 1] -eq '"') {
        $value = $value.Substring(1, $value.Length - 2)
    }
    if ([string]::IsNullOrWhiteSpace($value)) { return $null }
    return $value
}

function Get-SelectedKeywords {
    $all = @($Script:Keywords.GetEnumerator())
    if ([string]::IsNullOrWhiteSpace($Keyword)) { return ,$all }
    $hits = @($all | Where-Object {
        $_.Key -eq $Keyword -or $_.Value.slug -eq $Keyword -or $_.Key -like ($Keyword + '*')
    })
    if ($hits.Count -eq 0) { throw "No keyword matches '$Keyword' (expect k01..k20 or a slug, e.g. k13-agentic-ai-malawi)." }
    return ,$hits
}

function Get-TranscriptPath {
    param([string]$Engine, [string]$Key, [hashtable]$Info)
    $num = '{0:D2}' -f [int]($Key -replace 'k', '')
    $fileName = $num + '-' + $Info.slug + '.txt'
    return Join-Path (Join-Path (Join-Path $Script:TranscriptBase (Get-Date -Format 'yyyy-MM-dd')) $Engine) $fileName
}

function Save-Transcript {
    param([string]$Path, [string]$Prompt, [string]$Reply, [string]$Meta, [string]$Status = 'OK')
    $dir = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    $content = @(
        'STATUS: ' + $Status,
        'SAVED: ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'),
        'META: ' + $Meta,
        'PROMPT:',
        $Prompt,
        'ENGINE REPLY:',
        $Reply
    ) -join [Environment]::NewLine
    Set-Content -LiteralPath $Path -Value $content -Encoding UTF8
}

function Show-ManualInstructions {
    param([string]$Engine, [string]$Key, [hashtable]$Info, [string]$TranscriptPath)
    $label = switch ($Engine) {
        'chatgpt'   { 'ChatGPT (new chat at https://chatgpt.com)' }
        'perplexity'{ 'Perplexity (new chat at https://www.perplexity.ai)' }
        'gemini'    { 'Gemini (new chat at https://gemini.google.com)' }
        'bigpickle' { 'Big Pickle (new OpenCode chat)' }
        default     { $Engine }
    }
    Write-Host ('--- ' + $Engine + ' ' + $Key + '-' + $Info.slug + ' ---')
    Write-Output ('PROMPT to paste into a NEW ' + $label + ' chat (' + $Key + '-' + $Info.slug + '):')
    Write-Output $Info.prompt
    Write-Output ('TRANSCRIPT TARGET: ' + $TranscriptPath)
    Write-Output ''
}

# --- engine API calls (all return @{ Reply=...; Meta=... }) --------------
function Invoke-Gemini {
    param([string]$Prompt)
    $apiKey = Get-EnvValue 'GEMINI_API_KEY'
    if ([string]::IsNullOrWhiteSpace($apiKey)) { throw 'GEMINI_API_KEY not set' }
    $model = 'gemini-3.5-flash'
    $uri = 'https://generativelanguage.googleapis.com/v1beta/models/' + $model + ':generateContent'
    $body = @{
        contents         = @( @{ role = 'user'; parts = @( @{ text = $Prompt } ) } )
        generationConfig = @{ temperature = 0.2 }
    } | ConvertTo-Json -Depth 10
    $headers = @{ 'x-goog-api-key' = $apiKey; 'Content-Type' = 'application/json' }
    $resp = Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -Body $body -TimeoutSec 90
    $candidates = @($resp.candidates)
    if ($null -eq $resp.candidates -or $candidates.Count -eq 0 -or $null -eq $candidates[0] -or $null -eq $candidates[0].content) {
        throw 'Gemini returned no candidates'
    }
    $first = $candidates[0]
    $parts = @($first.content.parts)
    if ($parts.Count -eq 0) { throw 'Gemini returned no text parts' }
    $text = ($parts | ForEach-Object { $_.text }) -join ''
    if ([string]::IsNullOrWhiteSpace($text)) { throw 'Gemini returned empty text' }
    $meta = 'model=' + $model
    if ($null -ne $first.groundingMetadata) {
        $meta += ' grounding=' + (($first.groundingMetadata | ConvertTo-Json -Compress -Depth 6))
    }
    if ($null -ne $resp.usageMetadata) {
        $meta += ' usage=' + (($resp.usageMetadata | ConvertTo-Json -Compress -Depth 4))
    }
    return @{ Reply = $text; Meta = $meta }
}

function Invoke-Perplexity {
    param([string]$Prompt)
    $apiKey = Get-EnvValue 'PERPLEXITY_API_KEY'
    if ([string]::IsNullOrWhiteSpace($apiKey)) { throw 'PERPLEXITY_API_KEY not set' }
    $uri = 'https://api.perplexity.ai/chat/completions'
    $body = @{
        model    = 'sonar'
        messages = @( @{ role = 'user'; content = $Prompt } )
    } | ConvertTo-Json -Depth 8
    $headers = @{ 'Authorization' = 'Bearer ' + $apiKey; 'Content-Type' = 'application/json' }
    $resp = Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -Body $body -TimeoutSec 90
    $choices = @($resp.choices)
    if ($null -eq $resp.choices -or $choices.Count -eq 0 -or $null -eq $choices[0] -or $null -eq $choices[0].message) {
        throw 'Perplexity returned no choices'
    }
    $text = [string]$choices[0].message.content
    if ([string]::IsNullOrWhiteSpace($text)) { throw 'Perplexity returned empty content' }
    $meta = 'model=' + $resp.model
    $cits = @($resp.citations)
    if ($null -ne $resp.citations -and $cits.Count -gt 0) {
        $meta += ' citations=' + ($cits -join ' | ')
    }
    return @{ Reply = $text; Meta = $meta }
}

function Invoke-BigPickle {
    param([string]$Prompt)
    $apiBase = Get-EnvValue 'OPENCODE_API_BASE'
    $apiKey = Get-EnvValue 'OPENCODE_API_KEY'
    if ([string]::IsNullOrWhiteSpace($apiBase)) { throw 'OPENCODE_API_BASE not set' }
    if ([string]::IsNullOrWhiteSpace($apiKey)) { throw 'OPENCODE_API_KEY not set' }
    $uri = $apiBase.TrimEnd('/') + '/chat/completions'
    $body = @{
        model       = 'big-pickle'
        messages    = @( @{ role = 'user'; content = $Prompt } )
        temperature = 0.2
    } | ConvertTo-Json -Depth 8
    $headers = @{ 'Authorization' = 'Bearer ' + $apiKey; 'Content-Type' = 'application/json' }
    $resp = Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -Body $body -TimeoutSec 120
    $choices = @($resp.choices)
    if ($null -eq $resp.choices -or $choices.Count -eq 0 -or $null -eq $choices[0] -or $null -eq $choices[0].message) {
        throw 'Big Pickle returned no choices'
    }
    $text = [string]$choices[0].message.content
    if ([string]::IsNullOrWhiteSpace($text)) { throw 'Big Pickle returned empty content' }
    return @{ Reply = $text; Meta = 'engine=bigpickle model=' + $resp.model }
}

function Invoke-EngineCall {
    param([string]$EngineName, [string]$Prompt)
    switch ($EngineName) {
        'gemini'    { return Invoke-Gemini -Prompt $Prompt }
        'perplexity'{ return Invoke-Perplexity -Prompt $Prompt }
        'bigpickle' { return Invoke-BigPickle -Prompt $Prompt }
        default     { throw ($EngineName + ' has no automated path') }
    }
}

# --- main -----------------------------------------------------------------
$engines = switch ($Engine) {
    'all' { @('chatgpt', 'perplexity', 'gemini') }
    default { @($Engine) }
}
$selected = Get-SelectedKeywords

if ($KeywordsOnly) {
    Write-Host 'Keyword registry (20) - deterministic prompts:'
    foreach ($item in $selected) {
        $info = $item.Value
        Write-Output ($item.Key + ' | ' + $info.slug + ' | ' + $info.territory + ' | ' + $info.prompt)
    }
    Write-Host ('Emitted ' + $selected.Count + ' prompts. Done.')
    exit 0
}

$emitted = 0
$autoCalls = 0
$manual = 0

foreach ($eng in $engines) {
    $count = 0
    foreach ($item in $selected) {
        if ($Limit -gt 0 -and $count -ge $Limit) { break }
        $count++
        $key = $item.Key
        $info = $item.Value
        $path = Get-TranscriptPath -Engine $eng -Key $key -Info $info

        if ($eng -eq 'chatgpt') {
            Show-ManualInstructions -Engine $eng -Key $key -Info $info -TranscriptPath $path
            $manual++
            $emitted++
            continue
        }

        $apiKey = Get-EnvValue ($eng.ToUpperInvariant() + '_API_KEY')
        if ($eng -eq 'bigpickle') { $apiKey = Get-EnvValue 'OPENCODE_API_KEY' }

        $baseOk = $true
        if ($eng -eq 'bigpickle') { $baseOk = -not [string]::IsNullOrWhiteSpace((Get-EnvValue 'OPENCODE_API_BASE')) }

        $canAuto = $Auto -and (-not [string]::IsNullOrWhiteSpace($apiKey)) -and $baseOk
        if (-not $canAuto) {
            $reason = 'no -Auto flag passed'
            if ($Auto -and [string]::IsNullOrWhiteSpace($apiKey)) { $reason = ($eng.ToUpperInvariant() + '_API_KEY not found in .env') }
            elseif ($Auto -and $eng -eq 'bigpickle' -and -not $baseOk) { $reason = 'OPENCODE_API_BASE not found in .env' }
            Write-Host ($eng + ': ' + $reason + ' -> manual fallback')
            Show-ManualInstructions -Engine $eng -Key $key -Info $info -TranscriptPath $path
            $manual++
            $emitted++
            continue
        }

        $target = $eng + '/' + $key + '-' + $info.slug
        if ($PSCmdlet.ShouldProcess($target, 'call engine API and save verbatim transcript')) {
            try {
                $result = Invoke-EngineCall -EngineName $eng -Prompt $info.prompt
                Save-Transcript -Path $path -Prompt $info.prompt -Reply $result.Reply -Meta $result.Meta
                Write-Host ($eng + ' ' + $key + ' -> saved ' + $path)
                Write-Output $result.Reply
                $autoCalls++
            } catch {
                $err = $_.Exception.Message
                Save-Transcript -Path $path -Prompt $info.prompt -Reply '' -Meta $err -Status 'ERROR'
                Write-Host ('ERROR ' + $eng + ' ' + $key + ': ' + $err + ' -> transcript marked ERROR')
            }
        }
        $emitted++
    }
}

Write-Host ''
Write-Host ('Done. Prompts emitted: ' + $emitted + '  |  automated API calls: ' + $autoCalls + '  |  manual (paste): ' + $manual)
Write-Host ('Transcripts: ' + (Join-Path $Script:TranscriptBase (Get-Date -Format 'yyyy-MM-dd')))
Write-Host 'Next: score each transcript in results-ledger.csv per README sections 3.4 and 4.'
