# Credential Rotation Runbook (F-04 → R2)

**Source plan:** `reports/opencode-db-security-fix-2026-11-08.md` §6 ·
**Key inventory (names only):** `reports/env-inventory-2026-11-08.md` ·
**Owner:** CISO / Incident Response Lead · **Effort:** 2–4 h + provider-console time

**Assumption:** until OpenCode vendor documentation proves `credential.value`
is encrypted at rest, treat all 22 `credential` values as plaintext. Rotation
scope is therefore **everything the agent could have ingested** — not a
value-level list (values were never inspected, by design).

> **Rule zero:** never print, paste, or record a secret value while doing this
> runbook. Every step works with **labels, lengths, and key names** only.

---

## 1. Enumerate (metadata only, never values)

Read-only counts + label/length listing via `sqlite3 -readonly`:

```sql
SELECT label, LENGTH(value) AS len, datetime(time_created/1000,'unixepoch','localtime') AS created
FROM credential ORDER BY label, created;
```

*Do not `SELECT value`.* Expected labels (baseline 2026-11-08): 10× `API key`
(bulk import 2026-10-22), `Groq`, `Cohere`, `Google`, `Ollama (local)`,
`Default`, 6× `OpenCode Console*` (2026-10-28 → 11-03). Confirm the count is
still 22 and catch additions.

Enumber which `.env` files the agent read (paths only):

```sql
SELECT lower(json_extract(data,'$.state.input.filePath')) AS p, COUNT(*) AS n
FROM part WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.tool')='read'
  AND lower(json_extract(data,'$.state.input.filePath')) LIKE '%.env%'
GROUP BY 1 ORDER BY 2 DESC;
```

Baseline: 309 `.env` reads. Cross-check the file list against
`reports/env-inventory-2026-11-08.md` (names only).

## 2. Rotate at the provider, not in the DB

For each label, **revoke the old key in the provider console, then issue a
new one**. Order: highest-exposure first — `Google`, `Groq`, `Cohere`,
10× `API key`, 6× `OpenCode Console*`. `Ollama (local)` = local-only,
rotate if it guards any non-local resource.

Replace the credential via the supported UI/CLI — **never** direct SQL
`UPDATE` on a live DB. Same for `auth.json` / `mcp-auth.json` tokens.

## 3. Rotate every `.env` value the agent read

For each file in §1: diff its keys against the provider consoles and rotate
any key that was ever live. `.env.example` (template) is exempt **after**
confirming placeholders-only — check with
`python scripts/security/inventory_env_keys.py` (names + `set` flags only,
never values). Every `set=yes` row in the inventory on a non-example file
must be treated as live until the provider proves otherwise.

## 4. Residual exposure (cannot be undone — contain it)

Even after rotation, the 95-day corpus embeds the **old** values. Rotation
invalidates them; the corpus itself stays sensitive — handle it by F-02
(encryption) + F-10 (retention purge) in the fix plan, and never reuse a
rotated-away key. Any residual copies (`.bak`, snapshots) are disposed of
with F-03 — never restored as active credentials.

## 5. Record (fingerprints only)

Log the rotation per `AGENTS.md` §9.2: **date, provider, key label,
new-key fingerprint (last-4 + SHA-256 prefix), never the value**. Store the
log outside the trajectory store. A rotation log entry is the audit trail;
a missing one means the rotation did not happen.

## 6. Verify (post-rotation, read-only)

```sql
SELECT COUNT(*) AS credential_rows, AVG(LENGTH(value)) AS avg_len
FROM credential;
```

Plus provider-console confirmation that **old keys show as revoked**.
Record the console reference, not key material.

## 7. Rollback: none (by design)

Rotation is irreversible — if a new key fails, **re-issue from the provider;
never revert**. The "rollback state" is the pre-fix encrypted snapshot under
owner-only ACL (fix plan §12), which is strictly safer than the current
plaintext posture. Any rollback that re-opens R1/R2 escalates to the Human
CEO (CISO of record) with a compensating control note.
