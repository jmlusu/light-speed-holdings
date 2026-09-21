# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation. (Completed: spec.md and plan.md populated with Athena MVP scope)

## Implementation

### Frontend Routing (Critical Path)
- [ ] T010 Add Athena routes to `src/App.tsx` — /athena, /athena/jobs, /athena/applications, /athena/analytics, /athena/settings. Verify with: `npm run build` passes.

### Test Coverage
- [ ] T020 Create `tests/unit/test_athena_store.py` — test AthenaDB CRUD, JSONL persistence, file locking. Verify with: `pytest tests/unit/test_athena_store.py -v`
- [ ] T021 Create `tests/unit/test_athena_matching.py` — test matching engine score computation, keyword fallback, tier assignment. Verify with: `pytest tests/unit/test_athena_matching.py -v`
- [ ] T022 Create `tests/unit/test_athena_scorer.py` — test ATS scorer breakdown, overall score, auto-apply/flag thresholds. Verify with: `pytest tests/unit/test_athena_scorer.py -v`
- [ ] T023 Create `tests/unit/test_athena_api.py` — test API endpoints via FastAPI TestClient. Verify with: `pytest tests/unit/test_athena_api.py -v`

### Verification / Validation
- [ ] T030 Run linter on athena module: `ruff check src/ai_company/athena/` — Fix any issues.
- [ ] T031 Run type checker on athena module: `mypy src/ai_company/athena/` — Fix any type errors.
- [ ] T032 Run full pytest suite: `pytest tests/unit/ -v` — Ensure no regressions.
- [ ] T033 Run frontend build: `npm run build` — Confirm TypeScript compiles.

### Integration Smoke Test
- [ ] T040 Start dashboard server: `uv run uvicorn ai_company.dashboard:app --reload` (in background)
- [ ] T041 Create test profile via API: `curl -X POST http://localhost:8000/api/v1/athena/profiles -H "Content-Type: application/json" -d '{"email":"test@example.com","headline":"Software Engineer","summary":" experienced","skills":[{"name":"Python"}]}'`
- [ ] T042 Trigger scrape via API: `curl -X POST http://localhost:8000/api/v1/athena/scrape -H "Content-Type: application/json" -d '{"query":"software engineer","location":"remote","max_results":5}'`
- [ ] T043 Verify jobs in store: `curl http://localhost:8000/api/v1/athena/jobs | jq`
- [ ] T044 Run matching: `curl -X POST http://localhost:8000/api/v1/athena/match -H "Content-Type: application/json" -d '{"profile_id":"<id>","top_k":5}' | jq`
- [ ] T045 Check pipeline stats: `curl http://localhost:8000/api/v1/athena/stats/pipeline | jq`
- [ ] T046 Stop dashboard server.

### Cleanup & Commit
- [ ] T050 Verify all staged files for commit: `git status --short` — Ensure only Athena-relevant files included.
- [ ] T051 Commit Athena change: `git commit -m "feat(athena): MVP job & consultancy application platform

- Job scraping from Remote, Lilongwe, Consultancy boards
- Profile management with skills, experience, education
- Semantic + keyword matching engine with ATS scoring
- Application pipeline tracking (new → offer)
- Document generation (cover letter, resume)
- React dashboard with pipeline kanban, ATS gauges

Closes #XXX"` (Reference issue number)
- [ ] T052 Run post-commit: `.\scripts\lint-ecl.ps1` — Confirm ECL consistency.

## Deferred Tasks

- T100 [P] Implement auto-apply browser automation (Phase 2) — form_filler.py, submitter.py exist but not wired
- T101 [P] Add multi-user support (out of MVP scope)
- T102 [P] Integrate email sending for applications (out of MVP scope)
