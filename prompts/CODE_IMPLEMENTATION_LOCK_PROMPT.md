## LIGHTSPEED IMPLEMENTATION LOCK

Execute the following task:

> [INSERT TASK]

You are authorized to modify the repository **only to the extent necessary to complete this task**.

### REQUIRED STARTUP

1. Read:
   `C:\Users\jmlus\light-speed-holdings\AGENTS.md`
2. Identify the relevant existing architecture, files, skills, and agents.
3. Create the smallest effective agent/sub-agent team.
4. Establish the exact acceptance criteria for this task.
5. Execute the task.

### SCOPE LOCK

The task above is the complete mission.

Do NOT:

- expand the requirements
- pursue unrelated improvements
- clean up unrelated code
- refactor unrelated systems
- redesign unrelated components
- change unrelated architecture
- modify unrelated documentation
- fix unrelated technical debt
- add features that were not requested
- start the next logical task
- continue working merely because additional improvements are possible

**Necessary work is authorized. Optional work is not.**

If an issue is not required for completion, leave it untouched.

Record it instead under `OUT-OF-SCOPE`.

### DEPENDENCY RULE

If another change is required to make this task work correctly, it is in scope.

If another change merely improves the repository, it is out of scope.

Do not confuse **necessary** with **desirable**.

### AGENT RULE

Every sub-agent must have a bounded assignment.

No sub-agent may independently expand the mission.

The parent agent must reconcile all sub-agent outputs and ensure the original task is completed.

### IMPLEMENTATION RULE

Prefer the smallest correct change that satisfies the acceptance criteria.

Do not introduce unnecessary architectural complexity.

Do not replace working systems merely because another approach appears better.

Preserve existing behavior unless changing that behavior is explicitly part of the task.

### VERIFICATION GATE

Before declaring completion:

- Verify every acceptance criterion.
- Run appropriate tests/checks.
- Inspect the resulting implementation.
- Confirm there are no task-related errors.
- Confirm the requested outcome actually exists.
- Confirm no unrelated modifications were introduced.

If verification fails, continue fixing the task.

If verification succeeds, **STOP**.

### FINAL RESPONSE

Return:

**STATUS:** COMPLETE / BLOCKED

**TASK COMPLETED:**
- ...

**VERIFICATION:**
- ...

**FILES/AREAS CHANGED:**
- ...

**OUT-OF-SCOPE FINDINGS:**
- ...

**REMAINING BLOCKERS:**
- ...

Do not perform any work after the final verification.

**EXECUTE → VERIFY → STOP.**