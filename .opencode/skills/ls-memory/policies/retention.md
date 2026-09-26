# Retention Policy — LS-MEM

## ADR-019 Governance Mapping (Architecture §1, ADR-025 Decision Rule 4)

| ADR-019 Concept | LS-MEM Implementation |
|-----------------|----------------------|
| **TTL per type** | `ttl_days` column; defaults per type (see Data Model §3) |
| **Staleness (180d)** | `stale_at` column; computed on write; refreshed on access |
| **Conflict → supersede** | `superseded_by` FK; newest-wins; loser `status=SUPERSEDED` |
| **Pinned entries win** | `pinned=1` boolean; exempt from age pruning and auto-supersede |
| **Constitutional veto** | `constitutional_block=1`; `CONSTITUTIONAL_BLOCKLIST` patterns → `status=ARCHIVED` |
| **Curator pin/unpin** | `pin`/`unpin` CLI sets `pinned=1/0`; Tier 3 requires `verified_by` |

## Default TTL by Type (Data Model §3)

| Type | TTL (days) |
|------|------------|
| observation | 365 |
| decision | 730 |
| architecture | 1095 |
| requirement | 730 |
| preference | 365 |
| task | 180 |
| milestone | 1095 |
| bug | 365 |
| solution | 730 |
| lesson | 730 |
| entity | 1095 |
| document | 1095 |
| session | 30 |

## Tier System (Architecture §1, ADR-019)

| Score | Tier | TTL Multiplier | Persistence |
|-------|------|----------------|-------------|
| 0–1 | Discarded | N/A | Not persisted |
| 2 | Tier 1 | 1.0× | Default TTL |
| 3–4 | Tier 2 | 1.5× (+50%) | Extended TTL |
| 5 | Tier 3 | ∞ (infinite) | Pinned, `verified_by` required |

## Lifecycle States (Architecture §6)

| State | Transitions | Retention |
|-------|-------------|-----------|
| ACTIVE | → SUPERSEDED, → ARCHIVED, → EXPIRED, → PURGED | Per `ttl_days` |
| SUPERSEDED | → ARCHIVED, → PURGED | 90 days after supersede |
| ARCHIVED | → PURGED | 1 year |
| EXPIRED | → PURGED (auto after grace) | 30 days grace |
| PURGED | Terminal | Immediate |

## Audit Retention (Architecture §10.1)

| Event Type | Retention |
|------------|-----------|
| CRUD (create/update/delete/search) | 90 days |
| Gateway/external-transfer | 365 days |
| Export/import/rebuild | 365 days |

Pruning rewrites chain with new `CHAIN_HEAD` anchor; old anchors preserved in `audit/anchors/`.

## Export/Backup Retention

- User-managed — no automatic expiry
- Disaster recovery: `scripts/backup.ps1` pattern extended with LS-MEM section

## References

- Architecture: `docs/architecture/LS-MEM-ARCHITECTURE.md` §1, §6, §10.1, §16
- ADR-019: `docs/adr/019-memory-knowledge-governance.md`
- ADR-025: `docs/adr/025-lsmem-sqlite-engine-coexistence.md` Decision Rule 4
- Data Model: `docs/architecture/LS-MEM-DATA-MODEL.md` §5, §6
