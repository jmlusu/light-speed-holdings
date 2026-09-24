# External Access Policy — LS-MEM

## Permission Gateway (Architecture §9)

**Default config semantics:**
```yaml
external_access:
  enabled: false
approved_providers: []
approved_domains: []
approved_operations: []
data_classes_allowed:
  public: false
  internal: false
  confidential: false
  restricted: false
```

## Five-Gate Chain (Architecture §9; Threat T24)

```
enabled? → provider approved? → domain approved? → operation approved? → classification permitted?
    ↓           ↓                    ↓                   ↓                        ↓
   NO/BLOCK   NO/BLOCK             NO/BLOCK            NO/BLOCK                 NO/BLOCK
    ↓           ↓                    ↓                   ↓                        ↓
  BLOCK+audit BLOCK+audit          BLOCK+audit         BLOCK+audit              BLOCK+audit
```

**When all pass → Human approval with payload preview → Transmit → Audit**

**When uncertain → BLOCK** (locked decision 3; Rule 9)

## Human Approval Interface

Shows: agent, provider, operation, destination, classification, payload preview, reason, status BLOCKED, Approve?

User **must inspect payload** before approving.

## Tool Integration

| Tool | External Access | Gateway Behavior |
|------|-----------------|------------------|
| `memory-store` | None (local) | Auto-allow |
| `memory-search` | None (local) | Auto-allow |
| `memory-forget` | None (local) | Auto-allow |
| `memory-export` | File write only | Auto-allow |
| `memory-inject` | None (local) | Auto-allow |
| `memory-permission request` | Explicit | Full 5-gate chain |

## MCP Restriction

**LS-MEM tools never call MCP.** Memory content is not passed to MCP/LLM tools without gateway + human approval (recon C6; threat T13).

## Configuration Schema

See `schemas/gateway.schema.json` for full JSON schema.

## References

- Architecture: `docs/architecture/LS-MEM-ARCHITECTURE.md` §9, §9.1
- Threat model: T13, T14–T18, T24
- Locked decisions: deny-by-default, human approval, no MCP routing
