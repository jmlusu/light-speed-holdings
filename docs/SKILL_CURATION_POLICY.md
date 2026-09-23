# Skill Curation Policy

**Version:** 1.1
**Date:** 2026-09-23
**Owner:** Chief of Staff
**Status:** Active
**CISO of record:** Jack Mlusu (Human CEO)

---

## Purpose

This document defines the policy for adding, vetting, and managing skills in the OpenCode agent ecosystem without modifying `AGENTS.md`. Skills are auto-discovered from `.agents/skills/` — this policy governs *which* skills enter that directory and *how*.

---

## Governance Model

| Role | Responsibility |
|------|----------------|
| **Chief of Staff** | Owns this policy, approves additions, runs monthly audits |
| **Registry Owner** | Executes vetting checklist, runs `skill-check`, updates manifests |
| **Generator Owner** | Validates skill format compatibility with OpenCode |
| **QA Lead** | Tests skill activation in fresh sessions |

---

## Skill Discovery Mechanism (Verified)

> **OpenCode scans `.agents/skills/` at session start.** No `opencode.json` required. `AGENTS.md` is a human guide only — never read by the runtime.

**Implication:** Adding a skill folder to `.agents/skills/` makes it immediately available. The policy focus is *governance*, not config.

---

## Vetting Checklist (Mandatory for Every New Skill)

### 1. Identity & Collision Check
- [ ] Skill name is unique in `.agents/skills/` (no exact match)
- [ ] No semantic collision with existing skills (e.g., `tdd` vs `test-driven-development`)
- [ ] Name follows kebab-case, is descriptive, not generic

### 2. Format Validation
- [ ] Contains valid `SKILL.md` with YAML frontmatter
- [ ] Required frontmatter fields: `name`, `description`, `mode` (subagent/primary), `tools`, `permissions`
- [ ] `description` follows WHAT+WHEN pattern (routing contract)
- [ ] No hardcoded paths, stale dates, or deprecated syntax

### 3. License & Source
- [ ] License is MIT, Apache-2.0, or CC0 (permissive)
- [ ] Source is verifiable (GitHub repo with >100 stars, recent commits <6 months)
- [ ] Not a typosquat (verify exact owner/repo/skill name)

### 4. Security Audit
- [ ] Read ALL files in skill folder (`SKILL.md`, `scripts/`, `references/`)
- [ ] No prompt injection in `references/` ("ignore previous instructions", etc.)
- [ ] No network calls in `scripts/` without explicit user consent
- [ ] No file writes outside project sandbox
- [ ] **Third-party transmission scan** (see § Skill Third-Party Transmission Ban): no skill may send local code, docs, screenshots, memory/narratives, or prompts to an external host unless the vendor is on `docs/APPROVED-VENDORS.md` and the use is within the 90-day exception window (or dual sign-off is recorded)
- [ ] Run `skill-check` skill for structural validation

### 5. Dependency Check
- [ ] No external CLI dependencies not in project toolchain
- [ ] No conflicting tool requirements

---

## Installation Procedure

### Preferred: Skills CLI (Version-Tracked)
```bash
# Search
npx skills find <query> --owner <owner>

# Install (tracks in lockfile, enables `npx skills update`)
npx skills add <owner/repo@skill> --project -y

# Verify appears in project skills
npx skills list --json | jq '.[] | select(.name=="<skill-name>")'
```

### Fallback: Manual Copy (Unmanaged)
```bash
# 1. Stage in quarantine
cp -r /source/skill .agents/skills-staging/<name>/

# 2. Run full vetting checklist above

# 3. Promote to production
mv .agents/skills-staging/<name> .agents/skills/<name>/

# 4. Update local manifest
# Edit .agents/skills/.antigravity-install-manifest.json (add to entries array, update updatedAt)
```

---

## Directory Structure

```
.agents/
├── skills/                 # PRODUCTION — auto-discovered by OpenCode
│   ├── <skill-name>/       # 38 skills (28 original + 10 Addy)
│   │   └── SKILL.md
│   ├── .antigravity-install-manifest.json  # Local catalog
│   └── .skill-lock.json                    # Skills CLI lockfile (vercel-labs only)
├── skills-staging/         # QUARANTINE — NOT auto-discovered
│   └── <candidate-skill>/
└── skills-archive/         # RETIRED — deprecated/broken skills
```

---

## Current Skill Inventory (38 Skills)

### Original 28 (Antigravity Bundle)
`agenttrace-session-audit`, `api-endpoint-builder`, `ax-extract-workflow`, `brooks-lint`, `bug-hunter`, `codebase-audit-pre-push`, `diagnosing-bugs`, `ecl-harness-engineer`, `effective-agent-skills`, `find-skills`, `global-chat-agent-discovery`, `hono`, `improve-codebase-architecture`, `jq`, `logic-lens`, `performance-optimizer`, `prototype`, `python-pptx-generator`, `rayden-code`, `setup-matt-pocock-skills`, `skill-check`, `squirrel`, `tdd`, `technical-change-tracker`, `tmux`, `tree-ring-memory`, `triage`

### Added 2026-08-07 (Addy Osmani — Tier 1)
| Skill | Source | Installs | Collision Assessment |
|-------|--------|----------|---------------------|
| `spec-driven-development` | addyosmani/agent-skills | 20.4K | ✅ Unique |
| `planning-and-task-breakdown` | addyosmani/agent-skills | 20.4K | ✅ Unique |
| `incremental-implementation` | addyosmani/agent-skills | 19.1K | ✅ Unique |
| `code-review-and-quality` | addyosmani/agent-skills | 23.3K | ⚠️ Semantic: overlaps `brooks-lint`, `logic-lens` |
| `security-and-hardening` | addyosmani/agent-skills | 19.6K | ✅ Unique |
| `git-workflow-and-versioning` | addyosmani/agent-skills | 17.5K | ⚠️ Semantic: overlaps `technical-change-tracker`, `triage` |
| `ci-cd-and-automation` | addyosmani/agent-skills | 17.3K | ⚠️ Semantic: overlaps `codebase-audit-pre-push` |
| `documentation-and-adrs` | addyosmani/agent-skills | 19.6K | ✅ Unique |
| `observability-and-instrumentation` | addyosmani/agent-skills | 12.5K | ✅ Unique |
| `shipping-and-launch` | addyosmani/agent-skills | 16.8K | ✅ Unique |

### Meta-Skill (Auto-Routing)
| Skill | Purpose |
|-------|---------|
| `using-agent-skills` | Routes tasks to appropriate Addy skills based on lifecycle phase |

---

## Collision Management

| Collision Pair | Resolution |
|----------------|------------|
| `code-review-and-quality` ↔ `brooks-lint`/`logic-lens` | Keep both; descriptions differentiate (Addy = holistic review, Brooks = classic SE, Logic = formal logic) |
| `git-workflow-and-versioning` ↔ `technical-change-tracker`/`triage` | Keep both; Addy = git hygiene, existing = change tracking |
| `ci-cd-and-automation` ↔ `codebase-audit-pre-push` | Keep both; Addy = pipeline design, existing = pre-push gate |

**Rule:** Semantic overlap is acceptable if descriptions are distinct. Exact name match = reject.

---

## Maintenance Schedule

| Frequency | Action | Owner |
|-----------|--------|-------|
| **Per addition** | Run full vetting checklist | Registry Owner |
| **Monthly** | `npx skills update` for CLI-tracked skills | Chief of Staff |
| **Monthly** | Audit `.agents/skills/` for dead/duplicate skills | QA Lead |
| **Quarterly** | Review collision matrix, retire/archive as needed | Chief of Staff |
| **On demand** | `skill-check` validation on any skill | Registry Owner |

---

## Rollback Procedure

```bash
# 1. Move to archive
mv .agents/skills/<problem-skill> .agents/skills-archive/<problem-skill>-$(date +%Y%m%d)

# 2. Remove from manifest
# Edit .agents/skills/.antigravity-install-manifest.json

# 3. Verify removal
npx skills list --json | jq '.[] | select(.name=="<problem-skill>")'  # Should return empty

# 4. Restart agent session to confirm
```

---

## Skill Third-Party Transmission Ban

**Version:** 1.0 · **Effective:** 2026-09-23 · **CISO of record:** Jack Mlusu (Human CEO)

### Rule

No skill (project `.agents/skills/`, project `.opencode/skills/`, or global `~/.agents/skills/` / `~/.opencode/skills/`) may transmit LightSpeed local data to a third-party host — including source code, diffs, docs, screenshots, prompts, session transcripts, memory/narratives, PDFs, or API keys — unless **all** of the following are true:

1. The destination vendor is listed on [`docs/APPROVED-VENDORS.md`](APPROVED-VENDORS.md).
2. The transmission is documented in that vendor row (what is sent, to whom, auth mechanism).
3. The use is within the **90-day default exception window** from the approval date, **or** a dual sign-off (CEO + CISO) re-authorizes it.

**CISO of record = Jack Mlusu / Human CEO.** Sole authority for Tier A (local-data) exceptions. Dual sign-off means the CEO records the exception in `APPROVED-VENDORS.md` under their own authority (CEO acknowledges CISO role).

### Pre-install checklist (every new skill)

- [ ] Grep skill tree for outbound hosts (`https://`, `fetch(`, `axios`, `requests.post`, `webhook`, `cdn`, API base URLs)
- [ ] Classify: **Tier A** (sends local data) vs **Tier B** (public web / research only) vs **local-only**
- [ ] Tier A → reject unless vendor is on APPROVED-VENDORS with active window
- [ ] Record decision (approve / reject / exception) in APPROVED-VENDORS or skill manifest

### Runtime stop (agents)

If a skill attempts transmission of local data to a non-allow-listed host during a session:

1. **STOP** the skill immediately.
2. Do not retry, do not "fix" the payload to succeed.
3. Report the skill name + destination host + payload class to the CEO (CISO).
4. Treat as a policy violation incident under §9.2.

### Exceptions

- Default window: **90 days** from `approved_at` on APPROVED-VENDORS.
- Renewal: CEO/CISO re-approval recorded before expiry; no silent rollover.
- Retired vendors stay on the historical list with status `RETIRED` — never re-enable without a new approval entry.

### Monthly audit

Registry Owner runs a monthly scan of all skill roots for new outbound hosts not on APPROVED-VENDORS. Findings go to CEO (CISO) within 5 business days.

### Retired 2026-09-23 (skills deleted)

| Skill family | Destinations (historical) | Status |
|--------------|---------------------------|--------|
| `claude-mem-*` (20) | cmem.ai, api.telegram.org, NotebookLM/Workers | **RETIRED — deleted** local `~/.claude-mem` + plugin cache |
| `scroll-craft` | kie.ai / kieai.redpandaai.co | **RETIRED — deleted** + `scrollcraft/` workspace |
| `greploop`, `greploop-apps` | Greptile | **RETIRED — deleted** (global) |

Git backup before purge: `a179b62e`.

---

## Prohibited Actions

- ❌ Editing `AGENTS.md` to "register" skills (unnecessary, misleading)
- ❌ Installing skills without vetting checklist
- ❌ Adding skills with GPL/viral licenses
- ❌ Installing from unverified sources (<100 stars, no recent commits)
- ❌ Skipping security audit of `scripts/` and `references/`
- ❌ Installing or keeping skills that transmit local data to hosts not on `docs/APPROVED-VENDORS.md` (see § Skill Third-Party Transmission Ban)
- ❌ Reinstalling retired families: `claude-mem-*`, `scroll-craft`, `greploop` / `greploop-apps`
- ❌ Sending secrets or `.env` contents to any third-party skill endpoint

---

## Change Log

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-08-07 | 1.0 | Initial policy; added 10 Addy Tier-1 skills + meta-skill | Chief of Staff |
| 2026-09-23 | 1.1 | Added Third-Party Transmission Ban; CISO = Jack Mlusu; 90-day exceptions; retired claude-mem / scroll-craft / greploop | Chief of Staff / CEO |

---

## References

- [OpenCode Skill Discovery](https://opencode.ai/docs/skills)
- [Agentskills Specification](https://agentskills.io)
- [Effective Agent Skills](https://github.com/davidondrej/effective-agent-skills)
- Project: `AGENTS.md`, `docs/ECL.md`
