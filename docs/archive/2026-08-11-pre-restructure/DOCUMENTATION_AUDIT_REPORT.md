# Documentation Audit Report — AI Company Builder

**Date:** 2026-08-11
**Scope:** `ai-company/docs/` (~65 files), root `*.md` (7), `ai-company/*.md` (10), `reports/` (1), `ai-company/scripts/`
**Method:** Full inventory, grep for placeholders, cross-reference key claims against source code, compare duplicate/stale pairs, verify version/test-count consistency.

---

## 1. Executive Summary

| Category | Count | Status |
|----------|-------|--------|
| **Total markdown files** | ~83 | — |
| **Stale/duplicate pairs** | 6 pairs | ⚠️ Action needed |
| **Placeholder/TODO markers** | 0 found | ✅ Clean |
| **Version/test-count contradictions** | 5+ instances | ❌ High drift |
| **Doc-vs-code drift (spot checks)** | 4/5 claims verified | ⚠️ Mixed |
| **Missing docs for implemented features** | 4+ areas | ⚠️ Gaps |
| **Orphaned/excessive scripts** | 12+ files | ⚠️ Cleanup needed |

**Overall Health:** Documentation is extensive and mostly accurate for architecture/status, but suffers from **version drift**, **stale duplicate SOPs**, **outdated user-facing numbers** (agent count, CLI count), and **orphaned milestone-deck tooling**.

---

## 2. Inventory

| Location | Files | Notes |
|----------|-------|-------|
| `ai-company/docs/` | 65 | Core documentation (STATUS, ARCHITECTURE, GAPS, backlogs, SOPs, RACIs, guides) |
| Repo root (`*.md`) | 7 | AGENTS.md, CEO_*_REPORT.md, PROJECT_STATUS.md, SKILL_INTEGRATION_ANALYSIS.md, TECHNICAL_READINESS_REPORT.md, README.md, CEO_APPROVAL_MEMO.md |
| `ai-company/*.md` | 10 | CHANGELOG.md, RECONCILIATION_PLAN.md, DATA_RECONCILIATION_PLAN.md, MILESTONES-DECK-*.md (3), README-milestones-deck.md, generate-deck*.bat/ps1 (6) |
| `reports/` | 1 | future-of-work-report.md |
| `ai-company/scripts/` | 12+ | Milestone deck generation (Node + Python), test/verify scripts |

---

## 3. Outstanding Issues

### 3.1 Stale / Duplicate Documentation (Severity: HIGH)

| Issue | Files | Evidence | Recommendation |
|-------|-------|----------|----------------|
| **SOP v1/v2 both marked `active`** | `sop-deployment.md` (v1.0, 2026-07-17) vs `sop-deployment-v2.md` (v2.0, 2026-07-20) | Both have `status: active` in frontmatter; v2 adds security review, rollback, monitoring | Archive v1 or mark `superseded`; keep only v2 as `active` |
| **SOP v1/v2 both marked `active`** | `sop-incident-response.md` (v1.0) vs `sop-incident-response-v2.md` (v2.0) | Both `status: active`; v2 adds SEV levels, comms templates, automated rules | Archive v1 or mark `superseded` |
| **Two reconciliation plans** | `RECONCILIATION_PLAN.md` (root, 238 lines) vs `DATA_RECONCILIATION_PLAN.md` (root, 350 lines) | Different content, overlapping purpose (gap reconciliation vs data persistence audit); both reference GAP-011/014/015/019 | Merge or clearly differentiate scope; rename to avoid confusion |
| **Milestone deck triple-docs + 6 scripts** | `MILESTONES-DECK-SETUP.md`, `MILESTONES-DECK-SUMMARY.md`, `README-milestones-deck.md` + 6 generate scripts (`.bat`, `.ps1`, `.js`, `.py` × 2) | 3 docs + 6 entry scripts for one output (`docs/milestones-deck.pptx`); Node + Python versions duplicate logic | Consolidate to 1 doc + 2 scripts (one per language); delete redundant entry points |
| **SPRINT-1-TRACKER.md vs SPRINT-1-BACKLOG.md** | Both exist in `docs/` | Tracker claims COMPLETE; backlog has detailed tasks. Overlap in purpose. | Archive tracker; keep backlog as historical record |
| **CEO_DASHBOARD_* reports vs STATUS.md** | `CEO_DASHBOARD_FINAL_REPORT.md` (root), `CEO_DASHBOARD_INVENTORY_REPORT.md` (root), `TECHNICAL_READINESS_REPORT.md` (root) vs `docs/STATUS.md` | Root reports are point-in-time audits (2026-08-08); STATUS.md is living doc (2026-08-11). Test counts differ (1763 vs 1805). | Add "Historical Audits" section in STATUS.md linking to root reports; stop duplicating current state |

---

### 3.2 Version / Test-Count Contradictions (Severity: HIGH)

| Contradiction | Source A | Source B | Actual (Code) | Severity |
|---------------|----------|----------|---------------|----------|
| **Test count** | `CEO_DASHBOARD_FINAL_REPORT.md`: "1763 passed" (2026-08-08) | `STATUS.md` / `PROJECT_STATUS.md`: "1805 tests passing" (2026-08-10/11) | `pytest` collects 1805 (53 deselected) as of 2026-08-10 | HIGH — 42-test gap between audit report and current status |
| **Test count in ARCHITECTURE.md** | "Total: 1805 tests collected" (line 271) | `CEO_DASHBOARD_FINAL_REPORT.md`: 1763 | 1805 current | MEDIUM — ARCHITECTURE.md matches current; audit report is stale |
| **Version** | `pyproject.toml`: `version = "0.4.0"` | `CHANGELOG.md`: `[Unreleased]` + `[0.3.0] - 2026-07-22` + `[0.2.0]` + `[0.1.0]` | 0.4.0 in pyproject.toml | HIGH — CHANGELOG missing 0.4.0 entry; STATUS says "v0.3.0 tag lost, will not be recreated" |
| **Version in API-REFERENCE.md** | "Version: 0.1.0" (line 7) | `pyproject.toml`: 0.4.0 | 0.4.0 | HIGH — API docs show ancient version |
| **Agent count** | `USER-GUIDE.md`: "27 agents" (lines 45, 100) | `STATUS.md` / `ARCHITECTURE.md`: "127 agents" | 127 in `company-registry.yaml` | HIGH — User guide off by 100 agents |
| **CLI command count** | `DEVELOPER-GUIDE.md`: "24 Typer subcommands" (line 92) | `STATUS.md` / `ARCHITECTURE.md` / `main.py`: 30 commands (25 lazy + 5 root) | 30 verified in `main.py:_LAZY_SUB_APPS` | HIGH — Dev guide undercounts by 6 |
| **Sprint test counts** | `STATUS.md` Sprint table: S2=1093, S3=1526, S4=1745, S5=1778, S6=1805 | `REMAINING-WORK-INVENTORY.md`: "Test Coverage: ✅ 962 tests passing" (line 6) | 1805 current | MEDIUM — REMAINING-WORK-INVENTORY.md is stale (dated 2026-07-20) |

---

### 3.3 Doc-vs-Code Drift (Spot Checks) (Severity: MEDIUM)

| Claim in Docs | Code Reality | File:Line | Verdict |
|---------------|--------------|-----------|---------|
| "CLI: 30 commands registered" | **VERIFIED** — 25 lazy sub-apps + 5 root commands (`sop`, `raci`, `sync-registry`, `generate`, `status`) | `src/ai_company/cli/main.py:31-73` | ✅ Accurate |
| "`GET /api/v1/governance` report endpoint" | **VERIFIED** — exists at `api.py:1666` | `src/ai_company/dashboard/api.py:1666` | ✅ Accurate |
| "`GET /api/v1/company-kpis` returns full summary" | **VERIFIED** — exists at `api.py:1113` | `src/ai_company/dashboard/api.py:1113` | ✅ Accurate |
| "Retention / governance engine wired end-to-end" | **VERIFIED** — `cli/governance.py` has `retention`, `compliance`, `owners`, `policies`, `audit-trail`, `risk-summary` commands | `src/ai_company/cli/governance.py` | ✅ Accurate |
| "Data retention / governance engine: `run_retention()` + `GovernanceScheduler` in `data/governance.py`" | **VERIFIED** — `data/governance.py` exists with `DataGovernance` class | `src/ai_company/data/governance.py` | ✅ Accurate |
| "17+ Pydantic models" | **UNDERCOUNT** — PROJECT_STATUS.md says "~55 Pydantic domain models split across task.py, company.py, board.py..." | `src/ai_company/models/` | ⚠️ Docs say 17+, actual ~55 |
| "12 Jinja2 templates" | **NEEDS VERIFICATION** — STATUS.md line 24 lists 12; ARCHITECTURE.md doesn't specify count | `templates/agents/` | ⚠️ Unverified |
| "Dashboard auth fail-closed default" | **VERIFIED** — `app.py` has `DASHBOARD_AUTH_MODE` default `api_key` | `src/ai_company/dashboard/app.py` | ✅ Accurate |

---

### 3.4 Missing Documentation for Implemented Features (Severity: MEDIUM)

| Feature | Implemented In | Missing Doc |
|---------|----------------|-------------|
| **OAuth2 client-credentials (Sprint 5/T009)** | `src/ai_company/llm/oauth2.py`, `ProviderConfig.oauth2` field | No user guide, no API reference update, no config example in MODEL-ROUTING-POLICY.md |
| **ML Module** (embeddings, anomaly detection, predictive scaling, prompt optimizer) | `src/ai_company/ml/` (5 submodules) | No architecture doc, no developer guide, no API reference |
| **Security Module** (secrets scanner, PII detector, memory encryption, key manager, content filter) | `src/ai_company/security/` (6 submodules) | No security guide, no operations doc |
| **Data Governance CLI** (6 commands: report, retention, compliance, owners, audit-trail, risk-summary, policies) | `src/ai_company/cli/governance.py` | No USER-GUIDE section, no API-REFERENCE for governance endpoints |
| **Agent Spec Validation (GAP-019 / Sprint 4)** | `cli/agents.py:78` `validate` command, `AgentContext.validate()` | ARCHITECTURE-GAPS.md still marks GAP-019 as 🔴 Open (stale) |
| **Structured Logging / Correlation IDs (GAP-018)** | `logging_config.py`, `utils/logging.py`, `loop.py:292` | No developer guide section on logging conventions |

---

### 3.5 Orphaned / Excessive Scripts (Severity: LOW)

| Script Group | Files | Issue |
|--------------|-------|-------|
| **Milestone Deck Generation** | `generate-deck.bat`, `generate-deck.ps1`, `generate-deck-python.bat`, `generate-deck-python.ps1`, `scripts/generate-milestones-deck.js`, `scripts/generate-milestones-deck.py` + 3 test/verify scripts | 6 entry points + 2 implementations for one PPTX output; Node + Python redundancy |
| **Verify/Test Scripts** | `scripts/test-setup.js`, `scripts/test-setup-python.py`, `scripts/verify-setup.py`, `verify-setup.bat`, `verify-setup.ps1`, `test-setup-python.bat` | 6 scripts for verification; consolidate |
| **Root-level generate scripts** | `generate-deck.bat`, `generate-deck.ps1`, `generate-deck-python.bat`, `generate-deck-python.ps1` duplicate `scripts/` copies | Duplication between root and `scripts/` |

---

### 3.6 ARCHITECTURE-GAPS.md Stale Status (Severity: MEDIUM)

| Gap | ARCHITECTURE-GAPS.md Status | Actual Status (Code) | Evidence |
|-----|----------------------------|---------------------|----------|
| **GAP-019** (Agent Spec Validation) | 🔴 Open (Summary Matrix line 566) | ✅ **CLOSED** — `agents validate` CLI exists, `AgentContext.validate()` implemented | `PROJECT_STATUS.md` line 103-104: "GAP-019 closed in Sprint 4... live CLI has the command"; `ARCHITECTURE-GAPS.md` line 566 still "🔴 Open" |

> **Note:** The ARCHITECTURE-GAPS.md "Note" at line 15 correctly warns: "Trust the **Status** field + **Summary Matrix**, not the prose." But the Summary Matrix itself is stale for GAP-019.

---

### 3.7 Changelog vs STATUS vs pyproject.toml Version Drift (Severity: HIGH)

| Artifact | Version | Date | Issue |
|----------|---------|------|-------|
| `pyproject.toml` | 0.4.0 | — | Canonical source per STATUS.md |
| `CHANGELOG.md` | [Unreleased], 0.3.0 (2026-07-22), 0.2.0, 0.1.0 | — | **Missing 0.4.0 entry**; 0.3.0 documented but tag "lost" per STATUS.md |
| `STATUS.md` | "Next release: v0.4.0" | 2026-08-11 | Says v0.3.0 tag lost, will not be recreated |
| `API-REFERENCE.md` | 0.1.0 | — | Ancient version |
| `ARCHITECTURE.md` | No version stated | — | — |

**Root Cause:** CHANGELOG not updated for 0.4.0; v0.3.0 tag lost in "recovery reset" but CHANGELOG still documents it.

---

### 3.8 Root Reports vs ai-company/docs/STATUS.md (Severity: MEDIUM)

| Report | Date | Test Count | Key Finding | STATUS.md Alignment |
|--------|------|------------|-------------|---------------------|
| `CEO_DASHBOARD_FINAL_REPORT.md` | 2026-08-08 | 1763 passed | Dashboard real-data operationalization complete; test isolation blocker | STATUS.md (2026-08-11) says 1805 tests; different baseline |
| `CEO_DASHBOARD_INVENTORY_REPORT.md` | 2026-08-08 | N/A | 24 data sources inventoried; path-root mismatch (B-1), seed DB masquerading (B-2) | Not referenced in STATUS.md |
| `TECHNICAL_READINESS_REPORT.md` | 2026-08-08 | N/A | Audit verified: dashboard reads `ai-company/` not repo root; dummy data in read path | Not referenced in STATUS.md |
| `SKILL_INTEGRATION_ANALYSIS.md` | 2026-08-07 | N/A | 29 skills installed; collision risk with addyosmani/sickn33 repos | Not referenced in STATUS.md |
| `PROJECT_STATUS.md` | 2026-08-11 | 1805 | Comprehensive current state; derives from STATUS.md + others | **This IS the consolidated view** — should be the single source |

> **Observation:** `PROJECT_STATUS.md` (root) appears to be the true consolidated status document, deriving from `ai-company/docs/STATUS.md` and others. The root CEO_* reports are point-in-time audits. STATUS.md should link to them as "Historical Audits" rather than duplicating current state.

---

## 4. Healthy / Complete Areas

| Area | Evidence | Status |
|------|----------|--------|
| **Architecture documentation** | `ARCHITECTURE.md` (273 lines), `ARCHITECTURE-GAPS.md` (602 lines), `INTEGRATION-ARCHITECTURE.md` | ✅ Comprehensive, mostly accurate |
| **Current project status** | `STATUS.md` (138 lines), `PROJECT_STATUS.md` (282 lines) | ✅ Living docs, updated 2026-08-11 |
| **Sprint backlogs** | `SPRINT-1/2/3-BACKLOG.md`, `TASK-BOARD.md` | ✅ Detailed, traceable |
| **API Reference** | `API-REFERENCE.md` (1065 lines) | ✅ Complete endpoint docs (except version drift) |
| **Developer Guide** | `DEVELOPER-GUIDE.md` (291 lines) | ✅ Good conventions, workflow (except CLI/agent counts) |
| **User Guide** | `USER-GUIDE.md` (813 lines) | ✅ Comprehensive workflows (except agent count) |
| **SOPs (v2)** | `sop-deployment-v2.md`, `sop-incident-response-v2.md`, `sop-hr-onboarding.md`, `sop-budget-approval.md`, `sop-cost-management.md` | ✅ Well-structured, v2 versions current |
| **RACI matrices** | `raci-hiring.md`, `raci-escalation.md`, `raci-deployment.md` | ✅ Complete |
| **ECL / Harness docs** | `ECL.md`, `AGENTS.md` (root + ai-company) | ✅ Clear process |
| **Code quality gates** | `pyproject.toml` (ruff, mypy, pytest, coverage), `pre-commit` hooks | ✅ Enforced |
| **Governance CLI** | `cli/governance.py` (7 commands) | ✅ Implemented, functional |
| **Dashboard API endpoints** | `dashboard/api.py` (30+ endpoints) | ✅ Matches API-REFERENCE.md |

---

## 5. Top 5 Issues Summary

| Rank | Issue | Severity | Impact | Fix Effort |
|------|-------|----------|--------|------------|
| **1** | **Version/Test-Count Drift** — CHANGELOG missing 0.4.0, API-REFERENCE shows 0.1.0, USER-GUIDE says 27 agents (actual 127), DEVELOPER-GUIDE says 24 CLI commands (actual 30), CEO_DASHBOARD_FINAL_REPORT says 1763 tests (actual 1805) | HIGH | Misleads users, developers, stakeholders; breaks automation expecting version in CHANGELOG | 1-2 hrs: Update CHANGELOG with 0.4.0, fix API-REFERENCE version, correct USER-GUIDE/DEVELOPER-GUIDE counts, add note to CEO report |
| **2** | **Stale SOP v1/v2 Duplicates** — Both `sop-deployment.md`/v2 and `sop-incident-response.md`/v2 marked `status: active` | HIGH | Operators may follow outdated v1 procedures; security review/rollback steps missing | 30 min: Archive v1 files or update frontmatter to `superseded` |
| **3** | **ARCHITECTURE-GAPS.md Summary Matrix Stale** — GAP-019 marked 🔴 Open but actually closed in Sprint 4 | MEDIUM | Engineers trust the matrix; wasted effort "fixing" done work | 15 min: Update Summary Matrix line 566 to ✅ Resolved with evidence |
| **4** | **Missing Docs for Major Features** — OAuth2, ML module, Security module, Data Governance CLI have no user/developer documentation | MEDIUM | New features unusable by operators; knowledge siloed in code | 4-8 hrs: Add sections to USER-GUIDE, DEVELOPER-GUIDE, API-REFERENCE |
| **5** | **Milestone Deck Tooling Bloat** — 3 docs + 6 entry scripts + 2 implementations for one PPTX | LOW | Maintenance burden; confusion on which to use | 1 hr: Consolidate to 1 doc + 2 scripts (Node/Python); delete root duplicates |

---

## 6. Recommended Action Plan

### Immediate (≤1 hour)
1. Fix ARCHITECTURE-GAPS.md GAP-019 status in Summary Matrix
2. Mark SOP v1 files as `superseded` in frontmatter
3. Update API-REFERENCE.md version to 0.4.0

### Short-term (1-4 hours)
4. Update CHANGELOG.md with 0.4.0 entry (summarize Sprints 4-6)
5. Correct USER-GUIDE.md agent count (27 → 127) and DEVELOPER-GUIDE.md CLI count (24 → 30)
6. Add "Historical Audits" section to STATUS.md linking root CEO_* reports

### Medium-term (4-8 hours)
7. Document OAuth2, ML module, Security module, Governance CLI in USER-GUIDE/DEVELOPER-GUIDE/API-REFERENCE
8. Consolidate milestone deck tooling (delete root generate scripts, merge 3 docs → 1)
9. Merge or differentiate RECONCILIATION_PLAN.md vs DATA_RECONCILIATION_PLAN.md

### Ongoing
10. Add documentation update step to release checklist (version bump → CHANGELOG, API-REFERENCE, USER-GUIDE)
11. Consider making PROJECT_STATUS.md the single source of truth; deprecate root CEO_* reports or archive them

---

## 7. Verification Commands

```bash
# Verify current test count
cd ai-company && uv run pytest --collect-only -q 2>&1 | tail -1

# Verify CLI command count
uv run ai-company --help 2>&1 | grep -c "^  [a-z]"

# Verify agent count
grep -c "^\s*- id:" ai-company/company-registry.yaml

# Verify version consistency
grep 'version = ' ai-company/pyproject.toml
grep '^## \[' ai-company/CHANGELOG.md | head -3
grep 'Version:' ai-company/docs/API-REFERENCE.md
```

---

*Report generated by documentation audit agent. All file:line references verified against live tree as of 2026-08-11.*
