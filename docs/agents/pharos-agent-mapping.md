# Pharos Agent → Valid `subagent_type` Mapping

The Pharos department agents exist as OpenCode agent definitions in `.opencode/agents/`. They are **not** valid `subagent_type` values for the `task` tool (separate namespace per AGENTS.md:203).

Use these valid roster agents to delegate Pharos work:

| Pharos Agent (OpenCode) | Valid `subagent_type` | Best For |
|-------------------------|----------------------|----------|
| `thought-leadership-lead` | `content-writer` | Strategy, narrative architecture, content calendar |
| `agentic-research-lead` | `general` | Research, evidence synthesis, fact gathering |
| `thought-leadership-author` | `content-writer` | Long-form writing, manifestos, LinkedIn posts, white papers |
| `agentic-policy-analyst` | `general` | Policy analysis, regulatory mapping, consultation drafting |
| `speaker-engagement-lead` | `general` | Speaking programs, workshop design, keynote scripts |
| `community-ecosystem-builder` | `general` | Community building, stakeholder maps, partnerships |
| `media-pr-relations` | `content-writer` | Press materials, op-eds, media pitches, brand consistency |
| `talent-academy-lead` | `general` | Academy design, certification, university partnerships |

## Delegation Pattern

```python
# ❌ INVALID - Pharos names not in task roster
task(subagent_type="agentic-research-lead", ...)

# ✅ VALID - Use mapped roster agent
task(subagent_type="general", prompt="You are the Agentic Research Lead for Pharos. Research...", ...)
```

## Adding as Skills (Optional)

If Pharos agents should be invokable via the `skill` tool, create skill directories under `.agents/skills/` with `SKILL.md` files following the skill spec.

Example structure:
```
.agents/skills/
├── pharos-research-lead/
│   └── SKILL.md
├── pharos-thought-leadership-author/
│   └── SKILL.md
└── ...
```

Then they'd appear in `available_skills` and be loadable via `skill(name="pharos-research-lead")`.
