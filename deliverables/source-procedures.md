# Source Procedures - Browser-Assisted Job Discovery

## Overview

Procedures for capturing job postings from 13 supported sources using browser-assisted discovery. Each procedure documents the browser workflow, data fields to capture, and import considerations.

---

## 1. LinkedIn

**Source Type**: Professional networking site, job board
**Access**: Requires user login; MFA may be required

### Browser Workflow

1. Navigate to `https://www.linkedin.com/jobs/search/`
2. Accept cookies banner if present
3. Log in if prompted (user handles authentication)
4. Apply location filter: "Malawi" or "Remote"
5. Set experience level filter as needed
6. Filter by function or industry as relevant
7. Scroll to load more results (infinite scroll or pagination)
8. For each job card in view:
   - Hover/click to expand if collapsed
   - Extract: job title, company name, location, posting date
   - Click into job detail page
   - Extract: full job description, apply link, seniority level
   - Open apply link in new tab to verify
9. Capture full results page screenshot
10. Close detail tabs, proceed to next result batch

### Data Fields Captured

| Field | Required | Format |
|-------|----------|--------|
| title | Yes | String |
| company | Yes | String |
| location | Yes | String (city, country) |
| date_posted | Yes | ISO 8601 or relative |
| description | Yes | Text |
| apply_url | Yes | URL |
| seniority | No | String (e.g., "Executive", "Manager", "Entry") |
| function | No | String (e.g., "Engineering", "Marketing") |
| keywords | No | Array of strings |

### Import Notes

- LinkedIn job URLs may contain tracking parameters; strip to canonical apply URL
- Seniority levels vary; normalize to consistent taxonomy if possible
- May encounter duplicate postings; dedupe by title+company+location+date

### Screenshot Markers

- `linkedin_search_results.png` - Search results page
- `linkedin_job_detail.png` - Individual job detail page

---

## 2. CareerAd Malawi

**Source Type**: Malawi-specific job board, development focus
**Access**: Generally open; may require registration

### Browser Workflow

1. Navigate to `https://careerad.mw/jobs` (or applicable URL)
2. Accept cookies/banner if present
3. Set location filter: "All Malawi" or specific district (Lilongwe, Blantyre, etc.)
4. Filter by sector if available: "NGO", "Government", "International"
5. Apply keyword filter: "malawi", "development", "project"
6. Paginate through results or load more
7. For each job listing:
   - Click into job detail
   - Extract: title, organization, district/region, position level
   - Extract: sector, employment type, salary range if listed
   - Extract: application deadline
8. Capture results page screenshot
9. Close detail tabs, proceed

### Data Fields Captured

| Field | Required | Format |
|-------|----------|--------|
| title | Yes | String |
| organization | Yes | String |
| district | Yes | String (Malawi district) |
| level | Yes | String (Officer, Manager, Consultant, etc.) |
| sector | Yes | String (NGO, Government, International, Private) |
| employment_type | No | String (Full-time, Contract, Volunteer) |
| salary | No | String or number |
| deadline | No | ISO 8601 or text |
| source | Yes | String ("careerad-malawi") |

### Import Notes

- District names should match Malawi geographic standard
- Sector field is critical for Malawi job categorization
- Deadline formats vary; parse ISO if possible, store text otherwise

### Screenshot Markers

- `careerad_search.png` - Search results page
- `careerad_job_detail.png` - Individual job detail

---

## 3. Aganyu

**Source Type**: Development job platform (system name)
**Access**: Varies; may require API key or user account

### Browser Workflow

1. Navigate to Aganyu job platform URL
2. Accept cookies/banner
3. If login required, user handles authentication manually
4. Apply filters: location (Malawi), sector, job type
5. Search with keywords relevant to Malawi development
6. Paginate or scroll to load results
7. For each job:
   - Click into detail view
   - Extract: title, organization, job level, sector
   - Extract: posting date, application deadline
   - Capture any salary or benefit info if displayed
8. Capture results page screenshot
9. Close and proceed

### Data Fields Captured

| Field | Required | Format |
|-------|----------|--------|
| title | Yes | String |
| organization | Yes | String |
| level | Yes | String |
| sector | Yes | String |
| date_posted | Yes | ISO 8601 |
| deadline | No | ISO 8601 or text |
| salary | No | String or number |
| source | Yes | String ("aganyu") |

### Import Notes

- Aganyu may have unique field naming; map to standard taxonomy
- Level field should align with internal level system

### Screenshot Markers

- `aganyu_search.png` - Search results
- `aganyu_job_detail.png` - Job detail

---

## 4. Job Centre Malawi

**Source Type**: Malawi government job portal
**Access**: Open access; government-run

### Browser Workflow

1. Navigate to Malawi Job Centre URL (e.g., `https://jobcentre.mw` or similar)
2. Accept cookies/banner
3. Browse categories or use search
4. Filter by: job type, location, ministry/department
5. Apply keyword filter if search box available
6. List results; each listing may have summary detail
7. Click into individual job for full details
8. Extract: title, ministry, location, requirements
9. Capture application instructions/deadline
10. Capture results page screenshot
11. Close and proceed to next

### Data Fields Captured

| Field | Required | Format |
|-------|----------|--------|
| title | Yes | String |
| ministry | Yes | String (Malawian government ministry) |
| location | Yes | String |
| requirements | No | Text |
| deadline | No | ISO 8601 or text |
| job_type | No | String |
| source | Yes | String ("jobcentre-malawi") |

### Import Notes

- Government job portals often have rigid formats; extract as-is
- Ministry names should be preserved exactly for categorization
- Application instructions may be in format beyond simple deadline

### Screenshot Markers

- `jobcentre_search.png` - Search results
- `jobcentre_job_detail.png` - Job detail

---

## 5. ReliefWeb

**Source Type**: Humanitarian job listings, UN/NGO focused
**Access**: Generally open; may have newsletter signup

### Browser Workflow

1. Navigate to `https://reliefweb.int/jobs` or applicable URL
2. Accept cookies/banner
3. Filter by: sector, region, job type
4. Set region: "Malawi" or "Southern Africa"
5. Apply keyword filter: "humanitarian", "development", "emergency"
6. Load results; may use infinite scroll
7. For each job:
   - Click into detail
   - Extract: title, organization, sector, duty station
   - Extract: contract type, duration, salary range if listed
   - Extract: closing date, application instructions
8. Capture results page screenshot
9. Close detail tab, proceed

### Data Fields Captured

| Field | Required | Format |
|-------|----------|--------|
| title | Yes | String |
| organization | Yes | String |
| sector | Yes | String (Humanitarian / Development / Emergency) |
| duty_station | Yes | String |
| contract_type | No | String |
| duration | No | String |
| salary | No | String or number |
| closing_date | No | ISO 8601 or text |
| source | Yes | String ("reliefweb") |

### Import Notes

- ReliefWeb sectors are well-defined; use consistent values
- Duty station should include city/country

### Screenshot Markers

- `reliefweb_search.png` - Results page
- `reliefweb_job_detail.png` - Job detail

---

## 6. Devex

**Source Type**: Development industry jobs, donor-funded roles
**Access**: May require free account registration

### Browser Workflow

1. Navigate to `https://www.devex.com/jobs` or applicable URL
2. Accept cookies/banner
3. If login dialog, user handles manually; may skip for public listings
4. Filter by: sector, region, job function
5. Set region: "Malawi" or "Africa"
6. Apply keyword filter: "project manager", "officer", "consultant"
7. Load results; Devex uses pagination
8. For each job:
   - Click into job detail
   - Extract: title, organization, donor, sector
   - Extract: job level, contract type
   - Extract: location, posting date, application deadline
9. Capture results page screenshot
10. Close and proceed

### Data Fields Captured

| Field | Required | Format |
|-------|----------|--------|
| title | Yes | String |
| organization | Yes | String |
| donor | Yes | String (or "Unknown") |
| sector | Yes | String |
| level | Yes | String |
| contract_type | No | String |
| location | Yes | String |
| date_posted | Yes | ISO 8601 |
| deadline | No | ISO 8601 |
| source | Yes | String ("devex") |

### Import Notes

- Devex often lists donor name separately; capture as organization/donor
- Level field maps to internal taxonomy

### Screenshot Markers

- `devex_search.png` - Results page
- `devex_job_detail.png` - Job detail

---

## 7. UN Careers

**Source Type**: United Nations job board
**Access**: Requires user account; MFA common

### Browser Workflow

1. Navigate to `https://careers.un.org/` or applicable URL
2. Accept cookies/banner
3. Log in if prompted (user handles authentication and MFA)
4. Filter by: duty station, business unit, level
5. Set duty station: "Malawi" or regional offices
6. Apply level filter as needed (P-1, P-2, etc.)
7. Search with keywords: "malawi", "development"
8. Load results; UN uses standard job card format
9. For each job:
   - Click into job detail
   - Extract: title, duty station, level, contract type
   - Extract: closing date, job number, organization
10. Capture results page screenshot
11. Close detail tab, proceed

### Data Fields Captured

| Field | Required | Format |
|-------|----------|--------|
| title | Yes | String |
| organization | Yes | String (usually "United Nations") |
| duty_station | Yes | String |
| level | Yes | String (P-1, P-2, D-1, D-2, etc.) |
| contract_type | Yes | String (Fixed-term, Temporary, etc.) |
| closing_date | Yes | ISO 8601 |
| job_number | Yes | String (UN job reference) |
| source | Yes | String ("un-careers") |

### Import Notes

- UN job numbers are unique identifiers; preserve exactly
- Level and contract_type must match UN standardized values

### Screenshot Markers

- `uncareers_search.png` - Results page
- `uncareers_job_detail.png` - Job detail

---

## 8. UNDP Careers

**Source Type**: UNDP-specific job board
**Access**: Requires user account; MFA possible

### Browser Workflow

1. Navigate to `https://www.undp.org/careers` or applicable URL
2. Accept cookies/banner
3. Log in if prompted (user handles authentication and MFA)
4. Filter by: country, region, job function, level
5. Set country: "Malawi"
6. Apply function filter: "Project Management", "Operations", etc.
7. Set level as needed
8. Search; UNDP results have standard format
9. For each job:
   - Click into detail
   - Extract: title, job level, contract type
   - Extract: duty station, closing date, salary range if listed
   - Extract: job ID/referencenumber
10. Capture results page screenshot
11. Close and proceed

### Data Fields Captured

| Field | Required | Format |
|-------|----------|--------|
| title | Yes | String |
| organization | Yes | String (usually "UNDP") |
| duty_station | Yes | String |
| level | Yes | String |
| contract_type | Yes | String |
| job_id | Yes | String |
| closing_date | Yes | ISO 8601 |
| salary | No | String or number |
| source | Yes | String ("undp-careers") |

### Import Notes

- UNDP job IDs are unique; preserve exactly
- Salary field may be ranges or "competitive"; store as text

### Screenshot Markers

- `undp_search.png` - Results page
- `undp_job_detail.png` - Job detail

---

## 9. Impactpool

**Source Type**: International development job board, membership-based
**Access**: May require free account; some listings public

### Browser Workflow

1. Navigate to `https://impactpool.org/jobs/` or applicable URL
2. Accept cookies/banner
3. If login required, user handles; may browse public listings
4. Filter by: region, sector, job type
5. Set region: "Africa", "Malawi" if available
6. Apply sector: "International Development", "Humanitarian"
7. Search with keywords: "malawi", "project officer"
8. Load results; Impactpool uses card-based layout
9. For each job:
   - Click into job detail
   - Extract: title, organization, sector
   - Extract: job type, contract duration
   - Extract: duty station, posting date, application deadline
10. Capture results page screenshot
11. Close and proceed

### Data Fields Captured

| Field | Required | Format |
|-------|----------|--------|
| title | Yes | String |
| organization | Yes | String |
| sector | Yes | String |
| job_type | Yes | String (Contract, Full-time, etc.) |
| duration | No | String |
| duty_station | Yes | String |
| date_posted | Yes | ISO 8601 |
| deadline | No | ISO 8601 |
| source | Yes | String ("impactpool") |

### Import Notes

- Impactpool may have membership-gated details; capture what's publicly visible
- Job type field is important for categorization

### Screenshot Markers

- `impactpool_search.png` - Results page
- `impactpool_job_detail.png` - Job detail

---

## 10. UNjobs

**Source Type**: UN jobs aggregator, UN and specialized agency jobs
**Access**: Generally open; some agency-specific gates

### Browser Workflow

1. Navigate to `https://unjobs.org/` or applicable URL
2. Accept cookies/banner
3. Filter by: duty station, organization, category
4. Set duty station: "Malawi" or "Africa"
5. Apply organization filter: "UNDP", "UNICEF", "WHO", etc. if desired
6. Search with keywords: "malawi", "development", "project"
7. Load results; UNjobs lists in standard format
8. For each job:
   - Click into job detail
   - Extract: title, organization, duty station
   - Extract: level, contract type, closing date
   - Extract: job reference number, applying instructions
9. Capture results page screenshot
10. Close and proceed

### Data Fields Captured

| Field | Required | Format |
|-------|----------|--------|
| title | Yes | String |
| organization | Yes | String |
| duty_station | Yes | String |
| level | Yes | String |
| contract_type | Yes | String |
| closing_date | Yes | ISO 8601 |
| job_ref | Yes | String (UNjobs reference number) |
| source | Yes | String ("unjobs") |

### Import Notes

- UNjobs reference numbers are unique identifiers
- Level/contract_type should use standardized values

### Screenshot Markers

- `unjobs_search.png` - Results page
- `unjobs_job_detail.png` - Job detail

---

## 11. African Development Bank

**Source Type**: African Development Bank job board
**Access**: Requires user account; may have executive recruitment separate

### Browser Workflow

1. Navigate to AfDB careers/jobs URL (e.g., `https://www.afdb.org/en/jobs`)
2. Accept cookies/banner
3. Log in if prompted (user handles authentication)
4. Filter by: department, level, country
5. Set country: "Malawi" or "Regional (Africa)"
6. Apply department filter: "Economics", "Finance", "Operations", etc.
7. Set level as appropriate
8. Search; AfDB has structured job listings
9. For each job:
   - Click into job detail
   - Extract: title, department, level, duty station
   - Extract: closing date, job reference number, salary range if listed
   - Extract: contract type
10. Capture results page screenshot
11. Close and proceed

### Data Fields Captured

| Field | Required | Format |
|-------|----------|--------|
| title | Yes | String |
| organization | Yes | String (usually "African Development Bank") |
| department | Yes | String |
| level | Yes | String |
| duty_station | Yes | String |
| closing_date | Yes | ISO 8601 |
| job_ref | Yes | String (AfDB reference) |
| contract_type | Yes | String |
| salary | No | String or number |
| source | Yes | String ("afdb") |

### Import Notes

- AfDB department field is critical for categorization
- Job reference numbers are unique; preserve exactly

### Screenshot Markers

- `afdb_search.png` - Results page
- `afdb_job_detail.png` - Job detail

---

## 12. World Bank

**Source Type**: World Bank job board, international development
**Access**: Requires user account; extensive filtering options

### Browser Workflow

1. Navigate to World Bank careers URL (e.g., `https://careers.worldbank.org/`)
2. Accept cookies/banner
3. Log in if prompted (user handles authentication, may have MFA)
4. Filter by: country, region, business unit, level
5. Set country: "Malawi" or "Africa region"
6. Apply business unit: "Finance and Private Sector", "Operations", etc.
7. Set level as appropriate (Analyst, Specialist, Senior, etc.)
8. Search with keywords: "malawi", "development"
9. Load results; World Bank uses paginated results
10. For each job:
    - Click into job detail
    - Extract: title, business unit, level, duty station
    - Extract: closing date, job ID, salary range
    - Extract: contract type, applying instructions
11. Capture results page screenshot
12. Close and proceed

### Data Fields Captured

| Field | Required | Format |
|-------|----------|--------|
| title | Yes | String |
| organization | Yes | String (usually "World Bank") |
| business_unit | Yes | String |
| level | Yes | String |
| duty_station | Yes | String |
| closing_date | Yes | ISO 8601 |
| job_id | Yes | String |
| contract_type | Yes | String |
| salary | No | String or number |
| source | Yes | String ("world-bank") |

### Import Notes

- World Bank job IDs are unique; preserve exactly
- Business unit field is critical for categorization

### Screenshot Markers

- `wb_search.png` - Results page
- `wb_job_detail.png` - Job detail

---

## 13. AfricaWork

**Source Type**: Africa-focused job board, development and private sector
**Access**: Generally open; may have limited filtering

### Browser Workflow

1. Navigate to `https://africawork.com/jobs/` or applicable URL
2. Accept cookies/banner
3. Browse categories or use search box
4. Filter by: country, sector, job type if available
5. Set country: "Malawi" if filter exists; otherwise search keywords
6. Apply keyword: "malawi", "development", "project"
7. Load results; AfricaWork may use infinite scroll
8. For each job:
   - Click into detail
   - Extract: title, organization, country, job type
   - Extract: level, sector if listed
   - Extract: application deadline, posting date
9. Capture results page screenshot
10. Close and proceed

### Data Fields Captured

| Field | Required | Format |
|-------|----------|--------|
| title | Yes | String |
| organization | Yes | String |
| country | Yes | String (e.g., "Malawi") |
| level | Yes | String |
| sector | Yes | String |
| date_posted | Yes | ISO 8601 |
| deadline | No | ISO 8601 or text |
| source | Yes | String ("africawork") |

### Import Notes

- Country field should use standard Malawi naming
- Sector field aids categorization in development context

### Screenshot Markers

- `africawork_search.png` - Results page
- `africawork_job_detail.png` - Job detail

---

## Cross-Source Procedure Notes

### Authentication & MFA

- All sources may require user login; the user handles authentication and MFA manually
- OpenCode Browser navigates to the URL; user provides credentials
- Some sources (UN systems, AfDB, World Bank) have robust MFA; account setup may be needed in advance

### Screenshot Discipline

- Capture results page screenshot after each search/filter step
- Capture job detail page screenshot for each extracted job
- Screenshot filenames follow convention: `{source}_{step}.png`
- Screenshots serve as audit trail and debugging aid

### Data Quality & Dedup

- Normalize field values where possible (levels, sectors, countries)
- Deduplicate by: title + organization + duty_station + date_posted + source
- Store raw text for fields with variable formatting
- Flag unusual or missing fields for review

### Import Pipeline Integration

- All profiles export in JSON lines format
- Data is integrated into the existing Career import workflow
- Import scripts map source-specific fields to the internal taxonomy
- Failed extractions are logged for manual review

---

**Last Updated**: 2026-11-20
**Session**: Browser-Assisted Job Discovery Onboarding
**Total Sources**: 13