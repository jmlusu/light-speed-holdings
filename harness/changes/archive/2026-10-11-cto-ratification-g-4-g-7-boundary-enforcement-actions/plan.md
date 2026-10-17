# Plan

## Technical Approach

Four independent, additive edits following the G-1 precedent (static guard + tests):

- **G-4** — `ecosystem.config.cjs`: replace both hardcoded `script:` values with `"node_modules/vite/bin/vite.js"`, set `cwd: __dirname` (repo root of the config file), keep `args`/`port`/`env` untouched, add a comment noting `port` is declarative metadata whose parity is enforced by G-1 (`tests/unit/test_port_assignments.py::test_pm2_ports`).
- **G-5** — new `scripts/dev/verify-port-bindings.ps1`: for each of 1440/1441/8420/8421, (a) map the owning process via `Get-NetTCPConnection -State Listen`, (b) classify identity (node/vite vs python/uvicorn vs unbound), (c) apply the §5 contract probe when a listener exists — GET `/` on 1440/1441 must be HTML (fail if JSON `status`), GET `/health` on 8420/8421 must be JSON with a `status` field (fail if HTML). Exit non-zero on any cross-serving or identity mismatch; print a per-port table. Also remove the unused `$ProjectRoot` line from `scripts/dev/health-check.ps1:4`.
- **G-6** — `.github/workflows/site-principles-gate.yml`: add a step `python3 scripts/test/check-site-ports.py` (new, stdlib-only) asserting the four assignments in `vite.config.ts` (server 1441 / preview 1440) mirror `ecosystem.config.cjs` (vite-dev 1441 / vite-preview 1440). The workflow's PR trigger has no path filter, so the step runs on every PR including frontend-only ones (its stated design).
- **G-7** — `docs/organization/app-naming-and-port-assignments.md` §5: append a "Production residual risk (G-7)" note: in production the Dashboard is 8420 (internal/Docker) and the Marketing Site is Vercel :443 — different hosts, so cross-serving is structurally impossible; the §5 checklist therefore guards **local/dev/staging** exposure, which is where the four ports coexist on one machine.

G-6 uses a standalone Python script (not pytest) because the site gate runs in a bun/node job without the Python dependency set; the same assertions already exist as pytest for the Python CI path (G-1) — two surfaces, one meaning.

## Impacted Modules And Files

| File | Change |
|---|---|
| `ecosystem.config.cjs` | G-4: portable `script` + `cwd: __dirname` + metadata comment |
| `scripts/dev/verify-port-bindings.ps1` | G-5: new identity + contract-probe audit |
| `scripts/dev/health-check.ps1` | G-5: remove unused `$ProjectRoot` (line 4) |
| `.github/workflows/site-principles-gate.yml` | G-6: add port-assertion step |
| `scripts/test/check-site-ports.py` | G-6: new stdlib port-parity checker |
| `docs/organization/app-naming-and-port-assignments.md` | G-7: §5 residual-risk note + revision row |

Unchanged: `vite.config.ts`, `src/ai_company/**`, `tests/**`, compose/Docker files.

## Interfaces, Data, Permissions

- `verify-port-bindings.ps1`: read-only against local TCP table + HTTP GET probes; no auth needed (`/health` is auth-exempt per ADR-012). Exit codes: 0 = all four ports consistent (bound-correct or unbound), 1 = mismatch/cross-serving found, 2 = usage error.
- `check-site-ports.py`: reads two repo files, prints pass/fail lines, exit 0/1. No network, no deps beyond stdlib.
- No secrets, no new network egress, no permissions changes.

## Spec Gaps Found From Planning

- Ratification §7 does not name the G-6 checker's location; chose `scripts/test/check-site-ports.py` beside the existing `check-site-form-backend.py` pattern in the same workflow.
- Ratification does not define "identity" matching precisely; used process-image name (node vs python/uvicorn) per §5's "which process actually owns each port".

## Risks And Mitigations

- PM2 `cwd: __dirname` behavior differs from `"."` if pm2 is started outside the repo → `__dirname` is strictly *more* correct (config-relative); G-1 test + a manual `node -e "require('./ecosystem.config.cjs')"` check catch breakage.
- `Get-NetTCPConnection` is Windows-only → script targets the documented Windows dev host (AGENTS §12); non-Windows callers get a clear unsupported-OS exit 2.
- Concurrent session editing shared tree → only listed files touched; target files verified clean before edits.

## Verification Plan

1. `node -e "const c=require('./ecosystem.config.cjs'); ..."` → both apps resolve script/cwd, ports 1441/1440 intact.
2. `uv run pytest tests/unit/test_port_assignments.py -q` → green (G-1 parity after G-4 edit).
3. `python scripts/test/check-site-ports.py` → exit 0; then mutate a copy to confirm it fails (negative test via temp file, not committed).
4. `pwsh scripts/dev/verify-port-bindings.ps1` → runs on this host; with no servers bound expect "unbound" rows and exit 0; cross-serving negative check by pointing probes at a stub is optional (contract logic reviewed in-file).
5. `pwsh scripts/maintenance/lint-ecl.ps1` → PASS.
6. Confirm concurrent-session files remain untouched: `git status --porcelain` delta limited to this change's files.
