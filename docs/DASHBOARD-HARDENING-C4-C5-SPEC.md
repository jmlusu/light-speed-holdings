# C4 & C5 — Draft Spec (Dashboard Hardening Plan)

> **Status: DRAFT — awaiting CEO approval. Nothing is implemented yet.**
> These are the two remaining items from the CEO dashboard hardening plan
> (A1–A5 hardening + C1–C5 reliability/observability). A1–A3, C1, C2, C3 are
> complete and verified. This document specifies C4 and C5 for approval.
>
> **Important honesty note up front (C4):** the codenames "Path-of-RPG" and
> "FLORA" from the original handoff have **no matching plan, spec, or code
> anywhere in this repository** (searched `docs/`, `harness/`, source, and
> graph artifacts). I will not invent a meaning that may not be yours.
> C4 below therefore proposes the most reasonable interpretation and lists
> the **decisions I need from you** before I build anything. C5 is fully
> concrete and ready to build on your sign-off.

---

## C5 — ReportStore (concrete, ready to build)

### Problem

Agents persist their run output as `results/<run_id_or_name>/loop_result.json`
and similar files (e.g. `results/t1-status-summary/loop_result.json`,
`results/cost_log.jsonl`). Today there is **no single, queryable abstraction**
over these agent-produced reports:

- Reading any report means hand-walking the filesystem with no stable API.
- Timestamps are stored inconsistently (some naive `datetime.now().isoformat()`,
  some UTC) — so sorting "newest first" and comparing across reports is
  unreliable.
- There is no way to fetch "the latest N reports" or "the oldest N" by a
  consistent rule (query-based head/tail).

### Goal

Add a `ReportStore` abstraction (new module under `store/`) that:

1. **Lists and reads** agent-produced reports under a configured root
   (default the dashboard/`results/` root).
2. **Normalizes timestamps** — any stored `datetime`/ISO string is parsed
   defensively and exposed timezone-aware (naive assumed UTC, `Z` handled),
   so ordering is correct regardless of how a report was written.
3. **Exposes query-based head/tail**:
   - `latest(n)` — the newest `n` reports by timestamp.
   - `oldest(n)` — the oldest `n` reports.
   - filtering by agent/session/report name and a `since`/`until` window.
4. **Is fully unit-tested** (datetime parsing matrix, ordering, head/tail,
   empty/missing root, malformed reports).

### Non-goals (C5)

- No new persistence format, no migration of existing `results/` files.
- No schema enforcement on report *contents* (reports stay free-form JSON).
- No dashboard UI in C5 — UI surfacing is a separate follow-up (candidate for C4
  FLORA work if you confirm it).

### Approach / modules

- `src/ai_company/store/report_store.py` — new. `ReportStore(root: Path | None)`.
- Reuse existing patterns from `store/file_store.py` / `store/repo_write.py`
  where sensible; this is a read-heavy layer, so it will not force writes into
  the guarded-write path (reports are written by agents today, not here).
- `tests/unit/test_report_store.py` — new.

### Acceptance criteria (C5)

- A1: `ReportStore(root)` lists all report folders/shards under `root`.
- A2: `latest(n)` / `oldest(n)` return the correct records in the correct order
  even when timestamps mix naive-UTC and `Z`-suffixed forms.
- A3: a report with a missing/unparseable timestamp never crashes query — it is
  skipped or pushed to a sane end, and documented.
- A4: missing root is an empty store (no exception at construction).
- A5: `ruff check src/`, `mypy src/`, and `tests/unit/test_report_store.py`
  all pass; no regression in the existing `store/` suite.

---

## C4 — "Path-of-RPG / FLORA" (needs your decision)

### What I found

I searched the entire repo (docs, scripts, harness, source, graphify output)
for `path-of-rpg`, `FLORA`, and likely variants. There is **no definition** of
either codename in this codebase. The only near-matches were false positives
("path of the JSONL file").

### Most reasonable interpretation (my proposal)

Given this item sits at the end of a **reliability/observability** hardening
plan, the most defensible reading is:

- **"Path-of-RPG"** = a **task journey / lifecycle traceability** view — "the
  path a task takes as it travels through the system" (assigned → claimed →
  in-progress → completed / failed / escalated / dead-lettered). Visualise a
  single task's full arc across the queue, agent, approvals, and audit trail.
- **"FLORA"** (likely a product codename) = a **reports/outcome viewer** that
  surfaces the outputs agents produce (`results/*`), possibly on top of the C5
  `ReportStore`.

### Decisions I need from you (choose for each)

1. **Is "Path-of-RPG" a task-lifecycle traceability view?**
   - OPTION A — Yes: task journey timeline (assigned → … → final state)
     with audit-trace overlay. (Recommended, most consistent with the plan.)
   - OPTION B — No, it means something else (give me the plan/spec you meant).

2. **Is "FLORA" a reports/outcomes viewer?**
   - OPTION A — Yes: a "Reports" tab/page that lists agent-produced reports
     (built on C5's `ReportStore`). (Recommended.)
   - OPTION B — No, different meaning (point me at the intended spec).

3. **Scope for C4 dashboard UI** — which page/tab to add:
   - OPTION A — a read-only "Task Flow" page (task lifecycle) only.
   - OPTION B — a "Task Flow" page **and** a "Reports" page (both).
   - OPTION C — backend/API only, no UI this pass.

4. **Ordering** — build C5 (`ReportStore`) first and layer C4 on it (recommended),
   or C4 UI-first with mocked data?

> If you reply "OPTION A / A / B / C5-first" (the recommended set), I will
> proceed to write the full ECL plan + tasks and implement. If any answer is
> "give me the plan you meant" or "B — different meaning", **stop and paste the
> intended spec** before I write any code.

---

## Suggested C4 scope (if you pick the recommended set)

### Problem
The dashboard shows live snapshots but no way to **follow a single task's full
journey** or **open the actual report an agent produced** for a completed task.

### Goal
- **Task Flow view** — select a task ID → see its lifecycle timeline
  (created → claimed → in-progress → completed/failed/escalated/dead-letter),
  with timestamps and the audit events that touch it (leverages the C1 hash-chained
  audit trail).
- **Reports view** — list agent-produced reports under `results/`, newest-first,
  filterable, backed by C5's `ReportStore` (`latest(n)`/`oldest(n)` + filters).

### Non-goals (C4)
- No editing/mutation of tasks or reports from these views.
- No new persistence format.

### Acceptance criteria (C4 skeleton — refine with you)
- B1: `/task/<id>` (or a slide-out) shows the task's status transitions in order.
- B2: Reports page lists real `results/*` reports, newest-first, with open/download.
- B3: `ruff check src/`, `mypy src/`, and the targeted dashboard/store suites pass.

---

## How I will sequence (pending your answers)

1. Implement + test **C5 `ReportStore`** (small, self-contained).
2. Implement the **C4 UI/API** you pick, consuming C5.
3. Gate: `ruff check src/` + `mypy src/` + targeted `pytest` + smoke-test the new pages/commands.
4. Do NOT commit until you say so (consistent with the whole hardening effort).

---

## Open questions (blocking)

- C4 #1, #2, #3, #4 (above) — I need your choices.
- Confirm C5 scope is as written.

_Once you approve, I'll convert this into the ECL `spec.md`/`plan.md`/`tasks.md` and implement._
