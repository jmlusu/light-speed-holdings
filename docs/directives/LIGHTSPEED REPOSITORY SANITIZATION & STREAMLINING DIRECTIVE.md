# LIGHTSPEED REPOSITORY SANITIZATION & STREAMLINING DIRECTIVE

**Directive:** Repository Sanitation, Consolidation & Operational Hardening
**Objective:** Transform the current LightSpeed repository into a clean, coherent, maintainable, agent-friendly production repository.

---

## 1. EXECUTIVE MANDATE

The LightSpeed repository has evolved rapidly through a **ship-fast / fail-fast** development model.

That approach has produced useful velocity, but it has also created:

* duplicate implementations
* abandoned experiments
* obsolete files
* competing configuration
* overlapping documentation
* temporary scripts
* stale generated artifacts
* multiple versions of architectural concepts
* unclear ownership of functionality
* dead code
* inconsistent naming
* undocumented dependencies
* directories whose purpose is no longer obvious
* agent-generated artifacts that should not remain permanently
* potentially conflicting sources of truth

The objective of this directive is to perform a **controlled repository sanitation**, not a blind deletion exercise.

### Core principle

> **Do not preserve historical clutter merely because it exists. Preserve history in Git, not in the working tree.**

The repository should represent the **current canonical LightSpeed system**, not the entire history of how we arrived there.

---

# 2. NON-NEGOTIABLE SAFETY RULE

## DO NOT START BY DELETING FILES

The agents MUST first perform an inventory and produce a proposed cleanup plan.

No destructive cleanup should occur until the repository has been:

1. inventoried
2. classified
3. dependency-mapped
4. cross-referenced
5. compared against the current architecture
6. assigned a disposition

Every file must ultimately receive one of these classifications:

| Classification | Meaning                                      |
| -------------- | -------------------------------------------- |
| KEEP           | Canonical and actively required              |
| CONSOLIDATE    | Valid content exists but belongs elsewhere   |
| REFACTOR       | Required but structurally poor               |
| REPLACE        | Superseded by a better implementation        |
| ARCHIVE        | Historically useful but not part of runtime  |
| DELETE         | Obsolete, duplicate, generated, or abandoned |
| INVESTIGATE    | Cannot safely determine disposition          |

---

# 3. ESTABLISH THE CURRENT SOURCE OF TRUTH

Before changing anything, identify the authoritative versions of:

### Architecture

* overall LightSpeed architecture
* AI Company Builder architecture
* agent architecture
* orchestration
* memory
* runtime
* integrations
* application architecture
* frontend architecture
* backend architecture

### Product

* company positioning
* services
* sectors
* use cases
* thought leadership / Pharos
* website information architecture
* claims and metrics
* CTA strategy

### Brand

* logo
* visual identity
* colors
* typography
* design tokens
* imagery
* UI patterns

### Infrastructure

* deployment
* environment configuration
* local development
* remote runtime
* CI/CD
* observability
* secrets
* scheduled jobs

### AI

* model configuration
* providers
* local models
* OpenAI-compatible interfaces
* Ollama
* agent definitions
* orchestration
* memory
* retrieval
* embeddings

If multiple competing versions exist, **do not silently select one**.

Create a comparison and identify:

> CURRENT CANONICAL VERSION

---

# 4. CREATE A REPOSITORY BASELINE

Before cleanup, generate:

```text
/repo-audit/
    INVENTORY.md
    ARCHITECTURE_MAP.md
    DEPENDENCY_MAP.md
    DUPLICATES.md
    DEAD_CODE.md
    CONFIGURATION_AUDIT.md
    DOCUMENTATION_AUDIT.md
    GENERATED_FILES.md
    SECURITY_AUDIT.md
    NAMING_AUDIT.md
    CLEANUP_PLAN.md
    OPEN_QUESTIONS.md
```

This directory is temporary working material.

It should eventually either:

* be reduced to a small permanent architecture record, or
* be removed after the cleanup is complete.

---

# 5. COMPLETE FILE INVENTORY

Enumerate the entire repository.

For every file capture:

```text
path
extension
size
last modified
git tracked/untracked status
imported/referenced by
imports/references
runtime relevance
environment relevance
documentation relevance
generated/manual
duplicate candidate
disposition
```

Pay particular attention to:

```text
*.py
*.pyc
*.js
*.jsx
*.ts
*.tsx
*.json
*.yaml
*.yml
*.md
*.sh
*.ps1
*.bat
*.env*
Dockerfiles
package manifests
lockfiles
configuration files
scripts
tests
generated artifacts
build artifacts
cache directories
IDE configuration
agent artifacts
```

---

# 6. IDENTIFY GENERATED AND MACHINE-GENERATED CLUTTER

Locate and classify:

```text
__pycache__/
*.pyc
node_modules/
dist/
build/
.next/
.cache/
coverage/
*.log
temporary exports
AI-generated intermediate files
screenshots
debug dumps
test output
local databases
temporary JSON
temporary CSV
temporary Markdown
editor backups
```

Determine whether each is:

* correctly ignored
* incorrectly tracked
* required at runtime
* reproducible
* safe to remove

Anything reproducible should generally **not live in Git**.

---

# 7. FIND DUPLICATE IMPLEMENTATIONS

Search aggressively for multiple implementations of the same concept.

Examples:

```text
orchestrator
agent
memory
runtime
company builder
model provider
configuration
logging
authentication
API client
website content
brand configuration
design tokens
utilities
scripts
deployment
health checks
```

Look for:

```text
foo.py
foo_v2.py
foo_new.py
foo_old.py
foo_backup.py
foo-final.py
foo-final2.py
foo_latest.py
foo_temp.py
```

Also identify less obvious duplicates:

```text
src/...
app/...
lib/...
services/...
core/...
utils/...
```

where two directories implement overlapping functionality.

---

# 8. APPLY THE "ONE RESPONSIBILITY / ONE HOME" RULE

Every major capability must have one obvious canonical home.

For example:

```text
agents/
    agent definitions

orchestration/
    routing and coordination

memory/
    persistent memory

runtime/
    execution environment

models/
    model/provider abstraction

tools/
    reusable tools

config/
    configuration

scripts/
    operational scripts

tests/
    automated tests

docs/
    human-facing documentation
```

Do not blindly use these names if the existing architecture has better names.

The principle matters more than the exact directory names.

---

# 9. CONSOLIDATE CONFIGURATION

Configuration sprawl is particularly dangerous for agentic systems.

Find all:

```text
.env
.env.local
.env.example
config.py
settings.py
settings.json
config.json
yaml configuration
agent configuration
model configuration
provider configuration
deployment configuration
```

Determine:

### What is canonical?

### What is environment-specific?

### What is secret?

### What is default configuration?

### What is obsolete?

Establish a clear model such as:

```text
.env.example
.env.local
config/
    defaults
    development
    production
```

The exact structure may differ.

The important requirement is:

> An agent must not have to guess which configuration file controls a behavior.

---

# 10. CONSOLIDATE DOCUMENTATION

Documentation is currently likely to contain historical instructions that contradict newer decisions.

Classify every major Markdown/documentation file:

```text
CURRENT
HISTORICAL
IMPLEMENTATION
ARCHITECTURE
OPERATIONS
REFERENCE
TEMPORARY
OBSOLETE
```

Eliminate competing instructions.

There should be one obvious entry point:

```text
README.md
```

Then a small number of authoritative documents, for example:

```text
docs/
    ARCHITECTURE.md
    DEVELOPMENT.md
    DEPLOYMENT.md
    AGENTS.md
    OPERATIONS.md
    SECURITY.md
    CONTRIBUTING.md
```

Do not create documentation merely to satisfy the appearance of organization.

Prefer fewer authoritative documents.

---

# 11. ESTABLISH A "CURRENT STATE" ARCHITECTURE DOCUMENT

Create or update:

```text
docs/ARCHITECTURE.md
```

It must describe the architecture **as it actually exists**, not the architecture we hope to build.

It should cover:

```text
Human
  ↓
CEO Control Plane
  ↓
Orchestration
  ↓
Agents
  ↓
Tools / Models / Data
  ↓
Memory
  ↓
Runtime / Infrastructure
```

Include:

* major components
* responsibilities
* interfaces
* dependencies
* data flow
* control flow
* persistence
* model routing
* local vs remote execution
* external integrations
* deployment model

If something is planned but not implemented, label it:

```text
PLANNED
```

Never represent planned functionality as implemented functionality.

---

# 12. APPLY THE LIGHTSPEED 90-AGENT MODEL CONSISTENTLY

Audit all references to:

```text
90 agents
89 agents
90 including CEO agent
old 144-agent architecture
old 152-agent architecture
127-agent architecture
```

There must be one canonical explanation.

The current model should explicitly distinguish:

```text
90 total agentic units
    ├── 1 Human-CEO agent / CEO control representation
    └── 89 specialized agents
```

OR whatever the final authoritative implementation determines.

Do not allow conflicting counts to survive across:

* code
* README
* architecture documents
* website
* diagrams
* configuration
* tests
* prompts

---

# 13. AUDIT THE AI COMPANY BUILDER

Treat the AI Company Builder as a first-class subsystem.

Identify:

```text
entry point
orchestrator
agent registry
agent definitions
routing
memory
tools
model selection
execution
logging
persistence
failure handling
human approval
```

There must be one clear execution path.

Avoid:

```text
old orchestrator
new orchestrator
experimental orchestrator
legacy orchestrator
AI Studio orchestrator
OpenCode orchestrator
```

unless each has an explicitly documented purpose.

---

# 14. AUDIT LIGHTSPEED MEMORY

The memory subsystem must have a clear boundary.

Identify the canonical implementation of:

```text
memory.db
FTS5
audit.db
hash chain
redaction
integrity validation
embeddings
vector search
Ollama integration
memory APIs
```

Remove abandoned memory implementations.

The repository must clearly distinguish:

```text
persistent memory
working memory
cache
logs
audit records
vector index
```

Do not allow these concepts to become interchangeable.

---

# 15. AUDIT MODEL PROVIDERS

Create one canonical model abstraction.

Agents should not independently implement provider logic everywhere.

Look for duplicated provider handling across:

```text
OpenAI
Google
Ollama
DeepSeek
Moonshot
xAI
OpenCode
OmniRoute
local GGUF models
```

Centralize model/provider configuration where practical.

Agents should request capabilities rather than hard-code provider details wherever possible.

For example:

```text
"coding"
"reasoning"
"embedding"
"fast"
"vision"
```

rather than scattering provider-specific assumptions throughout the codebase.

---

# 16. SEPARATE PRODUCT CODE FROM DEVELOPMENT EXPERIMENTS

Create a clear distinction between:

```text
production
experimental
research
scratch
```

Do not allow experimental code to remain indistinguishable from production code.

If an experiment is worth preserving:

```text
experiments/
```

If it is no longer useful:

**delete it.**

Git already preserves its history.

---

# 17. CLEAN SCRIPTS

Inventory every script.

For every script ask:

1. What does this do?
2. Is it still used?
3. Is there another script doing the same thing?
4. Is it documented?
5. Can it be replaced by a package command?
6. Is it safe?
7. Is it platform-specific?
8. Does it modify production state?

Consolidate into something like:

```text
scripts/
    dev/
    build/
    test/
    deploy/
    maintenance/
    research/
```

Avoid dozens of one-off scripts at repository root.

---

# 18. ROOT DIRECTORY RULE

The repository root should be intentionally sparse.

The root should contain only files that are genuinely repository-level.

Examples:

```text
README.md
LICENSE
.gitignore
package.json
pyproject.toml
docker-compose.yml
Dockerfile
tsconfig.json
...
```

Do not allow the root to become a dumping ground for:

```text
notes
screenshots
temporary prompts
test output
agent reports
experiments
exports
one-off scripts
debug files
```

---

# 19. FIX .GITIGNORE

Audit `.gitignore`.

Ensure it covers all reproducible local artifacts.

But do NOT use `.gitignore` to hide architectural problems.

Bad:

```text
ignore entire source directory because it currently causes problems
```

Good:

```text
ignore generated artifacts
ignore secrets
ignore machine-specific files
ignore caches
ignore build output
```

Every ignored directory should have an intentional reason.

Pay particular attention to previously ignored source paths such as:

```text
src/ai_company/orchestrator/
```

Verify that important source code is not accidentally invisible to Git.

---

# 20. SECURITY SANITIZATION

Search the repository for:

```text
API keys
tokens
passwords
private keys
credentials
connection strings
JWT secrets
cloud credentials
hard-coded URLs containing secrets
personal information
```

Use pattern scanning plus manual inspection.

If secrets have ever been committed:

1. identify them
2. remove them from current files
3. determine whether Git history requires credential rotation
4. rotate credentials where appropriate

Do not merely rename the variable.

---

# 21. DEPENDENCY SANITIZATION

Audit:

```text
package.json
package-lock.json
requirements.txt
pyproject.toml
uv.lock
poetry.lock
Docker dependencies
```

Identify:

* unused dependencies
* duplicated libraries
* conflicting versions
* abandoned frameworks
* unnecessary heavy dependencies
* development dependencies accidentally required in production

For each dependency:

```text
USED
TRANSITIVE
DEVELOPMENT
OPTIONAL
UNUSED
UNKNOWN
```

Remove unused dependencies only after confirming they are not dynamically imported.

---

# 22. FRONTEND SANITIZATION

Audit:

```text
components
pages
routes
hooks
utilities
assets
styles
design tokens
icons
logos
images
```

Find:

```text
duplicate components
old components
unused components
unused pages
duplicate logo implementations
duplicate theme implementations
old design systems
hard-coded colors
hard-coded spacing
unused CSS
```

Establish the current LightSpeed design system as the source of truth.

The new logo and brand system must not coexist with abandoned visual systems unless explicitly required.

---

# 23. BRAND SYSTEM SANITIZATION

Identify the canonical sources for:

```text
logo
brand colors
typography
spacing
shadows
radius
motion
light theme
dark theme
design tokens
imagery
icons
```

Prefer:

```text
brand/tokens
```

or the existing authoritative structure.

Do not permit:

```text
#070A40
```

to be independently repeated hundreds of times if it should be a token.

The same applies to:

```text
#E63946
#00BFFF
#F2F2F2
...
```

---

# 24. TEST SANITIZATION

Determine:

```text
unit tests
integration tests
end-to-end tests
smoke tests
architecture tests
security tests
memory tests
agent tests
runtime tests
```

Remove:

* obsolete tests
* duplicate tests
* tests for deleted behavior

But do not delete failing tests merely because they fail.

Classify failures:

```text
EXPECTED BEHAVIOR CHANGE
BUG
STALE TEST
ENVIRONMENT FAILURE
MISSING DEPENDENCY
ARCHITECTURAL FAILURE
```

The final repository should have a **small, meaningful, high-signal test suite**.

---

# 25. STATIC ANALYSIS

Run appropriate tools for the actual stack.

Examples:

```text
lint
type checking
format checking
dependency checking
dead-code analysis
security scanning
test suite
build
production build
```

Do not add tooling merely for the sake of tooling.

The objective is:

> Fast feedback with high signal.

---

# 26. BUILD A REPOSITORY HEALTH CHECK

Create one canonical command.

For example:

```text
npm run health
```

or:

```text
python scripts/health_check.py
```

or an equivalent repository-native mechanism.

It should validate:

```text
structure
dependencies
configuration
types
lint
tests
build
security
generated artifacts
Git status
```

Output should clearly indicate:

```text
PASS
WARN
FAIL
```

---

# 27. CREATE AN AGENT-SAFE OPERATING MODEL

Because LightSpeed is itself an agentic development environment, the repository must be optimized for agents.

Agents should be able to answer quickly:

```text
Where is the source of truth?
Where does this feature live?
What owns this interface?
What should I modify?
What must I not modify?
How do I test it?
How do I build it?
What architecture rules apply?
```

Create:

```text
AGENTS.md
```

or the repository's equivalent.

It should define:

### Before changing code

```text
READ README
READ ARCHITECTURE
IDENTIFY OWNER
SEARCH FOR EXISTING IMPLEMENTATION
DO NOT CREATE DUPLICATES
```

### Before creating a file

```text
SEARCH FIRST
CHECK WHETHER EXISTING CODE CAN BE EXTENDED
CHECK CANONICAL DIRECTORY
CHECK NAMING CONVENTION
```

### Before deleting

```text
CHECK REFERENCES
CHECK DYNAMIC IMPORTS
CHECK BUILD
CHECK TESTS
CHECK DOCUMENTATION
```

---

# 28. INTRODUCE A "NO DUPLICATE BY DEFAULT" RULE

Agents MUST NOT create:

```text
*_new
*_v2
*_final
*_latest
*_backup
*_old
```

as a normal development pattern.

Instead:

```text
modify canonical implementation
```

If a replacement is necessary:

```text
create new implementation
migrate references
validate
delete old implementation
```

within the same controlled change.

---

# 29. INTRODUCE A "SEARCH BEFORE BUILD" RULE

Before creating any new:

```text
component
service
utility
agent
script
configuration
API
model adapter
memory interface
documentation
```

the agent must search the repository for an existing equivalent.

This should become a mandatory agent behavior.

---

# 30. CREATE A CANONICAL REPOSITORY MAP

The final README should include a compact map similar to:

```text
LightSpeed
│
├── src/
│   ├── agents/
│   ├── orchestration/
│   ├── memory/
│   ├── models/
│   ├── tools/
│   └── ...
│
├── app/
│
├── scripts/
│
├── tests/
│
├── docs/
│
├── brand/
│
└── infrastructure/
```

Use the actual architecture discovered during the audit.

The README should explain what belongs where.

---

# 31. GIT HYGIENE

Inspect:

```text
git status
git log
git branches
git tags
```

Identify:

* stale branches
* accidental generated files
* large binaries
* duplicated assets
* suspicious commits
* unfinished migrations

Do not rewrite Git history unless explicitly authorized.

Git history is the safety net.

The working tree is the product.

---

# 32. LARGE FILE AUDIT

Find unusually large files.

Classify:

```text
required binary
model
dataset
asset
generated artifact
accidental artifact
```

Do not allow:

```text
models
datasets
temporary archives
build output
logs
```

to silently inflate the repository.

If large models are needed locally, establish the correct local model strategy rather than casually committing them.

---

# 33. OPEN-SOURCE / OPEN-WEIGHT MODEL POLICY

Because LightSpeed is designed for African operating economics, model infrastructure must remain cost-conscious.

Document the intended hierarchy:

```text
FREE / LOCAL / OPEN-WEIGHT
        ↓
LOW-COST HOSTED
        ↓
PREMIUM HOSTED
```

Do not accidentally introduce a paid proprietary dependency when a suitable local/open model can perform the task.

The repository should make provider substitution possible.

---

# 34. REMOVE HISTORICAL ARCHITECTURE FROM ACTIVE CODE

Old architecture documents may remain useful for historical context, but they must not remain mixed with current implementation guidance.

Use:

```text
docs/archive/
```

for genuinely useful historical documents.

Otherwise delete them.

Remember:

> Git history is already an archive.

---

# 35. FINAL DIRECTORY STANDARD

After cleanup, the final structure should be intentional.

Do NOT force an arbitrary structure.

The agents must derive the final structure from the actual system.

However, conceptually it should resemble:

```text
/
├── README.md
├── AGENTS.md
├── LICENSE
├── package.json / pyproject.toml
├── .gitignore
│
├── src/
│   ├── agents/
│   ├── orchestration/
│   ├── memory/
│   ├── models/
│   ├── tools/
│   └── core/
│
├── app/
│
├── tests/
│
├── scripts/
│
├── docs/
│
├── brand/
│
└── infrastructure/
```

Only retain directories that are justified by the actual architecture.

---

# 36. VALIDATION GATE

The cleanup is NOT complete until all of the following pass.

## Architecture

* [ ] One canonical architecture
* [ ] No contradictory architecture documents
* [ ] One clear AI Company Builder execution path
* [ ] Agent model is consistently represented
* [ ] Memory architecture is clear
* [ ] Runtime architecture is clear

## Code

* [ ] No abandoned duplicate implementations
* [ ] No obvious dead code
* [ ] No unnecessary `*_old`, `*_new`, `*_v2` files
* [ ] No accidental generated artifacts
* [ ] No unexplained source directories

## Configuration

* [ ] Configuration has a clear source of truth
* [ ] Secrets are externalized
* [ ] Environment differences are documented
* [ ] No conflicting configuration systems

## Dependencies

* [ ] Unused dependencies removed
* [ ] Duplicate libraries evaluated
* [ ] Lockfiles consistent
* [ ] Production dependencies understood

## Documentation

* [ ] README is accurate
* [ ] Architecture documentation is accurate
* [ ] Agent instructions are current
* [ ] Historical documents are separated

## Frontend

* [ ] One design system
* [ ] One logo system
* [ ] One token system
* [ ] No obsolete components
* [ ] No unnecessary duplicated assets

## Security

* [ ] No active credentials committed
* [ ] Secrets scanned
* [ ] `.gitignore` reviewed
* [ ] Sensitive artifacts removed

## Runtime

* [ ] Build succeeds
* [ ] Tests succeed
* [ ] Health check succeeds
* [ ] Deployment configuration remains valid

---

# 37. REQUIRED FINAL REPORT

After cleanup, produce:

```text
docs/REPOSITORY_HEALTH.md
```

containing:

## Repository Health

```text
Status: HEALTHY / WARNING / BLOCKED
```

## Before

```text
Files:
Directories:
Duplicate implementations:
Dead code candidates:
Generated artifacts:
Documentation conflicts:
Configuration conflicts:
Dependencies:
Security findings:
```

## After

```text
Files:
Directories:
Deleted:
Consolidated:
Moved:
Refactored:
Archived:
Dependencies removed:
Tests added/fixed:
```

## Remaining Technical Debt

List only genuine remaining issues.

Each item must contain:

```text
Issue
Impact
Reason it remains
Recommended next action
```

---

# 38. FINAL PRINCIPLE

LightSpeed should be able to evolve quickly **without accumulating equal amounts of structural entropy**.

The desired development loop is:

```text
BUILD
  ↓
VALIDATE
  ↓
SHIP
  ↓
LEARN
  ↓
CONSOLIDATE
  ↓
RETURN TO BUILD
```

Not:

```text
BUILD
  ↓
FAIL
  ↓
PATCH
  ↓
COPY
  ↓
PATCH COPY
  ↓
CREATE V2
  ↓
CREATE V3
  ↓
DOCUMENT CONFUSION
  ↓
AGENT GETS LOST
```

The repository must become an environment where:

> **The fastest path is also the cleanest path.**

---

# 39. EXECUTION ORDER

Execute in these phases:

### PHASE 0 — FREEZE

Do not introduce unrelated features.

### PHASE 1 — INVENTORY

Understand everything.

### PHASE 2 — MAP

Establish architecture, dependencies and ownership.

### PHASE 3 — CLASSIFY

Assign every relevant artifact a disposition.

### PHASE 4 — CONSOLIDATE

Merge competing implementations.

### PHASE 5 — DELETE

Remove verified obsolete material.

### PHASE 6 — REFACTOR

Improve remaining architecture and naming.

### PHASE 7 — VALIDATE

Run tests, lint, type checks, builds and security scans.

### PHASE 8 — DOCUMENT

Update README, architecture and agent instructions.

### PHASE 9 — HEALTH CHECK

Create the repository health report.

### PHASE 10 — RETURN TO NORMAL DEVELOPMENT

Only after the repository reaches a clean baseline.

---

# 40. MOST IMPORTANT INSTRUCTION TO ALL AGENTS

**Do not optimize for the number of files deleted.**

Optimize for:

```text
clarity
coherence
single sources of truth
low cognitive load
low duplication
predictable architecture
fast agent comprehension
fast developer comprehension
reproducibility
security
testability
operational reliability
```

A smaller repository is good.

A **more understandable repository** is better.

A repository where a new LightSpeed agent can locate the correct implementation in seconds is the target.
