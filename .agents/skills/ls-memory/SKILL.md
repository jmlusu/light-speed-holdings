# LS-MEM Skill

**Skill ID:** `ls-memory`
**Version:** 0.1.0
**Author:** LightSpeed Holdings
**License:** Proprietary

## Description

LS-MEM (LightSpeed Memory) is the sanctioned local-first persistent memory and context system for the LightSpeed AI-agent workforce. It replaces the retired `claude-mem-*` family (retired 2026-09-23 per SKILL_CURATION_POLICY).

## Capabilities

- **Persistent local memory** with deterministic FTS5 search (works fully offline)
- **Pre-write secret scan + 4-tier classification** (PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED)
- **Default-deny permission gateway** for any external transfer with human approval
- **Session continuity** via ranked, quota-bounded memory injection
- **Coexistence** with existing JSON `MemoryStore` via one-way import bridge (ADR-025)
- **Audit trail** with tamper-evident SHA256 chaining
- **OpenCode tools**: `memory-store`, `memory-search`, `memory-forget`, `memory-status`, `memory-audit`, `memory-export`, `memory-permission`

## When to Use

- Agent needs to remember facts, decisions, architecture, requirements across sessions
- Agent needs to search prior context with keyword/semantic retrieval
- Agent needs to handle sensitive data (secrets, credentials, PII) safely
- Agent needs to request external access (embeddings, inference) via permission gateway
- Agent needs to forget/purge memories with audit trail

## When NOT to Use

- Cloud embeddings or external vector databases (handoff §13, §14)
- MCP routing of memory content (recon C6; threat T13)
- Remote dashboard/telemetry/auto-sync (handoff §2 principles 4,7)
- Human approval gate on every capture (ADR-019: automatic with veto+flag)

## Data Handling

- **Redaction token:** `[REDACTED_SECRET]` canonical; `[REDACTED]` legacy alias
- **Restricted data:** Never plaintext at rest; always blocked from export/egress
- **Classification:** Auto-classify with scanner; human can upgrade/downgrade (never past scanner hit on RESTRICTED)
- **Offline-first:** All operations work with network disabled; zero non-localhost sockets

## Tools Provided

| Tool | Description |
|------|-------------|
| `memory-store` | Store a new memory (type, title, content, classification) |
| `memory-search` | Search memories via FTS5 (quota 5-15, ~1-2k tokens) |
| `memory-forget` | Soft-delete (forget) or hard-delete (purge with confirm) |
| `memory-status` | Show engine status, counts, health |
| `memory-audit` | Query audit log, verify chain, export |
| `memory-export` | Export memories (local file, re-scans secrets, excludes RESTRICTED) |
| `memory-permission` | Request/approve external access via gateway |

## Policies

See `policies/`:
- `privacy.md` — network deny-by-default, no telemetry
- `classification.md` — 4-tier rules, inheritance, override
- `external-access.md` — gateway 5-gate chain, human approval
- `retention.md` — TTLs, staleness, supersede, pin, veto (ADR-019)

## Configuration

`config.yaml` in `.lightspeed/memory/`:
```yaml
schema_version: 1
injection:
  max_memories: 15
  max_tokens: 2000
  min_value_score: 2
fts:
  tokenizer: unicode61
  stopwords: ["the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"]
audit:
  retention_days_crud: 90
  retention_days_gateway: 365
gateway: { ... }
```

## Dual-Path Deployment (Locked Decision 1)

This skill is deployed to BOTH:
1. `.agents/skills/ls-memory/` — **Discovery Authority** (OpenCode scans here)
2. `.opencode/skills/ls-memory/` — Parallel deploy target (hash-identical copy)

**Content-identical enforcement:** Hash check in `tests/memory/test_dual_path_hash.py` (FM4).

## Security

- Zero outbound hosts in skill scripts (curation transmission scan)
- Skill transmissions third-party ban unless vendor on APPROVED-VENDORS within 90-day window (SKILL_CURATION_POLICY)
- Independent security audit required before implementation (handoff §29)

## References

- Master plan: `docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md`
- Architecture: `docs/architecture/LS-MEM-ARCHITECTURE.md`
- Data model: `docs/architecture/LS-MEM-DATA-MODEL.md`
- Threat model: `docs/security/LS-MEM-THREAT-MODEL.md`
- ADR-025: `docs/adr/025-lsmem-sqlite-engine-coexistence.md`
- ADR-019: `docs/adr/019-memory-knowledge-governance.md`
