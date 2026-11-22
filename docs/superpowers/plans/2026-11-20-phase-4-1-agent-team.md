# Phase 4.1 Agent Team — Browser-Assisted Job Discovery Onboarding

**Delivery Lead:** `chief_of_staff` (human-directed orchestration in this session)
**Execution model:** subagent-driven development — one fresh implementer per task, one fresh reviewer per task, whole-branch review at the end.

## Roster

| Phase role | Company agent (registry id) | Responsibility |
|---|---|---|
| Orchestrator / Delivery Lead | `chief_of_staff` | Sequences tasks, enforces gates, owns handoffs |
| Implementer — Onboarding docs | `technical_documentation_lead` | Tasks 1, 4, 7 |
| Implementer — Search profiles | `data_engineer` | Task 2 |
| Implementer — Source registry | `integration_engineer` | Task 3 |
| Implementer — Capture workflow | `senior_backend_engineer` | Task 5 |
| Implementer — Demonstration verification | `test_engineering_lead` | Task 6 |
| Implementer — Scope verification | `security_compliance_lead` | Task 8 |
| Reviewer — every task | `qa_lead` | Independent acceptance review |
| Reviewer — docs lens | `technical_documentation_lead` | Clarity/completeness on doc tasks |
| Whole-branch reviewer | `vp_engineering` | Integration, consistency, final verdict |
| Whole-branch reviewer | `qa_lead` | Regression, test integrity, final verdict |

## Dispatch Protocol

Because the runtime exposes only the built-in `general`/`explore` subagent types, each dispatch is a fresh `general` subagent primed with the company agent's mission, responsibilities, and operating guidelines. The role card in `.opencode/agents/<id>.md` is the source of truth for the prompt preamble.

### Per task

1. **Implementer** (fresh subagent): receives the task brief, repo constraints, acceptance criteria, and file list. Writes test first, then implementation; runs the test; reports files + command output + deviations. No git operations.
2. **Reviewer** (fresh subagent, different prompt): re-runs the test, inspects the diff/files, checks the task's acceptance criteria and the global constraints, and returns `APPROVE` or `REJECT` with findings. Rejects return to a *fresh* implementer run with the findings.
3. **Gate**: only an approved task unlocks the next task.

### Whole-branch

`vp_engineering` + `qa_lead` lens: run the full `pipeline/tests` suite, verify cross-task imports and names, scan for placeholders/secrets/personal data, confirm all 8 tasks are covered, and issue a final verdict.

## Guardrails Carried Into Every Dispatch

- Do not overwrite prior-session artifacts in `deliverables/` and `demonstration/`.
- Do not commit, push, or open PRs.
- Do not bypass CAPTCHA/auth/anti-bot controls.
- No automated LinkedIn fetching; manual browser discovery only.
- No resume edits, application submissions, external communications, or Notion writes.
- PowerShell-compatible commands; run tests with `.venv\Scripts\python.exe -m pytest`.
- Report honestly: "local only" unless verified; no fabricated evidence.

## Task → Agent Matrix

| Task | Implementer | Reviewer |
|---|---|---|
| 1. Browser onboarding instructions | `technical_documentation_lead` | `qa_lead` + docs lens |
| 2. Search profiles | `data_engineer` | `qa_lead` |
| 3. Source registry | `integration_engineer` | `qa_lead` |
| 4. Browser operating procedure | `technical_documentation_lead` | `qa_lead` + docs lens |
| 5. Local capture workflow | `senior_backend_engineer` | `qa_lead` |
| 6. Operational demonstration | `test_engineering_lead` | `qa_lead` |
| 7. Deliverables verification | `technical_documentation_lead` | `qa_lead` + docs lens |
| 8. Scope verification | `security_compliance_lead` | `qa_lead` |
| Whole-branch | — | `vp_engineering` + `qa_lead` |
