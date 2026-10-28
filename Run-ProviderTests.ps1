<#
.SYNOPSIS
  Loads only the keys opencode.json needs from .env (never prints values), checks DNS,
  then runs Test-OpencodeModels.ps1 against the cloud providers.

.USAGE
  Put this file next to Test-OpencodeModels.ps1 and opencode.json (the repo folder), then run:
    powershell -ExecutionPolicy Bypass -File .\Run-ProviderTests.ps1
#>
param(
  [string]$EnvFile = ".\.env"
)

Set-Location $PSScriptRoot

# env var the config expects  ->  names it may have in .env (first match wins)
$map = [ordered]@{
  GROQ_API_KEY          = @("GROQ_API_KEY")
  NVIDIA_API_KEY        = @("NVIDIA_API_KEY")
  MISTRAL_API_KEY       = @("MISTRAL_API_KEY")
  GOOGLE_API_KEY        = @("GOOGLE_API_KEY", "GEMINI_API_KEY")
  OLLAMA_API_KEY        = @("OLLAMA_API_KEY", "OLLAMA_CLOUD_API_KEY")
  CLOUDFLARE_ACCOUNT_ID = @("CLOUDFLARE_ACCOUNT_ID", "CLODFLARE_ACCOUNT_ID")
  CLOUDFLARE_API_TOKEN  = @("CLOUDFLARE_API_TOKEN")
  OMNIROUTE_API_KEY     = @("OMNIROUTE_API_KEY")
}

if (-not (Test-Path $EnvFile)) {
  Write-Host "No .env found at $EnvFile (current folder: $(Get-Location))" -ForegroundColor Red
  exit 1
}

$file = @{}
Get-Content $EnvFile | Where-Object { $_ -match '^\s*[^#\s][^=]*=' } | ForEach-Object {
  $k, $v = $_ -split '=', 2
  $file[($k.Trim() -replace '^export\s+', '')] = $v.Trim().Trim('"').Trim("'")
}

Write-Host "`n== Keys (True = loaded; the .env name it came from is shown, never the value) ==" -ForegroundColor Cyan
foreach ($m in $map.GetEnumerator()) {
  $used = $null
  foreach ($cand in $m.Value) {
    if ($file[$cand]) {
      [Environment]::SetEnvironmentVariable($m.Key, $file[$cand], 'Process')
      $used = $cand
      break
    }
  }
  $ok = [bool][Environment]::GetEnvironmentVariable($m.Key)
  $line = "{0,-24} {1,-6} from: {2}" -f $m.Key, $ok, $used
  if ($ok) { Write-Host $line -ForegroundColor Green } else { Write-Host $line -ForegroundColor Red }
}

Write-Host "`n== DNS check ==" -ForegroundColor Cyan
foreach ($h in @("api.mistral.ai", "generativelanguage.googleapis.com", "ollama.com", "api.cloudflare.com", "api.groq.com", "integrate.api.nvidia.com")) {
  try {
    $null = [System.Net.Dns]::GetHostAddresses($h)
    Write-Host ("{0,-40} OK" -f $h) -ForegroundColor Green
  } catch {
    Write-Host ("{0,-40} FAILED (DNS) - fix your network/DNS before trusting results" -f $h) -ForegroundColor Red
  }
}

$tester = Join-Path $PSScriptRoot "Test-OpencodeModels.ps1"
if (-not (Test-Path $tester)) {
  Write-Host "`nTest-OpencodeModels.ps1 not found next to this file." -ForegroundColor Red
  exit 1
}

Write-Host "`n== Cloud providers (not NVIDIA) ==" -ForegroundColor Cyan
& $tester -Only mistral-direct,gemini-studio-direct,cloudflare-direct,ollama-cloud-direct,groq-direct -KeepGoing -OutCsv results-cloud.csv

Write-Host "`n== NVIDIA (3 minute timeout, its free queue is slow) ==" -ForegroundColor Cyan
& $tester -Only nvidia-nim-direct -TimeoutSec 180 -OutCsv results-nvidia.csv
