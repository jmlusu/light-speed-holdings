#!/usr/bin/env bash
#
# backup-to-oci.sh — Daily state backup to Oracle Object Storage.
#
# Creates timestamped tar.gz archives of the state directories and ships them
# to a free-tier Object Storage bucket, either via:
#
#   1. OCI_BACKUP_PAR_URL  — a write-capable pre-authenticated request URL
#                            (generate in Console: Object Storage -> bucket ->
#                            Pre-Authenticated Requests -> Create). No API key
#                            needed on the VM.
#   2. OCI_BUCKET          — bucket name; uses the OCI CLI DEFAULT profile
#                            (configure once with: oci setup config).
#
# Environment:
#   REPO_PATH          repository root (default: /opt/ai-company)
#   DATA_DIR           data volume mount (default: /mnt/ai-company-data)
#   OCI_BACKUP_PAR_URL write PAR URL (uploads go to <PAR URL>/<filename>)
#   OCI_BUCKET         bucket name for the OCI CLI path
#   OCI_PREFIX         object prefix, e.g. 'ai-company-backups/' (default)
#   BACKUP_KEEP_DAYS   local retention (default: 7)
#   SRC_DIRS           space-separated dirs to archive (state is live-mounted via binds)
#
# Run via cron (installed by setup-vm.sh) and locally for testing.

set -euo pipefail

REPO_PATH="${REPO_PATH:-/opt/ai-company}"
DATA_DIR="${DATA_DIR:-/mnt/ai-company-data}"
BACKUP_KEEP_DAYS="${BACKUP_KEEP_DAYS:-7}"
OCI_PREFIX="${OCI_PREFIX:-ai-company-backups/}"
SRC_DIRS="${SRC_DIRS:-.opencode company logs results memory}"

STAMP="$(date -u +%Y%m%d-%H%M%SZ)"
LOCAL_DIR="$DATA_DIR/backups"
LOG="$LOCAL_DIR/backup.log"
[ -d "$LOCAL_DIR" ] || mkdir -p "$LOCAL_DIR"

[ -n "${OCI_BACKUP_PAR_URL:-}" ] || [ -n "${OCI_BUCKET:-}" ] || {
    echo "[backup] neither OCI_BACKUP_PAR_URL nor OCI_BUCKET set; nothing to do." >> "$LOG"
    exit 0
}

echo "[backup] $STAMP start" >> "$LOG"
failures=0

for dir in $SRC_DIRS; do
    src="$REPO_PATH/$dir"
    [ -d "$src" ] || continue
    archive="$LOCAL_DIR/ai-company-$dir-$STAMP.tar.gz"

    if tar -C "$REPO_PATH" -czf "$archive" "$dir" 2>/dev/null; then
        size_mb="$(du -m "$archive" | cut -f1)"
        echo "  ok  $dir ($size_mb MB)" >> "$LOG"
    else
        echo "  ERR tar failed: $dir" >> "$LOG"
        failures=$((failures + 1))
        continue
    fi

    # Upload — prefer the keyless PAR URL.
    if [ -n "${OCI_BACKUP_PAR_URL:-}" ]; then
        if curl -fsS -X PUT --upload-file "$archive" \
            "${OCI_BACKUP_PAR_URL%/}/ai-company-$dir-$STAMP.tar.gz" >> "$LOG" 2>&1; then
            echo "      uploaded (PAR) $dir" >> "$LOG"
        else
            echo "      ERR upload (PAR): $dir" >> "$LOG"
            failures=$((failures + 1))
        fi
    elif command -v oci >/dev/null 2>&1; then
        if oci os object put -bn "$OCI_BUCKET" \
            --name "${OCI_PREFIX}ai-company-$dir-$STAMP.tar.gz" \
            --file "$archive" --force >> "$LOG" 2>&1; then
            echo "      uploaded (bucket) $dir" >> "$LOG"
        else
            echo "      ERR upload (bucket): $dir" >> "$LOG"
            failures=$((failures + 1))
        fi
    else
        echo "      SKIP upload: no PAR URL and no oci CLI" >> "$LOG"
        failures=$((failures + 1))
    fi
done

# Local rotation.
find "$LOCAL_DIR" -type f -name 'ai-company-*.tar.gz' -mtime "+$BACKUP_KEEP_DAYS" -delete

echo "[backup] $STAMP done (failures=$failures)" >> "$LOG"
exit "$failures"
