---
name: prompt-manager
description: Manages LightSpeed Holdings prompt compliance and format validation. Use when user asks "verify my prompt", "which prompt should I use", or "create a status prompt". Do NOT use for general prompt writing, MCP server development, or editing arbitrary markdown files.
---

# Prompt Manager

## Instructions
### Step 1: Identify Prompt Type
Determine which LightSpeed prompt category applies:
- **Status/Report** → CEO dashboard, executive update, cost/benefit risk
- **Audit/Lock** → Session audit, task lock, plan execution lock, master task lock
- **Task/Execution** → Task verification, debugging, repository changes
- **Miscellaneous** → Research lock, audit brief

Check the `C:\Users\jmlus\light-speed-holdings\prompts` folder for the 24 available prompt files and their categories.

### Step 2: Validate the Prompt
Run validation checks against the skill-creator spec:

1. Frontmatter has `---` delimiters and `name` + `description` fields
2. Description states **WHAT** the prompt does AND **WHEN** to use it (under 1024 characters)
3. No XML angle brackets (`< >`) in frontmatter
4. Prompt name (if applicable) is kebab-case and matches folder name
5. No `README.md` inside the prompt structure
6. Description includes trigger phrases ("use when", "use this", "use for", "trigger")
7. Folder name is lowercase with hyphens only (kebab-case)

### Step 3: Categorize and Report
Provide the user with:
- The matching prompt type from the LightSpeed folder
- Key requirements of that prompt type (status, progress, objectives, completed items, risks, next actions, CEO decision)
- Any out-of-scope considerations (unrelated work, optional improvements)
- Next steps for using the prompt or creating a new one

## Examples
- **User says** "verify my prompt": Analyzes a prompt file or user-provided prompt text → Reports PASS/FAIL with specific errors → Suggests fixes for any gaps
- **User says** "which prompt for task status": Returns the CEO dashboard prompt (`LIGHTSPEED_MAIN_CEO_DASHBOARD_PROMPT.md`) with requirements and structure overview
- **User says** "create a task verification prompt": Guides through required sections (task verification table, completion score, missed requirements, next action) → Validates output against the spec

## Troubleshooting
- **Skill doesn't load when it should**: Description too vague — add "Use when..." clause and specific trigger phrases ("verify my prompt", "which prompt should I use", "create a status prompt")
- **Validation fails**: Check for XML brackets in frontmatter, description length, kebab-case name format
- **Unexpected trigger**: Add negative triggers ("Do NOT use for general prompt writing or MCP server development") to narrow scope
- **Skill loads but instructions ignored**: Instructions too verbose or buried — keep concise, put critical rules at top under `## Important`, move detail to `references/`

## References
- `references/format-guide.md` — Prompt format reference and best practices
- `assets/prompt-template.md` — Blank prompt template for guided creation
- `scripts/validate_prompt.py` — Custom validation script for prompt compliance

### Step 4: Run Validation
Execute the bundled validator to check skill compliance:

```bash
python scripts/validate_prompt.py
```

It checks: folder naming, frontmatter format and length, forbidden content, missing linked files, and body size. Fix every ERROR; treat WARNINGS as review prompts. Expected output on success: `PASS` with 0 errors.

### Step 5: Test and Iterate
Iterate on a single challenging task (e.g., validating a complex prompt) until it succeeds, then extract the winning approach into the skill. Then cover:

1. **Triggering**: Obvious phrasing loads it, paraphrases load it, unrelated queries don't.
2. **Function**: Outputs correct compliance reports, tool calls succeed, edge cases handled.
3. **Baseline comparison**: Fewer corrections / tool calls / tokens than manually reading 24 prompt files.

Debugging trick: Ask the agent "When would you use the prompt-manager skill?" — it will paraphrase the description back; fix what's missing.

Full test-case templates and iteration signals are in `references/testing.md`.