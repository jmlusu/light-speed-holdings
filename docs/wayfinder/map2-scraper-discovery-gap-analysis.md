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
- The Athena application source is **absent from HEAD**: `src/ai_company/athena/store.py` was deleted in commit `8f2e73d7` ("feat(site): gate #304 wave..."); history shows it was added by `51a52a45` (Athena MVP), extended by `ffbfb8fd` ("curated remote scrapes to the Malawi job-search track", #356), and fixed by `85b82929` (#358). Frontend paths `src/pages/athena/`, `src/components/athena/`, `src/lib/athena/` (listed in the archived ECL change `harness/changes/archive/2026-09-21-athena-mvp-job-consultancy-application-platform/summary.md`) are missing too.
- No wayfinder map, ticket, or `Not yet specified` entry anywhere covers any of this.

- **Ticket**: *Locate/provision the Athena scraper subsystem so its shape can be seen* - label `wayfinder:task` (manual work): confirm whether the deleted `src/ai_company/athena/` and the missing junta-leiloeiro scraper scripts are intentional removals, recoverable from history, or living outside this tree; record where the data shape is actually produced. This unblocks every later coverage decision.

### Gap 3 - Missing integration between wayfinder and scraper configuration

- No wayfinder map exists for scraper configuration decisions; no tracker tickets exist for scraper data-quality issues.
- `company-registry.yaml` (142,405 bytes) contains **0** lines matching `scrape`, `crawl`, `athena`, `tls`, or `junta` (its 241 `board` matches are all governance boards, e.g. `ai_ethics_board_chair`), so the registry cannot route scraper work into planning.
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
2. **Job Board Discovery Gap** - destination: a canonical, versioned job-board/source inventory exists in the registry (the absence found in Gap 3 is closed), with each board's crawl status recorded.
3. **TLS Scraper Configuration** - destination: TLS/privacy posture (https enforcement, robots/rate-limit policy, user-agent provenance) is decided and recorded for every external scraper source - today **no** such markers exist in any `company/athena/` file (only a bare `https` string inside a job's `application_url`).

- **Ticket**: *Sketch rough destinations for the three candidate maps* - label `wayfinder:prototype` (HITL): produce a cheap one-page outline per candidate map (destination + first 3 tickets) for the human to react to before any map is actually charted.

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
- **Test suite** - `tests/` contains scraper/athena tests (e.g. `tests/test_scraper_inventory.py`); tests are owned by a parallel agent and are read-only for this map - ticket answers should reference, not modify, them.

## Decisions so far

*the index - one line per closed ticket: enough to judge relevance, then zoom the link for the detail the ticket holds*

- No tickets closed yet - this map was charted from the audit recorded above; the evidence in the gap areas is charting-session output, not a resolved ticket.

## Not yet specified

*see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances*

- Whether deletion of `src/ai_company/athena/` (commit `8f2e73d7`) was an intentional retirement or an accidental loss - owner intent is unknown from the tree alone, and the answer reshapes several tickets above.
- Whether Athena data exists outside this repository (the 1-record files may be fixtures rather than the real corpus) - can't be pinned down without knowing where the runtime wrote its stores.
- Crawl frequency, rate-limit, and robots.txt policy per source - no config exists to read; too coarse to ticket until the coverage census (Gap 4 research ticket) returns.
- Whether `user_profiles.jsonl` should carry a `source`/provenance field at all - depends on the destination chosen for the Job Board Discovery Gap map.

## Out of scope

*see "Out of scope": work ruled beyond the destination; closed, never graduate*

- Implementing scrapers or restoring the Athena application code - this map plans and decides; it does not build (execution belongs to follow-on work once the way is clear).
- Redesigning the legacy maps' feature content (health monitor, revenue attribution, execution timeline, command bar) - only their *format/scope relationship* to wayfinder is in scope (Gap 1 ticket).
- Standing up a job board or publishing site - unrelated to the destination.
