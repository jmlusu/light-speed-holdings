# Browser-Assisted Job Discovery Onboarding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: subagent-driven-development. A fresh subagent implements each task; a fresh reviewer checks it before the next task starts; a whole-branch review closes the work. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish a repeatable, human-directed job discovery workflow using OpenCode Browser and the existing Unified Career Automation pipeline, enabling supervised discovery sessions across LinkedIn and Malawi/development sources.

**Architecture:** Human-directed browser sessions (user handles login/MFA and posting selection) feed captured evidence into the existing `pipeline/` package (`pipeline.discovery`, `pipeline.extraction`, `pipeline.models.job`). New configuration modules (search profiles, source registry) and documentation complete the Phase 4.1 onboarding layer. No new orchestrator, no automated scraping, no production writes.

**Tech Stack:** Python 3.11+, pytest, existing `pipeline/` modules, Markdown docs, JSON configuration.

**Spec:** Phase 4.1 — Browser-Assisted Job Discovery Onboarding (user-supplied). Execution amendments below adapt the spec's generic paths to this repository's real conventions.

---

## Execution Amendments (repo-adapted paths)

The spec references a "Career project" with `browser/`, `sources/`, and `career/` directories. This repository's existing Unified Career Automation pipeline lives in `pipeline/`. All new code follows that convention:

| Spec path | Repository path |
|---|---|
| `browser/search_profiles.json` | `pipeline/search_profiles.json` |
| `browser/search-profiles.py` | `pipeline/search_profiles.py` |
| `sources/registry.py` | `pipeline/sources.py` |
| `browser/operating-procedure.md` | `docs/browser-operating-procedure.md` |
| `browser/capture-workflow.py` | `pipeline/capture.py` |
| `demonstration/` | `demonstration/` (existing, prior session — do not overwrite) |
| `deliverables/` | `deliverables/` (existing, prior session — do not overwrite) |
| `verification/scope-verification.md` | `verification/scope-verification.md` |

Prior-session artifacts already present and treated as read-only inputs: `demonstration/results-report.md`, `deliverables/{browser-onboarding-instructions,search-profiles,source-procedures,import-results-report,unsupported-sources}.md`.

## Global Constraints

- Do not redesign the accepted architecture; do not create another orchestrator.
- Do not implement unauthorized scraping; LinkedIn remains manual browser discovery and local import.
- Do not bypass CAPTCHA, authentication controls, anti-bot restrictions, or site terms.
- Do not modify the master resume; do not submit applications; do not send external communications.
- Do not perform unauthorized production Notion writes.
- Do not start a comprehensive repository audit.
- Preserve original evidence files; never overwrite previously captured evidence or prior-session artifacts.
- Record capture timestamps and source metadata; preserve original URLs.
- Every task's tests run with `.venv\Scripts\python.exe -m pytest pipeline/tests/<file> -q`.

## Review Focus

1. **Manual authentication/MFA**: capture must proceed only after the user completes login; no credential handling in code.
2. **CAPTCHA/anti-bot**: document and enforce refusal; failures are reported, never bypassed.
3. **Provenance**: original URL, capture timestamp, and source metadata preserved; evidence files immutable.
4. **Import integration**: captured artifacts must flow into the existing `pipeline.discovery`/`pipeline.extraction` interfaces; extraction failures reported.
5. **Scope enforcement**: no architecture redesign, no new orchestrator, no resume edits, no applications, no external comms, no Notion writes.

---

## Task 1: Browser Onboarding Instructions

**Files:**
- Create: `docs/browser-assisted-job-discovery-onboarding.md`
- Test: `pipeline/tests/test_phase41_onboarding.py`

**Interfaces:**
- Consumes: nothing (documentation task).
- Produces: onboarding doc referenced by operators; no code interface.

- [ ] **Step 1: Write the failing test** — assert the doc exists and contains sections: Initiating a Browser Session, Authentication, Capture Methods, Import Handoff, Constraints.
- [ ] **Step 2: Run test, verify FAIL** — `pytest pipeline/tests/test_phase41_onboarding.py -q`.
- [ ] **Step 3: Write the doc** — operator steps, auth/MFA handling, navigation under user direction, capture methods (HTML/PDF/visible text/manual/JSON-LD), import handoff, provenance rules, prohibitions, troubleshooting.
- [ ] **Step 4: Run test, verify PASS.**
- [ ] **Step 5: Report for review** (lead commits).

## Task 2: Configure Initial Search Profiles

**Files:**
- Create: `pipeline/search_profiles.py`
- Create: `pipeline/search_profiles.json`
- Test: `pipeline/tests/test_search_profiles.py`

**Interfaces:**
- Produces: `load_profiles() -> dict`, `get_profile(name: str) -> dict | None`, `list_profiles() -> list[str]`, `validate_profile(profile: dict) -> list[str]`.

- [ ] **Step 1: Failing test** — 5 profiles (`malawi`, `international_development`, `multilateral`, `technology_ai`, `consulting_advisory`); Malawi has `Lilongwe`, `Blantyre`, `data architecture`; international development has `digital health`, `health information systems`; all profiles have non-empty `keywords` and `job_titles`.
- [ ] **Step 2: Verify FAIL.**
- [ ] **Step 3: Implement** JSON + module (spec keywords; include title variations).
- [ ] **Step 4: Verify PASS.**
- [ ] **Step 5: Report for review.**

## Task 3: Configure Initial Sources

**Files:**
- Create: `pipeline/sources.py`
- Test: `pipeline/tests/test_sources_registry.py`

**Interfaces:**
- Produces: `SOURCES: dict[str, dict]`, `is_source_registered(name) -> bool`, `get_access_mode(name) -> str`, `get_procedure(name) -> dict`.

- [ ] **Step 1: Failing test** — all 13 sources present; LinkedIn `access_mode == "manual_browser_discovery"`; no source has `automated_fetching_authorized` true.
- [ ] **Step 2: Verify FAIL.**
- [ ] **Step 3: Implement** registry with url, category, access mode, auth/MFA flags.
- [ ] **Step 4: Verify PASS.**
- [ ] **Step 5: Report for review.**

## Task 4: Browser Operating Procedure

**Files:**
- Create: `docs/browser-operating-procedure.md`
- Create: `pipeline/procedures.py`
- Test: `pipeline/tests/test_operating_procedure.py`

**Interfaces:**
- Produces: `PROCEDURE_STEPS: list[str]`, `validate_procedure_doc(path) -> list[str]` (missing steps).

- [ ] **Step 1: Failing test** — doc contains all 8 canonical steps; `validate_procedure_doc` returns `[]`.
- [ ] **Step 2: Verify FAIL.**
- [ ] **Step 3: Implement** doc + module.
- [ ] **Step 4: Verify PASS.**
- [ ] **Step 5: Report for review.**

## Task 5: Local Capture Workflow

**Files:**
- Create: `pipeline/capture.py`
- Test: `pipeline/tests/test_capture_posting.py`

**Interfaces:**
- Produces: `capture_posting(url, source, profile, content=None, capture_method="visible_text", evidence_dir=None) -> dict` with keys `saved`, `url`, `timestamp`, `source_metadata`, `file_path`, `job`, `warnings`. Never overwrites: adds a numeric suffix when a file exists.

- [ ] **Step 1: Failing test** — capture writes evidence, returns required keys, `file_path` exists; second identical capture produces a second file.
- [ ] **Step 2: Verify FAIL.**
- [ ] **Step 3: Implement** using `pipeline.extraction.extract_job_data`; timestamp ISO-8601 UTC; source metadata from `pipeline.sources`.
- [ ] **Step 4: Verify PASS.**
- [ ] **Step 5: Report for review.**

## Task 6: First Operational Demonstration

**Files:**
- Create: `demonstration/session-logs/README.md` (index only; report already exists)
- Test: `pipeline/tests/test_demonstration_report.py`

**Interfaces:**
- Consumes: `demonstration/results-report.md` (read-only).
- Produces: verification that the demonstration report covers LinkedIn (≥3), Malawi (≥2), development sources (≥2), and records provenance.

- [ ] **Step 1: Failing test** — report exists, contains the three source groups, meets minimum counts, includes original URLs.
- [ ] **Step 2: Verify FAIL.**
- [ ] **Step 3: Add session-log index** documenting available evidence honestly (no fabricated captures).
- [ ] **Step 4: Verify PASS.**
- [ ] **Step 5: Report for review.**

## Task 7: Deliverables Verification

**Files:**
- Create: `pipeline/tests/test_deliverables.py`
- Create: `deliverables/README.md`

**Interfaces:**
- Consumes: the five prior-session deliverables (read-only).
- Produces: automated completeness checks.

- [ ] **Step 1: Failing test** — five deliverables exist and are non-empty; `search-profiles.md` covers all 5 profiles; `source-procedures.md` covers all 13 sources; `unsupported-sources.md` names at least one unsupported source.
- [ ] **Step 2: Verify FAIL.**
- [ ] **Step 3: Add deliverables index** (no overwrites).
- [ ] **Step 4: Verify PASS.**
- [ ] **Step 5: Report for review.**

## Task 8: Scope Restrictions Verification

**Files:**
- Create: `verification/scope_verification.py`
- Create: `verification/scope-verification.md`
- Test: `pipeline/tests/test_scope_verification.py`

**Interfaces:**
- Produces: `check_scope_restrictions(repo_root=None) -> list[dict]` — scans the Phase 4.1 module set for forbidden patterns (CAPTCHA bypass, automated LinkedIn fetch, application submission, external comms, Notion writes, resume edits) and returns violations.

- [ ] **Step 1: Failing test** — `check_scope_restrictions()` returns `[]`; verification doc has PASS checklist.
- [ ] **Step 2: Verify FAIL.**
- [ ] **Step 3: Implement** scanner + doc from actual inspection.
- [ ] **Step 4: Verify PASS.**
- [ ] **Step 5: Report for review.**

---

## Whole-Branch Review

After Task 8: full `pipeline/tests` suite, cross-task consistency (imports, names, JSON validity), no placeholders, no secrets/personal data, plan coverage. Verdict recorded in `verification/scope-verification.md` appendix or final report.

## Commit Policy

Local only. The lead does not commit or push without explicit user approval because `deliverables/` and `demonstration/` contain personal career-search material and the repository is public.
