# Duplicate Implementations

Per §7 — search aggressively, then compare rather than silently pick.

---

## D-1. Brand token files — triplicated (CONFIRMED BYTE-IDENTICAL)

```
brand/tokens/brand-tokens.json       MD5 6E9D0EFA394D  ← canonical
public/brand/tokens/brand-tokens.json MD5 6E9D0EFA394D
static/brand/tokens/brand-tokens.json MD5 6E9D0EFA394D

brand/tokens/brand-tokens.css        MD5 975A7F6DE83F  ← canonical
public/brand/tokens/brand-tokens.css MD5 975A7F6DE83F
static/brand/tokens/brand-tokens.css MD5 975A7F6DE83F
```

`brand/CANONICAL_SOURCES.md` (per AGENTS.md) already declares `brand/**` canonical
with `static/brand/` + `public/brand/` as mirrors. `scripts/sync-brand.ps1` (6.1 KB)
is the generator.

**Disposition: CONSOLIDATE.** Keep `brand/` as the single editable source; treat
`public/`+`static/` as build mirrors. Two caveats before deleting anything:
1. Vite serves `public/` at a stable URL — `public/brand/tokens/*` may be **fetched
   at runtime by URL**, which makes it a build artifact, not a copy.
2. `static/` may be served by a different server (dashboard/backend), not Vite.
→ Correct action: keep mirrors, but **document them as generated** and add them to a
"do not hand-edit" list. Three identical files are only a problem if they can drift.
Verify runtime fetch paths before any change.

## D-2. `scroll-craft` — retired skill with 692 MB of surviving artifacts

`AGENTS.md` §9.2 states (retired 2026-09-23):

> Retired 2026-09-23: `claude-mem-*`, `scroll-craft`, `greploop`/`greploop-apps`
> (skills deleted; local `~/.claude-mem` purged).

Reality on disk:

| Path | Files | MB | Status |
|---|---:|---:|---|
| `.opencode/skills/scroll-craft/` | 171 | 692.3 | **retired skill still present** |
| `scrollcraft/` | 13 | 32.3 | duplicate feature copy |
| `docs/case-studies/lightspeed-scroll-page/artifacts/` | 22 | 78.9 | **duplicate of the above** |
| `lab/` | 39 | 216.1 | likely same screenshot corpus |

MD5 grouping inside `.opencode/skills/scroll-craft/` found **20 duplicate groups**,
including one group of 6 copies of a single 5.59 MB PNG and groups of 3 copies at
7.34 MB and 5.73 MB. Single largest duplicated asset ≈ 7.3 MB × 3.

**This is simultaneously a governance breach and the single largest hygiene item.**
A skill the governance policy declares deleted still ships ~692 MB of screenshot
artifacts into the agent skills directory, where it is auto-loadable context.

**Disposition: DELETE** (`.opencode/skills/scroll-craft/`, `scrollcraft/`,
`lab/` screenshots) with **ARCHIVE** reserved for the genuinely historical case-study
narrative in `docs/case-studies/`. Git history preserves the artifacts.

⚠️ Action ordering matters: this must be confirmed as the *intended* retirement, not
a reactivated skill. See OPEN_QUESTIONS.md Q1 — **do not delete on assumption.**

## D-3. Milestones deck generator — two implementations

```
scripts/generate-milestones-deck.js    25.5 KB
scripts/generate-milestones-deck.py   17.5 KB
```

Same output, two languages. §7 explicitly targets this pattern.

**Disposition: INVESTIGATE → CONSOLIDATE.** The `.js` is larger and the repo's
frontend toolchain is npm-based; the `.py` is the odd one out *if* the deck is a
frontend/render artifact. But `ls-presentation-design` prefers `python-pptx`.
Cannot be decided from filenames — needs to know which one is referenced.

## D-4. Three registry snapshots for the same company

```
company/agent-registry.json                    90 agents  ← current
company/agent-registry.json.bak-2026-09-18              ← backup (tracked!)
company/agent-registry.json.bak-2026-09-18-hybrid       ← backup (tracked!)
company/models.yaml                            11.7 KB   ← current
company/models.yaml.executor-bak                         ← obsolete config (tracked!)
```

All four are **tracked**, so Git is carrying hand-made `.bak` files — precisely the
§28 `*_backup` anti-pattern the directive forbids as a normal pattern.

**Disposition:** `.bak-2026-09-18-hybrid` = ARCHIVE (documents a real transition);
`.bak-2026-09-18` = DELETE (superseded by the hybrid, which is superseded by current);
`models.yaml.executor-bak` = ARCHIVE or DELETE depending on whether the executor
migration is live (OPEN_QUESTIONS.md Q5).

## D-5. One agent-operating-model file (not two)

```
AGENTS.md                      canonical (referenced everywhere, incl. §4 loading rules)
CLAUDE.md                      DOES NOT EXIST at the repo root — verified
open-design/{AGENTS,CLAUDE,CONTEXT}.md   nested project, own scope, not competing
.crush/                        a third agent tool's local state, UNTRACKED (crush.db, logs)
.mimocode/mimocode.jsonc       tracked tool config (no agent instructions)
.agents/skills/                tracked skill library (no agent instructions)
.opencode/agents/              tracked generated agent cards (output, not a contract)
```

There is **no root-level competing agent contract**. Only one instruction file
governs agent behaviour at the repo root: `AGENTS.md`. The genuine duplication risk
is narrower than it first appears:

- `open-design/` ships its own three instruction files, but they govern that nested
  project only; an agent loading `AGENTS.md` and then entering `open-design/` reads
  both by design.
- `.opencode/agents/` is **generated output** (GENERATED_FILES.md), so any drift from
  `company-registry.yaml` is a generation bug, not a competing contract.
- `.crush/` holds untracked local state, not instructions.

**Disposition: KEEP `AGENTS.md` as the single root contract.** No content conflict
to resolve. See OPEN_QUESTIONS.md Q6 for the residual tooling question.

## D-6. Root `orchestrator/` and `memory/` — data that looks like code

```
orchestrator/escalation_events.jsonl.bak          210.56 MB  untracked
orchestrator/escalation_events.jsonl.RUN2GENERATED 21.92 MB untracked
orchestrator/dead_letter.jsonl                     0.05 MB untracked
orchestrator/approvals.yaml                        tracked
memory/vector_index/vector_index.json              49.97 MB  untracked
memory/vector_index/tmp53nqnhf1.tmp                42.12 MB  untracked  ← literal .tmp
memory/aggregate.json                               2.93 MB  untracked
```

Not duplicate *implementations* — duplicate **locations**. The problem is that
runtime artifacts sit at the repo root where an agent will read them as
authoritative. `memory/aggregate.json` and `memory/vector_index/` overlap conceptually
with `src/ai_company/lsmem/`.

Also note the filename smell: `.RUN2GENERATED` and `tmp53nqnhf1.tmp` (§28 spirit —
version/run suffixes as filenames).

**Disposition:** relocate under an explicit runtime-state path; DELETE the `.bak`
and `.tmp`. ⚠️ **AGENTS.md §9.3 forbids writing/deleting inside evidence
directories** — `orchestrator/escalation_events.jsonl` and `orchestrator/dead_letter.jsonl`
are named audit evidence. Those two files must be **read-only** to any auditor, and
this run must not touch them.

## D-7. `open-design/` — a whole second repository

2.7 GB, 90,578 files, own `.git`, own `AGENTS.md` / `CLAUDE.md` / `CONTEXT.md` /
`LICENSE` / `vercel.json` / pnpm workspace, pulled in by
`scripts/setup-open-design.ps1`. Vendored, untracked (1 file).

**Disposition: INVESTIGATE → move out of the working tree.** It is a tool the
scripts install, not LightSpeed source. Per §18/§35 it has no justification as a
top-level LightSpeed directory.

## D-8. Legacy brand surface

```
brand/                        103 files   4.9 MB  ← canonical
Branding landing page/         52 files   2.8 MB  ← superseded
static/ + public/ (brand parts)          12.4 MB
```

**Disposition: ARCHIVE** `Branding landing page/`.

## Duplicate summary table

| ID | Subject | Size at stake | Disposition | Blocker |
|---|---|---:|---|---|
| D-1 | brand tokens ×3 | small (drift risk) | CONSOLIDATE as generated mirrors | verify runtime fetch |
| D-2 | scroll-craft corpus | ~1.0 GB | DELETE / ARCHIVE | Q1 |
| D-3 | milestones deck ×2 | 43 KB | CONSOLIDATE | find caller |
| D-4 | registry `.bak` ×3 | ~tracked | DELETE / ARCHIVE | Q5 |
| D-5 | root agent contract | — | KEEP `AGENTS.md` (no competitor) | none — verified |
| D-6 | runtime data at root | ~329 MB | RELOCATE + DELETE | §9.3 evidence guard |
| D-7 | `open-design/` | 2.7 GB | MOVE OUT | Q2 |
| D-8 | Branding landing page | 2.8 MB | ARCHIVE | none |

**Recoverable if all executed: ~4.0 GB on disk, and removal of every `*_bak`
filename from tracked state.**
