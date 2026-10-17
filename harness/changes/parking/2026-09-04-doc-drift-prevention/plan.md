# Plan: Documentation Drift Prevention

## Architecture

```
Source Files (canonical)          Manifest                    Validation
─────────────────────            ────────                    ──────────
company/departments.yaml  ──►    source-of-truth.yaml  ──►   validate-drift.ps1
company-registry.yaml     ──►         │                ──►   test_doc_drift.py
ai_company/paths.py       ──►         │                ──►   pre-commit hook
                                      │
Docs (dependent)  ◄───────────────────┘
README.md, STATUS.md, USER-GUIDE.md, etc.
```

## Data Flow

1. Developer changes `company/departments.yaml` (e.g., adds a department)
2. Pre-commit hook runs `validate-drift.ps1`
3. Script reads `source-of-truth.yaml`, finds `department_count` claim
4. Script extracts current count from `company/departments.yaml`
5. Script greps all listed docs for the old count pattern
6. If stale count found → exit non-zero, commit blocked
7. Developer updates docs, re-commits, hook passes

## File Layout

```
docs/source-of-truth.yaml          # Manifest
scripts/validate-drift.ps1         # Validation script
tests/docs/test_doc_drift.py       # Pytest enforcement
.pre-commit-config.yaml            # Hook wiring
CONTRIBUTING.md                    # Ownership model
docs/DRIFT-PREVENTION.md           # SOP documentation
```
