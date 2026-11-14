# Egress & Vendor Policy (F-07/F-08 → R4)

**Source plan:** `reports/opencode-db-security-fix-2026-11-08.md` §8 ·
**Implementation:** `src/ai_company/security/egress.py` (`validate_egress_url`,
`check_shell_egress`) + `config/egress_allowlist.yaml`,
`config/suspended_vendors.yaml`
**Wiring:** `ToolRunner._webfetch` (every URL, every redirect surface) and
`ToolRunner._execute` (shell `curl`/`wget`/`IWR`/`IRM` … URL allowlist).
Evaluated in **code**, never in the prompt.

## `webfetch` policy

1. **Scheme `https` only.** `http` is allowed **only** for dev loopback:
   `localhost`, `127.0.0.1`, `::1` and the observed dev host `172.30.96.1`
   (vite/dashboard ports). All 17 historical `http` fetches already qualify
   — enforce the rule, do not relax it.
2. **Reject userinfo** URLs (`user:pass@host`). Baseline: 8 observed.
3. **Reject token-like query parameter names** (`key`, `token`, `secret`,
   `api_key`, `auth`, `session`, …). Baseline: 93 query-string URLs. Log
   host + parameter **names only**, never values.
4. **Deny SSRF targets:** cloud metadata (`169.254.169.254/.253`),
   private ranges (`10/8`, `172.16/12`, `192.168/16`, `fc00::/7`,
   `fe80::/10`) — validated on literal-IP hosts.
5. **Deny schemes** `file:`, `data:`, `ftp:` (0 observed — keep denied).
6. **Suspended vendor hosts denied:** `resend.com`, `mcp.resend.com` (below).
7. **TOCTOU note:** DNS rebinding can swap a validated public IP for a
   private one between check and fetch. For high-risk callers, resolve once
   and pin the IP; at minimum re-validate on every redirect hop. (Denied
   redirects are enforced by exception in the fetch wrapper.)

`result_to_register_entry()` builds the §9.2 transmission-register row
(host + tool + class — **never** URLs or values).

## Shell egress policy

The dominant channel is shell, not `webfetch` (IWR 1,121 / curl 718 /
IRM 529 vs 745 webfetch). `check_shell_egress()` validates **every URL**
in `Invoke-WebRequest` / `Invoke-RestMethod` / `curl` / `wget` commands
against the same policy; an egress verb without a verifiable URL is denied
as unverifiable. Private-IP egress outside the dev ranges above alerts.
Shell output stored in `part.data` is capped (64 KB JSON ceiling already
caused 140 `Ripgrep JSON record exceeded 65536 bytes` errors).

## Suspended vendors (F-08 — §9.2)

**Verified 2026-11-08 against `docs/APPROVED-VENDORS.md`:** Resend,
Composio, and the `google_search`/`websearch` providers do **not** appear
in the allow-list → **unauthorized until signed off**. Flagged (never
deleted silently) in `config/suspended_vendors.yaml` + `egress.py`:

- **`resend.com` / `mcp.resend.com`** — denied in code
  (`suspended_vendor_host`); `opencode.json` `mcp.resend` kept at
  `"enabled": false`. `resend_list-api-keys` / `send-email` /
  `create-broadcast` (~35 calls incl. API-key material via a third-party
  tool) stay suspended.
- **`composio_*`** (~27 calls incl. `MULTI_EXECUTE_TOOL`) — no webfetch
  host in this workspace; tool-prefix suspension is the control.
- **`google_search` / websearch providers** — flagged for CEO/CISO
  decision, not hard-blocked (public research is Tier B in
  `APPROVED-VENDORS.md`); posting task context to them needs sign-off.

**Sign-off path:** CEO (as CISO of record under §9.2) records a row in
`docs/APPROVED-VENDORS.md` (approved_at, data class, host, auth,
window_end ≤ 90 days). No row → no transmission. Lifting a suspension
is a forward fix, never a silent rollback.

## Verification (read-only; hostnames/counts only, never values)

```sql
-- userinfo URLs in new data (expect 0; baseline 8 lifetime):
SELECT COUNT(*) FROM part WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.tool')='webfetch'
  AND json_extract(data,'$.state.input.url') LIKE '%@%'
  AND time_created > (strftime('%s','now','-7 days') * 1000);
-- third-party http in new data (expect 0; baseline 17 total, all dev-loopback):
-- resend/composio tool calls in new data (expect 0 while suspended):
SELECT COUNT(*) FROM part WHERE json_extract(data,'$.type')='tool'
  AND (json_extract(data,'$.tool') LIKE 'resend_%' OR json_extract(data,'$.tool') LIKE 'composio_%')
  AND time_created > (strftime('%s','now','-7 days') * 1000);
```
