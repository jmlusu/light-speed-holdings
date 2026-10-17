## LIGHTSPEED ROOT-CAUSE DEBUGGING LOCK

### INCIDENT / DEFECT

> [INSERT PROBLEM]

### SYSTEM / COMPONENT

> [INSERT COMPONENT IF KNOWN]

### EXPECTED

> [EXPECTED RESULT]

### ACTUAL

> [ACTUAL RESULT]

---

## MISSION

Find and resolve the root cause of the stated defect.

This is a **debugging assignment**, not a general improvement assignment.

Read:

`C:\Users\jmlus\light-speed-holdings\AGENTS.md`

Use the smallest team necessary.

---

## DEBUGGING PROTOCOL

### PHASE 1 — OBSERVE

Do not modify anything yet.

Establish:

- exact failure
- reproducibility
- affected component
- relevant inputs
- relevant outputs
- logs/errors
- recent relevant changes
- environmental conditions

### PHASE 2 — LOCALIZE

Determine where the failure originates.

Trace:

**INPUT → PROCESSING → DEPENDENCY → OUTPUT**

Identify the first point where actual behavior diverges from expected behavior.

### PHASE 3 — HYPOTHESIZE

Develop a small set of plausible root causes.

Rank them by evidence.

Do not make speculative modifications merely to see what happens.

### PHASE 4 — PROVE

Test the leading hypothesis using the least invasive diagnostic method available.

Do not treat correlation as proof.

### PHASE 5 — FIX

Implement the smallest correct fix.

Do not redesign the system unless the defect cannot be correctly resolved without doing so.

### PHASE 6 — VERIFY

Verify:

- original failure is resolved
- expected behavior is restored
- relevant tests pass
- no obvious regression was introduced
- fix works under the relevant conditions

### PHASE 7 — STOP

Once the defect is correctly resolved and verified:

**STOP.**

Do not continue into cleanup or optimization.

---

## SCOPE RULE

A discovered issue is actionable only if it is:

**A. The root cause of the stated defect**, or

**B. A direct consequence of the fix that must be resolved to make the fix correct.**

Everything else is out of scope.

---

## REQUIRED FINAL REPORT

**ROOT CAUSE:**  
...

**CONFIDENCE:** HIGH / MEDIUM / LOW

**EVIDENCE:**  
...

**FIX:**  
...

**FILES CHANGED:**  
...

**TESTS / VERIFICATION:**  
...

**REGRESSION STATUS:**  
...

**OUT-OF-SCOPE ISSUES:**  
...

**REMAINING RISKS:**  
...

**STATUS:** FIXED / BLOCKED

**REPRODUCE → LOCALIZE → PROVE → FIX → VERIFY → STOP.**