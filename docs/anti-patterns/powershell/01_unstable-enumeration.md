# Anti-Pattern: Unstable Directory Enumeration Order

## Symptom
Generated manifest (INDEX.json) differs byte-for-byte across environments even when content is identical. CI reports "stale" file while local check passes.

## Root Cause
`Get-ChildItem` in PowerShell returns entries in directory-enumeration order, which is an implementation detail and **not stable across platforms**:
- Windows PowerShell 5.1 orders differently from PowerShell 7.x (Linux/macOS)
- Running `reindex` twice on the same machine can produce different orderings

The ECL lint then compares serialised JSON strings, which fail when entry order differs, even though the semantic content is identical.

## Anti-Pattern Code
```powershell
# BAD: Depends on filesystem enumeration order
Get-ChildItem -LiteralPath $base -Directory

# BETTER: Sort explicitly at generation time
Get-ChildItem -LiteralPath $base -Directory | Sort-Object -Property Name

# BEST: Sort by semantic key (id) and compare objects, not strings
$entries | Sort-Object id
```

## Fix Pattern
1. **At generation time**: Always sort entries by a deterministic key
   ```powershell
   $entries | Sort-Object id
   ```
2. **At comparison time**: Parse JSON into objects, sort, compare property-by-property
   ```powershell
   $actualObj = (& $canonical $actual) | Sort-Object id
   $expectedObj = (& $canonical $expected) | Sort-Object id
   Compare-Object $actualObj $expectedObj -Property id,title,status,...
   ```

## Reference Bugs
- BUG-93e21736a: INDEX.json regenerated in different order on every platform
- BUG-84e037f13: INDEX.json lint compared JSON strings, so serialisation differences looked like drift

## Prevention
- Never let a generated file's byte layout depend on filesystem enumeration order
- Sort explicitly at generation time *and* compare semantically, not as strings
- Use `Sort-Object id` (or equivalent semantic key) in all PowerShell generation scripts
