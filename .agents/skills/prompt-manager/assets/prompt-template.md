# Prompt Template

Use this blank template when creating a new LightSpeed-style prompt. Fill in each section following the format reference in `references/format-guide.md`.

```markdown
# Prompt Title

## 1. STATUS
Choose exactly one:
- COMPLETE  
- COMPLETE WITH CONDITIONS  
- PARTIALLY COMPLETE  
- BLOCKED�
- FAILED  
- NOT STARTED

## 2. PROGRESS
**Progress:** X%

Base the percentage ONLY on completed, verified requirements.

## 3. OBJECTIVE
State the original task in one sentence.

## 4. COMPLETED
List the 3–7 most important completed items.
For each:
**Action → Result → Evidence**

## 5. REMAINING
List every required item that is still incomplete.

## 6. VERIFICATION
Report:
- Tests run
- Tests passed
- Tests failed
- Build status
- Runtime/server status
- Other relevant validation

## 7. RISKS / BLOCKERS
For each:
**Issue → Impact → Severity → Mitigation/Next Action**

## 8. REPOSITORY IMPACT
State:
- Files added
- Files modified
- Files deleted
- Important configuration/dependency changes
- Uncommitted changes

## 9. NEXT 3 ACTIONS
Only list actions directly required to complete the original objective.

## 10. CEO DECISION
**REQUIRED / NOT REQUIRED**

If required, state the exact decision.

## CEO BOTTOM LINE
Give me the current situation in 3 sentences or less, using plain English.

### Reporting Rules

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
```

## Quick Pre-Fill Checklist

Before writing, confirm:
- [ ] Prompt type (Status/Report, Audit/Lock, Task/Execution, Miscellaneous)
- [ ] Folder name is kebab-case (if creating as a skill)
- [ ] Name matches folder name (if applicable)
- [ ] Description will state WHAT + WHEN under 1024 chars
- [ ] No XML angle brackets in any YAML frontmatter
- [ ] Trigger phrases identified for skill loading