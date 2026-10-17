# Anti-Pattern: Unstable JSON Serialisation Comparison

## Symptom
ECL Harness Lint fails on CI while passing locally. The "expected" and "actual" dumps printed by the lint are visually identical, yet the check reports drift.

## Root Cause
`ConvertTo-Json -Depth 8 -Compress` output is **not stable across PowerShell versions**:
- Empty-array rendering differs between Windows PowerShell 5.1 and PowerShell 7.x
- Non-ASCII escaping differs between versions
- Number formatting differs between versions

Two content-identical indexes therefore serialise to different strings, and the string comparison (`-cne`) reports drift that does not exist semantically.

## Anti-Pattern Code
```powershell
# BAD: Compares serialised text, fails across PowerShell versions
ConvertTo-Json -Depth 8 -Compress $actual | -cne ConvertTo-Json -Depth 8 -Compress $expected

# CORRECT: Parse both sides into objects, sort, compare property-by-property
$canonical = { param([string]$S)
  if (-not $S -or $S -eq '""') { return @() }
  return ($S | ConvertFrom-Json | Sort-Object id)
}
$actualObj = & $canonical $actual
$expectedObj = & $canonical $expected
if ((Compare-Object $actualObj $expectedObj -Property id,title,status,location,modules,files,tags,decisions,validation_status,path,updated_at) -ne $null) {
  # real difference found
}
```

## Fix Pattern
1. **Parse both sides into JSON objects** using `ConvertFrom-Json`
2. **Sort both objects** by a deterministic key (`id`)
3. **Compare property-by-property** using `Compare-Object` with explicit `-Property` list
4. **Only real field differences** can now fail the check

## Reference Bugs
- BUG-84e037f13: INDEX.json lint compared JSON strings, so serialisation differences looked like drift
- BUG-93e21736a: INDEX.json regenerated in different order on every platform (combined fix with this pattern)

## Prevention
- Never compare serialised JSON text across PowerShell versions
- Always parse to objects first, sort deterministically, then compare semantically
- Use `ConvertFrom-Json | Sort-Object id` as the canonicalisation pipeline
- The rule of thumb: "JSON serialisation is an implementation detail of the runtime that produced it. Compare parsed structures, never the serialised text — especially across PowerShell editions."
