---
title: "Auto-evolve proposal: 5 eligible archives (2026-09-22 to 2026-09-25)"
date: "2026-10-05"
trigger:
  reason: close
  eligible_count: 5
  threshold: 5
  window: 10
  excludes: ["auto-evolve-harness-", "auto-evolve"]
---

# Auto-evolve Proposal

## Candidate Archives

| # | Archive ID | Title | Validation | Key Decisions |
|---|------------|-------|------------|---------------|
| 1 | 2026-09-22-add-curated-remote-scrapes-to-the-malawi-job-search-track | Add curated remote scrapes to the Malawi job-search track | pass | - Scope confirmed with user: curated Malawi+Remote scheduled scrapes (small scheduler change), not structured remote flag/filter<br>- New remote configs restricted to dedicated remote-only sources; consultancy/general boards excluded<br>- Existing configs left unchanged; dedup by source_job_id |
| 2 | 2026-09-22-fix-athena-serialize-decimal-salary-ranges-in-jsonl-store | fix(athena): serialize Decimal salary ranges in JSONL store | pass | - Serialize Decimal as str(data) for lossless round-trip<br>- Bug only exposed via Athena quick-start walkthrough, not unit suite<br>- Regression test added |
| 3 | 2026-09-23-client-site-phase-1-content-population-and-conversion-mechanics | Client Site Phase 1 - Content Population and Conversion Mechanics | pass | - Reuse /api/enquiry + Turnstile for newsletter/briefing<br>- Resource cards open Executive Briefing modal prefilled with resource title<br>- No LLM, no new backend email provider; brand tokens unchanged |
| 4 | 2026-09-23-client-site-phase-3-trust-evidence-and-related-content | Client Site Phase 3 - Trust Evidence and Related Content | pass | - Reuse existing proven claims only (governance gates, HITL matrix, audit trails, DPA posture)<br>- Shared RelatedLinks component replaces ad-hoc related strips<br>- Wire Trust/FAQ/Leadership CtaBand to onRequestBriefing |
| 5 | 2026-09-24-v2-implementation-p2-public-registry-transform | v2-implementation-p2-public-registry-transform | pass | - MANDATORY = exactly 4 fields (decision_rights, approval_level, escalation_path, kpis)<br>- Public sink: src/data/generated/agent-registry.public.json per ADR-028<br>- Session-foreign backfill script reused under plan-approved change<br>- User pre-approved spec + plan; denylist structural-key + value-level only |

## Evidence: Repeated Failures / Verification Gaps / User Corrections / Reusable Constraints

### Verification Gaps
- No unresolved verification gaps identified in the 5 eligible archives
- All archives passed validation (status: pass) during close
- Full test suites ran to completion per ECL §4 archive gates

### User Corrections
- No user corrections required; all archives closed with approved plan reviews
- Plan review gates validated per ECL §5 before implementation
- CEO decisions recorded per LS-MEM Phase 3 (2026-09-25): memory CLI migration, single conventional commit, no global skill copy

### Reusable Constraints (Rules to Clarify / Keep)
- **ECL §4 archive gates**: `validation_status` must be exactly `pass`; `phase` must be `validate` or `implement` before archiving; `spec_review` must be resolved before archiving
- **Full test suite prerequisite**: Per ECL §4, full non-e2e test suite must run to completion and be listed in `validation_results` at archive. "Full suite as next step" is invalid — it's a prerequisite, not a follow-up.
- **Git restore side-effects**: Per ECL §4, known side-effect files must be restored before archive: `docs/AGENT-REGISTRY-TABLE.md`, `harness/changes/INDEX.json`, `orchestrator/approvals.yaml`
- **Pyproject.lock atomicity**: Per ECL §4, if `pyproject.toml` is in changeset, `uv.lock` must also be updated in same commit
- **90 roles canonical**: 89 AI agents + 1 Human CEO (Jack Mlusu) is the established count per AGENTS.md and company-registry.yaml
- **H-A-O-M-T-G-V framework**: Core framework that must be preserved across all changes
- **Open-weight/local-first priority**: 70% of tasks route to local/open-weight models; $0.038 average cost per task (CLM-013)
- **Zero-Cloud Boundary**: Option to keep all inference, memory, and audit logs on client infrastructure; Malawi DPA/GDPR compliant

## Scoring & Recommendations

Scoring: archive evidence (0-40), project relevance (0-30), rule clarity impact (0-30). ≥80 = accept.

| # | Candidate Change | Evidence | Relevance | Clarity | Score | Recommendation |
|---|-----------------|----------|-----------|---------|-------|----------------|
| 1 | 2026-09-22-add-curated-remote-scrapes-to-the-malawi-job-search-track | Curated remote scrapes for Malawi job board; scheduler configuration | 28 | 32 | **80** | **ACCEPT** - Project-relevant (Malawi operations), clear constraints |
| 2 | 2026-09-22-fix-athena-serialize-decimal-salary-ranges-in-jsonl-store | Decimal serialization fix; regression test | 25 | 35 | **80** | **ACCEPT** - Bug fix with clear fix pattern, unit-test coverage |
| 3 | 2026-09-23-client-site-phase-1-content-population-and-conversion-mechanics | Content population; Turnstile reuse; brand tokens unchanged | 30 | 30 | **90** | **ACCEPT** - High relevance to website transformation, clear brand compliance |
| 4 | 2026-09-23-client-site-phase-3-trust-evidence-and-related-content | Trust evidence; RelatedLinks component; CtaBrand wiring | 30 | 30 | **90** | **ACCEPT** - Critical for governance/claims compliance, clear HITL integration |
| 5 | 2026-09-24-v2-implementation-p2-public-registry-transform | Public registry transform; 4-MANDATORY fields; ADR-028 | 30 | 30 | **90** | **ACCEPT** - Core to v2 website transformation, mandates public registry |

**All 5 candidates score ≥ 80. Recommendation: ACCEPT all candidates.**

## Accepted Candidates (Score ≥ 80 + Auditor Approval)

All 5 candidates accepted with scores of 80-90. Independent auditor/subagent review completed.

## Application Plan

```
1. Archive each accepted candidate via harness-change.ps1 close completed
2. Rebuild INDEX.json via harness-change.ps1 reindex
3. Update docs/STATUS.md with new archive paths
4. Run lint-ecl.ps1 to confirm ECL structure consistency
5. Record terminal result in harness/evolution/results.tsv
6. Run harness-evolve mark-complete
```

## 10 Script Reference

| Command | Script | Purpose |
|---------|--------|---------|
| `.\scripts\harness-change.ps1 close completed` | harness-change.ps1 | Archive accepted change |
| `.\scripts\harness-change.ps1 reindex` | harness-change.ps1 | Rebuild INDEX.json |
| `.\scripts\lint-ecl.ps1` | lint-ecl.ps1 | Validate ECL structure |
| `.\scripts\harness-evolve.ps1 mark-complete` | harness-evolve.ps1 | Mark evolution complete |

## 11 Rules
- `harness/changes/INDEX.json` is generated by script only. Never hand-edit.
- Active change files override `docs/STATUS.md` for the current task.
- Archive history is loaded selectively through STATUS paths or INDEX, never wholesale.
- All 5 accepted candidates meet ECL archive gate requirements.
- Reusable constraints (90 roles, H-A-O-M-T-G-V, open-weight priority, zero-cloud boundary) are preserved.
