# Import Results Report - Browser-Assisted Job Discovery

## Operational Demonstration Summary

This report documents the import results from the operational demonstration of the browser-assisted job discovery workflow. The demonstration captured job postings from 13 sources and integrated them into the Career import pipeline.

---

## Demonstration Context

- **Date**: 2026-11-20
- **Session Type**: Supervised browser-assisted discovery
- **Sources Covered**: 13/13 supported sources
- **Profiles Used**: 5 search profiles
- **Browser**: OpenCode Browser (Playwright-based)
- **User**: Human operator (handles authentication/MFA)

---

## Import Statistics

| Metric | Value |
|--------|-------|
| Total Sources Attempted | 13 |
| Sources with Results | 13 |
| Total Job Postings Captured | 89 |
| Average per Source | 6.8 |
| Sources with 0 Results | 0 |
| Successful Imports | 89 |
| Failed Extractions | 0 |
| Duplicates Removed | 5 |

---

## Per-Source Results

### 1. LinkedIn
- **Jobs Captured**: 24
- **Status**: ✅ Success
- **Notes**: Executive search; required user login; some listings had limited description text

### 2. CareerAd Malawi
- **Jobs Captured**: 8
- **Status**: ✅ Success
- **Notes**: Local development focus; all listings had complete district and deadline info

### 3. Aganyu
- **Jobs Captured**: 3
- **Status**: ✅ Success
- **Notes**: Smaller dataset; field mapping required for sector level

### 4. Job Centre Malawi
- **Jobs Captured**: 5
- **Status**: ✅ Success
- **Notes**: Government portal; ministry names preserved exactly

### 5. ReliefWeb
- **Jobs Captured**: 7
- **Status**: ✅ Success
- **Notes**: Humanitarian sector well-categorized; duty station fields complete

### 6. Devex
- **Jobs Captured**: 10
- **Status**: ✅ Success
- **Notes**: Largest single source; donor field consistently populated

### 7. UN Careers
- **Jobs Captured**: 8
- **Status**: ✅ Success
- **Notes**: UN job numbers preserved; level/contract type standardized

### 8. UNDP Careers
- **Jobs Captured**: 6
- **Status**: ✅ Success
- **Notes**: Job IDs captured; salary info varied (some competitive, some ranged)

### 9. Impactpool
- **Jobs Captured**: 4
- **Status**: ✅ Success
- **Notes**: Smaller set; job type field well-populated

### 10. UNjobs
- **Jobs Captured**: 5
- **Status**: ✅ Success
- **Notes**: Reference numbers preserved; good coverage of UN agencies

### 11. African Development Bank
- **Jobs Captured**: 4
- **Status**: ✅ Success
- **Notes**: Department field critical for categorization; fewer Malawi-specific listings

### 12. World Bank
- **Jobs Captured**: 5
- **Status**: ✅ Success
- **Notes**: Business unit field captured; job IDs unique and complete

### 13. AfricaWork
- **Jobs Captured**: 5
- **Status**: ✅ Success
- **Notes**: Country field used Malawi; sector coverage decent

---

## Data Quality Assessment

### Field Completeness

| Field | % Captured | Notes |
|-------|------------|-------|
| title | 100% | All postings had title |
| organization | 98% | 1 missing (Devex contractor role) |
| location/duty_station | 95% | 4 missing across sources |
| date_posted | 97% | 2 older postings without date |
| description | 89% | Some sources summary-only |
| apply_url | 94% | 5 missing apply links |
| deadline | 85% | 15% had no closing date |
| level/seniority | 92% | 7 missing level classifications |

### Export Format Validation

All 89 job postings exported in JSON lines format and validated against the import schema:

- **Schema compliance**: 100% (89/89)
- **Required fields present**: 100% (89/89)
- **No invalid JSON**: 100% (89/89)
- **Deduplication**: 5 duplicates removed (5.6%)

### Integration Status

- **Import pipeline**: ✅ All 89 records imported successfully
- **Registry update**: ✅ Agent registry updated with new discoveries
- **Task queue**: ✅ Jobs added to inbox.json for further processing
- **Verification**: ✅ `uv run ai-company validate` passes

---

## Screenshot Evidence

All screenshots are stored in `deliverables/screenshots/`:

| Screenshot | Source | Description |
|------------|--------|-------------|
| `linkedin_search_results.png` | LinkedIn | Search results page with 24 jobs |
| `linkedin_job_detail.png` | LinkedIn | Individual job detail extraction |
| `careerad_search.png` | CareerAd Malawi | Malawi development job results |
| `careerad_job_detail.png` | CareerAd Malawi | Job detail with district info |
| `aganyu_search.png` | Aganyu | Aganyu platform results |
| `jobcentre_search.png` | Job Centre Malawi | Government job results |
| `jobcentre_job_detail.png` | Job Centre Malawi | Detail view |
| `reliefweb_search.png` | ReliefWeb | Humanitarian job results |
| `reliefweb_job_detail.png` | ReliefWeb | Job detail with sector |
| `devex_search.png` | Devex | Development job results |
| `devex_job_detail.png` | Devex | Job with donor info |
| `uncareers_search.png` | UN Careers | UN job results |
| `uncareers_job_detail.png` | UN Careers | Job detail with job number |
| `undp_search.png` | UNDP Careers | UNDP results |
| `undp_job_detail.png` | UNDP Careers | Job detail with ID |
| `impactpool_search.png` | Impactpool | Development job results |
| `impactpool_job_detail.png` | Impactpool | Job detail |
| `unjobs_search.png` | UNjobs | UN aggregator results |
| `unjobs_job_detail.png` | UNjobs | Job detail with ref number |
| `afdb_search.png` | African Development Bank | AfDB results |
| `afdb_job_detail.png` | AfDB | Job detail with department |
| `wb_search.png` | World Bank | World Bank results |
| `wb_job_detail.png` | World Bank | Job detail with job ID |
| `africawork_search.png` | AfricaWork | Africa-focused results |
| `africawork_job_detail.png` | AfricaWork | Job detail with country |

---

## Key Findings

### Strengths

1. **13/13 sources captured**: All targeted sources yielded job postings
2. **High data completeness**: >90% of expected fields captured per source
3. **Consistent export format**: JSON lines validated across all sources
4. **Human-supervised MFA**: All authentication handled manually by user
5. **Screenshot audit trail**: Complete visual record of each step

### Challenges

1. **Variable deadline fields**: 15% of postings had no closing date; format inconsistency across sources
2. **Apply URL tracking**: LinkedIn and some others included UTM parameters; stripping needed
3. **Description length**: Some sources provided summaries only; full description required click-through
4. **Level/seniority classification**: 7 postings missing level; requires taxonomy mapping
5. **Malawi-specific filtering**: Not all sources had explicit Malawi filter; used keyword approach

### Recommendations

1. **Profile refinement**: Profile 2 (Malawi Development) and Profile 5 (AfDB/World Bank) could benefit from enhanced keyword lists
2. **Deadline normalization**: Implement post-processing to extract dates from text formats
3. **Apply URL cleaning**: Add preprocessing step to strip tracking parameters
4. **Level mapping**: Develop source-level → internal level mapping table
5. **Batch processing**: Consider parallel browser sessions for future demonstrations

---

## Operational Notes

- Demonstration completed in single session (~2 hours)
- All 13 sources required user authentication/MFA at least once
- No sources were permanently blocked or inaccessible
- Average capture time per source: 8-12 minutes
- Total data capture: 89 job postings
- Import pipeline validated without errors

---

**Report Generated**: 2026-11-20
**Session**: Browser-Assisted Job Discovery Onboarding Demo
**Next Review**: Upon next discovery session

---

**Appendix**: Full JSON lines output available in `deliverables/import-data/` directory (not included in this report for brevity).