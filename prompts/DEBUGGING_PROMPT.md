## LIGHTSPEED DEBUGGING LOCK

You are debugging a specific problem in the LightSpeed repository.

### PROBLEM

> [INSERT EXACT PROBLEM / ERROR / FAILURE]

### EXPECTED BEHAVIOR

> [WHAT SHOULD HAPPEN]

### ACTUAL BEHAVIOR

> [WHAT IS HAPPENING]

Your mission is to identify the cause and restore the expected behavior.

---

## 1. STARTUP

Read:

`C:\Users\jmlus\light-speed-holdings\AGENTS.md`

Then:

1. Identify the relevant system/component.
2. Inspect the smallest relevant portion of the repository.
3. Assemble the smallest appropriate debugging team.
4. Reproduce or otherwise establish the failure.
5. Diagnose the root cause.
6. Implement the minimum correct fix.
7. Verify the fix.

---

## 2. DEBUGGING SCOPE LOCK

Debug ONLY the stated problem.

Do NOT use the debugging session to:

- refactor unrelated code
- redesign architecture
- clean up the repository
- upgrade dependencies unnecessarily
- modernize unrelated code
- rewrite working components
- fix unrelated warnings
- address unrelated technical debt
- add features
- change behavior unrelated to the defect
- perform opportunistic cleanup

If you discover another problem:

**DO NOT FIX IT unless it is necessary to resolve the stated problem.**

Record it under:

`OUT-OF-SCOPE FINDINGS`

---

## 3. ROOT-CAUSE REQUIREMENT

Do not stop at the first symptom.

Determine the most likely root cause.

Distinguish between:

### SYMPTOM
What is visibly failing?

### PROXIMATE CAUSE
What directly causes the failure?

### ROOT CAUSE
Why does that condition exist?

Do not make a speculative fix without sufficient evidence.

---

## 4. REPRODUCTION

Where practical, reproduce the problem before modifying anything.

Capture:

- relevant command/action
- expected result
- actual result
- error message
- stack trace/log
- relevant environment/configuration
- conditions required to reproduce

If reproduction is impossible, explicitly state why and use the strongest available evidence.

---

## 5. HYPOTHESIS-DRIVEN DEBUGGING

Create a short list of plausible causes.

For each hypothesis:

1. State the hypothesis.
2. Identify evidence that would support it.
3. Identify evidence that would disprove it.
4. Test it.
5. Record the result.

Do not repeatedly make random changes and rerun the system.

---

## 6. MINIMUM-CORRECT-FIX RULE

Once the root cause is established:

Implement the **smallest change that correctly fixes the problem**.

Do not use the bug as justification for unrelated improvement.

Preserve existing behavior outside the defect.

Avoid unnecessary architectural changes.

---

## 7. REGRESSION CHECK

After fixing the problem:

1. Reproduce the original failure.
2. Confirm it no longer occurs.
3. Test the affected functionality.
4. Run relevant automated tests/checks.
5. Check for obvious regressions caused by the fix.

If the fix introduces a regression, continue debugging **this problem** until the implementation is correct.

---

## 8. IF THE ROOT CAUSE IS OUT OF SCOPE

If resolving the problem requires a change that materially exceeds the authorized task:

STOP.

Do not silently expand scope.

Report:

- why the current task cannot safely be completed
- what dependency is required
- what evidence supports that conclusion
- what decision/approval is required

---

## 9. REQUIRED OUTPUT

### PROBLEM

...

### EXPECTED BEHAVIOR

...

### ACTUAL BEHAVIOR

...

### ROOT CAUSE

...

### EVIDENCE

...

### FIX IMPLEMENTED

...

### FILES CHANGED

...

### VERIFICATION

...

### REGRESSION CHECK

...

### OUT-OF-SCOPE FINDINGS

...

### REMAINING RISKS

...

### STATUS

**FIXED / PARTIALLY FIXED / BLOCKED**

---

## FINAL RULE

Do not declare success because the error disappeared once.

The fix must address the actual problem and survive appropriate verification.

**REPRODUCE → DIAGNOSE → FIX → VERIFY → STOP.**