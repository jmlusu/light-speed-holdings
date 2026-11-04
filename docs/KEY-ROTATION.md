# Security — Key Rotation Procedure

Moved from `AGENTS.md` §11.

> Review needed: the LLM provider key list below predates the current OmniRoute routing. Verify it against the live setup before relying on it.

See also: [docs/DASHBOARD_KEY_ROTATION.md](docs/DASHBOARD_KEY_ROTATION.md) for detailed dashboard RBAC key rotation procedures.

**When to rotate:**
- Every 90 days (scheduled)
- Immediately on suspected compromise
- When team members with access leave
- After any security incident

**Procedure:**
1. **Generate new keys** for each provider/service (OpenCode, Gemini, Dashboard RBAC keys)
2. **Update local `.env`** with new values — NEVER commit `.env` to git (it's gitignored)
3. **Update deployed environments** (staging, production) via your secrets manager / platform:
   - GitHub Actions secrets for CI/CD
   - Docker / container platform secrets for runtime
   - Cloud provider secret stores (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault)
4. **Verify health endpoints** respond with new keys:
   - `curl http://<host>:8420/health` (production)
   - `curl http://<host>:8421/health` (staging)
5. **Revoke old keys** after confirming new ones work across all environments
6. **Update `.env.example`** placeholders if key format/naming changed
7. **Document rotation** in CHANGELOG.md with date and reason

**Dashboard RBAC keys** (in priority order):
- `DASHBOARD_ADMIN_KEY` — full access (also accepts `DASHBOARD_API_KEY` as alias)
- `DASHBOARD_APPROVE_KEY` — approve/reject tasks
- `DASHBOARD_RUN_KEY` — execute tasks, read KPIs
- `DASHBOARD_API_KEY` — legacy single-key mode (admin alias)

**LLM Provider keys:**
- `OPENCODE_API_KEY` — primary (Big Pickle)
- `GEMINI_API_KEY` — fallback (gemini-3.5-flash)
- Optional: `DEEPSEEK_API_KEY`, `KIMI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `MIMO_API_KEY`

**Verification commands:**
```bash
# Local verification
uv run python -c "from dotenv import load_dotenv; load_dotenv(); from ai_company.security.rbac import verify_keys; verify_keys()"

# Staging verification
curl -H "X-API-Key: \$DASHBOARD_ADMIN_KEY" http://localhost:8421/health

# Production verification (adjust host/port)
curl -H "X-API-Key: \$DASHBOARD_ADMIN_KEY" https://api.example.com/health
```
