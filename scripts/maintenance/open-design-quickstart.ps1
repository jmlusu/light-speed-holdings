[CmdletBinding()]
param(
    [switch]$SkipInstall
)

function Fail([string]$Message) {
    Write-Host "ERROR: $Message" -ForegroundColor Red
    exit 1
}

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$odRoot = Join-Path $repoRoot 'open-design'
$cli = Join-Path $odRoot 'apps\daemon\dist\cli.js'

if (-not (Test-Path -LiteralPath (Join-Path $odRoot 'package.json'))) {
    Fail "Open Design workspace not found at $odRoot."
}

$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node) {
    Fail "Node.js not found. Install Node 24 from https://nodejs.org/ and reopen the terminal."
}

$nodeVersion = (& node --version).Trim()
if ($nodeVersion -notmatch '^v(\d+)\.') {
    Fail "Could not parse node --version output: $nodeVersion"
}

$nodeMajor = [int]$Matches[1]
if ($nodeMajor -ne 24) {
    Fail "Node $nodeVersion detected. Open Design requires Node ~24 (Node 22 is unsupported)."
}

$pnpm = Get-Command pnpm -ErrorAction SilentlyContinue
if (-not $pnpm) {
    Fail "pnpm not found. Run: npm install -g pnpm@10.33.2"
}

$pnpmVersion = (& pnpm --version).Trim()
if ($pnpmVersion -ne '10.33.2') {
    Write-Host "WARN: pnpm $pnpmVersion detected; expected 10.33.2. If install fails, run: npm install -g pnpm@10.33.2" -ForegroundColor Yellow
}

Push-Location $odRoot
try {
    if (-not $SkipInstall) {
        Write-Host "Installing dependencies (builds apps/daemon/dist via postinstall; better-sqlite3 compiles, ~2 min)..."
        & pnpm install
        if ($LASTEXITCODE -ne 0) {
            Fail "pnpm install failed with exit code $LASTEXITCODE."
        }
    }

    if (-not (Test-Path -LiteralPath $cli)) {
        Fail "Daemon build missing at $cli. Run 'pnpm install' or 'pnpm bootstrap' in $odRoot."
    }

    Write-Host "Open Design version:"
    & node $cli version

    & node $cli daemon status --json 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Daemon already running."
    }
    else {
        Write-Host "Starting daemon detached (od daemon start is foreground/blocking)..."
        Start-Process -FilePath 'node' -ArgumentList @('apps/daemon/dist/cli.js', '--no-open') -WorkingDirectory $odRoot -WindowStyle Hidden

        $ready = $false
        for ($i = 0; $i -lt 15; $i++) {
            Start-Sleep -Seconds 2
            & node $cli daemon status --json 2>$null | Out-Null
            if ($LASTEXITCODE -eq 0) {
                $ready = $true
                break
            }
        }

        if (-not $ready) {
            Fail "Daemon did not become ready within 30 seconds. Run 'node apps/daemon/dist/cli.js --no-open' in $odRoot to see the error."
        }
    }

    Write-Host "Daemon status:"
    & node $cli daemon status --json
    if ($LASTEXITCODE -ne 0) {
        Fail "od daemon status failed with exit code $LASTEXITCODE."
    }

    Write-Host "MCP install preview (no changes written):"
    & node $cli mcp install opencode --print --json
    if ($LASTEXITCODE -ne 0) {
        Fail "od mcp install preview failed with exit code $LASTEXITCODE."
    }

    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "  1. Skill: .agents\skills\ls-od-runtime\SKILL.md"
    Write-Host "  2. Docs: open-design\QUICKSTART.md"
    Write-Host "  3. Install MCP: node apps/daemon/dist/cli.js mcp install opencode"
    Write-Host "  4. Stop daemon: node apps/daemon/dist/cli.js daemon stop"
}
finally {
    Pop-Location
}
