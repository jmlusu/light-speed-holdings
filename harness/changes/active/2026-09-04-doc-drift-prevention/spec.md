# Spec: Documentation Drift Prevention System

## Problem

When upstream sources change (department count, agent count, file paths), downstream documents are not automatically updated. This caused:
- 31+ files referencing "7 departments" when the org has 20
- CLI commands failing because `Path(__file__)` resolution was wrong while `get_project_root()` existed as the canonical pattern

## Requirements

1. A YAML manifest mapping factual claims to their authoritative source files
2. A validation script that reads the manifest and checks all dependent docs
3. A pytest test that enforces the same checks in CI
4. A pre-commit hook that runs validation on every commit
5. Updated CONTRIBUTING.md with ownership model and drift prevention workflow

## Non-Requirements

- Auto-generating docs from source (narrative docs need human authoring)
- Checking archived/ADR docs (they record historical state)
- Real-time sync (weekly scan is sufficient for catch-all)

## Success Criteria

- `scripts/validate-drift.ps1` exits 0 when no drift, non-zero when drift detected
- `pytest tests/docs/test_doc_drift.py` passes
- Pre-commit hook blocks commits with stale claims
- CONTRIBUTING.md documents the ownership model
