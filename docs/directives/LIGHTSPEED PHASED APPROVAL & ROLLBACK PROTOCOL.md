# LIGHTSPEED PHASED APPROVAL & ROLLBACK PROTOCOL

**Purpose:** Allow LightSpeed agents to aggressively sanitize, consolidate, and streamline the repository while ensuring that every meaningful change is reviewable, reversible, and independently verifiable.

---

# 1. CORE GOVERNANCE PRINCIPLE

Agents may move quickly.

They may **not move irreversibly**.

Every repository-cleanup operation must satisfy:

```text
OBSERVE
  ↓
PROPOSE
  ↓
APPROVE
  ↓
EXECUTE
  ↓
VALIDATE
  ↓
PROMOTE
  ↓
CLOSE
```

At every stage there must be a known recovery point.

The default assumption is:

> **If a change cannot be confidently rolled back, it is not ready for autonomous execution.**

---

# 2. CHANGE RISK LEVELS

Every proposed change must be assigned a risk class.

| Level | Change                                               | Approval                                |
| ----- | ---------------------------------------------------- | --------------------------------------- |
| R0    | Read-only inspection                                 | Agent                                   |
| R1    | Formatting / non-functional cleanup                  | Agent                                   |
| R2    | File moves / consolidation with verified references  | Agent + automated validation            |
| R3    | Code refactor / dependency changes                   | Human approval                          |
| R4    | Architecture / runtime / data changes                | Explicit human approval                 |
| R5    | Destructive / security / production-impacting change | Explicit human approval + rollback plan |

When uncertain, **use the higher risk level**.

---

# 3. PHASE 0 — BASELINE & FREEZE

Before modifying the repository:

### Required

```bash
git status
git branch
git log -n 20
```

Establish:

```text
BASELINE_COMMIT
CLEANUP_BRANCH
WORKTREE_STATUS
BUILD_STATUS
TEST_STATUS
HEALTH_STATUS
```

Create an immutable rollback reference:

```text
cleanup/baseline
```

or an equivalent Git tag/reference.

### Baseline acceptance gate

The agent must record:

```text
Commit:
Branch:
Build:
Tests:
Lint:
Typecheck:
Security:
Health:
```

If the baseline does not pass existing validation, **do not attribute those failures to the cleanup**.

Record them as pre-existing failures.

### APPROVAL GATE 0

Human approves:

> "Baseline captured. Proceed to repository audit."

---

# 4. PHASE 1 — READ-ONLY AUDIT

Agents perform:

* file inventory
* dependency analysis
* duplicate detection
* dead-code analysis
* configuration audit
* documentation audit
* security scan
* Git audit
* architecture mapping

### Prohibited

No:

```text
deletion
renaming
moving
dependency removal
configuration modification
code refactor
```

during this phase.

### Deliverable

```text
repo-audit/
    INVENTORY.md
    ARCHITECTURE_MAP.md
    DEPENDENCY_MAP.md
    DUPLICATES.md
    DEAD_CODE.md
    CONFIGURATION_AUDIT.md
    DOCUMENTATION_AUDIT.md
    SECURITY_AUDIT.md
    CLEANUP_PLAN.md
    OPEN_QUESTIONS.md
```

### APPROVAL GATE 1

Human reviews:

```text
WHAT EXISTS
WHAT IS CANONICAL
WHAT WILL CHANGE
WHAT WILL BE DELETED
WHAT IS UNCERTAIN
```

No implementation begins until the cleanup plan is approved.

---

# 5. PHASE 2 — LOW-RISK SANITIZATION

Agents may execute only low-risk changes such as:

```text
remove generated artifacts
fix .gitignore
format files
remove obvious temporary files
normalize naming
clean documentation formatting
remove verified cache files
```

Every logical group of changes must be a separate commit.

Example:

```text
chore(repo): remove generated artifacts
chore(repo): normalize repository metadata
chore(repo): clean documentation structure
```

Do NOT combine unrelated cleanup into one massive commit.

### Validation

After each logical change:

```text
build
tests
lint
typecheck
```

as applicable.

### ROLLBACK

If validation regresses:

```text
git revert <commit>
```

or reset the affected working branch to the last validated checkpoint.

Do not continue accumulating changes on top of a known-bad state.

---

# 6. PHASE 3 — CONSOLIDATION

This phase handles:

```text
duplicate implementations
duplicate services
duplicate utilities
duplicate configuration
duplicate components
duplicate scripts
old architecture paths
```

### Required procedure

For each consolidation:

```text
1. Identify canonical implementation
2. Identify all consumers
3. Identify behavioral differences
4. Migrate consumers
5. Run tests
6. Verify no references remain
7. Remove obsolete implementation
8. Run full validation
```

### Never do this

```text
delete old implementation
hope nothing depended on it
```

### Instead

```text
old implementation
       ↓
migrate references
       ↓
validate
       ↓
remove old implementation
       ↓
validate again
```

### APPROVAL GATE 2

Human approval required before deleting any implementation that:

* has external consumers
* is imported dynamically
* participates in runtime orchestration
* touches persistent data
* affects deployment
* affects authentication
* affects model routing
* affects memory
* affects production infrastructure

---

# 7. PHASE 4 — ARCHITECTURAL REFACTOR

This phase covers:

```text
directory restructuring
API changes
agent orchestration changes
memory architecture
model abstraction
configuration architecture
runtime architecture
deployment changes
frontend architecture
```

Each architectural change requires an explicit mini-proposal:

```text
CURRENT
TARGET
WHY
FILES AFFECTED
DEPENDENCIES
RISKS
VALIDATION
ROLLBACK
```

### Required rollback plan

Before execution, specify:

```text
rollback commit
rollback command
data rollback requirement
configuration rollback requirement
external-system rollback requirement
```

If data migration is involved:

> **A code rollback is insufficient.**

The agent must provide a data rollback or forward-recovery strategy.

### APPROVAL GATE 3

Human explicitly approves the architectural change.

---

# 8. PHASE 5 — DEPENDENCY & INFRASTRUCTURE CLEANUP

Dependency removal and infrastructure changes receive additional protection.

Before removing a dependency:

```text
SEARCH
STATIC ANALYSIS
DYNAMIC IMPORT CHECK
BUILD
TEST
```

Before changing infrastructure:

```text
LOCAL VALIDATION
STAGING VALIDATION
HEALTH CHECK
DEPLOYMENT CHECK
ROLLBACK CHECK
```

Never remove a dependency simply because static analysis says it is unused if the repository supports:

```text
plugins
dynamic imports
reflection
runtime discovery
configuration-based loading
```

---

# 9. PHASE 6 — SECURITY SANITIZATION

Security changes are handled separately from normal cleanup.

Examples:

```text
credential removal
secret rotation
authentication changes
permission changes
security configuration
certificate changes
access-control changes
```

### Rule

> **Never assume deleting a secret from the current tree invalidates a compromised credential.**

If a credential has been exposed:

```text
identify
revoke/rotate
remove
scan
verify
document
```

### APPROVAL GATE 4

Security-sensitive changes require explicit human approval unless they are clearly emergency containment actions.

---

# 10. PHASE 7 — FULL VALIDATION

Before declaring the cleanup successful, run the complete repository health suite.

Minimum:

```text
repository structure
dependency validation
lint
format
typecheck
unit tests
integration tests
E2E tests where applicable
security scan
build
production build
configuration validation
runtime health check
```

The final state must be compared against the baseline.

Generate:

```text
docs/REPOSITORY_HEALTH.md
```

with:

```text
BEFORE
AFTER
IMPROVEMENTS
REGRESSIONS
KNOWN LIMITATIONS
REMAINING TECHNICAL DEBT
```

---

# 11. PROMOTION MODEL

Repository cleanup should use explicit promotion states:

```text
DRAFT
  ↓
AUDITED
  ↓
APPROVED
  ↓
IN PROGRESS
  ↓
VALIDATED
  ↓
READY FOR PROMOTION
  ↓
PROMOTED
  ↓
CLOSED
```

A change may not skip directly from:

```text
IN PROGRESS → PROMOTED
```

without validation.

---

# 12. CHECKPOINT STRATEGY

Create checkpoints at meaningful boundaries.

For example:

```text
C0 = baseline
C1 = low-risk sanitation
C2 = consolidation
C3 = architectural refactor
C4 = dependency cleanup
C5 = final validation
```

Each checkpoint must:

```text
build
test
lint
typecheck
```

successfully, where applicable.

Checkpoint naming should make recovery obvious:

```text
cleanup/c0-baseline
cleanup/c1-sanitization
cleanup/c2-consolidation
cleanup/c3-architecture
cleanup/c4-dependencies
cleanup/c5-validated
```

---

# 13. ATOMIC COMMIT RULE

Agents must avoid enormous "cleanup everything" commits.

Bad:

```text
chore: clean repository
```

containing hundreds of unrelated changes.

Prefer:

```text
chore(repo): remove generated artifacts
refactor(memory): consolidate memory adapters
refactor(agents): consolidate agent registry
chore(config): remove obsolete configuration
docs(repo): establish canonical architecture guide
chore(deps): remove unused dependencies
```

Each commit should answer:

> "What single conceptual change happened here?"

---

# 14. ROLLBACK DECISION TREE

When validation fails:

```text
VALIDATION FAILURE
       │
       ├── Expected?
       │       └── Document and continue
       │
       └── Unexpected
               │
               ├── Can isolate to latest change?
               │       ├── YES → revert latest change
               │       └── NO
               │
               └── Return to last known-good checkpoint
```

Do not attempt increasingly complex patches on top of an unknown failure state.

---

# 15. AUTOMATIC STOP CONDITIONS

Agents MUST stop and request human review when they encounter:

```text
unknown production dependency
unknown data dependency
uncertain source of truth
conflicting architecture
unexpected test regression
unexpected runtime regression
security credential exposure
data migration requirement
destructive database operation
authentication change
authorization change
production infrastructure change
irreversible external-system change
ambiguous deletion
significant API contract change
```

The correct behavior is:

> STOP → REPORT → WAIT

Not:

> GUESS → PATCH → CONTINUE

---

# 16. ROLLBACK CONDITIONS

Rollback to the previous checkpoint if:

* build breaks unexpectedly
* critical tests regress
* runtime behavior changes unexpectedly
* agent orchestration breaks
* memory integrity fails
* configuration becomes ambiguous
* deployment becomes unsafe
* security posture worsens
* dependency resolution becomes unstable
* repository health materially decreases

Do not optimize for preserving cleanup work.

Optimize for preserving a **known-good system**.

---

# 17. ROLLBACK VS REVERT

Use:

### Revert

When a specific logical commit caused the problem:

```text
git revert <commit>
```

Preferred because it preserves history.

### Checkpoint rollback

When multiple changes have become entangled:

```text
return to last known-good checkpoint
```

Use when isolation is no longer reliable.

### Full branch abandonment

If the cleanup branch becomes contaminated:

```text
delete cleanup branch
recreate from baseline
```

This is acceptable.

The repository's Git history remains intact.

---

# 18. NEVER ROLLBACK BLINDLY

Before rollback, capture:

```text
failure
logs
test output
git diff
git status
affected components
configuration state
database state
```

If useful, preserve the failed state under:

```text
artifacts/failure-<timestamp>/
```

but do not commit it.

The failure should be diagnosable even after recovery.

---

# 19. DATA SAFETY PROTOCOL

Any operation touching persistent data requires special treatment.

Before:

```text
schema migration
database deletion
memory migration
index rebuild
audit-log transformation
persistent configuration migration
```

capture:

```text
backup
schema version
migration version
record counts
integrity checks
```

The agent must explicitly answer:

```text
Can this be rolled back?
If yes, how?
If no, what is the forward-recovery strategy?
```

"No rollback possible" is acceptable only with explicit approval.

---

# 20. AGENT PARALLELISM RULE

Multiple agents may work in parallel only when their work domains are independently bounded.

Good:

```text
Agent A → documentation audit
Agent B → dependency audit
Agent C → frontend duplicate audit
Agent D → security audit
```

Risky:

```text
Agent A → refactor agents/
Agent B → refactor agents/
Agent C → reorganize src/
```

Agents must not concurrently mutate the same architectural surface without coordination.

---

# 21. HANDOFF PROTOCOL

Every agent handoff must contain:

```text
STATUS
COMPLETED
CHANGED
NOT CHANGED
VALIDATION
KNOWN FAILURES
RISKS
NEXT ACTION
ROLLBACK POINT
```

Example:

```text
STATUS: READY FOR REVIEW

COMPLETED:
- consolidated 4 duplicate configuration loaders
- migrated 17 consumers
- removed 3 obsolete implementations

VALIDATION:
- tests: PASS
- typecheck: PASS
- lint: PASS
- build: PASS

ROLLBACK:
cleanup/c2-consolidation

OPEN QUESTION:
One dynamic import requires human confirmation.
```

---

# 22. HUMAN APPROVAL SHOULD BE SMALL AND HIGH-SIGNAL

Do not require human approval for every file.

Human attention should be reserved for decisions involving:

```text
architecture
behavior
data
security
production
irreversibility
ambiguity
```

Agents should handle:

```text
inventory
mechanical cleanup
formatting
obvious generated artifacts
verified renames
documentation normalization
automated validation
```

This preserves the speed advantage of LightSpeed without sacrificing control.

---

# 23. FINAL RELEASE GATE

The cleanup may be merged into the canonical branch only when:

```text
[ ] Baseline preserved
[ ] Cleanup plan approved
[ ] All destructive changes approved
[ ] All architectural changes approved
[ ] Tests pass
[ ] Build passes
[ ] Security scan passes
[ ] Health check passes
[ ] No unexplained regressions
[ ] Documentation reflects reality
[ ] Repository structure is coherent
[ ] Rollback checkpoint exists
[ ] Remaining technical debt documented
```

Final status:

```text
REPOSITORY SANITIZATION: APPROVED
```

or:

```text
REPOSITORY SANITIZATION: BLOCKED
```

Never use "mostly complete" as a release state.

---

# 24. POST-CLEANUP OBSERVATION PERIOD

After promotion, do not immediately declare the architecture permanently settled.

For the next development cycle, monitor:

```text
new duplicate files
new *_v2 patterns
new configuration sprawl
new root-level artifacts
new undocumented scripts
new dependency creep
new architectural exceptions
```

If entropy begins returning, fix the process rather than repeatedly performing giant cleanup projects.

---

# 25. THE LIGHTSPEED GOVERNANCE LOOP

The long-term model should be:

```text
FAST DEVELOPMENT
       ↓
SMALL CHANGE
       ↓
AUTOMATED VALIDATION
       ↓
CHECKPOINT
       ↓
PROMOTE
       ↓
OBSERVE
       ↓
CONSOLIDATE
```

rather than allowing:

```text
FAST DEVELOPMENT
       ↓
MANY PARALLEL EXPERIMENTS
       ↓
ARCHITECTURAL DRIFT
       ↓
MASSIVE CLEANUP
       ↓
HIGH-RISK MIGRATION
```

The objective is not to slow LightSpeed down.

It is to make **fast development sustainable**.

---

# 26. GOLDEN RULE

> **Every meaningful change must have a known owner, a known purpose, a known validation method, and a known recovery point.**

If any one of those four is missing:

```text
STOP
CLARIFY
THEN PROCEED
```

This protocol exists to ensure that LightSpeed can remain aggressively iterative without allowing iteration to become permanent repository entropy.
