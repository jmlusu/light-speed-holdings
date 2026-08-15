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
    Optional: Upload to cloud storage (S3/GCS) for offsite redundancy.

.PARAMETER BackupDir
    Where to store backups locally. Default: ./backups

.PARAMETER RetentionDays
    Delete local backups older than this many days. Default: 30

.PARAMETER CloudProvider
    Cloud storage provider for offsite backup. Options: 'S3', 'GCS', 'None'. Default: 'None'

.PARAMETER CloudBucket
    Cloud bucket name (required if CloudProvider is S3 or GCS).

.PARAMETER CloudPrefix
    Prefix/path within the cloud bucket. Default: 'ai-company-backups/'

.PARAMETER DryRun
    Show what would be backed up without actually creating archives.

.EXAMPLE
    .\scripts\backup.ps1
    .\scripts\backup.ps1 -RetentionDays 7
    .\scripts\backup.ps1 -CloudProvider S3 -CloudBucket my-backups-bucket
    .\scripts\backup.ps1 -CloudProvider GCS -CloudBucket my-gcs-bucket -CloudPrefix backups/
    .\scripts\backup.ps1 -DryRun
#>

[CmdletBinding()]
param(
    [string]$BackupDir = "./backups",
    [int]$RetentionDays = 30,
    [ValidateSet('None', 'S3', 'GCS')]
    [string]$CloudProvider = 'None',
    [string]$CloudBucket = '',
    [string]$CloudPrefix = 'ai-company-backups/',
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

# ── Validate cloud parameters ───────────────────────────────────
if ($CloudProvider -ne 'None' -and [string]::IsNullOrWhiteSpace($CloudBucket)) {
    Write-Error "CloudBucket is required when CloudProvider is $CloudProvider"
    exit 1
}

# Check for required CLI tools
if ($CloudProvider -eq 'S3') {
    if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
        Write-Error "AWS CLI not found. Install it to use S3 backups."
        exit 1
    }
} elseif ($CloudProvider -eq 'GCS') {
    if (-not (Get-Command gsutil -ErrorAction SilentlyContinue)) {
        Write-Error "gsutil not found. Install Google Cloud SDK to use GCS backups."
        exit 1
    }
}

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
if ($CloudProvider -ne 'None') {
    Write-Host "Cloud:      $CloudProvider://$CloudBucket/$CloudPrefix"
}
Write-Host ""

# ── Ensure backup directory exists ────────────────────────────
if (-not $DryRun) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
}

$totalSize = 0
$backedUp = @()
$archives = @()

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
                    $archives += $archivePath
                    Write-Host "    -> $archiveName" -ForegroundColor DarkGreen
                } else {
                    Write-Host "    WARNING: tar exited with code $LASTEXITCODE" -ForegroundColor Yellow
                    # Fallback: use Compress-Archive (creates .zip, rename to .tar.gz for convention)
                    $zipPath = $archivePath -replace '\.tar\.gz$', '.zip'
                    Compress-Archive -Path $dir -DestinationPath $zipPath -Force
                    $backedUp += ($archiveName -replace '\.tar\.gz$', '.zip')
                    $archives += $zipPath
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

# ── Upload to cloud storage ───────────────────────────────────
if (-not $DryRun -and $CloudProvider -ne 'None' -and $archives.Count -gt 0) {
    Write-Host ""
    Write-Host "Uploading to $CloudProvider..." -ForegroundColor Cyan

    foreach ($archivePath in $archives) {
        $archiveName = Split-Path $archivePath -Leaf
        $cloudPath = "$CloudPrefix$archiveName"

        try {
            if ($CloudProvider -eq 'S3') {
                Write-Host "  Uploading to s3://$CloudBucket/$cloudPath" -ForegroundColor Green
                aws s3 cp $archivePath "s3://$CloudBucket/$cloudPath" --only-show-errors
            } elseif ($CloudProvider -eq 'GCS') {
                Write-Host "  Uploading to gs://$CloudBucket/$cloudPath" -ForegroundColor Green
                gsutil -q cp $archivePath "gs://$CloudBucket/$cloudPath"
            }
            Write-Host "    -> Uploaded successfully" -ForegroundColor DarkGreen
        } catch {
            Write-Host "    ERROR uploading $archiveName: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# ── Summary ───────────────────────────────────────────────────
$totalMB = [math]::Round($totalSize / 1MB, 2)
Write-Host ""
Write-Host "Total size: $totalMB MB" -ForegroundColor Cyan
if (-not $DryRun -and $backedUp.Count -gt 0) {
    Write-Host "Archives created: $($backedUp.Count)" -ForegroundColor Cyan
}

# ── Rotation: delete old local backups ────────────────────────
if (-not $DryRun -and (Test-Path $BackupDir)) {
    $cutoff = (Get-Date).AddDays(-$RetentionDays)
    $oldFiles = Get-ChildItem -Path $BackupDir -File | Where-Object {
        $_.LastWriteTime -lt $cutoff -and ($_.Name -match "ai-company-.*\.(tar\.gz|zip)$")
    }

    if ($oldFiles.Count -gt 0) {
        Write-Host ""
        Write-Host "Rotating $($oldFiles.Count) old local backup(s) (>$RetentionDays days)..." -ForegroundColor Yellow
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
