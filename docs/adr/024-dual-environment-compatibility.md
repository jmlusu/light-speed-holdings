# ADR-024: Dual-Environment Compatibility Adaptation (OpenCode & AI Studio)

**Status:** Proposed
**Date:** 2026-09-23
**Deciders:** CTO, DevOps Lead, Dashboard Owner
**Technical Domain:** Build Tooling / Environment Parity / Web Security

## Context

The root `lightspeed-holdings` repository is operated in two environments: **OpenCode**
(local/production) and **AI Studio** (managed cloud preview). AI Studio's syncs are mirrored
back into OpenCode, which creates three failure modes:

1. **Lockfile mutation** — a non-bun package manager silently regenerates a competing
   `package-lock.json`, stranding the project on a lockfile that disagrees with the
   authoritative `bun.lock`.
2. **Security posture drift** — a cloud preview that strips or hardcodes CSP/clickjacking
   headers leaks into local runs, weakening the local security baseline.
3. **Merge thrash** — AI Studio branches that rewrite lockfiles/workspace configs fight
   OpenCode branches on every merge.

The repo follows `dual_environment_compatibility_standard.md` as the governing standard,
but that document is written generically (Corepack-enforced **pnpm**, **Fastify** + helmet,
database layer). This repo's actual stack differs:

- JS toolchain is **bun** (`bun.lock`) with node `>=22.0.0`; Python is **uv** (`uv.lock`).
- No Fastify — the web dev surface is a **Vite** dev server; the only server with security
  headers is the FastAPI **dashboard** (`uvicorn`).
- No database layer — persistence is **file-based** (JSON/YAML/JSONL, ADR-002, ADR-005).

This ADR records the adapted implementation of the standard against the real stack.

## Decision

Adopt the dual-environment compatibility standard, adapted to this repository's actual
toolchain and server surfaces as follows.

### Adaptation Map

| Standard § | Generic intent | This repo's implementation |
|---|---|---|
| §1 Package Manager | Force one canonical package manager; refuse others | **bun** pin in `package.json` (`engines.bun >=1.4.0`, `packageManager: bun@1.4.2`) + `preinstall` guard `scripts/check-package-manager.cjs` that refuses non-bun installs |
| §2 Git Protection | Lockfiles/configs survive merges | `.gitattributes` `merge=ours_lockfile` for `bun.lock`, `uv.lock`, `package-lock.json`, `.npmrc`; driver via `scripts/setup-git-hooks.sh` |
| §3 Dynamic Server | Detect environment; adapt bindings + security headers | Vite dev server already compliant; FastAPI dashboard `security_headers()` gated on `AISTUDIO_PREVIEW` |
| §4 Database | Prevent AI Studio from breaking DB extensions | **N/A** — no DB layer; file-based persistence (ADR-005) |

### §1 — Package-Manager Guard

`package.json` already declares `engines`/`packageManager`; the `preinstall` hook runs
`node scripts/check-package-manager.cjs` (a `.cjs` because this package is `"type": "module"`).
The guard classifies the caller as bun only when the user-agent is `bun/<ver>` **or**
`npm_execpath` resolves to the bun executable:

```js
const isBun =
  /^bun\/\d/.test(userAgent) ||
  /[\\/]bun(\.exe)?$/i.test(process.env.npm_execpath || '');
if (!isBun) process.exit(1);
```

**Why both signals:** when bun is installed through the npm shim (this dev machine's
`AppData\Roaming\npm\bun.ps1` → `node_modules/bun/bin/bun.exe`), bun 1.4.x exports
`npm_config_user_agent = "npm/undefined ..."` for its own lifecycle scripts, so the
user-agent alone is not a safe classifier. Real npm/pnpm/yarn point `npm_execpath` at their
own CLI entry instead, making the execpath the reliable differentiator. Refusing only when
a non-bun manager is identifiable keeps spurious enforcement out; unidentifiable or bun
invocations pass.

### §2 — Lockfile Merge Drivers

`.gitattributes` maps the four files to `merge=ours_lockfile`; the driver is registered via
`git config merge.ours_lockfile.{name,driver}`. On Windows, `system` bash is WSL and mutates
the WSL git config — developers must register the driver with a native Git Bash
(`C:\Program Files\Git\bin\bash.exe`), which `scripts/setup-git-hooks.sh` documents.

### §3 — Env-Driven Security Posture

- **Vite dev server** (`vite.config.ts`) already satisfies the standard — `host: '0.0.0.0'`,
  `port: 3000`, `allowedHosts: true`. No change required.
- **FastAPI dashboard** (`src/ai_company/dashboard/app.py::security_headers()`): when
  `AISTUDIO_PREVIEW=true` the dashboard must render inside AI Studio's iframe, so
  `frame-ancestors https://*.google.com https://*.aistudio.google` is emitted and the
  `X-Frame-Options: DENY` fallback is dropped. Any other value keeps the strict local
  posture (`frame-ancestors 'none'` + `X-Frame-Options: DENY`). `DASHBOARD_CSP`, when set,
  still overrides the whole policy. Host-guard and CORS blocks are unchanged.
- `AISTUDIO_PREVIEW=` documented in `.env.example`; covered by tests in
  `tests/unit/test_dashboard_security.py`.

### Verification Parity

CI proof of the parity contract lives in `.github/workflows/site-principles-gate.yml`:
`bun install --frozen-lockfile` + `bun run build` must stay green — the same commands a
developer runs locally, so a locally-verified commit is byte-identical in AI Studio.

## Options Considered

### 1. Adopt the standard verbatim (Corepack + pnpm + Fastify) — rejected

The repo uses bun, not pnpm, and has no Fastify server. Installing corepack/pnpm would
contradict the existing bun lockfile and ports the standard's assumptions onto unproven
surfaces.

### 2. No adaptation (dual-environment risk accepted) — rejected

Leaves `package-lock.json` stranding, merges fighting over lockfiles, and a dashboard that
could render with weakened or hardened headers in the wrong environment.

### 3. Adapted adoption (chosen)

Map each standard section to the real toolchain/server surfaces; where the standard names a
component that does not exist (Fastify, database), record N/A with the governing ADR.

## Consequences

### Positive

- `bun.lock` stays authoritative across environments; `npm install` is a hard error with a
  clear remediation message.
- Merge drivers keep lockfiles and `.npmrc` intact when AI Studio branches merge back.
- Dashboard clickjacking posture is strict locally and only relaxed under an explicit
  `AISTUDIO_PREVIEW` opt-in — no silent cloud-config leak.
- Verification parity: one green command set (`bun install --frozen-lockfile`, `bun run
  build`) is the contract for local, CI, and AI Studio.

### Negative

- Non-bun managers are refused outright, including edge environments that previously
  resolved npm installs.
- Requires the git merge driver to be registered per machine; unregistered machines get a
  generic conflict-resolution fallback.
- The guard is stricter than a pure "allow absent user-agent" design: an invocation with no
  identifiable `npm_execpath` and a non-bun UA is refused. Real bun always sets
  `npm_execpath`, so this is not a practical regression.

### Mitigations

- Guard failure message names the fix (`bun install`) and the reason (`package-lock.json`
  synthesis).
- `scripts/setup-git-hooks.sh` + ADR cross-reference give developers an exact registration
  path for Windows native Git Bash.
- `DASHBOARD_CSP` remains a last-resort operator override for any environment.

## Evidence

- `bun install --frozen-lockfile` → `Checked 253 installs across 330 packages (no changes)`, exit 0.
- Guard simulation matrix (all expected): bun UA no-execpath → 0; npm UA + `npm-cli.js` → 1;
  bun-quirk `npm/undefined` UA + `bun.exe` execpath → 0; pnpm UA + `pnpm.cjs` → 1.
- `bun run build` (`tsc --noEmit --pretty false; vite build`) → exit 0; only pre-existing
  non-fatal warnings (CSS `file` property, >500 kB chunk).
- `ruff check src/` and `mypy src/` clean; dashboard security suite 67 passed; full
  `pytest` 2457 passed.

## References

- `dual_environment_compatibility_standard.md` — governing standard (§1/§2 strings at
  lines 45–59); left untouched as source of truth.
- `scripts/check-package-manager.cjs` — package-manager guard (this ADR).
- `scripts/setup-git-hooks.sh` + `.gitattributes` — merge-driver registration and rules.
- `vite.config.ts` — already-compliant dev server bindings.
- `src/ai_company/dashboard/app.py` — `security_headers()` env-gated framing.
- `tests/unit/test_dashboard_security.py` — AI Studio preview framing tests.
- `.env.example` — `AISTUDIO_PREVIEW` documented.
- `.github/workflows/site-principles-gate.yml` — bun CI parity proof.
- `docs/adr/005-file-based-persistence.md`, `docs/adr/002-json-message-bus.md` — §4 N/A basis.

## Next Steps

1. Register the merge driver on any new dev machine via `scripts/setup-git-hooks.sh` (native
   Git Bash on Windows).
2. Smoke-test the dashboard framing with `AISTUDIO_PREVIEW=true` in an AI Studio preview
   session and confirm strict headers locally without the flag.
3. Extend the guard matrix to CI (npm CI run must fail the same way) if a JS-CI job is ever added.
