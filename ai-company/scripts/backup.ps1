<#
.SYNOPSIS
    Backup critical AI Company Builder state directories.

.DESCRIPTION
    Creates timestamped tar.gz backups of:
    - .opencode/    (agent files, inbox, cycle state)
    - company/      (registry, config, KPI definitions)
    - results/      (task execution artifacts)
    - logs/         (structured log files)
    - memory/       (memory store, if exists)

    Backups are stored in a backupper/ directory with rotation.

.PARAMETER BackupDir
    Where to store backups. Default: ./backups

.PARAMETER RetentionDays
    Delete backups older than this many days. Default: 30

.PARAMETER DryRun
    Show what would be backed up without actually creating archives.

.EXAMPLE
    .\scripts\backup.ps1
    .\scripts\backup.ps1 -RetentionDays 7
    .\scripts\backup.ps1 -DryRun
#>

[CmdletBinding()]
param(
    [string]$BackupDir = "./backups",
    [int]$RetentionDays = 30,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

# ── Directories to back up ────────────────────────────────────
$sourceDirs = @(
    ".opencode",
    "company",
    "results",
    "logs",
    "memory"
)

Write-Host "AI Company Builder — Backup" -ForegroundColor Cyan
Write-Host "===========================" -ForegroundColor Cyan
Write-Host "Timestamp:  $timestamp"
Write-Host "Backup dir: $BackupDir"
Write-Host "Retention:  $RetentionDays days"
Write-Host ""

# ── Ensure backup directory exists ────────────────────────────
if (-not $DryRun) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
}

$totalSize = 0
$backedUp = @()

foreach ($dir in $sourceDirs) {
    if (Test-Path $dir) {
        $archiveName = "ai-company-$dir-$timestamp.tar.gz"
        $archivePath = Join-Path $BackupDir $archiveName

        # Get directory size
        $size = (Get-ChildItem -Recurse -File $dir | Measure-Object -Property Length -Sum).Sum
        $sizeMB = [math]::Round($size / 1MB, 2)
        $totalSize += $size

        if ($DryRun) {
            Write-Host "  [DRY RUN] Would archive: $dir ($sizeMB MB) -> $archiveName" -ForegroundColor Yellow
        } else {
            Write-Host "  Backing up: $dir ($sizeMB MB)" -ForegroundColor Green
            try {
                tar -czf $archivePath $dir 2>$null
                if ($LASTEXITCODE -eq 0) {
                    $backedUp += $archiveName
                    Write-Host "    -> $archiveName" -ForegroundColor DarkGreen
                } else {
                    Write-Host "    WARNING: tar exited with code $LASTEXITCODE" -ForegroundColor Yellow
                    # Fallback: use Compress-Archive (creates .zip, rename to .tar.gz for convention)
                    $zipPath = $archivePath -replace '\.tar\.gz$', '.zip'
                    Compress-Archive -Path $dir -DestinationPath $zipPath -Force
                    $backedUp += ($archiveName -replace '\.tar\.gz$', '.zip')
                    Write-Host "    -> (fallback zip) $($archiveName -replace '\.tar\.gz$', '.zip')" -ForegroundColor DarkYellow
                }
            } catch {
                Write-Host "    ERROR: $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "  Skipping: $dir (not found)" -ForegroundColor DarkGray
    }
}

# ── Summary ───────────────────────────────────────────────────
$totalMB = [math]::Round($totalSize / 1MB, 2)
Write-Host ""
Write-Host "Total size: $totalMB MB" -ForegroundColor Cyan
if (-not $DryRun -and $backedUp.Count -gt 0) {
    Write-Host "Archives created: $($backedUp.Count)" -ForegroundColor Cyan
}

# ── Rotation: delete old backups ──────────────────────────────
if (-not $DryRun -and (Test-Path $BackupDir)) {
    $cutoff = (Get-Date).AddDays(-$RetentionDays)
    $oldFiles = Get-ChildItem -Path $BackupDir -File | Where-Object {
        $_.LastWriteTime -lt $cutoff -and ($_.Name -match "ai-company-.*\.(tar\.gz|zip)$")
    }

    if ($oldFiles.Count -gt 0) {
        Write-Host ""
        Write-Host "Rotating $($oldFiles.Count) old backup(s) (>$RetentionDays days)..." -ForegroundColor Yellow
        foreach ($f in $oldFiles) {
            if ($DryRun) {
                Write-Host "  [DRY RUN] Would delete: $($f.Name)" -ForegroundColor Yellow
            } else {
                Remove-Item $f.FullName -Force
                Write-Host "  Deleted: $($f.Name)" -ForegroundColor DarkYellow
            }
        }
    }
}

# ── List current backups ──────────────────────────────────────
if (Test-Path $BackupDir) {
    Write-Host ""
    Write-Host "Current backups in $BackupDir :" -ForegroundColor Cyan
    Get-ChildItem -Path $BackupDir -File | Sort-Object LastWriteTime -Descending | Select-Object -First 10 | ForEach-Object {
        $age = [math]::Round(((Get-Date) - $_.LastWriteTime).TotalDays, 1)
        Write-Host "  $($_.Name)  ($([math]::Round($_.Length / 1KB)) KB, ${age}d ago)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Backup complete." -ForegroundColor Green
