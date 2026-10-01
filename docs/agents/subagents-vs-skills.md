# Subagents vs. Skills: Canonical Namespaces

This file is the **single authoritative reference** for two distinct agent-dispatch
vocabularies that are frequently conflated. Mixing them up produced a real failure
(an attempt to launch `task` with `ecl-harness-engineer`, which is a *skill*, not a
*subagent* — the runtime rejected it with "Unknown agent type").

> **The one-line rule:** a *subagent* is a value passed to the `task` tool's
> `subagent_type`; a *skill* is a value passed to the `skill` tool's `name`, or a
> Markdown file under `.agents/skills/`. They are separate namespaces with separate
> allowed values. Never pass one namespace's value into the other namespace's tool.

---

## 1. `task` → `subagent_type` (subagents)

Only the values below are valid for the `task` tool's `subagent_type` parameter.
These are the **organization agent roster**. Anything not in this list is rejected
by the runtime (`Unknown agent type`).

Examples: `security-compliance-lead`, `platform-reliability-engineer`,
`platform-engineer`, `backend-engineer`, `fullstack-engineer`, `security-architect`,
`audit-trail-owner`, `dashboard-owner`, `qa-engineer`, `general`, `explore`, and any
other agent whose card defines a `mode: subagent` and a `subagent_type`.

**Source of truth:** the `task` tool's `subagent_type` enumeration in the agent's
system prompt (the "Available agent types" block). When in doubt, read that block —
never guess or derive the name from a path or a skill title.

## 2. `skill` → `name`, and `.agents/skills/` (skills)

Skills are loaded with the `skill` tool's `name` parameter, OR discovered as
Markdown skill files under `.agents/skills/*/SKILL.md` (and user-level skill dirs).
They provide **instructions and workflows**, not dispatachable agents.

Example: `ecl-harness-engineer` is a **skill** at
`.agents/skills/ecl-harness-engineer/SKILL.md` — it is NOT a `subagent_type`.

**Source of truth:** the `skill` tool's `name` enumeration (from the
`<available_skills>` block in the system prompt).

## 3. Why the conflation happens

| Signal that looks like an agent | Actually is...        |
| ------------------------------- | --------------------- |
| A `.agents/skills/<name>/SKILL.md` directory | A **skill** (instructions) |
| A `subagent_type` in the `task` tool spec  | A **subagent** (dispatchable) |
| A named role/title in `docs/agents/`        | Often a **skill** doc, not a `task` target |

A name can exist in BOTH namespaces, or only one. Presence in one is **no evidence**
the same name is valid in the other.

---

## 4. Recurrence-prevention measures

Apply these guardrails on **every** delegation:

1. **Validate before calling `task`.** Before invoking `task`, check the intended name
   against the canonical `subagent_type` list (the "Available agent types" block in the
   system prompt). If the name is not in that list: **do not call `task`** with it.

2. **Confuse-proof the fallback.** When a name is invalid as a `subagent_type`, pick a
   *different*, valid roster entry (e.g. `platform-engineer`, `backend-engineer`,
   `general`) OR do the work directly. Do **not** claim the original specialist was
   deployed, and do not silently map a skill name onto a subagent call.

3. **Never derive a `subagent_type` from a filesystem path or a skill title.** A
   `SKILL.md` path is the *skills* namespace, not the roster. If you found a name by
   globbing `.agents/skills/`, that is a skill — redirect to `skill` or re-check the
   roster, not to `task`.

4. **Report honestly.** In any handoff/summary, only state that a specialist subagent
   was deployed if a `task` call with that `subagent_type` actually returned. If you
   fell back to a generic agent or did it yourself, say so.

5. **Checklist before delegation:**
   - [ ] In `task`, is the value I'm passing a known `subagent_type`? (system prompt roster)
   - [ ] Did I accidentally copy a name from `.agents/skills/` or from a `skill` call?
   - [ ] If I'm invoking a workflow/instructions, am I using `skill`, not `task`?

6. **ADR / doc note:** this document is the canonical reference. If the roster or the
   skills set changes, update the relevant "Source of truth" lines here.

---

## 5. Where each "engineer" lives

A handy cross-check for the names that collide across namespaces (e.g. an
"ecl/security/platform" engineer that exists as a skill but not necessarily as a
subagent):

| Name                     | Skills (`skill`/`.agents/skills/`) | Subagent (`task` subagent_type) |
| ------------------------ | ---------------------------------- | ------------------------------- |
| `ecl-harness-engineer`   | YES (`.agents/skills/...`)         | NO (invalid)                    |
| `security-compliance-lead` | NO                                | YES                             |
| `platform-reliability-engineer` | NO                         | YES                             |
| `platform-engineer`      | NO                                 | YES                             |
| `security-architect`     | NO                                 | YES                             |

**If a row's `Subagent` column is NOT "YES", never pass that name to `task`.** Prefer a
name whose `Subagent` column is "YES", or do the work directly.
