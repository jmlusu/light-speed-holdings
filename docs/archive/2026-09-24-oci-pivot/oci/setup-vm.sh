#!/usr/bin/env bash
#
# setup-vm.sh — Bootstrap the AI Company Builder stack on an Ubuntu 24.04 VM.
#
# Runs on the OCI Always Free Ampere A1 instance and does everything needed to
# go from a bare OS to a running stack:
#
#   1. Format + mount the attached block volume (if present) as /mnt/ai-company-data
#   2. Clone (or reuse) the repository at /opt/ai-company
#   3. Bind-mount repo state dirs (.opencode, company, logs) onto the volume
#   4. Install Docker Engine + Compose v2
#   5. Create .env with freshly generated dashboard RBAC keys
#   6. docker compose up dashboard + worker + prometheus
#   7. Install Caddy as an HTTPS reverse proxy in front of :8421
#   8. Install the daily OCI backup cron (object storage bucket OR pre-authenticated request URL)
#
# Usage:
#   sudo bash setup-vm.sh /opt/ai-company [SITE_DOMAIN]
#
# Environment overrides:
#   REPO_URL          git URL to clone if the repo is not already present
#   REPO_BRANCH       branch to clone (default: main)
#   DATA_DIR          mount point for the block volume (default: /mnt/ai-company-data)
#   OCI_BUCKET        Object Storage bucket name for backups (uses OCI CLI profile DEFAULT)
#   OCI_BACKUP_PAR_URL  pre-authenticated request (write) URL for backups - no API key needed
#   BACKUP_KEEP_DAYS  local retention for backup archives (default: 7)
#   OCI_CLI_INSTALL   1 => install the OCI CLI via pipx (required only for bucket backups)
#
# Idempotent: safe to rerun after a partial failure or reboot.

set -euo pipefail

REPO_PATH="${1:-/opt/ai-company}"
SITE_DOMAIN="${2:-}"

REPO_URL="${REPO_URL:-https://github.com/jmlusu/light-speed-holdings.git}"
REPO_BRANCH="${REPO_BRANCH:-main}"
DATA_DIR="${DATA_DIR:-/mnt/ai-company-data}"
BACKUP_KEEP_DAYS="${BACKUP_KEEP_DAYS:-7}"

log()  { printf '\033[0;36m==> %s\033[0m\n' "$*" >&2; }
ok()   { printf '\033[0;32m    %s\033[0m\n' "$*" >&2; }
warn() { printf '\033[0;33mWARN: %s\033[0m\n' "$*" >&2; }
fail() { printf '\033[0;31mERROR: %s\033[0m\n' "$*" >&2; exit 1; }

[ "$(id -u)" -eq 0 ] || fail "run as root: sudo bash $0 $*"

# ---------------------------------------------------------------------------
# 0. OS check
# ---------------------------------------------------------------------------
if ! grep -qi "ubuntu" /etc/os-release; then
    fail "This script targets Ubuntu 24.04. Recreate the VM from a Canonical Ubuntu image."
fi
command -v apt-get >/dev/null 2>&1 || fail "apt-get not found; this host is not Ubuntu."

# ---------------------------------------------------------------------------
# 1. Block volume: format + mount
# ---------------------------------------------------------------------------
DATA_DEVICE=""
for dev in /dev/oracleoci/oraclevdb /dev/oracleoci/oraclevda \
           /dev/sdb /dev/sdc /dev/vdb /dev/vdc /dev/xvdb /dev/nvme1n1; do
    [ -b "$dev" ] || continue
    root_src="$(findmnt -n -o SOURCE / 2>/dev/null || echo /dev/none)"
    case "$dev" in
        "$root_src"*|/dev/oracleoci/oraclevda*) continue ;;
    esac
    DATA_DEVICE="$dev"
    break
done

if [ -z "$DATA_DEVICE" ]; then
    partprobe 2>/dev/null || true
    udevadm settle 2>/dev/null || true
    sleep 5
    for dev in /dev/oracleoci/oraclevdb /dev/sdb /dev/vdb; do
        [ -b "$dev" ] && { DATA_DEVICE="$dev"; break; }
    done
fi

if [ -n "$DATA_DEVICE" ]; then
    log "Preparing data volume $DATA_DEVICE at $DATA_DIR"
    mkdir -p "$DATA_DIR"

    if ! blkid "$DATA_DEVICE" >/dev/null 2>&1; then
        ok "Formatting $DATA_DEVICE (ext4)"
        mkfs.ext4 -F "$DATA_DEVICE" >/dev/null
    fi

    if ! mountpoint -q "$DATA_DIR"; then
        mount "$DATA_DEVICE" "$DATA_DIR"
        # Persist across reboots via UUID (device names change).
        if ! grep -qs "$DATA_DIR " /etc/fstab; then
            uuid="$(blkid -s UUID -o value "$DATA_DEVICE")"
            echo "UUID=$uuid $DATA_DIR ext4 defaults,noatime 0 2" >> /etc/fstab
        fi
    fi
    ok "Data volume mounted at $DATA_DIR"
else
    warn "No data block volume detected (attach one in the console, then reboot)."
    warn "Continuing with state on the boot volume - do NOT do this for production."
fi

# ---------------------------------------------------------------------------
# 2. Repository
# ---------------------------------------------------------------------------
log "Ensuring repository at $REPO_PATH"
REPO_EXISTS=0
if [ -d "$REPO_PATH/.git" ]; then
    REPO_EXISTS=1
    git -C "$REPO_PATH" fetch --depth 1 origin "$REPO_BRANCH" >/dev/null 2>&1 || true
    ok "Repository already present - reusing $REPO_PATH"
elif [ -n "$(ls -A "$REPO_PATH" 2>/dev/null)" ]; then
    fail "$REPO_PATH exists but is not a git repository. Move it away and rerun."
else
    mkdir -p "$(dirname "$REPO_PATH")"
    git clone --branch "$REPO_BRANCH" --depth 1 "$REPO_URL" "$REPO_PATH"
    REPO_EXISTS=1
    ok "Cloned $REPO_URL@$REPO_BRANCH to $REPO_PATH"
fi

# ---------------------------------------------------------------------------
# 3. Bind repo state dirs onto the volume (seed from the repo first)
# ---------------------------------------------------------------------------
if [ -n "$DATA_DEVICE" ]; then
    log "Binding state dirs onto the data volume"
    for d in .opencode company logs results memory; do
        tgt="$REPO_PATH/$d"
        src="$DATA_DIR/$d"
        mkdir -p "$tgt" "$src"
        if [ -z "$(find "$src" -mindepth 1 -maxdepth 1 2>/dev/null | head -n 1)" ]; then
            cp -a "$tgt/." "$src/" 2>/dev/null || true
        fi
        if ! mountpoint -q "$tgt"; then
            mount --bind "$src" "$tgt"
            if ! grep -qs "^$src $tgt " /etc/fstab; then
                echo "$src $tgt none bind 0 0" >> /etc/fstab
            fi
        fi
        ok "bind-mount: $src -> $tgt"
    done
fi

# ---------------------------------------------------------------------------
# 4. Docker Engine + Compose v2
# ---------------------------------------------------------------------------
log "Installing Docker Engine + Compose v2"
if ! command -v docker >/dev/null 2>&1; then
    apt-get update -qq
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
        | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
        > /etc/apt/sources.list.d/docker.list
    apt-get update -qq
    apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-compose-plugin curl openssl >/dev/null
    systemctl enable --now docker
    ok "Docker $(docker --version)"
fi
docker compose version >/dev/null 2>&1 || fail "docker compose v2 plugin missing."

# ---------------------------------------------------------------------------
# 5. .env with generated dashboard keys
# ---------------------------------------------------------------------------
log "Preparing $REPO_PATH/.env"
ENV_FILE="$REPO_PATH/.env"
if [ ! -f "$ENV_FILE" ]; then
    cp "$REPO_PATH/.env.staging.example" "$ENV_FILE"
    ADMIN_KEY="$(openssl rand -hex 24)"
    RUN_KEY="$(openssl rand -hex 24)"
    APPROVE_KEY="$(openssl rand -hex 24)"
    API_KEY="$(openssl rand -hex 24)"
    sed -i "s/^DASHBOARD_ADMIN_KEY=.*/DASHBOARD_ADMIN_KEY=$ADMIN_KEY/" "$ENV_FILE"
    sed -i "s/^DASHBOARD_RUN_KEY=.*/DASHBOARD_RUN_KEY=$RUN_KEY/" "$ENV_FILE"
    sed -i "s/^DASHBOARD_APPROVE_KEY=.*/DASHBOARD_APPROVE_KEY=$APPROVE_KEY/" "$ENV_FILE"
    sed -i "s/^DASHBOARD_API_KEY=.*/DASHBOARD_API_KEY=$API_KEY/" "$ENV_FILE"
    if [ -n "$SITE_DOMAIN" ]; then
        sed -i "s|^DASHBOARD_CORS_ORIGINS=.*|DASHBOARD_CORS_ORIGINS=https://$SITE_DOMAIN|" "$ENV_FILE"
    fi
    ok ".env created with random dashboard keys (admin=$ADMIN_KEY)"
    warn "LLM provider keys are still placeholders - edit $ENV_FILE and add OPENCODE_API_KEY / GEMINI_API_KEY / etc."
else
    warn ".env already exists - leaving untouched. Verify dashboards keys are set: grep '^DASHBOARD._KEY' $ENV_FILE"
fi

# ---------------------------------------------------------------------------
# 6. Compose up (dashboard + worker + prometheus)
# ---------------------------------------------------------------------------
log "Building and starting the stack (dashboard :8421, worker, prometheus :9091)"
cd "$REPO_PATH"
docker compose -f docker-compose.staging.yml --profile staging --profile monitoring up -d --build

log "Waiting for dashboard /health"
healthy=0
for i in $(seq 1 60); do
    if curl -fsS "http://127.0.0.1:8421/health" >/dev/null 2>&1; then
        healthy=1
        ok "dashboard healthy after ${i}x5s"
        break
    fi
    sleep 5
done
[ "$healthy" -eq 1 ] || warn "dashboard not healthy yet - check: docker compose -f $REPO_PATH/docker-compose.staging.yml logs dashboard"

# ---------------------------------------------------------------------------
# 7. Caddy reverse proxy (HTTPS when a domain is set)
# ---------------------------------------------------------------------------
log "Configuring Caddy"
if command -v caddy >/dev/null 2>&1 || apt-get install -y -qq caddy >/dev/null 2>&1; then
    if [ -n "$SITE_DOMAIN" ]; then
        SITE_ADDR="$SITE_DOMAIN"
    else
        SITE_ADDR=":80"
    fi
    mkdir -p /etc/caddy
    sed "s|__SITE_DOMAIN__|$SITE_ADDR|" "$REPO_PATH/deploy/oci/Caddyfile" > /etc/caddy/Caddyfile
    systemctl enable caddy >/dev/null 2>&1 || true
    systemctl restart caddy
    ok "Caddy proxying $SITE_ADDR -> 127.0.0.1:8421"
else
    warn "caddy could not be installed - dashboard reachable only via SSH tunnel (see docs/OCI-FREE-TIER-DEPLOYMENT.md)."
fi

# ---------------------------------------------------------------------------
# 8. OCI CLI (optional, only for bucket backups)
# ---------------------------------------------------------------------------
if [ "${OCI_CLI_INSTALL:-0}" = "1" ] && [ -n "${OCI_BUCKET:-}" ]; then
    log "Installing OCI CLI via pipx"
    apt-get install -y -qq pipx >/dev/null 2>&1 || true
    command -v oci >/dev/null 2>&1 || pipx install oci-cli >/dev/null 2>&1 || true
    if command -v oci >/dev/null 2>&1; then
        ok "OCI CLI installed. Configure it (oci setup config) with an API key that can write to $OCI_BUCKET."
    else
        warn "OCI CLI install failed - use OCI_BACKUP_PAR_URL instead."
    fi
fi

# ---------------------------------------------------------------------------
# 9. Daily backup cron
# ---------------------------------------------------------------------------
if [ -n "${OCI_BACKUP_PAR_URL:-}" ] || [ -n "${OCI_BUCKET:-}" ]; then
    log "Installing daily backup cron (02:30 UTC)"
    CRON_ENV=""
    [ -n "${OCI_BACKUP_PAR_URL:-}" ] && CRON_ENV="$CRON_ENV OCI_BACKUP_PAR_URL='$OCI_BACKUP_PAR_URL'"
    [ -n "${OCI_BUCKET:-}" ]         && CRON_ENV="$CRON_ENV OCI_BUCKET='$OCI_BUCKET'"
    cat > /etc/cron.d/ai-company-backup <<EOF
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
$CRON_ENV REPO_PATH=$REPO_PATH DATA_DIR=$DATA_DIR BACKUP_KEEP_DAYS=$BACKUP_KEEP_DAYS
30 2 * * * root bash "$REPO_PATH/deploy/oci/backup-to-oci.sh" >> "$DATA_DIR/backups/backup.log" 2>&1
EOF
    chmod 0644 /etc/cron.d/ai-company-backup
    ok "Backup cron installed (see /etc/cron.d/ai-company-backup)"
    bash -n "$REPO_PATH/deploy/oci/backup-to-oci.sh" || warn "backup-to-oci.sh has a syntax error!"
else
    warn "No bucket or PAR URL supplied - backups not installed. See docs/OCI-FREE-TIER-DEPLOYMENT.md."
fi

log "Bootstrap complete."
echo ""
if [ -n "$SITE_DOMAIN" ]; then
    echo "  Dashboard :   https://$SITE_DOMAIN/health"
else
    echo "  Dashboard :   reachable via SSH tunnel:"
    echo "                ssh -L 8421:127.0.0.1:8421 ubuntu@<PUBLIC_IP>"
    echo "                then browse http://localhost:8421"
fi
echo "  Prometheus :   docker compose -f $REPO_PATH/docker-compose.staging.yml --profile monitoring logs prometheus"
echo "  .env file  :   $ENV_FILE  (add your LLM provider keys)"
