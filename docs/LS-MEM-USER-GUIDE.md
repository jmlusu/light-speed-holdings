# LS-MEM — User Guide

**Project:** LightSpeed Holdings
**Date:** 2026-09-26
**Status:** Operational reference (workstream WS-C of the LS-MEM completion change)
**Security classification:** Internal
**Related:** `docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md` (§26–§28), `docs/security/LS-MEM-THREAT-MODEL.md`, `docs/security/LS-MEM-SECURITY-VERIFICATION.md`, `.agents/skills/ls-memory/SKILL.md`
**Locked decisions:** dual skill paths (`.agents/skills` + `.opencode/skills`); new SQLite engine + one-way bridge from the legacy JSON `MemoryStore`

Everything in this guide was verified by running the commands on 2026-09-26 unless a line explicitly says **not verified**. Where behavior could not be confirmed, it says so instead of guessing.

---

## 1. What LS-MEM is (and which CLI you are typing)

LS-MEM is the local-first company memory engine: an SQLite + FTS5 database with a secret
scanner, classification tiers, lifecycle rules, a hash-chained audit log, and a default-deny
permission gateway. It makes **no network requests** in its default configuration
(evidence: `docs/security/LS-MEM-SECURITY-VERIFICATION.md` Q1).

There are **two separate CLIs** — do not confuse them:

| Command | Store | Backed by |
|---------|-------|-----------|
| `ai-company memory …` | **LS-MEM** (this guide) | `<workspace>/.lightspeed/memory/memory.db` (`src/ai_company/cli/main.py:45`) |
| `ai-company knowledge …` | Legacy JSON store | `<workspace>/memory/*.json` (`src/ai_company/cli/main.py:46`, `src/ai_company/memory/engine.py:85`) |

Both are lazy subcommands of the same `ai-company` Typer app. Run
`uv run ai-company memory --help` (15 commands) or `uv run ai-company knowledge --help`
(legacy: `list`, `add`, `search`, `recall`, `consolidate`, `prune`, `stats`, `vector-index`).
Verified both `--help` outputs on 2026-09-26.

---

## 2. Quickstart (verified end-to-end, 2026-09-26)

```powershell
# Store a memory
uv run ai-company memory remember "Routers use retries with jitter" `
  --type observation --title "Router retries" --project myproj --created-by me

# Find it again (FTS5 full-text search)
uv run ai-company memory search "router retries" --project myproj

# Read one record by ID (ID comes from remember/search output)
uv run ai-company memory get <record-id>

# Health and statistics
uv run ai-company memory status
```

Every successful command prints `✓ …` with the record ID, tier, classification, and
correlation ID. The CLI reconfigures stdio to UTF-8 at startup so legacy Windows
consoles (cp1252) no longer crash on glyph output; set `$env:PYTHONUTF8=1` if the
terminal itself renders the glyphs wrong — see
[Troubleshooting](#7-troubleshooting).

---

## 3. Command reference

All commands operate on the workspace you run them from (`Path.cwd()`,
`src/ai_company/lsmem/cli.py:30`). Config is optional at
`.lightspeed/memory/config.yaml` (`cli.py:34`).

### Store and read

| Command | Key options | Behavior |
|---------|-------------|----------|
| `remember CONTENT` | `--type/-t` (required), `--title` (required), `--project/-p`, `--created-by`, `--source`, `--classification/-c` (default `INTERNAL`), `--confidence`, `--tags`, `--ttl` | Runs secret scan → auto-classification → constitutional veto → value scoring, then inserts (`engine.py:509-607`). Secrets are redacted and upgraded to `RESTRICTED` before disk (`engine.py:381-387`). Value score ≤ 1 is rejected (`engine.py:546-549`). Invalid type/classification raises (`engine.py:531-535`). |
| `search QUERY` | `--project`, `--type`, `--classification`, `--limit` (15), `--min-tier` (1), `--json` | FTS5 full-text search (`cli.py:152`). Excludes `RESTRICTED` and constitutional-blocked rows (`engine.py:817-819`). |
| `get ID` | `--json` | Returns the record **in any status**, including `PURGED` (verified). No status filter in `engine.py:609-618`. |

### Deletion and lifecycle

| Command | Key options | Behavior |
|---------|-------------|----------|
| `forget ID` | `--actor` | Soft delete: `ACTIVE` → `ARCHIVED` (`engine.py:874-905`), audited as `memory_delete`. |
| `purge ID` | `--actor`, `--confirm` | Hard delete: any status → `PURGED` (`engine.py:907-941`). Without `--confirm` it fails with `Purge requires explicit confirmation (--confirm-purge)` (`engine.py:910`) — the message says `--confirm-purge`, but the actual flag is `--confirm`. Verified. |
| `restore ID` | `--actor` | `ARCHIVED` → `ACTIVE` (`engine.py:943-973`). Purged records cannot be restored by this command — restore a backup file instead (§6.2). Verified both paths. |
| `pin ID` / `pin ID --unpin` | `--actor` | Pin exempts a record from age-based lifecycle pruning (`engine.py:1003`). |
| `verify ID` / `--unverify` | `--actor` | Human verification → **Tier 3** (or back down) (`cli.py:360-367`). |
| `lifecycle` | — | Marks stale records `ARCHIVED` and expired records `EXPIRED`; pinned records are respected (`engine.py:977-1006`). Run it from a scheduled job if you want TTLs enforced automatically — **not verified** as wired into any scheduler. |

### Maintenance, export, audit

| Command | Key options | Behavior |
|---------|-------------|----------|
| `status` | `--json` | Counts by status/type/classification/tier, FTS count, DB size, `PRAGMA integrity_check` result (`engine.py:1118-1173`). |
| `rebuild-fts` | — | Rebuilds the FTS5 index from the `memories` table (`engine.py:1040-1055`). Typer exposes `rebuild_fts` as `rebuild-fts` (verified in `--help`). |
| `export` | `--project`, `--include-restricted`, `--output/-o`, `--actor` | Writes JSON Lines to a local file (or prints rows). **Re-scans every record for secrets at export time** and upgrades hits to `RESTRICTED` (`engine.py:1095-1101`); `RESTRICTED` rows are excluded unless `--include-restricted` (`engine.py:1086-1087`). Audited as `export`. |
| `integrity` | — | `PRAGMA integrity_check` (`engine.py:1057-1064`); exit code 1 on failure. Structural check only — see §7. |
| `audit` | `--type`, `--start`, `--end`, `--actor`, `--correlation`, `--limit`, `--json` | Queries the hash-chained audit log (`audit.py:248`). |
| `permission list\|approve\|deny` | `--token`, `--by`, `--approve/--deny` | Manual override surface for the permission gateway (`cli.py:592-646`). See the limitation in §8. |

### Skill scripts (`.agents/skills/ls-memory/scripts/`, mirrored at `.opencode/skills/ls-memory/scripts/`)

Thin Python wrappers that forward to the CLI via `subprocess` (verified in
`scripts/memory-store:11-13`):

| Script | Forwards to |
|--------|-------------|
| `memory-store` | `ai-company memory remember` |
| `memory-search` | `ai-company memory search` |
| `memory-forget` | `ai-company memory forget` |
| `memory-status` | `ai-company memory status` |
| `memory-export` | `ai-company memory export` |
| `memory-audit` | `ai-company memory audit` |
| `memory-permission` | `ai-company memory permission` |

Both skill paths must stay byte-identical — enforced by
`tests/memory/test_dual_path_hash.py` (5 tests; the global-copy test is skipped when the
global skill is absent, which is the one skipped test in the suite).

---

## 4. Data, classification, and configuration

### Where things live (verified by inspecting a real workspace, 2026-09-26)

```text
<workspace>/
├── .lightspeed/memory/
│   ├── memory.db          # records + FTS5 index (WAL mode, engine.py:272)
│   ├── memory.db-wal      # present while writers are active — back it up too
│   ├── memory.db-shm
│   ├── audit/audit.db     # hash-chained audit log (cli.py:59)
│   └── config.yaml        # optional; defaults apply if absent (cli.py:38)
└── memory/*.json          # legacy JSON store (separate CLI: `ai-company knowledge`)
```

Git safety (handoff §26): `.gitignore:91-96` ignores `.lightspeed/memory/` and
`memory.db*`; `.gitignore:73-74` ignores `memory/*.json` and `memory/vector_index/`.
Enforced by `tests/memory/test_git_safety.py` (5 tests: patterns present, ignore effective
in a fresh repo, no memory DB in git history, no git commands in LS-MEM source, no
re-including negations).

### Classification and tiers

- Classifications: `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED` (`engine.py:230`);
  default is `INTERNAL`.
- `RESTRICTED` never appears in `search` results (`engine.py:819`) and never in `export`
  without `--include-restricted`.
- Tiers 0–3 are computed from a 0–5 value score (`engine.py:413-434`): 0 discarded,
  1 low, 2 normal, 3 high. `verify` forces Tier 3.
- Default TTLs by type (`engine.py:1177-1194`): `observation` 365d, `decision` 730d,
  `architecture` 1095d, `requirement` 730d, `preference` 365d, `task` 180d,
  `milestone` 1095d, `bug` 365d, `solution` 730d, `lesson` 730d, `entity` 1095d,
  `document` 1095d, `session` 30d, anything else 365d. Override with `remember --ttl`.

### Configuration (`.lightspeed/memory/config.yaml`, optional)

Defaults come from `EngineConfig` (`engine.py:61-133`) — create the YAML file only to
override them; the CLI does a shallow merge (`cli.py:43-48`). Notable defaults:

| Key | Default | Meaning |
|-----|---------|---------|
| `injection.max_memories` / `max_tokens` | 15 / 2000 | Session-injection quota (`engine.py:95-103`) |
| `audit.retention_days_crud` / `gateway` | 90 / 365 | Audit retention (`engine.py:104-106`) |
| `gateway.external_access.enabled` | `false` | Egress off; all four data classes denied (`engine.py:107-122`) |
| `ollama.enabled` | `false` | Semantic embeddings off (`engine.py:123-130`) |
| `bridge.dry_run` | `true` | Legacy import is dry-run unless explicitly flipped (`engine.py:131-133`) |

An annotated example exists at `.agents/skills/ls-memory/schemas/config.example.yaml`.

---

## 5. Offline and Ollama behavior

- **Default: fully offline.** Engine CRUD, search, lifecycle, index rebuild, and integrity
  checks all work with no network (tests: `tests/memory/test_offline.py`,
  `TestOfflineOperation`). `remember()` performs no outbound socket calls and engine
  startup performs no DNS resolution (`TestNetworkDeny`).
- **Ollama (optional, off by default):** if enabled and wired up, embeddings go only to
  `http://127.0.0.1:11434` (loopback) with model `nomic-embed-text`
  (`src/ai_company/lsmem/vector.py:22-30,111-114`). When disabled or unreachable, the
  vector store returns empty embeddings and search stays FTS5-only
  (`tests/memory/test_ollama_optional.py::test_disabled_returns_empty`).
- **Honest limitation:** `OllamaVectorStore` is not currently called by the engine or the
  CLI (grep of `src/` finds references only in `lsmem/vector.py` and `lsmem/__init__.py`).
  Today every search is FTS5 (`cli.py:152`).

---

## 6. Backup and recovery (handoff §27)

### 6.1 Back up

Two independent kinds of backup — take both if you care about the data:

**A. File backup (full fidelity):**

```powershell
# No LS-MEM process running (each CLI call is short-lived; run between calls)
Copy-Item .lightspeed\memory\memory.db        backups\memory.db -Force
Copy-Item .lightspeed\memory\audit\audit.db   backups\audit.db  -Force
# If memory.db-wal / memory.db-shm exist, copy them alongside as well.
```

**Verified 2026-09-26:** copy `memory.db` → `purge` a record (shows `Status: PURGED`) →
copy the file back → `get` shows `Status: ACTIVE` again and `integrity` reports OK.

**B. Content export (portable JSON Lines):**

```powershell
uv run ai-company memory export --output backup.jsonl          # RESTRICTED excluded
uv run ai-company memory export --include-restricted -o full.jsonl
```

**Verified 2026-09-26** (`Exported 1 memories to export.jsonl`; one JSON object per line
with id, content, classification, tier, correlation_id…). Remember: export re-scans for
secrets, so an export can re-classify a row even though it does not rewrite the DB.

### 6.2 Restore memory

1. Stop all LS-MEM processes/CLI calls.
2. Replace `.lightspeed/memory/memory.db` (and `audit/audit.db`) with the backup files.
3. Verify: `uv run ai-company memory integrity` and `uv run ai-company memory status`.

Verified (see §6.1). To bring back a single forgotten record instead of whole-file
restore, prefer `restore ID` while it is `ARCHIVED`; `PURGED` records require the file
backup.

### 6.3 Export memory

Covered in §6.1B and §3 (`export`). Output is local-file only — nothing is uploaded.

### 6.4 Migrate schema

Two different meanings:

**(a) LS-MEM SQLite schema changes — not available.** The schema is version 1
(`schema_version: int = 1`, `engine.py:65`) and tables are created with
`CREATE TABLE IF NOT EXISTS` (`engine.py:303-342`). There is **no migration framework**
(grep for `user_version|ALTER TABLE|migrat` finds nothing outside those lines), so today
you cannot upgrade an existing DB to a future schema with a supported tool. If the schema
changes, a migration tool must be written first — **documented as a gap, not a procedure**.

**(b) Legacy JSON store → LS-MEM — available via the bridge (Python API).** Verified
2026-09-26 in a scratch workspace:

```python
# uv run python -  (from the workspace root)
from pathlib import Path
from ai_company.lsmem.bridge import MemoryStoreBridge

bridge = MemoryStoreBridge(
    json_store_path=Path("memory"),                       # dir containing *.json
    sqlite_path=Path(".lightspeed/memory/memory.db"),
)
print(bridge.import_all(dry_run=True))    # report only, writes nothing (default)
print(bridge.import_all(dry_run=False))   # real import, secret-scanned + audited
```

Observed: `ImportStats(total_json_records=1, imported=1, …)` for both calls, and the
imported record was immediately findable with `ai-company memory search`. The bridge maps
the legacy 6 types to the 13 LS-MEM types (`bridge.py:20-27`), re-scans secrets, and
imports atomically. It is covered by
`tests/memory/test_integration.py::TestBridgeImport` (3 tests). Note: the JSON file must
be UTF-8 **without BOM** — a BOM file fails with `Unexpected UTF-8 BOM` (verified).

### 6.5 Rebuild indexes

```powershell
uv run ai-company memory rebuild-fts
# ✓ FTS5 rebuilt: N entries indexed
```

Verified (1 entry in the smoke workspace). Use it when search results look stale or a
record exists but does not match queries.

### 6.6 Recover from corruption

1. **Detect:** `uv run ai-company memory integrity` (exit code 1 on failure) or
   `ai-company memory status` → `Integrity: ✓ OK / ✗ FAIL`.
2. **Understand the limit (verified 2026-09-26):** `PRAGMA integrity_check` validates
   database **structure**, not row content. A deliberately corrupted content byte-range
   still reported `✓ Database integrity OK` while `get` returned silently corrupted text
   (`Content: Backup test two: AAAAAAAAAAAAAAAA`). Treat integrity OK as "file is not
   structurally broken", not "data is correct".
3. **Recover:**
   - Content wrong but structure fine → restore from the file backup (§6.2), or diff
     against an export (§6.3).
   - Structure broken (`integrity` fails / DB won't open) → restore the backup file.
   - No backup and the file is unusable → delete `.lightspeed/memory/memory.db*` and
     start fresh (next command recreates the schema); consider `rebuild-fts` after any
     partial repair.

### 6.7 Completely delete memory (also answer to "full uninstall")

```powershell
# 1. Stop anything that might write (no daemon in default setup)
# 2. Delete LS-MEM data
Remove-Item -Recurse -Force .lightspeed\memory       # memory.db*, audit/, config.yaml
# 3. Optionally delete the legacy JSON store too
Remove-Item -Recurse -Force .\memory                # memory/*.json + vector_index/
# 4. Confirm nothing is tracked by git
git status --porcelain
```

This removes every memory record, the audit log, and config. Verified directory contents
in the smoke workspace (`.lightspeed/memory/` containing `memory.db`, `memory.db-wal`,
`audit/audit.db`, `config.yaml` when present). The config default also mentions a global
path `~/.lightspeed/memory` (`engine.py:69`), but the CLI only ever uses the workspace
path (`cli.py:51`) — delete `~/.lightspeed/memory` manually if you created one.

---

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `UnicodeEncodeError: 'charmap' codec can't encode character '✓'` when output is piped/captured | Windows legacy console code page (cp1252) + rich success glyphs (`✓`/`✗`) in `cli.py` | The CLI now self-hardens stdio to UTF-8 at startup (`_ensure_utf8_stdio`, regression-tested in `tests/memory/test_cli_stdio.py`). If glyphs still render wrong, set `$env:PYTHONUTF8=1` (or `chcp 65001`). |
| `Purge requires explicit confirmation (--confirm-purge)` but there is no such flag | Error text says `--confirm-purge` (`engine.py:910`); CLI flag is `--confirm` (`cli.py:298`) | Use `ai-company memory purge <id> --confirm`. Verified. |
| `memory permission list` always prints `No pending approvals` | Pending approvals live in process memory only (`gateway.py:119`) — a new CLI process starts empty | Approvals must be handled in the same process that raised them (Python API); cross-process approve is non-functional. See security doc Q15/Q17. Verified. |
| `search --json` output fails JSON parsers | A trailing `Correlation IDs: …` line is printed after the JSON block (`cli.py:206-208`) | Strip everything after the closing `}` before parsing. Verified. |
| `get <id>` shows `Status: PURGED` even after purge | `get` intentionally returns records in any status (`engine.py:609-618`) | By design; use `search`/`status` for active counts. Verified. |
| `integrity` says OK but record content is garbage | Structural check only (§6.6) | Restore from backup. Verified. |
| Bridge import: `Unexpected UTF-8 BOM` | JSON file written with a UTF-8 BOM (common with some editors / `Set-Content -Encoding UTF8` on PowerShell 5.1) | Re-save as UTF-8 without BOM. Verified. |
| `remember` fails with `Value score N too low` | Value scoring rejects score ≤ 1 (`engine.py:546-549`) | Add content/title/project detail and raise `--confidence`; scoring input is content+classification+confidence+source. |
| Wrong store: you typed `knowledge …` and got JSON files | Two CLIs (§1) | `memory` = LS-MEM, `knowledge` = legacy JSON. |
| Command not found: `'ai-company' command not found` from a skill script | Skill scripts shell out to `ai-company` (`scripts/memory-store:17-22`) | Run via `uv run ai-company …` or activate the project environment so `ai-company` is on PATH. |

---

## 8. Known limitations (verified, not speculation)

1. **No schema migration tool** (§6.4a) — schema is fixed at version 1 today.
2. **`MemoryStoreBridge` has no CLI** — Python API only (no `@app.command` for it; grep of
   `cli.py` finds none). Tests cover it (`TestBridgeImport`).
3. **`LSMemInjector` has no CLI** — session injection is a Python API
   (`injector.py:285-290`, no CLI wiring found).
4. **Gateway approvals are per-process and unwired** — `_pending_approvals` is an
   in-memory dict (`gateway.py:119`); nothing in `src/` calls `PermissionGateway.evaluate`
   outside tests, and no code persists `gateway_*` audit events (they are declared in
   `audit.py:49-51` but never written). Today LS-MEM performs no egress at all, so this is
   latent, not an open hole. Full discussion: security doc Q15/Q16.
5. **Semantic search not wired** — FTS5 only (§5).
6. **`lifecycle`/TTL enforcement is manual** — run the command yourself; no scheduler
   wiring verified.

---

## 9. Where to go next

- Security posture and the 20 required answers: `docs/security/LS-MEM-SECURITY-VERIFICATION.md`
- Threat register: `docs/security/LS-MEM-THREAT-MODEL.md`
- Skill usage and policies: `.agents/skills/ls-memory/SKILL.md` and `policies/`
- Data model and lifecycle detail: `docs/LS-MEM-DATA-MODEL.md` (referenced by
  `engine.py:1178`)
