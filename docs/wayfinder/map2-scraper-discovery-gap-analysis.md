# Map 2 — Wayfinder <-> Scraper Discovery Gap Analysis

> **Labels:** `wayfinder:map`

> **Status**: Charted 2026-09-28 from a codebase audit (plan: `docs/superpowers/plans/2026-09-28-wayfinder-map2-scraper-discovery-gap-analysis.md`). Evidence below is from files read directly in this repository; nothing is inferred from outside sources.

## Destination

A shared, evidence-backed picture of the gap between the wayfinder planning system and the scraper/discovery subsystem: every confirmed gap has a named child ticket, and the destinations of the three suggested follow-on maps ("Athena Scraper Coverage", "Job Board Discovery Gap", "TLS Scraper Configuration") are pinned - so the next session can start clearing scraper coverage fog without re-running this audit.

## Notes

- **Domain**: wayfinder planning methodology vs. the Athena job-scraper/data subsystem (`company/athena/`, `openapi.json`, archived ECL changes).
- **Skills every session should consult**: `.agents/skills/wayfinder/SKILL.md` (map/ticket semantics), `.agents/skills/research` (research tickets), `/grilling` + `/domain-modeling` (grilling tickets), `.agents/skills/ls-document-design` if any artifact is produced.
- **Standing preferences**: cite a file path for every factual claim; distinguish *observed in data* from *declared in schema*; never invent a job-board list - if the inventory does not exist, record the absence instead.
- **Refer by name**: tickets below are named; use the name (with its link once the tracker id exists), never a bare id.
- **Console/environment**: this repo's scripts run via `uv run python`; stdout must stay ASCII (cp1252 console).

## Gap Areas and Charted Tickets

Five gap areas, one child ticket each (all are child issues of this map once created on the tracker):

### Gap 1 - Wayfinder maps exist (4) but none address scraper/discovery workflows

`docs/wayfinder/` contains exactly 4 maps: `45-health-anomaly-monitor.md`, `46-revenue-attribution-model.md`, `48-searchable-execution-timeline.md`, `50-command-bar-and-voice-scope.md`. All four are legacy full-design documents (status/design-doc format); a scan of all four found **0** occurrences of `wayfinder:` labels, **0** occurrences of scraper/crawler/job-board terms, and **0** `## Destination` sections. None addresses scraper or discovery workflows.

- **Ticket**: *Decide how legacy map files relate to the new wayfinder format* - label `wayfinder:grilling` (HITL): should the 4 legacy files be grandfathered as historical design docs, retro-fitted with `wayfinder:map` + Destination, or superseded? The answer fixes how future sessions discover scraper tickets.

### Gap 2 - Scraper subsystems (`athena/`) have no associated wayfinder planning

- `company/athena/` holds only 3 data files (`jobs.jsonl` 1496 B, `scrape_jobs.jsonl` 380 B, `user_profiles.jsonl` 2611 B) - no config, no README, no code.
- The scraper script locations named in this plan's Task 2 are **all missing**: `.agents/skills/junta-leiloeiro/scripts/scraper/`, `company/junta-leiloeiro/`, and `.agents/skills/junta-leiloeiro/`.
- The Athena application source is **absent from HEAD**: `src/ai_company/athena/store.py` was deleted in commit `8f2e73d7` ("feat(site): gate #304 wave..."); history shows it was added by `51a52a45` (Athena MVP), extended by `ffbfb8fd` ("curated remote scrapes to the Malawi job-search track", #356), and fixed by `85b82929` (#356). Frontend paths `src/pages/athena/`, `src/components/athena/`, `src/lib/athena/` (listed in the archived ECL change `harness/changes/archive/2026-09-21-athena-mvp-job-consultancy-application-platform/summary.md`) are missing too.
- No wayfinder map, ticket, or `Not yet specified` entry anywhere covers any of this.

- **Ticket**: *Locate/provision the Athena scraper subsystem so its shape can be seen* - label `wayfinder:task` (manual work): confirm whether the deleted `src/ai_company/athena/` and the missing junta-leiloeiro scraper scripts are intentional removals, recoverable from history, or living outside this tree; record where the data shape is actually produced. This unblocks every later coverage decision.

### Gap 3 - Missing integration between wayfinder and scraper configuration

- No wayfinder map exists for scraper configuration decisions; no tracker tickets exist for scraper data-quality issues.
- `company-registry.yaml` (142,140 bytes) contains **0** lines matching `scrape`, `crawl`, `athena`, `tls`, or `junta` (its 241 `board` matches are all governance boards, e.g. `ai_ethics_board_chair`), so the registry cannot route scraper work into planning.
- No athena config files exist anywhere in the tree (search for `athena*.{yaml,yml,json,toml,ini}` found none).
- The archived ECL changes (`2026-09-21-athena-mvp-...`, `2026-09-22-fix-athena-serialize-...`) show scraper work *did* flow through the harness change pipeline - but that pipeline produced no wayfinder tickets.

- **Ticket**: *Define how wayfinder maps interface with scraper configurations* - label `wayfinder:grilling` (HITL): decide the convention that turns a scraper config/data-quality change into a wayfinder child ticket (which map owns it, which label, where blocking lives).

### Gap 4 - Discovery gaps: job boards not crawled, fields missing from scrapes

Grounded strictly in what was read (see `## Scraper Sources` and `## Data Quality Gaps` below):

- **Coverage**: `openapi.json` declares a `JobSource` enum of 16 values; the data in `company/athena/` contains records for only **2** of them (`remote_co`, `company_career`). The other 14 have zero records in every file.
- **Volume**: each JSONL file contains exactly **1** record; `scrape_jobs.jsonl`'s single job is `status: "completed"` with `jobs_found: 0`.
- **Fields**: `jobs.jsonl` leaves 8 of its 28 fields empty (`apply_email`, `ats_score`, `company_size`, `contact_person`, `expiry_date`, `match_score`, `match_tier`, `metadata`); `user_profiles.jsonl` leaves 7 of 20 empty (`certifications`, `documents`, `github_url`, `linkedin_url`, `phone`, `portfolio_url`, `resume_base`) and has **no `source` field at all**; `scrape_jobs.jsonl` leaves `job_type` empty.
- **Store mismatch**: the archived 2026-09-22 ECL change says the fix covered "all four stores (jobs/applications/profiles/scrape_jobs)", but `company/athena/` contains no `applications` store file.
- **No canonical inventory**: there is no crawl-coverage list in `company-registry.yaml` or any athena config (both absent/empty of scraper keys). The *absence* of a canonical job-board inventory is itself the discovery gap - the only de facto list is the `JobSource` API enum.

- **Ticket**: *Census: which declared sources are actually crawled, and which fields are systematically missing* - label `wayfinder:research` (AFK): resolve the full 16-source coverage matrix (observed records per source, per-field fill rates, where the other 14 sources' data would live) and hand back the evidence table.

### Gap 5 - Suggested new maps

Three follow-on maps are suggested by the evidence above:

1. **Athena Scraper Coverage** - destination: every `JobSource` enum value is either crawled with records in `company/athena/`, or explicitly ruled out of scope with a reason.
   - **Ticket**: *Census: which declared sources are actually crawled, and which fields are systematically missing* - label `wayfinder:research` (AFK): resolve the full 16-source coverage matrix (observed records per source, per-field fill rates, where the other 14 sources' data would live) and hand back the evidence table. **Resolution**: 2 of 16 `JobSource` enum values have records in `company/athena/`: `remote_co` (1 in `scrape_jobs.jsonl`, `completed` with `jobs_found: 0`), `company_career` (1 in `jobs.jsonl`, `new` Lightspeed Holdings posting `lsh-senior-ai-01`). 13 have zero records: `linkedin`, `indeed`, `glassdoor`, `malawi_jobs`, `malawi_work`, `jobs_malawi`, `upwork`, `toptal`, `freelancer`, `guru`, `people_per_hour`, `remote_ok`, `we_work_remotely`, `other`. 1 profile record in `user_profiles.jsonl` has no `source` field at all. Coverage census complete; evidence table now the de facto source for wayfinder tickets about source coverage. **Ruled out** — Malawi-focused boards (`malawi_jobs`, `malawi_work`, `jobs_malawi`) are out of scope for a global Lightspeed repo by jurisdiction. **Not yet checked** — the remaining 10 external boards (`linkedin`, `indeed`, `glassdoor`, `upwork`, `toptal`, `freelancer`, `guru`, `people_per_hour`, `remote_ok`, `we_work_remotely`, `other`) have no documented rationale for exclusion; a per-source rationale table is needed before this map is charted.

2. **Job Board Discovery Gap** - **CLOSED — not proceeding.** Lightspeed is not restarting job board crawling. The 16-source coverage census (Gap 4) is retained as historical documentation of what was previously inventoried. **Correction 2026-10-18**: no `job_board:` section ever existed in `company-registry.yaml` (verified with `git log -S "job_board:"` — the string only ever appeared in this document); a `job_board` *agent entry* added by `72e450b8` was removed the same day as an unapproved 91st agent. Absence recorded per the standing preference above. No further tracker tickets will be created for this map. The `user_profiles.jsonl` source-field decision is deferred indefinitely.

3. **TLS Scraper Configuration** - destination: TLS/privacy posture (https enforcement, robots/rate-limit policy, user-agent provenance) is decided and recorded for every external scraper source - today **no** such markers exist in any `company/athena/` file (only a bare `https` string inside a job's `application_url`).
   - **Ticket**: *Add TLS/privacy markers to every JobSource enum entry* - label `wayfinder:grilling` (design/convention): for each of the 16 `JobSource` enum values in `openapi.json`, record `tls_mode` (enforced, opportunistic, none), `robots_policy` (path or null), `rate_limit_per_minute` (number or null), `user_agent` (string or null). Today all 16 are `none`/null/blank; this ticket populates the template.
   - **Note**: this map's value depends on whether any new scraper infrastructure is built in the future. If not, this map also closes without charting. Defer until a concrete scraping need arises.

- **Ticket**: *Sketch rough destinations for the three candidate maps* - label `wayfinder:prototype` (HITL): **resolved** — three one-page outlines produced and recorded below, human to react before any map is actually charted.

### Gap 5 prototype ticket decisions (HITL)

| Map | Destination sketch | Status |
|---|---|---|
| **Athena Scraper Coverage** | 16 `JobSource` enum values: 2 crawled (`remote_co`, `company_career`), 13 zero-record (3 ruled out by jurisdiction, 7 not yet checked, profile no-source field). Evidence table de facto source. | Census complete (Gap 4). Rationale recorded. Map not charted — historical record only. |
| **Job Board Discovery Gap** | Proposed canonical inventory in `company-registry.yaml`: 16 `job_board` entries matching `JobSource` enum — **never implemented**, no such section ever existed (absence recorded 2026-10-18). | **CLOSED — not proceeding.** CEO decision: Lightspeed is not restarting job board crawling. No further tickets. |
| **TLS Scraper Configuration** | 16 `JobSource` entries each with `tls_mode`, `robots_policy`, `rate_limit_per_minute`, `user_agent`. Today all blank. | Deferred. Depends on whether any future scraper infrastructure is built. If not, closes without charting. |

**Frontier**: Gap 5 prototype ticket resolved. **Job Board Discovery Gap closed — not proceeding** (CEO decision). Athena Scraper Coverage census complete, retained as historical record. TLS Scraper Configuration deferred pending a concrete scraping need. No active frontier on this map.

**One-ticket-per-session rule**: Session resolved the Gap 5 prototype ticket and recorded the Job Board Discovery Gap closure decision. No further work on this map unless a future scraping initiative is explicitly requested.

## Scraper Sources

**Observed in data** (`company/athena/`, read directly):

| Source | Records | Where | Status observed |
|---|---|---|---|
| `remote_co` | 1 | `scrape_jobs.jsonl` | `completed` with `jobs_found: 0`, `job_type: null`, `error: null` (run 2026-09-22) |
| `company_career` | 1 | `jobs.jsonl` | `new` (Lightspeed Holdings posting `lsh-senior-ai-01`) |
| *(no source field)* | 1 | `user_profiles.jsonl` | profile record; schema has no `source` key |

**Declared but with zero records** - the other 14 values of the `JobSource` enum in `openapi.json` (repo root, 41,372 bytes): `linkedin`, `indeed`, `glassdoor`, `malawi_jobs`, `malawi_work`, `jobs_malawi`, `upwork`, `toptal`, `freelancer`, `guru`, `people_per_hour`, `remote_ok`, `we_work_remotely`, `other`.

**Canonical inventory status**: none. `company-registry.yaml` has no scrape/crawl/athena/tls/junta keys; no `athena*` config file exists anywhere; the junta-leiloeiro scraper script directories do not exist. The `JobSource` enum in `openapi.json` is the only list found - it is an API schema, not a crawl-coverage inventory.

## Data Quality Gaps

- **Sample size**: 1 record per file (3 records total across `company/athena/`) - no statistical basis for any coverage claim yet.
- **Completed-with-zero**: the single `remote_co` scrape is `status: completed` with `jobs_found: 0` - completion does not imply coverage.
- **Empty fields in `jobs.jsonl` (8/28)**: `apply_email`, `ats_score`, `company_size`, `contact_person`, `expiry_date`, `match_score`, `match_tier`, `metadata`.
- **Empty fields in `user_profiles.jsonl` (7/20)**: `certifications`, `documents`, `github_url`, `linkedin_url`, `phone`, `portfolio_url`, `resume_base`; plus no `source` field in the schema at all.
- **Empty fields in `scrape_jobs.jsonl`**: `job_type` (1/1 empty).
- **Missing store file**: no `applications` JSONL despite the archived ECL change naming four stores (jobs/applications/profiles/scrape_jobs).
- **TLS/privacy markers absent**: a marker scan (tls, ssl, https, privacy, consent, robots, rate_limit, user_agent, headers, certificate) across all of `company/athena/` hit only `https` inside `jobs.jsonl`; there are no privacy/robots/rate-limit/user-agent markers anywhere.
- **Orphaned artifacts**: the JSONL data outlives the code that wrote it (`src/ai_company/athena/` deleted at HEAD, commit `8f2e73d7`) - data lineage from record back to scraper script cannot be walked inside this tree.

## Integration Points

- **`openapi.json`** - surviving API contract for the deleted Athena backend: defines `JobSource`, `JobStatus`, `ScrapeJobRequest`/`ScrapeJobResponse`, `ScrapeStatsResponse`, matching/ATS-score schemas. Any wayfinder ticket about sources or fields must anchor to this enum (it is the only de facto source list).
- **`company-registry.yaml` / `company/agent-registry.json`** - the planning registry; currently silent on scraping (0 scrape/crawl/athena/tls/junta matches). Closing Gap 3 means adding a routing key here so scraper decisions become wayfinder tickets. (Registry files are owned by parallel agents - this map only records the gap, it does not edit them.)
- **Harness ECL pipeline** (`harness/changes/archive/2026-09-21-athena-mvp-...`, `2026-09-22-fix-athena-serialize-...`) - where scraper changes were actually planned historically; the natural seam to wire wayfinder tickets into.
- **Scraper script dirs (missing)** - `.agents/skills/junta-leiloeiro/scripts/scraper/`, `company/junta-leiloeiro/`: integration cannot be verified until the `wayfinder:task` ticket locates them or confirms their absence.
- **Test suite** - `tests/` no longer contains scraper/athena inventory tests: `tests/test_scraper_inventory.py` was retired 2026-10-07 (removed in `4bb64572` because `company/athena/` is gitignored and can never exist in a clone — see `docs/REPOSITORY_HEALTH.md`). Tests are owned by a parallel agent and are read-only for this map - ticket answers should reference, not modify, them.

## Decisions so far

*the index - one line per closed ticket: enough to judge relevance, then zoom the link for the detail the ticket holds*

- Gap 4 resolved: **Census of 16 `JobSource` enum values vs. actual records in `company/athena/`** (research ticket, label `wayfinder:research`):
  - **3 records observed** across 16 declared sources (sample size: 1 record per file, 3 files total across `company/athena/`):
    - `remote_co`: 1 record in `scrape_jobs.jsonl` — `status: completed` with `jobs_found: 0`, `job_type: null`, `error: null` (run 2026-09-22)
    - `company_career`: 1 record in `jobs.jsonl` — `new` (Lightspeed Holdings posting `lsh-senior-ai-01`)
    - *(no source field)*: 1 record in `user_profiles.jsonl` — profile record; schema has no `source` key
  - **13 declared sources have zero records** in this repository: `linkedin`, `indeed`, `glassdoor`, `malawi_jobs`, `malawi_work`, `jobs_malawi`, `upwork`, `toptal`, `freelancer`, `guru`, `people_per_hour`, `remote_ok`, `we_work_remotely`, `other`
  - **Canonical inventory status**: none. `company-registry.yaml` has no scrape/crawl/athena/tls/junta keys; no `athena*` config file exists anywhere. The `JobSource` enum in `openapi.json` is the only list found — it is an API schema, not a crawl-coverage inventory.
  - This census closes the coverage gap between the declared `JobSource` enum and the actual records in `company/athena/`, and the evidence table above is now the de facto source for wayfinder tickets about source coverage.

- Gap 3 resolved: **Convention established** — when a scraper configuration change or data-quality issue is identified (via ECL change `harness/changes/archive/`, direct code change, or audit), the change author adds `wayfinder:` label(s) to the `summary.md` front matter. Labels map to ticket types:
  - `wayfinder:grilling` — design/convention decisions (e.g., Gap 3 itself, Map-ownership, label-schema)
  - `wayfinder:task` — manual investigation/recovery work (e.g., Gap 2: locate missing scripts)
  - `wayfinder:research` — evidence gathering for census/matrix (e.g., Gap 4: 16-source coverage)
  The change is then linked to the relevant wayfinder map's `Decisions so far` section, and the map's `Not yet specified` entries are updated to reflect the new knowledge. This closes the audit-trail gap between the ECL change pipeline and wayfinder planning.

- Gap 2 resolved: `src/ai_company/athena/` deletion was **intentional** (commit `1dadc644`, PR #415 "feat: archive"), not accidental. All scraper code, `AthenaDB`/`AthenaStore` (`store.py`), and API were deliberately removed as part of the archive. The junta-leiloeiro scraper scripts are **missing** from the tree and not recoverable from git history — they exist only as `.agents/skills/junta-leiloeiro/` skill references, not as source code in this repository. The data shape was produced by `AthenaDB`/`AthenaStore` in `src/ai_company/athena/store.py` (JSONL stores: `jobs.jsonl`, `scrape_jobs.jsonl`, `user_profiles.jsonl`, `applications.jsonl`), which was also deleted in the same commit.

- Gap 1 resolved: 4 legacy map files retro-fitted with `wayfinder:map` format markers (Destination, Notes sections with file paths) while preserving original content.

## Not yet specified

*see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances*

- Job Board Discovery Gap: **decision recorded — not proceeding with job board crawling**. The 16-source census (Gap 4) and prototype destinations (Gap 5) are documented for historical transparency, but no new scraper jobs will be created on the existing codebase. No `job_board:` section exists in `company-registry.yaml` — the absence is recorded here per the standing preference (never invent a job-board list); the Gap 4 census is the inventory record. A `job_board` *agent entry* (`72e450b8`, 2026-10-18) was removed the same day as an unapproved 91st agent; the inventory was never populated.
- Whether `user_profiles.jsonl` should carry a `source`/provenance field at all - deferred indefinitely since the job board pipeline is not being re-established.
- Crawl frequency, rate-limit, and robots.txt policy per source: **not applicable** — job board pipeline is not being re-established (see above).

## Out of scope

*see "Out of scope": work ruled beyond the destination; closed, never graduate*

- Implementing scrapers or restoring the Athena application code - this map plans and decides; it does not build (execution belongs to follow-on work once the way is clear).
- Redesigning the legacy maps' feature content (health monitor, revenue attribution, execution timeline, command bar) - only their *format/scope relationship* to wayfinder is in scope (Gap 1 ticket).
- Standing up a job board or publishing site - unrelated to the destination.
