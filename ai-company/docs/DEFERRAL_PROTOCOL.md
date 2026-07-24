# Deferred Item Protocol

**Owner:** Chief of Staff  
**Effective:** Immediate  
**Scope:** All agent delegations across the organization  

---

## 1. Definition

A **"deferred item"** is any recommendation, task, or action item that the executing agent chooses NOT to complete during the current execution cycle.

Deferral is a legitimate project management tool when used correctly. It is NOT a mechanism to avoid work or hide scope creep.

---

## 2. Mandatory Requirements Before Deferral

Before any item can be deferred, the executing agent **MUST** complete all five steps:

### Step 1: Explicitly Flag the Item

In the completion report, the item must be marked with status `DEFERRED` — not `SKIPPED`, `PENDING`, or `DEFERRED_UNTIL_LATER`. The exact status keyword is `DEFERRED`.

### Step 2: Provide Written Justification

The executing agent must explain **WHY** the item was deferred. Acceptable justifications include:

- **Technical complexity**: The implementation requires more time than available
- **Dependency**: Blocked by another task not yet completed
- **Scope**: The item was outside the original delegation scope
- **Risk**: Completing the item now would introduce unacceptable risk
- **Resource constraint**: Requires specialized expertise not available in the current cycle

Unacceptable justifications:
- "Ran out of time" (without explaining why)
- "Not important" (without evidence)
- "Will do later" (without a plan)

### Step 3: Quantify the Risk

Every deferral must include a risk assessment:

| Risk Dimension | Questions to Answer |
|----------------|---------------------|
| **Business impact** | What happens if this is not done this sprint? |
| **Technical debt** | Does deferral create compounding complexity? |
| **Security exposure** | Does deferral leave a vulnerability open? |
| **Downstream blockers** | Will other agents/tasks be blocked? |

Risk levels: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`

### Step 4: Propose a Target Completion Date

The agent must propose either:
- A specific target sprint or date, OR
- A dependency trigger (e.g., "when Task X is completed")

### Step 5: Obtain Explicit CEO Approval

**The deferral is NOT valid until the CEO (or delegated authority) approves it.** The agent must:
1. Submit the deferral request with all above information
2. Wait for explicit approval (not silence, not assumption)
3. Record the approval in the completion report

---

## 3. Completion Report Format

All execution reports MUST include a verification matrix:

```
| Item | Implemented | Tests Pass | Verified | Deferred | Justification |
|------|-------------|------------|----------|----------|---------------|
| R1   | ✅          | ✅         | ✅       | —        | —             |
| R2   | —           | —          | —        | ✅       | Reason...     |
```

The matrix must account for EVERY item in the original delegation scope. If an item is not listed, that is treated as a silent omission (see Section 5).

---

## 4. Items That Cannot Be Deferred

The following categories are **non-deferrable** regardless of justification:

| Category | Reason |
|----------|--------|
| **Data integrity fixes (GAP-type issues)** | These are correctness bugs that compound over time |
| **Security vulnerabilities** | Exposure risk increases with every cycle of delay |
| **Active production incidents** | Users are impacted right now |
| **Items explicitly marked P0 by leadership** | P0 means "do this NOW" |
| **Audit trail / compliance requirements** | Regulatory exposure |

If an item in one of these categories truly cannot be completed, the agent must **escalate to the CEO immediately** rather than deferring.

---

## 5. Enforcement

### CEO Advisor Audit

The CEO Advisor agent will audit completion reports against the original delegation scope. The audit checks:

1. Every item in the delegation scope appears in the verification matrix
2. Deferred items have all five mandatory fields completed
3. Non-deferrable items were not deferred without escalation
4. Risk assessments are reasonable and evidence-based

### Scope Discipline Failures

**Silent omission** — failing to include an item in the verification matrix at all — is treated as a **scope discipline failure**. This is more serious than a legitimate deferral because it indicates the agent either:
- Lost track of the scope, or
- Intentionally hid incomplete work

### Corrective Action

Repeated scope discipline failures (2+ in a sprint) require:
1. A root cause analysis from the responsible agent
2. A corrective action plan reviewed by the Chief of Staff
3. Increased verification scrutiny for subsequent delegations

---

## 6. Integration with Existing Workflow

### Where This Protocol Applies

- **CoS → Specialist delegations** (all of them)
- **CTO → Engineer delegations**
- **Any cross-department task assignment**
- **Sprint planning and review**

### Reference in AGENTS.md

Add under Safety Boundaries in `AGENTS.md`:

```
- All execution reports must include a verification matrix per `docs/DEFERRAL_PROTOCOL.md`.
- Deferred items require explicit CEO approval before the deferral is valid.
- Silent omission of scope items is a scope discipline failure.
```

### Active Change Tracking

The `harness/changes/active/summary.md` should include a deferral section:

```markdown
## Deferrals

| Item | Deferred By | Justification | Risk | Target | Approved |
|------|-------------|---------------|------|--------|----------|
| R2   | lead-backend | Complexity   | MED  | Sprint 3 | ✅ CEO  |
```

---

## 7. Example: Good vs. Bad Deferral

### ✅ Good Deferral

```
| Item | Implemented | Tests Pass | Verified | Deferred | Justification |
|------|-------------|------------|----------|----------|---------------|
| R2   | —           | —          | —        | ✅       | Depends on R1 SQLite migration completing first. Risk: MEDIUM — dashboard will have dual-backend until R2 lands. Target: Sprint 3 (after R1 verification). CEO approved 2026-07-24. |
```

### ❌ Bad Deferral (Scope Discipline Failure)

```
| Item | Implemented | Tests Pass | Verified | Deferred | Justification |
|------|-------------|------------|----------|----------|---------------|
| R1   | ✅          | ✅         | ✅       | —        | —             |
(R2 is not mentioned at all)
```

---

## 8. Quick Reference Checklist

Before submitting a completion report, verify:

- [ ] Every item from the delegation scope is in the verification matrix
- [ ] Deferred items have: `DEFERRED` status, justification, risk level, target date, CEO approval
- [ ] Non-deferrable items (GAP fixes, security, P0) are not deferred
- [ ] No items are silently omitted
- [ ] Risk assessments are evidence-based, not hand-wavy
