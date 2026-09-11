# Plan

## Technical Approach

Documentation reconciliation across two tracks running in parallel:
- **Track A (counts/versions)**: Update version references, test counts, agent counts, and CLI command counts in USER-GUIDE.md, DEVELOPER-GUIDE.md, API-REFERENCE.md, CHANGELOG.md, STATUS.md.
- **Track B (SOP/missing docs)**: Mark SOP v1 files as superseded; add documentation sections for OAuth2, ML module, Security module, and Governance CLI.

Files are independent (no merge conflicts) so tasks can run in parallel.

## Impacted Modules And Files

- `docs/CHANGELOG.md` — add 0.4.0 entry
- `docs/API-REFERENCE.md` — update version 0.1.0 → 0.4.0
- `docs/USER-GUIDE.md` — correct agent count 27 → 127
- `docs/DEVELOPER-GUIDE.md` — correct CLI count 24 → 30
- `docs/STATUS.md` — update GAP count 6 → 20, test count 1805 → 1856, add Historical Audits section
- `docs/sop-deployment.md` — mark `status: superseded`
- `docs/sop-incident-response.md` — mark `status: superseded`
- `docs/ORCHESTRATION-PLAN.md` — fix GAP-019 status in table

## Interfaces, Data, Permissions

No interface or data changes — documentation-only edits.

## Spec Gaps Found From Planning

- None.

## Risks And Mitigations

- **Risk**: Changing doc counts could introduce new inconsistencies if the audit report itself is stale.
- **Mitigation**: Cross-check every count against live source (`company-registry.yaml`, `main.py`, `pyproject.toml`, `pytest --collect-only`) before updating.

## Verification Plan

- `grep 'version = ' pyproject.toml` → 0.4.0
- `grep 'Version:' docs/API-REFERENCE.md` → 0.4.0
- `grep 'agents' docs/USER-GUIDE.md` → 127
- `grep -c 'commands' docs/DEVELOPER-GUIDE.md` → 30
- `grep '## \[0.4.0\]' docs/CHANGELOG.md` → exists
- `grep 'status: superseded' docs/sop-deployment.md docs/sop-incident-response.md` → both present
- `grep '20 of 20' docs/STATUS.md` → present
- `scripts/lint-ecl.ps1` → passes
- `uv run ruff check src/ tests/` → clean
- `uv run mypy src/` → clean
- `uv run pytest -q -m "not e2e"` → all pass
