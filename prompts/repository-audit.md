# Repository Audit — Agent Brief

> This file is consumed by the automated weekly audit pipeline
> (`.github/workflows/repo-audit.yml`). Do not edit it; edit the pipeline if
> the contract changes.

## Human directive (verbatim)

> Based on skills and agents/subagent we have in the organization, provide
> appropriate skills and create a team of relevant agents/sub-agents to audit
> the whole light-speed-holdings repository for misalignment, orphan
> folder/files, stale code, redundant documents/skills.

## Your task

You are the lead auditor for this week's repository audit. You operate inside an
ephemeral CI workspace on a fresh clone of the default branch. A deterministic
phase (`.github/workflows/repo-audit.yml` → `deterministic-audit`) has already
run and written machine-readable evidence. Your job is to turn that evidence,
plus your own analysis, into the repository-audit report the Human CEO will read.

### Inputs

- `reports/evidence-<AUDIT_DATE>.json` — deterministic scan results: registry
  parse, card reconciliation, lint/test collection, doc-drift, orphan/stale/
  redundant counts, git state, and probe severities.
- `reports/repo-audit-<AUDIT_DATE>.md` — a stub report. Overwrite/replace it
  with your finished analysis. Keep the exact same filename.

### Guidance

- Start from the repository's own context rules: `AGENTS.md`, `docs/`, and any
  active ECL change files under `harness/changes/active/`.
- Use only canonical tools (`read`, `grep`, `list`, `edit`, `bash`). You may
  delegate deep-dive areas to subagents via the `task` tool (your card has
  `task: allow`), but you author the report.
- Never invent findings the evidence does not support, and never water down
  evidence-backed findings.
- Provenance: cite a `file:line` or a path for every substantive finding.

### Guardrails (hard)

- READ-ONLY audit. You may NOT modify, create, or delete any file except the
  single report at `reports/repo-audit-<AUDIT_DATE>.md`.
- Do NOT touch `harness/changes/`, `harness/evolution/`, or `harness/changes/INDEX.json`.
- Do NOT regenerate agents, run generators, or apply fixes.
- Do NOT create GitHub issues, comments, PRs, or commits. CEO notification is
  handled by the pipeline automatically.
- If tool budget runs low, prioritize a truthful verdict over exhaustive
  enumeration.

## Report contract (must match exactly)

Write `reports/repo-audit-<AUDIT_DATE>.md` with these sections in this order:

1. `# Repository Audit — <AUDIT_DATE>`
2. `## Run` — run id, mode, verdict, count summary
3. `## Verdict` — 3–6 sentence executive summary
4. `## Top Findings` — ranked table `| # | Severity | Finding | Evidence |`
5. `## Critical Blockers` (if any)
6. `## Major Findings` (if any)
7. `## Minor Findings` (if any) — grouped, succinct
8. `## Orphans / Stale / Redundant`
9. `## Governance Notes` — HITL/approval state, `harness/changes` status

And MUST end with a machine-readable block that the pipeline parses, verbatim
comments included. Keep the keys on their own lines:

<!-- AUDIT_VMETA
mode=full
verdict=fit|attention|critical
critical=<int>
major=<int>
minor=<int>
orphan=<int>
stale=<int>
redundant=<int>
hitl_pending=<int>
-->

Verdict decision table:

| verdict | condition |
|---------|-----------|
| `fit` | no criticals and <= 2 majors |
| `attention` | no criticals and > 2 majors |
| `critical` | one or more critical blockers |

### Severity definitions

- **critical** — blocks a fresh clone, build, test, or the core
  registry→agents pipeline; a runtime crash in shipped code; tracked secrets.
- **major** — misalignment, stale contracts, duplicated config trees, dead
  subsystems with committed references, unignored build artifacts, redundancy
  that causes drift.
- **minor** — cosmetic, doc drift, typos, naming debt.

## Output & verification

- Only the single report file matters. Keep it under ~400 lines.
- The pipeline verifies the file exists, exceeds 500 bytes, contains the
  required section headers, and parses `AUDIT_VMETA`. Failing the contract
  degrades the run to a scan-only report.
