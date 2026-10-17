**Repository Outstanding Tasks Audit**

Perform a **repository-wide audit of all outstanding, incomplete, blocked, deferred, or unresolved work**.

### Objective
Determine **what remains to be done, its current status, and why it is still open**. Do not modify code or start implementing tasks. This is an **audit and status-reporting task only**.

### Instructions

1. **Read the repository's governing documentation first**, including applicable:
   - `AGENTS.md`
   - `DIRECTIVE.md`
   - architecture/specification documents
   - task/backlog documents
   - roadmap/planning documents
   - audit and verification reports
   - relevant README files
   - CI/CD documentation
   - agent/team instructions

2. **Search the entire repository** for evidence of outstanding work, including:
   - TODO / FIXME / XXX / HACK / WIP
   - incomplete implementations
   - placeholder/stub code
   - commented-out functionality
   - deferred work
   - known bugs
   - failing or skipped tests
   - failing CI checks
   - open validation gaps
   - incomplete migrations
   - temporary workarounds
   - architectural deviations
   - partially completed features
   - unfinished documentation
   - unresolved audit findings
   - "follow-up", "next step", "remaining", "pending", "blocked", "deferred", and similar language
   - task lists and checkboxes
   - references to branches, PRs, commits, or issues that indicate unfinished work

3. **Inspect Git state and history** to identify outstanding work:
   - current branch
   - working-tree changes
   - untracked files
   - recent commits
   - commit messages indicating unfinished work
   - branches containing unfinished work
   - merge/rebase state
   - recent implementation commits and their follow-up requirements

4. **Inspect CI/test status and repository validation evidence** where available.
   Identify:
   - current failures
   - flaky/skipped checks
   - unresolved warnings that represent real work
   - tests that were expected but not implemented
   - verification steps that remain outstanding.

5. **Reconcile conflicting sources.**
   Do not treat every TODO or old document as an active task.
   
   For every candidate task, determine whether it is:
   - **OPEN** — still genuinely outstanding
   - **IN PROGRESS** — actively being worked on
   - **BLOCKED** — cannot proceed without a dependency/decision
   - **DEFERRED** — intentionally postponed
   - **SUPERSEDED** — replaced by newer work
   - **STALE** — historical reference that is no longer applicable
   - **COMPLETED** — already resolved despite outdated documentation

6. **Trace each active task to evidence.**
   For every OPEN, IN PROGRESS, BLOCKED, or DEFERRED item, identify:
   - task description
   - source/document/file
   - relevant file(s)
   - current status
   - evidence supporting the status
   - why it remains open
   - dependency/blocker, if any
   - what must happen to close it
   - priority/urgency
   - whether it appears duplicated elsewhere.

7. **Do not create work merely because something looks imperfect.**
   Only classify something as outstanding when there is evidence that it was intended, required, reported, or committed to.

8. **Do not implement, refactor, clean up, or otherwise change the repository.**
   This task is strictly **discovery, reconciliation, and reporting**.

### Required CEO-Friendly Output

Produce the report in this structure:

## 1. Executive Summary
Maximum **150 words**:
- total genuinely outstanding items
- critical/high-priority items
- blocked items
- major themes
- overall repository completion/status assessment.

## 2. Outstanding Tasks

| # | Task | Status | Priority | Why Still Open | Blocker/Dependency | Evidence | Closure Criteria |
|---|---|---|---|---|---|---|---|

Rank by **business/technical importance**, not by discovery order.

## 3. Critical / Immediate Attention
List only tasks that could:
- block release/deployment
- cause broken functionality
- create architectural inconsistency
- fail required validation/CI
- create significant technical debt
- contradict an explicit repository directive/specification.

For each, explain the issue in plain CEO language.

## 4. Blocked / Waiting
List every blocked or dependency-dependent task and explain:
- what is blocking it
- who/what must resolve the blocker
- whether the blocker is technical, informational, architectural, approval-related, or external.

## 5. Deferred / Intentionally Postponed
Separate deliberately deferred work from genuinely forgotten work.

## 6. Stale / Superseded / Already Completed
Identify apparent outstanding tasks that **should NOT remain on the active backlog**, with evidence explaining why.

## 7. Duplicate / Related Tasks
Identify tasks that are actually the same work or should be consolidated.

## 8. Recommended Closure Order
Provide a concise sequence of the **next 5–10 highest-value actions**, based on dependencies and risk.

Do not invent tasks.

## 9. Audit Coverage
State:
- repositories/directories inspected
- key documentation inspected
- task sources inspected
- Git state inspected
- CI/test evidence inspected
- limitations or sources that could not be verified.

### Final Rule

**Do not simply report everything containing the word TODO. Reconstruct the repository's actual outstanding-work picture by reconciling documentation, implementation, Git history, tests, CI, and current repository state.**

The final report must clearly answer:

> **"What is still unfinished, what is its current status, and why has it not been closed?"**