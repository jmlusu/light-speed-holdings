# Dashboard Key Rotation Procedure

This document describes the procedure for rotating dashboard RBAC API keys. It complements the general key rotation procedure in [AGENTS.md#11-security--key-rotation-procedure](../AGENTS.md#11-security--key-rotation-procedure).

## Overview

The dashboard uses a 4-key RBAC system (ADR-012, ADR-013):

| Key | Role | Permissions |
|-----|------|-------------|
| `DASHBOARD_ADMIN_KEY` | `admin` | Full access (all endpoints) |
| `DASHBOARD_APPROVE_KEY` | `approve` | Approve/reject tasks, escalations |
| `DASHBOARD_RUN_KEY` | `run` | Execute tasks, read KPIs |
| `DASHBOARD_API_KEY` | `admin` (alias) | Legacy single-key mode |

Keys are hierarchical: `admin` implies `approve` implies `run`.

## When to Rotate

- **Scheduled**: Every 90 days
- **Immediate**: Suspected compromise, team member departure, security incident

## Rotation Procedure

### 1. Generate New Keys

Generate cryptographically secure keys for each role:

```bash
# Generate 4 new keys (32 bytes each, base64url encoded)
python -c "import secrets; [print(secrets.token_urlsafe(32)) for _ in range(4)]"
```

Example output:
```
DASHBOARD_ADMIN_KEY=<new_admin_key>
DASHBOARD_APPROVE_KEY=<new_approve_key>
DASHBOARD_RUN_KEY=<new_run_key>
DASHBOARD_API_KEY=<new_legacy_key>  # Optional: can mirror admin key
```

### 2. Update Local Environment

Update `.env` with new values (NEVER commit `.env` to git):

```bash
# Edit .env and replace each key
DASHBOARD_ADMIN_KEY=<new_admin_key>
DASHBOARD_APPROVE_KEY=<new_approve_key>
DASHBOARD_RUN_KEY=<new_run_key>
DASHBOARD_API_KEY=<new_legacy_key>
```

### 3. Update Deployed Environments

Update secrets in your deployment platform:

| Platform | Location |
|----------|----------|
| GitHub Actions | Repository/Organization Settings → Secrets → Actions |
| Docker/Container | Container orchestration secrets (Swarm, K8s, ECS, etc.) |
| Cloud Provider | AWS Secrets Manager / GCP Secret Manager / Azure Key Vault |

Update all three environments:
- **Development** (local `.env`)
- **Staging** (staging deployment secrets)
- **Production** (production deployment secrets)

### 4. Verify Health Endpoints

Confirm new keys work before revoking old ones:

```bash
# Local verification (requires .env loaded)
uv run python -c "
from dotenv import load_dotenv
load_dotenv()
from ai_company.security.rbac import verify_keys
verify_keys()
"

# Staging verification
curl -H "X-API-Key: \$DASHBOARD_ADMIN_KEY" http://localhost:8421/health

# Production verification (adjust host/port)
curl -H "X-API-Key: \$DASHBOARD_ADMIN_KEY" https://api.example.com/health
```

Expected response: `{"status":"ok"}` with HTTP 200.

### 5. Revoke Old Keys

After confirming new keys work across all environments, revoke the old keys in your secrets manager to prevent any future use.

### 6. Update Documentation

If key format or naming convention changed, update `.env.example` and `.env.staging.example` placeholders.

### 7. Document Rotation

Record the rotation in `CHANGELOG.md`:

```markdown
## [Unreleased]

### Security
- Rotated dashboard RBAC keys (2026-08-17)
  - Reason: Scheduled 90-day rotation
  - Keys rotated: ADMIN, APPROVE, RUN, API (legacy)
```

## Key Storage Best Practices

- **Never commit** keys to git (`.env` is in `.gitignore`)
- **Use secrets managers** in production/staging
- **Rotate on schedule** (90 days) or immediately on compromise
- **Audit access** quarterly — review who has access to which keys
- **Use unique keys per environment** — never reuse staging keys in production

## Troubleshooting

### `verify_keys()` fails

Common causes:
- Key missing from environment
- Key still has placeholder value (e.g., `your_admin_key_here`)
- Key contains whitespace or newline characters

Run with verbose output:
```bash
uv run python -c "
import os
from ai_company.security.rbac import verify_keys
try:
    verify_keys()
except RuntimeError as e:
    print(e)
"
```

### Health endpoint returns 401/403

- Verify the key matches exactly (no extra whitespace)
- Confirm `DASHBOARD_AUTH_MODE=api_key` (not `open`)
- Check the key is for the correct role (admin key for `/health`)

### Browser session tokens (ADR-013)

If using browser session tokens, those are minted on-demand and bound to IP. They don't need rotation — only the static env keys do.

## References

- [ADR-012: Dashboard RBAC](../adr/012-dashboard-rbac.md)
- [ADR-013: Browser Session Tokens](../adr/013-browser-session-tokens.md)
- [Security hardening parked change](harness/changes/parking/2026-08-15-security-hardening-env-key-sanitization-dashboard-auth-finalization-trivy-scanning-s3-backup-canary-release/)
- [AGENTS.md: Key Rotation Procedure](../AGENTS.md#11-security--key-rotation-procedure)
