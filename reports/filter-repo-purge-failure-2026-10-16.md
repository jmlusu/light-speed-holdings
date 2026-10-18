# Final Report — git filter-repo Purge Failure: Root Cause, Fix, and Validated Recovery Procedure

Scope: diagnosis and validation performed exclusively in throwaway clones under
`C:\Users\jmlus\AppData\Local\Temp\opencode\jev-diag\`. The real repository
(`C:\Users\jmlus\light-speed-holdings`) was never modified; no pushes were made.
All commands below were run against clones unless stated otherwise.

---

## 1. Root Cause (with quoted evidence)

**The failed invocation was missing `--invert-paths`.** With `--paths-from-file`,
git-filter-repo (2.47.0) defaults to *keep-only* semantics: the four paths in
`jev-purge-paths.txt` were treated as the ONLY paths to RETAIN, so every other
path in every tree was deleted.

Quoted from the failed run's debug output (captured in forensics):

```
[DEBUG] Passed arguments: Namespace(... inclusive=True,
  path_changes=[['filter', 'match', b'docs/adr/023-jev-system-one-integration.md'], ...])
```

Supporting source evidence (`git_filter_repo.py`, v2.47.0, line numbers = installed copy):

| Line | Evidence |
|---|---|
| 1956 | `action='store_false', dest='inclusive'` — `--invert-paths` is the only switch that sets `inclusive=False`; default is `inclusive=True` (keep-only) |
| 2265-2273 | `sanity_check_args` never forces `inclusive=False` when `path_changes` are present — the invocation runs "successfully" |
| 3716 | `_prunable()` — emptied commits are pruned during rewriting |
| 3824 / 3834-3892 | `--replace-text` rewrites blob contents only; binary blobs (NUL in first 8 KB) are skipped (no relation to the emptying) |

Failure chain: keep-only filter → only 4 paths retained → all other paths removed
from every tree → 4,100 files emptied from history → commits become empty
(tree == parent's tree) → pruned → result: **HEAD = `4d39675cf50bab288a0d44970555f12ed4d1b3cc`,
tree = `4b825dc642cb6eb9a060e54bf8d69288fcae41b9` (empty tree), 7 commits, 48 objects / 69.77 KiB**.
The same SHA `4d39675c` is what currently sits at `refs/heads/main` on
`https://github.com/jmlusu/light-speed-holdings.git` — i.e., the broken result was pushed.

Reproduction: `jev-diag\repro` (clone of `jev-purge-backup-20261016.bundle`) reproduced
the failure byte-for-byte (same HEAD `4d39675c`, same empty tree).

Component bisection (all four experiments complete):

| Variant run | Result |
|---|---|
| paths-only (`--paths-from-file`, no invert) | **catastrophic**: 7 commits, empty tree `4b825dc` |
| replace-only (`--replace-text` alone) | benign: 463 commits, 4,100 files |
| msg-only (`--message-callback` alone) | benign: 463 commits, 4,100 files, tree `579a158d` = baseline HEAD tree |
| each of the 4 path lines alone | **catastrophic** (2 / 3 / 5 / 3 commits, empty tree) |

Conclusion: no individual input line is bad; the missing `--invert-paths` flag is the
sole root cause. Replace-halves bisection was unnecessary once the whole replace
component proved benign.

Stream-level evidence (fast-export streams under `.git\filter-repo\`):

| Metric | Buggy run (`v-debug`) | Fixed run (`fixed-debug`) |
|---|---|---|
| Namespace `inclusive` | `True` | `False` |
| `commit refs/` records | 10 | 753 |
| change-lines kept | **695 of 49,144** | **49,094 of 49,144** |
| blob records | 12,305 (all passed through, later gc'd) | — |
| reset / tag records | 747 / 1 | 2 / 2 |
| exit code / HEAD / tree | (failed state) 7, `4d39675c`, empty | 0, `d28a5f7074f1ae740d5d7d421a76d5c20ffb0318`, `f993e94ab71d27d0d61802f97213775bff8e1a91` |

Evidence correction: earlier notes claimed export files of ~2.97 MB
(2,948,225 vs 2,974,966 B). Not reproducible: the actual files are
**1,215,765,137 B (original, 7,070,215 lines) vs 1,211,542,431 B (filtered)** in
`v-debug\.git\filter-repo\`. Reported here as measured.

## 2. The "4,100 files but empty tree" Anomaly — Explained

The two numbers describe opposite operations:

- The working tree really contained 4,100 tracked files (baseline `01facaf8`,
  tree `579a158d`).
- filter-repo's cleanup performs `git reset --hard <new-tree>`. With the new tree
  = empty tree, that reset **deletes all 4,100 files** and git prints:
  `Updating files: 100% (4100/4100), done.`
  The 4,100 is the DELETION count, not the content of the new tree.

Direct experiment (`jev-diag\anomaly-test`, empty-tree commit `f342442a`): the same
`reset --hard` reported deletion of the full 4,100-file index. The progress line's
appearance differs between logs (present mid-output in the original interactive
console run, absent from the captured repro log): git's progress UI is delay-gated
(≈2 s before first paint), so its presence depends on terminal timing. The deletion
itself is unconditional and was verified by experiment; the timing explanation is
inferred from the delay-gated rendering behavior observed in both runs.

## 3. The Exact Fix

The input files are NOT broken. `jev-purge-paths.fixed.txt` (4 lines, 130 B) and
`jev-purge-replace-text.fixed.txt` (53 tokens, 1,159 B) were verified **byte-identical**
to the originals (0 CR, LF line endings, same bytes). The fix is entirely in the
invocation — add `--invert-paths`:

```powershell
git filter-repo --force `
  --paths-from-file=C:\Users\jmlus\AppData\Local\Temp\opencode\jev-purge-paths.fixed.txt `
  --replace-text=C:\Users\jmlus\AppData\Local\Temp\opencode\jev-purge-replace-text.fixed.txt `
  --message-callback="import re; return re.sub(br'(?i)(jev|typesafe)', b'', message)" `
  --invert-paths
```

Reference implementation used for all validation runs: `jev-diag\driver.py`
(modes `fixed` / `fixed-debug`; exact args at lines 62-69).

Input hygiene rules that must continue to hold:

- Never edit the `.fixed.txt` files (they were validated as-is).
- Never introduce bare `jev` / `typesafe` literals into replace inputs — the
  base64 token `LjEv` (encoded `/jev`) exists in two package locks and is the
  documented corruption risk.
- No `#` comments in input files; LF only.

## 4. Validation Table (fixtest = fixed run on bundle clone)

| Gate | Expected | Measured | Verdict |
|---|---|---|---|
| Working-tree files (G1) | 4,100 | 4,100 | PASS |
| Commits on HEAD (G2) | within 5% of 463 (≈440-486) | 462 (463 − 1 intended prune) | PASS (99.8%) |
| Commits `--all` (G2b) | explained, no loss | 498 reachable outputs; 754 inputs = 1 zero-prune + 753 mapped, **all 498 distinct outputs reachable** | PASS (see §4.1) |
| 4 purge paths unreachable from any ref (G3) | 0 commits | 0 | PASS |
| 4 purge paths absent from worktree (G3b) | 0 files | 0 | PASS |
| Message scan: case-insensitive `jev\|typesafe` over `git log --all --format=%B` (G4) | 0 | 0 / 0 | PASS |
| Code scan: case-sensitive `-Gjev` (G5) | 0 | 20 commits | **FAIL as specified — unachievable by design, see §4.2** |
| Code scan: case-sensitive `-Gtypesafe` (G5b) | 0 | 4 commits | **FAIL as specified — same classification** |
| Lock files byte-identical to baseline `01facaf8` (G6/G7) | equal | 3 locks, equal=True (only case-insensitive hit = base64 `LjEv`, 2 locks, expected) | PASS |
| All 6 expected tags resolve (G8) | 6/6 | v0.4.0, v0.5.0, v0.5.1, v0.6.0, pre-restructure-2026-08-11, recovery-2026-07-26 | PASS |
| Spot checks `ceo_issues_list.md`, `.gitignore` (G9) | 0 hits | 0 | PASS |
| Working status clean (G10) | clean | clean | PASS |
| Repo stats | — | in-pack 19,349; pack 873.05 MiB | info |

### 4.1 Commits-`--all` accounting (why 754 → 498 with zero loss)

The input repository contains **two content-identical parallel copies of the same
history** — the local/remote divergence documented in `AGENTS.md` §16. Evidence:

- Pairs of input commits with identical tree, author/committer timestamps, and
  subject, differing only in parent links, e.g. `1dd7e0dc` (on base main) vs
  `f03b0484` (v0.6.0 tag lineage): both tree `b362599ed3bcae19609c772ab60411d78f134654`,
  both timestamp `1788382055`, both subject `style: apply pre-commit formatting fixes…`.
- Similar pair `3363a091` ↔ `7be94890` (origin-style v0.4.0 vs local v0.4.0 peeled).
- `git merge-base --is-ancestor 1dd7e0dc 01facaf8` → **yes** (main sits on the
  `1dd7e0dc`-style lineage); `f03b0484`/`8d35930a` chain → **not on base main**
  (152 side-only commits = `v060-not-main`).

Why the rewrite collapses each pair (recursion bottom-out proven at depth 26):

1. `--preserve-commit-hashes` is OFF by default — git_filter_repo.py:2043-2048:
   *"references to old commit hashes in commit messages are replaced with new commit
   hashes"* (code path line 3949). The validated invocation does not pass this flag.
2. Concrete pair at the divergence point: `8382e483` (main lineage, message
   `…changes from 837b9ed (…)`) vs `14b92001` (tag lineage, `…changes from 9f29b90 (…)`).
   commit-map: `837b9ed → 9f29b907` and `9f29b90 → 9f29b907` — the two copies of the
   referenced commit collapsed to one output, so the default hash-reference update
   rewrote message A's `837b9ed` into `9f29b90`, making the pair byte-identical.
   Tree was already identical (`3a28c775…`); only the message reference differed.
3. Equal content ⇒ same SHA under content-addressing ⇒ `commit-map` records two
   inputs for one output. Recursion converges down the chains to their common ancestor.

Resulting arithmetic (all cross-checked):

```
755 commit-map rows = 754 inputs + 1 bookkeeping
754 inputs = 463 (main chain) + 291 (tag-only chains)
outputs     = 1 zero-prune (aa8cf7fc, empty after filter, on main)
            + 753 mapped rows → 498 DISTINCT SHAs (255 outputs received 2 inputs)
498 = 462 (HEAD chain) + 36 (tag-only outputs)
462 HEAD   = 149 (shared ancestor region, unchanged)
           + 152 (side-lineage identity SHAs absorbed via collapse = v060-not-main)
           + 161 (main-unique commits rewritten to new SHAs)
463 main   = 149 shared + 314 unique (= 152 collapsed onto side + 161 own new + 1 pruned)
291 tag-only = 152 side-identity (collision partners of main) + 103 collapsed elsewhere + 36 unique
```

- `git rev-list --count --all` (fixtest) = 498 = distinct outputs, **all reachable** —
  earlier hypothesis of 255 unreachable kept commits is retracted.
- `301/301` v0.6.0-chain commits are members of fixtest `rev-list HEAD` (list membership
  verified directly), which is why `8d35930a` is an ancestor of rewritten HEAD
  (`merge-base --is-ancestor` → 0) but not of base main (→ 1): **the rewritten main
  chain absorbed the side lineage's unchanged SHAs through duplicate-collapse.**
- Consequence for tag lineages: input tag-only chains 291 → 36 distinct post-rewrite
  outputs (e.g. `backup/pre-strip-bulk-tag` chain overlap with HEAD grew from 262-unique-off-main
  to 8-unique-off-HEAD) — all consistent with the same collapse.

### 4.2 G5 / G5b classification (why the literal gates cannot pass)

Case-sensitive `-Gjev` (20 commits) / `-Gtypesafe` (4 commits) hits, classified:

| Class | Examples | Current at HEAD? |
|---|---|---|
| Random base64 substrings inside binary-ish assets | 12 `jev`-looking lines in logo SVGs (`public/logo-full.svg` et al.), `.venv/.../cacert.pem`, lock-file integrity hashes | Yes — SVG lines only (12) |
| Historical real tokens removed by later commits pre-rewrite | `# Jev / jevos` comment in `src/ai_company/llm/cost_tracker.py`; `jev:` keys + Jev/TypeSafe docstring in `.opencode/integrations/ecosystems/*`; `typesafe-path` npm package in `lightspeed-main-site/` + `marketing-site/package-lock.json` | No (history only) |

Zeroing these gates would require mutating base64/hash data (data corruption).
**Verdict: FAIL as literally written, unachievable by design; treated as documented
false-positives.** Case-insensitive scans additionally hit base64 `LjEv` in two
package locks — expected, by design, not a failure.

## 5. Exact Command Sequence for the Main Agent (real repository)

The validated procedure is **clone-based**: filter-repo never runs on the real working
tree, so untracked files (22 status lines), `refs/backup/*`, `refs/stash` (2 entries),
and the failed-run forensics in `.git\filter-repo\` are never touched.

```powershell
$real = "C:\Users\jmlus\light-speed-holdings"
$tmp  = "C:\Users\jmlus\AppData\Local\Temp\opencode"
$bundle = "$tmp\jev-purge-backup-20261016.bundle"

# 0. Preflight asserts (read-only) — all must hold before proceeding
git -C $real rev-parse HEAD            # expect 01facaf8a7d92a5a8ac005a5b5384b91c59a702e
git -C $real rev-parse HEAD^{tree}     # expect 579a158d…
git -C $real ls-files | Measure-Object # expect 4100
git ls-remote origin refs/heads/main   # expect 4d39675cf50bab288a0d44970555f12ed4d1b3cc (BROKEN)
# record backup ref SHAs (rollback anchors):
git -C $real for-each-ref 'refs/backup/*'
# bundle present: 915,049,778 B
Get-Item $bundle | Select-Object Length

# 1. Fresh run clone from the authoritative backup bundle (byte-identical inputs to fixtest)
git clone $bundle "$tmp\jev-run"

# 2. Fixed invocation (§3) — re-run via driver for exactness:
python "$tmp\jev-diag\driver.py" fixed "$tmp\jev-run"
#    (or the §3 command directly)

# 3. Assert outputs == validated fixtest result, then re-run gate battery
git -C "$tmp\jev-run" rev-parse HEAD   # MUST equal d28a5f7074f1ae740d5d7d421a76d5c20ffb0318
git -C "$tmp\jev-run" rev-parse HEAD^{tree}  # MUST equal f993e94ab71d27d0d61802f97213775bff8e1a91
#   G1:  git -C $r ls-files | Measure-Object                    → 4100
#   G2:  git -C $r rev-list --count HEAD                         → 462
#   G3:  rev-list --all -- <4 purge paths>                       → 0
#   G4:  git -C $r log --all --format=%B | Select-String -Pattern '(?i)jev|typesafe' → 0
#   G6:  git diff <baseline-sha> -- lock paths (3 locks)         → empty
#   G8:  6 expected tags resolve                                 → ok
#   G10: git -C $r status --porcelain                            → empty
# If HEAD ≠ d28a5f70: STOP — inputs drifted; do NOT push; re-validate before proceeding.

# 4. Push MAIN ONLY (force-with-lease pinned to the known broken SHA). Never push tags.
git -C "$tmp\jev-run" push --force-with-lease=refs/heads/main:4d39675cf50bab288a0d44970555f12ed4d1b3cc origin refs/heads/main:refs/heads/main

# 5. Post-push verify
git ls-remote origin refs/heads/main    # expect d28a5f7074f1ae740d5d7d421a76d5c20ffb0318

# 6. Bring the local real repo onto the new history (human-confirmed)
git -C $real fetch origin
git -C $real reset --hard origin/main   # untracked files untouched; backup refs keep old history anchored
```

Notes for step 4/6:

- `main` is protected (GitHub ruleset, 6 required checks, `.ai-company\constitution\11-GIT-STANDARDS.md`).
  A force-push will likely be rejected → **Jack Mlusu (CEO) must authorize a ruleset
  bypass / temporary allow-force-push.** Do not bypass silently.
- **Never push local tags.** Local v-tags are unchanged by the rewrite (`f03b0484`,
  `12d1ab82`, `ed559bbb`, `ee75c6d8` tag object, `1b30d8fe`, `e9809c0c`) while origin's
  v0.4.0/v0.5.0/v0.5.1/v0.6.0 point at *different* SHAs (`3363a091`, `89b20bab`,
  `f01e8e8b`, `1dd7e0dc`); a tag push would either be rejected or rewrite origin
  release pointers. Not required — the deliverable is main's history.
- Rollback (either before or after push): force-push the intact pre-failure main back:
  `git push --force origin 01facaf8a7d92a5a8ac005a5b5384b91c59a702e:refs/heads/main`
  (source: bundle clone), or restore from `$bundle` / `.lightspeed` backups.
- If a `jev-run` HEAD differs from `d28a5f70`: the inputs drifted — investigate before
  any push (the validated artifact is the pair of `.fixed.txt` files + exact args).
- Decision point (flag, do not assume): a **clone of the real repo** (as opposed to the
  bundle) exports a different ref set (no `refs/backup/*`, only 6 tags), which changes
  commit-map contents and could in principle change output SHAs via the default
  hash-reference update. The bundle-based sequence above is the validated path that is
  guaranteed to reproduce `d28a5f70`.

## 6. Old → New Ref / Tag SHA Map (base `01facaf8` → fixtest rewrite)

Annotated tags show tag object and peeled commit. `CHANGED` refs must be updated in
any tooling/docs that reference them; unchanged refs need no action.

| Ref | Old | New | Status |
|---|---|---|---|
| refs/heads/main | `01facaf8a7` | `d28a5f7074` | CHANGED |
| refs/tags/v0.6.0 (lightweight) | `f03b0484f7` | `f03b0484f7` | unchanged |
| refs/tags/v0.5.1 (lightweight) | `ed559bbcb0` | `ed559bbcb0` | unchanged |
| refs/tags/v0.5.0 (lightweight) | `12d1ab82ce` | `12d1ab82ce` | unchanged |
| refs/tags/v0.4.0 (annotated, object / peeled) | `ee75c6d874` / `7be948903c` | `ee75c6d874` / `7be948903c` | unchanged |
| refs/tags/pre-restructure-2026-08-11 | `1b30d8feaa` | `1b30d8feaa` | unchanged |
| refs/tags/recovery-2026-07-26 | `e9809c0c29` | `e9809c0c29` | unchanged |
| refs/tags/backup/pre-history-purge-one-skill | `1f3120d290` | `3d2346459b` | CHANGED |
| refs/tags/backup/pre-strip-bulk-tag | `22b7d0e2b1` | `c61fa4e414` | CHANGED |
| refs/tags/cleanup/c0-baseline | `048627adef` | `5329995b8d` | CHANGED |
| refs/tags/cleanup/c1-secrets | `d107ba44ec` | `c4f56ebf33` | CHANGED |
| refs/tags/cleanup/c2-caches | `aaef778e5f` | `70181ceb67` | CHANGED |
| refs/tags/cleanup/c3-root-moves | `87dae04ab4` | `495b116c8b` | CHANGED |
| refs/tags/cleanup/c4-scripts | `0690a16783` | `e6da29448c` | CHANGED |
| refs/tags/cleanup/c5-consolidation | `6b39ea44f6` | `37a278d376` | CHANGED |
| refs/tags/cleanup/c6-generated | `db06a21933` | `fb192ebfa4` | CHANGED |
| refs/tags/cleanup/c7-large-tools | `c3d2002d65` | `632b8dce8b` | CHANGED |
| refs/tags/cleanup/c8-docs | `c3ec018497` | `e7c71a2095` | CHANGED |
| refs/tags/cleanup/c9-validated | `bbe174c4be` | `6c06a620ff` | CHANGED |
| refs/tags/cleanup/c10-decommission | `b57c96fdf1` | `3793b61bf4` | CHANGED |
| refs/tags/cleanup/c11-landing (annotated, object / peeled) | `7fdcd5f20f` / `526f33d54f` | `88a4d443ed` / `6391f38b9e` | CHANGED |
| refs/remotes/origin/HEAD, origin/main | `01facaf8a7` | — | dropped by filter-repo (expected: remote-tracking refs removed) |

Origin state at diagnosis time (for lease assertions): `refs/heads/main` =
`4d39675cf50bab288a0d44970555f12ed4d1b3cc` (broken push); origin v0.4.0=`3363a091…`,
v0.5.0=`89b20bab…`, v0.5.1=`f01e8e8b…`, v0.6.0=`1dd7e0dc…` (differ from local —
do not overwrite; see §5 note). `pre-restructure-2026-08-11` and
`recovery-2026-07-26` match local. Post-rewrite, the new main descends through the
`f03b0484` (local-lineage) SHAs; origin's old-lineage tag objects keep their commits
reachable on the remote, so no GitHub-side GC exposure.

## 7. Residual Risks

1. **Protected-branch force-push** — ruleset with 6 required checks likely rejects
   step 4; requires explicit CEO authorization. Highest-probability blocker.
2. **G5/G5b literal zero-gates are unachievable** (§4.2). Do not "fix" by editing
   base64/hash data. Accept FAIL-with-classification, or reword the gate to
   case-insensitive messages (already 0) + current-HEAD real-token scan (12 SVG
   base64 lines only, benign).
3. **Historical real tokens remain in history** by design: `# Jev / jevos` comment
   (`cost_tracker.py`), `jev:` keys (ecosystems integrations), `typesafe-path` npm
   (marketing locks). They were removed by later commits before the rewrite; purging
   them from history would require a separate, much broader content rewrite.
4. **Case-insensitive scans hit base64 `LjEv`** in `packages/data-use-cases/package-lock.json`
   and `packages/design-system/package-lock.json` — expected; never "clean" these
   (corrupts integrity hashes). Any future input-file edit re-opens the corruption risk.
5. **Duplicate-lineage dedup changes history shape** (754 → 498 commits): 255 input
   pairs collapsed. Downstream references to pre-rewrite SHAs (backup/cleanup tags,
   docs, CI caches, releases) must use the §6 map. Old SHAs remain anchored locally via
   `refs/backup/*` + the bundle; on origin they remain anchored via origin's own tags.
6. **refs/stash (2 entries) and refs/backup/** on the real repo** — untouched under the
   clone-based procedure. Do NOT run filter-repo directly on the real repo: a direct
   run would rewrite stash/backup refs (as the failed run did) and destroy forensic anchors.
7. **Untracked files (22 lines)** — untouched by clone-based procedure and by
   `reset --hard` (untracked files are never removed by a hard reset to a different
   commit). Verify `git -C $real status --porcelain` after step 6 to confirm.
8. **Evidence corrections carried forward**: export files are ~1.216 GB, not ~2.97 MB
   (prior notes wrong); `commits --all` = 498 reachable with zero lost commits (earlier
   "255 unreachable" suspicion retracted); "4100 = deletions, not tree content".
9. **`aa8cf7fc` pruned** (zero-map) — intended: it became an empty commit after
   removing the purge paths (the only pruned commit; on main, hence 463 → 462).
10. **Post-push CI** — new main SHA triggers workflows; required checks must be green
    before any subsequent PR merges (they run on the new history).

---

### Evidence index (where to re-verify)

| Claim | Artifact |
|---|---|
| Root-cause Namespace quote / failed run | `filter-repo-state-failed-run\` (commit-map 617 lines/608 null, changed-refs 8) |
| Byte-exact reproduction (7 commits, `4d39675c`) | `jev-diag\repro\` |
| Component bisection | `jev-diag\v-paths\`, `v-replace\`, `v-msg\`, `v-path0..3\` |
| Streams (buggy vs fixed) | `jev-diag\v-debug\.git\filter-repo\fast-export.*`, `jev-diag\fixtest\.git\filter-repo\fast-export.filtered` |
| Fixed-run forensics | `jev-diag\fixtest\.git\filter-repo\{commit-map,ref-map,changed-refs,first-changed-commits,suboptimal-issues}` |
| Anomaly experiment | `jev-diag\anomaly-test\` (empty-tree commit `f342442a`) |
| Inputs (validated pair) | `Temp\opencode\jev-purge-{paths,replace-text}.fixed.txt` |
| Experiment driver | `jev-diag\driver.py` |
| Authoritative rollback | `Temp\opencode\jev-purge-backup-20261016.bundle` (915,049,778 B) |
| Source-of-truth for flag semantics | installed `git_filter_repo.py` lines 1956, 2043-2048, 2265-2273, 3716, 3834-3892, 3949 |
