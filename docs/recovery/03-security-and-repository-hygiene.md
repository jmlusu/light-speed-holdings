# 03 — Security and Repository Hygiene

**Date:** 2026-11-13
**Baseline HEAD:** `86d10e709c50424eb7109283ff7e7019a1a51bc2`
**Scope:** secrets, ignored-but-sensitive files, tracked session artifacts, CI workflow hygiene, and git-safety posture. Every claim below was produced by a command run in this session.

---

## 1. Committed-secret scan

A tracked-path scan (`git ls-files` filtered on `secret|token|credential|.pem|.key|.sqlite|.db|storageState|.env`) returned 33 paths. **None contains secret material.** Every hit is a code, test, doc, or asset filename:

| Match class | Examples | Assessment |
|---|---|---|
| Design tokens | `brand/tokens/brand-tokens.{css,json}`, `packages/design-system/src/tokens/*` | Colour/spacing tokens — not secrets |
| Auth **design** docs | `docs/adr/013-browser-session-tokens.md`, `harness/changes/archive/.../oauth2-client-credentials/*` | Architecture decision records — no credentials |
| Python token **budgeting** code | `src/ai_company/llm/token_bucket.py`, `token_counter.py`, `tests/unit/test_token_*.py` | LLM token accounting — not API tokens |
| Deployment tooling | `scripts/deploy/rotate-secrets.py` | A rotation *script*; contains no secret value |
| Public asset | `public/assets/sectors/credential-verification.svg` | Sector icon |
| Session state | `storageState.json` | See §2 |

No `.pem`, `.key`, `.sqlite`, or `.db` file is tracked. No committed file contains an API key, private key, password, or bearer token.

---

## 2. `storageState.json` (tracked session artifact)

| Property | Value |
|---|---|
| Tracked | yes |
| Size | 209 bytes |
| Contents | `cookies: []` (empty); one origin `http://localhost:1440`; one localStorage key `lightspeed_theme: dark` |
| Risk | **Low** — it stores a theme preference and no session cookies |

The file is a Playwright storage-state fixture. Because `cookies` is empty, it carries no authenticated session. It is safe to keep, but it is a dev-machine artifact; if it ever gains cookies it should be untracked. Recorded as a low-severity hygiene note (H-01).

---

## 3. Environment / secret file handling

| Path | Tracked? | Rule | Assessment |
|---|---|---|---|
| `.env` | **no** | `.gitignore:4` (`.env`) | Correctly excluded |
| `.env.*` | **no** | `.gitignore:5` | Correctly excluded |
| `.env.example` | yes | `!.env.example` (`.gitignore:6`) | Allowlisted placeholders only |
| `.env.staging.example` | yes | `!.env.staging.example` (`.gitignore:7`) | Allowlisted placeholders only |
| `opencode.local.json` | no | `.gitignore:8` | Correctly excluded |

The ignore rules are correct and the two example files are the only `.env*` paths tracked. **No live secret file is tracked.**

---

## 4. `_staging/` — ignored, untracked, and load-bearing

| Property | Value |
|---|---|
| Reference path | `_staging/lsh-prototype/` |
| Ignore rule | `.gitignore:256` = `_staging/` |
| Tracked files under `_staging/` | **0** (`git ls-files _staging` → 0) |
| Prototype source files | **241** under `_staging/lsh-prototype/src/` |

This is the single most important hygiene finding of the mission. The **only functional reference** for the AI Studio prototype is ignored by git and therefore exists solely on this workstation. If the directory is lost, the reconciliation in `02-…` can never be re-verified against the original. This is a **preservation risk, not a security leak** — no secrets live there. Recorded as **O-10**. This session did **not** alter the ignore rule or copy the prototype into the tracked tree (that would be an unauthorized scope change).

---

## 5. Git-safety posture

| Check | Result | Evidence |
|---|---|---|
| Active hooks | `commit-msg`, `post-commit`, `pre-commit` | `Get-ChildItem .git/hooks` (non-`.sample`) |
| `--no-verify` in recovery commits | none found | recovery commit subjects are plain conventional commits |
| Conflict markers in `src/**` | **0** | regex scan for `^<<<<<<<`, `^>>>>>>>`, `^=======$` |
| Force-push / rebase this session | none | no push performed at all |
| File deletions this session | none | working tree is additions + 3 modified files |

No hook was bypassed and no history was rewritten.

---

## 6. CI workflow hygiene — `.github/workflows/verify-vite.yml` (BROKEN)

The `Verify Vite Dev Server` workflow is red on `main` and has been red on every recent push. The workflow file is the cause:

| Line | Defect |
|---|---|
| `run: pnpm install` | `pnpm` is **not installed** on the `windows-latest` runner → `The term 'pnpm' is not recognized` |
| `pm2 start "C:\\Users\\jmlus\\light-speed-holdings\\scripts\\dev\\start-dev.ps1"` | Hard-codes a **developer-machine absolute path**; also depends on `pm2`, which is not provisioned in the job |
| `curl --output /dev/null ...` | Unix-only redirect; invalid on PowerShell/Windows |
| `run: pm2 delete vite-dev` | Same `pm2` dependency |

This is a **pre-existing repository-hygiene defect unrelated to the AI Studio recovery**. It does not gate `main` (the required checks are `CI` and `Site Build + Principles Gate`, both green at `86d10e70`), but it pollutes every push with a false-red check. Recorded as **O-01**; **not fixed this session** (fixing a CI workflow is a separate, authorized change).

---

## 7. Runtime hygiene observations (from the verification run)

These surfaced during route verification (`04-…`) and are environment/deployment issues, not repository leaks:

| Observation | Severity | Detail | Item |
|---|---|---|---|
| `/api/journey-events` → HTTP 404 | Low | The SPA POSTs telemetry to an endpoint that does not exist in the preview/dev server; the request is aborted and no data is lost | O-04 |
| Cloudflare Turnstile never settles on localhost | Low | The Insights page loads a challenge that fails DNS (`brunhild.challenges.cloudflare.com` unresolved) and blocks `networkidle`; page still renders | O-05 |
| Console CSP notice for `data:,` connect | Info | Turnstile's own `data:,` connect is blocked by the page CSP; harmless in the local context | O-05 |

None of these expose data or credentials.

---

## 8. Summary

| Area | Verdict |
|---|---|
| Committed secrets | **Clean** — none found |
| `.env` handling | **Correct** — only examples tracked |
| Session artifact | `storageState.json` low-risk (empty cookies) |
| Prototype reference | **At risk** — `_staging/` is untracked/ignored (O-10) |
| Git safety | **Clean** — hooks active, no bypass, no rewrite |
| CI workflow hygiene | **One broken workflow** (`verify-vite.yml`, O-01) — pre-existing, non-gating |

**No security defect was introduced by this session's changes.** The two standing hygiene items (O-01, O-10) predate the mission and are recorded, not silently altered.
