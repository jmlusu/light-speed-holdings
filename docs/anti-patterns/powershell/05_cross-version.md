# Anti-Pattern: Cross-PowerShell-Version Incompatibility

## Symptom
Scripts that work on Windows PowerShell 5.1 fail on PowerShell 7.x (or vice versa) with errors like `ConvertTo-Json` producing different output, `Get-ChildItem` ordering differently, or backtick escaping behaving differently.

## Root Cause
PowerShell version drift across developer machines and CI environments:
- Windows PowerShell 5.1 (default on many Windows dev boxes)
- PowerShell 7.x (used on CI/Linux servers, also installed alongside 5.1 on Windows)
- Scripts written for one version often fail or produce different output on the other

The project's ECL lint (`scripts/maintenance/lint-ecl.ps1`) and all harness scripts must work identically on both PowerShell 5.1 and 7.x.

## Anti-Pattern Code
```powershell
# BAD: Assumes one PowerShell version's JSON behaviour
ConvertTo-Json -Depth 8 -Compress $data  # differs between v5.1 and v7.x

# BETTER: Use version-agnostic patterns
# - Parse then re-serialise with version-neutral settings
# - Or avoid ConvertTo-Json entirely; compare parsed objects instead

# CORRECT: Compare parsed structures, never serialised text
$canonical = { param([string]$S)
  if (-not $S -or $S -eq '""') { return @() }
  return ($S | ConvertFrom-Json | Sort-Object id)
}
$actualObj = & $canonical $actual
$expectedObj = & $canonical $expected
if ((Compare-Object $actualObj $expectedObj -Property id,title,status,...) -ne $null) {
  # real difference
}
```

## Fix Pattern
1. **Avoid `ConvertTo-Json -Compress` for comparison** — it's version-dependent
2. **Parse to objects first**: `ConvertFrom-Json` is relatively stable
3. **Sort by semantic key** before comparison: `Sort-Object id`
4. **Use `Compare-Object` on parsed objects** with explicit `-Property` list
4. **Test on both PowerShell versions** if the environment supports both

## Reference Bugs
- BUG-84e037f13: INDEX.json lint compared JSON strings across PowerShell versions
- BUG-93e21736a: INDEX.json ordering unstable across Windows PowerShell 5.1 vs 7.x

## Prevention
- Assume the script will run on both PowerShell 5.1 and 7.x
- Never rely on version-specific JSON behaviour (empty arrays, number formatting, escaping)
- Always parse JSON to objects before comparing: `ConvertFrom-Json | Sort-Object id`
- Use `Compare-Object` on parsed objects with explicit `-Property` list, not on serialised text
- Test lint/scripts on both PowerShell versions if available
- Document the PowerShell version requirement in script headers
