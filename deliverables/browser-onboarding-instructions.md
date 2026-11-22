# Browser-Assisted Job Discovery Onboarding Instructions

## Overview

This document provides the complete onboarding instructions for browser-assisted job discovery using OpenCode Browser. The workflow enables supervised discovery sessions across LinkedIn and Malawi/development job sources, with captured job postings saved locally following existing Career project import conventions.

## Workflow Architecture

### Human-Directed Browser Workflow

- **OpenCode Browser** initiates and controls sessions
- **User** handles authentication and MFA manually
- **Captured job postings** are saved locally following existing Career project import conventions
- Workflow operates in **supervised sessions** with clear handoff points between:
  - Browser navigation
  - Local capture
  - Import pipeline integration

### Discovery Session Flow

1. **Profile Selection**: Choose a search profile tailored to specific job boards or regions
2. **Browser Navigation**: OpenCode Browser navigates to the target source
3. **Manual Authentication**: User logs in and completes MFA as needed
4. **Job Discovery**: Browse and identify relevant job postings
5. **Local Capture**: Save job details (title, description, company, location, etc.)
6. **Import Pipeline**: Integrate captured data into the existing Career import workflow
7. **Session Close**: Document findings and note any issues

## Search Profiles

Each search profile is a reusable configuration defining:

- Target job source/board
- Search keywords and filters
- Pagination strategy
- Data fields to capture
- Export format

See `deliverables/search-profiles.md` for the 5 reusable search profiles.

## Supported Sources

The following sources are supported for browser-assisted discovery:

| Source | Type | Notes |
|--------|------|-------|
| LinkedIn | Professional networking site | Manual browser discovery; requires user login |
| CareerAd Malawi | Malawi-specific job board | Local development job source |
| Aganyu | Development job platform | |
| Job Centre Malawi | Malawi government job portal | |
| ReliefWeb | Humanitarian job listings | |
| Devex | Development industry jobs | |
| UN Careers | United Nations jobs | |
| UNDP Careers | UNDP-specific jobs | |
| Impactpool | International development jobs | |
| UNjobs | UN jobs aggregator | |
| African Development Bank | AfDB jobs | |
| World Bank | World Bank jobs | |
| AfricaWork | Africa-focused job board | |

See `deliverables/source-procedures.md` for procedures for all 13 sources.

## Unsupported/Inaccessible Sources

See `deliverables/unsupported-sources.md` for sources that could not be automated or accessed.

## Import Results Report

See `deliverables/import-results-report.md` for the operational demonstration import report.

## Screenshots and Logs

See `deliverables/screenshots/` directory for screenshots and logs from the demonstration.

---

**Last Updated**: 2026-11-20
**Session**: Browser-Assisted Job Discovery Onboarding