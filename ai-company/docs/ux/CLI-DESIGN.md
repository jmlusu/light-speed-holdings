# CLI UX Design

> Command naming conventions, output formatting, error handling, and help text standards.

---

## 1. Design Principles

| Principle | Description |
|-----------|-------------|
| **Predictable** | Same verb patterns across all subcommands |
| **Self-documenting** | `--help` answers 90% of questions |
| **Human-first** | Plain language, not machine jargon |
| **Color with meaning** | Consistent palette across all commands |
| **Fail loudly** | Errors always visible, never silent |

---

## 2. Command Naming Conventions

### Top-Level Structure

```
ai-company <domain> <action> [args] [options]
```

| Domain | Description | Example |
|--------|-------------|---------|
| `agents` | Agent management | `ai-company agents list` |
| `board` | Board governance | `ai-company board list` |
| `company` | Bootstrap & config | `ai-company company run` |
| `dashboard` | Web dashboard | `ai-company dashboard` |
| `decision` | Decision engine | `ai-company decision evaluate "..."` |
| `departments` | Department mgmt | `ai-company departments list` |
| `doctor` | System diagnostics | `ai-company doctor run` |
| `executor` | Task execution | `ai-company executor tick` |
| `graph` | Knowledge graphs | `ai-company graph list` |
| `hr` | HR operations | `ai-company hr list-agents` |
| `legal` | Legal operations | `ai-company legal list-contracts` |
| `marketing` | Marketing ops | `ai-company marketing list-campaigns` |
| `memory` | Memory engine | `ai-company memory list` |
| `orchestrator` | Coordination | `ai-company orchestrator tick` |
| `sales` | Sales operations | `ai-company sales list-leads` |
| `specialists` | Specialist agents | `ai-company specialists list` |
| `workflows` | Workflow mgmt | `ai-company workflows list` |

### Verb Conventions

| Verb | Meaning | Example |
|------|---------|---------|
| `list` | Show all items | `ai-company agents list` |
| `show` / `get` | Show one item | `ai-company agents show lead-engineer` |
| `create` / `add` | Create new item | `ai-company memory add ...` |
| `remove` / `delete` | Delete item | `ai-company orchestrator escalation remove <id>` |
| `run` | Execute an operation | `ai-company doctor run` |
| `tick` | Run one cycle | `ai-company orchestrator tick` |
| `start` | Start continuous loop | `ai-company executor start` |
| `status` | Show current state | `ai-company executor status` |
| `evaluate` | Assess something | `ai-company decision evaluate "..."` |
| `search` | Find by query | `ai-company memory search --query "..."` |

### Subcommand Groups

Multi-level subcommands use a consistent pattern:

```
ai-company <domain> <subgroup> <action>
```

Example:
```bash
ai-company orchestrator approval pending
ai-company orchestrator approval approve <id>
ai-company orchestrator escalation list
ai-company orchestrator postmortem create <id>
```

---

## 3. Output Formatting Standards

### 3.1 Table Output

Standard table format (used by `agents list`, `tasks`, `models`, etc.):

```
Role                                 Type          Department              Reports To
---------------------------------------------------------------------------------------------------
Chief of Staff                       Executive     operations              human-ceo
CTO                                  Executive     engineering             chief-of-staff
Lead Engineer                        Specialist    engineering             cto

Total: 27 agents
```

**Rules:**
- Column headers: Title Case, right-aligned for numbers, left-aligned for text
- Separator line: dashes, one per column width
- Trailing blank line after table
- Summary line at bottom: `Total: N items`

### 3.2 Key-Value Output

Used for single-item display (`show`, `get`):

```
Engineering — KPI Dashboard
============================================================

  Deployment Frequency
    Target:    10 per week
    Frequency: weekly
    ID:        eng-deploy-freq
    Desc:      Number of deployments per week

  Cycle Time
    Target:    2 days
    Frequency: weekly
    ID:        eng-cycle-time
```

**Rules:**
- Section header with underline
- Key labels: Right-aligned in fixed-width column
- Values: After label, left-aligned
- Blank line between items

### 3.3 Status Messages

Success, warning, and error output:

```
# Success
✓ Request apr-7b3e9f APPROVED by human-operator

# Warning
⚠ TIMEOUT — Tier 2 request apr-7b3e9f expired

# Error
✗ Request 'apr-999' not found or already processed

# Info
Starting CEO dashboard at http://127.0.0.1:8420
Press Ctrl+C to stop.
```

### 3.4 Panel Output

Used for health checks and diagnostics:

```
┌─────────────────────────────────────────────┐
│ Auto-Fix Results                            │
│                                             │
│ Fixed:                                      │
│   - Created .opencode/ directory            │
│   - Generated 27 agent files                │
│   - Created empty .opencode/inbox.json      │
└─────────────────────────────────────────────┘
```

---

## 4. Color Coding System

### Terminal Colors

All colors follow the [NO_COLOR](https://no-color.org/) convention — disabled when `NO_COLOR` env var is set.

| Color | Hex | Usage |
|-------|-----|-------|
| **Green** | `#22c55e` | Success, completed, approved, PASS |
| **Yellow/Amber** | `#f59e0b` | Warning, pending, timeout approaching |
| **Red** | `#ef4444` | Error, failed, rejected, escalation |
| **Cyan** | `#06b6d4` | Headers, labels, emphasis |
| **Blue** | `#3b82f6` | Info, links, agent names |
| **Purple** | `#a855f7` | Approval badges, premium tier |
| **Gray** | `#6b7280` | Muted text, timestamps |
| **White** | `#ffffff` | Normal body text |

### Status Color Mapping

| Status | Color | Symbol |
|--------|-------|--------|
| `pending` | Yellow | — |
| `in_progress` | Blue | — |
| `completed` | Green | ✓ |
| `failed` | Red | ✗ |
| `escalated` | Red | ⚠ |
| `approved` | Green | ✓ |
| `rejected` | Red | ✗ |
| `expired` | Yellow | ⏰ |
| `resolved` | Green | ✓ |

### Tier Badge Colors

| Tier | Color | Label |
|------|-------|-------|
| T0 (Auto) | Gray | `T0` |
| T1 (Notify) | Gray | `T1` |
| T2 (Single) | Blue | `T2` |
| T3 (Dual) | Amber | `T3` |
| T4 (CEO) | Red | `T4` |

### Priority Colors

| Priority | Color |
|----------|-------|
| `low` | Gray |
| `medium` | Blue |
| `high` | Amber |
| `critical` | Red |

---

## 5. Error Message Guidelines

### Error Format

```
✗ <Action failed>: <Specific reason>
  <What to do about it>
```

### Error Categories

| Category | Prefix | Example |
|----------|--------|---------|
| Not Found | `✗ Not found:` | `✗ Not found: Agent 'xyz' not in registry` |
| Permission | `✗ Denied:` | `✗ Denied: Tier 4 requires CEO-only approval` |
| Validation | `✗ Invalid:` | `✗ Invalid: Priority must be low/medium/high/critical` |
| State | `✗ Cannot:` | `✗ Cannot: Request already processed` |
| System | `✗ Error:` | `✗ Error: Failed to write to .opencode/inbox.json` |
| Timeout | `⚠ TIMEOUT —` | `⚠ TIMEOUT — Tier 2 request apr-xxx expired` |

### Error Recovery Hints

Every error should include a hint when possible:

```
✗ Registry not found. Run 'ai-company company run' first.

✗ ModuleNotFoundError: No module named 'ai_company'
  Run: pip install -e ".[dev]"

✗ Dashboard won't start on port 8420
  Check if another process is using it: netstat -ano | findstr 8420
  Or use a different port: ai-company dashboard --port 9000
```

---

## 6. Help Text Standards

### Top-Level Help

```
$ ai-company --help

 Usage: ai-company [OPTIONS] COMMAND [ARGS]...

 AI Company Builder - Orchestrate AI agent hierarchies

│ Domain          │ Description                          │
│─────────────────│──────────────────────────────────────│
│ agents          │ Manage AI agents                     │
│ board           │ Manage Board of Directors            │
│ company         │ Bootstrap and manage the AI company  │
│ dashboard       │ CEO dashboard                        │
│ decision        │ Decision engine                      │
│ departments     │ Manage departments                   │
│ doctor          │ Run system diagnostics               │
│ executor        │ Autonomous task execution            │
│ graph           │ Graph engine                         │
│ hr              │ Human Resources operations           │
│ legal           │ Legal operations                     │
│ marketing       │ Marketing operations                 │
│ memory          │ Manage company memory                │
│ orchestrator    │ Autonomous coordination              │
│ sales           │ Sales operations                     │
│ specialists     │ Manage specialist agents             │
│ workflows       │ Manage workflows                     │
│ sop             │ View Standard Operating Procedures   │
│ raci            │ View RACI matrices                   │
│ generate        │ Regenerate all company files         │
│ status          │ Show current company status          │

Run 'ai-company COMMAND --help' for more information.
```

### Subcommand Help

```
$ ai-company orchestrator --help

 Usage: ai-company orchestrator [OPTIONS] COMMAND [ARGS]...

 Autonomous coordination

│ Command     │ Description                                    │
│─────────────│────────────────────────────────────────────────│
│ tick        │ Run one orchestrator cycle                     │
│ briefing    │ Generate daily executive briefing              │
│ approval    │ Manage human-in-the-loop approval gates        │
│ escalation  │ Manage escalation rules and view escalations   │
│ postmortem  │ Manage incident postmortems                    │
│ scheduler   │ Manage recurring task schedules                │
```

### Argument Documentation

Arguments use angle brackets, options use dashes:

```
$ ai-company decision evaluate --help

 Usage: ai-company decision evaluate [OPTIONS] ACTION

 Evaluate an action through the approval matrix and risk assessment.

│ Argument │ Description                              │ Required │
│──────────│──────────────────────────────────────────│──────────│
│ ACTION   │ The action to evaluate (quoted string)   │ Yes      │
│          │                                          │          │
│ Options: │                                          │          │
│ --json   │ Output as JSON instead of formatted text │ No       │
```

---

## 7. Interactive Prompts

When user input is required:

```
$ ai-company orchestrator approval approve apr-7b3e9f

  Approve request apr-7b3e9f?
  Agent:   lead-backend
  Action:  edit routes.py
  Risk:    25/100

  Approved by: [human-operator]_
  Notes (optional): Looks good, tested locally_
```

**Rules:**
- Default values in brackets
- Required fields marked with `*`
- Confirmation prompt for destructive actions
- `--yes` / `-y` flag to skip confirmations in scripts

---

## 8. Progress Indicators

For long-running operations:

```
$ ai-company company run

  Bootstrapping AI Company...
  ✓ Created .opencode/ directory
  ✓ Generated 27 agent files
  ✓ Created config files
  ✓ Initialized task inbox
  
  Done! 27 agents ready.
```

For continuous operations:

```
$ ai-company executor start --poll-interval 5.0

  Starting executor loop (poll every 5s)...
  [14:30:01] Processing task a3f2c1 → lead-engineer
  [14:30:03] Task a3f2c1 completed
  [14:30:06] Processing task b7d4e2 → cfo
  [14:30:08] Task b7d4e2 escalated → cto
  ^C
  Executor stopped. Processed 2 tasks.
```

---

## 9. JSON Output Mode

All commands support `--json` for machine-readable output:

```bash
$ ai-company agents list --json

[
  {
    "id": "chief-of-staff",
    "name": "Chief of Staff",
    "role": "Executive",
    "type": "Executive",
    "department": "operations",
    "reportsTo": "human-ceo"
  },
  ...
]
```

---

## 10. Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NO_COLOR` | unset | Disable color output when set |
| `AI_COMPANY_CONFIG` | `config/` | Config directory path |
| `AI_COMPANY_OUTPUT` | `.opencode/` | Output directory |
| `DASHBOARD_PORT` | `8420` | Dashboard port |
| `DASHBOARD_HOST` | `127.0.0.1` | Dashboard host |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

---

## 11. Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | General error (not found, invalid input, etc.) |
| `2` | Usage error (bad arguments) |
| `3` | Permission denied |
| `4` | Timeout |

---

## 12. Alias Conventions

Common abbreviations are accepted:

| Short | Full | Example |
|-------|------|---------|
| `ls` | `list` | `ai-company agents ls` |
| `rm` | `remove` | `ai-company orchestrator escalation rm <id>` |
| `s` | `status` | `ai-company executor s` |
