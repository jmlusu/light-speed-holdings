# Open Questions

Each question states what was observed, why it blocks, and what a decision unblocks.
Ordered by how much downstream work each one gates.

---

## Q1 — Which brand-token copy is canonical, and does anything fetch the mirrors?

**Observed:** `brand/tokens/`, `public/brand/tokens/`, `static/brand/tokens/` are
byte-identical. `brand/CANONICAL_SOURCES.md` and `AGENTS.md` name `brand/**` as
canonical; `scripts/sync-brand.ps1` exists to regenerate the mirrors.
**Blocks:** deleting either mirror. If a runtime path reads `static/brand/tokens/`
directly (not via the sync script), deleting it breaks the deployed site.
**Unblocks:** GENERATED_FILES.md classification, Stage 5.
**Ask:** is `static/brand/tokens/` read at runtime, or only written by
`sync-brand.ps1`? May the mirrors be gitignored and generated at build time?

---

## Q2 — What is `open-design/`, and how should it be tracked?

**Observed:** 2,731.8 MB, 90,578 files, its own `.git`, `AGENTS.md`, `CLAUDE.md`,
`CONTEXT.md`, `LICENSE`, `vercel.json`, pnpm workspace, `node_modules/`.
Recorded in the parent repo as `160000 6fd2f60802232e0fdb29121a6b3e745d2fe9ff42`
— **a gitlink with no `.gitmodules` file**.
**Blocks:** any `git clone` works correctly; Stage 7 disk reclamation.
**Ask:** is this a deliberate dependency? If yes, add a proper `.gitmodules` entry so
fresh clones can resolve it. If no, untrack the gitlink and have
`scripts/setup-open-design.ps1` fetch it on demand into a gitignored location.
**Note:** the current state is broken either way — a fresh clone yields an empty
`open-design/` and `git submodule update --init` cannot resolve it.

---

## Q3 — Which `generate-milestones-deck` survives?

**Observed:** `scripts/generate-milestones-deck.js` and
`scripts/generate-milestones-deck.py` are competing implementations with different
runtimes (Node vs Python).
**Blocks:** Stage 5 deduplication.
**Ask:** which output is in use? Is the other referenced by CI, `package.json`, or
`Makefile`? Which runtime does the repo standardise on (ties to Q7)?

---

## Q4 — Which memory implementation is canonical?

**Observed:** three candidates —
`src/ai_company/memory/` (Pydantic store), `src/ai_company/lsmem/` (LSM engine),
and root `memory/` (runtime vector state, 96.1 MB).
Root also carries `Clean-LSMEM.ps1` and a `.pytest_tmp_linkedin/` cache, suggesting
LSMEM was worked on recently.
**Blocks:** directive §14 (memory subsystem audit) sign-off; root runtime relocation.
**Ask:** which is the production path? Is `lsmem` a replacement in progress, an
experiment, or legacy? Root `memory/` is *runtime state*, so it must move regardless —
the question is only which *implementation* owns it.

---

## Q5 — Which agent registry is the source of truth?

**Observed:** `company-registry.yaml`, `company/agent-registry.json`, and
`.opencode/agents/*.md` all describe **90 agents**. The count agrees; field-level
consistency has **not** been verified. Two dated hand-made backups sit in Git
(`agent-registry.json.bak-2026-09-18`, `.bak-2026-09-18-hybrid`), plus
`company/models.yaml.executor-bak`.
**Blocks:** DEAD_CODE.yaml completeness; Stage 5; deleting the `.bak` files.
**Ask:** is the JSON generated from the YAML, or hand-maintained? Which drift, if
any, is authoritative? Are the `.bak` files needed, or is history sufficient?

---

## Q6 — One agent contract at root, or several tool configs?

**Observed:** `AGENTS.md` is thorough (11 sections) and is the **only** root-level
instruction file. A root `CLAUDE.md` **does not exist** — verified. `.opencode/agent/`
(singular) does not exist either; the tracked path is `.opencode/agents/` (plural),
which holds **generated** agent cards. Alongside these sit three tracked/untracked
tooling surfaces that are *configuration, not instructions*:
`.crush/` (untracked — `crush.db`, `logs/`), `.mimocode/mimocode.jsonc` (tracked),
`.agents/` (tracked — `skills/`, `.skill-lock.json`, `proposal-fix-team.md`).
`open-design/` additionally ships its own `AGENTS.md`/`CLAUDE.md`/`CONTEXT.md`, scoped
to that nested project.
**Blocks:** Stage 5 consolidation — specifically, deciding whether `.crush/`,
`.mimocode/`, and `.agents/` are promoted to documented surfaces or removed.
**Ask:** there is no competing root contract to reconcile, so the real question is
narrower: should `.crush/` (local tool state) be gitignored, and should `.mimocode/`
and `.agents/` be documented in `AGENTS.md` as supported tool config or retired?
**Resolved by evidence:** the "two contracts" framing is withdrawn — `AGENTS.md` is the
single root contract.

---

## Q7 — npm or Bun?

**Observed:** one `package.json` with **two** lockfiles — `package-lock.json` and
`bun.lock`. There is already a guard script, `scripts/check-package-manager.cjs`.
`AGENTS.md` documents `npm run dev`.
**Blocks:** Stage 5; reproducibility (§20).
**Ask:** which is canonical? A reference sweep is still needed across CI, hooks,
deployment, `Makefile`, and docs. Recommend deleting the loser's lockfile *after* that
sweep.

---

## Q8 — Is `scroll-craft` genuinely retired?

**Observed:** `AGENTS.md` §9.2 states the skill was **deleted** on 2026-09-23, and
names it as a governance violation. Reality: `.opencode/skills/scroll-craft/` holds
692.3 MB, `scrollcraft/` adds 32.3 MB tracked, and
`docs/case-studies/lightspeed-scroll-page/artifacts/` holds 78.9 MB of duplicate QA
screenshots. Roughly 800 MB total, plus 22 PNGs sharing exact hashes.
**Blocks:** Stage 7 — ~800 MB.
**Ask:** **confirmed safe to delete all three locations?** The policy and the
filesystem disagree; policy alone is not authorization. This is the single largest
reclaimable tracked footprint.

---

## Q9 — RESOLVED — no action: the "lmstudio" reference and the §40 premise

**Status:** resolved; nothing to decide.
**Why the original question was wrong:** it rested on two false premises. (1) §40
does not mention competitors — its only normative line is "**Do not optimize for
the number of files deleted.**" The four "competing" occurrences in the directive
(lines 17, 131, 428, 1535) concern internal configuration, model versions,
instructions, and implementations, not product mentions in documentation. (2)
`AGENTS.md` contains no `lmstudio` or "LM Studio" string at all; a direct search of
`AGENTS.md`, `README.md`, and `company-registry.yaml` returned zero matches. The
only occurrences in the tree are test fixtures in
`open-design/apps/daemon/tests/runtimes/run-failure-telemetry-smoke.test.ts`.
**Also retracted:** the earlier version of this question assumed a root
`CLAUDE.md` competitor file. Root `CLAUDE.md` is absent (verified) and
`AGENTS.md` is the single root contract, so there is no conflict to resolve.
**Matching correction:** the finding in `repo-audit/DOCUMENTATION_AUDIT.md` is
retracted for the same reasons.

---

## Q10 — Can runtime state be relocated out of the repo root?

**Observed:** root `orchestrator/` (232.6 MB) and `memory/` (96.1 MB) are runtime
output. `approvals.yaml` and `memory-index.yaml` are **tracked**; most JSONL/vector
artifacts are untracked.
**Constraint:** `orchestrator/escalation_events.jsonl` and
`orchestrator/dead_letter.jsonl` are declared audit evidence in `AGENTS.md` §9.3 and
**must keep their current paths**.
**Ask:** confirm a new runtime path (e.g. `~/.lightspeed/runtime/` or a gitignored
`runtime/`). Confirm the two evidence files stay put and that
`escalation_events.jsonl.bak` (210.56 MB) may be deleted.

---

## Q11 — Is `src.bak/` safe to delete?

**Observed:** `src.bak/` holds 410 files — a full copy of the Python source tree.
**Ask:** does it contain anything not in `src/`? Recommend delete-if-redundant.

---

## Q12 — What are the near-empty root directories for?

**Observed:** `api/` (5 files), `dashboard/` (9), `hr/` (2), `tasks/` (3), `prompts/` (2),
`survey/` (3), `.crush/` (3 — untracked), `.mimocode/` (1).
`dashboard/` conflicts by name with the real dashboard in `src/`.
**Ask:** delete as scaffolding, or fill in?

---

## Q13 — Where should `.md` (the file named exactly `.md`) come from?

**Observed:** a tracked root file named exactly `.md` — no name, just an extension.
Hidden from normal listings and never reviewed.
**Ask:** none needed if you authorise reading and deleting it. Flagged for visibility.

---

## Q14 — Which output directory is canonical?

**Observed:** `.gitignore` covers `results/`, `logs/`, `data/`, while QA output lands
at root and `backups/` is ignored-but-recreated by `scripts/backup.ps1`.
**Blocks:** a single declared output location (§7); ending the backup-in-repo pattern.
**Ask:** declare one output root (e.g. `reports/` for artefacts, outside the repo for
backups) and have `scripts/backup.ps1` write there.

---

## Q15 — Does CI run, and what does it gate?

**Observed:** `.github/` exists alongside `.github.bak/`, `.github.old/`, and
`.github-security/`. `.pre-commit-config.yaml` runs ruff, mypy, and bandit locally.
**Ask:** what workflows are live? This determines whether the cleanup can be verified
in CI or only locally, and whether the `.bak`/`.old` copies can go.

---

## Minimum set needed to proceed

**Q2, Q5, Q7, Q8** unblock the most work. Everything else can be deferred while the
zero-risk stages (Stage 0 docs, Stage 2 caches) proceed without any decision.

For full detail and recovery paths see `CLEANUP_PLAN.md`.
