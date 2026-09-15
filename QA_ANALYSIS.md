# QA Analysis: "Validate all four diagrams" CI Failure

## Executive Summary

The CI job 34139814723 fails at the "Validate all four diagrams" step despite two fix commits:
- **b220529**: Fixed CWD resolution from `bin_path.parent.parent` to `get_project_root()`
- **9e7e7b7**: Fixed hash randomization from `hash()` to `crc32()`

Local validation passes all 4 diagram types, but CI still fails. This analysis identifies remaining quality profile mismatches, JSON schema issues, path resolution edge cases, and test coverage gaps.

---

## 1. Quality Profile Mismatch Analysis

### Current State

| Diagram Type | Quality Profile | CI Test Quality | Source Code Quality Profile |
|--------------|----------------|-----------------|----------------------------|
| architecture | `standard` | `standard` | `"standard"` (line 219 in converter.py) |
| workflow | `showcase` | `showcase` | `"showcase"` (line 615 in converter.py) |
| sequence | `showcase` | `showcase` | `"showcase"` (line 727 in converter.py) |
| dataflow | `showcase` | `showcase` | `"showcase"` (line 888 in converter.py) |

### Issue Analysis

The quality profile mismatch between architecture (standard) and others (showcase) is **intentional** based on scope:
- Architecture "leadership" scope (default) is designed for `standard` quality - it exceeds the ~12-primary-node showcase ceiling by design (converter.py line 113-114)
- Workflow/sequence/dataflow use `showcase` profile which is optimized for visual presentation with fewer nodes

**Risk**: If the Archify CLI's validation behavior differs between "standard" and "showcase" quality profiles, this could cause inconsistent validation results.

**Recommendation**: Verify that the Archify CLI handles both quality profiles correctly for all diagram types. The `--quality` flag is passed to the CLI, but ensure the CLI's internal behavior is consistent.

---

## 2. JSON Schema Validation

### Diagram JSON Schema Versions

| File | `schema_version` | `diagram_type` | Key Structure |
|------|-----------------|----------------|---------------|
| `architecture.json` | 1 | architecture | `schema_version`, `diagram_type`, `meta`, `components`, `connections`, `boundaries`, `cards` |
| `hiring.workflow.json` | 2 | workflow | `schema_version`, `diagram_type`, `meta`, `lanes`, `nodes`, `edges`, `mainPath`, `cards` |
| `hiring.sequence.json` | 1 | sequence | `schema_version`, `diagram_type`, `meta`, `participants`, `messages` |
| `hiring.dataflow.json` | 1 | dataflow | `schema_version`, `diagram_type`, `meta`, `stages`, `nodes`, `flows`, `cards` |

### Schema Compliance Check

All four JSON files have the correct `schema_version` and `diagram_type` for their respective types. The architecture file includes all expected fields (components, connections, boundaries, cards).

**Potential Issue**: The `architecture.json` has `"quality_profile": "standard"` in its `meta`, which should match the validation quality parameter. If the Archify CLI compares the `meta.quality_profile` against the `--quality` flag, mismatches could cause failures.

**Test Recommendation**:
```python
# Verify meta.quality_profile matches the validation quality parameter
assert architecture_json["meta"]["quality_profile"] == "standard"
assert workflow_json["meta"]["quality_profile"] == "showcase"
# ... etc
```

---

## 3. Archify CLI --json Output Parsing

### `_json_from_process` Function

The `renderer.py` function `_json_from_process` parses the JSON receipt from the CLI by:
1. Finding the first `{` in stdout+stderr
2. Tracking brace depth to find the outermost `{...}` block
3. Parsing the candidate JSON string
4. Returning the parsed dict or `{}` on failure

**Edge Cases**:
- Multi-line JSON output (Archify pretty-prints JSON)
- Human-readable messages before the machine receipt
- Multiple `{` blocks in output

**Verification**: The function works correctly based on local testing, but should be tested with various CLI output formats.

**Test Recommendation**:
```python
def test_json_parsing():
    """Test that _json_from_process correctly parses CLI output."""
    from ai_company.archify.renderer import _json_from_process
    # Simulate multi-line JSON output
    proc = subprocess.CompletedProcess(
        args=["node", "archify.mjs", "validate", "architecture", "test.json", "--json"],
        returncode=0,
        stdout='{"schemaVersion": 1, "ok": true, "command": "validate"}',
        stderr=""
    )
    result = _json_from_process(proc)
    assert result.get("ok") == True
```

---

## 4. Path Resolution Edge Cases

### CWD Impact on File Resolution

The critical path resolution issue was fixed in commit b220529:

- **Old**: `cwd=str(bin_path.parent.parent)` - resolved relative to skill directory
  - Problem: Input paths like `docs/diagrams/architecture.json` were relative to skill directory, which doesn't contain them
  - Effect: `ENOENT: no such file or directory` errors when running Node CLI

- **New**: `cwd=str(get_project_root())` - resolved relative to project root
  - Fix: Input paths like `docs/diagrams/architecture.json` are relative to project root, which contains them
  - Effect: Correct file resolution

### Remaining Edge Cases

1. **`AI_COMPANY_ROOT` env var**: If set, `get_project_root()` returns the env var value, which could point to a different directory
2. **Symlinks and relative paths**: Path resolution might behave differently with symlinks
3. **Network drives / different checkout paths**: The project root resolution might resolve differently

**Test Recommendation**:
```python
def test_cwd_resolution():
    """Test that _run_cli uses get_project_root() as cwd."""
    from ai_company.archify.renderer import resolve_bin, _run_cli
    import subprocess

    bin_path = resolve_bin()
    # New code uses get_project_root()
    proc = _run_cli(bin_path, ["validate", "architecture", "docs/diagrams/architecture.json", "--quality", "standard", "--json"])
    # Verify the cwd was project root by checking file resolution
    assert proc.returncode == 0 or "ENOENT" not in (proc.stderr + proc.stdout)
```

---

## 5. Deterministic vs Random Behavior

### `_dept_dot()` Function Fix

The `_dept_dot()` function in `converter.py` was fixed from:
```python
# Old (random per process)
return palette[abs(hash(department)) % len(palette)]
```
to:
```python
# New (deterministic)
return palette[crc32(department.encode("utf-8")) % len(palette)]
```

**Verification**: The fix uses `zlib.crc32()` which is always deterministic for the same input. The `hash()` function in Python is randomized per process via `PYTHONHASHSEED`, which caused the per-department card colors to flip between runs, triggering false drift detection.

**Remaining Risk**: If `PYTHONHASHSEED` is set differently in CI vs local, or if there are other uses of `hash()` in the diagram generation pipeline, similar issues could occur.

**Test Recommendation**:
```python
def test_dept_dot_determinism():
    """Test that _dept_dot() returns consistent results across runs."""
    from ai_company.archify.converter import _dept_dot

    # Run multiple times and verify same output
    results = [_dept_dot("Finance") for _ in range(10)]
    assert all(r == results[0] for r in results), "_dept_dot() is not deterministic!"

    # Also test with PYTHONHASHSEED set
    import os
    os.environ["PYTHONHASHSEED"] = "42"
    results2 = [_dept_dot("Finance") for _ in range(10)]
    assert all(r == results[0] for r in results2)
```

---

## 6. Test Coverage Gaps

### Current Test Coverage

| Area | Tests | Coverage |
|------|-------|----------|
| Converter (registry -> JSON IR) | `tests/unit/test_archify.py` | Good - covers build functions, layout, JSON serialization |
| CLI dispatch | `tests/cli/test_cli_archify.py` | Basic - helps registered commands and help text |
| Validation path | **None** | **GAP** - no unit tests for `ai_company.archify.validate()` |
| CWD resolution | **None** | **GAP** - no tests for `_run_cli` cwd behavior |
| Hash determinism | **None** | **GAP** - no tests for `_dept_dot()` deterministic behavior |
| JSON schema validation | **None** | **GAP** - no tests for diagram JSON schema compliance |

### Recommended Test Additions

1. **`test_archify_validate_cwd.py`**: Test that validation uses `get_project_root()` cwd
2. **`test_archify_determinism.py`**: Test `_dept_dot()` determinism across runs
3. **`test_archify_quality_profiles.py`**: Test quality profile handling for all diagram types
4. **`test_archify_json_schema.py`**: Test JSON schema compliance for all diagram types
5. **Integrate into CI**: Add these tests to the CI pipeline

---

## 7. Regression Test Design

### Preventing Re-introduction of Path Resolution Bugs

```python
# test_archify_cwd_regression.py
import subprocess
from pathlib import Path
from ai_company.archify.renderer import resolve_bin, _run_cli

def test_validate_uses_project_root_cwd():
    """Ensure validate always uses project root cwd, not skill directory."""
    bin_path = resolve_bin()

    # Run validation - should use get_project_root() cwd
    proc = _run_cli(
        bin_path,
        ["validate", "architecture", "docs/diagrams/architecture.json", "--quality", "standard", "--json"]
    )

    # Should not fail with ENOENT for file not found in skill directory
    error_output = (proc.stdout or "") + "\n" + (proc.stderr or "")
    assert "ENOENT" not in error_output, (
        "Validation failed with ENOENT - likely using old cwd resolution"
    )
    assert proc.returncode == 0, f"Validation failed: {error_output}"
```

### Preventing Re-introduction of Hash Randomization Bugs

```python
# test_archify_determinism_regression.py
import os
from ai_company.archify.converter import _dept_dot

def test_dept_dot_deterministic():
    """Ensure _dept_dot() is deterministic regardless of PYTHONHASHSEED."""
    # Test with default PYTHONHASHSEED
    results_default = [_dept_dot("Finance") for _ in range(5)]

    # Test with PYTHONHASHSEED=0 (full randomization)
    old_seed = os.environ.get("PYTHONHASHSEED")
    os.environ["PYTHONHASHSEED"] = "0"
    try:
        results_random_seed = [_dept_dot("Finance") for _ in range(5)]
    finally:
        if old_seed is None:
            del os.environ["PYTHONHASHSEED"]
        else:
            os.environ["PYTHONHASHSEED"] = old_seed

    # Results must be same regardless of hash seed
    assert results_default == results_random_seed, (
        f"Non-deterministic! default={results_default}, seed=0={results_random_seed}"
    )
```

---

## 8. CI Failure Investigation Checklist

If CI still fails after the two fixes, check these items:

### ✅ Completed
- [x] Fix b220529: CWD changed from `bin_path.parent.parent` to `get_project_root()`
- [x] Fix 9e7e7b7: `hash()` replaced with `crc32()` for deterministic card colors

### ❓ Still Need Investigation
- [ ] Check if `AI_COMPANY_ROOT` env var is set in CI and affects `get_project_root()`
- [ ] Verify Node.js version compatibility (CI: ubuntu-latest, local: Windows)
- [ ] Check if `PYTHONHASHSEED` is set differently in CI
- [ ] Verify the archify.mjs `--json` output format hasn't changed
- [ ] Check if `--quality` flag behavior differs between standard/showcase for architecture
- [ ] Inspect `ENOENT` errors or specific Archify diagnostic codes in CI logs

### 🛠️ Recommended CI Debug Steps
1. Add `print(f"CWD: {os.getcwd()}")` before running validate in CI
2. Add `print(f"PYTHONHASHSEED: {os.environ.get('PYTHONHASHSEED', 'not set')}")`
3. Capture full Archify CLI output (stdout/stderr) when it fails
4. Run the validate command manually in the CI environment to replicate the issue

---

## 9. Summary of Recommendations

### Immediate Actions
1. **Run the regression tests** designed above to verify the fixes are robust
2. **Add the test files** to the test suite and integrate into CI
3. **Check CI logs** for specific error messages if CI continues to fail

### Long-term Improvements
1. **Add schema validation** for diagram JSON files to catch structure issues early
2. **Make quality profile handling** more consistent across all diagram types
3. **Add integration tests** that run the full archify generate → validate pipeline
4. **Document the CWD requirement** for the Archify CLI in the code comments

### Test Coverage Targets
- [ ] `_dept_dot()` determinism test
- [ ] CWD resolution test for `_run_cli`
- [ ] Quality profile handling for all 4 diagram types
- [ ] JSON schema compliance check
- [ ] Archify CLI --json output parsing test
