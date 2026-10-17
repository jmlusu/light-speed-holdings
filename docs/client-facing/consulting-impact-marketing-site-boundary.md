# Consulting Impact Note — "Marketing Site" Rename & Application/Port Boundary

**Date:** 2026-10-10
**From:** Consulting Engagement Lead
**To:** Chief of Staff, Chief Marketing Officer, Chief Strategy Officer
**Trigger:** Org-wide directive — the Vite Application is now the **Marketing Site** (owner: CMO; ports 1441 dev / 1440 preview, PM2 `ecosystem.config.cjs`). The CEO Dashboard (FastAPI/uvicorn, 8420 prod / 8421 dev) is a separate internal application. Never serve one on the other's port.
**Source of truth:** `docs/organization/app-naming-and-port-assignments.md` (CSO, 2026-10-10); boundary rules mirrored in `AGENTS.md` §12–§13.

---

## 1. Summary

The directive is primarily an engineering/ops control, but it has three client-facing surfaces for Consulting:

1. **Naming hygiene** — decks, SOWs, and proposals must say **Marketing Site**, not "Vite Application"/"Vite SPA".
2. **Demo isolation** — client demos may only ever point at the Marketing Site (local preview `:1440` or production `lightspeedholdings.vercel.app`). **Ports 8420/8421 are internal-only** — exposing the CEO Dashboard to a client leaks internal ops (task board, approvals, KPIs, org data) and breaks the "internal vs. external network domain" rule in the directive.
3. **Demo environment boundary** — any client demo environment must bind only to 1440/1441 and deploy like the Marketing Site; the dashboard must never be published on an external-facing/demo host.

**Status of existing consulting artifacts (scanned 2026-10-10):**

| Artifact | Finding | Risk |
|---|---|---|
| `proposal-deliverables/villagereach-ussd-consultant-proposal.md`, `Executive-Summary.md` | No port or app-name references | ✅ Clean — no rewrite |
| `docs/legal/sow-template.md` | No app names/ports (placeholder-driven) | ⚠️ Clean but has **no demo/environment boundary clause** — future SOWs could promise demos without the port rule |
| `whitepaper/lightspeed-malawi-investor-deck.*` + `generate-malawi-investor-deck.py` / `generate-malawi-investor-html.py` | External deck cites *"FastAPI REST + WebSocket dashboard (port 8420)"* | ⚠️ Correct port, but **internal port numbers should not appear in external decks**; consulting decks that inherit this copy will repeat it |
| `docs/client-facing/USE-CASE-CATALOG.md:526` | "Repo-root **Vite SPA**" (old name) | ⚠️ Stale naming in a client-facing doc |
| `docs/client-facing/website-compliance-ticket-ledger.md:40` | "Vite dev middleware" (technical, internal) | ✅ Acceptable (internal engineering note) |
| Consulting demo runbook | **Does not exist** | 🔴 Gap — no written rule preventing a demo from pointing clients at 8420/8421 |

---

## 2. Client-Facing Risk Assessment

| # | Risk | Severity | Why it matters to engagements |
|---|---|---|---|
| R1 | A client demo or screen-share opens `localhost:8420/8421` (CEO Dashboard) by mistake | **High** | Exposes internal approvals, KPIs, org health to a client; RBAC is fail-closed but that means a broken/blank screen in front of the client instead — either outcome damages delivery credibility and could breach confidentiality expectations in the MSA |
| R2 | A demo environment serves the wrong app on a shared port (Marketing Site on 8420, or dashboard on 1440) | **High** | Violates the directive's hard rule; health checks diverge (`GET /health` JSON vs `/` SPA) so demo monitoring silently probes the wrong service |
| R3 | Old name ("Vite Application", "Vite SPA") in client-facing docs and derived decks | **Medium** | Professionalism/consistency; clients see two names for one deliverable |
| R4 | Internal port numbers (8420/8421) quoted in external decks/proposals | **Medium** | Advertises internal attack surface; invites "can you show us that dashboard?" requests we must decline or re-scope |
| R5 | SOW promises a "demo" without pinning which application/port/environment | **Medium** | Ambiguity at acceptance time; potential scope/SLA dispute during delivery |

---

## 3. Action Items

| ID | Action | Owner | Due | Verification |
|---|---|---|---|---|
| **C-1** | **Acknowledge the directive** to the Chief of Staff (48h ack requirement in §7 of the source doc) on behalf of Consulting | Consulting Lead | **2026-10-12** | Ack recorded by Chief of Staff |
| **C-2** | **Publish a one-page Consulting Demo Environment Rule** (new section or sibling doc): client demos use the Marketing Site only — `http://localhost:1440` (preview) or `https://lightspeedholdings.vercel.app` (production); **never** 8420/8421; dashboard demos are internal-only and must be redacted/recorded, never live-shared | Consulting Lead | 2026-10-14 (Week 1) | Doc merged; linked from demo checklists |
| **C-3** | **Fix stale naming** in `docs/client-facing/USE-CASE-CATALOG.md` ("Repo-root Vite SPA" → "Marketing Site (repo-root Vite/React SPA)") | Consulting Lead (or CMO delegate) | 2026-10-14 (Week 1) | Grep for `Vite SPA` / `Vite Application` under `docs/client-facing/` returns 0 |
| **C-4** | **Raise a CMO/Pharos ticket** to strip internal port numbers (`port 8420`) from investor/regenerator deck sources (`whitepaper/generate-*.py`) and re-render the PPTX/HTML — consulting decks inherit this copy | Consulting Lead → CMO | 2026-10-17 (Week 1) | Deck sources contain no `8420/8421`; regenerated artifacts diffed |
| **C-5** | **Add a "Demo & Environment Boundary" clause to `docs/legal/sow-template.md`**: deliverable demos run on the Marketing Site (1440/1441 or production URL); internal dashboards (8420/8421) are out of scope for client access unless separately written into the SOW with access controls | Consulting Lead | 2026-10-17 (Week 1) | SOW template linted; next issued SOW includes the clause |
| **C-6** | **Pre-delivery demo checklist gate**: before any client-facing demo, verify (a) correct port/app (Marketing Site on 1440/1441, `pm2` status), (b) no dashboard process shared, (c) screen-share URL whitelist contains only Marketing Site origins | Consulting Lead + QA Lead | 2026-10-21 (Week 2) | Checklist used and signed off on the next live demo |
| **C-7** | **Sweep all proposal/deck generators** (`proposal-deliverables/*.py`, `whitepaper/*.py`, `static/brand/templates/generate-pitch-deck.py`) for old app names and internal ports; add a pre-flight grep to the deck QA step (`ls-artifact-qa` content QA) | Consulting Lead | 2026-10-24 (Week 2) | Generator outputs scanned clean; QA step rejects `Vite Application|8420|8421` |
| **C-8** | **Escalation path**: any suspected port misconfiguration during a client engagement → stop the demo, notify Chief of Staff same day, CSO review within 24h (per directive §6) | Consulting Lead | Standing | Incident logged |

---

## 4. What does NOT change

- VillageReach USSD proposal and Executive Summary: **no action** — they reference no ports or app names.
- The SOW/MSA legal framework: only the additive demo-boundary clause (C-5).
- Internal engineering docs (`docs/API-REFERENCE.md`, dashboard user guide): correct as written — 8420/8421 references there are internal and accurate.
- Delivery SLAs in existing engagements: unaffected; this is a naming/environment control, not a scope change.

---

## 5. Sign-off

- [ ] Consulting Lead — C-1, C-2, C-3, C-5, C-6, C-7
- [ ] CMO — C-3 (owner), C-4 (deck regeneration)
- [ ] Chief of Staff — directive ack + escalation contact (C-8)
- [ ] QA Lead — C-6 co-owner

*Two-week cadence: all items land within the current delivery window (by 2026-10-24).*
