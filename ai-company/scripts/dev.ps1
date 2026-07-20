<#
.SYNOPSIS
    Developer onboarding and environment management script for AI Company Builder.

.DESCRIPTION
    Sets up a complete development environment, runs validation checks,
    and provides status information. Designed for new developer onboarding.

.PARAMETER Action
    The action to perform: setup, test, lint, status, clean, generate, all
    Default is "all" (full onboarding).

.EXAMPLE
    .\scripts\dev.ps1              # Full onboarding
    .\scripts\dev.ps1 setup        # Just setup
    .\scripts\dev.ps1 test         # Run tests only
    .\scripts\dev.ps1 status       # Show project status
#>

param(
    [ValidateSet("setup", "test", "lint", "status", "clean", "generate", "all")]
    [string]$Action = "all"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

# ── Helpers ──────────────────────────────────────────────────────────

function Write-Step {
    param([string]$Message)
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Write-Ok {
    param([string]$Message)
    Write-Host "    [OK] $Message" -ForegroundColor Green
}

function Write-Warn {
    param([string]$Message)
    Write-Host "    [WARN] $Message" -ForegroundColor Yellow
}

function Write-Fail {
    param([string]$Message)
    Write-Host "    [FAIL] $Message" -ForegroundColor Red
}

function Test-CommandExists {
    param([string]$Command)
    $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
}

# ── Actions ──────────────────────────────────────────────────────────

function Invoke-Setup {
    Write-Step "Checking prerequisites"

    # Python
    if (Test-CommandExists "python") {
        $pyVer = python --version 2>&1
        Write-Ok "Python: $pyVer"
    } else {
        Write-Fail "Python not found. Install Python 3.12+ from https://python.org"
        exit 1
    }

    # Git
    if (Test-CommandExists "git") {
        Write-Ok "Git: $(git --version)"
    } else {
        Write-Warn "Git not found — version control features unavailable"
    }

    Write-Step "Creating virtual environment"
    $venvPath = Join-Path $ProjectRoot ".venv"
    if (-not (Test-Path $venvPath)) {
        python -m venv $venvPath
        Write-Ok "Created .venv at $venvPath"
    } else {
        Write-Ok "Virtual environment already exists"
    }

    # Activate
    $activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
    if (Test-Path $activateScript) {
        . $activateScript
        Write-Ok "Activated virtual environment"
    }

    Write-Step "Installing project in editable mode with dev dependencies"
    Push-Location $ProjectRoot
    pip install -e ".[dev]" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Ok "Dependencies installed successfully"
    } else {
        Write-Fail "Failed to install dependencies"
        Pop-Location
        exit 1
    }
    Pop-Location

    Write-Step "Installing pre-commit hooks"
    if (Test-CommandExists "pre-commit") {
        pre-commit install 2>&1 | Out-Null
        Write-Ok "Pre-commit hooks installed"
    } else {
        pip install pre-commit 2>&1 | Out-Null
        pre-commit install 2>&1 | Out-Null
        Write-Ok "Pre-commit installed and hooks configured"
    }

    Write-Step "Generating agents from registry"
    python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Ok "Agents generated successfully"
    } else {
        Write-Warn "Agent generation had issues — check company-registry.yaml"
    }

    Write-Host "`n==> Setup complete!" -ForegroundColor Green
    Write-Host "    Activate the venv: .venv\Scripts\Activate.ps1" -ForegroundColor Gray
    Write-Host "    Run tests:         .\scripts\dev.ps1 test" -ForegroundColor Gray
    Write-Host "    Run linter:        .\scripts\dev.ps1 lint" -ForegroundColor Gray
    Write-Host "    Check status:      .\scripts\dev.ps1 status" -ForegroundColor Gray
}

function Invoke-Test {
    Write-Step "Running test suite"
    Push-Location $ProjectRoot
    pytest --tb=short -q --cov=ai_company --cov-report=term-missing
    $exitCode = $LASTEXITCODE
    Pop-Location
    if ($exitCode -ne 0) {
        Write-Fail "Some tests failed"
        exit $exitCode
    }
    Write-Ok "All tests passed"
}

function Invoke-Lint {
    Write-Step "Running Ruff linter"
    ruff check src/ tests/
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "Lint errors found"
        exit 1
    }
    Write-Ok "Lint clean"

    Write-Step "Running Ruff format check"
    ruff format --check src/ tests/
    if ($LASTEXITCODE -ne 0) {
        Write-Warn "Format issues found — run: ruff format src/ tests/"
    } else {
        Write-Ok "Format clean"
    }

    Write-Step "Running Mypy type check"
    mypy src/ --ignore-missing-imports
    if ($LASTEXITCODE -ne 0) {
        Write-Warn "Type errors found (non-blocking)"
    } else {
        Write-Ok "Type check clean"
    }
}

function Invoke-Status {
    Write-Step "Project Status"

    # Python version
    $pyVer = python --version 2>&1
    Write-Host "  Python:          $pyVer" -ForegroundColor White

    # Git branch
    if (Test-CommandExists "git") {
        $branch = git branch --show-current 2>$null
        $commit = git log --oneline -1 2>$null
        Write-Host "  Git branch:      $branch" -ForegroundColor White
        Write-Host "  Latest commit:   $commit" -ForegroundColor White
    }

    # Virtual env
    $venvPath = Join-Path $ProjectRoot ".venv"
    if (Test-Path $venvPath) {
        Write-Host "  Virtual env:     .venv/ (active)" -ForegroundColor Green
    } else {
        Write-Host "  Virtual env:     NOT SET UP — run: .\scripts\dev.ps1 setup" -ForegroundColor Red
    }

    # Dependencies installed?
    $check = python -c "import ai_company" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Package:         installed (editable)" -ForegroundColor Green
    } else {
        Write-Host "  Package:         NOT INSTALLED — run: .\scripts\dev.ps1 setup" -ForegroundColor Red
    }

    # Agent count
    $agentCount = (Get-ChildItem -Path ".opencode\agents\*.md" -ErrorAction SilentlyContinue | Measure-Object).Count
    Write-Host "  Generated agents: $agentCount" -ForegroundColor White

    # Test count
    $testFiles = (Get-ChildItem -Path "tests\**\*.py" -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
    Write-Host "  Test files:      $testFiles" -ForegroundColor White

    # Inbox status
    $inboxPath = Join-Path $ProjectRoot ".opencode\inbox.json"
    if (Test-Path $inboxPath) {
        $tasks = Get-Content $inboxPath -Raw | python -c "import sys,json; d=json.load(sys.stdin); print(len(d))"
        Write-Host "  Pending tasks:   $tasks" -ForegroundColor White
    } else {
        Write-Host "  Pending tasks:   0 (no inbox)" -ForegroundColor White
    }

    # CI status
    Write-Host "`n  Quick commands:" -ForegroundColor Cyan
    Write-Host "    pytest                          Run tests" -ForegroundColor Gray
    Write-Host "    ruff check src/                 Lint" -ForegroundColor Gray
    Write-Host "    ruff format src/                Format" -ForegroundColor Gray
    Write-Host "    mypy src/                       Type check" -ForegroundColor Gray
    Write-Host "    pre-commit run --all-files      Pre-commit checks" -ForegroundColor Gray
    Write-Host "    ai-company --help               CLI help" -ForegroundColor Gray
}

function Invoke-Clean {
    Write-Step "Cleaning build artifacts"

    $dirs = @(
        "__pycache__",
        "*.egg-info",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "htmlcov",
        ".coverage",
        "dist",
        "build"
    )

    foreach ($pattern in $dirs) {
        Get-ChildItem -Path $ProjectRoot -Filter $pattern -Recurse -Directory -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    }

    # Remove coverage files
    Get-ChildItem -Path $ProjectRoot -Filter "coverage.xml" -File -ErrorAction SilentlyContinue |
        Remove-Item -Force -ErrorAction SilentlyContinue

    Write-Ok "Build artifacts cleaned"
}

function Invoke-Generate {
    Write-Step "Regenerating agents from company-registry.yaml"
    Push-Location $ProjectRoot
    python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"
    if ($LASTEXITCODE -eq 0) {
        Write-Ok "Agents regenerated successfully"
    } else {
        Write-Fail "Agent generation failed"
        Pop-Location
        exit 1
    }
    Pop-Location
}

# ── Main dispatch ────────────────────────────────────────────────────

Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "  AI Company Builder — Developer Setup" -ForegroundColor Cyan
Write-Host "======================================`n" -ForegroundColor Cyan

switch ($Action) {
    "setup"    { Invoke-Setup }
    "test"     { Invoke-Test }
    "lint"     { Invoke-Lint }
    "status"   { Invoke-Status }
    "clean"    { Invoke-Clean }
    "generate" { Invoke-Generate }
    "all" {
        Invoke-Setup
        Invoke-Lint
        Invoke-Test
        Invoke-Generate
        Invoke-Status
    }
}

Write-Host "`nDone.`n" -ForegroundColor Green
