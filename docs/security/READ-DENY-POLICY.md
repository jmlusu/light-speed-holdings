# Read-Deny Policy (F-06 → R2)

**Source plan:** `reports/opencode-db-security-fix-2026-11-08.md` §7.2 ·
**Implementation:** `src/ai_company/security/path_policy.py` (`deny_reason`,
`is_path_denied`, `find_denied_paths_in_command`) + `config/path_deny.yaml`
**Wiring:** `ToolRunner` — `run_plan` (pre-tier), `_read`, and the `_execute`
token scan for `bash` file-reads; `_grep` skips these files; `_list`
filters these names from listings. The **`read` and `bash` tools** are
denied in **code** — the system prompt is never the enforcement boundary
(LLM01).

---

## Denied paths (case-insensitive, basename + every path segment)

| Class | Patterns |
|---|---|
| Environment files | `.env*`, `*.env` (any extension variant) |
| MCP/agent auth | `auth.json`, `mcp-auth.json` (any directory) |
| Trajectory store | `opencode.db*`, `opencode-.db*` (db, wal, shm, bak…) |
| Private keys | `*.pem`, `*.key` |

**Exempt (placeholders-only — re-verify on every edit):** `.env.example`,
`.env.staging.example`. An exempt template must be confirmed to hold
placeholders only (`python scripts/security/inventory_env_keys.py` shows
names + `set` flags without values).

**Error shape:** denied tools return
`Automated permission policy: read denied for credential-bearing path …`
(matching the existing `rule prevents edit` error class). DENY-LOG
attribution (path + tool + session, never content) is recorded via
`log_permission_deny` in `ai_company.audit.integration`.

## Why the filesystem layer

The dominant exfil channel was **tool outputs** (`tool` = 188,713 parts in
the corpus): `.env` was read 309× and bash touched env files 4,394×
(§7.2). A prompt-only rule ("please don't read .env") is unenforceable
under prompt injection (LLM01), so the deny lives in the runner.

## Verification (read-only)

```sql
SELECT COUNT(*) FROM part WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.tool')='read'
  AND lower(json_extract(data,'$.state.input.filePath')) LIKE '%.env%'
  AND time_created > (strftime('%s','now','-7 days') * 1000);
-- Expect: 0 new .env reads after enforcement (baseline: 309 lifetime).
```

Plus a manual negative test: read a dummy `.env` (placeholder values only)
and confirm the permission error.

## Rollback

Rules are config (`config/path_deny.yaml`); revert by restoring the prior
set. Any rollback re-opens R2 and must be re-approved by the CISO with a
compensating control note.
