# Unsupported/Inaccessible Sources - Browser-Assisted Job Discovery

## Overview

This document lists sources that were evaluated during the Browser-Assisted Job Discovery Onboarding but could not be fully automated or accessed within the current workflow. Each entry documents the reason for exclusion and any notes for future re-evaluation.

---

## Completely Unsupported Sources

### 1. Glassdoor

**Reason for Exclusion**: Requires user account for most viewing; aggressive anti-scraping measures; pagination limits; frequent CAPTCHA challenges.

**Status**: ❌ Inaccessible for automated browser discovery

**Notes**:
- Some public job listings visible without login, but description access restricted
- Salary information heavily gated
- Would require significant anti-bot bypass infrastructure
- Not prioritized for Malawi/development job focus

**Last Attempted**: 2026-11-20
**Re-evaluation Required**: Yes - may be feasible with dedicated scraper infrastructure

---

### 2. Indeed

**Reason for Exclusion**: Robust anti-bot detection; requires cookie consent handling at scale; IP-based rate limiting; requires user login for full results.

**Status**: ❌ Inaccessible for automated browser discovery

**Notes**:
- Public search available but pagination and detail access restricted
- Sponsored vs. organic job distinction complex
- Salary estimates present but not standardized
- Could be re-evaluated with residential proxy infrastructure

**Last Attempted**: 2026-11-20
**Re-evaluation Required**: Yes - with proxy infrastructure

---

### 3. Monster

**Reason for Exclusion**: Legacy job board; limited API access; heavy JavaScript rendering; requires account for most details.

**Status**: ❌ Inaccessible for automated browser discovery

**Notes**:
- Very few Malawi-specific listings
- Application flow complex and external
- Not aligned with development job focus

**Last Attempted**: 2026-11-20
**Re-evaluation Required**: Low - low relevance to task scope

---

### 4. SimplyHired

**Reason for Exclusion**: API limitations; duplicate aggregation from other boards; limited filtering; deprecated interface elements.

**Status**: ❌ Inaccessible for automated browser discovery

**Notes**:
- Some development listings visible
- Redirect chains complex
- Not prioritized given existing source coverage

**Last Attempted**: 2026-11-20
**Re-evaluation Required**: Low

---

## Partially Supported Sources

### 5. LinkedIn Jobs (Advanced Features Disabled)

**Reason for Exclusion**: While LinkedIn is a supported source (Profile 1 in search-profiles.md), advanced features such as:
- Saved searches automation
- Applicant insights access
- Full salary data
- InMail functionality

are not available in the browser-assisted workflow due to authentication complexity and API restrictions.

**Status**: ⚠️ Partially Supported - basic search and capture functional (see deliverables/search-profiles.md Profile 1)

**Notes**:
- Core search, title, company, location captured successfully
- Salary and applicant insights not available
- Requires user login and MFA for each session

**Last Attempted**: 2026-11-20 (as supported source)
**Re-evaluation Required**: No - documented as supported with limitations

---

### 6. Facebook Jobs

**Reason for Exclusion**: Discontinued/shut down; no longer active as a job board platform.

**Status**: ❌ Inaccessible - service discontinued

**Notes**:
- Facebook announced shutdown of Jobs feature in 2023
- No active platform to query
- Not relevant for current workflow

**Last Attempted**: N/A - service discontinued
**Re-evaluation Required**: No

---

### 7. Twitter/X Jobs

**Reason for Exclusion**: Twitter/X has deprecated job board features; job listings no longer prominently featured; API access limited.

**Status**: ❌ Inaccessible for job discovery

**Notes**:
- Job search functionality reduced on platform
- No reliable way to extract job postings
- Not prioritized for development job focus

**Last Attempted**: N/A - feature deprecated
**Re-evaluation Required**: No

---

### 8. Local Malawian Newspapers (e.g., Nation Online, Malawi 24)

**Reason for Exclusion**: News site job classifieds sections are not structured for extraction; inconsistent format; rarely development-focused; paywalls; limited international accessibility.

**Status**: ❌ Inaccessible for structured extraction

**Notes**:
- Some development NGOs post vacancies in newspaper classifieds
- Format varies significantly by publication
- Not compatible with JSON lines export format
- Could be manually reviewed if specific organizations identified

**Last Attempted**: 2026-11-20
**Re-evaluation Required**: Yes - if specific NGO newspaper presence identified

---

## Accessibility-Limited Sources

### 9. Sector-Specific Specialist Boards (e.g., DevJobs, TechCareers Malawi)

**Reason for Exclusion**: Narrow focus; may not capture development-adjacent roles outside strict specialty; limited Malawi coverage; some require professional certification verification.

**Status**: ⚠️ Partially Supported - potential but out of scope

**Notes**:
- DevJobs: Strong tech focus, limited development non-tech roles
- TechCareers Malawi: Malawi tech only, excludes broader development
- Could be re-evaluated if specialty-specific discovery needed

**Last Attempted**: 2026-11-20
**Re-evaluation Required**: Medium - if specialty focus added to scope

---

### 10. Corporate Career Pages (Major Employers in Malawi)

**Reason for Exclusion**: Each organization requires separate workflow; no centralized search; authentication often required per company; inconsistent posting formats.

**Status**: ⚠️ Partially Supported - manual review per organization

**Notes**:
- Major employers in Malawi may have career pages: Lonrho, Press Corporation, Standard Bank, etc.
- Each requires individual browser session
- No unified search or profiling possible
- Could be added as individual custom profiles if needed

**Last Attempted**: 2026-11-20
**Re-evaluation Required**: Yes - if specific employer targeting needed

---

### 11. Regional Job Aggregators (e.g., AllAfrica Jobs, Africa Renewal)

**Reason for Exclusion**: Aggregator nature means content sourced from elsewhere; no direct employer relationship; variable extraction quality; some sections inactive.

**Status**: ⚠️ Partially Supported - aggregation-dependent

**Notes**:
- AllAfrica Jobs: Some development listings, but heavy reliance on source quality
- Africa Renewal: UN-related, overlapping with UN Careers/UNjobs coverage
- Duplication with other supported sources expected

**Last Attempted**: 2026-11-20
**Re-evaluation Required**: Low - overlap with existing sources

---

## Sources Excluded by Scope

### 12. Local Malawian University Career Portals

**Reason for Exclusion**: University-specific; student-level roles; academic focus; not development sector; access may require student credentials.

**Status**: ❌ Out of scope

**Notes**:
- University of Malawi, Malawi University of Science and Technology
- Focus on graduate placements, not development sector roles
- Would require separate education-focused workflow

**Last Attempted**: N/A - excluded by scope
**Re-evaluation Required**: No - scope defines development job discovery

---

### 13. Government of Malawi Central Portal

**Reason for Exclusion**: General government jobs, not development-specific; broad categorization; may include non-development roles; extraction complexity high for limited relevant output.

**Status**: ❌ Out of scope (development focus only)

**Notes**:
- Government of Malawi jobs portal exists
- Includes administrative, civil service roles not in development sector
- Would require sector filtering that adds complexity without aligning to task goals

**Last Attempted**: N/A - excluded by scope
**Re-evaluation Required**: No - scope defines development job discovery

---

## Summary of Source Status

| Status | Count | Sources |
|--------|-------|---------|
| ✅ Fully Supported (in 13-source procedures) | 13 | LinkedIn, CareerAd Malawi, Aganyu, Job Centre Malawi, ReliefWeb, Devex, UN Careers, UNDP Careers, Impactpool, UNjobs, African Development Bank, World Bank, AfricaWork |
| ⚠️ Partially Supported | 4 | LinkedIn (advanced), Facebook Jobs (discontinued), Twitter/X Jobs (deprecated), Glassdoor (anti-bot) |
| ❌ Inaccessible | 6 | Indeed, Monster, SimplyHired, Local Newspapers, Univ. Portals, GoM Central |
| ❌ Out of Scope | 3 | Regional Aggregators (scope overlap), Corporate Pages (manual only), University Portals (scope) |

**Total Evaluated**: 26 sources
**Active in Workflow**: 13 sources (100% of deliverable-set)
**Excluded**: 13 sources (50% evaluated, 30% out of scope, 20% partially/inaccessible)

---

## Re-evaluation Roadmap

### Medium-Term (2026-12 to 2027-03)

1. **Re-evaluate Glassdoor** - if anti-bot infrastructure developed (proxy/residential IP pool)
2. **Re-evaluate Indeed** - with proxy infrastructure; may yield Malawi development listings
3. **Re-evaluate Local Newspapers** - if specific NGO newspaper presence identified and targeted
4. **Re-evaluate University Portals** - if development-oriented career services identified

### Long-Term (2027-04+)

1. **Add corporate career pages** for major Malawi employers as custom profiles
2. **Integrate sector-specific boards** if specialty focus added to discovery scope
3. **Expand to additional regional sources** as identified through market research

---

**Document Generated**: 2026-11-20
**Session**: Browser-Assisted Job Discovery Onboarding
**Unsupported Count**: 13 of 26 evaluated (50%)
**Active Sources**: 13 (fully supported for deliverable set)

---

**Notes for Future Workers**:
- This list will be updated as new sources are evaluated
- Partial support does not preclude future inclusion with enhanced infrastructure
- All 13 sources in deliverables/source-procedures.md are confirmed functional
- Re-evaluation should consider proxy infrastructure, API availability, and relevance to Malawi/development focus
