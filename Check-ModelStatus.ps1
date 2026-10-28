<#
.SYNOPSIS
  One command that reports which models are available RIGHT NOW: OpenCode Zen (free models only),
  OmniRoute, every direct provider in opencode.json, and optionally local Ollama / llama.cpp.

.OUTPUT (written to .\status\)
  model-status.md        human/agent readable report (read this first)
  model-status.json      machine-readable
  available-models.txt   one "provider/model" per line, fastest first (opencode model-id format)

.USAGE (run from the repo folder, next to opencode.json and Test-OpencodeModels.ps1)
  powershell -ExecutionPolicy Bypass -File .\Check-ModelStatus.ps1
  powershell -ExecutionPolicy Bypass -File .\Check-ModelStatus.ps1 -IncludeLocal   # also local models (see warning)
  powershell -ExecutionPolicy Bypass -File .\Check-ModelStatus.ps1 -Deep           # test EVERY OmniRoute model
  powershell -ExecutionPolicy Bypass -File .\Check-ModelStatus.ps1 -Skip groq-direct,nvidia-nim-direct
  powershell -ExecutionPolicy Bypass -File .\Check-ModelStatus.ps1 -NoEnvFile      # use keys already in the environment

.SAFETY
  - Keys are read from .env (whitelist only) or the environment, held in this process only, never printed or written.
  - OpenCode Zen: ONLY models whose id ends in -free (plus big-pickle) are tested. Paid Zen models are listed but never called.
  - OmniRoute: by default only auto/*, *free* and big-pickle entries are called. -Deep calls all of them.
  - -IncludeLocal runs "ollama stop <model>" after each local model so memory is freed. If your agent itself runs on a local
    Ollama model, do NOT use -IncludeLocal from inside that agent.
#>
[CmdletBinding()]
param(
  [string]$ConfigPath = ".\opencode.json",
  [string]$EnvFile = ".\.env",
  [string]$OutDir = ".\status",
  [switch]$NoEnvFile,
  [switch]$IncludeLocal,
  [switch]$Deep,
  [string[]]$Skip = @(),
  [int]$MaxTokens = 64,
  [int]$TimeoutSec = 60,
  [int]$DelayMs = 1500
)

Set-Location $PSScriptRoot
try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 } catch { }
$Skip = @($Skip | ForEach-Object { $_ -split ',' } | Where-Object { $_ })
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
$freeRegex = '(-free$|^big-pickle$)'
$localProviders = @("ollama", "llamacpp")
$script:missingVars = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]
$rows = New-Object System.Collections.Generic.List[object]

# ------------------------------------------------------------------ helpers
function Expand-Env([string]$s) {
  if ([string]::IsNullOrEmpty($s)) { return $s }
  $rx = [regex]'\{env:([A-Za-z0-9_]+)\}'
  $ev = [System.Text.RegularExpressions.MatchEvaluator]{
    param($m)
    $v = [Environment]::GetEnvironmentVariable($m.Groups[1].Value)
    if ([string]::IsNullOrEmpty($v)) { $script:missingVars.Add($m.Groups[1].Value); return "" }
    return $v
  }
  return $rx.Replace($s, $ev)
}

function Add-Row($provider, $model, $status, $http, $ms, $note) {
  $rows.Add([pscustomobject]@{ Provider = $provider; Model = $model; Status = $status; HTTP = $http; Ms = [int]$ms; Note = $note })
}

function Invoke-Get([string]$url, [string]$key, [int]$timeout = 20) {
  $tmpOut = [IO.Path]::GetTempFileName()
  $tmpHdr = [IO.Path]::GetTempFileName()
  try {
    $hdr = "Accept: application/json"
    if (-not [string]::IsNullOrEmpty($key)) { $hdr += "`r`nAuthorization: Bearer $key" }
    [IO.File]::WriteAllText($tmpHdr, $hdr, $utf8NoBom)
    $curlArgs = @("-s", "--max-time", "$timeout", "-o", $tmpOut, "-w", "%{http_code}", $url, "-H", "@$tmpHdr")
    $code = (& curl.exe @curlArgs) -join ""
    $exit = $LASTEXITCODE
    $raw = ""
    if (Test-Path $tmpOut) { $r = Get-Content $tmpOut -Raw -Encoding UTF8; if ($r) { $raw = $r } }
    return [pscustomobject]@{ Code = "$code".Trim(); Exit = $exit; Raw = $raw }
  }
  finally { Remove-Item $tmpOut, $tmpHdr -Force -ErrorAction SilentlyContinue }
}

function Get-Ids($r) {
  try {
    $j = $r.Raw | ConvertFrom-Json
    if ($j.data) { return @($j.data | ForEach-Object { $_.id } | Where-Object { $_ }) }
    if ($j.models) { return @($j.models | ForEach-Object { $_.name } | Where-Object { $_ }) }
  } catch { }
  return @()
}

function Test-ListFailure($provider, $r, $label) {
  # returns $true (and records a row) if the listing call failed
  if ($r.Exit -ne 0 -or $r.Code -eq "000" -or [string]::IsNullOrEmpty($r.Code)) {
    Add-Row $provider "($label)" "UNREACHABLE" "-" 0 "curl exit $($r.Exit) - service down or no network"
    return $true
  }
  if ($r.Code -eq "401" -or $r.Code -eq "403") { Add-Row $provider "($label)" "AUTH" $r.Code 0 "key rejected when listing models"; return $true }
  if ($r.Code -ne "200") { Add-Row $provider "($label)" "ERROR" $r.Code 0 "listing returned HTTP $($r.Code)"; return $true }
  return $false
}

# ------------------------------------------------------------------ preflight
if (-not (Test-Path $ConfigPath)) { Write-Host "Config not found: $ConfigPath" -ForegroundColor Red; exit 1 }
$tester = Join-Path $PSScriptRoot "Test-OpencodeModels.ps1"
if (-not (Test-Path $tester)) { Write-Host "Test-OpencodeModels.ps1 must sit next to this file." -ForegroundColor Red; exit 1 }
if (-not (Get-Command curl.exe -ErrorAction SilentlyContinue)) { Write-Host "curl.exe not found." -ForegroundColor Red; exit 1 }
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }

$cfg = Get-Content $ConfigPath -Raw | ConvertFrom-Json

# env var the config expects -> names it may have in .env (first match wins)
$map = [ordered]@{
  GROQ_API_KEY          = @("GROQ_API_KEY")
  NVIDIA_API_KEY        = @("NVIDIA_API_KEY")
  MISTRAL_API_KEY       = @("MISTRAL_API_KEY")
  GOOGLE_API_KEY        = @("GOOGLE_API_KEY", "GEMINI_API_KEY")
  OLLAMA_API_KEY        = @("OLLAMA_API_KEY", "OLLAMA_CLOUD_API_KEY")
  CLOUDFLARE_ACCOUNT_ID = @("CLOUDFLARE_ACCOUNT_ID", "CLODFLARE_ACCOUNT_ID")
  CLOUDFLARE_API_TOKEN  = @("CLOUDFLARE_API_TOKEN")
  OMNIROUTE_API_KEY     = @("OMNIROUTE_API_KEY")
  OPENCODE_API_KEY      = @("OPENCODE_API_KEY")
}
$file = @{}
if (-not $NoEnvFile -and (Test-Path $EnvFile)) {
  Get-Content $EnvFile | Where-Object { $_ -match '^\s*[^#\s][^=]*=' } | ForEach-Object {
    $k, $v = $_ -split '=', 2
    $file[($k.Trim() -replace '^export\s+', '')] = $v.Trim().Trim('"').Trim("'")
  }
}
Write-Host "== Keys (names only; True = available to this run) ==" -ForegroundColor Cyan
foreach ($m in $map.GetEnumerator()) {
  foreach ($cand in $m.Value) {
    if ($file[$cand]) { [Environment]::SetEnvironmentVariable($m.Key, $file[$cand], 'Process'); break }
  }
  $ok = [bool][Environment]::GetEnvironmentVariable($m.Key)
  $c = "Red"; if ($ok) { $c = "Green" }
  Write-Host ("{0,-24} {1}" -f $m.Key, $ok) -ForegroundColor $c
}

# ------------------------------------------------------------------ DNS
Write-Host "`n== DNS ==" -ForegroundColor Cyan
$hosts = New-Object System.Collections.Generic.List[string]
$hosts.Add("opencode.ai")
foreach ($prov in $cfg.provider.PSObject.Properties) {
  $b = [string]$prov.Value.options.baseURL
  if (-not $b) { continue }
  try { $h = ([uri]($b -replace '\{env:[^}]+\}', 'x')).Host } catch { continue }
  if ($h -and $h -ne "127.0.0.1" -and $h -ne "localhost" -and -not $hosts.Contains($h)) { $hosts.Add($h) }
}
$dnsBad = New-Object System.Collections.Generic.List[string]
foreach ($h in $hosts) {
  try { $null = [System.Net.Dns]::GetHostAddresses($h); Write-Host ("{0,-42} OK" -f $h) -ForegroundColor Green }
  catch { $dnsBad.Add($h); Write-Host ("{0,-42} FAILED" -f $h) -ForegroundColor Red }
}
if ($dnsBad.Count -gt 0) {
  $warnings.Add("DNS lookup failed for: " + ($dnsBad -join ", ") + ". UNREACHABLE results for these hosts are a network problem, not a model problem.")
}

# ------------------------------------------------------------------ smallModel sanity
$small = [string]$cfg.smallModel
if ($small -like "opencode/*") {
  $sid = $small.Substring(9)
  if ($sid -notmatch $freeRegex) {
    $warnings.Add("smallModel is '$small', a PAID OpenCode Zen model (Zen needs billing). Consider a free one, e.g. opencode/big-pickle or opencode/deepseek-v4-flash-free.")
  }
}

# ------------------------------------------------------------------ build the cloud test config
$tmpProviders = [ordered]@{}

# direct providers (everything except local + omniroute)
foreach ($prov in $cfg.provider.PSObject.Properties) {
  $n = $prov.Name
  if ($Skip -contains $n) { continue }
  if ($localProviders -contains $n -or $n -eq "omniroute") { continue }
  $tmpProviders[$n] = $prov.Value
}

# OmniRoute (discover what it serves; call a safe subset unless -Deep)
$omni = $cfg.provider.omniroute
if ($omni -and ($Skip -notcontains "omniroute")) {
  $script:missingVars.Clear()
  $base = Expand-Env ([string]$omni.options.baseURL)
  $key = Expand-Env ([string]$omni.options.apiKey)
  if ($script:missingVars.Count -gt 0) {
    Add-Row "omniroute" "(all models)" "NO_KEY" "-" 0 ("env var not set: " + (($script:missingVars | Select-Object -Unique) -join ", "))
  } else {
    $r = Invoke-Get ($base.TrimEnd('/') + "/models") $key
    if (-not (Test-ListFailure "omniroute" $r "service")) {
      $served = Get-Ids $r
      $cfgIds = @($omni.models.PSObject.Properties | ForEach-Object { $_.Name })
      $missing = @($cfgIds | Where-Object { $served -notcontains $_ })
      foreach ($mm in $missing) { Add-Row "omniroute" $mm "NOT_FOUND" "-" 0 "in opencode.json but not served by OmniRoute" }
      if ($Deep) { $pick = $served } else { $pick = @($served | Where-Object { $_ -match '^auto' -or $_ -match 'free' -or $_ -match 'big-pickle' }) }
      $skipped = $served.Count - $pick.Count
      if ($skipped -gt 0) { $warnings.Add("OmniRoute serves $($served.Count) models; $skipped were listed but NOT called (use -Deep to call every one; some upstreams may be paid).") }
      $ms = [ordered]@{}
      foreach ($id in $pick) { $ms[$id] = [ordered]@{ name = $id } }
      if ($ms.Count -gt 0) {
        $tmpProviders["omniroute"] = [ordered]@{ name = "OmniRoute"; npm = $omni.npm; options = $omni.options; models = $ms }
      }
    }
  }
}

# OpenCode Zen: discover, test FREE models only
if ($Skip -notcontains "opencode-zen") {
  $zkey = [Environment]::GetEnvironmentVariable("OPENCODE_API_KEY")
  $zr = Invoke-Get "https://opencode.ai/zen/v1/models" $zkey
  if (-not (Test-ListFailure "opencode-zen" $zr "service")) {
    $zids = Get-Ids $zr
    $zfree = @($zids | Where-Object { $_ -match $freeRegex })
    $zpaid = @($zids | Where-Object { $_ -notmatch $freeRegex })
    if ($zpaid.Count -gt 0) { $warnings.Add("OpenCode Zen lists $($zpaid.Count) paid models (not called): " + (($zpaid | Select-Object -First 12) -join ", ") + $(if ($zpaid.Count -gt 12) { ", ..." } else { "" })) }
    if (-not $zkey) {
      Add-Row "opencode-zen" "(free models)" "NO_KEY" "-" 0 "env var not set: OPENCODE_API_KEY"
    } elseif ($zfree.Count -eq 0) {
      Add-Row "opencode-zen" "(free models)" "NOT_FOUND" "-" 0 "no model ids ending in -free were listed"
    } else {
      $ms = [ordered]@{}
      foreach ($id in $zfree) { $ms[$id] = [ordered]@{ name = $id } }
      $tmpProviders["opencode-zen"] = [ordered]@{
        name = "OpenCode Zen (free models)"; npm = "@ai-sdk/openai-compatible"
        options = [ordered]@{ baseURL = "https://opencode.ai/zen/v1"; apiKey = "{env:OPENCODE_API_KEY}" }
        models = $ms
      }
    }
  }
}

# ------------------------------------------------------------------ run the cloud tests
if ($tmpProviders.Count -gt 0) {
  $tmpCfg = Join-Path $OutDir ".status-cloud.tmp.json"
  $tmpObj = [ordered]@{ provider = $tmpProviders }
  [IO.File]::WriteAllText($tmpCfg, ($tmpObj | ConvertTo-Json -Depth 20), $utf8NoBom)
  Write-Host "`n== Testing cloud providers ==" -ForegroundColor Cyan
  $cloud = @(& $tester -ConfigPath $tmpCfg -KeepGoing -PassThru -MaxTokens $MaxTokens -TimeoutSec $TimeoutSec -DelayMs $DelayMs |
    Where-Object { $_.PSObject.Properties.Name -contains 'Status' })
  Remove-Item $tmpCfg -Force -ErrorAction SilentlyContinue
  foreach ($c in $cloud) { $rows.Add($c) }
}

# ------------------------------------------------------------------ local models (opt-in)
if ($IncludeLocal) {
  Write-Host "`n== Testing local models (one at a time; slow on first load) ==" -ForegroundColor Cyan
  $localProv = [ordered]@{}
  foreach ($pn in $localProviders) {
    $lp = $cfg.provider.$pn
    if ($lp -and ($Skip -notcontains $pn)) { $localProv[$pn] = $lp }
  }
  if ($localProv.Count -gt 0) {
    $tmpLocal = Join-Path $OutDir ".status-local.tmp.json"
    [IO.File]::WriteAllText($tmpLocal, ([ordered]@{ provider = $localProv } | ConvertTo-Json -Depth 20), $utf8NoBom)
    $haveOllama = [bool](Get-Command ollama -ErrorAction SilentlyContinue)
    foreach ($pn in $localProv.Keys) {
      foreach ($m in $localProv[$pn].models.PSObject.Properties) {
        $name = $m.Name
        $isDecision = $false
        if ($pn -eq "ollama" -and $haveOllama) {
          $show = (& ollama show $name 2>&1 | Out-String)
          if ($show -match '(?im)^\s*decision\s*$') { $isDecision = $true }
        }
        if ($isDecision) {
          $body = '{"model":' + ($name | ConvertTo-Json -Compress) + ',"state":"Checkout returns 500 errors.","questions":{"q":{"type":"choice","instructions":"Which label fits?","criteria":{"bug":"Software errors","billing":"Payments"}}}}'
          $url = ([string]$localProv[$pn].options.baseURL).TrimEnd('/') + "/systemone"
          $sw = [Diagnostics.Stopwatch]::StartNew()
          try {
            $resp = Invoke-RestMethod -Uri $url -Method Post -ContentType "application/json" -Body $body -TimeoutSec 240
            $sw.Stop()
            if ($resp.answers.q.choice) { Add-Row $pn "$name (decision model)" "PASS" "200" $sw.ElapsedMilliseconds "systemone answered: $($resp.answers.q.choice)" }
            else { Add-Row $pn "$name (decision model)" "ERROR" "200" $sw.ElapsedMilliseconds "systemone returned no choice" }
          } catch {
            $sw.Stop()
            Add-Row $pn "$name (decision model)" "ERROR" "-" $sw.ElapsedMilliseconds ("systemone failed: " + $_.Exception.Message.Substring(0, [Math]::Min(80, $_.Exception.Message.Length)))
          }
        } else {
          $res = @(& $tester -ConfigPath $tmpLocal -Only $pn -OnlyModel $name -KeepGoing -PassThru -MaxTokens $MaxTokens -DelayMs 500 |
            Where-Object { $_.PSObject.Properties.Name -contains 'Status' })
          foreach ($x in $res) { $rows.Add($x) }
        }
        if ($pn -eq "ollama" -and $haveOllama) { & ollama stop $name 2>&1 | Out-Null }
      }
    }
    Remove-Item $tmpLocal -Force -ErrorAction SilentlyContinue
  }
} else {
  $warnings.Add("Local models (ollama, llamacpp) were NOT tested. Run with -IncludeLocal to test them.")
}

# ------------------------------------------------------------------ report
$okSet      = @("PASS", "PASS_NOTEXT")
$unsureSet  = @("RATE_LIMIT", "TIMEOUT", "SERVER_ERR")
$untestSet  = @("NO_KEY", "SKIPPED")
$all = @($rows | Where-Object { $_ })
$avail   = @($all | Where-Object { $okSet -contains $_.Status } | Sort-Object Ms)
$unsure  = @($all | Where-Object { $unsureSet -contains $_.Status })
$untest  = @($all | Where-Object { $untestSet -contains $_.Status })
$failed  = @($all | Where-Object { ($okSet -notcontains $_.Status) -and ($unsureSet -notcontains $_.Status) -and ($untestSet -notcontains $_.Status) })

function Get-Health($g) {
  $g = @($g)
  $o = @($g | Where-Object { $okSet -contains $_.Status }).Count
  if ($o -gt 0) { return "UP ($o working)" }
  if (@($g | Where-Object { $_.Status -eq "NO_KEY" }).Count -eq $g.Count) { return "NOT TESTED (key missing)" }
  if (@($g | Where-Object { $_.Status -eq "UNREACHABLE" }).Count -gt 0) { return "DOWN / UNREACHABLE" }
  if (@($g | Where-Object { $_.Status -eq "AUTH" }).Count -gt 0) { return "KEY REJECTED" }
  if (@($g | Where-Object { $unsureSet -contains $_.Status }).Count -gt 0) { return "UNCERTAIN (rate limited / busy)" }
  return "NOTHING WORKING"
}
$health = @($all | Group-Object Provider | ForEach-Object {
  [pscustomobject]@{
    Provider = $_.Name
    Health   = (Get-Health $_.Group)
    Working  = @($_.Group | Where-Object { $okSet -contains $_.Status }).Count
    Failing  = @($_.Group | Where-Object { ($okSet -notcontains $_.Status) -and ($untestSet -notcontains $_.Status) -and ($unsureSet -notcontains $_.Status) }).Count
    Unsure   = @($_.Group | Where-Object { $unsureSet -contains $_.Status }).Count
  }
})

$now = Get-Date
$stampLocal = $now.ToString("yyyy-MM-dd HH:mm:ss")
$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine("# Model status report")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("Generated: $stampLocal (local time). Results are a snapshot; free tiers change without notice.")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("**$($avail.Count) models available**, $($failed.Count) failing, $($unsure.Count) uncertain, $($untest.Count) not tested.")
if ($warnings.Count -gt 0) {
  [void]$sb.AppendLine("")
  [void]$sb.AppendLine("## Warnings")
  foreach ($w in $warnings) { [void]$sb.AppendLine("- $w") }
}
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Provider health")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("| Provider | Health | Working | Failing | Uncertain |")
[void]$sb.AppendLine("|---|---|---|---|---|")
foreach ($h in $health) { [void]$sb.AppendLine("| $($h.Provider) | $($h.Health) | $($h.Working) | $($h.Failing) | $($h.Unsure) |") }
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Available now (fastest first)")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("Model id format is provider/model, as opencode expects.")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("| Model | Response ms | Note |")
[void]$sb.AppendLine("|---|---|---|")
foreach ($a in $avail) {
  $note = ""
  if ($a.Status -eq "PASS_NOTEXT") { $note = "empty reply at $MaxTokens tokens (reasoning model; usable)" }
  [void]$sb.AppendLine("| $($a.Provider)/$($a.Model) | $($a.Ms) | $note |")
}
if ($failed.Count -gt 0) {
  [void]$sb.AppendLine("")
  [void]$sb.AppendLine("## Failing")
  [void]$sb.AppendLine("")
  [void]$sb.AppendLine("| Model | Status | HTTP | Note |")
  [void]$sb.AppendLine("|---|---|---|---|")
  foreach ($f in $failed) { [void]$sb.AppendLine("| $($f.Provider)/$($f.Model) | $($f.Status) | $($f.HTTP) | $($f.Note) |") }
}
if ($unsure.Count -gt 0) {
  [void]$sb.AppendLine("")
  [void]$sb.AppendLine("## Uncertain (retry later; this is not proof they are broken)")
  [void]$sb.AppendLine("")
  [void]$sb.AppendLine("| Model | Status | HTTP | Note |")
  [void]$sb.AppendLine("|---|---|---|---|")
  foreach ($u in $unsure) { [void]$sb.AppendLine("| $($u.Provider)/$($u.Model) | $($u.Status) | $($u.HTTP) | $($u.Note) |") }
}
if ($untest.Count -gt 0) {
  [void]$sb.AppendLine("")
  [void]$sb.AppendLine("## Not tested")
  [void]$sb.AppendLine("")
  foreach ($n in $untest) { [void]$sb.AppendLine("- $($n.Provider) $($n.Model): $($n.Status) - $($n.Note)") }
}

[IO.File]::WriteAllText((Join-Path $OutDir "model-status.md"), $sb.ToString(), $utf8NoBom)
[IO.File]::WriteAllText((Join-Path $OutDir "available-models.txt"), (($avail | ForEach-Object { "$($_.Provider)/$($_.Model)" }) -join "`r`n"), $utf8NoBom)
$json = [ordered]@{
  generated = $now.ToUniversalTime().ToString("o")
  summary   = [ordered]@{ available = $avail.Count; failing = $failed.Count; uncertain = $unsure.Count; notTested = $untest.Count }
  warnings  = @($warnings)
  providers = @($health)
  available = @($avail | ForEach-Object { [ordered]@{ model = "$($_.Provider)/$($_.Model)"; ms = $_.Ms } })
  failing   = @($failed | ForEach-Object { [ordered]@{ model = "$($_.Provider)/$($_.Model)"; status = $_.Status; http = $_.HTTP; note = $_.Note } })
  uncertain = @($unsure | ForEach-Object { [ordered]@{ model = "$($_.Provider)/$($_.Model)"; status = $_.Status; http = $_.HTTP; note = $_.Note } })
  notTested = @($untest | ForEach-Object { [ordered]@{ model = "$($_.Provider)/$($_.Model)"; status = $_.Status; note = $_.Note } })
}
[IO.File]::WriteAllText((Join-Path $OutDir "model-status.json"), ($json | ConvertTo-Json -Depth 6), $utf8NoBom)

Write-Host "`n================ MODEL STATUS ($stampLocal) ================" -ForegroundColor Cyan
Write-Host ("{0,-22} {1,-34} {2,8} {3,8} {4,10}" -f "Provider", "Health", "Working", "Failing", "Uncertain")
foreach ($h in $health) {
  Write-Host ("{0,-22} {1,-34} {2,8} {3,8} {4,10}" -f $h.Provider, $h.Health, $h.Working, $h.Failing, $h.Unsure)
}
Write-Host "$($avail.Count) available, $($failed.Count) failing, $($unsure.Count) uncertain, $($untest.Count) not tested." -ForegroundColor Cyan
foreach ($w in $warnings) { Write-Host "WARNING: $w" -ForegroundColor Yellow }
Write-Host "Report: $(Join-Path $OutDir 'model-status.md')" -ForegroundColor Cyan
Write-Host "Usable model ids: $(Join-Path $OutDir 'available-models.txt')" -ForegroundColor Cyan
