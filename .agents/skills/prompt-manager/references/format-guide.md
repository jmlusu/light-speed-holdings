# Prompt Format Reference

This guide documents the LightSpeed Holdings prompt format conventions. Reference this when creating or validating prompts.

## Required Structure

Every LightSpeed prompt must follow this structure, matching the conventions in `C:\Users\jmlus\light-speed-holdings\prompts/`:

### 1. Status
Choose exactly one: COMPLETE, COMPLETE WITH CONDITIONS, PARTIALLY COMPLETE, BLOCKED, FAILED, NOT STARTED

### 2. Progress
**Progress:** X% — Base percentage ONLY on completed, verified requirements.

### 3. Objective
State the original task in one sentence.

### 4. Completed
List the 3–7 most important completed items. For each:
**Action → Result → Evidence**

### 5. Remaining
List every required item that is still incomplete.

### 6. Verification
Report:
- Tests run
- Tests passed
- Tests failed
- Build status
- Runtime/server status
- Other relevant validation

### 7. Risks / Blockers
For each:
**Issue → Impact → Severity → Mitigation/Next Action**

### 8. Repository Impact
State:
- Files added
- Files modified
- Files deleted
- Important configuration/dependency changes
- Uncommitted changes

### 9. Next 3 Actions
Only list actions directly required to complete the original objective.

### 10. CEO Decision
**REQUIRED / NOT REQUIRED**
If required, state the exact decision.

### CEO BOTTOM LINE
Give the current situation in 3 sentences or less, using plain English.

## Reporting Rules (strict)

- Report FACTS before opinions.
- Evidence before conclusions.
- Completed work before recommendations.
- Separate completed, attempted, and planned work.
- Never claim completion without verification.
- Never hide failed or skipped requirements.
- Never invent evidence.
- Never inflate the progress percentage.
- Never introduce unrelated work.
- If information is unavailable, say "Not verified."
- If uncertain, say "Uncertain" and explain why.
- Do not use vague phrases such as "improved", "optimized", "enhanced", "addressed", or "fixed" without explaining the actual change.

## Prompt Categories

### Status/Report Prompts (6 files)
- `LIGHTSPEED_MAIN_CEO_DASHBOARD_PROMPT.md` — CEO dashboard format
- `LIGHTSPEED_CEO_Status_Reporting_Prompt.md` — CEO status reporting
- `LIGHTSPEED_Cost_Benefit_Risk_Upodate_prompt.md` — Cost/benefit/risk table
- `LightSpeed_Progress_Against_the_Requested_Task_Prompt.md` — Progress comparison table
- `LightSpeed_Ultra_Short_Executive_Update_prompt.md` — Ultra-short executive update
- `LIGHTSPEED_VERIFICATION_ONLY_LOCK_PROMPT.md` — Verification-only lock

### Audit/Lock Prompts (6 files)
- `LIGHTSPEED_SESSION_AUDIT_VERIFICATION_LOCKmd.md` — Session audit lock
- `LightSpeed_TASK_VERIFICATION_PROMPT.md` — Task verification
- `LightSpeed_Progress_Against_the_Requested_Task_Prompt.md` — Progress comparison
- `LIGHTSPEED_BLOCKER_Failude_prompt.md` — Blocker/failure reports
- `LIGHTSPEED_EVERYDAY_TASK_LOCK_PROMPT.md` — Task lock (execute only authorized task)
- `LIGHTSPEED_MASTER_TASK_LOCK_PROMPT.md` — Master task lock

### Task/Execution Prompts (5 files)
- `LIGHTSPEED_DEBUGGING_PROMPT.md` — Debugging lock
- `LIGHTSPEED_PLAN_EXECUTION_LOCK_PROMPT.md` — Plan execution lock
- `LIGHTSPEED_WHAT_CHANGED_IN_THE_REPOSITORY_Prompt.md` — Repository changes review
- `LIGHTSPEED_SESSION_AUDIT_VERIFICATION_LOCKmd.md` — Session audit verification
- `repository-audit.md` — Repository audit brief

### Miscellaneous (2 files)
- `LightSpeed_RESEARCH_LOCK_PROMPT.md` — Research lock
- `LightSpeed_DO_NOT_GET_SIDETRACKED_status_prompt.md` — Sidetrack prevention

## Format Conventions

### YAML Frontmatter
- Always start with `---` on the first line
- Fields: `name` (kebab-case, matches folder), `description` (WHAT + WHEN, under 1024 chars)
- Close with `---` on its own line
- No XML angle brackets anywhere in frontmatter
- Name must not use reserved prefixes ("claude", "anthropic")

### Tables
- Use `| column | column |` format with pipe separators
- Header row required
- Consistent column alignment
- Do not merge cells or use complex formatting

### Triggers and Keywords
- Prompts often include literal trigger phrases users would say
- Common triggers: "use when", "use this", "use for", "trigger", "Do NOT"
- Negative triggers clarify scope ("Do NOT use for...", "not for general financial queries")
- Trigger phrases must be specific and actionable

## Common Patterns

### Lock Patterns
- All lock prompts enforce **read-only/audit mode**
- Explicit prohibition: "DO NOT MODIFY ANYTHING", "Do not fix issues", "Do not refactor"
- Scope discipline: "Review only history relevant to the requested task"
- Scoring: 0–100 based on evidence and completion gaps

### Task Pattern
- Compare original task request against work actually performed
- Table: Requirement | Required? | Completed? | Evidence | Notes
- Use ONLY: YES, PARTIAL, NO, NOT APPLICABLE
- Completion score: X / Y required items completed
- Overall status: COMPLETE / COMPLETE WITH CONDITIONS / PARTIALLY COMPLETE / BLOCKED / FAILED

### Report Patterns
- CEO bottom line: 3 sentences or less, plain English
- Maximum word counts vary by format (150, 300, 350, 500 words)
- Evidence takes precedence over assumptions
- Never describe planned work as completed

## Validation Checklist

Before considering a prompt compliant, verify:

- [ ] Frontmatter has `---` delimiters
- [ ] `name` field present in kebab-case, matches folder name
- [ ] `description` field present, under 1024 characters
- [ ] Description states WHAT the prompt does AND WHEN to use it
- [ ] No XML angle brackets in frontmatter
- [ ] No reserved words ("claude", "anthropic") in name
- [ ] Description includes trigger phrases ("use when", "use this", etc.)
- [ ] No `README.md` inside prompt structure
- [ ] Table format follows pipe-separated convention
- [ ] Reporting rules are followed (facts before opinions, evidence before conclusions)
- [ ] Vague phrases ("improved", "optimized", etc.) are explained with specifics
- [ ] Word count limits are respected for the prompt type