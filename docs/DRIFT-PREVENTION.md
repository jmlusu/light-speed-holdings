# Documentation Drift Prevention — SOP

## Purpose

Prevent documentation from becoming stale when source files change. This SOP defines
the process, tooling, and ownership for keeping factual claims in docs accurate.

## Scope

This SOP covers all factual claims in active documentation (non-archived):
- Organizational counts (agents, departments, KPIs, templates, providers)
- Code patterns (path resolution, anti-patterns)
- Runtime requirements (Python version)

Excluded: archived docs (`docs/archive/`), ADRs (`docs/adr/`), CHANGELOG.md — these
record historical state and should not be updated.

## Source of Truth

| Claim | Source File | Owner | Validation |
|-------|-------------|-------|------------|
| Department count | `company-registry.yaml` | CEO / Chief of Staff | `validate-drift.ps1` |
| Agent count | `company-registry.yaml` | CEO / Chief of Staff | `validate-drift.ps1` |
| KPI count | `company/config/kpis.yaml` | Dashboard Owner | `validate-drift.ps1` |
| KPI department count | `company/config/kpis.yaml` | Dashboard Owner | `validate-drift.ps1` |
| Template count | `templates/**/*.j2` | Generator Owner | `validate-drift.ps1` |
| Provider count | `company/models.yaml` | LLM Platform Owner | `validate-drift.ps1` |
| Path pattern | `src/ai_company/paths.py` | Platform Engineer | `test_doc_drift.py` |
| Python version | `pyproject.toml` | DevOps Lead | `validate-drift.ps1` |

## Process

### When a Source File Changes

1. **Identify affected claims** — Check `docs/source-of-truth.yaml` for claims that reference the changed file
2. **Update dependent docs** — For each affected claim, update all docs listed in the `docs:` field
3. **Run validation** — `.\scripts\validate-drift.ps1` and `uv run pytest tests/docs/test_doc_drift.py -v`
4. **Commit together** — Source file and doc updates must be in the same commit

### Adding a New Claim

1. Add the claim to `docs/source-of-truth.yaml`
2. Include `source`, `current_value`, `pattern`, and `docs` fields
3. Run validation to verify it passes
4. No code changes needed — the validation scripts read the manifest dynamically

### Adding a New Doc

1. If the doc makes factual claims, identify which claims it references
2. Add the doc path to the `docs:` list of each relevant claim in `source-of-truth.yaml`
3. Run validation to verify it passes

## Validation Layers

| Layer | Speed | Scope | Command |
|-------|-------|-------|---------|
| Pre-commit | ~2s | All claims | `pre-commit run validate-drift --all-files` |
| pytest | ~10s | All claims + anti-patterns | `pytest tests/docs/test_doc_drift.py -v` |
| Manual | ~5s | All claims | `.\scripts\validate-drift.ps1` |

## Troubleshooting

### "Stale count in docs" error

The doc contains a number that doesn't match the source file. Find the stale reference and update it.

### "Anti-pattern detected" error

Code uses `Path(__file__).parent.parent` instead of `get_project_root()`. Replace with:
```python
from ai_company.paths import get_project_root
root = get_project_root()
```

### "Source file not found" error

The source file listed in the manifest doesn't exist. Either create the file or update the manifest.

### False positive on archived docs

Check that the doc path doesn't match `docs/archive/` or `docs/adr/`. If it does, the claim should have `archived_exempt: true` in the manifest.

## RACI Matrix

| Activity | R (Responsible) | A (Accountable) | C (Consulted) | I (Informed) |
|----------|-----------------|------------------|----------------|---------------|
| Update source files | Change author | Department head | — | — |
| Update dependent docs | Change author | Tech Doc Lead | Knowledge Manager | — |
| Run validation | Change author | QA Lead | — | — |
| Maintain manifest | Knowledge Manager | Chief of Staff | — | — |
| Maintain validation scripts | DevOps Lead | CTO | — | — |
| Audit quarterly | QA Lead | CTO | Knowledge Manager | CEO |

## Metrics

Track quarterly:
- Number of drift incidents caught by pre-commit hook
- Number of drift incidents caught in CI
- Time between source change and doc update (target: same commit)
- Number of claims in manifest (should grow as new sources are added)
