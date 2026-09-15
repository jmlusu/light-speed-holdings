# Spec: Remove Dummy Tasks & Wire Real Organizational Data

## Context

The CEO Dashboard "Recent Tasks" widget shows dummy/test data (7 seeded test
tasks) and demo data (10 Acme Corp `proj-acme-chatbot` tasks). None of it
reflects real organizational activity. The dashboard must show only real task
data.

## Goals

1. Delete dummy/demo tasks from the primary SQLite store (`data/ai_company.db`).
2. Add a `ai-company dashboard cleanup` CLI command that removes demo/test
   tasks and reports the count removed.
3. Filter demo/test tasks out of the dashboard API at read time by default,
   with an `include_test=True` override for introspection.
4. Guard task creation points (CLI intake, specialists assignment, scheduler,
   onboarding) so demo/test data cannot be re-seeded in normal operation.

## Detection Contract (authoritative)

A task is demo/test data if and only if it matches one of these demonstrable
markers:

- task id contains `proj-acme-chatbot` (Acme Corp demo tasks), OR
- instruction contains `proj-acme-chatbot`, OR
- instruction starts with `Test ` (capital T, trailing space), OR
- task id starts with `test-` or `verify-` (lowercase).

Deliberately NOT a marker: the task receiver/agent name. Routing a task to the
real `test-agent` receiver is legitimate production behavior and must not mark
the task as dummy. The earlier over-broad receiver-name heuristic was removed
because it false-positived on the real `test-agent` and broke the integration
test suite.

## Non-Goals

- Do not block or alter real tasks routed to agents whose id starts with
  `test`.
- Do not change inbox.json fallback write behavior.
- Do not perform destructive cleanup automatically on startup or on a
  schedule; cleanup is an explicit operator command.

## Acceptance Criteria

- A1: `ai-company dashboard cleanup` removes all 7 test tasks and 10 Acme demo
  tasks and prints per-class counts.
- A2: `GET /api/v1/tasks` (default filter) shows neither test nor demo tasks;
  `?include_test=true` Restores them for diagnostics.
- A3: Scheduler, specialists assignment, client intake, and onboarding refuse
  to create tasks matching the detection contract.
- A4: `ruff check src/`, `mypy src/` (strict), and the unit test suite all
  pass; no regression in the real `test-agent` routing integration tests.
