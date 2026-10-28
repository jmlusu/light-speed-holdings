<#
.SYNOPSIS
  Sends ONE tiny chat request to every model in opencode.json and prints a pass/fail table.

.EXAMPLES
  .\Test-OpencodeModels.ps1                              # everything (local models are slow to load)
  .\Test-OpencodeModels.ps1 -SkipLocal                   # cloud providers only
  .\Test-OpencodeModels.ps1 -Only groq-direct,cerebras-direct
  .\Test-OpencodeModels.ps1 -Only ollama -OnlyModel qwen3-coder:30b
  .\Test-OpencodeModels.ps1 -Only ollama-cloud-direct -KeepGoing   # do not stop after repeated 402s
  .\Test-OpencodeModels.ps1 -Skip omniroute -OutCsv results.csv

  If scripts are blocked:
  powershell -ExecutionPolicy Bypass -File .\Test-OpencodeModels.ps1 -SkipLocal

.NOTES
  - Reads provider URLs and {env:VAR} key names from the config. Keys are never printed or written.
  - Costs a few tokens per model (MaxTokens caps the reply). Free tiers: expect some RATE_LIMIT rows.
  - Requires curl.exe (ships with Windows 10/11).
#>
[CmdletBinding()]
param(
  [string]$ConfigPath = ".\opencode.json",
  [string[]]$Only = @(),
  [string[]]$Skip = @(),
  [string[]]$OnlyModel = @(),
  [switch]$SkipLocal,
  [switch]$KeepGoing,
  [switch]$PassThru,
  [int]$MaxTokens = 64,
  [int]$TimeoutSec = 60,
  [int]$LocalTimeoutSec = 240,
  [int]$DelayMs = 1500,
  [string]$OutCsv = ""
)

# powershell -File passes "a,b,c" as ONE string; split it so comma lists work either way.
$Only      = @($Only      | ForEach-Object { $_ -split ',' } | Where-Object { $_ })
$Skip      = @($Skip      | ForEach-Object { $_ -split ',' } | Where-Object { $_ })
$OnlyModel = @($OnlyModel | ForEach-Object { $_ -split ',' } | Where-Object { $_ })

$localProviders = @("ollama", "llamacpp")
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
$script:missingVars = New-Object System.Collections.Generic.List[string]

function Expand-Env([string]$s) {
  if ([string]::IsNullOrEmpty($s)) { return $s }
  $rx = [regex]'\{env:([A-Za-z0-9_]+)\}'
  $ev = [System.Text.RegularExpressions.MatchEvaluator]{
    param($m)
    $name = $m.Groups[1].Value
    $v = [Environment]::GetEnvironmentVariable($name)
    if ([string]::IsNullOrEmpty($v)) { $script:missingVars.Add($name); return "" }
    return $v
  }
  return $rx.Replace($s, $ev)
}

function Get-ErrNote([string]$raw) {
  if ([string]::IsNullOrWhiteSpace($raw)) { return "" }
  $note = $raw
  try {
    $j = $raw | ConvertFrom-Json
    if ($j.error -and $j.error.message) { $note = [string]$j.error.message }
    elseif ($j.error -is [string]) { $note = $j.error }
    elseif ($j.message) { $note = [string]$j.message }
    elseif ($j.detail) { $note = [string]$j.detail }
    elseif ($j.errors) { $note = ($j.errors | ConvertTo-Json -Compress) }
  } catch { }
  $note = ($note -replace '\s+', ' ').Trim()
  if ($note.Length -gt 90) { $note = $note.Substring(0, 90) + "..." }
  return $note
}

function Invoke-ChatProbe([string]$baseUrl, [string]$key, [string]$model, [int]$timeout) {
  $tmpBody = [IO.Path]::GetTempFileName()
  $tmpHdr  = [IO.Path]::GetTempFileName()
  $tmpOut  = [IO.Path]::GetTempFileName()
  try {
    $modelJson = $model | ConvertTo-Json -Compress
    $body = '{"model":' + $modelJson + ',"messages":[{"role":"user","content":"Reply with the single word: ok"}],"max_tokens":' + $MaxTokens + '}'
    [IO.File]::WriteAllText($tmpBody, $body, $utf8NoBom)

    $hdr = "Content-Type: application/json"
    if (-not [string]::IsNullOrEmpty($key)) { $hdr += "`r`nAuthorization: Bearer $key" }
    [IO.File]::WriteAllText($tmpHdr, $hdr, $utf8NoBom)

    $url = $baseUrl.TrimEnd('/') + "/chat/completions"
    $curlArgs = @("-s", "--max-time", "$timeout", "-o", $tmpOut, "-w", "%{http_code}",
                  "-X", "POST", $url, "-H", "@$tmpHdr", "--data-binary", "@$tmpBody")
    $sw = [Diagnostics.Stopwatch]::StartNew()
    $code = (& curl.exe @curlArgs) -join ""
    $exit = $LASTEXITCODE
    $sw.Stop()

    $raw = ""
    if (Test-Path $tmpOut) {
      $r = Get-Content $tmpOut -Raw -Encoding UTF8
      if ($r) { $raw = $r }
    }
    return [pscustomobject]@{ Code = $code.Trim(); Exit = $exit; Ms = [int]$sw.ElapsedMilliseconds; Raw = $raw }
  }
  finally {
    Remove-Item $tmpBody, $tmpHdr, $tmpOut -Force -ErrorAction SilentlyContinue
  }
}

function Get-Verdict($r) {
  if ($r.Exit -eq 28) { return @("TIMEOUT", "no reply within the time limit") }
  if ($r.Exit -ne 0 -or $r.Code -eq "000" -or [string]::IsNullOrEmpty($r.Code)) {
    return @("UNREACHABLE", "curl exit $($r.Exit) - service down or no network")
  }
  switch -Regex ($r.Code) {
    '^200$' {
      $j = $null
      try { $j = $r.Raw | ConvertFrom-Json } catch { }
      if ($j -and $j.choices -and @($j.choices).Count -gt 0) {
        $txt = [string]$j.choices[0].message.content
        if ([string]::IsNullOrWhiteSpace($txt)) { return @("PASS_NOTEXT", "200 but empty text (reasoning model? try -MaxTokens 256)") }
        $txt = ($txt -replace '\s+', ' ').Trim()
        if ($txt.Length -gt 30) { $txt = $txt.Substring(0, 30) }
        return @("PASS", $txt)
      }
      return @("ERROR", "200 but no choices: " + (Get-ErrNote $r.Raw))
    }
    '^401$'       { return @("AUTH", (Get-ErrNote $r.Raw)) }
    '^403$'       { return @("FORBIDDEN", (Get-ErrNote $r.Raw)) }
    '^404$'       { return @("NOT_FOUND", (Get-ErrNote $r.Raw)) }
    '^400$'       { return @("BAD_REQUEST", (Get-ErrNote $r.Raw)) }
    '^402$'       { return @("NO_CREDIT", (Get-ErrNote $r.Raw)) }
    '^429$'       { return @("RATE_LIMIT", (Get-ErrNote $r.Raw)) }
    '^5\d\d$'     { return @("SERVER_ERR", (Get-ErrNote $r.Raw)) }
    default       { return @("ERROR", (Get-ErrNote $r.Raw)) }
  }
}

function Get-Color([string]$status) {
  switch ($status) {
    "PASS"        { return "Green" }
    "PASS_NOTEXT" { return "Green" }
    "RATE_LIMIT"  { return "Yellow" }
    "TIMEOUT"     { return "Yellow" }
    "NO_KEY"      { return "DarkGray" }
    "SKIPPED"     { return "DarkGray" }
    default       { return "Red" }
  }
}

function Add-Result($provider, $model, $status, $http, $ms, $note, [int]$n = 1) {
  $row = [pscustomobject]@{
    Provider = $provider; Model = $model; Status = $status
    HTTP = $http; Ms = $ms; Note = $note; N = $n
  }
  $script:results.Add($row)
  $line = "{0,-20} {1,-48} {2,-12} {3,4} {4,6}ms  {5}" -f $provider, $model, $status, $http, $ms, $note
  Write-Host $line -ForegroundColor (Get-Color $status)
}

# ---------------------------------------------------------------- main
if (-not (Test-Path $ConfigPath)) {
  Write-Host "Config not found: $ConfigPath (run from the folder containing opencode.json, or pass -ConfigPath)" -ForegroundColor Red
  exit 1
}
if (-not (Get-Command curl.exe -ErrorAction SilentlyContinue)) {
  Write-Host "curl.exe not found." -ForegroundColor Red
  exit 1
}

$cfg = Get-Content $ConfigPath -Raw | ConvertFrom-Json
$script:results = New-Object System.Collections.Generic.List[object]

Write-Host ("Testing with max_tokens={0}, delay={1}ms. Local models load into RAM on first call, so they can be slow." -f $MaxTokens, $DelayMs) -ForegroundColor Cyan
Write-Host ""

foreach ($prov in $cfg.provider.PSObject.Properties) {
  $pname = $prov.Name
  $p = $prov.Value

  if ($Only.Count -gt 0 -and $Only -notcontains $pname) { continue }
  if ($Skip -contains $pname) { continue }
  if ($SkipLocal -and $localProviders -contains $pname) { continue }

  $models = @($p.models.PSObject.Properties)
  if ($OnlyModel.Count -gt 0) { $models = @($models | Where-Object { $OnlyModel -contains $_.Name }) }
  $total = $models.Count
  if ($total -eq 0) { continue }

  $script:missingVars.Clear()
  $base = Expand-Env ([string]$p.options.baseURL)
  $hasKeyField = -not [string]::IsNullOrEmpty([string]$p.options.apiKey)
  $key = $null
  if ($hasKeyField) { $key = Expand-Env ([string]$p.options.apiKey) }

  if ($script:missingVars.Count -gt 0) {
    $names = ($script:missingVars | Select-Object -Unique) -join ", "
    Add-Result $pname "(all $total models)" "NO_KEY" "-" 0 "env var not set: $names" $total
    continue
  }
  if ($hasKeyField -and [string]::IsNullOrEmpty($key)) {
    Add-Result $pname "(all $total models)" "NO_KEY" "-" 0 "apiKey resolved to empty" $total
    continue
  }

  $timeout = $TimeoutSec
  if ($localProviders -contains $pname) { $timeout = $LocalTimeoutSec }

  $i = 0
  $noCreditStreak = 0
  foreach ($m in $models) {
    $i++
    $r = Invoke-ChatProbe $base $key $m.Name $timeout
    if ($r.Code -eq "429") {
      Start-Sleep -Seconds 8
      $r = Invoke-ChatProbe $base $key $m.Name $timeout
    }
    $v = Get-Verdict $r
    Add-Result $pname $m.Name $v[0] $r.Code $r.Ms $v[1]

    # Provider-wide failures: no point hammering the rest.
    # 402 (NO_CREDIT) and 403 (FORBIDDEN) are often per-model (plan gating or rollout),
    # so only stop after 2 in a row. 401 (AUTH) and UNREACHABLE always stop the provider.
    if (@("NO_CREDIT", "FORBIDDEN") -contains $v[0]) { $noCreditStreak++ } else { $noCreditStreak = 0 }
    if (@("AUTH", "UNREACHABLE") -contains $v[0] -or ($noCreditStreak -ge 2 -and -not $KeepGoing)) {
      $left = $total - $i
      if ($left -gt 0) {
        Add-Result $pname "(remaining $left models)" "SKIPPED" "-" 0 "provider-level failure above" $left
      }
      break
    }
    Start-Sleep -Milliseconds $DelayMs
  }
}

if ($script:results.Count -eq 0) {
  $names = ($cfg.provider.PSObject.Properties.Name) -join ", "
  Write-Host "Nothing was tested. Check -Only / -Skip spelling. Providers in the config: $names" -ForegroundColor Yellow
  exit 1
}

# ---------------------------------------------------------------- report
Write-Host ""
Write-Host "================ RESULTS (notes are in the lines above, or use -OutCsv) ================" -ForegroundColor Cyan
Write-Host ("{0,-20} {1,-48} {2,-12} {3,5} {4,8}" -f "Provider", "Model", "Status", "HTTP", "Ms")
foreach ($r in $script:results) {
  Write-Host ("{0,-20} {1,-48} {2,-12} {3,5} {4,8}" -f $r.Provider, $r.Model, $r.Status, $r.HTTP, $r.Ms) -ForegroundColor (Get-Color $r.Status)
}

Write-Host "================ SUMMARY (models) ================" -ForegroundColor Cyan
$summary = $script:results | Group-Object Provider | ForEach-Object {
  $g = @($_.Group)
  $sum = {
    param($rows)
    $s = ($rows | Measure-Object -Property N -Sum).Sum
    if ($s) { [int]$s } else { 0 }
  }
  $pass    = @($g | Where-Object { $_.Status -like "PASS*" })
  $unsure  = @($g | Where-Object { @("RATE_LIMIT", "TIMEOUT") -contains $_.Status })
  $nottest = @($g | Where-Object { @("NO_KEY", "SKIPPED") -contains $_.Status })
  $fail    = @($g | Where-Object {
    ($_.Status -notlike "PASS*") -and (@("RATE_LIMIT", "TIMEOUT", "NO_KEY", "SKIPPED") -notcontains $_.Status)
  })
  [pscustomobject]@{
    Provider  = $_.Name
    PASS      = & $sum $pass
    FAIL      = & $sum $fail
    UNSURE    = & $sum $unsure
    NOT_TESTED = & $sum $nottest
  }
}
Write-Host ("{0,-20} {1,5} {2,5} {3,7} {4,11}" -f "Provider", "PASS", "FAIL", "UNSURE", "NOT_TESTED")
foreach ($s in $summary) {
  Write-Host ("{0,-20} {1,5} {2,5} {3,7} {4,11}" -f $s.Provider, $s.PASS, $s.FAIL, $s.UNSURE, $s.NOT_TESTED)
}

Write-Host "Legend: PASS = works. PASS_NOTEXT = reached the model but reply was empty (usually a reasoning model; still usable)." -ForegroundColor Gray
Write-Host "NOT_FOUND = model ID not served (fix or remove in opencode.json). AUTH = bad or missing key (401). FORBIDDEN = 403, often a model not enabled for your account. BAD_REQUEST = often a wrong ID or unsupported parameter; read the Note." -ForegroundColor Gray
Write-Host "RATE_LIMIT/TIMEOUT = UNKNOWN, rerun later with -Only <provider>. NO_KEY/SKIPPED = not tested." -ForegroundColor Gray

if ($OutCsv) {
  $script:results | Select-Object Provider, Model, Status, HTTP, Ms, Note | Export-Csv -Path $OutCsv -NoTypeInformation -Encoding UTF8
  Write-Host "Saved: $OutCsv" -ForegroundColor Cyan
}

if ($PassThru) { $script:results.ToArray() }
