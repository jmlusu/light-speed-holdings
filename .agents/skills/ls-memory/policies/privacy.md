# Privacy Policy — LS-MEM

## Network Deny-by-Default

LS-MEM code paths make **no external requests** by default. No `requests`, `httpx`, `urllib`, `socket`, `http.client`, `ftplib`, `telnetlib`, or `xmlrpc.client` calls to non-allowlisted origins in engine core.

**Enforcement:**
- Engine package `src/ai_company/lsmem/` declares `__all__` with no network imports
- CI gate: `bandit -r src/ai_company/lsmem/ --skip B101` must pass
- Optional: seccomp-bpf filter or capability-drop sandbox for engine process

## No Telemetry / No Remote Logging

- No analytics dependencies
- No OTel export from LS-MEM
- Stdlib logging only to local files under `.lightspeed/memory/`
- No remote handlers in audit subsystem (threat T20)

## Pre-Write Security Filter

Every content blob passes through:
1. Secret scanner (§8) — detects and redacts secrets before persist
2. Classification layer (§7) — assigns classification tier
3. Constitutional veto (ADR-019) — blocks prohibited content

Only after all three filters does content become a persistent row.

## Explicit Markers

Agents can use explicit markers to control persistence:
- `<memory>` — explicitly request persistence (default)
- `<no-memory>` — suppress persistence entirely
- `<private>` — persist but mark as private (excluded from injection/egress)
- `<external-approved>` — prerequisite flag for egress of otherwise-blocked content

## Export Privacy

- Second redaction pass on export (threat T26)
- RESTRICTED excluded by default
- Local file write only — never auto-uploaded
- Any subsequent send goes through permission gateway (§9)

## References

- Architecture: `docs/architecture/LS-MEM-ARCHITECTURE.md` §6
- Threat model: `docs/security/LS-MEM-THREAT-MODEL.md` T14–T20
- Locked decisions: deny-by-default, no telemetry, offline-first
