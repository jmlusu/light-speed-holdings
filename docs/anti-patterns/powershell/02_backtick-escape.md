# Anti-Pattern: Backtick Before $ in Here-Strings

## Symptom
Auto-generated bug records contain literal `${sha}` instead of the resolved commit hash. The `Commit` line reads `**Commit:** ${sha}` rather than the actual SHA value.

## Root Cause
Inside PowerShell double-quoted here-strings (`@"..."@`), variables were written with a leading backtick: `` `${sha}` ``. PowerShell treats the backtick before `$` as an **escape character**, which suppresses variable substitution. The `$` is emitted literally, so the text `${sha}` appears verbatim in the output.

Fields written without the backtick (`${Issue}`, `${date}`, `${state}`) expanded correctly, which is why some lines were right and others were not.

## Anti-Pattern Code
```powershell
# BAD: Backtick before $ suppresses substitution in here-strings
$md = @"
**Commit:** ${sha}   ← backtick suppresses $, emits literal "${sha}"
"@

# CORRECT: Write $var without leading backtick inside here-strings
$md = @"
**Commit:** $sha      ← expands to the actual SHA value
"@
```

## Fix Pattern
1. **Remove the backtick** so every variable (`$sha`, `$title`, `$body`, `$state`, `$subject`) expands normally inside the here-string
2. **Conventional-commit fallback**: Commits whose subject matches `^fix(\([^)]*\))?:` and reference no issue are captured under a record id derived from the 9-character short SHA

## Reference Bugs
- BUG-d75423bb7: Bug records wrote literal `${sha}` instead of the commit hash

## Prevention
- In PowerShell, a backtick before `$` suppresses substitution. Inside double-quoted here-strings, write `$var` (or `${var}`) **without** a leading backtick
- Never emit a template placeholder from a script that had the value available at render time
- Review all here-strings in `.ps1` files for ` ${` pattern (space before dollar sign is the giveaway)
