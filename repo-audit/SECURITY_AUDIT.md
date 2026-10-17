# Security Audit

**Scope:** committed content, ignore rules, pre-commit/CI gates, hook configuration.
**Not in scope:** destructive action. No secret was rotated, revoked, or removed.

---

## 1. Findings

| # | Sev | Finding | Evidence | Fix |
|---|---|---|---|---|
| S-1 | **HIGH** | `opencode.local.json` is **untracked but not gitignored** | `git ls-files --error-unmatch` → untracked; `git check-ignore -v` → no match | Add to `.gitignore`. A `git add .` would commit a local agent/LLM config that commonly carries endpoints and keys. |
| S-2 | MED | 9 QA screenshots + 6 dev logs are **tracked** | `qa-*.png`, `qa-report*.json`, `install.log`, `probe.log`, `runtask.log`, `vite*.log` all in `git ls-files`, and `git check-ignore` confirms no rule covers them | Untrack + gitignore. Logs can contain URLs with tokens, internal hostnames, and pasted payloads. |
| S-3 | MED | `tmp/` and `lab/` are **not gitignored** (216 MB + scratch) | `git check-ignore` → "NOT IGNORED" | Add both to `.gitignore`. Untracked-but-visible scratch is one `git add .` from history. |
| S-4 | MED | No secret scanning in any gate | `.pre-commit-config.yaml` hooks = trailing-whitespace, end-of-file-fixer, check-yaml, ruff, mypy, bandit. No gitleaks/trufflehog | Add a secret-scan hook (§20 Security Sanitization; bandit finds code patterns, not leaked credentials) |
| S-5 | MED | `open-design` is a gitlink **without `.gitmodules`** | `git ls-files -s open-design` → `160000 6fd2f60…`, no `.gitmodules` in tree | Supply-chain gap: the pinned commit has no URL, no provenance, and no integrity story. Add `.gitmodules`, or untrack and fetch on demand. |
| S-6 | LOW | Personal absolute path + username committed | `.env.example:38` → `AI_COMPANY_ROOT = C:\Users\jmlus\light-speed-holdings` | Replace with a relative/placeholder value. Leaks developer identity and breaks portability (§20). |
| S-7 | LOW | Duplicate key in `.env.example` — later silently wins | `TURNSTILE_HOSTNAMES` at lines **47 and 54** | Remove the duplicate. Line 54 (`light-speed-holdings.vercel.app,…`) overrides line 47 (`localhost,127.0.0.1`). |
| S-8 | LOW | Tool cache inside repo tree | `mypy`, `ruff`, `harness`, `agenttrace`, `ab-testing`, `storybook`, `screenshots`, `research`, `thought-leadership`, `career`, `pharos`, `content` | §16 requires one purpose per directory. Mixes runtime tooling with business code. Consolidate to `tools/`. |

### Verified clean

- `.env` (3,954 B) and `.env.local` (1,247 B) exist on disk and **are correctly gitignored**.
- `.env.example`, `.env.staging.example` are tracked and contain **no secrets** — only
  placeholders and config values. Scanned for `sk-`, `ghp_`, `AKIA`, `-----BEGIN`,
  and JWT-shaped tokens: clean.
- `openapi.json`, `metadata.json`, `vercel.json`, `opencode.json`, `package.json`: no
  credential-shaped strings.
- `models/` (24.1 GB) is gitignored — large binary weights cannot enter history (§32).
- `scripts/rotate-secrets.py` exists — key rotation is at least contemplated (§20).

## 2. Not yet performed (needs a dedicated pass)

| Check | Why it matters | Command |
|---|---|---|
| **Git history secret scan** | A secret committed and later removed still lives in history. Nothing above can see that. | `gitleaks detect --source . --redact` |
| Bandit scope | Confirm bandit actually scans all of `src/`, not a subset | check `.pre-commit-config.yaml` `files:` pattern |
| Docker/CI secret handling | Whether CI injects keys via secrets rather than committed files | review `.github/workflows/` |
| Public exposure surface | `index.html`, `openapi.json`, `metadata.json` at root — are any served publicly? | review `vercel.json` |

I recommend the history scan before any other security work; it is the only check that
can reveal a credential already burned.

## 3. Audit-integrity constraint (AGENTS.md §9.3)

Two paths are declared **audit evidence** and must not be written, moved, renamed, or
deleted by an auditor:

```
orchestrator/escalation_events.jsonl
orchestrator/dead_letter.jsonl
```

`orchestrator/escalation_events.jsonl.bak` (210.56 MB) and
`…jsonl.RUN2GENERATED` (21.92 MB) sit beside them. The `.bak` is a strong deletion
candidate on hygiene grounds, **but** because it shares a directory with declared
evidence, §9.3 applies and it requires explicit user sign-off before removal.

## 4. Required hardening (§20)

1. Add `gitleaks` (or equivalent) to `.pre-commit-config.yaml` **and** CI.
2. Gitignore `opencode.local.json`, `tmp/`, `lab/`, `*.log`, `qa-*.png`, `qa-report*.json`.
3. Untrack the 15 generated root artifacts (S-2).
4. Replace the personal path in `.env.example` (S-6); de-duplicate the key (S-7).
5. Resolve the `open-design` submodule provenance (S-5).
6. Run the history scan and, if anything is found, **rotate the credential** — deleting
   the commit is not sufficient.

## 5. Git hygiene

- **83 pre-existing unstaged changes** (58 deletions, 20 modifications, 5 untracked)
  existed before this audit. Those deletions are the user's in-flight work and must
  not be swept into an automated cleanup commit (§31, Git hygiene).
- Do not combine unrelated cleanup into a single `git add -A`. Stage by category so
  each cleanup is independently reviewable and revertable.
