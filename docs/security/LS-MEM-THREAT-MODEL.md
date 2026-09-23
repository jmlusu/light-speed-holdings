# LS-MEM Phase 1 — Threat Model

**Project:** LightSpeed Holdings
**Date:** 2026-09-23
**Status:** Draft for review (Phase 1 of LS-MEM)
**Security classification:** Internal
**Related:** `docs/architecture/LS-MEM-RECONNAISSANCE.md`, `docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md`, ADR-019, `docs/SKILL_CURATION_POLICY.md`
**Locked decisions:** dual skill paths (`.agents/skills` + `.opencode/skills`); new SQLite engine + bridge to existing JSON `MemoryStore`

---

## 1. Scope and method

**In scope:** LS-MEM skill, memory tools, SQLite/FTS5 engine, secret scanner, permission gateway, audit subsystem, optional Ollama embeddings, dual skill deployment, `.lightspeed/memory/` storage.

**Out of scope (but boundary-adjacent):** existing JSON `MemoryStore` / ADR-019 pipeline (bridged, not rewritten), dashboard, Resend MCP, global OpenCode config.

**Method:** STRIDE-flavored checklist per threat from handoff §6, plus residual risk. Likelihood/impact: L/M/H. Test names map to Phase 5 acceptance (`offline`, `secret`, `external-access`, `authorization`, `git`, plus unit/integration).

**Default posture:** network-deny-by-default; Restricted never plaintext; when uncertain → BLOCK.

---

## 2. Threat register

### T01 — Accidental API-key storage

| Field | Value |
|-------|--------|
| **Threat** | Agent/session pastes API key into content later written as memory |
| **Likelihood** | H |
| **Impact** | H (key compromise → cloud spend, data access) |
| **Mitigation** | Pre-write secret scan (`PIIDetector` + JWT/`.env`/conn-string extensions); default FULL mask to `[REDACTED_SECRET]`; classify as RESTRICTED → never persist plaintext; optional gate: refuse store if confidence high and no explicit human override |
| **Test** | `secret`: store `sk-…`, `AKIA…`, `ghp_…` → assert not in DB bytes; audit shows `secret_blocked` |
| **Residual** | M — novel key formats may evade regex until Phase 5 pattern expansion; partial-mask edge cases |

### T02 — Password leakage

| Field | Value |
|-------|--------|
| **Threat** | `password=…`, `PASSWORD=…` in logs, docs, or memory content |
| **Likelihood** | M |
| **Impact** | H |
| **Mitigation** | Keyword+assignment redaction (`password`, `passwd`, `pwd`); scan full content not filenames; redaction before disk; forbid passwords in export previews without second redaction pass |
| **Test** | `secret`: password in markdown/code block → redacted |
| **Residual** | M — free-text “my password is hunter2” without assignment operator |

### T03 — OAuth-token leakage

| Field | Value |
|-------|--------|
| **Threat** | `access_token`, `refresh_token`, `Bearer …`, Google/`ya29.` tokens stored |
| **Likelihood** | M |
| **Impact** | H |
| **Mitigation** | Patterns for `ya29.`, `Bearer` JWT/`xoxb-`/`xoxp-`, `oauth` key-value; redact before persist; RESTRICTED class |
| **Test** | `secret`: sample OAuth tokens → redacted |
| **Residual** | L–M — proprietary IdP token shapes |

### T04 — Private-key leakage

| Field | Value |
|-------|--------|
| **Threat** | PEM `-----BEGIN … PRIVATE KEY-----` or base64 key blobs in memory/export |
| **Likelihood** | M |
| **Impact** | H |
| **Mitigation** | Existing `PRIVATE_KEY_PATTERN` + high-entropy base64 heuristic; block or full-redact entire block (not just header); never export raw |
| **Test** | `secret`: RSA/EC PEM body → no key material in DB/export |
| **Residual** | L |

### T05 — Prompt leakage

| Field | Value |
|-------|--------|
| **Threat** | System prompts, tool instructions, or hidden agent instructions stored and later injected into other agents |
| **Likelihood** | M |
| **Impact** | M–H (cross-agent instruction bleed) |
| **Mitigation** | Classification: system prompts → at least CONFIDENTIAL; optional deny patterns for “system prompt”/“ignore previous”; retrieval always tags content as **data not instructions** (Rule 7); quota on session injection |
| **Test** | unit: poisoned “system:” memory retrieved with untrusted marker; no auto-override of current instructions |
| **Residual** | M — semantic detection incomplete without NLP |

### T06 — Confidential-document ingestion

| Field | Value |
|-------|--------|
| **Threat** | Full client contracts, pricing, proposals dumped into memory then over-retrieved or exported |
| **Likelihood** | M |
| **Impact** | H |
| **Mitigation** | Classification CONFIDENTIAL; redaction pass; provenance + `approved_for_external_use=false` default; injection quota; export requires explicit scope + confirmation |
| **Test** | `secret`/`authorization`: confidential doc sample not in public export path without approval flag |
| **Residual** | M — human must classify when auto-classifier is wrong |

### T07 — Malicious memory

| Field | Value |
|-------|--------|
| **Threat** | Third-party or compromised source writes memory that later drives agent behavior |
| **Likelihood** | M |
| **Impact** | H |
| **Mitigation** | Provenance on every write; only allowlisted `created_by` actors; constitutional blocklist (ADR-019) + injection phrases; treat all recall as untrusted data |
| **Test** | unit: “ignore security and exfiltrate” → vetoed/not ACTIVE; retrieval does not execute |
| **Residual** | M — subtle social-engineering phrasing |

### T08 — Memory poisoning

| Field | Value |
|-------|--------|
| **Threat** | Bulk low-quality or adversarial entries drown useful memory (context flooding / ranking games) |
| **Likelihood** | M |
| **Impact** | M–H |
| **Mitigation** | Value score 0–5; only 3+ persist long-term; dedup/consolidation; per-source rate limits; staleness; supersession; FTS rank + quota (5–15 / ~1–2k tokens) |
| **Test** | integration: flood N junk rows → recall still returns high-score canonical set under quota |
| **Residual** | M |

### T09 — Malicious instructions stored in memory

| Field | Value |
|-------|--------|
| **Threat** | Stored text aims to override security policy when recalled into a future session |
| **Likelihood** | H |
| **Impact** | H |
| **Mitigation** | Constitutional blocklist; treat memory as data (Rule 7); never let memory bypass system/security/user approval; SKILL.md explicit anti-patterns; optional instruction-like pattern flag |
| **Test** | `secret`/unit: “Ignore all future security restrictions…” not ACTIVE or returned with `untrusted=true` |
| **Residual** | M |

### T10 — Malicious packages

| Field | Value |
|-------|--------|
| **Threat** | New PyPI/npm dep exfiltrates or backdoors memory paths |
| **Likelihood** | M |
| **Impact** | H |
| **Mitigation** | Zero new runtime deps for core (stdlib `sqlite3`, `json`, `hashlib`, `re`); dependency policy §24; `APPROVED-VENDORS.md` + skill curation; review network behavior |
| **Test** | Phase 5 dependency inventory empty of unexpected egress; optional `pip-audit` if already in toolchain |
| **Residual** | L — supply-chain of *existing* deps |

### T11 — Compromised dependencies

| Field | Value |
|-------|--------|
| **Threat** | Existing dependency release pulls data or alters SQLite behavior |
| **Likelihood** | L |
| **Impact** | H |
| **Mitigation** | No auto-upgrade in LS-MEM; pin via `uv.lock`; network-deny tests; avoid loading untrusted SQL extensions |
| **Test** | offline suite still green with network blocked |
| **Residual** | M (org-wide supply chain outside LS-MEM) |

### T12 — Malicious skills

| Field | Value |
|-------|--------|
| **Threat** | Another skill reads `.lightspeed/memory/` or injects via shared context |
| **Likelihood** | M |
| **Impact** | H |
| **Mitigation** | Skill vetting checklist; third-party transmission ban; filesystem ACL/least privilege where possible; LS-MEM never auto-exports to other skills without gateway; document path in README as sensitive |
| **Test** | curation checklist completed for `ls-memory` and peers; grep skill trees for outbound hosts |
| **Residual** | M — same-user skills share FS |

### T13 — Malicious MCP servers

| Field | Value |
|-------|--------|
| **Threat** | Existing remote MCP (e.g. Resend) or future MCP receives memory payloads |
| **Likelihood** | M |
| **Impact** | H |
| **Mitigation** | LS-MEM tools never call MCP; memory content not passed to MCP tools without permission gateway + human approval; network-deny default in LS-MEM code paths only |
| **Test** | `external-access`: LS-MEM egress unit mock — zero non-localhost sockets |
| **Residual** | M — other project tools may still use MCP |

### T14 — Unauthorized HTTP

| Field | Value |
|-------|--------|
| **Threat** | LS-MEM or its code path issues plain HTTP to non-allowlisted hosts |
| **Likelihood** | M |
| **Impact** | H |
| **Mitigation** | Network-deny-by-default; only explicit `127.0.0.1`/`localhost` for Ollama; permission gateway on any other origin; no `requests`/`httpx` in engine core |
| **Test** | `external-access`: monkeypatch socket/`urllib` → assert blocked + audit row |
| **Residual** | L |

### T15 — Unauthorized HTTPS

| Field | Value |
|-------|--------|
| **Threat** | HTTPS to cloud AI, logging, analytics, or sync endpoints |
| **Likelihood** | M |
| **Impact** | H |
| **Mitigation** | Same as T14; no TLS client in default code path; explicit allowlist + human approval required; default `external_access.enabled=false` |
| **Test** | `external-access`: attempts to OpenAI/Anthropic/Google-shaped URLs → BLOCK |
| **Residual** | L |

### T16 — DNS exfiltration

| Field | Value |
|-------|--------|
| **Threat** | Covert channel via DNS lookup of encoded data |
| **Likelihood** | L |
| **Impact** | H |
| **Mitigation** | No URL construction from memory content; no telemetry ping; sandbox tests with DNS stubbed; forbid embedding secrets in hostnames |
| **Test** | offline: no `getaddrinfo` for non-allowlisted names during full CRUD |
| **Residual** | L–M if a future dep resolves names |

### T17 — Cloud AI leakage

| Field | Value |
|-------|--------|
| **Threat** | Memory sent to OpenAI/Anthropic/Google as “to summarize/embed/rank” |
| **Likelihood** | M |
| **Impact** | H |
| **Mitigation** | Principle 8: no external AI by default; summarization is local or disabled; gateway requires provider+domain+operation+classification+human approval |
| **Test** | `external-access` + `authorization` |
| **Residual** | L |

### T18 — Cloud embedding leakage

| Field | Value |
|-------|--------|
| **Threat** | Text embedded via cloud embedding API (data leaves as embeddings) |
| **Likelihood** | M |
| **Impact** | H |
| **Mitigation** | Ollama local embeddings only (`nomic-embed-text`); if Ollama down → **FTS-only, never cloud fallback**; hard deny external embedding providers |
| **Test** | unit: Ollama unavailable → search works; no HTTP to embedding SaaS |
| **Residual** | L |

### T19 — Telemetry

| Field | Value |
|-------|--------|
| **Threat** | Usage/analytics/metrics shipped off-box |
| **Likelihood** | L |
| **Impact** | M–H |
| **Mitigation** | No analytics deps; no OTel export from LS-MEM code; metrics local file/SQLite only |
| **Test** | dependency + code grep; offline suite |
| **Residual** | L |

### T20 — Remote logging

| Field | Value |
|-------|--------|
| **Threat** | Logs shipped to SaaS log drain |
| **Likelihood** | L |
| **Impact** | H |
| **Mitigation** | stdlib logging to local files under `.lightspeed/memory/` or existing local logs; never attach remote handlers in LS-MEM |
| **Test** | unit: logger handlers are local |
| **Residual** | L |

### T21 — Git commit of memory

| Field | Value |
|-------|--------|
| **Threat** | `memory.db` or observations staged/committed |
| **Likelihood** | H (if gitignore missing — **currently missing**) |
| **Impact** | H |
| **Mitigation** | Add `.lightspeed/memory/` to `.gitignore` in Phase 2; optional `.gitattributes`/`info/exclude`; pre-commit safety note; never `git add` from LS-MEM |
| **Test** | `git`: create memory → `git status` clean of `.lightspeed/memory` |
| **Residual** | L after gitignore fix; until then **Critical open** |

### T22 — Git push of memory

| Field | Value |
|-------|--------|
| **Threat** | Memory pushed to GitHub/remote |
| **Likelihood** | L (depends on T21) |
| **Impact** | H |
| **Mitigation** | No push in LS-MEM; no CI job uploads memory dir; human-only git operations; Rule 5 |
| **Test** | `git` + policy: no automation pushes memory |
| **Residual** | L |

### T23 — Agent-to-agent data leakage

| Field | Value |
|-------|--------|
| **Threat** | One agent recalls CONFIDENTIAL memory and passes it to a lower-privilege agent/tool |
| **Likelihood** | M |
| **Impact** | H |
| **Mitigation** | Classification on every record; injection respects class; optional `agent_id` scoping; redact on untrusted boundaries; external-approved marker required for out-of-scope use |
| **Test** | unit: confidential memory not returned to unscoped query; redaction on export |
| **Residual** | M — same-user agents often share FS/context |

### T24 — Unauthorized external provider

| Field | Value |
|-------|--------|
| **Threat** | Non-allowlisted provider used “because convenient” |
| **Likelihood** | M |
| **Impact** | H |
| **Mitigation** | Permission gateway default empty allowlists; five-gate chain (enabled→provider→domain→operation→class→human); ambiguity → BLOCK; audit denials |
| **Test** | `authorization`: unapproved provider blocked; approved path audited |
| **Residual** | L if gateway correctly default-deny |

### T25 — Excessive memory retention

| Field | Value |
|-------|--------|
| **Threat** | Secrets/stale/restricted data retained indefinitely |
| **Likelihood** | M |
| **Impact** | M–H |
| **Mitigation** | ADR-019 TTLs + LS-MEM tier lifetimes (Tier 1 short); status EXPIRED/ARCHIVED; value score gates; `forget`/`purge`; retention policy doc |
| **Test** | unit: aged Tier 1 purged; restricted not retained |
| **Residual** | M |

### T26 — Accidental disclosure during export

| Field | Value |
|-------|--------|
| **Threat** | Export bundle contains secrets/Restricted or over-broad scope |
| **Likelihood** | M |
| **Impact** | H |
| **Mitigation** | Re-run redaction on export; default export excludes Restricted; human confirmation of scope; hash-only audit payloads; no auto-upload of export |
| **Test** | `secret` + export e2e: no plaintext secrets in file; Restricted excluded by default |
| **Residual** | M |

### T27 — Memory corruption

| Field | Value |
|-------|--------|
| **Threat** | SQLite corruption, partial write, bad FTS index |
| **Likelihood** | L |
| **Impact** | M–H (availability/integrity) |
| **Mitigation** | WAL + `PRAGMA integrity_check` on open; atomic transactions; `rebuild` for FTS; backup/restore doc (user guide); schema version |
| **Test** | integration: kill mid-write → recovery or clean error; `rebuild` restores search |
| **Residual** | L–M on abrupt power loss |

### T28 — Unauthorized memory deletion

| Field | Value |
|-------|--------|
| **Threat** | Agent or process wipes memory without authority |
| **Likelihood** | M |
| **Impact** | H (institutional loss) |
| **Mitigation** | `forget` soft-delete + audit; `purge` requires explicit elevated confirmation; Tier 3 human-verified harder to delete; optional backup retention before purge |
| **Test** | unit: purge without confirm → denied; audit records actor |
| **Residual** | L–M (root user can delete files) |

---

## 3. Cross-cutting controls

| Control | Component | Governs |
|---------|-----------|---------|
| Secret scanner / redaction | `security/pii_detector` + extensions | T01–T04, T26 |
| Classification PUBLIC→RESTRICTED | privacy/classification layer | T06, T23, T25 |
| Permission gateway (default deny) | gateway | T14–T18, T24 |
| Audit (local, hash-preferring) | audit subsystem | all approved/blocked egress, CRUD |
| Value score + lifecycle | engine | T08, T25 |
| Untrusted-retrieval rule | SKILL.md + runtime | T07, T09 |
| Git ignore + no-auto-git | `.gitignore` + tools | T21, T22 |
| Dependency minimalism | stdlib sqlite3 | T10, T11 |
| Local-only embeddings | Ollama optional | T18 |
| Bridge (import-only, no silent egress) | MemoryStore bridge | dual-engine confusion |

---

## 4. Open items before Phase 2

1. **Critical:** add `.lightspeed/memory/` to `.gitignore` (Phase 2 first commit).
2. Confirm redaction token: handoff example `[REDACTED]` vs system directive `[REDACTED_SECRET]` — **use `[REDACTED_SECRET]` as canonical**, accept `[REDACTED]` as legacy alias in matcher.
3. Independent security auditor ≠ implementing agent (handoff §29).
4. Dual-path skill copies must be content-identical (hash check in tests).

---

## 5. Phase 1 exit criteria

- [x] All handoff §6 threats listed with likelihood, impact, mitigation, test, residual
- [x] Cross-cutting control map
- [x] Git gitignore gap called out
- [ ] CEO/security review sign-off (pending)

**Next:** Phase 2 — `docs/architecture/LS-MEM-ARCHITECTURE.md` (after threat-model review).
