# LS-MEM Skill

LightSpeed Memory — Local-first persistent memory and context system for the LightSpeed AI-agent workforce.

## Quick Start

```bash
# Install skill (dual-path)
cp -r .agents/skills/ls-memory .opencode/skills/ls-memory

# Verify hash identity
python -m pytest tests/memory/test_dual_path_hash.py -v

# Run all memory tests
python -m pytest tests/memory/ -v
```

## Tools

| Tool | Description |
|------|-------------|
| `memory-store` | Store new memory |
| `memory-search` | Search memories (FTS5) |
| `memory-forget` | Soft/hard delete |
| `memory-status` | Engine status |
| `memory-audit` | Query audit, verify chain |
| `memory-export` | Export memories (local) |
| `memory-permission` | Request/approve external access |

## Configuration

Copy `schemas/config.example.yaml` to `.lightspeed/memory/config.yaml` (workspace) or `~/.lightspeed/memory/config.yaml` (global).

## Dual-Path Deployment

This skill is deployed to BOTH paths (locked decision 1):
- `.agents/skills/ls-memory/` — **Discovery Authority**
- `.opencode/skills/ls-memory/` — Parallel deploy target

**Hash-identical enforcement:** `tests/memory/test_dual_path_hash.py`

## Policies

See `policies/`:
- `privacy.md` — Network deny-by-default, no telemetry
- `classification.md` — 4-tier rules, inheritance
- `external-access.md` — Gateway 5-gate chain
- `retention.md` — TTLs, ADR-019 mapping

## Schemas

See `schemas/`:
- `memory.schema.json` — Memory record format
- `gateway.schema.json` — Gateway config
- `audit.schema.json` — Audit log format
- `config.example.yaml` — Example configuration

## Testing

```bash
# All memory tests
python -m pytest tests/memory/ -v

# Specific test suites
python -m pytest tests/memory/test_redaction.py -v
python -m pytest tests/memory/test_dual_path_hash.py -v
python -m pytest tests/memory/test_git_safety.py -v
```

## References

- Architecture: `docs/architecture/LS-MEM-ARCHITECTURE.md`
- Data Model: `docs/architecture/LS-MEM-DATA-MODEL.md`
- Threat Model: `docs/security/LS-MEM-THREAT-MODEL.md`
- ADR-025: `docs/adr/025-lsmem-sqlite-engine-coexistence.md`
- ADR-019: `docs/adr/019-memory-knowledge-governance.md`
- Master Plan: `docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md`
