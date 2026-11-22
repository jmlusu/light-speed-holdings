# Search Profiles - Browser-Assisted Job Discovery

## Overview

Five reusable search profiles for browser-assisted job discovery across different job boards and regions. Each profile is designed to be parameterized and run within the OpenCode Browser framework.

---

## Profile 1: LinkedIn Executive Search

**Source**: LinkedIn Jobs
**Target Role**: Executive/Leadership positions
**Keywords**: `chief executive officer, ceo, vice president, vice director, director level, head of`

### Search Parameters

- **Location Filter**: Malawi, Southern Africa, Remote
- **Experience Level**: 10+ years
- **Function**: Executive Management
- **Keywords**: `leadership, strategy, operations, growth, transformation`

### Browser Workflow

1. Navigate to `https://www.linkedin.com/jobs/search/`
2. Apply location filter: Malawi / Remote
3. Set experience level to "10+ years"
4. Filter by function: "Executive Management"
5. Save results page screenshot
6. Extract job cards with the following fields:
   - Job title
   - Company name
   - Location
   - Posting date
   - Job description summary
   - Apply link

### Data Fields Captured

| Field | Format |
|-------|--------|
| title | String |
| company | String |
| location | String |
| date_posted | ISO 8601 |
| description | Text |
| apply_url | URL |
| seniority | "Executive" |

### Export Format

JSON lines format per job:
```json
{"title":"CEO","company":"Acme Corp","location":"Lilongwe, Malawi","date_posted":"2026-11-20","description":"...","apply_url":"https://...","seniority":"Executive"}
```

---

## Profile 2: Malawi Development Jobs

**Source**: CareerAd Malawi, Job Centre Malawi, AfricaWork
**Target Role**: Development sector positions in Malawi
**Keywords**: `malawi, development, project officer, program manager, consultant`

### Search Parameters

- **Location**: Malawi (all regions)
- **Sector**: Development, NGO, Government
- **Keywords**: `malawi, lilongwe, blantyre, mangochi, zomba, development`

### Browser Workflow

1. Navigate to the target Malawi job board
2. Set location to "Malawi" or leave blank for all Malawi regions
3. Filter by sector: Development / NGO / Government
4. Apply keyword filter: "malawi development"
5. Paginate through results (typically 20 per page)
6. Save results page screenshot
7. Extract job cards with the following fields:
   - Job title
   - Organization
   - District/Region
   - Position level
   - Sector
   - Application deadline

### Data Fields Captured

| Field | Format |
|-------|--------|
| title | String |
| organization | String |
| district | String (e.g., "Lilongwe", "Blantyre") |
| level | String (e.g., "Officer", "Manager", "Consultant") |
| sector | String (e.g., "NGO", "Government", "International") |
| deadline | ISO 8601 or null |
| source | String (source identifier) |

### Export Format

JSON lines format per job:
```json
{"title":"Project Officer","organization":"UNICEF","district":"Lilongwe","level":"Officer","sector":"NGO","deadline":"2026-12-15","source":"careerad-malawi"}
```

---

## Profile 3: UN & International Organizations

**Source**: UN Careers, UNDP Careers, Impactpool, UNjobs
**Target Role**: International development, UN, multilateral roles
**Keywords**: `un, undp, impactpool, jobs, coordinator, analyst, specialist`

### Search Parameters

- **Organization Filter**: UN, UNDP, Undp, Impactpool, UNjobs
- **Contract Type**: P-1 to D-2, Fixed-term, Temporary
- ** Duty Station**: Malawi, Regional (Nairobi, Addis Ababa), Global
- **Keywords**: `un job, undp vacancy, impactpool, development`

### Browser Workflow

1. Navigate to the target UN/international organization job board
2. Filter by organization: UN / UNDP / Impactpool / UNjobs
3. Set duty station: "Malawi" or "Regional"
4. Filter contract type as needed
5. Apply keyword filter: "malawi" or "development"
6. Paginate through results
7. Save results page screenshot
8. Extract job cards with the following fields:
   - Job title
   - Organization
   - Duty station
   - Level (P-1, P-2, D-1, etc.)
   - Contract type
   - Closing date
   - Job ID

### Data Fields Captured

| Field | Format |
|-------|--------|
| title | String |
| organization | String |
| duty_station | String |
| level | String (P-1, P-2, D-1, D-2, etc.) |
| contract_type | String |
| closing_date | ISO 8601 or null |
| job_id | String |
| source | String |

### Export Format

JSON lines format per job:
```json
{"title":"Program Analyst","organization":"UNDP","duty_station":"Lilongwe","level":"P-2","contract_type":"Fixed-term","closing_date":"2026-12-20","job_id":"UNDP-2026-1234","source":"undp-careers"}
```

---

## Profile 4: Devex & ReliefWeb

**Source**: Devex, ReliefWeb
**Target Role**: Humanitarian, development project roles
**Keywords**: `devex, reliefweb, humanitarian, emergency, project manager`

### Search Parameters

- **Sector**: Humanitarian, Development, Emergency Response
- **Keyword Filter**: "devex" or "reliefweb" specific terms
- **Location**: Developing countries, Malawi, regional
- **Keywords**: `humanitarian, emergency response, project management, donor-funded`

### Browser Workflow

1. Navigate to the target Devex/ReliefWeb job board
2. Filter by sector: "Humanitarian" or "Development"
3. Apply location filter: Malawi / Developing Countries
4. Set keyword filter based on source-specific terms
5. Paginate through results (may use infinite scroll)
6. Save results page screenshot
7. Extract job cards with the following fields:
   - Job title
   - Organization/Donor
   - Sector
   - Location
   - Contract duration
   - Posting date

### Data Fields Captured

| Field | Format |
|-------|--------|
| title | String |
| organization | String |
| sector | String (Humanitarian / Development / Emergency) |
| location | String |
| contract_duration | String or null |
| posting_date | ISO 8601 |
| source | String |

### Export Format

JSON lines format per job:
```json
{"title":"Emergency Coordinator","organization":"WHO","sector":"Humanitarian","location":"Blantyre, Malawi","contract_duration":"3 months","posting_date":"2026-11-20","source":"devex"}
```

---

## Profile 5: African Development Bank & World Bank

**Source**: African Development Bank, World Bank
**Target Role**: Senior development, policy, finance roles
**Keywords**: `african development bank, world bank, economist, senior specialist, policy`

### Search Parameters

- **Organization**: African Development Bank / World Bank
- **Job Function**: Economics, Finance, Policy, Operations
- **Country**: Malawi, Regional (Africa), Global
- **Keywords**: `afdb, world bank, economist, senior specialist, policy analyst`

### Browser Workflow

1. Navigate to the target African Development Bank/World Bank job portal
2. Select organization: "African Development Bank" or "World Bank"
3. Filter by job function: "Economics", "Finance", "Policy", "Operations"
4. Set country filter: "Malawi" or "Regional Africa"
5. Apply seniority filter as appropriate
6. Paginate through results
7. Save results page screenshot
8. Extract job cards with the following fields:
   - Job title
   - Organization
   - Department/Function
   - Level/seniority
   - Duty station
   - Closing date
   - Job reference number

### Data Fields Captured

| Field | Format |
|-------|--------|
| title | String |
| organization | String |
| department | String |
| level | String |
| duty_station | String |
| closing_date | ISO 8601 or null |
| job_ref | String (reference number) |
| source | String |

### Export Format

JSON lines format per job:
```json
{"title":"Senior Economist","organization":"African Development Bank","department":"Economics","level":"Senior","duty_station":"Lilongwe","closing_date":"2027-01-15","job_ref":"AfDB-2026-8742","source":"afdb"}
```

---

## Profile Usage Notes

- All profiles export in **JSON lines format** (one JSON object per line)
- Profiles are designed for **supervised browser sessions** where the user handles authentication and MFA
- Each profile includes **browser workflow steps** adapted to the source's UI
- Data fields are **minimal viable** for import into the Career pipeline
- Screenshots are captured at each step for audit and debugging
- Profiles can be chained or combined for comprehensive discovery

---

**Last Updated**: 2026-11-20
**Session**: Browser-Assisted Job Discovery Onboarding
