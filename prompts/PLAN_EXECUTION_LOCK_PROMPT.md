## LIGHTSPEED PLAN EXECUTION LOCK

Read:

`C:\Users\jmlus\light-speed-holdings\AGENTS.md`

Then execute the **existing approved plan**:

> [INSERT PLAN / REFERENCE]

### MISSION

Implement the approved plan exactly as specified.

The plan is the source of truth for the task.

Do not replace the plan with a different approach unless the existing plan is technically impossible or would cause a clear failure.

### TEAM

Based on the available LightSpeed skills, agents, and sub-agents:

- assemble the smallest appropriate team
- assign bounded responsibilities
- work in parallel where there are no dependencies or conflicts

The parent agent remains responsible for completion.

### SCOPE LOCK

Only implement work contained in, or strictly necessary to execute, the approved plan.

Do not use implementation as an opportunity to:

- clean up the repository
- redesign unrelated systems
- refactor unrelated code
- improve unrelated UX
- introduce additional features
- rewrite working systems
- address unrelated technical debt
- begin future phases
- implement recommendations that are not part of the plan

Record those items as `OUT-OF-SCOPE`.

### CHANGE CONTROL

If implementation reveals that the plan is incomplete:

1. Determine whether the missing work is technically necessary.
2. If necessary, perform the minimum required work.
3. If not necessary, do not implement it.
4. If the discovery materially changes the approved objective, stop and request clarification.

### COMPLETION

Do not declare success until the approved plan has actually been implemented and verified.

After verification:

**STOP.**

Do not proceed to the next phase, next recommendation, or next improvement.

### FINAL REPORT

Report:

- Plan items completed
- Verification performed
- Files/areas changed
- Deviations from plan, if any
- Out-of-scope findings
- Remaining blockers

**IMPLEMENT THE PLAN → VERIFY → STOP.**