# Plan

## Technical Approach

Athena is a job & consultancy application platform built as a self-contained module within the AI Company Builder. The architecture follows a layered pattern:

1. **Data Layer** (`src/ai_company/athena/store.py`, `models/`)
   - JSONL-based file store with file locking for persistence
   - Pydantic models for Jobs, Applications, UserProfiles, ScrapeJobs

2. **API Layer** (`src/ai_company/athena/api/routes.py`)
   - FastAPI router at `/api/v1/athena`
   - 20+ endpoints covering jobs, profiles, applications, scraping, matching, scoring, stats, scheduler

3. **Matching/Scoring Layer** (`src/ai_company/athena/matching/`, `ats/`)
   - Semantic matching using sentence-transformers embeddings (with keyword fallback)
   - ATS resume scoring with breakdown: keyword, semantic, experience, education

4. **Scraper Layer** (`src/ai_company/athena/scrapers/`)
   - Base scraper class with Playwright support for JS-rendered pages
   - Concrete scrapers: RemoteJobs, LilongweJobs, ConsultancyJobs
   - Registry pattern for multi-source scraping

5. **Document Layer** (`src/ai_company/athena/documents/`)
   - Cover letter and resume generation from templates
   - Document humanizer for AI detection evasion

6. **Automation Layer** (`src/ai_company/athena/automation/`)
   - Browser automation for form filling and submission (Phase 2)

7. **Scheduler Layer** (`src/ai_company/athena/scheduler/`)
   - APScheduler-based periodic scraping jobs

8. **Frontend Layer** (`src/pages/athena/`, `src/components/athena/`, `src/lib/athena/`)
   - React dashboard with pipeline kanban, ATS gauges, job cards, stats

## Impacted Modules And Files

### Core Athena Module
- `src/ai_company/athena/__init__.py` — module root, exports
- `src/ai_company/athena/models/` — Pydantic models (Job, UserProfile, Application, etc.)
- `src/ai_company/athena/store.py` — AthenaDB, AthenaStore
- `src/ai_company/athena/api/routes.py` — FastAPI routes
- `src/ai_company/athena/api/schemas.py` — request/response schemas
- `src/ai_company/athena/matching/engine.py` — semantic matching
- `src/ai_company/athena/matching/embeddings.py` — embedding model wrapper
- `src/ai_company/athena/ats/scorer.py` — ATS resume scoring
- `src/ai_company/athena/ats/keywords.py` — keyword extraction
- `src/ai_company/athena/scrapers/base.py` — scraper base class
- `src/ai_company/athena/scrapers/remote.py` — remote job scraper
- `src/ai_company/athena/scrapers/lilongwe.py` — Malawi Lilongwe scraper
- `src/ai_company/athena/scrapers/consultancy.py` — consultancy board scraper
- `src/ai_company/athena/documents/generator.py` — document generation
- `src/ai_company/athena/documents/humanizer.py` — AI humanizer
- `src/ai_company/athena/documents/parser.py` — document parsing
- `src/ai_company/athena/automation/browser.py` — Playwright wrapper
- `src/ai_company/athena/automation/form_filler.py` — form automation
- `src/ai_company/athena/automation/submitter.py` — submission automation
- `src/ai_company/athena/scheduler/jobs.py` — APScheduler jobs

### Frontend
- `src/pages/athena/Dashboard.tsx` — main dashboard
- `src/pages/athena/JobList.tsx` — job listing
- `src/pages/athena/JobDetail.tsx` — job detail view
- `src/pages/athena/DocumentEditor.tsx` — document editor
- `src/components/athena/*.tsx` — UI components (7 components)
- `src/lib/athena/api.ts` — API client
- `src/lib/athena/types.ts` — TypeScript types
- `src/lib/athena/utils.ts` — utilities

### Integration Points
- `src/ai_company/dashboard/api.py` — Athena router inclusion (line 56-57)
- `pyproject.toml` — new deps: sentence-transformers, apscheduler, playwright, pytest-playwright
- `company/athena/` — data directory (created at runtime)

### Tests (to be added)
- `tests/unit/test_athena_store.py`
- `tests/unit/test_athena_matching.py`
- `tests/unit/test_athena_scorer.py`
- `tests/unit/test_athena_api.py`

## Interfaces, Data, Permissions

### API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/athena/jobs` | Create job |
| GET | `/api/v1/athena/jobs` | List jobs (with filters) |
| GET | `/api/v1/athena/jobs/{id}` | Get job |
| PATCH | `/api/v1/athena/jobs/{id}` | Update job |
| DELETE | `/api/v1/athena/jobs/{id}` | Delete job |
| POST | `/api/v1/athena/profiles` | Create profile |
| GET | `/api/v1/athena/profiles` | List profiles |
| GET | `/api/v1/athena/profiles/{id}` | Get profile |
| PATCH | `/api/v1/athena/profiles/{id}` | Update profile |
| POST | `/api/v1/athena/applications` | Create application |
| GET | `/api/v1/athena/applications` | List applications |
| PATCH | `/api/v1/athena/applications/{id}` | Update application |
| POST | `/api/v1/athena/scrape` | Trigger scrape job |
| GET | `/api/v1/athena/scrape/history` | Scrape history |
| POST | `/api/v1/athena/match` | Match jobs to profile |
| GET | `/api/v1/athena/score/{job_id}/{profile_id}` | ATS score |
| GET | `/api/v1/athena/stats/pipeline` | Pipeline stats |
| GET | `/api/v1/athena/stats/scraping` | Scraping stats |
| POST | `/api/v1/athena/scheduler/start` | Start scheduler |
| POST | `/api/v1/athena/scheduler/stop` | Stop scheduler |
| GET | `/api/v1/athena/scheduler/status` | Scheduler status |

### Data Models
- **Job**: title, company, location, description, requirements, responsibilities, keywords, benefits, salary, job_type, source, status, ats_score, match_score, match_tier, application_url, scraped_at
- **UserProfile**: email, headline, summary, skills[], experience[], education[], certifications[], languages[], preferences
- **Application**: job_id, user_profile_id, status, submitted_at, confirmed_at, notes
- **ScrapeJob**: query, location, job_type, max_results, sources, status, jobs_found, jobs_new

### Permissions
- No authentication on MVP (single-user assumption)
- No authorization layer — all endpoints open
- Future: API key or session-based auth

## Spec Gaps Found From Planning

1. **Frontend routing**: Athena pages exist in `src/pages/athena/` but are NOT wired into `src/App.tsx` — the UI is inaccessible
2. **Test coverage**: Zero tests exist for Athena module
3. **Document templates**: Templates exist in `src/ai_company/athena/documents/templates/` but validation needed
4. **Data directory**: `company/athena/` not created in repository — runtime-created

## Risks And Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Job board structure changes break scrapers | Medium | High | Add scraper version pinning; log failures; alert on parsing errors |
| Embedding model loading fails | Low | Medium | Keyword fallback already implemented |
| JSONL file locking contention | Low | Low | Using filelock; single-user reduces contention |
| Rate limiting from job boards | Medium | Medium | 1-second delay between requests; configurable |
| Playwright browser issues in CI | Medium | Medium | Use headless; skip e2e in unit test gate |
| Large resume/description causes memory issues | Low | Low | Size limits in models; streaming for docs |

## Verification Plan

### Pre-commit / Local Validation
```bash
ruff check src/ai_company/athena/     # Lint
mypy src/ai_company/athena/           # Type check
pytest tests/unit/ -v                  # Unit tests
npm run build                          # Frontend build
npm run lint                           # Frontend lint
```

### Integration / Smoke Test
1. Start dashboard: `uv run uvicorn ai_company.dashboard:app --reload`
2. Create profile: `POST /api/v1/athena/profiles` with {email, headline, summary, skills}
3. Trigger scrape: `POST /api/v1/athena/scrape` with {query: "software engineer", location: "remote"}
4. Get matches: `POST /api/v1/athena/match` with {profile_id, top_k: 10}
5. Get ATS score: `GET /api/v1/athena/score/{job_id}/{profile_id}`
6. Check stats: `GET /api/v1/athena/stats/pipeline`

### Frontend Validation
1. `npm run dev` to start frontend
2. Navigate to `/athena` (after adding route)
3. Verify dashboard loads, pipeline displays, job cards render
4. Trigger a scrape from UI, verify jobs appear
5. Test matching workflow end-to-end
