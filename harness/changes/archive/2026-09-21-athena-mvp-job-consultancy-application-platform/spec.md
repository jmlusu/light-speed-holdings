# Spec

## Intake Review

- Intake type: **Structured Change**
- Input shape: **mixed** (plan-first implementation, now formalizing through ECL)
- Questions asked this round: 2
  1. What is the scope of "complete" for an MVP? (Answer: Job scraping, profile matching, ATS scoring, application tracking, document generation)
  2. Should automation (auto-apply) be included in MVP or post-MVP? (Answer: MVP - core scoring/tracking is MVP, auto-apply is phase 2)

## Goal And Evidence

- **Real problem or user request**: Jack needs an automated system to find consultancy and job opportunities across Malawi (Lilongwe), remote boards, and consultancy firms; score his profile against each role; track applications through the pipeline; and generate tailored cover letters — reducing manual effort from hours per application to minutes.

- **Current behavior**: Manual job search across 5+ websites, manual resume tailoring per application, spreadsheet tracking of applications, no systematic scoring.

- **Source of evidence**: Direct user request; existing manual workflow documented in personal notes; competitor analysis of tools like Simplify, LinkedIn Easy Apply.

## User Scenarios And Success

### Primary User Scenario
Jack creates a profile once, then Athena daily scrapes job boards, ranks opportunities by fit score, surfaces top matches, and generates application documents. Jack reviews, applies, and tracks status in the pipeline.

### Secondary User Scenario: Client Proposal Deliverables (Consulting)
Beyond applications, Athena's document generation and local artifact store are used to produce client consulting deliverables: scoping briefs, proposal documents and slide decks, executive summaries, and audit checklists (for example the VillageReach USSD proposal and the solo-consultant proposal set). All deliverable artifacts are consolidated under `proposal-deliverables/` so each proposal is a repeatable, versioned output rather than a manual one-off build.

### Success Criteria
1. **Scraping**: Can pull jobs from at least 3 sources (Remote, Lilongwe, Consultancy) with title, company, location, description, requirements, salary, application URL
2. **Profile**: Can store user profile with headline, summary, skills, experience, education, certifications
3. **Matching**: Can compute match score (0-100) between profile and job using keyword + semantic similarity
4. **ATS Scoring**: Can score resume against job on keyword match, semantic similarity, experience relevance, education match
5. **Application Tracking**: Can track jobs through pipeline stages (new → fetched → matched → scored → applied → interview → offer)
6. **Document Gen**: Can generate cover letter from template with job-specific customization
7. **Dashboard**: Can view pipeline, stats, and individual job details via web UI

### Acceptance Criteria
- [ ] API endpoints functional: /jobs, /profiles, /applications, /scrape, /match, /score, /stats/*
- [ ] All scrapers return valid Job objects with required fields
- [ ] Matching engine returns scores 0-100 with tier labels (Excellent/Good/Fair/Poor)
- [ ] ATS scorer provides breakdown: keyword, semantic, experience, education, overall
- [ ] Frontend routes added: /athena, /athena/jobs, /athena/applications
- [ ] Tests exist for core modules (store, matching, scoring, API)
- [ ] Lint + typecheck pass: ruff check src/, mypy src/
- [ ] Full pytest suite passes

## Non-Goals

- **Auto-apply automation**: Browser-based form filling and submitter are built but marked as Phase 2 (not in MVP scope)
- **Email integration**: Sending applications via email is out of scope
- **Multi-user support**: Single-user (Jack) profile assumed
- **Social job boards**: LinkedIn, Indeed parsing beyond what's currently implemented
- **Interview scheduling**: Pipeline stops at "offer" — no calendar integration

## Constraints

- **Data storage**: JSONL file-based store with file locking (no external DB required for MVP)
- **No external APIs for embeddings**: Uses sentence-transformers locally; falls back to keyword matching if unavailable
- **Rate limiting**: Scrapers respect 1-second delays between requests
- **Playwright for JS-rendered pages**: Some job boards require browser automation

## Assumptions

- Single-user MVP (Jack as user)
- Local file storage sufficient (company/athena/*.jsonl)
- sentence-transformers model will fit in local environment
- Job board structures won't change frequently (scraper maintainability)

## Open Questions

- [RESOLVED] Should auto-apply be MVP? → **No, Phase 2**
- [RESOLVED] Multi-user support needed? → **No, single-user MVP**
- **Remaining**: What is the acceptable scrape frequency without triggering rate limits/blocks on major job boards?

## Resolved Clarifications

- 2026-09-20: Scope confirmed as MVP (scraping + matching + ATS + tracking + docs) — auto-apply deferred to Phase 2
