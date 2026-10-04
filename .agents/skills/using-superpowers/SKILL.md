---
name: using-superpowers
description: Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## The Rule

**Invoke relevant or requested skills BEFORE any response or action** — including clarifying questions, exploring the codebase, or checking files. If it turns out wrong for the situation, you don't have to use it.

**Before entering plan mode:** if you haven't already brainstormed, invoke the brainstorming skill first.

Then announce "Using [skill] to [purpose]" and follow the skill exactly. If it has a checklist, create a todo per item.

## Skill Priority

When multiple skills apply, process skills come first — they set the approach, then implementation skills (frontend-design, etc.) carry it out. Brainstorming and systematic-debugging are Superpowers' most common process skills, but the rule holds for any of them.

- "Let's build X" → superpowers:brainstorming first, then implementation skills.
- "Fix this bug" → superpowers:systematic-debugging first, then domain skills.

## Red Flags

These thoughts mean STOP—you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "Let me gather information first" | Skills tell you HOW to gather information. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I know what that means" | Knowing the concept ≠ using the skill. Invoke it. |

## Platform Adaptation

If your harness appears here, read its reference file for special instructions:

- Claude Code: `references/claude-code-tools.md`
- Codex: `references/codex-tools.md`
- Pi: `references/pi-tools.md`
- Antigravity: `references/antigravity-tools.md`
- Hermes Agent: `references/hermes-tools.md`
- Muse: `references/muse-tools.md`

## PowerShell Anti-Pattern Review (Mandatory Before Touching .ps1 Files)

**Before responding to any task that involves modifying a PowerShell script (`*.ps1`), you MUST review the anti-pattern knowledge base:**

1. Read `docs/anti-patterns/powershell/` — all 5 files cover the canonical failure modes
2. **Specifically verify your changes do not contain:**
   - a) Backtick before `$` inside here-strings (`@"...`@`) — e.g. `` `${sha}` ``
   - b) `ConvertTo-Json -Compress` comparison without first parsing to objects and sorting by `id`
   - c) `Get-ChildItem` enumeration without explicit `Sort-Object id` or equivalent deterministic key
   - d) Assuming `ConvertTo-Json` output is stable across PowerShell 5.1 vs 7.x
3. Run the verification lint: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/lint-ecl.ps1`
4. If any of the above patterns are present in your changes, **stop and fix them before proceeding**

**Reference Bugs (for context):**
- BUG-93e21736a: Unstable directory enumeration order
- BUG-d75423bb7: Backtick before `$` in here-strings
- BUG-84e037f13: Unstable JSON serialisation comparison
- BUG-81c94142a: INDEX.json committed with untracked inputs
- BUG-ff0d33a7f: Canonical source drift / Verify path bug
- BUG-9d688faee: Hook timeout blocking stash restore

User instructions (CLAUDE.md, AGENTS.md, GEMINI.md, etc, direct requests) take precedence over skills, which in turn override default behavior. Only skip skill workflows or instructions when your human partner has explicitly told you to.
