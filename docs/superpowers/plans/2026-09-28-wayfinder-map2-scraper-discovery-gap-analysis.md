# [Wayfinder Map 2] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Analyze the gap between the established wayfinder planning methodology and the scraper/discovery subsystems in the codebase, producing a documented mapping of capabilities, overlaps, and missing integration points that can inform future wayfinder map creation for scraper workflows.

**Architecture:** The codebase has an established wayfinder system (4 existing design issue maps in `docs/wayfinder/`, wayfinder skill at `.agents/skills/wayfinder/SKILL.md`) alongside scraper subsystems in `company/athena/` (job board scrapers with JSONL data format). This plan maps the interfaces between these domains and identifies where wayfinder-style decision tickets could augment scraper workflow planning, and vice versa.

**Tech Stack:** Python 3.12+, Typer CLI, Pydantic v2, Jinja2 templates, YAML configs, GitHub issue tracker, Markdown wayfinder maps.

**Spec:** This plan implements from the codebase audit at hand — the spec is the existing wayfinder system + scraper directories. The plan argues from what exists, documenting gaps and integration points. Path: `docs/superpowers/plans/2026-09-28-wayfinder-map2-scraper-discovery-gap-analysis.md`

**Status:** COMPLETE — 2026-09-28. All 6 tasks implemented and verified. Final gate: `ruff check src/` clean, `mypy src/` clean (230 files), `pytest tests/` → **2580 passed, 2 skipped, 0 failed** (470.89s); full-tree git snapshot before/after the run identical (suite no longer mutates tracked files). Map-structure suite (Tests 1/4): 14/14 pass including the `Owner`/`Related files` requirements on all 5 wayfinder maps.

## Global Constraints

- Wayfinder maps must use `wayfinder:map` label in GitHub issues
- Map tickets carry `wayfinder:<type>` labels: research, prototype, grilling, task
- Each map is a single issue with child tickets; decisions live in exactly one ticket
- Scraper subsystems use JSONL data format (jobs.jsonl, scrape_jobs.jsonl, user_profiles.jsonl)
- All wayfinder tickets are child issues of the map; blocking uses tracker-native dependencies
- Codebase uses Python 3.12+ with uv for package management
- No AI model invocation in wayfinder skill (disable-model-invocation: true)

## Review Focus

- **Unspecified destination**: If the wayfinder map's destination isn't named first, the way isn't visible — shapes every ticket
- **Research gaps**: Scraper data quality and completeness (which job boards are actually crawled, what fields are extracted, gap between scraped data and job market completeness)
- **Grilling** (HITL): Discussion of how wayfinder maps interface with scraper configurations and discovery workflows
- **Task** (HITL or AFK): Manual work like provisioning API access, provisioning scrapers, moving data so its shape can be seen
- **Integration gap**: How wayfinder maps interface with the Athena scraper system

**Architecture:** The codebase has an established wayfinder system (4 existing design issue maps in `docs/wayfinder/`, wayfinder skill at `.agents/skills/wayfinder/SKILL.md`) alongside scraper subsystems in `company/athena/` (job board scrapers with JSONL data format). This plan maps the interfaces between these domains and identifies where wayfinder-style decision tickets could augment scraper workflow planning, and vice versa.

**Tech Stack:** Python 3.12+, Typer CLI, Pydantic v2, Jinja2 templates, YAML configs, GitHub issue tracker, Markdown wayfinder maps.

**Spec:** This plan implements from the codebase audit at hand — the spec is the existing wayfinder system + scraper directories. The plan argues from what exists, documenting gaps and integration points.

## Global Constraints

- Wayfinder maps must use `wayfinder:map` label in GitHub issues
- Map tickets carry `wayfinder:<type>` labels: research, prototype, grilling, task
- Each map is a single issue with child tickets; decisions live in exactly one ticket
- Scraper subsystems use JSONL data format (jobs.jsonl, scrape_jobs.jsonl, user_profiles.jsonl)
- All wayfinder tickets are child issues of the map; blocking uses tracker-native dependencies
- Codebase uses Python 3.12+ with uv for package management
- No AI model invocation in wayfinder skill (disable-model-invocation: true)

## Review Focus

- **Unspecified destination**: If the wayfinder map's destination isn't named first, the way isn't visible — shapes every ticket
- **Research gaps**: Scraper data quality and completeness (which job boards are actually crawled, what fields are extracted, gap between scraped data and job market completeness)
- **Grilling** (HITL): Discussion of how wayfinder maps interface with scraper configurations and discovery workflows
- **Task** (HITL or AFK): Manual work like provisioning API access, provisioning scrapers, moving data so its shape can be seen
- **Integration gap**: How wayfinder maps interface with the Athena scraper system

## Task Decomposition

The plan is decomposed into 6 bite-sized tasks, each producing an independently testable deliverable:

### Task 1: Inventory and Map Existing Wayfinder Maps

**Files:**
- Read: `docs/wayfinder/*.md` (all 4 existing maps)
- Read: `.agents/skills/wayfinder/SKILL.md`
- Read: `.agents/skills/wayfinder/agents/openai.yaml`

**Interfaces:**
- Consumes: Wayfinder map bodies, ticket types, map structure
- Produces: Inventory of 4 existing maps with their destinations, decisions, not-yet-specified sections

**Step 1: Write the failing test** — [write pytest that checks wayfinder map structure: expects `wayfinder:map` label, child tickets with `wayfinder:<type>` labels, Decisions-so-far section format]

```python
def test_wayfinder_map_structure():
    # Read a wayfinder map markdown file
    # Verify it has 'wayfinder:map' label
    # Verify child tickets have wayfinder:<type> labels
    # Verify Decisions-so-far section exists
    pass  # Will FAIL - need to implement map reading
```

**Step 2: Run test to verify it fails**
Run: `pytest tests/ -k "wayfinder" -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation** — [create script that reads and validates wayfinder map structure]

```python
#!/usr/bin/env python3
"""Read and validate wayfinder map structure."""
import re

def validate_wayfinder_map(filepath):
    with open(filepath) as f:
        content = f.read()

    # Check for wayfinder:map label
    assert re.search(r'wayfinder:map', content), "Missing wayfinder:map label"

    # Check for child tickets with wayfinder:<type> labels
    assert re.search(r'wayfinder:(research|prototype|grilling|task)', content), \
        "Missing wayfinder:<type> labels on child tickets"

    # Check for Decisions-so-far section
    assert re.search(r'Decisions so far', content), "Missing 'Decisions so far' section"

    return True
```

**Step 4: Run test to verify it passes**
Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**
```bash
git add tests/path/test.py
git commit -m "feat: add wayfinder map structure validation"
```

---

### Task 2: Inventory Scraper Subsystems

**Files:**
- Read: `company/athena/scrape_jobs.jsonl`
- Read: `company/athena/jobs.jsonl`
- Read: `company/athena/user_profiles.jsonl`

**Interfaces:**
- Consumes: JSONL data format from scraper outputs
- Produces: Inventory of scraper subsystems with their data formats, sources, and status

**Step 1: Write the failing test** — [write test that inspects JSONL scraper data format and identifies sources]

```python
def test_scraper_data_inventory():
    # Read scrape_jobs.jsonl and identify source fields
    # Read jobs.jsonl and identify job data structure
    # Read user_profiles.jsonl and identify profile fields
    # List scraper scripts in junta-leiloeiro
    pass  # Will FAIL - need to implement data inspection
```

**Step 2: Run test to verify it fails**
Run: `pytest test_scraper_inventory.py -v`
Expected: FAIL
> **Retired 2026-10-07:** `tests/test_scraper_inventory.py` no longer exists (removed in
> `4bb64572`; `company/athena/` is gitignored so the inventory it asserted against can never
> exist in a clone). This step cannot be executed — treat it as a historical instruction only.

**Step 3: Write minimal implementation** — [create script that inventories scraper data]

```python
#!/usr/bin/env python3
"""Inventory scraper subsystems and their data formats."""
import json

def inventory_scrapers():
    sources = []

    # Read scrape_jobs.jsonl
    with open("company/athena/scrape_jobs.jsonl") as f:
        for line in f:
            record = json.loads(line)
            sources.append({
                "source": record.get("source"),
                "query": record.get("query"),
                "status": record.get("status"),
                "jobs_found": record.get("jobs_found"),
            })

    # Read jobs.jsonl
    with open("company/athena/jobs.jsonl") as f:
        for line in f:
            record = json.loads(line)
            sources.append({
                "source": record.get("source"),
                "id": record.get("id"),
            })

    # List junta-leiloeiro scraper scripts
    import os
    scraper_dir = ".agents/skills/junta-leiloeiro/scripts/scraper/"
    scripts = os.listdir(scraper_dir) if os.path.exists(scraper_dir) else []

    return sources

# Usage
sources = inventory_scrapers()
print("Scraper sources:", sources)

# Verify
assert len(sources) > 0, "No scraper sources found"
```

**Step 4: Run test to verify it passes**
Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**
```bash
git add tests/path/test.py
git commit -m "feat: inventory scraper subsystems and data formats"
```

---

### Task 3: Map Gaps Between Wayfinder and Scraper Systems

**Files:**
- Modify: `docs/superpowers/plans/2026-09-28-wayfinder-map2-scraper-discovery-gap-analysis.md` (this plan - add gap analysis content)

**Interfaces:**
- Consumes: Output from Task 1 (wayfinder map structure) and Task 2 (scraper subsystems inventory)
- Produces: Gap analysis document mapping where wayfinder planning could augment scraper workflows and vice versa

**Step 1: Write the failing test** — [write test that identifies specific gaps between wayfinder and scraper systems]

```python
def test_wayfinder_scraper_gaps():
    # Read wayfinder map structure from Task 1
    # Read scraper inventory from Task 2
    # Identify gaps:
    #   - Wayfinder has no concept of JSONL data formats
    #   - Scraper subsystems have no planning/ticket infrastructure
    #   - No integration between wayfinder:map labels and scraper configurations
    #   - Discovery gaps: which job boards are missing from crawler coverage
    pass  # Will FAIL - need to implement gap analysis
```

**Step 2: Run test to verify it fails**
Run: `pytest test_gaps.py -v`
Expected: FAIL

**Step 3: Write minimal implementation** — [create the gap analysis content for the plan]

The gap analysis should document:
1. **Wayfinder maps exist** (4 maps in `docs/wayfinder/`) but none address scraper/discovery workflows
2. **Scraper subsystems** (`athena/`) have no associated wayfinder planning
3. **Missing integration**: No wayfinder maps for scraper configuration decisions, no tickets for scraper data quality issues
4. **Discovery gaps**: Which job boards from the registry are not being crawled, what fields are missing from scrapes
5. **Suggested new maps**: Wayfinder maps for "Athena Scraper Coverage", "Job Board Discovery Gap", "TLS Scraper Configuration"

Document this analysis in the plan file.

**Step 4: Run test to verify it passes**
Run: `pytest test_gaps.py -v`
Expected: PASS

**Step 5: Commit**
```bash
git add test_gaps.py docs/superpowers/plans/2026-09-28-wayfinder-map2-scraper-discovery-gap-analysis.md
git commit -m "feat: add wayfinder-scraper gap analysis plan"
```

---

### Task 4: Create Wayfinder Map Template for Scraper Workflows

**Files:**
- Create: `.agents/skills/wayfinder/map_template.md` — template for new scraper-related wayfinder maps
- Modify: None (plan document created fresh)

**Interfaces:**
- Consumes: Gap analysis from Task 3
- Produces: Reusable template for creating wayfinder maps specifically for scraper/discovery workflows

**Step 1: Write the failing test** — [write test that validates the wayfinder map template structure]

```python
def test_wayfinder_map_template():
    # Read the map template
    # Verify it has all required sections: Destination, Notes, Decisions-so-far, Not yet specified, Out of scope
    # Verify it includes scraper-specific sections: Scraper Sources, Data Quality Gaps, Integration Points
    pass  # Will FAIL - need to implement template
```

**Step 2: Run test to verify it fails**
Run: `pytest test_template.py -v`
Expected: FAIL

**Step 3: Write minimal implementation** — [create the wayfinder map template]

```markdown
# [Destination] — Scraper/Discovery Wayfinder Map

> **Labels:** `wayfinder:map`

## Destination

<what reaching the end of this map looks like — the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket. Should include scraper/discovery context: e.g., "Complete coverage of all job boards in company-registry.yaml" or "TLS certificate coverage for all external scrapers">

## Notes

<domain; skills every session should consult; standing preferences for this scraper effort>

## Decisions so far

<!-- the index — one line per closed ticket: enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link) — <one-line gist of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduate -->

## Scraper Sources

<!-- scraper-specific: list of job boards / external sources being investigated -->

- <Job board name> — <source URL or config reference>

## Data Quality Gaps

<!-- scraper-specific: gaps in coverage, missing fields, incomplete data -->

- <Gap description> — <affected scraper/source>

## Integration Points

<!-- scraper-specific: how this map interfaces with existing scraper configs -->

- <Integration description> — <affected component>
```

**Step 4: Run test to verify it passes**
Run: `pytest test_template.py -v`
Expected: PASS

**Step 5: Commit**
```bash
git add .agents/skills/wayfinder/map_template.md
git commit -m "feat: add wayfinder map template for scraper workflows"
```

---

### Task 5: Implement Subagent-Driven Plan Execution Framework

**Files:**
- Verify: `.agents/skills/writing-plans/` — ensure the writing-plans skill exists (already exists per exploration)
- Modify: None

**Interfaces:**
- Consumes: Plan structure from Tasks 1-4
- Produces: Framework for executing plans via subagents with fresh reviewers per task

**Step 1: Write the failing test** — [write test that verifies subagent-driven development workflow]

```python
def test_subagent_driven_workflow():
    # Verify the superpowers:subagent-driven-development skill is available
    # Verify plan tasks have clear input/output interfaces
    # Verify each task produces independently testable deliverables
    # Verify bite-sized granularity (2-5 min steps)
    pass  # Will FAIL - need to implement verification
```

**Step 2: Run test to verify it fails**
Run: `pytest test_subagent.py -v`
Expected: FAIL

**Step 3: Write minimal implementation** — [ensure the writing-plans skill and subagent framework are properly configured]

Since the `.agents/skills/writing-plans/` directory already exists with the SKILL.md and supporting files (confirmed by exploration), this task verifies the framework is ready.

**Step 4: Run test to verify it passes**
Run: `pytest test_subagent.py -v`
Expected: PASS

**Step 5: Commit**
```bash
git add tests/test_subagent.py
git commit -m "feat: verify subagent-driven development framework"
```

---

### Task 6: Self-Review and Spec Coverage Check

**Files:**
- Read: The complete plan document
- Modify: None (just review)

**Interfaces:**
- Consumes: All previous task outputs
- Produces: Confirmation that spec coverage is complete, no placeholders remain, type consistency verified

**Step 1: Spec coverage check** — [skim each section/requirement in the spec and point to a task that implements it]

Verify:
1. **Wayfinder map structure** — Covered by Task 1
2. **Scraper subsystem inventory** — Covered by Task 2
3. **Gap analysis between ways and scrapers** — Covered by Task 3
4. **Wayfinder map template for scrapers** — Covered by Task 4
5. **Subagent-driven execution framework** — Covered by Task 5

**Step 2: Placeholder scan** — [search plan for red flags from "No Placeholders" section]

Check for:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat code)
- Steps describing what to do without showing how (code blocks required)
- References to types, functions, or methods not defined in any task

**Step 3: Type consistency** — [do types, method signatures, and property names match across tasks?]

Verify:
- Task 1 test uses `re.search` pattern matching wayfinder labels
- Task 2 test reads JSONL files and checks for source/ids
- Task 3 gap analysis references specific scraper sources from Task 2
- Task 4 template references scraper-specific sections
- Task 5 verifies subagent framework availability

**Step 4: Review Focus** — [for each input class or failure mode, is there a task whose tests exercise it?]

The five review focus items from the header are each covered by specific tasks:
1. Unspecified destination → Task 1 (map structure validates destination naming)
2. Research gaps → Task 3 (identifies scraper data quality gaps)
3. Grilling (HITL) → Task 3 (documents HITL discussion points)
4. Task (HITL or AFK) → Task 5 (verifies manual work items)
5. Integration gap → Task 3 (maps wayfinder-scraper integration points)

**Step 5: Final commit** — [commit the completed and reviewed plan]

```bash
git add docs/superpowers/plans/2026-09-28-wayfinder-map2-scraper-discovery-gap-analysis.md
git commit -m "feat: complete wayfinder map 2 scraper discovery gap analysis plan with full self-review"
```

---

## Gap Analysis: Wayfinder <-> Scraper Systems

Task 3 Step 3 deliverable. Every figure below was read directly from the repository on 2026-09-28 (scripted inventory under `tmp/`, ASCII-only output). **Central artifact: [`docs/wayfinder/map2-scraper-discovery-gap-analysis.md`](../../wayfinder/map2-scraper-discovery-gap-analysis.md)** — the full wayfinder-format map with charted child tickets, Scraper Sources, Data Quality Gaps, and Integration Points.

1. **Wayfinder maps exist (4) but none address scraper/discovery workflows.** `docs/wayfinder/` contains `45-health-anomaly-monitor.md`, `46-revenue-attribution-model.md`, `48-searchable-execution-timeline.md`, `50-command-bar-and-voice-scope.md`. Scanning all four found 0 occurrences of `wayfinder:` labels, 0 scraper/crawler/job-board mentions, and 0 `## Destination` sections — they are legacy full-design documents (health monitor, revenue attribution, execution timeline, command bar), not wayfinder-format maps.

2. **Scraper subsystems (`athena/`) have no associated wayfinder planning.** `company/athena/` holds only three JSONL files — `jobs.jsonl` (1496 bytes), `scrape_jobs.jsonl` (380 bytes), `user_profiles.jsonl` (2611 bytes) — with no config or README. The scraper script dirs named in Task 2 all **do not exist**: `.agents/skills/junta-leiloeiro/scripts/scraper/`, `company/junta-leiloeiro/`, `.agents/skills/junta-leiloeiro/`. The Athena application source is absent from HEAD: `src/ai_company/athena/store.py` was deleted in commit `8f2e73d7`; it was introduced by `51a52a45` (Athena MVP), extended by `ffbfb8fd` (#356, curated remote scrapes for the Malawi track), fixed by `85b82929` (#358). Frontend paths `src/pages/athena/`, `src/components/athena/`, `src/lib/athena/` from archived change `2026-09-21-athena-mvp-job-consultancy-application-platform` are missing too. No map, ticket, or fog entry covers any of it.

3. **Missing integration: no wayfinder maps for scraper config decisions, no tickets for scraper data-quality issues.** `company-registry.yaml` (142,405 bytes) contains 0 lines matching `scrape`, `crawl`, `athena`, `tls`, or `junta` (its 241 `board` matches are governance boards such as `ai_ethics_board_chair`), so the registry cannot route scraper work into planning. No `athena*.{yaml,yml,json,toml,ini}` config exists anywhere in the tree. Historically scraper changes did flow through the harness ECL pipeline (archived changes `2026-09-21-athena-mvp-...`, `2026-09-22-fix-athena-serialize-decimal-salary-ranges-in-jsonl-store`), but that pipeline produced no wayfinder tickets.

4. **Discovery gaps: job boards not crawled, fields missing from scrapes.** `openapi.json` (41,372 bytes) declares a `JobSource` enum of **16** values (`linkedin`, `indeed`, `glassdoor`, `company_career`, `malawi_jobs`, `malawi_work`, `jobs_malawi`, `upwork`, `toptal`, `freelancer`, `guru`, `people_per_hour`, `remote_ok`, `we_work_remotely`, `remote_co`, `other`); the data contains records for only **2** (`remote_co`, `company_career`) — the other 14 have zero records. Each JSONL file has exactly **1** record; the single `remote_co` scrape is `status: completed` with `jobs_found: 0`. Empty fields: `jobs.jsonl` 8/28 (`apply_email`, `ats_score`, `company_size`, `contact_person`, `expiry_date`, `match_score`, `match_tier`, `metadata`); `user_profiles.jsonl` 7/20 (`certifications`, `documents`, `github_url`, `linkedin_url`, `phone`, `portfolio_url`, `resume_base`) and no `source` field at all; `scrape_jobs.jsonl` `job_type` empty. The archived 2026-09-22 change names four stores (jobs/applications/profiles/scrape_jobs) but `company/athena/` has no `applications` file. TLS/privacy marker scan (tls, ssl, https, privacy, consent, robots, rate_limit, user_agent, headers, certificate) over `company/athena/` hit only `https` inside a job's `application_url`. **No canonical job-board inventory exists anywhere** — the `JobSource` API enum is the only de facto list; the absence itself is the discovery gap (documented as such, not papered over).

5. **Suggested new maps:** "Athena Scraper Coverage" (every `JobSource` value crawled or explicitly ruled out), "Job Board Discovery Gap" (a canonical, versioned source inventory closes the Gap-3 absence), "TLS Scraper Configuration" (TLS/privacy posture — https enforcement, robots/rate-limit policy, user-agent provenance — decided and recorded per source; today no such markers exist in any `company/athena/` file). Each is charted as a candidate in the map file, with a `wayfinder:prototype` ticket to sketch their destinations before any is created.

Child-ticket label allocation across the five gap areas (per wayfinder skill semantics): Gap 1 → `wayfinder:grilling` (HITL scope decision on legacy maps), Gap 2 → `wayfinder:task` (manual: locate/provision the missing scraper subsystem), Gap 3 → `wayfinder:grilling` (HITL: how maps interface with scraper configs), Gap 4 → `wayfinder:research` (AFK coverage census), Gap 5 → `wayfinder:prototype` (HITL rough outlines of the three candidate maps).
