# Classification Policy — LS-MEM

## Four-Tier Classification (Architecture §7)

| Class | Definition | Examples | Egress Default |
|-------|-----------|----------|----------------|
| **PUBLIC** | Intended for public release | Published site content, public docs, articles | Blocked (allowlist empty) |
| **INTERNAL** | Normal internal info | Architecture, roadmaps, agent instructions | Blocked |
| **CONFIDENTIAL** | Business-sensitive | Client info, proposals, pricing, contracts, strategy; system prompts ≥ CONFIDENTIAL | Blocked |
| **RESTRICTED** | Highly sensitive | Passwords, API keys, tokens, private keys, credentials, highly sensitive PII | **Never plaintext; always blocked** |

## Rules

1. **Restricted never plaintext** (locked decision 3) — secret scanner forces classification upgrade on hit
2. **Ambiguity → BLOCK** (locked decision 3) — when uncertain, classify RESTRICTED
3. **Classification gates:**
   - Injection respects class + optional `agent_id` scoping
   - Export default excludes RESTRICTED
   - Gateway `data_classes_allowed` all `false` by default
4. **Auto-classification may err** — human can override upward/downward
5. **Never downgrade past scanner hit** on RESTRICTED content (threat T06 residual)

## Auto-Classification Rules

| Pattern | Classification | Confidence |
|---------|---------------|------------|
| `(?i)\b(password\|secret\|api[_-]?key\|token\|credential)\b` | RESTRICTED | 0.9 |
| `(?i)\b(confidential\|proprietary\|internal only\|not for distribution)\b` | CONFIDENTIAL | 0.8 |
| `(?i)\b(public\|published\|open source\|mit license\|apache license)\b` | PUBLIC | 0.7 |

## Inheritance (Architecture §13.2)

Child chunks inherit parent classification **at minimum** (upgrade only):

```python
def propagate_classification(parent, child):
    order = [PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED]
    return max(parent, child, key=order.index)
```

Applies to: chunking during `remember`, consolidation digestion, bridge import.

## Human Override

- Can upgrade or downgrade
- **Never downgrade past scanner hit** on RESTRICTED content

## References

- Architecture: `docs/architecture/LS-MEM-ARCHITECTURE.md` §7
- Threat model: T01–T06, T23, T25
- Locked decision 3: Restricted never plaintext, ambiguity → BLOCK
