# Scraper/Discovery Wayfinder Map Template

> **Labels:** `wayfinder:map`

> **Every session**: orient to the **Destination** before choosing a ticket. The destination is the concrete outcome — not a vague intent.

---

## Destination

*What reaching the end of this map looks like — the spec, decision, or change this scraper/discovery effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.*

**Examples:**
- Complete coverage of all job boards listed in `company-registry.yaml`
- TLS certificates configured and verified for all external scrapers
- All scraper data quality gaps documented and addressed
- Integration between wayfinder maps and scraper configuration decisions complete

---

## Notes

*Domain, skills every session should consult, standing preferences for this scraper effort.*

**Skills to consult:** `.agents/skills/ls-frontend-design`, `.agents/skills/ls-diagramming`, `.agents/skills/ls-visual-storytelling`, `.agents/skills/ls-artifact-qa`

**Standing preferences:** Enforce brand tokens (navy #070A40 / red #E63946 / cyan #00BFFF), 4px spacing grid, Arial type scale; validate scraper data against company registry before committing.

---

## Decisions so far

*the index — one line per closed ticket: enough to judge relevance, then zoom the link for the detail the ticket holds*

- [ ] `<ticket title>` — <one-line gist of the answer>
  - Link: `<GitHub issue URL>`

---

## Not yet specified

*see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances*

- Which job boards from the company registry are not yet crawled
- Exact data quality metrics for scraper output validation
- Integration points between wayfinder maps and Athena scraper configs
- Optimal scraping frequency and rate limits per board

---

## Out of scope

*see "Out of scope": work ruled beyond the destination; closed, never graduate*

- Building a new job board from scratch
- Developing proprietary search algorithms
- Creating a standalone job board website

---

## Scraper Sources

*list of job boards / external sources being investigated*

- `<Job board name>` — `<source URL or config reference>`
  - Registry reference: `<company-registry.yaml anchor>`
  - Last crawled: `<date>`
  - Jobs found: `<number>`

---

## Data Quality Gaps

*gaps in coverage, missing fields, incomplete data*

- `<Gap description>` — `<affected scraper/source>`
  - Missing fields: `<list of expected but missing data fields>`
  - Quality issues: `<description of data quality problems>`
  - Impact: `<how this gap affects downstream systems>`

---

## Integration Points

*how this map interfaces with existing scraper configs*

- `<Integration description>` — `<affected component>`
  - Wayfinder map reference: `<related wayfinder map>`
  - Scraper config update: `<configuration file or script>`
  - Data flow change: `<how data flows change>`
