# Oracle Cloud Free Tier Deployment

Deploy the full AI Company Builder stack (dashboard, orchestrator worker,
Prometheus) on **Oracle Cloud Infrastructure Always Free** — no monthly cost —
and back it up to free Object Storage.

All automation lives in [`deploy/oci/`](../deploy/oci/):

| File | What it does |
|------|--------------|
| `provision.ps1` | Windows-side OCI CLI script: VCN + subnet + security list, Ampere A1 instance, block volume, SSH key; optionally deploys to the VM |
| `setup-vm.sh` | On-VM bootstrap: Docker + Compose, data volume mount, `.env` keys, `docker compose up`, Caddy HTTPS proxy, backup cron |
| `backup-to-oci.sh` | Daily tar.gz of state → Object Storage (bucket or pre-authenticated request) |
| `Caddyfile` | Reverse proxy in front of the dashboard (template — `__SITE_DOMAIN__` replaced at setup) |

---

## 1. What this fits into

The stack is small and JSON-file based — no database needed — so it lives
comfortably inside Always Free:

| Need | Always Free allowance | This deployment uses |
|------|------------------------|----------------------|
| Compute | 4 OCPU / 24 GB Ampere A1 + 2× AMD micro | 1 A1 instance, 2 OCPU / 12 GB |
| Block Volume | 200 GB total | 1 × 50 GB data volume |
| Object Storage | 10 GB | ~50–200 MB/day of backups |
| Egress | 10 TB/month | trivial |
| Load balancing / TLS | Flexible LB 10 Mbps | Caddy on the VM (simpler) |
| Monitoring / Alerts / Email | free | optional `/health` alerts |

The existing `docker-compose.staging.yml` is used as-is. Base images in the
`Dockerfile` (`python:3.12-slim`, `ghcr.io/astral-sh/uv`) are multi-arch and build
natively on ARM64 — **no code changes required**.

> One pre-existing break was fixed to make this path work: the staging compose
> referenced a Dockerfile stage named `base` that did not exist (the Dockerfile
> only defines `builder` and `runtime`). Both `docker-compose.staging.yml`
> services now build against `target: runtime`. See
> `docker-compose.staging.yml` and [§10 Troubleshooting](#10-troubleshooting).

---

## 2. Prerequisites

- Oracle Cloud Free Tier account (see [§3 Sign up](#3-sign-up)).
- OCI CLI installed and configured **on your Windows/laptop machine**:

  ```powershell
  winget install Oracle.OracleCli
  oci setup config        # Enter region (e.g. af-johannesburg-1), paste API key, etc.
  oci iam compartment list -c <tenancy-ocid>   # verify auth works
  ```

- OpenSSH client (`ssh`, `scp`) — ships with Windows 10/11.
- Optional: `rsync` for faster repo sync, `git`.

---

## 3. Sign up

1. Go to <https://signup.cloud.oracle.com/>. The card is for identity
   verification only (a temporary hold is released) — choose **Always Free** and
   do not upgrade unless you want the $300 trial first.
2. **Choose South Africa (Johannesburg)** as the home region — nearest to
   Malawi/SADC and Free Tier eligible. Fallbacks: London, Frankfurt.
   > Home region cannot be changed later; capacity is per-region.
3. After signup, confirm your account and log into the OCI Console.

---

## 4. Provision the environment

### 4a. One-shot script (recommended)

From the repo root on your Windows machine:

```powershell
.\deploy\oci\provision.ps1 -Region af-johannesburg-1
```

It creates (idempotently — rerun-safe):

- VCN `10.0.0.0/16` + internet gateway + default route + public subnet
- Security list allowing only **SSH 22, HTTP 80, HTTPS 443** (the dashboard port
  is *not* exposed publicly)
- Ampere A1 instance `VM.Standard.A1.Flex` @ **2 OCPU / 12 GB RAM** (default),
  auto-discovered **Ubuntu 24.04** image
- A **50 GB** block volume attached paravirtualized
- An ed25519 key pair at `~/.ssh/ai-company_oci` (or use `-SshPublicKeyPath`)

It prints the public IP and SSH command.

Key parameters:

| Parameter | Default | Notes |
|-----------|---------|-------|
| `-Ocpus` | `2` | Always Free max is 4. |
| `-MemoryGb` | `12` | A1 requires 6 GB per OCPU (6/12/18/24). |
| `-DataVolumeGb` | `50` | Free allowance is 200 GB total. |
| `-CompartmentId` | your tenancy root (auto-detected) | |
| `-AvailabilityDomain` | `...-AD-1` | Retry a different AD on "out of capacity". |
| `-Deploy` | off | Also syncs the repo to the VM and runs `setup-vm.sh`. |
| `-DryRun` | off | Prints the intended configuration only. |

Add `-Deploy` to include steps [§5](#5-bootstrap-the-vm) automatically:

```powershell
.\deploy\oci\provision.ps1 -Region af-johannesburg-1 -Deploy
```

### 4b. Manual (Console) alternative

1. Compute → **Instances** → **Create instance**: shape `VM.Standard.A1.Flex`,
   2 OCPU / 12 GB RAM; Ubuntu 24.04 image; upload your SSH key.
2. Networking → **Virtual cloud networks**: create VCN `10.0.0.0/16` with
   internet gateway + route + subnet, and add **Ingress rules** for 22, 80, 443.
3. Block Storage → **Block volumes**: create 50 GB, attach to the instance
   (paravirtualized).

> **If "out of capacity"**: A1 capacity is often contended. Retry in a few
> minutes, switch availability domain, or (last resort) pick a less-loaded region.
> Keep the rest of the plan on Carlo; only the instance shape changes.

---

## 5. Bootstrap the VM

With the instance RUNNING and SSH key in hand:

```powershell
ssh -i $env:USERPROFILE\.ssh\ai-company_oci ubuntu@<PUBLIC_IP>
```

Then, to install Docker, mount the data volume, generate dashboard keys, start
the full stack, and configure Caddy:

```bash
sudo bash /opt/ai-company/deploy/oci/setup-vm.sh /opt/ai-company
```

If you did **not** pass `-Deploy` to the provisioner, copy the repo over first
(the app's own `scripts/backup.ps1 -CloudProvider` won't help here; use rsync/scp):

```powershell
rsync -az --exclude-from .gitignore --exclude .venv --exclude node_modules `
  -e "ssh -i $env:USERPROFILE\.ssh\ai-company_oci" `
  ./ ubuntu@<PUBLIC_IP>:/opt/ai-company/
```

What `setup-vm.sh` does:

1. Formats/mounts the block volume at `/mnt/ai-company-data` (with `<UUID>` in
   `/etc/fstab`) and bind-mounts `.opencode`, `company`, `logs` (+ `results`,
   `memory`) onto the volume so state survives container rebuilds.
2. Installs Docker Engine + Compose v2 + Caddy.
3. Generates a `.env` with **random** dashboard RBAC keys
   (`DASHBOARD_ADMIN_KEY`/`RUN`/`APPROVE`/`API`) and prints `DASHBOARD_ADMIN_KEY`.
4. `docker compose -f docker-compose.staging.yml --profile staging --profile monitoring up -d --build`
   → dashboard + worker + Prometheus.
5. Waits for `http://127.0.0.1:8421/health`.

Verify health, then add your LLM keys:

```bash
curl -fsS http://127.0.0.1:8421/health
sudo nano /opt/ai-company/.env     # add OPENCODE_API_KEY / GEMINI_API_KEY / ...
docker compose -f /opt/ai-company/docker-compose.staging.yml restart dashboard
```

> `.env` is gitignored and never leaves the VM. Rotate the generated dashboard
> keys the same way you would any secret (see `docs/DASHBOARD_KEY_ROTATION.md`).

---

## 6. HTTPS / domain

- **No domain yet** — the dashboard is reachable only over an SSH tunnel
  (nothing is exposed publicly):

  ```powershell
  ssh -i $env:USERPROFILE\.ssh\ai-company_oci -L 8421:127.0.0.1:8421 ubuntu@<PUBLIC_IP>
  # then browse http://localhost:8421 with X-API-Key: $DASHBOARD_ADMIN_KEY
  ```

- **With a domain** — point your DNS A record at the public IP, then rerun setup
  with the domain and Caddy obtains a Let's Encrypt cert automatically:

  ```bash
  sudo bash /opt/ai-company/deploy/oci/setup-vm.sh /opt/ai-company dashboard.example.com
  ```

  Caddy listens on 443 and proxies to `127.0.0.1:8421`. Point `DASHBOARD_CORS_ORIGINS`
  at `https://dashboard.example.com` in `.env` (the app rejects `*`).

Security notes: only 22/80/443 are open; the app is API-key **fail-closed** by
default (`DASHBOARD_AUTH_MODE=api_key`); WebSocket uses `?api_key=...`.

---

## 7. Backups → free Object Storage

Two ways to push the daily archives (see `backup-to-oci.sh`):

**A. Keyless pre-authenticated request (simplest).** In the Console:
Object Storage → Create bucket `ai-company-backups` → in the bucket →
**Pre-Authenticated Requests** → create a **write** PAR → copy the URL, then:

```bash
sudo bash /opt/ai-company/deploy/oci/setup-vm.sh /opt/ai-company \
  2>/dev/null   # rerun safely; it is idempotent
# or just hand-install the cron:
sudo env OCI_BACKUP_PAR_URL='https://objectstorage.af-johannesburg-1.oraclecloud.com/p/...' \
  bash -c 'REPO_PATH=/opt/ai-company DATA_DIR=/mnt/ai-company-data \
  /opt/ai-company/deploy/oci/backup-to-oci.sh'
```

**B. OCI CLI bucket path (API key).** On the VM:

```bash
sudo apt-get install -y pipx && sudo -u ubuntu pipx install oci-cli
sudo -u ubuntu oci setup config   # region + API key your user has
# create the bucket in the console, then rerun setup-vm.sh with:
OCI_CLI_INSTALL=1 OCI_BUCKET='ai-company-backups' \
  sudo bash /opt/ai-company/deploy/oci/setup-vm.sh /opt/ai-company
```

Both install a 02:30 UTC cron (`/etc/cron.d/ai-company-backup`) that archives
`.opencode`, `company`, `logs`, `results`, `memory` as timestamped tar.gz,
uploads, and keeps 7 days locally. Add an Object Lifecycle Policy (archive after
7 days, delete after 90) to stay well inside the 10 GB free bucket.

For a quick restore:

```bash
ssh ubuntu@<PUBLIC_IP> "sudo tar -xzf /mnt/ai-company-data/backups/ai-company-.opencode-<STAMP>.tar.gz -C /opt/ai-company"
```

---

## 8. Anti-idle and monitoring (keep the account!)

- OCI **suspends accounts idle 30+ days**. The compose `worker` runs the
  orchestrator tick continuously, which counts as usage — but add a simple
  keep-alive if you ever stop the stack:

  ```bash
  printf '*/5 * * * * root curl -fsS http://127.0.0.1:8421/health >/dev/null || systemctl restart docker\n' > /etc/cron.d/ai-company-keepalive
  ```

- OCI **Monitoring** (always free): create a metric alarm on the instance CPU
  utilization and a notification on `GET /health` failing. Email Delivery gives
  3,000 messages/month free for the notifications topic.
- Set a **budget** with alert = $0 so any PAYG surprise triggers immediately.

---

## 9. Operations cheat-sheet

```bash
# Logs
docker compose -f /opt/ai-company/docker-compose.staging.yml logs -f --tail=100 dashboard
sudo journalctl -u caddy -f

# Restart one service
docker compose -f /opt/ai-company/docker-compose.staging.yml restart worker

# Rebuild after a code deploy (git pull on the VM)
git -C /opt/ai-company pull
docker compose -f /opt/ai-company/docker-compose.staging.yml --profile staging up -d --build

# Health / metrics
curl -fsS http://127.0.0.1:8421/health
# Prometheus (inside docker network): docker compose ... exec prometheus sh -c 'wget -qO- localhost:9090/metrics | head'
```

---

## 10. Troubleshooting

| Symptom | Fix |
|---------|-----|
| Docker build fails "stage not found / target base" | Pull latest - `docker-compose.staging.yml` now builds `target: runtime` (the `base` stage never existed). |
| `out of capacity` on A1 | Retry / different AD / different region; keep resources otherwise unchanged |
| instance can't be reached | Check security list ingress; `oci compute instance list-vnics` for IP; wait for RUNNING |
| dashboard not healthy | `docker compose ... logs dashboard`; confirm `.env` has keys; LLM keys are placeholders until you fill them |
| volume not mounted | `sudo reboot` (hot-attach can lag), rerun `setup-vm.sh` |
| can't reach dashboard directly | by design — nothing on 8421 is public; use the SSH tunnel (§6) |
| HTTPS fails | DNS must resolve before Caddy's first cert attempt; `sudo journalctl -u caddy -e` |

---

## 11. Cost guardrails

- Stay inside Always Free: A1 total ≤ 4 OCPU/24 GB (this plan uses 2/12),
  block volume ≤ 200 GB, egress ≤ 10 TB/mo, bucket ≤ 10 GB.
- Do **not** run a second A1 that would exceed the aggregate; the plan leaves
  headroom for a later brand-site VM (AMD micro) if needed.
- The $300 trial credit, if used, expires 30 days after signup — it does not
  affect Always Free resources.

Related docs: [Deployment Guide](DEPLOYMENT-GUIDE.md) (bare-metal/systemd path),
[Key Rotation](DASHBOARD_KEY_ROTATION.md), [API Reference](API-REFERENCE.md).
