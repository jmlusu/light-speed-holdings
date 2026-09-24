<#
.SYNOPSIS
    Provision an Oracle Cloud Infrastructure (OCI) Always Free environment for
    the AI Company Builder stack (dashboard, worker, Prometheus).

.DESCRIPTION
    Uses the OCI CLI to create, in one shot, everything the VM needs:

      - Compartment (defaults to your tenancy root; pass -CompartmentId to use
        an existing compartment)
      - VCN, Internet Gateway, Route Table, public Subnet, Security List
        (SSH 22, HTTP 80, HTTPS 443 only - the dashboard port 8421 is NOT exposed)
      - Ampere A1 Flex instance (default 2 OCPU / 12 GB RAM, Always Free)
      - Ubuntu 24.04 image auto-discovered for the A1 shape
      - Block Volume (default 50 GB, Always Free allowance is 200 GB total) + paravirtualized attach
      - Optional SSH key generation

    Run this from your Windows machine with the OCI CLI installed and configured
    (oci setup config). It prints the public IP and the SSH command to provision
    the VM with deploy/oci/setup-vm.sh.

.PARAMETER CompartmentId
    Compartment OCID to deploy into. Default: detected from ~/.oci/config tenancy
    (the tenancy root compartment).

.PARAMETER Region
    OCI region (e.g. af-johannesburg-1). Default: detected from ~/.oci/config.

.PARAMETER OciProfile
    OCI CLI config profile to use. Default: DEFAULT

.PARAMETER AvailabilityDomain
    Availability domain index. Default: first AD returned by the region.

.PARAMETER VcnCidr
    VCN CIDR block. Default: 10.0.0.0/16

.PARAMETER SubnetCidr
    Public subnet CIDR. Default: 10.0.0.0/24

.PARAMETER Ocpus
    OCPUs for the A1 flex shape. Always Free max 4. Default: 2

.PARAMETER MemoryGb
    RAM in GB. A1 requires multiples of 6 (6 per OCPU). Default: 12

.PARAMETER DataVolumeGb
    Block volume size in GB. Always Free allowance is 200 GB total. Default: 50

.PARAMETER InstanceName
    Display name for the instance. Default: ai-company

.PARAMETER SshPublicKeyPath
    Path to an existing public key (.pub). If omitted, an ed25519 key pair is
    generated at ~/.ssh/ai-company_oci.

.PARAMETER SshKeyDir
    Directory for generated SSH keys. Default: ~/.ssh

.PARAMETER Deploy
    After the instance is RUNNING, copy this repository to the VM and run
    deploy/oci/setup-vm.sh over SSH (requires a local OpenSSH client and the
    repo's git remote to be accessible from the VM).

.PARAMETER RepoUrl
    Git URL used when -Deploy clones onto the VM. Default: the origin remote of
    this repository (https://github.com/jmlusu/light-speed-holdings.git).

.PARAMETER RepoBranch
    Branch checked out on the VM. Default: main

.PARAMETER SshUser
    SSH user for -Deploy. Ubuntu images use "ubuntu". Default: ubuntu

.PARAMETER DryRun
    Print the intended configuration instead of running the OCI commands.

.EXAMPLE
    .\deploy\oci\provision.ps1

.EXAMPLE
    .\deploy\oci\provision.ps1 -Region af-johannesburg-1 -Deploy

.EXAMPLE
    .\deploy\oci\provision.ps1 -Ocpus 1 -MemoryGb 6 -DataVolumeGb 50 -CompartmentId ocid1.compartment.oc1...
#>

[CmdletBinding()]
param(
    [string]$CompartmentId = '',
    [string]$Region = '',
    [string]$OciProfile = 'DEFAULT',
    [string]$AvailabilityDomain = '',
    [string]$VcnCidr = '10.0.0.0/16',
    [string]$SubnetCidr = '10.0.0.0/24',
    [ValidateRange(1, 4)]
    [int]$Ocpus = 2,
    [ValidateRange(6, 24)]
    [int]$MemoryGb = 12,
    [ValidateRange(1, 200)]
    [int]$DataVolumeGb = 50,
    [string]$InstanceName = 'ai-company',
    [string]$SshPublicKeyPath = '',
    [string]$SshKeyDir = '',
    [switch]$Deploy,
    [string]$RepoUrl = '',
    [string]$RepoBranch = 'main',
    [string]$SshUser = 'ubuntu',
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

function Write-Step([string]$Message) {
    Write-Host "" -ForegroundColor DarkGray
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Fail([string]$Message) {
    Write-Host "ERROR: $Message" -ForegroundColor Red
    exit 1
}

# OCI CLI runner
function Invoke-Oci {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,
        [switch]$AllowFailure
    )
    $output = & oci @Arguments 2>&1
    $code = $LASTEXITCODE
    if ($code -ne 0 -and -not $AllowFailure) {
        Fail "oci command failed (exit $code):`n$($output -join "`n")"
    }
    return ($output | Out-String).Trim()
}

# Read a value from the OCI CLI config INI (~/.oci/config).
function Get-OciConfigValue {
    param([string]$Section, [string]$Key)
    $configPath = Join-Path $env:USERPROFILE '.oci\config'
    if (-not (Test-Path -LiteralPath $configPath)) { return $null }

    $lines = Get-Content -LiteralPath $configPath
    $inside = $false
    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        if ($trimmed -match '^\[(.+)\]$') {
            $inside = ($matches[1] -eq $Section)
            continue
        }
        if ($inside -and $trimmed -match '^([^\s=]+)\s*=\s*(.+)$') {
            if ($matches[1] -eq $Key) { return $matches[2].Trim() }
        }
    }
    return $null
}

# Look up an existing resource by display name, returning its OCID (or '').
function Get-OciIdByDisplayName {
    param([string[]]$Arguments)
    $id = Invoke-Oci -Arguments $Arguments -AllowFailure
    if ($id -eq '' -or $id -match '^oci apierror') { return '' }
    return $id
}

# ---------------------------------------------------------------------------
# Preflight: OCI CLI present + configured
# ---------------------------------------------------------------------------
Write-Step "Preflight"
$ociCli = Get-Command oci -ErrorAction SilentlyContinue
if (-not $ociCli) {
    Fail @'
OCI CLI not found. Install it first:
  winget install Oracle.OracleCli
  (or) bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
Then run: oci setup config
'@
}

if ($Region -eq '') { $Region = Get-OciConfigValue $OciProfile 'region' }
if ([string]::IsNullOrWhiteSpace($Region)) {
    Fail "Could not detect region from ~/.oci/config [$OciProfile]. Pass -Region (e.g. af-johannesburg-1)."
}

if ($CompartmentId -eq '') {
    $tenancyFromConfig = Get-OciConfigValue $OciProfile 'tenancy'
    if ([string]::IsNullOrWhiteSpace($tenancyFromConfig)) {
        Fail "Could not detect tenancy from ~/.oci/config [$OciProfile]. Pass -CompartmentId."
    }
    $CompartmentId = $tenancyFromConfig
    Write-Host "  Compartment: tenancy root ($CompartmentId)" -ForegroundColor DarkGray
} else {
    Write-Host "  Compartment: $CompartmentId" -ForegroundColor DarkGray
}

if ($RepoUrl -eq '') {
    $remote = git remote get-url origin 2>$null
    if ($LASTEXITCODE -eq 0) { $RepoUrl = $remote } else { $RepoUrl = 'https://github.com/jmlusu/light-speed-holdings.git' }
}

$suffix = $Region -replace '-1$', ''
if ($AvailabilityDomain -eq '') { $AvailabilityDomain = "$suffix-AD-1"; Write-Host "  AD: $AvailabilityDomain (default)" -ForegroundColor DarkGray }

Write-Host "  Region: $Region, AD: $AvailabilityDomain" -ForegroundColor DarkGray
Write-Host "  Shape: VM.Standard.A1.Flex ($Ocpus OCPU / $MemoryGb GB RAM), data volume $DataVolumeGb GB" -ForegroundColor DarkGray

# Sanity-check Always Free A1 memory constraint (6 GB per OCPU).
if (($MemoryGb % 6) -ne 0) {
    Fail "Ampere A1 memory must be a multiple of 6 (6 GB per OCPU). Got $MemoryGb."
}

# ---------------------------------------------------------------------------
# SSH key
# ---------------------------------------------------------------------------
if ($SshKeyDir -eq '') { $SshKeyDir = Join-Path $env:USERPROFILE '.ssh' }
if ($SshPublicKeyPath -eq '') {
    $keyBase = Join-Path $SshKeyDir 'ai-company_oci'
    $keyPrivate = "$keyBase"
    $keyPublic = "$keyBase.pub"
    if (-not (Test-Path -LiteralPath $keyPublic)) {
        if ($DryRun) {
            Write-Host "  [DRY RUN] would create key pair: ssh-keygen -t ed25519 -f $keyPrivate" -ForegroundColor Yellow
        } else {
            New-Item -ItemType Directory -Path $SshKeyDir -Force | Out-Null
            ssh-keygen -t ed25519 -f $keyPrivate -N '""' -C 'ai-company-oci' | Out-Null
            if ($LASTEXITCODE -ne 0) { Fail "ssh-keygen failed (is OpenSSH client installed?)." }
            Write-Host "  Generated key pair: $keyPrivate" -ForegroundColor DarkGreen
        }
    }
    $SshPublicKeyPath = $keyPublic
}
if (-not (Test-Path -LiteralPath $SshPublicKeyPath)) {
    Fail "Public key not found: $SshPublicKeyPath"
}
$sshPublicKey = (Get-Content -LiteralPath $SshPublicKeyPath -Raw).Trim()
Write-Host "  SSH public key: $SshPublicKeyPath" -ForegroundColor DarkGray

if ($DryRun) {
    Write-Host ""
    Write-Host "DRY RUN - no OCI resources were created." -ForegroundColor Yellow
    Write-Host "Would deploy: region=$Region compartment=$CompartmentId shape=A1.Flex($Ocpus ocpu/$MemoryGb gb) volume=${DataVolumeGb}gb" -ForegroundColor DarkGray
    exit 0
}

# ---------------------------------------------------------------------------
# Image discovery (Ubuntu 24.04 for Ampere A1)
# ---------------------------------------------------------------------------
Write-Step "Discovering Ubuntu 24.04 image for VM.Standard.A1.Flex"
$imageId = Invoke-Oci @(
    'compute', 'image', 'list',
    '--compartment-id', $CompartmentId,
    '--shape', 'VM.Standard.A1.Flex',
    '--operating-system', 'Canonical Ubuntu',
    '--all',
    '--query', 'sort_by(data[?contains("display-name", `"Ubuntu-24.04`")], &"time-created")[-1].id',
    '--raw-output'
)
if ([string]::IsNullOrWhiteSpace($imageId) -or $imageId -like '*=*') {
    Fail "Could not find a Canonical Ubuntu 24.04 image for A1 in $Region. Pick one manually:`n  oci compute image list -c `$compartment --shape VM.Standard.A1.Flex --operating-system 'Canonical Ubuntu' --all"
}
Write-Host "  Image: $imageId" -ForegroundColor DarkGray

# ---------------------------------------------------------------------------
# VCN + Internet Gateway + Route Table + Subnet + Security List
# ---------------------------------------------------------------------------
Write-Step "Creating VCN / Internet Gateway / Route Table / Subnet / Security List"
$vcnName = 'ai-company-vcn'
$vcnId = Get-OciIdByDisplayName @('network', 'vcn', 'list', '--compartment-id', $CompartmentId, '--display-name', $vcnName, '--query', 'data[0].id', '--raw-output')
if ($vcnId -eq '') {
    $vcnId = Invoke-Oci @('network', 'vcn', 'create', '--compartment-id', $CompartmentId, '--cidr-block', $VcnCidr, '--display-name', $vcnName, '--dns-label', 'aicompany', '--query', 'data.id', '--raw-output')
    Write-Host "  VCN: $vcnId" -ForegroundColor DarkGreen
} else {
    Write-Host "  VCN already exists: $vcnId" -ForegroundColor DarkGray
}

$igwName = 'ai-company-igw'
$igwId = Get-OciIdByDisplayName @('network', 'internet-gateway', 'list', '--compartment-id', $CompartmentId, '--display-name', $igwName, '--query', 'data[0].id', '--raw-output')
if ($igwId -eq '') {
    $igwId = Invoke-Oci @('network', 'internet-gateway', 'create', '--compartment-id', $CompartmentId, '--vcn-id', $vcnId, '--is-enabled', 'true', '--display-name', $igwName, '--query', 'data.id', '--raw-output')
    Write-Host "  IGW: $igwId" -ForegroundColor DarkGreen
}

$rtName = 'ai-company-route-table'
$rtId = Get-OciIdByDisplayName @('network', 'route-table', 'list', '--compartment-id', $CompartmentId, '--display-name', $rtName, '--query', 'data[0].id', '--raw-output')
if ($rtId -eq '') {
    $routeRules = '[{"cidrBlock":"0.0.0.0/0","networkEntityId":"' + $igwId + '"}]'
    $rtId = Invoke-Oci @('network', 'route-table', 'create', '--compartment-id', $CompartmentId, '--vcn-id', $vcnId, '--display-name', $rtName, '--route-rules', $routeRules, '--query', 'data.id', '--raw-output')
    Write-Host "  Route table: $rtId" -ForegroundColor DarkGreen
}

$subnetName = 'ai-company-public-subnet'
$subnetId = Get-OciIdByDisplayName @('network', 'subnet', 'list', '--compartment-id', $CompartmentId, '--display-name', $subnetName, '--query', 'data[0].id', '--raw-output')
if ($subnetId -eq '') {
    $subnetId = Invoke-Oci @('network', 'subnet', 'create', '--compartment-id', $CompartmentId, '--vcn-id', $vcnId, '--cidr-block', $SubnetCidr, '--route-table-id', $rtId, '--display-name', $subnetName, '--dns-label', 'public', '--query', 'data.id', '--raw-output')
    Write-Host "  Subnet: $subnetId" -ForegroundColor DarkGreen
}

# Security list: SSH 22, HTTP 80, HTTPS 443 (dashboard 8421 stays internal).
$slName = 'ai-company-security-list'
$slId = Get-OciIdByDisplayName @('network', 'security-list', 'list', '--compartment-id', $CompartmentId, '--display-name', $slName, '--query', 'data[0].id', '--raw-output')
if ($slId -eq '') {
    $ingressJson = '[{"source":"0.0.0.0/0","protocol":"6","isStateless":false,"description":"SSH","tcpOptions":{"destinationPortRange":{"min":22,"max":22}}},{"source":"0.0.0.0/0","protocol":"6","isStateless":false,"description":"HTTP","tcpOptions":{"destinationPortRange":{"min":80,"max":80}}},{"source":"0.0.0.0/0","protocol":"6","isStateless":false,"description":"HTTPS","tcpOptions":{"destinationPortRange":{"min":443,"max":443}}}]'
    $egressJson = '[{"destination":"0.0.0.0/0","protocol":"all","isStateless":false,"description":"All egress"}]'
    $slId = Invoke-Oci @('network', 'security-list', 'create', '--compartment-id', $CompartmentId, '--vcn-id', $vcnId, '--display-name', $slName, '--ingress-security-rules', $ingressJson, '--egress-security-rules', $egressJson, '--query', 'data.id', '--raw-output')
    Write-Host "  Security list: $slId" -ForegroundColor DarkGreen
}

# Attach the security list to the subnet.
$null = Invoke-Oci @('network', 'subnet', 'update', '--subnet-id', $subnetId, '--security-list-ids', ('["' + $slId + '"]'), '--force')

# ---------------------------------------------------------------------------
# Instance
# ---------------------------------------------------------------------------
Write-Step "Launching Ampere A1 instance ($Ocpus OCPU / $MemoryGb GB RAM)"
try {
    $instanceId = Invoke-Oci @(
        'compute', 'instance', 'launch',
        '--compartment-id', $CompartmentId,
        '--availability-domain', $AvailabilityDomain,
        '--shape', 'VM.Standard.A1.Flex',
        '--shape-config', ('{"ocpus":' + $Ocpus + ',"memoryInGBs":' + $MemoryGb + '}'),
        '--subnet-id', $subnetId,
        '--image-id', $imageId,
        '--ssh-authorized-keys-file', $SshPublicKeyPath,
        '--display-name', $InstanceName,
        '--assign-public-ip', 'true',
        '--wait-for-state', 'RUNNING',
        '--query', 'data.id',
        '--raw-output'
    )
    Write-Host "  Instance: $instanceId" -ForegroundColor DarkGreen
} catch {
    Fail "Instance launch failed. Ampere A1 can transiently report 'out of capacity' - wait a few minutes and rerun, or switch the home region.`n$($_.Exception.Message)"
}

# ---------------------------------------------------------------------------
# Block volume + attach
# ---------------------------------------------------------------------------
Write-Step "Creating block volume (${DataVolumeGb} GB) and attaching (paravirtualized)"
$volumeId = Invoke-Oci @(
    'bv', 'volume', 'create',
    '--compartment-id', $CompartmentId,
    '--availability-domain', $AvailabilityDomain,
    '--size-in-gbs', "$DataVolumeGb",
    '--display-name', 'ai-company-data',
    '--wait-for-state', 'AVAILABLE',
    '--query', 'data.id',
    '--raw-output'
)
Write-Host "  Volume: $volumeId" -ForegroundColor DarkGreen

$null = Invoke-Oci @(
    'compute', 'volume-attachment', 'create',
    '--instance-id', $instanceId,
    '--volume-id', $volumeId,
    '--type', 'paravirtualized',
    '--wait-for-state', 'ATTACHED',
    '--query', 'data.id',
    '--raw-output'
)
Write-Host "  Attachment complete" -ForegroundColor DarkGreen

# ---------------------------------------------------------------------------
# Public IP
# ---------------------------------------------------------------------------
Write-Step "Fetching public IP"
$publicIp = ''
for ($try = 0; $try -lt 20 -and $publicIp -eq ''; $try++) {
    Start-Sleep -Seconds 5
    $publicIp = Invoke-Oci @('compute', 'instance', 'list-vnics', '--instance-id', $instanceId, '--query', 'data[0]."public-ip"', '--raw-output')
}
if ([string]::IsNullOrWhiteSpace($publicIp)) {
    Fail "Instance is RUNNING but no public IP was assigned yet. Run: oci compute instance list-vnics --instance-id $instanceId"
}

Write-Host ""
Write-Host "Provisioning complete." -ForegroundColor Green
Write-Host "  Public IP : $publicIp" -ForegroundColor Green
Write-Host "  SSH       : ssh -i $($SshPublicKeyPath -replace '\.pub$','') $SshUser@$publicIp" -ForegroundColor Green
Write-Host "  Next step : copy this repo to the VM and run setup-vm.sh (see docs/OCI-FREE-TIER-DEPLOYMENT.md)."

# ---------------------------------------------------------------------------
# Optional: deploy onto the VM
# ---------------------------------------------------------------------------
if ($Deploy) {
    $privateKey = $SshPublicKeyPath
    if ($privateKey -match '\.pub$') { $privateKey = $privateKey -replace '\.pub$', '' }
    if (-not (Test-Path -LiteralPath $privateKey)) {
        Fail "Cannot find private key $privateKey for SSH deployment."
    }
    $repoCopy = git rev-parse --show-toplevel 2>$null
    if (-not $repoCopy) {
        Fail "-Deploy requires running this script from inside the repository."
    }

    Write-Step "Copying repository to VM and bootstrapping (this takes several minutes)"
    $tmp = Join-Path $env:TEMP 'ai-company-repo'
    if (Test-Path $tmp) { Remove-Item -Recurse -Force $tmp }
    git clone --depth 1 --branch $RepoBranch $RepoUrl $tmp 2>$null
    if ($LASTEXITCODE -ne 0) { Fail "git clone of $RepoUrl failed. Is the VM able to reach the remote?" }

    $sshOpts = "-i $privateKey -o StrictHostKeyChecking=accept-new"
    $hasRsync = [bool](Get-Command rsync -ErrorAction SilentlyContinue)
    if ($hasRsync) {
        & rsync -az --exclude-from "$tmp/.gitignore" --exclude '.git' --exclude '.venv' --exclude 'node_modules' -e "ssh $sshOpts" "$tmp/" "$SshUser@${publicIp}:/tmp/ai-company-src/" 2>$null
    }
    if (-not $hasRsync -or $LASTEXITCODE -ne 0) {
        # Fallback for hosts without rsync: scp a tarball and extract on the VM.
        $tarball = Join-Path $env:TEMP 'ai-company-src.tar.gz'
        Push-Location $tmp
        tar -czf $tarball --exclude='.git' --exclude='.venv' --exclude='node_modules' .
        Pop-Location
        & scp -i $privateKey -o StrictHostKeyChecking=accept-new $tarball "$SshUser@${publicIp}:/tmp/ai-company-src.tar.gz" 2>$null
        if ($LASTEXITCODE -ne 0) { Fail "scp of repository to VM failed." }
        & ssh -i $privateKey -o StrictHostKeyChecking=accept-new $SshUser@$publicIp 'mkdir -p /tmp/ai-company-src && tar -xzf /tmp/ai-company-src.tar.gz -C /tmp/ai-company-src && rm -f /tmp/ai-company-src.tar.gz' 2>$null
        if ($LASTEXITCODE -ne 0) { Fail "extracting repository on VM failed." }
    }
    Remove-Item -Recurse -Force $tmp

    & ssh -i $privateKey -o StrictHostKeyChecking=accept-new $SshUser@$publicIp 'sudo mv /tmp/ai-company-src /opt/ai-company; sudo chown -R $USER:$USER /opt/ai-company; sudo bash /opt/ai-company/deploy/oci/setup-vm.sh /opt/ai-company' 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "setup-vm.sh did not complete cleanly. Check logs on the VM." -ForegroundColor Yellow
    }
}
